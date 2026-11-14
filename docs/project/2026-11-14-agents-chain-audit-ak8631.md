---
summary: "Audit of the AGENTS.md instruction chain below ~/ai-society (AK 8631): what each file says, what is duplicated, contradictory or dead, and a proposed target text per file. Nothing is applied."
read_when:
  - "You are about to change an AGENTS.md file or an AGENTS.md template below ~/ai-society."
  - "You decide on the proposals of AK 8631."
type: "proposal"
status: "proposal; not applied; each file needs its owner's approval (section 6)"
---

# Audit of the AGENTS.md chain (AK 8631)

Producer: nodecode session s-IZD1MTQW, 2026-11-14, commissioned by s-338VQQGH. No instruction file was
changed. Sizes are characters (`wc -m`) of the files as read on 2026-11-14. Line numbers refer to those
files. This is one session's reading; no second session has checked it.

Owner's word (2026-11-14): the AGENTS.md files are to be clear instructions, ordered by hierarchy,
without junk, with added context per company.

## 1. Result in short

1. A session in `nodecode-cells` loads 18,780 characters today. With the proposed texts it loads 9,847,
   of which 2,826 are the vocabulary card, which the owner placed in the root file on purpose.
2. The duplication is produced by the templates and held in place by a check.
   `softwareco/scripts/check-template-ci.sh:439-441, 1002-1008, 1382-1385` requires every generated
   repo file to contain "Deterministic tooling policy", `scripts/rocs.sh`, `diary/` and "Recursion
   policy". The company files come from `core/tpl-template-repo/copier-template/AGENTS.md.jinja`, the
   lane and repo files from `copier/tpl-*/AGENTS.md.j2`. A cleaned file is overwritten at the next
   template update unless the template and that check change first.
3. Five instructions contradict each other across files (section 4), among them push to `main`
   without asking (four files) against "ask before push" (root).
4. Three places name where an agent repo lives, and they disagree; one of the three does not exist
   (C6). This decides which company text a role holder receives. Owner choice 1.
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
| C4 | `softwareco/infra/AGENTS.md:29`, `fork:28`: update `strategic_goals.md`, `tactical_goals.md`, `operating_plan.md` | `agent-kernel/AGENTS.md:121`, `teachingco/informatik/AGENTS.md:39`, `agent-adoption-steward:26`: do not revive them | No clash in the letter (the lane rule is conditional), but a session in a repo without AK-native direction reads only the first. Keep the conditional rule in the lane, one sentence. |
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
| ROCS launcher, ROCS first | root 134-135; softwareco 32, 37-38; infra 34; contrib 13-14; fork 33; teachingco 22, 28-29; mathe 25, 27 | root (the command); company (prefer repo commands) |
| Inline Python only without a command | softwareco 39; owned 31; infra 35; contrib 15; fork 34; teachingco 30; mathe 28; adoption-steward 39 | company |
| Main-first | softwareco 20-21; infra 26-27; fork 23-24; nodecode-cells 34 | company |
| `docs/_core/**` immutable | contrib 9; fork 25; nodecode-cells 33; mathe 19; all `agents/*` | company (64 of 80 owned repos have the folder) |
| Engineering docs before engineering work | root 114-117; owned 40; nodecode-cells 27 | root |
| DB preflight | root 76, 127-128; agent-kernel 253 | root |
| Scratch and heavy jobs | root 77-78, 130-132 | root, once as rule, once as command |
| Recursion policy | softwareco 74-82; contrib 30-37; teachingco 105-113; mathe 59-66; adoption-steward 59-66 | template documentation (README), not the chain |
| Crystallization flow | contrib 17-28; teachingco 94-103; mathe 46-57; adoption-steward 48-57 | company: one line "write session notes to `diary/`" |
| Templates and lane bootstrap | softwareco 33-34, 41-65; teachingco 23-24, 32-81; `softwareco/README.md:48-75` | README |

## 5. Proposed target text per file

Rules followed: one fact in one place; a file states only what holds for everything below it; the
company file adds company context; no history; imperative sentences. Each block below is the complete
proposed file. Sentences that are new (not taken from an existing file) are named after the block.

### 5.1 `AGENTS.md` (root): 9,779 to 6,962

````markdown
# AGENTS.md — ai-society

Holds for every session below `~/ai-society`. Paths resolve from there unless absolute.
Each lower AGENTS.md (company, lane, repo) adds only what is specific to it. Before you change
anything outside the folder chain you started in, read the AGENTS.md chain of the target.

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

Never absorb one owner surface into another. Hand off explicitly.

## Work and authority
- Before acting, orient: `git log` and `git status` in every repo you will touch, `ak task show` for
  each task (including `broken_commitments`), and the peer sessions busy in that repo. Tell them
  before a build or e2e run.
- Work one exact AK task: claim it, keep evidence in the result JSON, release the claim before you
  stop. The task id is your execution authority; do not broaden it.
- Record deferred work as an AK task, not as a TODO comment or a local queue.
- `proceed` or `go ahead` continues the active task. It does not authorize lifecycle closeout,
  source-owner mutation, publication or knowledge promotion.
- Ask before push, deploy, publication, device actions and changes to another owner's surface.
  A local commit grants none of them.
- Where the AK decision workflow has landed, `ak decision list` and `ak decision passport` are the
  runtime authority. RFCs, ADRs, docs, task-scope snapshots and direction exports are projections.
- Where AK has not landed, use the repo's declared process. If there is none, stop and route the gap
  to the repo owner.
- Fix must-fixes and adopt recommendations without asking. Settle open questions with
  many-of-the-greats (`~/.pi/agent/prompts/many-of-the-greats.md`). Bring only value or ownership
  choices to the operator, as multiple choice with a recommended option.
- Reason broadly; change only the surface that owns the fact. If the operator calls your scope
  stale, pause and correct the plan first.
- Work in the repo of your start folder. Inspect another repo only when the operator names it or the
  task belongs there.

## Safety
- No secrets in git.
- Work inside a component repo, not in the workspace root, unless the work is workspace-level.
- Honor `TMPDIR`. Never use `/tmp` for clones, worktrees, builds, caches or large output. Run
  multi-GiB jobs through `heavy-job`.
- Run the preflight before any direct mutation of a workspace database.
- Delete only scratch you own and can prove inactive.
- State with no live owner (a lock no process holds; uncommitted work, stashes, branches or processes
  untouched for 30 days with no active AK task): move it to a quarantine and record that in AK.
  Never delete it.

## Reading and engineering
- Read the AK task scope first, then only the documents the task needs. Find them with `docs-list`.
  Do not read whole documentation folders.
- Before engineering work, read the repo's `docs/engineering.local.md` and
  `policy/engineering-lane.json`.
- Run the repo's declared checks before merge.
- Keep files within: code 500 lines / 50 KB, tests 1000 / 80 KB, markdown 800 / 60 KB.

## Commands (use exactly)
```bash
# before any direct sqlite on society.v2.db; run from ~/ai-society
./scripts/db-change-preflight.sh --db-path <db-path> --stage db-dev

# heavy jobs; /home is nearly full, so select the /data root
AI_SOCIETY_SCRATCH_ROOT=/data/ai-society-scratch heavy-job run --label <label> --task <task-id> -- <command...>

# ROCS, from the target repo; contracts first for an unfamiliar operation
./scripts/rocs.sh contracts

# docs-list, from the target repo; add no wrapper
node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --task "<task>" --top 8
```
All other recipes are in the `ai-society-runtime-recipes` skill.

## Vocabulary card
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
````

Changes: front matter, the notes to editors, the loading mechanics and the dates are removed. The
loading mechanics (lines 19-22) and the rule for future edits (141-142) are for whoever edits these
files; they move to the skill `agents-layering-and-codification`. Moved up from lower files: deferred
work as AK task (owned 23), bounded reading (owned 37-44). "A local commit grants none of them" is
taken from `teachingco/AGENTS.md:12`. The router skills move to the softwareco file. The card is
unchanged, without its comment. No new rule.

### 5.2 `softwareco/AGENTS.md`: 3,563 to 1,226

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

Each lane and each repo below it is its own git repo. Pick the lane first. To find the repo for a
task, use the skill `softwareco-owned-repo-router`, `softwareco-infra-repo-router` or
`softwareco-contrib-repo-router`.

## Rules for every softwareco repo
- Commit to `main`. Open a GitHub PR only for a release or when the operator asks for one.
- Prefer a repo command (`just <recipe>`, `./scripts/rocs.sh`, a repo script) to an ad-hoc script.
  Write inline Python only when no such command exists.
- Do not edit `docs/_core/**`.
- Keep `.copier-answers.yml` committed.
- Write session notes to the repo's own `diary/`.

To create a repo or a lane from a template, read `README.md` of this folder.
````

The first sentence is taken from `docs/org/purpose.md` ("AI Society's product-engineering company").
The `softwareco-agents/` row depends on owner choice 1. `docs/_core` is moved up from four lower files.
Templates, lane bootstrap and recursion policy stay in `README.md:48-75`, where they already are.

### 5.3 Lanes

`softwareco/owned/AGENTS.md`: 3,311 to 470

````markdown
# AGENTS.md — softwareco/owned

- Do a repo's work in that repo. Change here only what belongs to the whole lane: this file,
  `docs/project/`, `scripts/`.
- To choose a repo, read `docs/project/repo-capability-map.md` of this lane. It is a hint; confirm
  in the chosen repo's own docs before you implement.
- Use the repo's `Justfile`; `just help` lists its recipes. If a repo has none, set it up after
  `docs/project/standardized-justfile-contract.md` of this lane.
````

The adoption-scan line (30) is needed only at the lane root; it belongs in the lane's `README.md`.

`softwareco/infra/AGENTS.md`: 1,887 to 516

````markdown
# AGENTS.md — softwareco/infra

- Do a repo's work in that repo. Change here only what belongs to the whole lane.
- To choose a repo, read `docs/project/repo-capability-map.md` of this lane. It is a hint; confirm
  in the chosen repo's own docs before you implement.
- If a repo keeps direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`),
  update them in the same pass as the task that changes direction, link tasks and decisions as
  `task:` / `decision:`, and run `ak direction check`.
````

`softwareco/fork/AGENTS.md`: 2,595 to 459

````markdown
# AGENTS.md — softwareco/fork

- Do a repo's work in that repo. Change here only what belongs to the whole lane.
- Record in the fork's `docs/decisions/` why the fork exists and which upstream boundary failed.
- If a repo keeps direction docs (`strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`),
  update them in the same pass as the task that changes direction, link tasks and decisions as
  `task:` / `decision:`, and run `ak direction check`.
````

`softwareco/contrib/AGENTS.md`: 1,660 to 439

````markdown
# AGENTS.md — softwareco/contrib

- Do a repo's work in that repo. Change here only what belongs to the whole lane.
- A repo's own AGENTS.md may come from its upstream. Where it conflicts with the files above it,
  the files above it hold for our work; the upstream file holds for what we send upstream.
- If a repo's direction docs under `docs/project/` change, run `ak direction import`, then
  `ak direction check`, from the repo root.
````

New in contrib: the second line. Some contrib repos carry their upstream's AGENTS.md
(`beads_rust` 54,145 bytes, `beads_viewer` 45,869 bytes), which nobody here edits. The lane owner
confirms or strikes the line.

### 5.4 `softwareco/softwareco-agents/AGENTS.md`: 694 to 408

````markdown
# AGENTS.md — softwareco-agents

This repo holds the contract, the registry and the role cards for softwareco's agents.

- Before you create or change an agent, read `docs/agent-registry.md` and
  `docs/agent-operating-contract.md`.
- One repo prepares one agent. A repo or a registry row grants no authority and appoints nobody.
- State an agent's behaviour explicitly: triggers, invariants, failure modes.
````

"Grants no authority" is from `docs/agent-registry.md` (Boundary); "appoints nobody" from
`agents/agent-adoption-steward/AGENTS.md:4`. The file names no role and no holder; the appointment is
the mycel role record (roles synthesis, point 2).

Pattern for an agent repo (the source is `copier/tpl-agent-repo/AGENTS.md.j2`, 4,858 bytes today): 424 plus
the agent's own rules

````markdown
# AGENTS.md — agent-<name>

This repo prepares the agent <name> for softwareco. `agent.json` and
`docs/person/system-prompt.md` are its executable identity; keep the rest of the repo consistent
with them.

- This repo grants no authority and appoints nobody. Find your delegation in AK and in the role
  record. If it is missing, expired or unclear, stop and escalate.
- <rules that hold for this agent only, one line each>
````

### 5.5 `softwareco/owned/nodecode-cells/AGENTS.md`: 2,127 to 1,189

````markdown
# AGENTS.md — nodecode-cells

A family of native Nodecode cells. Autoresearch is the first cell.

- Products live in `cells/<primary-asdf-system>/`. No nested git repositories.
- ASDF is the only dependency and build contract. Allowlist each maintained system; do not register
  references, templates or other ASDF definitions recursively. Exception: `cells/xeno-lab/` may hold
  a Bend kernel (pinned compiler) and a Rust member (cargo) whose checks join `just ci`.
- Use the host's own lifecycle, settings, tools and UI. Do not build a parallel platform.
- Loading code must be inert. Record cleanup at acquisition and observe actual quiescence.
- Replace changed source with a fresh process; do not presume hot-unload is safe.
- Selected-folder installation, coexistence and lifecycle each need their own evidence.
- Do not extract a shared runtime kit until two real consumers justify it.
- Never describe tests of fake adapters or synthetic observations as real campaigns.
- Keep policy at the repo root; add guidance to a member only where it deviates.
- Before implementation, read `docs/project/product_posture.md`.
- Ask before installing into a real profile or promoting a cell.
````

### 5.6 `softwareco/owned/agent-kernel/AGENTS.md`: 20,606 to 4,274

````markdown
# AGENTS.md — agent-kernel

AK is the local runtime that holds ai-society's coordination state. The active database (`AK_DB`,
default `~/ai-society/society.v2.db`) is the source of truth; YAML, JSON and markdown files are
projections unless a surface says otherwise.

## Never
- Never invoke the `ak` binary directly. Every call goes through `scripts/ak-runtime-gate.sh`, which
  checks the binary digest against `policy/ak-runtime-access.json`.
- Never open the live database with `./scripts/fsqlite.sh`, `sqlite3`, Python `sqlite3` or a dev
  build. Inspect copies.
- Never add an FCOS surface. AK does not import, parse, evaluate, select, project, mutate or repair
  FCOS state (Decision 129); a tripwire test pins every site.
- Never recreate `docs/project/strategic_goals.md`, `tactical_goals.md` or `operating_plan.md`.
  Direction lives in AK direction rows.
- Never run `ak repo delete --force`, and never delete or replace `society.v2.db`, without a separate
  authorization. Recovery is from backup only.
- Never clear a fence marker you did not set.

## Direction and tasks
- Read direction with `ak strategy list --repo .` and `ak wave list --repo .`. Change it with
  `ak direction ...`. Reconcile with `ak direction check --repo . --machine`.
- When a wave needs its next route, read `docs/project/product-posture.md` and the open-frame status,
  then create or select the concrete execution task and link it as `execution_task`. Do not create an
  "await route" task. Wait for the operator only on real ambiguity or risk; then name the recommended
  route and the exact decision needed.
- For a non-trivial task, set the done contract early (`ak task contract set-done`,
  `set-guardrails`), use `ak task reconcile open|close` when planned and actual scope diverge, and run
  `ak task close-check <id> -F json` before completion. close-check is advisory.
- After a task lifecycle or direction-link change, run `python3 scripts/render-direction-explorer-mvp.py`
  and then the same with `--check`, or record that the refresh is deferred.
- `governance/work-items.json` is a projection; the DB wins. `ak work-items` is deprecated.

## Publication
- Merging to local `main` deploys everything the main checkout serves: the gate, the policy,
  `validate.sh`, hooks and this file. Only `docs/`, `diary/`, `tests/` and `README.md` are inert.
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

Moved, not deleted, and to be moved before the cut: recovery procedures and backup (291-332) into
`docs/project/database-incident-response.md`, which does not carry them today; known backend debt
(277-289) and adapter layer (334-351) into `docs/project/database-backend-runtime.md`; FCOS schema
detail (72-80) stays in the Decision 129 documents it cites. This file is live on merge by its own
rule (line 171), so the change needs the ak-dev proof of that rule.

### 5.7 `teachingco/AGENTS.md`: 4,364 to 715

````markdown
# AGENTS.md — teachingco

teachingco holds the teaching work: one monorepo per subject (`mathe/`, `nt/`, `wib/`,
`informatik/`) and class material.

- No pupil data anywhere: not in git, tests, examples, artifacts or messages to other sessions. Use
  abstract groups and invented words, never a class.
- Commit to local `main`. Git workflow: `CONTRIBUTING.md`.
- Prefer a repo command (`just <recipe>`, `./scripts/rocs.sh`, a repo script) to an ad-hoc script.
  Write inline Python only when no such command exists.
- Do not edit `docs/_core/**`.
- Keep `.copier-answers.yml` committed.
- Write session notes to the repo's own `diary/`.

To create a repo or a lane from a template, read `README.md` of this folder.
````

The first sentence describes the folders as they are. The owner has yet to state teachingco's purpose
(roles synthesis, owner choice 3); that sentence replaces it.

Pattern for the subject repos, shown for `teachingco/mathe/AGENTS.md`: 2,767 to 458

````markdown
# AGENTS.md — mathe

Monorepo for the subject Mathematik.

- `packages/` holds libraries, `apps/` holds deployables. Neither has its own `.git`.
- Package manager: uv. The workspace is configured at the root; a member's pinned lane command is
  in its `policy/stack-lane.json`, its local deltas in its `docs/tech-stack.local.md`.
- Commit with `.pi/prompts/commit.md`. Scope: the package name, the app name, or `root`,
  `monorepo`, `ci`, `docs`, `release`.
````

`nt`, `wib` and `informatik` take the same text with their subject and with
`policy/engineering-lane.json` and `docs/engineering.local.md` as the file names.

### 5.8 `~/ai-society/agents/*`

The four old repos (health, triage, consent-steward, pilot) carry the unfilled template text and the
retired GitLab. `softwareco-agents/docs/legacy-agent-backfill.md` owns their backfill; they take the
agent-repo pattern of 5.4 then. `agent-adoption-steward` keeps lines 4-6 and 15-19 and loses the rest
(4,308 to about 1,300).

## 6. Effect in numbers

Characters loaded at session start, start folder inclusive.

| Start folder | Today | Proposed | Change |
|---|---|---|---|
| `softwareco/softwareco-agents/` | 9,779 + 3,563 + 694 = 14,036 | 6,962 + 1,226 + 408 = 8,596 | -39 % |
| an agent repo below it (repo file as last generated, `agent-adoption-steward`, 4,308; proposed pattern 424 plus own rules) | 18,344 | 9,020 | -51 % |
| an agent repo at `~/ai-society/agents/` (same repo file) | 9,779 + 4,308 = 14,087 | 6,962 + 424 = 7,386 | -48 % |
| `softwareco/owned/nodecode-cells/` | 9,779 + 3,563 + 3,311 + 2,127 = 18,780 | 6,962 + 1,226 + 470 + 1,189 = 9,847 | -48 % |
| `softwareco/owned/agent-kernel/` | 37,259 | 12,932 | -65 % |
| `teachingco/` | 9,779 + 4,364 = 14,143 | 6,962 + 715 = 7,677 | -46 % |
| `teachingco/mathe/` | 16,910 | 8,135 | -52 % |

With owner choice 3 answered B (card on demand) every proposed figure falls by a further 2,700.

## 7. Owner choices

**Choice 1. Where does a company's agent repo live?** Three places are written down (C6).
- A. `~/ai-society/agents/agent-<name>`, as the registry says. The chain gives the holder the root
  file only; the softwareco text must reach it through its own prompt.
- B. Below the company, in `softwareco/softwareco-agents/`. The chain gives the holder root, company
  and the agents file (9,020 characters). Agents that serve all companies stay at `~/ai-society/agents/`.
  The registry sentence and `softwareco/AGENTS.md:16, 46, 71` change to say so.
- C. A new lane `softwareco/agents/`, as `softwareco/AGENTS.md` says today.
- **Recommended: B.** It is the only one that delivers "added context for each company" through the
  chain, it needs no new folder, and AK 8630 already works there. The session holding AK 8630
  (s-U3SNXAYW) should hear the answer before it places the repo.

**Choice 2. How does work reach `main` in an agent repo?** (C2)
- A. Main-first, as in every other softwareco repo. **Recommended:** the merge-request route ran over
  the NAS GitLab, which is retired, and its commands are gone.
- B. Branch and merge request only, on GitHub.

**Choice 3. The vocabulary card (2,826 characters in every session).**
- A. Stays in the root file, without its comment. **Recommended:** it binds every text a session
  writes, and decisions D16, D22, D26 put it there.
- B. One line in the root file points to the card; the card is read when governance text is written.

**Choice 4. teachingco's first sentence.** The owner states the purpose; until then the descriptive
sentence of 5.7 stands.

Settled without asking, as recommendations to adopt: C1 (root holds), C3 (bounded reading), C5
(remove), C7, C8. Many-of-the-greats was not run on them; each follows from a newer or higher text.

## 8. Who approves what

No CODEOWNERS file exists at the root, in softwareco or in teachingco. Approval therefore follows the
repo that holds the file.

| Change | Approver |
|---|---|
| root `AGENTS.md` (5.1) | the owner, as a sign-off of its own (AK 8631 title); the card under D16, D22, D26 |
| `core/tpl-template-repo/copier-template/AGENTS.md.jinja`, `copier/tpl-*/AGENTS.md.j2` and the assertions in `scripts/check-template-ci.sh` | owner of `core/tpl-template-repo`; must come first, or the next template update restores today's text |
| `softwareco/AGENTS.md` (5.2) and the embedded `softwareco/copier/tpl-*` | softwareco's owner; the chief of staff routes, it does not approve |
| `softwareco/{owned,infra,fork,contrib}/AGENTS.md` (5.3) | softwareco's owner, in each lane repo |
| `softwareco/softwareco-agents/AGENTS.md`, agent-repo pattern (5.4) | softwareco's owner with the holder of AK 8630; after choices 1 and 2 |
| `nodecode-cells/AGENTS.md` (5.5) | owner of nodecode-cells |
| `agent-kernel/AGENTS.md` (5.6) | owner of agent-kernel; ak-dev proof, since the file is live on merge |
| `teachingco/AGENTS.md` and subject repos (5.7) | teachingco's owner; after choice 4; `teachingco/copier/tpl-*` with it |
| `~/ai-society/agents/*` (5.8) | owner of each agent repo, through the backfill in `softwareco-agents` |

Order: choices 1-4, then templates and their check, then root, then company files, then lanes, then repos.

## 9. Not covered

- holdingco, tradingco, familyco, healthco and `~/ai-society/core/*` were not audited. Their company
  files come from the same template (holdingco 6,025, tradingco 6,033, familyco 6,026 bytes).
- Of the 80 folders in `softwareco/owned/`, two repo files were read (nodecode-cells, agent-kernel).
  `pi-server/AGENTS.md` has 50,449 bytes.
- Six worktree folders `softwareco/owned/.wt-security-watch-ak*` and `.wt-pi-extensions-ak-8605` each
  carry a copy of their repo's AGENTS.md; not examined.
- The proposed texts were not loaded into a session and tried.
