---
summary: "Bounded evidence for the Software Factory Operating Protocol RFC."
read_when:
  - "Reviewing whether Softwareco's software-factory gap is evidenced rather than assumed."
  - "Reviewing the Software Factory Operating Protocol RFC."
type: "evidence-note"
system4d:
  container:
    boundary: "Read-only observations about Softwareco operating coherence; not capability certification for every child repo."
    edges:
      - "[Problem/intent](2026-07-12-software-factory-operating-system-problem-intent.md)"
      - "[RFC](2026-07-12-software-factory-operating-system-rfc.md)"
  compass:
    driver: "Ground the RFC in current runtime and repository evidence."
    outcome: "Reviewers can distinguish existing components from missing company-wide operation."
  engine:
    invariants:
      - "Routing maps are not treated as production capability proof."
      - "Documentation claims are separated from live AK observations."
  fog:
    risks:
      - "A broad repository census may overcount inactive or contributed repositories."
      - "Absence of a discovered artifact is not proof that no local practice exists."
---

# Software Factory Operating System — evidence note

## Evidence date

2026-07-12

## High-confidence observations

### 1. Softwareco has substantial component capability

Existing owner surfaces include:

- AK / `society.v2.db` for canonical direction, tasks, decisions, evidence, and lineage;
- FCOS for first-class cross-repo control-board coordination;
- Pi, ASC, and society-orchestrator for execution and coordination;
- ROCS for semantics;
- engineering-core for shared engineering discipline;
- workstation, provisioning, NAS, and replay infrastructure;
- runtime tracing, dependency intelligence, testing, and quality tools;
- KES and DSPx/Oracle learning and empirical-analysis surfaces.

References:

- `owned/docs/project/repo-capability-map.md`
- `infra/docs/project/repo-capability-map.md`
- `owned/agent-kernel/docs/project/ai-society-convergence-architecture.md`
- `../holdingco/governance-kernel/docs/core/definitions/ai-society-stack-map.md`

Interpretation: the primary gap is not an absence of components.

### 2. Company direction is not operationalized in AK

Read-only command:

```bash
ak direction export -r /home/tryinget/ai-society/softwareco
```

Observed result:

- vision anchor present;
- direction nodes: `0`;
- direction edges: `0`.

The startup packet also reported `missing_direction_nodes` and one ready root task concerned with template implementation rather than a company outcome.

Interpretation: Softwareco does not currently expose an AK-native company strategy/wave decomposition against which repo work can be evaluated.

### 3. Company narrative direction and ownership remain placeholders

> **Continuity note:** This section records the evidence observed before the 2026-07-12 organization-doc overhaul. The placeholder bodies and root `@template-owner` presentation were subsequently replaced in the working tree. The evidence remains historical input to the RFC; current narrative content is in `docs/org/`, while owner appointment and AK direction activation remain unresolved runtime/governance gates.

Observed files:

- `docs/org/purpose.md` asks the author to describe why the organization exists;
- `docs/org/vision.md` asks the author to describe a target future state;
- `docs/org/governance.md` asks for decision rights and incident handling;
- `docs/org/operating_model.md` names `@template-owner` as maintainer;
- root `README.md` also names `@template-owner`.

Interpretation: the root remains optimized as an L1 template repository and does not yet function as a truthful Softwareco operating front door.

### 4. Engineering discipline is much stronger than company flow

The generated engineering-core adoption dashboard reports:

- 41 owned repositories;
- 47 package/member surfaces;
- 88/88 structurally adopted;
- 88/88 semantically OK;
- 88/88 loop validation complete.

Reference:

- `owned/docs/project/engineering-core-adoption-dashboard.md`

Interpretation: standardization after work selection is demonstrably stronger than portfolio selection, release promotion, and outcome management.

### 5. Release automation is not a root factory default

The Softwareco root README states:

- release automation pack: disabled;
- community intake pack: disabled;
- trust-gate baseline: disabled.

This does not mean child repos lack CI or release machinery. A broad static scan found many child repos with workflows or language release manifests. It means there is no evidenced common company promotion contract connecting verified source, artifact, environment, deployment receipt, health verification, and rollback.

### 6. Capability maps route but do not operate the company

Both owned and infra capability maps explicitly describe themselves as routing/selection surfaces rather than production capability truth. They help an agent find an owner but do not answer:

- which company outcome has priority;
- what capacity is committed;
- whether the service is safely operated;
- whether the intended outcome improved.

### 7. Current architecture already warns against adding another authority layer

The convergence architecture states that canonical operational state should converge around `society.v2.db`, with AK as runtime/CLI, while other systems remain explicit owner layers, authoring layers, execution layers, or projections.

Interpretation: a new factory database, scheduler, or universal workflow engine would increase authority debt.

### 8. Template/AGENTS preflight

The Pi loader source confirms that the global context is loaded first and ancestor `AGENTS.md`/`CLAUDE.md` files are appended from filesystem root to the current working directory. Files are returned as raw content; there is no hard precedence marker that resolves contradictory instructions.

Review of `core/tpl-template-repo` found that the generic L0 AGENTS templates already carry the reusable owner/AK/projection guardrails needed by this RFC. Factory-specific WIP, cadence, packet, risk-tier, and terminal-decision language must not propagate to L0 before two successful, materially different pilots.

A separate Softwareco-local contradiction was found: the company AGENTS policy is main-first, while three L2 AGENTS templates still said never to push to main. The project template had already been corrected. The Softwareco templates and deterministic check are aligned as a separate company-policy repair, not as Factory Flow propagation.

### 9. Selected pilot evidence

The first candidate pilot is safe retirement of `softwareco/owned/fcos-proving-lane`.

Evidence:

- the operator directly reported confusion about why both `fcos-control-board` and `fcos-proving-lane` exist;
- the proving lane describes itself as an isolated Ring-0 evidence canary and explicitly not a product or policy authority;
- current native FCOS product authority is `holdingco/fcos-control-board`;
- proving-lane AK direction has zero nodes;
- one ready task is generic engineering adoption rather than product direction;
- the worktree has 48 status entries and five untracked paths;
- substantial historical evidence and dirty migration work make immediate deletion/reset unsafe;
- source and test surfaces contain only placeholders rather than a unique FCOS product implementation.

This supports an R2 evidence-preserving retirement pilot: preserve/classify/restore-proof first, make active-vs-historical status unambiguous, and defer physical deletion.

## Adversarial discovery

A Transcendent loop was run as bounded RFC design research:

- run: `transcendent-1783876054863`;
- phases: diagnose, two 100x passes, debt targeting, dissolve, rebuild, alien pass, closure gate;
- result: successful;
- closure posture: RFC-ready, not implementation-ready.

The strongest repeated finding was:

> The smallest coherent factory is a federated flow protocol over existing owners, not a new factory platform.

Package-local raw captures live under:

- `owned/pi-extensions/packages/pi-society-orchestrator/diary/2026-07-12--phase-transcendent-*.md`

Those KES captures are supporting research, not canonical Softwareco direction or decision authority.

## Evidence limitations

- The broad repo census includes many contributed/upstream repositories and must not be interpreted as an active-product count.
- This note did not certify every child repo's release or operational maturity.
- Local undocumented practices may exist.
- No broad customer-outcome dataset was available at the Softwareco root.
- The first pilot uses direct internal-operator evidence and cannot prove human-facing product delivery.
- A materially different second pilot must therefore be human-facing before factory-wide effectiveness or template/schema propagation is claimed.
