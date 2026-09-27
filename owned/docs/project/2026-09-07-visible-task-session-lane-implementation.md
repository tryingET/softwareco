---
summary: "Task5481: actual DB-free installed-identity/classification consumer, bounded negative/outside compatibility proof, and unverified installation/custody gates."
read_when:
  - "Consuming the lane Decision151 implementation or verifying its producer seam."
type: implementation_evidence
---

# Decision151 — lane implementation (task5481)

## Current source behavior

Owner: canonical `softwareco/owned`, branch `main`; parent owns canonical AK
mutations/evidence. Pre-existing dirty `AGENTS.md` and
`docs/project/repo-capability-map.md` remain forbidden and untouched.

The earlier universal-refusal commit was an interim gate, not accepted final
compatibility. Its implementation limit is now resolved **in source**:

1. Validate the complete legacy argv, expand the 609–615 preset and reject
   duplicate tasks/options, conflicting modes, malformed IDs/log options,
   unknown options and mixed help. Standalone help never invokes the producer.
2. Resolve exactly `pi-task-session` once from PATH to its physical executable;
   no runtime override, alternate command, ordinary AK lookup or guessed identity.
3. Build one canonical `classify-installed-request.v1` with all task IDs and
   physical cwd. No `akInstance` is supplied by the caller/lane. Derive a stable
   classification request ID from its semantic input, not a launch/admission ID.
4. Call actual `identity`, verify the exact configured descriptor, then call
   actual `classify-installed`. Validate strict response shape, exact producer
   package/version/interface, canonical request digest and namespace metadata.
   Require identityDigest and namespace to agree with the descriptor. Concurrent
   descriptor/snapshot drift refuses conservatively; no automatic retry.
5. Only verified `outside` reaches the retained legacy body. Enrolled, unknown,
   mixed, missing, incompatible, malformed, oversized or timed-out results refuse
   the **whole request** with exit 2 before log mkdir/date, AK, terminal/Pi or focus.
   Dry-run is gated identically. No per-task classification or partial classified
   batch is launched.

The embedded stdlib consumer runs Python with `-I -S -B`: no checkout/PYTHONPATH
imports, site initialization or bytecode writes. Producer subprocesses drop
`NODE_OPTIONS`/`NODE_PATH`; those runtime flags cannot inject a classifier loader.
Legacy post-gate environment behavior is otherwise retained.

Transport is bounded to 64 KiB UTF-8 JSON output and three seconds per producer
operation, using in-memory nonblocking pipes. Duplicate keys, BOM/invalid UTF-8,
non-integer JSON numbers, trailing objects and unknown fields refuse. Raw
producer stderr/output and filesystem exceptions are not printed. Timeout closes
only the newly owned DB-free classifier child, never a task worker or effect.
No files/directories are created by the consumer before successful classification.

Outside-domain legacy semantics remain: single interactive/multi print defaults,
explicit mode/hold/log options, historical prompt, AK task-to-repo resolution,
Ghostty shell argv and optional niri focus. This is not the sealed replacement
host or a claim of live terminal fidelity. Existing downstream legacy failures
are not reinterpreted as task admission or effect retirement.

## Actual producer identity and contract

Producer commit: `6b90412bc8a848cf72e89419f6dc71cf9e9f6b87`, ordinary main worktree
`/home/tryinget/.local/state/pi-quests/tmp/decision151-main.5gPphB/pi-extensions`.
That path is neither canonical registration nor nominated/enrolled live domain.

Read source and emitted `bin`, `core`, `installed-identity`, `classify`, `state`,
`json`, and the lazy `native` dependency as needed. The owning memo is
`pi-extensions/docs/project/2026-09-07-visible-task-session-pi-implementation.md`
at that source worktree. Do not mistake the old pre-binding packed tarball for
this updated artifact; the later binding needs its own release/pack identity.

| Wire fact | Actual owner contract consumed |
|---|---|
| Producer | `@tryinget/pi-little-helpers`, `0.9.0`, interface `pi.task-session.classification.v1` |
| Discovery | `pi-task-session identity`, no input/options; exact `pi.task-session.installed-identity.v1` configured descriptor |
| Descriptor binding | `akInstance`, namespace id/generation/snapshotDigest, exact classification export/request schema and SHA256 identityDigest |
| Classification | `pi-task-session classify-installed`; exact fields `schema,requestId,taskIds,cwd`; schema `pi.task-session.classify-installed-request.v1` |
| Result | Exact classification.v1 fields plus identityDigest; only outside with nonnull matching namespace and empty reasons proceeds |
| Canonical digest | Sorted ASCII object keys, compact JSON, literal UTF-8 strings, safe integers; SHA256 of the canonical bytes. Request digest hashes the installed request, not a lane-invented AK-instance request |
| Limits | 1–256 unique positive safe-integer IDs, request ID 1–128 ASCII identifier chars, 4096-byte canonical existing cwd, 64 KiB request/output |

Producer binds canonical identity from **one complete, non-withdrawn existing
owner snapshot with exactly one AK instance**; the classifier freshly derives
identity and classification from one snapshot. No lane registry/config file or
caller-invented identity is introduced. Missing, mixed-instance, incomplete,
withdrawn or physically replaced inventory refuses. Classification is a read-only
observation, **not** an admission, freshness lock or cached outside certificate.
Cooperative positive custody must prevent competing changes after observation.

The lane validates protocol/operational digests, not a cryptographic attestation
of an arbitrary executable on PATH. Exact immutable installed artifact selection,
public account-root lookup, wrapper/canonical authority alignment and positive
custody remain owner rollout proofs. Package version alone cannot certify them.

## Bounded verification

`just check` runs shell/Python syntax, scoped whitespace and isolated Python
standard-library tests. Every launcher execution uses a scrubbed environment and
fresh owned-TMPDIR executable stubs for AK, Pi, Ghostty, niri and filesystem/log
helpers. Ghostty stubs record shell argv/environment but never run the payload.
Refusal tests demand no legacy-effect calls; positive tests check historic
prompts/defaults/overrides/log paths/focus arguments after the gate.

An explicit additional test setting enables the **actual emitted classifier
body**, not hardcoded outside responses:

```bash
TASK_SESSION_PRODUCER_DIST=<reviewed-emitted-task-session-directory> just check
```

This variable is read only by tests, never the production launcher. Tests pin
five emitted-module SHA256 values and use owner functions `identityFromSnapshot`
and `classifyInstalledInNamespace` against newly constructed private synthetic
state. No public OS-account locator is called. Real producer classification and
canonical digest results flow through the actual lane process. Coverage includes
outside single/batch/preset, unknown/mixed/enrolled, independent task/common-Git/
overlap/shared-effect conflicts, retained unresolved attempts, and withdrawn/
incomplete/mixed-instance/physical-identity uncertainty. Synthetic snapshot bytes
and namespace contents remain unchanged. This is stronger than mock-only consumer
proof, but **not** public account-bound CLI or installed capability proof.

Without that explicit path, four emitted tests are visibly skipped; local tests
still run. Exact commands/results, emitted pins, failures/fixes and commits are
in [continuation evidence](../../diary/2026-09-07--decision151-lane-classifier-integration.md).

## Standard entrypoints and policy boundary

The standard Justfile contract and local bootstrap prompt were read. No
`docs/engineering.local.md` or `policy/engineering-lane.json` exists at this lane
root, and no adoption policy is fabricated. The shell/documentation lane uses
Python standard-library tests; no child Pi stack addendum applies. The task
forbids live Pi, so bootstrap prompt spawning was not used.

`help` lists targets; `doctor` checks local tools/TMPDIR only; `lint` checks syntax
and scoped whitespace; `test` runs synthetic tests; `check` composes lint/test once.
`ci` intentionally exits 2 because old smoke/fast can fetch Git remotes and full
CI invokes AK/task-scopes/ROCS. No runtime-bearing profile is hidden behind a
passing alias. Build/fmt/run/dev are omitted because no truthful corresponding
surface is established. The scoped force-added Justfile needed no ignore edit.

## Remaining owner gates

See the [positive custody/reinstatement runbook](2026-09-07-visible-task-session-lane-custody.md).
No live checkout is nominated/certified. Public installed identity/account-root
proof, updated immutable package/CLI closure, canonical AK-wrapper alignment,
positive writer/trigger/candidate/prior-effect custody, and separately authorized
useful canaries remain. The Pi/AK replacement startup/integration limitations in
their owner memo are independent of this lane consumer. No install/enrollment,
AK/DB/provider call, trigger change, fork retry or claim/effect recovery occurred.
