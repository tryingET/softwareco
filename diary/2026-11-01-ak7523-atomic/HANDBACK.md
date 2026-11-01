# AK7523 — bounded parent handback

Corrected after independent inspection found invalid-threshold false greens in the initial
22-test patch. The corrected source passes 27 synthetic tests; awaiting parent inspection and
commit. Controller/claim details were supplied by dispatch, not changed or queried here.

## Exact touched paths (relative to `/home/tryinget/ai-society/softwareco`)

- `scripts/ubs-adoption-canary.py`
- `tests/test_ubs_adoption_canary.py`
- `docs/project/2026-10-07-ubs-service-adoption-gate.md`
- `diary/2026-11-01-ak7523-atomic/HANDBACK.md`
- `diary/2026-11-01-ak7523-atomic/red.log`
- `diary/2026-11-01-ak7523-atomic/green.log`
- `diary/2026-11-01-ak7523-atomic/green-final.log`
- `diary/2026-11-01-ak7523-atomic/final-checks.log`
- `diary/2026-11-01-ak7523-atomic/source-test.diff`
- `diary/2026-11-01-ak7523-atomic/runbook.diff`
- `diary/2026-11-01-ak7523-atomic/threshold-red.log`
- `diary/2026-11-01-ak7523-atomic/threshold-green.log`
- `diary/2026-11-01-ak7523-atomic/threshold-final-checks.log`
- `diary/2026-11-01-ak7523-atomic/source-test-v2.diff`
- `diary/2026-11-01-ak7523-atomic/runbook-v2.diff`

The `*-v2.diff` receipts contain the exact current source/test and runbook Git diffs.
`threshold-final-checks.log` contains current hashes, diff statistics, status custody, and an
empty scoped staged-file listing. Earlier diffs/checks and all RED/GREEN logs are retained
unchanged as historical evidence. Initially the three allowed tracked files were clean.
Unrelated dirty paths were observed only through Git status and were not touched.

## Implemented behavior

- Nonzero `git ls-files` status raises a setup error with repo, exit status and stderr;
  even plausible partial stdout cannot become a successful scan selection.
- Empty language selection, nonpositive file caps, and zero executed pairs exit 2.
  Empty individual repo/language pairs remain skippable if another pair actually runs.
- OS setup errors, including scratch creation, staging and scanner launch failures,
  produce diagnostics and exit 2 instead of a traceback or successful verdict.
  Missing optional hooks/ignore files and already-deleted tracked files remain expected.
- Requested reports are marked non-success before setup. Handled setup failures record
  `setup_error`, the error, and available partial results. A candidate launch failure
  retains its already-run incumbent result; later listing failures retain earlier pairs.
- `executed_pairs` counts both returned invocations, including timeouts; it is not a
  completeness or exhaustive-coverage claim. `judge()` and valid-argument comparison policy
  are unchanged. Selected files disappearing during staging fail rather than silently skip.
- Threshold parsing now happens inside handled setup: timeout and max-slowdown must be finite
  and positive; floor must be finite and nonnegative. Invalid text, NaN, infinities and
  overflow-to-infinity values exit 2 before any scanner launch. Unchecked inputs stay text
  in reports; checked inputs become numeric, keeping error reports standard JSON.

## Actual execution

All test-suite runs used this exact command from the company repo (publication-failure tests
invoke `main()` in-process with targeted I/O injection, still using executable scanner stubs):

```bash
TMPDIR=/home/tryinget/.local/state/pi-quests/tmp PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_ubs_adoption_canary.py -v
```

- `red.log`: source diff checked clean (exit 0) before the production edit; 20 tests
  ran in 8.916 s, exit 1, with 17 failures (including subtests) and 1 error. The
  original eight scenarios passed. Logs show actual old `verdict: pass` on empty
  selections/zero scans and failed listings, and stale old pass reports.
- `green.log`: patched source, same 20 tests, 8.011 s, exit 0; scoped diff check exit 0.
- `green-final.log`: two additional report-I/O scenarios added after that first green;
  22 tests, 9.936 s, exit 0. These two additional checks have no pre-patch red claim.
- `final-checks.log`: initial `git diff --check` on all three tracked touched paths, exit 0.
- `threshold-red.log`: before the threshold production change, source SHA-256 matched the
  initial handback (`3c8d8f8352f087f788b0d352e65b61c8c836b9039b7228f693c4ba0d65d096a9`).
  27 tests ran in 9.775 s, exit 1: 20 failed threshold subtests and 9 strict-JSON errors.
  Actual false-green stdout for timeout 0/-1 and max-slowdown NaN is recorded. Malformed
  numeric text also demonstrably left a stale pass; nonfinite timeouts could traceback.
- `threshold-green.log`: same 27 tests after correction, 9.793 s, exit 0.
- Both injected final-publication tests already passed in `threshold-red.log` and still pass
  afterward: recovery preserves actual results in a setup-error report; failed recovery
  removes the unusable report and diagnoses both failures. No production fix or pre-patch
  RED is claimed for these two existing-positive branches.
- `threshold-final-checks.log`: current scoped `git diff --check`, exit 0; no staged files.

## Independent findings and disposition

| Finding | Bounded correction / evidence |
| --- | --- |
| Timeout 0/-1 could pass with unfinished scans | Reject nonpositive/nonfinite timeout before scans; 7 invalid-timeout subtests now exit 2, current non-pass report, zero calls. |
| NaN/infinite/nonpositive slowdown invalidated the ratio check | Finite positive slowdown guard; 7 invalid-slowdown subtests now exit 2 without calls. Valid slowdown policy and `judge()` unchanged. |
| Negative/nonfinite floor was unchecked | Finite nonnegative floor guard; 6 invalid-floor subtests now exit 2. Legitimate floor 0 still runs and refuses the deliberately slower stub under the existing ratio. |
| Error reports serialized NaN/Infinity as nonstandard numbers | Parse raw strings during guarded setup; 9 strict-JSON nonfinite-input subtests now pass. Invalid numeric text also gets a fresh error report instead of preserving an old pass. |
| Optional final-publication recovery coverage absent | Added both write-then-close failure regressions; both were green before the threshold edit, with no source recovery change. |

### Current SHA-256 summary

- `scripts/ubs-adoption-canary.py`: `853155f84030fea67ac0bf38d912f71d03ef5ac42058e604e221fb02955c2cd5`
- `tests/test_ubs_adoption_canary.py`: `c9a12e94ca9097a840479df14914b270ae9643cc3ab4743d49eb2343865d5bfa`
- `docs/project/2026-10-07-ubs-service-adoption-gate.md`: `add8221b60721e4487f8863f77f065b61509017045a75c6d47ac0dff30a4cd5f`

Coverage includes discovered-repo Git failure with partial stdout, explicit nonrepo,
absent selected-language files, empty selections, zero/negative caps, stale reports
across setup errors, mixed empty/nonempty pairs, scratch/staging/launch OS failures,
partial-result retention, unusable report paths, original comparison scenarios and
consumer immutability. A new incumbent-timeout test explicitly preserves the existing
non-refusal behavior; it is not an endorsement of that policy.

## Limits and parent actions

- Only lightweight synthetic Git fixtures and executable scanner stubs were used,
  with temporary fixtures under the supplied TMPDIR. Fixture Git initialization,
  staging and commits are part of the pre-existing test harness; no company or child
  repository staging/commits were performed.
- No real scanner/adoption run, installation, heavy job, hook/pin/budget/policy/private
  data change, child-repo mutation, or AK lifecycle write occurred.
- Root README's broad `scripts/check-template-ci.sh` contract was identified but not
  run under this dispatch's synthetic-only constraint. Root `docs/engineering.local.md`
  and `policy/engineering-lane.json` were absent. No company-wide all-green claim.
- AK7524/AK7525 incumbent-incomplete/comparison behavior remains unchanged and explicitly
  documented/tested. The independent threshold findings were repaired here, not deferred.
  No additional in-scope defect is known from the corrected synthetic checks.
- Threshold numeric-text errors are now handled setup errors with current reports. Report
  handling still begins after argparse accepts the CLI shape: missing/unknown options and
  unrelated argument-type errors remain usage errors with no current-report promise.
- If storage prevents both writing and removing an existing report, it cannot be
  physically invalidated: exit 2 and an explicit NOT-current warning are authoritative.
  That failure path was tested with an unusable directory report fixture, not a real
  read-only mount. Final-publication/recovery close failures were injected after actual
  report writes. Abrupt termination, concurrent report writers, and real filesystem
  permission/race conditions were not exercised.
- Parent must independently inspect the supplied diffs/tests and perform any authorized
  commit or subsequent validation. No lifecycle closeout or adoption is claimed here.
