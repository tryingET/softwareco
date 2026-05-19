---
summary: "Single-file session handoff to avoid stale status/next-steps docs."
read_when:
  - "At the start of every work session"
  - "When resuming after a pause"
---

# Next Session Prompt

## SESSION TRIGGER (AUTO-START)
Reading this file is authorization to begin immediately.
Do not ask for permission to start.

## ANTI-STALE RULES (HARD)
- Keep this file short and current.
- Keep only the active handoff window (not a history log).
- Move finished session narrative to `diary/`.
- Crystallize durable patterns in `docs/learnings/` and decisions in `docs/decisions/`.
- Track deferred work in `governance/work-items.json` (not in ad-hoc TODO notes).

## SOURCE-OF-TRUTH MAP
- Repo operating contract: `AGENTS.md`
- Mission and goals: `docs/project/`
- Active/deferred work contract: `governance/work-items.json`
- Prior decisions: `docs/decisions/`
- Crystallized learnings: `docs/learnings/`
- Raw session capture: `diary/`

## ACTIVE HANDOFF
- `fork/` lane baseline remains the control-plane shell for the softwareco fork lane.
- The first actual child repo now exists: `softwareco/fork/pi-mono`.
- Lane-root work is now mostly policy/inventory; repo-local execution should happen inside child repos.
- Next bounded slice for the DSPY line lives in `pi-mono/`: decide upstream import/sync posture and pick the first executable local slice.
- Latest diary entry: `diary/2026-03-13--feat-first-fork-repo-bootstrap.md`

## SESSION PREFLIGHT (FILL BEFORE EXECUTION)
- Objective (one sentence): keep lane-root policy truthful and route real work into child repos.
- Constraints (hard limits): keep fork rationale explicit; do not re-centralize child-repo execution back into the lane root.
- Assumptions (max 3): fork lane remains for long-lived divergence; `pi-mono/` is the active child repo for the current DSPY line; future fork repos should follow the same rationale-first pattern.
- Blockers (none or list): none at lane-root level.

## READ-FIRST ALLOWLIST (STARTUP BUDGET)
1. `AGENTS.md`
2. `README.md`
3. `governance/work-items.json`
4. `docs/project/mission.md`
5. `docs/project/tactical_goals.md`
6. Most recent `diary/YYYY-MM-DD--type-scope-summary.md`

## EXECUTION MODE (ONE SESSION = ONE SLICE)
1. Pick one highest-leverage actionable slice from `governance/work-items.json`.
2. Implement end-to-end on a branch.
3. Validate:
   - `./scripts/ci/smoke.sh`
   - `./scripts/ci/full.sh` (when CI/policy/ontology/contracts changed)
4. Update source-of-truth artifacts before commit.

## SESSION CHECKPOINT (UPDATE BEFORE /commit)
- Slice executed: create the first concrete repo under `softwareco/fork/`
- Outcome: `pi-mono/` now exists as the first child repo; lane-root handoff now points execution into that child repo
- Files changed: lane-root README/mission/goals/work-items/diary/handoff
- Validation commands + results: `./scripts/ci/smoke.sh` (pass); `node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs docs --strict` (pass)
- Deferred tasks updated in `governance/work-items.json`: yes
- Next-session starting point: repo-local work should start in `pi-mono/`

## END-OF-SESSION
Run `/commit` and ensure this file reflects the real checkpoint for the next operator/agent.
