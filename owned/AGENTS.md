---
summary: "Group-level defaults for delivery repos under softwareco/owned."
read_when:
  - "You work in softwareco owned repos and need archetype-level guardrails."
  - "You are deciding whether guidance belongs at lane level or repo level."
type: "reference"
---

# AGENTS.md — softwareco/owned

## Scope
Group-level defaults for delivery repos under `softwareco/owned/`.
This file is parent context for every owned repo.

## First-principles boundary
Because AGENTS files are concatenated from parents into leaf repos:
- keep this file concise and archetype-level
- keep repo-specific implementation rules in each repo's own `AGENTS.md`
- avoid duplicating detailed decision logs here

## Guardrails
- Track deferred work in Agent Kernel, not scattered TODOs.
- Treat `governance/work-items.json` as the repo-local deterministic projection emitted from AK, and operate on it through `./scripts/ak.sh` rather than manual edits.
- If a repo uses repo-local direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`), update those docs in the same pass when a direction slice task lands, or bind the doc-sync follow-up into AK with an explicit deferral.
- In repos that import task links from direction docs, use typed refs such as `task:` / `decision:` instead of raw `#123` shorthand.
- Treat `ak direction check` as an authority-reconciliation gate when that substrate exists, not just a markdown parser smoke test.

## Deterministic tooling
- Prefer deterministic wrappers (e.g., `./scripts/rocs.sh`) over ad-hoc one-off scripts.
- Prefer the standardized repo-local `Justfile` surface when present: `just help`, `just test`, `just check`, `just build`, `just lint`, `just fmt`, `just ci`, `just doctor`, plus `just run` when the repo has a truthful one-shot primary entrypoint and `just dev` when the repo has a natural dev/watch surface.
- Transition rule: if a `softwareco/owned` repo does not yet expose that standard `Justfile` surface, read `/home/tryinget/ai-society/softwareco/owned/docs/project/standardized-justfile-contract.md` and establish it from that repo root with `pi -p "/establish-standard-justfile"`.
- Use inline Python only as an explicit fallback when no deterministic command exists.

## Default read order inside owned repos
1. `docs/_core/` (if present)
2. `docs/org_context/` (if present)
3. `docs/project/`
4. `docs/decisions/`
5. `docs/learnings/`
6. `diary/`
7. repo `AGENTS.md`
