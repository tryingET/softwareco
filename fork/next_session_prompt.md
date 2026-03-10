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
- `fork/` lane baseline was materialized on 2026-03-10 from `tpl-project-repo`.
- Parent repo still needs to commit `.gitignore`, `scripts/bootstrap-lane-root.sh`, and `fork/` before lane-root git can be initialized with:
  - `./scripts/bootstrap-lane-root.sh fork --init-lane-git`
- Immediate intended use: host local forks for DSPY-related work that will no longer be pursued through `badlogic/pi-mono` upstream requests.

## SESSION PREFLIGHT (FILL BEFORE EXECUTION)
- Objective (one sentence): initialize first actual fork repo under this lane
- Constraints (hard limits): do not init lane git before parent repo commit; keep fork rationale explicit in docs/decisions
- Assumptions (max 3): fork lane remains for long-lived divergence, not casual mirrors; parent `softwareco/` repo owns lane policy; first fork likely comes from DSPY/pi-mono needs
- Blockers (none or list): parent repo commit still pending before `--init-lane-git`

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
- Slice executed:
- Outcome:
- Files changed:
- Validation commands + results:
- Deferred tasks updated in `governance/work-items.json`:
- Next-session starting point:

## END-OF-SESSION
Run `/commit` and ensure this file reflects the real checkpoint for the next operator/agent.
