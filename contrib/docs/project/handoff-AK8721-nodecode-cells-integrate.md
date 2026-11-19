---
summary: "Handoff AK8721: reconcile contrib/nodecode and contrib/cells with upstream and put them on contrib.syncMode integrate."
read_when:
  - "You were opened with this file as your first prompt."
type: "handoff"
---

# AK8721: bring contrib/nodecode and contrib/cells back onto upstream, for good

You are a nodecode session opened for exactly one AK task: **8721**. Claim it first
(`ak task claim 8721`), keep evidence in its result JSON, release it when you stop.
The operator asked for this on 2026-11-15 (from AK8700, the nodecode-scope session s-G4OWC333).

## Situation

- `~/ai-society/softwareco/contrib/nodecode`: `main` is **ahead 1, behind 219** of
  `origin/main` (nodecode-ai/nodecode). The one local commit is `5540dc3 fix(local): a gateway
  client refuses :store-path (until nodecode-ai/nodecode#242 lands)`. The checkout is **dirty**:
  `docs/cell-api.mdx`, `nodecode.asd`, `src/cli/entry.lisp` are modified by someone else - find out
  whose (AK, peer sessions, `git stash list`, worktree owners) before touching anything; never
  discard it. 39 local branches; many linked worktrees under `/data/ai-society-scratch/...` belong to
  other tasks (AK8702, AK8657 ...) - leave them alone.
- `~/ai-society/softwareco/contrib/cells`: `main` is **ahead 2, behind 846** (`db091320
  claude-code: subscription-token ...`, `880ac816 openai-codex: discover Pi subscriptions ...`).
- Why they fell behind: the hourly `contrib-all-repos-pull.timer` (script
  `contrib/scripts/pull-all-local-contrib-repos.sh`) ran them in `branch` mode, which only
  fast-forwards; with local commits on `main` it just warned `diverged` every hour.
- Both are now on `contrib.syncMode fetch` (fetch only, never touched) as a holding state.

## The target (already built and tested, use it)

`contrib.syncMode integrate` + `contrib/scripts/contrib-integrate.sh` (tests:
`scripts/test-contrib-integrate.sh` 8/8, `scripts/test-pull-all-local-contrib-repos.sh` 45/45;
commit 6ee6827e7 in the contrib repo). Our integration branch (`main`) is rebuilt every hour as
upstream + the branches listed in the clone's git config `contrib.integration.patch`, in a
throwaway worktree with rerere; it moves only when every merge and `contrib.integration.check`
pass, the tree is clean and no commit would be lost. Read the script's header. CUI already runs
this way (`git -C contrib/CUI config --get-all contrib.integration.patch`).

## What to do

1. Orient (workspace AGENTS working loop): `git log`/`status` in both repos, the peer sessions busy
   there, who owns the dirty files, which local branches are in use and by which AK tasks.
2. **Find what the live nodecode install is built from** (`~/.local/share/nodecode-main/int-*`,
   the current one `int-87acdf4`; its `src/`; the build/install recipe that makes them - search
   nodecode-cells, contrib/nodecode, workstation scripts). The reconciled `main` must still build
   that install, or the recipe must be pointed at the integration branch. Do not install or restart
   the live organism without the operator.
3. For each local commit on `main` and each branch our install or open PRs depend on: is it
   already upstream (merged, or superseded)? Then drop it. Still needed? Then it becomes a patch
   branch on the fork (`tryingET/...`; nodecode has no fork remote yet - add one only if the operator
   approves, else keep local branches), and goes into `contrib.integration.patch` in order.
4. Resolve the conflicts against current upstream once, in a worktree under `$TMPDIR` or
   `/data/ai-society-scratch` (never `/tmp`), so rerere records them. Set
   `contrib.integration.check` to the repo's own fast check (e.g. the declared test recipe), if one
   exists that runs in minutes.
5. Run `contrib/scripts/contrib-integrate.sh --dry-run <repo>`, then for real; then set
   `git config contrib.syncMode integrate`. Prove one timer-equivalent run:
   `contrib/scripts/pull-all-local-contrib-repos.sh --root ~/ai-society/softwareco/contrib --dry-run`
   and a live run limited to the two repos if the script allows, else wait for the next hourly run
   and read its log (`contrib/.logs/github-sync/`).
6. cells is consumed by nodecode (`cells: pin ...` commits upstream); check how our nodecode build
   pins cells and keep the two consistent.

## Boundaries

- Never delete anyone's work: dirty files, stashes, branches, worktrees. Quarantine per workspace
  AGENTS only when the rule allows, recorded in AK.
- No pushes to upstream, no PRs, no installing/restarting the live nodecode: ask the operator
  (multiple choice, with a recommendation).
- Report to the operator: what was dropped as already-upstream, what became patch branches, the
  final `contrib.integration.patch` lists, the integrate run outputs, and anything left open.
