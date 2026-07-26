---
summary: "Decision 83 runtime/operator review attempt 1 of commit 443d45e; revision required."
read_when:
  - "Reviewing Decision 83 runtime/operator review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-26"
decision_id: 83
reviewed_commit: "443d45e9465d9c1c0daf08ea64ef2b4cea5359b9"
dispatch_id: "dispatch-1785089589503"
---

# Decision 83 runtime/operator review — attempt 1

## Verdict

**REVISE.** Static validation confirmed Pi `0.80.10`, real `replace_base` preview semantics, the native `--system-prompt` distinction, sixteen tests, matching package digests, rendered systemd validity, and inactive service state. Production/model and 24-hour behavior remained unrun.

Blocking runtime gaps:

1. handoff directly executed bundled `0444` Python files rather than invoking `python3`;
2. systemd home masking omitted the live AK database;
3. five-second expiry guard was shorter than RPC cleanup grace and stop-timer accuracy;
4. stop ignored service/timer failure;
5. collector output/traversal resources were not enforced during collection;
6. provider/model and normalized per-cycle/cumulative cost controls were absent.

## Required correction

Use explicit Python invocation, bind the AK DB read-only, add a pre-expiry process deadline and verified cgroup termination, verify timer cleanup, bound probe pipes and supplemental census, pin provider/model, and fail closed on missing or excessive cost telemetry.

This attempt's verdict remains `REVISE` regardless of later corrections.
