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

`SF3 state_detail` is the authority-owned delegation readback:

- active: `delegated_active_decision_74;effective_at_utc=<RFC3339>;expires_at_utc=<RFC3339>`;
- revoked: `delegation_revoked_decision_74;revoked_at_utc=<RFC3339>;revoked_by=human-operator;governance_receipt_id=<id>`;
- superseded: `delegation_superseded_decision_74;superseding_decision_id=<id>;superseded_at_utc=<RFC3339>`;
- mandate terminal: `delegation_terminal_decision_74;terminal_action=<continue|stop|redirect|complete>;decided_at_utc=<RFC3339>;decision_evidence_id=<id>`.

Only the exact active form authorizes CTO control, and only before its expiry. Revocation, supersession, and terminal transitions require a claimed, scoped Softwareco task plus attributable human evidence; `ak direction update` then replaces the active detail atomically. Expiry is effective by time even before a cleanup update. On any disagreement among Decision 74, `SF3`, controller state, or projections, advisory-only behavior wins.

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

### Finite governance decision-right delta

For Decision 74's mandate only, the following rule temporarily specializes the current governance table:

| Concern | Accountable acceptance | Delegated CTO decision | Source-owner boundary |
|---|---|---|---|
| Portfolio ranking and technical sequence among accepted commitments | Softwareco Org Owner retains residual accountability; affected Product/Domain Owners accept the outcome and capacity envelope | CTO ranks investments and selects their technical ordering | No task or product lifecycle mutation follows from ranking alone |
| Portfolio-wave admission, pause, redirect, displacement, completion | Affected Product/Domain Owners accept outcome, capacity, displacement, and terminal evidence; `human-operator` acts when a required role is vacant or ambiguous | CTO chooses and operates the portfolio wrapper inside those accepted envelopes | Wrapper lifecycle never mutates an owner task |
| Exact repository task | Project Maintainer/source owner accepts scope; Service/Platform Owner also accepts when operations or a shared contract are affected | CTO may request, claim, and execute only as the task contract permits | AK/source-owner task lifecycle remains controlling |
| Cross-repo coordination | Affected Product/Domain Owners accept the cross-owner outcome; FCOS owner accepts any board mutation | CTO requests and stewards coordination | FCOS remains non-claimable and cannot approve owner work |

This delta does not transfer Product/Domain outcome accountability to the CTO. It delegates the technical sequencing choice **after** the relevant owners have accepted their outcome, capacity, and displacement envelopes. Silence is never acceptance.

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

### Acceptance records and objections

Role acceptance is recorded as an AK governance receipt, not free-form prose. The controller uses `ak governance record` with:

- `concern=softwareco-portfolio-wave:<wave_key>:<role>:acceptance`;
- `source_authority=<named accountable role/owner>`;
- `mito_layer=Design & Configuration`;
- `s3_domain_ref=<accepted domain or repo>`;
- `agreement_ref=decision:74`;
- `to_state=accepted`, `consent_mode=explicit`, `status=applied`;
- `task_id=<Softwareco coordinator task>`, `repo_scope=<affected scope>`, `actor=<named accountable actor>`;
- details schema `softwareco.portfolio-role-acceptance.v1` containing `role`, `wave_key`, `outcome_envelope`, `capacity_envelope`, `displacement_refs`, `owner_task_ref` where applicable, and `accepted_at_utc`.

Required receipts are Product/Domain outcome-priority-capacity acceptance, Project Maintainer/source-owner exact task acceptance, Service/Platform acceptance when duties change, and attributable `human-operator` fallback when a required role is vacant or disputed. Their receipt ids are referenced by the coordinator admission evidence; lifecycle state remains owner-native. Silence, an FCOS item, task creation alone, or model-written prose is not acceptance.

An affected owner may object before admission or request a stop afterward through a governance receipt with `to_state=objected`. Unresolved objections stop admission or further CTO control and route to `human-operator`; they never authorize the CTO to override the owner.

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

#### Canonical membership

- An admitted wave is an `SF3` child `work_wave` with `state=active` and `state_detail=portfolio_admitted_decision_74`.
- Each admitted wave has exactly one Softwareco coordinator task linked to that wave through `ak direction link-task`.
- Each owner task is admitted by an append-only AK evidence event on the coordinator task with `check_type=portfolio_task_admission`, `result=pass`, and details schema `softwareco.portfolio-task-admission.v1`.
- The details contain `event=admit|release`, `wave_key`, `owner_repo_scope`, `owner_task_id`, `role_acceptance_governance_receipt_ids`, `release_governance_receipt_id` when releasing, observed owner status, controller task id, controller claimant, controller lease expiry, and observed UTC time.
- The latest evidence id for each distinct `(owner_repo_scope, owner_task_id)` is controlling. One owner task may belong to only one admitted wave; duplicate refs count once and cross-wave sharing is prohibited.

#### Counting and release

- At most two admitted waves may be active.
- At most six distinct admitted owner tasks may be outstanding.
- An admitted owner task counts while its owner-native status is `pending`, `claimed`, `running`, or `blocked`.
- `done` or `failed` does not free capacity until the affected owner records an applied `softwareco-portfolio-task:<repo>:<id>:release` governance receipt with explicit consent and the controller records a `release` event referencing it.
- A nonterminal owner task may leave the portfolio only when its accountable owner records the same release receipt with `to_state=returned_to_owner`, explicitly accepting that the task continues or is disposed under owner law. Displacement or portfolio pause alone never frees capacity.
- Release uses the same revalidate → owner receipt → fresh read → append event → post-read/recount protocol as admission; ambiguous or stale release fails closed.
- Softwareco controller/coordinator tasks and FCOS-owner coordination tasks are excluded from the six owner-task limit but must be reported as coordination overhead.
- Unrelated owner work is never counted or displaced unless its accountable owner explicitly admits it.
- The second concurrent portfolio wave requires an explicit `human-operator` checkpoint during the first canary, even though two is the authorized ceiling.

#### Single controller and admission transaction

AK does not expose an atomic cross-repository portfolio-admission primitive. The first mandate therefore uses one Softwareco controller task linked to `SF3` and forbidden from source mutation. Before claim, `human-operator` explicitly confirms a controller designation and the session records an AK governance receipt with `concern=softwareco-portfolio-cto-controller-designation`, `source_authority=human-operator`, `agreement_ref=decision:74`, `to_state=delegated`, `consent_mode=explicit`, `task_id=<controller task>`, `actor=human-operator`, and details schema `softwareco.portfolio-controller-designation.v1` containing the unique claimant id, `lease_seconds` (maximum 14,400), designation time, and designation expiry.

The designated session atomically claims that task with the exact claimant and lease. A second claim fails. Every pre-operation read requires receipt/task/claimant equality and an unexpired designation and task lease. Handover requires admission stop, an attributable `human-operator` governance receipt with `to_state=handover_approved`, exact unclaim of the controller task, a new designation receipt, and a fresh atomic claim. After a crash or expiry, only `human-operator` may attest staleness and authorize exact unclaim/reclaim. A stale session, expired lease, ambiguous claimant, or conflicting readback is advisory only.

Every wave/controller/coordinator mutation requires its own claimed, scoped Softwareco AK task. Every admission is serialized as:

1. revalidate Decision 74, `SF3`, exact UTC expiry, controller claim/lease, and existing membership;
2. obtain every role-specific owner acceptance;
3. fresh-read the wave, coordinator, owner task, evidence, and FCOS refs;
4. write one admission event;
5. post-write read back and recount;
6. stop and escalate on ambiguity, drift, duplicate membership, or limit breach.

This is an atomic-claim plus serialized procedural invariant, not a global lock. If controller exclusivity cannot be demonstrated, every admission requires immediate `human-operator` approval or the canary narrows to read-only portfolio analysis.

### FCOS boundary

Use native FCOS Layer 5 only when a wave materially coordinates multiple source-owner repositories. FCOS current items are coordination-only and non-claimable; AK or the source-owner runtime remains authoritative for executable work and evidence.

Softwareco delegation does not authorize FCOS mutation. The CTO must hand off a proposed coordination item to `holdingco/fcos-control-board`. Real `fcos new` or `fcos close` requires an exact FCOS-owner AK task and the owner command's `--task <id> --json` contract. The resulting FCOS item must carry typed references to the Softwareco coordinator task and affected owner tasks/decisions; it must not copy their lifecycle state. FCOS close-evidence validation is not Product/Domain/Project acceptance. If the FCOS owner does not accept the handoff, the wave is blocked unless the affected owners genuinely redesign and reaccept it as single-owner; relabeling alone is prohibited.

## Pi workbench design

### Immutable Pi Modes dependency

Decision 74 pins exactly `@tryinget/pi-modes` release `0.3.0`, tag `pi-modes-v0.3.0`, owner commit `173b508b0bea27550f061e252e1d86a0638d2d71`. Changing this dependency requires a reviewed Decision 74 revision or superseding decision. The immutable release contains schema-v2 modes, named presets, `/mode use`, JSON status/preview, ancestor mode/preset discovery, linter, and release checks. A mutable local checkout is feasibility evidence only and cannot satisfy the activation gate.

Validation must extract or install the exact release, run its `mode:lint` and package release gate, then perform a fresh Pi load and live command proof. Softwareco must not fork or locally reimplement Pi Modes to bypass this dependency.

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

The template must declare `argument-hint: "<objective>"`, interpolate `$ARGUMENTS`, stop as advisory when the objective is absent, and echo the normalized objective plus a compact preflight table.

Normative invocation begins from the trusted Softwareco root. Pi Modes may inherit the ancestor mode/preset into owned descendants, but Pi prompt-template ancestor discovery is not assumed; descendant `/cto` support may be claimed only after live proof.

Before representing the session as an active CTO delegate, and again before every wave, controller, coordinator, owner-task, admission-evidence, or FCOS mutation, the prompt requires:

1. require Decision 74 `outcome=accepted` and read its acceptance timestamp;
2. require `SF3 state=active` and an exact state detail containing `delegated_active_decision_74`, `effective_at_utc`, and `expires_at_utc`;
3. require current UTC before expiry and no revocation, supersession, or mandate terminal decision;
4. fail closed on any mismatch with the charter/governance projections, which remain consistency views only;
5. require a currently claimed, unexpired Softwareco controller task and identify the unique claimant;
6. inspect admitted waves, coordinator tasks, latest admission/release evidence, owner-native task states, role acceptances, and FCOS refs;
7. identify the exact objective, jurisdiction, owner surfaces, and reserved decisions;
8. remain advisory and emit every failed or ambiguous condition.

The accepted AK decision and `SF3` state own activation/expiry readback; the charter does not. This remains a behavioral preflight, not a security boundary. Mutation authority still requires exact AK/source-owner/FCOS task contracts.

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

Revocation or expiry in AK remains controlling even if the mode stays selected. It stops CTO admission and control, records owner handoffs, and returns every outstanding owner task to its owner; it never auto-closes, pauses, redirects, releases, or fails those tasks.

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

- extract or install exact Pi Modes `0.3.0` / `173b508b0bea27550f061e252e1d86a0638d2d71`, run its `mode:lint` and release gate, and record the package/version/commit evidence;
- validate selective `.pi` tracking and ignored local state boundaries;
- verify mode strategy is `append` and preset uses native base;
- verify `/cto` contains every preflight and stop condition;
- verify the post-decision charter, governance, and operating-model projections name the accepted decision ID, exact UTC expiry, finite decision-right change, consultation duties, revocation path, WIP/admission limitation, and human-reserved powers without enlarging AK authority;
- run Softwareco strict docs validation and `git diff --check`;
- inspect `/mode-preview --json`, `/mode use softwareco-cto`, `/mode-status --json`, and `/cto` discovery/invocation in a trusted Softwareco-root session;
- treat trusted Softwareco-root invocation as normative; separately verify ancestor mode/preset discovery from an owned-repo cwd, but do not claim descendant `/cto` discovery without proof;
- independently review authority, WIP, owner boundaries, and operator usability.

The mode must not be described as live merely because JSON lint passes. Live invocation requires an observed Pi command after reload/fresh startup.

## Rollout

1. Commit the exact RFC revision for immutable review.
2. Complete strict review attempts and a controlling synthesis with explicit outcome.
3. If the outcome is `ready_for_adr`, record the human's accepted AK decision and its ADR projection.
4. Record post-ADR implementation and validation/rollout/rollback artifacts.
5. Update `docs/org/cto-agent-charter.md`, `docs/org/governance.md`, and `docs/org/operating_model.md` as post-decision projections with the accepted decision ID, exact UTC expiry, finite decision-right change, consultation obligations, revocation path, WIP/admission limitation, and human-reserved powers. Until that lands, the current Decision 68 projection remains expired and no new delegation is active.
6. Validate and install the immutable Pi Modes owner release, then land the tracked mode, preset, prompt, operator guidance, and deterministic checks.
7. Create the scoped Softwareco controller task, have `human-operator` designate the first controller, and record the exact task/claim protocol.
8. Activate the accepted delegation only after steps 3–7 validate by setting `SF3 state_detail` to `delegated_active_decision_74;effective_at_utc=<RFC3339>;expires_at_utc=<RFC3339>`, where effective time is the AK acceptance time and expiry is exactly 30 days later.
9. Run one read-only CTO portfolio-thesis canary.
10. Admit the first wave and no more than six owner tasks through role-specific acceptance; require an explicit `human-operator` checkpoint before a second concurrent wave; request FCOS owner coordination only for genuine cross-repo work.
11. Execute one selected outcome wave through source-owner tasks.
12. Record outcome evidence and obtain the human mandate terminal decision.

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

The revised RFC is ready for re-review, not presumptively ADR-ready. No architecture-shaping question is intentionally deferred. The first portfolio investment remains unknown by design because evidence-backed selection inside accepted owner envelopes is the delegated capability being tested. Descendant `/cto` discovery is a non-blocking post-ADR usability question; trusted Softwareco-root invocation is the accepted baseline.
