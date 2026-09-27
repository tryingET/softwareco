---
summary: "Task5481 source/test landing receipt: fail-closed legacy gate and bounded checks, with unresolved producer identity/compatibility and no live effects."
read_when:
  - "Attaching canonical task5481 evidence or resuming the exact producer integration gap."
type: evidence
---

# Decision151 lane receipt — task5481

## Observed source execution

Canonical repo: `/home/tryinget/ai-society/softwareco/owned`; starting main HEAD
`5f02859` and landing commit:

`a9891357e31d9f5fbafe1b85d7c2d8c0631cfc6c`
— `fix: refuse legacy task launches pending domain classification`

Eight exact files committed: launcher, scoped synthetic test, Justfile, scoped
check wrapper, README, legacy launcher doc, lane implementation evidence and
positive-custody/reinstatement runbook. No child repo or canonical AK state was
mutated. Parent owns claim/evidence/task closeout; this receipt is not AK state.

Before staging: asserted branch `main`, expected starting HEAD, empty index and
unchanged forbidden-file diff. After staging: compared sorted staged paths to
the exact eight-file allowlist and ran `git diff --cached --check`. After commit:
asserted branch `main`, empty index and unchanged forbidden-file diff again.
`Justfile` required `git add -f` because existing `.gitignore:3:*` ignores it;
no ignore-policy edit was made. Commit hooks were absent (sample files only,
no configured alternate hook path); no hook/trigger configuration was changed.

The pre-existing dirty files remain `AGENTS.md` and
`docs/project/repo-capability-map.md`. SHA256 of their combined `git diff --`
bytes before and after landing:

`d405446efbf8cd313a2b82ea203ecc7a4eec23041958d62a4e8e23b583528033`

Receipt commit: `790fd657fdedd50bdb6e6af92f252afde1fa99c7`.
The post-receipt raw diff-hash assertion initially failed: Git's automatic index
abbreviation grew from seven to eight characters after the commit. This was a
serialization change, not forbidden-file mutation. Repeating with explicit
`git diff --abbrev=7 -- AGENTS.md docs/project/repo-capability-map.md` reproduces
the original `d405446e…` hash exactly. Stable `--full-index` diff SHA256 is
`a16656ae633d840a7dd54dc3219bdb0c33594cce5125fcd687f6c401c8f8d905`.
Final assertions use explicit abbreviation/full-index, not Git's auto width.
No forbidden file was edited, staged or restored to repair this evidence check.

Source SHA256 at landing:

| File | SHA256 |
|---|---|
| `scripts/launch-pi-ak-task-ghostty.sh` | `38e235583ec678b3d4b48384b7eda61f45cfcd104ce791a397109faeae109ee1` |
| `tests/test_ghostty_task_session.py` | `1f3cbae6c2fab0ea0d3919004f3e4be5a7c225099d5379b39bb39b39179ede8e` |

## Exact verification and one test-harness repair

- Initial direct command:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p '*task_session*.py' -v`.
  **Failed** in three subcases: help and no-args reached existing `cat` usage,
  but the deliberately isolated PATH omitted `cat`. Return 127 was not expected
  0/2. No live runtime or classifier call occurred. Repaired the test harness by
  adding a symlink to the system text utility; no launcher fallback was added.
- `just doctor`: **passed**, local bash/python3/git/just and owned TMPDIR only.
- `just check`: **passed**, including immediately before commit (four test methods,
  47 launcher subprocess invocations across subcases; unittest reported 0.096s).
  Static dimensions: Bash syntax, Python AST and scoped Git whitespace. Dynamic
  dimension: the actual launcher process with scrubbed environment and synthetic
  executable runtime dependencies. Each dimension runs once.
- `just help`: **passed**, bounded surface listed.
- `just --dry-run check`: inspected; lint and tests each once.
- `just --dry-run ci`: inspected; reaches only explicit blocked wrapper.
- `just ci`: **expected refusal, exit 2**. Printed that full lane CI reaches
  network/AK/ROCS and is not authorized. This is a verified blocker, **not a
  passing CI-equivalent gate**.
- `git diff --check` and `git diff --cached --check`: **passed**.

Synthetic tests allocate only fresh `lane-task-session-*` directories under
owned TMPDIR; the test context removes its own inactive scratch after each case.
Runtime-bearing stubs record calls but never execute the Ghostty shell payload,
AK or Pi. Refusal assertions require zero recorded calls and no log/.pi creation.
No real terminal/provider/AK/namespace/config/account/fleet probe, install,
enrollment, trigger suspension, claim/effect recovery or fork retry was run.

## What the tests actually establish

- Standalone `--help` and `-h` remain effect-free.
- Entire valid-looking requests, including batches and the expanded 609–615
  preset, refuse at the pending classifier gate before dependencies, mkdir/date,
  AK resolution, terminal/Pi launch or niri focus. Dry-run and mode/log/focus
  options do not bypass it. Maximum 256-task and safe-integer boundaries covered.
- Invalid IDs (including command-shaped/newline/oversized data), repeated tasks,
  unknown options, conflicting/repeated mode/hold/focus/log/dry-run/preset options,
  missing/empty log arguments and help mixed with tasks refuse before effects.
- Runtime/HOME-XDG-related test environment changes and unavailable AK/Pi/Ghostty
  dependencies cannot cause fallback or move refusal after those effects.

**Not established:** positive-outside legacy compatibility, actual emitted
classifier integration, real Ghostty shell execution, installed identity,
producer negative/fault behavior, positive custody or stakeholder-use canaries.
Universal refusal is intentionally incomplete integration, not the accepted
replacement operation or a completed task5481 compatibility claim.

## Producer checkpoint and exact remaining seam

Read the required accepted ADR and both canonical plans in pi-extensions. ADR
SHA256 `6db4ce80dca8ec2d8cec296ddb14a11f32f09db1d976d874ad53f6375609dd35`;
implementation plan `a6b5f57910dda5dacfbe644e735759f2221f6472d963b3abddc64b26338f6c2e`;
validation plan `d8af4ac978b2e283d6f5f6a54a668bf8db65736f8474bca981edbe3f8f0883c4`.

Task5480's explicitly named ordinary main producer worktree was read only:
`/home/tryinget/.local/state/pi-quests/tmp/decision151-main.5gPphB/pi-extensions`.
Latest observed producer commit remained `3b633e03e` (planned interface publication)
at source landing. Mutable classify/json/state sources appeared during this work;
the source list still had no CLI at the last checkpoint. The published document
explicitly labels the interface planned, not implemented/installed.

The published `pi-task-session classify` request requires canonical `akInstance`.
Existing lane callers only supply task IDs/cwd. The producer locator inspected
has no instance field and no supported DB-free instance-discovery operation is
published. Guessing a value, reading ordinary AK, creating lane configuration or
inventing another command would violate this task. The lane therefore contains
no speculative executable consumer and no opt-out.

Smallest continuation: task5480 supplies exact actual emitted classifier/fixtures,
immutable artifact identity, response/digest validation rules and the supported
DB-free canonical-instance binding for this legacy caller. Then replace only
`classify_legacy_request` with the actual consumer and add mixed enrolled/unknown,
malformed/incompatible producer and positive-outside compatibility tests. Existing
scope covers that follow-up; no policy/AGENTS/capability-map edit is needed.
Do not claim source-stub compatibility proves installed identity or custody.

The [implementation evidence](../docs/project/2026-09-07-visible-task-session-lane-implementation.md)
and [custody/reinstatement runbook](../docs/project/2026-09-07-visible-task-session-lane-custody.md)
name the remaining producer, install, positive owner-custody and safe retirement
proofs. No domain is nominated/certified. Full repository CI remains separately
authorized, and task completion remains with the parent rather than this receipt.
