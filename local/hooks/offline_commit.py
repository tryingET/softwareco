#!/usr/bin/env python3
"""AK7597: real UBS first, then explicit native checks of the exact index, offline."""
from pathlib import Path
import hashlib
import json
import os
import socket
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# Git selects the committing repository, worktree and index through these variables; any
# other GIT_* from the committer (GIT_CONFIG_COUNT/KEY/VALUE, GIT_CONFIG_PARAMETERS,
# GIT_EXEC_PATH, ...) could inject configuration such as a core.fsmonitor command.
GIT_LOCATION_ENV = {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE", "GIT_CEILING_DIRECTORIES",
                    "GIT_DISCOVERY_ACROSS_FILESYSTEM"}
# Every git call disables the filesystem monitor: its command would run inside index reads.
GIT = ["git", "--no-lazy-fetch", "-c", "core.fsmonitor=false"]


def origin_env():
    env = clean_env()
    env.update({k: v for k, v in os.environ.items() if k in GIT_LOCATION_ENV})
    # Global and system config are the committer's, not the repository's: they can define
    # hooks (hook.<name>.event = post-index-change fires on the private-index write-tree).
    # The repository's own config remains the declared trusted boundary.
    env.update(GIT_NO_REPLACE_OBJECTS="1", GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0",
               GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    return env


def git(root, *args, env=None):
    return subprocess.check_output([*GIT, "-C", str(root), *args],
                                   env=origin_env() if env is None else env).decode().strip()


# Only these inherited variables reach UBS and the native checks. Everything else from
# the committer's environment (UBS_*, BASH_ENV/ENV, PYTHON*, NODE_OPTIONS, LD_*, agent
# sockets, CI knobs, GIT_*) could weaken or redirect a check, so it is dropped. PATH is
# not inherited at all: main() pins it, because UBS resolves its language modules from
# PATH first and the runner itself resolves git and unshare (inspection F2).
SAFE_PATH = "/usr/bin:/bin"
ALLOWED_ENV = {"PATH", "HOME", "TMPDIR", "USER", "LOGNAME", "LANG", "LANGUAGE", "TERM", "TZ"}


def clean_env():
    env = {k: v for k, v in os.environ.items() if k in ALLOWED_ENV or k.startswith("LC_")}
    # Tighten-only knob: an operator may demand the whole-file UBS result, never relax it.
    if os.environ.get("UBS_STAGED_STRICT") == "1":
        env["UBS_STAGED_STRICT"] = "1"
    return env


def regular(path):
    path = Path(path)
    if path.is_symlink() or any(p.is_symlink() for p in path.parents) or not path.is_file():
        raise RuntimeError(f"required regular file missing or symlinked: {path}")
    return path


def capture_index(root, env):
    """write-tree may refresh index caches; operate on a private byte copy only."""
    scratch = os.environ.get("TMPDIR")
    if not scratch or not Path(scratch).is_dir():
        raise RuntimeError("TMPDIR must name an existing scratch directory")
    index = Path(git(root, "rev-parse", "--path-format=absolute", "--git-path", "index", env=env))
    if not index.is_absolute():
        index = root / index
    before = sha(regular(index))
    with tempfile.TemporaryDirectory(prefix="hook-index-copy-", dir=scratch) as work:
        private = Path(work) / "index"
        shutil.copyfile(index, private)
        if sha(private) != before or sha(index) != before:
            raise RuntimeError("index changed while copying candidate")
        tree = git(root, "write-tree", env=dict(env, GIT_INDEX_FILE=str(private)))
    return tree, before


def materialize(root, tree, snapshot, env):
    """Export literal blobs/modes, with no attributes, filters or export-ignore."""
    raw = subprocess.check_output([*GIT, "-C", str(root), "ls-tree", "-r", "-z", tree], env=env)
    with subprocess.Popen([*GIT, "-C", str(root), "cat-file", "--batch"], env=env,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
        for record in raw.split(b"\0"):
            if not record:
                continue
            fields, name = record.split(b"\t", 1)
            mode, kind, oid = fields.split()
            rel = Path(os.fsdecode(name))
            if rel.is_absolute() or any(p in (".", "..", ".git") for p in rel.parts):
                raise RuntimeError("unsafe candidate path")
            target = snapshot / rel
            if mode == b"160000":
                target.mkdir(parents=True, exist_ok=True)
                continue
            if kind != b"blob" or mode not in (b"100644", b"100755", b"120000"):
                raise RuntimeError("unsupported candidate object mode")
            process.stdin.write(oid + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().split()
            if len(header) != 3 or header[:2] != [oid, b"blob"]:
                raise RuntimeError("cannot read candidate blob")
            data = process.stdout.read(int(header[2]))
            if len(data) != int(header[2]) or process.stdout.read(1) != b"\n":
                raise RuntimeError("truncated candidate blob")
            target.parent.mkdir(parents=True, exist_ok=True)
            if mode == b"120000":
                target.symlink_to(os.fsdecode(data))
            else:
                target.write_bytes(data)
                target.chmod(0o755 if mode == b"100755" else 0o644)
        process.stdin.close()
        if process.wait():
            raise RuntimeError("candidate blob export failed")


def main(config):
    # Isolated mode ignores PYTHON* variables and keeps this directory off sys.path, so
    # neither can replace a module before the hash checks below. A stale entry hook
    # without -I is refused rather than run unisolated.
    if not sys.flags.isolated:
        raise RuntimeError("the offline hook must run under python3 -I; reinstall it with install_offline.py")
    os.environ["PATH"] = SAFE_PATH
    # Replacement refs would make cat-file report the indexed oid with other bytes (F6).
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    config = Path(config).resolve()
    meta = json.loads(regular(config).read_text())
    if meta["protocol"] != "softwareco-offline-index-v1":
        raise RuntimeError("unsupported installed hook protocol")
    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))
    common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    if common != Path(meta["common_dir"]):
        raise RuntimeError("installed hook belongs to a different repository")
    for path, expected in meta["source_hashes"].items():
        if sha(regular(path)) != expected:
            raise RuntimeError(f"qualified hook source drift: {path}")
    staged_wrapper = regular(HERE.parents[1] / "scripts/ubs-staged.sh")
    if str(staged_wrapper) != meta["ubs_staged"] or str(staged_wrapper) not in meta["source_hashes"]:
        raise RuntimeError("UBS wrapper must be the qualified shared source's fixed entrypoint")
    if sha(regular(meta["scanner"])) != meta["scanner_sha256"]:
        raise RuntimeError("qualified UBS executable changed; re-qualify before reinstall")
    # Never trust an environment boolean as evidence of isolation. Compare actual
    # network namespace identities across the re-exec; failure is a hard refusal.
    previous = os.environ.get("SOFTWARECO_HOOK_PARENT_NETNS")
    current = os.readlink("/proc/self/ns/net")
    if previous is None:
        env = dict(os.environ, SOFTWARECO_HOOK_PARENT_NETNS=current)
        os.execvpe("unshare", ["unshare", "--user", "--map-current-user", "--net", "--",
                              sys.executable, "-I", str(Path(__file__).resolve()), str(config)], env)
    if (not previous.startswith("net:[") or not previous.endswith("]") or not previous[5:-1].isdigit()
            or current == previous or any(name != "lo" for _, name in socket.if_nameindex())):
        raise RuntimeError("external-network isolation was not established")
    # Origin repository reads: location variables only (see origin_env).
    env = origin_env()
    # Capture the real index, including Git's per-commit GIT_INDEX_FILE.
    # Unmerged entries fail write-tree rather than selecting a different tree.
    tree, index_bytes = capture_index(root, env)
    head = git(root, "rev-parse", "--verify", "HEAD^{commit}", env=env)
    base = git(root, "merge-base", head, meta["base_ref"], env=env)
    print(f"offline-hook: UBS first; candidate-index={tree}; base={base}; netns isolated", flush=True)
    scratch = os.environ.get("TMPDIR")
    if not scratch or not Path(scratch).is_dir():
        raise RuntimeError("TMPDIR must name an existing scratch directory")
    with tempfile.TemporaryDirectory(prefix="offline-index-", dir=scratch) as work:
        snapshot = Path(work)
        isolated = clean_env()
        isolated.update(UBS_BIN=meta["scanner"], UBS_NO_AUTO_UPDATE="1", UBS_NO_CACHE="1", UV_OFFLINE="1",
                        UV_NO_SYNC="1", PIP_NO_INDEX="1", npm_config_offline="true",
                        CARGO_NET_OFFLINE="true", PYTHONDONTWRITEBYTECODE="1",
                        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_NO_LAZY_FETCH="1",
                        GIT_NO_REPLACE_OBJECTS="1")
        subprocess.run(["git", "init", "-q", str(snapshot)], env=isolated, check=True)
        # Object reads only: do not clone/fetch, modify refs in the consumer, or
        # borrow its index. The snapshot is deliberately a standalone Git repo.
        objects = Path(git(root, "rev-parse", "--path-format=absolute", "--git-path", "objects", env=env))
        if "\n" in str(objects):
            raise RuntimeError("object-directory newline cannot be represented safely")
        (snapshot / ".git/objects/info/alternates").write_text(str(objects) + "\n")
        git(snapshot, "update-ref", "HEAD", head, env=isolated)
        git(snapshot, "read-tree", tree, env=isolated)
        materialize(root, tree, snapshot, env)
        # Only this shared source's fixed, qualified shell wrapper may execute;
        # metadata cannot select an alternate executable or interpreter source.
        subprocess.run([str(staged_wrapper)], cwd=snapshot, env=isolated, check=True)
        if capture_index(root, env) != (tree, index_bytes) or git(root, "rev-parse", "HEAD", env=env) != head:
            raise RuntimeError("HEAD/index changed during UBS; refusing stale candidate")
        mode = meta["native_mode"]
        if mode == "native-v1":
            smoke = regular(snapshot / "scripts/ci/smoke.sh")
            entry = regular(snapshot / ".githooks/pre-commit")
            if sha(smoke) != meta["native_sha256"] or sha(entry) != meta["native_hook_sha256"]:
                raise RuntimeError("candidate native entry/smoke differs from qualified owner source")
            subprocess.run(["./.githooks/pre-commit", "--base-ref", base],
                           cwd=snapshot, env=isolated, check=True)
        elif mode == "softwareco":
            # Root's own protected-path obligation covers the candidate tree,
            # including gitlinks hidden by indexed .gitmodules ignore settings.
            protected = subprocess.run([*GIT, "diff", "--no-ext-diff",
                                        "--no-textconv", "--no-renames", "--ignore-submodules=none",
                                        "--quiet", base, tree, "--", ":(top,literal)docs/_core"],
                                       cwd=snapshot, env=isolated)
            if protected.returncode != 0:
                raise RuntimeError("Softwareco protected docs/_core candidate change or diff failure")
            # The original local pre-commit contains only UBS, already run first.
            # Refuse added native obligations instead of silently omitting them.
            for rel, expected in meta["root_contracts"].items():
                if sha(regular(snapshot / rel)) != expected:
                    raise RuntimeError(f"Softwareco native entry contract changed: {rel}")
            regular(snapshot / "scripts/ci/smoke.sh")
            subprocess.run(["./scripts/ci/smoke.sh"],
                           cwd=snapshot, env=isolated, check=True)
        else:
            raise RuntimeError("unknown native mode")
        if capture_index(root, env) != (tree, index_bytes) or git(root, "rev-parse", "HEAD", env=env) != head:
            raise RuntimeError("HEAD/index changed during native checks; refusing stale candidate")
    print(f"ok: offline UBS + native candidate-index checks ({tree})", flush=True)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("usage: offline_commit.py <installed-config.json>")
        main(sys.argv[1])
    except (KeyError, OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"offline-hook: REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
