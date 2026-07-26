#!/usr/bin/env python3
"""Collect a bounded, breadth-complete, read-only Softwareco owned-portfolio snapshot."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

MAX_PROBE_BYTES = 2_000_000
MAX_PACKET_BYTES = 8_000_000


def run(argv: list[str], cwd: Path, timeout: int = 60) -> dict[str, Any]:
    env = {k: v for k, v in os.environ.items() if k in {"HOME", "PATH", "AK_DB"}}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C", "TZ": "UTC"})
    try:
        cp = subprocess.run(argv, cwd=cwd, env=env, text=False, capture_output=True,
                            timeout=timeout, check=False)
        stdout, stderr = cp.stdout, cp.stderr
        oversized = len(stdout) > MAX_PROBE_BYTES or len(stderr) > MAX_PROBE_BYTES
        return {
            "argv": argv, "exit_code": cp.returncode,
            "stdout": stdout[:MAX_PROBE_BYTES].decode("utf-8", "replace"),
            "stderr": stderr[:MAX_PROBE_BYTES].decode("utf-8", "replace"),
            "oversized": oversized,
        }
    except subprocess.TimeoutExpired:
        return {"argv": argv, "exit_code": 124, "stdout": "", "stderr": f"timeout after {timeout}s", "oversized": False}


def parse_json(result: dict[str, Any]) -> Any:
    if result["exit_code"] != 0 or result["oversized"]:
        return None
    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError:
        return None


def payload(value: Any) -> Any:
    if isinstance(value, dict) and "payload" in value and "ok" in value:
        return value.get("payload") if value.get("ok") is True else None
    return value


def digest(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {"exists": False}
    stat = path.stat()
    return {"exists": True, "size": stat.st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "mtime_ns": stat.st_mtime_ns}


def discover_git_roots(owned: Path) -> list[str]:
    roots: set[str] = set()
    for marker in owned.rglob(".git"):
        if marker.is_dir() or marker.is_file():
            roots.add(str(marker.parent.resolve()))
    return sorted(roots)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--root", default="/home/tryinget/ai-society/softwareco", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    owned = root / "owned"
    args.output.parent.mkdir(parents=True, exist_ok=True)

    repo_probe = run(["ak", "repo", "list", "--format", "json"], root)
    inventory = parse_json(repo_probe)
    if not isinstance(inventory, list):
        print("AK repository inventory was not valid bounded JSON", file=sys.stderr)
        return 2
    prefix = str(owned) + os.sep
    registered = sorted((r for r in inventory if str(r.get("path", "")).startswith(prefix)), key=lambda r: r["path"])
    filesystem = discover_git_roots(owned)
    registered_paths = [str(Path(r["path"]).resolve()) for r in registered]

    records: list[dict[str, Any]] = []
    gaps: list[str] = []
    for registration in registered:
        path = Path(registration["path"]).resolve()
        record: dict[str, Any] = {"registration": registration, "exists": path.is_dir()}
        if not path.is_dir():
            gaps.append(f"registered repository missing: {path}")
            records.append(record)
            continue
        probes = {
            "git_status": run(["git", "status", "--porcelain=v2", "--branch"], path),
            "git_head": run(["git", "rev-parse", "HEAD"], path),
            "tasks_pending": run(["ak", "task", "list", "--repo", str(path), "--status", "pending", "--machine"], root),
            "tasks_claimed": run(["ak", "task", "list", "--repo", str(path), "--status", "claimed", "--machine"], root),
            "tasks_blocked": run(["ak", "task", "list", "--repo", str(path), "--status", "blocked", "--machine"], root),
            "direction": run(["ak", "direction", "export", "--repo", str(path), "--machine"], root),
        }
        normalized: dict[str, Any] = {}
        for name, probe in probes.items():
            parsed = parse_json(probe) if name.startswith("tasks_") or name == "direction" else None
            normalized[name] = {
                "argv": probe["argv"], "exit_code": probe["exit_code"], "oversized": probe["oversized"],
                "data": payload(parsed) if parsed is not None else None,
                "stdout": probe["stdout"] if parsed is None else None,
                "stderr": probe["stderr"],
            }
            if probe["exit_code"] != 0:
                gaps.append(f"{path}: {name} exited {probe['exit_code']}")
            if probe["oversized"]:
                gaps.append(f"{path}: {name} exceeded {MAX_PROBE_BYTES} bytes")
            if (name.startswith("tasks_") or name == "direction") and parsed is None:
                gaps.append(f"{path}: {name} did not produce valid bounded JSON")
        record["probes"] = normalized
        records.append(record)

    unregistered = sorted(set(filesystem) - set(registered_paths))
    missing_on_disk = sorted(set(registered_paths) - set(filesystem))
    # AK registration defines portfolio membership; filesystem extras are surfaced, not silently admitted.
    authority_db = Path(os.path.expanduser(os.environ.get("AK_DB", "~/ai-society/society.v2.db")))
    packet = {
        "schema_version": 2,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority": "AK and checked-in owner policy; this snapshot and every worker output are noncanonical",
        "scope": str(owned),
        "coverage": {
            "registered_repos_expected": len(registered),
            "registered_repos_observed": len(records),
            "complete": len(records) == len(registered) and not gaps,
            "gaps": gaps,
            "filesystem_git_roots_not_registered": unregistered,
            "registered_paths_without_git_marker": missing_on_disk,
        },
        "authority_db_before": digest(authority_db),
        "repo_inventory_probe": {"argv": repo_probe["argv"], "exit_code": repo_probe["exit_code"]},
        "repositories": records,
    }
    encoded = (json.dumps(packet, indent=2, sort_keys=True) + "\n").encode()
    if len(encoded) > MAX_PACKET_BYTES:
        print(f"snapshot exceeded {MAX_PACKET_BYTES} bytes; refusing partial model input", file=sys.stderr)
        return 2
    args.output.write_bytes(encoded)
    print(json.dumps({"output": str(args.output), "registered": len(registered), "filesystem": len(filesystem),
                      "gaps": len(gaps), "bytes": len(encoded)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
