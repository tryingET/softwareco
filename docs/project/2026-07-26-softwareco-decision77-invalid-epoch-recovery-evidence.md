---
summary: "Observed evidence for malformed Decision 77 epoch receipt 8967 and its zero-effect state."
read_when:
  - "Reviewing the Decision 77 epoch recovery amendment."
type: "evidence"
status: "accepted"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
governance_task_id: 4226
---

# Evidence — invalid Decision 77 epoch recovery

## Immutable receipt facts

Fresh `ak governance show 8967 --json` reports:

- concern `softwareco-portfolio-cto:decision77:epoch-index`;
- direct `human-operator` source and actor;
- transition `inactive -> epoch:d77-e1-20260725`;
- controller task `4220` and claimant `pi-session-softwareco-cto-d77-epoch1`;
- `authorized_at_utc=2026-07-26T02:42:39.056097206Z`;
- `authorization_expires_at_utc=2026-07-26T06:42:39.057171386Z`;
- `lease_seconds=14400`;
- status `applied`.

The timestamp interval is `14,400.001074180` seconds, `1,074,180` nanoseconds beyond the hard maximum.

## Cause

The session-local helper `/tmp/softwareco-decision77-epoch1-authorize.sh` sampled `authorized_at_utc` and the base for `authorization_expires_at_utc` with two separate `date` calls. Execution delay between those calls enlarged the interval. This establishes the mechanical source of the mismatch; no inference about intended authority is used.

## Fail-closed proof

`./scripts/check-cto-operator-surface.sh --require-77-framework` exits nonzero with:

```text
cto-operator-surface: FAIL: historical epoch duration mismatch
```

The checker validates every applied historical authorization before mode-specific success. An ordinary handback would therefore leave the malformed historical receipt blocking all modes.

## Zero-operation proof

Fresh `ak task show 4220 --machine` after receipt `8967` reports:

- `status=pending`;
- `claimed_by=null`;
- `claimed_at=null`;
- `lease_expires_at=null`;
- `entity_version=1`, the creation version;
- `allowed_paths=[]`, `required_paths=[]`, `forbidden_paths=["**"]`.

Agent Kernel source defines task `entity_version` as monotonic and increments it on task-row mutation, including claim and unclaim (`owned/agent-kernel/crates/ak-core/src/tasks.rs`, `prepare_task_row_mutation` and `claim_task_tx`). Thus creation-version `1` plus null claim fields is the available authoritative AK proof that task `4220` had not undergone a claim/unclaim task-row mutation at observation time.

To close the claim race, task `4220` was placed under active deferral `182`, triggered on Decision `79`, by the recovery task claimant. Its task row remains at entity version `1`; Agent Kernel refuses claims while an active deferral exists. This is quarantine, not epoch authority.

At detection time, direction projected `phase=awaiting_epoch` and `thesis_head_evidence_id=none`; `ak evidence task` returned count `0` for controller `4220` and objective `4221`; task `4221` had no result; and the Decision-77 direction child census contained only framework node `IW-SF3-CTO77-RECURRING`, with no admitted outcome wave. These bounded AK observations show no AK-governed thesis, admission, release, or owner task derived from `8967`.

No complete machine ledger exists for all possible off-system/publication/external effects. Their absence is not inferred. The direct-human amendment acceptance and invalidation receipts must explicitly attest zero such effects for the interval from receipt `8967` creation through invalidation.

## Independent review

Read-only review `dispatch-1785033803205` concluded:

- controller claim is unlawful under receipt `8967`;
- handback alone cannot repair historical validation;
- Decision 77 contains no invalidation semantics;
- a human-accepted architecture amendment or successor framework is required;
- lawful recovery must preserve receipt `8967`, prove zero operation, and use a new controller task and epoch identity.
