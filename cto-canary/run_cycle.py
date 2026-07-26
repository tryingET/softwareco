#!/usr/bin/env python3
"""Run one accepted CTO canary cycle with a fresh ephemeral, tool-free Pi RPC worker."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / "config.json").read_text())
ROOT = Path(CONFIG["cwd"])
sys.path.insert(0, str(HERE))
from validate_output import validate  # noqa: E402

HEX40 = re.compile(r"^[0-9a-f]{40}$")
ACTIVATION_KEYS = {
    "schema_version", "state", "decision_id", "acceptance_receipt_id", "activation_receipt_id",
    "accepted_commit", "bundle_dir", "bundle_manifest_sha256", "started_at_utc", "expires_at_utc",
    "max_cycles", "interval_seconds", "activated_by", "control_concern",
}
UNIT_NAMES = (
    "softwareco-cto-canary.service", "softwareco-cto-canary.timer",
    "softwareco-cto-canary-stop.service", "softwareco-cto-canary-stop.timer",
)


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def parse_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else None
    except ValueError:
        return None


def run(argv: list[str], cwd: Path = ROOT, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout, check=False)


def json_command(argv: list[str]) -> Any:
    cp = run(argv)
    if cp.returncode:
        raise RuntimeError(f"{' '.join(argv)} failed: {cp.stderr.strip()}")
    return json.loads(cp.stdout)


def payload(value: Any) -> Any:
    if isinstance(value, dict) and "payload" in value and "ok" in value:
        if value.get("ok") is not True:
            raise RuntimeError("AK machine envelope reported failure")
        return value["payload"]
    return value


def directory_digest(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix().encode()
        data = path.read_bytes()
        h.update(len(relative).to_bytes(8, "big")); h.update(relative)
        h.update(len(data).to_bytes(8, "big")); h.update(data)
    return h.hexdigest()


def git_blob(commit: str, relative: str) -> bytes:
    cp = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=ROOT, capture_output=True, check=False)
    if cp.returncode:
        raise RuntimeError(f"accepted Git blob is unavailable: {relative}: {cp.stderr.decode(errors='replace').strip()}")
    return cp.stdout


def rendered_unit(commit: str, name: str, bundle: Path) -> bytes:
    text = git_blob(commit, f"cto-canary/systemd/{name}").decode()
    text = text.replace("@BUNDLE_DIR@", str(bundle / "cto-canary")).replace("@ROOT@", str(ROOT))
    return text.encode()


def verify_bundle(activation: dict[str, Any], unit_dir: Path | None = None) -> list[str]:
    """Bind bundle, manifest, project mode, and installed units to accepted Git objects."""
    errors: list[str] = []
    bundle = Path(activation["bundle_dir"])
    commit = activation["accepted_commit"]
    manifest_path = bundle / "manifest.json"
    if sha256(manifest_path) != activation["bundle_manifest_sha256"]:
        errors.append("installed bundle manifest digest differs from activation")
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError):
        return errors + ["installed bundle manifest is unreadable"]
    try:
        accepted_config = json.loads(git_blob(commit, "cto-canary/config.json"))
        expected_files = accepted_config["accepted_bundle_files"]
    except (RuntimeError, KeyError, json.JSONDecodeError) as exc:
        return errors + [f"accepted Git config/file set is unreadable: {exc}"]
    if (manifest.get("accepted_commit") != commit or manifest.get("decision_id") != activation["decision_id"] or
            manifest.get("acceptance_receipt_id") != activation["acceptance_receipt_id"] or
            set(manifest.get("files", {})) != set(expected_files)):
        errors.append("installed bundle manifest identity/file set is invalid")
    for relative in expected_files:
        try:
            accepted = git_blob(commit, relative)
        except RuntimeError as exc:
            errors.append(str(exc)); continue
        accepted_sha = hashlib.sha256(accepted).hexdigest()
        if manifest.get("files", {}).get(relative) != accepted_sha:
            errors.append(f"manifest is not bound to accepted Git blob: {relative}")
        if sha256(bundle / relative) != accepted_sha:
            errors.append(f"installed artifact differs from accepted Git blob: {relative}")
    try:
        accepted_mode_sha = hashlib.sha256(git_blob(commit, ".pi/modes/softwareco-cto-canary.json")).hexdigest()
    except RuntimeError as exc:
        errors.append(str(exc)); accepted_mode_sha = None
    if sha256(ROOT / ".pi/modes/softwareco-cto-canary.json") != accepted_mode_sha:
        errors.append("trusted-root CTO canary mode differs from accepted Git blob")
    unit_dir = unit_dir or Path.home() / ".config/systemd/user"
    for name in UNIT_NAMES:
        try:
            expected = rendered_unit(commit, name, bundle)
        except RuntimeError as exc:
            errors.append(str(exc)); continue
        installed = unit_dir / name
        if not installed.is_file() or installed.read_bytes() != expected:
            errors.append(f"installed systemd unit differs from accepted rendered template: {name}")
    return errors


def read_activation(path: Path, state_dir: Path, current_run_reserved: bool = False) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"activation gate unreadable: {exc}"]
    if not isinstance(value, dict) or set(value) != ACTIVATION_KEYS:
        return None, ["activation gate has wrong shape"]
    if value.get("schema_version") != 1 or value.get("state") != "active":
        errors.append("activation state is not active")
    decision_id = value.get("decision_id")
    if not isinstance(decision_id, int) or isinstance(decision_id, bool) or decision_id in (74, 77):
        errors.append("activation does not cite a separate decision")
    if value.get("activated_by") != "human-operator":
        errors.append("activation is not direct-human attributed")
    if not isinstance(value.get("accepted_commit"), str) or not HEX40.fullmatch(value["accepted_commit"]):
        errors.append("accepted commit is not a full lowercase Git hash")
    start, expiry = parse_time(value.get("started_at_utc")), parse_time(value.get("expires_at_utc"))
    now = datetime.now(timezone.utc)
    if start is None or expiry is None or expiry <= start:
        errors.append("activation time window is invalid")
    elif int((expiry - start).total_seconds()) != CONFIG["window_seconds"]:
        errors.append("activation window is not exactly 24 hours")
    elif not (start <= now < expiry):
        errors.append("activation window is not currently active")
    if value.get("max_cycles") != CONFIG["max_cycles"] or value.get("interval_seconds") != CONFIG["interval_seconds"]:
        errors.append("activation cycle bounds differ from accepted config")
    run_count = len([p for p in (state_dir / "runs").glob("*") if p.is_dir()]) if (state_dir / "runs").exists() else 0
    if run_count > CONFIG["max_cycles"] or (run_count == CONFIG["max_cycles"] and not current_run_reserved):
        errors.append("maximum canary cycle count reached")
    if errors:
        return value, errors

    try:
        decision = payload(json_command(["ak", "decision", "get", str(decision_id), "--machine"]))["decision"]
        acceptance = json_command(["ak", "governance", "show", str(value["acceptance_receipt_id"]), "--format", "json"])
        activation = json_command(["ak", "governance", "show", str(value["activation_receipt_id"]), "--format", "json"])
        chain = json_command(["ak", "governance", "list", "--concern", value["control_concern"], "--limit", "100", "--json"])
    except (RuntimeError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return value, [f"live AK activation readback failed: {exc}"]
    expected_rfc = str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md")
    if not (decision.get("outcome") == "accepted" and decision.get("state") == "unblocked" and
            decision.get("rfc_ref") == expected_rfc and
            decision.get("evidence_ref") == f"governance:{value['acceptance_receipt_id']}"):
        errors.append("live decision is not the exact accepted/unblocked canary decision")
    if not (acceptance.get("source_authority") == "human-operator" and acceptance.get("actor") == "human-operator" and
            acceptance.get("status") == "applied" and acceptance.get("to_state") == "accepted" and
            acceptance.get("agreement_ref") == f"decision:{decision_id}" and
            acceptance.get("details", {}).get("rfc_commit") == value["accepted_commit"]):
        errors.append("direct-human architecture acceptance receipt mismatch")
    details = activation.get("details", {})
    if not (activation.get("id") == value["activation_receipt_id"] and
            activation.get("concern") == value["control_concern"] and
            activation.get("source_authority") == "human-operator" and activation.get("actor") == "human-operator" and
            activation.get("status") == "applied" and activation.get("from_state") == "inactive" and
            activation.get("to_state") == f"active:{details.get('run_id')}" and
            activation.get("agreement_ref") == f"decision:{decision_id}" and
            details.get("schema") == "softwareco.autonomous-cto-canary-activation.v1" and
            details.get("accepted_commit") == value["accepted_commit"] and
            details.get("started_at_utc") == value["started_at_utc"] and details.get("expires_at_utc") == value["expires_at_utc"] and
            details.get("max_cycles") == CONFIG["max_cycles"] and details.get("interval_seconds") == CONFIG["interval_seconds"]):
        errors.append("direct-human canary activation receipt mismatch")
    if not isinstance(chain, list) or not chain or chain[-1].get("id") != value["activation_receipt_id"]:
        errors.append("canary control chain head is not the activation receipt")
    errors.extend(verify_bundle(value))
    modes_package = Path(CONFIG["pi_modes_package"])
    if directory_digest(modes_package) != CONFIG["pi_modes_package_digest"]:
        errors.append("installed pi-modes package differs from the reviewed pinned digest")
    pi_package = Path(CONFIG["pi_package"])
    if directory_digest(pi_package) != CONFIG["pi_package_digest"]:
        errors.append("installed Pi package differs from the reviewed pinned digest")
    version = run(["/usr/bin/node", CONFIG["pi_entrypoint"], "--version"]).stdout.strip()
    if version != CONFIG["pi_version"]:
        errors.append(f"Pi version drift: expected {CONFIG['pi_version']}, observed {version}")
    return value, errors


def watched_state(packet: dict[str, Any], db_path: Path) -> list[str]:
    drift: list[str] = []
    if packet.get("authority_db_before", {}).get("sha256") != sha256(db_path):
        drift.append("AK database bytes changed during cycle")
    for repo in packet.get("repositories", []):
        if not repo.get("exists"):
            continue
        path = Path(repo["registration"]["path"])
        probes = repo["probes"]
        for name, argv in (("git_head", ["git", "rev-parse", "HEAD"]),
                           ("git_status", ["git", "status", "--porcelain=v2", "--branch"])):
            current = run(argv, path)
            prior = probes[name].get("stdout")
            if current.returncode or current.stdout != prior:
                drift.append(f"watched repository {name} changed during cycle: {path}")
    return drift


def worker_argv() -> list[str]:
    extension = str(Path(CONFIG["pi_modes_package"]) / "extensions/mode.ts")
    return ["/usr/bin/node", CONFIG["pi_entrypoint"], *CONFIG["worker_arguments"], "--extension", extension]


def read_event(proc: subprocess.Popen[str], selector: selectors.BaseSelector, deadline: float) -> dict[str, Any]:
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("RPC deadline exceeded")
        if not selector.select(remaining):
            raise TimeoutError("RPC produced no complete line before deadline")
        assert proc.stdout
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError(f"RPC worker exited before response (code={proc.poll()})")
        try:
            return json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"RPC emitted invalid JSON: {exc}") from exc


def send(proc: subprocess.Popen[str], value: dict[str, Any]) -> None:
    assert proc.stdin
    proc.stdin.write(json.dumps(value, separators=(",", ":")) + "\n")
    proc.stdin.flush()


def mode_proof_errors(records: list[dict[str, Any]]) -> list[str]:
    mode_path = ROOT / ".pi/modes/softwareco-cto-canary.json"
    try:
        base_prompt = json.loads(mode_path.read_text())["systemPrompt"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        return [f"accepted mode is unreadable: {exc}"]
    expected_selection = {"baseKey": CONFIG["mode_base_key"], "overlayKeys": []}
    for value in records:
        components = value.get("components", [])
        component_ok = any(
            component.get("key") == CONFIG["mode_base_key"] and component.get("role") == "base" and
            component.get("strategy") == "replace_base" and component.get("scope") == "project" and
            component.get("path") == str(mode_path) and component.get("digest") == CONFIG["mode_component_digest"]
            for component in components
        )
        prompt = value.get("prompt")
        prompt_ok = (isinstance(prompt, str) and prompt.startswith(base_prompt) and "<project_context>" in prompt and
                     f"Current date: {datetime.now().date().isoformat()}" in prompt and
                     f"Current working directory: {ROOT}" in prompt)
        if value.get("selection") == expected_selection and component_ok and prompt_ok and not value.get("diagnostics"):
            return []
    return ["mode preview did not prove accepted project source, fingerprint, replace_base prompt, and dynamic context"]


def rpc_cycle(packet: dict[str, Any], stderr_path: Path, timeout: int) -> tuple[object, dict[str, Any]]:
    env = {key: os.environ[key] for key in ("HOME", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS") if key in os.environ}
    env.update({"PATH": "/usr/bin:/bin", "PI_MODES": json.dumps({"baseKey": CONFIG["mode_base_key"], "overlayKeys": []}, separators=(",", ":")),
                "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C", "TZ": "UTC", "TMPDIR": os.environ.get("TMPDIR", "/tmp")})
    argv = worker_argv()
    events: list[dict[str, Any]] = []
    violations: list[str] = []
    with stderr_path.open("w") as stderr:
        proc = subprocess.Popen(argv, cwd=ROOT, env=env, text=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=stderr, start_new_session=True)
        selector = selectors.DefaultSelector()
        assert proc.stdout
        selector.register(proc.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + timeout
        try:
            send(proc, {"id": "mode-preview", "type": "prompt", "message": "/mode-preview --json"})
            while True:
                event = read_event(proc, selector, deadline); events.append(event)
                if event.get("type") == "extension_error":
                    violations.append(f"extension error: {event.get('error')}")
                if event.get("id") == "mode-preview":
                    if event.get("success") is not True:
                        raise RuntimeError("mode preview command failed")
                    break
            prompt = (
                "Produce exactly one JSON object matching the CTO canary output schema below. "
                "Use only the supplied snapshot. Every factual reference must resolve as "
                "snapshot://portfolio.json#/... . Do not use tools, execute commands, dispatch, or cause effects.\n\n"
                f"OUTPUT SCHEMA:\n{(HERE / 'output.schema.json').read_text()}\n\n"
                f"PORTFOLIO SNAPSHOT:\n{json.dumps(packet, sort_keys=True)}"
            )
            send(proc, {"id": "cycle-prompt", "type": "prompt", "message": prompt})
            prompt_accepted = False
            settled = False
            while not settled:
                event = read_event(proc, selector, deadline); events.append(event)
                if event.get("id") == "cycle-prompt":
                    prompt_accepted = event.get("success") is True
                if event.get("type") == "extension_error":
                    violations.append(f"extension error: {event.get('error')}")
                if event.get("type") == "tool_execution_start":
                    violations.append(f"tool execution attempted: {event.get('toolName')}")
                if event.get("type") == "extension_ui_request":
                    violations.append(f"extension UI attempted: {event.get('method')}")
                    if event.get("method") in {"select", "confirm", "input", "editor"}:
                        send(proc, {"type": "extension_ui_response", "id": event["id"], "cancelled": True})
                if event.get("type") == "agent_settled":
                    settled = True
            if not prompt_accepted:
                raise RuntimeError("cycle prompt was not accepted")
            send(proc, {"id": "cycle-result", "type": "get_last_assistant_text"})
            result: object = None
            while True:
                event = read_event(proc, selector, deadline); events.append(event)
                if event.get("type") == "extension_error":
                    violations.append(f"extension error: {event.get('error')}")
                if event.get("id") == "cycle-result":
                    result = event.get("data", {}).get("text")
                    break
            if not isinstance(result, str):
                raise RuntimeError("worker returned no assistant text")
            try:
                proposal = json.loads(result)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"worker response was not an exact JSON object: {exc}") from exc
        finally:
            selector.close()
            if proc.poll() is None:
                try:
                    assert proc.stdin
                    proc.stdin.close()
                    proc.wait(timeout=10)
                except (subprocess.TimeoutExpired, BrokenPipeError):
                    os.killpg(proc.pid, signal.SIGTERM)
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait(timeout=5)
    status_records: list[dict[str, Any]] = []
    for line in stderr_path.read_text(errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "selection" in value:
            status_records.append(value)
    violations.extend(mode_proof_errors(status_records))
    return proposal, {"pid": proc.pid, "argv": argv, "events": events, "violations": violations,
                      "mode_status_records": status_records}


def fixture_cycle() -> tuple[object, dict[str, Any]]:
    """Exercise the RPC framing with a distinct deterministic no-model worker process."""
    argv = [sys.executable, str(HERE / "fixture_rpc_worker.py")]
    proc = subprocess.Popen(argv, cwd=ROOT, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    send(proc, {"id": "fixture-prompt", "type": "prompt", "message": "fixture"})
    events = [json.loads(proc.stdout.readline()) for _ in range(3)]
    send(proc, {"id": "fixture-result", "type": "get_last_assistant_text"})
    result_event = json.loads(proc.stdout.readline()); events.append(result_event)
    proposal = json.loads(result_event["data"]["text"])
    pid = proc.pid
    proc.stdin.close(); proc.wait(timeout=5)
    return proposal, {"pid": pid, "argv": argv, "events": events, "violations": [], "mode_status_records": []}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true", help="deterministic no-model implementation test; never a live canary")
    parser.add_argument("--state-dir", type=Path, default=None)
    parser.add_argument("--activation-file", type=Path, default=None)
    parser.add_argument("--timeout", type=int, default=CONFIG["cycle_timeout_seconds"])
    args = parser.parse_args()
    state = args.state_dir or Path(os.environ.get("STATE_DIRECTORY", Path.home() / ".local/state/softwareco-cto-canary"))
    state.mkdir(parents=True, exist_ok=True)
    activation_file = args.activation_file or state / "activation.json"

    activation: dict[str, Any] | None = None
    if not args.fixture:
        activation, gate_errors = read_activation(activation_file, state)
        if gate_errors:
            print("REFUSED: " + "; ".join(gate_errors), file=sys.stderr)
            return 3

    lock_file = (state / "cycle.lock").open("w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("REFUSED: a cycle is already running", file=sys.stderr)
        return 4
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run_dir = state / "runs" / run_id
    run_dir.mkdir(parents=True)
    packet_path = run_dir / "portfolio.json"
    db_path = Path(os.path.expanduser(os.environ.get("AK_DB", "~/ai-society/society.v2.db")))

    if args.fixture:
        packet = {"schema_version": 2, "authority": "fixture",
                  "coverage": {"registered_repos_expected": 2, "registered_repos_observed": 2,
                               "complete": True, "gaps": [], "filesystem_git_roots_not_registered": [],
                               "registered_paths_without_git_marker": []},
                  "repositories": [], "authority_db_before": {"sha256": sha256(db_path)}}
        packet_path.write_text(json.dumps(packet) + "\n")
        proposal, trace = fixture_cycle()
    else:
        cp = subprocess.run([sys.executable, str(HERE / "collect_snapshot.py"), "--output", str(packet_path)], cwd=ROOT)
        if cp.returncode:
            return cp.returncode
        packet = json.loads(packet_path.read_text())
        activation, gate_errors = read_activation(activation_file, state, current_run_reserved=True)
        if gate_errors or activation is None:
            (run_dir / "failure.txt").write_text("authority changed before worker start: " + "; ".join(gate_errors) + "\n")
            print("REFUSED: authority changed before worker start: " + "; ".join(gate_errors), file=sys.stderr)
            return 3
        expiry = parse_time(activation["expires_at_utc"])
        assert expiry is not None
        remaining = int((expiry - datetime.now(timezone.utc)).total_seconds()) - CONFIG["expiry_guard_seconds"]
        worker_timeout = min(args.timeout, remaining)
        if worker_timeout < 1:
            (run_dir / "failure.txt").write_text("insufficient authority time remains for a worker\n")
            print("REFUSED: insufficient authority time remains for a worker", file=sys.stderr)
            return 3
        try:
            proposal, trace = rpc_cycle(packet, run_dir / "worker.stderr", worker_timeout)
        except Exception as exc:
            (run_dir / "failure.txt").write_text(f"{type(exc).__name__}: {exc}\n")
            print(f"cycle failed closed: {exc}", file=sys.stderr)
            return 2

    errors = validate(proposal, packet)
    proposal_coverage = proposal.get("coverage", {}) if isinstance(proposal, dict) else {}
    packet_coverage = packet.get("coverage", {})
    for key in ("registered_repos_expected", "registered_repos_observed", "complete", "gaps"):
        if proposal_coverage.get(key) != packet_coverage.get(key):
            errors.append(f"coverage does not match snapshot: {key}")
    drift = [] if args.fixture else watched_state(packet, db_path)
    if not args.fixture:
        _, final_gate_errors = read_activation(activation_file, state, current_run_reserved=True)
        trace["violations"].extend(f"post-cycle authority gate: {error}" for error in final_gate_errors)
    verified = not errors and not drift and not trace["violations"]
    result = {
        "schema_version": 2, "canonical": False, "classification": "proposal_only", "run_id": run_id,
        "fresh_worker_pid": trace["pid"], "worker_argv": trace["argv"], "proposal": proposal,
        "validation_errors": errors, "watched_state_changes": drift,
        "runtime_policy_violations": trace["violations"], "verified_behavior": verified,
        "verification_scope": "output contract, accepted runtime gate, mode composition, disabled tools/extensions, and watched AK/Git before-after checks; not proof of all external effects",
    }
    (run_dir / "rpc-events.json").write_text(json.dumps(trace["events"], indent=2) + "\n")
    (run_dir / "mode-preview.json").write_text(json.dumps(trace["mode_status_records"], indent=2) + "\n")
    (run_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run_dir": str(run_dir), "verified_behavior": verified,
                      "validation_errors": errors, "watched_state_changes": drift,
                      "runtime_policy_violations": trace["violations"]}, sort_keys=True))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
