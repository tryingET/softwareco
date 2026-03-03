---
summary: "Company-level lane policy for softwareco repositories."
read_when:
  - "You start work in a softwareco repo and need lane-level routing and shared guardrails."
  - "You are editing lane/group/repo AGENTS files under softwareco."
type: "reference"
---

# AGENTS.md — softwareco

## Scope
Company-level policy for repos under `softwareco/`.
Keep this file lane-oriented and stable.

## Lanes
- `owned/` — directly operated delivery repos
- `infra/` — platform/runbooks/internal infrastructure
- `contrib/` — upstream-coupled repos
- `agents/` — AI-agent-focused repos

## Layering rule
This file is parent context for all lane/repo AGENTS below.
Therefore:
- keep rules meta-level
- avoid project-specific implementation details
- push concrete execution rules to leaf repos

## Guardrails
- No secrets in git.
- Branch + MR workflow (no direct `main` pushes).
- Keep `.copier-answers.yml` committed where templates expect it.

## Shared tooling
- Docs discovery: `./scripts/docs-list.sh --task "<task>" --top 8`
- Deterministic ROCS launcher: `./scripts/rocs.sh <rocs args...>`
- New L2 repo from template: `./scripts/new-repo-from-copier.sh <template> <dest> -d repo_slug=<slug> --defaults`
