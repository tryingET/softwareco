#!/usr/bin/env python3
"""Direct-human one-shot activation of an installed accepted 24-hour canary bundle."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CONFIG = json.loads((HERE / "config.json").read_text())
MANIFEST_PATH = BUNDLE / "manifest.json"
ROOT = Path(CONFIG["cwd"])
ROLLBACK = str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-validation-rollout-rollback.md")


def run(argv: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    if check and cp.returncode:
        raise RuntimeError(f"{' '.join(argv)} failed: {cp.stderr.strip()}")
    return cp


def main() -> int:
    parser = argparse.ArgumentParser(description="Record direct-human activation and start the exact 24-hour canary")
    parser.add_argument("--start", action="store_true", help="explicit direct-human activation acknowledgement")
    args = parser.parse_args()
    if not args.start:
        print("REFUSED: pass --start only after reviewing the installed accepted bundle", file=sys.stderr); return 3
    try:
        manifest = json.loads(MANIFEST_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REFUSED: installed manifest unavailable: {exc}", file=sys.stderr); return 3
    decision_id = manifest.get("decision_id")
    acceptance_id = manifest.get("acceptance_receipt_id")
    commit = manifest.get("accepted_commit")
    if not isinstance(decision_id, int) or decision_id in (74, 77):
        print("REFUSED: invalid installed decision identity", file=sys.stderr); return 3
    state_dir = Path.home() / ".local/state/softwareco-cto-canary"
    activation_path = state_dir / "activation.json"
    if activation_path.exists():
        print("REFUSED: activation state already exists; reconcile/stop it first", file=sys.stderr); return 3
    concern = f"softwareco-autonomous-cto-canary:decision-{decision_id}:control"
    existing = json.loads(run(["ak", "governance", "list", "--concern", concern, "--limit", "100", "--json"]).stdout)
    if existing:
        print("REFUSED: this accepted canary decision already has a control history", file=sys.stderr); return 3

    started = datetime.now(timezone.utc)
    expires = started + timedelta(seconds=CONFIG["window_seconds"])
    started_text = started.isoformat()
    expires_text = expires.isoformat()
    run_id = uuid.uuid4().hex
    details = {
        "schema": "softwareco.autonomous-cto-canary-activation.v1",
        "decision_id": decision_id, "acceptance_receipt_id": acceptance_id,
        "accepted_commit": commit, "run_id": run_id,
        "started_at_utc": started_text, "expires_at_utc": expires_text,
        "max_cycles": CONFIG["max_cycles"], "interval_seconds": CONFIG["interval_seconds"],
        "activity_envelope": CONFIG["activity_envelope"], "external_effects_authorized": ["model_api_calls", "local_canary_state"],
        "forbidden_effects": ["ak_mutation_by_canary", "owner_repo_mutation", "orchestrator_self_dispatch", "publication", "release"],
    }
    run([
        "ak", "governance", "record", "--concern", concern,
        "--source-authority", "human-operator", "--mito-layer", "Operations",
        "--s3-domain-ref", "softwareco", "--agreement-ref", f"decision:{decision_id}",
        "--from-state", "inactive", "--to-state", f"active:{run_id}",
        "--consent-mode", "explicit", "--evidence-ref", f"git:{commit}",
        "--rollback-ref", ROLLBACK, "--repo-scope", str(ROOT), "--actor", "human-operator",
        "--details", json.dumps(details, separators=(",", ":")),
    ])
    chain = json.loads(run(["ak", "governance", "list", "--concern", concern, "--limit", "100", "--json"]).stdout)
    if len(chain) != 1 or chain[0].get("details") != details or chain[0].get("status") != "applied":
        print("REFUSED: activation receipt fresh-read did not match; reconcile manually", file=sys.stderr); return 3
    activation_id = chain[0]["id"]
    state_dir.mkdir(parents=True, exist_ok=True)
    activation = {
        "schema_version": 1, "state": "active", "decision_id": decision_id,
        "acceptance_receipt_id": acceptance_id, "activation_receipt_id": activation_id,
        "accepted_commit": commit, "bundle_dir": str(BUNDLE),
        "bundle_manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "started_at_utc": started_text, "expires_at_utc": expires_text,
        "max_cycles": CONFIG["max_cycles"], "interval_seconds": CONFIG["interval_seconds"],
        "activated_by": "human-operator", "control_concern": concern,
    }
    temporary = activation_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(activation, indent=2, sort_keys=True) + "\n")
    temporary.chmod(0o600); temporary.replace(activation_path)
    try:
        run(["systemctl", "--user", "enable", "--now", "softwareco-cto-canary.timer", "softwareco-cto-canary-stop.timer"])
    except RuntimeError as exc:
        print(f"ACTIVATION RECORDED BUT START FAILED: {exc}", file=sys.stderr)
        print(f"Run {HERE / 'stop_candidate.py'} --human-stop to reconcile.", file=sys.stderr)
        return 2
    print(json.dumps({"active": True, "activation_receipt_id": activation_id,
                      "started_at_utc": started_text, "expires_at_utc": expires_text,
                      "max_cycles": CONFIG["max_cycles"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
