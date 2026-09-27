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
5. For the bounded launcher slice, use `just doctor` and `just check`. The historical CI profiles require separate authorization (see Validation).

## Key files

- `AGENTS.md` — lane/root operating contract inherited by descendant repos
- `docs/project/` — purpose, mission, vision, goals
- `docs/project/repo-capability-map.md` — routing substrate for selecting the correct owned repo from arbitrary working directories
- `docs/project/ghostty-ak-task-launcher.md` — legacy launcher refusal and withdrawn affected-domain batch/preset support
- `docs/project/2026-09-07-visible-task-session-lane-custody.md` — positive nomination/custody and safe reinstatement gates; no live domain certified
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
./scripts/launch-pi-ak-task-ghostty.sh --help
```

The legacy launcher is not the accepted visible task-session operation. It refuses
whole affected/unknown requests before mkdir, AK, terminal or focus, including
batches, presets and dry-run. Missing classification never enables fallback.
The actual DB-free `identity` / `classify-installed` consumer permits legacy
behavior only after a typed, version/digest-bound positive outside result.
See [producer/integration status](docs/project/2026-09-07-visible-task-session-lane-implementation.md).
Copied recipes and private aliases require positive owner support withdrawal;
this checked-in gate cannot certify or intercept them.

## Validation

```bash
just help
just doctor
just check
```

The bounded standard surface is shell/Python syntax plus scoped whitespace
(`lint`), isolated synthetic launcher tests (`test`), and their union (`check`).
`doctor` checks local test tools/TMPDIR only. No real AK/Pi/Ghostty/provider calls,
account/config/fleet inspection or enrollment occurs. Tests require owned `TMPDIR`.
Four emitted-classifier tests are opt-in via a reviewed `TASK_SESSION_PRODUCER_DIST`
path; otherwise they report skips. That variable is test-only. The emitted tests
use a synthetic locator, not live account configuration or public installed proof.

`just ci` intentionally exits 2: historical `scripts/ci/smoke.sh` and `fast.sh`
can fetch Git remotes; `full.sh` also reaches AK, task scopes and ROCS. Those
profiles remain separately gated, not hidden behind a passing bounded alias.
Full repository validation has **not** been certified by `just check`.
No distributable build, formatter, primary runtime or dev/watch surface is
established here, so `build`, `fmt`, `run` and `dev` are intentionally omitted.
The no-live-Pi task boundary supersedes spawning the usual Justfile bootstrap
prompt; its contract was read and applied directly without invoking Pi.

Use repo-local deterministic wrappers when possible and keep work in this repo limited to lane-root concerns.
