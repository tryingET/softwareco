# UBS branch policy and archived worktree retirement — AK5807/5808

## Root cause and bounded repair

The hourly `contrib-all-repos-pull.timer` used the updater's global release-first policy. Git reflog and scheduled logs show UBS switched to main and fast-forwarded on September18, then the timer checked out v5.4.7/v5.4.8/v5.4.9 in detached HEAD. This was updater policy, not recurrence of the old local-main divergence.

Added owner-local `git config --local contrib.syncMode branch` support to `scripts/pull-all-local-contrib-repos.sh`. It skips GitHub release lookup and follows the existing origin-default-branch clean-tree/fast-forward guards. Unset/explicit `release` retains release-first behavior for other repos. Linked worktrees remain skipped. Invalid, duplicate, empty and newline-bearing local values fail closed before fetch; global policy is not consulted.

UBS local config is now `contrib.syncMode=branch`. Two actual UBS-only executions of the unchanged extracted worker returned `policy=branch`, first fast-forwarding main to `862357b201f60b859caa271c56bd1894dd7d5fd2`, then reporting main current. Primary is clean and attached; no scanner edits, installation, push, tags or feature ports.

## Validation

- Original updater: new branch-policy regression RED (release lookup attempted).
- Reviewer found Bash newline trimming could admit a valid value followed by an empty value. Additional regression RED; sentinel-based parsing fixed it.
- Final isolated local-Git/fake-gh suite: **39 PASS**. Includes default/explicit release, branch repeat runs, clean/detached/dirty/diverged, invalid/duplicate/newline policies, topology failures and linked-worktree no-mutation checks.
- Bash syntax, ShellCheck, scoped diff whitespace and owner smoke PASS.
- Declared `scripts/ci/full.sh` PASS in an isolated copy with current owner inputs and `ROCS_WORKSPACE_ROOT=/home/tryinget/ai-society`: ROCS validation and relay/evidence-index tests. First attempt lacking workspace-root failed dependency resolution; retained, not counted green.
- Independent code review: `dispatch-1789832677419`, approved after correction.

## Worktree custody and authorized retirement

The earlier cleanup session confirmed it removed only eight separately approved worktrees. The remaining candidates were not newly recreated by this repair. The current controller acknowledged a no-mutation hold and no active worker/heavy job before custody capture.

Durable private archive (not scratch):

`/home/tryinget/.local/state/ubs-recovery/2026-09-19-AK5808.h5BmUP/`

Contains all 19 original directory trees (primary plus 18 linked), including ignored/untracked files, shared Git objects/refs/reflogs, per-worktree indexes, exact manifests, path mapping, and a relocated recovery proof. Independent reviewer `dispatch-1789833078420` verified **21,393 entries /17,303 files**, all19 HEAD/status/index identities,227 user refs and restoration with originals hidden. No content promotion or historical task acceptance inferred.

Operator explicitly authorized the exact `bash .../retire-approved.sh` command and then confirmed its restated scope. Verbatim responses, exact script/hash and timestamps are in `operator-authorization.md` and `retirement.log`. Execution at **2026-09-19T18:02:12–18:02:15+02:00** removed only eighteen inventory-listed linked worktrees using `git worktree remove --force`; all source bytes had passed fresh drift checks. Primary, branch refs, archive, and sibling evidence directories were preserved. The exact unowned zero-byte index lock was renamed into the archive, not deleted.

Post-retirement independent readback: **one registered worktree**, clean main equals fetched origin/main, all18 originals absent, raw manifests/indexes unchanged. All10 prior local branch names remain; nine tips unchanged and main advanced by fast-forward. Deferred AK tasks were not cancelled or completed by this operation.

## Bounded limitations

- Ordinary Git fsck finds a pre-existing stale commit-graph cache (same102 missing cached commit references in live and restored copies). Actual Git object checks PASS with `core.commitGraph=false`. Cache bytes and diagnostics retained; no claim that missing historical objects were recovered or cache repaired.
- A raw orphan index.lock is retained as evidence; the validated read-only restore bypasses it via `GIT_OPTIONAL_LOCKS=0`. README explains writable-copy handling. Historical failed restore attempts remain retained.
- Process checks found no accessible same-user worktree users; seven protected desktop/service processes and other-UID internals are not exhaustively visible. Known-owner hold supplements that bounded check.
- Archive is same-filesystem, not off-device disaster recovery. It covers registered worktree directories, not every unrelated or sibling scratch artifact.
- Installed `~/.local/bin/ubs`, old branches, issue-tracker remote-state reconciliation and thirteen existing task deferrals are outside this two-operation change.
