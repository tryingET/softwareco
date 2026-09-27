---
summary: "Infra-owned retry index for the three collision-skipped engineering-core v0.12.0 consumers from AK6051."
read_when:
  - "Resuming the infra portion of the engineering-core v0.12.0 fleet rollout."
  - "Checking why issue-tracker, workstation, or replay-fabric still pins an older release."
type: "rollout-projection"
---

# Engineering-core v0.12.0 — infra batch-2 retry index

This is an owner-local **projection**, not a second task ledger or a claim that the repos have migrated. AK task **6051** is the completed batch disposition and evidence source (`ak task show 6051`; `ak evidence task 6051`). AK task **6093** was closed as superseded: exact repo tasks AK6104–AK6106 handled the retries at the newer v0.12.1 release. The source procedure and exact target pin are in `~/ai-society/core/engineering-core/docs/project/2026-09-27-v0.12.0-fleet-rollout.md`.

At the original retry-index capture, each policy declared `engineering_core.ref: v0.7.0`. **Current resolution (2026-09-27):** `issue-tracker` is `v0.12.1` under AK6104, committed **local-only** because a prior stranded commit prevented pushing; `workstation` is `v0.12.1` and pushed under AK6105; `replay-fabric` is `v0.12.1` and pushed under AK6106. These are AK result claims with policy readback, not a new gate run by AK6093. Do not rerun the historical retry instructions as a fresh migration. Read the exact tasks for validation and remaining transport constraints.

| Repo | AK6051 evidence | Why skipped | Retry condition |
|---|---:|---|---|
| `issue-tracker` | 10866 | A live Claude session had the repo as its working directory; a recent non-owned commit was present. | Agent has finished; re-run git status/fetch, recency and live-process checks. |
| `workstation` | 10867 | Live Claude/Pi sessions and a heavily dirty working tree. | Agents have finished and files the migration needs are unmodified; re-run the full preflight. |
| `replay-fabric` | 10868 | Live Claude session and dirty docs/source/tests; branch had non-owned unpushed commits. | Agent has finished, target files are clear and branch/upstream state has been rechecked. |

## Historical retry procedure (not an open queue)

1. For any future release, work **one repo at a time** under a new exact owner task, not completed AK6093. Read the source handoff fully; repeat its preflight, baseline gate, pin/lane adoption, post-change gate, scan, explicit-path commit and push check. Skip or block rather than collide or guess. Do not remove anyone's files or locks.
2. Record fresh AK evidence per repo and keep the disposition in the AK task result. A structural `engineering-core scan-adoption` result is a pin/shape observation, not proof that a gate passed, a commit was pushed, or a skipped repo became safe to edit.
3. This index can be revised from AK evidence as a human-readable scope-owner view; it must not independently advance a repo's status.

`ds1621-admin` (`d47bfa2`) and `ts-quality-tools` (`c0461ba`) were migrated **local-only** under AK6051. A later readback showed `ds1621-admin` level with its tracking branch, but this index does not claim who pushed it. `ts-quality-tools` remains one commit ahead with a GitHub remote that returned repository-not-found; transport/remote ownership is tracked by AK6142, not a blind push. Future engineering-core releases do not automatically propagate to consumers: each repo owns its selected pin, local deviations, validation and landing, while engineering-core owns the reusable guidance and scanner.
