from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cto-canary"))
from validate_output import validate
from fixture_rpc_worker import PROPOSAL
from collect_snapshot import registered_under_owned, run as collector_run
from run_cycle import CONFIG, expected_composed_prompt, mode_proof_errors, prior_cost, read_activation
from runtime_integrity import UNIT_NAMES, directory_digest, rendered_unit, runtime_packages, verify_bundle
from start_candidate import acceptance_errors


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

        self.assertEqual((config["model_provider"], config["model_id"]), ("openai-codex", "gpt-5.6-sol"))
        self.assertGreater(config["max_cost_usd_per_cycle"], 0)
        self.assertGreater(config["max_cost_usd_total"], config["max_cost_usd_per_cycle"])
        self.assertGreaterEqual(config["expiry_guard_seconds"], 30)

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

    def test_install_and_start_require_explicit_human_acknowledgement_flags(self):
        install = subprocess.run([sys.executable, str(ROOT / "cto-canary/activate_candidate.py"),
                                  "--decision-id", "83", "--acceptance-receipt-id", "1",
                                  "--accepted-commit", "a" * 40], cwd=ROOT, text=True, capture_output=True)
        start = subprocess.run([sys.executable, str(ROOT / "cto-canary/start_candidate.py"),
                                "--decision-id", "83", "--acceptance-receipt-id", "1",
                                "--accepted-commit", "a" * 40], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual((install.returncode, start.returncode), (3, 3))
        self.assertIn("REFUSED", install.stderr); self.assertIn("REFUSED", start.stderr)

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
        record = {
            "selection": {"baseKey": "softwareco-cto-canary", "overlayKeys": []},
            "components": [{"key": "softwareco-cto-canary", "role": "base", "strategy": "replace_base",
                            "scope": "project", "path": str(mode_path), "digest": CONFIG["mode_component_digest"]}],
            "prompt": expected_composed_prompt(),
            "diagnostics": [],
        }
        self.assertEqual(mode_proof_errors([record]), [])
        record["components"][0]["path"] = "/wrong/mode.json"
        self.assertTrue(mode_proof_errors([record]))
        record["components"][0]["path"] = str(mode_path)
        record["prompt"] += "\nunreviewed injection"
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

        self.assertIn("BindReadOnlyPaths=%h/ai-society/society.v2.db", service)

    def test_expiry_stop_verifies_inflight_service_termination(self):
        activation = {"state": "active", "expires_at_utc": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
                      "control_concern": "fixture", "activation_receipt_id": 1, "decision_id": 83}
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); state = home / ".local/state/softwareco-cto-canary"; state.mkdir(parents=True)
            (state / "activation.json").write_text(json.dumps(activation))
            bindir = home / "bin"; bindir.mkdir(); fake = bindir / "systemctl"
            fake.write_text("#!/bin/sh\ncase \"$*\" in\n  *\"stop softwareco-cto-canary.service\"*) [ \"$FAKE_STOP_FAIL\" = 1 ] && exit 1 || exit 0;;\n  *\"show softwareco-cto-canary.service --property=ActiveState\"*) [ \"$FAKE_ACTIVE\" = 1 ] && echo active || echo inactive; exit 0;;\n  *\"show softwareco-cto-canary.service --property=ControlGroup\"*) echo ''; exit 0;;\n  *\"show softwareco-cto-canary.timer --property=ActiveState\"*|*\"show softwareco-cto-canary-stop.timer --property=ActiveState\"*) echo inactive; exit 0;;\n  *\"is-enabled\"*) echo disabled; exit 1;;\n  *\"disable --now\"*) exit 0;;\n  *) exit 0;;\nesac\n")
            fake.chmod(0o755)
            env = os.environ.copy(); env.update({"HOME": str(home), "PATH": str(bindir) + ":/usr/bin", "FAKE_ACTIVE": "1", "FAKE_STOP_FAIL": "0"})
            failed = subprocess.run([sys.executable, str(ROOT / "cto-canary/stop_candidate.py"), "--expiry"],
                                    cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(json.loads((state / "activation.json").read_text())["state"], "active")
            env["FAKE_ACTIVE"] = "0"
            passed = subprocess.run([sys.executable, str(ROOT / "cto-canary/stop_candidate.py"), "--expiry"],
                                    cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertEqual(json.loads((state / "activation.json").read_text())["state"], "expired_by_time")

    def test_runtime_digest_rejects_external_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"; root.mkdir(); outside = Path(tmp) / "outside"; outside.write_text("x")
            (root / "escape").symlink_to(outside)
            with self.assertRaises(RuntimeError):
                directory_digest(root)

    def test_installed_runtime_never_falls_back_to_shared_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp); (bundle / "manifest.json").write_text("{}")
            with self.assertRaisesRegex(RuntimeError, "missing an isolated"):
                runtime_packages(bundle)
    def test_collector_output_limit_is_enforced_by_bounded_pipe_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = collector_run([sys.executable, "-c", "import os; os.write(1, b'x'*2100000)"], Path(tmp), 20)
        self.assertTrue(result["oversized"] or result["exit_code"] != 0)

    def test_prior_cost_is_normalized_and_malformed_history_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp); prior = state / "runs/one"; current = state / "runs/two"
            prior.mkdir(parents=True); current.mkdir()
            (prior / "result.json").write_text(json.dumps({"usage": {"cost": 1.25}}))
            self.assertEqual(prior_cost(state, current), (1.25, []))
            (prior / "result.json").write_text("{}")
            self.assertTrue(prior_cost(state, current)[1])
            (prior / "result.json").write_text(json.dumps({"usage": {"cost": float("nan")}}))
            self.assertTrue(prior_cost(state, current)[1])

    def test_installer_clean_scope_includes_decision_and_plans(self):
        source = (ROOT / "cto-canary/activate_candidate.py").read_text()
        self.assertIn("docs/decisions/2026-07-26-softwareco-autonomous-cto-canary.md", source)
        self.assertIn("docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md", source)
        self.assertIn("tests/test_cto_canary.py", source)
        start_source = (ROOT / "cto-canary/start_candidate.py").read_text()
        self.assertIn("Run python3", start_source)

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
                        "acceptance_receipt_id": 999, "files": hashes,
                        "runtime_digests": {
                            accepted_config["runtime_pi_package_relative"]: accepted_config["pi_package_digest"],
                            accepted_config["runtime_pi_modes_package_relative"]: accepted_config["pi_modes_package_digest"]}}
            manifest_path = bundle / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, sort_keys=True))
            for name in UNIT_NAMES:
                (units / name).write_bytes(rendered_unit(commit, name, bundle))
            activation = {"bundle_dir": str(bundle), "accepted_commit": commit, "decision_id": 83,
                          "acceptance_receipt_id": 999,
                          "bundle_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
            self.assertEqual(verify_bundle(activation, units, verify_runtime=False), [])
            unit = units / "softwareco-cto-canary.service"; original_unit = unit.read_bytes(); unit.write_text("tampered\n")
            self.assertTrue(any("systemd unit" in error for error in verify_bundle(activation, units, verify_runtime=False)))
            unit.write_bytes(original_unit)
            target = bundle / "cto-canary/run_cycle.py"; target.write_text("tampered\n")
            manifest["files"]["cto-canary/run_cycle.py"] = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest, sort_keys=True))
            activation["bundle_manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            self.assertTrue(any("accepted Git blob" in error for error in verify_bundle(activation, units, verify_runtime=False)))

    def test_activation_authority_contract_rejects_state_actor_and_commit_drift(self):
        decision_id, receipt_id, commit = 83, 999, "a" * 40
        decision = {"outcome": "accepted", "state": "unblocked",
                    "rfc_ref": str(ROOT / "docs/project/2026-07-26-softwareco-autonomous-cto-canary-rfc.md"),
                    "evidence_ref": f"governance:{receipt_id}"}
        receipt = {"source_authority": "human-operator", "actor": "human-operator", "status": "applied",
                   "to_state": "accepted", "agreement_ref": f"decision:{decision_id}",
                   "details": {"schema": "softwareco.architecture-decision-acceptance.v1",
                               "decision_id": decision_id, "rfc_commit": commit}}
        self.assertEqual(acceptance_errors(decision, receipt, decision_id, receipt_id, commit), [])
        decision["state"] = "blocked"; receipt["actor"] = "agent"; receipt["details"]["rfc_commit"] = "b" * 40
        errors = acceptance_errors(decision, receipt, decision_id, receipt_id, commit)
        self.assertEqual(set(errors), {"decision unblocked", "human actor", "accepted commit"})


if __name__ == "__main__":
    unittest.main()
