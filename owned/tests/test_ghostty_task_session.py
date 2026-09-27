"""Isolated process tests: no real AK, terminal, Pi, provider or focus execution."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts/launch-pi-ak-task-ghostty.sh"

# Every runtime-bearing dependency is a synthetic executable. Do not execute
# the Ghostty shell payload: these tests prove the gate and legacy argv only.
STUB = """#!/usr/bin/env python3
import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
with open(os.environ['TEST_EVENTS'], 'a') as f:
    f.write(json.dumps({'name': name, 'args': sys.argv[1:]}) + '\\n')
if name == 'ak':
    print(json.dumps({'repo': os.environ['TEST_REPO'],
                      'title': 'Synthetic task', 'status': 'ready'}))
"""


class IsolatedLauncherTest(unittest.TestCase):
    def setUp(self):
        scratch = os.environ.get("TMPDIR")
        if not scratch:
            self.fail("TMPDIR must name owned scratch; no /tmp fallback")
        self.tmp = tempfile.TemporaryDirectory(prefix="lane-task-session-", dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.events = self.base / "events.jsonl"
        self.logs = self.base / "must-not-create"
        self.repo = self.base / "synthetic-repo"
        self.repo.mkdir()
        for name in ("python3", "bash", "cat", "env"):
            (self.bin / name).symlink_to(shutil.which(name))
        for name in ("ak", "ghostty", "pi", "niri", "mkdir", "date", "sleep", "basename"):
            path = self.bin / name
            path.write_text(STUB)
            path.chmod(0o755)
        # Do not inherit caller runtime/config overrides into this test.
        self.env = {
            "PATH": str(self.bin), "HOME": str(self.base), "TMPDIR": str(self.base),
            "AK_WRAPPER": str(self.bin / "ak"), "TEST_EVENTS": str(self.events),
            "TEST_REPO": str(self.repo), "LC_ALL": "C.UTF-8",
            "PI_AK_TASK_GHOSTTY_LOG_ROOT": str(self.logs),
        }

    def run_launcher(self, *args):
        return subprocess.run(
            [str(self.bin / "bash"), str(LAUNCHER), *args],
            cwd=self.repo, env=self.env, text=True, capture_output=True, timeout=5,
        )

    def recorded(self):
        if not self.events.exists():
            return []
        return [json.loads(line) for line in self.events.read_text().splitlines()]

    def assert_no_effects(self):
        self.assertEqual(self.recorded(), [])
        self.assertFalse(self.logs.exists())
        self.assertFalse((self.base / ".pi").exists())


class LegacyGateTests(IsolatedLauncherTest):
    def test_standalone_help_is_db_free(self):
        for flag in ("--help", "-h"):
            with self.subTest(flag=flag):
                result = self.run_launcher(flag)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Affected or unknown", result.stdout)
                self.assert_no_effects()

    def test_missing_producer_refuses_entire_request(self):
        for args in (
            ("1",), ("1", "2"), ("--justfile-rollout-pilots",),
            ("1", "--justfile-rollout-pilots", "999"),
            ("--dry-run", "1"), ("--focus-last", "1", "2"),
            ("--interactive", "1"), ("--print", "--hold-open", "1"),
            ("--no-hold-open", "1"), ("--log-dir", str(self.logs), "1"),
            ("9007199254740991",), tuple(str(i) for i in range(1, 257)),
        ):
            with self.subTest(args=args):
                result = self.run_launcher(*args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("classification unavailable", result.stderr)
                self.assert_no_effects()

    def test_strict_whole_request_parsing(self):
        for args in (
            (), ("0",), ("01",), ("-1",), ("1.0",), ("task1",), ("1;touch nope",),
            ("1\n2",), ("9007199254740992",), ("9" * 1000,),
            tuple(str(i) for i in range(1, 258)),
            ("--unknown", "1"), ("--", "1"), ("1", "1"),
            ("--interactive", "--print", "1"), ("--print", "--interactive", "1"),
            ("--interactive", "--interactive", "1"),
            ("--hold-open", "--no-hold-open", "1"),
            ("--no-hold-open", "--hold-open", "1"),
            ("--hold-open", "--hold-open", "1"),
            ("--no-hold-open", "--no-hold-open", "1"),
            ("--print", "--print", "1"),
            ("--focus-last", "--focus-last", "1"),
            ("--dry-run", "--dry-run", "1"),
            ("--log-dir",), ("--log-dir", "", "1"),
            ("--log-dir", "--focus-last", "1"),
            ("--log-dir", "a", "--log-dir", "b", "1"),
            ("--justfile-rollout-pilots", "609"),
            ("--justfile-rollout-pilots", "--justfile-rollout-pilots"),
            ("--help", "1"), ("1", "--help"),
        ):
            with self.subTest(args=args):
                result = self.run_launcher(*args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assert_no_effects()

    def test_classifier_does_not_import_checkout_or_pythonpath_modules(self):
        for name in ("json", "hashlib", "selectors", "sitecustomize"):
            (self.repo / (name + ".py")).write_text(
                "from pathlib import Path\nPath(" + repr(str(self.events)) + ").write_text('import effect')\n"
            )
        self.env["PYTHONPATH"] = str(self.repo)
        result = self.run_launcher("1")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assert_no_effects()
        self.assertFalse((self.repo / "__pycache__").exists())

    def test_runtime_overrides_do_not_bypass_classification(self):
        self.env.update({
            "AK_WRAPPER": str(self.base / "missing-ak"),
            "PI_TARGET_REPO": str(self.repo), "PI_LAUNCH_PROMPT": "not authority",
            "XDG_CONFIG_HOME": str(self.base / "empty-config"),
            "XDG_STATE_HOME": str(self.base / "empty-state"),
        })
        for name in ("ghostty", "pi", "niri"):
            (self.bin / name).unlink()
        result = self.run_launcher("--focus-last", "--log-dir", str(self.logs), "1")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("classification unavailable", result.stderr)
        self.assert_no_effects()


if __name__ == "__main__":
    unittest.main()
