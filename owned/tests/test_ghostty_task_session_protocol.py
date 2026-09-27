"""Pure consumer contract tests against the exact embedded production validator."""
import copy
import json
import subprocess
import time
from pathlib import Path
import unittest

import test_ghostty_task_session as legacy
LAUNCHER = legacy.LAUNCHER

SOURCE = LAUNCHER.read_text().split("<<'CLASSIFIER'\n", 1)[1].split("\nCLASSIFIER\n", 1)[0]
CONSUMER = {"__name__": "lane_classifier_test"}
exec(compile(SOURCE, str(LAUNCHER) + ":classifier", "exec"), CONSUMER)  # ubs:ignore -- runs the launcher's embedded production classifier under test


class ClassificationProtocolTests(unittest.TestCase):
    def setUp(self):
        self.sent = CONSUMER["request"]([1, 2], str(LAUNCHER.parent))
        self.binding = {
            "schema": "pi.task-session.installed-identity.v1", "producer": CONSUMER["PRODUCER"],
            "configured": True, "akInstance": "synthetic-ak",
            "namespace": {"id": "synthetic", "generation": 1, "snapshotDigest": "a" * 64},
            "classificationExport": "classifyInstalledTaskSessionRequest",
            "classificationRequestSchema": "pi.task-session.classify-installed-request.v1",
        }
        self.binding["identityDigest"] = CONSUMER["digest"](self.binding)
        self.valid = {
            "schema": "pi.task-session.classification.v1",
            "producer": CONSUMER["PRODUCER"].copy(),
            "requestDigest": CONSUMER["digest"](self.sent),
            "identityDigest": self.binding["identityDigest"],
            "namespace": {"id": "synthetic", "generation": 1, "snapshotDigest": "a" * 64},
            "classification": "outside", "reasons": [],
        }

    def validate(self, value):
        raw = json.dumps(value).encode()
        return CONSUMER["classification"](CONSUMER["decode"](raw), self.sent, self.binding)

    def test_outside_and_negative_results(self):
        self.assertEqual(self.validate(self.valid), "outside")
        for state, reasons, namespace in (
            ("enrolled", ["protected_domain"], self.valid["namespace"]),
            ("unknown", ["incomplete_domain_inventory"], self.valid["namespace"]),
            ("unknown", ["not_configured_or_incompatible"], None),
        ):
            with self.subTest(state=state, namespace=namespace):
                value = dict(self.valid, classification=state, reasons=reasons, namespace=namespace)
                if namespace is None:
                    value["identityDigest"] = None
                self.assertEqual(self.validate(value), state)

    def test_exact_response_shape_and_binding(self):
        cases = []
        for key in self.valid:
            value = copy.deepcopy(self.valid)
            del value[key]
            cases.append(value)
        for key, replacement in (
            ("schema", "pi.task-session.classification.v2"),
            ("producer", dict(CONSUMER["PRODUCER"], version="0.9.1")),
            ("producer", dict(CONSUMER["PRODUCER"], extra=True)),
            ("producer", dict(CONSUMER["PRODUCER"], interface="v2")),
            ("requestDigest", "0" * 64), ("namespace", None),
            ("classification", "not-enrolled"), ("classification", None),
            ("reasons", ["uncertainty"]), ("reasons", None),
        ):
            cases.append(dict(self.valid, **{key: replacement}))
        cases.append(dict(self.valid, extra="not allowed"))
        for key, replacement in (
            ("id", ""), ("generation", 0), ("generation", True),
            ("generation", 9007199254740992), ("snapshotDigest", "A" * 64),
        ):
            cases.append(dict(self.valid, namespace=dict(self.valid["namespace"], **{key: replacement})))
        for value in cases:
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                self.validate(value)
        other = CONSUMER["request"]([2, 1], str(LAUNCHER.parent))
        with self.assertRaises(ValueError):
            CONSUMER["classification"](self.valid, other, self.binding)

    def test_json_is_bounded_strict_and_duplicate_rejecting(self):
        for raw in (
            b'{"a":1,"a":2}', b'{"a":{"x":1,"x":2}}', b'{} {}', b'\xff',
            b'\xef\xbb\xbf{}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":1.5}',
            b' ' * 65537, b'', b'{' * 2000,
        ):
            with self.subTest(raw=raw[:40]), self.assertRaises((ValueError, RecursionError)):
                CONSUMER["decode"](raw)

    def test_descriptor_shape_and_digest(self):
        self.assertEqual(CONSUMER["identity"](self.binding), self.binding)
        cases = []
        for key in self.binding:
            value = copy.deepcopy(self.binding)
            del value[key]
            cases.append(value)
        for key, replacement in (
            ("configured", False), ("configured", 1), ("akInstance", ""),
            ("identityDigest", "0" * 64), ("schema", "v2"), ("namespace", None),
            ("classificationExport", "classifyTaskSessionRequest"),
            ("classificationRequestSchema", "pi.task-session.classify-request.v1"),
        ):
            cases.append(dict(self.binding, **{key: replacement}))
        cases.append(dict(self.binding, extra=True))
        for value in cases:
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                CONSUMER["identity"](value)

    def test_descriptor_and_classification_drift(self):
        for key, replacement in (("identityDigest", "b" * 64),
                                 ("namespace", dict(self.binding["namespace"], generation=2))):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(dict(self.valid, **{key: replacement}))

    def test_request_limits_and_stability(self):
        self.assertEqual(self.sent, CONSUMER["request"]([1, 2], str(LAUNCHER.parent)))
        self.assertTrue(self.sent["requestId"].startswith("lane-legacy-"))
        for instance, ids, cwd in (
            ("synthetic-ak", [], str(LAUNCHER.parent)),
            ("synthetic-ak", [1, 1], str(LAUNCHER.parent)),
            ("synthetic-ak", [True], str(LAUNCHER.parent)),
            ("synthetic-ak", [0], str(LAUNCHER.parent)),
            ("synthetic-ak", [9007199254740992], str(LAUNCHER.parent)),
            ("synthetic-ak", list(range(1, 258)), str(LAUNCHER.parent)),
            ("synthetic-ak", [1], "."),
        ):
            with self.subTest(instance=instance, ids=ids[:3], cwd=cwd), self.assertRaises(ValueError):
                CONSUMER["request"](ids, cwd)


class ProducerPipeTests(legacy.IsolatedLauncherTest):

    def producer(self, code):
        path = self.bin / "pi-task-session"
        path.write_text("#!/usr/bin/env python3\n" + code)
        path.chmod(0o755)
        return str(path)

    def test_deadline_covers_blocked_input_and_exit_after_closed_stdout(self):
        for code in (
            "import time; time.sleep(30)",
            "import os, time; os.close(1); time.sleep(30)",
        ):
            with self.subTest(code=code):
                start = time.monotonic()
                with self.assertRaises((ValueError, subprocess.TimeoutExpired)):
                    CONSUMER["call"](self.producer(code), "classify-installed", {"x": "y" * 60000})
                self.assertLess(time.monotonic() - start, 4)
                self.assert_no_effects()

    def test_bounded_call_good_and_bad_output(self):
        for code, okay in (
            ("import sys; sys.stdin.buffer.read(); print('{}')", True),
            ("print('{}'); raise SystemExit(2)", False),
            ("print('x' * 1000000)", False),
            ("print('{} {}')", False),
            ("import os; os.write(1, b'\\xff')", False),
        ):
            with self.subTest(code=code):
                path = self.producer(code)
                # The pipe transport only executes this freshly owned stub.
                if okay:
                    self.assertEqual(CONSUMER["call"](path, "classify", self.env), {})
                else:
                    with self.assertRaises((ValueError, OSError)):
                        CONSUMER["call"](path, "classify", self.env)
                self.assert_no_effects()


if __name__ == "__main__":
    unittest.main()
