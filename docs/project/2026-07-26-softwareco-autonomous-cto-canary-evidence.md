---
summary: "Inactive implementation evidence for the autonomous CTO canary candidate."
read_when:
  - "Reviewing what has and has not been proved before canary acceptance."
type: "evidence"
status: "candidate_inactive_evidence"
date: "2026-07-26"
task_id: 4284
decision_id: 83
---

# Autonomous CTO canary candidate evidence

## Observed implementation facts

- Pi `0.80.10` exposes native `--system-prompt <text>` and repeatable `--append-system-prompt <text>` flags.
- Installed `@tryinget/pi-modes` `0.3.0` supports `replace_base`, which replaces the static base and retains the dynamic host envelope.
- Candidate mode and preset lint successfully.
- A fresh trusted-root no-session RPC process, with all extensions disabled except the pinned Pi Modes entrypoint, selected `softwareco-cto-canary` as role `base`, strategy `replace_base`, with no overlay and no diagnostics.
- `/mode-preview --json` contained the exact canary prompt plus global/workspace/Softwareco AGENTS context, current date, and cwd.
- Python compilation and twenty-three deterministic unit tests passed, including path-escape, prompt-source/fingerprint, expiry, home-hiding, in-flight stop, and scoped-installer controls.
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

## Not yet proved

- AK Decision `83` exists but remains `review_pending`; it grants no operational authority;
- no direct-human acceptance or activation receipt exists;
- no bundle or user unit has been installed;
- no service/timer has been enabled or started;
- no production model cycle or 24-hour canary has run;
- no canary output usefulness, cost, reliability, or complete-window behavior has been observed;
- three authority/security attempts and two runtime/operator attempts required revision; no review of the latest correction commit has closed.

Passing fixtures and prompt preview are implementation proofs only, not operational canary proof.
