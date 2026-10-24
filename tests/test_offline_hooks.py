"""AK7597 hook transport regressions; fixture scanners never install in real repos."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

OWNER = Path(__file__).resolve().parents[1]
INSTALLER = OWNER / "local/hooks/install_offline.py"
RUNNER = OWNER / "local/hooks/offline_commit.py"
REAL_SCANNER = Path.home() / "ai-society/softwareco/contrib/ultimate_bug_scanner-local/ubs"

NATIVE = '''#!/usr/bin/env python3
from pathlib import Path
import os, subprocess, sys
assert sys.argv[1:3] == ["--offline", "--index"]
assert sys.argv[3] == "--base-ref"
base = sys.argv[4]
changed = subprocess.check_output(["git", "diff", "--cached", "--name-only", "-z", base]).split(b"\\0")
if any(p.startswith(b"docs/_core/") for p in changed): sys.exit(1)
with open(os.environ["HOOK_TEST_LOG"], "a") as f: f.write("native\\n")
if Path("control").read_text() != "good\\n": sys.exit(1)
'''
ENTRY = '''#!/bin/sh
set -eu
root="$(git rev-parse --show-toplevel)"
exec "$root/scripts/ci/smoke.sh" --offline --index "$@"
'''
SCANNER = '''#!/usr/bin/env python3
from pathlib import Path
import os, subprocess, sys
with open(os.environ["HOOK_TEST_LOG"], "a") as f: f.write("ubs\\n")
source = subprocess.run(["git", "show", ":app.py"], capture_output=True).stdout
ignore = Path(".ubsignore").read_text() if Path(".ubsignore").exists() else ""
sys.exit(1 if b"BAD" in source and "app.py" not in ignore else 0)
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def environment():
    return {k: v for k, v in os.environ.items()
            if not k.startswith("GIT_") and k != "SOFTWARECO_HOOK_PARENT_NETNS"}


class OfflineHookFeature(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="hook-tests-"))
        self.addCleanup(shutil.rmtree, self.work, True)
        self.home = self.work / "home"
        self.repo = self.home / "ai-society/softwareco/owned/dep-viz"
        self.repo.mkdir(parents=True)
        self.log = self.work / "events"
        self.env = dict(environment(), HOME=str(self.home), TMPDIR=str(self.work),
                        HOOK_TEST_LOG=str(self.log), UBS_STAGED_STRICT="1",
                        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "hook fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.put("scripts/ci/smoke.sh", NATIVE, executable=True)
        self.put("scripts/ci/full.sh", "#!/bin/sh\nexit 0\n", executable=True)
        self.put(".githooks/pre-commit", ENTRY, executable=True)
        self.put("control", "good\n")
        self.put("app.py", "print('good')\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture seed")
        self.scanner = self.home / "ai-society/softwareco/contrib/ultimate_bug_scanner-local/ubs"
        self.scanner.parent.mkdir(parents=True)
        self.scanner.write_text(SCANNER)
        self.scanner.chmod(0o755)
        self.common = self.repo / ".git"

    def git(self, *args, root=None, check=True):
        return subprocess.run(["git", "-C", str(root or self.repo), *args], env=self.env,
                              capture_output=True, text=True, check=check)

    def put(self, rel, text, executable=False, root=None):
        target = (root or self.repo) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        if executable:
            target.chmod(0o755)
        return target

    def install(self, root=None, check=True):
        root = root or self.repo
        result = subprocess.run([sys.executable, str(INSTALLER), "--repo", str(root),
                                 "--mode", "native-v1", "--native-sha256", sha(root / "scripts/ci/smoke.sh"),
                                 "--native-hook-sha256", sha(root / ".githooks/pre-commit")],
                                env=self.env, capture_output=True, text=True)
        if check:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def hook(self, root=None, **extra):
        return subprocess.run(["git", "hook", "run", "pre-commit"],
                              cwd=root or self.repo, env={**self.env, **extra},
                              capture_output=True, text=True)

    def events(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def stage(self, rel, text, root=None):
        self.put(rel, text, root=root)
        self.git("add", "--", rel, root=root)

    def test_installer_is_idempotent_absolute_and_preserves_prepush(self):
        self.put(".githooks/pre-push", "#!/bin/sh\nprintf 'push\\n'\n", executable=True)
        self.git("add", ".githooks/pre-push")
        first = self.install()
        config = self.common / "softwareco-offline-hooks-v1/config.json"
        stamp = config.stat().st_mtime_ns
        second = self.install()
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(stamp, config.stat().st_mtime_ns)
        self.assertTrue(Path(self.git("config", "--get", "core.hooksPath").stdout.strip()).is_absolute())
        push = subprocess.run([str(config.parent / "pre-push")], cwd=self.repo,
                              env=self.env, capture_output=True, text=True)
        self.assertEqual(push.stdout, "push\n")

    def test_standalone_chain_orders_real_wrapper_before_native(self):
        self.stage("app.py", "print('changed')\n")
        self.install()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_linked_gitfile_worktree_uses_correct_index_and_shared_config(self):
        wt = self.work / "linked"
        self.git("worktree", "add", "-qb", "candidate", str(wt))
        self.assertTrue((wt / ".git").is_file())
        self.stage("app.py", "print('candidate')\n", root=wt)
        self.install(wt)
        before = self.git("status", "--porcelain=v1", root=self.repo).stdout
        result = self.hook(wt, GIT_DIR=str(self.common / "worktrees/linked"),
                           GIT_INDEX_FILE=str(self.common / "worktrees/linked/index"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])
        self.assertEqual(before, self.git("status", "--porcelain=v1", root=self.repo).stdout)

    def test_staged_good_working_bad_passes_without_mutation(self):
        self.stage("app.py", "print('good staged')\n")
        self.put("app.py", "BAD\n")
        self.install()
        tree = self.git("write-tree").stdout
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree, self.git("write-tree").stdout)
        self.assertEqual((self.repo / "app.py").read_text(), "BAD\n")

    def test_staged_bad_working_good_refuses_before_native(self):
        self.stage("app.py", "BAD\n")
        self.put("app.py", "print('fixed only in worktree')\n")
        self.install()
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), ["ubs"])

    def test_staged_ignore_not_working_ignore_controls_scanner(self):
        self.stage("app.py", "BAD\n")
        self.stage(".ubsignore", "app.py\n")
        self.put(".ubsignore", "")
        self.install()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_unstaged_ignore_cannot_hide_index_problem(self):
        self.stage("app.py", "BAD\n")
        self.stage(".ubsignore", "")
        self.put(".ubsignore", "app.py\n")
        self.install()
        self.assertNotEqual(self.hook().returncode, 0)
        self.assertEqual(self.events(), ["ubs"])

    def test_native_reads_indexed_controls_not_working_tree(self):
        self.stage("control", "bad\n")
        self.put("control", "good\n")
        self.install()
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_staged_protected_path_is_not_hidden_by_head_or_worktree(self):
        self.stage("docs/_core/protected.md", "protected\n")
        (self.repo / "docs/_core/protected.md").unlink()
        self.install()
        self.assertNotEqual(self.hook().returncode, 0)

    def test_namespace_rejects_forged_environment(self):
        self.stage("app.py", "print('changed')\n")
        self.install()
        result = self.hook(SOFTWARECO_HOOK_PARENT_NETNS="forged")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), [])

    def test_unknown_existing_hooks_are_retained_and_refused(self):
        self.git("config", "core.hooksPath", "custom-hooks")
        result = self.install(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.strip(), "custom-hooks")

    def test_unknown_default_precommit_is_refused_before_metadata_changes(self):
        old = self.common / "hooks/pre-commit"
        old.write_text("#!/bin/sh\nexit 1\n")
        old.chmod(0o755)
        result = self.install(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown default pre-commit", result.stderr)
        self.assertEqual(old.read_text(), "#!/bin/sh\nexit 1\n")
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())
        self.assertNotEqual(self.git("config", "--get", "core.hooksPath", check=False).returncode, 0)

    def test_primary_worktree_override_refuses_before_mutation(self):
        self.git("config", "extensions.worktreeConfig", "true")
        self.git("config", "--worktree", "core.hooksPath", ".githooks")
        result = self.install(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("worktree hooks override", result.stderr)
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.strip(), ".githooks")

    def test_other_linked_worktree_override_refuses_install_everywhere(self):
        wt = self.work / "linked"
        self.git("worktree", "add", "-qb", "candidate", str(wt))
        self.git("config", "extensions.worktreeConfig", "true")
        self.git("config", "--worktree", "core.hooksPath", ".githooks", root=wt)
        result = self.install(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("worktree hooks override", result.stderr)
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())

    def test_alternate_commit_index_is_the_candidate_not_default_index(self):
        self.install()
        alternate = self.work / "alternate-index"
        shutil.copy2(self.common / "index", alternate)
        self.stage("app.py", "BAD\n")
        result = self.hook(GIT_INDEX_FILE=str(alternate))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("BAD", self.git("show", ":app.py").stdout)

    def test_literal_snapshot_ignores_export_ignore_and_eol_attributes(self):
        self.stage(".gitattributes", "control export-ignore\ncontrol text eol=crlf\n")
        self.stage("control", "good\n")
        self.install()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_symlink_native_entry_is_refused_at_install(self):
        (self.repo / ".githooks/pre-commit").unlink()
        (self.repo / ".githooks/pre-commit").symlink_to("../scripts/ci/smoke.sh")
        self.git("add", ".githooks/pre-commit")
        result = self.install(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())

    def test_legacy_prepush_migration_from_linked_worktree_is_preserved(self):
        self.put(".githooks/pre-push", "#!/bin/sh\nprintf 'push\\n'\n", executable=True)
        self.git("add", ".githooks/pre-push")
        self.git("commit", "-qm", "fixture push hook")
        old_dir = self.common / "ubs-chain-hooks"
        old_dir.mkdir()
        old_ubs = self.home / "ai-society/softwareco/scripts/ubs-staged.sh"
        old = (f'#!/usr/bin/env sh\nset -eu\n"{old_ubs}" || exit $?\n'
               f'if [ -x "{self.repo}/.githooks/pre-commit" ]; then\n'
               f'  exec "{self.repo}/.githooks/pre-commit"\nfi\nexit 0\n')
        (old_dir / "pre-commit").write_text(old)
        (old_dir / "pre-push").symlink_to(self.repo / ".githooks/pre-push")
        self.git("config", "core.hooksPath", ".git/ubs-chain-hooks")
        wt = self.work / "linked"
        self.git("worktree", "add", "-qb", "candidate", str(wt))
        self.stage("app.py", "print('candidate')\n", root=wt)
        self.install(wt)
        self.assertEqual((old_dir / "pre-commit").read_text(), old)
        result = self.hook(wt)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])
        push = subprocess.run(["git", "hook", "run", "pre-push"], cwd=wt,
                              env=self.env, capture_output=True, text=True)
        self.assertEqual(push.returncode, 0, push.stdout + push.stderr)
        self.assertEqual(push.stdout + push.stderr, "push\n")

    def test_origin_index_bytes_are_not_refreshed_by_capture(self):
        self.stage("app.py", "print('different')\n")
        self.install()
        before = (self.common / "index").read_bytes()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.common / "index").read_bytes(), before)

    def test_native_index_drift_is_detected_before_return(self):
        script = NATIVE + '''\nroot = os.environ['HOOK_ORIGIN']\nsubprocess.run(['git', '-C', root, 'add', 'control'], check=True)\n'''
        self.put("scripts/ci/smoke.sh", script, executable=True)
        self.git("add", "scripts/ci/smoke.sh")
        self.put("control", "working-only-change\n")
        self.install()
        result = self.hook(HOOK_ORIGIN=str(self.repo))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HEAD/index changed during native", result.stderr)

    def test_ubs_index_drift_refuses_before_native(self):
        self.scanner.write_text(SCANNER.replace('sys.exit(1 if',
            "subprocess.run(['git', '-C', os.environ['HOOK_ORIGIN'], 'add', 'control'], check=True)\nsys.exit(1 if"))
        self.stage("app.py", "print('changed')\n")
        self.put("control", "working-only-change\n")
        self.install()
        result = self.hook(HOOK_ORIGIN=str(self.repo))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HEAD/index changed during UBS", result.stderr)
        self.assertNotIn("native", self.events())

    def test_missing_promisor_blob_refuses_without_lazy_fetch_child(self):
        self.stage("app.py", "print('different missing object')\n")
        self.install()
        oid = self.git("rev-parse", ":app.py").stdout.strip()
        (self.common / "objects" / oid[:2] / oid[2:]).unlink()
        self.git("remote", "add", "origin", "file:///nonexistent-hook-fixture")
        self.git("config", "remote.origin.promisor", "true")
        trace = self.work / "trace.jsonl"
        result = self.hook(GIT_TRACE2_EVENT=str(trace))
        self.assertNotEqual(result.returncode, 0)
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        fetches = [e for e in events if e.get('event') == 'child_start' and 'fetch' in e.get('argv', [])]
        self.assertEqual(fetches, [])
        self.assertEqual(self.events(), [])

    def test_missing_native_entry_refuses_install(self):
        self.git("rm", ".githooks/pre-commit")
        # Avoid test helper hashing the removed file; supply a deliberately stale hash.
        result = subprocess.run([sys.executable, str(INSTALLER), "--repo", str(self.repo),
                                 "--mode", "native-v1", "--native-sha256", sha(self.repo / "scripts/ci/smoke.sh"),
                                 "--native-hook-sha256", "0" * 64],
                                env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())

    def test_metadata_cannot_select_an_alternate_ubs_wrapper(self):
        self.stage("app.py", "print('candidate')\n")
        self.install()
        other = self.work / "alternate-wrapper"
        other.write_text("#!/bin/sh\nexit 0\n")
        other.chmod(0o755)
        config = self.common / "softwareco-offline-hooks-v1/config.json"
        meta = json.loads(config.read_text())
        meta["ubs_staged"] = str(other)
        meta["source_hashes"][str(other)] = sha(other)
        config.write_text(json.dumps(meta))
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fixed entrypoint", result.stderr)
        self.assertEqual(self.events(), [])

    def test_index_native_drift_refuses_without_execution(self):
        self.install()
        self.stage("scripts/ci/smoke.sh", NATIVE + "# changed after qualification\n")
        self.assertNotEqual(self.hook().returncode, 0)
        self.assertNotIn("native", self.events())

    def test_native_network_attempt_cannot_leave_namespace(self):
        script = NATIVE + '''\nimport socket\ns = socket.socket()\ntry:\n s.connect(("192.0.2.1", 9))\nexcept OSError:\n pass\nelse:\n sys.exit(99)\n'''
        self.put("scripts/ci/smoke.sh", script, executable=True)
        self.git("add", "scripts/ci/smoke.sh")
        self.install()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def use_real_scanner(self):
        if not REAL_SCANNER.is_file():
            self.fail("real service scanner unavailable: qualification cannot be skipped")
        self.install()
        config = self.common / "softwareco-offline-hooks-v1/config.json"
        meta = json.loads(config.read_text())
        meta.update(scanner=str(REAL_SCANNER), scanner_sha256=sha(REAL_SCANNER))
        config.write_text(json.dumps(meta))

    def test_real_ubs_both_content_directions(self):
        self.stage("app.py", "print('staged safe')\n")
        self.put("app.py", "def risky(x):\n return eval(x)\n")
        self.use_real_scanner()
        passed = self.hook()
        self.assertEqual(passed.returncode, 0, passed.stdout[-3000:] + passed.stderr[-3000:])
        self.log.unlink(missing_ok=True)
        self.stage("app.py", "def risky(x):\n return eval(x)\n")
        self.put("app.py", "print('unstaged safe')\n")
        refused = self.hook()
        self.assertNotEqual(refused.returncode, 0, refused.stdout[-3000:] + refused.stderr[-3000:])
        self.assertNotIn("native", self.events())

    def test_real_ubs_both_ignore_directions(self):
        self.stage("app.py", "def risky(x):\n return eval(x)\n")
        self.stage(".ubsignore", "app.py\n")
        self.put(".ubsignore", "")
        self.use_real_scanner()
        passed = self.hook()
        self.assertEqual(passed.returncode, 0, passed.stdout[-3000:] + passed.stderr[-3000:])
        self.stage(".ubsignore", "")
        self.put(".ubsignore", "app.py\n")
        self.log.unlink(missing_ok=True)
        refused = self.hook()
        self.assertNotEqual(refused.returncode, 0, refused.stdout[-3000:] + refused.stderr[-3000:])
        self.assertNotIn("native", self.events())


if __name__ == "__main__":
    unittest.main()
