---
summary: "RFC for a standing Softwareco portfolio CTO mandate with bounded operating epochs and recurring fresh-session D2E proof."
read_when:
  - "Reviewing or implementing the recurring successor to Decision 74."
type: "rfc"
status: "in_review"
date: "2026-07-25"
predecessor_decision_id: 74
governance_task_id: 4205
review_mode: "strict-adversarial-multi-lane"
review_closure_mode: "multi_lane_requires_synthesis"
---

# RFC — recurring Softwareco portfolio CTO operating loop

## Decision requested

Accept a **prospective successor** to terminal Decision 74 that establishes a standing, human-accountable Softwareco portfolio CTO mandate over registered `softwareco/owned` repositories, operated only through short, human-authorized controller epochs.

The successor must enable repeated sensing and owner-native outcome waves without making a Pi session, strategic-root state, proof target, or completed wave into continuing authority.

See:

- [Problem and intent](2026-07-25-softwareco-recurring-portfolio-cto-problem-intent.md)
- [Evidence](2026-07-25-softwareco-recurring-portfolio-cto-evidence.md)

## Corrective principle

Decision 74's one-wave proof target was a **canary acceptance condition**, not the full recurring product outcome. This RFC separates six lifecycle facts:

| Fact | Effect |
|---|---|
| Objective completed | closes only the requested objective |
| Owner task completed | changes only owner-native task lifecycle |
| Portfolio wave completed | closes only that portfolio wrapper after owner evidence |
| Recurrence proof met | records maturity evidence; does not terminate authority |
| Controller epoch expires or hands back | ends only that operating epoch |
| Standing mandate terminal/revoked/superseded | ends the delegated office |

No checker, task result, evidence record, or wave transition may promote the first five into the sixth.

## Decision 74 preservation

The successor does not reopen, reverse, amend, or erase Decision 74 or human receipt `8870`.

- Decision 74 remains the accepted finite-canary decision.
- Receipt `8870` remains its terminal event.
- Controller task `4182` remains closed.
- The DesignMD wave and evidence remain attributed to Decision 74.
- `SF3` retains its Decision 74 terminal detail as historical readback unless a separately reviewed direction projection is adopted; strategic-root `state=active` alone never grants CTO authority.
- Every successor receipt, controller, epoch, task, and evidence record uses the successor decision identity.

## Goals

1. Reconstruct authority and portfolio state in a fresh process without session memory.
2. Maintain freshness-bounded portfolio-thesis revisions as AK evidence rather than a shadow backlog.
3. Select and execute successive owner-native outcome waves.
4. Preserve Product/Domain/Project/Service/Platform/FCOS authority.
5. Keep WIP finite and admissions serialized.
6. Permit recurring operation without a new architecture decision for each ordinary wave.
7. Keep every epoch bounded, revocable, and advisory on ambiguity.
8. Prove at least one additional independent outcome plus post-outcome re-entry.

## Non-goals

- no permanent autonomous executive;
- no generated CTO agent repository in this decision;
- no shadow database, backlog, scheduler, or global lock;
- no transfer of owner task lifecycle to Softwareco wrappers;
- no release, publication, product lifecycle, owner appointment, architecture acceptance, or external-effect authority;
- no reinterpretation of Decision 74 as active;
- no requirement that recommendations be byte-identical across models or sessions;
- no change to Decision 68's template-propagation freeze.

## Authority architecture

### Standing mandate

The accepted successor decision creates a standing constitutional delegation with:

- residual accountable owner: `human-operator`;
- delegated functional role: `softwareco-cto-agent`;
- jurisdiction: registered `softwareco/owned` repositories;
- WIP: at most two admitted waves and six outstanding admitted owner tasks;
- review interval: at least every 30 days;
- end conditions: direct human terminal decision, direct revocation, or explicitly superseding accepted decision.

Meeting a proof target or completing an objective does not end the standing mandate.

The accepted decision alone is necessary but not sufficient for operation. Without a valid operating epoch, `/cto` is advisory-only.

### Operating epoch

Each mutation-capable operating period has a unique `epoch_id`, new controller task, exact claimant, and direct human authorization receipt. Maximum authorization and controller-claim duration is 14,400 seconds.

Conceptual authorization concern:

```text
softwareco-portfolio-cto:decision:<decision_id>:epoch:<epoch_id>:authorization
```

The applied receipt must be directly originated by `human-operator`, use explicit consent and mandatory evidence, and contain:

```json
{
  "schema": "softwareco.portfolio-cto-epoch-authorization.v1",
  "decision_id": "<successor>",
  "epoch_id": "<unique>",
  "controller_task_id": "<task>",
  "claimant_id": "<exact claimant>",
  "authorized_at_utc": "<RFC3339>",
  "authorization_expires_at_utc": "<RFC3339>",
  "lease_seconds": "<=14400",
  "jurisdiction": "softwareco/owned"
}
```

Operation begins only after the exact claimant atomically claims the exact controller task inside the authorization window. The controller task is forbidden from source mutation. Every admission/release operation fresh-reads receipt, decision, controller, leases, standing-mandate terminal concerns, WIP membership, objections, and owner receipts before and after mutation.

A later fresh sensing process may reconstruct state read-only without being the controller claimant. Any mutation still requires the active epoch controller plus an exact execution task for the acting session.

Epoch expiry or handback makes mutation advisory-only but does not terminalize the standing mandate. Renewal requires a new human-originated epoch receipt; stale-session recovery and claimant transfer require direct human receipts.

### Standing terminal events

Exact successor concerns are decision-specific:

```text
softwareco-portfolio-cto:decision:<decision_id>:revocation
softwareco-portfolio-cto:decision:<decision_id>:terminal
softwareco-portfolio-cto:decision:<decision_id>:supersession
```

A direct applied revocation or terminal receipt ends authority immediately, before projection reconciliation. An explicitly superseding accepted decision independently ends the mandate. Terminal `continue` still ends the current standing mandate and requires a new or superseding accepted decision; ordinary recurrence uses epoch renewal, not terminal `continue`.

## Owner federalism

### Selection

Before selection, every affected Product/Domain owner directly accepts:

- outcome envelope;
- capacity envelope;
- displacement/deferment;
- success and stop criteria;
- applicable user or product evidence.

Sensing may rank proposal options before these receipts. It may not call one selected, admitted, or executable.

### Admission and execution

Before admission or execution:

- Project/source owners directly accept every exact owner-task scope;
- Service/Platform owners accept operational/shared-contract consequences when applicable;
- owner-native evidence references are mandatory;
- the acting session has an exact claimed task covering every mutation;
- WIP and objections pass fresh readback;
- FCOS writes, if genuinely cross-repo, occur only through FCOS owner authority.

Portfolio wrappers never claim, close, pause, resume, release, or return owner tasks. Owner lifecycle remains owner-native.

### Terminal acceptance and release

A wave completes only after every applicable owner directly accepts terminal outcome and implementation/operational evidence. A separate portfolio release record frees WIP only after the owner task is terminal or its owner explicitly accepts return-to-owner lifecycle.

Wave completion starts the next sensing opportunity; it does not end the standing mandate.

## Durable portfolio thesis

The live thesis is an AK evidence series, not a Markdown backlog. Each revision uses a schema equivalent to:

```json
{
  "schema": "softwareco.portfolio-thesis.v2",
  "mandate_decision_id": "<successor>",
  "thesis_revision": 1,
  "observed_at_utc": "<RFC3339>",
  "valid_until_utc": "<RFC3339>",
  "strategic_frame": "SF3",
  "membership": {
    "admitted_waves": [],
    "outstanding_owner_tasks": [],
    "released_waves": []
  },
  "evaluated_domains": [],
  "observations": [],
  "inferences": [],
  "uncertainties": [],
  "ranked_proposals": [],
  "deferred_or_displaced": [],
  "owner_evidence_refs": [],
  "prior_thesis_evidence_id": null
}
```

Every factual observation cites AK or fresh source-owner evidence. Inference and uncertainty are labeled. Ranked proposals create no task, owner consent, or backlog commitment. A revision expires rather than silently remaining current.

Markdown may explain a revision but cannot become live authority.

## Fresh-session continuity contract

Recurrence proof uses independent trusted-root `pi --mode rpc --no-session` processes. They receive no prior assistant transcript, generated thesis, or hidden state.

### Run A — reconstruct and sense

- discover and activate the tracked CTO mode;
- resolve the successor standing mandate and current epoch from AK;
- reconstruct portfolio membership, previous Decision 74 outcome, owner facts, WIP, objections, and uncertainties;
- record a new proposal-only thesis revision.

### Run B — owner-native outcome

After direct owner acceptance:

- admit one non-DesignMD wave;
- execute through an exact source-owner AK task;
- validate behavior in the owner repository;
- obtain direct terminal owner acceptance;
- release portfolio WIP and record outcome evidence.

### Run C — post-outcome re-entry

A later independent `--no-session` process must:

- fresh-read the still-standing mandate and current epoch posture;
- identify the completed new wave and released capacity;
- reconstruct the new membership state;
- produce the next proposal-only thesis revision without inheriting Run A's recommendation.

Pass requires agreement on authority, membership, owner facts, and evidence references—not byte-identical prose.

A negative control must show Decision 74 remains advisory-only under receipt `8870`.

## Current-objective completion

The operator-confirmed current objective is complete when:

1. this successor is accepted and one epoch is active;
2. Run A fresh-session reconstruction passes;
3. one additional independent owner outcome completes through the full federal chain;
4. Run C post-outcome re-entry passes;
5. the workbench's active/terminal checker distinguishes standing mandate, epoch, wave, and objective lifecycle;
6. AK evidence records the recurrence proof and remaining limits;
7. no standing-mandate terminal receipt is inferred or automatically created.

This completion permits reporting the objective done. It does not itself end the standing mandate.

## Operator surface changes after acceptance

Implementation should generalize, not weaken, the existing surface:

- `.pi/prompts/cto.md`: resolve successor standing mandate and epoch, separate read-only worker sensing from controller mutation, and require thesis evidence lineage;
- `.pi/modes/softwareco-cto.json`: describe recurring semantics without granting authority;
- `scripts/check-cto-operator-surface.sh`: retain Decision 74 terminal verification and add successor preactivation/epoch-active/epoch-inactive/standing-terminal checks;
- charter/governance/operating model: project accepted standing mandate and current epoch posture without pretending docs are authority;
- evidence docs: preserve negative and positive fresh-session traces with exact hashes and owner refs.

The implementation must not silently make the checker discover an arbitrary "latest" accepted decision. It validates the exact accepted successor binding and fails closed on multiple or ambiguous candidates.

## Controller and WIP mechanics

AK does not provide an atomic cross-repository admission transaction. The accepted procedural boundary remains:

1. one epoch-bound controller serializes portfolio membership changes;
2. pre-read exact authority, WIP, receipts, task scope, and objections;
3. create or update only the Softwareco wrapper under a scoped execution task;
4. record admission/release evidence referencing owner-native facts;
5. post-read and recount;
6. stop for manual reconciliation on disagreement; never claim compare-and-swap.

Maximum WIP remains two admitted waves and six outstanding admitted owner tasks. A second concurrent wave requires a direct `human-operator` checkpoint for its exact wave key.

## Options considered

### A — Reopen Decision 74

Rejected. Receipt `8870` is immutable terminal authority and cannot be undone by interpretation.

### B — New finite one-wave decision for every wave

Rejected as the recurring architecture. It preserves safety but repeats the exact canary mistake and makes ordinary operation depend on architecture decisions.

### C — Standing mandate with bounded operating epochs

Selected. It separates constitutional delegation from short controller authority, preserves human revocation, supports fresh-session reconstruction, and allows ordinary wave recurrence without an immortal session.

### D — Generated autonomous CTO agent repository

Deferred. Packaging behavior does not solve authority, owner consent, or durable state and adds another runtime surface before the workbench contract is mature.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| "Standing" becomes permanent unchecked authority | bounded epochs, 30-day human review, immediate terminal/revocation, fail-closed checker |
| Fresh session impersonates controller | read-only sensing allowed; mutations require exact epoch controller plus exact execution task |
| Thesis becomes a shadow backlog | AK evidence only, expiry, proposal labels, no lifecycle mutation |
| Wave completion silently renews/ends mandate | explicit lifecycle separation and checker assertions |
| Owner consent is centralized | direct owner-originated receipts with owner-native evidence |
| Strategic-root state is mistaken for delegation | accepted decision + epoch receipt + matching controller required; `SF3 state` alone never sufficient |
| Procedural controller is described as a lock | explicitly serialized best-effort protocol with post-read and manual reconciliation |
| Human receipt UX becomes burdensome | prepare one exact epoch command, direct execution, fresh AK readback; no paste-back ritual |

## Review requirements

Use strict adversarial multi-lane review with at least:

1. **authority/constitutional track** — standing-vs-epoch legality, Decision 74 preservation, human reservations, owner federalism;
2. **runtime/operator track** — fresh-session reconstruction, controller identity, thesis evidence, checker implementability, and dogfood proof.

A controlling synthesis must cite both exact review artifacts and emit `ready_for_adr`, `revise_rfc`, or `reject_current_direction`. ADR is illegal until the synthesis says `ready_for_adr`.

## Rollout sequence

After acceptance only:

1. write ADR, implementation plan, and validation/rollback plan;
2. generalize prompt, mode, and checker while Decision 74 stays terminal;
3. validate successor preactivation and Decision 74 negative control;
4. create a new source-mutation-forbidden epoch controller task;
5. obtain direct human epoch authorization and atomically claim the controller;
6. record current projections and positive active checker proof;
7. run fresh-session Run A and record thesis evidence;
8. obtain owner acceptance for one independent wave;
9. execute and verify through the source owner;
10. run fresh-session Run C and record recurrence evidence;
11. close the current objective without creating a standing terminal receipt.

## Rollback and escape hatch

Before successor activation, revert only successor implementation/projection changes and leave Decision 74 terminal history intact.

After epoch activation:

- direct human revocation or terminal receipt ends authority immediately;
- epoch expiry or handback stops mutation without ending the standing mandate;
- stop admissions and preserve owner lifecycle;
- reconcile Softwareco wrappers through explicit release/handoff facts;
- owner repositories roll back only through their own tasks and acceptance;
- preserve all receipts and evidence; do not rewrite the event as if it never occurred.
