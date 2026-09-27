---
summary: "Task5481 continuation: actual installed-identity consumer and positive-outside emitted-classifier proof, exact commits/tests, and unverified live gates."
read_when:
  - "Attaching task5481 continuation evidence or assessing remaining rollout obligations."
type: evidence
---

# Decision151 lane classifier continuation — task5481

## Execution and exact landing

Parent continued the same claimed task; no claim reset or AK call occurred.
Canonical source remained `softwareco/owned`, branch `main`, starting
`80af9ae9d619ed4d45f9b6955a406aa42c17c128`.

Implementation commit:

`fbb39c1eedd3be93b8083106439aefa2c7bbd935`
— `feat: integrate account-bound legacy task classification`

Eight exact files: launcher, README, legacy launcher doc, lane implementation
evidence, original refusal tests, compatibility tests, emitted-body tests and
protocol tests. Main/expected-HEAD/empty-index assertions preceded staging;
sorted staged paths matched the exact allowlist; cached whitespace checks passed.
After commit the index was empty and forbidden-file preservation passed.
No scope expansion, child-repo mutation, branch change or Justfile semantics
change was needed. The launcher remains below the 500-line budget (482 lines).

Launcher SHA256:
`77ad865cf95a980cbf6e9d7b7462e040081de0751a8095061f097356c258c901`.

The original dirty `AGENTS.md` and `docs/project/repo-capability-map.md` were not
edited, staged, committed or restored. Stable full-index diff SHA256 before and
after continuation landing:
`a16656ae633d840a7dd54dc3219bdb0c33594cce5125fcd687f6c401c8f8d905`.

## Producer consumed, not guessed

The initial updated memo described implemented v1 plus 63 producer tests/pack,
but lacked canonical-instance binding. While waiting, the lane implemented
strict request/response validation and bounded producer pipes, with pure tests.
The producer then published actual source/emitted installed identity at:

`6b90412bc8a848cf72e89419f6dc71cf9e9f6b87`
— `feat: expose account-bound DB-free task-session identity for lane5481`

Explicitly named producer source:
`/home/tryinget/.local/state/pi-quests/tmp/decision151-main.5gPphB/pi-extensions`.
Read its updated implementation memo and actual source/emitted CLI/core plus
installed-identity/classify/state/json/native closure. No public account locator,
provider, AK or installed Pi command was executed during that inspection.

Consumer uses exactly `pi-task-session identity`, then `classify-installed` with
all task IDs and physical cwd. No AK-instance flag/value/registry is invented.
Exact schemas/package/version/interface are checked; descriptor identityDigest,
classification requestDigest, identityDigest and namespace metadata are validated.
Descriptor drift refuses instead of trusting cached outside or retrying.

The producer's positive canonical binding is a projection of one complete,
non-withdrawn existing inventory containing exactly one AK instance. This closes
the previous **source integration** gap. It does not certify installation,
account configuration, native AK startup or live custody.

## Actual checks and outcomes

Observed tool versions: Node `v26.8.1`, Python `3.14.7` on this Linux workstation.

```bash
# Canonical lane root; owned TMPDIR inherited.
TASK_SESSION_PRODUCER_DIST=/home/tryinget/.local/state/pi-quests/tmp/decision151-main.5gPphB/pi-extensions/packages/pi-little-helpers/dist/task-session just check
just doctor
just --dry-run check
just --dry-run ci
just ci
```

- Explicit emitted-path `just check`: **23 passed, zero failed/skipped**, including
  immediately before commit (12.799s). Shell syntax, embedded Python compilation
  through tests, Python AST and scoped whitespace dimensions passed.
- Default `just check` without emitted path: **19 passed, four visibly skipped**.
  Those four require explicit reviewed emitted artifacts; no silent fallback.
- `just doctor`: passed, local test tools and owned scratch only.
- Dry-run `check`: lint and tests once each. Dry-run `ci`: only blocked wrapper.
- `just ci`: **expected exit 2**, not green CI; no runtime-bearing historical
  network/AK/task-scope/ROCS profile was invoked.
- `git diff --check` / `git diff --cached --check`: passed.

### Coverage actually exercised

1. Complete parser/batch/preset refusal, standalone DB-free help, no dependency
   fallback and no checkout/PYTHONPATH/sitecustomize import or bytecode creation.
2. Exact descriptor/result shape and digest binding, unknown versions/fields,
   duplicate nested keys, invalid UTF-8/BOM/numbers/trailing JSON, null namespace,
   unknown/enrolled results, conflicting identities and generation/digest drift.
3. Producer output/input bounds and nonzero/malformed/oversized output, plus real
   owned stub deadlines both with blocked stdin and closed stdout followed by
   non-exit. Only these freshly created classifier children were terminated.
4. Positive-outside legacy compatibility: interactive/print defaults and
   overrides, single/batch/preset dry-run, log directory/paths, hold-open options,
   unchanged task prompt and AK show argv. Synthetic Ghostty receives the actual
   legacy shell argv/environment; synthetic niri verifies focus arguments.
   The Ghostty shell payload and real Pi are **not executed**.
5. Four tests through hash-pinned actual emitted producer functions: positive
   outside single/batch/preset; mixed enrolled and missing task inventory;
   task-only/common-Git/overlap/shared-effect/unresolved-attempt conflicts;
   withdrawn/incomplete/mixed-instance/physical-identity uncertainty. Actual
   JavaScript canonical digests are validated by the Python consumer. Ambient
   NODE_OPTIONS/NODE_PATH cannot inject the classifier loader. Synthetic state
   bytes and namespace contents remain unchanged.

Every launcher process has a scrubbed environment and isolated synthetic runtime
executables in freshly owned TMPDIR. Refusal asserts zero legacy mkdir/date/AK/
Ghostty/Pi/focus calls. No real AK/DB/provider, terminal, public account config,
installation/enrollment, trigger change, fork retry, other worker action or
claim/effect recovery occurred. Test teardown removes only its owned inactive
synthetic scratch.

### Emitted artifact identity and limit

`tests/test_ghostty_task_session_emitted.py` pins these exact emitted modules;
all were read/hashed before executing their internal synthetic-locator seam:

| Module | SHA256 |
|---|---|
| installed-identity.js | `ab7eba6c56ee636db2884ed1bbef0cf79ac02dc22924301f1b7a46ce01b99544` |
| classify.js | `6f1f5768995bc8b7a318d54a3da102b8e798f81b55e602ff9a93646fbac44fbd` |
| state.js | `7cfdf64b021a02b8ec2c6f10216f9012d55f6ba0be3533c5a6e738539b7c663b` |
| json.js | `39575888a264343d386d9f97c2f909d89ec99c6d95a4c74e49e07696c5e7a673` |
| native.js | `a34ed26e977bbd9a85eb2bf76ac85a771aa0f1a409e0975af4ed903b80aea3ac` |

The fixture shim calls actual `identityFromSnapshot(readSnapshot(locator))` and
`classifyInstalledInNamespace(input, locator)` using only newly created synthetic
files. It does not hardcode an outside outcome. This exercises the production
classifier body and lane consumer, **not the public CLI/account-root wrapper**.
No native addon is needed/loaded for these read-only paths. No source/global
fallback is present in the production launcher.

These hashes are not a released tarball receipt. The old packed artifact in the
producer memo predates the binding continuation and cannot certify this version
of the CLI. A new immutable artifact/installed closure proof remains necessary.

## Failures and bounded repairs retained

- First compatibility run: 15 subcase failures because generated producer/runtime
  stubs contained unescaped newline literals. Negative exit alone could otherwise
  hide this harness defect; event assertions exposed it. Fixed literal escaping
  and added compilation of generated stubs before execution.
- Next run: two synthetic terminal tests failed because the isolated PATH lacked
  the ordinary `env` utility used by the unchanged legacy body. Added the utility
  symlink; no real terminal or fallback was introduced.
- Review identified pre-classification import risk: Python stdin mode could import
  checkout/PYTHONPATH code. The consumer now uses `-I -S -B`, with a negative test.
  Producer subprocesses also drop NODE_OPTIONS/NODE_PATH; actual emitted positive
  tests prove invalid ambient flags do not alter classification bootstrap.
- A test-file generation command initially had nested-quote syntax failure before
  writing; corrected the authoring operation, not validation behavior.

## Remaining owner gates / no overclaim

No consumer API/binding gap remains at this recorded producer revision. Stop
before live action: actual updated immutable package/CLI release and canonical
account-root identity, AK wrapper/authority alignment, positive existing-domain
writer/trigger/candidate/prior-effect custody, and separately authorized canaries
remain unverified. Descriptor validation is not cryptographic executable
attestation, and classification is not an admission/freshness lock. The accepted
cooperative custody restrictions must keep competing routes from changing the
facts between observation and legacy consideration.

Pi/AK replacement startup/host/transport/recovery incompleteness remains with
those owners, not solved by an outside legacy path. The custody/reinstatement
runbook remains in force; no live domain is certified. Parent owns canonical AK
evidence and any task closeout decision. Historical universal-refusal evidence
stays immutable and is superseded only for current source integration status.
