---
summary: "Proposed target texts for the AGENTS.md chain (AK 8631, revision 2 after the independent check): complete proposed wording per file. Nothing is applied."
read_when:
  - "You decide on or apply the proposals of AK 8631."
  - "You read section 5 of 2026-11-14-agents-chain-audit-ak8631.md."
type: "proposal"
status: "proposal, revision 2; not applied; each file needs its owner's approval"
---

# Proposed target texts for the AGENTS.md chain (AK 8631, revision 2)

Section 5 of `2026-11-14-agents-chain-audit-ak8631.md`. Rules followed: one fact in one place; a file
states only what holds for everything below it; the company file adds company context; no history;
imperative sentences; no rule that is needed is lost (audit section 7). Each block is the complete
proposed file. Figures are characters (`wc -m`), today to proposed. The texts are written as if
owner choices 3 and 6 were answered A; the choices stay open, and the notes say what changes otherwise.

## 5.1 `AGENTS.md` (root): 9,779 to 8,709

````markdown
# AGENTS.md — ai-society

Holds for every session below `~/ai-society`. Paths resolve from there unless absolute.
Each lower AGENTS.md (company, lane, repo) adds only what is specific to it. The order in which the
files are loaded creates no precedence; the owner table is the authority boundary. Before you change
anything outside the folder chain you started in, read the AGENTS.md chain of the target or start a
session at the target's root.

## Owners
| Concern | Owner surface |
|---|---|
| Tasks, direction, decisions, evidence | Agent Kernel (`ak`) + society.v2.db |
| Reusable prompts/procedures | Prompt Vault |
| Ontology / controlled semantics | ROCS owner repos |
| Operator workbench / extension UX | Pi runtime / pi-extensions |
| Empirical behavior analysis | Oracle / DSPx |
| Learnings and activation | KES / docs/learnings / AK knowledge |
| Steward explanation and publication | steward/publication owners |
| Templates and their rollout | template owner repos (`core/tpl-template-repo`) and propagation |

Never absorb one owner surface into another. Hand off explicitly.

## Work and authority
- Before acting, orient: `git log` and `git status` since the last session in every repo you will
  touch, `ak task show` for each task (including `broken_commitments`), and the peer sessions busy in
  that repo (Claude Code: ListAgents). Tell them before a build or e2e run.
- Work one exact AK task: claim it, keep evidence in the result JSON, release the claim before you
  stop. The task id is your execution authority; do not broaden it.
- Author task scope in AK and freeze it for a repo with `ak task scope export <id>`. Files
  `governance/task-scopes/AK-*.snapshot.json` are exports; never edit them by hand.
- Record deferred work as an AK task, not as a TODO comment, a local queue or a checked-in
  work-items file.
- `proceed` or `go ahead` continues the active task. It does not authorize lifecycle closeout,
  source-owner mutation, publication or knowledge promotion. A closeout or readiness row is an input
  to a decision, not an authorization.
- Ask before push, deploy, publication, device actions and changes to another owner's surface.
  A local commit grants none of them.
- Where the AK decision workflow has landed, `ak decision list` and `ak decision passport` are the
  runtime authority. RFCs, ADRs, docs, task-scope snapshots and direction exports are projections.
- Where AK has not landed, use the repo's declared process. If there is none, stop and route the gap
  to the repo owner.
- Where a repo declares AK-native direction, do not revive `strategic_goals.md`, `tactical_goals.md`
  or `operating_plan.md`; they are archive. `docs/project/vision.md` is durable product direction and
  `docs/project/product_posture.md` a maturity bridge; neither is a queue, a roadmap or execution
  authority.
- Fix must-fixes and adopt recommendations without asking. Settle open questions with
  many-of-the-greats (`~/.pi/agent/prompts/many-of-the-greats.md`). Bring only value or ownership
  choices to the operator, as multiple choice with a recommended option.
- Reason broadly; change only the surface that owns the fact, with its preflight. If the operator
  calls your scope stale, pause and correct the plan first.
- Work in the repo of your start folder. Inspect another repo only when the operator names it or the
  task belongs there. If the repo is unclear, use a router: the skills
  `softwareco-owned-repo-router`, `softwareco-infra-repo-router`, `softwareco-contrib-repo-router`,
  `ai-society-core-repo-router`, or the holdingco capability map. A router's answer is a hint;
  confirm in the chosen repo's own docs before you implement.

## Safety
- No secrets in git.
- Work inside a component repo. Change the workspace root, a company root or a lane root only for
  work that belongs to that folder itself.
- Honor `TMPDIR`. Never use `/tmp` for clones, worktrees, builds, caches or large output.
- Delete only scratch you own and can prove inactive.
- State with no live owner (a lock no process holds; uncommitted work, stashes, branches or processes
  untouched for 30 days with no active AK task): move it to a quarantine and record that in AK.
  Never delete it.

## In every repo
- Prefer a repo command (`just <recipe>`, `./scripts/rocs.sh`, a repo script) to an ad-hoc script.
  Write inline Python only when no such command exists.
- Do not edit `docs/_core/**`.
- Keep `.copier-answers.yml` committed.
- Write session notes to the repo's own `diary/`. Move what lasts to `docs/learnings/` and
  `docs/decisions/`; propose a TIP when a pattern holds beyond the repo.
- Read the AK task scope first, then only the documents the task needs (docs-list, below). Do not
  read whole documentation folders.
- Before engineering work, read the repo's `docs/engineering.local.md` and
  `policy/engineering-lane.json`; consumer policy is local adoption truth.
- Run the repo's declared checks before merge; repo-owned checks win.
- File budgets: code 500 LOC / 50 KB, tests 1000 / 80 KB, markdown 800 / 60 KB. They are ratchets
  for existing files, enforced by the repo's checks.

## Commands (use exactly)
```bash
# before ANY direct mutation of a workspace database; run from ~/ai-society
./scripts/db-change-preflight.sh --db-path <db-path> --stage db-dev

# every multi-GiB job; /home is nearly full, so select the /data root
AI_SOCIETY_SCRATCH_ROOT=/data/ai-society-scratch heavy-job run --label <label> --task <task-id> -- <command...>

# ROCS, from the target repo; contracts first for an unfamiliar operation
./scripts/rocs.sh contracts

# docs-list, from the target repo; add no wrapper
node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --task "<task>" --top 8
```
All other recipes are in the `ai-society-runtime-recipes` skill.

## Vocabulary card
<!-- BEGIN vocabulary-card (at most 25 lines) -->
One meaning per word in our own text and records; [brackets] say what kind of thing a word names. Keep
identifiers as they are (`fcos gates`, `consent_mode`); quote a source's word with its mapping: "S3 *requirement* (goal)".
- **requirement** [a binding statement]: one verifiable "shall" with an owner. S3 "requirement" → **goal**;
  Binner *Anforderung* → **stakeholder expectation**.
- **decision gate** [an act: a named authority decides against criteria set in advance]; never bare "gate".
  Binner "Gates" → **measuring point**; `fcos gates` → **health checks**; FCOS close → **close gate**.
- **verification** [a check against a requirement or DoD row]; **validation** [fitness for purpose, judged by the
  receiver]. Schema validation → **schema check**; FCOS validation tiers → **test tiers**; replay → **replay check**.
- **authorization** [an act: a sign-off that grants a permission]; **consent** [a state: a consent round ended with
  no objection standing]; **dissent** [a record of a disagreement, kept with the decision]. Never swap them.
- **directive** [a binding rule]; **direction** [AK strategy]; **guidance** [Prompt Vault advice].
- Never bare: **measure** → **action** or **metric**; **model** → **organisation model**, **system model**, **LLM**;
  **baseline** → **commitment baseline**, **plan figures**, **freshness baseline**;
  **review** → readiness / agreement / Leitung / role **review**, conformance / process **audit**, **work-product inspection**.
- **level** [a MITO level with an owner]; NASA product structure → **product layer**; architecture → **Layer-N**.
- **maturity** [how far round the MITO loop a process is institutionalised]; NASA document states →
  **artefact status**; TRL → **technology readiness**.
- **FCOS** is the **coordination board (Leitstand)** [it records, screens and verifies; it never decides], not a
  "control board". FCOS "transition" in prose → **authority migration**; NASA product transition → **handover**.
- **variance** [plan figures vs actuals], not "deviation"; **relief** [release from a rule, by the rule's owner];
  **waiver** [released, commitment unchanged]; **carried obligation**, not "lien", on proceed decisions only.
- **readiness** [preflight or readiness review only]; FCOS "readiness contract" → **item contract**.
- **driver** [a situation that calls for a response]; NASA "design driver" → **dominant constraint**.
- **task claim** (AK) [your commitment to the requester for the lease]: release it when you stop; a lease that
  runs out is a broken commitment. `core.Claim` is different [an assertion].
- **configuration** [control of controlled items]; Binner's organisation sense → **organisation design**.
  **operations** [doing the work]; NASA Phase E → **operations mode**. **plan** = the MITO Input segment.
<!-- END vocabulary-card -->
````

Removed: front matter, the notes to editors (12-14, 17-18, 141-142), the loading mechanics (19-22),
the dates, the card's origin comment. The notes to editors and the loading mechanics, with the hook
`scripts/claude-agents-chain-hook.mjs`, must first be written into the skill
`agents-layering-and-codification`, which does not hold them today.
Moved up from lower files, each a rule that already stands in several of them:
- template row in the owner table (agent-kernel:92, nodecode-cells:37, informatik:37);
- task scope and its snapshot files (owned:24, informatik:30, adoption-steward:12);
- deferred work as AK task, no work-items file (owned:23, infra:28, contrib:10, fork:26, informatik:29);
- closeout and readiness rows; no revival of SG/TG/OP; vision and product posture (informatik:35,
  38-39, adoption-steward:24, 26, `copier/tpl-agent-repo/AGENTS.md.j2:28, 31-32`);
- "a local commit grants none of them" (teachingco:12);
- "a router's answer is a hint" (owned:35) and the contrib router, which exists and was not named;
- the section "In every repo": repo command and inline Python (softwareco:37-39), `docs/_core`
  (contrib:9, fork:25), `.copier-answers.yml` and `diary/` (softwareco:24-25), learnings and TIP
  (contrib:17-28), bounded reading (owned:37-44). Owner choice 6 decides whether the first four stay
  here or go back into each company file.
Kept on purpose in two places: "release the claim" stands in the work rules and in the card, because
the card's wording is fixed by owner decision and defines the term. Heavy-job and the DB preflight now
stand once, with their command. No new rule.

## 5.2 `softwareco/AGENTS.md`: 3,563 to 1,251

````markdown
# AGENTS.md — softwareco

softwareco is the product-engineering company of ai-society. Company documents: `docs/org/`.

## Lanes
| Folder | Holds |
|---|---|
| `owned/` | repos softwareco builds and operates |
| `infra/` | platform, runbooks, internal infrastructure |
| `contrib/` | repos coupled to an upstream we contribute to |
| `fork/` | forks that diverge from their upstream on purpose |
| `softwareco-agents/` | contract, registry and role cards for softwareco's agents |
| `ontology/` | softwareco's ROCS ontology |

Each lane and each repo below it is its own git repo. Pick the lane first, then follow its file.

## Rules for every softwareco repo
- Commit to `main`. Open a GitHub PR only for a release or when the operator asks for one.
- If a repo keeps direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`),
  update them in the same pass as the task that changes direction, or bind the follow-up as an AK
  task. Link tasks and decisions as `task:` / `decision:`. Run `ak direction import` when the docs
  changed, then `ak direction check`.
- For a shallow status of many repos, run `./scripts/preflight-repo-census.sh [scope]`.

To create a repo or a lane from a template, read `README.md` of this folder.
````

The first sentence is from `docs/org/purpose.md:18`. New, a statement of fact: "Each lane and each
repo below it is its own git repo" (checked with `git rev-parse` in each lane and both sample repos).
The `softwareco-agents/` row depends on owner choice 1 (under C it reads `agents/`). The
direction-docs rule joins infra:29-31, fork:28-30 and contrib:40-42 in one place. Templates, lane
bootstrap and recursion policy stay in `README.md:46-80, 266-272`.

## 5.3 Lanes

`softwareco/owned/AGENTS.md`: 3,311 to 396

````markdown
# AGENTS.md — softwareco/owned

- Use the repo's `Justfile`; `just help` lists its recipes. If a repo has none, set it up after
  `docs/project/standardized-justfile-contract.md` of this lane.
- At the lane root only: engineering-core adoption coverage runs through
  `./scripts/engineering-core-adoption-scan.sh`. The dashboard and snapshot files it writes are
  projections owned by this lane.
````

`softwareco/infra/AGENTS.md`: 1,887 to 92; `softwareco/contrib/AGENTS.md`: 1,660 to 94

````markdown
# AGENTS.md — softwareco/infra

This lane adds no rule; the root and softwareco files hold.
````

Every rule of these two files now stands in the root or the softwareco text. The lane template
requires the file to exist; if its owner drops that, the file can go. Contrib repos may carry their
upstream's AGENTS.md (`beads_rust` 54,145 bytes, `beads_viewer` 45,869 bytes); revision 1 proposed a
precedence rule for them, which is withdrawn (owner choice 5).

`softwareco/fork/AGENTS.md`: 2,595 to 128

````markdown
# AGENTS.md — softwareco/fork

- Record in the fork's `docs/decisions/` why the fork exists and which upstream boundary failed.
````

## 5.4 `softwareco/softwareco-agents/AGENTS.md`: 694 to 685

````markdown
# AGENTS.md — softwareco-agents

This repo holds the contract, the registry and the role cards for softwareco's agents.

- Before you create or change an agent, read `docs/agent-registry.md` (creation needs an exact AK
  task) and `docs/agent-operating-contract.md`.
- One repo prepares one agent. A repo or a registry row grants no authority and appoints nobody.
- An agent is advisory by default. Its persona may narrow this, never broaden it.
- An agent proposes; the human executes real-world actions.
- An agent writes to another repository only under an exact active AK task owned by that repository.
- State an agent's behaviour explicitly: triggers, invariants, failure modes.
````

Sources: "grants no authority" `docs/agent-registry.md:9-17`; "appoints nobody"
`agents/agent-adoption-steward/AGENTS.md:4`; "advisory by default" and "writes to another repository"
`copier/tpl-agent-repo/AGENTS.md.j2:14, 17`; "the human executes" today's line 8. The file names no
role and no holder; the appointment is the mycel role record (roles synthesis, point 2).

Pattern for an agent repo (source `copier/tpl-agent-repo/AGENTS.md.j2`, 4,858 bytes today):
501 plus the agent's own rules

````markdown
# AGENTS.md — agent-<name>

This repo prepares the agent <name> for softwareco. `agent.json` and
`docs/person/system-prompt.md` are its executable identity; keep the rest of the repo consistent
with them.

- Find your delegation in AK and in the role record. If it is missing, expired or unclear, stop and
  escalate.
- Refresh from the template plan-first: read the plan of `./scripts/propagate-template.sh`, then run
  it again with `--apply`.
- <rules that hold for this agent only, one line each>
````

The pattern assumes the file above it is loaded (owner choice 1, B or C). Under A it is not; then the
five rule lines of the file above join the pattern (about 480 characters).

## 5.5 `softwareco/owned/nodecode-cells/AGENTS.md`: 2,127 to 1,324

````markdown
# AGENTS.md — nodecode-cells

A family of native Nodecode cells. Autoresearch is the first cell. Pi's implementation is a
reference, not a required workflow.

- Products live in `cells/<primary-asdf-system>/`. No nested git repositories.
- ASDF is the only dependency and build contract. Allowlist each maintained system; do not register
  references, templates or other ASDF definitions recursively. Exception (owner decision A, AK 8235):
  `cells/xeno-lab/` may hold a Bend kernel (pinned compiler) and a Rust member (cargo) whose checks
  join `just ci`.
- Use the host's own lifecycle, settings, tools and UI. Do not build a parallel platform.
- Loading code must be inert. Record cleanup at acquisition and observe actual quiescence.
- Replace changed source with a fresh process; do not presume hot-unload is safe.
- Selected-folder installation, coexistence and lifecycle each need their own evidence.
- Do not extract a shared runtime kit until two real consumers justify it.
- Never describe tests of fake adapters or synthetic observations as real campaigns.
- Do not claim AK adoption from a document.
- Keep policy at the repo root; add guidance to a member only where it deviates.
- Before implementation, read `docs/project/product_posture.md`.
- Ask before installing into a real profile or promoting a cell.
````

## 5.6 `softwareco/owned/agent-kernel/AGENTS.md`: 20,606 to 5,539

````markdown
# AGENTS.md — agent-kernel

AK is the local runtime that holds ai-society's coordination state. The active database (`AK_DB`,
default `~/ai-society/society.v2.db`) is the source of truth; YAML, JSON and markdown files are
projections unless a surface says otherwise.

Axioms: one canonical record per concern. Identical queries and checks give identical results. L2
repos cannot weaken L1 constraints. Every pass/fail decision emits machine-checkable evidence.

## Never
- Never invoke the `ak` binary directly. Every call goes through `scripts/ak-runtime-gate.sh`, which
  checks the binary digest against `policy/ak-runtime-access.json`.
- Never open the live database with `./scripts/fsqlite.sh`, `sqlite3`, Python `sqlite3` or a dev
  build. Inspect copies.
- Never source `.ak-env`, select a checkout binary or restore the database main file alone. Never
  combine a restored main file with a newer WAL.
- Never add an FCOS surface. AK does not import, parse, evaluate, select, project, mutate or repair
  FCOS state (Decision 129); a tripwire test pins every site.
- Never recreate `docs/project/strategic_goals.md`, `tactical_goals.md` or `operating_plan.md`.
  Before further cleanup of the legacy direction archive, run
  `python3 scripts/ci/check-direction-legacy-markdown-readiness.py --require-ready`.
- Never run `ak repo delete --force`, and never delete or replace `society.v2.db`, without a separate
  authorization. Recovery is from backup only.
- Never clear a fence marker you did not set.
- Never copy live database state into a document when a command can query it.

## Direction and tasks
- Authority by surface: tasks `ak task`; direction `ak direction` (read with `ak strategy list
  --repo .` and `ak wave list --repo .`); packets `ak packet`; decisions `ak decision`; evidence
  `ak evidence`. Reconcile with `ak direction check --repo . --machine`. For direction, packet,
  decision or wave work, read `docs/project/layer-12-protocol.md`.
- Bounded mutation is not bounded thinking. For strategic-frame, closeout, activation or
  cross-domain work, reason broadly before you choose the next bounded change. A broad
  implementation wave is valid when it is cohesive, bounded by acceptance criteria and checked
  truthfully.
- When a wave needs its next route, read `docs/project/product-posture.md` and the open-frame status,
  then create or select the concrete execution task and link it as `execution_task`. Do not create an
  "await route" task. Wait for the operator only on real ambiguity or risk; then name the recommended
  route and the exact decision needed.
- For a non-trivial task, set the done contract early (`ak task contract set-done`,
  `set-guardrails`), use `ak task reconcile open|close` when planned and actual scope diverge, and run
  `ak task close-check <id> -F json` before completion. close-check is advisory; when you accept a
  gap, record why in the evidence.
- After a task lifecycle or direction-link change, run `python3 scripts/render-direction-explorer-mvp.py`
  and then the same with `--check`, or record that the refresh is deferred.
- `governance/work-items.json` is a projection; the DB wins. `ak work-items` is deprecated.
- Release your own claim with `ak task unclaim <id> --agent <session> --reason '<why>'`. Return an
  expired claim with `ak task release-expired --task <id> --agent <session>`, after `--dry-run`.

## Publication
- Merging to local `main` deploys everything the main checkout serves: `scripts/ak-runtime-gate.sh`,
  the policy, `validate.sh`, hooks and this file. Only `docs/`, `diary/`, `tests/` and `README.md`
  are inert.
- For any other change, run the fast and full checks, then prove the exact commit on ak-dev before
  merge or push: `ak-dev prove --task <id> --candidate <clean worktree at the commit> --scenario
  '<its tests>'` (`docs/project/ak-dev.md`). The pre-push hook refuses a live commit without its
  proof note.
- Stage only what you changed, by exact path.

## Code
- Run cargo only through `./scripts/cargo-operator.sh <cargo args>`. After code changes run
  `./scripts/validate.sh --quiet-success fast`; before a commit run it with `full`. During an
  admission hold it exits 75; run it again after the hold.
- Rust edition 2024, nightly toolchain, `#![forbid(unsafe_code)]`.
- Async: asupersync, never tokio. Every async function takes `&Cx` first. Cancellation is a
  protocol, not a flag.
- Schema: `crates/ak-core/src/db.rs`. Migrations are additive first. Backend compatibility stays in
  `crates/ak-db`.
- Multi-statement writes use `with_transaction` or `with_transaction_immediate`. Every write returns
  or records evidence.
- JSON: `parse_json_or_warn` on read paths, `parse_json` / `parse_json_opt` on write paths.
- An enum that fails to parse is an error: no `.unwrap_or_default()` for archetype, layer or status.
- Lease duration is 1–86400 seconds. Always set `lease_expires_at` on claim.
- After a failed atomic operation do not re-fetch; return what you know.
- Version fields auto-increment. Canonicalize repo-scoped inputs before authority use. Compare audit
  timestamps with the shared parsed-time comparison.

## Incidents
- Emergency brake: `scripts/ak-runtime-fence.sh --live set --reason '<why>'`. It does not stop
  task-session routes. Within 60 minutes publish a bounded fence or clear it.
- Stuck claim, model-search regression, failed migration, disaster recovery, backup: follow
  `docs/project/database-incident-response.md` and `docs/project/database-backend-runtime.md`. Do not
  improvise.
````

Preconditions, to be done before the cut: write the recovery procedures and backup notes (291-332)
into `docs/project/database-incident-response.md`, and known backend debt (277-289) and the adapter
layer (334-351) into `docs/project/database-backend-runtime.md`; neither document carries them today.
FCOS schema detail (72-80) stays in the Decision 129 documents it cites. This file is live on merge by
its own rule (line 171), so the change needs the ak-dev proof of that rule.

## 5.7 `teachingco/AGENTS.md`: 4,364 to 458

````markdown
# AGENTS.md — teachingco

teachingco holds the teaching work: one monorepo per subject (`mathe/`, `nt/`, `wib/`,
`informatik/`) and class material.

- No pupil data anywhere: not in git, tests, examples, artifacts or messages to other sessions. Use
  abstract groups and invented words, never a class.
- Commit to local `main`. Git workflow and approval rules: `CONTRIBUTING.md`.

To create a repo or a lane from a template, read `README.md` of this folder.
````

The first sentence describes the folders as they are; the owner's purpose sentence replaces it
(request 4).

Pattern for the subject repos, shown for `teachingco/mathe/AGENTS.md`: 2,767 to 628

````markdown
# AGENTS.md — mathe

Monorepo for the subject Mathematik.

- `packages/` holds libraries, `apps/` holds deployables. Neither has its own `.git`.
- Freeze task-scope snapshots at the monorepo root, never in a package or an app.
- Package manager: uv. The workspace is configured at the root; a member's pinned lane command is
  in its `policy/stack-lane.json`, its local deltas in its `docs/tech-stack.local.md`.
- Commit with `.pi/prompts/commit.md`. Scope: the package name, the app name, or `root`,
  `monorepo`, `ci`, `docs`, `release`.
- For a shallow status of many repos, run `./scripts/preflight-repo-census.sh [scope]`.
````

`nt`, `wib` and `informatik` take the same text with their subject and with
`policy/engineering-lane.json` and `docs/engineering.local.md` as the file names.

## 5.8 `~/ai-society/agents/*`

The four old repos (health, triage, consent-steward, pilot) carry the unfilled template text and the
retired GitLab. `softwareco-agents/docs/legacy-agent-backfill.md` owns their backfill; they take the
agent-repo pattern then. `agent-adoption-steward` keeps lines 4-6 and 15-19 and loses the rest
(4,308 to about 1,300).
