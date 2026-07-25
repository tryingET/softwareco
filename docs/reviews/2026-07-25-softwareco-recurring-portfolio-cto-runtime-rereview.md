---
summary: "Runtime/operator re-review of Decision 77 RFC revision 2 at commit c2e0487."
read_when:
  - "Tracing why Decision 77 required RFC revision 3."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "c2e0487108186444ca57ddd4f6ad04246ffec090"
review_outcome: "revise_rfc"
---

# Decision 77 runtime/operator re-review — attempt 2

## Identity

- Track: runtime/operator recurrence.
- Exact reviewed commit: `c2e0487108186444ca57ddd4f6ad04246ffec090`.
- Reviewer dispatch: `dispatch-1784988042988`.
- Outcome: `revise_rfc`.

## Resolved attempt-1 blockers

- Epoch discovery uses a fixed concern and a bounded single-head chain.
- Fresh workers are read-only; the controller independently verifies and records evidence.
- Thesis schema/lineage, WIP semantics, objective proof, checker modes, negative controls, and periodic-review consequences are normative in principle.
- Attempt-1 review artifacts and synthesis exist in Git and AK.

## Remaining blockers

1. The RFC assumes unsupported `ak evidence search` repo/limit/JSON options for thesis and WIP reconstruction.
2. The projection kind `implementation_wave` is not legal native AK authoring.
3. Supersession has no deterministic bounded machine relation.
4. AK's current review lineage exposes one `current_track`; the strongest supported synthesis must cite both review refs explicitly even if machine track identity is lossy.

## Required correction

Use shipped structured reads only: direction projection head IDs, `ak evidence show --json`, epoch controller task IDs, and `ak evidence task --machine`. Use `work_wave`, define fixed supersession receipt law, and make the next synthesis explicitly cite both exact review artifacts in its document and AK note.

## Legal next move

Revise and rerun both tracks. Do not record an ADR or accept Decision 77 until the latest synthesis says `ready_for_adr`.
