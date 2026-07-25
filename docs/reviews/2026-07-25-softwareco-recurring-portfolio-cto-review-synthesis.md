---
summary: "Controlling synthesis for Decision 77 review attempt 1 at commit 7f02483."
read_when:
  - "Determining the legal next move after the first Decision 77 review set."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "7f024832046f98c4c67beb95304f7a49aed7e27c"
review_outcome: "revise_rfc"
---

# Decision 77 review synthesis — attempt 1

## Review set

- Exact RFC revision: commit `7f024832046f98c4c67beb95304f7a49aed7e27c`.
- Authority track: `2026-07-25-softwareco-recurring-portfolio-cto-authority-review.md`, dispatch `dispatch-1784988042987`, outcome `revise_rfc`.
- Runtime/operator track: `2026-07-25-softwareco-recurring-portfolio-cto-runtime-review.md`, dispatch `dispatch-1784988042988`, outcome `revise_rfc`.
- Synthesizer: task `4205` claimant `pi-session-softwareco-cto-successor-governance`.
- Rule: all blocking findings must be resolved; either required track may block ADR readiness.

## Controlling findings

The direction remains viable, but the RFC is not constitutionally or operationally closed. Revision must:

1. make Decision 77 a finite-review framework under which actual delegated authority exists only inside a human-authorized epoch;
2. define exact epoch, review, handback, revocation, terminal, and supersession receipt state machines;
3. adopt a Decision-77-specific direction projection without overwriting Decision 74 terminal history;
4. restore exact owner acceptance, objection, terminal, return, and release law;
5. enumerate all human-reserved stop conditions;
6. define deterministic current-epoch discovery and exactly-one semantics;
7. resolve the read-only worker versus thesis-recording actor split;
8. define a non-forking, expiry-bounded AK thesis series;
9. define canonical wave events and conservative WIP reconstruction;
10. define objective-proof evidence and a complete checker/negative-control state matrix.

## Outcome

`revise_rfc`

## Legal next move

Revise the RFC at a new immutable commit, then run new authority and runtime/operator review attempts against that exact revision. Prior reviews remain historical. ADR and acceptance are illegal until the latest controlling synthesis emits `ready_for_adr`.
