---
summary: "ADR accepting the Softwareco Factory Flow Protocol for one bounded evidence-preserving retirement pilot."
read_when:
  - "Operating Decision 62 or the first Softwareco Factory Flow pilot."
  - "Evaluating what the Factory Flow ADR did and did not authorize."
type: "adr"
status: "accepted"
date: "2026-07-18"
decision_id: 62
system4d:
  container:
    boundary: "Acceptance of the Factory Flow architecture and pilot 001 only; not factory-wide rollout or physical repository deletion."
    edges:
      - "[RFC](../project/2026-07-12-software-factory-operating-system-rfc.md)"
      - "[Pilot selection](../project/2026-07-18-factory-flow-pilot-fcos-proving-lane.md)"
      - "[Review synthesis](../reviews/2026-07-18-software-factory-rfc-v3-synthesis.md)"
  compass:
    driver: "Prove one owner-correct demand-to-outcome loop without adding another authority platform."
    outcome: "A bounded, evidence-producing pilot tests the protocol and ends in a human terminal decision."
  engine:
    invariants:
      - "Human authority remains residual and explicit."
      - "AK and source-owner facts remain canonical; FCOS is used only for real cross-owner gates."
      - "Preservation and restoration proof precede retirement projection changes."
  fog:
    risks:
      - "Process conformance is mistaken for outcome improvement."
      - "Historical or dirty evidence is lost."
      - "A first internal pilot is overgeneralized into company or L0 template policy."
---

# ADR — Accept Factory Flow Protocol for pilot 001

## Decision

Accept the Softwareco Factory Flow Protocol defined by:

- `docs/project/2026-07-12-software-factory-operating-system-rfc.md`;
- exact reviewed RFC blob `ff27c45a112e152dd891d9f7ddb79db34055d8eb`;
- exact reviewed RFC SHA-256 `9b0c14de59e5f2f55519d28e5272588f883eed857cc33e70971eb1b05c1531a7`;
- controlling review synthesis `docs/reviews/2026-07-18-software-factory-rfc-v3-synthesis.md`.

Authorize one bounded post-ADR pilot:

> `SOFTWARECO-FACTORY-PILOT-001` — safely preserve, classify, restore-prove, and make unambiguously historical the zombie `softwareco/owned/fcos-proving-lane` repository, without physical deletion in the first wave.

## Human acceptance and delegation

The higher-level human operator selected this pilot, requested an agent CTO-like role, and instructed execution to continue through legal completion.

This ADR activates a bounded, revocable **Softwareco CTO Agent** delegation for pilot 001:

- may prepare technical options, coordinate scoped tasks, enforce this ADR's gates, stop unsafe automation, gather evidence, and recommend a terminal decision;
- may not accept or change this ADR, authorize physical deletion, waive preservation or recovery, mutate FCOS product authority, start another pilot, or become residual accountable human authority;
- expires at the pilot terminal decision or immediate human revocation.

The human operator retains irreversible-retirement, physical-deletion, ADR-change, and final `continue`/`stop`/`redirect`/`complete` authority.

## Rationale

Option C—a federated protocol over existing owners—best addresses the missing connective tissue without introducing a shadow platform. The selected proving-lane concern is real, operator-evidenced, reversible when preservation is correct, and rich enough to test:

- work admission and finite WIP;
- owner discovery and projection safety;
- cross-repo boundary discipline;
- lossless preservation and restoration;
- operator cold-start discoverability;
- evidence-driven terminal decisions and learning.

It does not prove human-facing product delivery; that requires a materially different second pilot.

## Consequences

### Authorized after required execution plans are tracked

- create one Softwareco AK strategic frame for the accepted pilot;
- record one bounded capacity admission;
- create one source-owner preservation/classification task with exact scope;
- create an FCOS item only if a genuine multi-owner gate emerges;
- perform read-only capture, preservation, classification, restoration rehearsal, owner routing, validation, cold-start testing, and human outcome review;
- update active projections only after restoration proof and through their owners.

### Not authorized

- physical deletion of `fcos-proving-lane`;
- destructive reset or cleanup before preservation/restoration proof;
- mutation of `holdingco/fcos-control-board` authority or product state;
- automatic Factory Flow schema, L2 template, or L0 propagation;
- a second pilot;
- company-wide claim that Softwareco now has a proven product factory;
- appointment of the CTO Agent as residual human owner.

## Required follow-through

Before source-owner mutation:

1. track an implementation plan;
2. track a validation/rollout/rollback plan;
3. attach both to Decision 62;
4. create/activate the Softwareco strategic frame;
5. reevaluate task `#4028` and create the exact source-owner task;
6. refresh the operator packet against current owner-native state.

Pilot closure requires:

- protocol conformance verdict;
- effectiveness verdict;
- successful preservation/restoration evidence;
- independent cold-start outcome;
- overhead and blocked-age evidence;
- mandatory KES learning;
- human terminal decision.

## Supersession

A later ADR may change or supersede this decision. Until then, any ambiguity resolves toward preservation, human authority, owner-native truth, and no destructive mutation.
