"""Feature: scripts/ubs-staged.sh scans staged changes the way the repo's UBS config says.

The pre-commit wrapper handed every staged path to `ubs` as an explicit file
argument. UBS scans explicitly named files even when `.ubsignore` excludes them,
so a repo's ignore list (for example ultimate_bug_scanner's own `test-suite/`
of intentionally buggy fixtures) never applied at commit time, and committing a
buggy fixture failed the hook. `ubs --staged` applies `.ubsignore`.

Scenarios are written Given/When/Then.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "scripts" / "ubs-staged.sh"
REAL_UBS = Path.home() / "ai-society" / "softwareco" / "contrib" / "ultimate_bug_scanner" / "ubs"

STUB = """#!/usr/bin/env sh
printf '%s\\n' "$*" >> "$STUB_LOG"
case " $* " in *" --format=json "*) printf '%s' "${STUB_JSON:-}" ;; esac
exit "${STUB_RC:-0}"
"""


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class UbsStagedFeature(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ubs-staged-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        self.stub = self.tmp / "ubs"
        self.stub.write_text(STUB)
        self.stub.chmod(0o755)
        self.log = self.tmp / "calls.log"

    def stage(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        git(self.repo, "add", rel)

    def run_wrapper(self, ubs_bin: Path, **env: str) -> subprocess.CompletedProcess:
        full_env = {**os.environ, "UBS_BIN": str(ubs_bin), "STUB_LOG": str(self.log),
                    "UBS_NO_AUTO_UPDATE": "1", **env}
        return subprocess.run(["sh", str(WRAPPER)], cwd=self.repo, env=full_env,
                              capture_output=True, text=True, timeout=300)

    def calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_scenario_staged_changes_are_scanned_through_ubs_staged_mode(self) -> None:
        # Given a staged source file
        self.stage("src/app.py", "print('hi')\n")
        # When the wrapper runs
        result = self.run_wrapper(self.stub)
        # Then UBS is asked for its --staged mode instead of an explicit file list
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.calls()), 1, self.calls())
        self.assertIn("--staged", self.calls()[0].split())
        self.assertNotIn("src/app.py", self.calls()[0])

    def test_scenario_nothing_staged_skips_the_scanner(self) -> None:
        # Given a repo with nothing staged
        # When the wrapper runs
        result = self.run_wrapper(self.stub)
        # Then it passes without calling UBS
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [])

    def test_scenario_scanner_exit_codes_keep_their_meaning(self) -> None:
        # Examples: stub exit | json on rerun | wrapper exit
        for rc, json_doc, expected in [("0", "", 0), ("1", "", 1), ("2", "", 2),
                                       ("3", '{"result":"no-supported-languages"}', 0),
                                       ("3", '{"scanners":[]}', 3)]:
            with self.subTest(rc=rc, json_doc=json_doc):
                self.log.unlink(missing_ok=True)
                # Given a staged file and a scanner that exits with the example status
                self.stage("src/app.py", f"print({rc})\n")
                # When the wrapper runs
                result = self.run_wrapper(self.stub, STUB_RC=rc, STUB_JSON=json_doc)
                # Then only a confirmed no-language 3 becomes a pass
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def default_scanner_home(self, with_service: bool) -> dict:
        home = self.tmp / "home"
        contrib = home / "ai-society" / "softwareco" / "contrib"
        for name, present in (("ultimate_bug_scanner", True), ("ultimate_bug_scanner-local", with_service)):
            if not present:
                continue
            (contrib / name).mkdir(parents=True, exist_ok=True)
            stub = contrib / name / "ubs"
            stub.write_text(STUB.replace('"$*"', f'"{name} $*"'))
            stub.chmod(0o755)
        env = {k: v for k, v in os.environ.items() if k != "UBS_BIN"}
        return {**env, "HOME": str(home), "STUB_LOG": str(self.log), "UBS_NO_AUTO_UPDATE": "1"}

    def run_default(self, env: dict) -> subprocess.CompletedProcess:
        return subprocess.run(["sh", str(WRAPPER)], cwd=self.repo, env=env, capture_output=True, text=True, timeout=60)

    def test_scenario_default_scanner_is_the_service_worktree(self) -> None:
        # Given a staged file, no UBS_BIN, and both the mirror checkout and the
        #   ultimate_bug_scanner-local service worktree present
        self.stage("src/app.py", "print('hi')\n")
        env = self.default_scanner_home(with_service=True)
        # When the wrapper runs
        result = self.run_default(env)
        # Then it runs the service worktree's scanner, which carries the local adoptions
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c.split()[0] for c in self.calls()], ["ultimate_bug_scanner-local"], self.calls())

    def test_scenario_missing_service_worktree_falls_back_visibly(self) -> None:
        # Given a staged file, no UBS_BIN, and only the mirror checkout
        self.stage("src/app.py", "print('hi')\n")
        env = self.default_scanner_home(with_service=False)
        # When the wrapper runs
        result = self.run_default(env)
        # Then it scans with the mirror checkout and says it fell back
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c.split()[0] for c in self.calls()], ["ultimate_bug_scanner"], self.calls())
        self.assertIn("ultimate_bug_scanner-local", result.stdout + result.stderr)

    @unittest.skipUnless(REAL_UBS.is_file(), "contrib ultimate_bug_scanner checkout not present")
    def test_scenario_docs_only_commit_passes(self) -> None:
        # Given only a markdown file is staged
        self.stage("docs/notes.md", "# Notes\n")
        # When the wrapper runs with the real scanner
        result = self.run_wrapper(REAL_UBS)
        # Then the commit is not blocked
        self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])

    @unittest.skipUnless(REAL_UBS.is_file(), "contrib ultimate_bug_scanner checkout not present")
    def test_scenario_ubsignore_applies_to_staged_files(self) -> None:
        buggy = "import pickle\n\ndef load(blob):\n    return eval(blob)\n"
        # Given a repo whose .ubsignore excludes fixtures/ and an intentionally buggy staged fixture
        self.stage(".ubsignore", "fixtures/\n")
        self.stage("fixtures/buggy.py", buggy)
        # When the wrapper runs with the real scanner
        ignored = self.run_wrapper(REAL_UBS)
        # Then the ignored fixture does not fail the commit
        self.assertEqual(ignored.returncode, 0, ignored.stdout[-2000:] + ignored.stderr[-2000:])
        # And the same code outside the ignored path still does
        self.stage("src/buggy.py", buggy)
        scanned = self.run_wrapper(REAL_UBS)
        self.assertEqual(scanned.returncode, 1, scanned.stdout[-2000:] + scanned.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
