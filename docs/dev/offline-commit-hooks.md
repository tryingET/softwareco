---
summary: "AK7597: qualified, explicit offline candidate-index UBS/native hooks for Softwareco and the four dep-* consumers; targeted Git-metadata installation and refusal rules."
read_when:
  - "Installing the offline hook chain in Softwareco or dep-viz/dep-diet/dep-surgeon/dep-redteam."
  - "A linked worktree's relative .git/ubs-chain-hooks path fails to execute required checks."
type: reference
---

# Offline candidate-index commit hooks

AK7597 owns the shared implementation in `local/hooks/`; native consumer owners
own their `scripts/ci/smoke.sh`, `.githooks/pre-commit`, and native tests. The
company-local location follows [L1 extension ownership](l1-local-extensions.md).
This is not a fleet rollout, hook exemption, or security clearance.

## What executes

1. The generated Git pre-commit runs the runner as `python3 -I` (isolated: `PYTHON*`
   variables and the runner's own directory cannot inject modules). The runner refuses
   an unisolated interpreter, but an entry hook generated before this rule still
   imports modules before that check, so after any source change **reinstall every
   consumer immediately** (a stale entry hook then refuses at the `-I` check, unless an
   inherited `PYTHONPATH` hijacks an import first). The runner then pins
   `PATH=/usr/bin:/bin` and `GIT_NO_REPLACE_OBJECTS=1` for itself and everything it
   starts. Its own Git calls on the committing repository get the environment
   allowlist below plus only the Git location variables (`GIT_DIR`, `GIT_WORK_TREE`,
   `GIT_INDEX_FILE`, `GIT_COMMON_DIR`, object directories, `GIT_NAMESPACE`, discovery
   limits), ignore global and system configuration (`GIT_CONFIG_GLOBAL=/dev/null`,
   `GIT_CONFIG_NOSYSTEM=1`), and run with `-c core.fsmonitor=false`. So committer
   configuration (`GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`, `GIT_EXEC_PATH`,
   `~/.gitconfig`, including config-defined hooks such as `post-index-change`) cannot
   run commands during the index reads. The repository's own `.git/config` remains a
   trusted boundary, like its hooks configuration. It resolves the actual worktree through Git and
   verifies installed source hashes and the real UBS service executable hash. The
   network-namespace re-exec keeps `-I`.
   Relative index selection follows Git's repository context, not a path inferred
   by concatenating the shell cwd. Tests compare the captured tree against Git's
   original-context `write-tree`, including explicit Git directory/worktree bindings.
2. Linux `unshare --user --map-current-user --net` creates an externally isolated
   network namespace. Unavailable isolation is a refusal, not a network fallback.
3. A private byte copy of the actual commit index (including `GIT_INDEX_FILE`)
   produces an immutable tree. The originating index is not rewritten. Missing
   objects, unmerged entries, or unsupported Git `--no-lazy-fetch` fail closed.
4. The tree is materialized as literal blobs, modes and symlinks in a new scratch
   standalone Git repository. No smudge, EOL, export-ignore or checkout filters
   transform it. Its HEAD is the originating HEAD and its index is the candidate
   tree. Source objects are referenced through alternates, not fetched or cloned.
   UBS and the native checks receive an **environment allowlist** only: the pinned
   `PATH`, `HOME`, `TMPDIR`, `USER`, `LOGNAME`, `LANG`, `LANGUAGE`, `LC_*`, `TERM`,
   `TZ`, plus the explicit offline settings (including `UBS_NO_CACHE=1`), and
   `UBS_STAGED_STRICT=1` when the committer sets it (tighten-only). Everything else
   is dropped, including `GIT_*`, `UBS_*` (for example `UBS_SKIP_CATEGORIES`),
   `BASH_ENV`/`ENV`, `PYTHON*`, `NODE_OPTIONS`, agent sockets and CI knobs: before
   this, an inherited `BASH_ENV` or `UBS_SKIP_CATEGORIES` could make the real scanner
   pass a critical finding, and a caller `PATH` could supply UBS language modules
   (AK7597 inspections, 2026-11-01/02). Tools the checks need must therefore live in
   `/usr/bin` or `/bin`. No origin index, ref, or worktree is used as the native
   context; replacement refs cannot substitute candidate bytes.
5. The real `scripts/ubs-staged.sh` runs **first in that snapshot**, using the real
   service scanner. Thus both source bytes and `.ubsignore` come from the index.
   When the staged scan fails, the wrapper may compare per-file critical counts with
   HEAD's versions only if the staged rescan is complete (exit 0/1, `status` ok, no
   failed module) and itself shows a critical finding; otherwise it keeps the
   whole-file refusal (inspection D2). Both rescans name the checkout's own scan policy
   (`--config=<checkout>/.ubs.json`, else `--no-config`), so a `.ubs.json` of a
   repository enclosing `TMPDIR` cannot apply. Known residual: the comparison counts
   criticals only, so under a project policy that fails on warnings a new warning in
   a file that already has criticals can still pass.
6. Native-v1 verifies both indexed native entrypoint and smoke hashes and runs:

   ```text
   .githooks/pre-commit --base-ref <resolved-local-merge-base-commit>
   ```

   Its owner-qualified entrypoint forwards arguments:

   ```sh
   exec "$repo_root/scripts/ci/smoke.sh" --offline --index "$@"
   ```

   Native smoke preserves its own checks, including protected paths compared
   **base → candidate index**, indexed executable control files, and any indexed
   documentation-link checks. It must not attempt a fetch, including Git lazy
   fetching. Namespace denial alone is not proof that native code makes no attempt.
7. Original HEAD and index bytes/tree are compared after UBS and after native
   checks. Drift refuses the commit. Native failure never becomes a fallback pass.

Softwareco mode is deliberately different: its known template entrypoint and
UBS-only local addition are checked against their original hashes; the same real
UBS gate runs first, then a root-owned **base → candidate-tree `docs/_core`
protection check** (including gitlinks hidden by indexed ignore settings, with
external diff/textconv disabled), then **indexed `scripts/ci/smoke.sh`**, including
company tests. It does not claim a separately pinned native-v1 smoke implementation. Unknown
changes to either root entry contract require owner qualification.

This pre-commit does not replace full CI, tests, lint, schema checks, or real
consumer verification. Record those results and any unrun checks separately. No
package acquisition, deployment, external push, or task completion is granted.

## Targeted installation

First qualify the shared source and independently inspect each consumer's native
source. Obtain the exact **indexed** smoke and pre-commit SHA-256 from that owner.
Do not substitute a hash of dirty working-tree content. Use a retained, committed
shared source location; the installer binds absolute source paths and their hashes.

```sh
SHARED=/home/tryinget/ai-society/softwareco
TARGET=/absolute/path/to/the/authorized/repo-or-linked-worktree
python3 "$SHARED/local/hooks/install_offline.py" \
  --repo "$TARGET" --mode native-v1 --base-ref refs/heads/main \
  --native-sha256 <qualified-indexed-smoke-sha256> \
  --native-hook-sha256 <qualified-indexed-pre-commit-sha256>
```

For the explicitly authorized Softwareco source adoption only, use
`--mode softwareco` instead of the two native hash arguments.

Before installation, each native entry must be an exact stage-0 executable,
nonempty, actually readable **blob object**. Mode-derived type labels and tree
listings are not proof; full object reads must complete successfully.

Installation is limited to Softwareco and the four named dep-* repositories. It
writes only the target's Git metadata and an absolute common-directory
`core.hooksPath`, so `.git` **files** in linked worktrees work. After activation, Git's own
hook resolution is checked for every live worktree **and every administrative worktree
directory**, including ones Git lists as prunable (a moved checkout), so overrides via
`config.worktree`, `include.path`/`includeIf` or a masked `extensions.worktreeConfig`
are refused; a refusal restores the prior `core.hooksPath` first. Installing twice
with identical inputs preserves generated bytes and mtimes. All listed worktrees'
Git hook discovery is checked. Conflicting worktree-specific overrides, unknown
hooks, missing native entries, scanner/source drift, or unavailable local bases
require explicit owner disposition—not a bypass. Recognized legacy pre-push
symlinks are preserved by a worktree-resolving delegate, not a canonical-path call.

The installer prints source/scanner/native hashes and configuration identity.
Keep that receipt outside the checkout. Then, from the target with its intended
candidate staged, run the **actual Git-discovered hook**:

```sh
git -C "$TARGET" hook run pre-commit
```

This runs real UBS plus native checks. It is not permission to install missing
scanner dependencies or ignore a partial scan. Commit only through the ordinary
Git command after all required checks and the independent inspection pass.

## Verification and rollback

`tests/test_offline_hooks.py` separates synthetic transport fixtures from real
service-scanner checks. Its synthetic executables never install into actual
consumer metadata. It covers standalone/linked worktrees, Git-discovered execution,
old-hook/override refusal, argument forwarding, pre-push preservation, index versus
HEAD/worktree content and ignore rules, literal export, index-byte preservation,
namespace isolation, missing promisor objects, and drift/refusal ordering.

Before adoption, retain the prior local hooks configuration and hook files. The
installer leaves old hook files intact. Rollback needs an owner-approved source
and configuration plan that still executes required checks; do not blindly restore
an old broken relative path in a linked worktree or use `--no-verify`. Reverting a
source commit is not proof of rollback compatibility: rerun the required checks.

Source/scanner changes invalidate installed hashes. Requalify and rerun the
idempotent installer from the intended stable source; never edit generated hashes
by hand to manufacture acceptance.
