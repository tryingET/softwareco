---
summary: "Audit of the AGENTS.md instruction chain below ~/ai-society (AK 8631): what each file says, what is duplicated, contradictory or dead, and a proposed target text per file. Nothing is applied."
read_when:
  - "You are about to change an AGENTS.md file or an AGENTS.md template below ~/ai-society."
  - "You decide on the proposals of AK 8631."
type: "proposal"
status: "proposal, revision 2 after the independent check; not applied; each file needs its owner's approval (section 9)"
---

# Audit of the AGENTS.md chain (AK 8631)

Producer: nodecode session s-IZD1MTQW, 2026-11-14, commissioned by s-338VQQGH. No instruction file was
changed. Sizes are characters (`wc -m`) of the files as read on 2026-11-14. Line numbers refer to those
files. Revision 2 (2026-11-14) follows the independent check `2026-11-14-agents-chain-audit-ak8631-check.md`
(verdict CONFIRMED-WITH-DIFFERENCES): lost rules restored, order of changes corrected, choice 1 rewritten,
figures measured again. The proposed texts are in `2026-11-14-agents-chain-audit-ak8631-texts.md`; they were
moved out to keep both files within the markdown budget. Revision 2 has not been checked by a second session.

Owner's word (2026-11-14): the AGENTS.md files are to be clear instructions, ordered by hierarchy,
without junk, with added context per company.

## 1. Result in short

1. A session in `nodecode-cells` loads 18,780 characters today. With the proposed texts it loads
   11,680, of which 2,905 are the vocabulary card. Revision 1 claimed 9,847; it
   had dropped rules, which revision 2 restores (section 7).
2. The duplication in lane and repo files is produced by the templates and held in place by a check on
   the templates: `scripts/check-template-ci.sh:439-441` (template source), `1002-1008`, `1272-1278`,
   `1382-1385` (a freshly rendered repo) require "Deterministic tooling policy", `scripts/rocs.sh`,
   `diary/`, "Recursion policy", `policy/engineering-lane.json` and `docs/engineering.local.md`. No
   assertion reads a live repo's AGENTS.md. The company files are company-owned
   (`contracts/template-ownership.yml`, enforced at `check-template-ci.sh:519-521`) and are not
   overwritten by a template update; the root file and `softwareco-agents/AGENTS.md` have no
   `.copier-answers.yml`. So root, company and softwareco-agents files can change first (section 9).
3. Eight instructions contradict each other across files (section 4, C1-C8), among them push to
   `main` without asking (four files) against "ask before push" (root).
4. Four places name where an agent repo lives; they give three answers, and one of the places does
   not exist (C6, section 8 choice 1). This decides which company text a role holder receives.
5. No file on the chain defines a role. `softwareco-agents/AGENTS.md:4` and the four old agent repos
   come closest ("no hierarchy, work via proposals"); the proposed texts say only that a repo
   appoints nobody.
6. `teachingco/AGENTS.md` is the unfilled company template: its four lanes do not exist, three of its
   read-first documents do not exist. Its one company rule (no pupil data, line 15) sits in the middle.

## 2. What is loaded today

Every harness loads the files from `~/ai-society` down to the start folder (root file lines 19-23).

| File | Chars | Lines | Git repo that holds it |
|---|---|---|---|
| `AGENTS.md` (root) | 9,779 | 148 | ai-society |
| `softwareco/AGENTS.md` | 3,563 | 82 | softwareco |
| `softwareco/owned/AGENTS.md` | 3,311 | 44 | softwareco/owned |
| `softwareco/infra/AGENTS.md` | 1,887 | 44 | softwareco/infra |
| `softwareco/contrib/AGENTS.md` | 1,660 | 51 | softwareco/contrib |
| `softwareco/fork/AGENTS.md` | 2,595 | 54 | softwareco/fork |
| `softwareco/softwareco-agents/AGENTS.md` | 694 | 18 | softwareco-agents |
| `softwareco/ontology/AGENTS.md` | 429 | 10 | softwareco-ontology |
| `softwareco/owned/nodecode-cells/AGENTS.md` | 2,127 | 38 | nodecode-cells |
| `softwareco/owned/agent-kernel/AGENTS.md` | 20,606 | 382 | agent-kernel |
| `teachingco/AGENTS.md` | 4,364 | 113 | teachingco |
| `teachingco/{mathe,nt,wib,informatik}/AGENTS.md` | 2,767 / 2,778 / 2,923 / 4,550 | 76-94 | one each |
| `agents/agent-{health,triage}/AGENTS.md` | 668 each | 19 | one each |
| `agents/agent-consent-steward`, `agents/pilot-agent-strict-l2-20260212` | 457 / 574 | 14 / 15 | one each |
| `agents/agent-adoption-steward/AGENTS.md` | 4,308 | 75 | agent-adoption-steward |

Not present: an AGENTS.md at `~/ai-society/agents/`, at `~/ai-society/core/`, a `softwareco/core/`,
a `softwareco/agents/`. No CLAUDE.md or AGENTS.override.md on these chains.
Files the chain makes mandatory and that exist: `docs/engineering.local.md` and
`policy/engineering-lane.json` (checked in nodecode-cells and softwareco-agents), the skills
`ai-society-runtime-recipes` and the three routers, `scripts/db-change-preflight.sh`, `heavy-job`,
`docs-list.mjs`, `~/.pi/agent/prompts/many-of-the-greats.md`.

## 3. Each file, block by block

Kinds: **ALL** rule every session below needs. **SOME** rule only some sessions need. **CTX** context
or a description of the file itself. **HIST** history. **DUP** repeats another place (named).
**CONTRA** contradicts another place (see section 4). **DEAD** points at something that is not there.

### 3.1 `AGENTS.md` (root, 9,779)

| Lines | Block | Kind |
|---|---|---|
| 1-8 | front matter (summary, read_when) | CTX; the file is always loaded, `read_when` selects nothing |
| 12-14 | scope; "keep this file stable and small" | CTX, addressed to editors of the file |
| 17-18 | what each chain file is for | CTX |
| 19-22 | how Pi, Codex and Claude Code load the chain | CTX for editors; SOME |
| 22-23 | read the target chain before mutating outside the loaded ancestry | ALL |
| 24 | render order creates no precedence | CTX |
| 26-37 | owner table; never absorb another owner surface | ALL |
| 39-71 | vocabulary card (3,178 with its comment) | ALL by owner decisions D16, D22, D26 |
| 40-43 | comment on the card's origin | HIST (324) |
| 74 | no secrets in git | ALL |
| 75 | work inside component repos | ALL |
| 76 | DB preflight | ALL; DUP of 127-128 |
| 77-78 | TMPDIR, never /tmp, heavy-job | ALL; DUP of 130-132 |
| 79 | delete only own scratch | ALL |
| 80-82 | ownerless state: quarantine, never delete | ALL; date is HIST |
| 84-86 | reason broadly, mutate narrowly; stale scope | ALL |
| 88-92 | default to cwd repo; router skills | ALL; the skill list is company detail and incomplete (`softwareco-contrib-repo-router` exists, is not named) |
| 94-102 | AK authority, `proceed`, decisions, projections, no-AK case | ALL; 100 has a broken line wrap |
| 104-112 | working loop | ALL; "(operator, 2026-11-02)" is HIST; "(Claude Code: ListAgents)" is SOME |
| 108 | one exact task, claim, evidence, release | DUP of 95-96 and of card 67-68 |
| 114-117 | read engineering.local.md and engineering-lane.json | ALL |
| 119-122 | run declared checks before merge; file budgets | ALL; "enforced by repo validation, not by this file" is CTX |
| 124-139 | four commands | ALL |
| 141-142 | rule for future edits of the block | CTX for editors |
| 144-148 | everything else is in the recipes skill | DUP: the skill is named five times (76, 78, 102, 117, 145) |

The file breaks its own card: "validation" at 2, 119-122 means checks, which the card (50-51) reserves
for "fitness for purpose". Lower files use "gate" for a PR or a check, not for a decision gate:
`softwareco/AGENTS.md:21` ("review gate"), `infra:31`, `fork:30`, `contrib:42`.

### 3.2 `softwareco/AGENTS.md` (3,563)

| Lines | Block | Kind |
|---|---|---|
| 1-7 | front matter | CTX |
| 11-17 | the five lanes | CTX every session needs; `agents/` (16) is DEAD, `softwareco-agents/` and `ontology/` are missing |
| 20-21 | commit to `main`; PR only for release or on request | ALL (company) |
| 22 | pick lane first | SOME (sessions at the company root) |
| 23 | no secrets in git | DUP of root 74 |
| 24 | keep `.copier-answers.yml` committed | ALL (company); 67 of 80 owned repos have one |
| 25 | repo-local `diary/` | ALL (company) |
| 28-30 | docs-list | DUP of root 137-138 |
| 31 | repo census preflight | SOME (company root) |
| 32, 37-38 | rocs launcher, ROCS first | DUP of root 134-135 |
| 33-34 | new repo from template, lane bootstrap | SOME (company root); DUP of `softwareco/README.md:48-75` |
| 39 | inline Python only as escape hatch | ALL (company); repeated in five lower files |
| 41-49 | template table | SOME; DUP of README; 46 `agents/agent-<slug>/` DEAD |
| 51-65 | lane bootstrap commands | SOME; DUP of README 72-75 |
| 67-72 | placement reminders | DUP of 11-17; 71 DEAD |
| 74-82 | recursion policy L0/L1/L2 | SOME (template work); the terms are not explained anywhere on the chain |

### 3.3 `softwareco/owned/AGENTS.md` (3,311)

| Lines | Block | Kind |
|---|---|---|
| 1-7, 11-19 | front matter, scope, "keep this file concise" | CTX about the file |
| 22 | lane-root work here, repo work in the repo | ALL (lane) |
| 23 | deferred work in AK, not TODOs | ALL, but holds everywhere: belongs in root; DUP in infra 28, contrib 10, fork 26 |
| 24 | task scope is authored in AK; snapshots are exports | DUP of root 98-100 |
| 27, 31 | deterministic wrappers; inline Python | DUP of softwareco 37-39 |
| 28 | standard Justfile recipes | ALL (lane); 59 of 80 repos have a Justfile |
| 29 | set up a missing Justfile | SOME; absolute path where a relative one serves |
| 30 | engineering-core adoption scan | SOME (lane root only) |
| 34-35 | capability map; it is a hint | ALL (lane) |
| 38 | "apply the already injected instructions" | CTX |
| 39-42 | task scope first, engineering docs, docs-list, read only what is needed | ALL, but holds everywhere: belongs in root; 40-41 DUP of root 114-117, 137-138 |
| 44 | doc folders are categories, not a reading sequence | CONTRA with infra 37-44, fork 47-54, contrib 44-51 (C3) |

### 3.4 `softwareco/infra/AGENTS.md` (1,887), `fork/AGENTS.md` (2,595), `contrib/AGENTS.md` (1,660)

| File:lines | Block | Kind |
|---|---|---|
| infra 1-22, fork 1-19 | front matter, scope, "stays concise" | CTX about the file |
| contrib 3-4 | "Template for a delivery project repo" | DEAD: unfilled template sentence |
| infra 25, fork 22, contrib 7 | no secrets | DUP of root 74 |
| infra 26-27, fork 23-24 | main-first, PR on request | DUP of softwareco 20-21 |
| contrib 8 | "commit to `main` and push to `main`" | CONTRA with root 111-112 (C1) |
| contrib 9, fork 25 | `docs/_core/**` immutable | ALL; same line in nodecode-cells 33, mathe 19: belongs one step up |
| infra 28, contrib 10, fork 26 | deferred work in AK | DUP (see owned 23); fork 26 carries Decision 127 as HIST |
| infra 29-31, fork 28-30 | SG/TG/OP direction docs, typed refs, `ak direction check` | SOME: 5 of 27 infra repos, 1 of 16 fork entries have the files; CONTRA in tendency with agent-kernel 121 (C4) |
| contrib 40-42 | `ak direction import/check/export` | SOME: 0 of 314 contrib entries have `strategic_goals.md` |
| fork 27 | record why the fork exists | ALL (lane) |
| infra 34-35, fork 33-34, contrib 13-15 | wrappers, ROCS first, inline Python | DUP of softwareco 37-39 |
| fork 36-45 | when to use `fork/` | SOME (needed when choosing a lane, so above this file); DUP of softwareco 11-17 |
| contrib 17-28 | knowledge crystallization flow, "weekly" promotion | SOME; no session runs weekly; DUP of softwareco 25 in part |
| contrib 30-37 | recursion policy | DUP of softwareco 74-82 |
| infra 37-44, fork 47-54, contrib 44-51 | fixed read order through whole folders; own AGENTS.md last | CONTRA (C3); item 7 is CTX, the file is already loaded |

### 3.5 `softwareco/softwareco-agents/AGENTS.md` (694), `softwareco/ontology/AGENTS.md` (429)

| File:lines | Block | Kind |
|---|---|---|
| agents 4 | "how agents propose work, coordinate by consent ... without hierarchy" | CTX; describes an organisation design the chain should not carry |
| agents 7 | no secrets | DUP of root 74 |
| agents 8 | "work is proposals + MRs; you (human) executes real-world actions" | CONTRA with softwareco 20-21 (C2) |
| agents 9 | triggers, invariants, failure modes | ALL (this repo) |
| agents 11-14 | NAS GitLab through `gl-nas`, `gl-nas-git` | DEAD: neither command is on PATH; `ontology/AGENTS.md:10` says the NAS GitLab is retired (AK 6118) |
| agents 17-18 | references | 18 DEAD (`holdingco/holdingco-templates` missing); 17 CTX |
| ontology 3-7 | rocs commands, concept-level retrieval | ALL (this repo) |
| ontology 9-10 | the check command; remote; "NAS GitLab is retired (AK 6118)" | ALL; last clause HIST |

### 3.6 `softwareco/owned/nodecode-cells/AGENTS.md` (2,127)

| Lines | Block | Kind |
|---|---|---|
| 1-6 | front matter | CTX |
| 11-12 | purpose | CTX every session needs; "Pi's implementation informs the ambition" HIST |
| 15-24 | structure and native boundaries | ALL (repo); "(owner decision A, 2026-11-03, AK #8235)" HIST |
| 27 | engineering.local.md, policy projection | DUP of root 114-117; `product_posture.md` is the repo's own |
| 28 | `just help` | DUP of owned 28 |
| 29-30 | fake adapters are not real campaigns; root policy stays at the root | ALL (repo) |
| 33 | no secrets; `docs/_core/**` immutable | DUP of root 74, contrib 9 |
| 34 | work on `main`; publication, real-profile installation, promotion need authorization | DUP of softwareco 20 and root 111-112; real-profile installation is the repo's own |
| 35-37 | AK owns tasks; owner boundaries | DUP of root 26-37, 94-102 |
| 38 | "this bootstrap authorizes repository creation" | HIST |

### 3.7 `softwareco/owned/agent-kernel/AGENTS.md` (20,606)

| Lines | Block | Kind |
|---|---|---|
| 12-15 | runtime gate: never call the binary directly | ALL (repo) |
| 17-21 | intent | CTX every session needs |
| 23-30 | six axioms | CTX; 30 DUP of root 26-37 |
| 32-55 | reasoning breadth vs mutation scope | DUP of root 84-86, expanded to 2,000 characters |
| 59-66 | runtime authority per `ak` command family | SOME; 66 `ak work-items` deprecated: CONTRA with teachingco 21, 27 (C5) |
| 70-80 | FCOS boundary | ALL (repo) as one rule; schema 43/46 detail and AK numbers HIST |
| 82-92 | owner table | DUP of root 27-35, two more rows |
| 96-117 | direction commands | SOME |
| 119-128 | direction rules, no route-wait | ALL (repo); 122-124 HIST |
| 130-143 | exact task vs strategic frame | DUP of root 94-96, 108 |
| 145-165 | done contract, reconcile, close-check | ALL (repo) |
| 169-174 | publication: `main` is live, prove on ak-dev | ALL (repo) |
| 176-187 | Rust rules | ALL (repo); 183-185 compatibility wrappers SOME |
| 189-205 | async, database rules | ALL (repo) |
| 207-213 | pointer to backend doc | CTX |
| 215-224 | code health invariants | 1 and 5 DUP of 192, 201-203; 222 timer history HIST |
| 226-251 | common commands | DUP of 179-182; task commands DUP of the recipes skill |
| 253 | workspace DB preflight | DUP of root 76, 127-128; names `society.db`, root names `society.v2.db` |
| 255-264 | read order through five source files | CONTRA with the bounded reading rule (C3) |
| 266-275 | cognitive tools | DUP of 32-55 |
| 277-289 | known backend debt | HIST / status; the file itself says the canonical place is `database-backend-runtime.md` |
| 291-332 | recovery procedures, backup | SOME (incidents); 295 and 325-328 are ALL (repo) |
| 334-351 | adapter layer, code sample | CTX |
| 353-369 | template layer context | CTX; 360 `softwareco/tpl-owned-repo` DEAD |
| 371-380 | "no GitLab required" | HIST |
| 382 | never open the live DB with another engine | ALL (repo), placed last |

### 3.8 `teachingco/AGENTS.md` (4,364) and the subject repos

| File:lines | Block | Kind |
|---|---|---|
| teachingco 3-8 | lanes `owned/`, `contrib/`, `infra/`, `agents/` | DEAD: none exists; the folders are `mathe/`, `nt/`, `wib/`, `informatik/` and material |
| 11-12 | main-first; do not infer push permission | ALL (company); 12 DUP of root 111-112 |
| 13 | pick lane first | DEAD (no lanes) |
| 14 | no secrets | DUP of root 74 |
| 15 | no pupil data anywhere | ALL (company): the one teachingco rule |
| 16 | `.copier-answers.yml` | ALL (company) |
| 19-20 | docs-list | DUP of root 137-138 |
| 21, 27 | `ak` for repos with `governance/work-items.json`; `ak work-items` | CONTRA (C5) |
| 22, 28-30 | rocs, inline Python | DUP of root 134-135; as softwareco 37-39 |
| 23-24, 32-81 | templates, lane bootstrap, creating repos | SOME (company root); DUP of `teachingco/README.md:14-18` in part |
| 83-87 | placement reminders | DEAD |
| 89-92 | read `docs/lane-policy-matrix.md`, `repo-placement-policy.md`, `archetype-lane-crosswalk.md` | DEAD: none exists |
| 94-103 | knowledge crystallization flow | SOME |
| 105-113 | recursion policy | SOME (template work) |
| mathe/nt/wib/informatik 3-4, 10-11 | "Template for a monorepo workspace" | DEAD: unfilled template sentence |
| mathe 6-14 | folder list | CTX |
| mathe 17, 19, 22 | no secrets; `docs/_core`; deferred work in AK | DUP of root 74, of the company rule, of owned 23 |
| mathe 18, nt 18, informatik 25 | "commit to `main` and push to `main`" | CONTRA (C1); wib 18-19 is already corrected |
| mathe 20-21 | packages and apps have no `.git` | ALL (repo) |
| mathe 24-28 | ROCS first, inline Python | DUP |
| mathe 30-37 | uv; stack contract files | ALL (repo); mathe names `stack-lane.json`, nt/wib/informatik name `engineering-lane.json` |
| mathe 39-44 | commit prompt and scopes | ALL (repo) |
| mathe 46-57, 59-66 | crystallization flow, recursion policy | DUP of teachingco 94-113 |
| mathe 68-76 | read order through all folders incl. `packages/`, `apps/` | CONTRA (C3) |
| informatik 32-39 | AK-native route guardrails | DUP of root 94-102, 26-37 |

### 3.9 `~/ai-society/agents/*`

| File:lines | Block | Kind |
|---|---|---|
| health, triage, consent-steward, pilot 3-4 | "Template for an agent repo: ... no hierarchy, work via proposals + merge requests" | DEAD: unfilled template sentence |
| same 7 | no secrets (GitLab CI variables, 1Password) | DUP of root 74 |
| same 8 | "never push to `main`; open branches + MRs" | CONTRA with adoption-steward 10 (C2) |
| same 9 | `docs/_core/**` immutable | ALL |
| health, triage 11-14 | NAS GitLab | DEAD (see 3.5) |
| same 16-19 | read order | SOME |
| adoption-steward 4-6 | what the repo is; "does not appoint the agent to an organizational role" | CTX every session needs; matches the roles synthesis |
| adoption-steward 9-12 | secrets, main-first, `docs/_core`, task scope | 9 DUP root 74; 12 DUP root 98-100 |
| adoption-steward 15-19 | delegation, WIP, outcome, effect | ALL (repo) |
| adoption-steward 22-26 | AK-native route guardrails | DUP of root 94-102, 26-37 |
| adoption-steward 28-35, 37-39, 41-46, 48-57, 59-66, 68-75 | scope export, ROCS, stack contract, Prompt Vault, crystallization, recursion, read order | DUP of root or template text |

## 4. Contradictions and duplicates across files

### Contradictions

| # | One place | Other place | Proposed resolution |
|---|---|---|---|
| C1 | `softwareco/contrib/AGENTS.md:8`, `teachingco/mathe/AGENTS.md:18`, `teachingco/nt/AGENTS.md:18`, `teachingco/informatik/AGENTS.md:25`: "commit to `main` and push to `main`" | root `AGENTS.md:111-112`: push is asked for; `teachingco/AGENTS.md:12`; `teachingco/wib/AGENTS.md:18-19` | Root holds. Remove the four lines. |
| C2 | `softwareco/softwareco-agents/AGENTS.md:8` "work is proposals + MRs"; `agents/agent-health/AGENTS.md:8` (and triage, consent-steward, pilot) "never push to `main`; open branches + MRs" | `softwareco/AGENTS.md:20-21` main-first; `agents/agent-adoption-steward/AGENTS.md:10` main-first | Owner choice 2. |
| C3 | `softwareco/infra/AGENTS.md:37-44`, `fork:47-54`, `contrib:44-51`, `teachingco/mathe:68-76`, `agent-kernel:255-264`: read these folders in this order | `softwareco/owned/AGENTS.md:37-44`: task scope first, then only what the task needs; folders are categories, "not a mandatory ingestion sequence" | The owned wording is the newer one and agrees with root 137-138. It moves to the root file; the fixed orders go. |
| C4 | `softwareco/infra/AGENTS.md:29`, `fork:28`: update `strategic_goals.md`, `tactical_goals.md`, `operating_plan.md` | `agent-kernel/AGENTS.md:121`, `teachingco/informatik/AGENTS.md:39`, `agent-adoption-steward:26`: do not revive them | No clash in the letter (the lane rule is conditional). The "do not revive" half goes to the root, the conditional "keep them current" half once to the softwareco file. |
| C5 | `teachingco/AGENTS.md:21, 27`: use `ak work-items import/export/check`, repos "that ship `governance/work-items.json`" | `agent-kernel/AGENTS.md:66`: the surface is deprecated since 2026-08-22; `fork/AGENTS.md:26`: the mirror is retired (Decision 127); `teachingco/mathe/AGENTS.md:22`: no such projection exists | Remove both teachingco lines. |
| C6 | `softwareco/AGENTS.md:16, 46, 71`: agent repos at `softwareco/agents/agent-<slug>` (folder does not exist) | `softwareco/softwareco-agents/docs/agent-registry.md` (Boundary): at `ai-society/agents/agent-<name>`; AK 8630 is registered on `softwareco/softwareco-agents` | Owner choice 1. |
| C7 | root `AGENTS.md:50-51` (card): "validation" means fitness for purpose; `:48` a gate is a decision gate | root `AGENTS.md:2, 119-122` "validation" for checks; `softwareco/AGENTS.md:21` "review gate"; `infra:31`, `fork:30`, `contrib:42` "authority-reconciliation gate" | The proposed texts say "checks" and avoid both words. |
| C8 | `agent-kernel/AGENTS.md:253`: `society.db` | root `AGENTS.md:127`: `society.v2.db` | Removed with the duplicate. |

### Duplicates (one fact, many places)

| Fact | Places | Proposed single place |
|---|---|---|
| No secrets in git | root 74; softwareco 23; infra 25; contrib 7; fork 22; softwareco-agents 7; nodecode-cells 33; teachingco 14; mathe/nt/wib 17; informatik 24; all five `agents/*` | root |
| Deferred work is an AK task | owned 23; infra 28; contrib 10; fork 26; mathe 22; informatik 29 | root (it is not there today) |
| `proceed` continues, authorizes no closeout | root 96-98; informatik 34; adoption-steward 23 | root |
| Owner boundaries | root 26-37; agent-kernel 30, 82-92; nodecode-cells 37; informatik 37; adoption-steward 25 | root |
| Exact task, do not broaden | root 95-96, 108; agent-kernel 130-141 | root |
| Reason broadly, mutate narrowly | root 84-86; agent-kernel 32-55, 266-275 | root |
| Task-scope snapshots are AK exports | root 98-100; owned 24; informatik 30; adoption-steward 12 | root |
| docs-list, no wrappers | root 137-138; softwareco 28-30; teachingco 19-20; owned 41 | root |
| ROCS launcher, ROCS first | root 134-135; softwareco 32, 37-38; infra 34; contrib 13-14; fork 33; teachingco 22, 28-29; mathe 25, 27 | root |
| Inline Python only without a command | softwareco 39; owned 31; infra 35; contrib 15; fork 34; teachingco 30; mathe 28; adoption-steward 39 | root (owner choice 6) |
| Main-first | softwareco 20-21; infra 26-27; fork 23-24; nodecode-cells 34 | company |
| `docs/_core/**` immutable | contrib 9; fork 25; nodecode-cells 33; mathe 19; all `agents/*` | root (owner choice 6; 64 of 80 owned repos have the folder) |
| Engineering docs before engineering work | root 114-117; owned 40; nodecode-cells 27 | root |
| DB preflight | root 76, 127-128; agent-kernel 253 | root |
| Scratch and heavy jobs | root 77-78, 130-132 | root, once as rule, once as command |
| Recursion policy | softwareco 74-82; contrib 30-37; teachingco 105-113; mathe 59-66; adoption-steward 59-66 | template documentation (README), not the chain |
| Crystallization flow | contrib 17-28; teachingco 94-103; mathe 46-57; adoption-steward 48-57 | root, two sentences (owner choice 6) |
| Templates and lane bootstrap | softwareco 33-34, 41-65; teachingco 23-24, 32-81; `softwareco/README.md:48-75` | README |

## 5. Proposed target text per file

The complete proposed wording per file, with sources and preconditions, is in
`2026-11-14-agents-chain-audit-ak8631-texts.md` (sections 5.1 to 5.8).

## 6. Effect in numbers

Characters loaded at session start, start folder inclusive. "Proposed" is revision 2, measured on
the blocks of the texts file.

| File | Today | Proposed |
|---|---|---|
| root | 9,779 | 8,709 |
| softwareco | 3,563 | 1,251 |
| owned / infra / contrib / fork | 3,311 / 1,887 / 1,660 / 2,595 | 396 / 92 / 94 / 128 |
| softwareco-agents | 694 | 685 |
| nodecode-cells / agent-kernel | 2,127 / 20,606 | 1,324 / 5,539 |
| teachingco / mathe | 4,364 / 2,767 | 458 / 628 |

| Start folder | Today | Proposed | Change |
|---|---|---|---|
| `softwareco/softwareco-agents/` | 14,036 | 10,645 | -24 % |
| agent repo below softwareco (choice 1 B or C; repo file today as `agent-adoption-steward`, 4,308; proposed pattern plus own rules) | 18,344 | 11,146 | -39 % |
| agent repo at `~/ai-society/agents/` (choice 1 A; pattern plus the five fleet lines, about 480) | 14,087 | 9,690 | -31 % |
| `softwareco/owned/nodecode-cells/` | 18,780 | 11,680 | -38 % |
| `softwareco/owned/agent-kernel/` | 37,259 | 15,895 | -57 % |
| `teachingco/` | 14,143 | 9,167 | -35 % |
| `teachingco/mathe/` | 16,910 | 9,795 | -42 % |

Revision 1 gave 8,596 / 9,020 / 9,847 / 12,932 / 7,677 / 8,135 for rows 1, 2, 4, 5, 6, 7. The
difference is the restored rules: the root text grew from 6,962 to 8,709.
With choice 3 answered B (card on demand) every proposed figure falls by about 2,785.
Choice 6 does not change a session's total inside a company: about 400 characters stand either in
the root or in the company file.

## 7. No needed rule lost

L1-L15 are the checker's findings. L16-L21 were found in this cycle by reading the template
`copier/tpl-agent-repo/AGENTS.md.j2` and the files again.

### Restored

| # | Rule | Now in |
|---|---|---|
| L1 | core router skill and holdingco capability map | root, last work rule (as today, one place for all routers) |
| L2 | templates are an owner surface | root, new row in the owner table |
| L3 | load order creates no precedence; the owner table is the boundary | root, opening paragraph, today's wording. "L2 repos cannot weaken L1 constraints" stays an agent-kernel axiom. The contrib precedence sentence of revision 1 is withdrawn. Choice 5 asks whether the root should say more. |
| L4 | budgets are ratchets enforced by repo checks; repo-owned checks win | root, "In every repo" |
| L5 | readiness script before legacy direction cleanup | agent-kernel, "Never" |
| L6 | every pass/fail decision emits evidence | agent-kernel, axioms |
| L7 | `preflight-repo-census.sh` | softwareco; mathe pattern (the script exists in both) |
| L8 | task scope authored in AK, `ak task scope export`, snapshot path | root, work rules |
| L9 | recovery never-rules; `unclaim`, `release-expired` | agent-kernel, "Never" and "Direction and tasks"; the long procedures are a precondition move (texts 5.6) |
| L10 | no mirrored live DB state; reason for an accepted close-check gap; `layer-12-protocol.md` | agent-kernel |
| L11 | do not claim AK adoption from a document | nodecode-cells |
| L12 | the human executes real-world actions | softwareco-agents |
| L13 | engineering-core adoption scan | owned (kept in the lane file; no precondition) |
| L14 | "or start a session at the target's root"; ListAgents; "since the last session"; "with its preflight"; "consumer policy is local adoption truth"; card markers with "at most 25 lines" | root |
| L15 | decision reference of the xeno-lab exception | nodecode-cells |
| L16 | closeout and readiness rows are inputs, not authorization (informatik:35, adoption-steward:24, template:28) | root |
| L17 | vision is durable direction, product posture a bridge, neither a queue (informatik:38, template:31) | root |
| L18 | do not reintroduce a checked-in work-items file (informatik:29) | root |
| L19 | advisory by default, persona may narrow; writes to another repo need that repo's AK task; template refresh plan-first (template:14, 17, 18) | softwareco-agents; agent-repo pattern |
| L20 | task-scope snapshots at the monorepo root only (informatik:30) | monorepo pattern |
| L21 | bounded mutation is not bounded thinking; a broad wave is valid when cohesive and bounded (agent-kernel:36-38); authority per `ak` surface (59-65); axioms 1-2 (25-26); Pi as reference, not workflow (nodecode-cells:12); learnings and TIP (contrib:25-28) | agent-kernel; nodecode-cells; root |

### Let go, with the reason and who must agree

| Text | Reason it may go | Must agree |
|---|---|---|
| front matter of chain files | the file is always loaded; no script requires it (check D5) | owner of each file |
| root 12-14, 17-22, 141-142: notes to editors, loading mechanics | for editors only; goes after it is written into the skill `agents-layering-and-codification` (not there today, check D6) | owner; owner of the skill |
| root dates and the card's origin comment (40-43, 82, 104) | history; git and the AK decisions D16, D22, D26 keep it | owner |
| softwareco 33-34, 41-82: templates, bootstrap, placement, recursion | stand in `softwareco/README.md:46-80, 266-272`; 46 and 71 are dead | softwareco's owner |
| owned 28-29 recipe list and `pi -p` command; 34 capability map | `just help` prints the list; the command is in the Justfile contract (line 110); the router skills read the map | softwareco's owner |
| fixed read orders (infra, fork, contrib, mathe, agent-kernel 255-264, agents/*) | C3: replaced by bounded reading in the root | owner of each file |
| fork 36-45: when to use `fork/` | needed before a lane is chosen, so not below it; one line stands in the softwareco lane table. The long form may move to `softwareco/README.md` | softwareco's owner |
| "end of session", "weekly" in the crystallization flow | no session runs on a weekly cadence; the flow itself is kept in the root | owner of `core/tpl-template-repo` |
| GitLab NAS, `holdingco-templates` (softwareco-agents 11-18, agents/*) | dead | softwareco's owner |
| "work is proposals + MRs", "never push to `main`" in agent files | open: owner choice 2 | owner |
| agent-kernel 183-185, 226-251 | compatibility wrappers and command lists repeat 179-182 and `ak --help` | owner of agent-kernel |
| agent-kernel 266-275 cognitive tools; template `Cognitive Tools` section | names of thinking tools; the rule they serve is kept (L21) | owner of agent-kernel; template owner |
| agent-kernel 222 (timer), 353-380 (template context, "no GitLab") | history; 360 is dead | owner of agent-kernel |
| agent-kernel 72-80, 277-351 | moved first, not let go (texts 5.6) | owner of agent-kernel |
| nodecode-cells 38 | history of the repo's creation | owner of nodecode-cells |
| teachingco 3-8, 13, 21, 27, 32-92 | dead lanes and documents; C5; templates stand in `teachingco/README.md:14-20, 39-68` | teachingco's owner |

The proposed agent-kernel text no longer uses bare "gate" (check, section 4); it names
`scripts/ak-runtime-gate.sh`.

## 8. Owner choices (all open)

**Choice 1. Where does a company's agent repo live?** Four places speak (C6):
`softwareco-agents/docs/agent-registry.md:9-15` and `copier/tpl-agent-repo/AGENTS.md.j2:11, 15` say
`ai-society/agents/agent-<name>`, "do not nest agents". `softwareco/AGENTS.md:16, 46, 71` say
`softwareco/agents/agent-<slug>`; `softwareco/README.md:44` calls `agents/` "a declared target lane"
that is not materialized and adds that `softwareco-agents/` "must not be silently treated as the
target lane". AK 8630 is registered on `softwareco/softwareco-agents`.

| | A. `~/ai-society/agents/agent-<name>` | B. inside `softwareco/softwareco-agents/` | C. new lane `softwareco/agents/` |
|---|---|---|---|
| Written today in | registry, agent template; five repos are there | nowhere; README:44 warns against assuming it | softwareco AGENTS.md and README (declared, not built) |
| Chain of the holder | root, repo | root, softwareco, softwareco-agents file, repo | root, softwareco, lane file, repo |
| Company text through the chain | no; it must come through the agent's own prompt | yes | yes |
| Characters (proposed) | 9,690 | 11,146 | 11,146, if the lane file carries the fleet rules of texts 5.4 |
| What must change | `softwareco/AGENTS.md:16, 46, 71`, README:44 | registry and template sentences; README:44; a `.gitignore` in `softwareco-agents` (none today) so the nested repo is not seen as untracked; the "do not nest" sentence | registry and template sentences; the lane bootstrap for `agents` (`softwareco/AGENTS.md:51-65`); `softwareco/.gitignore:125-158` is already prepared |
| Nesting | none | agent repos inside a repo that holds documents | lane repo with ignored child repos, as `owned/` |
| AK 8630 | repo is created elsewhere than registered | as registered | lane is created first |

Revision 1 recommended B with the reason that only B delivers the company text; that reason was wrong,
C delivers it as well. **Recommended now: C**, because it is the declared intent, its tooling is
prepared, and it nests nothing inside a document repo; agents that serve all companies stay under A's
folder. B is the cheaper step today. The session holding AK 8630 (s-U3SNXAYW) needs the answer before
it places the repo.

**Choice 2. How does work reach `main` in an agent repo?** (C2; the agent template line 22 also says
"never push to `main`; open branches + MRs")
- A. Main-first, as in every other softwareco repo. **Recommended:** the merge-request route ran over
  the NAS GitLab, which is retired, and its commands are gone.
- B. Branch and merge request only, on GitHub.
"The human executes real-world actions" is kept under both answers.

**Choice 3. The vocabulary card (2,905 characters in every session).**
- A. Stays in the root file, with its two marker lines, without its origin comment. **Recommended:**
  it binds every text a session writes, and decisions D16, D22, D26 put it there.
- B. One line in the root file points to the card; the card is read when governance text is written.

**Request 4 (not a choice). teachingco's first sentence.** The owner states the purpose; until then
the descriptive sentence of texts 5.7 stands.

**Choice 5. Which file holds when two files of the chain conflict?** Today root:24 says the load
order creates no precedence and the owner table is the boundary; agent-kernel:27 says a repo cannot
weaken a constraint above it.
- A. Keep today's sentence only (as in the proposed root text). **Recommended** as the smaller step.
- B. Add to the root: "A lower file may narrow a rule of a higher file; it may not weaken it." This
  would also settle upstream AGENTS.md files in `contrib/`.

**Choice 6. Where do the rules stand that are the same in every company?** (repo command and inline
Python, `docs/_core/**`, `.copier-answers.yml`, `diary/`)
- A. In the root, once (as in the proposed texts). **Recommended:** otherwise the same lines are kept
  in softwareco, teachingco, holdingco, tradingco, familyco and healthco.
- B. In each company file; the root stays shorter by about 400 characters, each company file longer
  by the same.

Settled without asking, as recommendations to adopt: C1 (root holds), C3 (bounded reading), C5
(remove), C7, C8. Many-of-the-greats was not run on them; each follows from a newer or higher text.

## 9. Who approves what, and the order

No CODEOWNERS file exists at the root, in softwareco or in teachingco. Approval follows the repo that
holds the file and `contracts/template-ownership.yml`.

| Change | Approver |
|---|---|
| root `AGENTS.md` (texts 5.1) | the owner, as a sign-off of its own (AK 8631 title); the card under D16, D22, D26 |
| `softwareco/AGENTS.md` (5.2), `teachingco/AGENTS.md` (5.7) | the company's owner; the files are company-owned and survive a template update. The chief of staff routes, it does not approve |
| `softwareco/softwareco-agents/AGENTS.md` (5.4) | softwareco's owner with the holder of AK 8630; after choices 1 and 2 |
| `core/tpl-template-repo`: `copier-template/AGENTS.md.jinja`, `copier/tpl-*/AGENTS.md.j2`, the assertions of `scripts/check-template-ci.sh` (439-441, 1002-1008, 1272-1278, 1382-1385) | owner of `core/tpl-template-repo`. `scripts/**` and `copier/**` inside softwareco and teachingco are template-owned copies and change by propagation, not by the company |
| lane files (5.3), subject repos (5.7), generated repo files | owner of each repo, after propagation: a copier update skips only `next_session_prompt.md` (`copier/tpl-project-repo/copier.yml:9-10`, read, not run) |
| `nodecode-cells/AGENTS.md` (5.5) | owner of nodecode-cells |
| `agent-kernel/AGENTS.md` (5.6) | owner of agent-kernel; preconditions of 5.6; ak-dev proof, since the file is live on merge |
| `~/ai-society/agents/*` (5.8) | owner of each agent repo, through the backfill in `softwareco-agents` |

Order:
1. Owner choices 1, 2, 3, 5, 6 and request 4.
2. Write the loading mechanics and the notes to editors into the skill `agents-layering-and-codification`.
3. Root, softwareco, teachingco and softwareco-agents files: owner sign-off only. This is the whole
   chain of a role holder.
4. In parallel to 3: the templates and their check in `core/tpl-template-repo`, then propagation to
   the companies.
5. Lane files and repo files. agent-kernel after its preconditions.

One live check to keep in view: `scripts/ci/smoke.sh` in generated repos requires AGENTS.md to name
`docs/dev/now.md` when that file exists (nodecode-cells:52-53, agent-kernel:61, mathe:48-49). None of
the three has the file today.

## 10. Not covered

- holdingco, tradingco, familyco, healthco and `~/ai-society/core/*` were not audited. Their company
  files come from the same template (holdingco 6,025, tradingco 6,033, familyco 6,026 bytes).
- Of the 80 folders in `softwareco/owned/`, two repo files were read (nodecode-cells, agent-kernel).
  `pi-server/AGENTS.md` has 50,449 bytes.
- Six worktree folders `softwareco/owned/.wt-security-watch-ak*` and `.wt-pi-extensions-ak-8605` each
  carry a copy of their repo's AGENTS.md; not examined.
- `teachingco/nt`, `wib` and `informatik` were compared with `mathe` by diff and by reading
  informatik; the pattern for them was not written out per file.
- The proposed texts were not loaded into a session and tried. Revision 2 is not independently checked.
