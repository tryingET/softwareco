---
summary: "AK5528/5421: stop scheduled release sync from rolling back pi-sub-maintained."
read_when:
  - "Investigating the September 5/7 pi-sub-maintained rollback or recovery evidence."
type: "implementation"
---

# Linked-worktree sync refusal and preserved pi-sub recovery

The operator requested a progress-preserving investigation, then explicitly chose
backup, linked-worktree exclusion, regression tests, maintained-branch restoration
and provider-free loading verification. Canonical investigation task: AK5421 in
pi-extensions; source-owner task: AK5528 in contrib.

## Cause and bounded fix

The scheduled contrib updater selected marckrenn origin's v1.5.0 release after
fetching both origin and maintained remotes, then detached the clean maintained
worktree. Reflog and two updater logs correlate; September 7 also has service-journal
attribution. No corresponding causative Pi/Claude tool call was observed in the
inspected time windows. Notification-only pi-little-helpers and Pi local-path package
handling are not supported as the cause.

Changed only the worker eligibility guard/help in
`scripts/pull-all-local-contrib-repos.sh`, added its fixture tests and the
[runbook](../docs/project/contrib-sync-worktree-safety.md). Linked Git/common dirs
differ: SKIP before fetch/release/checkout. Unknown topology: FAIL without worker
mutation. Ordinary clones, including standalone separate-git-dir clones, retain
existing behavior. No global timer disable or remote changes.

## Preservation and recovery proof

- Verified 4.1 MiB preservation capture: complete Git bundle including all refs and
  16 worktree HEADs; binary staged/unstaged patches and untracked archives. Durable
  private copy: `~/.local/state/pi-recovery/pi-sub-preserve-5421.IVKqR9`.
- Dirty work in primary pi-sub and pi-pr-5437 was captured and left unchanged.
- Independent guard review approved the patch, required explicit writer and
  hook/filter checks; parent completed those before recovery.
- Held the existing sync lock across guard application, applied-source tests,
  clean-target/expected-ref checks, ordinary `git switch` and postchecks.
- Restored existing `local/maintained-provider-stack` at
  `908cda097e30c753f56647bc53c6e2cd25db9511` (seven commits ahead of maintained/main).
- All shared refs, other 15 worktree HEADs/statuses/patches/untracked archives stayed
  unchanged. Target is clean. Lock explicitly released; timer remains active.
- No dependency install: existing links resolve the restored @eiei114 namespace.

## Validation

- Bash syntax + ShellCheck pass.
- Applied updater: 26 fixture cases pass, including original-source negative
  reproduction. Evidence: `$TMPDIR/ak5528-updater.TQQaV6mM/applied-tests.log`.
- Fresh installed Pi 0.84.4 SDK loaded both maintained extension factories in a
  network-isolated, empty-HOME process: no load errors; correct three commands,
  handlers/subscriptions/shortcuts registered. No session_start/provider/UI actions.
  Syscall trace observed no network, credential-path access or executable children.
  Source hashes/HEAD/status unchanged. Evidence: `$TMPDIR/pi-sub-load-proof.3ay7Zd`.
- This is registration proof, not a full live-provider/full-upstream-suite result.
  Full contrib CI mutates unrelated ontology/projections and was not run for this
  scoped source repair. No validation bypass is claimed.

No user files were reset/cleaned/stashed/deleted. Backup excludes ignored artifacts
such as node_modules from its source-change inventory; those were not reinstalled,
cleaned or intentionally modified. The recovery does not prove a universal defense
against arbitrary external Git writers; it closes the evidenced scheduled path.
