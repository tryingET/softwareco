---
summary: "Machine-readable evidence timeline for upstream pi-mono changes and downstream pi-extensions compatibility outcomes."
read_when:
  - "You need one queryable place that summarizes relay receipts and downstream compatibility status."
  - "You are extending the pi-mono compatibility relay with richer evidence or follow-up automation."
  - "You want agents to inspect unresolved compatibility risk without reconstructing raw receipts by hand."
system4d:
  container: "Contrib-side evidence layer over the pi-mono compatibility relay."
  compass: "Turn receipts into reusable operational memory instead of one-off log lines."
  engine: "Read receipts -> enrich workflow state when possible -> classify follow-up risk -> write one deterministic index."
  fog: "Without an evidence index, upstream-to-downstream compatibility knowledge remains scattered across logs and workflow links."
---

# pi-mono compatibility evidence index

## Intent

The relay already detects upstream Pi movement and dispatches downstream validation.
This index adds the next layer: a single machine-readable timeline that future agents and operators can query directly.

It summarizes:

- upstream `pi-mono` deltas,
- relay receipts,
- downstream canary dispatch/run state when available,
- unresolved follow-up risk.

## Source files

- Builder/query script: `scripts/pi-mono-compatibility-evidence-index.mjs`
- Relay integration point: `scripts/pi-mono-compatibility-relay.sh`
- Focused test: `scripts/test-pi-mono-compatibility-evidence-index.sh`

## Canonical output

Default index path:

- `.state/pi-mono-compatibility-relay/evidence-index.json`

Default source receipts:

- `.logs/pi-mono-compatibility-relay/`

## Commands

Rebuild the full index:

```bash
node ./scripts/pi-mono-compatibility-evidence-index.mjs rebuild
```

Show summary only:

```bash
node ./scripts/pi-mono-compatibility-evidence-index.mjs summary
```

List unresolved entries:

```bash
node ./scripts/pi-mono-compatibility-evidence-index.mjs unresolved
```

Emit JSON for agents/scripts:

```bash
node ./scripts/pi-mono-compatibility-evidence-index.mjs summary --json
node ./scripts/pi-mono-compatibility-evidence-index.mjs unresolved --json
```

Offline rebuild without GitHub run enrichment:

```bash
node ./scripts/pi-mono-compatibility-evidence-index.mjs rebuild --offline
```

## Resolution model

Each entry is classified into one of these states:

- `not_applicable` — no actionable compatibility work implied
- `safe` — downstream validation is known good for the upstream delta
- `pending` — downstream validation is in flight or not yet concluded
- `needs_attention` — retry, investigation, or manual follow-up is needed

Follow-up hints include:

- `none`
- `wait_for_downstream`
- `retry_dispatch`
- `investigate_failure`
- `manual_review`

## Enrichment behavior

When possible, the index script enriches recent `workflow-dispatched` receipts with live GitHub Actions run state via `gh run view`.

That lets the index distinguish between:

- workflow dispatched and still queued/running
- workflow completed successfully
- workflow completed with failure/cancellation

If GitHub enrichment is unavailable, the entry remains machine-readable and falls back to receipt-only evidence.

## Relay integration

Every time the relay writes a new receipt, it also rebuilds the evidence index.

This means the scheduled contrib pull path now maintains:

1. raw receipt history,
2. current index state,
3. query-ready unresolved compatibility risk.

## Why this is additive

This does not replace the relay, the canary, or the workflow.
It adds a memory layer over them so future upgrades benefit from today’s evidence instead of re-deriving it from raw logs.
