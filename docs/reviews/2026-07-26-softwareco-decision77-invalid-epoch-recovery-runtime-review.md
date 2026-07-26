---
summary: "Runtime review of Decision 79's one-time quarantine for malformed Decision 77 epoch receipt 8967."
read_when:
  - "Reviewing Decision 79 runtime closure."
type: "review"
status: "ready_for_adr"
date: "2026-07-26"
decision_id: 79
review_track: "runtime-state-machine"
review_outcome: "ready_for_adr"
---

# Runtime review — Decision 79 invalid epoch recovery

## Outcome

`ready_for_adr`

## Reviewed candidate

- RFC commits: `1283c8f`, corrected by `0dc276f`
- Review session: `dispatch-1785034179906`

## Findings

The recovery is implementable as a graph-complete validator with an exact one-time invalidation branch, immutable zero-operation evidence, live controller-deferral checks, overflow detection, and mutation-free fixtures. AK task `entity_version=1` plus null claim fields is the authoritative task-row proof available; active deferral `182` closes the claim race. Off-system absence remains an explicit human attestation rather than machine inference. Replacement authorization derives expiry from one captured timestamp and asserts nanosecond equality before recording.

No material runtime blocker remains. Production modes remain fail-closed until Decision 79 acceptance, checker implementation, and exact human invalidation all exist.
