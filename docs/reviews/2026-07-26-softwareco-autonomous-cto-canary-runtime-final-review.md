---
summary: "Decision 83 runtime/operator review attempt 2 of a53427a; revision required."
read_when:
  - "Reviewing Decision 83 runtime/operator review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-26"
decision_id: 83
reviewed_commit: "a53427a019e1338d68f19eb15d7c0beb94af5b02"
dispatch_id: "dispatch-1785091698336"
---

# Decision 83 runtime/operator review — attempt 2

## Verdict

**REVISE.** Twenty-two tests, mode semantics, AK DB binding, static systemd validation, package digests, and inactive state passed. Production and 24-hour behavior remained intentionally unrun. Four blockers remained:

1. activation could still select shared package trees instead of required isolated copies;
2. supplemental top-level census materialized every directory entry before checking its limit;
3. non-finite cost values such as `NaN` bypassed comparisons;
4. the start-failure recovery message directly executed a non-executable `0444` stop script.

The next correction requires isolated trees when an installed manifest exists, bounds enumeration before sorting, rejects non-finite costs, and prints an explicit `python3` recovery command.

This attempt's verdict remains `REVISE` regardless of later corrections.
