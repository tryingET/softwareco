---
summary: "Define softwareco/owned as a lane-root control-plane repo."
read_when:
  - "When deciding whether work belongs in the lane root or a child repo"
type: "decision"
---

# ADR 0001 — `softwareco/owned` is a lane-root control plane

## Status
Accepted — 2026-03-17

## Context
This repository is the git root above many nested child repos. The template scaffold read like a generic single-project repo, which made it easy to misplace work, duplicate child-repo state, or treat the lane root like a product repo.

## Decision
Treat `softwareco/owned` as a lane-root control-plane repo.

- Track only lane-root-local docs, tooling, and planning here.
- Make implementation changes inside the child repo that owns the work.
- Use this repo for navigation, shared wrappers, ontology, and repo census visibility.
- Do not mirror child-repo task state in this repo's work-items model.

## Consequences
- README and project docs must describe the lane-root role explicitly.
- `governance/work-items.json` only captures lane-root-local work.
- `next_session_prompt.md` should steer operators toward one lane-root-local slice at a time.
