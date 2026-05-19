---
summary: "Short org context snapshot for this project."
read_when:
  - "When onboarding or making decisions affected by org rules"
---

# Org Summary

- Org purpose: `softwareco/owned` groups Software Company's directly operated delivery repos under one navigable lane root.
- Non-negotiables:
  - main-first workflow unless the operator explicitly asks for a review gate
  - no secrets in git
  - keep lane-root work here and child-repo work in the child repo that owns it
  - track deferred lane-root work in Agent Kernel and keep `governance/work-items.json` as the checked-in projection
- Approval/consent notes: lane-root maintenance can land directly on `main`; use PRs only for releases or explicit review requests.
