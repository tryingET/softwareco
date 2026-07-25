---
summary: "Validation, rollout, rollback, and revocation gates for Decision 74's Softwareco portfolio CTO workbench."
read_when:
  - "Validating, activating, rolling back, or revoking Decision 74."
type: "plan"
status: "active"
date: "2026-07-25"
decision_id: 74
execution_task_id: 4156
---

# Decision 74 — validation, rollout, and rollback

## Validation classes

### V1 — authority and projection

Require:

- Decision 74 `outcome=accepted` and ADR recorded;
- accepted timestamp from governance receipt `8818`;
- `SF3` not delegated before activation;
- Decision 68 described as expired history;
- Decision 74 charter/governance/operating-model projection consistency;
- exact human-reserved powers;
- owner-origin receipt and objection/fallback rules;
- exact hard expiry `2026-08-24T08:11:27.729630885Z`.

Failure leaves every CTO interaction advisory.

### V2 — Pi Modes package

From exact release `0.3.0` / `173b508b0bea27550f061e252e1d86a0638d2d71`:

- owner quality/check gate passes;
- release artifact gate passes;
- package has no runtime dependency substitution;
- installed package identity is exact;
- errors and stderr are inspected, not hidden behind command acceptance.

A mutable local checkout does not pass this gate.

### V3 — Softwareco mode/preset/prompt

Require:

- owner linter passes mode and preset;
- mode is schema v2 `append`;
- preset is native base plus only `softwareco-cto` overlay;
- selective `.pi` Git tracking passes;
- `/cto` has `argument-hint`, `$ARGUMENTS`, missing-objective stop, compact preflight, direct-owner receipt pause, repeated per-operation checks, and exact controller id;
- trusted Softwareco-root discovery and activation are observed live;
- `/mode off` returns to native host.

JSON/schema success is not live proof.

### V4 — controller and activation

Require:

- exactly one controller task linked to `SF3`;
- source mutation forbidden by its scope/guardrails;
- direct human designation governance receipt with exact claimant, evidence ref, and lease ≤14,400 seconds;
- atomic claim/readback equality;
- no revocation, terminal, supersession, or expiry;
- pre/post-read around `SF3` activation;
- exact accepted/activated/expiry arithmetic.

No human receipt means no activation.

### V5 — negative behavior

Prove advisory/stop behavior for:

- missing objective;
- untrusted or non-root invocation;
- Decision 74 not accepted;
- inactive/malformed/mismatched `SF3`;
- before activation or at/after expiry;
- revocation before `SF3` reconciliation;
- terminal `continue`;
- explicit supersession;
- missing/stale controller claim or designation;
- controller-authored owner consent;
- owner objection and invalid fallback;
- missing terminal receipts;
- duplicate/cross-wave task admission;
- WIP ceiling;
- declined FCOS handoff.

Behavioral tests are evidence, not a security proof over every model response.

## Rollout sequence

```text
accepted ADR
-> plans attached in AK
-> task 4156 reevaluated/unblocked
-> tracked workbench + projection implementation
-> deterministic checks
-> exact package install
-> fresh live Pi proof
-> controller task creation
-> direct human designation
-> controller claim
-> exact SF3 activation
-> advisory portfolio-thesis canary
-> first owner-accepted outcome wave
-> human terminal decision
```

Do not combine controller designation, delegation activation, first wave admission, and mandate terminal choice into one implied consent event.

## Rollback before activation

- `/mode off` if selected;
- revert only isolated `.pi`, script, and projection changes;
- restore prior exact Pi package setting if installation causes regression;
- keep `SF3` active only as a non-delegated decision/implementation frame;
- leave Decision 74 and review history immutable;
- no owner or FCOS work exists to unwind.

## Revocation after activation

1. `human-operator` directly records the exact revocation governance receipt.
2. Authority ends immediately even if `SF3` still displays active detail.
3. Stop admissions and CTO-controlled mutation.
4. Record owner handoffs for every admitted task.
5. Owners choose continuation, pause, failure, or completion under their own law.
6. Fresh-read and reconcile `SF3` to revoked detail; do not claim CAS.
7. `/mode off` for operator clarity.
8. Preserve evidence and perform a learning review.

Revocation never auto-closes owner tasks or FCOS items.

## Recovery and failure claims

- If Pi package install succeeds but live proof fails, report `installed_not_proved`; do not activate.
- If `SF3` update conflicts, report `activation_reconciliation_required`; do not retry mechanically.
- If controller claim expires, report `controller_stale`; require direct human stale-session/handover receipt before exact unclaim/reclaim.
- If an external effect somehow occurred, record the effect and owner recovery; do not call compensation exact rollback.
- If hard expiry arrives before activation, Decision 74 expires without an operating canary and requires a new decision to continue.

## Minimum closeout evidence for task 4156

- commits for plan, ADR, workbench, projections, validation, and live proof;
- owner linter and Softwareco checker outputs;
- strict docs and `git diff --check`;
- immutable Pi Modes package/version/hash evidence;
- live mode/preset/prompt command receipt;
- independent cold-start review;
- exact AK evidence ids;
- explicit state that portfolio thesis/outcome execution is a successor leaf, not completed by workbench activation.
