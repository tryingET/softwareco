---
summary: "ADR accepting a finite Softwareco owned-portfolio CTO mandate and governed Pi workbench under Decision 74."
read_when:
  - "Operating, reviewing, revoking, or superseding Decision 74."
type: "adr"
status: "accepted"
date: "2026-07-25"
decision_id: 74
accepted_at: "2026-07-25T08:11:27.729630885Z"
expires_at: "2026-08-24T08:11:27.729630885Z"
system4d:
  container:
    boundary: "Thirty-day technical portfolio sequencing over softwareco/owned; source-owner execution and human residual authority remain outside the delegated office."
  compass:
    driver: "Turn the previously documentary CTO role into an operable, evidence-driven portfolio function without confusing Pi behavior with authority."
  engine:
    invariants:
      - "AK decision and SF3 own delegation; Pi Modes never grants authority."
      - "Owners originate outcome, capacity, task, objection, and terminal acceptance."
      - "At most two portfolio waves and six admitted owner-repo tasks are outstanding."
      - "FCOS is used only through its owner for genuine cross-repo coordination."
  fog:
    risks:
      - "Controller-authored consent impersonates an owner."
      - "Non-atomic cross-repo admission is overstated as a global lock."
      - "A portfolio wrapper silently mutates owner-task lifecycle."
---

# ADR — Softwareco owned-portfolio CTO workbench and finite mandate

## Decision

Accept the exact RFC candidate at Softwareco commit `a76c53b101537ce401867199259b30fd8c7a92ac` and its controlling final synthesis:

- [RFC](../project/2026-07-25-softwareco-portfolio-cto-rfc.md)
- [Evidence](../project/2026-07-25-softwareco-portfolio-cto-evidence.md)
- [Final review synthesis](../reviews/2026-07-25-softwareco-portfolio-cto-final-review-synthesis.md)

The accountable human selected **Accept Decision 74** through the structured Decision 74 gate on 2026-07-25.

Appoint `human-operator` as residual accountable Softwareco Org Owner for this mandate and delegate `softwareco-cto-agent` to rank and sequence technical investments across the registered `softwareco/owned` portfolio inside accepted owner envelopes.

## Finite authority

The mandate:

- begins only after post-decision projections, workbench implementation, validation, controller creation/designation, and exact `SF3` activation;
- expires exactly 30 days after AK acceptance, or earlier at the mandate terminal decision, direct revocation, or an explicitly superseding accepted decision;
- allows at most two admitted portfolio waves and six outstanding admitted owner-repo tasks;
- requires explicit `human-operator` acceptance before the second concurrent wave;
- proves itself through one evidence-backed portfolio thesis and one completed outcome wave.

The CTO may choose technical portfolio ordering, operate portfolio wrappers, coordinate accepted owner work, enforce gates, stop unsafe automation, and determine wrapper completion after every required terminal acceptance.

## Owner and human reservations

The decision does not delegate:

- Product/Domain outcome, capacity, displacement, objection, or terminal acceptance;
- Project/source-owner task scope or lifecycle;
- Service/Platform operational or shared-contract acceptance;
- product creation, permanent stop/retirement, durable portfolio commitment, or owner appointment;
- architecture-significant acceptance;
- release, publication, public, irreversible, or external effects;
- privacy, consent, ethics, licensing, or security exceptions;
- mandate-level `continue`, `stop`, `redirect`, or `complete`.

Owners directly originate governance receipts with owner-native evidence. The controller may prepare or reference them but may not assert another actor's consent.

## Runtime architecture

```text
Decision 74 accepted + exact active SF3 detail
-> one human-designated leased Softwareco controller task
-> tracked Pi Modes 0.3.0 softwareco-cto overlay/preset
-> trusted Softwareco-root /cto <objective>
-> owner-originated acceptance receipts
-> Softwareco portfolio wave + coordinator task
-> exact owner-repo AK tasks
-> FCOS owner handoff only when genuinely cross-repo
-> outcome evidence and human terminal review
```

Pi Modes is pinned to `@tryinget/pi-modes` `0.3.0`, tag `pi-modes-v0.3.0`, owner release commit `173b508b0bea27550f061e252e1d86a0638d2d71`.

## Consequences

- Softwareco gains a real portfolio technical-sequencing office rather than a persona claim.
- Owner consent and execution remain federated.
- The first mandate uses atomic controller-task claim plus serialized procedural admission; it is not a global cross-repository lock.
- A mode, preset, prompt, session, coordinator task, or FCOS item never appoints the CTO.
- No generated CTO agent repository is created in this slice.
- `infra/issue-tracker` remains a downstream-dependency issue-filing system, not the CTO backlog.
- Decision 68's template-propagation freeze remains unchanged.

## Activation gate

This ADR does not activate the CTO by itself. Activation requires:

1. post-ADR implementation and validation/rollout/rollback artifacts;
2. corrected charter, governance, and operating-model projections;
3. tracked and validated mode, preset, `/cto` prompt, operator guide, and deterministic checks;
4. exact Pi Modes release installation and live command proof;
5. a scoped Softwareco controller task and direct human controller designation;
6. exact `SF3` active detail with accepted, activated, and expiry timestamps;
7. clean pre/post-read authority reconciliation.

Until all seven pass, `SF3` remains a decision/implementation frame and every CTO invocation is advisory.

## Revocation and rollback

`human-operator` may revoke immediately through the accepted governance-receipt contract. Revocation ends CTO control before projection reconciliation but never auto-mutates owner tasks. `/mode off` removes prompt behavior only; it is not authority revocation.

Revert isolated workbench files if defective, return admitted tasks to owners through explicit owner release/handoff, reconcile `SF3`, preserve immutable decision/evidence history, and do not describe compensation as exact rollback of external effects.
