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
- parent repo still needs a commit before `fork/` can be initialized as its own git root via:

```bash
./scripts/bootstrap-lane-root.sh fork --init-lane-git
```

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
└── tools/rocs-cli/        # vendored ROCS tooling baseline
```

## ROCS command flow

Use the repository wrapper for deterministic execution:

```bash
./scripts/rocs.sh --doctor
./scripts/rocs.sh build --repo . --resolve-refs --clean
./scripts/rocs.sh validate --repo . --resolve-refs
```
