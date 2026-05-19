---
summary: "Deterministic Ghostty launcher for opening one Pi terminal per AK task with a pre-submitted `pi -p` prompt."
read_when:
  - "You want to open one new terminal per AK task and start Pi already running the task-specific prompt."
  - "You are deciding whether to use a Ghostty/niri prompt-template workflow or a deterministic script for batch AK task launches."
  - "You are launching the standardized Justfile rollout pilot tasks in parallel."
---

# Ghostty AK task launcher

## Why this exists

For batch repo/task execution, a deterministic script is better than a prompt-template-driven text-injection workflow.

Why:
- `pi -p` can submit the task prompt directly without editor typing or `wtype`
- batch launching multiple repo/task terminals is easier to script than to drive via an interactive skill
- the script can resolve repo paths from AK task ids directly
- Ghostty can still be used as the terminal surface, with optional `niri` focus for the last-launched window

## Canonical launcher

```bash
./scripts/launch-pi-ak-task-ghostty.sh <task-id>...
```

Current convenience preset for the standardized Justfile rollout pilot wave:

```bash
./scripts/launch-pi-ak-task-ghostty.sh --justfile-rollout-pilots
```

Optional flags:

```bash
./scripts/launch-pi-ak-task-ghostty.sh --dry-run --justfile-rollout-pilots
./scripts/launch-pi-ak-task-ghostty.sh --focus-last 609 610 611
./scripts/launch-pi-ak-task-ghostty.sh --interactive 610
./scripts/launch-pi-ak-task-ghostty.sh --print --hold-open 609
./scripts/launch-pi-ak-task-ghostty.sh --log-dir /tmp/pi-launch-logs 609
```

## Prompt injected per task

For each task id `<N>`, the launcher starts Pi with this initial prompt:

```text
read next_session_prompt.md and attend next ak task #<N> and then proceed with the workflow until completed and commited.
```

The task number is derived from the actual AK task id being launched.

Launch mode defaults:
- single-task launch -> interactive `pi "<prompt>"`
- multi-task launch -> non-interactive `pi -p "<prompt>"`

You can override that with `--interactive` or `--print`.

## Dependencies

Required:
- `ghostty`
- `pi`
- `python3`
- AK wrapper at `~/ai-society/softwareco/owned/agent-kernel/scripts/ak.sh`

Optional:
- `niri` for best-effort focus of the last-launched window when `--focus-last` is used

Current focus strategy:
1. try the unique Ghostty class/app id used at launch
2. if Ghostty/niri do not expose that identity cleanly, fall back to matching the final repo basename against the terminal title (for example `π - dspx`)

Current observability behavior:
- print-mode launches write per-task stdout/stderr logs under `~/.pi/agent/ghostty-ak-task-launches/<timestamp>/` by default
- single-task launches default to interactive Pi so the operator can watch the live session directly
- interactive launches now also keep the launcher shell open after Pi exits and print the interactive exit status, so startup failures do not vanish with the terminal
- single-task print-mode launches hold the shell open after `pi -p` exits unless `--no-hold-open` is passed
- multi-task print-mode launches close on success by default, but still keep per-task logs
- non-zero print-mode exits keep the shell open so failures remain inspectable

## Scope

This launcher is intentionally narrow:
- one Ghostty window per AK task
- repo path resolved from AK task truth
- prompt passed directly to `pi -p`

It does **not** replace the richer Ghostty/niri text-injection procedure for workflows that must leave text in the Pi editor unsent.
For this batch task-launch case, direct `pi -p` is the lower-drift surface.
