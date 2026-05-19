---
summary: "Strategic goals for this project."
read_when:
  - "When planning quarters"
---

# Strategic Goals

- Goal: Keep the lane-root boundary explicit so work lands in the correct repo.
  Metric: Lane-root docs contain no placeholder scope text and defer child-repo implementation work to the owning repo.
- Goal: Preserve deterministic operator entry points at the lane root.
  Metric: `./scripts/preflight-repo-census.sh .` plus lane-root CI wrappers stay usable from a clean checkout.
- Goal: Make current lane-root state legible to the next operator.
  Metric: `next_session_prompt.md` stays current and `governance/work-items.json` remains a reviewable projection of lane-root AK state.
