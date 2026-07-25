---
summary: "Validation, rollout, revocation, and rollback contract for Decision 77's recurring CTO framework."
read_when:
  - "Validating or rolling out Decision 77 after acceptance, or stopping an epoch/framework."
type: "plan"
status: "blocked_pending_decision_acceptance"
date: "2026-07-25"
decision_id: 77
governance_task_id: 4205
---

# Decision 77 validation, rollout, and rollback

## Validation layers

### Documentation and review

- docs strict validation passes;
- `git diff --check` passes;
- exact problem/evidence/RFC/review/ADR/plan chain is tracked;
- Decision 77 passport reports aligned `ready_for_adr` closure before acceptance;
- after acceptance, ADR/evidence refs and linked-task re-evaluation are present.

### Decision 74 negative control

The existing terminal proof remains mandatory:

```bash
./scripts/check-cto-operator-surface.sh --require-terminal
```

It must continue to prove receipt `8870`, terminal controller `4182`, completed DesignMD wave, exact `SF3` terminal detail, and historical task-link topology. Any Decision 77 implementation that weakens this check fails rollout.

### Decision 77 deterministic modes

The extended checker must independently prove:

- `--require-77-preactivation`;
- `--require-77-framework`;
- `--require-77-epoch-active`;
- `--require-77-epoch-inactive`;
- `--require-77-framework-terminal` when applicable;
- `--require-77-thesis-current`;
- `--require-77-objective-complete`.

Unknown options and ambiguous state exit nonzero.

### Required negative controls

Test at least:

- absent/unaccepted Decision 77;
- accepted framework without epoch;
- expired, handed-back, overlapping, forked, or malformed epoch chain;
- claimant/task/lease mismatch;
- expired/paused/forked framework review;
- terminal/revocation/supersession precedence;
- wrong/missing Decision-77 projection;
- thesis task/head mismatch, fork, orphan, gap, cycle, stale head, and bounds;
- admission/release/projection/owner disagreement;
- WIP limit breach and missing second-wave checkpoint;
- read-only worker mutation attempt;
- objective proof with any framework terminal/revocation/supersession event;
- Decision 74 terminal state after all successor changes.

### Fresh-session proof

Run A and Run C each use a distinct `pi --mode rpc --no-session` process. Evidence captures:

- process start and runtime identity;
- exact prompts and tool commands;
- absence of previous transcript/thesis input;
- mode/prompt digests;
- AK/source-owner readbacks;
- stdout/stderr hashes;
- repository commits;
- worker candidate payload;
- controller independent verification.

Run C must identify the new completed wave and released WIP without receiving Run A's recommendation.

### Owner outcome proof

The selected non-DesignMD owner repo must prove:

- direct owner acceptance receipts;
- exact scoped AK task;
- observed baseline defect/need;
- implemented behavior;
- smallest truthful owner validation plus full owner gate where required;
- terminal owner acceptance;
- direct owner release;
- controller release and outcome evidence;
- clean landed owner worktree;
- zero unauthorized external effects.

## Rollout gates

```text
review closure
-> candidate ADR/plans
-> direct human Decision 77 acceptance
-> post-ADR task re-evaluation
-> inactive operator-surface implementation
-> Decision 74 negative control
-> controller/objective tasks
-> direct human epoch authorization
-> active epoch proof
-> Run A thesis
-> owner acceptance/admission/execution/release/outcome
-> Run C thesis
-> objective proof without framework terminal
```

Do not combine Decision acceptance, epoch authorization, owner acceptance, admission, or objective closeout into one implied event.

## Stop conditions

Stop immediately on:

- missing/expired/ambiguous framework review or epoch;
- claimant/controller mismatch;
- any terminal/revocation/supersession event;
- thesis or WIP fork/orphan/disagreement;
- owner objection;
- missing owner-native evidence;
- task-scope mismatch;
- dirty owner baseline not explicitly accepted;
- failed owner validation;
- architecture, product, appointment, exception, release, publication, public, irreversible, or external effect requiring reserved acceptance;
- inability to preserve Decision 74 terminal proof.

## Rollback before epoch activation

- revert Decision-77 prompt/mode/checker/projection changes through scoped commits;
- leave Decision 77 acceptance and immutable review history intact;
- leave Decision 74 and receipt `8870` untouched;
- no owner task compensation is needed because no wave was admitted.

## Epoch handback or expiry

- authority ends immediately at handback receipt or expiry time;
- stop admissions and mutations;
- do not infer framework terminal action;
- preserve active owner task lifecycle;
- record WIP handoff/reconciliation refs;
- a new epoch requires new human authorization and controller task.

## Framework revocation or terminal action

- direct human receipt ends every epoch immediately;
- stop all CTO control before projection reconciliation;
- return lifecycle decisions to owners through direct release/return receipts;
- reconcile Decision-77 projection to done only after fresh readback;
- preserve all evidence and report conflicts; do not retry mechanically.

## Owner rollback

Owner repositories roll back only through owner-native tasks, acceptance, and validation. A Softwareco wrapper cannot revert owner commits or change owner task status.

## Success criteria

Current objective success requires:

- one additional independent completed owner outcome;
- two fresh-session thesis revisions separated by that outcome;
- released portfolio WIP;
- exact recurrence proof evidence;
- Decision 77 framework remains nonterminal;
- Decision 74 remains terminal;
- direction, docs, checker, owner, and independent review gates pass.
