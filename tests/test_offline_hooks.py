"""AK7597 hook transport regressions; fixture scanners never install in real repos."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib

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
changed = subprocess.check_output(["git", "diff", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none", "--no-renames", "--cached", "--name-only", "-z", base]).split(b"\\0")
if any(p.startswith(b"docs/_core/") for p in changed): sys.exit(1)
with open(Path(os.environ["HOME"]).parent / "events", "a") as f: f.write("native\\n")
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
with open(Path(os.environ["HOME"]).parent / "events", "a") as f: f.write("ubs\\n")
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
                        UBS_STAGED_STRICT="1",
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
        script = NATIVE + '''\nroot = str(Path(os.environ['HOME']) / 'ai-society/softwareco/owned/dep-viz')\nsubprocess.run(['git', '-C', root, 'add', 'control'], check=True)\n'''
        self.put("scripts/ci/smoke.sh", script, executable=True)
        self.git("add", "scripts/ci/smoke.sh")
        self.put("control", "working-only-change\n")
        self.install()
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HEAD/index changed during native", result.stderr)

    def test_ubs_index_drift_refuses_before_native(self):
        self.scanner.write_text(SCANNER.replace('sys.exit(1 if',
            "subprocess.run(['git', '-C', str(Path(os.environ['HOME']) / 'ai-society/softwareco/owned/dep-viz'), 'add', 'control'], check=True)\nsys.exit(1 if"))
        self.stage("app.py", "print('changed')\n")
        self.put("control", "working-only-change\n")
        self.install()
        result = self.hook()
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

    def relative_index_case(self, linked):
        root = self.repo
        if linked:
            root = self.work / "linked"
            self.git("worktree", "add", "-qb", "relative-candidate", str(root))
        self.install(root)
        sub = root / "sub"
        sub.mkdir()
        actual_index = Path(self.git("rev-parse", "--path-format=absolute", "--git-path", "index", root=root).stdout.strip())
        caller_index = sub / "index"
        shutil.copy2(actual_index, caller_index)
        shutil.copy2(actual_index, root / "index")
        self.put("app.py", "BAD\n", root=root)
        subprocess.run(["git", "-C", str(root), "add", "app.py"],
                       env=dict(self.env, GIT_INDEX_FILE=str(caller_index)), check=True, capture_output=True)
        gitdir = self.git("rev-parse", "--absolute-git-dir", root=root).stdout.strip()
        for bindings in ({}, {"GIT_DIR": gitdir}, {"GIT_DIR": gitdir, "GIT_WORK_TREE": str(root)}):
            with self.subTest(linked=linked, bindings=bindings):
                env = dict(self.env, GIT_INDEX_FILE="index", **bindings)
                # Git's original-context selection is the oracle, not sub/index
                # inferred from filesystem cwd. Explicit Git bindings matter.
                expected = subprocess.check_output(["git", "write-tree"], cwd=sub, env=env, text=True).strip()
                chosen = Path(subprocess.check_output(["git", "rev-parse", "--path-format=absolute", "--git-path", "index"],
                                                     cwd=sub, env=env, text=True).strip())
                before = chosen.read_bytes()
                content = subprocess.check_output(["git", "show", ":app.py"], cwd=sub, env=env)
                for command in ([str(self.common / "softwareco-offline-hooks-v1/pre-commit")],
                                ["git", "hook", "run", "pre-commit"]):
                    self.log.unlink(missing_ok=True)
                    result = subprocess.run(command, cwd=sub, env=env, capture_output=True, text=True)
                    self.assertIn("candidate-index=" + expected, result.stdout + result.stderr)
                    self.assertEqual(result.returncode == 0, b"BAD" not in content, result.stdout + result.stderr)
                    self.assertEqual(chosen.read_bytes(), before)

    def test_relative_index_matches_original_git_oracle_standalone(self):
        self.relative_index_case(False)

    def test_relative_index_matches_original_git_oracle_linked(self):
        self.relative_index_case(True)

    def symlink_dotdot_index_case(self, linked):
        root = self.repo
        if linked:
            root = self.work / "linked"
            self.git("worktree", "add", "-qb", "symlink-candidate", str(root))
        self.install(root)
        actual = root / "actual"
        (actual / "deep").mkdir(parents=True)
        (root / "link").symlink_to("actual/deep", target_is_directory=True)
        source_index = Path(self.git("rev-parse", "--path-format=absolute", "--git-path", "index", root=root).stdout.strip())
        shutil.copy2(source_index, actual / "index")
        shutil.copy2(source_index, root / "index")
        self.put("app.py", "BAD\n", root=root)
        subprocess.run(["git", "-C", str(root), "add", "app.py"],
                       env=dict(self.env, GIT_INDEX_FILE=str(actual / "index")), check=True, capture_output=True)
        before = (actual / "index").read_bytes()
        result = subprocess.run([str(self.common / "softwareco-offline-hooks-v1/pre-commit")],
                                cwd=root, env=dict(self.env, GIT_INDEX_FILE="link/../index"),
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, "lexical normalization selected a good decoy index")
        self.assertEqual((actual / "index").read_bytes(), before)
        self.assertNotIn("native", self.events())

    def test_actual_git_commit_only_uses_its_temporary_index(self):
        self.stage("safe.txt", "original\n")
        self.git("commit", "-qm", "fixture partial-commit input")
        self.install()
        self.stage("app.py", "BAD\n")
        self.put("safe.txt", "partial commit change\n")
        result = self.git("commit", "--only", "safe.txt", "-m", "fixture real partial commit", check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        committed = self.git("rev-parse", "HEAD^{tree}").stdout.strip()
        self.assertIn("candidate-index=" + committed, result.stdout + result.stderr)
        self.assertEqual(self.git("show", "HEAD:app.py").stdout, "print('good')\n")
        self.assertEqual(self.git("show", ":app.py").stdout, "BAD\n")
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_symlink_dotdot_caller_index_never_selects_decoy_standalone(self):
        self.symlink_dotdot_index_case(False)

    def test_symlink_dotdot_caller_index_never_selects_decoy_linked(self):
        self.symlink_dotdot_index_case(True)

    def installer_control(self):
        spec = importlib.util.spec_from_file_location("installer_fixture", INSTALLER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.index_file(self.repo, "scripts/ci/full.sh")

    def test_installer_helper_rejects_tree_disguised_as_native_blob(self):
        tree = self.git("rev-parse", "HEAD^{tree}").stdout.strip()
        self.git("update-index", "--cacheinfo", "100755", tree, "scripts/ci/full.sh")
        with self.assertRaises(RuntimeError):
            self.installer_control()

    def test_installer_helper_rejects_missing_native_blob(self):
        self.git("update-index", "--cacheinfo", "100755", "1" * 40, "scripts/ci/full.sh")
        with self.assertRaises(subprocess.CalledProcessError):
            self.installer_control()

    def test_installer_helper_rejects_empty_native_blob(self):
        oid = subprocess.check_output(["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
                                      input=b"", env=self.env).decode().strip()
        self.git("update-index", "--cacheinfo", "100755", oid, "scripts/ci/full.sh")
        with self.assertRaises(RuntimeError):
            self.installer_control()

    def test_installer_helper_checks_native_blob_identity_not_only_type_size(self):
        oid = self.git("rev-parse", ":scripts/ci/full.sh").stdout.strip()
        data = (self.repo / "scripts/ci/full.sh").read_bytes()
        forged = b"blob " + str(len(data)).encode() + b"\0partial"
        object_path = self.common / "objects" / oid[:2] / oid[2:]
        object_path.chmod(0o600)  # This test owns its disposable loose object.
        object_path.write_bytes(zlib.compress(forged))
        self.assertEqual(self.git("cat-file", "-t", oid).stdout.strip(), "blob")
        self.assertEqual(self.git("cat-file", "-s", oid).stdout.strip(), str(len(data)))
        with self.assertRaises((RuntimeError, subprocess.CalledProcessError)):
            self.installer_control()

    def test_installer_helper_rejects_truncated_compressed_native_blob(self):
        oid = self.git("rev-parse", ":scripts/ci/full.sh").stdout.strip()
        object_path = self.common / "objects" / oid[:2] / oid[2:]
        compressed = object_path.read_bytes()
        object_path.chmod(0o600)
        object_path.write_bytes(compressed[:len(compressed) // 2])
        with self.assertRaises((RuntimeError, subprocess.CalledProcessError)):
            self.installer_control()

    def test_installer_helper_accepts_actual_readable_native_blob(self):
        self.assertEqual(self.installer_control(), (self.repo / "scripts/ci/full.sh").read_bytes())

    def configure_root_native_fixture(self):
        self.put("scripts/ci/smoke.sh", '#!/bin/sh\nprintf "native\\n" >> "$HOME/../events"\n', executable=True)
        self.git("add", "scripts/ci/smoke.sh")
        self.install()
        config = self.common / "softwareco-offline-hooks-v1/config.json"
        meta = json.loads(config.read_text())
        # Synthetic root-mode transport fixture, never a production installation.
        meta["native_mode"] = "softwareco"
        meta["root_contracts"] = {}
        config.write_text(json.dumps(meta))

    def test_root_native_mode_accepts_unprotected_candidate(self):
        self.configure_root_native_fixture()
        result = self.hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_root_native_mode_refuses_staged_protected_path_before_native(self):
        self.configure_root_native_fixture()
        self.stage("docs/_core/protected.md", "new staged protected content\n")
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Softwareco protected", result.stderr)
        self.assertEqual(self.events(), ["ubs"])

    def test_root_native_mode_refuses_ignored_protected_gitlink(self):
        self.configure_root_native_fixture()
        self.stage(".gitmodules", '[submodule "protected"]\n path = docs/_core/sub\n url = file:///unused\n ignore = all\n')
        head = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("update-index", "--add", "--cacheinfo", "160000", head, "docs/_core/sub")
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Softwareco protected", result.stderr)
        self.assertEqual(self.events(), ["ubs"])

    def test_tree_object_disguised_as_executable_blob_refuses_before_gates(self):
        self.install()
        tree = self.git("rev-parse", "HEAD^{tree}").stdout.strip()
        self.git("update-index", "--cacheinfo", "100755", tree, "scripts/ci/full.sh")
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), [])

    def test_missing_cached_control_blob_refuses_before_gates(self):
        self.install()
        oid = self.git("rev-parse", ":scripts/ci/full.sh").stdout.strip()
        (self.common / "objects" / oid[:2] / oid[2:]).unlink()
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), [])

    def test_protected_gitlink_and_ignore_all_are_transported_to_native_guard(self):
        self.stage(".gitmodules", '[submodule "protected"]\n path = docs/_core/sub\n url = file:///unused\n ignore = all\n')
        head = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("update-index", "--add", "--cacheinfo", "160000", head, "docs/_core/sub")
        self.install()
        result = self.hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.events(), ["ubs"])
        # Native fixture refuses protected input before logging its success event.
        self.assertNotIn("native", self.events())

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


    # AK7597 repair (2026-11-02 inspection D1): the committer's environment must not
    # weaken the checks. Only an allowlist reaches UBS and native checks.
    def test_inherited_environment_cannot_disable_real_ubs(self):
        # A shell call on user input is critical only through categories UBS_SKIP_CATEGORIES can skip
        # (verified against the real scanner: exit 2 without the skip, 0 with it).
        self.stage("app.py", "import os\nos.system(input())\n")  # ubs:ignore[py.security.os-system-shell] fixture data: the staged file the scanner under test must flag; never executed here
        self.use_real_scanner()
        silencer = self.put("bash-env-silencer.sh", "exit 0\n", root=self.work)
        for extra in ({"BASH_ENV": str(silencer)},
                      {"UBS_SKIP_CATEGORIES": ",".join(str(n) for n in range(1, 100))}):
            self.log.unlink(missing_ok=True)
            refused = self.hook(**extra)
            self.assertNotEqual(refused.returncode, 0, f"{extra}: " + refused.stdout[-2000:])
            self.assertNotIn("native", self.events())

    def test_python_path_cannot_hijack_the_hook(self):
        evil = self.work / "evil-python"
        evil.mkdir()
        (evil / "pathlib.py").write_text("raise SystemExit(0)\n")
        self.stage("app.py", "BAD\n")
        self.install()
        refused = self.hook(PYTHONPATH=str(evil))
        self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)

    def test_runner_refuses_an_unisolated_interpreter(self):
        self.stage("app.py", "print('changed')\n")
        self.install()
        config = self.common / "softwareco-offline-hooks-v1/config.json"
        self.assertIn(" -I ", (config.parent / "pre-commit").read_text())
        direct = subprocess.run([sys.executable, str(RUNNER), str(config)], cwd=self.repo,
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(direct.returncode, 2, direct.stdout + direct.stderr)
        self.assertIn("python3 -I", direct.stderr)
        self.assertEqual(self.events(), [])

    def test_checks_receive_only_the_environment_allowlist(self):
        probe = NATIVE + (
            "\nhostile = ['BASH_ENV', 'ENV', 'PYTHONPATH', 'UBS_SKIP_CATEGORIES', 'SSH_AUTH_SOCK',"
            " 'NODE_OPTIONS', 'HOSTILE_PROBE']\n"
            "if any(k in os.environ for k in hostile) or not all(os.environ.get(k) for k in ('HOME', 'TMPDIR'))"
            " or os.environ.get('PATH') != '/usr/bin:/bin':\n"
            "    sys.exit(1)\n")
        self.put("scripts/ci/smoke.sh", probe, executable=True)
        self.git("add", "scripts/ci/smoke.sh")
        self.install()
        silencer = self.put("bash-env-noop.sh", ":\n", root=self.work)
        result = self.hook(BASH_ENV=str(silencer), ENV=str(silencer), PYTHONPATH=str(self.work),
                           UBS_SKIP_CATEGORIES="1", SSH_AUTH_SOCK=str(self.work / "agent"),
                           NODE_OPTIONS="--require=/nonexistent", HOSTILE_PROBE="1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.events(), ["ubs", "native"])

    def test_caller_path_cannot_substitute_tools_or_ubs_modules(self):
        self.stage("app.py", "def risky(x):\n return eval(x)\n")
        self.use_real_scanner()
        hostile = self.work / "hostile-bin"
        hostile.mkdir()
        marker = self.work / "fake-tool-used"
        (hostile / "git").symlink_to(shutil.which("git"))
        for name in ("unshare", "ubs-python"):
            fake = hostile / name
            fake.write_text(f"#!/bin/sh\ntouch {marker}\nexit 0\n")
            fake.chmod(0o755)
        refused = self.hook(PATH=f"{hostile}:{os.environ['PATH']}")
        self.assertNotEqual(refused.returncode, 0, refused.stdout[-2000:] + refused.stderr[-2000:])
        self.assertFalse(marker.exists(), "a tool from the caller's PATH was executed")
        self.assertNotIn("native", self.events())

    def test_replace_refs_cannot_change_the_bytes_native_checks_see(self):
        self.install()
        bad_oid = subprocess.run(["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"], input="bad\n",
                                 env=self.env, capture_output=True, text=True, check=True).stdout.strip()
        good_oid = subprocess.run(["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"], input="good\n",
                                  env=self.env, capture_output=True, text=True, check=True).stdout.strip()
        self.stage("control", "bad\n")
        self.git("replace", bad_oid, good_oid)
        refused = self.hook()
        self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)

    def test_moved_worktree_keeps_its_hooks_override_checked(self):
        self.git("config", "extensions.worktreeConfig", "true")
        linked = self.work / "linked-before-move"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        self.git("config", "--worktree", "core.hooksPath", str(self.work / "elsewhere"), root=linked)
        linked.rename(self.work / "linked-after-move")
        result = self.install(check=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertRegex(result.stderr, "conflicting worktree hooks override|did not activate qualified chain")
        self.assertEqual(self.git("config", "--get", "core.hooksPath", check=False).stdout, "")

    def test_committer_git_config_cannot_run_commands_in_origin_git_calls(self):
        self.stage("control", "bad\n")
        self.install()
        marker = self.work / "fsmonitor-ran"
        fixer = self.put("fixer.sh", f'#!/bin/sh\ntouch {marker}\nfor d in "$TMPDIR"/offline-index-*; do '
                         '[ -d "$d" ] && printf "good\\n" > "$d/control"; done\nexit 1\n',
                         executable=True, root=self.work)
        refused = self.hook(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.fsmonitor", GIT_CONFIG_VALUE_0=str(fixer))
        self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
        self.assertFalse(marker.exists(), "an injected core.fsmonitor command ran")

    def test_global_config_hooks_cannot_run_inside_origin_git_calls(self):
        self.stage("control", "bad\n")
        self.install()
        marker = self.work / "config-hook-ran"
        fixer = self.put("fixer.sh", f'#!/bin/sh\ntouch {marker}\nfor d in "$TMPDIR"/offline-index-*; do '
                         '[ -d "$d" ] && printf "good\\n" > "$d/control"; done\nexit 0\n',
                         executable=True, root=self.work)
        self.put(".gitconfig", f'[hook "fixer"]\n\tevent = post-index-change\n\tcommand = {fixer}\n',
                 root=self.home)
        refused = self.hook()  # the committer even sets GIT_CONFIG_GLOBAL=/dev/null (self.env)
        self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
        self.assertFalse(marker.exists(), "a config-defined hook ran inside the offline hook")

    def test_undecodable_override_path_still_rolls_back(self):
        self.git("config", "extensions.worktreeConfig", "true")
        linked = self.work / "linked-before-move"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        subprocess.run([b"git", b"-C", os.fsencode(linked), b"config", b"--worktree", b"core.hooksPath",
                        os.fsencode(self.work) + b"/\xff-hooks"], env=self.env, check=True)
        linked.rename(self.work / "linked-after-move")
        result = self.install(check=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(self.git("config", "--get", "core.hooksPath", check=False).stdout, "")

    def test_locked_worktree_with_offline_checkout_installs(self):
        linked = self.work / "removable-media"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        self.git("worktree", "lock", str(linked))
        shutil.rmtree(linked)
        self.install()
        self.assertEqual(Path(self.git("config", "--get", "core.hooksPath").stdout.strip()),
                         self.common / "softwareco-offline-hooks-v1")

    def moved_worktree_with(self, configure):
        linked = self.work / "linked-before-move"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        configure(linked)
        linked.rename(self.work / "linked-after-move")

    def assert_install_refused_and_rolled_back(self):
        result = self.install(check=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("did not activate qualified chain", result.stderr)
        self.assertEqual(self.git("config", "--get", "core.hooksPath", check=False).stdout, "")

    def test_moved_worktree_override_through_an_include_is_refused(self):
        self.git("config", "extensions.worktreeConfig", "true")
        included = self.put("hooks-include.cfg", f"[core]\n\thooksPath = {self.work / 'elsewhere'}\n",
                            root=self.work)
        self.moved_worktree_with(lambda linked: self.git("config", "--worktree", "include.path", str(included),
                                                        root=linked))
        self.assert_install_refused_and_rolled_back()

    def test_masked_worktree_config_extension_cannot_hide_an_override(self):
        self.git("config", "extensions.worktreeConfig", "true")
        self.moved_worktree_with(lambda linked: self.git("config", "--worktree", "core.hooksPath",
                                                        str(self.work / "elsewhere"), root=linked))
        self.git("config", "--worktree", "extensions.worktreeConfig", "false")
        self.assert_install_refused_and_rolled_back()

    def test_installer_refuses_repository_outside_scope(self):
        other = self.home / "ai-society/softwareco/owned/other-repo"
        other.mkdir(parents=True)
        for rel in ("scripts/ci/smoke.sh", ".githooks/pre-commit"):
            self.put(rel, (self.repo / rel).read_text(), executable=True, root=other)
        self.git("init", "-q", "-b", "main", root=other)
        self.git("add", ".", root=other)
        self.git("-c", "user.name=f", "-c", "user.email=f@example.invalid", "commit", "-qm", "seed",
                 root=other)
        result = self.install(root=other, check=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("outside exact AK7597", result.stderr)
        self.assertEqual(self.git("config", "--get", "core.hooksPath", root=other, check=False).stdout, "")

    def test_installer_skips_prunable_worktrees_and_activates_live_ones(self):
        live = self.work / "live-linked"
        gone = self.work / "deleted-linked"
        self.git("worktree", "add", "-q", "--detach", str(live))
        self.git("worktree", "add", "-q", "--detach", str(gone))
        shutil.rmtree(gone)
        self.assertIn("prunable", self.git("worktree", "list", "--porcelain").stdout)
        self.install()
        hook = self.common / "softwareco-offline-hooks-v1/pre-commit"
        discovered = self.git("rev-parse", "--path-format=absolute", "--git-path", "hooks/pre-commit", root=live)
        self.assertEqual(Path(discovered.stdout.strip()), hook)
        self.assertIn("prunable", self.git("worktree", "list", "--porcelain").stdout)

    def test_softwareco_mode_is_root_only(self):
        result = subprocess.run([sys.executable, str(INSTALLER), "--repo", str(self.repo),
                                 "--mode", "softwareco"], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("root-only", result.stderr)
        self.assertFalse((self.common / "softwareco-offline-hooks-v1").exists())


# D2: the non-strict wrapper compares per-file critical counts with HEAD. That
# comparison may only pass a failed --staged scan when it is complete and consistent.
STUB_SCANNER = '''#!/usr/bin/env python3
import json, os, sys
with open(os.path.join(os.environ["HOME"], "calls"), "a") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
if "--staged" in sys.argv:
    sys.exit(1)
spec = json.loads(os.environ["STUB_REPORTS"])[os.path.basename(os.getcwd())]
finding = {"severity": "critical", "rule_id": "py.eval-exec", "file": os.path.join(os.getcwd(), "app.py")}
print(json.dumps({"status": spec["status"], "failed_modules": spec["failed"],
                  "findings": [finding] * spec["criticals"]}))
sys.exit(spec["exit"])
'''


class StagedWrapperComparison(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="wrapper-tests-"))
        self.addCleanup(shutil.rmtree, self.work, True)
        self.repo = self.work / "repo"
        self.repo.mkdir()
        self.stub = self.work / "ubs"
        self.stub.write_text(STUB_SCANNER)
        self.stub.chmod(0o755)
        self.env = dict(environment(), HOME=str(self.work), TMPDIR=str(self.work), UBS_BIN=str(self.stub),
                        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
        self.env.pop("UBS_STAGED_STRICT", None)
        for args in (("init", "-q", "-b", "main"), ("config", "user.name", "f"),
                     ("config", "user.email", "f@example.invalid")):
            subprocess.run(["git", *args], cwd=self.repo, env=self.env, check=True)
        (self.repo / "app.py").write_text("print('base')\n")
        subprocess.run(["git", "add", "app.py"], cwd=self.repo, env=self.env, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=self.repo, env=self.env, check=True)
        (self.repo / "app.py").write_text("print('candidate')\n")
        subprocess.run(["git", "add", "app.py"], cwd=self.repo, env=self.env, check=True)

    def run_wrapper(self, head, staged):
        def spec(criticals, exit_code, status="ok", failed=()):
            return {"criticals": criticals, "exit": exit_code, "status": status, "failed": list(failed)}
        env = dict(self.env, STUB_REPORTS=json.dumps({"head": spec(*head), "staged": spec(*staged)}))
        return subprocess.run([str(OWNER / "scripts/ubs-staged.sh")], cwd=self.repo, env=env,
                              capture_output=True, text=True)

    def test_preexisting_criticals_still_pass(self):
        result = self.run_wrapper((1, 1), (1, 1))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_critical_still_refuses(self):
        result = self.run_wrapper((0, 0), (1, 1))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_partial_staged_rescan_refuses(self):
        result = self.run_wrapper((0, 0), (0, 2, "partial", ("python",)))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("keeping the whole-file result", result.stderr)

    def rescans(self):
        return [line for line in (self.work / "calls").read_text().splitlines() if "--format=json" in line]

    def test_rescans_disable_a_foreign_project_config(self):
        self.run_wrapper((1, 1), (1, 1))
        self.assertEqual(len(self.rescans()), 2)
        self.assertTrue(all("--no-config" in line for line in self.rescans()), self.rescans())

    def test_rescans_use_the_checkout_scan_policy(self):
        (self.repo / ".ubs.json").write_text('{"version": 1}\n')
        self.run_wrapper((1, 1), (1, 1))
        expected = f"--config={self.repo}/.ubs.json"
        self.assertTrue(all(expected in line for line in self.rescans()), self.rescans())

    def test_rescan_without_the_failing_criticals_refuses(self):
        result = self.run_wrapper((0, 0), (0, 0))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("keeping the whole-file result", result.stderr)


if __name__ == "__main__":
    unittest.main()
