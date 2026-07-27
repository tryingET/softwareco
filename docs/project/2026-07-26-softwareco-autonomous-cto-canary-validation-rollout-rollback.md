---
summary: "Validation, rollout, stop, and rollback contract for the 24-hour autonomous CTO canary."
read_when:
  - "Validating, installing, starting, observing, or stopping the autonomous CTO canary."
type: "plan"
status: "decision86_corrective_candidate"
date: "2026-07-26"
task_id: 4284
decision_id: 86
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

Render `@ROOT@` and `@BUNDLE_DIR@` into a temporary directory and run `systemd-analyze --user verify` on all five units, including the narrow snapshot helper. The unrelated workstation `school-asr-recorder.service` warning is outside this candidate.

Run a real transient snapshot-service probe with `ProtectSystem=strict`, `ProtectHome=tmpfs`, read-only binds for only the authority DB and optional WAL, no network address family, and private writable state. Require it to stage the current stable pair, then require installed AK in a separate model-service-equivalent sandbox without source-DB/workspace access to read a known decision from that snapshot. A source read-only-filesystem error, broad workspace bind, or direct AK/model-service access to the source DB fails the correction.

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
- wrong provider/model, missing normalized usage/cost, per-cycle stop-threshold breach, malformed/non-finite prior cost history, or inability to reserve the next cycle under the cumulative threshold;
- runtime-package symlink escape or isolated package-copy digest drift;
- malformed, unresolvable, or coverage-divergent proposal output;
- watched AK DB or repository state change during a cycle.
- missing, unstable, incoherent, or catalog-invalid source DB+WAL snapshot;
- AK configured to open the source authority DB instead of the private snapshot;
- source authority DB or watched Git drift after collection but before the model call;
- active/nonterminal predecessor activation, missing predecessor stop-chain head, or reused decision-specific control history;
- noncanonical MITO governance token or a stopped empty-cgroup service retained as `failed` without reset and verification.

## Operational rollout

The candidate is inactive until two separate human actions:

Decision `83` is not restartable. Decision `86` requires a fresh acceptance receipt and commit-addressed bundle. Its start path may archive Decision 83's `human_stopped` activation only after verifying receipt `9201` as that predecessor control-chain head.

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

Before corrective acceptance, revert only candidate paths and preserve Decisions 74/77 plus Decision 83 receipts `9173`, `9189`, and `9201`. After installation but before activation, disable/remove the four user units and the new commit-addressed bundle; no Decision 86 control receipt exists. After activation, use direct-human early stop, preserve receipts/results, then disable units. Never delete governance history or predecessor state to simulate rollback.

Owner repositories need no compensation because the canary has no owner mutation authority. Any observed owner change is a stop-and-investigate event, not automatically attributed to the canary.

## Success criteria

Success requires verified supervision for the intended window, no more than 24 fresh cycles, hard expiry, useful evidence-linked proposals, transparent gaps and cost, zero canary-authored authority/owner lifecycle mutation, and independent synthesis. It does not authorize a successor autonomous executor.
