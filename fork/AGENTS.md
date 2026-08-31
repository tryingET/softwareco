---
summary: "Group-level defaults for maintained forks under softwareco/fork."
read_when:
  - "You work in softwareco fork repos and need lane-level guardrails."
  - "You are deciding whether upstream divergence belongs in fork/ or another lane."
type: "reference"
---

# AGENTS.md — softwareco/fork

## Scope
Group-level defaults for maintained forks and deliberate divergence repos under `softwareco/fork/`.
This file is parent context for every fork repo.

## First-principles boundary
Because parent AGENTS files are injected into all descendants:
- keep this file concise and lane-level
- keep repo-specific divergence strategy in each fork repo's own `AGENTS.md`
- avoid copying upstream-specific issue history here

## Guardrails
- No secrets in git.
- Main-first workflow: commit directly to `main` for normal repo work.
- Use GitHub PRs for releases or when the operator explicitly asks for review.
- Treat `docs/_core/**` as immutable.
- Track active and deferred work in Agent Kernel (`ak task ready|list|show`); the generic checked-in `governance/work-items.json` mirror is retired under accepted Decision 127, while frozen task-scope exports and owner-native state remain separate.
- Record why the fork exists and what upstream boundary failed in repo-local docs/decisions.
- If a fork repo uses repo-local direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`), update them in the same pass when a direction slice task lands, or bind the doc-sync follow-up into AK with an explicit deferral.
- In fork repos that import runtime links from direction docs, use typed refs such as `task:` / `decision:` instead of raw `#123` shorthand.
- Treat `ak direction check` as an authority-reconciliation gate when that substrate exists, not just a markdown parser smoke test.

## Deterministic tooling
- Prefer deterministic wrappers (`./scripts/rocs.sh`, repo scripts) over ad-hoc shell/Python.
- Use inline Python only when no deterministic command exists.

## Fork-lane intent
Use `fork/` when:
- upstream scope or governance no longer fits the required feature set
- long-lived divergence is intentional
- the work is no longer best modeled as upstream follow-up tickets alone

Do not use `fork/` for:
- normal first-party delivery repos (`owned/`)
- platform/runbook repos (`infra/`)
- upstream-coupled mirrors you still mainly contribute back to (`contrib/`)

## Default read order inside fork repos
1. `docs/_core/` (if present)
2. `docs/org_context/` (if present)
3. `docs/project/`
4. `docs/decisions/`
5. `docs/learnings/`
6. `diary/`
7. repo `AGENTS.md`
