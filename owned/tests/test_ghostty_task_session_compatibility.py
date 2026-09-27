"""Whole launcher process tests using explicit synthetic producer/runtime stubs."""
import json
import time
import unittest

import test_ghostty_task_session as legacy

PRODUCER_STUB = r"""#!/usr/bin/env python3
import hashlib, json, os, sys
from pathlib import Path

def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, ensure_ascii=False,
                         separators=(',', ':')).encode()).hexdigest()
mode = os.environ.get('TEST_CLASSIFICATION', 'outside')
producer = {'package': '@tryinget/pi-little-helpers', 'version': '0.9.0',
            'interface': 'pi.task-session.classification.v1'}
ns = {'id': 'synthetic', 'generation': 1, 'snapshotDigest': 'a' * 64}
identity = {'schema': 'pi.task-session.installed-identity.v1', 'producer': producer,
            'configured': True, 'akInstance': 'synthetic-ak', 'namespace': ns,
            'classificationExport': 'classifyInstalledTaskSessionRequest',
            'classificationRequestSchema': 'pi.task-session.classify-installed-request.v1'}
identity['identityDigest'] = digest(identity)
op = sys.argv[1]
request = json.load(sys.stdin) if op == 'classify-installed' else None
with open(os.environ['TEST_EVENTS'], 'a') as f:
    f.write(json.dumps({'name': 'producer', 'args': sys.argv[1:], 'request': request}) + '\n')
if mode == 'exit': raise SystemExit(2)
if mode == 'invalid': print('{} {}'); raise SystemExit()
if mode == 'duplicate': print('{"schema":1,"schema":2}'); raise SystemExit()
if mode == 'huge': print('x' * 1000000); raise SystemExit()
if mode == 'utf8': os.write(1, b'\xff'); raise SystemExit()
if op == 'identity':
    if mode == 'unconfigured': identity['configured'] = False
    if mode == 'bad-producer': identity['producer']['version'] = '0.9.1'
    if mode == 'bad-identity': identity['identityDigest'] = '0' * 64
    print(json.dumps(identity))
    raise SystemExit()
assert op == 'classify-installed'
assert set(request) == {'schema', 'requestId', 'taskIds', 'cwd'}
assert request['schema'] == 'pi.task-session.classify-installed-request.v1'
# These explicit test outcomes do not replace producer conflict semantics.
state = 'enrolled' if mode == 'enrolled' else 'unknown' if mode == 'unknown' else 'outside'
value = {'schema': 'pi.task-session.classification.v1', 'producer': producer,
         'requestDigest': digest(request), 'identityDigest': identity['identityDigest'],
         'namespace': ns, 'classification': state,
         'reasons': [] if state == 'outside' else ['synthetic_denial']}
if mode == 'wrong-request': value['requestDigest'] = '0' * 64
if mode == 'wrong-identity': value['identityDigest'] = 'b' * 64
if mode == 'drift': value['namespace'] = dict(ns, generation=2)
if mode == 'no-namespace': value['namespace'] = None
if mode == 'unknown-field': value['extra'] = True
print(json.dumps(value))
"""

RUNTIME_STUB = r"""#!/usr/bin/env python3
import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
fields = ['PI_TARGET_REPO', 'PI_LAUNCH_PROMPT', 'PI_TASK_ID', 'PI_TASK_TITLE',
          'PI_TASK_STDOUT_LOG', 'PI_TASK_STDERR_LOG', 'PI_TASK_HOLD_OPEN']
with open(os.environ['TEST_EVENTS'], 'a') as f:
    f.write(json.dumps({'name': name, 'args': sys.argv[1:],
                       'env': {k: os.environ[k] for k in fields if k in os.environ}}) + '\n')
if name == 'ak':
    print(json.dumps({'repo': os.environ['TEST_REPO'], 'title': 'Synthetic task', 'status': 'ready'}))
elif name == 'mkdir':
    for p in sys.argv[1:]:
        if p == '-p': continue
        path = pathlib.Path(p)
        assert path.is_relative_to(pathlib.Path(os.environ['HOME']))
        path.mkdir(parents=True, exist_ok=True)
elif name == 'date':
    print('20260907T000000' if sys.argv[1] == '+%Y%m%dT%H%M%S' else '123456789')
elif name == 'basename':
    print(pathlib.Path(sys.argv[1]).name)
elif name == 'niri' and sys.argv[1:] == ['msg', '-j', 'windows']:
    print(json.dumps([{'id': 7, 'app_id': 'synthetic', 'title': 'π - synthetic-repo'}]))
# ghostty deliberately does NOT run its shell payload; Pi is never executed.
"""


class LegacyCompatibilityTests(legacy.IsolatedLauncherTest):
    def setUp(self):
        super().setUp()
        for name, source in [('pi-task-session', PRODUCER_STUB)] + [
            (n, RUNTIME_STUB) for n in ('ak', 'mkdir', 'date', 'basename', 'ghostty', 'pi', 'niri', 'sleep')
        ]:
            compile(source, name, 'exec')
            path = self.bin / name
            path.write_text(source)
            path.chmod(0o755)

    def assert_refused_without_legacy_effects(self, result):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(all(e['name'] == 'producer' for e in self.recorded()))
        self.assertFalse(self.logs.exists())

    def test_entire_batch_and_preset_refuse_negative_classification(self):
        for mode in ('enrolled', 'unknown'):
            self.env['TEST_CLASSIFICATION'] = mode
            for ids, args in (([1, 2], ['1', '2']),
                              (list(range(609, 616)), ['--justfile-rollout-pilots']),
                              ([1, *range(609, 616), 999], ['1', '--justfile-rollout-pilots', '999'])):
                with self.subTest(mode=mode, args=args):
                    self.events.unlink(missing_ok=True)
                    result = self.run_launcher('--focus-last', '--log-dir', str(self.logs), *args)
                    self.assert_refused_without_legacy_effects(result)
                    events = self.recorded()
                    self.assertEqual([e['args'] for e in events], [['identity'], ['classify-installed']])
                    self.assertEqual(events[-1]['request']['taskIds'], ids)
                    self.assertNotIn('akInstance', events[-1]['request'])

    def test_incompatible_producer_refuses_before_any_legacy_effect(self):
        for mode in ('exit', 'invalid', 'duplicate', 'huge', 'utf8', 'unconfigured',
                     'bad-producer', 'bad-identity', 'wrong-request', 'wrong-identity',
                     'drift', 'no-namespace', 'unknown-field'):
            with self.subTest(mode=mode):
                self.events.unlink(missing_ok=True)
                self.env['TEST_CLASSIFICATION'] = mode
                self.assert_refused_without_legacy_effects(self.run_launcher('--dry-run', '1', '2'))

    def test_parse_and_help_never_invoke_even_available_producer(self):
        for args, code in ((['--help'], 0), (['1', '--help'], 2),
                           (['--interactive', '--print', '1'], 2),
                           (['--justfile-rollout-pilots', '609'], 2)):
            with self.subTest(args=args):
                self.assertEqual(self.run_launcher(*args).returncode, code)
                self.assertEqual(self.recorded(), [])

    def test_positive_outside_dry_run_modes_logs_and_whole_batch(self):
        for options, ids, mode, hold in (([], ['1'], 'interactive', '0'),
                ([], ['1', '2'], 'print', '0'),
                (['--print'], ['1'], 'print', '1'),
                (['--print', '--no-hold-open'], ['1'], 'print', '0'),
                (['--interactive'], ['1', '2'], 'interactive', '0'),
                (['--print', '--hold-open'], ['1', '2'], 'print', '1'),
                (['--justfile-rollout-pilots'], [], 'print', '0')):
            with self.subTest(options=options, ids=ids):
                self.events.unlink(missing_ok=True)
                result = self.run_launcher('--dry-run', '--log-dir', str(self.logs), *options, *ids)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('launch_mode_default=' + mode, result.stdout)
                self.assertIn('hold_open_default=' + hold, result.stdout)
                events = self.recorded()
                self.assertEqual([e['name'] for e in events[:2]], ['producer', 'producer'])
                expected = list(range(609, 616)) if not ids else list(map(int, ids))
                self.assertEqual(events[1]['request']['taskIds'], expected)
                self.assertEqual([e['args'] for e in events if e['name'] == 'ak'],
                                 [['task', 'show', str(i), '-F', 'json'] for i in expected])
                self.assertTrue(self.logs.is_dir())
                self.assertFalse(any(e['name'] in ('ghostty', 'pi', 'niri') for e in events))

    def launched(self, *args, count):
        result = self.run_launcher(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            events = self.recorded()
            launches = [e for e in events if e['name'] == 'ghostty']
            if len(launches) == count:
                return result, events, launches
            time.sleep(0.01)
        self.fail('synthetic Ghostty stub did not finish')

    def test_positive_outside_interactive_shell_argv_and_prompt(self):
        result, events, launches = self.launched('1', count=1)
        launch = launches[0]
        self.assertEqual(launch['args'][1:4], ['-e', 'bash', '-lc'])
        self.assertIn('pi "$PI_LAUNCH_PROMPT"', launch['args'][4])
        self.assertEqual(launch['env']['PI_TARGET_REPO'], str(self.repo))
        self.assertEqual(launch['env']['PI_TASK_ID'], '1')
        self.assertIn('attend next ak task #1', launch['env']['PI_LAUNCH_PROMPT'])
        self.assertNotIn('PI_TASK_STDOUT_LOG', launch['env'])
        self.assertFalse(any(e['name'] == 'pi' for e in events))

    def test_positive_outside_print_logs_hold_and_focus(self):
        result, events, launches = self.launched('--focus-last', '--print', '--hold-open',
                                               '--log-dir', str(self.logs), '1', '2', count=2)
        self.assertIn('focused_last_window=7', result.stdout)
        self.assertTrue(any(e['name'] == 'niri' and e['args'][:3] == ['msg', 'action', 'focus-window'] for e in events))
        for launch in launches:
            self.assertIn('pi -p "$PI_LAUNCH_PROMPT"', launch['args'][4])
            self.assertEqual(launch['env']['PI_TASK_HOLD_OPEN'], '1')
            task = launch['env']['PI_TASK_ID']
            self.assertEqual(launch['env']['PI_TASK_STDOUT_LOG'], str(self.logs / f'task-{task}.stdout.log'))
        self.assertFalse(any(e['name'] == 'pi' for e in events))


if __name__ == '__main__':
    unittest.main()
