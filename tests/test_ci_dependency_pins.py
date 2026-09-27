"""Keep CI pins aligned with the indexed dependency adoption, including pre-commit."""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CIDependencyPinsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = (ROOT / ".github/workflows/ci.yml").read_text()
        # The company-specific checks live in local/ (refresh-safe) and, until the next L1
        # refresh replaces it, also in the template checker; every copy must carry the pins.
        checkers = [ROOT / "scripts/check-template-ci.sh", ROOT / "local/ci/check-template-ci.sh"]
        cls.checker = "\n".join(path.read_text() for path in checkers if path.is_file())
        entry = subprocess.check_output(
            ["git", "ls-files", "--stage", "--", "ontology"], cwd=ROOT, text=True
        ).split()
        if len(entry) != 4 or entry[0] != "160000" or entry[2:] != ["0", "ontology"]:
            raise AssertionError("Expected the current ontology submodule topology")
        cls.ontology_oid = entry[1]

    def test_workflow_ontology_pins_match_indexed_gitlink(self) -> None:
        pins = re.findall(r"--expected-oid ([0-9a-f]{40})", self.workflow)
        self.assertEqual(pins, [self.ontology_oid, self.ontology_oid])

    def test_template_checker_pin_matches_indexed_gitlink(self) -> None:
        pins = re.findall(r"expected_oid=([0-9a-f]{40})", self.checker)
        self.assertTrue(pins)
        self.assertEqual(set(pins), {self.ontology_oid})

    def test_core_tags_match_adopted_resolution(self) -> None:
        resolution = json.loads((ROOT / "governance/ontology-dist/resolve.json").read_text())
        core = [layer for layer in resolution["layers"] if layer["name"] == "core"]
        self.assertEqual(len(core), 1)
        match = re.fullmatch(r"<repo:core/ontology-kernel@([^>]+)>", core[0]["origin"])
        self.assertIsNotNone(match)
        assert match is not None
        tags = re.findall(r"git clone --quiet --depth 1 --branch (\S+)", self.workflow)
        self.assertEqual(tags, [match[1], match[1]])
        defaults = re.findall(
            r'assert_yaml_default "copier/tpl-(?:project-repo|monorepo|package)/copier.yml" '
            r"kernel_ontology_ref '([^']+)'",
            self.checker,
        )
        self.assertGreaterEqual(len(defaults), 3)
        self.assertEqual(set(defaults), {core[0]["origin"]})

    def test_core_oid_is_identical_in_both_lanes_and_checker(self) -> None:
        pins = re.findall(
            r'core/ontology-kernel" rev-parse HEAD\)" = \\\n\s+([0-9a-f]{40})',
            self.workflow,
        )
        self.assertEqual(len(pins), 2)
        self.assertEqual(pins[0], pins[1])
        self.assertIn(
            f'assert_contains "$ci_workflow" "{pins[0]}"', self.checker
        )


if __name__ == "__main__":
    unittest.main()
