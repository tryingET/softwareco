---
summary: "Decision 74 Track A review of constitutional authority and source-owner federalism for the Softwareco portfolio CTO."
read_when:
  - "Reviewing Decision 74 authority closure."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
review_track: "authority-source-owner-federalism"
reviewed_commit: "bcce0340812163042f45876932141f4ce62de0c1"
review_outcome: "revise_rfc"
---

# Decision 74 review — constitutional authority and source-owner federalism

## Reviewed artifact

- RFC: `docs/project/2026-07-25-softwareco-portfolio-cto-rfc.md`
- exact Softwareco commit: `bcce0340812163042f45876932141f4ce62de0c1`
- FCOS authority reference: `holdingco/fcos-control-board` commit `b5efb2502608c6973ffabd3667f245bc1bbf342f`

## Determination

A finite portfolio CTO delegation is constitutionally possible through an accepted Tier-1 AK decision. The candidate substantially preserves human residual powers, AK execution authority, source-owner implementation authority, and FCOS ownership.

It is not ADR-ready because the operative law does not yet reconcile autonomous portfolio sequencing with current Product/Domain accountability, role-specific owner acceptance, expiry/revocation readback, and the non-atomic single-controller constraint.

## Must-fixes

1. **Finite decision-right delta:** identify the temporarily amended governance allocations. Preserve the Softwareco Org Owner as accountable human; require Product/Domain acceptance for wave outcome, priority, and capacity; Project Maintainer acceptance for each exact task; and Service/Platform acceptance when operational or shared-contract obligations are affected.
2. **Role-specific acceptance:** name the authoritative artifact for each acceptance and reference it without copying lifecycle state. Repository acceptance cannot substitute automatically for Product or Domain acceptance because a repository is not necessarily a product or organizational domain.
3. **Separate lifecycles:** pausing, redirecting, displacing, or completing a portfolio wrapper must not mutate an owner task. Displacement requires the affected accountable owner's acceptance.
4. **Exact authority readback:** record accepted decision, `effective_at`, exact UTC `expires_at`, required `SF3` state, revocation action, terminal decision, and mismatch precedence. Revalidate before every admission or mutation, not only `/cto` startup.
5. **Post-expiry disposition:** expiry/revocation ends CTO control and admission but does not close, pause, redirect, or release owner tasks; hand them back to their source owners.
6. **Operable controller protocol:** designate one controller through an exact Softwareco AK task, define human designation/handover/stale-session behavior, serialize admissions, and perform pre/post readback. If exclusivity cannot be demonstrated, require a human checkpoint per admission or narrow the canary.
7. **Softwareco mutation scope:** every `SF3` child-wave, controller, or coordinator mutation requires an exact claimed Softwareco-root AK task.
8. **Repair stale projections:** governance and charter still describe Decision 68 as active-bounded while AK terminal evidence says it expired. Activation must fail on AK/`SF3`/governance/charter disagreement.

## Material nice-to-haves

- Add lawful portfolio-wrapper versus unlawful owner-task-control examples.
- State that FCOS creation/closure is coordination evidence, not owner acceptance.
- State whether coordinator and FCOS-owner tasks count toward WIP.
- Add an owner objection/appeal route.
- Require a human checkpoint before admitting the second concurrent wave in the first canary.

## Open questions

Six material questions remain: role precedence for wave acceptance; the boundary between technical sequencing and product ordering; controller identity representation; whether AK claim is sufficient or human serialization is required; owner-task disposition on expiry; and whether two concurrent canary waves are justified before controller proof.

## Preserved boundary

The RFC correctly keeps FCOS coordination-only and non-claimable, does not authorize FCOS writes from Softwareco, and does not require FCOS for single-repository work.

## Outcome and legal next move

- review outcome: `revise_rfc`
- legal next move: revise and commit a new immutable RFC candidate, then re-run Track A and controlling synthesis.
- prohibited next moves: Decision 74 acceptance, ADR recording, CTO activation, owner-task admission, or FCOS mutation from this candidate.

No files were mutated by the reviewer.
