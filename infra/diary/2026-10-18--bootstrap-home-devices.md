---
summary: "AK7219: bootstrapped home-devices with tpl-project-repo and added infra discovery routing; no live-device changes."
read_when:
  - "Locating the household device catalogue or tracing its creation."
type: "diary"
---

# Home-devices bootstrap

Operator selected home-devices and documentation-first catalogue/cinema definition in the
interview. Created `~/ai-society/softwareco/infra/home-devices` via Softwareco's canonical
`new-repo-from-copier.sh tpl-project-repo` wrapper at source revision
`91b17e983d18e9169ec8425bb74e19c733ac3009`, Copier 9.11.1, software pack disabled, compact docs.
Local main, no remote. Guarded AK bootstrap registered the canonical leaf (evidence 16144).
Child documentation scope is task:7220; parent bootstrap/routing is task:7219.

Added one row to `docs/project/repo-capability-map.md`. The child remains ignored by the parent
as designed; no submodule/gitlink or ignore-rule change. Existing issue-tracker changes remain
foreign and must not be staged with this work. No home-network/workstation source migration.

Child catalogue covers dated AV/Loxone, solar, appliances, owner-linked computers/displays and
infrastructure. Cinema/PWA/health collection remain proposals. Phone presence is opt-in only,
with no collection enabled. No device contact or physical effect occurred in this bootstrap.
See the child diary for evidence, source limitations and its full-check results.

Parent verification is scoped to smoke, changed documentation metadata and diff whitespace.
The legacy parent full script cleans/rebuilds unrelated ontology artifacts and is outside this
documentation-only task. No claim of parent full verification, deployment, push or lifecycle
closure. Final evidence/task state is in AK.
