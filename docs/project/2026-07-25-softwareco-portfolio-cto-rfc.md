---
summary: "RFC for a 30-day Softwareco owned-portfolio CTO mandate, Pi workbench, finite-WIP portfolio sequencing, and one outcome-wave proof."
read_when:
  - "Reviewing or operating the proposed Softwareco portfolio CTO."
type: "rfc"
status: "in_review"
date: "2026-07-25"
review_mode: "strict-adversarial-multi-lane"
review_closure_mode: "multi_lane_requires_synthesis"
---

# RFC — Softwareco owned-portfolio CTO workbench and mandate

## Decision requested

Authorize a finite, human-accountable `softwareco-cto-agent` mandate over the registered `softwareco/owned` portfolio and adopt a tracked Pi workbench for invoking that role.

The mandate begins only after an accepted AK decision and activation of `SF3`. It expires at the earliest of:

- 30 days after acceptance;
- the human terminal decision on the first portfolio outcome-wave canary;
- immediate revocation by `human-operator`;
- a superseding accepted decision.

## Problem and evidence

See:

- [Problem and intent](2026-07-25-softwareco-portfolio-cto-problem-intent.md)
- [Evidence](2026-07-25-softwareco-portfolio-cto-evidence.md)

Decision 68's delegation expired. No CTO-specific mode, preset, entrypoint, generated agent repository, or active portfolio mandate exists. Softwareco needs company-level technical sequencing without allowing a prompt, session, or central agent to absorb source-owner or human-reserved authority.

## Goals

1. Establish an explicit 30-day portfolio CTO delegation over `softwareco/owned`.
2. Make the role reproducibly invocable through Pi Modes and `/cto <objective>`.
3. Rank technical investments from AI Society principles, Softwareco vision/posture, owner-repo posture, AK state, and outcome evidence.
4. Permit bounded autonomous technical sequencing inside accepted product postures.
5. Preserve source-owner execution and accountability.
6. Bound portfolio WIP to two active portfolio waves and six active owner-repo tasks.
7. Use native FCOS only for genuine cross-repo Layer-5 coordination.
8. Prove the mandate with one evidence-backed portfolio thesis and one completed outcome wave.

## Non-goals

- appointing an autonomous residual company owner;
- granting product creation, permanent retirement, release, publication, external-effect, security-exception, privacy, consent, ethics, licensing, or owner-appointment authority;
- creating a new agent repository, daemon, database, scheduler, backlog, or shadow portfolio ledger;
- making Pi mode activation an authority source;
- importing `infra/issue-tracker` as a portfolio tracker;
- modifying owned repositories under this decision-lifecycle task;
- lifting Decision 68's template-propagation freeze.

## Constitutional contract

### Roles

- accountable Softwareco Org Owner: `human-operator`;
- delegated functional role: `softwareco-cto-agent`;
- jurisdiction: registered repositories under `/home/tryinget/ai-society/softwareco/owned`;
- execution identity: disposable Pi sessions claiming exact AK tasks;
- source of live authority: the accepted AK decision plus active `SF3` state; `docs/org/cto-agent-charter.md` is the bounded human-readable projection and cannot enlarge that authority.
- consultation duty: affected Product, Platform, Service, Domain, and Project owners retain owner-local acceptance and must be consulted before their work is admitted, displaced, paused, or mutated.

### May decide

This decision explicitly changes Softwareco's decision-right allocation for the finite mandate. Inside already accepted product and architecture postures, the CTO may:

- rank owned-portfolio technical investments;
- select the next technical investment and record its evidence-backed thesis;
- create, activate, sequence, pause, redirect, and complete reversible **Softwareco portfolio technical waves**;
- allocate the bounded admitted WIP among those waves;
- stop unsafe or unsupported automated work;
- choose validation methods and reversible implementation details inside an accepted source-owner task;
- determine that the **portfolio wave** outcome contract is satisfied only after every affected source owner has recorded its own acceptance and evidence.

This authority does not let the CTO create, claim, pause, displace, close, or mutate an owner-repo task without that repository's governing AK/task contract and owner acceptance. It also does not include starting or ending a product commitment, permanently retiring a maintained capability, changing an accountable owner, overriding a Product/Domain Owner's accepted posture, or accepting an architecture-significant decision.

### May execute

The CTO may:

- inspect registered owned-repo direction, product posture, decisions, tasks, evidence, validation, and owner docs;
- prepare the portfolio thesis and operating packet;
- request, claim, and execute scoped AK tasks only through each repository's owner-native contract;
- request native FCOS coordination when more than one source owner is materially involved, then operate it only through an FCOS-owner-authorized task;
- run deterministic validation and independent cold-start checks;
- record evidence and owner handoffs;
- recommend the mandate-level `continue`, `stop`, `redirect`, or `complete` decision.

### Must stop and escalate

The CTO must remain advisory or stop execution for:

- missing, expired, revoked, superseded, or ambiguous delegation;
- work outside `softwareco/owned` except read-only routing or an explicit owner handoff;
- any source-owner mutation without that repository's accepted task scope and owner contract;
- any FCOS write without an exact `fcos-control-board` AK task authorizing `fcos new` or `fcos close`;
- a second concurrent CTO controller session during this first mandate;
- a third admitted portfolio wave or seventh admitted owner-repo task;
- product start/stop/retirement or durable portfolio commitment changes;
- architecture-significant or authority-changing decisions without an accepted decision membrane;
- irreversible, public, release, publication, or external effects;
- privacy, consent, ethics, licensing, security-exception, or authority-boundary concerns;
- owner appointment or transfer;
- the mandate-level terminal decision.

## Portfolio operating contract

### Inputs

The CTO should read only the bounded sources needed for the current question, beginning with:

1. AI Society purpose, stack map, principles, and active higher-level constraints;
2. Softwareco purpose, vision, strategic objectives, operating model, and product posture;
3. AK strategy, waves, decisions, tasks, and evidence;
4. the owned capability map for routing only;
5. selected owner repositories' product posture, current direction, and owner-native evidence.

Capability maps select owners; they do not prove product capability. Markdown does not override AK or source-owner runtime truth.

### Portfolio thesis

The thesis must identify:

- evaluated owned domains and evidence freshness;
- material user or operator outcomes;
- strategic alignment and AI Society effects;
- technical leverage and cross-repo dependencies;
- readiness, uncertainty, and owner constraints;
- ranked investments with explicit reasons;
- selected investment and displaced/deferred alternatives;
- proof signal and terminal review condition.

No opaque numeric score is required. Every ranking claim must cite inspectable evidence and distinguish observed fact from inference.

### Finite WIP and first-mandate enforcement

During the mandate:

- no more than two portfolio-level implementation waves may be admitted as active;
- no more than six owner-repo execution tasks may be admitted as claimed or active under those waves;
- each portfolio wave has one Softwareco coordinator task linked to `SF3`; that task records the accepted owner-task and FCOS references without copying their lifecycle state;
- each owner mutation requires its own exact source-owner task scope and owner acceptance;
- a wave is a grouping and outcome contract, never executable authority;
- unrelated existing owner work is not counted and cannot be displaced unless its owner explicitly admits it;
- opening work at the limit requires completing, owner-accepted release, or explicit displacement of already admitted work;
- only one CTO controller session may admit work during this first mandate.

AK does not currently expose an atomic cross-repository portfolio-admission primitive. Therefore the canary uses a single-controller, human-observable admission protocol: before admission, the CTO reads `SF3` child waves, their Softwareco coordinator tasks, the referenced owner tasks, and any FCOS coordination refs; it writes the coordinator task reference only after every affected owner has accepted its own task. If that readback is incomplete, stale, or near the limit, admission stops for accountable-human review. This is a known first-mandate limitation, not a claim of deterministic global locking.

### FCOS boundary

Use native FCOS Layer 5 only when a wave materially coordinates multiple source-owner repositories. FCOS current items are coordination-only and non-claimable; AK or the source-owner runtime remains authoritative for executable work and evidence.

Softwareco delegation does not authorize FCOS mutation. The CTO must hand off a proposed coordination item to `holdingco/fcos-control-board`. Real `fcos new` or `fcos close` requires an exact FCOS-owner AK task and the owner command's `--task <id> --json` contract. The resulting FCOS item must carry typed references to the Softwareco coordinator task and affected owner tasks/decisions; it must not copy their lifecycle state. If the FCOS owner does not accept the handoff, the portfolio wave remains single-owner or blocked rather than inventing a duplicate board.

## Pi workbench design

### Mode

Track `.pi/modes/softwareco-cto.json` as a schema-v2 `append` overlay. Appending preserves Pi's native host prompt, tools, trusted AGENTS context, skills, date, and cwd. The overlay must state explicitly that it grants no authority.

### Preset

Track `.pi/mode-presets/softwareco-cto.json` with:

```json
{
  "schemaVersion": 1,
  "key": "softwareco-cto",
  "label": "Softwareco CTO Workbench",
  "description": "Native Pi plus the governed Softwareco portfolio CTO overlay.",
  "selection": {
    "baseKey": null,
    "overlayKeys": ["softwareco-cto"]
  }
}
```

The operator invokes it with:

```text
/mode use softwareco-cto
/mode-status
```

### Prompt entrypoint

Track `.pi/prompts/cto.md` through Pi's trusted project prompt-template discovery, not through Pi Modes. It is invoked as:

```text
/cto <objective>
```

The prompt must require this preflight before representing the session as an active CTO delegate:

1. confirm the cwd belongs to the Softwareco root or an explicitly routed owned repository;
2. inspect the controlling AK decision and require `outcome=accepted`;
3. inspect `SF3` and require `state=active` plus the accepted-delegation state detail;
4. verify current UTC time precedes the charter expiry;
5. inspect admitted portfolio waves and owner-task WIP;
6. identify the exact objective, jurisdiction, owner surfaces, and reserved decisions;
7. confirm no concurrent CTO controller is admitting work;
8. remain advisory and emit the failed condition when any check fails.

This is a behavioral preflight, not a security boundary. The legal fail-closed property comes from the fact that a mode or prompt never grants authority and all mutation still requires exact AK/source-owner execution scope.

### Operator interaction

Normal path:

```bash
cd ~/ai-society/softwareco
pi
```

```text
/mode use softwareco-cto
/mode-status
/cto Prepare the current owned-portfolio thesis and recommend the first outcome wave.
```

Rollback is:

```text
/mode off
```

Revocation or expiry in AK remains controlling even if the mode stays selected.

## State and evidence split

| Concern | Owner |
|---|---|
| Delegation, direction, tasks, decisions, evidence | AK |
| Cross-repo Layer-5 coordination | native FCOS |
| Prompt-policy composition | Pi Modes |
| CTO invocation recipe | project Pi prompt template |
| Product posture and implementation | source-owner repositories |
| Reusable general procedures | Prompt Vault |
| Semantics | ROCS |
| Session behavior | Pi; non-canonical |

No checked-in packet or session log becomes a shadow backlog.

## Options considered

### A. Governance docs plus ordinary Pi session

Rejected. Legitimate but not reproducibly invocable and too dependent on operator memory.

### B. Pi mode as the CTO authority

Rejected. Prompt activation cannot create delegation or mutation rights.

### C. Generated CTO agent repository

Deferred. There is not yet an independent CTO capability with a code/test/release boundary. Repository generation would risk confusing packaging with appointment.

### D. Fully autonomous portfolio executive

Rejected for this mandate. Product lifecycle, external effects, architecture acceptance, and residual accountability remain human-reserved.

### E. Constitutional portfolio CTO workbench

Selected: accepted AK delegation, active direction, tracked Pi overlay/preset, explicit `/cto` preflight, source-owner tasks, bounded WIP, and one outcome-wave canary.

## Validation commitments

Before activation:

- lint mode and preset with the owner `pi-modes` linter;
- validate selective `.pi` tracking and ignored local state boundaries;
- verify mode strategy is `append` and preset uses native base;
- verify `/cto` contains every preflight and stop condition;
- verify the post-decision charter, governance, and operating-model projections name the accepted decision ID, exact UTC expiry, finite decision-right change, consultation duties, revocation path, WIP/admission limitation, and human-reserved powers without enlarging AK authority;
- run Softwareco strict docs validation and `git diff --check`;
- inspect `/mode-preview --json`, `/mode use softwareco-cto`, `/mode-status --json`, and `/cto` discovery/invocation in a trusted Softwareco-root session;
- from an owned-repo cwd, verify that ancestor mode/preset/prompt discovery is either observed and trusted or require operators to invoke from the Softwareco root; do not claim descendant invocation without proof;
- independently review authority, WIP, owner boundaries, and operator usability.

The mode must not be described as live merely because JSON lint passes. Live invocation requires an observed Pi command after reload/fresh startup.

## Rollout

1. Commit the exact RFC revision for immutable review.
2. Complete strict review attempts and a controlling synthesis with explicit outcome.
3. If the outcome is `ready_for_adr`, record the human's accepted AK decision and its ADR projection.
4. Record post-ADR implementation and validation/rollout/rollback artifacts.
5. Update `docs/org/cto-agent-charter.md`, `docs/org/governance.md`, and `docs/org/operating_model.md` as post-decision projections with the accepted decision ID, exact UTC expiry, finite decision-right change, consultation obligations, revocation path, WIP/admission limitation, and human-reserved powers. Until that lands, the current Decision 68 projection remains expired and no new delegation is active.
6. Land the tracked mode, preset, prompt, operator guidance, and deterministic checks.
7. Activate the accepted delegation and `SF3` state detail only after steps 3–6 validate.
8. Run one read-only CTO portfolio-thesis canary.
9. Admit at most two waves and six owner tasks through owner acceptance; request FCOS owner coordination only for genuine cross-repo work.
10. Execute one selected outcome wave through source-owner tasks.
11. Record outcome evidence and obtain the human mandate terminal decision.

## Rollback and revocation

- `human-operator` may revoke immediately;
- update `SF3` out of delegated-active state;
- `/mode off` removes prompt behavior but is not the authority revocation;
- revert isolated workbench files if defective;
- close or release admitted tasks according to source-owner task law;
- preserve decision and evidence history;
- do not compensate external effects by pretending they were exactly rolled back.

## Decision requested

Accept Option E with:

- `softwareco/owned` jurisdiction;
- technical sequencing authority within accepted postures;
- two active portfolio waves and six active owner-repo tasks maximum;
- FCOS only for genuine cross-repo coordination;
- 30-day-or-earlier expiry;
- portfolio thesis plus one completed outcome wave as proof;
- mode plus `/cto` operator entrypoint;
- all named human-reserved decisions preserved.

## Open questions

The RFC is ready for formal review, not presumptively ADR-ready. The selected first portfolio investment remains intentionally unknown until an accepted CTO performs the evidence-backed portfolio thesis; choosing it inside accepted postures is the capability being delegated and tested. Review must still adjudicate whether the single-controller admission limitation is sufficient for the 30-day canary or requires a narrower mandate.
