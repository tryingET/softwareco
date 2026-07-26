---
summary: "Implementation sequence for the inactive autonomous CTO canary and later human-gated 24-hour run."
read_when:
  - "Implementing or activating the autonomous CTO canary."
type: "plan"
status: "candidate"
date: "2026-07-26"
task_id: 4284
decision_id: 83
---

# Autonomous CTO canary implementation plan

## Slice 1 — inactive artifacts

1. Track the `replace_base` mode and exact preset.
2. Track bounded collector, validator, supervisor cycle, commit-addressed drift-detecting installer, direct-human start/stop tools, and systemd unit templates.
3. Track strict output schema and deterministic fixture tests.
4. Keep every production cycle fail-closed without accepted decision plus activation receipt.

## Slice 2 — implementation proof

Validate:

- Python compile and unit tests;
- Pi Modes schema lint;
- rendered systemd unit verification;
- absent-activation refusal;
- two deterministic fresh fixture cycles;
- fresh real Pi `/mode-preview` source/fingerprint/composition proof;
- collector bounded real read-only snapshot;
- no AK, Git, direction, owner, service, or external mutation from fixture proof.

A real model cycle is not legal before acceptance and activation.

## Slice 3 — architecture decision

1. Create one company-scoped architecture decision linked to task `4284`.
2. Attach problem, RFC, plans, evidence, and required review-set plan.
3. Run separate authority/security and runtime/operator reviews.
4. Require a controlling synthesis that cites both tracks.
5. Prepare the ADR only after `ready_for_adr` closure.

## Slice 4 — human acceptance and commit-addressed installation

1. Commit the exact reviewed candidate and ADR.
2. Prepare one exact architecture-acceptance command binding the full commit.
3. Pause for direct-human execution.
4. Fresh-read the receipt and AK decision.
5. Direct human runs `activate_candidate.py --install`; it installs exact Git blobs but starts nothing.

## Slice 5 — 24-hour test drive

1. Review installed manifest and systemd units.
2. Direct human runs `start_candidate.py` with exact decision, receipt, commit, and `--start` arguments.
3. Fresh-read activation receipt and timer status.
4. Observe the first cycle before relying on later cycles.
5. Monitor at most 24 hourly run directories, model/API failures, coverage, usefulness, and cost.
6. Stop immediately on authority drift, unexpected capabilities, unbounded cost, invalid evidence, or operational instability.
7. At exact expiry, runtime refuses further cycles and the stop timer disables triggers.

## Slice 6 — synthesis

Create an evidence-backed closeout distinguishing:

- installed and observed runtime behavior;
- proposal quality and false-positive/false-negative patterns;
- model/API and local-state effects;
- failures and coverage gaps;
- whether to stop, repeat another bounded canary, or propose a separately governed autonomous execution envelope.

No result automatically changes Decisions 74 or 77, owner authority, or canary scope.
