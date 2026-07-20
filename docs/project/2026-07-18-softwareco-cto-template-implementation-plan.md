---
summary: "Implementation plan for Softwareco CTO Agent governance and L1 agent/project template activation."
read_when:
  - "Implementing Decision 68."
type: "implementation-plan"
status: "active"
date: "2026-07-18"
decision_id: 68
---

# Implementation plan — CTO Agent and L1 templates

## Phase 1 — governance

- activate `docs/org/governance.md` through Decision 68;
- add `docs/org/cto-agent-charter.md`;
- update the operating model with the bounded CTO packet and current activation state.

## Phase 2 — shared template contract

- add company-neutral delegation discovery, finite WIP, outcome/effect, escalation, and terminal-authority rules to project and agent AGENTS templates;
- preserve project-template product posture, AK projection, and source-owner rules.

## Phase 3 — agent-template parity

- redefine agent repos as product/capability owners rather than appointments;
- add AK work-items and task-scope projection files/checkers;
- update full CI to use plain installed `ak`;
- add generic engineering-core and Prompt Vault routing;
- remove embedded cognitive-tool templates.

## Phase 4 — deterministic acceptance

- extend template CI with source and rendered positive/negative assertions;
- test drift failure through a deterministic fake `ak`;
- run strict docs, template CI, and diff checks;
- obtain independent final review.

## Phase 5 — canary handoff

After L1 acceptance, create a separate `infra/issue-tracker` source-owner task under the repository's main-first workflow. Do not mutate the canary from this task, and use a branch or PR only if the operator explicitly requests a review gate.
