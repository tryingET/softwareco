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

1. The generated Git pre-commit resolves the actual worktree through Git, then
   verifies installed source hashes and the real UBS service executable hash.
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
   Originating `GIT_*` variables are cleared; explicit offline settings are then
   restored. No origin index, ref, or worktree is used as the native context.
5. The real `scripts/ubs-staged.sh` runs **first in that snapshot**, using the real
   service scanner. Thus both source bytes and `.ubsignore` come from the index.
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
`core.hooksPath`, so `.git` **files** in linked worktrees work. Installing twice
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
