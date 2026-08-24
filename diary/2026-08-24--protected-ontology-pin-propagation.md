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
