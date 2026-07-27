---
summary: "Stopped Decision 83 evidence and inactive corrective candidate evidence for Decision 86."
read_when:
  - "Reviewing what has and has not been proved before canary acceptance."
type: "evidence"
status: "decision83_stopped_pre_model_decision86_corrective_candidate"
date: "2026-07-26"
task_id: 4284
decision_id: 86
---

# Autonomous CTO canary candidate evidence

## Observed implementation facts

- Pi `0.80.10` exposes native `--system-prompt <text>` and repeatable `--append-system-prompt <text>` flags.
- Installed `@tryinget/pi-modes` `0.3.0` supports `replace_base`, which replaces the static base and retains the dynamic host envelope.
- Candidate mode and preset lint successfully.
- A fresh trusted-root no-session RPC process, with all extensions disabled except the pinned Pi Modes entrypoint, selected `softwareco-cto-canary` as role `base`, strategy `replace_base`, with no overlay and no diagnostics.
- `/mode-preview --json` contained the exact canary prompt plus global/workspace/Softwareco AGENTS context, current date, and cwd.
- The original candidate passed twenty-four deterministic tests before Decision 83 acceptance. The corrective candidate passes twenty-six tests, adding coherent WAL-snapshot and canonical governance-token/reset controls.
- Two fixture cycles used distinct process IDs, produced noncanonical proposal-only outputs, and passed strict validation.
- Production cycle invocation without activation refused with exit `3`.
- Rendered service, hourly timer, expiry service, and 24-hour timer passed `systemd-analyze --user verify`. The command also reported an unrelated pre-existing warning from `school-asr-recorder.service`.
- A real read-only collector run enumerated all 41 registered owned child repositories and produced a compact bounded 742 KB packet. It truthfully reported two missing registered repositories (`fcos-proving-lane` and `voice-dictation`) as coverage gaps rather than inferring completeness.

## Review correction

The first transcendent-loop implementation phase timed out and was not accepted as completed behavior. Independent review identified three blocking defects in that partial candidate:

1. mutable checkout code was not bound to the accepted commit;
2. the timer repeated indefinitely rather than ending after 24 hours;
3. the worker exposed too much host state and extension surface.

The first formal authority/security review of commit `3c551c4` returned `REVISE`. It additionally found self-attested bundle/unit identity, stale activation readback, in-flight expiry, path escape, broad home/environment exposure, incomplete mode-source proof, and missing negative controls. The correction compares bundle and rendered units with accepted Git objects, rereads decision/receipt before activation, caps and kills in-flight workers at stop/expiry, resolves portfolio paths under the owned root, hides general home state, filters the worker environment, pins Pi and Pi Modes trees, validates exact preview source/fingerprint/context, and adds negative tests. Remaining claims require fresh review of the correction commit.

Attempt-2 authority and runtime reviews of `443d45e` also returned `REVISE`. The next correction verifies service/timer stop results, uses a 30-second process-wide pre-expiry guard, binds the AK DB, copies Pi and Pi Modes into digest-pinned isolated bundle trees with symlink containment, reconstructs the complete expected prompt byte-for-byte, bounds probe pipes and the supplemental top-level census, pins `openai-codex/gpt-5.6-sol`, records normalized usage/cost, and records USD 2 cycle/USD 25 cumulative supervisory stop thresholds. These changes require another independent review.

Attempt-3 authority and runtime reviews of `a53427a` again returned `REVISE`. The latest correction removes installed-runtime fallback, verifies isolated trees, gates exact prompt and provider/model before any model call, strictly verifies systemd stop/cgroup/timer state, bounds top-level iteration before sorting, rejects non-finite cost, reserves the next cycle threshold, discloses possible one-call billing overrun, and fixes the Python recovery command. It requires final independent review.

Attempt-4 authority/runtime reviews of `f73a351` found an absent-manifest fallback, missing prior-cycle threshold stop, incomplete negative paths, and a timer-retrigger race during stop. The latest correction requires isolated runtime at every non-canonical location, verifies runtime copies, fails on prior threshold breach, disables/verifies triggers before main-service/cgroup stop, and adds 24 total executable controls. It requires closure review.

Final authority review `dispatch-1785093118453` and runtime review `dispatch-1785093118453-1` both returned `READY` for `f36547935826bbf8f4597f928b545127cff10003`. Controlling synthesis is tracked at `cc6c029`; AK reports Decision `83` `ready_for_adr` and ADR-recorded readiness.

## Decision 83 operational result and bounded correction

The human accepted Decision `83` through receipt `9173`, installed commit `4af9ee03346de33f62ae95381a3c2900d9560c8a`, and activated it through receipt `9189`. Two hourly service invocations failed closed before creating a run directory or model worker because AK's SQLite WAL reader required writable private `-shm` state while the service exposed only the live DB file as read-only. No model API call occurred. The direct-human stop is receipt `9201`; the activation file is `human_stopped`, all four units are inactive, both timers are disabled, and zero run directories exist.

The accepted start/stop scripts also used noncanonical MITO token `Operations`; activation and stop required a temporary direct-human compatibility shim to translate it to AK's canonical `Operations & Evaluation`. The stop path initially treated systemd's historical `failed` state as a live process even with an empty cgroup; the human reset that state and completed the governed stop.

The inactive Decision `86` correction:

- uses canonical `Operations & Evaluation` directly in start and stop receipts;
- resets historical failed service state before verifying an empty cgroup and inactive service;
- preserves and archives the stopped predecessor activation before a separately accepted successor starts;
- byte-copies a hash-stable source DB+WAL pair into private writable `StateDirectory`, validates its SQLite catalog, and points AK only at that snapshot;
- continues hashing the live source DB and checking all watched Git state before the model call and after it;
- refreshes the private AK snapshot immediately before the pre-model authority gate and after the worker;
- passed a real transient-systemd `ProtectSystem=strict`/`ProtectHome=tmpfs` probe in which AK read Decision `83` successfully from the private snapshot.

Decision `86` is separate corrective authority. It does not reopen, rewrite, or continue Decision `83`'s stopped activation window.

## Not yet proved

- Decision `86` has no corrective `ready_for_adr` review closure, acceptance receipt, installation, activation, or model-call authority yet;
- the private WAL-snapshot path has real sandbox/AK read proof but not an accepted production canary cycle;
- no canary output usefulness, provider cost, successful hourly recurrence, or complete 24-hour window has been observed;
- Decision `83` remains immutable accepted-and-stopped history under receipts `9173`, `9189`, and `9201`.

Passing tests, sandbox probes, fixtures, and prompt preview are implementation proofs only, not operational successor-canary proof.
