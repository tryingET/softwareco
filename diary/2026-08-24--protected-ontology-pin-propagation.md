---
summary: "Selectively sync the protected ontology-kernel v0.2.0 default into Softwareco templates."
type: diary
---

# Protected ontology pin propagation

AK task `4960` selectively updates Softwareco's intentionally divergent `tpl-project-repo` copy
from rolling `@main` to protected `@v0.2.0` and adds an L1 assertion preventing regression. It does
not overwrite the rest of the L1 template from L0.

The same validation pass also removes four stale `work-items.cue` assertions left behind after the
files were removed from agent/monorepo template and fixture surfaces; this restores the L1 gate
without reintroducing retired projections.
The gate also drops seven stale README/full-CI assertions for `ak work-items` commands removed from
the corresponding template surfaces in commits `2e3adca` and `41b1590`. Existing JSON projection
files are not changed while decision `#127` remains review-pending.
The obsolete generated-agent fake-AK drift exercise is removed for the same reason: agent full CI
no longer invokes the retired work-items projection gate.
The Softwareco L1 repository's own company-overlay manifest is also a live consumer, so it now pins
the same protected release rather than `@main`.

Post-review correction: the tracked Softwareco root ontology outputs are regenerated under
`main-strict` against `@v0.2.0`, the authoritative validate receipt is retained, and template CI
now fails if any provenance/summary output drifts from the protected pin.
The root full gate now resolves strictly, validates and builds while retaining per-command
receipts; deep validation then asserts every provenance/summary output binds the protected pin.
This closes the prior validate-only freshness gap without byte-comparing machine-local paths.
Final review hardening: parser-backed checks now reject mixed/stale core refs and require strict,
authoritative, zero-error build/validate receipts. Full CI enters the repo root before `--repo .`.
