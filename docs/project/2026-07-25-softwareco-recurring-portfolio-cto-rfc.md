---
summary: "Revised RFC for a Softwareco portfolio CTO framework whose authority exists only inside bounded human-authorized epochs."
read_when:
  - "Reviewing or implementing Decision 77, the recurring successor to terminal Decision 74."
type: "rfc"
status: "in_review"
date: "2026-07-25"
decision_id: 77
predecessor_decision_id: 74
governance_task_id: 4205
revision: 4
supersedes_reviewed_commit: "814ffa58beed385ba2e4fbe9fa76a404240b09a2"
review_mode: "strict-adversarial-multi-lane"
review_closure_mode: "multi_lane_requires_synthesis"
---

# RFC — recurring Softwareco portfolio CTO operating framework

## Decision requested

Accept Decision 77 as a **durable constitutional framework**, not an indefinitely appointed office. Actual `softwareco-cto-agent` delegation exists only inside one affirmative, finite, direct-human-authorized operating epoch.

Between epochs the framework is dormant and `/cto` is advisory-only. Objective, proof, task, and wave completion neither create nor terminate the framework. A missed framework review prevents new epochs.

See:

- [Problem and intent](2026-07-25-softwareco-recurring-portfolio-cto-problem-intent.md)
- [Evidence](2026-07-25-softwareco-recurring-portfolio-cto-evidence.md)
- [Review attempt 1 synthesis](../reviews/2026-07-25-softwareco-recurring-portfolio-cto-review-synthesis.md)

## Review-attempt-1 corrections

This revision:

1. replaces the indefinite standing delegation with a dormant framework plus finite epochs;
2. makes epoch, review, handback, terminal, revocation, and supersession state machines exact;
3. adds a Decision-77-specific child direction projection while preserving `SF3` Decision 74 terminal detail;
4. restores exact owner acceptance, objection, terminal, return, and release law;
5. makes every human reservation an operative stop condition;
6. defines deterministic epoch, thesis, wave/WIP, and objective-proof reconstruction;
7. separates read-only fresh workers from controller evidence mutation;
8. defines a checker state matrix and negative controls.

## Lifecycle separation

| Fact | Canonical effect |
|---|---|
| Objective completed | closes only its exact AK task/proof record |
| Owner task completed | changes only owner-native task lifecycle |
| Portfolio wave completed | closes only that wrapper after owner terminal evidence |
| Recurrence proof met | records maturity evidence; does not terminate framework or epoch |
| Epoch expires/hands back | ends only that epoch and current delegation |
| Framework review expires | blocks new epochs; never extends an existing epoch |
| Framework terminal/revoked/superseded | permanently blocks further epochs under Decision 77 |

No checker, task result, evidence record, or wrapper transition may promote one row into another.

## Decision 74 preservation

Decision 77 does not reopen, reverse, amend, continue, or erase Decision 74 or human receipt `8870`.

- Decision 74 remains accepted historical law for its finite canary.
- Receipt `8870` remains its terminal event.
- Controller task `4182` remains closed.
- The DesignMD wave and evidence remain attributed to Decision 74.
- `SF3 state=active` remains structural; its exact Decision 74 terminal detail remains unchanged and grants no authority.
- Every Decision 77 epoch, receipt, controller, thesis, wave event, and objective proof carries `decision_id=77`.

## Goals

1. Reconstruct exact current authority and portfolio state in a fresh process without session memory.
2. Maintain freshness-bounded proposal-only thesis revisions as AK evidence, not a backlog.
3. Execute successive owner-native waves without absorbing owner authority.
4. Keep WIP finite and membership mutations serialized.
5. Permit ordinary recurrence through fresh finite epochs rather than architecture decisions for each wave.
6. Prove one additional independent outcome and post-outcome re-entry.
7. Remain advisory on any missing, expired, conflicting, malformed, or ambiguous authority/state fact.

## Non-goals

- no permanent or continuously appointed autonomous executive;
- no generated CTO agent repository in this decision;
- no shadow database, backlog, scheduler, current-pointer file, or global lock;
- no owner-task lifecycle mutation by portfolio wrappers;
- no product lifecycle, durable portfolio commitment, architecture acceptance, owner appointment, exception, release, publication, public, irreversible, or external-effect authority;
- no arbitrary “latest accepted decision” discovery;
- no reinterpretation of Decision 74 as active;
- no change to Decision 68's template-propagation freeze.

# Authority model

## Dormant Decision 77 framework

Acceptance establishes only the framework and the right for `human-operator` to authorize finite epochs under its exact contract. It does not appoint an active CTO between epochs.

Framework validity requires:

- Decision 77 remains accepted and unblocked;
- no applied Decision 77 revocation, terminal, or supersession event;
- the current framework-review window is valid;
- the Decision-77 direction projection is unambiguous;
- Decision 74 terminal negative control still passes.

Framework validity alone grants no mutation or portfolio selection authority. Read-only sensing may report proposals, but selection/admission/execution requires an active epoch and owner gates.

## Framework review window

Initial framework review validity ends exactly 30 days after the Decision 77 acceptance receipt timestamp. Every later review is direct-human-originated under fixed concern:

```text
softwareco-portfolio-cto:decision77:framework-review
```

Required governance envelope:

- `source_authority=human-operator`;
- `actor=human-operator`;
- `agreement_ref=decision:77`;
- `repo_scope=/home/tryinget/ai-society/softwareco`;
- `consent_mode=explicit`;
- `status=applied`;
- mandatory `evidence_ref`;
- `from_state=review_due|framework_valid`;
- `to_state=framework_valid|framework_paused`.

Details schema:

```json
{
  "schema": "softwareco.portfolio-cto-framework-review.v1",
  "decision_id": 77,
  "reviewed_at_utc": "<RFC3339>",
  "valid_until_utc": "<RFC3339, <= reviewed + 30 days>",
  "outcome": "continue_framework|pause_framework",
  "prior_review_receipt_id": "<id|null>",
  "evidence_refs": []
}
```

The exact concern is read with limit `100`. Applied review receipts must form one non-forking predecessor chain. Zero valid heads after the initial window, multiple heads, gaps, malformed timestamps, `framework_paused`, or expiry blocks new epochs. Epoch expiry may not exceed review `valid_until_utc`; an existing epoch is never extended by review.

## Decision-77 direction projection

After acceptance, implementation creates exactly one AK-native child of `SF3`:

```text
key: IW-SF3-CTO77-RECURRING
kind: work_wave
parent: SF3
state before implementation readiness: pending
state while the framework is nonterminal: active
state after framework terminal/revoked/superseded: done
state_detail: decision77_recurring_framework;phase=<phase>;objective_task_id=<id>;thesis_task_ids=<none|sorted-csv>;thesis_head_evidence_id=<none|id>
```

`work_wave` is the legal AK-native authoring kind; `implementation_wave` may appear only as a derived vocabulary label. Decision 77 links to this exact node with `governs`; execution tasks link using legal roles. This node is rollout, lineage, and the structured thesis-head projection—not authority. The controller updates its thesis-head field only after evidence recording, with fresh pre-read, one update, post-read, and manual reconciliation on disagreement; no compare-and-swap is claimed. It never replaces or rewrites `SF3`'s Decision 74 terminal detail. Missing, duplicate, wrong-parent, wrong-decision, or conflicting projection fails closed. Objective completion leaves this node active and changes only `objective_task_id`/phase; framework/epoch authority still derives only from Decision 77 receipts and controller state. Only framework terminal/revoked/superseded reconciliation marks it done.

## Fixed current-epoch chain

All epoch authorization and handback transitions use one exact concern:

```text
softwareco-portfolio-cto:decision77:epoch-index
```

The checker queries this concern with limit `100`. Every applied receipt contains `prior_epoch_receipt_id`. The set must form one linear, non-forking chain with exactly one unreferenced head. Zero receipts means no epoch. Gaps, duplicate predecessor references, cycles, multiple heads, more than 100 applicable receipts, or malformed transitions fail closed.

Valid transitions:

```text
inactive -> epoch:<epoch_id>       # direct human authorization
epoch:<epoch_id> -> inactive       # exact claimant handback or direct human stop
epoch:<epoch_id> -> revoked        # direct human revocation
inactive|epoch:<id> -> terminal    # direct human terminal
```

A new authorization is legal only from `inactive`. Overlapping epochs are prohibited.

## Epoch authorization

An authorization receipt must have:

- exact epoch-index concern above;
- `source_authority=human-operator` and `actor=human-operator`;
- `agreement_ref=decision:77`;
- exact Softwareco repo scope;
- explicit consent, applied status, and mandatory evidence;
- `from_state=inactive`, `to_state=epoch:<epoch_id>`;
- exact controller task ID and claimant.

Details schema:

```json
{
  "schema": "softwareco.portfolio-cto-epoch-authorization.v1",
  "decision_id": 77,
  "epoch_id": "<unique>",
  "controller_task_id": "<new task>",
  "claimant_id": "<exact claimant>",
  "authorized_at_utc": "<RFC3339>",
  "authorization_expires_at_utc": "<RFC3339>",
  "lease_seconds": "1..14400",
  "jurisdiction": "softwareco/owned",
  "prior_epoch_receipt_id": "<head id|null>",
  "framework_review_receipt_id": "<id|null for initial window>",
  "evidence_refs": []
}
```

The authorization interval is a hard, non-renewable maximum of 14,400 seconds and must end no later than the current framework review window. Operation begins only when the exact claimant atomically claims the exact source-mutation-forbidden controller task after authorization and before expiry. Controller claim expiry must be no later than authorization expiry.

Claim extension cannot extend epoch authority. Claimant replacement, handover, or stale recovery requires epoch handback/expiry, a new controller task, a new epoch ID, and new direct human authorization. No in-epoch claimant transfer exists.

## Epoch handback

The exact claimant may end its epoch early with an applied epoch-index receipt:

- `source_authority=decision77-epoch-controller`;
- `actor=<exact claimant>`;
- `agreement_ref=decision:77`;
- `from_state=epoch:<id>`, `to_state=inactive`;
- mandatory evidence;
- details schema `softwareco.portfolio-cto-epoch-handback.v1` with decision, epoch, controller task, prior head, time, WIP handoff refs, and `external_effects`.

`human-operator` may record the same transition with human source/actor. Expiry ends authority by time even without handback; a later human reconciliation receipt may move the chain to `inactive` but never retroactively extends authority.

## Framework revocation, terminal, and supersession

Direct-human fixed concerns:

```text
softwareco-portfolio-cto:decision77:revocation
softwareco-portfolio-cto:decision77:terminal
softwareco-portfolio-cto:decision77:supersession
```

Every applied event requires human source/actor, decision agreement, exact repo scope, explicit consent, mandatory evidence, event time, Decision 77, reason, current epoch/head ref, and prior event ref where applicable.

- Revocation: any nonterminal posture (`framework_valid|framework_paused|review_expired|inactive|epoch:<id>|reconciliation_pending`) -> `revoked`, schema `softwareco.portfolio-cto-framework-revocation.v1`.
- Terminal: any nonterminal posture -> `terminal`, schema `softwareco.portfolio-cto-framework-terminal.v1`, action `complete|stop|redirect` only.
- Supersession: any nonterminal posture -> `superseded`, schema `softwareco.portfolio-cto-framework-supersession.v1`.

The fixed supersession receipt is the mandatory machine-readable Decision-77 supersession relation. Its details name `superseding_decision_id`, and the checker must fresh-read that exact AK decision as accepted/unblocked and verify its RFC/ADR explicitly says it supersedes Decision 77. A later decision cannot lawfully claim Decision-77 supersession without this receipt. The receipt is therefore an operative runtime projection backed by the accepted successor decision, not optional provenance.

Any applied revocation, terminal, or valid supersession event ends every epoch immediately before direction/projection reconciliation. Conflicts, malformed events, or multiple unchained heads fail closed. There is no terminal `continue`; ordinary recurrence uses a new epoch.

# Human-reserved stop conditions

The CTO must stop and escalate for:

- product creation, permanent stop/retirement, or durable product/portfolio commitment;
- Product/Domain posture, capacity, displacement, or accountability conflict;
- architecture-significant acceptance;
- owner appointment, transfer, or vacancy resolution beyond identity clarification;
- privacy, consent, ethics, licensing, security, or legal exception;
- irreversible, public, release, publication, or external effect;
- framework-level pause, redirect, stop, complete, review, revocation, or supersession;
- any cumulative sequence of ordinary waves that would produce one of these effects.

Repeated waves cannot bootstrap a reserved decision. `human-operator` remains residual accountable owner.

# Owner federalism

## Exact owner receipt families

Every receipt is applied, explicit, owner-originated, bound to Decision 77 and exact `wave_key`, accountable role/owner, scope ID, owner-native evidence, and Softwareco/source-owner repo scope as applicable.

```text
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:envelope-acceptance
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:objection
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:objection-resolution
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:task-scope-acceptance
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:terminal-acceptance
softwareco-portfolio-wave:<wave_key>:<role>:<owner_id>:<scope_id>:release
```

Every payload includes `schema`, `decision_id=77`, `wave_key`, `role`, `owner_id`, `scope_id`, `epoch_id`, `prior_receipt_id`, `owner_evidence_refs`, and `observed_at_utc`. Exact transitions and additional required fields are:

| Concern suffix / schema | Transition | Additional required fields |
|---|---|---|
| `envelope-acceptance` / `softwareco.portfolio-owner-envelope-acceptance.v2` | `proposed -> envelope_accepted` | `outcome_envelope`, `capacity_envelope`, `displacement`, `success_criteria`, `stop_criteria` |
| `task-scope-acceptance` / `softwareco.portfolio-owner-task-scope-acceptance.v2` | `proposed -> task_scope_accepted` | exact `owner_repo`, `owner_task_ids`, task titles, allowed/required/forbidden scope, validation contract |
| `objection` / `softwareco.portfolio-owner-objection.v2` | `clear -> objected` | `objection_kind`, `risk`, `affected_scope`, `requested_resolution`, referenced acceptance receipt IDs |
| `objection-resolution` / `softwareco.portfolio-owner-objection-resolution.v2` | `objected -> resolved|withdrawn` | `objection_receipt_id`, `resolution`, `resolution_evidence_refs`, and accepted human-reserved decision ref when the accountable owner did not resolve it |
| `terminal-acceptance` / `softwareco.portfolio-terminal-acceptance.v2` | `admitted -> terminal_accepted` | `owner_task_ids`, implementation/outcome/operational evidence refs, residual risk |
| `release` / `softwareco.portfolio-owner-release.v2` | `admitted -> released_terminal|returned_to_owner` | `owner_task_ids`, terminal or continuing-lifecycle disposition, release evidence refs |

Receipt envelope source/actor must equal the accountable owner identity recorded for the exact role/scope. Objection resolution/withdrawal must come from that same owner; only a separately accepted human-reserved decision cited in the payload may resolve a substantive owner conflict. Predecessor IDs form a non-forking chain per exact concern; duplicates, multiple heads, incompatible transitions, or missing fields fail closed.

Product/Domain owners accept outcome, capacity, displacement, success, and stop criteria before selection. Project/source owners accept every exact owner-task scope before admission. Service/Platform owners accept applicable operational/shared-contract consequences. Every applicable owner accepts terminal evidence.

A substantive applied objection immediately blocks selection/admission/further CTO control for that scope, including after admission. Control resumes only after one valid resolution/withdrawal transition. Vacancy fallback applies only to genuine role vacancy or identity ambiguity and requires separate human evidence; it never overrides a substantive objection.

## Owner release law

Portfolio WIP is freed only after a direct owner-originated release receipt:

- terminal owner task: `to_state=released_terminal` with terminal task/evidence refs;
- nonterminal return: `to_state=returned_to_owner` with explicit owner acceptance of continuing/disposal lifecycle.

Controller observation of `task.status=done`, wave pause, displacement, or wrapper completion is never sufficient. Wrappers never mutate owner tasks.

# Durable recurrence state

## Fresh worker/controller split

Fresh Run A and Run C workers are trusted-root `pi --mode rpc --no-session` processes with read-only tools. They receive no previous transcript, generated thesis, or recommendation. They may produce a candidate thesis payload but perform no AK/source mutation.

The active epoch controller, acting under a separately claimed exact objective/thesis task, must:

1. receive the worker payload plus captured input/tool/output manifest;
2. independently fresh-read every cited AK/source-owner fact;
3. reject missing, stale, uncited, or inconsistent facts;
4. allocate the next thesis revision;
5. record AK evidence.

The worker and controller identities, commands, process start time, tool readbacks, stdout/stderr hashes, prompt/mode digest, repo commits, and absence of prior-session input are evidence fields.

## Normative thesis series

AK evidence uses:

- `check_type=portfolio_thesis_v2`;
- `result=pass`;
- Softwareco repo scope;
- exact active epoch controller's claimed thesis/objective task;
- details schema `softwareco.portfolio-thesis.v2`.

Required details:

```json
{
  "schema": "softwareco.portfolio-thesis.v2",
  "decision_id": 77,
  "epoch_id": "<id>",
  "revision": 1,
  "prior_thesis_evidence_id": null,
  "observed_at_utc": "<RFC3339>",
  "valid_until_utc": "<RFC3339, <= observed + 24h and <= epoch expiry>",
  "census_basis": [],
  "membership": {},
  "observations": [],
  "inferences": [],
  "uncertainties": [],
  "ranked_proposals": [],
  "deferred_or_displaced": [],
  "fact_refs": [],
  "worker_trace": {}
}
```

Every task permitted to bear valid thesis evidence must first be linked to `IW-SF3-CTO77-RECURRING` as `existing_anchor` and added to the projection's sorted unique `thesis_task_ids` field. The controller performs that projection update before recording evidence. At most 100 thesis-bearing tasks are valid.

Discovery uses `ak direction show IW-SF3-CTO77-RECURRING --machine`, validates every projected thesis task has the exact link/repo/scope contract, then calls `ak evidence task <task_id> --machine` for each. It collects every evidence record matching exact check type/schema/Decision 77; records on unprojected tasks are non-authorizing and never valid thesis state. The collected set, capped at 100 thesis records, must form exactly one complete non-forking chain from revision 1 to one head, and that head must equal projected `thesis_head_evidence_id`. This enumeration detects a crash after evidence recording but before head update as an unprojected head/orphan and fails closed.

Revision 1 has no predecessor. Each later revision references one collected predecessor and equals predecessor revision + 1. Missing or wrong projected task/head, gaps, duplicate revisions, multiple successors, forks, cycles, multiple heads, expired head, invalid fact refs, over-limit sets, or missing census basis fails closed. Recommendations are proposal-only and never create owner commitments.

## Canonical wave and WIP model

Successor wave keys use `IW-SF3-CTO77-<SLUG>` and are direct children of `SF3`, linked to Decision 77. Every admitted wave requires:

- direction state/detail equals one exact legal projection form below;
- AK evidence `check_type=portfolio_wave_admission_v2`, schema `softwareco.portfolio-wave-admission.v2`;
- exact decision, epoch, wave, owner task IDs, owner acceptance receipts, controller task, pre-count, and post-count.

Exact direction projection forms use sorted unique CSV ID lists:

```text
# state=active
portfolio_admitted_decision_77;epoch_id=<id>;admission_evidence_id=<id>;owner_task_ids=<csv>;release_evidence_ids=none;outstanding_owner_task_ids=<csv>

# state=active
portfolio_partial_release_decision_77;epoch_id=<id>;admission_evidence_id=<id>;owner_task_ids=<csv>;release_evidence_ids=<csv>;outstanding_owner_task_ids=<csv>

# state=active and admission blocked
portfolio_reconciliation_required_decision_77;admission_evidence_id=<id>;release_evidence_ids=<none|csv>;outstanding_owner_task_ids=<csv>;reason_evidence_id=<id>

# state=done, no completed outcome
portfolio_returned_decision_77;admission_evidence_id=<id>;release_evidence_ids=<csv>;outcome_evidence_id=none

# state=done, completed outcome
portfolio_completed_decision_77;admission_evidence_id=<id>;release_evidence_ids=<csv>;outcome_evidence_id=<id>
```

Every projected release ID maps through its evidence payload to exactly one admitted owner task. `outstanding_owner_task_ids` equals admitted task IDs minus valid released/returned task IDs. Wrong order, duplicates, missing mappings, illegal state/detail combinations, or disagreement with controller evidence enters `portfolio_reconciliation_required_decision_77` and blocks admission.

Each owner-task membership has a linear event chain in Decision-77 admission/release evidence using exact predecessor event ID. Valid transitions:

```text
not_admitted -> admitted
admitted -> released_terminal
admitted -> returned_to_owner
```

No duplicate admission or release is legal. A multi-task wave remains outstanding until every admitted task has a valid owner release receipt and matching controller release evidence. Wave completion is separate and additionally requires all terminal acceptances and outcome evidence.

WIP reconstruction uses only shipped structured AK reads:

1. `ak direction show SF3 --machine` enumerates every `IW-SF3-CTO77-*` child and its projected admission/release/outcome evidence IDs.
2. The bounded epoch-index chain enumerates every Decision-77 controller task ID (maximum 100 epochs).
3. `ak evidence task <controller_task_id> --machine` enumerates that epoch's admission/release evidence; more than 500 total Decision-77 membership events fails closed.
4. Exact `ak evidence show <id> --json`, `ak governance show <id> --json`, and `ak task show <id> --machine` validate projected event, owner receipt, and task refs.

Decision 74 events are excluded by decision ID. Admission becomes effective only when valid controller evidence and matching direction projection both exist. Any orphan evidence, missing projection/event, duplicate/fork, partial release, owner disagreement, or post-read mismatch counts the affected wave/task as outstanding and blocks new admission until explicit reconciliation. Limits remain two admitted waves and six outstanding owner tasks. A second concurrent wave requires a direct human exact-wave checkpoint.

# Objective proof and checker

## Current-objective proof

After the additional independent wave and Run C, the exact successor objective task records:

- `check_type=portfolio_cto_recurrence_objective_v1`;
- `result=pass`;
- schema `softwareco.portfolio-cto-recurrence-objective.v1`;
- Decision 77 and objective task ID;
- Run A and Run C trace/hashes;
- pre/post thesis evidence IDs;
- wave, owner receipts/task/evidence, release, and outcome refs;
- deterministic checker results;
- known limitations;
- `framework_terminal_receipt_created=false`;
- `framework_revocation_receipt_created=false`;
- `framework_supersession_receipt_created=false`;
- `external_effects`.

The objective task may then close. No framework terminal receipt is created or inferred. `IW-SF3-CTO77-RECURRING` remains `active` as the non-authorizing framework/head projection and records objective-complete phase plus the post-outcome thesis head; only framework terminal/revoked/superseded reconciliation marks it `done`.

## Normative checker matrix

The owner checker retains `--require-terminal` for the Decision 74 negative control and adds exact Decision 77 modes:

| Mode | Required result |
|---|---|
| `--require-77-preactivation` | decision accepted/implementation ready; no epoch; advisory |
| `--require-77-framework` | framework accepted, reviewed, nonterminal; no claim that epoch is active |
| `--require-77-epoch-active` | exact epoch-chain head, controller claimant/lease, review window, owner/WIP reads pass |
| `--require-77-epoch-inactive` | no active epoch due absence, handback, or expiry; advisory |
| `--require-77-framework-terminal` | terminal/revoked/superseded precedence; advisory |
| `--require-77-thesis-current` | exactly one valid nonexpired thesis head |
| `--require-77-objective-complete` | exact recurrence proof passes while no framework terminal/revocation/valid supersession exists |

Every mode binds exact Decision 77, exact concerns/schemas, and deterministic bounded queries. Unknown mode or ambiguity exits nonzero.

## Required negative controls

Tests must cover:

- Decision 74 remains terminal;
- no accepted Decision 77;
- accepted framework with no epoch;
- expired, handed-back, or overlapping epoch;
- claimant/task/lease mismatch;
- overdue, paused, forked, or invalid framework review;
- applied revocation, terminal, or supersession overriding apparent epoch state;
- malformed, stale, forked, gapped, or multiply headed thesis;
- admission/release/projection/owner disagreement;
- two-wave/six-task limits and missing second-wave checkpoint;
- read-only worker attempting mutation;
- objective proof completion with no terminal receipt;
- terminal receipt taking precedence over objective or epoch evidence.

# Options considered

## Reopen Decision 74

Rejected. Receipt `8870` is immutable terminal authority.

## New architecture decision for every wave

Rejected as ordinary recurrence. Safe but repeats the canary mistake.

## Indefinite standing delegated office

Rejected by review. Human silence would preserve an appointed office.

## Dormant framework plus finite human-authorized epochs

Selected. It supports recurrence while authority expires automatically and is absent between epochs.

## Generated autonomous agent repository

Deferred. Packaging does not solve authority or durable state.

# Rollout and rollback

## Post-acceptance rollout

1. Write ADR, implementation plan, and validation/rollback plan.
2. Create `IW-SF3-CTO77-RECURRING` without altering `SF3` terminal detail.
3. Generalize prompt/mode/checker and validate all negative controls.
4. Create separate source-mutation-forbidden epoch controller and exact objective/thesis tasks.
5. Obtain one direct human epoch authorization and atomically claim controller.
6. Run fresh read-only Run A; controller verifies and records thesis revision.
7. Obtain direct owner receipts for one non-DesignMD wave.
8. Admit, execute, validate, terminally accept, release, and record outcome through owner-native tasks.
9. Run fresh read-only Run C; controller records post-outcome thesis revision.
10. Record objective proof and close the objective task without a framework terminal receipt.

## Rollback and escape hatch

Before epoch activation, revert only Decision-77 implementation/projection changes. Decision 74 history remains untouched.

After epoch activation:

- expiry or handback ends the epoch;
- human revocation/terminal ends all authority immediately;
- stop admissions and preserve owner lifecycle;
- reconcile wrappers through owner-originated release/return facts;
- source owners roll back only through their own tasks;
- preserve immutable receipts/evidence and report reconciliation conflicts rather than retry mechanically.
