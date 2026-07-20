---
summary: "AK projection and task-scope guidance for generated agent product repositories."
read_when:
  - "Operating work-items or explicit task scope in a generated agent repo."
type: "reference"
---

# Agent product work items

AK is the live authority for this repository. `governance/work-items.json` is a checked-in deterministic projection and `governance/work-items.cue` validates only that projection's shape.

## Workflow

```bash
ak work-items import --repo . --path governance/work-items.json
ak work-items export --repo . --path governance/work-items.json
ak work-items check --repo . --path governance/work-items.json
```

Do not repair drift by hand-editing JSON and pretending it is authoritative.

## Explicit task-scope snapshots

```bash
mkdir -p governance/task-scopes
ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json
./scripts/check-task-scope-snapshots.sh
```

Snapshots are frozen AK exports. They do not appoint the agent, grant delegation, or replace live task scope.

## Optional schema validation

```bash
cue vet governance/work-items.json governance/work-items.cue
```

Missing required AK access fails closed. Cross-repo coordination belongs in FCOS only when a genuine cross-owner gate exists.
