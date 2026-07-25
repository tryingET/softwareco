---
summary: "Controlling synthesis for Decision 77 review attempt 2 at commit c2e0487."
read_when:
  - "Determining why Decision 77 RFC revision 2 was not ADR-ready."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "c2e0487108186444ca57ddd4f6ad04246ffec090"
review_outcome: "revise_rfc"
---

# Decision 77 review synthesis — attempt 2

## Inputs

- Authority: `2026-07-25-softwareco-recurring-portfolio-cto-authority-rereview.md`, dispatch `dispatch-1784988042987`.
- Runtime/operator: `2026-07-25-softwareco-recurring-portfolio-cto-runtime-rereview.md`, dispatch `dispatch-1784988042988`.
- Exact RFC revision: commit `c2e0487108186444ca57ddd4f6ad04246ffec090`.
- Synthesizer: task `4205` claimant.
- Rule: either blocking track requires revision.

## Controlling result

Revision 2 corrected the fundamental standing-authority defect, but it still assumes an illegal direction kind and unsupported evidence-query options, leaves owner receipt payload/objection resolution incomplete, and lacks a deterministic supersession relation.

## Outcome

`revise_rfc`

## Legal next move

Revise the RFC to use shipped structured AK surfaces and complete the remaining authority contracts. Run new authority and runtime reviews against the exact revised commit. ADR remains illegal until their controlling synthesis says `ready_for_adr`.
