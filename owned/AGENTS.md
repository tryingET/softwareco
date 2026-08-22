---
summary: "Lane-root defaults for the brownfield softwareco/owned lane and its descendants."
read_when:
  - "You work at the softwareco/owned lane root."
  - "You work inside a descendant repo under softwareco/owned and need lane-level guardrails."
type: "reference"
---

# AGENTS.md — softwareco/owned

## Scope
Lane-root defaults for `softwareco/owned/`.
This file is parent context for the brownfield owned lane root and descendant repos nested under it.

## First-principles boundary
Because AGENTS files are concatenated from parents into leaf repos:
- keep this file concise and lane-level
- keep repo-specific implementation rules in each repo's own `AGENTS.md`
- avoid duplicating detailed decision logs here

## Guardrails
- Keep lane-root work in the lane root; child-repo implementation belongs in the child repo that owns it.
- Track deferred work in Agent Kernel, not scattered TODOs.
- When explicit task scope is in play, author it in AK and freeze repo-consumption snapshots via `ak task scope show|export ...`; treat `governance/task-scopes/AK-*.snapshot.json` as AK exports, not manual truth.

## Deterministic tooling
- Prefer deterministic wrappers (for example `./scripts/rocs.sh`) over ad-hoc one-off scripts.
- Prefer the standardized repo-local `Justfile` surface when present: `just help`, `just test`, `just check`, `just build`, `just lint`, `just fmt`, `just ci`, `just doctor`, plus `just run` when the repo has a truthful one-shot primary entrypoint and `just dev` when the repo has a natural dev/watch surface.
- Transition rule: if a `softwareco/owned` repo does not yet expose that standard `Justfile` surface, read `/home/tryinget/ai-society/softwareco/owned/docs/project/standardized-justfile-contract.md` and establish it from that repo root with `pi -p "/establish-standard-justfile"`.
- Engineering-core adoption coverage uses the lane-root wrapper `./scripts/engineering-core-adoption-scan.sh`, which delegates scanner semantics to `~/ai-society/core/engineering-core`; generated dashboard/snapshot files remain owned lane-root projections.
- Use inline Python only as an explicit fallback when no deterministic command exists.

## Cross-repo routing
- Use `docs/project/repo-capability-map.md` when you need to choose the right owned repo from vague cues or an arbitrary working directory.
- Treat lane-root routing summaries as conservative hints; confirm authority and runtime boundaries in the selected repo's own docs before implementing.

## Default bounded read order inside owned repos
1. Apply the already injected ancestor and deepest repo/package `AGENTS.md` instructions; confirm the selected owner repo before reading broadly.
2. Read the exact AK task scope or owner-supplied file set when one exists.
3. For engineering work, read the nearest `docs/engineering.local.md` and use the workspace compact `jq` projection for `policy/engineering-lane.json` when present.
4. If more documentation discovery is needed, run task-focused `docs-list` from the selected repo.
5. Read only the selected documents needed for the task; do not bulk-read documentation directories.

Use `docs/_core/`, `docs/org_context/`, `docs/project/`, `docs/decisions/`, `docs/learnings/`, `diary/`, and `docs/system4d/` as discovery categories, not a mandatory ingestion sequence.
