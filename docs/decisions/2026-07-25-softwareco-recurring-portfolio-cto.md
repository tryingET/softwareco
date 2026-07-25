---
summary: "ADR candidate for Decision 77's dormant recurring CTO framework with finite human-authorized epochs."
read_when:
  - "Operating, reviewing, activating, revoking, or superseding the recurring Softwareco CTO framework."
type: "adr"
status: "pending_human_acceptance"
date: "2026-07-25"
decision_id: 77
system4d:
  container:
    boundary: "Recurring technical portfolio sequencing over registered softwareco/owned repositories; owner lifecycle and human-reserved decisions remain outside."
  compass:
    driver: "Turn the one-wave Decision 74 canary into a restartable recurring loop without creating a permanent autonomous office."
  engine:
    invariants:
      - "No CTO is appointed between finite direct-human-authorized epochs."
      - "Decision 74 and receipt 8870 remain immutable terminal history."
      - "Owners originate acceptance, objection, terminal, return, and release decisions."
      - "Objective completion never implies framework continuation or termination."
  fog:
    risks:
      - "A dormant framework is mistaken for active delegation."
      - "Thesis evidence becomes a shadow backlog."
      - "WIP projections diverge from owner facts."
---

# ADR — recurring Softwareco portfolio CTO operating framework

## Status

Candidate ADR for AK Decision `77`. It becomes accepted only after direct accountable-human acceptance is recorded in AK. This document currently grants no authority.

## Decision

Adopt the exact Decision 77 RFC candidate at commit `d2a372e388a990231160e1d8bd9b0360d10ab262` and controlling review synthesis:

- [RFC](../project/2026-07-25-softwareco-recurring-portfolio-cto-rfc.md)
- [Problem](../project/2026-07-25-softwareco-recurring-portfolio-cto-problem-intent.md)
- [Evidence](../project/2026-07-25-softwareco-recurring-portfolio-cto-evidence.md)
- [Closure synthesis](../reviews/2026-07-25-softwareco-recurring-portfolio-cto-closure-synthesis.md)

Decision 77 establishes a durable **dormant framework**. Actual `softwareco-cto-agent` delegation exists only inside one finite, direct-human-authorized epoch of at most 14,400 seconds. No CTO is appointed between epochs.

## Corrected outcome

The framework supports a recurring loop:

```text
fresh read-only worker
-> AK/source-owner reconstruction
-> controller-verified thesis evidence
-> direct owner acceptance
-> serialized portfolio admission
-> exact owner task execution
-> owner terminal acceptance and release
-> outcome evidence
-> fresh post-outcome re-entry
```

The current objective requires at least one additional independent non-DesignMD outcome and post-outcome fresh-session reconstruction. Completing that objective closes only its exact task/proof record; it neither terminalizes nor renews the framework.

## Authority

Framework validity requires accepted Decision 77, a current human review window, no terminal/revocation/supersession, and an exact Decision-77 projection. Mutation/selection additionally requires one valid epoch-index head, matching source-mutation-forbidden controller task and claimant, unexpired authorization/claim, exact execution task, owner receipts, and WIP/objection gates.

Decision 74, receipt `8870`, `SF3` terminal detail, controller task `4182`, and the DesignMD canary remain immutable historical facts. Decision 77 never reopens them.

## Owner and human reservations

Owners directly originate outcome/capacity/displacement, task scope, objection/resolution, terminal acceptance, return, and release receipts with owner-native evidence. Portfolio wrappers never mutate owner task lifecycle.

Stop and escalate for product lifecycle or durable commitment, posture/accountability conflict, architecture acceptance, appointment/transfer, sensitive exception, release/publication/public/irreversible/external effect, or framework-level review/pause/redirect/stop/complete/revocation/supersession. Repeated ordinary waves cannot bootstrap a reserved decision.

## Runtime contract

- Decision-77 projection: native `work_wave` `IW-SF3-CTO77-RECURRING`, child of `SF3`, explicitly non-authorizing.
- Fixed epoch chain: `softwareco-portfolio-cto:decision77:epoch-index`.
- Epoch duration: hard non-renewable maximum 14,400 seconds.
- Framework review: initial acceptance plus at most 30 days; later direct-human review receipts, max 30 days.
- Thesis: bounded non-forking `portfolio_thesis_v2` AK evidence series whose task IDs and head are projected in AK direction.
- WIP: at most two admitted waves and six outstanding owner tasks; disagreement counts as outstanding.
- Current objective: exact `portfolio_cto_recurrence_objective_v1` proof, with no terminal/revocation/supersession inferred.

## Consequences

- Softwareco can run repeated bounded CTO cycles without a new architecture decision for each ordinary wave.
- Human silence never appoints or continues an active CTO epoch.
- Fresh workers may sense read-only but cannot record evidence or mutate authority.
- The controller remains a serialized procedural membrane, not a global lock.
- More AK receipts/evidence are required, but their roles are explicit and owner-native.
- The existing tracked mode/prompt/checker must be generalized after acceptance while retaining Decision 74 terminal negative controls.

## Alternatives rejected

- Reopen Decision 74: illegal because receipt `8870` is terminal.
- One architecture decision per wave: safe but not recurring operation.
- Indefinite standing delegated office: rejected because human silence would preserve appointment.
- Generated autonomous agent repository: premature and does not solve authority.

## Validation and rollback

Implementation follows:

- [Implementation plan](../project/2026-07-25-softwareco-recurring-portfolio-cto-implementation-plan.md)
- [Validation, rollout, and rollback](../project/2026-07-25-softwareco-recurring-portfolio-cto-validation-rollout-rollback.md)

No implementation, epoch, or portfolio mutation is legal before direct Decision 77 acceptance and post-acceptance gates.
