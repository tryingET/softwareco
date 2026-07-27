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
from runtime_integrity import directory_digest, verify_bundle  # noqa: E402


def run(argv: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    if check and cp.returncode:
        raise RuntimeError(f"{' '.join(argv)} failed: {cp.stderr.strip()}")
    return cp


def acceptance_errors(decision: dict, receipt: dict, decision_id: int, acceptance_id: int, commit: str) -> list[str]:
    expected_rfc = str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md")
    checks = {
        "decision accepted": decision.get("outcome") == "accepted",
        "decision unblocked": decision.get("state") == "unblocked",
        "decision RFC": decision.get("rfc_ref") == expected_rfc,
        "decision evidence": decision.get("evidence_ref") == f"governance:{acceptance_id}",
        "human source": receipt.get("source_authority") == "human-operator",
        "human actor": receipt.get("actor") == "human-operator",
        "applied acceptance": receipt.get("status") == "applied" and receipt.get("to_state") == "accepted",
        "decision agreement": receipt.get("agreement_ref") == f"decision:{decision_id}",
        "receipt schema": receipt.get("details", {}).get("schema") == "softwareco.architecture-decision-acceptance.v1",
        "receipt decision": receipt.get("details", {}).get("decision_id") == decision_id,
        "accepted commit": receipt.get("details", {}).get("rfc_commit") == commit,
    }
    return [label for label, passed in checks.items() if not passed]


def predecessor_errors(prior: dict, activation: dict, stop: dict, chain: list[dict], required: dict) -> list[str]:
    decision_id = required["decision_id"]
    activation_id = required["activation_receipt_id"]
    stop_id = required["stop_receipt_id"]
    concern = f"softwareco-autonomous-cto-canary:decision-{decision_id}:control"
    checks = {
        "local predecessor state": prior.get("state") == "human_stopped",
        "local predecessor decision": prior.get("decision_id") == decision_id,
        "local predecessor activation": prior.get("activation_receipt_id") == activation_id,
        "local predecessor concern": prior.get("control_concern") == concern,
        "activation id": activation.get("id") == activation_id,
        "activation human source": activation.get("source_authority") == "human-operator",
        "activation human actor": activation.get("actor") == "human-operator",
        "activation applied": activation.get("status") == "applied",
        "activation agreement": activation.get("agreement_ref") == f"decision:{decision_id}",
        "stop id": stop.get("id") == stop_id,
        "stop human source": stop.get("source_authority") == "human-operator",
        "stop human actor": stop.get("actor") == "human-operator",
        "stop applied": stop.get("status") == "applied",
        "stop agreement": stop.get("agreement_ref") == f"decision:{decision_id}",
        "stop transition": stop.get("from_state") == activation.get("to_state") and stop.get("to_state") == "stopped",
        "stop evidence": stop.get("evidence_ref") == f"governance:{activation_id}",
        "stop activation detail": stop.get("details", {}).get("activation_receipt_id") == activation_id,
        "newest control head": bool(chain) and chain[0].get("id") == stop_id,
    }
    return [label for label, passed in checks.items() if not passed]


def main() -> int:
    parser = argparse.ArgumentParser(description="Record direct-human activation and start the exact 24-hour canary")
    parser.add_argument("--decision-id", required=True, type=int)
    parser.add_argument("--acceptance-receipt-id", required=True, type=int)
    parser.add_argument("--accepted-commit", required=True)
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
    if (not isinstance(decision_id, int) or decision_id in (74, 77) or
            (args.decision_id, args.acceptance_receipt_id, args.accepted_commit) != (decision_id, acceptance_id, commit)):
        print("REFUSED: explicit activation identity differs from installed accepted identity", file=sys.stderr); return 3
    decision_envelope = json.loads(run(["ak", "decision", "get", str(decision_id), "--machine"]).stdout)
    decision = decision_envelope.get("payload", {}).get("decision", {})
    receipt = json.loads(run(["ak", "governance", "show", str(acceptance_id), "--format", "json"]).stdout)
    authority_errors = acceptance_errors(decision, receipt, decision_id, acceptance_id, commit)
    if authority_errors:
        print("REFUSED: live decision/acceptance mismatch: " + ", ".join(authority_errors), file=sys.stderr); return 3
    pseudo_activation = {"bundle_dir": str(BUNDLE), "accepted_commit": commit, "decision_id": decision_id,
                         "acceptance_receipt_id": acceptance_id,
                         "bundle_manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()}
    artifact_errors = verify_bundle(pseudo_activation)
    try:
        if directory_digest(Path(CONFIG["pi_modes_package"])) != CONFIG["pi_modes_package_digest"]:
            artifact_errors.append("pi-modes package digest drift")
        if directory_digest(Path(CONFIG["pi_package"])) != CONFIG["pi_package_digest"]:
            artifact_errors.append("Pi package digest drift")
    except (OSError, RuntimeError) as exc:
        artifact_errors.append(f"runtime package digest failed closed: {exc}")
    version = run(["/usr/bin/node", CONFIG["pi_entrypoint"], "--version"]).stdout.strip()
    if version != CONFIG["pi_version"]:
        artifact_errors.append("Pi version drift")
    for unit in ("softwareco-cto-canary.timer", "softwareco-cto-canary-stop.timer"):
        if run(["systemctl", "--user", "is-active", "--quiet", unit], check=False).returncode == 0:
            artifact_errors.append(f"unit unexpectedly active before activation: {unit}")
        if run(["systemctl", "--user", "is-enabled", "--quiet", unit], check=False).returncode == 0:
            artifact_errors.append(f"unit unexpectedly enabled before activation: {unit}")
    if artifact_errors:
        print("REFUSED: " + "; ".join(artifact_errors), file=sys.stderr); return 3
    state_dir = Path.home() / ".local/state/softwareco-cto-canary"
    activation_path = state_dir / "activation.json"
    concern = f"softwareco-autonomous-cto-canary:decision-{decision_id}:control"
    existing = json.loads(run(["ak", "governance", "list", "--concern", concern, "--limit", "100", "--json"]).stdout)
    if existing:
        print("REFUSED: this accepted canary decision already has a control history", file=sys.stderr); return 3
    required = CONFIG["required_predecessor"]
    history = state_dir / "history"
    archived = history / (f"activation-decision-{required['decision_id']}-"
                          f"receipt-{required['activation_receipt_id']}.json")
    if activation_path.exists() and archived.exists():
        print("REFUSED: predecessor activation exists in both live and archive locations", file=sys.stderr); return 3
    predecessor_path = activation_path if activation_path.exists() else archived
    try:
        prior = json.loads(predecessor_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REFUSED: exact stopped predecessor state is unavailable: {exc}", file=sys.stderr); return 3
    expected_concern = f"softwareco-autonomous-cto-canary:decision-{required['decision_id']}:control"
    prior_activation = json.loads(run(["ak", "governance", "show", str(required["activation_receipt_id"]),
                                       "--format", "json"]).stdout)
    prior_stop = json.loads(run(["ak", "governance", "show", str(required["stop_receipt_id"]),
                                 "--format", "json"]).stdout)
    prior_chain = json.loads(run(["ak", "governance", "list", "--concern", expected_concern,
                                  "--limit", "100", "--json"]).stdout)
    prior_errors = predecessor_errors(prior, prior_activation, prior_stop, prior_chain, required)
    if prior_errors:
        print("REFUSED: exact predecessor activation/stop receipt chain is invalid: " +
              ", ".join(prior_errors), file=sys.stderr); return 3
    if activation_path.exists():
        history.mkdir(parents=True, exist_ok=True)
        activation_path.replace(archived)

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
        "--source-authority", "human-operator", "--mito-layer", "Operations & Evaluation",
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
        print(f"Run python3 {HERE / 'stop_candidate.py'} --human-stop to reconcile.", file=sys.stderr)
        return 2
    print(json.dumps({"active": True, "activation_receipt_id": activation_id,
                      "started_at_utc": started_text, "expires_at_utc": expires_text,
                      "max_cycles": CONFIG["max_cycles"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
