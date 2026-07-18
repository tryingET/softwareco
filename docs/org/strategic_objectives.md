---
summary: "Softwareco strategic objectives, company-level measures, accountable roles, and review horizons."
read_when:
  - "Setting Softwareco portfolio direction or evaluating whether work advances company outcomes."
  - "Preparing monthly outcome or horizon reviews."
type: "reference"
mito_layers:
  - "Strategic"
  - "Operations & Evaluation"
---

# Softwareco strategic objectives

## How to use these objectives

These objectives define company-level outcomes, not a parallel task queue. Narrative meaning stays here; active strategic frames, implementation waves, decisions, tasks, and evidence belong in AK. Cross-repo coordination belongs in FCOS only when genuinely required.

Targets without a current baseline begin with a baseline phase. Owners may refine a target through an accepted AK decision, but must preserve the original rationale and measurement history.

## Control envelope

| Field | Current value |
|---|---|
| `as_of` | 2026-07-12 |
| narrative status | proposed company direction; not yet activated in AK |
| activation gate | accepted Softwareco Org Owner appointment/delegation plus an AK-native Softwareco strategic frame |
| baseline packet deadline | 2026-09-30; if activation is still blocked, record the blocker and rebaseline through an AK decision rather than silently moving the date |
| first operating horizon | 2027-06-30 |
| vision horizon | 2030-12-31 |
| authoritative progress state | AK direction/tasks/decisions/evidence after activation; this document remains narrative direction |

| ID | Objective | First auditable target |
|---|---|---|
| `SOFT-O1` | Trustworthy factory flow | first pilot by 2026-12-31; second materially different pilot by 2027-03-31 |
| `SOFT-O2` | Governed agent/local-AI platform coherence | two owner-proved supported journeys by 2027-06-30 |
| `SOFT-O3` | Human-facing vertical proof | first vertical outcome review by 2027-06-30; two sustained vertical proofs by 2030-12-31 |
| `SOFT-O4` | Operational trust | service inventory baseline by 2026-12-31; 100% of supported services meet declared posture by 2027-06-30 |
| `SOFT-O5` | Compounding engineering system | flow/rework/evidence baseline by 2026-12-31; owner-approved improvement targets by 2027-03-31 |
| `SOFT-O6` | Sustainable open-source stewardship | consume/contribute/fork posture for strategic external dependencies by 2027-06-30 |

Missing baseline or owner evidence makes an objective `blocked` or `insufficient_evidence`; it must not be reported as on track from narrative confidence.

## O1 — Operate one trustworthy software-factory flow

**Outcome:** Softwareco can repeatedly turn validated demand into safely operated, measurable outcomes without relying on operator memory as the integration layer.

**Measures:**

- establish an AK-native Softwareco strategic frame and named accountable portfolio owner;
- complete one end-to-end pilot of the Factory Flow Protocol, including outcome registration, finite WIP, owner-native execution, promotion or explicit non-deployment learning, terminal decision, and learning closure;
- complete a second materially different pilot before template or schema propagation;
- record demand-to-commitment, commitment-to-release, blocked age, protocol overhead, and release-to-outcome-review time;
- zero packet-only mutations of canonical task, decision, promotion, or closure state.

**Accountable role:** Softwareco Org Owner.

**Review cadence:** weekly flow review during pilots; monthly outcome review; quarterly horizon review.

**Reference:** [[softwareco/docs/project/2026-07-12-software-factory-operating-system-rfc.md|Softwareco Factory Flow Protocol RFC]].

## O2 — Make the governed agent and local-AI platform coherent

**Outcome:** Products and operators can use agent execution and local AI capabilities through stable, owner-correct contracts rather than bespoke integrations.

**Measures:**

- select and document the first supported platform journeys across AK, Pi execution, local AI capability resolution, evidence, and recovery;
- each supported journey has an owner, exact operator path, automated proof, failure classification, and rollback or containment path;
- reduce duplicated lifecycle/resource/receipt implementations in adopting products from a measured baseline;
- pass a cold-start operator test for each promoted journey without private author coaching;
- no higher-layer capability claim exceeds owner-repo maturity proof.

**Accountable role:** Platform Domain Owner, appointed by the Softwareco Org Owner.

**Review cadence:** monthly platform health review; quarterly portfolio review.

## O3 — Prove the platform through selected human-facing verticals

**Outcome:** Platform investment produces measurable benefit for people rather than becoming self-referential infrastructure work.

**Measures:**

- choose no more than three active vertical bets at one time;
- every active bet identifies a user group, observed problem, current workaround, outcome baseline, target, guardrail, owner, support posture, and stop/redirect threshold;
- demonstrate at least two materially different verticals with sustained use and measurable user benefit within the vision horizon;
- include teaching/learning, household/knowledge work, accessibility, or small-institution needs in portfolio consideration;
- stop or redirect bets whose evidence does not justify continued constrained capacity.

**Accountable role:** Relevant Product Owner; portfolio accountability remains with the Softwareco Org Owner.

**Review cadence:** monthly product outcome review; quarterly investment decision.

## O4 — Establish operational trust for supported services

**Outcome:** Softwareco knows what it operates, who owns it, how it is observed, and how it recovers.

**Measures:**

- 100% of supported operated services have a named Service Owner, environment/version discovery, health/readiness path, support boundary, incident path, and retirement path;
- every stateful or risk-significant service has risk-appropriate recovery evidence, including RTO/RPO where meaningful;
- every R2-or-higher service completes at least one recovery or containment rehearsal per year;
- promotion records distinguish verified source, artifact/configuration, environment, readback, observation window, and rollback/forward-recovery posture;
- incident and failed-promotion learnings reach KES or an explicit owner decision.

**Accountable role:** Service Owners; company-wide exceptions belong to the Softwareco Org Owner.

**Review cadence:** monthly service health review; immediate incident review; annual recovery exercise minimum.

## O5 — Build a compounding, evidence-led engineering system

**Outcome:** Each delivery wave makes future work safer, faster, and easier to understand without adding uncontrolled process layers.

**Measures:**

- maintain engineering-core adoption and semantic/loop validation across active owned products and packages;
- measure lead time, rework, blocked age, rollback rate, and evidence freshness for factory pilots before setting optimization targets;
- promote reusable learnings into tests, contracts, runbooks, templates, or owner-approved governance instead of prose-only status;
- track the percentage of significant closed work with linked evidence and an explicit learning disposition;
- reduce stale, duplicated, or misleading authority/projection surfaces from a measured baseline.

**Accountable role:** Engineering Domain Owner with product and service owners.

**Review cadence:** monthly engineering-system review; quarterly standards review.

## O6 — Practice sustainable and reciprocal open-source stewardship

**Outcome:** Softwareco's use of open source strengthens the ecosystems and responsibilities on which it depends.

**Measures:**

- every strategically important external dependency or upstream-coupled repo has an explicit consume/contribute/fork posture;
- compatibility-sensitive upstream changes have bounded validation and evidence paths;
- maintained forks name divergence rationale, owner, update policy, security posture, and exit conditions;
- public releases contain no secrets and include licensing, attribution, support, and security expectations appropriate to maturity;
- mature products evaluate at least one sustainable revenue, partnership, or funding path that does not require surveillance, coercive lock-in, or authority compromise.

**Accountable role:** Relevant Product/Platform Owner; portfolio tradeoffs belong to the Softwareco Org Owner.

**Review cadence:** quarterly dependency and sustainability review.

## Portfolio guardrails

- Company WIP is finite; starting work requires naming what is deferred, displaced, or stopped.
- Capability maps route; owner repositories prove.
- A repository is not automatically an active product.
- An experiment without a timebox and decision threshold is not a strategic commitment.
- A passing build is not an operated outcome.
