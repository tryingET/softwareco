from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cto-canary"))
from validate_output import validate
from fixture_rpc_worker import PROPOSAL
from collect_snapshot import registered_under_owned
from run_cycle import CONFIG, UNIT_NAMES, mode_proof_errors, read_activation, rendered_unit, verify_bundle


class CanaryContractTests(unittest.TestCase):
    def test_mode_owns_base_and_preset_is_exact(self):
        mode = json.loads((ROOT / ".pi/modes/softwareco-cto-canary.json").read_text())
        preset = json.loads((ROOT / ".pi/mode-presets/softwareco-cto-canary.json").read_text())
        self.assertEqual(mode["promptStrategy"], "replace_base")
        self.assertEqual(preset["selection"], {"baseKey": "softwareco-cto-canary", "overlayKeys": []})
        for required in ("AGENTS/CLAUDE", "skills", "date", "cwd", "append-system", "selected overlays"):
            self.assertIn(required, mode["systemPrompt"])
        self.assertIn("never self-dispatch", mode["systemPrompt"])

    def test_config_is_exactly_24_hours_and_24_cycles(self):
        config = json.loads((ROOT / "cto-canary/config.json").read_text())
        self.assertEqual(config["window_seconds"], 86_400)
        self.assertEqual(config["interval_seconds"], 3_600)
        self.assertEqual(config["max_cycles"], 24)
        arguments = config["worker_arguments"]
        for required in ("--no-session", "--no-tools", "--no-skills", "--no-prompt-templates",
                         "--no-themes", "--no-extensions", "--offline"):
            self.assertIn(required, arguments)

    def test_timer_and_expiry_timer_are_bounded(self):
        timer = (ROOT / "cto-canary/systemd/softwareco-cto-canary.timer").read_text()
        stop = (ROOT / "cto-canary/systemd/softwareco-cto-canary-stop.timer").read_text()
        self.assertIn("OnUnitActiveSec=1h", timer)
        self.assertIn("Persistent=false", timer)
        self.assertIn("OnActiveSec=24h", stop)
        self.assertIn("Persistent=false", stop)

    def test_valid_fixture_proposal_resolves_snapshot_refs(self):
        snapshot = {"authority": "fixture", "coverage": {"complete": True}}
        self.assertEqual(validate(PROPOSAL, snapshot), [])

    def test_authority_and_dispatch_fail_closed(self):
        proposal = json.loads(json.dumps(PROPOSAL))
        proposal["authority_claimed"] = True
        proposal["attempted_effects"] = ["ak task create"]
        proposal["escalation"]["self_dispatched"] = True
        errors = validate(proposal, {"authority": "fixture", "coverage": {}})
        self.assertTrue(any("authority" in error for error in errors))
        self.assertTrue(any("dispatch" in error for error in errors))

    def test_missing_or_unresolved_evidence_fails_closed(self):
        proposal = json.loads(json.dumps(PROPOSAL))
        proposal["theses"][0]["evidence_refs"] = ["snapshot://portfolio.json#/missing"]
        self.assertTrue(any("resolve" in error for error in validate(proposal, {"authority": "fixture", "coverage": {}})))

    def test_boolean_count_and_bad_draft_fail_closed(self):
        proposal = json.loads(json.dumps(PROPOSAL))
        proposal["coverage"]["registered_repos_expected"] = True
        proposal["drafts"]["ak_tasks"] = [{}]
        errors = validate(proposal, {"authority": "fixture", "coverage": {}})
        self.assertTrue(any("expected count" in error for error in errors))
        self.assertTrue(any("drafts.ak_tasks" in error for error in errors))

    def test_production_cycle_refuses_without_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            cp = subprocess.run([sys.executable, str(ROOT / "cto-canary/run_cycle.py"),
                                 "--state-dir", tmp, "--activation-file", str(Path(tmp) / "absent.json")],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 3)
        self.assertIn("REFUSED", cp.stderr)

    def test_deterministic_manual_fixture_cycles_are_noncanonical_and_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, str(ROOT / "cto-canary/run_cycle.py"), "--fixture",
                       "--state-dir", tmp, "--timeout", "20"]
            first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual((first.returncode, second.returncode), (0, 0), first.stderr + second.stderr)
            runs = sorted((Path(tmp) / "runs").iterdir())
            one = json.loads((runs[0] / "result.json").read_text())
            two = json.loads((runs[1] / "result.json").read_text())
            self.assertTrue(one["verified_behavior"] and two["verified_behavior"])
            self.assertNotEqual(one["fresh_worker_pid"], two["fresh_worker_pid"])
            self.assertFalse(one["canonical"])
            self.assertTrue(one["worker_argv"][-1].endswith("fixture_rpc_worker.py"))

    def test_expiry_math_is_exact(self):
        start = datetime.now(timezone.utc)
        expiry = start + timedelta(seconds=json.loads((ROOT / "cto-canary/config.json").read_text())["window_seconds"])
        self.assertEqual(int((expiry - start).total_seconds()), 86_400)

    def test_registered_path_escape_and_symlink_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); owned = base / "owned"; owned.mkdir()
            outside = base / "outside"; outside.mkdir()
            (owned / "link").symlink_to(outside, target_is_directory=True)
            inventory = [
                {"path": str(owned / "valid")},
                {"path": str(owned / ".." / "outside")},
                {"path": str(owned / "link")},
            ]
            accepted, rejected = registered_under_owned(inventory, owned)
        self.assertEqual([Path(item["path"]).name for item in accepted], ["valid"])
        self.assertEqual(len(rejected), 2)

    def test_mode_proof_binds_source_fingerprint_prompt_and_dynamic_context(self):
        mode_path = ROOT / ".pi/modes/softwareco-cto-canary.json"
        base = json.loads(mode_path.read_text())["systemPrompt"]
        record = {
            "selection": {"baseKey": "softwareco-cto-canary", "overlayKeys": []},
            "components": [{"key": "softwareco-cto-canary", "role": "base", "strategy": "replace_base",
                            "scope": "project", "path": str(mode_path), "digest": CONFIG["mode_component_digest"]}],
            "prompt": base + "\n<project_context>\nCurrent date: " + datetime.now().date().isoformat() +
                      "\nCurrent working directory: " + str(ROOT),
            "diagnostics": [],
        }
        self.assertEqual(mode_proof_errors([record]), [])
        record["components"][0]["path"] = "/wrong/mode.json"
        self.assertTrue(mode_proof_errors([record]))

    def test_expired_activation_refuses_before_live_ak_readback(self):
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=25); expiry = start + timedelta(hours=24)
        activation = {
            "schema_version": 1, "state": "active", "decision_id": 83,
            "acceptance_receipt_id": 1, "activation_receipt_id": 2,
            "accepted_commit": "a" * 40, "bundle_dir": "/missing", "bundle_manifest_sha256": "b" * 64,
            "started_at_utc": start.isoformat(), "expires_at_utc": expiry.isoformat(),
            "max_cycles": 24, "interval_seconds": 3600, "activated_by": "human-operator",
            "control_concern": "fixture",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "activation.json"; path.write_text(json.dumps(activation))
            _, errors = read_activation(path, Path(tmp))
        self.assertTrue(any("not currently active" in error for error in errors))

    def test_service_hides_home_and_stop_kills_inflight_worker(self):
        service = (ROOT / "cto-canary/systemd/softwareco-cto-canary.service").read_text()
        stop = (ROOT / "cto-canary/stop_candidate.py").read_text()
        self.assertIn("ProtectHome=tmpfs", service)
        self.assertIn("KillMode=control-group", service)
        self.assertIn('"stop", "softwareco-cto-canary.service"', stop)

    def test_installer_clean_scope_includes_decision_and_plans(self):
        source = (ROOT / "cto-canary/activate_candidate.py").read_text()
        self.assertIn("docs/decisions/2026-07-26-softwareco-autonomous-cto-canary.md", source)
        self.assertIn("docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md", source)
        self.assertIn("tests/test_cto_canary.py", source)

    def test_bundle_and_units_bind_to_git_not_rewritten_manifest(self):
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                                capture_output=True, check=True).stdout.strip()
        accepted_config = json.loads(subprocess.run(
            ["git", "show", f"{commit}:cto-canary/config.json"], cwd=ROOT,
            text=True, capture_output=True, check=True).stdout)
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"; units = Path(tmp) / "units"; units.mkdir()
            hashes = {}
            for relative in accepted_config["accepted_bundle_files"]:
                data = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=ROOT,
                                      capture_output=True, check=True).stdout
                target = bundle / relative; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
                hashes[relative] = hashlib.sha256(data).hexdigest()
            manifest = {"schema_version": 1, "accepted_commit": commit, "decision_id": 83,
                        "acceptance_receipt_id": 999, "files": hashes}
            manifest_path = bundle / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, sort_keys=True))
            for name in UNIT_NAMES:
                (units / name).write_bytes(rendered_unit(commit, name, bundle))
            activation = {"bundle_dir": str(bundle), "accepted_commit": commit, "decision_id": 83,
                          "acceptance_receipt_id": 999,
                          "bundle_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
            self.assertEqual(verify_bundle(activation, units), [])
            target = bundle / "cto-canary/run_cycle.py"; target.write_text("tampered\n")
            manifest["files"]["cto-canary/run_cycle.py"] = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest, sort_keys=True))
            activation["bundle_manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            self.assertTrue(any("accepted Git blob" in error for error in verify_bundle(activation, units)))


if __name__ == "__main__":
    unittest.main()
