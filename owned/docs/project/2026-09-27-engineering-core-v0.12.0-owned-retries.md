---
summary: "Owned-lane retry index for engineering-core v0.12.0 collision skips and one blocked repo across AK6052–6054."
read_when:
  - "Planning the next engineering-core v0.12.0 adoption retry across softwareco/owned repos."
  - "Investigating why a batch-3, batch-4, or batch-5 repo remains on an older pin."
type: "rollout-projection"
---

# Engineering-core v0.12.0 — owned-lane retry index

This is an **owner-local projection**, not another task ledger. The completed batch results and per-repo evidence are in AK6052 (batch 3), AK6053 (batch 4), and AK6054 (batch 5): `ak task show <id>` and `ak evidence task <id>`. AK6096–AK6098 were closed as superseded by the exact repo tasks below; this is now historical retry context, not an open mutation queue. The exact pin, gate, collision and push rules are in `~/ai-society/core/engineering-core/docs/project/2026-09-27-v0.12.0-fleet-rollout.md`.

At the original capture, all 12 rows declared `engineering_core.ref: v0.7.0`. **Rollout resolution:** all 12 reached at least `v0.12.1` under the exact tasks below. Later on 2026-09-27, `workstation-capabilities` and `apex-cathedral` already showed `v0.12.2`; do not treat this table as a live pin inventory. The exact AK results report:

| Original batch | Consumer | Exact task | Transport / limitation |
|---|---|---:|---|
| 3 | `dep-redteam` | 6107 | Pushed |
| 3 | `workstation-capabilities` | 6108, 6139 | AK6108 was local-only; AK6139 repaired the gate, advanced to v0.12.2 and fast-forward pushed the held range |
| 3 | `email-copilot` | 6130 | Pushed `845f805`; normal UBS hook passed after a behavior-preserving local rename; full `just ci` passed |
| 3 | `agent-kernel` | 6109 | Pushed |
| 3 | `apex-cathedral` | 6110 | Pushed; SDK TypeScript 5 deviation retained |
| 4 | `dep-diet` | 6111 | Pushed |
| 4 | `obsidian-plugins` | 6112 | Pushed; existing dependency-cruiser zero-module warning remains |
| 4 | `pi-server` | 6113 | Pushed |
| 4 | `runtime-trace-insights` | 6114 | Pushed |
| 4 | `zotero-plugins` | 6115 | Pushed; pre-existing gate failures recorded in AK |
| 5 | `designmd-foundry` | 6116 | Pushed |
| 5 | `dotfiles-managed` | 6117 | Pushed; full gate still unverified due pre-existing dependency/cache and private Termux test blockers |

The owned-lane `engineering-core-adoption-dashboard.md` is a **generated structural snapshot**, not rollout authority. An existing uncommitted 2026-09-27 snapshot is partial with four omissions and predates several v0.12.1 upgrades; do not overwrite or promote it without owner review (AK6144). The owner wrapper can provide a read-only preview. AK tasks and repo pins remain the source for migration and transport facts.

## Batch 3 — AK6052 → AK6096

| Repo | Evidence | Disposition and original cause | Retry condition |
|---|---:|---|---|
| `dep-redteam` | 10967 | Skipped: live Claude agent had repo cwd. | Agent finished; repeat git/status/fetch and live-process preflight. |
| `workstation-capabilities` | 10942 | Skipped: live repo-cwd Python processes. | Processes finished or owner establishes a safe window; repeat preflight. |
| `email-copilot` | 10966 | **Blocked:** normal commit hook rejected five pre-existing UBS critical findings in `apps/operator-ui/src/App.tsx`; candidate changes were removed. | Resolve hook findings with the owner or obtain an owner-approved disposition; never bypass hooks. Repeat baseline and migration only after that. |
| `agent-kernel` | 10968 | Skipped: live Claude sessions; dirty `Cargo.lock` and other work preserved. | Agents finished and target files clear; repeat preflight. |
| `apex-cathedral` | 10969 | Skipped: required TS lane-adoption files already modified, with broader dirty work. | Owner's changes are resolved or a safe isolated handoff is arranged; do not overwrite. |

## Batch 4 — AK6053 → AK6097

| Repo | Evidence | Disposition and original cause | Retry condition |
|---|---:|---|---|
| `dep-diet` | 10953 | Skipped: live Claude agent and recent non-owned commit. | Agent finished; recheck recency and branch ownership. |
| `obsidian-plugins` | 10955 | Skipped: live Pi session and recent non-owned commits. | Agent finished; recheck Git/index state. Any pre-existing `index.lock` belongs to someone else: do not delete it. |
| `pi-server` | 10935 | Skipped: branch behind upstream; incoming `CHANGELOG.md` overlaps local dirty changes. | Owner reconciles the overlap so a clean fast-forward is possible; do not stash or reset it. |
| `runtime-trace-insights` | 10956 | Skipped: live Claude process had repo cwd. | Agent finished; repeat preflight. |
| `zotero-plugins` | 10958 | Skipped: live npm/node servers in repo and dirty package files. | Owner establishes a safe window and target files are clear. |

## Batch 5 — AK6054 → AK6098

| Repo | Evidence | Disposition and original cause | Retry condition |
|---|---:|---|---|
| `designmd-foundry` | 10954 | Skipped: live Claude/render-smoke processes and a recent non-owned commit. | Processes finished; repeat recency and file preflight. |
| `dotfiles-managed` | 10939 | Skipped: live Pi session and unrelated dirty files. | Agent finished; recheck Git/index state. Any pre-existing `index.lock` belongs to someone else: do not delete it. |

## Operating boundary

For future releases, retry **one repo at a time** under a new exact owner task, not the completed/superseded AK6096–AK6098. Start with the source handoff and the repo's own instructions; compare baseline and post-change gates, run `scan-adoption`, record fresh AK evidence, and commit/push only as permitted. An open Pi session or a structural `adopted` scan is not a completion or push receipt. Skip or block anew if the preflight still collides. Refresh this projection from AK results rather than assigning statuses here.

The former `email-copilot` hook blocker was resolved and the v0.12.1 pin was pushed under AK6130 without disabling hooks. The `workstation-capabilities` local-only range was subsequently landed under AK6139 after repairing its full-gate failure. The operator confirmed `glimpseui-linux` was deleted: AK6143 dispositions the absent checkout and the AK6054 local-only commit `47df70d` as retired, **not pushed or eligible for retry**. The exact child path has no AK repo registration; AK path resolution falls back to the owned parent, which must not be deleted. Dated rollout records remain historical evidence, not a current census. Other original local-only results must be judged against current Git and AK, not this historical table. New engineering-core releases do not automatically advance consumer pins.
