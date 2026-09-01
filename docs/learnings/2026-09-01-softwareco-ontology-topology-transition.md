---
summary: "Decision 144 learning: separate physical source ownership from parent integration outputs, then change established ownership through receipted, history-bound transitions."
read_when:
  - "Designing a parent-to-owner repository topology or targeted submodule materialization."
  - "Relocating generated outputs across an ownership boundary."
  - "Changing an established L1 template ownership map after adoption."
type: "learning"
status: "candidate_local_learning"
date: "2026-09-01"
decision_id: 144
governance_task_id: 5287
---

# Learning — topology transitions need physical and historical ownership membranes

## Observed outcome

Decision `144` replaced Softwareco's overlapping parent/ontology source indexes with candidate C:
a true `ontology` submodule at owner commit
`07d4b8b89f6ca436618adb42827885e9a45289c7`, recorded by parent commit
`89824a68dec4f55f4d35512c8c430bca5e72b5fa`. Parent integration outputs moved to
`governance/ontology-dist/`. The established L1 ownership map changed through a receipted v2
transition rather than an inline hash edit.

The transition was deliberately decomposed:

1. task `5256` added targeted atomic materialization and hard missing-manifest gates;
2. task `5271` moved parent receipts and their producers/consumers;
3. task `5284` propagated strict v2 provenance checking with full-history CI;
4. task `5283` applied the gitlink and two-commit ownership transition;
5. task `5286` independently exercised fresh-checkout, failure, provenance, and rollback behavior.

This ordering made each owner boundary and stop condition independently testable.

## Reusable lessons

### 1. Separate the physical source owner from parent-owned outputs

A parent can own the relation to a source repository without owning that repository's authored
bytes. Here the parent owns `.gitmodules`, the exact mode-`160000` OID, the targeted materializer,
integration gates, and parent receipts. The ontology repository remains the sole Git and semantic
source owner; ROCS remains semantic validation authority; AK remains lifecycle and evidence
authority.

Generated parent outputs cannot live below a source-owner gitlink. Relocating them is not merely a
path rename: producers, readers, cleanup, receipt identity, failure behavior, and rollback references
must move together while preserving canonical parent identity.

### 2. Prefer a true OID relation plus targeted atomic materialization

The accepted topology uses Git's native parent-to-owner OID binding and initializes exactly
`ontology`. Generic recursive submodule initialization was unsafe because unrelated raw gitlinks
were not governed by the same module map.

A trustworthy materializer verifies the approved source and expected commit before activation,
changes no unrelated gitlink or parent index entry, and leaves no partial metadata when the source
is missing, unavailable, wrong, or interrupted. An uninitialized checkout must fail before semantic
validation; a missing manifest must never become a successful skip. Evidence `8090` and `8157`
covered the targeted 13-case matrix, fresh uninitialized failure, exact activation, idempotence, and
rollback/rematerialization.

### 3. Verification and execution must have one byte custody chain

A generated wrapper that verifies files and later imports them again by pathname leaves a
verify-to-execute race. ROCS `0.4.1` instead descriptor-captured regular singly linked files,
materialized verified bytes into sealed anonymous ZIP/native memfds, and executed from those sealed
descriptors without a consumer-path reopen. ROCS `0.4.2` provided the generic argument-forwarding
launcher while preserving the separate fixed CI profile. Evidence `8125` and `8138` support those
bounded implementation claims. Their focused suites passed; their full local suites retained the
known Node `26.8.1` versus pinned `26.1.0` environment-baseline failures, so they do not claim an
otherwise all-green full-suite run.

The general rule is:

```text
capture by no-follow descriptor
→ verify captured bytes
→ seal the executable representation
→ execute only from that representation
```

A digest check alone does not establish that the checked bytes are the bytes later executed.

### 4. External-output cleanup is an authority operation

Moving generated outputs outside the source owner makes cleanup cross a more visible boundary.
Cleanup must therefore use a marked output root, a closed artifact allowlist, pinned-directory and
private-inode checks, exact temporary-file grammar, and fail-closed handling of unknown, nested,
hardlinked, substituted, or concurrently inserted entries. Broad pathname deletion or receipt-name
matching is not sufficient. ROCS `0.4.2` supplied this bounded cleanup behavior before Softwareco
adopted external parent receipts.

### 5. Causal experiments must isolate command chronology

The first candidate experiment incorrectly blamed ontology-owner CI for six changed downstream
receipts. The status snapshot had been delayed until after three separate consumer validations.
A focused rerun captured state immediately after each command: owner CI left all six outputs
byte-identical, while each consumer changed only its own pair. Evidence `8040` supersedes the false
writer claim.

For cross-owner mutation claims, record before/after hashes and status at every command boundary.
Do not infer causality from the final dirty set of a multi-command experiment.

### 6. Established ownership maps require successor transitions

Once an L1 ownership map has an adoption receipt, changing its classification is a governance
transition, not ordinary configuration editing. The generic v2 protocol bound:

- predecessor commit and prior state/map digests;
- canonical transition plan digest and complete Git/map deltas;
- Decision, ADR commit, task, and executor;
- pending apply commit and required validation;
- external AK evidence;
- a state-only final commit.

Softwareco's plan digest was
`bd4ed944e633d548d67202a063135ad7048f93822a221847b9cfb3b211a7ff1f`; evidence `8156`
binds pending commit `1d71fd69cd67f92a4ecaf640ff29cff8f9dbd0b8`, and the final state commit is
`89824a68dec4f55f4d35512c8c430bca5e72b5fa`. L0 evidence `8151` covers the reusable transition
engine. This two-step form prevents a self-authored final state from serving as its own receipt.

### 7. Provenance checks need full history

The v2 checker proves parent/child relationships, exact deltas, and a unique state-only
finalization. Those are historical statements. A shallow checkout cannot prove them and must fail
closed; generated workflow lanes that invoke the checker must use full Git history. Evidence `8153`
records the L0 hardening; corrected Softwareco propagation evidence `8155` supersedes failed
earlier-candidate evidence `8152` and hash-incorrect evidence `8154`; and independent evidence
`8157` records both full-history success and
shallow-history rejection in Softwareco.

### 8. Preserve owner metadata as data, not as an assumed side effect

A topology change can preserve worktree bytes while still losing refs, remote bindings, or stashes.
The migration used verified full-ref bundles, before/after inventories, same-filesystem metadata
moves, and journaled interruption recovery. Rollback was rehearsed as ordered forward/revert history
plus exact rematerialization—not reset, ref rewriting, or stash activation. The preserved owner
state included both stashes, including `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`.

## Claim boundary

The independent closeout proof passed locally at the exact parent and owner commits (evidence
`8157`). The Softwareco root has no remote, so verified local bundles were the Git transport used
for this local adoption. The final verifier had no private GitHub token and used the verified complete
owner bundle/local narrow transport; it confirmed canonical `origin/main` readback but did not claim
a new authenticated publication readback.

These results prove the bounded Softwareco Decision-144 transition and reusable local mechanisms.
They do not prove root push or publication, Healthco rollout, workspace-wide submodule convergence,
or a universal template policy. Any broader adoption requires its own owner decision, exact task,
current source verification, and evidence.

## Evidence index

- Decision `144` and accepted-ADR continuation evidence `8066`;
- corrected causality: evidence `8040`;
- targeted materializer: task `5256`, evidence `8090`;
- sealed runtime and cleanup: evidence `8125` and `8138`;
- parent receipt migration: task `5271`, evidence `8146`;
- reusable ownership transition/checker: evidence `8151` and `8153`;
- corrected Softwareco checker propagation: task `5284`, evidence `8155` (superseding failed
  earlier-candidate evidence `8152` and hash-incorrect evidence `8154`);
- Softwareco ownership transition: task `5283`, evidence `8156`;
- independent fresh-checkout closeout: task `5286`, evidence `8157`.
