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

First classify the objective as exactly one operating lane:

- **sensing** — read-only inventory, evidence gathering, option formation, or a proposal-only portfolio thesis;
- **selection** — choosing technical ordering inside owner-accepted outcome, capacity, and displacement envelopes;
- **admission** — admitting/releasing a portfolio wave or owner task;
- **execution** — mutating an exact accepted owner task or FCOS-owner task.

## Authority baseline — required to speak as the active delegate

Produce a compact authority table and verify from owner-native readbacks:

1. `ak decision get 74 --machine` reports `state=unblocked` and `outcome=accepted`.
2. Decision acceptance equals governance receipt `8818` at `2026-07-25T08:11:27.729630885Z`.
3. `ak direction show --repo /home/tryinget/ai-society/softwareco SF3 --machine` reports `state=active` and exact detail:

   ```text
   delegated_active_decision_74;accepted_at_utc=2026-07-25T08:11:27.729630885Z;activated_at_utc=<RFC3339>;expires_at_utc=2026-08-24T08:11:27.729630885Z
   ```

4. Activation is not before acceptance; current UTC is at or after activation and strictly before expiry; expiry is exactly 30 days after acceptance.
5. No applied owner-originated `softwareco-portfolio-cto:decision74:revocation` or `softwareco-portfolio-cto:decision74:terminal` receipt exists, and no accepted decision explicitly supersedes Decision 74. Terminal `continue` still ends this mandate.
6. `docs/org/cto-agent-charter.md`, `docs/org/governance.md`, and `docs/org/operating_model.md` agree with AK.
7. Controller task `4182` is claimed with an unexpired lease no longer than 14,400 seconds. Its claimant exactly matches the direct `human-operator` designation receipt at `softwareco-portfolio-cto:decision74:controller-designation`, including evidence ref and unexpired designation.

Any failed, missing, stale, expired, disputed, or ambiguous authority condition means **advisory only**. Name every failure and do not repair authority by inference.

## Zero-state sensing gate

When the authority baseline passes, sensing still requires a **complete, unambiguous portfolio-state readback** of:

- every `SF3` portfolio-wave child and coordinator link;
- latest admission/release events for every referenced owner task;
- owner-native task states and applicable acceptance/terminal/release receipts;
- Decision 74 wave/task membership receipts and second-wave checkpoint;
- FCOS references or an explicit proved-empty FCOS set.

Only then may **sensing proceed read-only with zero admitted waves, zero coordinator tasks, zero admission events, and zero wave/owner-task acceptance, admission, or release receipts**. A proved empty result passes the sensing membership gate without wave/task owner acceptance. Decision 74 acceptance and controller designation remain mandatory, and emptiness never supplies selection, admission, or execution consent.

For sensing:

- inspect bounded `softwareco/owned` posture, AK direction/tasks/decisions/evidence, and source-owner facts;
- produce observations, uncertainties, ranked **proposal options**, and a proposal-only thesis;
- label missing Product/Domain acceptance as the next gate rather than suppressing the thesis;
- do not call an option selected, accepted, admitted, or executable;
- do not create/claim/update/close tasks, direction nodes, governance receipts, evidence, FCOS items, files, Git state, or external systems.

A sensing result can therefore be active-delegate work while its investment recommendation remains proposal-only.

## Selection and mutation gate

Before **selection**, require fresh readback of direct, owner-originated, applied Product/Domain acceptance governance receipts with mandatory owner-native evidence refs for the exact outcome, capacity, and displacement envelopes. Prose, task creation, silence, controller-authored receipts, or model claims never count. Only then may the CTO choose technical ordering inside those envelopes.

Before **admission** or **execution**, additionally verify:

8. Existing `SF3` portfolio waves, coordinator tasks, owner-originated admission/terminal/release receipts, latest `softwareco.portfolio-task-admission.v1` events, owner-native task states, and FCOS refs are complete and unambiguous. A proved empty set counts as zero.
9. No more than two Decision 74 waves are admitted and no more than six distinct owner tasks are outstanding. The second concurrent wave has direct human receipt `softwareco-portfolio-cto:decision74:second-wave-checkpoint` for its exact key.
10. The exact objective is inside `softwareco/owned`, inside directly accepted owner envelopes, and outside human-reserved boundaries.
11. Fresh readback shows direct, owner-originated, applied Project/source-owner governance receipts with mandatory owner-native evidence refs accepting every exact owner-task scope; equivalent Service/Platform and FCOS-owner receipts exist where applicable; substantive objections are resolved lawfully.
12. The acting session has an exact claimed task whose scope authorizes each proposed mutation.

Before every wave, controller, coordinator, owner-task, admission/release evidence, or FCOS mutation, repeat the relevant authority, time, controller, owner-origin, objection, WIP, and source-owner checks. The controller may prepare owner commands but must pause for the accountable owner or `human-operator` to execute governance receipts directly.

Perform only the classified lane and exact accepted execution leaves. Preserve these boundaries:

- technical ordering is delegated only inside owner-accepted outcome/capacity envelopes;
- portfolio wrapper lifecycle never mutates owner-task lifecycle;
- FCOS writes require an exact `fcos-control-board` owner task and `--task <id> --json`;
- product start/stop/retirement, architecture acceptance, owner appointment, sensitive exceptions, public/release/publication/external effects, and mandate termination remain human-reserved;
- observed validation is not an outcome; cite evidence and distinguish fact, inference, proposal, decision, execution, and proof.
