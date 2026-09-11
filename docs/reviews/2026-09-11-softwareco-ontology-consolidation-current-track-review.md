---
summary: "Independent current-track architecture review finds Decision 157 ready for ADR with explicit owner, cutover and rollback prerequisites."
read_when:
  - "Synthesizing Decision 157 or writing its accepted ADR."
type: "review-memo"
status: "ready_for_adr"
date: "2026-09-11"
decision_id: 157
governance_task_id: 5650
review_track: "current_track"
review_outcome: "ready_for_adr"
reviewer_dispatch_id: "dispatch-1789114941099"
---

# Decision 157 current-track review

Outcome: **ready_for_adr**, architecture only. This records independent read-only review
`dispatch-1789114941099`, not implementation approval or legal AK closure.

## Exact reviewed inputs

- RFC: `../project/2026-09-11-softwareco-ontology-consolidation-rfc.md`.
- Plan: `../project/2026-09-11-softwareco-ontology-consolidation-plan.md`.
- RFC/plan commit: `09aa3d78d28e912701e0f566c95bd1025b7d2ec2`.
- RFC blob: `01df8bd869e14065a12184fb33c1a749ab5d0ce4`.
- RFC SHA-256: `5af2963903f7f242b6a49dd58248b5a8e40dd40f0240480502e366120d295559`.
- Plan SHA-256: `a09cd0f1b95b039abb2e1f5d547d68d69e462655b57493d123ba1218f8ead853`.
- Review-set plan: `../project/2026-09-11-softwareco-ontology-consolidation-review-set-plan.md`;
  commit `c79a86d94fd66774ea33e6bf747cbf63881ddc3f`, SHA-256
  `320a882a4a6198be57cd99fc7a8918c265d8656ce2687ae859592d1b6817e352`.

The reviewer verified the packet's committed identities by read-only local object inspection.
Prior Decision-144 ADR was also read, but its committed-byte identity was not independently verified
by that reviewer; no execution/source/registry behavior was tested.

## Conclusion and ranked findings

The independent-source requirement can coherently be superseded under the operator's clarified
intent. Git authoring ownership is distinct from ROCS semantic and AK runtime authority. No remaining
architectural choice requires RFC revision. Missing capabilities are execution blockers only if the
ADR carries the following obligations without dilution.

### R1 — reverse transition is an owner prerequisite

High consequence. Existing tree-to-gitlink support does not establish reverse support. Require
L0-owned plan/apply/finalize, narrow ancestor-delta admission, negative tests, history verification,
interruption/retry and rollback, then generated-checker fresh/existing convergence. A consumer-local
patch or inline ownership hash repair is not acceptable.

### R2 — AK lifecycle rollback must be explicit

High consequence. Filesystem and consumer rollback do not automatically restore AK registration
semantics. Before canonical cutover, bind and rehearse an AK-owner-approved reversible lifecycle
operation, or keep irreversible retirement explicitly unperformed until rollback retention ends.
Do not infer recovery from restoring `.git`, rewrite the database, or invent a compatibility alias.
This strengthens the plan's existing owner-supported identity prerequisite and must appear in the
ADR and subsequent exact execution contract.

### R3 — close the consumer denominator

High consequence. The 30/27 census is provisional and exact-old locators are not the complete scope.
Include prefixed/legacy/path variants, already-parent consumers, persisted Copier inputs,
generators, receipt readers/writers and external contracts. Owner-disposed exclusions remain in the
denominator. Test fresh generation and reruns. A genuinely necessary independent access/release
promise returns to design; do not conceal it behind loose resolution or a mirror.

### R4 — preservation and dirty receipts

High consequence. Canonical root gates can overwrite unrelated receipt WIP. Require isolated writer
execution, fresh fingerprints, explicit integration disposition, verified private restore archives,
and exact source import/exclusion classification. Never import historical private refs, stashes or
Git configuration into parent history as the preservation method. Dated WIP observations need fresh
execution-time readback.

### R5 — accept revision coupling honestly

Medium consequence. Parent revision changes can affect snapshots, caches, evidence and bound requests
without semantic byte changes. Bind exact candidate revision and receipt-generation sequence; prove
expected invalidation without weakening strict provenance. Performance optimization is optional and
not justification for an unneeded distribution subsystem.

## Required ADR invariants

1. Explicit successor to Decision144's independent-source/gitlink/materialization rules; preserve
   historical evidence and applicable custody, semantic, full-history and rollback controls.
2. Parent authorship; ROCS semantic authority and AK runtime/identity authority unchanged.
3. Exact retained semantic bytes/modes; excluded standalone machinery archived inertly.
4. No canonical de-nesting until R1–R4 and coordinated parent/consumer rollback gates are proved.
5. No old-locator shim, dual authoring, template spillover or hidden source fallback.
6. Missing/malformed/symlink source still fails closed; core dependency and full-history checks stay.
7. No push, visibility change, credentials operation, remote retirement or hosted-success claim.

## Evidence limit and next legal move

This is documentary architecture review, not executed migration verification. The reviewer did not
independently validate source behavior, live registrations, census completeness, current dirty state
or restore capability. Attach the committed review, obtain designated synthesis on the same bytes,
then record an ADR and exact owner-scoped prerequisite tasks. No canonical topology changes follow
from this memo alone.
