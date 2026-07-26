---
summary: "RFC for one-time append-only invalidation of malformed Decision 77 epoch receipt 8967."
read_when:
  - "Reviewing or implementing recovery of Decision 77 epoch receipt 8967."
type: "rfc"
status: "proposed"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
governance_task_id: 4226
---

# RFC — one-time invalidation of Decision 77 epoch receipt 8967

## Decision requested

Amend Decision 77 with one exact recovery transition for malformed authorization receipt `8967`. Preserve its immutable history, prospectively quarantine that malformed chain element, restore the epoch-index head to `inactive`, and retain strict validation for every other authorization.

Receipt `8967` remains an immutable malformed authorization receipt and never passes authorization validation. This amendment neither rewrites its fields nor retroactively revokes authority: Decision 77 operation required both a valid authorization and a later exact controller claim, and neither existed. The successor receipt prospectively reconciles the chain head. This is an authority-contract amendment, not a checker-only exception, and becomes operative only after direct-human acceptance through AK.

## Scope

The amendment applies only when all exact facts hold:

- invalidated receipt ID `8967`;
- epoch ID `d77-e1-20260725`;
- controller task ID `4220`;
- claimant `pi-session-softwareco-cto-d77-epoch1`;
- measured interval `14,400.001074180` seconds;
- excess `1,074,180` nanoseconds;
- task `4220` remains at monotonic creation `entity_version=1`, with null claim fields and active quarantine deferral `182`;
- bounded AK censuses show no thesis, admission, owner task, or release derived from the receipt;
- the accountable human directly attests that no unenumerated publication, irreversible, or external effect derived from the receipt.

It creates no general timestamp tolerance and no reusable invalidation family.

## Amendment acceptance membrane

Decision `79` grants amendment authority only after all of the following are pinned and checked:

- one applied `architecture-decision` receipt with `agreement_ref=decision:79`;
- direct `human-operator` source and actor, explicit consent, and exact Softwareco repo scope;
- `from_state=decision_pending`, `to_state=accepted`;
- details schema `softwareco.architecture-decision-amendment-acceptance.v1`;
- `decision_id=79`, `amends_decision_id=77`, `outcome=accepted`;
- exact immutable RFC commit, review-closure commit, and ADR-plan commit;
- `epoch_authorized=false`, `invalidation_authorized=true`, `external_effects=0`;
- direct-human attestation that no authority-dependent or off-system effect occurred under receipt `8967`;
- AK Decision `79` reconciled to `outcome=accepted`, `state=unblocked`, with `evidence_ref` equal to that receipt.

The checker pins the final acceptance receipt ID and commits during post-acceptance implementation. Document presence, Decision state alone, and invalidation payload assertions never count. Until this membrane and the later invalidation both pass, every Decision 77 framework/epoch mode remains fail-closed.

## One-time transition

After this amendment is directly accepted, `human-operator` may append exactly one applied receipt to the existing epoch-index concern:

```text
epoch:d77-e1-20260725 -> inactive
```

Required envelope:

- concern `softwareco-portfolio-cto:decision77:epoch-index`;
- `source_authority=human-operator`, `actor=human-operator`;
- `agreement_ref=decision:77`;
- explicit consent and Softwareco repo scope;
- `task_id=4220`;
- mandatory evidence referencing receipt `8967`, task `4220` zero-operation proof, and the accepted amendment decision;
- `prior_epoch_receipt_id=8967`.

Required details:

```json
{
  "schema": "softwareco.portfolio-cto-epoch-invalidation.v1",
  "decision_id": 77,
  "amendment_decision_id": 79,
  "amendment_acceptance_receipt_id": "<pinned direct-human receipt>",
  "epoch_id": "d77-e1-20260725",
  "controller_task_id": 4220,
  "claimant_id": "pi-session-softwareco-cto-d77-epoch1",
  "invalidated_receipt_id": 8967,
  "invalidated_at_utc": "<RFC3339>",
  "reason": "authorization_interval_exceeds_hard_maximum",
  "observed_interval_ns": 14400001074180,
  "declared_lease_seconds": 14400,
  "excess_ns": 1074180,
  "controller_entity_version": 1,
  "controller_claim_fields_null": true,
  "controller_quarantine_deferral_id": 182,
  "zero_operation_evidence_id": "<pinned evidence>",
  "authority_dependent_effects": 0,
  "external_effects_attested": 0,
  "wip_handoff_refs": [],
  "prior_epoch_receipt_id": 8967,
  "evidence_refs": ["governance:8967", "task:4220@entity-version:1", "decision:79", "governance:<acceptance>", "evidence:<zero-operation>"]
}
```

## Checker semantics

The checker continues to require exact equality between every ordinary authorization's declared lease and timestamp interval.

Receipt `8967` may be quarantined only when its immediate successor is the unique exact invalidation above and all checks pass:

1. the Decision-79 acceptance membrane passes and predates invalidation;
2. direct-human source/actor, applied status, exact predecessor/state/schema/identities;
3. measured constants equal the immutable timestamps in receipt `8967`;
4. the pinned zero-operation evidence records task `4220` at `entity_version=1`, pending/null claim fields, source-mutation-forbidden scope, and active deferral `182`;
5. bounded AK censuses show zero controller/objective evidence, thesis head `none`, no Decision-77 child outcome wave, and no owner admission/release receipt before invalidation;
6. the direct-human receipts attest zero unenumerated external effects;
7. no duplicate, fork, gap, malformed candidate, or later reuse of epoch, controller, or claimant identity exists.

The epoch-index query requests `101` receipts and fails if more than `100` applied receipts exist. Validation builds the predecessor graph rather than trusting storage order: exactly one null-predecessor root, each non-root predecessor exists, at most one successor per node, no cycles, all nodes reachable, and exactly one head. Exactly one invalidation-schema receipt may exist; it must be the sole immediate successor of `8967`. The chain validator has three explicit branches: ordinary authorization, ordinary handback, and this exact one-time invalidation. Every field of `8967` remains validated; only its duration-equality failure is quarantined after the complete invalidation branch succeeds. All other authorizations retain exact equality.

The checker must never make receipt `8967` active or valid. Before the exact invalidation exists, every Decision 77 mode remains fail-closed.

## Recovery after invalidation

After verified inactive recovery, a later optional Decision 77 operation may:

1. create a new source-mutation-forbidden controller task;
2. use a new epoch ID and claimant;
3. capture `authorized_at_utc` once and derive expiration from that exact string, for example `expires=$(date -u -d "$authorized + 7200 seconds" +%Y-%m-%dT%H:%M:%S.%NZ)`;
4. reparse both values to integer nanoseconds and assert `expires_ns-authorized_ns == lease_seconds*1000000000` before recording;
5. use a lease shorter than the remaining review window and at most 14,400 seconds;
6. obtain a new direct-human authorization from `inactive`;
7. atomically claim the exact task with a shorter lease whose resulting expiry is verified no later than epoch expiry;
8. rerun Decision 74 terminal, Decision 77 framework, and active-epoch checks before sensing or mutation.

Task `4220`, epoch `d77-e1-20260725`, and claimant `pi-session-softwareco-cto-d77-epoch1` are permanently retired. Deferral `182` keeps task `4220` unclaimable; it is never resumed.

## Authority boundaries

- Amendment acceptance does not itself invalidate receipt `8967`; the exact human invalidation receipt is still required.
- Invalidation grants no epoch, owner acceptance, task scope, release, or external-effect authority.
- Decision 74 receipt `8870` and terminal proof remain unchanged.
- Decision 77 remains nonterminal.
- Owner and human reservations remain unchanged.
- The unrelated capability-map modification remains outside scope.
- Every other Decision 77 clause, owner boundary, hard-duration check, and terminal rule remains unchanged; this fixed exception is non-derogating and non-precedential.

## Alternatives rejected

- Ignore the millisecond excess: violates the hard maximum.
- Claim with a shorter lease: cannot cure malformed authorization history.
- Ordinary handback: restores the head but does not satisfy historical validation.
- Edit or delete receipt `8967`: destroys immutable authority history.
- Checker-only special case: changes accepted authority without human decision.
- Supersede Decision 77: lawful but unnecessarily discards the accepted recurring framework.

## Validation

The checker includes a mutation-free fixture/self-test path while production mode remains bound to live `ak`. Fixtures cover: absent invalidation; wrong predecessor/state/schema/amendment/evidence; duplicate invalidation; fork/gap/cycle/101st receipt; claimed or mutated controller; nonzero thesis/wave/owner evidence; reused epoch/task/claimant; exact inactive recovery; replacement authorization before claim; and valid replacement authorization after claim.

Expected state matrix:

| Chain state | Framework | Inactive | Active |
|---|---:|---:|---:|
| malformed `8967`, no invalidation | fail | fail | fail |
| malformed or partial invalidation | fail | fail | fail |
| exact invalidation head | pass | pass | fail |
| valid new authorization, unclaimed | pass | fail | fail |
| valid new authorization and claim | pass | fail | pass |

Before acceptance, all Decision 77 framework/epoch modes must fail closed on receipt `8967`. After implementation but before invalidation, they must still fail closed. After exact invalidation, framework/inactive modes must pass and active mode must fail. After new valid authorization and claim, active mode must pass. Decision 74 terminal proof, direction check, docs strict validation, and independent authority/runtime review must pass throughout.

## Rollback

Before acceptance, delete only the proposed amendment artifacts. After acceptance but before invalidation, revert checker implementation while preserving decision history. After invalidation, never delete or reinterpret either receipt; fail closed and use a successor decision if the amendment implementation cannot be safely maintained.
