---
summary: "Governance directory placeholder for generated monorepos."
read_when:
  - "A generated monorepo needs governance artifact placement guidance."
type: "reference"
---

# Monorepo Work Items


## Authority model

| Surface | Role | Authority |
|---|---|---|

Do not treat manual JSON edits as the live source of truth.
If you are migrating a legacy JSON-first monorepo, import once, then continue from AK and re-export the projection.

## Workflow

Use plain installed `ak` as the canonical operator path:

```bash
```

## Optional explicit task-scope snapshots

When a monorepo AK task needs explicit scope:

- author/update it in AK via `ak task scope show|set|update ...`
- keep repo-side copies under `governance/task-scopes/AK-<TASK-ID>.snapshot.json` as frozen exports
- refresh a checked-in snapshot with `mkdir -p governance/task-scopes && ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json`
- verify checked-in snapshots with `./scripts/check-task-scope-snapshots.sh` before commit or in CI
- keep package/app consumers pointed at the monorepo-root snapshot instead of inventing per-member task-scope files

## Brownfield migration boundary

If this monorepo is retiring hand-authored `governance/task-scopes/AK-*.json` files:

- author/update the scope in AK first, then export `AK-<TASK-ID>.snapshot.json`
- keep the legacy `AK-*.json` file only as temporary compatibility fallback while local/CI still depend on it
- remove legacy manifest authoring from workflow docs and handoffs as soon as `./scripts/check-task-scope-snapshots.sh` passes
- if the task still uses repo-default scope, do not invent a snapshot or a replacement legacy manifest

Optional schema-only validation:

```bash
```

## State machine

```
triage → queued → doing → review → done
```

## Program vs project/monorepo

| Type | Location | Scope | Authority |
|------|----------|-------|-----------|
| **Program** | governance-kernel/governance/programs/ | Cross-company | L0 scheduler / FCOS |
| **Program** | company-templates/governance/programs/ | Company | Planning only |

## Non-negotiable

- Do not leave deferred work as ad-hoc TODO comments or scattered markdown notes.
- Do not hand-author `governance/task-scopes/AK-*.snapshot.json` as if it were the live task-scope source of truth.
- For legacy/manual JSON slices, import to AK and then export the projection back out.
