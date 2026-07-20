---
summary: "Softwareco governance: domains, accountable roles, decision rights, escalation, incidents, and authority boundaries."
read_when:
  - "Determining who may decide, execute, review, or escalate a Softwareco concern."
  - "Handling a high-impact change, cross-repo concern, incident, exception, or ownership conflict."
type: "policy"
status: "active_bounded"
as_of: "2026-07-20"
decision_id: 68
mito_layers:
  - "Design & Configuration"
  - "Implementation"
  - "Operations & Evaluation"
---

# Softwareco governance

> **Status as of 2026-07-20: active within Decision 68's bounded domain.** Decision 68 appoints `human-operator` as Softwareco Org Owner and delegates `softwareco-cto-agent` under [[softwareco/docs/org/cto-agent-charter.md|the CTO Agent charter]]. Authority outside that accepted domain remains owner-local or human-reserved; this document does not enlarge the decision.

## Governance intent

The Softwareco model uses **distributed ownership with explicit human accountability**. Within Decision 68's bounded activation, it makes decisions safer and clearer without creating a new council, PMO, shadow database, or approval queue.

```text
human-owned domain
-> explicit delegation
-> owner-local execution in AK/source repo
-> FCOS coordination only when cross-repo
-> evidence and outcome review
-> KES learning
```

Sociocracy 3.0 supplies governance semantics such as drivers, domains, agreements, consent, objections, delegation, and organizational learning. AK, FCOS, source-owner repositories, and other runtime surfaces record and execute accepted concerns according to their authority.

## Scope and change authority

This policy applies only within domains activated through accepted Softwareco-scoped decisions. Decision 68 currently activates technical strategy, L1 template work, and the issue-tracker canary preparation domain; it does not silently activate every portfolio decision.

- **Policy owner:** `human-operator` in the Softwareco Org Owner role recorded by Decision 68.
- **Change path:** architecture-significant or authority-changing revisions follow the Tier-1 decision lifecycle.
- **Operational details:** remain with Product, Service, Platform, and Project owners inside their delegated domains.

### Governance activation and vacancy rule

The Softwareco Org Owner role becomes active only when an accepted Softwareco-scoped AK decision records the appointee, delegated domain, reserved decisions, review date, revocation path, and evidence reference. Appointment changes company accountability and therefore must not be inferred from authorship, tool access, or this document.

Decision 68 satisfies the first bounded activation record: appointee `human-operator`; Softwareco domain; human-reserved decisions; 30-day/canary review; immediate revocation; reviewed RFC/ADR evidence; and linked execution task. Its CTO delegation is defined in `docs/org/cto-agent-charter.md`.

Outside that decision:

- no additional portfolio start/stop, cross-domain exception, or owner-appointment authority is created by these docs;
- Product, Service, Platform, and Project Maintainers retain owner-local authority;
- agents may prepare evidence and proposals but may not enlarge the activated domain by implication.

## Domains

A domain is a bounded area of decision-making and accountability, not necessarily a repository or hierarchy.

| Domain class | Examples | Primary accountability |
|---|---|---|
| Product | user-facing product or maintained package | user outcomes, lifecycle, prioritization |
| Service | continuously operated capability | reliability, support, incidents, recovery, retirement |
| Platform/enabling | AK/Pi integrations, local AI, engineering tooling, templates | stable contracts, adoption, developer/operator outcomes |
| Infrastructure | workstation, provisioning, runtime cell implementation, backup | availability, security, recovery, operational truth |
| Contribution/fork | upstream-coupled contributions or maintained divergence | reciprocity, compatibility, divergence and maintenance burden |
| Cross-system owner | AK, FCOS, ROCS, Prompt Vault, Pi, KES, DSPx | remains governed by that owner surface; Softwareco does not absorb it |

A domain can span repositories. Each active domain must identify one accountable human role, its driver, scope, exclusions, delegated authorities, reserved decisions, health signals, review date, and temporary-cover/succession rule.

## Roles

| Role | Accountability |
|---|---|
| Softwareco Org Owner | Portfolio posture, company boundaries, appointments, cross-domain tradeoffs, company-level risk and exceptions. |
| Domain Owner | Outcomes, boundaries, delegation, and health of a product/platform/service family. |
| Product Owner | Product vision, users, outcome priorities, lifecycle, and investment case. |
| Service Owner | Reliability, security, support, incident readiness, continuity, and decommissioning. |
| Platform Owner | Shared contract, adoption, compatibility, and operator/developer experience. |
| Project Maintainer | Source-owner acceptance, repository quality, releases, and day-to-day change control. |
| Incident Lead | Temporary coordination under bounded delegation; does not erase Product/Service Owner accountability. |
| Softwareco CTO Agent | Named agent delegatee for bounded technical strategy, architecture, flow stewardship, implementation coordination, verification, and escalation; never the residual accountable human or unilateral company portfolio authority. |
| Agent delegatee | Analysis, implementation, validation, or explicitly delegated low-impact decisions; never residual human accountability. |

One person may hold multiple roles, but the accountabilities remain explicit.

## Delegation contract

Every material delegation states:

```text
delegator
accountable owner
domain and scope
may decide / may execute
must consult / must escalate
constraints and non-authorizations
evidence required
expiry or review date
revocation and emergency-stop path
```

Defaults:

- Agents may recommend in any domain.
- Agents may execute claimable AK tasks within exact scope.
- Low-impact, reversible, repo-local decisions may be delegated explicitly.
- Authority-boundary, security/privacy, irreversible, public, cross-domain, and company-level portfolio decisions remain human-reserved.
- Silence is not consent unless an accepted agreement names stakeholders, notice, objection window, and delegation.

### CTO Agent boundary

The appointing human authority may delegate technical stewardship to a named **Softwareco CTO Agent**. That role may maintain technical coherence, prepare portfolio options, coordinate bounded execution, enforce accepted gates, stop unsafe automated work, and recommend `continue`, `stop`, `redirect`, or `complete`. The role may not appoint itself, accept an architecture-significant decision, authorize irreversible retirement, waive human-reserved safety/ethics constraints, or become the residual accountable owner. Human authorization and revocation remain explicit in the delegation record.

## Proposed decision rights

These allocations are operative only where an accepted activation/delegation record covers the domain. Decision 68 activates the bounded CTO/template/canary-preparation domain; other rows remain proposed until separately activated. **A = accountable human decider; R = responsible executor; C = consulted.**

| Decision | A | R | C | Authoritative record |
|---|---|---|---|---|
| Repo-local reversible implementation | Project Maintainer | AK assignee/agent | relevant reviewers | AK task, owner tests/evidence |
| Product ordering within accepted posture | Product Owner | Maintainer/agent | Service Owner if affected | AK direction/task links |
| Service operation within agreed limits | Service Owner | operator/agent | Product Owner | owner runbook plus AK task/evidence |
| Start a new product/service, transfer it across domains, merge products, or permanently retire a company commitment | Softwareco Org Owner | Product/Service Owner | affected owners/users | AK decision plus narrative rationale |
| Routine pause/resume, sequencing, or lifecycle adjustment inside an accepted product posture and delegation | Product Owner | maintainer/agent | Service Owner if operational impact exists | AK direction/task/owner evidence |
| Change domain scope or accountable owner | Softwareco Org Owner | Domain Owner | affected owners | AK decision/delegation record |
| Cross-repo coordination | relevant Domain/Product Owner | source-owner maintainers | FCOS/Org Owner as needed | FCOS item referencing AK/source facts |
| Architecture-significant or authority-changing change | relevant human owner | decision-support contributors | affected owner surfaces | AK decision + RFC/review/ADR chain |
| Release/promotion | Product or Service Owner under delegated policy | release operator/agent | security/runtime owner | source-owner release evidence |
| Incident containment | Service Owner or delegated Incident Lead | responders/agents | Product Owner and affected owners | incident record plus AK evidence where accepted |
| Ontology/semantic change | ROCS/ontology owner | semantic contributors | consumers | ROCS owner workflow |
| Reusable procedure change | Prompt Vault owner | author/reviewer | consumers | Prompt Vault governance |
| Empirical behavior conclusion | DSPx/Oracle owner | analysts/agents | affected owners | empirical artifact; advisory to decisions |

## Impact tiers

### Tier 0 — delegated local change

Reversible, repo-local, no durable authority or shared-contract effect. Use AK task scope and owner tests.

### Tier 1 — architecture-significant

Changes authority, shared contracts, lifecycle legality, privacy/security posture, cross-repo behavior, or durable product commitments. Requires problem/evidence, RFC, immutable review attempt(s), a controlling synthesis bundle when parallel review is used, ADR, execution/validation/rollback plan, and evidence.

### Tier 2 — constitutional or multi-company

Changes society-level governance, fundamental rights/consent, or multi-company boundaries. Escalate to the appropriate Holdingco/AI Society owner; Softwareco cannot authorize it alone.

## Proposed operating cadence

| Cadence | Purpose | Required output |
|---|---|---|
| Continuous | Intake, incident handling, evidence capture | owner-native state updates |
| Weekly | Active flow, WIP, blockers, promotions | stop/defer/escalate/continue actions in AK/source owners |
| Monthly | Product/service outcomes and portfolio choices | continue/stop/redirect/complete and capacity decisions |
| Quarterly horizon | Direction, domain health, vertical bets, sustainability | AK direction/decision updates and explicit non-goals |
| After incident or surprising rollout | Learn and improve | evidence, corrective owner action, KES disposition |

Meetings are not authority. Decisions update the owning runtime or source surface during or immediately after the review.

## FCOS and AK boundary

- Use **AK** for repo-local direction, tasks, decisions, evidence, contracts, and accepted runtime facts.
- Use **FCOS** only for genuinely cross-repo control-board coordination, gates, and handoffs.
- An FCOS item identifies source-owner execution; it does not become a duplicate task queue.
- Markdown explains rationale and policy; it does not replace live AK or FCOS state.

## Incidents

1. Protect people, data, and service integrity first.
2. The Service Owner or delegated Incident Lead may contain, disable, roll back, or isolate within the incident delegation.
3. Record impact, timeline, decisions, evidence, and residual risk.
4. Notify affected owners and users proportionately.
5. Restore or forward-recover through the source-owner runbook.
6. Reconcile emergency actions into canonical records.
7. Conduct a learning review focused on system improvement, not blame.

## Exceptions

Exceptions must be explicit, bounded, and expiring. Record:

- rule being waived;
- driver and evidence;
- accountable approver;
- affected people/systems;
- risk and containment;
- expiry/review date;
- exit or rollback plan.

An exception cannot silently transfer authority or waive law, consent, privacy, licensing, or non-negotiable ethics boundaries.

## Objections and appeals

A reasoned objection is information about risk or unmet need, not disloyalty. The accountable owner must either resolve it, show why the concern is already addressed, or escalate it. People affected by consequential software must have a discoverable appeal or human review path proportionate to impact.

## Canonical references

- [[holdingco/governance-kernel/docs/dev/decision-lifecycle.md|Decision Lifecycle]]
- [[holdingco/governance-kernel/docs/core/definitions/s3-governance-semantics.md|S3.0 Governance Semantics]]
- [[holdingco/governance-kernel/docs/core/definitions/runtime-authority-matrix.md|Runtime Authority Matrix]]
- [[softwareco/owned/agent-kernel/docs/project/direction-to-execution-model.md|Direction-to-Execution Model]]
- [[holdingco/fcos-control-board/docs/project/authority-boundary.md|FCOS Authority Boundary]]
