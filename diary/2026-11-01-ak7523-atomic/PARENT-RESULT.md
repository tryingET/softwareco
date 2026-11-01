# AK7523 — parent verification and bounded acceptance

## Resolved findings

- Nonzero Git listing, including plausible partial stdout, is a setup error rather than an empty successful selection.
- Empty language selection, nonpositive file caps and zero executed pairs cannot report pass.
- Handled setup/staging/scanner-launch/report failures produce exit2, non-success reporting and retained available diagnostics rather than a stale green report.
- Independent inspection additionally reproduced false green from timeout0/-1 and NaN slowdown. Timeout/slowdown must now be finite and positive; floor must be finite and nonnegative. Valid zero floor/scientific notation and the original comparison policy remain unchanged. Error reports are standard JSON even for rejected NaN/Infinity arguments.
- Final-publication recovery/removal behavior has explicit regression tests; that behavior already worked before the numeric fix and is not falsely described as a newly repaired defect.

## Actual evidence

Implementation handback: `HANDBACK.md`, source/test/runbook diffs and retained RED/GREEN logs.

- Original setup repair: actual20 tests RED, then GREEN; additional report checks gave22 GREEN.
- Numeric follow-up: actual27 test methods RED with20 failed subtests and9 strict-JSON errors; the same27 then GREEN.
- Independent reviewer `dispatch-1793508326162` reran27 GREEN and independently retested signed zero/underflow, mixed invalid thresholds, launch suppression, strict JSON and publication-recovery outcomes. No remaining in-scope blocker.
- Parent normal heavy-job admission ran an isolated local Git clone of the company HEAD plus exactly the three changed source/test/runbook files. `parent-source.sha256` and before/after custody checks bind those inputs.
- `parent-template-ci.txt`: declared template CI PASSED, offline, including its explicitly expected unmaterialized-ontology refusal and generated disposable template tests. This is not a successful validation/build of the live primary ontology.
- `parent-canary-tests.txt`: parent independently reran27 synthetic tests, PASSED.
- `parent-validation-status.txt`: template_ci0/canary_tests0/custody0. Managed scratch removed after actual success. The primary governance/task-scope/ontology outputs were not used as a mutable CI sandbox.

## Preserved boundaries

`judge()` and valid-argument scan/comparison policy remain unchanged, as confirmed independently by AST comparison. Both real invocations returning timeout results count as an executed pair, NOT completed source coverage. A valid positive timeout can still leave both scans unfinished under the existing comparative policy; that is explicitly not complete-coverage/adoption clearance.

AK7524 owns the broader full-suite environment limitations; AK7525 owns incomplete comparative coverage/performance and its unqualified candidate. Their existing obligations remain open before any full-green/adoption claim. No real consumer scan, scanner installation/repin/adoption, hook/budget/policy relaxation, GitHub action, private-data access or child-repo mutation occurred.

Publication and ownership/source changes outside these three files were neither staged nor reconciled by this task. Exact commit and actual normal hook/post-commit results are to be recorded in AK after they occur. This file does not self-certify a future commit.
