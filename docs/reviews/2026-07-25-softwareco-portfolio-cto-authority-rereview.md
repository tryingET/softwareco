---
summary: "Decision 74 Track A re-review of the revised portfolio CTO constitutional authority contract."
read_when:
  - "Reviewing the second Decision 74 authority attempt."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
review_track: "authority-source-owner-federalism"
reviewed_commit: "269035fcda9e2964ded86516ca6d7a471fd1acb1"
review_outcome: "revise_rfc"
---

# Decision 74 Track A re-review

## Determination

The revision closes the prior finite-governance-delta, lifecycle separation, WIP, controller, Softwareco task-scope, FCOS, and stale-projection defects. Four constitutional defects remain.

## Prior must-fix disposition

- finite governance delta: resolved;
- role-specific acceptance: partially resolved because the controller can still assert another owner's identity;
- wrapper/owner-task lifecycle split: resolved;
- activation/expiry/revocation: partially resolved because acceptance and activation time are conflated and immediate revocation lacks a first controlling event;
- post-expiry owner-task disposition: resolved;
- one-controller protocol: substantially resolved, pending attributable human origin;
- Softwareco-root task authority: resolved;
- Decision 68 projection mismatch: resolved as a fail-closed activation gate.

## Remaining must-fixes

1. **Owner-attributable governance receipts:** controller-written `source_authority` and `actor` strings are not consent. Require the accountable owner to originate the receipt or require a mandatory verified `evidence_ref` to owner-native acceptance. Apply this to Product/Domain/Project/Service/Platform acceptance, controller designation/handover, second-wave checkpoint, revocation, and terminal decision.
2. **Objection versus fallback:** fallback applies only to genuine role vacancy or role-identity ambiguity. A substantive owner objection blocks the wave unless a separate lawful human-reserved decision resolves the underlying posture or ownership conflict.
3. **Terminal acceptance:** define distinct terminal receipts for Product/Domain outcome and terminal evidence, Project/source-owner implementation evidence, and Service/Platform acceptance where applicable. Require all before portfolio-wrapper completion.
4. **Activation/revocation timing:** distinguish `accepted_at_utc` from actual `activated_at_utc`; keep expiry exactly 30 days after acceptance. An attributable revocation receipt terminates authority immediately, while the subsequent `SF3` update is readback/reconciliation. Pre-operation checks query revocation/supersession/terminal concerns directly. Do not imply `ak direction update` has compare-and-swap; use fresh pre/post-read and manual conflict reconciliation.

## Material nice-to-haves

- Land deterministic validators for governance/controller/admission details before activation.
- Add a worked multi-owner acceptance/objection example.
- Give the second-wave checkpoint an exact concern and readback rule.
- Define heterogeneous owner-status mapping where a source owner does not use AK's status vocabulary.
- State that terminal `continue` still ends the finite delegation and requires renewal/supersession.

## Open questions

Four decision-blocking questions remain: owner-origin proof, substantive objection handling, terminal role acceptances, and distinct acceptance/activation/revocation/terminal events. Descendant `/cto` discovery is the only non-blocking usability question.

## Outcome and legal next move

- outcome: `revise_rfc`
- legal next move: revise, commit a new immutable candidate, repeat Track A, and run a new controlling synthesis.
- blocked: Decision 74 acceptance, ADR, or CTO activation from commit `269035f`.

No files or runtime state were mutated by the reviewer.
