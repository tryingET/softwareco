---
summary: "Repair the stale generated ROCS workspace-root default in the fork lane root."
type: diary
---

# ROCS workspace-root default repair

AK task `4961` changes the stale L2 default from `$HOME` to `$HOME/ai-society`, matching the ROCS
workspace layout and sibling infra consumer. This is a one-file generated-consumer repair; a full
recopy would overwrite intentional divergence.

The same stale script previously defaulted every profile to loose resolution. `branch-ci` and
`main-strict` now default to—and require—strict resolution, while `local-dev` remains loose by
default.
