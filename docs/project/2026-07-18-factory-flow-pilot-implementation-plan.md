---
summary: "Post-ADR implementation plan for Factory Flow pilot 001 and safe fcos-proving-lane retirement."
read_when:
  - "Executing or reviewing Decision 62 after ADR acceptance."
type: "implementation-plan"
status: "accepted_post_adr_plan"
date: "2026-07-18"
decision_id: 62
---

# Factory Flow pilot 001 — implementation plan

## Authority

- ADR: `docs/decisions/2026-07-18-software-factory-flow-protocol-pilot.md`
- Decision: AK `#62`, `adr_recorded / accepted`
- pilot: `SOFTWARECO-FACTORY-PILOT-001`
- human authority: current higher-level human operator
- technical steward: Softwareco CTO Agent under the ADR's bounded delegation

This plan authorizes no physical repository deletion and no FCOS product mutation.

## Outcome

Preserve every recoverable proving-lane byte and lineage fact, classify and route all current work, prove restoration, make the repository unambiguously historical/non-product in active owner projections, and produce an independent operator outcome plus human terminal decision.

## Execution structure

### Strategic frame

Create after this plan and its validation companion are tracked:

- key: `SF1`
- title: `Operate the first Softwareco Factory Flow pilot`
- state: `active`
- boundary: pilot 001 only

### Implementation wave

Create only if useful:

- key: `IW-SF1-PILOT-001`
- title: `Safely retire fcos-proving-lane as historical evidence`
- parent: `SF1`

### Task split

1. **Softwareco coordination task** — close Decision 62 preparation, maintain packet/direction/evidence, and coordinate owner projections.
2. **Source-owner preservation task** in `fcos-proving-lane` — read-only capture, classification artifacts, restoration rehearsal, and non-destructive historical-status changes allowed by exact scope.
3. Add separate owner tasks only when a projection or misplaced artifact belongs elsewhere.
4. Create an FCOS item only if more than one source owner needs a shared active gate.

## Preservation location

Primary local archive:

```text
/home/tryinget/ai-society/archive/20260718-softwareco-factory-pilot-001/
```

The archive is evidence storage, not a new active repository or authority surface. AK records hashes and receipts. Secrets/private data, if found, are quarantined with restrictive permissions and never copied into Git.

## Phases and gates

### Phase 0 — refresh and admission

- refresh packet revisions, Decision 62 passport, proving-lane HEAD/status hash, and FCOS owner revision;
- verify the operator packet is current;
- create direction/wave and exact source-owner task;
- record WIP admission and deferred task `#3455`;
- stop on any owner or scope conflict.

### Phase 1 — lossless capture

Without changing proving-lane bytes:

- record filesystem/repo identity;
- capture all refs, tags, branches, stashes, worktrees, nested repos/submodules, reachable/unreachable objects, index/worktree status, tracked binary-safe diff, untracked and ignored files, symlink/mode/size metadata;
- create a Git bundle or equivalent verified object archive plus worktree payload;
- calculate SHA-256 for manifests, patches, bundle, and every untracked/ignored artifact;
- run secret-sensitive classification before any Git publication.

Gate: every discovered path/object class has a manifest entry and owner/security disposition.

### Phase 2 — classify and route

Classify each changed/untracked artifact as:

- historical FCOS canary/scorecard evidence;
- generic template/ROCS migration;
- misplaced workstation/task evidence;
- active dependency requiring redirect;
- duplicate/generated/disposable material, with proof;
- secret/private/quarantined material.

Do not move or delete merely from classification. Create source-owner handoffs/tasks when needed.

Gate: unclassified count is zero and no owner dispute remains.

### Phase 3 — restoration rehearsal

- restore archive into a disposable path outside the source repo;
- compare refs, objects, tracked bytes, untracked/ignored bytes, modes, symlinks, and status representation;
- run bounded docs/ROCS checks only after byte restoration is proven;
- retain command transcript and comparison receipt.

Gate: restoration is byte/metadata equivalent for all retained material. Failure forces `stop` or explicit `continue`.

### Phase 4 — historical-status transition

Only after Phase 3:

- update proving-lane owner docs to state historical/retired/non-product status;
- close or supersede generic active work through AK without deleting history;
- update Softwareco capability/fleet projections through their owner surfaces so they no longer imply an active FCOS product;
- retain direct links to preserved evidence and the native FCOS product owner;
- do not delete the repository.

Gate: deterministic owner checks pass and no current dependency is broken.

### Phase 5 — outcome and learning

- run the independent ten-minute cold-start test;
- record protocol overhead, blocked age, unclassified-path trend, recovery results, and authority-drift incidents;
- produce protocol-conformance and effectiveness verdicts separately;
- crystallize mandatory KES learning;
- request human `continue`, `stop`, `redirect`, or `complete` decision.

## Stop conditions

- secret/private material without safe handling;
- path/object not represented in the manifest;
- repository identity or status drift during capture;
- restoration mismatch;
- owner dispute;
- proposed physical deletion;
- FCOS product mutation without FCOS owner authorization;
- four-hour agent budget exhausted without explicit continuation;
- human revocation.

## Completion definition

This plan completes only when the human terminal decision is recorded. `complete` requires both protocol conformance and effectiveness `improved`; documentary completion alone is insufficient.
