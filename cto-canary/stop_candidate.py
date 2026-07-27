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


def unit_property(unit: str, name: str) -> tuple[str | None, str | None]:
    result = run(["systemctl", "--user", "show", unit, f"--property={name}", "--value"], check=False)
    if result.returncode:
        return None, f"{unit} {name} query failed rc={result.returncode}: {result.stderr.strip()}"
    return result.stdout.strip(), None


def cgroup_members(control_group: str | None, root: Path = Path("/sys/fs/cgroup")) -> str:
    if not control_group:
        return ""
    procs = root / control_group.lstrip("/") / "cgroup.procs"
    return procs.read_text().strip() if procs.exists() else ""

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
    if state.get("state") != "active":
        print("REFUSED: activation is not active; repeated or stale stop is forbidden", file=sys.stderr); return 3
    if args.expiry and now < expiry:
        print("REFUSED: expiry service fired before the exact authority deadline", file=sys.stderr); return 3
    # Remove every trigger before stopping the main service so it cannot race/retrigger during reconciliation.
    units = ["softwareco-cto-canary.timer", "softwareco-cto-canary-stop.timer"]
    disable = run(["systemctl", "--user", "disable", "--now", *units], check=False)
    residual: list[str] = []
    for unit in units:
        active, active_error = unit_property(unit, "ActiveState")
        enabled = run(["systemctl", "--user", "is-enabled", unit], check=False)
        if active_error or active != "inactive" or enabled.stdout.strip() != "disabled":
            residual.append(f"{unit}(active={active},active_error={active_error},enabled={enabled.stdout.strip()},rc={enabled.returncode})")
    if disable.returncode or residual:
        print(f"REFUSED: trigger cleanup failed before service stop (rc={disable.returncode}): {residual}", file=sys.stderr)
        return 2
    # Kill the model service and any authority-snapshot helper before recording stopped state.
    services = ["softwareco-cto-canary.service", "softwareco-cto-canary-snapshot.service"]
    stop_result = run(["systemctl", "--user", "stop", *services], check=False)
    reset_result = run(["systemctl", "--user", "reset-failed", *services], check=False)
    service_residual: list[str] = []
    for service in services:
        active_state, state_error = unit_property(service, "ActiveState")
        control_group, cgroup_error = unit_property(service, "ControlGroup")
        cgroup_processes = cgroup_members(control_group)
        if state_error or cgroup_error or active_state != "inactive" or cgroup_processes:
            service_residual.append(
                f"{service}(state={active_state},state_error={state_error},"
                f"cgroup_error={cgroup_error},cgroup_processes={cgroup_processes!r})"
            )
    if stop_result.returncode or reset_result.returncode or service_residual:
        print(f"REFUSED: service termination unverified: stop_rc={stop_result.returncode} "
              f"reset_rc={reset_result.returncode} residual={service_residual}", file=sys.stderr)
        return 2
    if args.human_stop:
        chain = json.loads(run(["ak", "governance", "list", "--concern", state["control_concern"], "--limit", "100", "--json"]).stdout)
        if not chain or chain[0].get("id") != state["activation_receipt_id"]:
            print("REFUSED: activation is not the live control-chain head", file=sys.stderr); return 3
        details = {"schema": "softwareco.autonomous-cto-canary-stop.v1",
                   "decision_id": state["decision_id"], "activation_receipt_id": state["activation_receipt_id"],
                   "stopped_at_utc": now.isoformat(), "reason": "direct_human_early_stop"}
        run(["ak", "governance", "record", "--concern", state["control_concern"],
             "--source-authority", "human-operator", "--mito-layer", "Operations & Evaluation",
             "--s3-domain-ref", "softwareco", "--agreement-ref", f"decision:{state['decision_id']}",
             "--from-state", chain[0]["to_state"], "--to-state", "stopped",
             "--consent-mode", "explicit", "--evidence-ref", f"governance:{state['activation_receipt_id']}",
             "--rollback-ref", ROLLBACK, "--repo-scope", str(ROOT), "--actor", "human-operator",
             "--details", json.dumps(details, separators=(",", ":"))])
        fresh_chain = json.loads(run(["ak", "governance", "list", "--concern", state["control_concern"],
                                      "--limit", "100", "--json"]).stdout)
        if (not fresh_chain or fresh_chain[0].get("to_state") != "stopped" or
                fresh_chain[0].get("source_authority") != "human-operator" or
                fresh_chain[0].get("actor") != "human-operator" or
                fresh_chain[0].get("status") != "applied" or
                fresh_chain[0].get("evidence_ref") != f"governance:{state['activation_receipt_id']}" or
                fresh_chain[0].get("details") != details):
            print("REFUSED: stop receipt fresh-read did not match", file=sys.stderr); return 3
        state["state"] = "human_stopped"
    else:
        # The accepted activation receipt contains the exact deadline; authority ends by time.
        # This local transition only stops future process triggers and never claims an AK receipt.
        state["state"] = "expired_by_time"
    state["stopped_at_utc"] = now.isoformat()
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n"); temporary.chmod(0o600); temporary.replace(STATE)
    print(json.dumps({"state": state["state"], "stopped_at_utc": state["stopped_at_utc"],
                      "main_service_active": False, "timers_active_or_enabled": []}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
