---
summary: "Exact reproducible read-only R3 fixture/mapping/digest construction checker; not a policy or birth-admission implementation."
read_when:
  - "Replaying the local construction checks without confusing them with real owner or runtime verification."
type: "reference"
status: "documentation-check-command-not-authority-enforcer"
task: "AK6635"
decision_id: 173
as_of: "2026-10-04"
---
# Reproducible R3 construction check

Run from `/home/tryinget/ai-society` using existing Python 3. The command reads only
this RFC directory's fixed Markdown/JSON inputs and prints a report. It writes
nothing, invokes no owner API, installs nothing and starts no agent session. It is
an inert retained **documentation diagnostic**, not production source implementation,
a permissions store, a birth adapter or a test of actual concurrency/fencing.

The fixture booleans are assumed synthetic inputs. Passing this checker means the
specified oracle obeys its own stated constraints; it does NOT prove that an actual
owner issued a grant, a right was consumed or any effect boundary denied a write.
Real proof remains V01–V09 under the admitted source owners.

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib
import json
import re

root = Path('softwareco/docs/project/principal-policy-resolution-2026-10-04')

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, ('duplicate JSON key', key)
        result[key] = value
    return result

def no_nonfinite(value):
    raise AssertionError(('non-finite JSON value', value))

def load(name):
    return json.loads((root / name).read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object, parse_constant=no_nonfinite)

base_bytes = (root / 'policy-fixtures-r2.json').read_bytes()
base = load('policy-fixtures-r2.json')
fixture = load('policy-fixtures-r3.json')
assert fixture['baseline_file'] == 'policy-fixtures-r2.json'
assert hashlib.sha256(base_bytes).hexdigest() == fixture['baseline_sha256']
assert fixture['authority_effect'] == 'none'
assert fixture['data_class'] == 'entirely-synthetic'
assert base['clause_checks'] == {f'P{i:02}': f'V{i:02}' for i in range(1, 10)}
assert len(base['cases']) == 28
assert {c['check'] for c in base['cases']} == set(base['clause_checks'].values())

edges = {}
for row in base['birth_transitions']:
    key = (row['from'], row['event'])
    assert key not in edges
    assert row['from'] in base['birth_states'] and row['to'] in base['birth_states']
    edges[key] = row
for forbidden in base['forbidden_birth_pairs']:
    assert not any([r['from'], r['to']] == forbidden for r in edges.values())
for case in base['cases']:
    if 'before' not in case:
        continue
    row = edges[(case['before'], case['event'])]
    guards = all(case['input'].get(g) is True for g in row['guards'])
    if case['expected'].get('transition_admitted') is False:
        assert not guards and case['after'] == case['before']
    else:
        assert guards and case['after'] == row['to']
        assert case['expected']['new_start_admissions'] == row['new_start_admissions']

birth_cases = {c['id'] for c in base['cases'] if c['check'] == 'V05'}
assert set(fixture['baseline_parent_extensions']) == birth_cases
for ext in fixture['baseline_parent_extensions'].values():
    consumption = ext.get('consumption', ext.get('consumption_before'))
    assert consumption in fixture['parent_consumption_values']
    assert ext['admission'] in fixture['parent_admission_values']
    assert ext['canonical_right']

assert len(fixture['cases']) == 16
all_ids = [c['id'] for c in base['cases'] + fixture['cases']]
assert len(all_ids) == len(set(all_ids)) == 44
for case in fixture['cases']:
    p, i, e = case['parent'], case['input'], case['expected']
    assert p['consumption'] in fixture['parent_consumption_values']
    assert p['admission'] in fixture['parent_admission_values']
    assert p['canonical_right'] and p['o3_act']
    assert type(e['new_starts']) is int and e['new_starts'] in (0, 1)
    if i.get('creator_current_authority') is False:
        assert e['new_starts'] == 0
    if 'intended_subject_actor_association' in i:
        assert e['creator_authority_binding_separate_from_subject'] is True
        assert e['different_actor_required'] is False
        assert e['principal_appointment_inferred'] is False
        assert e['principal_activation_inferred'] is False
    if p['consumption'] == 'spent':
        assert e['parent_consumption_after'] == 'spent'
    if p['consumption'] == 'unknown':
        assert e['parent_consumption_after'] == 'unknown'
        assert e['new_starts'] == 0
        assert e.get('nonexecution_inferred') is False
    if e['new_starts'] == 1:
        assert i['creator_authority_and_other_guards'] is True
        assert i['qualified_atomic_parent_reservation'] is True
        if case['action'] == 'replacement_start':
            assert i['fresh_o3_act'] is True
            assert i['new_o3_act'] != p['o3_act']
            assert i['new_canonical_right'] != p['canonical_right']
            assert i['o3_links_old_right_and_attempt'] is True
            assert i['old_attempt_disposition_established'] is True
            assert i['new_right_unused_and_open'] is True
            assert e['reservation_key'] == i['new_canonical_right']
            assert e['new_right_consumption_after'] == 'spent'
        else:
            assert p['consumption'] == 'unused' and p['admission'] == 'open'
            assert e['reservation_key'] == p['canonical_right']
    if i.get('same_o3_right') and (p['consumption'] != 'unused' or p['admission'] != 'open'):
        assert e['new_starts'] == 0
    if e.get('new_right_issued') is True:
        assert i['fresh_o3_act'] is True
        assert i['new_o3_act'] != p['o3_act']
        assert i['new_canonical_right'] != p['canonical_right']
        assert i['o3_links_old_right_and_attempt'] is True
    if e['admission'] == 'admit_recovery_only':
        assert case['action'] == 'same_attempt_recovery' and e['new_starts'] == 0
        assert i['attempt'] == p['original_attempt'] == e['attempt_preserved']
        for guard in ('confirmed_original_parent_start', 'original_permit_correlation',
                      'fresh_recovery_authority', 'old_executor_fenced',
                      'unchanged_inputs_and_subject', 'remaining_step_proved'):
            assert i[guard] is True
        assert e['new_right_issued'] is False

main = (root / 'resolution-rfc-r3.md').read_text(encoding='utf-8')
contract = (root / 'contracts-r3.md').read_text(encoding='utf-8')
answers = (root / 'reviewer-answers-r3.md').read_text(encoding='utf-8')
assert re.findall(r'^### (P\d\d) —', main, re.M) == [f'P{i:02}' for i in range(1, 10)]
for n in range(1, 10):
    assert f'P{n:02} / V{n:02}' in contract
for n in range(1, 8):
    assert f'| O{n} |' in contract
for n in range(1, 5):
    assert f'### Q{n}.' in answers
plan = (root / 'review-set-plan-r3.md').read_text(encoding='utf-8')
for field, name in [('reviewed_artifact_sha256', 'resolution-rfc-r3.md'),
                    ('contract_appendix_sha256', 'contracts-r3.md')]:
    declared = re.search(r'^' + field + r': "([a-f0-9]{64})"$', plan, re.M).group(1)
    assert declared == hashlib.sha256((root / name).read_bytes()).hexdigest()
for name in ('resolution-rfc-r3.md', 'contracts-r3.md', 'reviewer-answers-r3.md',
             'evidence-r3.md', 'review-findings-r2.md', 'review-set-plan-r3.md',
             'construction-check-r3.md'):
    text = (root / name).read_text(encoding='utf-8')
    assert len(text.splitlines()) <= 800 and len(text.encode('utf-8')) <= 60000
    assert text.endswith('\n') and not text.endswith('\n\n')
    assert all(line.rstrip() == line for line in text.splitlines()), name
print(json.dumps({'construction_check': 'passed', 'baseline_cases': 28,
                  'new_cases': 16, 'total_cases': 44, 'clause_checks': 9,
                  'owner_slots': 7, 'reviewer_answers': 4,
                  'runtime_implementation_exercised': False,
                  'owner_approval_proven': False}, sort_keys=True))
PY
```

Reference/metadata/source checks remain separate canonical owner commands. This
checker does not incorporate native AK state into a pretend permission oracle.
To replay byte custody afterward, run the output/source manifest checks from the
workspace root. Native Decision 173 readiness/owner acts must still be read directly.

### Negative construction probes (not native admission tests)

The following read-only probes use the same parent/creator/fresh-O3/original-attempt
assertions to ensure malformed oracles are rejected. They mutate copies in memory,
not fixtures on disk, and exercise no owner or runtime. A rejection proves only
that the corresponding construction guard detects that deliberate inconsistency.

```sh
python3 - <<'PY'
from pathlib import Path
import copy
import json

path = Path('softwareco/docs/project/principal-policy-resolution-2026-10-04/policy-fixtures-r3.json')
cases = {c['id']: c for c in json.loads(path.read_text(encoding='utf-8'))['cases']}

def check(c):
    p, i, e = c['parent'], c['input'], c['expected']
    if i.get('creator_current_authority') is False:
        assert e['new_starts'] == 0
    if p['consumption'] == 'unknown':
        assert e['parent_consumption_after'] == 'unknown'
        assert e.get('nonexecution_inferred') is False
    if e['new_starts'] == 1 and c['action'] != 'replacement_start':
        assert p['consumption'] == 'unused' and p['admission'] == 'open'
    if e.get('new_right_issued') is True:
        assert i['fresh_o3_act'] is True
        assert i['new_o3_act'] != p['o3_act']
        assert i['new_canonical_right'] != p['canonical_right']
    if e['admission'] == 'admit_recovery_only':
        assert i['attempt'] == p['original_attempt'] == e['attempt_preserved']

probes = [
    ('spent-parent-start', 'G02', 'expected', 'new_starts', 1),
    ('unknown-as-nonexecution', 'G09', 'expected', 'nonexecution_inferred', True),
    ('o6-mints-right', 'G05', 'expected', 'new_right_issued', True),
    ('new-attempt-labelled-recovery', 'G10', 'input', 'attempt', 'fixture:T2'),
    ('creator-false-hidden-by-composite', 'G12', 'input', 'creator_current_authority', False),
]
for name, ident, part, key, value in probes:
    c = copy.deepcopy(cases[ident])
    check(c)
    c[part][key] = value
    try:
        check(c)
    except AssertionError:
        continue
    raise AssertionError(('probe failed to reject inconsistent oracle', name))
print(json.dumps({'construction_probes_rejected': len(probes),
                  'runtime_implementation_exercised': False}, sort_keys=True))
PY
```
