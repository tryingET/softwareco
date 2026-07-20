---
summary: "Evidence supporting Softwareco CTO Agent governance activation and bounded L1 template changes."
read_when:
  - "Reviewing evidence for the CTO Agent and template activation RFC."
type: "evidence-note"
status: "proposed"
date: "2026-07-18"
---

# Evidence — CTO Agent and template activation

## Current governance

- `docs/org/governance.md` declares the Softwareco governance model `proposed_inactive` and says no accepted decision appoints an Org Owner.
- Decision 62 delegated `softwareco-cto-agent` only for pilot 001 and explicitly expired that delegation at the terminal decision.
- The human operator has now directed: implement the governance/template recommendations first, then use `infra/issue-tracker` as the test repository.

## Current template evidence

### Project template

`copier/tpl-project-repo/AGENTS.md.j2` already includes:

- AK-native route guardrails;
- work-items projection semantics;
- task-scope exports;
- owner-surface handoff boundaries;
- main-first policy and deterministic validation.

It does not yet state how an agent discovers a company delegation, admits finite WIP, distinguishes validation from outcomes, or reserves terminal decisions.

### Agent template

`copier/tpl-agent-repo/AGENTS.md.j2` currently:

- describes one repository per agent and “proposals + merge requests” while also declaring main-first work;
- lacks project-template parity for AK work-items and task-scope projections;
- embeds a growing cognitive-tool catalog instead of routing reusable procedures through Prompt Vault;
- does not distinguish an agent product repository from an organizational agent delegation.

## Canary evidence

`infra/issue-tracker` is an active operator-facing infrastructure repository with:

- canonical AK issue state and a generated `STATE.json` projection;
- explicit external-effect risk around upstream issue submission;
- repo-local docs that, at evidence-capture time, claimed an MR-only exception; closeout later proved that claim stale and restored Softwareco's main-first policy (`518ab43`, correction evidence `#4971`);
- deterministic validation and sequence workflows;
- two existing pending tasks and a preserved non-promoted WIP branch.

It is materially different from pilot 001 because it exercises active operator work, projection truth, review readiness, and external-effect boundaries. It does not by itself prove customer-product delivery.

## Propagation boundary

This activation changes only Softwareco's L1 embedded templates. Existing L2 repositories, L0 `core/tpl-template-repo`, and external/public templates do not change automatically. Broader propagation requires canary evidence and a separate owner decision.
