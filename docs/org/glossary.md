---
summary: "Softwareco organization and AI Society operating vocabulary with authority-safe definitions."
read_when:
  - "Interpreting Softwareco strategy, governance, operating, or architecture terms."
  - "Adding cross-repo language that may overlap AK, FCOS, ROCS, Pi, KES, or DSPx ownership."
type: "reference"
mito_layers:
  - "Design & Configuration"
---

# Softwareco glossary

This glossary explains how Softwareco uses important terms. It is a human navigation surface, not semantic authority. Governed cross-system meaning belongs to ROCS or the named owner surface.

## Organization and direction

**Purpose**
Why Softwareco exists independent of any product, plan, or implementation.

**Mission**
What Softwareco does now to advance its purpose.

**Vision**
The observable future state Softwareco intends to help create over a three-to-five-year horizon.

**Strategic objective**
A company-level outcome with measures, accountable role, and review horizon. Objectives are narrative direction; active decomposition belongs in AK direction.

**Strategic frame**
The current major bet below vision, represented through AK direction. It answers why this bounded direction matters now.

**Implementation wave**
A bounded grouping that advances a strategic frame toward execution leaves. It is not a permanent backlog container.

**Product posture**
A narrative, vision-level account of current maturity, target experience, important gaps, and proof signals. It is not a task queue or release log.

**Discovery**
Time-bounded work that establishes the user/problem evidence, owner boundaries, current reality, and safest next stage before commitment.

**Committed flow**
An RFC-local Software Factory term for a finite commitment with an outcome owner, preregistered outcome, constrained capacity, canonical execution carriers, and terminal decision. It is not currently a governed AK state token.

## Accountability

**Domain**
A bounded area of decision-making and accountability. A domain may span repositories and is not automatically an organizational hierarchy.

**Softwareco Org Owner**
The human role accountable for company portfolio posture, appointments, domain boundaries, cross-domain tradeoffs, and company-level exceptions. The role must be assigned through an accepted governance/AK surface.

**Domain Owner**
The human accountable for the outcomes, boundaries, delegation, and health of a bounded product, platform, service, infrastructure, or contribution domain.

**Product Owner**
The human accountable for users, product vision, outcome priorities, and routine lifecycle/investment decisions inside an accepted posture and delegation. Creating, transferring, merging, or permanently retiring a company commitment remains a reserved portfolio decision.

**Service Owner**
The human accountable for reliability, security, support, incident readiness, recovery, and decommissioning of an operated service.

**Project Maintainer**
The human accountable for source-owner acceptance, repository quality, releases, and normal change control.

**Steward**
A governed human-facing role that mediates between a person or jurisdiction and AI Society. A steward is not canonical runtime, semantic, procedure, or empirical authority.

**Delegation**
An explicit, bounded grant stating who may decide or execute what, under which constraints, evidence, expiry, and revocation path. Accountability remains with the human delegator unless governance explicitly assigns it elsewhere.

**Consent**
Agreement without unresolved qualifying objections from the people entitled to participate in the decision. Silence is not consent unless an accepted agreement explicitly defines that mechanism.

## Authority and evidence

**Canonical authority**
The single accepted owner of operational truth for one concern.

**Owner surface**
The repository, runtime, model, or governance process authorized to define or mutate a concern.

**Projection**
A derived human or interop view over canonical facts. A projection must not silently become a second authority.

**Evidence**
An attributable observation, test, receipt, artifact, or user outcome supporting a claim. Evidence informs decisions; it does not decide by itself.

**Receipt**
A machine- or operator-verifiable record that a transition or operation occurred under stated inputs and authority.

**Capability maturity**
The distinction between proposed, internally implemented, exact-path supported, friendly operator-supported, and production-claimed capability. Only the owner repo may promote its maturity claim.

**Local-first**
An architecture and product posture that keeps important capability, data, inspectability, and operational control local where practical. It does not mean “never networked” or “never cloud-assisted.”

**Operated service**
A deployed capability with an owner, environment/version, health path, support boundary, incident and recovery posture, and retirement path.

**Operational risk tier**
A pilot/release classification used by the Factory Flow Protocol: R0 exploration, R1 local/reversible, R2 shared or stateful, and R3 critical/security-sensitive. These are RFC-local operating labels until promoted through an accepted owner contract.

## AI Society owner systems

**AK — Agent Kernel**
Canonical runtime/CLI for accepted task, evidence, decision, direction, contract, receipt, and related `society.v2.db` concerns.

**FCOS — control board**
First-class Layer-5 cross-repo coordination product owned by `holdingco/fcos-control-board`. It is not a synonym for AK tasks or a generic repo queue.

**ROCS**
Semantic and ontology authority plus deterministic semantic tooling. It does not own live task or decision state.

**Prompt Vault**
Owner of reusable prompts and procedures. A procedure may guide a transition but does not become canonical runtime state.

**Pi**
Live agent execution host and operator workbench, including extension/runtime surfaces. Session state and tool execution are not automatically canonical society authority.

**KES — Knowledge Evolution System**
Human crystallization path from diary evidence through learnings and reusable promotion. KES is memory and learning, not live execution authority.

**DSPx / Oracle**
Program engineering, replay, optimization, and empirical behavior analysis. Its conclusions are advisory evidence rather than normative governance authority.

**Runtime Cell**
The k3s + Envoy local-first service substrate intent for running society services without becoming their authority.

## Structuring models

**MITO**
The required structuring lens for Strategic, Design & Configuration, Implementation, and Operations & Evaluation concerns. MITO is not a second runtime or governance authority.

**Sociocracy 3.0 / S3.0**
The primary governance-semantics source for drivers, domains, agreements, consent, objections, delegation, governance, and organizational learning. It is not the execution runtime.

## Navigation

- [[holdingco/governance-kernel/docs/core/definitions/ai-society-stack-map.md|AI Society Stack Map]]
- [[holdingco/governance-kernel/docs/core/definitions/runtime-authority-matrix.md|Runtime Authority Matrix]]
- [[holdingco/governance-kernel/docs/core/definitions/discoverability-and-truth-model.md|Discoverability and Truth Model]]
- [[holdingco/governance-kernel/docs/core/definitions/mito-model.md|MITO Model]]
- [[holdingco/governance-kernel/docs/core/definitions/s3-governance-semantics.md|S3.0 Governance Semantics]]
