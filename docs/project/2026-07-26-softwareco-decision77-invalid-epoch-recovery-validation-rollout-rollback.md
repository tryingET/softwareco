---
summary: "Validation, rollout, and rollback contract for Decision 79's one-time invalid epoch quarantine."
read_when:
  - "Validating or rolling back Decision 79."
type: "plan"
status: "active"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
governance_task_id: 4226
---

# Decision 79 validation, rollout, and rollback

## Required gates

- docs strict validation and `git diff --check`;
- direct-human Decision-79 acceptance membrane and AK reconciliation;
- Decision 74 `--require-terminal` remains passing;
- before invalidation, every Decision-77 mode fails on receipt `8967`;
- fixture self-tests cover absent/partial/duplicate invalidation, bad amendment/evidence, graph fork/gap/cycle/overflow, controller mutation, nonzero operation, identity reuse, exact inactive recovery, and valid replacement authorization before/after claim;
- after exact invalidation, framework/inactive pass and active fails;
- direction check passes and unrelated capability-map content is untouched.

## Rollout sequence

```text
review closure
-> candidate ADR/plans
-> direct-human Decision-79 acceptance
-> AK reconciliation and task re-evaluation
-> zero-operation evidence
-> checker + fixture implementation
-> fail-closed pre-invalidation proof
-> direct-human invalidation
-> inactive recovery proof
-> Decision-79 implementation closeout
```

A later Decision-77 epoch is a separate operation.

## Stop conditions

Stop on missing/ambiguous human acceptance, task `4220` entity-version or deferral drift, any controller claim, any Decision-77 thesis/wave/owner evidence derived from `8967`, overflow/incomplete enumeration, nonzero or uncertain AK-governed effect, failed fixture, Decision 74 regression, or any required external-effect attestation the human cannot make.

## Rollback

Before acceptance, revert only Decision-79 candidate docs. After acceptance but before invalidation, revert checker implementation while preserving decision/receipt history. After invalidation, never delete or reinterpret receipt `8967` or its invalidation; fail closed and use a successor decision if maintenance is unsafe. Owner repositories require owner-native rollback and are not mutated by this amendment.

## Success

Decision 79 succeeds when exact invalidation is verified, Decision 77 returns to a valid inactive nonterminal framework, Decision 74 remains terminal, task `4220` remains quarantined, and no epoch is inferred. Optional future epoch success is outside Decision-79 completion.
