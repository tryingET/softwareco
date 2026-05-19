---
summary: "Lane-root overview and operator entrypoint for softwareco/owned."
read_when:
  - "Starting work at the softwareco/owned lane root"
  - "Deciding whether a change belongs in the lane root or a child repo"
---

# softwareco/owned lane root

Brownfield lane-root repository for Software Company's directly operated delivery repos under `softwareco/owned/`.

## Purpose

This repo is the control plane above the child repos nested inside it. It exists to:

- provide shared navigation and operating context for the owned lane
- hold lane-root-local governance, ontology, and deterministic helper scripts
- give operators a trustworthy starting point before they drop into a child repo
- route fresh-context operators into the correct child repo via `docs/project/repo-capability-map.md`
- converge control-plane template improvements without erasing meaningful lane-local state

## Scope boundary

### What belongs here

- lane-root documentation and operating rules
- shared scripts such as `./scripts/preflight-repo-census.sh` and `./scripts/rocs.sh`
- lane-root-local planning and its checked-in projection in `governance/work-items.json`
- session handoff and diary capture for this repo itself

### What does not belong here

- implementation work that belongs to a child repo
- duplicated task state for child repos
- ad-hoc TODO tracking outside the authoritative AK/work-items flow
- template re-renders that overwrite lane-root semantics without review

## Operator workflow

1. Read `next_session_prompt.md`
2. Review `governance/work-items.json` and, when needed, reconcile it with AK using `ak work-items check --repo . --path governance/work-items.json`
3. Run `./scripts/preflight-repo-census.sh .`
4. Pick one lane-root-local slice
5. Validate with `./scripts/ci/smoke.sh`, `./scripts/ci/fast.sh`, and, when appropriate, `./scripts/ci/full.sh`

## Key files

- `AGENTS.md` — lane/root operating contract inherited by descendant repos
- `docs/project/` — purpose, mission, vision, goals
- `docs/project/repo-capability-map.md` — routing substrate for selecting the correct owned repo from arbitrary working directories
- `docs/project/ghostty-ak-task-launcher.md` — how to open one Ghostty + Pi instance per AK task with a pre-submitted task prompt
- `docs/decisions/` — durable decisions about how this lane root should operate
- `docs/system4d/` — boundary, outcomes, invariants, and risks
- `governance/README.md` — AK-first work-items projection rules for this repo
- `governance/work-items.json` — checked-in lane-root projection/mirror
- `diary/` — raw session capture

## Useful operator helpers

```bash
./scripts/preflight-repo-census.sh .
ak work-items check --repo . --path governance/work-items.json
./scripts/check-task-scope-snapshots.sh
./scripts/launch-pi-ak-task-ghostty.sh --justfile-rollout-pilots
./scripts/launch-pi-ak-task-ghostty.sh --focus-last 609 610 611
./scripts/launch-pi-ak-task-ghostty.sh --interactive 610
./scripts/launch-pi-ak-task-ghostty.sh --print --hold-open 609
```

## Validation

```bash
./scripts/ci/smoke.sh
./scripts/ci/fast.sh
./scripts/ci/full.sh
./scripts/preflight-repo-census.sh .
```

Use repo-local deterministic wrappers when possible and keep work in this repo limited to lane-root concerns.
