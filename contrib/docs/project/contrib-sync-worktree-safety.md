---
summary: "Why contrib sync skips linked worktrees, with safe pi-sub recovery evidence."
read_when:
  - "Changing automatic contrib synchronization or recovering maintained worktree drift."
type: "reference"
---

# Contrib sync and linked worktrees

## Rule

`scripts/pull-all-local-contrib-repos.sh` skips linked worktrees before the worker
performs a fetch, release lookup, checkout, merge, or dry-run eligibility report.
It compares Git's absolute `--git-dir` and `--git-common-dir` values. Different
directories mean a linked worktree. Missing/failed metadata produces a `FAIL`
record without worker mutation; `--strict` makes those failures exit nonzero.
A standalone clone with `--separate-git-dir` remains eligible because the two
directories coincide. This is not a blanket refusal of all `.git` files.

Ordinary clones retain the existing release-first/default-branch behavior. The
root updater still performs its existing authentication setup, logging and locking
before invoking workers. Therefore whole-script `--dry-run` is not a side-effect-free
probe of user configuration. Do not run it against a live root merely to test this
worker guard.

A primary clone can still fetch shared remote refs/tags. Skipping a linked
worktree is not a complete shared-repository write lock or an independent clone.
The normal configured fetch refspecs update remote-tracking refs, not the local
maintained branch. Future changes to those refspecs need separate review.

## Incident: maintained pi-sub reverted to marckrenn v1.5.0

The updater discovered `pi-sub-maintained` through its `.git` file, fetched origin
and the maintained upstream, then selected the latest stable release from **origin**.
The linked worktree shares configuration with `pi-sub`: origin is marckrenn, while
`local/maintained-provider-stack` tracks `maintained/main` from eiei114.
A clean worktree was treated as safe to replace with the origin release, regardless
of newer committed local development. Clean does not mean disposable.

Evidence:

- `pi-sub/.git/worktrees/pi-sub-maintained/logs/HEAD` records checkout to
  `refs/tags/v1.5.0` on September 5 at 15:09:32 and September 7 at 13:06:21
  (UTC+02:00).
- `.logs/github-sync/all-repos-20260905-150959.log:184` and
  `.logs/github-sync/all-repos-20260907-130648.log:184` both report
  `pi-sub-maintained ... release=v1.5.0:checked-out`.
- The September 7 service journal brackets the invocation at 13:05:02–13:06:48.
  The updater is called by the enabled `contrib-all-repos-pull.service`/timer.
  The September 5 launcher identity was not independently recovered.
- Pi settings contain local core/bar paths; Pi's local-path package handling and
  pi-little-helpers' notification checks do not explain these checkouts.

The old source imported `@marckrenn/pi-sub-shared`, while installed workspace links
still used `@eiei114/pi-sub-shared`, producing the loader errors. Installing the
old missing namespace would have masked the rollback, not restored maintained work.

## Recovery performed on 2026-09-07

Authorized under AK5421 and contrib-owned companion AK5528:

1. Backed up all refs and all 16 worktree HEADs in a verified Git bundle. Captured
   reflogs, each worktree's staged/unstaged binary patches, status and untracked
   archives where present. The primary checkout and one other worktree had dirty
   progress; neither was changed.
2. Checked the service was inactive, no exact updater script invocation was
   observed, checkout hooks/custom filters were absent, and fetch refspecs were
   ordinary remote-tracking mappings. These checks are evidence, not a universal
   claim that arbitrary external writers cannot exist.
3. Held the updater's existing `.locks/git-pull-all.lock` across applying the tested
   guard, fresh state verification, branch restoration and postchecks. Released
   the lock afterward. No timer or service configuration was changed.
4. Switched the clean, detached target from
   `65deb56853b924fbbcee1b77e09c71f5f08fc9a2` to the existing
   `local/maintained-provider-stack` branch at
   `908cda097e30c753f56647bc53c6e2cd25db9511`.
5. Verified target branch/HEAD/cleanliness, unchanged shared refs, and unchanged
   other 15 worktree HEADs, statuses, binary patches and archived untracked files.
6. Verified all three manifests identify `@eiei114/pi-sub-*` version 2.2.3, and
   both core/bar resolve the existing shared dependency. No npm install occurred.

No reset, clean, stash, cherry-pick, rebase, remote change, ref reconstruction,
provider call, or deletion of user progress was part of recovery.

Private preservation copy (not committed):
`~/.local/state/pi-recovery/pi-sub-preserve-5421.IVKqR9/`.
The bundle verifies as complete; its SHA-256 is
`339134b51a400c3ce89e2c79e322cf0a27f3aae17d5348916ad7365aae4c322f`.
Patches/untracked archives can contain private work; keep the directory private.
The SHA manifest records original capture paths; the durable copy contains the
same bundle and capture artifacts.

## Validation

```bash
bash -n scripts/pull-all-local-contrib-repos.sh scripts/test-pull-all-local-contrib-repos.sh
shellcheck scripts/pull-all-local-contrib-repos.sh scripts/test-pull-all-local-contrib-repos.sh
bash scripts/test-pull-all-local-contrib-repos.sh
```

The default suite has 25 cases using isolated HOME/Git config, real disposable Git
repositories and worktrees, file-only Git transport and fake GitHub responses.
Passing the original updater as a second argument adds a 26th baseline-regression
case proving the original moves a clean linked HEAD to an older release.
The applied source passed all 26 cases. Coverage includes clean/dirty/detached
worktrees, include-root/dry-run, malformed topology, ordinary clones, standalone
separate Git directories, and existing upstream/default-branch behavior.

Fresh installed Pi 0.84.4 SDK loading also passed under `env -i` and
`bwrap --unshare-all`, with an empty HOME and read-only source mounts. Both extension
factories loaded with no errors, registering `/sub-core:settings`,
`/sub-bar:settings`, `/sub-bar:import`, lifecycle handlers and bus subscriptions.
A syscall trace showed no network calls, credential-path access or child executable
launches during the probe. It did not start a Pi session, run lifecycle startup,
execute UI commands or contact providers. Normal startup may probe providers and
bar loading with real historical settings may migrate settings; neither was tested.
No full upstream suite or root ontology-mutating CI run is claimed.

## Future recovery precautions

Do not blindly replay an old SHA/branch switch. Inspect current refs, all relevant
worktrees, dirty/ignored state, hooks/filters, active writers and updater ownership.
Preserve current progress first. Stop on drift; never use force checkout, reset,
clean or a dependency reinstall to suppress the symptom. If another writer can
change topology or refs concurrently, coordinate quiescence before recovery.
