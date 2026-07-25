---
summary: "Runtime and operator review of Decision 77 recurring CTO RFC at commit 7f02483."
read_when:
  - "Revising or assessing the first Decision 77 RFC candidate."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "7f024832046f98c4c67beb95304f7a49aed7e27c"
review_outcome: "revise_rfc"
---

# Decision 77 runtime/operator review — attempt 1

## Identity

- Track: runtime/operator recurrence.
- Reviewed artifact: `docs/project/2026-07-25-softwareco-recurring-portfolio-cto-rfc.md`.
- Exact reviewed commit: `7f024832046f98c4c67beb95304f7a49aed7e27c`.
- Reviewer dispatch: `dispatch-1784988042988`.
- Method: strict adversarial, read-only.
- Outcome: `revise_rfc`.

The unrelated modification at `owned/docs/project/repo-capability-map.md` was excluded.

## Blocking findings

### R1 — No deterministic current-epoch discovery

The RFC names an epoch-specific concern that requires knowing `epoch_id` before lookup. It defines no fixed index, uniqueness rule, bounded lookup, overlap handling, or tie-breaker.

**Required correction:** define one fixed Decision-77 current-epoch surface and exact algorithm. Zero, multiple, overlapping, malformed, expired, handed-back, or ambiguous candidates fail closed. Never select an arbitrary latest accepted decision.

### R2 — Fresh worker conflicts with thesis mutation

Run A permits a non-controller read-only process but requires that process to record AK thesis evidence. The current sensing lane forbids mutation.

**Required correction:** define Run A/Run C actors, tools, claimed tasks, controller handoff, mutation owner, inputs, outputs, hashes, and state references. A fresh worker must not inherit or silently record a prior thesis.

### R3 — Thesis series is not reconstructible

“Schema equivalent to” does not enforce schema identity, task/decision binding, revision uniqueness, predecessor validity, expiry, fact-reference format, or a unique head.

**Required correction:** make exact `check_type`, schema, decision/epoch/task fields, revision allocation, predecessor rule, validity bound, census basis, fact refs, and latest-head selection normative. Forks, gaps, duplicates, expiry, missing refs, or multiple heads fail closed.

### R4 — WIP and repeated-wave reconstruction underspecified

No canonical counting algorithm handles event/projection disagreement, duplicate events, partial release, returned tasks, missing release, or Decision 74 versus Decision 77 wrappers.

**Required correction:** define canonical keys, decision/epoch identity, event transitions and ordering, owner-task membership, partial release, return semantics, wave completion, and exact counts. Disagreement counts conservatively as outstanding and blocks admission.

### R5 — Objective completion has no authoritative record

No exact entity or schema proves Run A + outcome + Run C while leaving the framework nonterminal.

**Required correction:** define an objective-proof evidence schema and task/direction binding with trace hashes, thesis IDs, owner receipts, task/outcome/release refs, checker results, limits, and explicit `standing_terminal_receipt_created=false`. Add a dedicated checker mode.

## Additional required corrections

### R6 — Checker needs a normative state matrix

Define exact modes, inputs, expected exits, and fail-closed behavior for:

- Decision 74 terminal negative control;
- Decision 77 preactivation;
- framework valid/expired/revoked/terminal/superseded;
- epoch absent/active/expired/handed back;
- claimant/lease mismatch;
- thesis current/stale/forked/ambiguous;
- WIP and projection disagreement;
- objective incomplete/complete without mandate termination.

### R7 — Negative controls incomplete

Add tests for no accepted successor, no epoch, expired/handed-back epoch, claimant mismatch, overlap, revocation/terminal/supersession, overdue framework review, thesis failure modes, WIP limits, missing second-wave checkpoint, read-only mutation attempt, objective proof without a terminal receipt, and terminal precedence over apparent epoch activity.

### R8 — Periodic review has no runtime consequence

Define the human-originated review concern/evidence, validity interval, bounded discovery, and checker behavior. Missing, overdue, ambiguous, or invalid review makes mutation advisory-only.

### R9 — Review closure is not yet evidenced

The Decision 77 review-plan note is not two review artifacts or a controlling synthesis.

**Required correction:** attach exact authority and runtime memos plus synthesis, and verify aligned legal closure through the AK passport.

## Legal next move

Do not advance Decision 77. Persist this memo, revise the RFC, rerun both tracks against the revised commit, and obtain controlling synthesis. ADR becomes legal only after `ready_for_adr` closure.
