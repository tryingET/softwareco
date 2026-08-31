---
summary: "Review-set plan binding Decision 144 to the exact RFC, candidate experiments, corrected causality, and current-track outcome."
read_when:
  - "Reviewing Decision 144 or checking the integrity of its current-track review."
type: "review-plan"
status: "complete"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5244
review_track: "current_track"
---

# Decision 144 review-set plan

## Reviewed artifact

- Decision: AK `144`
- RFC: `2026-08-31-softwareco-ontology-topology-rfc.md`
- RFC commit: `d71750ab1b13f169f352f6b47fff916c7e28dd0f`
- RFC blob: `06004e55467d61bf098933eebb537c59399a5558`
- RFC SHA-256: `98c79db2df614dae35aa64781717639c4373cc608328949c5c811cc0f9290c01`
- Review profile: architecture, `strict_convergence`, `multi_lane_requires_synthesis`
- Required track: `current_track`

The RFC asks review to choose among outcomes A–E. Selecting one candidate is therefore review work,
not an RFC revision, provided the chosen outcome preserves the RFC invariants and closes its stated
measurement questions.

## Bound evidence set

1. Original problem/evidence/validation packet committed at `d71750ab` under AK `5228`, evidence
   `8005`.
2. Commit-bound parent/owner census: parent 22 paths, owner 46, common 16, owner-only 30,
   parent-only 6, exactly one common blob mismatch.
3. Static consumer census:
   - eight owner semantic paths are consumed by parent ROCS behavior;
   - `.gitkeep` is a parent template marker;
   - 37 remaining owner paths are owner control/docs/tooling, not parent runtime inputs;
   - the six parent receipts have no independent literal reader but carry parent/path identity.
4. C-vs-E scratch artifact:
   `/home/tryinget/.local/state/pi-quests/evidence/decision144-c-vs-e-20260831T063519Z`, manifest-file
   SHA-256 `5216f88bb26188cb7a5b6e24b1ba547cf5cad341a74744c6cfb5cab9e8d90b11`.
5. Corrected owner-CI causal audit:
   `/home/tryinget/.local/state/pi-quests/evidence/decision144-owner-ci-causality-20260831T142438Z`,
   manifest-file SHA-256 `056444d49e68d8f407de8f441bdffde39d49e4ec77f45126e42eb576924e4953`,
   also recorded as AK evidence `8040`.
6. AK `5197` finalization commit `74cc0a59786d2450f172ee87a249f327a044ff07`, evidence `8033`:
   the existing ownership state is established, so a later topology change must use a new map/state
   transition rather than modifying pending state.
7. Current review boundary: Softwareco `2f7653dc618bb6e7ffe26b4b724e50055c972ed0`;
   ontology owner `07d4b8b89f6ca436618adb42827885e9a45289c7`, clean; preserved stash
   `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`.

## Review questions

1. Which A–E candidate best enforces one source owner and physical write isolation?
2. Does fresh materialization fail closed without ambient nested Git metadata?
3. Are the six receipts moved and regenerated under correct parent identity before their old paths
   disappear?
4. Can generic raw-gitlink recursion be avoided while materializing exactly `ontology`?
5. Does the selected outcome provide a new plan-first ownership-map/state transition after AK 5197?
6. Are unavailable-source behavior and rollback atomic and byte-preserving?
7. Does any observed command cross owner boundaries without authority?

## Integrity controls

- The current-track memo must cite this plan and the exact artifact identities above.
- The earlier claim that ontology-owner CI wrote downstream consumer receipts is superseded by the
  focused causal audit; repeating it is a review-integrity failure.
- Scratch candidates are feasibility evidence, not implementation or adoption authority.
- No current `ontology/**` worktree entry may be staged before accepted ADR and exact post-ADR tasks.
- Legal closure requires a separately attached designated synthesis that cites the current-track
  attempt.
