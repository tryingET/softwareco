#!/usr/bin/env python3
"""Parser-backed task-scope snapshot validation.

This helper exists because shell entrypoints should not parse JSON or iterate
snapshot paths with newline-delimited shell strings.
"""

from __future__ import annotations

import argparse
import difflib
import functools
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SNAPSHOT_NAME = re.compile(r"AK-([0-9]+)\.snapshot\.json")
# Tolerated without validation: a directory placeholder and the documented legacy
# AK-<TASK-ID>.json compatibility fallback (governance/README.md). Any other name fails
# closed, so a snapshot cannot dodge the drift check behind a near-miss name.
TOLERATED_NAMES = (re.compile(r"\.gitkeep"), re.compile(r"AK-[0-9]+\.json"))
# Repository-locating variables (`git rev-parse --local-env-vars`) that a git hook may
# export; inherited, they would make every path resolve to the hook's repository.
GIT_REPO_ENV = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_DIR",
        "GIT_GRAFT_FILE",
        "GIT_IMPLICIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_NO_REPLACE_OBJECTS",
        "GIT_OBJECT_DIRECTORY",
        "GIT_PREFIX",
        "GIT_REPLACE_REF_BASE",
        "GIT_SHALLOW_FILE",
        "GIT_WORK_TREE",
    }
)


def die(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_json_file(path: Path, label: str) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        die(f"{label} missing: {path}")
    except json.JSONDecodeError as exc:
        die(
            f"{label} is not valid JSON: {path} "
            f"({exc.msg} at line {exc.lineno}, column {exc.colno})"
        )


def normalize_snapshot(payload: Any, label: str) -> Any:
    if not isinstance(payload, dict):
        die(f"{label} must be a JSON object")

    normalized = dict(payload)
    normalized.pop("exported_at", None)
    normalized.pop("commit_sha", None)
    return normalized


def json_text(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def resolve_ak_command(raw_value: str) -> list[str]:
    if "/" in raw_value:
        ak_path = Path(raw_value)
        if not ak_path.exists():
            die(f"missing executable: {ak_path}")
        return [str(ak_path)]

    resolved = shutil.which(raw_value)
    if resolved is None:
        die(f"missing ak command on PATH: {raw_value}")
    return [resolved]


def run_ak(repo_root: Path, ak_cmd: list[str], args: list[str], label: str) -> str:
    result = subprocess.run(
        [*ak_cmd, *args],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        if detail:
            die(f"{label}: {detail}")
        die(label)
    return result.stdout


def run_ak_json(repo_root: Path, ak_cmd: list[str], args: list[str], label: str) -> Any:
    stdout = run_ak(repo_root, ak_cmd, args, label)
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        die(
            f"{label}: AK returned invalid JSON "
            f"({exc.msg} at line {exc.lineno}, column {exc.colno})"
        )


def canonical_dir(path_value: str, label: str) -> str:
    try:
        return str(Path(path_value).resolve(strict=True))
    except FileNotFoundError:
        die(f"{label} path does not exist: {path_value}")


@functools.lru_cache(maxsize=None)
def git_repo_identity(path: Path) -> tuple[str, str] | None:
    """Return (git common dir, path relative to its worktree root), or None.

    Linked worktrees of one repository share the common dir, so a task recorded for
    the main checkout is recognised from any of its worktrees.
    """
    env = {key: value for key, value in os.environ.items() if key not in GIT_REPO_ENV}
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(path),
                "rev-parse",
                "--path-format=absolute",
                "--git-common-dir",
                "--show-toplevel",
            ],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    lines = result.stdout.splitlines()
    if result.returncode != 0 or len(lines) != 2:
        return None
    toplevel = Path(lines[1]).resolve()
    if not path.is_relative_to(toplevel):
        return None
    return (str(Path(lines[0]).resolve()), path.relative_to(toplevel).as_posix())


def same_repository(task_repo: Path, repo_root: Path) -> bool:
    task_identity = git_repo_identity(task_repo)
    return task_identity is not None and task_identity == git_repo_identity(repo_root)


def iter_snapshots(snapshots_dir: Path) -> list[Path]:
    snapshots: list[Path] = []
    unrecognized: list[Path] = []
    for path in sorted(snapshots_dir.rglob("*"), key=lambda path: path.as_posix()):
        if path.is_dir():
            continue
        if path.is_file() and SNAPSHOT_NAME.fullmatch(path.name):
            snapshots.append(path)
        elif not (path.is_file() and any(p.fullmatch(path.name) for p in TOLERATED_NAMES)):
            unrecognized.append(path)
    if unrecognized:
        for path in unrecognized:
            print(f"error: unrecognized task-scope file: {str(path)!r}", file=sys.stderr)
        die(
            "task-scope snapshot filename must use a numeric task id: "
            "AK-<TASK-ID>.snapshot.json (rename or remove the files above)"
        )
    return snapshots


def validate_snapshot(repo_root: Path, ak_cmd: list[str], snapshot_path: Path) -> None:
    match = SNAPSHOT_NAME.fullmatch(snapshot_path.name)
    if match is None:
        die(f"task-scope snapshot filename must use a numeric task id: {snapshot_path}")
    task_id = match.group(1)

    task_payload = run_ak_json(
        repo_root,
        ak_cmd,
        ["task", "show", task_id, "-F", "json"],
        f"unable to load AK task {task_id} for snapshot {snapshot_path}",
    )
    task_repo = task_payload.get("repo")
    if not isinstance(task_repo, str) or not task_repo:
        die(f"unable to extract repo for AK task {task_id}")

    task_repo_canonical = canonical_dir(task_repo, f"AK task {task_id} repo")
    if task_repo_canonical != str(repo_root) and not same_repository(
        Path(task_repo_canonical), repo_root
    ):
        die(
            f"snapshot {snapshot_path} belongs to repo {task_repo} "
            f"(canonical: {task_repo_canonical}), expected {repo_root}"
        )

    exported_payload = run_ak_json(
        repo_root,
        ak_cmd,
        ["task", "scope", "export", task_id],
        f"unable to export AK task scope for task {task_id}",
    )
    actual_payload = load_json_file(snapshot_path, "task-scope snapshot")

    expected_normalized = normalize_snapshot(exported_payload, f"AK task scope export {task_id}")
    actual_normalized = normalize_snapshot(actual_payload, f"task-scope snapshot {snapshot_path}")

    if expected_normalized == actual_normalized:
        return

    print(f"error: task-scope snapshot drift detected: {snapshot_path}", file=sys.stderr)
    expected_lines = json_text(expected_normalized).splitlines(keepends=True)
    actual_lines = json_text(actual_normalized).splitlines(keepends=True)
    for line in difflib.unified_diff(
        expected_lines,
        actual_lines,
        fromfile=f"AK-{task_id}.expected.normalized.json",
        tofile=f"AK-{task_id}.actual.normalized.json",
    ):
        sys.stderr.write(line)
    print(
        f"hint: refresh with ak task scope export {task_id} > "
        f"governance/task-scopes/AK-{task_id}.snapshot.json",
        file=sys.stderr,
    )
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--ak", required=True)
    parser.add_argument("--snapshots-dir", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve(strict=True)
    ak_cmd = resolve_ak_command(args.ak)
    snapshots_dir = Path(args.snapshots_dir)

    if not snapshots_dir.is_dir():
        print("ok: no task-scope snapshots")
        return

    snapshots = iter_snapshots(snapshots_dir)
    if not snapshots:
        print("ok: no task-scope snapshots")
        return

    for snapshot_path in snapshots:
        validate_snapshot(repo_root, ak_cmd, snapshot_path)

    print(f"ok: task-scope snapshots ({len(snapshots)} checked)")


if __name__ == "__main__":
    main()
