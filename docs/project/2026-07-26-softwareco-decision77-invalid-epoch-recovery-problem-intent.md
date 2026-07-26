---
summary: "Problem and intent for append-only recovery from malformed Decision 77 epoch receipt 8967."
read_when:
  - "Reviewing or recovering the first Decision 77 epoch authorization."
type: "problem"
status: "accepted"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
governance_task_id: 4226
---

# Problem and intent — invalid Decision 77 epoch recovery

## Trigger

Direct-human epoch authorization receipt `8967` was recorded for Decision 77. It declares `lease_seconds=14400`, but its independently sampled timestamps span `14,400.001074180` seconds. This exceeds Decision 77's hard maximum by `1,074,180` nanoseconds.

At detection, controller task `4220` remained at its creation entity version with null claim fields; no fresh sensing run, thesis evidence, or Decision-77 wave was observed. Machine reads cannot prove absence from every off-system external-effect surface, so that residual must be stated and directly attested by the accountable human rather than inferred.

## Fail-closed consequence

The accepted checker correctly rejects every Decision 77 mode with `historical epoch duration mismatch`. A later ordinary handback cannot repair this: the checker revalidates every applied historical authorization, and Decision 77 defines no invalidation receipt. Claiming controller task `4220`, treating the discrepancy as tolerance, editing receipt `8967`, or silently weakening the checker would violate the accepted framework.

## Intent

Preserve immutable receipt `8967` while adding one narrowly bounded, direct-human invalidation path that:

1. applies only to receipt `8967` and epoch `d77-e1-20260725`;
2. binds immutable AK snapshots showing controller task `4220` remained at creation entity version and unclaimed through quarantine;
3. enumerates AK-governed authority-dependent effects and separately requires direct-human attestation for off-system effects;
4. returns the epoch-index head to `inactive` through an append-only receipt;
5. keeps exact duration validation for every ordinary authorization;
6. makes epoch/controller identity `d77-e1-20260725`/`4220` permanently non-reusable;
7. requires a new controller task, epoch ID, and direct-human authorization before operation.

## Completion boundary

Amendment closure is staged: reviewed RFC; direct-human acceptance and ADR recording; fail-closed checker implementation; direct-human invalidation; and verified inactive recovery. A later epoch authorization and claim are a separate optional Decision 77 operation, not amendment completion. Acceptance of this amendment grants no epoch, owner, release, or external-effect authority.
