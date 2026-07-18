---
summary: "Completed protocol-conformance, effectiveness, and human terminal outcome for Softwareco Factory Flow pilot 001."
read_when:
  - "Reviewing whether Factory Flow pilot 001 satisfied its execution and outcome gates."
  - "Reviewing the human terminal completion and retained pilot limits."
type: "pilot-outcome"
status: "complete"
as_of: "2026-07-18T08:12:36Z"
decision_id: 62
pilot_id: "SOFTWARECO-FACTORY-PILOT-001"
---

# Factory Flow pilot 001 — outcome

## Verdicts

| Verdict | Result | Basis |
|---|---|---|
| protocol conformance | **pass, G0–G5** | accepted ADR and plans; governed AK execution; lossless preservation; exact restoration; zero unclassified paths; bounded owner-doc rollout; independent cold-start result; attached KES learning; human terminal completion |
| effectiveness | **improved** | a clean-context operator identified the native owner, retired status, no-deletion boundary, and escalation path in 56 seconds with zero wrong-owner claims and zero unsafe mutation attempts |
| physical deletion | **not performed / not authorized** | Decision 62 and the source retirement record prohibit it |
| factory-wide or template propagation | **not justified** | this is one internal evidence-retirement pilot, not a materially different human-facing delivery pilot |

The timeout-derived form result recorded as evidence `#4781` had consent ambiguity because the recommended option was preselected while the operator was AFK. The higher-level human operator subsequently and explicitly affirmed **`complete`** by replying `1` at `2026-07-18T08:12:36Z`. AK evidence `#4822` is the controlling terminal-authority confirmation.

## Gate results

### G0 — authority and source identity: pass

- Decision `#62`: `unblocked / accepted`.
- Governing ADR: `docs/decisions/2026-07-18-software-factory-flow-protocol-pilot.md`.
- Direction: `IW-SF1-PILOT-001` is done. AK requires exactly one active strategic root, so `SF1` is retained as `terminal_anchor_no_active_wave` rather than leaving the graph invalid; Decision 62 governs both and task `#4028` is linked to `SF1`.
- Human residual authority remained unchanged; the bounded CTO-Agent pilot delegation expired at terminal completion.

### G1 — preservation completeness: pass

- Archive: `/home/tryinget/ai-society/archive/20260718-softwareco-factory-pilot-001/`.
- Manifest SHA-256: `ec85c71e267bf914718e835cf78f125a1deaced9e3814cd441f7285b4de9d408`.
- Preserved source HEAD: `aa9fe9e6a5d2b636ea91ab18d2e01d6de2a9588f`.
- Preserved status SHA-256: `12e79926370c511fe887ca7053a36786662ee581ec0f498d9928d8e1997b07f9`.
- Preserved status entries: 48; untracked: 5; ignored: 0.
- AK evidence: `#4749`.

### G2 — restoration proof: pass

Disposable restoration matched the exact pre-Git file and metadata inventories, logical index, HEAD, and status. `git fsck` passed. AK evidence: `#4750`.

### G3 — bounded status rollout: pass

- Source commit: `71b1a6a699cb7c5b3e09aeeacf4d184f24bd0864`.
- Changed paths: `AGENTS.md`, `README.md`, and `docs/project/2026-07-18-fcos-proving-lane-retirement.md` only.
- Classification: 3 historical FCOS evidence + 8 template/ROCS migration + 3 misplaced/other-owner + 3 generated/disposable + 31 active dependency redirects + 0 secret/private quarantine = 48, with 0 unclassified.
- Native FCOS product authority remains `holdingco/fcos-control-board`.
- Current proving-lane state remains available at HEAD `71b1a6a`; its 46 remaining dirty status entries were not cleaned or accepted as active product work.
- Source task `#4036` completed with AK evidence `#4758`, `#4759`, and `#4760`.
- Softwareco routing projections did not claim `fcos-proving-lane` as an active product. Engineering-core scan/dashboard references are inventory/adoption projections, not product authority, and were left untouched.

### G4 — independent operator outcome: pass

Clean scout run: `scoutpeer-mrpxs64n-873ecae4`.

Tracked raw receipt: `docs/project/2026-07-18-factory-flow-pilot-cold-start-receipt.md`.

- start: `2026-07-18T05:39:06Z`;
- end: `2026-07-18T05:40:02Z`;
- elapsed: 56 seconds;
- wrong-owner claims: 0;
- unsafe mutation attempts: 0;
- command errors: 0;
- stale packet used as authority: no.

The operator correctly concluded:

1. native FCOS product owner: `holdingco/fcos-control-board`;
2. `fcos-proving-lane`: preserved historical/non-product evidence;
3. physical deletion: not authorized;
4. reactivation: a new accepted owner decision must supersede the retirement record, name a human owner, prove a unique unowned capability and bounded contract, and govern restoration/migration;
5. ambiguity or integrity risk: stop automation, capture read-only evidence, and escalate to the higher-level human operator.

Primary consulted owner evidence included the proving-lane `README.md`, `AGENTS.md`, retirement record, FCOS Control Board owner docs and native status, Decision 62, tasks `#3455`/`#4036`, and evidence `#4758`–`#4760`.

### G5 — closure: pass

- protocol conformance verdict: this report;
- effectiveness verdict: this report and evidence `#4771`;
- recovery result: G2 and evidence `#4750`;
- independent outcome: `docs/project/2026-07-18-factory-flow-pilot-cold-start-receipt.md` and evidence `#4769`;
- overhead and blocked-age observations: below and evidence `#4772`;
- mandatory KES learning: `docs/learnings/2026-07-18-factory-flow-pilot-001.md`, attached to Decision 62;
- human terminal decision: **`complete`**, explicitly confirmed by evidence `#4822` after resolving the timeout/preselection ambiguity in `#4781`;
- reconciliation: implementation wave archived; `SF1` retained as the required active terminal anchor with no active work; task `#4028` completed; bounded CTO-Agent pilot delegation expired.

## Time and flow observations

| Observation | Measured wall time |
|---|---:|
| coordination task creation to G4 completion | 43m 52s |
| lossless preservation task | 3m 37s |
| source retirement task creation to completion | 14m 53s |
| source retirement claimed execution | 4m 24s |
| dependency-blocked age of task `#4036` on task `#4035` | 3m 36s |
| post-unblock queue/claim delay for task `#4036` | 6m 53s |
| independent cold-start | 56s |

The 43m 52s interval includes governance readback, AK authoring, archive verification, classification, documentation, and operator-test setup; it is not a claim that all of that time is irreducible protocol overhead. No unresolved execution blocker remained at G4.

## Capacity and unresolved work

- Work was serialized as preservation → classification/status transition → independent outcome.
- Generic task `#3455` remains manually deferred because generic modernization conflicts with preserved historical status.
- The 31-path ROCS migration bundle remains preserved and redirected, not accepted as product work.
- No FCOS board item was needed: the pilot did not require an active multi-owner gate.
- Physical deletion, a second pilot, and template/L0 propagation remain outside Decision 62.

## Human terminal decision

The higher-level human operator selected **`complete pilot 001`**.

Terminal meaning:

- protocol conformance and effectiveness `improved` are accepted for this bounded pilot;
- `IW-SF1-PILOT-001` is archived; `SF1` is retained as AK's required active terminal anchor with `state_detail=terminal_anchor_no_active_wave`, not as active pilot work;
- coordination task `#4028` is completed with the attached evidence;
- the CTO-Agent pilot delegation is expired;
- task `#3455` remains explicitly deferred unless a later owner decision supersedes retirement;
- physical deletion, factory-wide claims, template propagation, and a second pilot remain unauthorized.
