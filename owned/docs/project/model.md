---
summary: "Project model overview (purpose/mission/vision/goals)."
read_when:
  - "When onboarding or aligning scope"
---

# Project Model

`softwareco/owned` is a brownfield lane-root control-plane repo, not a single delivery product.

## It exists to capture
- Purpose / mission / vision for the owned lane root
- Strategic + tactical goals for lane-root-local improvements
- Constraints + resources for operating above child repos
- System4D context for boundary, outcomes, invariants, and risks

## Operating model
- Child repos own implementation work and repo-local task execution.
- This repo owns lane-root-local docs, helper scripts, planning projection, and navigation.
- Agent Kernel is the live deferred-work authority for this repo; `governance/work-items.json` is the checked-in mirror.
- Operators should start with `next_session_prompt.md`, then `governance/work-items.json` and/or `ak work-items check --repo . --path governance/work-items.json`, then `./scripts/preflight-repo-census.sh .`.

## Primary artifacts
- `docs/project/` for intent and goals
- `docs/decisions/` for durable scope decisions
- `docs/system4d/` for boundary and risk framing
- `governance/work-items.json` for the checked-in lane-root projection
- `diary/` for raw session capture
