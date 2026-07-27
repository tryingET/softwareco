---
summary: "Human acceptance, install, activation, observation, and stop handoff for the autonomous CTO canary."
read_when:
  - "Preparing to accept or run the 24-hour autonomous CTO canary."
type: "runbook"
status: "decision83_stopped_decision86_corrective_review_pending"
date: "2026-07-26"
task_id: 4284
decision_id: 86
---

# Autonomous CTO canary human handoff

## Current legal state

Decision `83` is accepted history but its activation was stopped before any model call. Acceptance receipt `9173`, activation receipt `9189`, and direct-human stop receipt `9201` are immutable. Its installed bundle remains for evidence; all units are inactive, both timers are disabled, its activation file is `human_stopped`, and it has zero run directories.

Decision `86` is the inactive corrective candidate. It has no acceptance, installation, activation, or model-call authority. It must receive fresh exact-source review and a new direct-human acceptance bound to a new commit. Do not reuse receipts `9173` or `9189`, the Decision 83 bundle, or the temporary MITO compatibility shim.

Do not substitute Decisions `74`, `77`, or `83`.

## Gate A — review and architecture acceptance

Require all of the following:

- separate AK decision is `ready_for_adr` through controlling multi-lane synthesis;
- candidate ADR and implementation/validation plans are committed;
- exact candidate commit passes code, mode, systemd, docs, decision, and independent-review gates;
- Decisions 74 and 77 remain unchanged;
- direct human reviews the external effects: up to 24 `openai-codex/gpt-5.6-sol` calls, a USD 2 post-call stop threshold and USD 25 cumulative preflight threshold (not provider-side hard caps; one call may overrun), plus private local state.

The controller prepares one exact acceptance script with concrete `<DECISION_ID>`, `<TASK_ID>`, `<COMMIT>`, and review references, then pauses. The human executes it directly. Fresh-read the resulting receipt and decision; pasted output is not authority.

## Gate B — commit-addressed install, no start

After accepted readback:

```bash
python3 cto-canary/activate_candidate.py \
  --decision-id <DECISION_ID> \
  --acceptance-receipt-id <ACCEPTANCE_RECEIPT_ID> \
  --accepted-commit <COMMIT> \
  --install
```

Expected result states `installed=true`, `started=false`, and `enabled=false`. Inspect the commit-addressed bundle and rendered units. Installation is a direct-human external effect and does not activate the canary.

## Gate C — exact 24-hour activation

From the installer-reported accepted bundle:

```bash
python3 <ACCEPTED_BUNDLE>/cto-canary/start_candidate.py \
  --decision-id <DECISION_ID> \
  --acceptance-receipt-id <ACCEPTANCE_RECEIPT_ID> \
  --accepted-commit <COMMIT> \
  --start
```

This direct-human command records the decision-specific activation receipt, writes its exact 24-hour activation membrane, and enables both timers. Fresh-read the control concern and timer state. Stop if receipt, time, commit, or timer state differs.

## Observe

```bash
systemctl --user list-timers 'softwareco-cto-canary*'
systemctl --user status softwareco-cto-canary.timer softwareco-cto-canary-stop.timer
journalctl --user -u softwareco-cto-canary.service --since today
find ~/.local/state/softwareco-cto-canary/runs -mindepth 1 -maxdepth 1 -type d | sort
```

For each cycle inspect `result.json`, `mode-preview.json`, and errors. Treat all content as proposal-only. Human/AK/owner workflows remain separate.

The first corrected cycle must additionally prove: the narrow snapshot helper stages a private `ak-snapshot/`; the model service has no source-DB or broad-workspace bind; AK live-gate reads succeed through the snapshot; the packet fingerprints both source DB and WAL; and no DB, WAL, or watched Git change occurred from collection through immediate pre-dispatch and post-call checks.

## Early stop

```bash
python3 <ACCEPTED_BUNDLE>/cto-canary/stop_candidate.py --human-stop
```

Fresh-read the stop receipt and disabled timer state. Preserve run artifacts for synthesis.

## Expiry

At the exact receipt-bound deadline, authority ends by time. The expiry timer disables triggers and updates local state without writing an AK receipt. A late main-service invocation still refuses independently. If timers remain enabled, disable them manually and record the operational discrepancy; do not infer extended authority.
