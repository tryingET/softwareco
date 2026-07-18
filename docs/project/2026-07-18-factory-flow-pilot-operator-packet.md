---
summary: "Worked operator packet and canonical command path for the first Softwareco Factory Flow pilot."
read_when:
  - "Operating or reviewing the fcos-proving-lane retirement pilot."
  - "Testing whether a cold-start operator can follow the Factory Flow Protocol without private coaching."
type: "operator-packet"
status: "proposed_pre_adr"
as_of: "2026-07-18"
---

# Factory Flow pilot operator packet

## Boundary

This is a **worked pre-ADR packet** for safe retirement of `softwareco/owned/fcos-proving-lane`. It is a linked view, not canonical authority. Before an accepted ADR, use only the read-only inspection commands below.

## Packet identity

| Field | Value |
|---|---|
| packet ID | `SOFTWARECO-FACTORY-PILOT-001` |
| packet revision | `2` — supersedes revision 1 in Git history because Decision 62 now exists |
| generated/reconciled | 2026-07-18; exact timestamp and source revisions are frozen in the next tracked revision |
| reconciliation owner | `softwareco-cto-agent` under scoped preparation task `#4028`; human operator retains decision authority |
| freshness | stale after 24 hours or immediately on any referenced AK/Git/FCOS/delegation change |
| work class | committed-flow candidate; not admitted before ADR |
| risk tier | R2 shared/stateful evidence concern |
| selected outcome | make the proving lane unambiguously historical while preserving all unique evidence |
| residual accountable authority | current higher-level human operator |
| proposed post-ADR technical steward | Softwareco CTO Agent; pre-ADR authority is limited to scoped packet preparation under task `#4028` |
| source owner | `softwareco/owned/fcos-proving-lane` |
| current FCOS product owner | `holdingco/fcos-control-board` |
| canonical pilot decision | AK Decision `#62`, currently `review_pending`; not authorizing |
| canonical strategic frame | not yet created; prohibited before ADR acceptance |
| canonical execution task | preparation task `#4028`; post-ADR source-owner task not yet created |
| FCOS item | not required unless a later cross-owner gate proves necessary |
| packet status | proposed / fail-closed for mutation |

## Canonical-source map

| Fact | Read from | Change through |
|---|---|---|
| Softwareco direction | `ak direction export -r ~/ai-society/softwareco` | `ak direction create` after accepted ADR |
| RFC/decision lifecycle | tracked RFC/reviews plus `ak decision show` | AK decision commands and tracked artifacts |
| execution scope/state | `ak task show` in the owning repo | scoped AK task commands |
| proving-lane bytes | Git object/worktree plus preservation manifest | source-owner task after ADR |
| FCOS product authority | `holdingco/fcos-control-board` docs and `fcos status` | FCOS owner surface only |
| retirement projection | capability/fleet owner surfaces | their owner task or accepted propagation path |
| terminal decision | AK decision/evidence plus human acceptance | human operator through accepted decision path |

## Cold-start read-only path

```bash
# 1. Confirm Softwareco factory direction is not yet active.
ak direction export -r ~/ai-society/softwareco
ak decision show 62
ak decision passport 62

# 2. Inspect the selected source owner without mutating it.
cd ~/ai-society/softwareco/owned/fcos-proving-lane
git status --short
git log --oneline -12
ak direction export -r "$PWD"
ak task ready -r "$PWD"

# 3. Confirm the actual FCOS product owner.
cd ~/ai-society/holdingco/fcos-control-board
fcos status --json

# 4. Read the candidate selection and RFC.
cd ~/ai-society/softwareco
cat docs/project/2026-07-18-factory-flow-pilot-fcos-proving-lane.md
cat docs/project/2026-07-12-software-factory-operating-system-rfc.md
```

Expected interpretation:

- no Softwareco pilot direction before ADR;
- proving lane is dirty historical/canary material, not a clean retirement target;
- native FCOS authority remains in `fcos-control-board`;
- this packet cannot authorize mutation.

## Stale/conflict test

The packet is stale if any of these change:

- proving-lane HEAD or status count;
- AK direction/task/decision state;
- current FCOS owner declaration;
- RFC hash or controlling review outcome;
- human delegation or revocation.

When stale:

1. mark the packet `stale`;
2. do not admit, mutate, promote, or close from packet content;
3. re-read owner-native state;
4. update owner-native records first;
5. regenerate this packet or its post-ADR successor;
6. preserve the previous revision in Git history.

Emergency data-loss containment may still stop automation or copy bytes read-only; it must not delete or reclassify authority.

## Post-ADR execution outline

Only after ADR acceptance:

1. create/activate the Softwareco strategic frame;
2. create one bounded implementation wave if grouping is useful;
3. create a source-owner AK task with explicit allowed/required/forbidden paths;
4. create a preservation bundle outside destructive paths;
5. inventory and hash tracked changes, untracked files, ignored files, refs, stashes, object reachability, nested repos/submodules, and relevant file metadata;
6. rehearse full restoration in a disposable directory and compare manifests;
7. route misplaced work through the owning repo;
8. update active maps/scans only through their owners;
9. record validation evidence;
10. ask the human operator for the terminal decision.

## Required preservation manifest fields

```text
canonical repository path and filesystem identity
repo HEAD plus all refs, tags, branches, and stash inventory
reachable/unreachable object inventory or verified bundle/fsck receipt
worktree porcelain-v1 -z bytes + SHA-256
tracked binary-safe diff patch + SHA-256
untracked file manifest + per-file SHA-256
ignored-file manifest + per-file SHA-256
file type, executable bit, symlink target, size, and permission metadata where restoration depends on it
submodule/nested-repo/worktree inventory
classification per changed, untracked, and ignored path
source owner per retained artifact
restoration command, disposable target, and byte/metadata comparison result
recovery commander, decision deadline, blast-radius boundary, dependencies, and reconciliation owner
excluded/destructive actions
human acceptance reference
```

## Failure containment and organizational unwind

| Concern | Pilot value |
|---|---|
| containment commander | human operator; CTO Agent may immediately stop automation and perform read-only capture |
| decision deadline | containment is immediate; human continue/stop/redirect decision within 30 minutes of an integrity/authority trigger when available |
| recovery horizon | restoration proof must complete inside the initial four-hour execution budget or the pilot stops/continues through explicit human decision |
| blast radius | `fcos-proving-lane` bytes plus a new external preservation directory; no FCOS product, fleet, capability-map, or source-owner mutation until restoration passes |
| dependencies | Git object database, local filesystem/storage, SHA-256 tooling, AK readback, and explicit owner routes for misplaced artifacts |
| reconciliation owner | CTO Agent prepares reconciliation; human operator accepts authority/retirement consequences |
| protocol unwind | mark packet historical, close/supersede pilot task and delegation, leave canonical owner state intact |
| organizational unwind | restore displaced task/capacity posture, notify affected owner surfaces, and preserve the stop/redirect rationale |

An irreversible migration has no place in the first wave. Physical repository deletion is a separate later decision.

## Stop conditions

Stop immediately when:

- a dirty or untracked path lacks classification;
- a path may contain secrets or private data;
- repository identity or hashes drift during capture;
- the target owner is disputed;
- restoration cannot reproduce the captured bytes;
- a proposed action would delete the source repository;
- an FCOS product mutation is proposed without FCOS owner authorization;
- the human operator revokes CTO-Agent delegation.

## Success and overhead observations

Record separately:

- protocol conformance;
- pilot effectiveness;
- operator cold-start outcome;
- preparation/update time;
- blocked age;
- unclassified-path count;
- authority-drift incidents;
- human terminal decision.

A complete packet with no outcome improvement is not a successful pilot.

A pilot counts toward later propagation only when it has: protocol conformance, effectiveness `improved`, canonical terminal decision, cold-start and recovery evidence, overhead evidence, and mandatory KES learning crystallization. A second materially different human-facing pilot and a separate template-owner decision remain required.
