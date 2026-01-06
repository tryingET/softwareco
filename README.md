# softwareco-templates

SoftwareCo-specific repo templates (overrides vs HoldingCo).

Copier templates:
- `copier/tpl-agent-repo`
- `copier/tpl-org-repo`
- `copier/tpl-project-repo`

Usage:
- run copier via uv: `uvx copier --version`
- create repo tree: `./scripts/new-repo-from-copier.sh tpl-org-repo /path/to/dest -d repo_slug=softwareco-handbook`
