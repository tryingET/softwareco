---
summary: "Terminal linked operator view for completed Factory Flow pilot 001."
read_when:
  - "Reviewing completed Factory Flow pilot 001 or its retained evidence and limits."
  - "Checking current FCOS ownership and fcos-proving-lane retirement without private coaching."
type: "operator-packet"
status: "complete_historical_packet"
as_of: "2026-07-18T06:02:23Z"
decision_id: 62
pilot_id: "SOFTWARECO-FACTORY-PILOT-001"
---

# Factory Flow pilot 001 — operator packet

## Boundary

This is a **post-ADR linked view**, not canonical authority. Owner-native Git/runtime state and AK win on conflict. The packet authorizes no physical deletion, FCOS product mutation, second pilot, or template propagation.

## Packet identity

| Field | Current value |
|---|---|
| packet revision | 3; supersedes the pre-ADR revision 2 in Git history |
| reconciled through | `2026-07-18T06:02:23Z` |
| reconciliation owner | `softwareco-cto-agent` under task `#4028`; higher-level human operator selected terminal `complete` |
| freshness | stale on referenced source/owner Git change, AK decision/task/direction lifecycle change, delegation change, or human terminal decision |
| accepted decision | AK `#62`, `unblocked / accepted` |
| governing ADR | `docs/decisions/2026-07-18-software-factory-flow-protocol-pilot.md` |
| reviewed RFC blob / SHA-256 | `ff27c45a112e152dd891d9f7ddb79db34055d8eb` / `9b0c14de59e5f2f55519d28e5272588f883eed857cc33e70971eb1b05c1531a7` |
| strategic frame / wave | `SF1` / `IW-SF1-PILOT-001`, archived after terminal completion |
| coordination task | `#4028`, done |
| preservation task | `#4035`, done |
| source retirement task | `#4036`, done |
| preserved source HEAD / status SHA-256 | `aa9fe9e6a5d2b636ea91ab18d2e01d6de2a9588f` / `12e79926370c511fe887ca7053a36786662ee581ec0f498d9928d8e1997b07f9` |
| archive manifest SHA-256 | `ec85c71e267bf914718e835cf78f125a1deaced9e3814cd441f7285b4de9d408` |
| current proving-lane HEAD / status SHA-256 | `71b1a6a699cb7c5b3e09aeeacf4d184f24bd0864` / `c13624120c01bfcac47f2fb14c58ad59f45f3f4df063f97a567519a6c010385e` |
| current proving-lane status entries | 46; preserved, not cleaned or accepted as active product work |
| current FCOS owner revision | `holdingco/fcos-control-board@7152e0d713011b4a6416be8666fdd41d65461b59` with a dirty owner worktree; native read-only status still reports this repo as live FCOS product home |
| source status | preserved historical/non-product evidence; no physical deletion |
| residual accountable authority | current higher-level human operator |
| technical delegate | Softwareco CTO Agent pilot delegation expired at `2026-07-18T06:02:23Z` |
| human terminal decision | `complete`; AK evidence `#4781` |
| packet state | G0–G5 passed; terminally reconciled |

## Canonical-source map

| Fact | Read from | Change through |
|---|---|---|
| direction and execution lineage | `ak direction export -r ~/ai-society/softwareco`; AK task records | AK direction/task commands in the owning repo |
| decision and delegation | `ak decision passport 62`; accepted ADR | human decision path and AK decision/evidence surfaces |
| preserved bytes and recovery | archive manifest plus evidence `#4749`/`#4750` | human-authorized recovery path only |
| source retirement status | proving-lane `README.md`, `AGENTS.md`, and retirement record at commit `71b1a6a` | new accepted source-owner decision; not this packet |
| native FCOS product | `holdingco/fcos-control-board` owner docs and native `fcos status --json` | FCOS owner surface only |
| pilot outcome | `docs/project/2026-07-18-factory-flow-pilot-outcome.md` | tracked evidence plus human terminal decision |
| learning | `docs/learnings/2026-07-18-factory-flow-pilot-001.md` | KES acceptance/activation through its owner path |

## Current read-only operator path

```bash
# 1. Confirm accepted decision and active pilot lineage.
cd ~/ai-society/softwareco
ak decision passport 62
ak direction export -r "$PWD"
ak task show 4028

# 2. Confirm source retirement without touching preserved work.
cd ~/ai-society/softwareco/owned/fcos-proving-lane
git status --short
git rev-parse HEAD
cat README.md
cat docs/project/2026-07-18-fcos-proving-lane-retirement.md
ak task show 4036

# 3. Confirm the native FCOS product owner through its owner surface.
cd ~/ai-society/holdingco/fcos-control-board
./bin/fcos status --json

# 4. Review the measured outcome and learning.
cd ~/ai-society/softwareco
cat docs/project/2026-07-18-factory-flow-pilot-outcome.md
cat docs/project/2026-07-18-factory-flow-pilot-cold-start-receipt.md
cat docs/learnings/2026-07-18-factory-flow-pilot-001.md
```

Expected interpretation:

- `holdingco/fcos-control-board` is the native FCOS product owner;
- `fcos-proving-lane` is preserved historical/non-product evidence;
- its dirty migration/history state remains preserved;
- physical deletion is not authorized;
- reactivation requires a new accepted owner decision;
- the human terminal decision was `complete`, without authorizing physical deletion or broader rollout.

## Completed gate evidence

| Gate | Evidence |
|---|---|
| G0 authority/source | Decision `#62`; ADR; `SF1`; `IW-SF1-PILOT-001`; scoped tasks |
| G1 preservation | evidence `#4749`; manifest SHA-256 above |
| G2 restoration | evidence `#4750`; exact file/metadata/index/HEAD/status match and passing `git fsck` |
| G3 bounded rollout | source commit `71b1a6a`; evidence `#4758`–`#4760`; zero unclassified paths |
| G4 operator outcome | `docs/project/2026-07-18-factory-flow-pilot-cold-start-receipt.md`; clean scout `scoutpeer-mrpxs64n-873ecae4`: 56 seconds, 0 wrong-owner claims, 0 unsafe mutation attempts, 0 errors |
| G5 closure | outcome and KES learning tracked/attached; human `complete` recorded as evidence `#4781`; direction/task/delegation reconciled |

No FCOS item was created because no active multi-owner gate emerged. Softwareco routing maps did not claim the proving lane as an active FCOS product, so no capability-map mutation was required.

## Stale/conflict membrane

This packet is stale when any referenced source HEAD/status, archive hash, AK decision/task/direction lifecycle state, FCOS owner declaration/revision, or delegation changes. Expected evidence attachment that leaves those lifecycle facts unchanged does not by itself invalidate the packet.

On staleness or conflict:

1. stop mutation and do not close from packet content;
2. read owner-native state;
3. preserve conflicting evidence;
4. reconcile the owning surface first;
5. produce a new tracked packet revision;
6. escalate authority/integrity ambiguity to the higher-level human operator.

Emergency containment may stop automation and copy bytes read-only. It may not delete, clean, reset, reactivate, or reassign authority.

## Terminal result

The higher-level human operator selected **`complete pilot 001`**. The pilot direction is archived, task `#4028` is done, and the bounded CTO-Agent pilot delegation is expired.

This completion does not authorize factory-wide rollout, physical deletion, another pilot, FCOS authority changes, or template propagation. Reactivation or further retirement requires a new accepted owner decision.
