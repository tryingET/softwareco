---
summary: "AK6804: before re-pinning the UBS service worktree that every repo's pre-commit runs, time the candidate against the incumbent on each consumer repo's real JS/TS and Python with scripts/ubs-adoption-canary.py, and refuse it on a timeout, a partial scan or a large slowdown; then roll out to one repo before all."
read_when:
  - "You re-pin or rebuild contrib/ultimate_bug_scanner-local (a UBS upgrade or a new local adoption)."
  - "A pre-commit suddenly reports `partial: js timeout` across repos after a UBS change."
type: "reference"
status: "implemented"
date: "2026-10-07"
governance_task_id: 6804
---

# UBS service adoption gate (AK6804)

## Why

`contrib/ultimate_bug_scanner-local` (branch `local`) is the scanner behind
`scripts/ubs-staged.sh`, which every softwareco repo's pre-commit runs, and behind the
workstation's quality gate. A re-pin changes all of them at once. On 2026-10-06 05:22 the pin
moved to UBS 5.4.18 (AK6424) after its own suite and refusal-count checks. Within hours its
taint_js livelocked on ordinary find-first loops, and commits in workstation (AK6750) and
test-capabilities (AK6781) were refused as `partial: js timeout`. Each refused attempt cost about
15 minutes of CPU, and the workarounds (a partial-scan override, split commits) weakened the gate.
Nothing in the adoption measured whether the candidate still finishes on our own files.

## The gate

```bash
# from ~/ai-society/softwareco, with the candidate checked out somewhere other than the service worktree
python3 scripts/ubs-adoption-canary.py --candidate /path/to/candidate/ubs --report "$TMPDIR/ubs-canary.json"
```

- Consumers are discovered, not listed: every Git repo under `~/ai-society` whose pre-commit hook
  (or `scripts/quality-gate.sh`) runs `ubs-staged` or the service worktree. `--repo` scans named
  repos instead.
- Per repo and language (`js`, `python`), the tracked files are copied to scratch and scanned as one
  batch, so imports between them count (AK6781's hang needed both files of a pair). Over
  `--max-files` (400) the largest files are kept. Consumer repos are never written.
- The incumbent defaults to the service worktree's `ubs`. Both builds run
  `ubs --ci --no-cargo --only=<lang> --format=json .` with caching off.
- **Refuse** (exit 1) when, where the incumbent finished, the candidate does not finish within
  `--timeout` (300 s, the pre-commit module timeout); or reports a partial scan or failed modules;
  or is more than `--max-slowdown` (5) times slower, ignoring scans under `--floor` (2 s).
- **Report, not refuse**: criticals the candidate no longer finds. Findings change across releases,
  but a solver that stops early also loses findings, which 5.4.18 did.
- Exit 0 pass, 2 usage or setup error. Empty `--langs`, nonpositive `--max-files`, failed Git
  listings (including explicit non-repos), and zero executed repo/language pairs are setup
  errors, never passes. Individual pairs without matching tracked files are skipped; at least
  one pair must actually run both scanner invocations.
- `--timeout` and `--max-slowdown` must be finite and positive; `--floor` must be finite
  and nonnegative (zero remains supported). Invalid numeric text, NaN, infinity and
  overflow-to-infinity values are setup errors before any scanner launch. In reports,
  unchecked/rejected threshold inputs remain JSON strings; checked values are numbers,
  so NaN/infinity inputs cannot produce nonstandard JSON numeric constants.
- After argument parsing, a requested JSON report is invalidated before setup. Handled setup
  errors write `verdict: setup_error` and an `error` diagnostic, retaining any actual scan
  results, including an incumbent result if candidate launch failed. If reporting fails, the
  canary attempts to remove the unusable report; if that also fails, stderr explicitly warns
  that any existing report is **not current**. Exit 2 remains authoritative.
- The report's `executed_pairs` counts pairs for which both invocations returned a result
  (including timeouts), not successful or exhaustive coverage. On setup errors, `scans` may
  include a partially executed pair with only the available result. Comparison policy is
  unchanged: an incumbent timeout does not itself refuse adoption (AK7524/AK7525); a pass
  is not proof that every scan completed.

Run it before step "move `local`" of the rebuild recipe (contrib-upstream skill,
`references/repos.md`, ultimate_bug_scanner) and record the report path in the adoption task.

## Staged rollout

The gate catches what our files reveal in a single run. A second line of defence is to let one
repo carry a new pin for a day before all repos do: run the candidate from a second linked
worktree and point a single repo's hook at it with `UBS_BIN` (both `ubs-staged.sh` and the
workstation gate honour it). Only then fast-forward the service worktree. This is a
recommendation; no hook was changed for it.

## Verification

- `tests/test_ubs_adoption_canary.py`, Given/When/Then: 8 scenarios (pass; refuse on slowdown,
  timeout, partial scan; floor; dropped criticals reported; discovery; consumer repos untouched).
  Red before the script existed (8 of 8), green after. Mutation checks: 7 of 7 killed (timeout,
  partial, floor, service-worktree marker, in-place scan, dropped-count, exit code).
- Replay of AK6424's real adoption (incumbent: the pre-5.4.18 local 7f618756, candidate: 5.4.18
  ac2ebf35) on test-capabilities and workstation: **refuse**, exit 1. test-capabilities/js (185
  files) 21.7 s against more than 300 s, and workstation/js (4 files) 1.2 s against more than
  300 s did not finish; both Python scans finished (workstation/python: 3 criticals the candidate
  no longer reports, listed). The gate would have stopped the 5.4.18 pin.
- The same kind of run is the admission check for AK6809 (adopting v5.4.19, which finishes the
  large tippio and ts-quality files the live build cannot).
- AK7523 (2026-11-01): fail-closed setup regression checks use executable scanner stubs and
  synthetic Git repos under `$TMPDIR`, not real consumer scans. Actual pre-patch run: 20 tests,
  exit 1 (17 failed assertions/subtests, 1 error); patched run: 20 tests, exit 0. Two additional
  report-I/O checks brought the first handback run to 22 tests, exit 0, retaining the original eight.
  Commands and logs: `diary/2026-11-01-ak7523-atomic/{red,green,green-final}.log`.
  Independent inspection then found invalid-threshold false greens. The corrective run
  (`threshold-red.log`) exercised 27 tests before changing threshold handling: exit 1,
  20 failed subtests and 9 strict-JSON errors. After the fix, the same 27 tests passed
  (`threshold-green.log`, exit 0). Two final-publication write/close recovery checks
  already passed before this correction and remain regression coverage, not new fixes.
  These checks do not establish real scanner adoption or company-wide conformance.
