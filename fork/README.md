---
summary: "Lane-root baseline for maintained forks under softwareco/fork."
read_when:
  - "You need the purpose of the softwareco fork lane."
  - "You are deciding whether a repo belongs under softwareco/fork."
type: "reference"
---

# fork

Software Company lane root for maintained forks and deliberate divergence repos.

## Context

- **Location**: fork
- **Language**: python

## Purpose

This is a lane root, not a normal delivery repo.
It exists to host forked repositories when upstream scope, governance, or roadmap constraints no longer fit what Software Company needs.

Use this lane for:
- maintained forks of upstream repositories
- long-lived divergence repos
- codebases whose roadmap has moved from upstream issue requests to local ownership

## Current motivation

The immediate driver is DSPY-related work previously tracked against `badlogic/pi-mono`.
That upstream line is now considered closed locally; future work should move into a fork instead of more upstream requests.

## Bootstrap status

- lane baseline materialized from `tpl-project-repo`
- lane-root git initialized on 2026-03-10
- first concrete child repo created on 2026-03-13: `pi-mono/`
- lane-root role now returns to policy + inventory; active execution should happen inside child repos

## Current child repos

- `pi-mono/` — local home for post-upstream DSPY work formerly tracked against `badlogic/pi-mono`

## Structure

```text
fork/
├── AGENTS.md              # lane-level policy for descendant fork repos
├── next_session_prompt.md # active handoff for lane bootstrap / cutover work
├── docs/                  # lane-root docs / decisions / learnings
├── governance/            # compatibility work queue projection
├── ontology/              # lane-root ontology baseline
├── policy/                # lane-root policy hooks
├── scripts/               # lane-root deterministic wrappers
├── src/                   # placeholder source root from template baseline
├── tests/                 # placeholder test root from template baseline
└── pi-mono/               # first concrete fork-lane repo
```

## ROCS command flow

Use the repository wrapper for deterministic execution. It resolves ROCS via the workspace core checkout (or `ROCS_BIN` / `rocs` on `PATH`):

```bash
./scripts/rocs.sh --doctor
./scripts/rocs.sh build --repo . --resolve-refs --clean
./scripts/rocs.sh validate --repo . --resolve-refs
```
