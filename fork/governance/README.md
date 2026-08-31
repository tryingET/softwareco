---
summary: "AK-native planning boundary for fork lane-root work."
read_when:
  - "When routing active or deferred fork lane-root work"
  - "When deciding whether work belongs in the lane root or a child repo"
---

# Project Work Authority

Agent Kernel is the live authority for active and deferred work in this registered repository. Use `ak task ready`, `ak task list`, and exact `ak task show <id>` readbacks; the generic checked-in `governance/work-items.json` mirror is retired under accepted Decision 127.

The retained `governance/work-items.cue` file is a non-operational historical schema, not task authority. Frozen AK task-scope exports and other owner-native state are separate surfaces and are not retired by analogy.

If work is specific to a child repo, route it through that child repo's own registered task authority instead of centralizing execution here.
