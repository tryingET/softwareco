# AGENTS.md (softwareco)

Preferred workflow:
- `rocs summary --repo .`
- `rocs pack <concept_id> --repo . --profile company-agent`

Do not load all files; use concept-level retrieval.

GitLab (NAS):
- API (issues/MRs/etc): `gl-nas -- <gitlab-cli args...>`
- Git (clone/fetch/push): `gl-nas-git -- <git args...>`
- Reference: `holdingco/governance-kernel/docs/dev/gitlab-access.md`
