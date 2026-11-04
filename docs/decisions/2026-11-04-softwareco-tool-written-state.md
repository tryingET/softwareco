---
summary: "ADR accepting Decision 191: state that tools write into repositories has one owner, the producer; out of tree by default or a producer-written self-ignoring marker; consumers carry no copies; committed tool state is a defect; the producer proves it under isolated Git configuration."
read_when:
  - "A tool, extension or MCP server writes caches, identity, logs or snapshots into repositories."
  - "You are about to add an ignore line for another owner's tool state, or find tool state tracked in a repo."
  - "You are giving a tool 'preferred/first-step' guidance or a fleet-wide install."
type: "adr"
status: "accepted"
date: "2026-11-04"
decision_id: 191
governance_task_id: 8281
---

# ADR — tool-written state has one owner, the producer

- **Decision:** AK `191`, accepted by the operator on a decision card on 2026-11-04 (evidence 20335).
- **RFC:** [`docs/project/2026-11-01-tool-written-state.md`](../project/2026-11-01-tool-written-state.md),
  at `376b537`. Its text is the rule; this ADR does not restate or change it.
- **Trigger:** the SCI retirement, Decision 190 (SCI repo ADR-0008).
- **Inspections:** four rounds in the SCI repo, `docs/project/retirement-decision-independent-review.md`,
  `retirement-reinspection-gpt-6-1-sol.md`, `retirement-third-inspection.md` and
  `retirement-final-text-inspection.md` (the legal closure, `ready_for_adr`).

The AK record's title still begins "PROPOSAL (operator approval pending)", and the RFC's frontmatter
still says "proposal". Both predate this acceptance: AK has no retitle command, and the RFC is kept as
inspected. This ADR is the acceptance record.

## Decision

Rules 1 to 6 of the RFC are binding for every producer of state that tools write into softwareco
repositories:

1. Every class of state has exactly one owner, the producer.
2. The producer keeps state out of the tree by default, or writes a self-ignoring marker
   (`<dir>/.gitignore` containing `*`), documents retention and retirement, and keys identity on
   values that survive a remount and a reboot.
3. Consumers do not carry another owner's obligations. A per-repo ignore line is a named stopgap,
   never in contrib forks; existing lines stay until their owner removes them.
4. Committed tool state is a defect. Removing it from the index is that repo owner's change under an
   exact task; deleting data needs the owner's decision and a backup.
5. A tool that writes into repositories needs this contract before it gets "preferred/first-step"
   guidance or a fleet-wide install.
6. The producer proves its contract with a test of its real write path in a scratch repository,
   under isolated Git configuration. A clean `git status` alone proves nothing.

## Notes from the fourth inspection (no change to the rule)

- **Rule 6 and repo-local excludes.** `.git/info/exclude` hides in-tree state even under the
  isolation rule 6 names. That is not configuration. Rule 6 still fails such state, because it also
  requires the marker or out-of-tree placement. A producer test should check the marker, not only
  status (dep-redteam `tests/test_repo_ignores.py` is a working example).
- **Rule 6 and the default excludes path.** Git reads `~/.config/git/ignore` even when no
  configuration names it. `GIT_CONFIG_GLOBAL=/dev/null` alone does not isolate; the empty
  `core.excludesFile` that rule 6 names is required.
- **SCI's discharge.** The RFC's stage table omits two SCI writers that were also closed: the SessionStart
  hook in the SCI repo (AK8135) and the managed shell export and runtime (AK7953).

## Not decided

- No AGENTS, policy, template or hook change follows from this acceptance. Each needs its owner.
- The repo census in rule 6 is proposed, not implemented.
- Whether ROCS's tracked receipts (for example `governance/ontology-dist/`) count as tool state under
  rules 1 and 4 is not settled here. That classification stays with ROCS's owner (AK7929).

## Consequences

- A new producer that writes into repositories needs a rule-6 test before agents are told to use it.
- Existing per-repo `.ontology/` lines (dep-redteam `5a28113`, `tpl-project-repo` `5d9935d`) stay
  until their owners remove them, each with its guarding test in the same change.
- AK7355 (a new per-repo line in pult) conflicts with rule 3 now that SCI is retired and the machine
  ignore exists. Its owner decides.

## Rollback

Nothing is deployed. Reverting is a new decision that supersedes 191
(`ak decision advance 191 --state superseded --authority <authority> --superseded-by <id>`).

## Limits

- Three of four inspections, and the closing one, came from the same LLM family as the author; one
  came from the GPT family.
- The rule's evidence is one producer (SCI). Its cost to the next producer is not measured.
