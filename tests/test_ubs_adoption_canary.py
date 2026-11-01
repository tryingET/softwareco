"""Feature: scripts/ubs-adoption-canary.py refuses a UBS candidate that real consumer files stall.

UBS 5.4.18 passed its suite and the refusal-count checks, was pinned into the service worktree
that every repo's pre-commit runs, and within hours livelocked on ordinary find-first loops in
workstation and test-capabilities files (AK6750, AK6781). Before a re-pin, the canary scans each
consumer repo's tracked JS/TS and Python with the incumbent and the candidate and refuses the
candidate when it does not finish where the incumbent does, or is much slower.

Scenarios are written Given/When/Then.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

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


def reject_json_constant(value: str) -> None:
    raise ValueError(f"nonstandard JSON constant: {value}")


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
        self.report = json.loads(report.read_text()) if report.is_file() else None
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

    def assert_setup_error(self, result: subprocess.CompletedProcess, diagnostic: str) -> None:
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stderr)
        self.assertNotIn("verdict: pass", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIsNotNone(self.report)
        self.assertEqual(self.report["verdict"], "setup_error")
        self.assertIn("error", self.report)

    def test_git_listing_failure_after_discovery_is_not_an_empty_success(self) -> None:
        # Given a discovered consumer and Git returning plausible paths but a failure status
        bindir = self.tmp / "bin"
        bindir.mkdir()
        wrapper = bindir / "git"
        wrapper.write_text('#!/bin/sh\ncase " $* " in *" ls-files "*) '
                           'printf "a.js\\0"; echo "listing failed" >&2; exit 73;; esac\n'
                           f'exec "{shutil.which("git")}" "$@"\n')
        wrapper.chmod(0o755)
        # When listing fails, even though discovery succeeded
        result = self.run_canary(PATH=str(bindir) + os.pathsep + os.environ["PATH"])
        # Then setup fails closed without invoking either scanner
        self.assert_setup_error(result, "git ls-files")
        self.assertIn("73", result.stderr)
        self.assertIn("listing failed", result.stderr)
        self.assertFalse(self.log.exists())

    def test_an_explicit_nonrepo_is_a_listing_setup_error(self) -> None:
        # Given an existing directory that is not a Git repo
        nonrepo = self.tmp / "nonrepo"
        nonrepo.mkdir()
        # When explicitly selected, then Git failure is not normalized to no files
        result = self.run_canary("--repo", str(nonrepo))
        self.assert_setup_error(result, "git ls-files")
        self.assertFalse(self.log.exists())

    def test_no_selected_language_files_means_zero_pairs_not_pass(self) -> None:
        # Given a consumer with Python but no tracked JS files
        git(self.consumer, "rm", "-q", "a.js")
        # When only JS is selected, then zero executed pairs is a setup error
        result = self.run_canary("--langs", "js")
        self.assert_setup_error(result, "no repo/language pairs executed")
        self.assertEqual(self.report["executed_pairs"], 0)
        self.assertEqual(self.report["scans"], [])
        self.assertFalse(self.log.exists())

    def test_empty_language_selection_is_a_setup_error(self) -> None:
        # Given empty language selections, when invoked, then neither can pass vacuously
        for langs in ("", ","):
            with self.subTest(langs=langs):
                result = self.run_canary("--langs", langs)
                self.assert_setup_error(result, "at least one language")
                self.assertFalse(self.log.exists())

    def test_nonpositive_file_caps_are_setup_errors(self) -> None:
        # Given zero or negative file caps, when invoked, then reject before scanning
        for cap in ("0", "-1"):
            with self.subTest(cap=cap):
                result = self.run_canary("--max-files", cap)
                self.assert_setup_error(result, "--max-files must be positive")
                self.assertFalse(self.log.exists())

    def test_a_stale_pass_report_is_replaced_on_handled_setup_errors(self) -> None:
        # Given a report left by a previous successful invocation
        empty = self.tmp / "empty"
        empty.mkdir()
        cases = (("--langs", ""), ("--langs", "unknown"), ("--max-files", "0"),
                 ("--candidate", str(self.tmp / "missing")), ("--root", str(empty)),
                 ("--root", str(self.tmp / "missing-root")))
        for args in cases:
            with self.subTest(args=args):
                (self.tmp / "report.json").write_text('{"verdict":"pass","scans":[]}\n')
                # When setup fails, then that old pass cannot look like the current result
                result = self.run_canary(*args)
                self.assert_setup_error(result, "ubs-adoption-canary:")
                self.assertEqual(self.report["executed_pairs"], 0)
        self.assertFalse(self.log.exists())

    def test_mixed_languages_and_empty_repos_pass_if_an_actual_pair_runs(self) -> None:
        # Given one Python-only consumer and another without either selected language
        git(self.consumer, "rm", "-q", "a.js")
        empty = self.make_repo("empty", hook="exec ubs-staged.sh\n")
        git(empty, "rm", "-q", "a.js", "b.py")
        # When default languages run, then absent pairs do not prevent a real comparison
        result = self.run_canary()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.report["verdict"], "pass")
        self.assertEqual(self.report["executed_pairs"], 1)
        self.assertEqual([(r["repo"], r["lang"]) for r in self.report["scans"]],
                         [(str(self.consumer), "python")])
        self.assertEqual(len(self.log.read_text().splitlines()), 2)

    def test_scratch_creation_os_failure_is_a_reported_setup_error(self) -> None:
        # Given a file where a scratch directory is required
        blocker = self.tmp / "blocker"
        blocker.write_text("not a directory")
        # When scratch setup fails, then exit 2 with a diagnostic, never a traceback/pass
        result = self.run_canary("--scratch", str(blocker / "scratch"))
        self.assert_setup_error(result, str(blocker))
        self.assertFalse(self.log.exists())

    def test_staging_os_failure_is_a_reported_setup_error(self) -> None:
        # Given an unusable staging destination in our own scratch fixture
        blocked = self.tmp / "scratch" / "000-consumer-js" / "files" / "a.js"
        blocked.mkdir(parents=True)
        # When the copy fails, then preserve an honest non-pass report
        result = self.run_canary()
        self.assert_setup_error(result, "a.js")
        self.assertEqual(self.report["executed_pairs"], 0)
        self.assertFalse(self.log.exists())

    def test_later_listing_failure_keeps_completed_pair_diagnostics(self) -> None:
        # Given a valid consumer followed by an explicitly selected non-repo
        nonrepo = self.tmp / "nonrepo"
        nonrepo.mkdir()
        # When setup fails after real stub comparisons, then retain them, but never pass
        result = self.run_canary("--repo", str(self.consumer), "--repo", str(nonrepo))
        self.assert_setup_error(result, "git ls-files")
        self.assertEqual(self.report["executed_pairs"], 2)
        self.assertEqual(len(self.report["scans"]), 2)
        self.assertTrue(all(row["incumbent"]["status"] == "ok" and
                            row["candidate"]["status"] == "ok" for row in self.report["scans"]))

    def test_scanner_launch_os_failure_retains_the_incumbent_result(self) -> None:
        # Given an executable candidate whose interpreter does not exist
        (self.tmp / "candidate").write_text("#!/no/such/interpreter\n")
        # When candidate launch fails after the incumbent ran, then do not lose its result
        result = self.run_canary()
        self.assert_setup_error(result, "candidate")
        self.assertEqual(self.report["executed_pairs"], 0)
        self.assertEqual(self.report["scans"][0]["incumbent"]["status"], "ok")
        self.assertNotIn("candidate", self.report["scans"][0])
        self.assertEqual(len(self.log.read_text().splitlines()), 1)

    def test_an_unwritable_report_path_fails_before_scanning(self) -> None:
        # Given a report destination whose parent does not exist
        report = self.tmp / "missing" / "report.json"
        # When reporting cannot start, then no successful verdict or scanner run is allowed
        result = self.run_canary("--report", str(report))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot write report", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("verdict: pass", result.stdout)
        self.assertFalse(report.exists())
        self.assertFalse(self.log.exists())

    def test_a_report_that_cannot_be_invalidated_has_an_explicit_diagnostic(self) -> None:
        # Given a directory where the JSON report should be
        (self.tmp / "report.json").mkdir()
        # When both writing and unlinking fail, then fail closed and flag the unusable report
        result = self.run_canary()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot remove stale report", result.stderr)
        self.assertIn("any existing report is NOT current", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("verdict: pass", result.stdout)
        self.assertFalse(self.log.exists())

    def test_invalid_thresholds_fail_before_scanning_and_replace_stale_pass(self) -> None:
        # Given invalid numeric thresholds and an old successful report
        cases = {"--timeout": ("0", "-1", "nan", "inf", "-inf", "1e309", "invalid"),
                 "--max-slowdown": ("0", "-1", "nan", "inf", "-inf", "1e309", "invalid"),
                 "--floor": ("-1", "nan", "inf", "-inf", "1e309", "invalid")}
        for option, values in cases.items():
            for value in values:
                with self.subTest(option=option, value=value):
                    self.log.unlink(missing_ok=True)
                    (self.tmp / "report.json").write_text('{"verdict":"pass"}\n')
                    # When invoked, then reject before either scanner launches
                    result = self.run_canary(f"{option}={value}", "--langs", "js")
                    self.assert_setup_error(result, option)
                    self.assertFalse(self.log.exists())
                    self.assertEqual(self.report["executed_pairs"], 0)
                    self.assertEqual(self.report["scans"], [])

    def test_nonfinite_threshold_error_reports_are_standard_json(self) -> None:
        # Given NaN/infinity spellings that Python's permissive JSON encoder accepts
        for option in ("--timeout", "--max-slowdown", "--floor"):
            for value in ("nan", "inf", "-inf"):
                with self.subTest(option=option, value=value):
                    # When the error report is read with nonstandard constants forbidden
                    self.run_canary(f"{option}={value}", "--langs", "js")
                    report = json.loads((self.tmp / "report.json").read_text(),
                                        parse_constant=reject_json_constant)
                    # Then it remains standard JSON and explicitly non-successful
                    self.assertEqual(report["verdict"], "setup_error")
                    self.assertEqual(report["executed_pairs"], 0)

    def test_zero_floor_remains_valid_and_enforces_the_existing_ratio(self) -> None:
        # Given a legitimate zero floor and a clearly slower candidate
        # When scanned, then accept the argument but still refuse on the existing ratio
        result = self.run_canary("--floor", "0", "--max-slowdown", "1", "--langs", "js",
                                 STUB_incumbent_SLEEP="0.05", STUB_candidate_SLEEP="0.2")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.report["verdict"], "refuse")
        self.assertEqual(self.report["thresholds"]["floor"], 0)
        self.assertEqual(self.report["executed_pairs"], 1)
        self.assertTrue(any("slower" in reason for reason in self.report["scans"][0]["refusals"]))

    def run_with_publication_failure(self, fail_recovery: bool) -> tuple[int, str, str, list[str]]:
        """Inject write-then-close errors only on our report; scanners remain executable stubs."""
        spec = importlib.util.spec_from_file_location("ubs_canary_publication_test", CANARY)
        canary = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(canary)
        report = self.tmp / "report.json"
        original_write = Path.write_text
        writes = []

        def write_then_fail(path: Path, data: str, *args, **kwargs):
            result = original_write(path, data, *args, **kwargs)
            if path == report:
                writes.append(json.loads(data)["verdict"])
                if len(writes) == 2 or (fail_recovery and len(writes) == 3):
                    raise OSError("injected publication close failure")
            return result

        argv = [str(CANARY), "--incumbent", str(self.tmp / "incumbent"),
                "--candidate", str(self.tmp / "candidate"), "--repo", str(self.consumer),
                "--scratch", str(self.tmp / "scratch"), "--report", str(report), "--langs", "js"]
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", argv), \
                patch.dict(os.environ, {**clean_env(), "STUB_LOG": str(self.log)}, clear=True), \
                patch.object(Path, "write_text", write_then_fail), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            code = canary.main()
        self.report = json.loads(report.read_text()) if report.is_file() else None
        return code, stdout.getvalue(), stderr.getvalue(), writes

    def test_final_publication_failure_recovers_a_setup_error_with_scan_results(self) -> None:
        # Given initial publication works, but final write-then-close fails
        # When error-report recovery succeeds, then retain actual results without passing
        code, stdout, stderr, writes = self.run_with_publication_failure(fail_recovery=False)
        self.assertEqual(code, 2, stdout + stderr)
        self.assertEqual(writes, ["setup_error", "pass", "setup_error"])
        self.assertNotIn("verdict: pass", stdout)
        self.assertIn("injected publication close failure", stderr)
        self.assertEqual(self.report["verdict"], "setup_error")
        self.assertIn("injected publication close failure", self.report["error"])
        self.assertEqual(self.report["executed_pairs"], 1)
        self.assertEqual(self.report["scans"][0]["candidate"]["status"], "ok")
        self.assertEqual(len(self.log.read_text().splitlines()), 2)

    def test_final_publication_and_recovery_failures_remove_the_unusable_report(self) -> None:
        # Given initial publication works, but final and recovery write-then-close both fail
        # When recovery is exhausted, then exit 2, diagnose both failures and remove the report
        code, stdout, stderr, writes = self.run_with_publication_failure(fail_recovery=True)
        self.assertEqual(code, 2, stdout + stderr)
        self.assertEqual(writes, ["setup_error", "pass", "setup_error"])
        self.assertNotIn("verdict: pass", stdout)
        self.assertEqual(stderr.count("injected publication close failure"), 2)
        self.assertIsNone(self.report)
        self.assertFalse((self.tmp / "report.json").exists())
        self.assertEqual(len(self.log.read_text().splitlines()), 2)

    def test_incumbent_timeout_comparison_policy_is_unchanged(self) -> None:
        # Given an incumbent timing out (AK7524/7525 are outside this patch)
        # When the candidate also times out, then preserve the existing non-refusal policy
        result = self.run_canary("--langs", "js", "--timeout", "0.1",
                                 STUB_incumbent_SLEEP="0.3", STUB_candidate_SLEEP="0.3")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.report["verdict"], "pass")
        self.assertEqual(self.report["scans"][0]["refusals"], [])
        self.assertFalse(self.report["scans"][0]["incumbent"]["finished"])
        self.assertFalse(self.report["scans"][0]["candidate"]["finished"])

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
