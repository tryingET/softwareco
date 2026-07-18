---
summary: "Architecture and authority review attempt for the initial Software Factory Flow Protocol RFC draft."
read_when:
  - "Reviewing the first adversarial RFC review set."
type: "review-attempt"
---

# Review attempt — architecture and authority

## Review chain status

- review kind: Tier 1 pre-ADR review attempt
- reviewed artifact: `docs/project/2026-07-12-software-factory-operating-system-rfc.md`
- reviewed worktree SHA-256: `31e194ea9b77dc439a7f9b1b9ad1dac3e92fc7ca981b3c9a3c2888a04d1cb298`
- reviewed Git blob hash: `07cca7fa08d43d9248d3b84565e81404440ca7f3`
- revision status: untracked worktree content at review time
- method: Prompt Vault `layer12-070-decision-rfc-review`
- ADR legal now?: no
- reason: the RFC was untracked and decisive authority/projection contracts were under-specified.

## Lenses

1. runtime authority and platform boundary;
2. semantic and contract precision;
3. verification and migration.

## Strengths

- Correctly rejects a new factory platform or database.
- Preserves AK, FCOS, ROCS, Pi, KES, DSPx, and source-owner boundaries.
- Uses a bounded, reversible pilot rather than broad rollout.
- Separates engineering completion, promotion, operation, and outcome.

## Must-fix findings

1. Assign exactly one canonical authority and mutation actor for each decision-bearing field; phrases such as “AK or accepted governance owner surface” are insufficient.
2. Define the manual packet as a projection membrane: identity, canonical links, freshness, reconciliation owner, conflict behavior, and prohibition on packet-only decisions.
3. Resolve overlapping work classifications and normalize terminal-decision tokens.
4. Complete the Tier-1 vocabulary preflight fields and promotion decision.
5. Define executable drift, rollback, and pilot evaluation checks.
6. Track the RFC and review artifacts before they can support ADR legality.

## Workflow result

- review_outcome: `revise_rfc`
- next legal move: `revise_rfc`
- controlling rationale:
  - good architectural direction;
  - unresolved canonical write surfaces could create shadow authority;
  - semantic and reconciliation contracts are not testable enough;
  - artifact immutability requirements are not met.

## Final recommendation

Request another RFC revision round. Do not open an ADR from this reviewed revision.
