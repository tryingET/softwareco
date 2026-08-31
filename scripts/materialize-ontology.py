#!/usr/bin/env python3
"""Atomically materialize only the Decision-144 ontology submodule."""
from __future__ import annotations
import argparse
import base64
import contextlib
import fcntl
import json
import os
import re
import secrets
import shutil
import signal
import stat
import subprocess
import sys
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse
SCHEMA = "softwareco.ontology-materialization/1"
APPROVED_SOURCE = "https://github.com/tryingET/softwareco-ontology.git"
OID = re.compile(r"[0-9a-f]{40}\Z")
PHASES = {"preparing", "prepared", "activating", "activated", "registering_url", "registering_active", "registered"}
JOURNAL_KEYS = set("schema repo ontology gitdir scratch oid source phase had_empty old_url old_active".split())
GIT_ENV_KEYS = set("""GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_ALLOW_PROTOCOL GIT_ASKPASS
GIT_CEILING_DIRECTORIES GIT_COMMON_DIR GIT_CONFIG GIT_CONFIG_COUNT GIT_CONFIG_GLOBAL
GIT_CONFIG_NOSYSTEM GIT_CONFIG_PARAMETERS GIT_CONFIG_SYSTEM GIT_DIR
GIT_DISCOVERY_ACROSS_FILESYSTEM GIT_EXEC_PATH GIT_EXTERNAL_DIFF GIT_GRAFT_FILE
GIT_IMPLICIT_WORK_TREE GIT_INDEX_FILE GIT_NAMESPACE GIT_NO_REPLACE_OBJECTS
GIT_OBJECT_DIRECTORY GIT_PREFIX GIT_PROTOCOL_FROM_USER GIT_PROXY_COMMAND
GIT_QUARANTINE_PATH GIT_REPLACE_REF_BASE GIT_SHALLOW_FILE GIT_SSH GIT_SSH_COMMAND
GIT_TEMPLATE_DIR GIT_WORK_TREE SSH_ASKPASS SSH_AUTH_SOCK""".split())
class MaterializationError(RuntimeError): pass
class MaterializationInterrupted(MaterializationError): pass
def _env() -> dict[str, str]:
    env = os.environ.copy()
    for key in tuple(env):
        if (key in GIT_ENV_KEYS or key.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))
                or key.lower().endswith("_proxy")):
            env.pop(key, None)
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    return env
def _run(argv: list[str], cwd: Path | None = None, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = _env(); env.update(extra_env or {})
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, env=env)
def _git(repo: Path, *args: str, check: bool = True, auth: dict[str, str] | None = None) -> str:
    cmd = ["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false", "-C", str(repo), *args]
    probe = _run(cmd, extra_env=auth)
    if check and probe.returncode:
        raise MaterializationError(f"git {' '.join(args)} failed: {(probe.stderr or probe.stdout).strip()}")
    return probe.stdout
def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0))
    try: os.fsync(fd)
    finally: os.close(fd)
def _fsync_file(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode): raise MaterializationError(f"not a regular file: {path}")
        os.fsync(fd)
    finally: os.close(fd)
@contextlib.contextmanager
def _lock(common: Path) -> Iterator[None]:
    path = common / "softwareco-ontology-materialization.lock"
    flags = os.O_RDWR | os.O_CREAT | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise MaterializationError("materialization lock must be one regular non-symlink file")
        try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc: raise MaterializationError("ontology materialization already in progress") from exc
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN); os.close(fd)
@contextlib.contextmanager
def _signals() -> Iterator[None]:
    prior: dict[int, object] = {}
    def stop(number: int, _frame: object) -> None: raise MaterializationInterrupted(f"interrupted by signal {number}")
    for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        prior[number] = signal.getsignal(number); signal.signal(number, stop)
    try: yield
    finally:
        for number, handler in prior.items(): signal.signal(number, handler)
@contextlib.contextmanager
def _block_signals() -> Iterator[None]:
    if not hasattr(signal, "pthread_sigmask"): yield; return
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM, signal.SIGHUP})
    try: yield
    finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous)
def _regular(path: Path, label: str) -> None:
    try: mode = path.lstat().st_mode
    except OSError as exc: raise MaterializationError(f"missing {label}: {path}") from exc
    if path.is_symlink() or not stat.S_ISREG(mode): raise MaterializationError(f"{label} must be regular and non-symlink")
def _empty_dir(path: Path) -> bool: return path.is_dir() and not any(path.iterdir())
def _common(repo: Path) -> Path:
    raw = Path(_git(repo, "rev-parse", "--git-common-dir").strip())
    return (raw if raw.is_absolute() else repo / raw).resolve()
def _config(repo: Path, file: Path, key: str) -> str:
    out = _run(["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false", "-C", str(repo),
                "config", "-f", str(file), "--get", key])
    if out.returncode or not out.stdout.strip(): raise MaterializationError(f".gitmodules lacks {key}")
    return out.stdout.strip()
def _index_entry(repo: Path, path: str, mode: str) -> str:
    rows = [x for x in _git(repo, "ls-files", "--stage", "--", path).splitlines() if x]
    if len(rows) != 1: raise MaterializationError(f"index must contain one {path} entry")
    meta, tab, actual = rows[0].partition("\t"); fields = meta.split()
    if not tab or actual != path or len(fields) != 3 or fields[0] != mode or fields[2] != "0":
        raise MaterializationError(f"index {path} must be stage-0 mode {mode}")
    return fields[1]
def _head_entry(repo: Path, path: str, mode: str) -> str:
    rows = [x for x in _git(repo, "ls-tree", "HEAD", "--", path).splitlines() if x]
    if len(rows) != 1: raise MaterializationError(f"HEAD must contain one {path} entry")
    meta, tab, actual = rows[0].partition("\t"); fields = meta.split()
    kind = "commit" if mode == "160000" else "blob"
    if not tab or actual != path or fields[:2] != [mode, kind] or len(fields) != 3:
        raise MaterializationError(f"HEAD {path} must be mode {mode} {kind}")
    return fields[2]
def _relation(repo: Path, oid: str, source: str) -> None:
    modules = repo / ".gitmodules"; _regular(modules, ".gitmodules")
    index_module = _index_entry(repo, ".gitmodules", "100644")
    if index_module != _head_entry(repo, ".gitmodules", "100644"):
        raise MaterializationError("indexed .gitmodules differs from HEAD")
    head_bytes = _git(repo, "show", "HEAD:.gitmodules").encode()
    if head_bytes != _git(repo, "show", ":.gitmodules").encode() or modules.read_bytes() != head_bytes:
        raise MaterializationError("worktree/index/HEAD .gitmodules bytes differ")
    if _config(repo, modules, "submodule.ontology.path") != "ontology":
        raise MaterializationError("ontology submodule path must be ontology")
    if _config(repo, modules, "submodule.ontology.url") != source:
        raise MaterializationError("source differs from tracked .gitmodules")
    if _config(repo, modules, "submodule.ontology.branch") != "main":
        raise MaterializationError("ontology submodule branch must be main")
    if _index_entry(repo, "ontology", "160000") != oid or _head_entry(repo, "ontology", "160000") != oid:
        raise MaterializationError("expected OID differs from HEAD/index gitlink")
def _source(source: str, allow_local: bool) -> None:
    if source == APPROVED_SOURCE: return
    if allow_local:
        path = Path(source)
        if path.is_absolute() and not path.is_symlink() and (not path.exists() or path.is_dir() or path.is_file()): return
    parsed = urlparse(source)
    if parsed.scheme or "::" in source or "\n" in source: raise MaterializationError("source protocol is not approved")
    raise MaterializationError("source must be the approved HTTPS owner remote")
def _auth(source: str, token_env: str | None, allow_local: bool) -> dict[str, str]:
    if allow_local and source != APPROVED_SOURCE: return {}
    if token_env != "SOFTWARECO_ONTOLOGY_TOKEN":
        raise MaterializationError("approved HTTPS source requires --token-env SOFTWARECO_ONTOLOGY_TOKEN")
    token = os.environ.get(token_env, "")
    if not token: raise MaterializationError("approved HTTPS source token is unavailable")
    encoded = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    return {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
            "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: basic {encoded}"}
def _git_values(repo: Path, key: str) -> list[str]:
    probe = _run(["git", "-C", str(repo), "config", "--local", "--get-all", key])
    return probe.stdout.splitlines() if probe.returncode == 0 else []
def _set_git_values(repo: Path, key: str, values: list[str]) -> None:
    _run(["git", "-C", str(repo), "config", "--local", "--unset-all", key])
    for value in values:
        probe = _run(["git", "-C", str(repo), "config", "--local", "--add", key, value])
        if probe.returncode: raise MaterializationError(f"unable to register {key}")
    _fsync_file(_common(repo) / "config"); _fsync_dir(_common(repo))
def _write_journal(path: Path, data: dict[str, object]) -> None:
    temp = path.with_name(path.name + ".new"); temp.unlink(missing_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(temp, flags, 0o600)
    try:
        payload = memoryview((json.dumps(data, sort_keys=True) + "\n").encode())
        while payload: payload = payload[os.write(fd, payload):]
        os.fsync(fd)
    finally: os.close(fd)
    os.replace(temp, path); _fsync_dir(path.parent)
def _phase(path: Path, data: dict[str, object], phase: str) -> None:
    data["phase"] = phase; _write_journal(path, data)
def _marker(marker: Path, gitdir: Path) -> bool:
    if marker.is_symlink() or not marker.is_file(): return False
    text = marker.read_text(); prefix = "gitdir: "
    if not text.startswith(prefix) or not text.endswith("\n") or "\n" in text[:-1]: return False
    target = Path(text[len(prefix):-1]); return (target if target.is_absolute() else marker.parent / target).resolve() == gitdir
def _recover(journal: Path, repo: Path, ontology: Path, gitdir: Path, oid: str, source: str) -> None:
    if not journal.exists(): return
    _regular(journal, "recovery journal")
    try: data = json.loads(journal.read_text())
    except json.JSONDecodeError as exc: raise MaterializationError("invalid recovery journal") from exc
    scratch = Path(str(data.get("scratch", ""))).resolve(); allowed = {Path(os.environ.get("TMPDIR", repo.parent)).resolve(), repo.parent.resolve()}
    old_url, old_active, had_empty = data.get("old_url"), data.get("old_active"), data.get("had_empty")
    typed_config = (isinstance(old_url, list) and all(isinstance(x, str) for x in old_url)
                    and isinstance(old_active, list) and all(isinstance(x, str) for x in old_active))
    if (set(data) != JOURNAL_KEYS or data.get("schema") != SCHEMA or data.get("repo") != str(repo)
            or data.get("ontology") != str(ontology) or data.get("gitdir") != str(gitdir)
            or data.get("oid") != oid or data.get("source") != source or data.get("phase") not in PHASES
            or not isinstance(had_empty, bool) or not typed_config or scratch.parent not in allowed
            or not scratch.name.startswith("softwareco-ontology-materialize.")):
        raise MaterializationError("recovery journal binding mismatch")
    current_url = _git_values(repo, "submodule.ontology.url"); current_active = _git_values(repo, "submodule.ontology.active")
    phase = data["phase"]
    if phase in {"preparing", "prepared", "activating", "activated"}:
        valid_transition = current_url == old_url and current_active == old_active
    elif phase == "registering_url":
        valid_transition = current_url in (old_url, [], [source]) and current_active == old_active
    elif phase == "registering_active":
        valid_transition = current_url == [source] and current_active in (old_active, [], ["true"])
    else:
        valid_transition = current_url == [source] and current_active == ["true"]
    if not valid_transition: raise MaterializationError("recovery journal parent-config transition mismatch")
    if ontology.exists():
        if had_empty and _empty_dir(ontology): pass
        elif _marker(ontology / ".git", gitdir): shutil.rmtree(ontology); _fsync_dir(ontology.parent)
        else: raise MaterializationError("recovery refuses unknown ontology path")
    if gitdir.exists():
        if gitdir.is_symlink() or not gitdir.is_dir(): raise MaterializationError("recovery refuses unknown gitdir")
        shutil.rmtree(gitdir); _fsync_dir(gitdir.parent)
    _set_git_values(repo, "submodule.ontology.url", old_url)
    _set_git_values(repo, "submodule.ontology.active", old_active)
    if had_empty and not ontology.exists(): ontology.mkdir(); _fsync_dir(ontology.parent)
    if scratch.exists(): shutil.rmtree(scratch); _fsync_dir(scratch.parent)
    journal.unlink(); _fsync_dir(journal.parent)
def _live(repo: Path, oid: str, auth: dict[str, str]) -> None:
    _git(repo, "fetch", "--quiet", "--no-tags", "origin", "main", auth=auth)
    probe = _run(["git", "-C", str(repo), "merge-base", "--is-ancestor", oid, "FETCH_HEAD"], extra_env=auth)
    if probe.returncode: raise MaterializationError("expected OID is not contained in live origin/main")
def _manifest(repo: Path) -> None: _regular(repo / "manifest.yaml", "ontology manifest")
def _existing(repo: Path, ontology: Path, gitdir: Path, oid: str, source: str, auth: dict[str, str]) -> dict[str, object] | None:
    marker = ontology / ".git"
    if not marker.exists() and not marker.is_symlink(): return None
    if not _marker(marker, gitdir) or not gitdir.is_dir() or gitdir.is_symlink():
        raise MaterializationError("ontology is not the registered parent submodule")
    worktree = _run(["git", "--git-dir", str(gitdir), "config", "--get", "core.worktree"])
    if worktree.returncode or Path(worktree.stdout.strip()).resolve() != ontology:
        raise MaterializationError("ontology core.worktree mismatch")
    if _git(repo, "config", "--local", "--get", "submodule.ontology.url").strip() != source:
        raise MaterializationError("parent submodule URL is not registered")
    if _git(repo, "config", "--local", "--get", "submodule.ontology.active").strip() != "true":
        raise MaterializationError("parent submodule active flag is not registered")
    if _git(ontology, "rev-parse", "HEAD").strip() != oid or _git(ontology, "status", "--porcelain", "--untracked-files=all").strip():
        raise MaterializationError("materialized ontology OID/status mismatch")
    if _git(ontology, "remote", "get-url", "origin").strip() != source: raise MaterializationError("ontology origin mismatch")
    _manifest(ontology); _live(ontology, oid, auth)
    status = _git(repo, "submodule", "status", "--", "ontology").rstrip("\n")
    if not status.startswith(" " + oid): raise MaterializationError("parent submodule status is not initialized")
    return {"outcome": "already_materialized", "oid": oid, "tree": _git(ontology, "rev-parse", f"{oid}^{{tree}}").strip(), "source": source}
def _activate(worktree: Path, prepared_gitdir: Path, ontology: Path, gitdir: Path) -> Path | None:
    backup = worktree.parent / "empty-ontology"; had_empty = ontology.exists(); moved_git = moved_tree = False
    try:
        with _block_signals():
            if had_empty:
                if not _empty_dir(ontology): raise MaterializationError("ontology destination is not empty")
                os.replace(ontology, backup); _fsync_dir(ontology.parent)
            os.replace(prepared_gitdir, gitdir); moved_git = True; _fsync_dir(gitdir.parent)
            os.replace(worktree, ontology); moved_tree = True; _fsync_dir(ontology.parent)
    except BaseException:
        if moved_tree and ontology.exists(): os.replace(ontology, worktree); _fsync_dir(ontology.parent)
        if moved_git and gitdir.exists(): os.replace(gitdir, prepared_gitdir); _fsync_dir(gitdir.parent)
        if had_empty and backup.exists(): os.replace(backup, ontology); _fsync_dir(ontology.parent)
        raise
    return backup if had_empty else None
def _scratch_root(repo: Path, common: Path) -> Path:
    configured = Path(os.environ.get("TMPDIR", repo.parent)).resolve()
    for root in (configured, repo.parent.resolve()):
        root.mkdir(parents=True, exist_ok=True)
        if not root.is_symlink() and root.stat().st_dev == repo.stat().st_dev == common.stat().st_dev: return root
    raise MaterializationError("no same-filesystem scratch root")
def _transaction(repo: Path, common: Path, ontology: Path, gitdir: Path, journal: Path, oid: str, source: str, auth: dict[str, str]) -> dict[str, object]:
    parent = _scratch_root(repo, common); scratch = parent / f"softwareco-ontology-materialize.{secrets.token_hex(8)}"
    old_url = _git_values(repo, "submodule.ontology.url"); old_active = _git_values(repo, "submodule.ontology.active")
    data: dict[str, object] = {"schema": SCHEMA, "repo": str(repo), "ontology": str(ontology), "gitdir": str(gitdir),
        "scratch": str(scratch), "oid": oid, "source": source, "phase": "preparing", "had_empty": ontology.exists(),
        "old_url": old_url, "old_active": old_active}
    try:
        _write_journal(journal, data)
        scratch.mkdir(); _fsync_dir(parent); template = scratch / "template"; template.mkdir()
        worktree = scratch / "worktree"; prepared_gitdir = scratch / "gitdir"
        clone = _run(["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false", "clone", "--quiet", "--no-checkout",
            "--no-hardlinks", "--template", str(template), "--separate-git-dir", str(prepared_gitdir), "--", source, str(worktree)], cwd=scratch, extra_env=auth)
        if clone.returncode: raise MaterializationError(f"source unavailable: {clone.stderr.strip()}")
        if _git(worktree, "remote", "get-url", "origin").strip() != source: raise MaterializationError("prepared source mismatch")
        _git(worktree, "cat-file", "-e", f"{oid}^{{commit}}"); _live(worktree, oid, auth)
        _git(worktree, "checkout", "--quiet", "--detach", oid); _manifest(worktree)
        if _git(worktree, "status", "--porcelain", "--untracked-files=all").strip(): raise MaterializationError("prepared worktree dirty")
        tree = _git(worktree, "rev-parse", f"{oid}^{{tree}}").strip(); marker = worktree / ".git"; _regular(marker, "prepared gitfile")
        marker.write_text(f"gitdir: {gitdir}\n"); bind = _run(["git", "--git-dir", str(prepared_gitdir), "config", "core.worktree", str(ontology)])
        if bind.returncode: raise MaterializationError("unable to bind prepared core.worktree")
        _phase(journal, data, "prepared"); _relation(repo, oid, source)
        modules = gitdir.parent; made_modules = not modules.exists(); modules.mkdir(parents=True, exist_ok=True)
        _phase(journal, data, "activating"); backup = _activate(worktree, prepared_gitdir, ontology, gitdir); _phase(journal, data, "activated")
        _phase(journal, data, "registering_url"); _set_git_values(repo, "submodule.ontology.url", [source])
        _phase(journal, data, "registering_active"); _set_git_values(repo, "submodule.ontology.active", ["true"])
        _phase(journal, data, "registered")
        if _existing(repo, ontology, gitdir, oid, source, auth) is None: raise MaterializationError("activated ontology missing")
        if backup and backup.exists(): backup.rmdir()
        shutil.rmtree(scratch); _fsync_dir(parent); journal.unlink(); _fsync_dir(common)
        if made_modules and not modules.exists(): raise MaterializationError("Git modules directory disappeared")
        return {"outcome": "materialized", "oid": oid, "tree": tree, "source": source}
    except BaseException as exc:
        try:
            if journal.exists(): _recover(journal, repo, ontology, gitdir, oid, source)
            else:
                journal.with_name(journal.name + ".new").unlink(missing_ok=True)
                if scratch.exists(): shutil.rmtree(scratch); _fsync_dir(parent)
        except BaseException as recovery: raise MaterializationError(f"recovery required: {recovery}") from exc
        raise
def materialize(repo_root: Path, oid: str, source: str, allow_local: bool = False, token_env: str | None = None) -> dict[str, object]:
    repo = repo_root.resolve()
    if repo_root.absolute() != repo or repo_root.is_symlink() or Path(_git(repo, "rev-parse", "--show-toplevel").strip()).resolve() != repo:
        raise MaterializationError("repo root must be the canonical Git worktree root")
    if not OID.fullmatch(oid): raise MaterializationError("expected OID must be 40 lowercase hex")
    _source(source, allow_local); auth = _auth(source, token_env, allow_local); _relation(repo, oid, source); common = _common(repo)
    ontology = repo / "ontology"; gitdir = common / "modules/ontology"; journal = common / "softwareco-ontology-materialization.json"
    if ontology.is_symlink() or journal.is_symlink(): raise MaterializationError("ontology/journal may not be symlink")
    with _lock(common), _signals():
        _relation(repo, oid, source); _recover(journal, repo, ontology, gitdir, oid, source)
        existing = _existing(repo, ontology, gitdir, oid, source, auth)
        if existing: return existing
        if ontology.exists() and not _empty_dir(ontology): raise MaterializationError("unmaterialized ontology contains files")
        if gitdir.exists() or gitdir.is_symlink(): raise MaterializationError("partial ontology Git metadata exists")
        return _transaction(repo, common, ontology, gitdir, journal, oid, source, auth)
def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--expected-oid", required=True); parser.add_argument("--source", required=True); parser.add_argument("--allow-local-source", action="store_true"); parser.add_argument("--token-env")
    return parser
def main() -> int:
    args = _parser().parse_args()
    try: result = materialize(args.repo_root, args.expected_oid, args.source, args.allow_local_source, args.token_env)
    except (MaterializationError, OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"schema": SCHEMA, "ok": False, "error": str(exc)}, sort_keys=True), file=sys.stderr); return 2
    print(json.dumps({"schema": SCHEMA, "ok": True, **result}, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
