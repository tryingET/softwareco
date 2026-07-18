---
summary: "Controlling synthesis of four adversarial review attempts against the initial Software Factory Flow Protocol RFC draft."
read_when:
  - "Determining the legal next move after the first RFC review set."
type: "review-synthesis"
---

# Review synthesis — Software Factory Flow Protocol RFC v0

## Review set

- reviewed artifact: `docs/project/2026-07-12-software-factory-operating-system-rfc.md`
- reviewed worktree SHA-256: `31e194ea9b77dc439a7f9b1b9ad1dac3e92fc7ca981b3c9a3c2888a04d1cb298`
- revision status: untracked worktree content at review time
- synthesis rule: designated synthesizer; any critical authority/lifecycle blocker or repeated high-confidence blocker forces revision
- input review attempts:
  - `docs/reviews/2026-07-12-software-factory-rfc-v0-architecture-authority.md`
  - `docs/reviews/2026-07-12-software-factory-rfc-v0-flow-quality.md`
  - `docs/reviews/2026-07-12-software-factory-rfc-v0-product-accountability.md`
  - `docs/reviews/2026-07-12-software-factory-rfc-v0-operations-adoption.md`

## Agreement across tracks

All four tracks support the core direction:

- do not build another factory platform;
- use a federated protocol over owner-native authority;
- prove it through a bounded pilot;
- keep deployment, operation, and outcome evidence distinct.

All four tracks independently found the RFC not ready for ADR.

## Controlling blockers

1. **Authority:** decisive fields and appointment/decision rights lack one canonical owner and conflict rule.
2. **Projection safety:** the manual packet lacks identity, freshness, drift, and reconciliation behavior.
3. **Flow economics:** WIP units, total-load accounting, admission authority, and constraint hypothesis are undefined.
4. **Customer/outcomes:** the first pilot lacks a selected segment/problem, preregistered baseline/target, and falsification threshold.
5. **Reliability:** operational evidence can be documentary rather than demonstrated; risk tiers and recovery proof are missing.
6. **Measurement:** start/stop events, gaming defenses, and protocol-conformance versus effectiveness are not separated.
7. **Rollback:** protocol, release, data/state, and organizational rollback are conflated.
8. **Lifecycle legality:** reviewed artifacts were not tracked repository revisions.

## Workflow result

- review_outcome: `revise_rfc`
- next legal move: `revise_rfc`
- ADR legal now?: no
- controlling rationale:
  - preferred direction remains viable;
  - the pilot contract is not yet precise or falsifiable enough;
  - responsibility and canonical-write ambiguity could create shadow authority;
  - a new immutable review cycle is required after revision.

## Revision requirements

The next RFC revision must at minimum:

- add authority and decision-rights matrices;
- define packet projection/reconciliation behavior;
- normalize classification and terminal decisions;
- define WIP units, total load, admission, and constraint-testing rules;
- require a selected evidence-backed pilot before ADR implementation planning;
- preregister pilot outcomes and measurement events;
- add risk-tiered release/service acceptance;
- split rollback families;
- add cold-start operator and overhead tests;
- complete vocabulary preflight;
- be tracked before any review can establish ADR legality.
