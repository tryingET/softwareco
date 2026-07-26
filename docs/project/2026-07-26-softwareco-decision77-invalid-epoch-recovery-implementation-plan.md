---
summary: "Post-acceptance implementation plan for Decision 79's one-time invalid epoch quarantine."
read_when:
  - "Implementing accepted Decision 79."
type: "plan"
status: "active"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
governance_task_id: 4226
---

# Decision 79 implementation plan

## Preconditions

Direct-human receipt `8973` accepted Decision 79; AK is `unblocked`; task `4226` is re-evaluated `still_valid`; controller deferral `182`, task `4220` entity version `1`, and Decision 74 terminal proof remain required. Checker implementation is authorized. Invalidation still requires its separate exact human receipt.

## Slice 1 — Immutable zero-operation evidence

Fresh-read receipt `8967`, task/deferral `4220`, tasks `4221`/`4226`, Decision-77 direction, task evidence, epoch/governance concerns, worktree, and UTC. Record bounded `softwareco.decision77-invalid-epoch-zero-operation.v1` evidence on task `4226` with command/output hashes and explicit coverage limits.

## Slice 2 — Checker implementation

Add the accepted Decision-79 membrane, overflow-safe predecessor graph, preserved authorization/handback/revocation/terminal branches, exact invalidation branch, identity retirement, live task/deferral checks, and immutable evidence checks. Add mutation-free fixture self-tests. Keep every Decision-77 production mode fail-closed before invalidation.

## Slice 3 — Human invalidation

Prepare one exact direct-human command with pinned Decision-79 acceptance and zero-operation evidence IDs. Pause for human execution. Fresh-read the receipt; never infer it from stdout. Verify inactive framework and negative active mode.

## Slice 4 — Amendment closeout

Record implementation evidence, complete task `4226`, and preserve Decision 79/77 as nonterminal accepted history. A later Decision-77 epoch is separate from amendment closeout.

## Optional later Decision-77 operation

Create a new source-mutation-forbidden controller, new epoch ID, and new claimant. Generate expiry from one captured timestamp with exact nanosecond preflight. Obtain a new human authorization, claim with a shorter lease, and pass active-epoch checks before Run A.

## Commit strategy

Commit candidate governance artifacts; accepted checker plus fixtures; then post-invalidation evidence/closeout. Never include `owned/docs/project/repo-capability-map.md`.
