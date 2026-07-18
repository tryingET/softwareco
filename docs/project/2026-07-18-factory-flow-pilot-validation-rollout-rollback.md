---
summary: "Validation, rollout, rollback, and recovery plan for Factory Flow pilot 001."
read_when:
  - "Validating, rolling out, stopping, or recovering Decision 62 pilot work."
type: "validation-rollout-rollback"
status: "accepted_post_adr_plan"
date: "2026-07-18"
decision_id: 62
---

# Factory Flow pilot 001 — validation, rollout, and rollback

## Validation principles

- Preservation evidence precedes historical-status mutation.
- Protocol conformance and pilot effectiveness are independent verdicts.
- Owner-native state wins over packet/projection state.
- No physical repository deletion occurs in this pilot.
- Failure is surfaced as `stop`, `continue`, or `redirect`, never hidden by documentary completion.

## Phase gates

### G0 — authority and source identity

Pass when:

- Decision 62 is `adr_recorded / accepted`;
- implementation and this validation plan are attached;
- packet, RFC, decision, proving-lane, and FCOS owner references are current;
- direction/task scope is exact;
- human/CTO-Agent authority split is unchanged.

### G1 — preservation completeness

Pass when:

- refs/tags/branches/stashes/worktrees/submodules/nested repos inventoried;
- reachable/unreachable objects or verified bundle captured;
- NUL-delimited status and tracked binary-safe patch hashed;
- untracked and ignored files hashed;
- type/mode/symlink/size metadata captured;
- all paths classified for owner/security handling;
- `git fsck` or equivalent object validation has no unexplained failure.

### G2 — restoration proof

Pass when a disposable restoration reproduces:

- repository HEAD and refs;
- tracked content and index/worktree state;
- untracked/ignored retained bytes;
- executable bits, file types, and symlink targets;
- manifest hashes.

Any mismatch blocks rollout.

### G3 — bounded status rollout

Pass when:

- only accepted historical-status/docs/projection paths change;
- current FCOS product owner remains unchanged;
- no active dependency breaks;
- source-owner validation passes;
- no secret/private material enters Git;
- physical repository remains available.

### G4 — operator outcome

Pass effectiveness `improved` when an independent operator:

- starts from the AI Society root;
- identifies `holdingco/fcos-control-board` as native FCOS owner;
- identifies `fcos-proving-lane` as preserved historical/non-product evidence;
- completes within ten minutes;
- makes zero wrong-owner claims and zero unsafe mutation attempts;
- cites owner evidence and knows the escalation path.

Retain raw timestamps, consulted paths, errors, escalation, and final answer.

### G5 — closure

Pass when:

- protocol conformance verdict recorded;
- effectiveness verdict recorded;
- overhead and blocked-age evidence recorded;
- mandatory KES learning tracked and attached;
- human terminal decision recorded in AK;
- packet and direction reflect the terminal decision.

## Deterministic checks

At minimum:

```bash
# Softwareco docs and template policy
cd ~/ai-society/softwareco
node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs docs --strict
bash ./scripts/check-template-ci.sh
ak decision passport 62
ak direction export -r "$PWD"

# Source identity and object health
cd ~/ai-society/softwareco/owned/fcos-proving-lane
git status --porcelain=v1 -z | sha256sum
git rev-parse HEAD
git for-each-ref --format='%(refname) %(objectname)'
git stash list
git worktree list --porcelain
git fsck --full --no-reflogs

# Current FCOS owner boundary
cd ~/ai-society/holdingco/fcos-control-board
fcos status --json
```

The post-ADR source-owner task must add exact archive/restore commands before executing them.

## Rollout strategy

1. read-only capture;
2. classification only;
3. disposable restoration;
4. owner-doc historical-status change;
5. active projection correction through owners;
6. independent cold-start test;
7. human terminal decision.

Do not combine phases 1–3 with phase 4 in one irreversible action.

## Rollback families

### Protocol rollback

Trigger: packet ambiguity, overhead breach, or shadow-state behavior.

Action:

- stop using packet as active view;
- retain history;
- reconcile AK/source-owner facts;
- revoke CTO-Agent pilot delegation if directed;
- restore deferred capacity posture.

### Source/release rollback

Trigger: owner-doc/projection changes produce wrong routing or break a dependency.

Action:

- revert only the accepted status/projection commits;
- verify source owner and FCOS routing return to the prior state;
- preserve preservation archive and incident evidence.

### State/data recovery

Trigger: any source byte, object, untracked artifact, or metadata is missing/corrupt.

Action:

- stop mutation immediately;
- restore from verified archive into a disposable path first;
- compare manifest;
- restore source path only under human authorization;
- record recovery time and residual risk.

### Organizational unwind

Trigger: pilot `stop` or `redirect`.

Action:

- close/supersede direction and tasks without deleting history;
- restore/defer task `#3455` posture explicitly;
- route active dependencies through new owner tasks if required;
- revoke pilot delegation;
- notify affected owners;
- retain rationale and learning.

## Commanders and timing

- containment commander: human operator;
- CTO Agent: immediate automation stop and read-only capture authority;
- containment deadline: immediate;
- human decision target after integrity/authority trigger: 30 minutes when available;
- restoration proof budget: four agent hours before explicit continuation;
- blast radius: proving-lane bytes plus external archive only until G2 passes.

## Escape hatch

If no safe classification/restoration path exists, choose `stop`: leave the proving lane unchanged, preserve all gathered evidence, close the pilot honestly, and do not claim factory effectiveness.
