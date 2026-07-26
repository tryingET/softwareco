---
summary: "Validation, rollout, stop, and rollback contract for the 24-hour autonomous CTO canary."
read_when:
  - "Validating, installing, starting, observing, or stopping the autonomous CTO canary."
type: "plan"
status: "candidate"
date: "2026-07-26"
task_id: 4284
decision_id: 83
---

# Autonomous CTO canary validation, rollout, and rollback

## Inactive validation

```bash
python3 -m py_compile cto-canary/*.py
python3 -m unittest -v tests.test_cto_canary
npm --prefix owned/pi-extensions/packages/pi-modes run mode:lint -- \
  "$PWD/.pi/modes/softwareco-cto-canary.json" \
  "$PWD/.pi/mode-presets/softwareco-cto-canary.json"
```

Render `@ROOT@` and `@BUNDLE_DIR@` into a temporary directory and run `systemd-analyze --user verify` on all four units. The unrelated workstation `school-asr-recorder.service` warning is outside this candidate.

Run two `--fixture` cycles in a temporary state directory and require distinct process IDs, `canonical=false`, empty validation/runtime violations, and `verified_behavior=true`. Run production without an activation file and require exit `3` plus `REFUSED`.

Start a fresh no-session Pi RPC process with only the pinned Pi Modes extension and structured `PI_MODES`. `/mode-preview --json` must prove:

- base `softwareco-cto-canary`;
- role `base` and strategy `replace_base`;
- project source path;
- no overlays or diagnostics;
- composed prompt contains the exact canary base and dynamic AGENTS context.

This is prompt-composition proof, not a live canary cycle.

## Required adversarial review

Before ADR readiness require:

1. authority/security review of source-owner boundaries, receipt law, accepted-Git binding, capability isolation, secret exposure, and expiry;
2. runtime/operator review of Pi RPC, mode composition, systemd behavior, timeouts, cost, observability, recovery, and usefulness;
3. controlling synthesis citing both exact reviews.

## Acceptance and activation negative controls

Prove refusal for:

- Decision IDs `74` or `77`;
- unaccepted/blocked/wrong-RFC decision;
- non-human or malformed acceptance receipt;
- receipt commit different from accepted `HEAD`;
- dirty scoped candidate artifacts;
- mutable or missing installed bundle blobs;
- changed project mode, Pi version, or Pi Modes package digest;
- absent/malformed activation file;
- activation chain not headed by the exact receipt;
- non-human activation, wrong decision/commit/window/count;
- current UTC outside the exact 24-hour interval;
- 24 existing run directories;
- failed/oversized/incomplete portfolio probes;
- mode diagnostics, extension errors, UI, or tool execution;
- wrong provider/model, missing normalized usage/cost, per-cycle budget breach, malformed prior cost history, or cumulative budget exhaustion;
- runtime-package symlink escape or isolated package-copy digest drift;
- malformed, unresolvable, or coverage-divergent proposal output;
- watched AK DB or repository state change during a cycle.

## Operational rollout

The candidate is inactive until two separate human actions:

1. `activate_candidate.py --install` installs exact accepted Git blobs and disabled units;
2. installed `start_candidate.py` with repeated exact identity arguments plus `--start` records the activation receipt and enables the hourly and expiry timers.

Immediately inspect:

```bash
systemctl --user status softwareco-cto-canary.timer softwareco-cto-canary-stop.timer
systemctl --user list-timers 'softwareco-cto-canary*'
journalctl --user -u softwareco-cto-canary.service --since today
```

Do not call a cycle successful merely because the process exited zero. Inspect `result.json`, exact mode preview, provider/model, token/usage/cost and cumulative cost, coverage, validation errors, watched state changes, runtime policy violations, and the proposal's evidence references.

## Stop conditions

Stop immediately on unexpected AK/Git change, tool or extension activation, prompt drift, non-fresh worker identity, unresolved evidence, inaccurate portfolio coverage, owner-authority language, self-dispatch, repeated provider failure, runaway model cost, timer persistence after expiry, or any public/release/external effect beyond model API calls and private local state.

Direct-human early stop:

```bash
python3 <accepted-bundle>/cto-canary/stop_candidate.py --human-stop
```

Expiry is authority by time. The stop timer invokes `--expiry` to disable triggers and update only local state; it does not impersonate a human AK receipt. Runtime also rejects late execution independently.

## Rollback

Before acceptance, revert only candidate paths and preserve Decisions 74/77. After installation but before activation, disable/remove the four user units and commit-addressed bundle; no AK control receipt exists. After activation, use direct-human early stop, preserve receipts/results, then disable units. Never delete governance history to simulate rollback.

Owner repositories need no compensation because the canary has no owner mutation authority. Any observed owner change is a stop-and-investigate event, not automatically attributed to the canary.

## Success criteria

Success requires verified supervision for the intended window, no more than 24 fresh cycles, hard expiry, useful evidence-linked proposals, transparent gaps and cost, zero canary-authored authority/owner lifecycle mutation, and independent synthesis. It does not authorize a successor autonomous executor.
