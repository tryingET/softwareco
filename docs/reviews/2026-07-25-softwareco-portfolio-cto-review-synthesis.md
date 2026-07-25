---
summary: "Controlling first review synthesis for Decision 74, requiring RFC revision before ADR readiness."
read_when:
  - "Determining the legal next move for Decision 74."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
reviewed_commit: "bcce0340812163042f45876932141f4ce62de0c1"
review_outcome: "revise_rfc"
---

# Decision 74 first review synthesis

## Review set

- reviewed RFC commit: `bcce0340812163042f45876932141f4ce62de0c1`
- authority/source-owner track: [authority review](2026-07-25-softwareco-portfolio-cto-authority-review.md)
- runtime/operator/WIP/FCOS track: [runtime review](2026-07-25-softwareco-portfolio-cto-runtime-review.md)
- synthesis owner: `human-accountable Pi decision-support session` under task `4156`
- synthesis rule: every material must-fix from either required track blocks ADR readiness; no majority override.

## Shared judgment

Both tracks accept the architectural direction: the CTO may become a finite AK-governed portfolio sequencing role; Pi Modes may provide behavior but not authority; owner repositories retain execution; FCOS remains coordination-only.

Both tracks reject the exact candidate as ADR-ready. The gaps converge into five controlling requirements:

1. specify the finite governance decision-right delta and role-specific owner acceptance;
2. bind exact activation, expiry, revocation, controller identity, and per-operation revalidation to authority-owned AK/`SF3` state;
3. define WIP membership, counting states, admission/release, coordinator relations, and non-atomic single-controller serialization without claiming a lock;
4. pin an immutable Pi Modes owner revision/release and root-only `/cto` contract with exact argument behavior;
5. keep portfolio-wave, owner-task, and FCOS-item lifecycles separate, including post-expiry handback and declined-handoff behavior.

## Open questions

The first review set leaves architecture-shaping questions unresolved. They concern role precedence, technical-versus-product sequencing, exact controller/admission representation, task-state counting, Pi Modes release identity, expiry state, and first-canary concurrency. These are not acceptable post-ADR implementation details.

## Controlling outcome

- final review outcome: `revise_rfc`
- legal next move: revise the RFC, commit a new immutable candidate, run new Track A and Track B review attempts, and produce a new controlling synthesis.
- blocked: ADR, Decision 74 acceptance, delegated `SF3` activation, workbench activation, portfolio admission, owner-repo mutation, and FCOS mutation.

The review attempts remain immutable historical evidence and must not be overwritten by the re-review.
