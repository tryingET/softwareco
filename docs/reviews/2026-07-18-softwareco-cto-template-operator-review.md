---
summary: "Template and operator review of the Softwareco CTO Agent and L1 template activation RFC."
read_when:
  - "Reviewing template implementation and canary readiness."
type: "review"
review_outcome: "revise_rfc"
date: "2026-07-18"
---

# Template/operator review — CTO Agent and template activation

## Verdict

`revise_rfc`

## Blocking findings

1. `infra/issue-tracker` cannot test changed template sources without an explicit one-repository migration/overlay exception or a fresh-render mechanism.
2. Agent-template AK parity must enumerate generated governance files, task-scope checker, plain installed `ak` behavior, README commands, and CI behavior.
3. Template CI must assert all shared contract points in source and rendered outputs, reject the stale “proposals + merge requests” intent and embedded cognitive-tool directory, verify Prompt Vault routing, and test plain-AK projection drift behavior.

## Clarifications

- Keep template language company-neutral; Softwareco's named CTO delegation belongs in Softwareco governance.
- Define the agent repo as an agent product/capability owner, not an organizational appointment.
- The issue-tracker canary validates the project/operator boundary; fresh agent-template renders validate agent output structure.
- Canary rollback needs exact baseline, allowed paths, restoration, prohibited external effects, expected classifications, and a human terminal decision.
