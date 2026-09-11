---
summary: "ADR selecting parent-owned Softwareco ontology, superseding Decision 144's independent-source requirement without authorizing publication or bypassing migration gates."
read_when:
  - "Implementing or reviewing parent-owned Softwareco ontology and dependent identity cutover."
type: "adr"
status: "accepted"
date: "2026-09-11"
decision_id: 157
governance_task_id: 5650
supersedes_decision_id: 144
---

# ADR — author Softwareco ontology in its parent repository

## Decision and supersession

Accept the ordinary tracked-directory architecture reviewed in Decision 157. After the admitted
migration, `softwareco/ontology/` is part of the Softwareco repository, not an independently authored
Git repository, submodule or synchronized projection. The parent commit binds the retained company
ontology. ROCS remains semantic validation authority; AK remains runtime, identity, task, decision
and evidence authority.

This explicitly supersedes Decision 144's independent Git-source, gitlink and ongoing targeted
ontology-materialization requirements. It does not rewrite that decision, invalidate its historical
proof, or restore overlapping indexes. Applicable source custody, generated-output isolation,
full-history provenance, no-ambient-mutation, evidence and bounded rollback controls remain.

The operator clarified that the old private ontology setting was uninformed and instructed local
consolidation. Privacy is therefore not a requirement to preserve a separate repository. This is
**not** permission to publish: no push, visibility change, credentials action, remote retirement or
private-history import into the public parent is authorized. Future publication needs separate
permission and exact-tree secret/disclosure checks.

Current canonical topology remains unchanged until the accepted migration prerequisites and exact
owner tasks pass. Accepted architecture is not a statement that migration is implemented.

## Why this architecture

One company-authored source, atomic parent integration and lower operator/agent coordination costs
outweigh the independent Git-revision axis under clarified intent. Logical ontology ownership does
not require a distinct repository. Existing consumers are real migration contracts; they are not,
by themselves, proof that separate release/access control is necessary.

The cost is explicit: consumers switch source repository identity, and unrelated parent revisions
can change revision-bound snapshots even when semantic bytes do not. Accept correct invalidation;
do not weaken strict provenance or build a new publishing/cache subsystem without measured need.
A genuinely indispensable independent access/release promise discovered during final census stops
execution and returns to design rather than being hidden behind a compatibility mechanism.

## Mandatory migration invariants

1. **Single source and exact content.** Transfer only the explicitly classified retained source/doc
   paths from a freshly bound old owner OID/tree. Retained semantic bytes/modes remain exact.
   Semantic edits require their separate owner workflow. The old repository becomes inert preserved
   history, not a live mirror, locator shim or second authoring root.
2. **Private historical preservation.** Verify restore-capable full-ref bundles and necessary
   configuration/reflog/ignored/untracked preservation. Do not delete nested Git metadata, rewrite
   refs, pop/drop stashes or import old private history into parent Git. No generic recursive
   submodule operation or mutation of unrelated gitlinks.
3. **Source-owned reverse transition.** Prove L0-owned narrow gitlink-to-files plan/apply/finalize,
   ancestor/mode/OID/payload/authority/scope checks, negative tests, history verification,
   interruption/retry and rollback. Prove generated-checker fresh/existing convergence and promote
   through L0-to-L1. No consumer-local workaround or inline map/state hash edits.
4. **Receipted new ownership.** Classify parent `ontology/**` as company/agent-owned through a new
   exact predecessor-bound transition. Preserve historical Decision-144 state. Apply pending state,
   record external evidence, then finalize under the existing state-only commit contract.
5. **Complete consumer denominator.** Close and bind the census across actual registered owners,
   all locator variants, persisted Copier answers, source-owned generators, receipt readers/writers
   and independent consumers. Record exclusions and owner dispositions. The initial 30 physical/27
   tracked exact-old count is not completion coverage. Prove fresh generation and update convergence.
6. **Explicit source identity.** Select the parent locator/ref for each consumer, preserve strict
   checks and re-baseline source-bound snapshots/requests/receipts. No `.git` shim, alias, path
   redirection, loose-mode fallback or permanent synchronization pipeline. Do not broaden global
   template defaults for unrelated companies.
7. **AK lifecycle and rollback.** Before canonical cutover, bind and rehearse an AK-owner-approved
   reversible lifecycle operation, or keep irreversible retirement explicitly unperformed until
   rollback retention ends. Source identity and stale-path behavior must still be safe during that
   retention: no stale registration may silently authorize work against a different enclosing repo.
   Restoring `.git` is not AK recovery. No database edit, stale-state restoration, invented alias or
   silent re-registration. This is a mandatory supplement to companion-plan S2 and rollback, and
   must be repeated in every exact cutover execution contract.
8. **Coordinated cutover.** Prepare and prove parent/consumers in isolation; pause affected writers
   and bind the ordered cutover before canonical de-nesting. No intermediate inconsistent state is
   announced usable. Rehearse whole-wave rollback including AK identity, parent state and consumer
   locators; do not restore only the gitlink. No pre-publication against unavailable parent commits.
9. **Output custody and WIP.** Keep parent outputs at `governance/ontology-dist/` under canonical
   parent identity. Regenerate only plan-authorized outputs, never relabel old evidence. Freshly
   fingerprint and preserve unrelated WIP; use isolated writers. Do not run cleanup in the current
   dirty canonical receipt directory or silently overwrite it because it is generated.
10. **Fresh-checkout truth.** Prove ordinary source in a fresh full-history parent checkout with no
    ontology token, old remote or nested Git dependency. Missing, malformed or symlinked ontology
    still fails closed. Keep core dependency, semantic, supply-chain and historical-provenance gates.
    Actual affected owner gates and parent full/deep acceptance must pass at exact recorded identities.
11. **Separate local and hosted proof.** Local consolidation is not hosted CI repair. Task 5502 must
    remain explicitly reconciled until the owner-authorized replacement is published and a fresh
    hosted run passes. No remote effect or final hosted claim follows from this ADR.

## Execution order and controlling documents

The reviewed companion plan is
`../project/2026-09-11-softwareco-ontology-consolidation-plan.md` at commit
`09aa3d78d28e912701e0f566c95bd1025b7d2ec2`, SHA-256
`a09cd0f1b95b039abb2e1f5d547d68d69e462655b57493d123ba1218f8ead853`.
It supplies implementation and validation/rollout/rollback detail. Invariant 7 explicitly strengthens
its AK rollback contract as required by independent review; exact execution artifacts must carry it.

Order: complete preservation/census; prove L0 reverse transition and AK lifecycle capability; prepare
source-owned generator and per-owner consumers; prove isolated parent transition; make the admitted
coordinated canonical cutover; independently verify and record evidence. Each owner requires its own
exact task. Task 5650 is documentation/review only and cannot perform these implementation actions.

## Review lineage and claim boundary

Exact RFC commit `09aa3d78d28e912701e0f566c95bd1025b7d2ec2`, SHA-256
`5af2963903f7f242b6a49dd58248b5a8e40dd40f0240480502e366120d295559`;
current-track attempt 630 from `dispatch-1789114941099`; designated synthesis
`dispatch-1789115131353`, attached as AK review-synthesis artifact 1423, `ready_for_adr`.

Both reviews are documentary architecture assessments. They do not prove reverse-transition code,
AK lifecycle support, final consumer census, canonical WIP safety, restore, migration or hosted CI.
Any failed prerequisite stays a hard stop or an explicit owner-bound deferral, not a waived gate.
