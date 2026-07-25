---
summary: "Softwareco operating model and navigation hub: identity, lanes, ownership, flow, cadence, authority, and AI Society architecture links."
read_when:
  - "Starting company-level Softwareco work or onboarding an operator or agent."
  - "Deciding where a concern belongs and which canonical architecture documents to read."
  - "Reviewing how Softwareco turns direction into products, services, evidence, and learning."
type: "reference"
status: "accepted_preactivation"
as_of: "2026-07-25"
decision_id: 74
mito_layers:
  - "Strategic"
  - "Design & Configuration"
  - "Implementation"
  - "Operations & Evaluation"
---

# Softwareco operating model

## Identity

Softwareco's constitutional role is **AI Society's product-engineering company**. It builds software and, where owner and runtime evidence prove support, operates capabilities through which AI Society becomes useful. The portfolio named here is direction and routing context, not a claim that every journey is currently supported.

Its posture is:

- platform first, proved through selected verticals;
- local-first and public-benefit-oriented;
- sustainable revenue where aligned with autonomy and trust;
- open-source reciprocal;
- ambitious about capability and conservative about authority claims.

Read first:

- [[softwareco/docs/org/purpose.md|Purpose]]
- [[softwareco/docs/org/mission.md|Mission]]
- [[softwareco/docs/org/vision.md|Vision]]
- [[softwareco/docs/org/strategic_objectives.md|Strategic Objectives]]
- [[softwareco/docs/org/values_ethics.md|Values and Ethics]]
- [[softwareco/docs/org/governance.md|Governance]]
- [[softwareco/docs/org/glossary.md|Glossary]]

## Organizational shape

Softwareco is a federated company of product, platform, service, infrastructure, contribution, and fork domains. Repositories are source-owner homes; they are not automatically products or organizational units.

### Lanes

| Lane | Role |
|---|---|
| `owned/` | Directly operated products, platforms, and capabilities. |
| `infra/` | Runtime, provisioning, reliability, recovery, and operational infrastructure. |
| `contrib/` | Upstream-coupled work and compatibility evidence. |
| `agents/` | Declared target lane for dedicated agent-product archetypes; not materialized at the root as of 2026-07-12. `softwareco-agents/` currently exists as a separate legacy/current path. |
| `fork/` | Deliberate maintained divergence with explicit ownership burden. |

Lane maps route work; owner repos prove current capability. Start with:

- [[softwareco/owned/docs/project/repo-capability-map.md|Owned Repo Capability Map]]
- [[softwareco/infra/docs/project/repo-capability-map.md|Infra Repo Capability Map]]

## Accountability model

The company uses role-based accountability. Decision 74 preserves `human-operator` as residual **Softwareco Org Owner** and accepts a finite `softwareco-cto-agent` technical portfolio mandate over `softwareco/owned` through [[softwareco/docs/org/cto-agent-charter.md|the CTO charter]]. The delegation remains preactivation until the controller, workbench, validation, and exact `SF3` gates pass. The human retains residual accountability and every reserved decision.

Product, Service, Platform, Domain, and Project owners retain authority inside explicit delegations. Agents execute and advise within scope but do not hold residual accountability or enlarge the activated domain.

Full decision rights: [[softwareco/docs/org/governance.md|Softwareco Governance]].

## Direction-to-outcome loop

This is the target company loop. It is not yet proved as a recurring Softwareco-wide operating practice.

```text
purpose and vision
-> product posture
-> AK strategic frame
-> discovery and design where needed
-> AK implementation wave
-> AK execution leaves / owner-repo work
-> FCOS coordination only when cross-repo
-> validation and promotion
-> operation and outcome evidence
-> continue / stop / redirect / complete
-> KES learning and standards improvement
```

Rules:

- Narrative purpose, vision, rationale, and posture remain in docs.
- AK owns active state for the concern surfaces that its current implementation and accepted contracts expose; consult AK owner commands/docs rather than inferring unlanded authority from this summary.
- FCOS owns cross-repo control-board meaning, not repo-local execution.
- Product and service owners own user and operational facts.
- A passing build is not a release; a release is not an outcome.
- Company WIP is finite. Starting a commitment names what is deferred, displaced, or stopped.

Factory contract: Decision 62 accepted [[softwareco/docs/project/2026-07-12-software-factory-operating-system-rfc.md|the Softwareco Factory Flow Protocol]] for pilot 001. Decision 68's template/canary delegation is terminal and expired; its L2/L0 propagation freeze remains. Decision 74 now governs the accepted preactivation owned-portfolio CTO workbench and 30-day mandate. It does not lift the template freeze or turn `infra/issue-tracker` into a company backlog. Consult AK and the accepted decisions rather than inferring authority from this summary.

## Proposed operating cadence

Decision 74 accepts a bounded owned-portfolio CTO cadence whose proof target is one portfolio thesis and one completed outcome wave. It is not yet active or proved as recurring company operation. Cadence outputs belong in AK/source-owner evidence and the freshness-bounded CTO packet, not in this table.

| Cadence | Question |
|---|---|
| Continuous | What signal, incident, or evidence requires owner action now? |
| Weekly flow review | What is active, blocked, over WIP, ready for promotion, or ready to stop? |
| Monthly product/service review | Did the user or operational outcome improve, and what decision follows? |
| Quarterly horizon review | Which strategic frames, vertical bets, services, and capacity allocations should change? |
| Post-incident/rollout | What evidence and learning must change the system? |

Cadence produces owner-native updates, not meeting-only ledgers.

## MITO placement

| MITO layer | Softwareco concern | Primary docs/surfaces |
|---|---|---|
| Strategic | purpose, mission, vision, objectives, portfolio posture | `docs/org/`, product posture, AK strategic frames |
| Design & Configuration | governance, ethics, architecture, contracts, templates | governance docs, ROCS, RFC/ADR, engineering-core |
| Implementation | waves, tasks, code, release preparation | AK waves/tasks, source-owner repos, Pi execution |
| Operations & Evaluation | services, incidents, outcomes, evidence, learning | service owners, AK evidence, KES, DSPx/Oracle |

## Do not conflate the three layer models

AI Society uses “layer” in three different, orthogonal ways:

| Layer model | What it means | Canonical start |
|---|---|---|
| Architectural/authority layers | Constitutional, governance, semantic, runtime, steward, execution, learning, and empirical owner layers | [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/ai-society-stack-map.md|AI Society Stack Map]] |
| Layer 12 protocol | Purpose-to-publication direction, discovery, design, decision, execution, evidence, learning, and activation traceability | [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/layer-12-protocol.md|Layer-12 Protocol — Start Here]] |
| L0/L1/L2 render lineage | L0 template authoring → L1 company template repo → L2 standalone generated repo; filesystem depth and lanes are not new layers | [[/home/tryinget/ai-society/core/tpl-template-repo/docs/dev/architecture/layer-taxonomy-and-propagation-architecture.md|Layer Taxonomy and Propagation Architecture]] |

For current operator vocabulary and workflow, prefer [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/layer-12-protocol.md|Layer-12 Protocol — Start Here]] and [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/2026-04-25-layer-12-operator-vocabulary-boundary.md|Layer-12 Operator Vocabulary Boundary]]. [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/layer-12-direction-substrate-status.md|Layer-12 Direction Substrate Status]] remains useful for shipped storage/command history, but some SG/TG/operating-slice terminology is compatibility history rather than the preferred `strategic_frame` / `implementation_wave` operator grammar.

Softwareco is an **L1 company template/control-plane repo** in render lineage. Its child standalone repos remain L2 even when nested below lane-root repositories. That render classification does not determine runtime authority, organizational accountability, or MITO placement.

## Authority quick map

| Concern | Owner |
|---|---|
| Accepted task, direction, decision, evidence, contract, receipt, and related AK runtime concerns | AK / `society.v2.db` |
| Cross-repo Layer-5 control board | FCOS |
| Semantic meaning | ROCS / ontology owners |
| Reusable procedures | Prompt Vault |
| Live agent execution | Pi and owner packages |
| Human learning/crystallization | KES and source-owner docs |
| Empirical behavior analysis | DSPx / Oracle |
| Service deployment substrate | Runtime Cell intent plus Softwareco infra owners |
| Human-facing consent, delegation, explanation | steward layer target; not yet one complete runtime |

## Essential AI Society map

These are the important workspace files that should be discoverable from Softwareco. Wiki links assume `/home/tryinget/ai-society` is the knowledge-workspace root.

### Start and constitution

- [[/home/tryinget/ai-society/README.md|AI Society Workspace Entrypoint]] — shortest workspace start page.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/ai-society-stack-map.md|AI Society Stack Map]] — which document owns each architectural altitude.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/dream-model-stack.md|Dream Model Stack]] — constitutional model/projection/evidence axioms.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/runtime-authority-matrix.md|Runtime Authority Matrix]] — current and target owner of each concern.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/discoverability-and-truth-model.md|Discoverability and Truth Model]] — selection versus capability-truth law.

### Governance and direction

- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/s3-governance-semantics.md|S3.0 Governance Semantics]] — domains, agreements, consent, objections, and delegation.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/mito-model.md|MITO Model]] — Strategic, Design & Configuration, Implementation, Operations & Evaluation.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/dev/decision-lifecycle.md|Decision Lifecycle]] — problem/evidence → RFC → review → ADR → rollout → learning.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/dev/review-synthesis.v6.toml|Review Synthesis Contract]] — main-first ADR-closing review topology.
- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/direction-to-execution-model.md|Direction-to-Execution Model]] — narrative direction into governed execution.
- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/decision-runtime-and-roadmap.md|AK Decision Runtime and Roadmap]] — what decision runtime owns today.

### System assembly and human interface

- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/ai-society-convergence-architecture.md|AI Society Convergence Architecture]] — 10,000-foot system assembly.
- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/steward-runtime-and-jurisdiction-model.md|Steward Runtime and Jurisdiction Model]] — human-facing steward membrane.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/steward-continuity-model.md|Steward Continuity Model]] — continuity, activation, wake-up, and V4/V5 boundary.
- [[/home/tryinget/ai-society/holdingco/infra/docs/project/ai-society-runtime-cell-problem-intent.md|AI Society Runtime Cell]] — k3s + Envoy service substrate intent.
- [[/home/tryinget/ai-society/holdingco/fcos-control-board/README.md|FCOS Control Board]] — native Layer-5 product entrypoint.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/project/fcos-current-vs-target-authority.md|FCOS Current-vs-Target Authority Map]] — historical hybrid-bridge inventory; useful for migration lineage, but its opening claim that governance-kernel is the live FCOS control plane is superseded by the native `holdingco/fcos-control-board` cutover, the Stack Map, Runtime Authority Matrix, and live `fcos status`.

## Navigation rules

1. Start with this operating model for Softwareco identity and flow.
2. Use the Stack Map when the concern's architectural layer is unclear.
3. Use the Runtime Authority Matrix when ownership is unclear.
4. Use lane capability maps only to select a repository.
5. Confirm capability maturity in the selected owner repo.
6. Use AK for live execution truth and FCOS only for cross-repo coordination.
7. Treat this and other markdown as narrative/policy, not a substitute for canonical runtime state.

## Current reality

Softwareco contains many component repositories and shared engineering-policy surfaces, but that topology alone does not prove supported products or a functioning company loop. At the 2026-07-12 validation point:

- `ak direction list --repo /home/tryinget/ai-society/softwareco --format json` returned `[]`;
- the Software Factory Flow Protocol was an untracked draft whose current bytes lacked a controlling review and whose latest recorded review outcome was `revise_rfc`;
- the Softwareco Org Owner role was defined but not yet assigned in accepted runtime/governance state;
- product and service maturity varied substantially across owner repos.

Those bullets describe the dated 2026-07-12 baseline. Decision 68 later activated and completed bounded template/canary work; its CTO delegation is expired. Decision 74 was accepted on 2026-07-25 for a finite `softwareco/owned` portfolio CTO, but it remains preactivation until controller task `4182`, exact Pi workbench proof, projections, and `SF3` activation reconcile. Live status must still be read from AK, FCOS, and owner repositories rather than copied forward here.

Dated evidence:

- [[softwareco/docs/project/2026-07-12--status--softwareco-company-claim-validation.md|2026-07-12 Company-Claim Validation]]
- [[softwareco/docs/project/2026-07-12--status--transition-document-inventory.md|2026-07-12 Transition-Document Inventory]]

Relevant commits after those dates require revalidation; the dated files must not be treated as current runtime truth.
