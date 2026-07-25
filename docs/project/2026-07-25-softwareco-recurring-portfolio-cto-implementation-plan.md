---
summary: "Post-acceptance implementation plan for Decision 77's recurring CTO framework and recurrence proof."
read_when:
  - "Implementing Decision 77 after accountable-human acceptance."
type: "plan"
status: "blocked_pending_decision_acceptance"
date: "2026-07-25"
decision_id: 77
governance_task_id: 4205
---

# Decision 77 implementation plan

## Preconditions

Do not begin implementation until:

- Decision 77 passport reports `ready_for_adr`;
- candidate ADR and execution plans are tracked;
- `human-operator` directly accepts Decision 77 in AK;
- acceptance receipt and timestamp are fresh-read;
- task `4205` is explicitly re-evaluated for post-ADR execution;
- Decision 74 terminal checker still passes;
- direction check passes;
- unrelated `owned/docs/project/repo-capability-map.md` remains untouched.

## Slice 1 — Framework projection and inactive surface

1. Create AK-native `IW-SF3-CTO77-RECURRING` as `work_wave`, child of `SF3`, `pending`, linked to Decision 77.
2. Preserve `SF3` Decision 74 terminal detail exactly.
3. Generalize `.pi/prompts/cto.md` and `.pi/modes/softwareco-cto.json` for dormant-framework/epoch semantics.
4. Extend `scripts/check-cto-operator-surface.sh` with exact Decision 77 modes while preserving Decision 74 terminal mode.
5. Reconcile charter, governance, and operating-model projections to accepted-but-no-epoch posture.
6. Run deterministic preactivation and negative controls.

Pass: Decision 74 terminal proof passes; Decision 77 preactivation/framework checks pass; epoch-active check fails closed.

## Slice 2 — Objective and controller carriers

Create separate AK tasks:

- epoch controller: all source paths forbidden;
- recurrence objective/thesis task: exact Softwareco prompt/checker/evidence scope;
- later source-owner outcome task: created and accepted only in selected owner repo.

Link the objective/thesis task to `IW-SF3-CTO77-RECURRING` as `existing_anchor` and project its ID before any thesis evidence. Controller identity remains epoch-specific.

Pass: task scopes are exact, controller cannot mutate source, direction check passes, and no authority exists before human epoch authorization.

## Slice 3 — Human epoch authorization and activation

1. Prepare one exact `softwareco-portfolio-cto:decision77:epoch-index` authorization command.
2. Pause for direct human execution; do not request pasted stdout by default.
3. Fresh-read the receipt.
4. Atomically claim the exact controller task with lease ending no later than epoch expiry.
5. Run `--require-77-epoch-active` and projection checks.

Pass: exactly one valid epoch head, claimant/task/lease equality, current review window, no terminal/revocation/supersession, and no WIP ambiguity.

## Slice 4 — Fresh Run A and thesis revision

1. Start a trusted-root `pi --mode rpc --no-session` read-only process.
2. Provide no previous transcript, thesis, or recommendation.
3. Let it reconstruct Decision 74 history, Decision 77 authority, portfolio membership, owner facts, WIP, objections, and proposals.
4. Capture commands, readbacks, hashes, mode digest, process time, and repository commits.
5. Controller independently rereads every cited fact.
6. Project the thesis-bearing task ID if not already present.
7. Record `portfolio_thesis_v2` evidence, then update projected head with pre/post-read.
8. Run `--require-77-thesis-current`.

Pass: exactly one bounded thesis chain/head; no hidden session input; proposals create no consent or task lifecycle.

## Slice 5 — Independent owner outcome

1. Fresh-sense candidate owner repos; do not inherit Decision 74's selection.
2. Exclude DesignMD staged-impact work from the required independent outcome.
3. Obtain direct Product/Domain envelope and Project/source-owner task-scope receipts.
4. Create an exact owner-native task and applicable Service/Platform acceptance.
5. Revalidate WIP, objections, epoch/controller, and task scopes.
6. Create Decision-77 wave projection and controller admission evidence.
7. Execute in the owner repo under its task and validation contract.
8. Obtain terminal owner acceptance and direct owner release.
9. Record controller release and outcome evidence; reconcile direction detail.

Pass: complete federal chain, owner task lifecycle unchanged by wrapper, deterministic owner outcome proof, no unauthorized external effect.

## Slice 6 — Fresh Run C and objective closeout

1. Start a separate trusted-root `--no-session` read-only process.
2. Reconstruct the completed new wave, release, current WIP, and framework/epoch posture solely from durable facts.
3. Produce a new candidate thesis without inheriting Run A recommendation.
4. Controller independently verifies and records the next thesis revision/head.
5. Record `portfolio_cto_recurrence_objective_v1` evidence referencing Run A/C, both thesis IDs, owner receipts/task/evidence, release, outcome, checker results, and limitations.
6. Prove no Decision 77 terminal/revocation/supersession receipt was created.
7. Complete only the objective task and mark projection phase objective-complete; keep framework projection active and non-authorizing.

Pass: `--require-77-objective-complete`, direction check, docs check, owner gate, and independent review all pass.

## Slice 7 — Epoch disposition

Objective completion does not decide epoch disposition. The exact claimant may hand back early, or the epoch expires. Human framework terminal action is not requested or inferred.

Any future epoch requires new human authorization, controller task, claimant, and hard expiry.

## Commit strategy

Main-first, bounded commits:

1. accepted framework projection/operator surface;
2. epoch activation evidence/projections;
3. Run A thesis evidence/projection;
4. owner-repo implementation and owner projection commits;
5. portfolio outcome and Run C recurrence closeout.

Never include the unrelated capability-map modification.
