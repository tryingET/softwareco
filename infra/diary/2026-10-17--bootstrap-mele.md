---
summary: "Created the thin MeLE repo through tpl-project-repo and added infra discovery routing without machine changes."
read_when:
  - "Tracing the creation and discoverability of infra/mele"
type: "diary"
---

# MeLE repository bootstrap

Operator approved the thin integration/recovery direction and explicitly requested
the infra project template. AK7176 scopes parent bootstrap and routing; AK7177 scopes
the new repository documentation. Neither task is closed by this record.

Ran Softwareco `scripts/new-repo-from-copier.sh tpl-project-repo` at L1 revision
`91b17e983d18e9169ec8425bb74e19c733ac3009`, using Copier 9.11.1 with `repo_slug=mele`,
`location=infra`, `language=bash`, software pack off and compact org context.
Destination: `~/ai-society/softwareco/infra/mele`; local main, no Git remote.
Guarded AK bootstrap classified the canonical leaf auto-safe and registered it
(evidence 16001). The child repo is ignored by the infra parent as designed; no
new submodule/gitlink or parent ignore-policy change was made.

Added the MeLE row in `docs/project/repo-capability-map.md`. The existing foreign
`issue-tracker` gitlink change was not staged or modified. No template, dotfiles,
provisioning, workstation runtime or remote machine source was changed.

Child evidence lives at `mele/docs/project/2026-10-17-observed-state.md` and its raw
readback, relative to the infra directory. Those records distinguish live MeLE
60 Hz/scale 1.25 from the snapshot's 100 Hz and stock running niri from Steve's
selected custom binary. Recovery is a preflight document, not a completed restore.
The child check log is in its diary; final check results belong in AK evidence.

Existing shared-owner work stays in AK5999/AK6000. New AK7178 retains the planning
slice for machine recovery/backup/offline acceptance with no live-apply authority.
No push, restart, package installation, dotfiles application or lifecycle closure.

Parent verification: `scripts/ci/smoke.sh`, `git diff --check` and strict docs
metadata over `docs/project/` passed. Broad `--docs docs --strict` failed because
`docs/learnings/README.md` lacks frontmatter/read_when; the defect is present at
HEAD, outside this task, and retained in AK7179. No unrelated repair was attempted.
The legacy parent full script was not run: it cleans/rebuilds ontology artifacts
outside the documentation-only scope. Child full checks are separate evidence,
not a substitute for a parent full run.
