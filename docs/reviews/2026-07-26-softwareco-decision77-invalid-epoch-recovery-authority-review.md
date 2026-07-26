---
summary: "Authority review of Decision 79's one-time quarantine for malformed Decision 77 epoch receipt 8967."
read_when:
  - "Reviewing Decision 79 authority closure."
type: "review"
status: "ready_for_adr"
date: "2026-07-26"
decision_id: 79
review_track: "constitutional-authority"
review_outcome: "ready_for_adr"
---

# Authority review — Decision 79 invalid epoch recovery

## Outcome

`ready_for_adr`

## Reviewed candidate

- RFC commits: `1283c8f`, corrected by `0dc276f`
- Review session: `dispatch-1785034179905`

## Findings

The proposal preserves receipt `8967` as immutable malformed history, never validates it as authority, and adds only a fixed direct-human quarantine transition. Decision-79 acceptance, invalidation, and any later Decision-77 epoch remain separate gates. The acceptance membrane binds the exact human receipt and immutable commits; the checker must fresh-read controller quarantine on every pass; raw overflow and predecessor-graph validation prevent hidden chain entries; all prior Decision-77 transitions remain intact; and the exception is non-retroactive, non-derogating, and non-precedential.

No material authority blocker remains. Human acceptance is still required before implementation or invalidation.
