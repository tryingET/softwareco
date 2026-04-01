---
summary: "Group-level defaults for infrastructure repos under softwareco/infra."
read_when:
  - "You work in softwareco infra repos and need lane-level guardrails."
  - "You are separating infrastructure-archetype policy from repo-specific operations."
type: "reference"
---

# AGENTS.md — softwareco/infra

## Scope
Group-level defaults for infrastructure/platform repos under `softwareco/infra/`.
This file is parent context for infra repos.

## First-principles boundary
Parent AGENTS files are injected into every descendant repo prompt.
Therefore this file stays:
- concise
- meta-level
- infrastructure-archetype focused

Repo-specific operational details belong in each infra repo's local `AGENTS.md`.

## Guardrails
- No secrets in git.
- Main-first workflow: commit directly to `main` for normal repo work.
- Use GitHub PRs for releases or when the operator explicitly asks for review.
- Track deferred work in `governance/work-items.json` where available.
- If an infra repo uses repo-local direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`), update them in the same pass when a direction slice task lands, or bind the doc-sync follow-up into AK with an explicit deferral.
- In infra repos that import runtime links from direction docs, use typed refs such as `task:` / `decision:` instead of raw `#123` shorthand.
- Treat `ak direction check` as an authority-reconciliation gate when that substrate exists, not just a markdown parser smoke test.

## Deterministic tooling
- Prefer deterministic wrappers (`./scripts/rocs.sh`, repo scripts) over ad-hoc shell/Python.
- Use inline Python only when no deterministic command exists.

## Default read order inside infra repos
1. `docs/_core/` (if present)
2. `docs/org_context/` (if present)
3. `docs/project/`
4. `docs/decisions/`
5. `docs/learnings/`
6. `diary/`
7. repo `AGENTS.md`
