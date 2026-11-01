---
summary: "Proposed fleet rule for state that tools write into repositories (one owner, the producer; out of tree by default), and pointer to the SCI retirement decision that triggered it."
read_when:
  - "A tool, extension or MCP server writes caches, identity, logs or snapshots into repositories."
  - "A repo shows untracked or tracked tool state (such as .ontology/) and you are about to add an ignore line."
  - "You need the status of the Semantic Code Intelligence retirement at fleet level."
type: "rfc"
status: "proposal; AK decision pending operator review (not accepted)"
as_of: "2026-11-01"
---

# Tool-written state in repositories (proposal)

## Why this exists

On 2026-11-01 the operator decided, on decision cards, to retire Semantic Code Intelligence (SCI)
from agent sessions in stages. The evidence and the decision record live in
`owned/semantic-code-intelligence/docs/project/retirement-from-agent-sessions-decision.md`.

SCI wrote runtime state (cache, workspace identity, snapshots, MCP logs) into `.ontology/` inside
every repository a Pi session ran in.

**Effects on the fleet:**

- 61 repos ended up with the directory, 193 MiB in total.
- 28 of them did not ignore it.
- This meta repo tracked the live SQLite db.

**Remediation work that resulted:**

- Lint broke in dep-surgeon.
- At least nine AK tasks went to per-repo fixes, and those fixes contradicted each other.
- The fixes were attributed to the wrong owner, because `.ontology` reads like ROCS's `ontology/`.

**Root cause:** no owner was responsible for tool-written state. Obligations travelled by copy,
through templates and per-repo ignore lines. No AK decision covered the class.

## Proposed rule

1. **Every class of state has exactly one owner, the producer.**

   | Class | Where it lives |
   |---|---|
   | Source | git, reviewed |
   | Derived build output | regenerable, and ignored by the producer |
   | Runtime cache, identity and logs | machine-local, outside the repo by default (`$XDG_STATE_HOME` / `$XDG_CACHE_HOME`, keyed by repo identity) |
   | Pinned upstream layers | resolved from pinned or published inputs for anything called authoritative |

2. **Producer obligations.**
   - Keep state out of the tree by default.
   - If state must live in the tree, write a self-ignoring marker (`<dir>/.gitignore` containing
     `*`) when the directory is created.
   - Document what is written, its retention, and the uninstall and data-retirement path.
3. **Consumers do not carry another owner's obligations.** A per-repo ignore line for someone
   else's state is a stopgap: it must name the producer, and it must never go into contrib forks.
4. **Committing tool state is a defect.** Removing it from the index needs no decision; deleting
   the data needs the owner's decision and a backup.
5. **Contract first.** A tool that writes into repositories needs this contract before it gets
   "preferred/first-step" guidance or a fleet-wide install.

## How SCI discharges it (retirement, not repair)

| Stage | Change | AK |
|---|---|---|
| 1 | Pi package removed from the operator's Pi settings; new sessions write no `.ontology/` | AK7928 |
| 2a | Machine-level `~/.config/git/ignore` with `.ontology/`, managed in dotfiles-managed | AK7932 |
| 2b | This repo stops tracking `.ontology/ontology.db*` (commit `9c9ef5b`); the copies in history and on the private NAS remote stay under AK6985 | AK7935 |
| later | Owner-approved backup and quarantine of the remaining directories; nothing deleted before that decision | — |

The per-repo ignore sweep (AK7890) and the XDG relocation (AK7907) are superseded by this
retirement plan. Their lifecycle closeout needs the operator.

## Not decided here

- Whether this rule becomes binding. That is the AK decision, now a proposal.
- Any AGENTS, policy or template change. Those belong to their owners.
- ROCS pin and freshness drift. That is a separate failure class with the same root, tracked in
  core/rocs-cli AK7929.
