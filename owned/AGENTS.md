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
- No secrets in git.
- Branch + MR workflow.
- Track deferred work in `governance/work-items.json` (not scattered TODOs).

## Deterministic tooling
- Prefer deterministic wrappers (e.g., `./scripts/rocs.sh`) over ad-hoc one-off scripts.
- Use inline Python only as an explicit fallback when no deterministic command exists.

## Default read order inside owned repos
1. `docs/_core/` (if present)
2. `docs/org_context/` (if present)
3. `docs/project/`
4. `docs/decisions/`
5. `docs/learnings/`
6. `diary/`
7. repo `AGENTS.md`
