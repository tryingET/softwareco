# Governance — contrib lane root

Deferred and active work for this lane lives in the **Agent Kernel DB** (`ak task ...`).
The AK DB is the sole work authority; no checked-in work-items projection exists or should be reintroduced.

The retired `governance/work-items.json` / `work-items.cue` pair contained only completed
(`done`) historical task references already recorded in AK; nothing was lost at retirement.

## Optional explicit task-scope snapshots

When a lane-root AK task needs explicit scope:

- author/update the scope in AK via `ak task scope show|set|update ...`
- keep repo-side copies under `governance/task-scopes/AK-<TASK-ID>.snapshot.json` as frozen exports
- refresh a checked-in snapshot with `mkdir -p governance/task-scopes && ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json`
- verify checked-in snapshots with `./scripts/check-task-scope-snapshots.sh` before commit or in CI

## Non-negotiable

- Do not leave deferred work as ad-hoc TODO comments or scattered markdown notes.
- Do not reintroduce a checked-in `governance/work-items.json` projection; the AK DB is authoritative.
- Do not hand-author `governance/task-scopes/AK-*.snapshot.json` as if it were the live task-scope source of truth.
