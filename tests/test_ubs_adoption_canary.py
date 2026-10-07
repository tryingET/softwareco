"""Feature: scripts/ubs-adoption-canary.py refuses a UBS candidate that real consumer files stall.

UBS 5.4.18 passed its suite and the refusal-count checks, was pinned into the service worktree
that every repo's pre-commit runs, and within hours livelocked on ordinary find-first loops in
workstation and test-capabilities files (AK6750, AK6781). Before a re-pin, the canary scans each
consumer repo's tracked JS/TS and Python with the incumbent and the candidate and refuses the
candidate when it does not finish where the incumbent does, or is much slower.

Scenarios are written Given/When/Then.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CANARY = REPO_ROOT / "scripts" / "ubs-adoption-canary.py"

# A stand-in for `ubs --ci --no-cargo --only=<lang> --format=json .`, tuned per role.
STUB = """#!/usr/bin/env sh
role="$(basename "$0")"
eval "delay=\\${STUB_${role}_SLEEP:-0}; status=\\${STUB_${role}_STATUS:-ok}; criticals=\\${STUB_${role}_CRITICAL:-0}"
printf '%s %s in %s\\n' "$role" "$*" "$PWD" >>"$STUB_LOG"
sleep "$delay"
findings=""
i=0
while [ "$i" -lt "$criticals" ]; do
  [ -z "$findings" ] || findings="$findings,"
  findings="$findings{\\"rule_id\\":\\"js.taint.xss\\",\\"severity\\":\\"critical\\",\\"file\\":\\"$PWD/a.js\\",\\"line\\":$((i + 1)),\\"suppressed\\":false}"
  i=$((i + 1))
done
printf '{"status":"%s","failed_modules":[],"totals":{"critical":%s},"findings":[%s]}' "$status" "$criticals" "$findings"
"""


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and not k.startswith("STUB_")}


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
                          env=clean_env()).stdout


class UbsAdoptionCanaryFeature(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ubs-canary-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.log = self.tmp / "calls.log"
        for role in ("incumbent", "candidate"):
            stub = self.tmp / role
            stub.write_text(STUB)
            stub.chmod(0o755)
        self.workspace = self.tmp / "workspace"
        self.consumer = self.make_repo("consumer", hook="exec /x/softwareco/scripts/ubs-staged.sh\n")

    def make_repo(self, name: str, hook: str | None) -> Path:
        repo = self.workspace / name
        repo.mkdir(parents=True)
        git(repo, "init", "-q")
        (repo / "a.js").write_text("export const a = 1;\n")
        (repo / "b.py").write_text("B = 1\n")
        (repo / "notes.md").write_text("not scanned\n")
        git(repo, "add", ".")
        git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
        if hook is not None:
            hooks = repo / ".git" / "hooks"
            hooks.mkdir(exist_ok=True)
            (hooks / "pre-commit").write_text("#!/bin/sh\n" + hook)
        return repo

    def run_canary(self, *args: str, **stub_env: str) -> subprocess.CompletedProcess:
        env = {**clean_env(), "STUB_LOG": str(self.log), **stub_env}
        report = self.tmp / "report.json"
        result = subprocess.run(
            [sys.executable, str(CANARY), "--incumbent", str(self.tmp / "incumbent"),
             "--candidate", str(self.tmp / "candidate"), "--root", str(self.workspace),
             "--scratch", str(self.tmp / "scratch"), "--report", str(report), *args],
            capture_output=True, text=True, env=env, timeout=120)
        self.report = json.loads(report.read_text()) if report.exists() else None
        return result

    def test_a_candidate_that_behaves_like_the_incumbent_passes(self) -> None:
        # Given a candidate as fast and as complete as the incumbent
        # When the canary scans the consumer repo
        result = self.run_canary()
        # Then it passes and records both scans per language
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.report["verdict"], "pass")
        langs = sorted(row["lang"] for row in self.report["scans"])
        self.assertEqual(langs, ["js", "python"])
        self.assertIn("consumer", result.stdout)

    def test_a_much_slower_candidate_is_refused(self) -> None:
        # Given a candidate six times slower than the incumbent, above the time floor
        result = self.run_canary("--floor", "0.1", "--max-slowdown", "5",
                                 STUB_incumbent_SLEEP="0.2", STUB_candidate_SLEEP="1.3")
        # Then the canary refuses and names the repo, the language and the slowdown
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.report["verdict"], "refuse")
        reasons = [r for row in self.report["scans"] for r in row["refusals"]]
        self.assertTrue(any("slower" in reason for reason in reasons), reasons)
        self.assertIn("consumer", result.stdout)

    def test_a_slowdown_inside_the_floor_is_not_refused(self) -> None:
        # Given a candidate slower in ratio but faster than the floor in absolute time
        result = self.run_canary("--floor", "2", "--max-slowdown", "5",
                                 STUB_incumbent_SLEEP="0.05", STUB_candidate_SLEEP="0.4")
        # Then the ratio alone does not refuse it
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_a_candidate_that_does_not_finish_is_refused(self) -> None:
        # Given a candidate that runs past the per-scan timeout
        result = self.run_canary("--timeout", "1", STUB_candidate_SLEEP="5")
        # Then the canary refuses: the pre-commit would hit its module timeout
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        reasons = [r for row in self.report["scans"] for r in row["refusals"]]
        self.assertTrue(any("did not finish" in reason for reason in reasons), reasons)

    def test_a_candidate_reporting_a_partial_scan_is_refused(self) -> None:
        # Given a candidate whose scan reports partial where the incumbent's is complete
        result = self.run_canary(STUB_candidate_STATUS="partial")
        # Then the canary refuses: ubs-staged refuses a partial scan
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        reasons = [r for row in self.report["scans"] for r in row["refusals"]]
        self.assertTrue(any("partial" in reason for reason in reasons), reasons)

    def test_dropped_criticals_are_reported_without_refusing(self) -> None:
        # Given a candidate that reports fewer criticals than the incumbent
        result = self.run_canary(STUB_incumbent_CRITICAL="3", STUB_candidate_CRITICAL="1")
        # Then it passes (findings legitimately change across releases) but lists the drop,
        # because a solver that stops early also loses findings (AK6781)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        dropped = [row["criticals_dropped"] for row in self.report["scans"] if row["lang"] == "js"]
        self.assertEqual(dropped, [2])
        self.assertIn("dropped", result.stdout)

    def test_only_repos_whose_pre_commit_runs_the_service_scanner_are_scanned(self) -> None:
        # Given a second repo without a UBS hook and a third that runs the service worktree directly
        self.make_repo("unhooked", hook=None)
        self.make_repo("gate", hook="UBS=$HOME/softwareco/contrib/ultimate_bug_scanner-local/ubs\n")
        # When the canary discovers consumers
        result = self.run_canary()
        # Then only the hooked repos are scanned
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        repos = sorted({Path(row["repo"]).name for row in self.report["scans"]})
        self.assertEqual(repos, ["consumer", "gate"])

    def test_the_consumer_repo_is_left_untouched(self) -> None:
        # Given a consumer repo with a clean tree
        before = git(self.consumer, "status", "--porcelain", "--ignored")
        # When the canary scans it
        self.run_canary()
        # Then nothing in it changed: scans run on scratch copies of tracked files
        self.assertEqual(git(self.consumer, "status", "--porcelain", "--ignored"), before)
        self.assertNotIn(str(self.consumer), self.log.read_text())


if __name__ == "__main__":
    unittest.main()
