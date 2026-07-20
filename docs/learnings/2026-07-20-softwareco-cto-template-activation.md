---
summary: "Decision 68 learning: template-first activation is safe only when propagation stays frozen and executable canary evidence remains separate."
read_when:
  - "Reviewing CTO Agent delegation or propagating the updated agent/project template contract."
type: "learning"
status: "accepted_activation_learning"
date: "2026-07-20"
decision_id: 68
---

# Learning — template-first activation needs a hard propagation freeze

The operator intentionally reversed pilot 001's evidence-first ordering: establish governance and L1 template recommendations, then test them in `infra/issue-tracker`.

The reversal remained authority-correct because the accepted contract separated four things that are easy to conflate:

1. L1 source-template authoring;
2. disposable fresh-render validation;
3. one reversible existing-L2 canary;
4. broader L2/L0 propagation.

Only the first two are complete. The issue-tracker canary requires a separate source-owner task and review branch. Every other production L2 generation/update remains frozen until a separate accepted template-owner decision, regardless of the canary's terminal outcome.

The agent template also exposed a useful distinction: an agent repository owns an agent product/capability, while an organizational CTO appointment lives in accepted governance/AK state. Mixing those concerns turns repository text into accidental authority.

Reusable cognitive procedures were removed from the agent template and routed to Prompt Vault; runtime decisions and evidence remain in AK. This keeps generated repositories smaller and preserves owner boundaries.
