---
summary: "Authority re-review of Decision 77 RFC revision 2 at commit c2e0487."
read_when:
  - "Tracing why Decision 77 required RFC revision 3."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "c2e0487108186444ca57ddd4f6ad04246ffec090"
review_outcome: "revise_rfc"
---

# Decision 77 authority re-review — attempt 2

## Identity

- Track: authority, constitutional legality, and owner federalism.
- Exact reviewed commit: `c2e0487108186444ca57ddd4f6ad04246ffec090`.
- Reviewer dispatch: `dispatch-1784988042987`.
- Outcome: `revise_rfc`.

## Resolved attempt-1 blockers

- The accepted decision is now a dormant framework; no CTO is appointed between epochs.
- Epoch authorization is finite, non-renewable, claimant-bound, and fail-closed.
- A distinct Decision-77 child projection preserves `SF3` and receipt `8870`.
- Human-reserved stop conditions are operative and cumulative waves cannot bypass them.
- Framework-review expiry blocks new epochs.

## Remaining blockers

1. `IW-SF3-CTO77-RECURRING` used unsupported native kind `implementation_wave`; AK native authoring supports `work_wave`.
2. Owner receipt schemas were named but lacked exact payload fields, transitions, and objection resolution/withdrawal law.
3. Revocation and terminal transitions were not legal from every nonterminal framework posture.
4. Supersession lacked an exact machine-readable authoritative relation.

## Required correction

Use `work_wave`; specify normative owner payload/state contracts and non-forking objection resolution; permit direct human terminal/revocation from every nonterminal posture; and make a fixed Decision-77 supersession receipt the required runtime relation backed by an exact accepted successor decision.

## Legal next move

Revise and rerun both tracks. ADR and acceptance remain illegal until a later controlling synthesis emits `ready_for_adr`.
