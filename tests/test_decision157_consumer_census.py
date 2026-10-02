"""DB-free synthetic fixtures for the Decision157 read-only inventory."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "census", Path(__file__).resolve().parents[1] / "local/scripts/decision157-consumer-census.py"
)
assert SPEC and SPEC.loader
CENSUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CENSUS)


class CensusTests(unittest.TestCase):
    def setUp(self):
        scratch = os.environ.get("TMPDIR", str(Path(__file__).resolve().parents[1]))
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "softwareco"
        self.workspace.mkdir()
        self.repo = self.workspace / "owned/demo"
        self.repo.mkdir(parents=True)
        for args in (("init", "-q"), ("config", "user.name", "fixture"),
                     ("config", "user.email", "fixture@example.invalid")):
            self.git(*args)
        (self.repo / ".copier-answers.yml").write_text(
            'company_ontology_ref: "<repo:softwareco/ontology@main>"\n'
        )
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def git(self, *args):
        env = {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
        command = ["/usr/bin/git", "-c", f"core.hooksPath={os.devnull}", "-c", "core.fsmonitor=false",
                   "-C", str(self.repo), *args]
        return subprocess.check_output(command, text=True, env=env, timeout=30)

    def collect(self, paths=None):
        return CENSUS.collect(
            [{"path": str(p), "company": "softwareco"} for p in (paths or [self.repo])],
            self.workspace,
        )

    def test_index_and_worktree_drift_are_both_retained(self):
        (self.repo / ".copier-answers.yml").write_text(
            'company_ontology_ref: "<repo:softwareco@main>"\n'
        )
        report = self.collect()
        rows = report["inputs"]
        self.assertEqual({r["origin"] for r in rows}, {"index", "worktree"})
        self.assertEqual({ref["class"] for row in rows for ref in row["references"]},
                         {"old_owner", "parent"})
        self.assertFalse(report["closure_complete"])

    def test_nested_generation_input_and_untracked_manifest(self):
        nested = self.repo / "apps/fixture/.copier-answers.yml"
        nested.parent.mkdir(parents=True)
        nested.write_text('company_ontology_ref: "<repo:softwareco/ontology@main>"\n')
        self.git("add", "apps")
        manifest = self.repo / "ontology/manifest.yaml"
        manifest.parent.mkdir()
        manifest.write_text('ref: "../../ontology"\n')
        report = self.collect()
        rows = report["inputs"]
        self.assertTrue(any(r["path"] == "apps/fixture/.copier-answers.yml" for r in rows))
        row = next(r for r in rows if r["path"] == "ontology/manifest.yaml")
        self.assertFalse(row["tracked"])
        self.assertEqual(row["references"][0]["class"], "relative")

    def test_shared_git_root_is_not_an_independent_registration(self):
        child = self.repo / "package"
        child.mkdir()
        report = self.collect([self.repo, child])
        self.assertEqual(len(report["git_roots"]), 1)
        statuses = {r["status"] for r in report["registrations"]}
        self.assertEqual(statuses, {"independent", "enclosing_git_root"})

    def test_missing_external_and_symlinked_roots_fail_closed(self):
        link = self.workspace / "link"
        link.symlink_to(self.repo, target_is_directory=True)
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        report = self.collect([link, outside, self.workspace / "missing"])
        self.assertEqual({r["status"] for r in report["registrations"]},
                         {"symlink_path", "outside_workspace", "missing"})
        self.assertEqual(report["inputs"], [])

    def test_symlinked_input_is_not_followed(self):
        manifest = self.repo / "ontology/manifest.yaml"
        manifest.parent.mkdir()
        manifest.symlink_to(self.repo / ".copier-answers.yml")
        report = self.collect()
        self.assertTrue(any(r["reason"] == "symlink_path" for r in report["omissions"]))
        self.assertFalse(any(r["path"] == "ontology/manifest.yaml" for r in report["inputs"]))

    def test_repository_state_unchanged(self):
        before = self.git("status", "--porcelain=v1")
        head = self.git("rev-parse", "HEAD")
        self.collect()
        self.assertEqual(before, self.git("status", "--porcelain=v1"))
        self.assertEqual(head, self.git("rev-parse", "HEAD"))

    def test_refs_classified_without_executing_embedded_text(self):
        references = CENSUS.references(
            'ref: "<repo:softwareco/ontology@deadbeef>"\n'
            'company_ontology_ref: "<repo:healthco@main>"\n'
            'ref: "<gitlab:example/company@main>"\n'
        )
        self.assertEqual({r["class"] for r in references},
                         {"old_owner_variant", "other_company", "legacy_gitlab"})

    def test_prefixed_and_legacy_old_owner_are_not_other_company(self):
        refs = CENSUS.references(
            'ref: "<repo:ai-society/softwareco/ontology@main>"\n'
            'ref: "<gitlab:ai-society/softwareco/ontology@main>"\n'
            'ref: "<repo:other/core/ontology-kernel@main>"\n'
        )
        self.assertEqual([r["class"] for r in refs], ["old_owner", "old_owner", "other_company"])
        self.assertEqual(refs[1]["transport"], "gitlab")

    def test_fsmonitor_hook_never_executes(self):
        marker = self.workspace / "hook-executed"
        hook = self.workspace / "fsmonitor"
        hook.write_text(f'#!/bin/sh\nprintf invoked >> "{marker}"\n')
        hook.chmod(0o700)
        self.git("config", "core.fsmonitor", str(hook))
        report = self.collect()
        self.assertFalse(marker.exists())
        self.assertEqual(report["summary"]["omissions"], 0)

    def test_external_gitdir_is_rejected_before_inventory(self):
        metadata = self.repo / ".git"
        external = Path(self.temp.name) / "metadata"
        metadata.rename(external)
        metadata.symlink_to(external, target_is_directory=True)
        report = self.collect()
        self.assertEqual(report["inputs"], [])
        self.assertEqual(report["registrations"][0]["status"], "git_error")
        self.assertIn("git_metadata", report["registrations"][0]["error"])

    def test_gitdir_file_cannot_escape_workspace(self):
        metadata = self.repo / ".git"
        external = Path(self.temp.name) / "metadata"
        metadata.rename(external)
        metadata.write_text(f"gitdir: {external}\n")
        self.assertEqual(self.collect()["inputs"], [])

    def test_alternates_rejected(self):
        alternate = self.repo / ".git/objects/info/alternates"
        alternate.write_text(str(Path(self.temp.name) / "other-objects"))
        report = self.collect()
        self.assertEqual(report["inputs"], [])
        self.assertIn("alternates", report["registrations"][0]["error"])

    def test_absent_root_inputs_are_explicit(self):
        report = self.collect()
        absent = {r["path"] for r in report["coverage"] if r["worktree_status"] == "absent"}
        self.assertEqual(absent, {"ontology/manifest.yaml", "copier.yml"})

    def test_invalid_utf8_does_not_hide_other_inputs(self):
        (self.repo / "copier.yml").write_bytes(b"\xff")
        self.git("add", "copier.yml")
        report = self.collect()
        self.assertTrue(any(r["reason"] == "invalid_utf8" for r in report["omissions"]))
        self.assertTrue(any(r["path"] == ".copier-answers.yml" for r in report["inputs"]))

    def test_rejected_worktree_redirect_does_not_enqueue_root(self):
        sibling = self.workspace / "owned/sibling"
        sibling.mkdir()
        self.git("config", "core.worktree", str(sibling))
        report = self.collect()
        self.assertEqual(report["git_roots"], [])
        self.assertEqual(report["inputs"], [])
        self.assertEqual(report["registrations"][0]["error"], "git_root_not_registration_ancestor")

    def test_bom_prefixed_config_include_rejected(self):
        config = self.repo / ".git/config"
        config.write_text('\ufeff[include]\n path = /nonexistent/external\n' + config.read_text())
        report = self.collect()
        self.assertEqual(report["inputs"], [])
        self.assertEqual(report["registrations"][0]["error"], "unsupported_git_config_include")

    def test_unreadable_reference_directory_fails_closed(self):
        directory = self.repo / ".git/refs/heads"
        directory.chmod(0o100)
        self.addCleanup(directory.chmod, 0o700)
        report = self.collect()
        self.assertEqual(report["inputs"], [])
        self.assertEqual(report["registrations"][0]["error"], "uninspectable_git_metadata")

    def test_fifo_head_refused_without_invoking_git(self):
        head = self.repo / ".git/HEAD"
        head.unlink()
        os.mkfifo(head)
        report = self.collect()
        self.assertEqual(report["inputs"], [])
        self.assertEqual(report["registrations"][0]["error"], "nonregular_git_metadata_member")

    def test_replacement_blob_does_not_change_index_observation(self):
        indexed = self.git("rev-parse", ":.copier-answers.yml").strip()
        replacement_path = self.workspace / "replacement"
        replacement_path.write_text('company_ontology_ref: "<repo:softwareco@main>"\n')
        replacement = self.git("hash-object", "-w", str(replacement_path)).strip()
        self.git("replace", indexed, replacement)
        report = self.collect()
        indexed_row = next(r for r in report["inputs"] if r["origin"] == "index")
        self.assertEqual(indexed_row["references"][0]["class"], "old_owner")
        self.assertEqual(indexed_row["blob"], indexed)

    def test_relative_path_layers_include_company_not_self_source(self):
        refs = CENSUS.references(
            '    - name: company\n      path: "../../ontology/src"\n'
            '    - name: repo\n      path: "ontology/src"\n'
            '    - path: "../ontology/src"\n'
        )
        self.assertEqual([r["locator"] for r in refs],
                         ["../../ontology/src", "../ontology/src"])
        self.assertEqual({r["class"] for r in refs}, {"relative"})

    def test_git_uses_fixed_executable_and_clean_environment(self):
        poison = {"PATH": "/untrusted/bin", "LD_PRELOAD": "/untrusted/loader.so",
                  "PYTHONPATH": "/untrusted/modules", "GIT_DIR": "/untrusted/repository"}
        with mock.patch.dict(os.environ, poison), mock.patch.object(CENSUS.subprocess, "run") as execute:
            execute.return_value = subprocess.CompletedProcess([], 0, stdout=b"fixture\n", stderr=b"")
            self.assertEqual(CENSUS.git(self.repo, "rev-parse", "HEAD"), b"fixture\n")
        argv = execute.call_args.args[0]
        environment = execute.call_args.kwargs["env"]
        self.assertEqual(argv[0], "/usr/bin/git")
        self.assertEqual(environment["PATH"], os.defpath)
        for key in ("LD_PRELOAD", "PYTHONPATH", "GIT_DIR"):
            self.assertNotIn(key, environment)


if __name__ == "__main__":
    unittest.main()
