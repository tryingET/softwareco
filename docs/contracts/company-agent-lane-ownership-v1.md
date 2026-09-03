---
summary: "Candidate SoftwareCo contract for company-appointed agent placement and non-overlapping parent/child Git ownership."
read_when:
  - "Creating, locating, migrating, or reviewing a SoftwareCo-appointed agent repository."
  - "Changing the SoftwareCo agents-lane baseline or parent ignore rules."
type: "contract-candidate"
status: "owner_acceptance_pending"
---

# SoftwareCo company-agent lane ownership v1

## Decision status

This is a candidate owner contract for Gate A formalization. It does not appoint an agent, create or move a child repository, approve a release, authorize a run, or activate a runtime. Acceptance requires explicit SoftwareCo owner disposition of the exact revision.

## Problem and observed state

The ratified architecture places company-appointed agents at `~/ai-society/<company>/agents/agent-*`, with one standalone repository and one canonical role per agent. A company parent must own the lane baseline while each child owns its own repository. Without an explicit ownership split, parent and child Git repositories can track the same files, propagation can overwrite agent-owned content, and a directory path can be mistaken for jurisdiction or authority.

SoftwareCo already documents an `agents/` lane, while current society-level agents remain separate repositories under the global society agents root. This contract records the target ownership rule without claiming that every desired child already exists or is migrated.

## Semantic owner and non-owner boundaries

SoftwareCo owns:

- the `~/ai-society/softwareco/agents/` lane baseline;
- parent-level `AGENTS.md`, `CODEOWNERS`, and ignore behavior for that lane;
- the company-side decision to host a SoftwareCo-appointed child under that lane after an accountable appointment exists;
- compatibility and rollback of the parent lane layout.

SoftwareCo does not own through this contract:

- society-level appointment or global-agent jurisdiction;
- the child repository's persona, source history, releases, or local decisions;
- provider profile or Prompt Vault content semantics;
- Agent Kernel release acceptance or task-bound run authorization;
- Pi/ASC runtime custody, observations, credentials, or effect settlement.

## Selected invariants

1. **Home follows accountable appointment.** A SoftwareCo-appointed agent defaults to `~/ai-society/softwareco/agents/agent-<name>`. Read territory, product affinity, profile provider, and execution host do not determine home.
2. **One agent, one repository, one canonical role.** A child root is a standalone Git repository. The parent never absorbs the child's history.
3. **Parent owns only the lane baseline.** The parent may track `agents/.gitignore`, `agents/AGENTS.md`, `agents/CODEOWNERS`, and other explicitly accepted lane-baseline files. It must ignore child `agent-*` repositories.
4. **No dual Git ownership.** No path may be tracked by both parent and child repositories. An overlap is a blocking error, not an accepted convenience.
5. **Paths are locators.** A repository path is neither stable identity nor authority. Stable `agent_id` and an accountable appointment record are separate facts.
6. **Placement is not activation.** Repository creation, appointment, release acceptance, run authorization, runtime launch, and effect authority remain distinct actions.
7. **Persona can narrow only.** Child persona and policy may narrow capability or territory; they may not widen the parent/company appointment, permit, runtime ceiling, or effect authority.

## Creation and migration workflow

The only accepted workflow is `inspect -> plan -> explicit apply`:

1. inspect the parent index, ignore rules, candidate child root, existing Git metadata, stable identity, appointment, and role collision evidence;
2. produce a no-apply plan naming every parent-baseline addition, every ignored child path, the child repository origin/history, and rollback;
3. reject on parent/child tracked-file overlap, missing appointment, duplicate `agent_id`, ambiguous jurisdiction, or an attempt to derive authority from the path;
4. apply only through an exact owner-authorized task after review;
5. verify parent and child indexes independently and preserve the child's full history.

Gate A accepts only the contract and fixtures. Materializing or moving a live child is Stage B work and requires its own transition authority.

## Failure semantics

- `parent_child_overlap`: blocked until one owner relinquishes the path and indexes prove the correction.
- `missing_appointment`: no company-agent home or role claim may be finalized.
- `duplicate_agent_id`: both candidates are ineligible until the identity conflict is resolved by the accountable owner.
- `ambiguous_jurisdiction`: use the conservative non-placement default; do not infer company home from read scope or product affinity.
- `path_claimed_as_authority`: reject the claim. Paths can support discovery only.
- `child_history_loss_risk`: stop migration and retain the current repository unchanged.

These are contract-local outcomes, not a new global error enum.

## Security, privacy, and operational implications

Separate repositories reduce accidental parent propagation into persona, diary, learning, policy, or evidence content. They do not provide OS confinement, confidentiality, credential isolation, or runtime least privilege. Those claims require runtime and host evidence from their owners.

Parent ignore rules must be reviewable and tested. Operators must be able to enumerate which files the parent tracks and prove that a child repository's files are absent from the parent index. Support responsibility for child source remains with the child owner; the company lane owner supports baseline placement and routing only.

## Compatibility and rollback

This contract is additive. It preserves current parent and child repositories and changes no fleet default. Existing society-level agents remain society-level. Schema-1 and current runtime paths are unaffected.

Rollback is to close or revert the candidate revision, retain the current lane and child layout, and perform no repository move, creation, retirement, or activation. A rollback never rewrites child history or agent-owned content.

## Acceptance scenarios

The owner can accept this contract only when the following are reviewable:

- parent baseline files are explicitly named and child roots are ignored;
- a representative child root is a distinct Git repository with zero tracked-file overlap;
- a company appointment identifies the child without using the path as proof of authority;
- same local names in different jurisdictions remain distinguishable by stable `agent_id` and appointment;
- a migration plan is no-apply by default, preserves history, and has an exact rollback path.

## Alternatives rejected

- **Track child files in the parent for convenience:** rejected because it creates dual ownership and destructive propagation risk.
- **Use the global society agents root as a miscellaneous fleet directory:** rejected because that root denotes society-level jurisdiction.
- **Choose home from provider or read territory:** rejected because neither is accountable appointment.
- **Use repository path as stable identity:** rejected because paths can move and do not establish authority.
- **Create a universal fleet repository:** rejected because it adds an authority surface and couples independent child histories.

## Reversal triggers

Reopen this decision if Git cannot enforce non-overlap, if an accepted jurisdiction law changes company-agent placement, if child history cannot be preserved, or if the layout would require authority to be inferred from a locator. A preference for fewer repositories is not by itself a reversal trigger.
