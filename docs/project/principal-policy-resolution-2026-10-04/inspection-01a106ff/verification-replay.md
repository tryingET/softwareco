---
summary: "Read-only inspection replay: exact retained R3 diagnostics and two nonblocking construction-check blind spots, with separate supplemental guards."
read_when:
  - "Reproducing the fresh inspector's construction evidence without executing birth or owner admission."
type: "reference"
status: "inspection-diagnostic-not-runtime-implementation"
task_id: 6635
decision_id: 173
as_of: "2026-10-04"
---
# Fresh inspection diagnostic replay

The [retained checker](../construction-check-r3.md) passes its declared 44-case
construction scan and five negative probes. Its assertions are not an exhaustive
check of every oracle field. Two additional in-memory mutations demonstrate this:
G01 can claim a second winning contender while keeping its aggregate start count
one; G10 can remove the composite creator/other-guards assertion while keeping the
original recovery-specific guards true. The retained main checker accepts both.
The actual unmodified fixtures assert the correct values; the policy contract is
not contradicted. This is nonblocking diagnostic coverage, not a policy must-fix.

The supplemental guards below reject those two malformed copies. They neither fix
nor replace the frozen checker, and do not implement admission. Their positive
inputs and negative results are still synthetic. Only native V05 observations can
establish parent reservation, authentication, fencing, writes or recovery.

Run from `/home/tryinget/ai-society` using existing Python. It reads fixed files,
mutates copies in memory, and prints JSON; it writes nothing or invokes an owner API.

```sh
python3 - <<'PY'
from pathlib import Path
import contextlib
import copy
import hashlib
import io
import json
import re

root = Path('softwareco/docs/project/principal-policy-resolution-2026-10-04')
sha = lambda value: hashlib.sha256(value).hexdigest()
text = (root / 'construction-check-r3.md').read_text()
assert sha(text.encode()) == 'fa7acf8394fb19031e7bc3dbc4e4c9da84185341750e5c11368d991a729272fe'
blocks = re.findall(r'```sh\n(.*?)\n```', text, re.S)
assert len(blocks) == 2
hashes = ['284d3443ea9b6d836acdd9c741bb229a688c9226d6980d2f678a493b3e5d1766',
          'b7c32b617250b9f0c7fb09a9d03cd602887be8f4e12a2766d639465abab36f7a']
codes = []
retained = []
for block, expected in zip(blocks, hashes):
    assert sha(block.encode()) == expected
    assert block.startswith("python3 - <<'PY'\n") and block.endswith('\nPY')
    code = block.split('\n', 1)[1].rsplit('\nPY', 1)[0]
    codes.append(code)
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(compile(code, '<retained-read-only-diagnostic>', 'exec'), {})
    retained.append(json.loads(stream.getvalue()))

cases = {c['id']: c for c in json.loads((root / 'policy-fixtures-r3.json').read_text())['cases']}

def supplemental(case):
    parent, inputs, expected = case['parent'], case['input'], case['expected']
    if case['action'] == 'competing_new_starts':
        assert inputs['same_o3_right'] is True
        assert len(set(inputs['permits'])) >= 2
        assert expected['new_starts'] == 1
        assert expected['second_contender_starts'] == 0
        assert expected['reservation_key'] == parent['canonical_right']
    if expected['admission'] == 'admit_recovery_only':
        assert inputs['creator_authority_and_other_guards'] is True
        assert inputs['attempt'] == parent['original_attempt'] == expected['attempt_preserved']
        assert expected['new_starts'] == 0 and expected['new_right_issued'] is False

for case in cases.values():
    supplemental(case)
probes = [('second-winning-contender', 'G01', 'expected', 'second_contender_starts', 1),
          ('recovery-composite-guards-false', 'G10', 'input', 'creator_authority_and_other_guards', False)]
observations = []
anchor = "fixture = load('policy-fixtures-r3.json')"
assert codes[0].count(anchor) == 1
for name, ident, part, key, value in probes:
    malformed = copy.deepcopy(cases[ident])
    malformed[part][key] = value
    inject = ("\nfor c in fixture['cases']:\n"
              f"    if c['id'] == {ident!r}: c[{part!r}][{key!r}] = {value!r}")
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(compile(codes[0].replace(anchor, anchor + inject), '<in-memory-probe>', 'exec'), {})
    assert json.loads(stream.getvalue())['construction_check'] == 'passed'
    try:
        supplemental(malformed)
    except AssertionError:
        observations.append({'probe': name, 'retained_main_checker_accepts': True,
                             'supplemental_guard_rejects': True})
    else:
        raise AssertionError(('supplemental guard failed', name))
print(json.dumps({'retained': retained, 'supplemental_positive_cases': len(cases),
                  'observations': observations, 'runtime_implementation_exercised': False,
                  'owner_approval_proven': False}, sort_keys=True))
PY
```

Hash identity above excludes the newline after the fenced shell body. An initial
inspection harness appended that newline and rejected its own hash assertion before
diagnostic execution; exact extraction resolves the mismatch, not a source rewrite.
[Before-output checks](checks-before.json) retain that limitation and fresh results.
