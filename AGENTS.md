---
summary: "Company-level lane policy for softwareco repositories."
read_when:
  - "You start work in a softwareco repo and need lane-level routing and shared guardrails."
  - "You are editing lane/group/repo AGENTS files under softwareco."
type: "reference"
---

# AGENTS.md — softwareco

## Intent
Coordinate Software Company work across explicit lanes:
- `owned/` — directly operated delivery repos
- `infra/` — platform/runbooks/internal infrastructure
- `contrib/` — upstream-coupled repos
- `agents/` — AI-agent-focused repos
- `fork/` — maintained forks and deliberate divergence repos when upstream scope no longer fits

## Guardrails
- Main-first workflow: commit directly to `main` for normal work.
- Use GitHub PRs only for releases or when the operator explicitly asks for a review gate.
- Pick lane first, then follow lane policy and template contract.
- No secrets in git.
- Keep `.copier-answers.yml` committed in all repos.
- Use repo-local `diary/` capture in descendant repos; do not invent a company-wide diary authority.

## Shared tooling
- Docs discovery/scoping: use target-repo `./scripts/docs-list.sh --task "<task>" --top 8` when that wrapper exists; otherwise run `~/ai-society/softwareco/scripts/docs-list.sh --task "<task>" --top 8` from the target repo.
- Prompt read-scope allowlist: use the same wrapper selection with `--from-prompt <prompt-file> --paths-only --wikilink`.
- Repo census preflight: `./scripts/preflight-repo-census.sh [scope]`
- Deterministic ROCS launcher: `./scripts/rocs.sh <rocs args...>`
- New L2 repo from template: `./scripts/new-repo-from-copier.sh <template> <dest> -d repo_slug=<slug> --defaults`
- Lane bootstrap helper: `./scripts/bootstrap-lane-root.sh <lane> [--init-lane-git]`

## Deterministic tooling policy (ROCS-first)
- Prefer `./scripts/rocs.sh <args...>` before ad-hoc inline scripting.
- For ontology/policy checks, use ROCS commands as the default execution path.
- Use inline Python only as an explicit escape hatch when no deterministic command exists.

## L2 Templates (in copier/)

| Template | Purpose | Generates |
|----------|---------|-----------|
| `copier/tpl-project-repo/` | Delivery projects | `owned/<project>/`, `infra/<project>/`, `contrib/<project>/`, or lane-root baselines |
| `copier/tpl-agent-repo/` | AI agent repositories | `agents/agent-<slug>/` |
| `copier/tpl-org-repo/` | Organization handbooks | `<org>-handbook/` |
| `copier/tpl-monorepo/` | Monorepo workspaces | `<monorepo>/` (packages + apps) |
| `copier/tpl-package/` | Packages inside monorepos | `packages/<name>/` (NO .git) |

## Lane root bootstrap (before nesting child repos)

Use this two-phase sequence so lane roots track baseline control-plane files while child repos remain ignored:

```bash
# 1) Materialize lane baseline in the parent repo
./scripts/bootstrap-lane-root.sh fork

# 2) Commit lane baseline in parent repo
git add .gitignore fork
git commit -m "chore: bootstrap fork lane baseline"

# 3) Initialize lane-root git repo
./scripts/bootstrap-lane-root.sh fork --init-lane-git
```

## Placement reminders
- owned: `~/ai-society/softwareco/owned/<repo>`
- infra: `~/ai-society/softwareco/infra/<repo>`
- contrib: `~/ai-society/softwareco/contrib/<upstream-or-repo>`
- agents: `~/ai-society/softwareco/agents/agent-<slug>`
- fork: `~/ai-society/softwareco/fork/<repo>`

## Recursion policy (explicit)
Allowed:
- `L0 -> L1`
- `L1 -> L2`

Forbidden:
- `L1 -> L0`
- `L2 -> L1`
- any cycle
