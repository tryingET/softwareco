"""Opt-in real emitted classifier body, synthetic filesystem; no OS account locator.

TASK_SESSION_PRODUCER_DIST must explicitly name the reviewed emitted task-session
folder. Pins stop accidental testing of a different concurrent mutable build.
This test shim selects the owner's internal synthetic locator seam, not the
public CLI's account lookup. Production launcher has no test/locator override.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import unittest

import test_ghostty_task_session as legacy
import test_ghostty_task_session_compatibility as compatibility

PINS = {
    'installed-identity.js': 'c8b1804c8de466cc342d5bf9f916cf0d87671de4646f588f40eab63c057469b1',
    'classify.js': 'ea714789ce1a45eb4ed596e6498b1e32bab9464a9945a15ef45e15f057f1aeb2',
    'state.js': 'b2303b1438b12105bbccfc6e466a56d9236173ca3da043d623f167bcd8d64106',
    'json.js': '39575888a264343d386d9f97c2f909d89ec99c6d95a4c74e49e07696c5e7a673',
    'native.js': 'a34ed26e977bbd9a85eb2bf76ac85a771aa0f1a409e0975af4ed903b80aea3ac',
}


@unittest.skipUnless(os.environ.get('TASK_SESSION_PRODUCER_DIST'),
                     'emitted producer proof requires explicit reviewed artifact path')
class EmittedClassifierTests(legacy.IsolatedLauncherTest):
    def setUp(self):
        super().setUp()
        self.dist = Path(os.environ['TASK_SESSION_PRODUCER_DIST']).resolve(strict=True)
        for name, expected in PINS.items():
            self.assertEqual(hashlib.sha256((self.dist / name).read_bytes()).hexdigest(), expected, name)
        for name in ('ak', 'mkdir', 'date', 'basename', 'ghostty', 'pi', 'niri', 'sleep'):
            path = self.bin / name
            path.write_text(compatibility.RUNTIME_STUB)
            path.chmod(0o755)
        self.state_root = self.base / 'synthetic-namespace'
        self.state_root.mkdir(mode=0o700)
        lock = self.state_root / 'namespace.lock'
        lock.touch(mode=0o600)
        root_stat, lock_stat = self.state_root.stat(), lock.stat()
        locator = {'schema': 'pi.task-session.locator.v1', 'namespace': 'synthetic',
                   'root': str(self.state_root), 'uid': os.getuid(),
                   'rootDev': root_stat.st_dev, 'rootIno': root_stat.st_ino,
                   'lockDev': lock_stat.st_dev, 'lockIno': lock_stat.st_ino}
        domains = []
        for task in [1, 2, *range(609, 616)]:
            checkout = self.repo if task == 1 else self.base / f'checkout-{task}'
            checkout.mkdir(exist_ok=True)
            git = checkout / '.git'
            git.mkdir()
            physical = lambda p: f'{p.stat().st_dev}:{p.stat().st_ino}'
            domains.append({'akInstance': 'synthetic-ak', 'taskId': task,
                            'checkout': str(checkout), 'commonGit': str(git),
                            'sharedEffects': [],
                            'physical': {'checkout': physical(checkout), 'commonGit': physical(git)}})
        self.state = {'schema': 'pi.task-session.state.v1', 'namespace': 'synthetic',
                      'generation': 1, 'withdrawn': False, 'inventoryComplete': True,
                      'domains': domains, 'enrolled': [], 'attempts': []}
        self.state_path = self.state_root / 'state.json'
        self.publish()
        # Only owned synthetic files are read here. The public account locator is
        # deliberately never called. No invented classification success branch.
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node required for explicit emitted proof')
        shim = self.bin / 'producer.mjs'
        shim.write_text(f'#!{node}\n' + f'''
import {{ identityFromSnapshot, classifyInstalledInNamespace }} from {json.dumps((self.dist / 'installed-identity.js').as_uri())};
import {{ readSnapshot }} from {json.dumps((self.dist / 'state.js').as_uri())};
import {{ parseJson }} from {json.dumps((self.dist / 'json.js').as_uri())};
import {{ appendFileSync }} from 'node:fs';
const locator = {json.dumps(locator)};
const op = process.argv[2];
try {{
  let request = null;
  if (op === 'classify-installed') {{
    let input = ''; for await (const c of process.stdin) input += c;
    request = parseJson(input, 65536);
  }}
  if (!['identity', 'classify-installed'].includes(op)) throw Error('bad_operation');
  const response = op === 'identity' ? identityFromSnapshot(readSnapshot(locator))
                                    : classifyInstalledInNamespace(request, locator);
  appendFileSync(process.env.TEST_EVENTS, JSON.stringify({{name:'producer',args:[op],request,response}}) + '\\n');
  console.log(JSON.stringify(response));
}} catch {{ process.exitCode = 2; }}
''')
        shim.chmod(0o755)
        (self.bin / 'pi-task-session').symlink_to(shim)

    def publish(self):
        self.state_path.write_text(json.dumps(self.state))
        self.state_path.chmod(0o600)

    def classify(self, args, allowed, outcome=None):
        self.events.unlink(missing_ok=True)
        self.publish()
        before = self.state_path.read_bytes()
        result = self.run_launcher('--dry-run', *args)
        self.assertEqual(result.returncode, 0 if allowed else 2, result.stderr)
        events = self.recorded()
        if outcome is not None:
            self.assertEqual(events[1]['response']['classification'], outcome)
        if not allowed:
            self.assertTrue(all(e['name'] == 'producer' for e in events))
        self.assertEqual(self.state_path.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.state_root.iterdir()), ['namespace.lock', 'state.json'])
        return events

    def test_real_emitted_outside_whole_batch_and_preset(self):
        # Ambient Node flags must not become executable classifier bootstrap input.
        self.env["NODE_OPTIONS"] = "--invalid-task-session-test-option"
        self.env["NODE_PATH"] = str(self.base / "not-a-module-registry")
        for args, ids in ((['1'], [1]), (['1', '2'], [1, 2]),
                          (['--justfile-rollout-pilots'], list(range(609, 616)))):
            with self.subTest(args=args):
                events = self.classify(args, True, 'outside')
                self.assertEqual(events[1]['request']['taskIds'], ids)
                self.assertEqual([e['args'][2] for e in events if e['name'] == 'ak'], list(map(str, ids)))

    def test_real_emitted_mixed_unknown_and_enrolled(self):
        self.classify(['1', '999'], False, 'unknown')
        self.state['enrolled'] = [self.state['domains'][1]]
        self.classify(['1'], True, 'outside')
        self.classify(['1', '2'], False, 'enrolled')
        self.state['enrolled'] = [self.state['domains'][-1]]
        self.classify(['--justfile-rollout-pilots'], False, 'enrolled')

    def test_real_emitted_unknown_identity_refuses(self):
        original = copy.deepcopy(self.state)
        for change in ('withdrawn', 'incomplete', 'mixed-instance', 'physical-replaced'):
            with self.subTest(change=change):
                self.state = copy.deepcopy(original)
                if change == 'withdrawn': self.state['withdrawn'] = True
                if change == 'incomplete': self.state['inventoryComplete'] = False
                if change == 'mixed-instance': self.state['domains'][1]['akInstance'] = 'other-ak'
                if change == 'physical-replaced': self.state['domains'][1]['physical']['checkout'] = '1:1'
                self.classify(['1'], False)

    def test_real_emitted_independent_conflict_predicates(self):
        original = copy.deepcopy(self.state)
        for kind in ('task-only', 'common-git', 'overlap', 'shared-effect', 'unresolved'):
            with self.subTest(kind=kind):
                self.state = copy.deepcopy(original)
                target = self.state['domains'][0]
                protected = copy.deepcopy(self.state['domains'][1])
                # Enrolled domains must be physically real: the producer refuses a recorded path whose
                # inode or Git topology differs on disk (D151-I01) before it classifies anything.
                physical = lambda p: f'{p.stat().st_dev}:{p.stat().st_ino}'
                if kind == 'task-only': protected['taskId'] = 1
                if kind == 'common-git':
                    # A linked worktree of the target's repository: same common Git directory.
                    shared = Path(target['commonGit'])
                    worktree = self.base / 'linked-worktree'
                    admin = shared / 'worktrees' / 'linked'
                    admin.mkdir(parents=True, exist_ok=True)
                    (admin / 'commondir').write_text('../..\n')
                    worktree.mkdir(exist_ok=True)
                    (worktree / '.git').write_text(f'gitdir: {admin}\n')
                    protected['checkout'] = str(worktree)
                    protected['commonGit'] = target['commonGit']
                    protected['physical'] = {'checkout': physical(worktree), 'commonGit': physical(shared)}
                if kind == 'overlap':
                    nested = self.repo / 'nested'
                    (nested / '.git').mkdir(parents=True, exist_ok=True)
                    protected['checkout'], protected['commonGit'] = str(nested), str(nested / '.git')
                    protected['physical'] = {'checkout': physical(nested), 'commonGit': physical(nested / '.git')}
                if kind == 'shared-effect':
                    protected['sharedEffects'] = target['sharedEffects'] = ['external-effect']
                if kind == 'unresolved':
                    self.state['attempts'] = [{'requestId':'old', 'semanticDigest':'b'*64,
                        'attempt':'old', 'incarnation':'old', 'domain':copy.deepcopy(target),
                        'hostClosed':True, 'effectsDisposed':False, 'claimResolved':True}]
                else:
                    self.state['enrolled'] = [protected]
                self.classify(['1'], False, 'enrolled')


if __name__ == '__main__':
    unittest.main()
