---
summary: "ADR activating the Softwareco Org Owner and bounded CTO Agent delegation, plus L1 template changes before an issue-tracker canary."
read_when:
  - "Operating Decision 68 or the Softwareco CTO/template activation."
type: "adr"
status: "accepted"
date: "2026-07-18"
decision_id: 68
system4d:
  container:
    boundary: "Bounded Softwareco Org Owner/CTO activation, L1 source templates, and one later issue-tracker canary; no broader L2/L0 propagation."
  compass:
    driver: "Make technical delegation and agent/project operating contracts explicit before the operator canary."
  engine:
    invariants:
      - "Human residual authority remains explicit."
      - "AK and source-owner state remain canonical."
      - "Non-canary production propagation stays frozen."
  fog:
    risks:
      - "Template text is mistaken for delegation authority."
      - "Canary success is overstated as product-factory proof."
---

# ADR — Activate Softwareco CTO Agent and L1 template contract

## Decision

Accept the reviewed RFC at `docs/project/2026-07-18-softwareco-cto-template-activation-rfc.md` and controlling synthesis at `docs/reviews/2026-07-18-softwareco-cto-template-synthesis.md`.

Appoint `human-operator` as the accountable Softwareco Org Owner for this activation and delegate bounded technical flow stewardship to `softwareco-cto-agent` under `docs/org/cto-agent-charter.md`.

Authorize:

- Softwareco governance activation for this bounded domain;
- L1 project and agent template changes defined by the RFC;
- fresh-render template validation;
- one later reversible existing-L2 canary in `infra/issue-tracker` through a separate source-owner task.

## Expiry and reserved authority

The CTO Agent delegation expires 30 days after acceptance, at the issue-tracker canary terminal decision, or on immediate human revocation. The human retains terminal, portfolio, appointment, privacy, consent, ethics, licensing, security-exception, irreversible, public, external-effect, and authority-boundary decisions.

## Propagation freeze

No production generation of new L2 repositories and no non-canary existing-L2 update may use this changed contract until a separate accepted template-owner AK decision. No canary terminal outcome lifts this freeze by itself.

## Required execution order

1. Track implementation and validation/rollback plans.
2. Land governance and L1 template changes with deterministic tests.
3. Validate fresh renders.
4. Open the issue-tracker canary as a separate source-owner task on the repository's main-first workflow; use a branch or PR only if the operator explicitly requests a review gate.
5. Record conformance, effectiveness, learning, and a human terminal decision.

## Rollback

Supersede/revoke the delegation in AK, revert isolated L1 commits, restore the issue-tracker canary baseline if started, and re-run owner validations. Decision/evidence history remains immutable.
