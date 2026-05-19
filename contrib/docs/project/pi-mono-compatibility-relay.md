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
