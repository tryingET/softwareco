---
summary: "Flow, constraints, quality, and measurement review attempt for the initial Software Factory Flow Protocol RFC draft."
read_when:
  - "Reviewing the first adversarial RFC review set."
type: "review-attempt"
---

# Review attempt — flow, constraints, quality, and measurement

## Review chain status

- review kind: Tier 1 pre-ADR review attempt
- reviewed artifact: `docs/project/2026-07-12-software-factory-operating-system-rfc.md`
- reviewed worktree SHA-256: `31e194ea9b77dc439a7f9b1b9ad1dac3e92fc7ca981b3c9a3c2888a04d1cb298`
- revision status: untracked worktree content at review time
- method: Prompt Vault `layer12-070-decision-rfc-review`
- traditions applied: Lean/Toyota flow, constraint management, and system-quality thinking; no persona simulation
- ADR legal now?: no

## Lenses

1. flow and WIP economics;
2. systemic quality and feedback;
3. measurement and gaming resistance.

## Strengths

- Makes finite WIP, displacement, blocked age, and stopping visible.
- Separates deployment from outcomes.
- Resists optimizing coding throughput before locating the system constraint.
- Preserves a bounded pilot.

## Must-fix findings

1. Define WIP units, scope, counting rules, and treatment of exploration, maintenance, and exceptions that consume the same constrained capacity.
2. Name admission, displacement, expedite, stop-work, and over-limit authority.
3. Require the pilot to state a hypothesized constraint and detect when it moves.
4. Define immutable start/stop events for lead-time measures.
5. Separate protocol conformance from pilot effectiveness; documentary completeness alone cannot prove improvement.
6. Pre-register the pilot outcome, baseline, horizon, guardrails, and stop/redirect threshold.
7. Define “successful pilot” before using two successful pilots as a propagation gate.
8. Normalize terminal-decision tokens and restrict the learning waiver after failure or redirect.

## Workflow result

- review_outcome: `revise_rfc`
- next legal move: `revise_rfc`
- controlling rationale:
  - central WIP and measurement controls are not operationally falsifiable;
  - non-commitment classes can hide total load;
  - a compliant packet could pass without improving flow, quality, or outcomes.

## Final recommendation

Revise before ADR and re-review the exact revised artifact.
