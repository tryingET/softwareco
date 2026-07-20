---
summary: "Validation, rollout, and rollback plan for Decision 68."
read_when:
  - "Validating or rolling back Softwareco CTO/template activation."
type: "validation-rollout-rollback"
status: "active"
date: "2026-07-18"
decision_id: 68
---

# Validation, rollout, and rollback — CTO Agent and L1 templates

## Validation gates

1. Strict validation for changed docs.
2. Template CI source assertions.
3. Fresh project and agent renders.
4. Rendered agent governance/work-items/task-scope file checks.
5. Deterministic fake-AK proof that full CI invokes plain `ak` and rejects projection drift.
6. Negative proof that stale MR-only intent and embedded cognitive tools are absent.
7. `git diff --check` and independent review.

## Rollout

- Stage A: governance and L1 template source only.
- Stage B: fresh-render validation only; no production consumer generation.
- Stage C: one issue-tracker main-first canary under its own AK task; branch/PR only on explicit operator request.
- Stage D: human terminal decision and learning.
- Stage E: optional broader propagation only through a separate accepted template-owner decision.

## Rollback

- revoke/supersede the CTO delegation in AK;
- revert the isolated governance/template commits;
- delete disposable fresh renders;
- revert issue-tracker canary commits if Stage C began;
- verify no external effects occurred;
- re-run prior template CI and source-owner validation.

Rollback never deletes AK decision/evidence history or rewrites the canary baseline.
