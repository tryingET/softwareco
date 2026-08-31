---
summary: "Validation, rollout, stop, and rollback contract for Decision 144 candidate C."
read_when:
  - "Validating or rolling back the Softwareco ontology submodule adoption."
type: "plan"
status: "accepted"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5251
---

# Candidate C validation, rollout, and rollback

## Preflight invariants

Every implementation task must re-read and record:

- accepted Decision 144, ADR, current implementation/validation artifacts, and exact task scope;
- parent HEAD/index/worktree and unrelated WIP fingerprints;
- ontology owner full OID/tree, clean state, refs, live authorized publication, and remote config;
- stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` and every newer stash OID;
- current consumer and receipt path census;
- current ownership map/state hash and AK-5197 ancestry;
- verified full-ref parent/owner bundles.

Any drift changes the plan input. Stop; do not force, reset, clean, stash, or mechanically retry.

## Materializer matrix

| Case | Required result |
|---|---|
| Fresh checkout, ontology uninitialized | Root gate fails before ROCS; no silent skip |
| Exact approved source/OID available | Targeted ontology-only activation succeeds |
| Generic recursive submodule command | Not invoked; tests prove it is unnecessary |
| Wrong source or OID | Fail before activation |
| Source unavailable | Fail with no `ontology/.git`, index, or receipt residue |
| Interrupted preparation | Complete rollback of temporary metadata |
| Existing partial metadata | Reject or restore deterministically before activation |
| Idempotent exact rerun | No byte/index/ref change |
| Materialized owner status | Clean at exact expected OID |

Tests must inspect filesystem and Git metadata, not only command exit text.

## Receipt migration matrix

- Generate all six outputs under canonical parent identity at `governance/ontology-dist/`.
- Hash and inspect repo/path/source/command bindings.
- Prove owner-only strict CI leaves all six parent outputs unchanged.
- Run contrib, fork, and infra consumer validation separately; each may update only its own declared
  receipt pair.
- Search source, docs, CI, fixtures, manifests, and generated contracts for stale
  `ontology/dist/` parent-receipt consumers.
- Fail if an old-path consumer, scratch/owner identity, or generation-inside-submodule path remains.
- Preserve the correction recorded by evidence `8040`; do not reintroduce the falsified
  cross-owner-writer claim.

## Ownership transition checks

The reviewed plan must prove:

- old and new ownership-map hashes;
- exact parent before commit and owner OID/tree;
- `.gitmodules` bytes and mode-`160000` index entry;
- complete classification of additions/removals/replacements;
- no `.git/**`, stash, ignored owner output, local ref, or unclassified path in the parent plan;
- parent receipts are outside the gitlink;
- pending state binds plan/map/Decision/ADR/materializer/gates;
- external AK evidence binds apply commit and validation;
- final state changes no pending binding except receipt/finalization fields.

A map/state mismatch must fail. Never repair by editing hashes inline.

## Required gates

Run from governed clean overlays with the protected ontology-kernel revision required by current
policy.

### Ontology owner

```bash
./scripts/ci/full.sh
```

Confirm owner status remains clean and relocated parent receipts are unchanged.

### Parent and consumers

```bash
./scripts/preflight-repo-census.sh
./scripts/ci/smoke.sh
./scripts/check-template-ci.sh
./scripts/ci/full.sh --deep
git diff --check
```

Also run strict ROCS validation for `infra`, `owned`, `contrib`, and `fork`. Generated validation
outputs must remain in scratch or be exact plan-classified receipt updates.

### Fresh-checkout proof

A new checkout must:

1. fail before ontology materialization;
2. materialize only `ontology` at the exact OID;
3. pass all strict gates;
4. survive unavailable-source and rollback probes without partial metadata;
5. require no ambient pre-existing `ontology/.git` state.

## Staging and integration gates

- Stage exactly the active task/plan path set.
- Forbid `infra/issue-tracker` and every unrelated owner WIP path.
- Compare parent status and untracked tar fingerprints before/after.
- Verify owner HEAD/status/refs/stashes and remote binding before/after.
- Preserve exact AK-5197 apply/finalization ancestry.
- Commit one bounded phase at a time and create verified full-ref bundles.
- Integrate only by reviewed fast-forward/ordered commits; never squash/cherry-pick scratch evidence.

## Stop conditions

Stop before mutation or publication on:

- absent/non-current Decision/ADR/task authority;
- source OID or live publication drift;
- dirty owner or ambiguous remote;
- consumer/receipt census drift;
- non-atomic materializer behavior;
- missing-manifest skip;
- generic recursive submodule use;
- stale/scratch/owner receipt identity;
- ownership plan/state/hash mismatch;
- unexpected staged path or unrelated WIP change;
- failed owner, consumer, parent, unavailable-source, or rollback gate;
- missing bundle/evidence reachability.

## Rollback

### Before a canonical adoption commit

Discard only owned scratch/candidate worktrees and unsigned plans. Remove temporary materialization
state created by the task after proving it is task-owned. Canonical parent/owner bytes remain
untouched.

### After a phase commit, before full adoption

Use a new exact rollback task and revert only that phase's commit. Restore prior receipt consumers,
materializer/gate behavior, or ownership state from committed parent history; rerun the complete
phase gate.

### After candidate C adoption

Use ordered forward/revert commits to:

1. restore the previous ownership map/state through its rollback contract;
2. remove the gitlink/`.gitmodules` relation and restore the prior ordinary parent ontology tree;
3. restore the six old parent receipt paths and consumers;
4. verify/rematerialize the exact previous owner state;
5. rerun owner/consumer/parent gates and create new bundles/evidence.

Never rewrite parent or owner refs, force a remote, pop/drop owner stashes, or restore AK from stale
files. If rollback changes the selected architecture, open a successor decision; E does not activate
automatically.

## Success boundary

Success means candidate C is commit-bound, materially fresh-checkout-safe, externally receipted,
and leaves both parent and owner truthfully clean. It does not mean root push, issue publication,
Healthco propagation, or workspace-wide submodule adoption.
