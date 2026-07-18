---
summary: "Dated inventory of living product-posture surfaces and undated transition/status snapshot candidates in active Softwareco repos."
read_when:
  - "When planning owner-repo migration to dated transition documents and evidence-backed living product posture."
type: "evidence"
as_of: "2026-07-12"
status: "historical_inventory_snapshot"
---

# Softwareco transition-document inventory — 2026-07-12

## Scope and exclusions

Read-only inventory across 60 active Git roots under Softwareco root, `owned/`, `infra/`, `softwareco-agents/`, and `fork/`. It excluded candidate/autoresearch worktrees, backups, nested duplicate clones, `contrib/`, vendored/generated trees, diary entries, and ontology snapshots.

The inventory separates:

- **living posture** — stable `docs/project/product-posture.md` or `product_posture.md` path that should gain evidence/freshness metadata rather than a date-prefixed filename;
- **time-bounded snapshot** — transition, migration, current-vs-target, status, or closeout material that should be date-prefixed when an owner next migrates it;
- **history** — useful evidence that must not be routed as current truth without revalidation.

Dates below come from repository Git history, not filesystem modification times. “Later relevant commits” is a triage signal inferred from code/evidence path changes; each owner must validate semantic impact.

## Living product-posture surfaces found

Twenty-two living posture files were found across these owner roots/packages:

- `infra/replay-fabric/docs/project/product-posture.md`
- `infra/workstation/docs/project/product-posture.md`
- `owned/agent-kernel/docs/project/product-posture.md`
- `owned/calisthenics-ai-coach/docs/project/product-posture.md`
- `owned/dep-diet/docs/project/product-posture.md`
- `owned/dep-redteam/docs/project/product-posture.md`
- `owned/dep-viz/docs/project/product-posture.md`
- `owned/designmd-foundry/docs/project/product-posture.md`
- `owned/dspx/docs/project/product-posture.md`
- `owned/local-ai-control-plane/docs/project/product-posture.md`
- `owned/pi-extensions/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-agent-vent/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-autonomous-session-control/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-autoresearch/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-context-packer/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-little-helpers/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-session-compaction/docs/project/product-posture.md`
- `owned/pi-extensions/packages/pi-society-orchestrator/docs/project/product-posture.md`
- `owned/runtime-trace-insights/docs/project/product-posture.md`
- `owned/semantic-code-intelligence/docs/project/product-posture.md`
- `owned/test-capabilities/docs/project/product-posture.md`
- `owned/ts-quality/docs/project/product-posture.md`

Most predate later code/evidence commits. This does not prove every claim is wrong; it proves that freshness cannot be established from their current filenames alone. The highest-volume later-change signals were in `pi-extensions` packages, `agent-kernel`, `infra/workstation`, `dspx`, and `semantic-code-intelligence`.

## Strong undated snapshot candidates

| Owner repo | Current path | Git date to preserve when migrated | Why it is time-bounded |
|---|---|---:|---|
| `infra/provisioning` | `docs/dev/status.md` | 2026-03-01 | generic implementation/status snapshot |
| `infra/workstation` | `docs/project/voice-migration-status.md` | 2026-03-29 | migration status followed by substantial later change |
| `owned/apex-cathedral` | `docs/project/transition-summary.md` | 2026-03-09 | transition summary |
| `owned/dep-redteam` | `docs/project/mvp_closeout.md` | 2026-05-05 | point-in-time closeout |
| `owned/dspx` | `PROJECT_STATUS.md` | 2026-07-10 | mutable project status surface |
| `owned/dspx` | `docs/project/oracle-backend-current-status.md` | 2026-05-29 | current-status snapshot with many later commits |
| `owned/fcos-proving-lane` | `docs/dev/status.md` | 2026-03-01 | generic status snapshot |
| `owned/feedbackApp` | `docs/runtime-seed/source/PROJECT_STATUS.md` | 2026-03-28 | seeded point-in-time status |
| `owned/kinetic-caption-studio` | `docs/project/karaoke-current-vs-target-matrix.md` | 2026-04-14 | seam-specific current-vs-target snapshot |
| `owned/lehrplan-viz` | `docs/IMPLEMENTATION_STATUS.md` | 2026-03-17 | implementation snapshot |
| `owned/lehrplan-viz` | `docs/dev/PROJECT_STATUS.md` | 2026-03-17 | project status snapshot |
| `owned/obsidian-plugins` | `packages/obsidian-excalidraw-layer-manager/docs/project/current-vs-target.md` | 2026-04-18 | current-vs-target snapshot followed by later commits |
| `owned/pi-extensions` | `packages/pi-autonomous-session-control/docs/design/IMPLEMENTATION_STATUS.md` | 2026-03-22 | implementation snapshot with extensive later change |
| `owned/pi-extensions` | `packages/pi-autonomous-session-control/docs/dev/monorepo-migration-dashboard-slice.md` | 2026-05-12 | migration snapshot with extensive later change |
| `owned/pi-extensions` | `packages/pi-autoresearch/docs/project/current-vs-target.md` | 2026-05-04 | current-vs-target snapshot with extensive later change |
| `owned/semantic-code-intelligence` | `PROJECT_STATUS.md` | 2026-07-12 | mutable status snapshot |
| `owned/semantic-flow-diff` | `docs/dev/status.md` | 2026-02-28 | generic status snapshot |
| `owned/test-capabilities` | `docs/dev/ts-quality-current-vs-target.md` | 2026-05-14 | current-vs-target snapshot followed by later commits |

Sixteen tracked `.migration-notes.txt` files were also found with a 2026-03-01 Git date. They require owner-by-owner classification: rename to dated historical evidence, absorb durable facts into current docs, or remove only through the owning repo's normal review. This inventory does not authorize deletion.

## Migration rule

For each owner repo:

1. read its `AGENTS.md` and owner entrypoint;
2. inspect the document and its Git first-added/last-change history;
3. validate current claims against code, tests, generated artifacts, operator paths, and runtime readback;
4. keep living `product-posture.md` stable and add the required evidence metadata;
5. rename time-bounded snapshots to `YYYY-MM-DD--<kind>--<scope>.md`, preserving the truthful snapshot/validation date;
6. update inbound links atomically;
7. mark superseded history explicitly and do not route it as current truth;
8. run owner-repo validation and commit within that repo.

No child-repo files were renamed in this root-policy pass. The owner-specific changes are a follow-up migration wave, not an implicit side effect of changing the L1 template.
