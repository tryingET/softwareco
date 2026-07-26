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
- Python compilation and ten deterministic unit tests passed.
- Two fixture cycles used distinct process IDs, produced noncanonical proposal-only outputs, and passed strict validation.
- Production cycle invocation without activation refused with exit `3`.
- Rendered service, hourly timer, expiry service, and 24-hour timer passed `systemd-analyze --user verify`. The command also reported an unrelated pre-existing warning from `school-asr-recorder.service`.

## Review correction

The first transcendent-loop implementation phase timed out and was not accepted as completed behavior. Independent review identified three blocking defects in that partial candidate:

1. mutable checkout code was not bound to the accepted commit;
2. the timer repeated indefinitely rather than ending after 24 hours;
3. the worker exposed too much host state and extension surface.

The corrected candidate uses a commit-addressed blob bundle and per-cycle digest/readback, exact 24-hour/cycle bounds with a stop timer and runtime refusal, and a tool-free worker with all extensions disabled except the pinned Pi Modes package. Remaining claims require fresh review of the corrected version.

## Not yet proved

- no AK architecture decision exists for this candidate yet;
- no direct-human acceptance or activation receipt exists;
- no bundle or user unit has been installed;
- no service/timer has been enabled or started;
- no production model cycle or 24-hour canary has run;
- no canary output usefulness, cost, reliability, or complete-window behavior has been observed;
- no authority/security and runtime/operator review of the corrected candidate has closed.

Passing fixtures and prompt preview are implementation proofs only, not operational canary proof.
