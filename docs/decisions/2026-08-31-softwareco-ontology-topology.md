---
summary: "ADR selecting a true ontology submodule with targeted atomic materialization and parent-owned receipt relocation."
read_when:
  - "Implementing or reviewing Softwareco ontology materialization, receipts, or ownership-map migration."
type: "adr"
status: "accepted"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5251
---

# ADR — adopt a true Softwareco ontology submodule

## Decision

Accept RFC candidate **C** as selected by the current-track review and designated synthesis:

- `ontology` becomes a true Git submodule, represented by `.gitmodules` and a mode-`160000` entry;
- the initial accepted owner OID is
  `07d4b8b89f6ca436618adb42827885e9a45289c7`, subject to fresh live-publication verification at apply time;
- automation materializes exactly `ontology`, never every raw gitlink recursively;
- the six parent-owned ontology receipts move outside the submodule to
  `governance/ontology-dist/` and are regenerated under canonical Softwareco-parent identity;
- the established post-AK-5197 ownership map changes only through a new deterministic
  map/state plan and external receipt;
- the current 31 ontology worktree entries remain held evidence until exact post-ADR tasks apply
  the accepted transition.

Candidate E, the selective nine-path projection, remains a rollback alternative only. It is not an
active second topology.

## Authority and owner split

- `/home/tryinget/ai-society/softwareco/ontology` remains the sole authored Git and semantic source
  owner.
- Softwareco owns only the parent relation: `.gitmodules`, the exact gitlink OID, targeted
  materialization and gates, relocated parent receipts, and integration receipts.
- ROCS remains semantic/validation authority; parent receipts and Git metadata do not replace it.
- AK remains task, evidence, and Decision-144 lifecycle authority.
- Scratch candidates `016cf156…` and `aeea5616…` are evidence, not cherry-pick or apply authority.

## Mandatory controls

1. **True source binding.** `.gitmodules` and mode-`160000` `ontology` bind one full, live-published
   owner OID. Metadata-less gitlinks and copied source trees are forbidden.
2. **Targeted atomic materialization.** The materializer operates only on `ontology`, verifies the
   expected OID and allowed source before activation, and never invokes generic recursive
   submodule initialization while unrelated raw gitlinks remain unmapped.
3. **Fail-closed absence.** Missing, unavailable, mismatched, or interrupted source leaves no
   partial `.git`, changed parent index, activated wrong OID, or receipt mutation. Missing
   `../../ontology/manifest.yaml` is a hard gate failure, never a skip.
4. **Parent receipt identity.** All six current `ontology/dist/**` parent outputs are regenerated at
   `governance/ontology-dist/` with canonical parent identity. Every producer, consumer, artifact
   reference, and rollback path migrates before the old paths disappear.
5. **New ownership transition.** Narrowing `../../contracts/template-ownership.yml` requires a new
   post-AK-5197 manifest, deterministic plan, applied state, external evidence, and final receipt.
   Inline map-hash edits are forbidden.
6. **Physical membrane.** Ordinary ontology-owner CI cannot mutate relocated parent outputs.
   Parent tooling cannot overwrite owner source bytes except through Git submodule operations bound
   to the accepted OID.
7. **Truthful gates.** Fresh checkout and strict root, owner, infra, owned, contrib, and fork gates
   exercise actual materialization. Template stubs are not materialization proof.
8. **Bounded rollback.** Verified pre/post bundles preserve parent and owner refs, remote binding,
   and stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`. Rollback is forward/revert history plus exact
   rematerialization, never ref rewriting or stash activation.
9. **Owner-decomposed rollout.** Materialization, receipt migration, ownership transition/adoption,
   and final independent proof are separate exact tasks. Existing ontology WIP is not an implicit
   apply plan.

## Why candidate C

C provides Git-native parent-to-owner OID binding, removes overlapping source indexes, and preserves
the canonical ROCS locator path. Scratch proof established targeted materialization, strict resolver
compatibility, owner CI, unavailable-source failure, and exact rollback feasibility.

Candidate E worked in scratch but retained overlapping indexes and required a second path-selection
API, ignore contract, excluded-drift checker, and custom nested-Git activation. Candidates A, B, and
D retain duplication, break canonical path contracts, or rely on weaker command-coverage membranes.

The earlier claim that owner CI changed downstream receipts is superseded by evidence `8040`:
owner-only CI left them byte-identical; later consumer validations each updated only their own pair.
No ROCS-core aggregate-writer change follows from that false attribution.

## Consequences

- Fresh parent checkouts require one explicit ontology-only materialization step before ROCS gates.
- Receipt paths and identity change; consumers must migrate atomically.
- Parent ownership classification and state gain a new receipted transition after AK 5197.
- Root CI must fail when ontology is unmaterialized instead of silently skipping validation.
- The root has no remote, so verified local bundles remain required after every adoption commit.

## Execution order

1. Land and prove targeted atomic materialization plus hard missing-manifest gates.
2. Regenerate and migrate all six parent receipts and consumers to `governance/ontology-dist/`.
3. Produce/review the new ownership-map/state transition plan.
4. Apply candidate C at a freshly verified owner OID, converting the parent tree to the true
   gitlink without staging unrelated WIP.
5. Run fresh-checkout, unavailable-source, strict owner/parent, rollback, and independent review.
6. Record AK evidence and close only the exact tasks whose outcomes passed.

## Non-authorizations

This ADR does not authorize an arbitrary ontology commit, owner stash mutation, issue-tracker
publication, root push, recursive submodule conversion, Healthco propagation, or reinterpretation of
passing validation as rollout completion.

## Rollback

Before canonical adoption, discard only isolated candidate state. After adoption, use an exact
rollback task to revert the bounded parent commits, restore the previous ordinary-tree and receipt
paths from verified parent history, and rematerialize the exact previous owner state. If C cannot
meet atomic materialization, a successor review may reconsider E; do not activate E by convenience.
