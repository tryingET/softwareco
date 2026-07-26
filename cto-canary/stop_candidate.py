#!/usr/bin/env python3
"""Bounded expiry shutdown or direct-human early stop for the CTO canary."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / "config.json").read_text())
ROOT = Path(CONFIG["cwd"])
STATE = Path.home() / ".local/state/softwareco-cto-canary/activation.json"
ROLLBACK = str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-validation-rollout-rollback.md")


def run(argv: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    if check and cp.returncode:
        raise RuntimeError(f"{' '.join(argv)} failed: {cp.stderr.strip()}")
    return cp


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--expiry", action="store_true", help="supervisor expiry path; never writes AK")
    group.add_argument("--human-stop", action="store_true", help="direct-human early stop and receipt")
    args = parser.parse_args()
    try:
        state = json.loads(STATE.read_text())
        expiry = datetime.fromisoformat(state["expires_at_utc"].replace("Z", "+00:00"))
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"REFUSED: activation state unreadable: {exc}", file=sys.stderr); return 3
    now = datetime.now(timezone.utc)
    if args.expiry and now < expiry:
        print("REFUSED: expiry service fired before the exact authority deadline", file=sys.stderr); return 3
    # Kill any in-flight model process through the main service cgroup before disabling triggers.
    run(["systemctl", "--user", "stop", "softwareco-cto-canary.service"], check=False)
    if args.human_stop:
        chain = json.loads(run(["ak", "governance", "list", "--concern", state["control_concern"], "--limit", "100", "--json"]).stdout)
        if not chain or chain[-1].get("id") != state["activation_receipt_id"]:
            print("REFUSED: activation is not the live control-chain head", file=sys.stderr); return 3
        details = {"schema": "softwareco.autonomous-cto-canary-stop.v1",
                   "decision_id": state["decision_id"], "activation_receipt_id": state["activation_receipt_id"],
                   "stopped_at_utc": now.isoformat(), "reason": "direct_human_early_stop"}
        run(["ak", "governance", "record", "--concern", state["control_concern"],
             "--source-authority", "human-operator", "--mito-layer", "Operations",
             "--s3-domain-ref", "softwareco", "--agreement-ref", f"decision:{state['decision_id']}",
             "--from-state", chain[-1]["to_state"], "--to-state", "stopped",
             "--consent-mode", "explicit", "--evidence-ref", f"governance:{state['activation_receipt_id']}",
             "--rollback-ref", ROLLBACK, "--repo-scope", str(ROOT), "--actor", "human-operator",
             "--details", json.dumps(details, separators=(",", ":"))])
        state["state"] = "human_stopped"
    else:
        # The accepted activation receipt contains the exact deadline; authority ends by time.
        # This local transition only stops future process triggers and never claims an AK receipt.
        state["state"] = "expired_by_time"
    state["stopped_at_utc"] = now.isoformat()
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n"); temporary.chmod(0o600); temporary.replace(STATE)
    run(["systemctl", "--user", "disable", "--now", "softwareco-cto-canary.timer", "softwareco-cto-canary-stop.timer"], check=False)
    print(json.dumps({"state": state["state"], "stopped_at_utc": state["stopped_at_utc"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
