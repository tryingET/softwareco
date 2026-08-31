---
summary: "Validation, rollout, stop, and rollback contract for a future Softwareco ontology topology adoption."
read_when:
  - "Reviewing implementation readiness for the Softwareco ontology topology decision."
  - "Planning an ontology projection refresh, checkout relocation, gitlink adoption, or receipt relocation."
type: "plan"
status: "proposed"
date: "2026-08-31"
governance_task_id: 5228
---

# Softwareco ontology topology — validation, rollout, and rollback

## Current posture

The decision packet is proposal-only. No `ontology/**` path may be staged or normalized until:

1. the architecture decision is created and passes governed review;
2. an ADR records the accepted outcome;
3. implementation and validation/rollback artifacts are registered;
4. affected tasks are re-evaluated and exact post-ADR tasks are claimed.

The current 31 ontology worktree entries are held evidence of unresolved topology, not a cleanup
queue.

## Pre-implementation evidence gate

Re-read, do not replay, all live inputs:

- Softwareco parent commit and worktree/index status;
- ontology owner commit, tree, clean status, branches, remotes, and live publication containment;
- parent and owner tracked-path sets, common/owner-only/parent-only sets, byte and mode differences;
- AK `4960`, `4962`, and `4973` scopes/results/evidence;
- architecture decision passport, accepted ADR, linked implementation plan, and task scopes;
- stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` reachability and unchanged identity;
- parent-generated receipt paths and their protected core-layer binding;
- every ordinary owner command that can write/delete `dist` or another parent-owned path;
- measured parent/template/CI consumers for complete versus selective projection;
- accepted physical membrane: receipt relocation, checkout separation, gitlink materialization, or
  enforceable owner-operation isolation;
- unrelated parent WIP fingerprints and local full-ref safety bundles.

Any drift requires a new plan and, when it changes the selected tradeoff, decision re-evaluation.

## Candidate test matrix

| Case | Expected result |
|---|---|
| Owner worktree/index dirty | Stop before plan |
| Selected source commit not on authorized live remote ref | Stop before plan |
| Source path is symlink, case-colliding, or escapes destination | Stop before apply |
| Path absent from ownership manifest | Stop as unclassified |
| Parent projected path differs from source without a plan entry | Stop |
| Parent-generated `dist/**` path appears in source copy/delete set | Stop |
| Canonical owner build/validate changes a parent-owned path while owner status stays clean | Reject candidate topology |
| Receipt relocation leaves a stale consumer/path/repo binding | Stop |
| Checkout relocation leaves stale AK/tool/operator path authority | Stop |
| Fresh checkout depends on ambient nested `.git` state | Stop |
| `.git/**`, stash, ignored file, or untracked owner file appears in plan | Stop |
| Plan hash/source commit changes between review and apply | Stop |
| Exact projected bytes/modes equal source; generated class preserved | Continue to gates |
| Owner or parent strict gate fails | Do not commit |
| Staged set differs from exact task/plan scope | Do not commit |
| Unrelated WIP fingerprint changes | Do not commit |
| Post-commit bundle verification fails | Do not close task |

## Required validation

### Source-owner and physical-membrane validation

First run owner validation from an isolated clean worktree at the selected source commit:

```bash
./scripts/ci/full.sh
```

Then exercise the accepted topology's ordinary canonical owner path and command surface. The test
must prove owner build/validate cannot delete, replace, or conceal a parent-owned receipt/output. A
candidate that passes only because validation avoided the canonical co-location is insufficient.

Use the owner-declared strict ROCS workspace/profile contract. Verify publication against the remote
selected by the accepted decision; do not silently fall back from an unavailable remote. If the
outcome relocates the owner checkout, also prove AK repo binding, operator commands, workspace refs,
branches, remotes, stashes, and fresh materialization at the new path. If it relocates receipts,
prove every old consumer fails or redirects deterministically and every new receipt identity/path is
correct.

### Outcome-specific parent validation

When the outcome includes a complete or selective projection, a deterministic checker must prove:

- source commit/tree and remote evidence match the plan;
- source tracked paths and measured consumers justify the projected ownership class;
- every projected byte and mode equals source Git;
- every parent-only path belongs to a physically safe generated class;
- no extra/unclassified `ontology/**` path exists;
- `.git/**` and stash/local-ref content is absent from the parent index;
- state/receipt hashes match the active manifest and plan.

For a gitlink/submodule outcome, instead prove exact mode/OID, authorized materialization metadata,
fresh-checkout behavior, receipt relocation, and no source bytes tracked beneath the pointer. For a
physically separated owner checkout, prove the parent projection contains no owner Git metadata and
that ordinary owner operations at the new path leave the parent unchanged.

### Parent integration gates

Run from a clean isolated Softwareco worktree/strict overlay:

```bash
./scripts/preflight-repo-census.sh
./scripts/ci/smoke.sh
./scripts/check-template-ci.sh
./scripts/ci/full.sh --deep
git diff --check
```

The overlay must resolve the protected ontology-kernel commit required by current parent policy.
Generated ROCS output from validation must remain confined to scratch or be included only when the
accepted plan classifies it as a parent-owned output update.

### Preservation checks

- owner worktree/index remains clean;
- stash `c66f2e0…` remains reachable, unchanged, and un-applied;
- unrelated fork and other operator WIP remains byte-identical;
- parent index contains only task-scoped plan paths;
- parent retains exact L1 candidate ancestry required by AK `5197`;
- Healthco and all L2 repositories remain untouched.

## Rollout sequence

```text
commit decision packet
-> create AK architecture decision
-> independent authority + operations review
-> review synthesis and legal closure
-> record accepted ADR, implementation plan, and validation/rollback artifacts
-> re-evaluate/link exact implementation tasks
-> capture fresh full-ref owner and parent bundles
-> observe live source/remote/census
-> add missing consumer and ordinary-owner-operation measurements
-> select one physically safe outcome through review closure
-> generate and review an outcome-specific deterministic plan
-> apply the selected topology in isolated candidate context
-> run physical-membrane, source-owner, materialization, and parent gates
-> independently review candidate
-> commit one bounded parent adoption
-> record receipt + AK evidence
-> verify both owner and parent clean
-> only then return to AK 5197 canonical finalization
```

## Stop conditions

Stop and do not force, clean, stash, or retry mechanically on:

- missing or non-accepted architecture authority;
- ambiguous source remote or source commit;
- owner/stash/ref drift;
- path-count or ownership-classification drift;
- destination symlink/escape/case collision;
- parent-generated receipt path in a source deletion/replacement set without explicit ADR scope;
- ordinary canonical owner validation mutating parent-owned bytes invisibly;
- missing consumer census or unsupported “least disruptive” claim;
- receipt relocation or checkout relocation without complete path/authority migration proof;
- unexpected staged path;
- any failed source or parent gate;
- any mutation of unrelated WIP;
- missing post-commit reachability/bundle proof;
- a plan that relies on popping/dropping `c66f2e0…`;
- a proposal to treat copied bytes as new semantic authority.

## Rollback

### Before decision acceptance

Revert only proposal/review docs and AK proposal records through their owning workflows. Leave all
ontology worktree bytes, owner history, and stash state unchanged.

### After acceptance, before implementation commit

Discard only an isolated candidate worktree and plan artifact. Do not reset or clean the canonical
parent or owner worktrees. Preserve accepted decision history and record why implementation stopped.

### After topology adoption commit

Use a new exact rollback task and revert the bounded adoption commits in the accepted owner order.
The rollback must restore the prior parent projection/receipt paths and, when relocation occurred,
the prior owner/AK/tool path contract without losing Git objects, remote refs, stashes, or local
branches. Re-run physical-membrane, materialization, source, and parent gates; create new verified
bundles for every repository changed.

If the adopted contract has already produced downstream consumers, do not rewrite parent history or
force remote refs. Use a successor decision when rollback changes the architecture or receipt path.

## Success criteria

The rollout succeeds only when:

- one accepted decision and ADR name the topology and owners;
- the selected topology and every source/generated class are complete and machine-checked;
- any projection refresh or gitlink/relocation adoption is commit-bound, plan-first, and receipted;
- ordinary owner operation cannot invisibly mutate parent-owned bytes;
- owner and parent worktrees are independently truthful and clean;
- owner publication and source commit are verified;
- stash `c66f2e0…` and unrelated WIP are preserved;
- strict owner and parent gates pass;
- AK evidence records observed behavior without replacing Git/ROCS/decision authority.

A clean Softwareco worktree then unblocks the path-bound AK `5197` finalizer; it does not by itself
complete that task.
