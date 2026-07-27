---
summary: "Decision 86 runtime/operator review of corrective commit 2c7659e; outcome revise_rfc."
read_when:
  - "Reviewing Decision 86 corrective review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-27"
decision_id: 86
review_track: "runtime_operator"
reviewed_commit: "2c7659ef74ef7cb4128f2c0defc860238e9eee74"
dispatch_id: "dispatch-1785173240793"
---

# Decision 86 corrective runtime/operator review

## Outcome

`revise_rfc`

## Material findings

1. WAL-only changes bypassed watched-state verification; the reviewer reproduced `db_changed=false`, `wal_changed=true`, and no drift.
2. Runtime and stop selected the oldest governance receipt rather than AK's newest-first head.
3. Full artifact verification between the pre-model state check and dispatch left a substantial TOCTOU interval.

## Required correction

Compare DB+WAL fingerprints at collection, pre-call, and post-call; use newest-first receipt semantics; and refresh plus rerun lightweight authority and watched-state checks immediately before model dispatch.
