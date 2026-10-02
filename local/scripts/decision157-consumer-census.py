#!/usr/bin/env python3
"""Read-only, bounded Decision157 inventory; observations never authorize migration.

Consumes an explicit `ak repo list --company softwareco -F json` export. Does not
invoke AK, traverse outside --workspace, initialize submodules, run hooks, or
read arbitrary untracked content. JSON output contains paths, hashes and locator
references only. Missing/excluded inputs remain explicit and closure stays false.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess

MAX_BYTES = 128 * 1024
MAX_INPUTS = 1000
LOCATOR = re.compile(r"<(?:repo|gitlab):[^>\n]+>")
RELATIVE = re.compile(r'^\s*(?:-\s*)?(?:ref|path|company_ontology_ref):\s*[\"\']?([^\"\'\n#]+)', re.M)
ROOT_INPUTS = (".copier-answers.yml", "ontology/manifest.yaml", "copier.yml")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def references(text: str) -> list[dict]:
    result = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for match in LOCATOR.finditer(line):
            ref = match.group()
            transport, body = ref[1:-1].split(":", 1)
            owner, separator, revision = body.rpartition("@")
            if not separator:
                owner = body
            if "{{" in ref:
                kind = "generator_parameter"
            elif owner in {"core/ontology-kernel", "ai-society/core/ontology-kernel"}:
                kind = "core"
            elif owner in {"softwareco/ontology", "ai-society/softwareco/ontology"}:
                kind = "old_owner" if revision == "main" else "old_owner_variant"
            elif owner in {"softwareco", "ai-society/softwareco"}:
                kind = "parent"
            elif transport == "gitlab":
                kind = "legacy_gitlab"
            else:
                kind = "other_company"
            result.append({"line": line_no, "class": kind, "locator": ref, "transport": transport})
        match = RELATIVE.match(line)
        if match:
            ref = match[1].strip()
            if "ontology" in ref and ref.startswith(("../", "./", "/")) and not LOCATOR.search(ref):
                result.append({"line": line_no, "class": "relative", "locator": ref})
    return result


def git(root: Path, *args: str) -> bytes:
    # No inherited loader, interpreter, Git, credential or PATH configuration.
    env = {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0", "GIT_NO_LAZY_FETCH": "1",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_NO_REPLACE_OBJECTS": "1"}
    command = ["/usr/bin/git", "--no-optional-locks", "-c", "core.fsmonitor=false",
               "-c", "core.untrackedCache=false", "-c", f"core.hooksPath={os.devnull}",
               "-C", str(root), *args]
    try:
        completed = subprocess.run(command, capture_output=True, env=env, check=False, timeout=30)
    except subprocess.TimeoutExpired as error:
        raise ValueError(f"git command timed out: {args[0]}") from error
    if completed.returncode:
        raise ValueError(f"git command failed: {args[0]} (exit {completed.returncode})")
    return completed.stdout


def symlink_path(path: Path, workspace: Path) -> bool:
    current = workspace
    for part in path.relative_to(workspace).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def metadata_text(path: Path, workspace: Path) -> str:
    """Bounded metadata locator/config inspection before invoking Git."""
    if not path.is_relative_to(workspace) or symlink_path(path, workspace):
        raise ValueError("external_or_symlinked_git_metadata")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("nonregular_git_metadata")
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("git_metadata_byte_limit")
    return data.decode("utf-8-sig")


def check_metadata(path: Path, workspace: Path) -> None:
    """Reject external gitdirs, shared object stores and config includes."""
    current = path
    while not (current / ".git").exists() and not (current / ".git").is_symlink():
        if current == workspace:
            raise ValueError("missing_git_metadata")
        current = current.parent
    meta = current / ".git"
    if symlink_path(meta, workspace):
        raise ValueError("external_or_symlinked_git_metadata")
    if not meta.is_dir():
        text = metadata_text(meta, workspace).strip()
        if not text.startswith("gitdir: "):
            raise ValueError("invalid_gitdir_file")
        meta = (current / text[8:]).resolve()
    if not meta.is_relative_to(workspace) or symlink_path(meta, workspace):
        raise ValueError("external_or_symlinked_git_metadata")
    common = meta
    if (meta / "commondir").exists() or (meta / "commondir").is_symlink():
        common = (meta / metadata_text(meta / "commondir", workspace).strip()).resolve()
    if not common.is_relative_to(workspace) or symlink_path(common, workspace):
        raise ValueError("external_or_symlinked_git_metadata")
    for config in {common / "config", meta / "config.worktree"}:
        if (config.exists() or config.is_symlink()) and re.search(r"^\s*\[include", metadata_text(config, workspace), re.M | re.I):
            raise ValueError("unsupported_git_config_include")
    objects = common / "objects"
    if symlink_path(objects, workspace):
        raise ValueError("symlinked_git_object_store")
    alternates = objects / "info/alternates"
    if (alternates.exists() or alternates.is_symlink()) and metadata_text(alternates, workspace).strip():
        raise ValueError("unsupported_git_object_alternates")
    # Git may otherwise read symlinked indexes, refs, pack files or loose objects.
    for item in {meta / "index", meta / "HEAD", common / "HEAD", common / "packed-refs",
                 common / "shallow", common / "info/grafts"}:
        if symlink_path(item, workspace):
            raise ValueError("symlinked_git_metadata_member")
        if item.exists() and not stat.S_ISREG(item.stat().st_mode):
            raise ValueError("nonregular_git_metadata_member")
    def traversal_error(error: OSError) -> None:
        raise ValueError("uninspectable_git_metadata") from error

    count = 0
    for directory in (common / "objects", common / "refs"):
        if symlink_path(directory, workspace):
            raise ValueError("symlinked_git_metadata_member")
        if directory.exists() and not directory.is_dir():
            raise ValueError("nonregular_git_metadata_directory")
        for current_dir, dirs, files in os.walk(directory, followlinks=False, onerror=traversal_error):
            for name in dirs + files:
                count += 1
                if count > 200000:
                    raise ValueError("git_metadata_member_limit")
                member = Path(current_dir) / name
                mode = member.lstat().st_mode
                if stat.S_ISLNK(mode):
                    raise ValueError("symlinked_git_metadata_member")
                if not stat.S_ISREG(mode) and not stat.S_ISDIR(mode):
                    raise ValueError("nonregular_git_metadata_member")


def relevant(path: str) -> bool:
    p = Path(path)
    if p.name.startswith(".copier-answers") and p.suffix in {".yml", ".yaml"}:
        return True
    if p.name == "copier.yml":
        return True
    if p.name == "manifest.yaml" and "ontology" in p.parts:
        return True
    return p.name == "resolve.json" and any("dist" in part for part in p.parts)


def collect(registrations: list[dict], workspace: Path) -> dict:
    workspace = workspace.resolve(strict=True)
    paths = sorted({row["path"] for row in registrations if row.get("company") == "softwareco"})
    report = {
        "schema": "softwareco.decision157-consumer-census.v1",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "collector_sha256": digest(Path(__file__).read_bytes()),
        "git_version": git(workspace, "--version").decode().strip(),
        "registration_paths_sha256": digest(("\n".join(paths) + "\n").encode()),
        "closure_complete": False,
        "limits": [
            "Root declaration inputs plus selected indexed declarations/resolution projections only",
            "No arbitrary untracked scan, external discovery, receipt-reader/writer closure or owner disposition",
            "Index/worktree snapshots may change during collection; not a writer-fenced preservation proof",
            "Text locator observations, not parsed semantic validity or authorization",
        ],
        "registrations": [], "git_roots": [], "inputs": [], "coverage": [], "omissions": [],
    }
    roots = set()
    root_declarations = set()
    for raw in paths:
        path = Path(raw)
        row = {"path": raw}
        report["registrations"].append(row)
        if not path.is_absolute() or ".." in path.parts or not path.is_relative_to(workspace):
            row["status"] = "outside_workspace"
            continue
        if symlink_path(path, workspace):
            row["status"] = "symlink_path"
            continue
        if not path.is_dir():
            row["status"] = "missing"
            continue
        try:
            check_metadata(path, workspace)
            root = Path(git(path, "rev-parse", "--show-toplevel").decode().strip())
            if not root.is_relative_to(workspace):
                row["status"] = "git_root_outside_workspace"
                continue
            if not path.is_relative_to(root):
                raise ValueError("git_root_not_registration_ancestor")
            check_metadata(root, workspace)
            declarations = {(root, str((path / name).relative_to(root))) for name in ROOT_INPUTS}
            row.update(git_root=str(root), status="independent" if root == path else "enclosing_git_root")
            roots.add(root)
            root_declarations.update(declarations)
        except (ValueError, OSError, UnicodeError) as error:
            row.update(status="git_error", error=str(error))
    for root in sorted(roots):
        root_row = {"path": str(root)}
        report["git_roots"].append(root_row)
        try:
            check_metadata(root, workspace)
            root_row["head"] = git(root, "rev-parse", "HEAD").decode().strip()
            # NUL paths preserve whitespace/newlines; conflicting stages remain omissions.
            index = {}
            index_bytes = git(root, "ls-files", "--stage", "-z")
            for entry in index_bytes.split(b"\0"):
                if not entry:
                    continue
                metadata, raw_path = entry.split(b"\t", 1)
                name = raw_path.decode("utf-8")
                if relevant(name):
                    mode, oid, stage = metadata.decode().split()
                    index.setdefault(name, []).append((mode, oid, stage))
            names = sorted(set(index) | {name for owner, name in root_declarations if owner == root})
            if len(names) > MAX_INPUTS:
                report["omissions"].append({"root": str(root), "reason": "input_limit", "total": len(names)})
                names = names[:MAX_INPUTS]
            root_row["index_sha256"] = digest(index_bytes)
            for name in names:
                entries = index.get(name, [])
                base = {"root": str(root), "path": name, "tracked": bool(entries)}
                coverage = {**base, "root_declaration": (root, name) in root_declarations,
                            "worktree_status": "unread"}
                report["coverage"].append(coverage)
                for mode, oid, stage in entries:
                    if mode not in {"100644", "100755"} or stage != "0":
                        report["omissions"].append({**base, "stage": stage, "mode": mode,
                                                   "reason": "nonregular_or_conflicted_index"})
                        continue
                    size = int(git(root, "cat-file", "-s", oid))
                    if size > MAX_BYTES:
                        report["omissions"].append({**base, "origin": "index", "reason": "byte_limit"})
                        continue
                    data = git(root, "cat-file", "blob", oid)
                    try:
                        refs = references(data.decode("utf-8"))
                    except UnicodeError:
                        report["omissions"].append({**base, "origin": "index", "reason": "invalid_utf8"})
                        continue
                    report["inputs"].append({**base, "origin": "index", "blob": oid,
                        "sha256": digest(data), "references": refs})
                target = root / name
                if not target.is_relative_to(workspace) or ".." in Path(name).parts:
                    report["omissions"].append({**base, "reason": "unsafe_path"})
                    continue
                if symlink_path(target, workspace):
                    coverage["worktree_status"] = "symlink_path"
                    report["omissions"].append({**base, "reason": "symlink_path"})
                    continue
                try:
                    # O_NOFOLLOW closes the final-component symlink race. Ancestor writers
                    # are not fenced; races are explicitly outside this inventory's proof.
                    fd = os.open(target, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                    with os.fdopen(fd, "rb") as stream:
                        info = os.fstat(stream.fileno())
                        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                            coverage["worktree_status"] = "nonregular_or_byte_limit"
                            report["omissions"].append({**base, "reason": "nonregular_or_byte_limit"})
                            continue
                        data = stream.read(MAX_BYTES + 1)
                    if len(data) > MAX_BYTES:
                        report["omissions"].append({**base, "reason": "byte_limit"})
                        continue
                    refs = references(data.decode("utf-8"))
                    coverage["worktree_status"] = "read"
                    report["inputs"].append({**base, "origin": "worktree", "sha256": digest(data),
                        "references": refs})
                except FileNotFoundError:
                    coverage["worktree_status"] = "absent"
                    if entries:
                        report["omissions"].append({**base, "reason": "missing_worktree"})
                except (OSError, UnicodeError) as error:
                    coverage["worktree_status"] = type(error).__name__
                    report["omissions"].append({**base, "reason": type(error).__name__})
            root_row["head_after"] = git(root, "rev-parse", "HEAD").decode().strip()
            root_row["index_sha256_after"] = digest(git(root, "ls-files", "--stage", "-z"))
            root_row["metadata_stable"] = (root_row["head"] == root_row["head_after"] and
                root_row["index_sha256"] == root_row["index_sha256_after"])
        except (ValueError, OSError, UnicodeError) as error:
            report["omissions"].append({"root": str(root), "reason": "git_error", "error": str(error)})
    report["summary"] = {
        "registrations": len(paths), "git_roots": len(roots),
        "registration_status": dict(Counter(r["status"] for r in report["registrations"])),
        "inputs": len(report["inputs"]), "omissions": len(report["omissions"]),
        "coverage_status": dict(Counter(r["worktree_status"] for r in report["coverage"])),
        "distinct_input_paths": len({(r["root"], r["path"]) for r in report["inputs"]}),
        "reference_classes": dict(Counter(ref["class"] for row in report["inputs"] for ref in row["references"])),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registrations", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.registrations.read_text())
    if not isinstance(rows, list) or any(not isinstance(row, dict) or
            not isinstance(row.get("path"), str) for row in rows):
        parser.error("registrations must be an AK repository-array export")
    print(json.dumps(collect(rows, args.workspace), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
