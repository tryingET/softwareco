---
summary: "Capability map for softwareco/infra repos used for cross-repo routing from arbitrary working directories."
read_when:
  - "A task clearly belongs to softwareco/infra but the current cwd is elsewhere."
  - "You need to choose the right infra repo and minimal read-first docs before diving deeper."
type: "reference"
---

# softwareco/infra repo capability map

## Use
This document is the routing substrate for cross-repo discovery across `~/ai-society/softwareco/infra`.
It does not replace repo-local contracts.
Use it to select the right infra repo, the right first docs, and the next handoff.

Seeded scope in this first production-ready cut:
- the infra lane root itself
- the most frequently referenced active infra repos

Expand only when routing pressure becomes real.

## Cross-lane runtime-cell boundary

For k3s / Envoy / AI Society Runtime Cell work, start with the holding-level problem/intent note:

- `~/ai-society/holdingco/infra/docs/project/ai-society-runtime-cell-problem-intent.md`

Interpretation:

- `holdingco/infra` owns the Runtime Cell concept, intent, and source-owner boundary: k3s + Envoy are infrastructure substrate/service membrane, not society authority.
- `softwareco/infra` owns concrete implementation below that intent when the work becomes workstation runtime, provisioning, NAS administration, packaging, validation, or service operation.

## Repo map

| Repo | Owns | Trigger cues | Read first | Domain skill | Notes |
|---|---|---|---|---|---|
| `infra (root)` | lane-root infra docs, governance, shared direction, cross-repo infra boundaries | `softwareco/infra` root, infra lane, infra root docs, infra governance, lane-level infra planning | `~/ai-society/softwareco/infra/README.md`, `~/ai-society/softwareco/infra/AGENTS.md` | none | Use the root when the concern is lane-level infrastructure direction rather than one subrepo's implementation. |
| `workstation` | workstation build/run docs, milestone scripts, runtime services, promoted local runtime/control-plane surfaces | workstation build, runtime service, lane-op, local runtime, teacher-prep runtime, baseline text service, baseline vs canary, Zotero bridge API packaging, backup/recovery lane | `~/ai-society/softwareco/infra/workstation/README.md`, `~/ai-society/softwareco/infra/workstation/AGENTS.md`, `~/ai-society/softwareco/infra/workstation/docs/project/2026-03-29-cross-repo-boundary-map.md` | `workstation-runtime-operator` | Owns workstation runtime/control plane and packaging below `owned/workstation-capabilities`. |
| `provisioning` | machine/bootstrap provisioning, Comtrya-based package install, secrets bootstrap, setup validation | provisioning, bootstrap, Comtrya, setup profile, package install, machine provisioning, `just setup`, first-run bootstrap | `~/ai-society/softwareco/infra/provisioning/README.md`, `~/ai-society/softwareco/infra/provisioning/AGENTS.md` | none | Owns reproducible machine provisioning, not product runtime semantics. |
| `ds1621-admin` | Synology DS1621+ administration, NAS-side backup target contract, SSH/account/admin runbooks | DS1621, Synology, NAS backup target, pi-ops, DSM admin, restic target contract, NAS SSH | `~/ai-society/softwareco/infra/ds1621-admin/README.md`, `~/ai-society/softwareco/infra/ds1621-admin/AGENTS.md` | none | Use when the concern is NAS/admin truth rather than workstation-side backup consumers. |
| `issue-tracker` | AK-backed external issue tracker, sequence manifests, import/export/sync workflows, pre-submit and post-close verification helpers | issue tracker, sequencer, upstream issues, `STATE.json`, issue sync, verifier gate, sequence manifest | `~/ai-society/softwareco/infra/issue-tracker/README.md`, `~/ai-society/softwareco/infra/issue-tracker/AGENTS.md` | none | DB live state wins over compatibility projections; treat this as external issue workflow machinery. |
| `replay-fabric` | local-first replay and recovery ledger/viewer, hook ingest, bounded Pi/recovery milestones, replay desk UI | Replay Fabric, replay ledger, webhook ingest, Pi milestones, recovery milestones, replay desk, hook sidecar | `~/ai-society/softwareco/infra/replay-fabric/README.md`, `~/ai-society/softwareco/infra/replay-fabric/AGENTS.md` | none | Owns replayable history and bounded recovery guidance, not live Pi or restore authority. |
| `ts-quality-tools` | reusable TS/JS quality tooling monorepo (`ts-mutate`, `crap4ts`), validation and release-trust workflows | ts-mutate, crap4ts, mutation testing, CRAP metric, TS quality tooling, quality intelligence | `~/ai-society/softwareco/infra/ts-quality-tools/README.md`, `~/ai-society/softwareco/infra/ts-quality-tools/AGENTS.md` | none | Workflow-level quality intelligence repo, not one product repo's local quality gate. |

## Routing rule
1. If the operator names an exact repo or path, trust that first.
2. Otherwise match trigger cues conservatively.
3. Read only the top candidate repo's minimal read-first docs.
4. Do not widen to sibling infra repos unless the first repo clearly fails to own the concern.
