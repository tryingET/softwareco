---
summary: "System4D: Engine (states/invariants/lifecycle) for this project."
read_when:
  - "When defining invariants and lifecycle"
---

# System4D — Engine

## Invariants
- Invariant(s):
  - Agent Kernel owns the live deferred lane-root work; `governance/work-items.json` remains the checked-in projection
  - `next_session_prompt.md` reflects the next real starting point
  - child repos remain autonomous for implementation and repo-local planning
  - lane-root helper scripts are deterministic entry points, not hidden operator lore
