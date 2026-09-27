from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "governance/ontology-dist"
BUNDLE_LOCK = ROOT / "tools/rocs-cli/VENDORED_HASHES.json"
EXPECTED_SOURCE_COMMIT = "b72ce580c99eb24e30499b7e3c8502f32eb9ad67"
EXPECTED_LOCK_SHA256 = "259e5264e9c3dc620981448a75efbad0d840d213898c9cacf87655b3980d80b7"
EXPECTED_OUTPUTS = {
    ".rocs-output-root.json",
    ".authority-receipt.lock",
    "authority-receipt.json",
    "authority-receipt.validate.json",
    "authority-receipt.build.json",
    "resolve.json",
    "summary.json",
    "id_index.json",
}
LEGACY_OUTPUTS = {
    "ontology/dist/.authority-receipt.lock",
    "ontology/dist/authority-receipt.json",
    "ontology/dist/authority-receipt.validate.json",
    "ontology/dist/id_index.json",
    "ontology/dist/resolve.json",
    "ontology/dist/summary.json",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


WRAPPER = ROOT / "scripts/rocs.sh"
COMPANY_ENV = ROOT / "local/rocs.env"


def sealed_launcher() -> bool:
    """True while scripts/rocs.sh is the owner-generated sealed 0.4.2 wrapper.

    An L1 template refresh replaces it with the L0 pinned-core launcher, which runs
    ~/ai-society/core/rocs-cli and takes the parent contract from local/rocs.env.
    """
    return "_sealed_memfd" in WRAPPER.read_text(encoding="utf-8")


def launcher_version() -> str:
    result = subprocess.run(
        [str(WRAPPER), "version"], cwd=ROOT, text=True, capture_output=True, check=True
    )
    match = re.search(r"rocs-cli (\d+\.\d+\.\d+)", result.stdout)
    if match is None:
        raise AssertionError(f"unexpected rocs version output: {result.stdout!r}")
    return match.group(1)


class TestOntologyReceipts(unittest.TestCase):
    def test_schema3_bundle_is_bound_to_reviewed_rocs_release(self) -> None:
        if not sealed_launcher():
            self.skipTest("pinned-core launcher: the vendored 0.4.2 bundle is no longer executed")
        lock_bytes = BUNDLE_LOCK.read_bytes()
        self.assertEqual(hashlib.sha256(lock_bytes).hexdigest(), EXPECTED_LOCK_SHA256)
        receipt = json.loads(lock_bytes)
        self.assertEqual(receipt["schema_version"], 3)
        self.assertEqual(receipt["artifact"], "rocs-cli-self-contained")
        self.assertEqual(receipt["upstream_version"], "0.4.2")
        self.assertEqual(receipt["source_commit"], EXPECTED_SOURCE_COMMIT)
        self.assertRegex(receipt["uv_lock_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(receipt["bundle_manifest_digest"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(len(receipt["files"]), 581)

    def test_only_parent_owned_output_root_is_active(self) -> None:
        for relative in LEGACY_OUTPUTS:
            self.assertFalse((ROOT / relative).exists(), relative)

        self.assertTrue(OUTPUT.is_dir())
        self.assertFalse(OUTPUT.is_symlink())
        self.assertEqual({path.name for path in OUTPUT.iterdir()}, EXPECTED_OUTPUTS)
        for path in OUTPUT.iterdir():
            mode = path.lstat().st_mode
            self.assertTrue(stat.S_ISREG(mode), path)
            self.assertFalse(path.is_symlink(), path)

        marker = load_json(OUTPUT / ".rocs-output-root.json")
        self.assertEqual(
            marker,
            {
                "path": "governance/ontology-dist",
                "purpose": "rocs-managed-output",
                "schema": "rocs-managed-output-root/1",
            },
        )

    def test_validate_and_build_receipts_bind_current_parent_identity(self) -> None:
        canonical_repo = str(ROOT.resolve())
        aggregate = load_json(OUTPUT / "authority-receipt.json")
        self.assertEqual(aggregate["schema_version"], 3)
        self.assertEqual(aggregate["version"], "0.4.2" if sealed_launcher() else launcher_version())
        self.assertEqual(aggregate["repo"], canonical_repo)
        self.assertEqual(aggregate["output_root"], "governance/ontology-dist")
        self.assertEqual(aggregate["last_command"], "build")
        self.assertEqual(aggregate["command_files"], {
            "build": "authority-receipt.build.json",
            "validate": "authority-receipt.validate.json",
        })
        self.assertEqual(set(aggregate["commands"]), {"build", "validate"})

        for command in ("validate", "build"):
            command_receipt = load_json(OUTPUT / f"authority-receipt.{command}.json")
            self.assertEqual(command_receipt, aggregate["commands"][command])
            self.assertEqual(command_receipt["repo"], canonical_repo)
            self.assertEqual(command_receipt["output_root"], "governance/ontology-dist")
            self.assertEqual(command_receipt["command"], command)
            self.assertTrue(command_receipt["ok"])
            self.assertTrue(command_receipt["authoritative"])
            self.assertEqual(command_receipt["authority_mode"], "strict_ref_resolution")
            self.assertEqual(command_receipt["workspace_ref_mode"], "strict")
            self.assertTrue(command_receipt["resolve_refs_requested"])

        self.assertEqual(load_json(OUTPUT / "resolve.json")["repo"], canonical_repo)
        self.assertEqual(load_json(OUTPUT / "summary.json")["repo"], canonical_repo)
        resolved = load_json(OUTPUT / "resolve.json")
        layers = {layer["name"]: layer for layer in resolved["layers"]}
        self.assertEqual(
            layers["company"]["src_root"],
            str(ROOT.resolve() / "ontology/src"),
        )
        # rocs-cli >= 0.4.5 binds the pinned core ref to its exact ontology tree: read in place
        # when the kernel checkout's ontology tree is that tree, else from an immutable snapshot.
        # Assert the binding, not a checkout path that moves with kernel main.
        kernel = Path.home() / "ai-society/core/ontology-kernel"
        requested = layers["core"]["origin"].rsplit("@", 1)[1].rstrip(">")
        expected_tree = subprocess.run(
            ["git", "-C", str(kernel), "rev-parse", f"{requested}:ontology"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        core_source = layers["core"]["source"]
        self.assertIn(core_source, {"workspace", "workspace_ref_snapshot"})
        if core_source == "workspace":
            self.assertEqual(layers["core"]["src_root"], str(kernel / "ontology/src"))
        else:
            self.assertTrue(layers["core"]["src_root"].endswith(f"/workspace-ref-snapshots/{expected_tree}/ontology/src"))
        for command in ("validate", "build"):
            receipt_core = [layer for layer in aggregate["commands"][command]["layer_sources"] if layer["name"] == "core"]
            self.assertEqual(len(receipt_core), 1)
            self.assertEqual(receipt_core[0]["source"], core_source)
            self.assertEqual(receipt_core[0]["binding"]["requested_ref"], requested)
            self.assertEqual(receipt_core[0]["binding"]["ontology_tree"], expected_tree)
        self.assertNotIn(".local/state/pi-quests/tmp", json.dumps(resolved))

    def test_parent_producers_declare_external_output_contract(self) -> None:
        wrapper = WRAPPER.read_text(encoding="utf-8")
        full = (ROOT / "scripts/ci/full.sh").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        company_env = COMPANY_ENV.read_text(encoding="utf-8")
        for text in (company_env, workflow):
            self.assertIn("governance/ontology-dist", text)
            self.assertIn("ROCS_AUTHORITY_AGGREGATE", text)
        self.assertIn("ROCS_OUTPUT_ROOT must be $softwareco_output_root", company_env)
        for text in (wrapper, full, workflow, company_env):
            self.assertNotIn("$repo_root/ontology/dist", text)
        if not sealed_launcher():
            # Pinned-core launcher: the parent contract comes from local/rocs.env and the
            # template full gate runs cleanup -> validate -> build through the launcher.
            self.assertIn('. "$repo/local/rocs.env"', wrapper)
            self.assertIn("./scripts/rocs.sh cleanup --repo .", full)
            self.assertIn("scripts/lib/run-local-hook.sh local/ci/full.sh", full)
            return
        for text in (wrapper, full):
            self.assertIn("governance/ontology-dist", text)
            self.assertIn("ROCS_AUTHORITY_AGGREGATE", text)
        self.assertIn('ROCS_REPO="$repo_root" "$repo_root/scripts/rocs.sh"', full)
        self.assertIn("_TRUSTED_RECEIPT_SHA256 = \"259e5264e9c3dc620981448a75efbad0d840d213898c9cacf87655b3980d80b7\"", wrapper)
        self.assertIn("_private_archive", wrapper)
        self.assertIn("_sealed_memfd", wrapper)
        self.assertIn("ROCS_OUTPUT_ROOT must be $required_output_root", wrapper)
        self.assertIn("ROCS_OUTPUT_ROOT must be $required_output_root", full)
        self.assertIn("refusing ROCS cleanup with unknown managed output", full)

    def test_wrapper_rejects_noncanonical_output_override_before_execution(self) -> None:
        env = os.environ.copy()
        env["ROCS_OUTPUT_ROOT"] = "governance/alternate-output"
        result = subprocess.run(
            [str(WRAPPER), "version"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("ROCS_OUTPUT_ROOT must be governance/ontology-dist", result.stderr)
        self.assertFalse((ROOT / "governance/alternate-output").exists())

    def test_generic_launcher_rejects_nonparent_repo_targets(self) -> None:
        result = subprocess.run(
            [
                str(WRAPPER),
                "validate",
                "--repo",
                "ontology",
                "--resolve-refs",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--repo must be the Softwareco parent", result.stderr)
        self.assertFalse((ROOT / "ontology/governance/ontology-dist").exists())

        env = os.environ.copy()
        env["ROCS_REPO"] = str(ROOT / "ontology")
        env_result = subprocess.run(
            [str(WRAPPER), "version"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(env_result.returncode, 2)
        self.assertIn("ROCS_REPO must be the Softwareco parent", env_result.stderr)

    def test_generic_sealed_launcher_preserves_diagnostic_contract(self) -> None:
        if not sealed_launcher():
            doctor = subprocess.run(
                [str(WRAPPER), "--doctor"], cwd=ROOT, text=True, capture_output=True, check=False
            )
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertIn("output root: governance/ontology-dist", doctor.stdout)
            self.assertIn("company env: local/rocs.env", doctor.stdout)
            self.assertRegex(doctor.stdout, r"ok: rocs-cli \d+\.\d+\.\d+ satisfies pin")
            return
        which = subprocess.run(
            ["bash", str(ROOT / "scripts/rocs.sh"), "--which"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(which.returncode, 0, which.stderr)
        self.assertIn("owner-generated sealed vendored ROCS 0.4.2", which.stdout)

        version = subprocess.run(
            ["bash", str(ROOT / "scripts/rocs.sh"), "version"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(version.returncode, 0, version.stderr)
        self.assertIn("rocs-cli 0.4.2", version.stdout)


if __name__ == "__main__":
    unittest.main()
