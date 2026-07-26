#!/usr/bin/env python3
"""Direct-human installer for the exact accepted canary commit; never called by the canary."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
RFC = str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
FILES = [
    ".pi/modes/softwareco-cto-canary.json",
    ".pi/mode-presets/softwareco-cto-canary.json",
    "cto-canary/config.json",
    "cto-canary/output.schema.json",
    "cto-canary/collect_snapshot.py",
    "cto-canary/validate_output.py",
    "cto-canary/fixture_rpc_worker.py",
    "cto-canary/run_cycle.py",
    "cto-canary/start_candidate.py",
    "cto-canary/stop_candidate.py",
    "cto-canary/systemd/softwareco-cto-canary.service",
    "cto-canary/systemd/softwareco-cto-canary.timer",
    "cto-canary/systemd/softwareco-cto-canary-stop.service",
    "cto-canary/systemd/softwareco-cto-canary-stop.timer",
]


def command(argv: list[str], check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(argv, cwd=ROOT, capture_output=True, check=False)
    if check and cp.returncode:
        raise RuntimeError(f"{' '.join(argv)} failed: {cp.stderr.decode(errors='replace').strip()}")
    return cp


def json_command(argv: list[str]) -> dict:
    return json.loads(command(argv).stdout)


def blob(commit: str, relative: str) -> bytes:
    return command(["git", "show", f"{commit}:{relative}"]).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description="Install an accepted immutable CTO canary bundle without starting it")
    parser.add_argument("--decision-id", required=True, type=int)
    parser.add_argument("--acceptance-receipt-id", required=True, type=int)
    parser.add_argument("--accepted-commit", required=True)
    parser.add_argument("--install", action="store_true", help="explicit direct-human installation acknowledgement")
    args = parser.parse_args()
    if not args.install:
        print("REFUSED: pass --install only after reviewing the exact accepted commit", file=sys.stderr); return 3
    if args.decision_id in (74, 77) or not HEX40.fullmatch(args.accepted_commit):
        print("REFUSED: use a separate decision and full lowercase commit hash", file=sys.stderr); return 3
    head = command(["git", "rev-parse", "HEAD"]).stdout.decode().strip()
    source_blob = blob(args.accepted_commit, "cto-canary/activate_candidate.py")
    if head != args.accepted_commit or hashlib.sha256(Path(__file__).read_bytes()).digest() != hashlib.sha256(source_blob).digest():
        print("REFUSED: installer is not executing from the exact accepted HEAD/blob", file=sys.stderr); return 3
    scoped_status = command(["git", "status", "--porcelain", "--", *FILES, "cto-canary/activate_candidate.py"]).stdout
    if scoped_status:
        print("REFUSED: accepted canary paths have uncommitted changes", file=sys.stderr); return 3

    envelope = json_command(["ak", "decision", "get", str(args.decision_id), "--machine"])
    decision = envelope.get("payload", {}).get("decision", {})
    receipt = json_command(["ak", "governance", "show", str(args.acceptance_receipt_id), "--format", "json"])
    checks = [
        decision.get("outcome") == "accepted", decision.get("state") == "unblocked",
        decision.get("rfc_ref") == RFC, decision.get("evidence_ref") == f"governance:{args.acceptance_receipt_id}",
        receipt.get("source_authority") == "human-operator", receipt.get("actor") == "human-operator",
        receipt.get("status") == "applied", receipt.get("to_state") == "accepted",
        receipt.get("agreement_ref") == f"decision:{args.decision_id}",
        receipt.get("details", {}).get("decision_id") == args.decision_id,
        receipt.get("details", {}).get("rfc_commit") == args.accepted_commit,
        receipt.get("details", {}).get("schema") == "softwareco.architecture-decision-acceptance.v1",
    ]
    if not all(checks):
        print("REFUSED: AK decision/acceptance does not bind the exact candidate", file=sys.stderr); return 3

    bundle = Path.home() / ".local/lib/softwareco-cto-canary" / args.accepted_commit
    if bundle.exists():
        print(f"REFUSED: immutable bundle already exists: {bundle}", file=sys.stderr); return 3
    file_hashes: dict[str, str] = {}
    for relative in FILES:
        data = blob(args.accepted_commit, relative)
        target = bundle / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        file_hashes[relative] = hashlib.sha256(data).hexdigest()
    manifest = {"schema_version": 1, "accepted_commit": args.accepted_commit,
                "decision_id": args.decision_id, "acceptance_receipt_id": args.acceptance_receipt_id,
                "files": file_hashes}
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    unit_dir = Path.home() / ".config/systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    replacements = {"@BUNDLE_DIR@": str(bundle / "cto-canary"), "@ROOT@": str(ROOT)}
    for name in ("softwareco-cto-canary.service", "softwareco-cto-canary.timer",
                 "softwareco-cto-canary-stop.service", "softwareco-cto-canary-stop.timer"):
        text = (bundle / "cto-canary/systemd" / name).read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        (unit_dir / name).write_text(text)
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    print(json.dumps({"installed": True, "started": False, "enabled": False,
                      "bundle": str(bundle), "accepted_commit": args.accepted_commit}, sort_keys=True))
    print(f"Next direct-human gate: {bundle / 'cto-canary/start_candidate.py'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
