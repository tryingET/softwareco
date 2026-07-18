---
summary: "Reliability, operator-adoption, and failure-containment review attempt for the initial Software Factory Flow Protocol RFC draft."
read_when:
  - "Reviewing the first adversarial RFC review set."
type: "review-attempt"
---

# Review attempt — operations, adoption, and failure containment

## Review chain status

- review kind: Tier 1 pre-ADR review attempt
- reviewed artifact: `docs/project/2026-07-12-software-factory-operating-system-rfc.md`
- reviewed worktree SHA-256: `31e194ea9b77dc439a7f9b1b9ad1dac3e92fc7ca981b3c9a3c2888a04d1cb298`
- revision status: untracked worktree content at review time
- method: Prompt Vault `layer12-070-decision-rfc-review`
- ADR legal now?: no

## Lenses

1. release and service reliability;
2. operator ergonomics and adoption;
3. failure containment and rollback.

## Strengths

- Separates engineering completion, promotion, operation, and outcomes.
- Requires health/readback, rollback, and named service posture.
- Preserves owner boundaries.
- Proposes a reversible pilot instead of migration.

## Must-fix findings

1. Add risk-tiered operational acceptance with evidence thresholds, observation windows, rollback/restore proof, and incident ownership.
2. Define prototype/light-posture eligibility and expiry.
3. Provide a worked operator journey and packet, including field-by-field canonical update paths.
4. Specify cadence mechanics, decision rights, escalation, degraded operation, and conflict reconciliation.
5. Add cold-start operator and protocol-overhead acceptance criteria.
6. Separate protocol rollback, release rollback, state/data recovery, and organizational unwind.
7. Define rollback triggers, commander, time bounds, blast-radius control, irreversible migration handling, and failure exercise.

## Workflow result

- review_outcome: `revise_rfc`
- next legal move: `revise_rfc`
- controlling rationale:
  - documentary completeness could pass without demonstrated reliability;
  - operator success depends on tacit knowledge the protocol is meant to remove;
  - protocol abandonment is reversible, but releases, state, and organizational commitments may not be.

## Final recommendation

Request another RFC revision and a new review attempt against the durable revised artifact.
