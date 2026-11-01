"""AK7893 task-scope snapshot check (all five copies) and template TMPDIR regressions.

Every scenario runs checked-in scripts copied into a scratch `git init` repo under the
test's temp dir, with a stub `ak` first on PATH: no real AK DB is ever consulted.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
import unittest

OWNER = Path(__file__).resolve().parents[1]
PROJECT = OWNER / "copier/tpl-project-repo"
# The template and L1 copies of the task-scope checker; each must carry the same fix.
# (owned/scripts/lib holds the owned lane root's own rendered copy, tracked separately.)
COPIES = {
    "tpl_project_repo": PROJECT,
    "tpl_agent_repo": OWNER / "copier/tpl-agent-repo",
    "tpl_org_repo": OWNER / "copier/tpl-org-repo",
    "tpl_monorepo": OWNER / "copier/tpl-monorepo",
    "softwareco": OWNER,
}
WRAPPER = "scripts/check-task-scope-snapshots.sh"
HELPER = "scripts/lib/check-task-scope-snapshots.py"
FULL = "scripts/ci/full.sh"
DOCUMENT_POLICY = "scripts/check-document-policy.sh"

STUB_AK = r'''#!/usr/bin/env python3
"""Stub ak: answers from $STUB_AK_STATE/tasks.json and never opens a real AK DB."""
import json, os, sys
from pathlib import Path

state = Path(os.environ["STUB_AK_STATE"])
args = sys.argv[1:]
with (state / "calls.log").open("a", encoding="utf-8") as log:
    log.write(json.dumps(args) + "\n")
tasks = json.loads((state / "tasks.json").read_text(encoding="utf-8"))
if len(args) == 5 and args[:2] == ["task", "show"] and args[3:] == ["-F", "json"]:
    task = tasks.get(args[2]) or sys.exit(f"error: stub ak has no task {args[2]!r}")
    print(json.dumps({"id": args[2], "repo": task["repo"]}))
elif len(args) == 4 and args[:3] == ["task", "scope", "export"]:
    task = tasks.get(args[3]) or sys.exit(f"error: stub ak has no task {args[3]!r}")
    print(json.dumps(dict(task["scope"], exported_at="2026-11-01T00:00:00Z"), indent=2))
else:
    sys.exit(f"error: unexpected stub ak call: {args!r}")
'''

# Records every mktemp call. A template under $STUB_MKTEMP_ROOT (the fixture dir, wherever
# tempfile put it) is created as asked; any other template (e.g. the /tmp fallback) is
# created under $STUB_MKTEMP_REDIRECT instead, so a test never writes outside its fixture.
STUB_MKTEMP = '''#!/bin/sh
set -eu
printf '%s\\n' "$*" >>"$STUB_MKTEMP_LOG"
dir_flag=""
template=""
for arg in "$@"; do
  case "$arg" in
  -d) dir_flag=-d ;;
  -*) ;;
  *) template=$arg ;;
  esac
done
case "$template" in
"$STUB_MKTEMP_ROOT"/*) created="$(__REAL_MKTEMP__ "$@")" ;;
*) created="$(__REAL_MKTEMP__ $dir_flag "$STUB_MKTEMP_REDIRECT/${template##*/}")" ;;
esac
printf '%s\\n' "$created" >>"$STUB_MKTEMP_CREATED"
printf '%s\\n' "$created"
'''

FAST = '''#!/bin/sh
printf 'fast\\n' >>"$FAST_LOG"
'''

SCOPE = {"schema_version": 1, "allowed": ["README.md", "src/**"], "required": ["README.md"]}


def environment():
    return {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "AK_"))}


class TaskScopeFixture(unittest.TestCase):
    COPY = PROJECT

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="tpl-task-scope-")).resolve()
        self.addCleanup(shutil.rmtree, self.work, True)
        self.scratch = self.work / "scratch"
        self.scratch.mkdir()
        self.state = self.work / "ak-state"
        self.state.mkdir()
        self.tasks = {}
        self.save_tasks()
        bin_dir = self.work / "bin"
        bin_dir.mkdir()
        real_mktemp = shutil.which("mktemp")
        self.assertIsNotNone(real_mktemp)
        self.put(bin_dir / "ak", STUB_AK, executable=True)
        self.put(bin_dir / "mktemp", STUB_MKTEMP.replace("__REAL_MKTEMP__", real_mktemp), executable=True)
        self.mktemp_log = self.work / "mktemp.log"
        self.mktemp_created = self.work / "mktemp-created.log"
        self.redirect = self.work / "redirected"
        self.redirect.mkdir()
        self.fast_log = self.work / "fast.log"
        self.env = dict(
            environment(),
            HOME=str(self.work / "home"),
            TMPDIR=str(self.scratch),
            PATH=f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}",
            AK_CMD="ak",
            STUB_AK_STATE=str(self.state),
            STUB_MKTEMP_LOG=str(self.mktemp_log),
            STUB_MKTEMP_CREATED=str(self.mktemp_created),
            STUB_MKTEMP_ROOT=str(self.work),
            STUB_MKTEMP_REDIRECT=str(self.redirect),
            FAST_LOG=str(self.fast_log),
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
        )
        self.repo = self.make_repo(self.work / "repo")

    def put(self, path, text, executable=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if executable:
            path.chmod(0o755)

    def git(self, cwd, *args):
        return subprocess.run(["git", *args], cwd=cwd, env=self.env, check=True,
                              capture_output=True, text=True, timeout=60).stdout

    def make_repo(self, root):
        root.mkdir(parents=True)
        sources = {WRAPPER: self.COPY / WRAPPER, HELPER: self.COPY / HELPER,
                   FULL: PROJECT / FULL, DOCUMENT_POLICY: PROJECT / DOCUMENT_POLICY}
        for relative, source in sources.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            target.chmod(0o755 if relative.endswith(".sh") else 0o644)
        self.put(root / "scripts/ci/fast.sh", FAST, executable=True)
        self.put(root / "README.md", "fixture\n")
        self.put(root / "src/app.txt", "app\n")
        self.git(root, "init", "-q", "-b", "main")
        self.git(root, "config", "user.name", "tpl fixture")
        self.git(root, "config", "user.email", "fixture@example.invalid")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "fixture seed")
        return root

    def add_worktree(self):
        worktree = self.work / "wt"
        self.git(self.repo, "worktree", "add", "-q", "-b", "wt", str(worktree))
        return worktree

    def save_tasks(self):
        (self.state / "tasks.json").write_text(json.dumps(self.tasks), encoding="utf-8")

    def add_task(self, task_id, repo, scope=SCOPE):
        self.tasks[str(task_id)] = {"repo": str(repo), "scope": dict(scope, task_id=task_id)}
        self.save_tasks()

    def snapshots_dir(self, root):
        return root / "governance/task-scopes"

    def write_snapshot(self, root, name, payload):
        self.put(self.snapshots_dir(root) / name, json.dumps(payload, indent=2) + "\n")

    def matching_snapshot(self, task_id):
        return dict(SCOPE, task_id=task_id, exported_at="2026-10-31T23:59:59Z")

    def run_script(self, root, relative, env=None):
        return subprocess.run([str(root / relative)], cwd=root, env=env or self.env,
                              capture_output=True, text=True, timeout=120)

    def check(self, root, env=None):
        return self.run_script(root, WRAPPER, env)

    def ak_calls(self):
        log = self.state / "calls.log"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    def mktemp_calls(self):
        if not self.mktemp_log.exists():
            return []
        return self.mktemp_log.read_text(encoding="utf-8").splitlines()

    def tmpdir_cases(self):
        """(label, env, expected template dir, dir the stub creates in) per TMPDIR state:
        honoured when set; the /tmp fallback only when unset or empty, which the stub
        records but creates inside the fixture instead."""
        unset = {k: v for k, v in self.env.items() if k != "TMPDIR"}
        return (("set", self.env, str(self.scratch), self.scratch),
                ("unset", unset, "/tmp", self.redirect),
                ("empty", dict(self.env, TMPDIR=""), "/tmp", self.redirect))

    def assert_temp_use(self, template, created_in):
        """Exactly one mktemp call used `template`, its path was created in `created_in`
        (inside the fixture), and the script removed it again."""
        self.assertEqual(self.mktemp_calls(), [template])
        created = self.mktemp_created.read_text(encoding="utf-8").splitlines()
        self.assertEqual([Path(path).parent for path in created], [created_in])
        self.assertFalse(Path(created[0]).exists(), "temporary path was not cleaned up")
        self.assertEqual(list(self.scratch.iterdir()) + list(self.redirect.iterdir()), [])

    def reset_temp_logs(self):
        self.mktemp_log.unlink(missing_ok=True)
        self.mktemp_created.unlink(missing_ok=True)

    def assert_ok(self, result, stdout):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(stdout, result.stdout)

    def assert_refused(self, result, *needles, code=1):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("ok:", result.stdout)
        for needle in needles:
            self.assertIn(needle, result.stderr)


class LinkedWorktreeScenarios:
    def test_main_checkout_snapshot_is_accepted(self):
        """Given an AK task recorded for the main checkout and its matching snapshot,
        when the check runs in the main checkout, then the snapshot is accepted."""
        self.add_task(1, self.repo)
        self.write_snapshot(self.repo, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.assert_ok(self.check(self.repo), "ok: task-scope snapshots (1 checked)")

    def test_linked_worktree_snapshot_of_same_repository_is_accepted(self):
        """Given an AK task recorded for the main checkout path, when the check runs in a
        linked worktree of that repository holding the matching snapshot, then the
        worktree counts as the same repository and the snapshot is accepted."""
        worktree = self.add_worktree()
        self.add_task(1, self.repo)
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.assert_ok(self.check(worktree), "ok: task-scope snapshots (1 checked)")

    def test_linked_worktree_still_reports_drift(self):
        """Given a linked worktree whose snapshot no longer matches the AK export, when
        the check runs there, then it fails with a drift report, not a repo mismatch."""
        worktree = self.add_worktree()
        self.add_task(1, self.repo)
        self.write_snapshot(worktree, "AK-1.snapshot.json", dict(self.matching_snapshot(1), allowed=["**"]))
        result = self.check(worktree)
        self.assert_refused(result, "task-scope snapshot drift detected")
        self.assertNotIn("belongs to repo", result.stderr)

    def test_linked_worktree_is_accepted_under_hook_git_environment(self):
        """Given git's hook environment (GIT_DIR, GIT_WORK_TREE) exported for a linked
        worktree, when the check runs there for a task of the main checkout, then the
        repository identity is still resolved correctly and the snapshot is accepted."""
        worktree = self.add_worktree()
        git_dir = self.git(worktree, "rev-parse", "--path-format=absolute", "--git-dir").strip()
        self.add_task(1, self.repo)
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        env = dict(self.env, GIT_DIR=git_dir, GIT_WORK_TREE=str(worktree))
        self.assert_ok(self.check(worktree, env), "ok: task-scope snapshots (1 checked)")

    def test_linked_worktree_refuses_task_of_another_repository(self):
        """Given an AK task recorded for a different git repository, when the check runs
        in a linked worktree holding that task's snapshot, then the snapshot is refused."""
        other = self.make_repo(self.work / "other")
        worktree = self.add_worktree()
        self.add_task(1, other)
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.assert_refused(self.check(worktree), "belongs to repo")

    def test_hook_git_environment_cannot_launder_another_repository(self):
        """Given GIT_DIR exported for the worktree, as git hooks do, when the check runs
        for a task of a different repository, then the inherited git environment cannot
        make the other repository look like this one and the snapshot is refused."""
        other = self.make_repo(self.work / "other")
        worktree = self.add_worktree()
        git_dir = self.git(worktree, "rev-parse", "--path-format=absolute", "--git-dir").strip()
        self.add_task(1, other)
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        for extra in ({"GIT_DIR": git_dir}, {"GIT_DIR": git_dir, "GIT_WORK_TREE": str(worktree)}):
            with self.subTest(env=sorted(extra)):
                self.assert_refused(self.check(worktree, dict(self.env, **extra)), "belongs to repo")

    def test_subdirectory_of_the_same_checkout_is_not_the_repository(self):
        """Given an AK task recorded for a subdirectory of this checkout, when the check
        runs in a linked worktree, then sharing a git directory is not enough and the
        snapshot is refused."""
        worktree = self.add_worktree()
        self.add_task(1, self.repo / "src")
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.assert_refused(self.check(worktree), "belongs to repo")


class SnapshotNameScenarios:
    def test_uppercase_extension_snapshot_fails_closed(self):
        """Given a snapshot saved as AK-1.snapshot.JSON, when the check runs, then it
        fails closed and names the file instead of reporting no snapshots."""
        self.add_task(1, self.repo)
        self.write_snapshot(self.repo, "AK-1.snapshot.JSON", {"drifted": True})
        self.assert_refused(self.check(self.repo), "AK-1.snapshot.JSON", "numeric task id")

    def test_near_miss_names_fail_closed(self):
        """Given any near-miss file name in governance/task-scopes, when the check runs,
        then it fails closed and names the file."""
        self.add_task(1, self.repo)
        names = ["ak-1.snapshot.json", "AK-1.Snapshot.json", "AK-1.snapshot.json.bak",
                 "AK-1.snapshot.jsonl", "AK-1.snapshot.json~", " AK-1.snapshot.json",
                 "AK-1.snapshot.json ", "AK-01x.snapshot.json", "AK-1.snapshot", "notes.md"]
        for name in names:
            with self.subTest(name=name):
                shutil.rmtree(self.snapshots_dir(self.repo), ignore_errors=True)
                self.write_snapshot(self.repo, name, {"drifted": True})
                self.assert_refused(self.check(self.repo), name)

    def test_misnamed_file_beside_valid_snapshot_fails(self):
        """Given a valid snapshot beside a misnamed one, when the check runs, then the
        misnamed file fails the check instead of being skipped silently."""
        self.add_task(1, self.repo)
        self.add_task(2, self.repo)
        self.write_snapshot(self.repo, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.write_snapshot(self.repo, "AK-2.snapshot.JSON", {"drifted": True})
        self.assert_refused(self.check(self.repo), "AK-2.snapshot.JSON")

    def test_misnamed_file_in_subdirectory_fails(self):
        """Given a misnamed snapshot in a subdirectory of governance/task-scopes, when the
        check runs, then it fails closed like a top-level one."""
        self.add_task(1, self.repo)
        self.write_snapshot(self.repo, "nested/AK-1.snapshot.JSON", {"drifted": True})
        self.assert_refused(self.check(self.repo), "AK-1.snapshot.JSON")

    def test_documented_placeholders_are_tolerated(self):
        """Given only a .gitkeep and a documented legacy AK-<ID>.json fallback, when the
        check runs, then it reports no snapshots without consulting AK, and a valid
        snapshot beside them is still checked."""
        self.put(self.snapshots_dir(self.repo) / ".gitkeep", "")
        self.write_snapshot(self.repo, "AK-7.json", {"legacy": True})
        self.assert_ok(self.check(self.repo), "ok: no task-scope snapshots")
        self.assertEqual(self.ak_calls(), [])
        self.add_task(1, self.repo)
        self.write_snapshot(self.repo, "AK-1.snapshot.json", self.matching_snapshot(1))
        self.assert_ok(self.check(self.repo), "ok: task-scope snapshots (1 checked)")

    def test_newline_bearing_name_keeps_numeric_task_id_error(self):
        """Given a snapshot name with an embedded newline, when the check runs, then it
        fails with the 'numeric task id' error the template CI relies on."""
        self.add_task(1, self.repo)
        self.write_snapshot(self.repo, "AK-1\nextra.snapshot.json", self.matching_snapshot(1))
        self.assert_refused(self.check(self.repo), "numeric task id")


# One concrete TestCase per checked-in copy, each running that copy's own wrapper+helper.
for _copy, _root in COPIES.items():
    for _scenarios in (LinkedWorktreeScenarios, SnapshotNameScenarios):
        _name = f"{_scenarios.__name__.removesuffix('Scenarios')}Feature_{_copy}"
        globals()[_name] = type(_name, (_scenarios, TaskScopeFixture),
                                {"COPY": _root, "__module__": __name__})
del _copy, _root, _scenarios, _name


class HelperCopiesFeature(unittest.TestCase):
    def test_all_helper_copies_are_byte_identical(self):
        """Given the template and L1 copies of the task-scope helper, when compared,
        then they are byte-identical, so a fix cannot land in only some of them."""
        reference = (PROJECT / HELPER).read_bytes()
        drifted = [name for name, root in COPIES.items() if (root / HELPER).read_bytes() != reference]
        self.assertEqual(drifted, [], f"copies differ from {PROJECT / HELPER}")


class FullGateTmpdirFeature(TaskScopeFixture):
    def full(self, root, env=None):
        return self.run_script(root, FULL, env)

    def test_full_honors_tmpdir_and_falls_back_to_tmp_only_when_unset(self):
        """Given TMPDIR set, unset, or empty, when the template full gate runs, then it
        passes, its log dir template lies under TMPDIR when set and under /tmp only
        when unset or empty, and the log dir is removed afterwards."""
        for label, env, template_dir, created_in in self.tmpdir_cases():
            with self.subTest(tmpdir=label):
                self.reset_temp_logs()
                self.assert_ok(self.full(self.repo, env), "ok: full")
                self.assert_temp_use(f"-d {template_dir}/tpl-project-full.XXXXXX", created_in)

    def test_full_passes_in_linked_worktree_with_snapshot(self):
        """Given a linked worktree holding a matching snapshot for a task of the main
        checkout, when the template full gate runs there, then it passes."""
        worktree = self.add_worktree()
        self.add_task(1, self.repo)
        self.write_snapshot(worktree, "AK-1.snapshot.json", self.matching_snapshot(1))
        result = self.full(worktree)
        self.assert_ok(result, "ok: full")
        self.assertIn("ok: task-scope snapshots (1 checked)", result.stdout)


class DocumentPolicyTmpdirFeature(TaskScopeFixture):
    def setUp(self):
        super().setUp()
        baseline = self.git(self.repo, "rev-parse", "HEAD").strip()
        self.put(self.repo / "docs/project/product_posture.md",
                 "---\nsummary: \"fixture posture\"\nas_of: 2026-11-01\nlast_validated: 2026-11-01\n"
                 f"last_validated_commit: {baseline}\nevidence_paths:\n  - src/app.txt\n---\n\n# Posture\n")
        self.git(self.repo, "add", "docs/project/product_posture.md")
        self.git(self.repo, "commit", "-qm", "validate posture")
        self.env.update(PRODUCT_POSTURE_TEST_MODE="1", PRODUCT_POSTURE_TODAY="2026-11-01")

    def policy(self, env=None):
        return self.run_script(self.repo, DOCUMENT_POLICY, env)

    def test_document_policy_honors_tmpdir_and_falls_back_to_tmp_only_when_unset(self):
        """Given TMPDIR set, unset, or empty and a fresh posture, when the template
        document policy runs, then it passes, its evidence file template lies under
        TMPDIR when set and under /tmp only when unset or empty, and the file is removed."""
        for label, env, template_dir, created_in in self.tmpdir_cases():
            with self.subTest(tmpdir=label):
                self.reset_temp_logs()
                self.assert_ok(self.policy(env), "ok: document freshness and dated-snapshot policy")
                self.assert_temp_use(f"{template_dir}/product-posture-evidence.XXXXXX", created_in)


if __name__ == "__main__":
    unittest.main()
