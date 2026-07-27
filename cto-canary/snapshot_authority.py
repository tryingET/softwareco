#!/usr/bin/env python3
"""Stage a coherent read-only authority DB+WAL view into private service state."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def source_fingerprint(source: Path) -> dict[str, str | None]:
    return {"db": sha256(source), "wal": sha256(Path(str(source) + "-wal"))}


def prepare_ak_snapshot(source: Path, state: Path, attempts: int = 4) -> tuple[Path, dict[str, str | None]]:
    """Copy a byte-stable SQLite DB+WAL pair into private writable cycle state."""
    state.mkdir(parents=True, exist_ok=True)
    target_dir = state / "ak-snapshot"
    for attempt in range(1, attempts + 1):
        before = source_fingerprint(source)
        if before["db"] is None:
            raise RuntimeError(f"authority DB is unavailable: {source}")
        temporary = Path(tempfile.mkdtemp(prefix=".ak-snapshot-", dir=state))
        try:
            snapshot = temporary / source.name
            shutil.copyfile(source, snapshot)
            source_wal = Path(str(source) + "-wal")
            snapshot_wal = Path(str(snapshot) + "-wal")
            if before["wal"] is not None:
                shutil.copyfile(source_wal, snapshot_wal)
            after = source_fingerprint(source)
            copied = {"db": sha256(snapshot), "wal": sha256(snapshot_wal)}
            if before != after or copied != before:
                continue
            connection = sqlite3.connect(snapshot)
            try:
                connection.execute("PRAGMA query_only=ON")
                schema_version = connection.execute("PRAGMA schema_version").fetchone()
                catalog_count = connection.execute("SELECT COUNT(*) FROM sqlite_master").fetchone()
                if not schema_version or not catalog_count or catalog_count[0] < 1:
                    raise RuntimeError("authority snapshot catalog validation failed")
            finally:
                connection.close()
            if target_dir.exists():
                shutil.rmtree(target_dir)
            temporary.replace(target_dir)
            return target_dir / source.name, before
        except (OSError, sqlite3.Error) as exc:
            if attempt == attempts:
                raise RuntimeError(f"authority snapshot failed: {exc}") from exc
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    raise RuntimeError(f"authority DB changed during {attempts} bounded snapshot attempts")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--state-dir", required=True, type=Path)
    args = parser.parse_args()
    args.state_dir.mkdir(parents=True, exist_ok=True)
    lock_path = args.state_dir / "authority-snapshot.lock"
    with lock_path.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        snapshot, fingerprint = prepare_ak_snapshot(args.source, args.state_dir)
        manifest = {
            "schema_version": 1,
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "snapshot": str(snapshot),
            "source_fingerprint": fingerprint,
        }
        target = args.state_dir / "authority-snapshot.json"
        temporary = target.with_suffix(".tmp")
        temporary.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        temporary.chmod(0o600)
        temporary.replace(target)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
