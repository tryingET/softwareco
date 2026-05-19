---
summary: "System4D: Container (boundary/constraints) for this project."
read_when:
  - "When scoping project work"
---

# System4D — Container

## Boundary
- In scope:
  - lane-root docs, governance, ontology, and helper scripts
  - repo census and other deterministic lane-root operator workflows
  - planning for this repo itself and its checked-in AK projection
- Out of scope:
  - implementation changes owned by nested child repos
  - duplicating or overriding child-repo task state

## Constraints
- Constraints:
  - keep the lane root lightweight and navigation-oriented
  - prefer deterministic wrappers over ad-hoc scripting
  - keep session handoff current in `next_session_prompt.md`
