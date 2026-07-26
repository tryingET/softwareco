---
summary: "Human acceptance, install, activation, observation, and stop handoff for the autonomous CTO canary."
read_when:
  - "Preparing to accept or run the 24-hour autonomous CTO canary."
type: "runbook"
status: "blocked_pending_review_and_acceptance"
date: "2026-07-26"
task_id: 4284
decision_id: 83
---

# Autonomous CTO canary human handoff

## Current legal state

The candidate is inactive. No service has been installed, enabled, or started. No production model cycle is authorized. The exact decision ID, accepted commit, review closure, ADR, and architecture-acceptance receipt must be filled from fresh AK/Git readback after review.

Do not substitute Decision `74` or `77`.

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
  --decision-id 83 \
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

## Early stop

```bash
python3 <ACCEPTED_BUNDLE>/cto-canary/stop_candidate.py --human-stop
```

Fresh-read the stop receipt and disabled timer state. Preserve run artifacts for synthesis.

## Expiry

At the exact receipt-bound deadline, authority ends by time. The expiry timer disables triggers and updates local state without writing an AK receipt. A late main-service invocation still refuses independently. If timers remain enabled, disable them manually and record the operational discrepancy; do not infer extended authority.
