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
- Do **not** mirror low-level live state that is directly queryable from a DB, CLI, CI, or runtime script.
- If state can be queried, point to the command instead of restating the result.
- Move finished session narrative to `diary/`.
- Crystallize durable patterns in `docs/learnings/` and decisions in `docs/decisions/`.
- Track deferred work in Agent Kernel and keep `governance/work-items.json` as the checked-in projection (not in ad-hoc TODO notes).

## SOURCE-OF-TRUTH MAP
- Repo operating contract: `AGENTS.md`
- Mission and goals: `docs/project/`
- Active/deferred work authority: Agent Kernel work-items state
- Checked-in work-items projection: `governance/work-items.json`
- Explicit task-scope snapshots (when present; frozen exports, not hand-authored truth): `governance/task-scopes/AK-<TASK-ID>.snapshot.json`
- Prior decisions: `docs/decisions/`
- Crystallized learnings: `docs/learnings/`
- Raw session capture: `diary/`
- Queryable live state: runtime commands / DB / CI outputs (reference commands, do not copy snapshots)

## WORK-ITEMS COMMANDS
- Check projection drift: `ak work-items check --repo . --path governance/work-items.json`
- Refresh projection from AK: `ak work-items export --repo . --path governance/work-items.json`
- Legacy JSON bootstrap only: `ak work-items import --repo . --path governance/work-items.json`
- Show explicit task scope (when used): `ak task scope show <TASK-ID>`
- Refresh task-scope snapshot (when used): `mkdir -p governance/task-scopes && ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json`
- Legacy `governance/task-scopes/AK-*.json` files are compatibility-only; do not treat them as primary authored truth.

## SESSION PREFLIGHT (FILL BEFORE EXECUTION)
- Objective (one sentence): Finalize safe brownfield adoption for the `softwareco/owned` lane root without losing lane-local semantics.
- Constraints (hard limits): Preserve meaningful lane-root docs/scripts, do not touch child repos as part of the slice, and do not reintroduce GitLab surfaces.
- Assumptions (max 3):
  1. Template convergence in `softwareco` is already committed and `bash ./scripts/check-template-ci.sh` passes at the L1 root.
  2. `./scripts/bootstrap-lane-root.sh owned` provided the baseline overlay, but the brownfield lane root still requires intentional merge treatment.
  3. `governance/work-items.json` and other generated projections should only be committed through an explicit decision, not as incidental adoption noise.
- Blockers (none or list): explicit decision still pending on whether to commit the current `governance/work-items.json` export.

## READ-FIRST ALLOWLIST (STARTUP BUDGET)
1. `AGENTS.md`
2. `README.md`
3. `governance/README.md`
4. `governance/work-items.json`
5. `docs/project/tactical_goals.md`
6. `git status --short`

## EXECUTION MODE (ONE SESSION = ONE SLICE)
1. Separate baseline adoption changes from generated/runtime artifacts.
2. Preserve lane-root semantics while adopting deterministic tooling improvements.
3. Validate the intended commit surface.
4. Update source-of-truth artifacts before commit.

## SESSION CHECKPOINT (UPDATE BEFORE /commit)
- Slice executed: Restored lane-root docs/prompts, kept template-derived control-plane/tooling updates, and separated obvious generated artifacts from baseline adoption.
- Outcome: `softwareco/owned` again reads as a brownfield lane root rather than a generic L2 project repo; projection-heavy surfaces still require explicit commit decisions.
- Files changed: lane-root docs/prompts, `.gitignore`/ownership metadata, control-plane scripts, vendored `tools/rocs-cli`, and pending projection artifacts requiring explicit review.
- Validation commands + results:
  - not run yet in this reconciliation pass
- Deferred/pending decision: decide whether the current `governance/work-items.json` export belongs in the adoption series or should be handled separately.
- Next-session starting point: inspect `git status --short`, stage only keep/merge surfaces, and decide the fate of `governance/work-items.json` before running the final validation lane.

## END-OF-SESSION
Run `/commit` only after this file reflects the real checkpoint for the next operator/agent.
