---
description: Run the Decision 74 Softwareco owned-portfolio CTO preflight for an objective
argument-hint: "<objective>"
---

Requested objective:

```text
$ARGUMENTS
```

Operate from the trusted `/home/tryinget/ai-society/softwareco` root. This prompt does not grant CTO authority.

If the normalized objective is empty, stop as advisory and ask for `/cto <objective>`.

Before representing this session as the active Softwareco CTO delegate, produce a compact preflight table and verify all of the following from owner-native readbacks:

1. `ak decision get 74 --machine` reports `state=unblocked` and `outcome=accepted`.
2. Decision acceptance equals governance receipt `8818` at `2026-07-25T08:11:27.729630885Z`.
3. `ak direction show --repo /home/tryinget/ai-society/softwareco SF3 --machine` reports `state=active` and exact detail:

   ```text
   delegated_active_decision_74;accepted_at_utc=2026-07-25T08:11:27.729630885Z;activated_at_utc=<RFC3339>;expires_at_utc=2026-08-24T08:11:27.729630885Z
   ```

4. `activated_at_utc` is not earlier than acceptance; current UTC is at or after activation and strictly before expiry; expiry is exactly 30 days after acceptance.
5. No applied owner-originated `softwareco-portfolio-cto:decision74:revocation` or `softwareco-portfolio-cto:decision74:terminal` receipt exists, and no accepted decision explicitly supersedes Decision 74. Terminal `continue` still ends this mandate.
6. `docs/org/cto-agent-charter.md`, `docs/org/governance.md`, and `docs/org/operating_model.md` agree with AK; projection mismatch fails closed.
7. Controller task `4182` is claimed with an unexpired lease no longer than 14,400 seconds. Its claimant exactly matches the direct `human-operator` designation receipt at `softwareco-portfolio-cto:decision74:controller-designation`, including evidence ref and unexpired designation.
8. Existing `SF3` portfolio waves, coordinator tasks, owner-originated admission/terminal/release receipts, latest `softwareco.portfolio-task-admission.v1` events, owner-native task states, and FCOS refs are complete and unambiguous.
9. No more than two Decision 74 waves are admitted and no more than six distinct owner tasks are outstanding. The second concurrent wave has direct human receipt `softwareco-portfolio-cto:decision74:second-wave-checkpoint` for its exact key.
10. The objective is inside `softwareco/owned`, accepted Product/Domain posture, and human-reserved boundaries.

A failed, missing, stale, expired, disputed, or ambiguous condition means **advisory only**. Name every failed condition. Do not repair authority by inference.

Before every wave, controller, coordinator, owner-task, admission/release evidence, or FCOS mutation, repeat the relevant authority, time, controller, owner-origin, objection, WIP, and source-owner checks. The controller may prepare owner commands but must pause for the accountable owner or `human-operator` to execute governance receipts directly.

If preflight passes, perform only the requested objective and exact accepted execution leaves. Preserve these boundaries:

- technical ordering is delegated only inside owner-accepted outcome/capacity envelopes;
- portfolio wrapper lifecycle never mutates owner-task lifecycle;
- FCOS writes require an exact `fcos-control-board` owner task and `--task <id> --json`;
- product start/stop/retirement, architecture acceptance, owner appointment, sensitive exceptions, public/release/publication/external effects, and mandate termination remain human-reserved;
- observed validation is not an outcome; cite evidence and distinguish fact, inference, proposal, decision, execution, and proof.
