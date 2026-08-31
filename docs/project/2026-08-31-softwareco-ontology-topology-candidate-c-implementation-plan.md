---
summary: "Owner-decomposed implementation plan for Decision 144 candidate C."
read_when:
  - "Planning the ontology submodule, targeted materializer, receipt migration, or ownership-state transition."
type: "plan"
status: "accepted"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5251
---

# Candidate C implementation plan

## Outcome boundary

Implement the accepted Decision-144 topology without treating the current 31 ontology worktree
entries or scratch commit `016cf156…` as authority. Each phase starts from fresh Git/AK/remote
readback and stops on drift.

## Phase 0 — admission and preservation

Before every mutation phase:

- read the live Decision-144 passport and exact task scope;
- verify the Softwareco parent commit/index/worktree and unrelated WIP fingerprints;
- verify ontology owner HEAD, clean index/worktree, branches, remotes, live publication containment,
  and stash OIDs;
- reproduce or explain drift from the commit-bound `22/46/16/30/1/6` census;
- create and verify full-ref parent and owner bundles;
- verify the selected owner OID is a full 40-hex commit on an authorized live ref;
- stop if any source, consumer, receipt, or ownership-map input differs from the reviewed plan.

## Phase 1 — targeted materializer and hard gates

Create one parent-owned materialization surface that:

1. accepts only repository root, expected ontology OID, and approved source metadata;
2. prepares Git metadata/object acquisition in owned temporary state;
3. verifies source, commit, tree, and expected OID before activation;
4. activates only the `ontology` submodule atomically;
5. removes all temporary/partial metadata on failure;
6. reports stable machine-readable outcomes;
7. never initializes `contrib-guide`, `infra/issue-tracker`, `softwareco-agents`, or another raw
   gitlink.

Update local and CI entrypoints so missing `../../ontology/manifest.yaml` fails before ROCS. Test:

- uninitialized checkout;
- exact local/bundle materialization;
- authorized live source materialization;
- wrong OID, wrong source, unavailable source, interruption, and pre-existing partial metadata;
- idempotent rerun and exact rollback.

No Phase-1 task stages source-owner files or changes the parent ontology entry.

## Phase 2 — parent receipt migration

Move the six parent-owned outputs from `ontology/dist/` to `governance/ontology-dist/`:

- `.authority-receipt.lock`;
- `authority-receipt.json`;
- `authority-receipt.validate.json`;
- `id_index.json`;
- `resolve.json`;
- `summary.json`.

Do not copy old bytes as authority. Regenerate each output under canonical Softwareco-parent identity
in an isolated strict overlay. Migrate every producer, consumer, artifact reference, docs path,
fixture, and rollback check before deleting old paths. Prove:

- owner CI leaves the relocated outputs byte-identical;
- each consumer validation updates only its own declared receipts;
- no old receipt path remains an active consumer;
- parent identity/repo/path bindings are current;
- failure cannot first generate inside the source-owner submodule path.

## Phase 3 — ownership-map/state transition plan

Define a schema-versioned transition that binds:

- accepted Decision 144 and ADR;
- parent before commit and exact owner OID/tree;
- `.gitmodules` bytes and mode-`160000` target;
- old/new ownership-map hashes and complete path classification;
- receipt relocation paths and identities;
- deterministic additions, replacements, removals, modes, and unchanged paths;
- materializer/gate versions and required validation;
- unrelated WIP fingerprints;
- executor, rollback, and external AK evidence.

The ownership map must cease claiming all `ontology/**` as parent template-owned. It must classify
the gitlink relation, parent-owned metadata/materializer/receipts, and forbidden ambient owner bytes
without becoming semantic authority. Apply writes a pending state; external evidence finalizes it.
Directly editing the established AK-5197 state/map hash is forbidden.

## Phase 4 — exact candidate C adoption

In a clean isolated candidate context:

1. verify Phases 1–3 and exact current inputs;
2. relocate/regenerate parent receipts;
3. remove the ordinary parent ontology subtree under the reviewed plan;
4. add `.gitmodules` and mode-`160000` `ontology` at the exact owner OID;
5. apply the new ownership transition pending state;
6. targeted-materialize `ontology` and run owner/consumer/parent gates;
7. obtain independent review and external evidence;
8. finalize the ownership transition and commit only plan-scoped paths;
9. integrate by fast-forward only after unrelated canonical WIP rechecks.

The existing 31 ontology WIP entries may inform byte/OID comparison but are never staged one by one
or copied into parent history.

## Phase 5 — final proof and handback

Prove from a fresh checkout:

- uninitialized root gate fails;
- targeted materialization succeeds at the exact OID;
- generic recursive initialization is neither required nor invoked;
- strict root, ontology owner, infra, owned, contrib, and fork gates pass;
- relocated receipts have correct parent identity;
- unavailable source and bounded rollback leave no partial metadata;
- parent and owner status/ref/stash truth is clean and current;
- bundles and AK evidence resolve to committed artifacts.

Record limitations honestly. Do not claim root publication, Healthco rollout, or workspace-wide
submodule convergence.

## Task boundaries

The fanout artifact defines four ordered implementation tasks. No task may absorb another owner's
surface or stage unrelated issue-tracker/owner WIP. Passing one phase authorizes only its declared
next gate, not terminal completion of a later phase.
