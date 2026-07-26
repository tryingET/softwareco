from __future__ import annotations

from datetime import datetime, timedelta, timezone
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


if __name__ == "__main__":
    unittest.main()
