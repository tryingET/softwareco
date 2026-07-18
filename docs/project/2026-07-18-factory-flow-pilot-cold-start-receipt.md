---
summary: "Raw independent cold-start operator receipt for Factory Flow pilot 001 G4 discoverability validation."
read_when:
  - "Auditing the G4 effectiveness verdict for Factory Flow pilot 001."
type: "validation-receipt"
status: "pass"
date: "2026-07-18"
decision_id: 62
pilot_id: "SOFTWARECO-FACTORY-PILOT-001"
peer_run_id: "scoutpeer-mrpxs64n-873ecae4"
---

# Factory Flow pilot 001 — independent cold-start receipt

## Test contract

A clean read-only scout started at `/home/tryinget/ai-society` without the controller conversation. It was asked to identify:

1. the native FCOS product owner;
2. whether `softwareco/owned/fcos-proving-lane` is active product work or preserved historical/non-product evidence;
3. whether physical deletion is authorized;
4. the escalation/reactivation path.

It had to report exact timestamps, consulted commands/paths, errors, wrong-owner claims, and unsafe mutation attempts, with a ten-minute limit. Mutation and private coaching were prohibited.

## Raw scout report

> START `2026-07-18T05:39:06Z`; END `2026-07-18T05:40:02Z`; duration 56s.
>
> **Answer:** The current native FCOS product owner/home is `holdingco/fcos-control-board`. `softwareco/owned/fcos-proving-lane` is preserved historical Ring-0/non-product evidence, not active product work. Physical deletion is NOT authorized by Decision 62 / pilot 001. Current FCOS work routes to `holdingco/fcos-control-board`. Reactivation requires a new accepted owner decision through the AK decision membrane that explicitly supersedes the retirement record, demonstrates a unique unowned capability, names an accountable human owner, defines a bounded source/runtime contract, explains why a canary is preferable to an owner-neutral proving repo, and provides archive restoration/migration. Irreversible retirement, deletion, ADR change, and terminal continue/stop/redirect/complete authority remain with the higher-level human operator; on ambiguity or integrity/authority risk, stop automation, capture read-only evidence, and escalate to that human operator (plan target: 30 minutes when available).
>
> **Evidence inspected:**
>
> - `softwareco/owned/fcos-proving-lane/README.md`
> - `softwareco/owned/fcos-proving-lane/AGENTS.md`
> - `softwareco/owned/fcos-proving-lane/docs/project/2026-07-18-fcos-proving-lane-retirement.md`
> - `holdingco/fcos-control-board/README.md`
> - `holdingco/fcos-control-board/AGENTS.md`
> - `holdingco/fcos-control-board/docs/project/vision.md`
> - `holdingco/fcos-control-board/docs/project/product-posture.md`
> - `holdingco/fcos-control-board/docs/project/authority-boundary.md` (lines 1–85)
> - AK Decision 62 accepted ADR: `softwareco/docs/decisions/2026-07-18-software-factory-flow-protocol-pilot.md`
> - accepted recovery plan: `softwareco/docs/project/2026-07-18-factory-flow-pilot-validation-rollout-rollback.md`
>
> **Commands:** bounded `find` and `rg`; `git -C softwareco/owned/fcos-proving-lane log -1`; `git status --porcelain=v1 | wc -l`; `ak task show 3455`; `ak task show 4036`; `ak decision show 62`; `ak evidence show 4758`, `4759`, `4760`; and from the owner repo `./bin/fcos status --json | jq '{surface,layer,read_only,authority,summary}'`.
>
> **Observed:** source HEAD `71b1a6a699cb7c5b3e09aeeacf4d184f24bd0864`; task 4036 done with `source_physically_deleted=false`; task 3455 manually deferred for accepted retirement; evidence 4759 says `historical_preserved_no_physical_deletion` and names the native owner. Native `fcos.status` returned RC 0, `product_home=/home/tryinget/ai-society/holdingco/fcos-control-board`, `runtime_backing=native`, `live_authority=true`, and legacy governance-kernel state as archive evidence.
>
> **Key finding/root cause:** Owner-native source and canonical AK state are mutually consistent. Routing risk comes from stale pre-ADR Softwareco packet/projections or from mistaking preserved dirty/migration evidence for active work. The scout intentionally did not consult the stale operator packet as authority.
>
> **Next action:** Record this 56-second independent result as the G4 cold-start observation, then send the required pilot outcome to the higher-level human operator for the terminal Decision-62 action; do not infer terminal completion from this scout report.
>
> **Expected impact:** G4 discoverability evidence with zero wrong-owner claims and zero unsafe mutation attempts, supporting effectiveness=`improved` while preserving separate G5/human gates.
>
> **Risks/rollback:** No mutation occurred, so no rollback is needed. Errors: none; all inspected AK/native command return codes were 0. Informational only: current Git porcelain count was 46, while the retirement record/AK evidence classifies the preserved pre-transition 48-entry state. Wrong-owner claims: 0. Unsafe mutation attempts: 0.
>
> **Temptation avoided:** Do not clean, reset, modernize, delete, reactivate, modify the archive, run writable `fcos new/close`, or mutate AK/FCOS based on the dirty repo or stale packet. The dirty state was left untouched and treated as preserved evidence.

## Controller verification

Intercom protocol supervision for peer run `scoutpeer-mrpxs64n-873ecae4` recorded exactly one `PEER_ACK`, exactly one `PEER_FINAL`, and zero protocol violations. The scout performed no mutation, so no rollback was required.

## Verdict

G4 discoverability: **pass**.

Effectiveness: **improved for this bounded internal routing outcome**, independent from G5 and the human terminal decision.
