---
summary: "Many-of-the-greats adjudication for AK #5919: the hourly contrib sync timer switches a fork checkout that runs local adoptions (ultimate_bug_scanner, which serves every repo's pre-commit hook) back to upstream main. The script already skips linked worktrees, so the service branch moves into a linked worktree and the primary checkout stays the mirror the timer wants. No new sync mode and no script change are needed."
read_when:
  - "A contrib checkout must run a fork branch (local adoptions) while contrib-all-repos-pull.timer keeps checkouts fresh."
  - "Changing pull-all-local-contrib-repos.sh sync policy, or where ubs-staged.sh finds the scanner."
type: adjudication
task_id: 5919
---

# QUESTION

`contrib-all-repos-pull.timer` runs `pull-all-local-contrib-repos.sh` hourly.
With `contrib.syncMode=branch`, each run checks out upstream `main` in the
clean `ultimate_bug_scanner` checkout (log: `policy=branch; default=main:checked-out`).
That checkout is the scanner behind every repo's pre-commit hook, and it is
meant to run `local` (upstream plus local adoptions). Between 2026-09-23 22:12
and 2026-09-25 the hooks ran plain upstream. How should freshness and the
fork branch coexist?

# MODE 1 — The strongest schools

**One source of truth per place (Unix, Pike: make each program do one thing).**
A directory is one thing. A checkout that is both "mirror of upstream" and
"the fork we run" has two owners and will be fought over by whichever
automation runs last.

**Policy as configuration (the sync script's own design).** Owner-local
`contrib.syncMode` already selects behaviour per repo. Add a third value
(`fork-local`: fetch, fast-forward mirror branches, never move HEAD) and
the conflict disappears where it arises.

**Structure over policy (Parnas, information hiding; "make illegal states
unrepresentable").** Do not teach every automation about every branch model.
Arrange the filesystem so that no automation can reach the thing it must not
touch.

**Operational humility (Gall's law; Chesterton's fence).** The timer, its
`branch|release` policy work (uncommitted, another session's) and the hook
wrapper all exist for reasons not visible here. The smallest change that
removes the collision without editing someone else's in-flight code wins.

# MODE 2 — Confrontation

**Policy-as-config vs structure.** A new sync mode works, but it has to land
in a file that carries another session's uncommitted `syncMode` work. It
also requires every future automation (self-update, `doctor --fix`, the review
gate's ff-only pull) to honour the mode. Structure needs no cooperation. The
corpus decides it: the script already skips linked worktrees (`SKIP
pi-sub-maintained linked worktree` in every run log), and `pi-sub-maintained`
already runs a fork branch this way.

**One-thing vs policy-as-config.** Aligned once structure wins: the primary
checkout becomes only the mirror (the timer's `policy=branch` is then
correct, not hostile), and the linked worktree is only the service.

**Humility vs structure.** Structure is the humble option here. It changes
one default path in `ubs-staged.sh` (ours) and adds a worktree. The timer, the
sync script and its uncommitted work stay untouched.

**Residual tension.** A linked worktree shares the object store. A `git gc` or
`worktree prune` in the primary is safe, because live worktrees are protected.
But deleting the directory by hand would silently fall back to the mirror. The
fallback must be visible, not silent.

# MODE 3 — Decision

**True synthesis: the mirror lives in the primary checkout, the service lives in
a linked worktree, and the hook prefers the service while naming its fallback.**

- `contrib/ultimate_bug_scanner` stays on `main` and follows upstream. The
  timer's existing `policy=branch` does exactly that.
- `contrib/ultimate_bug_scanner-local` is a linked worktree on `local`, which
  the timer skips. The hooks run it.
- `scripts/ubs-staged.sh` defaults to the service worktree's `ubs` when it
  exists and falls back to the primary checkout with a one-line notice.
  `UBS_BIN` still overrides both.
- A `fork-local` sync mode is not needed. AK #5919 closes on this design; add
  the mode later only if a second repo needs one and cannot use a worktree.

# PRACTICAL CONSEQUENCE

1. Create `contrib/ultimate_bug_scanner-local` on branch `local`, rebased onto
   current upstream. The ctcompare adoption is dropped because upstream
   a735fc11 supersedes it.
2. Change `ubs-staged.sh`'s default scanner path, test-first (Given/When/Then),
   and verify that a timer run leaves the service worktree untouched.
3. Record in the contrib-upstream skill's UBS recipe that the service is the
   linked worktree and the primary checkout is the mirror.
