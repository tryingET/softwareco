---
summary: "Bridge from upstream pi-mono updates in contrib to downstream pi-extensions compatibility validation."
read_when:
  - "You are wiring or debugging the contrib pull automation around pi-mono updates."
  - "You need to understand how upstream Pi changes trigger downstream extension compatibility checks."
  - "You are changing the relay mode, watched paths, or receipt behavior for pi-mono compatibility dispatch."
system4d:
  container: "Contrib-root automation bridge for upstream-to-downstream compatibility signaling."
  compass: "Keep upstream pull mechanics and downstream validation ownership separate but connected."
  engine: "Detect relevant pi-mono movement -> dispatch pi-extensions canary -> persist receipt keyed to the upstream delta."
  fog: "Without a relay, contrib updates and downstream extension compatibility drift into disconnected manual memory."
---

# pi-mono compatibility relay

## Intent

This repo owns the **upstream update trigger**, not the extension compatibility tests themselves.

The relay connects:

- upstream Pi movement in `contrib/pi-mono`
- downstream compatibility validation in `owned/pi-extensions`

without relocating the canary away from the extension project that owns it.

## Source files

- Relay script: `scripts/pi-mono-compatibility-relay.sh`
- Exact candidate resolver: `scripts/pi-mono-compatibility-contract.mjs`
- Evidence index: `scripts/pi-mono-compatibility-evidence-index.mjs`
- Pull orchestrator: `scripts/pull-all-local-contrib-repos.sh`
- systemd timer/service:
  - `scripts/systemd/contrib-all-repos-pull.service`
  - `scripts/systemd/contrib-all-repos-pull.timer`
- cron fallback:
  - `scripts/cron/contrib-all-repos-pull.cron`

## Default behavior

After the contrib pull script completes, it invokes the relay.

The relay then:

1. reads the current `contrib/pi-mono` HEAD,
2. compares it with the last processed HEAD stored under `.state/`,
3. filters for watched upstream paths,
4. triggers the downstream `pi-extensions` compatibility canary when relevant paths changed,
5. writes a machine-readable receipt under `.logs/`.

Current default watched upstream paths:

- `packages/coding-agent`
- `packages/tui`

These are the upstream surfaces most likely to affect our Pi extension runtime behavior.

### Exact upgrade contract

An `upgrade` dispatch supplies all three workflow inputs: `profile`, `host_version`,
and `changelog_ref`. Local mode passes the same version and anchor through
`PI_HOST_COMPAT_HOST_VERSION` and `PI_HOST_COMPAT_CHANGELOG_REF`.

By default, the relay reads `packages/coding-agent/package.json` from the exact
upstream trigger commit, checks its package name and exact semantic version, and
uses that commit's `packages/coding-agent/CHANGELOG.md` URL as the review anchor.
The checkout must have a GitHub `origin`; uncommitted files do not change the
candidate. This anchor records immutable trigger context; it does not assert
that a person reviewed the change or approved adopting it.

To select a separately reviewed candidate, set **both** overrides together:

```bash
PI_HOST_COMPAT_HOST_VERSION=1.5.0 \
PI_HOST_COMPAT_CHANGELOG_REF='https://github.com/earendil-works/pi/compare/v1.4.0...v1.5.0' \
./scripts/pi-mono-compatibility-relay.sh
```

A partial override is rejected rather than paired with unrelated upstream
metadata. Versions must be exact; GitHub anchors must name a tag, commit, or
comparison rather than a moving branch, including DNS-absolute `github.com.` URLs.
Anchors containing whitespace or ASCII control characters are rejected before any
dispatch. A read-only `npm view` must confirm the exact package name and version
against public npm; both the default and `@earendil-works` scoped registry are
explicitly set so local scoped configuration cannot redirect this check.
An unpublished release or unavailable registry leaves the upstream delta pending
for retry and creates a failure receipt without dispatching a broken CI run.
No dependencies are installed by this check. The relay requires Node and npm for
effectful upgrade runs; a dry-run resolves the contract but skips registry access.

Receipts add `candidate_contract` with the selected package, version, review
anchor, contract source, and `published-npm-package` target. The canary tests
that published package version, **not** an upstream Git checkout. An upstream
commit can be newer than the published package it declares; its `after_head`
remains trigger provenance and does not become source-head compatibility proof.
Workflow dispatch acceptance also remains distinct from a passing canary result.
A same-repository run URL returned on its own line by `gh workflow run` is recorded
with `downstream_repo.run_identity_source: dispatch-output`. Missing, malformed,
or ambiguous run URLs leave the dispatch uncorrelated and pending in the index;
the relay never substitutes the latest run on the branch. Accepted dispatches
still advance the processed-head state, even when run identity is unavailable.
The `current` profile uses the downstream pinned baseline and needs no upgrade
contract or registry preflight; `off` retains the pending delta.

## Ownership boundary

### contrib owns
- detection of upstream `pi-mono` movement
- relay invocation from scheduled pull automation
- local relay state and receipts

### pi-extensions owns
- the compatibility canary contract
- scenario definitions
- package-level compatibility commands
- the dedicated compatibility workflow

That split is deliberate.

## Modes

### `workflow`
Dispatch `.github/workflows/compatibility-canary.yml` in `owned/pi-extensions` via `gh workflow run`.

This is the default mode for unattended automation.
The workflow file must already exist on the target remote branch; before this relay change is merged, branch-local verification should use `local` mode.

### `local`
Run the local canary runner in the `pi-extensions` checkout directly.

Useful for deterministic debugging when you want immediate local proof without GitHub Actions dispatch.

### `off`
Disable downstream dispatch while keeping relay detection code in place.

Useful for temporary maintenance windows only.

## State and receipts

### State

Persisted last-processed pi-mono head:

- `.state/pi-mono-compatibility-relay/pi-mono.current-head`

The relay advances this state only when the upstream delta is either:
- irrelevant to watched paths, or
- successfully handed off downstream.

If downstream dispatch fails, the state is **not** advanced so the relay can retry on the next scheduled run.

### Receipts

Machine-readable receipts are written to:

- `.logs/pi-mono-compatibility-relay/`

Receipt states include:
- `initialized`
- `skipped`
- `dry-run`
- `workflow-dispatched`
- `local-passed`
- `local-failed`
- `dispatch-failed`
- `failed`

### Evidence index

A normalized evidence timeline is rebuilt at:

- `.state/pi-mono-compatibility-relay/evidence-index.json`

This index is query-ready and classifies each relay receipt into machine-readable compatibility states such as `safe`, `pending`, `needs_attention`, or `not_applicable`.
See [pi-mono-compatibility-evidence-index.md](pi-mono-compatibility-evidence-index.md).

## Manual use

Preview behavior without dispatching or updating state:

```bash
./scripts/pi-mono-compatibility-relay.sh --dry-run
```

Force local debugging path:

```bash
PI_COMPAT_RELAY_MODE=local ./scripts/pi-mono-compatibility-relay.sh
```

Disable relay during a one-off pull:

```bash
./scripts/pull-all-local-contrib-repos.sh --no-pi-compat-relay
```

## Why this exists here

The relay belongs in `contrib` because this repo is where upstream Pi checkouts are actually refreshed on a schedule.

The canary stays in `pi-extensions` because that repo owns the downstream compatibility knowledge.

The relay is the connective tissue between those two existing realities.

## Validation

Run `bash contrib/scripts/test-pi-mono-compatibility-relay.sh` from the company
repository root (or `bash scripts/test-pi-mono-compatibility-relay.sh` from the
contrib lane). The suite uses temporary Git repositories and mocked npm/GitHub
clients; it verifies workflow and local input forwarding, committed-source
resolution, rejected contracts, publication failures, and retry state without
network dispatch. It also exercises real npm configuration resolution with an
empty fixture-local cache and `--offline`; npm is required, but no network is
used by that check. The company smoke gate also runs this suite.
