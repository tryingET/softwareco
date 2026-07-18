---
summary: "RFC proposing a federated Softwareco Factory Flow Protocol over existing AI Society authority and execution surfaces."
read_when:
  - "Reviewing how Softwareco should become an operated, outcome-driven software factory."
  - "Deciding whether to pilot a company-wide flow from demand through operation and learning."
type: "rfc"
system4d:
  container:
    boundary: "Company operating protocol across existing owner surfaces; no new platform, scheduler, database, or universal authority."
    edges:
      - "[Problem/intent](2026-07-12-software-factory-operating-system-problem-intent.md)"
      - "[Evidence](2026-07-12-software-factory-operating-system-evidence.md)"
      - "[AI Society convergence architecture](../../owned/agent-kernel/docs/project/ai-society-convergence-architecture.md)"
      - "[Decision lifecycle](../../../holdingco/governance-kernel/docs/dev/decision-lifecycle.md)"
  compass:
    driver: "Make Softwareco repeatedly convert real demand into safely operated, measurable outcomes."
    outcome: "One paved value stream with accountable selection, finite WIP, owner-native execution, safe promotion, and evidence-driven steering."
  engine:
    invariants:
      - "AK remains canonical for direction, tasks, decisions, evidence, and lineage."
      - "FCOS is used only when cross-repo control-board coordination is required."
      - "Engineering completion, release completion, and outcome realization remain distinct facts."
      - "Every committed flow has an accountable outcome owner, finite WIP, and a terminal continue/stop/redirect decision."
  fog:
    risks:
      - "Protocol ceremony could outgrow delivered value."
      - "A dashboard or projection could become a shadow authority."
      - "Metrics could reward throughput while hiding poor outcomes."
      - "Company standardization could erase product-specific delivery needs."
---

# RFC — Softwareco Factory Flow Protocol

## Status

- status: draft
- date: 2026-07-12
- accountable authority: current higher-level human operator for this bounded decision
- proposed post-ADR technical steward: Softwareco CTO Agent under revocable bounded delegation; pre-ADR work is limited to scoped packet preparation under task `#4028`
- selected pilot: safe evidence-preserving retirement of `softwareco/owned/fcos-proving-lane`
- reviewers: four first-cycle adversarial tracks completed; tracked revised-cycle review pending
- decision_deadline: after a tracked revision receives a controlling `ready_for_adr` review synthesis
- supersedes_revision: initial worktree SHA-256 `31e194ea9b77dc439a7f9b1b9ad1dac3e92fc7ca981b3c9a3c2888a04d1cb298`
- revision_driver: `docs/reviews/2026-07-12-software-factory-rfc-v0-synthesis.md` (`revise_rfc`)
- lifecycle tier: Tier 1 architecture-significant
- related_docs:
  - `docs/project/2026-07-12-software-factory-operating-system-problem-intent.md`
  - `docs/project/2026-07-12-software-factory-operating-system-evidence.md`
  - `docs/project/2026-07-18-factory-flow-pilot-fcos-proving-lane.md`
  - `docs/project/2026-07-18-factory-flow-pilot-operator-packet.md`
  - `~/ai-society/holdingco/governance-kernel/docs/dev/decision-lifecycle.md`
  - `owned/agent-kernel/docs/project/ai-society-convergence-architecture.md`

## Executive summary

Softwareco already has strong engineering, governance, execution, infrastructure, evidence, and learning components. It lacks a routinely operated company loop connecting demand, discovery, finite commitment, owner-repo delivery, safe promotion, service operation, outcome evidence, and changed direction.

This RFC proposes a **Factory Flow Protocol**: a small federated operating contract over existing owner surfaces. It does not create another platform or database. AK remains canonical for direction/tasks/decisions/evidence; FCOS coordinates only genuinely cross-repo concerns; product and service owners execute in their repositories; Pi provides execution; KES and DSPx handle learning and empirical analysis through their existing boundaries.

The requested decision is whether this protocol is precise and safe enough to become the basis for an ADR authorizing one bounded **internal retirement-corridor pilot**—not factory-wide rollout. This first pilot can prove preservation, authority, WIP, packet, recovery, and outcome-review behavior; it cannot by itself prove normal product discovery-to-operated-outcome delivery.

## Vocabulary preflight

The following terms are RFC-local and **incubating**, not newly governed ROCS vocabulary:

| Term | Kind | Meaning in this RFC | Owner surface | Status / retrieval source | Semantic reference | Promotion required now? |
|---|---|---|---|---|---|---|
| Factory Flow Protocol | process label | The cross-owner operating contract proposed here | Softwareco decision artifacts | incubating; this RFC | none | no; pilot label only |
| flow | projection concept | Traceable chain from demand signal to outcome decision | owner-native records, rendered by Softwareco packet | incubating; this RFC | direction-to-execution model | no; must not become runtime state |
| committed flow | classification | Flow with owner, preregistered outcome, finite capacity, and canonical carriers | AK direction/decision plus source-owner facts | incubating; this RFC | AK direction-to-execution | no for pilot projection; yes before machine-governed token use |
| promotion | operational event label | Verified artifact/configuration moved into an operated environment with readback and recovery evidence | release/runtime owner | local/common term; owner release contract | runtime/service owner docs | no central promotion; owner contract remains authoritative |
| outcome review | decision event label | Accountable terminal decision using technical and product evidence | AK decision when the decision changes company commitment; source-owner decision for local product choices | incubating composition; this RFC | AK decision lifecycle | no for pilot; cross-repo governed tokenization requires owner review |
| work class | classification family | Exploration, committed flow, operational exception, or maintenance obligation | protocol projection only | incubating; this RFC | none | yes before machine-enforced cross-repo use |
| terminal decision | closed decision-token family | `continue`, `stop`, `redirect`, or `complete` | AK decision for company commitment; source-owner decision if purely local | incubating; this RFC | AK decision lifecycle | yes before machine-enforced token use |

No term in this table may be added to AK, FCOS, ROCS, or a machine schema merely because it appears here. If accepted terminology needs cross-repo governed meaning, promotion must route through its owner surface, using ROCS for semantics where applicable.

## Problem statement

Softwareco's strongest standards apply after work selection. Its weakest links are:

- accountable company direction;
- comparable demand intake and discovery;
- portfolio choice and finite capacity allocation;
- a single operator path across owner surfaces;
- common release/promotion evidence;
- service ownership and reliability expectations;
- product-outcome measurement;
- a cadence that changes direction based on evidence.

The failure is systemic: each component can work locally while the end-to-end value stream remains unowned.

## Goals and non-goals

### Goals

1. Establish one paved operating path from demand to outcome decision.
2. Make company commitments finite, comparable, owned, and visible.
3. Preserve owner-native execution and authority boundaries.
4. Distinguish discovery, commitment, engineering completion, promotion, operation, and outcome realization.
5. Require safe promotion and minimum operational ownership for delivered services.
6. Turn evidence into explicit continue/stop/redirect decisions.
7. Prove the protocol through one bounded pilot before broader adoption.
8. Keep protocol overhead proportional to risk and cross-repo complexity.

### Non-goals

- Building a new factory platform, database, scheduler, workflow engine, or universal dashboard.
- Replacing AK, FCOS, ROCS, Prompt Vault, Pi, KES, DSPx, or source-owner repositories.
- Defining one identical CI/CD stack for all languages and products.
- Centralizing all product decisions at Softwareco root.
- Treating every experiment as committed delivery work.
- Declaring existing products production-ready.
- Authorizing an ADR or implementation through this RFC alone.

### Invariants that must not break

- **Authority:** AK remains canonical for direction, tasks, decisions, evidence, and lineage.
- **Coordination:** FCOS is required only for cross-repo control-board concerns; it must not become a duplicate repo task queue.
- **Semantics:** ROCS remains semantic authority.
- **Execution:** Pi/ASC/orchestrator execute work but do not gain canonical society-state authority.
- **Learning:** KES crystallization and DSPx empirical analysis do not become decision authority.
- **No shadow state:** protocol views and reports must be derived from or link to owner-native facts.
- **Finite commitment:** every committed flow has explicit WIP/capacity allocation.
- **Outcome separation:** passing CI, deploying successfully, and improving an outcome are separate evidence claims.
- **Reversibility:** the pilot can stop without migrating canonical state or disabling existing repo workflows.

## Current-state evidence

The accompanying evidence note records:

- a broad component ecosystem;
- zero Softwareco AK direction nodes at review time;
- placeholder company purpose/vision/governance/ownership docs at initial evidence capture; narrative placeholders were later overhauled, while accepted owner appointment and AK direction activation remain open gates;
- strong engineering-core adoption across owned repos;
- no evidenced common company promotion and service-operation contract;
- an architecture requirement not to add a competing authority layer;
- a completed Transcendent adversarial design loop whose closure recommendation was RFC-ready, not implementation-ready.

## Work recognition rule

Softwareco should recognize work through one **primary admission class**:

1. **Operational exception:** incident, security response, or urgent reliability work. This class has precedence at admission and enters through the owning incident/exception path. It consumes capacity and requires retrospective reconciliation within two working review cycles.
2. **Maintenance obligation:** recurring or bounded work required by an accepted service, contract, security posture, or dependency. It is admitted against a named obligation and reserved capacity.
3. **Exploration:** time-bounded learning with no delivery promise. It states question, owner, timebox, capacity consumed, evidence plan, and terminal decision.
4. **Committed flow:** finite company/product commitment with outcome owner, preregistered outcome, capacity allocation, canonical carriers, promotion/operation posture, and review date.

Precedence resolves overlap at admission: exception > maintenance > exploration > committed flow. A record may link to other concerns, but only its primary class counts for load and cadence. Reclassification requires an owner-native decision and preserves the previous classification as history.

All four classes consume total capacity. “Committed-flow WIP” is therefore never reported without exception, maintenance, and exploration load beside it. Unclassified personal/local activity must not be presented as a Softwareco commitment.

The closed terminal-decision set is:

- `continue`: retain the current commitment and next review horizon;
- `stop`: end commitment without replacement direction;
- `redirect`: end the current approach and link a newly framed direction/decision;
- `complete`: intended bounded outcome and obligations are satisfied.

Supersession is represented as `redirect` with a link to the replacement. Service retirement is `stop` plus owner-native retirement evidence. These are RFC-local pilot labels, not a proposed AK state machine.

## Proposed protocol

### Protocol view

```text
Signal
  -> Discovery
  -> Commitment
  -> Delivery
  -> Promotion
  -> Operation
  -> Outcome review
  -> Learning / next decision
```

These are protocol checkpoints, not new canonical lifecycle states. Each checkpoint links to existing owner-native facts.

### Required flow contract

Every committed flow must make the following fields discoverable:

| Field | Requirement | Canonical owner |
|---|---|---|
| demand/problem evidence | Link to user, operational, strategic, incident, or research evidence | source owner; AK evidence when promoted |
| intended outcome | Measurable change, target, horizon, and guardrail | AK direction plus linked AK evidence; controlling change in an AK decision |
| outcome owner | One accountable role/person with delegated decision rights | appointment/delegation evidence linked from AK direction/decision |
| product/service owner | Owner of implementation and operated behavior | source-owner repo/governance |
| work class | exploration, committed flow, operational exception, or maintenance obligation | protocol projection over owner facts |
| capacity/WIP | Explicit finite allocation and competing commitment displaced or deferred | AK capacity-admission decision linked to active direction |
| execution carriers | Exact AK tasks/decisions and source-owner paths | AK/source owner |
| cross-repo coordination | FCOS item only when required | FCOS |
| promotion evidence | artifact/version, environment, validation, health/readback, rollback | release/runtime owner; linked into AK evidence |
| service posture | owner, health check, reliability target, incident and restore path where applicable | runtime/service owner |
| outcome evidence | technical and user/product measures with timestamp | source owner; linked into AK evidence |
| terminal decision | `continue`, `stop`, `redirect`, or `complete` | controlling AK decision when company commitment changes; source-owner decision only when effect is purely local |
| learning route | mandatory diary/learning closure for every pilot counted toward protocol adoption or propagation | KES/source owner |

The pilot should initially implement this as a human-readable linked packet plus owner-native records. A machine schema may be proposed later only if repeated operation proves the need and ROCS/AK owner reviews approve it.

### Canonical authority and decision rights

The pilot must use the following deterministic authority rules. If an exact existing command or record type is unavailable, the pilot cannot be authorized until the owning authority records a specific delegation/agreement through its accepted decision surface. The packet can never supply missing authority.

| Concern | Canonical record for pilot | May decide/change | Consulted or veto boundary |
|---|---|---|---|
| company strategic outcome and commitment | AK direction/decision | human operator accepts/revokes; CTO Agent prepares and stewards within delegation | source owners and affected users; no agent unilateral acceptance |
| outcome definition and acceptance | AK evidence plus controlling AK decision when company commitment changes | human operator accepts; CTO Agent gathers evidence and recommends | source owner supplies evidence; human resolves commitment consequence |
| product implementation | owner-repo AK tasks/decisions and source | product/service owner | runtime/release owner may veto unsafe promotion |
| capacity admission/displacement | post-ADR AK decision/direction linkage | human operator; CTO Agent may recommend and enforce accepted WIP | affected owners must be recorded; incident authority may pre-empt temporarily |
| cross-repo coordination | FCOS native board item | FCOS concern owner under FCOS rules | participant repos retain native implementation facts |
| promotion | release/runtime owner record | named release authority | service owner or incident authority may abort |
| incident override | owner incident record | named incident commander | retrospective portfolio reconciliation required |
| service retirement | source-owner decision, linked to AK if company commitment changes | service owner plus portfolio steward for company effect | users/support and data-retention owners consulted |
| learning promotion | KES/source-owner process | learning owner | no effect on runtime authority without separate owner action |

The pilot-selection packet records the human operator's selection and proposes the Softwareco CTO Agent as a bounded post-ADR technical steward. Before ADR acceptance, the agent holds no durable company role; it only prepares the decision packet under scoped AK task `#4028`. Human ADR acceptance activates the proposed revocable pilot delegation, which excludes destructive retirement, company portfolio authority, and residual human accountability. Post-ADR source-owner tasks must name their own maintainer/release/incident authorities before mutation.

Conflict order is: safety/security incident authority for immediate containment; release/runtime owner for promotion safety; product/service owner for implementation facts; outcome owner for evidence interpretation; portfolio steward for company commitment/capacity. Disputes that alter authority, policy, or durable commitments require an AK decision membrane. No meeting note or protocol packet breaks a tie.

### Projection membrane for the manual packet

The packet is a derived coordination view and must contain:

- packet ID and revision timestamp;
- exact canonical record URI/path/ID for every decision-bearing field;
- source revision or evidence timestamp;
- freshness expectation per field;
- named reconciliation owner;
- explicit stale/conflict status;
- immutable history of prior packet revisions.

Packet-only mutation of commitment, capacity, task state, promotion, incident, or terminal decisions is prohibited. On disagreement, the canonical owner record wins. “Fail closed” means the packet cannot authorize a new commitment, promotion, or closure until reconciled; it must not block emergency containment or rollback. Reconciliation updates the owner-native record first and then regenerates the packet.

## Operating cadence

### Continuous

- route new signals to the responsible product/service owner;
- handle operational exceptions immediately through owner runbooks;
- keep blocked work and promotion failures visible.

### Weekly flow review

Purpose: manage flow, not redesign strategy.

Required questions:

- Which committed flows are active?
- Which are blocked, aging, or exceeding WIP?
- What entered as an exception?
- What is ready for promotion or outcome review?
- What must stop or be deprioritized to preserve finite capacity?

Outputs must update owner-native AK/FCOS/source-owner state rather than a parallel meeting ledger.

The pilot steward convenes the review; outcome and product/service owners are required for decisions affecting their domains. Missing required evidence permits blocker triage but not commitment, promotion, or closure. Decisions are recorded during the review in owner-native surfaces. Unresolved disagreements escalate through the authority matrix above.

### WIP, total load, and the constraint

For the pilot, the WIP unit is **one active flow competing for the pilot's named constrained resource**. Gate 1 must name:

- the constrained resource or queue (for example outcome-owner attention, release capacity, test environment, or specialist execution capacity);
- its available slots or time budget for the review horizon;
- reserved maintenance capacity;
- exception/expedite policy and maximum expedite count;
- exploration budget;
- committed-flow limit;
- the actor allowed to admit, displace, expedite, or stop work.

Total load is reported as all four admission classes against that same constraint. Adding work over the limit requires an AK-recorded displacement decision or incident override. The pilot preregisters a constraint hypothesis and one observable buffer signal (queue age, blocked age, utilization window, or promotion backlog). Each weekly review asks whether evidence indicates the constraint moved; changing the named constraint requires an owner-native decision, not retrospective metric editing.

For competing admission candidates, the portfolio steward records a comparison across expected outcome value, urgency/cost of delay, risk reduction or opportunity enablement, estimated constrained-resource consumption, confidence/evidence strength, reversibility, and the named alternative displaced. The comparison supports judgment; it is not a universal numeric score or automatic priority algorithm.

### Monthly portfolio and outcome review

Purpose: choose and steer commitments.

Required decisions:

- continue;
- stop;
- redirect;
- promote an exploration into a committed flow;
- retire or sustain an operated service;
- change capacity allocation.

### Horizon review

Review company direction, product/service portfolio, capacity allocation, and systemic constraints. The cadence may be quarterly initially but should be evidence-driven rather than calendar ceremony.

## Minimum release and service contract

A flow that changes an operated product or service cannot close merely because code merged or tests passed.

### Promotion evidence

At minimum:

- immutable artifact or exact source/config revision;
- target environment;
- validation result;
- deployment/promotion receipt;
- health or readback verification;
- rollback mechanism and authority.

### Service posture

For an operated service, at minimum:

- accountable owner;
- user/support boundary;
- environment and current version discovery;
- health/readiness path;
- reliability target appropriate to impact;
- incident/escalation path;
- backup/restore expectation where stateful;
- rollback or containment path.

Products that are prototypes or local tools may declare a lighter posture only when they have no external dependents, no durable user data, no privileged/security-sensitive effect, and a fixed expiry/review date. Crossing any boundary triggers reclassification before further promotion.

### Operational risk tiers

| Tier | Typical impact | Minimum acceptance evidence |
|---|---|---|
| R0 — exploration | no operated dependency or durable user data | exact revision, bounded test evidence, expiry, cleanup path |
| R1 — local/reversible | single operator or easily restored local state | validation, observable readback, named rollback actor, tested rollback command/path |
| R2 — shared/stateful | multiple users, shared service, or durable data | R1 plus SLI/health signal, observation window, incident owner, backup/restore or migration recovery proof, stated RTO/RPO where relevant |
| R3 — critical/security-sensitive | material safety, privacy, security, or society-control impact | separate owner risk review and rollout/rollback plan; this pilot RFC alone cannot authorize it |

Gate 1 must classify the pilot. Promotion has explicit go/no-go authority, abort criteria, observation window, and blast-radius boundary. For irreversible migrations, the plan must define forward recovery and data reconciliation; a binary rollback claim is not accepted. At least one rollback or recovery path must be rehearsed before pilot closure.

## Measures

### Flow measures

- demand-to-commitment time;
- commitment-to-first-operated-release time;
- blocked age;
- active committed-flow count versus WIP limit;
- promotion success/rollback rate;
- time from promotion to outcome decision.

### Outcome measures

Each flow defines one primary outcome and guardrails. Examples include:

- user task success;
- adoption or retained use;
- quality/reliability improvement;
- operator time saved;
- incident reduction;
- validated learning that causes a stop/redirect decision.

### System-health measures

- percentage of committed flows with complete required contract fields;
- percentage with explicit terminal decision;
- percentage of operated services with minimum service posture;
- evidence freshness;
- number of shadow/unlinked trackers discovered;
- protocol overhead as a proportion of flow lead time.

Targets for broad adoption must be set from pilot baselines, not invented in this RFC.

Before commitment, the pilot freezes a measurement registration containing: customer/internal-user segment, observed problem and current workaround, primary outcome, baseline and source, target or decision threshold, horizon, guardrails, sampling method, immutable start/stop events, and stop/redirect rule. Changes require a dated decision and preserve the original registration.

Clock events are defined as canonical evidence timestamps: demand clock starts at the first accepted evidence record; commitment starts at the capacity-admission decision; operated release starts at successful promotion readback; outcome-review time ends at the controlling terminal decision. The review reports medians/raw values rather than a single vanity aggregate and records reclassification, paused time, exceptions, and missing data. Metric improvement without guardrail health is not success.

## Options considered

### Option A — Continue decentralized evolution

**Description:** Keep improving AK, FCOS, templates, and repo practices independently; rely on operator judgment to connect them.

**Pros:**

- no new protocol burden;
- maximum local flexibility;
- no transition cost.

**Cons:**

- selection and outcome accountability remain implicit;
- local completion continues to substitute for company outcomes;
- operator knowledge remains the integration layer.

**Risk:** more sophisticated components increase coordination complexity without improving end-to-end flow.

### Option B — Build a centralized factory platform

**Description:** Create a new service/database/dashboard that owns intake, portfolio, workflow, releases, metrics, and learning.

**Pros:**

- potentially unified UI;
- strong apparent standardization;
- easier centralized reporting.

**Cons:**

- duplicates AK/FCOS/source-owner authority;
- creates a large integration and migration program;
- centralizes failure and encourages dashboard truth over runtime truth;
- delays real product delivery.

**Risk:** the factory becomes the main product and Softwareco ships less.

### Option C — Federated Factory Flow Protocol over existing owners (preferred)

**Description:** Standardize required cross-owner facts, checkpoints, cadence, and terminal decisions while preserving existing authorities and repo-native execution.

**Pros:**

- attacks the missing connective tissue directly;
- low migration risk;
- compatible with current architecture;
- can be piloted manually and automated only after evidence;
- reversible.

**Cons:**

- initially depends on disciplined operation;
- operator experience may remain fragmented until a derived front door matures;
- requires clear accountability and willingness to stop work.

**Risk:** the protocol becomes documentation theater unless coupled to WIP limits, releases, outcome decisions, and owner-native updates.

### Option D — Single-product factory first

**Description:** Ignore company-wide protocol design and perfect one product's lifecycle before generalizing.

**Pros:**

- direct empirical grounding;
- minimal scope;
- faster local learning.

**Cons:**

- may encode one product's peculiarities as company policy;
- does not resolve company portfolio and capacity decisions;
- cross-repo owner boundaries may remain untested.

**Risk:** successful local practice fails to transfer.

**Use in preferred direction:** Option D is incorporated as the rollout strategy for Option C: define the minimal protocol, then test it through one product/value stream.

## Proposed direction

Adopt Option C as the proposed architecture and Option D as its proving method.

The stable core is only:

1. work classification;
2. accountable outcome ownership;
3. finite commitment/WIP;
4. links to owner-native facts;
5. promotion and service evidence when applicable;
6. explicit outcome review and terminal decision;
7. learning/next-action closure.

Everything else—UI, automation, schemas, metric pipelines, templates—is an adapter or later optimization and must earn its existence through pilot evidence.

## Pilot boundary

The pre-ADR pilot-selection evidence is recorded in `docs/project/2026-07-18-factory-flow-pilot-fcos-proving-lane.md`. It identifies:

- AI Society operators/maintainers as the internal-user segment;
- direct operator confusion between `fcos-control-board` and `fcos-proving-lane`;
- a memory- and archaeology-dependent current workaround;
- repository evidence: 48 dirty status entries, no direction nodes, one generic ready task, and no substantive product implementation;
- safe evidence-preserving retirement as the smallest intervention;
- rejected keep/merge/delete alternatives;
- human-reserved accountability, CTO-Agent delegation, and R2 risk classification.

The first pilot must include:

- one evidence-backed real product or internal service outcome;
- one accountable outcome owner and one product/service owner;
- one time-bounded discovery or already-evidenced problem;
- one finite commitment with an explicit WIP limit;
- at least one owner-repo AK execution carrier;
- one FCOS item only if the pilot is genuinely cross-repo;
- one operated release or an explicit non-deployment learning outcome;
- one outcome review;
- one `continue`, `stop`, `redirect`, or `complete` decision;
- one mandatory learning closure. No pilot may count toward adoption or propagation without crystallized learning; failure, `stop`, `redirect`, or insufficient evidence also require learning capture.

It must not include:

- company-wide migration;
- new canonical storage;
- automatic ingestion from every repo;
- a new universal state machine;
- mandatory uniform CI/CD tooling;
- broad template propagation before pilot evidence.

## Rollout and migration plan

### Gate 0 — RFC legality

- problem and evidence notes exist;
- multi-perspective review attempts target this exact RFC revision;
- synthesis emits `ready_for_adr`, `revise_rfc`, or `reject_current_direction`;
- no implementation authority exists before an accepted ADR.

### Gate 1 — Pre-ADR accountability and selected pilot

Before an ADR may authorize pilot launch:

- record the human-reserved authority and revocable CTO-Agent delegation;
- select the evidence-backed pilot and R2 risk tier;
- preregister outcome, baseline, guardrails, stop/redirect thresholds, WIP, and deferred alternatives;
- provide the worked operator packet;
- track the exact RFC/addendum/packet revision and obtain controlling review closure.

This gate reserves no execution capacity and creates no active strategic frame before the ADR.

### Gate 2 — Post-ADR direction and canonical carriers

- create/activate one bounded Softwareco AK strategic frame;
- create an implementation wave only if grouping materially helps;
- record capacity admission and displaced/deferred work;
- create one source-owner AK task with explicit scope;
- create an FCOS item only if a genuine multi-owner gate appears;
- bind the linked packet to exact canonical IDs and establish baseline measures.

### Gate 3 — Delivery and promotion

- execute in owner repos;
- capture validation and promotion evidence;
- verify health/readback and rollback;
- do not claim outcome success at deployment time.

### Gate 4 — Outcome review

- gather technical and product/user evidence;
- make explicit continue/stop/redirect decision;
- close or reshape canonical work accordingly;
- capture learning.

### Gate 5 — Protocol evaluation

Review:

- whether the pilot improved clarity and lead time;
- protocol overhead;
- missing or redundant fields;
- authority drift or shadow-state incidents;
- whether another pilot is justified.

Only after at least two materially different successful pilots should template propagation or machine-readable protocol schemas be proposed. A countable pilot requires protocol conformance, effectiveness `improved`, canonical terminal decision, cold-start and drift/recovery evidence, overhead evidence, and mandatory learning crystallization. The second pilot must be human-facing. Even then, propagation is only eligible for a separate template-owner proposal, preview/migration plan, validation, and rollback decision; it is never automatic L1-to-L0 mutation.

## Rollback and escape hatch

Rollback is split into four independent families:

| Family | Trigger and authority | Required response/evidence |
|---|---|---|
| protocol rollback | overhead, ambiguity, or shadow-state trigger; portfolio steward | stop active packet use, retain history, reconcile canonical records, unwind cadence/WIP reservations and delegated pilot roles |
| release rollback/containment | abort criteria or degraded readback; release authority or incident commander | contain blast radius, execute tested rollback/kill path, verify readback, record receipt |
| state/data recovery | integrity loss, failed migration, or restore need; service/data owner | execute restore or forward-recovery plan, verify integrity, record RTO/RPO result and residual risk |
| organizational unwind | pilot stop/redirect; portfolio steward | restore or explicitly reallocate displaced commitments, close delegation, notify affected owners/users, preserve decision history |

Each pilot plan names trigger thresholds, commander, maximum decision/recovery time, blast-radius boundary, dependencies, and reconciliation owner. Emergency containment remains available if normal AK/FCOS views are stale or unavailable; canonical records are reconciled afterward.

Rollback must not delete valid task, decision, release, incident, or evidence history.

## Validation plan

### Documentation validation

```bash
node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs . --strict
```

### Review validation

- run independent architecture, operations/flow, and governance/adoption review attempts;
- synthesize them against the exact RFC revision;
- require explicit outcome and legal next move.

### Pilot validation

Validation reports two independent verdicts.

**Protocol conformance** passes only if:

- all required fields link to owner-native facts with packet identity/freshness;
- no new canonical database or shadow task/decision state exists;
- authority, WIP/load, constraint hypothesis, and measurement registration are explicit;
- risk-tier promotion/service evidence meets its thresholds;
- one outcome review produces a canonical terminal decision;
- protocol, release, recovery, and organizational escape paths are evidenced.

**Pilot effectiveness** is `improved`, `not_improved`, or `insufficient_evidence` against the frozen primary outcome and guardrails. A conformant pilot may still be ineffective. Only `improved` counts toward the two-pilot propagation gate; `not_improved` and `insufficient_evidence` must produce stop/redirect decisions.

Operator adoption also requires:

- a worked example packet and command/path guide;
- one cold-start operator who did not author the RFC can locate canonical facts, update one permitted fact, detect one stale/conflicting field, and identify escalation without private coaching;
- packet preparation/update effort is recorded; if protocol overhead exceeds 10% of observed pilot lead time or two hours per weekly review, whichever is lower, continuation requires an explicit exception decision;
- one injected drift or recovery exercise is completed.

### Factory-level success criteria

The proposal should not be called factory-wide successful until repeated pilots demonstrate:

- shorter or at least explainable demand-to-outcome lead time;
- fewer unowned or indefinitely active commitments;
- explicit stop/redirect decisions, not only completions;
- reliable promotion/readback/rollback evidence;
- operated-service ownership visibility;
- evidence-driven changes to portfolio or standards;
- no material authority duplication.

## Risk register

| Risk | Trigger | Mitigation | Rollback |
|---|---|---|---|
| Ceremony exceeds value | packet upkeep materially delays flow | minimal fields; measure overhead; delete optional sections | stop protocol use after pilot |
| Shadow authority emerges | protocol packet disagrees with AK/FCOS/source owner | links only; fail closed on drift; owner-native facts win | freeze packet as history |
| Metrics are gamed | throughput rises while outcomes or reliability fall | pair flow metrics with outcome and guardrail measures | retire misleading metric |
| WIP limit is ignored | new commitments enter without displacement decision | weekly review must stop/defer something before adding commitment | suspend new commitments |
| Central steward bottleneck | ordinary product decisions wait on company review | delegate product decisions; centralize only portfolio/cross-repo constraints | narrow steward domain |
| FCOS becomes duplicate task queue | repo-local leaves appear as board work | require cross-repo test for FCOS entry | return execution to AK/source owner |
| One pilot overfits policy | later product cannot use the protocol | require two different pilots before propagation | keep protocol pilot-only |
| Release contract excludes prototypes | experiments incur production ceremony | explicit exploration/prototype classification | reclassify and timebox |
| Outcome evidence unavailable | flow closes on deployment alone | define proxy and evidence plan before commitment; allow stop for insufficient evidence | close as learning, not success |
| Automation arrives too early | schema/dashboard work begins before repeated use | Gate 5 forbids propagation/automation without pilot evidence | abandon adapter work |

## Adversarial objections

### “This is management bureaucracy disguised as architecture.”

Valid if the protocol merely adds documents. The proposal survives only if finite WIP, owner-native updates, promotion evidence, and terminal outcome decisions change behavior. Overhead is itself a measured failure condition.

### “AK should simply implement all of this.”

AK should remain canonical for the concerns it owns, but product discovery, release semantics, service operation, and source-owner facts do not become AK-owned by convenience. A future AK feature requires its own evidence and owner decision.

### “FCOS is already the portfolio.”

FCOS supplies the cross-repo control-board product. The missing part is Softwareco's operated portfolio content, accountable cadence, capacity decisions, and linkage to outcomes—not another board implementation.

### “A single operator can coordinate this informally.”

Informal coordination does not scale across agents, sessions, products, or time. The protocol preserves the smallest durable facts needed for continuity without attempting to encode every judgment.

### “Optimize coding throughput first.”

Engineering-core adoption and extensive tooling suggest coding discipline is not the dominant systemic constraint. Increasing local throughput before improving selection and outcome feedback can accelerate waste.

### “Company-wide standards will destroy autonomy.”

The protocol standardizes cross-boundary facts and decision obligations, not implementation stacks. Product owners retain local execution choices within shared safety and evidence constraints.

### “You cannot measure outcomes for research or infrastructure.”

Not every outcome is revenue or user adoption. Valid outcomes include reduced recovery time, validated technical feasibility, a decision to stop, improved reliability, or removed uncertainty—provided the measure and decision are explicit.

## Open questions

Resolved for this revision:

1. The current higher-level human operator retains appointment, revocation, ADR acceptance, irreversible retirement, and terminal-decision authority; the Softwareco CTO Agent is a bounded technical delegate.
2. The first pilot is safe evidence-preserving retirement of `fcos-proving-lane`.
3. Capacity is admitted only after ADR through AK direction/decision linkage; FCOS gains no capacity authority.
4. Review closure uses independent architecture/authority, flow/measurement, product/accountability, and operations/adoption tracks plus one controlling synthesis.

Still open beyond the first pilot:

- What minimum evidence should qualify a non-deployed exploration across future product archetypes?
- Which release/runtime evidence should become a reusable company contract after two materially different pilots?
- Which human-facing product should serve as the required materially different second pilot?

## Decision requested

Reviewers must decide whether to:

1. approve Option C as the basis for an ADR authorizing one bounded pilot;
2. request revision because ownership, contracts, evidence, or rollback remain too weak;
3. reject the protocol and retain decentralized evolution; or
4. request additional evidence before selecting a direction.

The RFC specifically does **not** request approval for factory-wide rollout, schema creation, template propagation, or a new platform.

## Follow-through

If the latest controlling review synthesis returns `ready_for_adr`, create a follow-up ADR limited to the first pilot. Then create implementation, validation, rollout, and rollback artifacts linked to that ADR.

If review returns `revise_rfc`, revise this RFC and conduct a new immutable review cycle.

If review returns `reject_current_direction`, close or reframe the proposal without opening an ADR for this direction.
