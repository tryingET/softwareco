---
summary: "Stable session-start procedure that routes live state to AK/runtime commands and dated diary capture."
read_when:
  - "At the start of every work session"
  - "When resuming after a pause"
---

# Next Session Prompt

## SESSION ORIENTATION
Reading this file authorizes read-only orientation only. Mutation requires explicit operator intent or a claimable AK task whose scope covers the change. If neither exists, report the ready options instead of selecting work by implication.

## ANTI-STALE RULES (HARD)
- Keep this file short, procedural, and stable.
- Do not store an active handoff window or checkpoint in this file.
- Do **not** mirror low-level live state that is directly queryable from a DB, CLI, CI, or runtime script.
- If state can be queried, point to the command instead of restating the result.
- Move finished session narrative to `diary/`.
- Crystallize durable patterns in `docs/learnings/` and decisions in `docs/decisions/`.
- Track deferred work in Agent Kernel and keep `governance/work-items.json` as the checked-in projection (not in ad-hoc TODO notes).

## SOURCE-OF-TRUTH MAP
- Repo operating contract: `AGENTS.md`
- Durable direction: `docs/project/vision.md`
- Product maturity bridge: `docs/project/product_posture.md`
  - Validate freshness with `./scripts/check-document-policy.sh` before relying on current-posture claims.
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

## READ-FIRST ALLOWLIST (STARTUP BUDGET)
1. `AGENTS.md`
2. `README.md`
3. `governance/work-items.json` (projection only; query AK if you need live state)
4. Relevant `governance/task-scopes/AK-<TASK-ID>.snapshot.json` (when explicit task scope is in play; frozen export only)
5. `docs/project/vision.md`
6. `docs/project/product_posture.md`
7. `docs/project/mission.md`
8. Most recent `diary/YYYY-MM-DD--type-scope-summary.md`

## EXECUTION MODE (ONE SESSION = ONE SLICE)
1. Inspect the exact operator-authorized concern or claimable AK task; do not treat a projection or this procedure as execution authority.
2. Claim when required, verify scope, and implement only that bounded slice using the repository's declared git workflow. If no authorized slice exists, stop after read-only orientation.
3. Validate:
   - `./scripts/ci/fast.sh`
   - `./scripts/ci/full.sh` (when CI/policy/ontology/contracts/work-items changed; it runs `fast.sh` first, then heavier checks)
4. Update source-of-truth artifacts before commit, including task-scope snapshots when they are part of the slice.
5. Update `docs/project/product_posture.md` only when product-wide claims changed, then validate it against a prior evidence commit as required by its freshness contract.
6. Name separate time-bounded transition, migration, current-vs-target, and status documents with a `YYYY-MM-DD--<kind>--<scope>.md` filename.

## END-OF-SESSION
Record session-specific outcomes and the next starting point in a dated `diary/YYYY-MM-DD--type-scope-summary.md` entry, update AK-owned state, run validation, and commit the bounded slice. Do not turn this procedure into a status snapshot.
