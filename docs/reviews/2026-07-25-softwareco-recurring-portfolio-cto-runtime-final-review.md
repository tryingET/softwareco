---
summary: "Runtime/operator review attempt 3 of Decision 77 RFC at commit 814ffa5."
read_when:
  - "Tracing why Decision 77 required one final RFC correction."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "814ffa58beed385ba2e4fbe9fa76a404240b09a2"
review_outcome: "revise_rfc"
---

# Decision 77 runtime/operator review — attempt 3

## Identity

- Track: runtime/operator recurrence.
- Exact commit: `814ffa58beed385ba2e4fbe9fa76a404240b09a2`.
- Reviewer dispatch: `dispatch-1784988042988`.
- Outcome: `revise_rfc`.

## Resolved

- Unsupported evidence-search options were removed in favor of shipped structured AK reads.
- `work_wave` is legal native direction authoring.
- Fixed supersession receipt discovery is deterministic.
- Epoch, worker/controller, thesis schema, objective proof, checker matrix, negative controls, and review-expiry semantics remain implementable in principle.

## Remaining blockers

1. Walking only backward from projected thesis head cannot detect a second valid thesis fork or an evidence-write/head-update crash orphan.
2. WIP reconstruction expects wave direction projection to contain release/outcome evidence IDs, but only admitted state detail is defined.
3. Objective-complete checker must require absence of valid supersession as well as terminal/revocation.

## Required correction

- Make every valid thesis-bearing task discoverable from the exact Decision-77 direction node, enumerate each through `ak evidence task --machine`, and require one complete chain whose head equals the projection.
- Define exact admitted, partial-release, returned, completed, and reconciliation-required wave state details with sorted task/event IDs.
- Add supersession absence to objective-complete semantics.

## Legal next move

Revise and rerun both tracks. ADR remains illegal until a later synthesis emits `ready_for_adr`.
