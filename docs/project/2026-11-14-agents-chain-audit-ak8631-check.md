---
summary: "Independent check of the AGENTS.md chain audit (AK 8631). Revision 1: CONFIRMED-WITH-DIFFERENCES (lost rules, repeated facts, wrong order). Revision 2 (section 8): CONFIRMED, six small remarks."
read_when:
  - "You decide on or apply the proposals of AK 8631."
  - "You read 2026-11-14-agents-chain-audit-ak8631.md."
type: "reference"
---

# Check of the AGENTS.md chain audit (AK 8631)

Checker: nodecode session, 2026-11-14, commissioned by s-338VQQGH; not the producer (s-IZD1MTQW), who was not
consulted. Object: `2026-11-14-agents-chain-audit-ak8631.md` at commits 56dcdf8 and 03882e5. Read-only on every
instruction file. Section 1 was written before the audit was opened.

**Verdict: CONFIRMED-WITH-DIFFERENCES.** The audit's measurements, citations, contradictions and dead references
hold. The proposed target texts are not ready to apply: they lose rules (section 3), they still state several facts
twice (section 4), and the stated order of changes is wrong for the root and company files (section 2, D1-D3).

## 1. Independent view, written before reading the audit

Files read: `~/ai-society/AGENTS.md` (9836 bytes), `softwareco/AGENTS.md` (3575), `softwareco/owned/AGENTS.md` (3313),
`softwareco/softwareco-agents/AGENTS.md` (700), `owned/nodecode-cells/AGENTS.md` (2129), `owned/agent-kernel/AGENTS.md` (20658),
`teachingco/AGENTS.md` (4372). `~/ai-society/agents/` has no AGENTS.md of its own; `softwareco/agents/` does not exist.

Three worst duplicates:
1. Source-owner table: root `AGENTS.md` (table under "Source-owner boundaries") against agent-kernel:82-92, again as axiom
   agent-kernel:30 and as nodecode-cells:37.
2. Reasoning breadth against mutation scope, and exact-task discipline: root "Reasoning vs mutation" and "Task, decision, and
   direction authority" against agent-kernel:32-55, 130-143 and 266-275.
3. Deterministic tooling and docs discovery: softwareco "Shared tooling" and "Deterministic tooling policy" against
   owned:27,31,40-41 and root "Critical invocations"/"Engineering guidance"; nodecode-cells:27 repeats the engineering read.
   "No secrets in git" stands at root, softwareco, softwareco-agents:7, nodecode-cells:33, teachingco:14.

Contradictions and dead references:
- softwareco-agents:8,11-14 ("Work is proposals + MRs", GitLab NAS, `gl-nas`) against softwareco main-first and
  agent-kernel:371 "No GitLab required"; `gl-nas`/`gl-nas-git` are not on PATH; `holdingco/holdingco-templates` (line 18) is missing.
- softwareco names an `agents/` lane at `softwareco/agents/agent-<slug>`; the directory does not exist (the real one is
  `softwareco/softwareco-agents`, and agent repos sit in `~/ai-society/agents/`).
- teachingco:4-8,84-87 names four lanes; none of `owned/ contrib/ infra/ agents/` exists. teachingco:90-92 names three
  documents that do not exist. teachingco:21,27 prefers `ak work-items`, which agent-kernel:66 calls deprecated.
- agent-kernel:360 "Generated from `softwareco/tpl-owned-repo`" (no such template); agent-kernel:253 `society.db` against `society.v2.db`.
- agent-kernel:171-173 (merge to main is a live deploy, proof first) narrows softwareco "commit directly to main"; a repo
  narrowing, to be stated as such.
- nodecode-cells:38 is history ("This bootstrap authorizes repository creation").

What a nodecode-cells session truly needs: root safety (secrets, scratch/heavy-job, DB preflight, quarantine rule), owner
boundaries, AK task authority and the working loop; from softwareco only main-first and the lane names; from owned the `just`
surface and the bounded read order; its own structure/boundary/authorization rules. It does not need: the copier template
table, lane bootstrap, placement reminders, recursion policy, the Justfile transition rule, the adoption-scan sentence, the
per-agent loading mechanics in the root layering contract.

## 2. What was checked, and the result

### (a) Sizes: confirmed
`wc -m` on all 20 files gives the audit's figures exactly (root 9,779; softwareco 3,563; owned 3,311; infra 1,887;
contrib 1,660; fork 2,595; softwareco-agents 694; ontology 429; nodecode-cells 2,127; agent-kernel 20,606;
teachingco 4,364; mathe 2,767; nt 2,778; wib 2,923; informatik 4,550; the five `agents/*` 4,308/457/668/668/574).
The twelve proposed blocks, extracted from the audit between their fences and counted in characters, give
6,962 / 1,226 / 470 / 516 / 459 / 439 / 408 / 424 / 1,189 / 4,274 / 715 / 458, as stated. The sums and percentages
of audit section 6 are arithmetically right. The card with its comment is 3,178 characters (root lines 39-71). Byte
figures (`beads_rust` 54,145, `beads_viewer` 45,869, `pi-server` 50,449, tpl-agent-repo 4,858) are right. Counts are
right: of 80 folders in `owned/`, 67 have `.copier-answers.yml`, 59 a Justfile, 64 `docs/_core`; 5 of 27 infra
folders have `docs/project/strategic_goals.md`.

### (b) Citations: confirmed (over 40 sampled, none wrong)
Root 22-24, 74-76, 94-96, 100 (broken wrap), 108, 111-112, 119-122, 127-128, 137-138. softwareco 16, 20-21, 46, 71.
owned 22-24, 27-31, 34-35, 38-44. infra 25-31, 34-35, 37-44. fork 22-30, 36-45, 47-54. contrib 3-4, 7-10, 13-15,
17-28, 30-37, 40-42, 44-51. softwareco-agents 4, 7-9, 11-14, 17-18. ontology 9-10. nodecode-cells 11-12, 15-24,
27-30, 33-38. agent-kernel 12-15, 30, 32-55, 66, 82-92, 121, 171, 253, 255-264, 295, 360, 382. teachingco 3-8, 12,
15, 21, 27, 83-92. mathe 17-22, 24-28, 30-44, 59-76. informatik 24-25, 29-30, 32-39. wib 18-19. agent-health 3-4,
7-9, 11-14, 16-19. adoption-steward 4-6, 9-12, 15-19, 22-26.

### (c) Contradictions and dead references: confirmed
C1-C8 each hold at both cited places. Dead references reproduced: `gl-nas` and `gl-nas-git` not on PATH (`which`);
`holdingco/holdingco-templates`, `softwareco/agents/`, `teachingco/{owned,contrib,infra,agents}`,
`teachingco/docs/{lane-policy-matrix,repo-placement-policy,archetype-lane-crosswalk}.md` do not exist; no template
`softwareco/tpl-owned-repo`. Every pointer the proposed texts introduce exists (`softwareco/docs/org/purpose.md:18`,
`softwareco-agents/docs/agent-registry.md:9-13`, `agent-operating-contract.md`, `legacy-agent-backfill.md`,
`infra/docs/project/repo-capability-map.md`, agent-kernel `database-incident-response.md`, `product-posture.md`,
`ak-dev.md`, `teachingco/mathe/.pi/prompts/commit.md`, the skill `agents-layering-and-codification`).
My own pre-audit notes (section 1) found nothing the audit missed among contradictions and dead references.

### (g) Order of changes and `check-template-ci.sh`: partly wrong
The script was read. Lines 439-441 assert on the template source `copier/$tpl/AGENTS.md.j2`; lines 1002-1008 and
1382-1385 assert on a repo freshly rendered into a temporary folder (`l2_dir="$tmp_root/$tpl"`, line 943). So far the
audit is right. Differences:

- **D1. The company files are not overwritten by a template update.** `softwareco/contracts/template-ownership.yml`
  lists `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `docs/org/**` as company-owned, and the same script enforces it:
  `scripts/check-template-ci.sh:519-521` ("L1 ownership map must preserve company-owned $company_path"). The audit's
  sentence "A cleaned file is overwritten at the next template update unless the template and that check change
  first" (its section 1 item 2, section 8 row 2) is false for `softwareco/AGENTS.md` and `teachingco/AGENTS.md`. The
  root file and `softwareco/softwareco-agents/AGENTS.md` have no `.copier-answers.yml` at all. Root, company and
  softwareco-agents files, which are the whole chain of a role holder, can therefore change first, without waiting
  for the templates.
- **D2. The script and the embedded templates are not softwareco's to change.** The same ownership file lists
  `scripts/**` and `copier/**` as `template_owned`. `softwareco/scripts/check-template-ci.sh` is a rendered copy
  (identical to `teachingco/scripts/check-template-ci.sh` by `cmp`; it differs from
  `core/tpl-template-repo/copier-template/scripts/check-template-ci.sh` from line 346). Audit section 8 row 3 gives
  "the embedded `softwareco/copier/tpl-*`" to softwareco's owner; by the ownership map it belongs to the owner of
  `core/tpl-template-repo`, and each company receives it by propagation.
- **D3. The check binds templates, not live files, and the audit's list of assertions is incomplete.** No assertion
  reads a live repo's AGENTS.md; a cleaned live file fails nothing in this script. Templates-first is needed for the
  lane and repo files only because `copier/tpl-project-repo/copier.yml:9-10` skips nothing but
  `next_session_prompt.md` on update. Also asserted and not named by the audit: lines 1007-1008 and 1275-1276
  (`policy/engineering-lane.json`, `docs/engineering.local.md` must appear in the generated file) and 1272-1278
  (tpl-package, "internal member of an L2 monorepo"). The proposed root text moves the engineering pointers to the
  root, so these assertions must go as well. One live check exists that the audit does not mention:
  `scripts/ci/smoke.sh` in generated repos (nodecode-cells:52-53, agent-kernel:61, mathe:48-49) requires AGENTS.md to
  name `docs/dev/now.md` when that file exists. None of the three has it today, so nothing fails now.

Corrected order: choices; root, company and softwareco-agents files (owner sign-off only); in parallel the L0
template and its check in `core/tpl-template-repo`, then propagation; then lanes and repos.

## 3. Lost rules (check d)

A rule counts as lost when it stands in a file today and in no proposed text at any level. Ordered by weight.

| # | Rule today | Where today | State in the proposal |
|---|---|---|---|
| L1 | Router for core and holdingco: `ai-society-core-repo-router`, `holdingco` capability map | root, "Repo routing" (88-92) | Lost. The audit moves "the router skills" to softwareco; the softwareco text names the three softwareco routers only. |
| L2 | Templates are an owner surface ("company templates retain their owner boundaries"; "Template rollout: template/propagation owner repos") | nodecode-cells:37; agent-kernel:30, :92; informatik:37; adoption-steward:25 | Lost. The root owner table has no template row and every lower mention is deleted. This is the very boundary D2 turns on. |
| L3 | Conflict between levels: "Render order creates no precedence; owner-surface tables are the authority boundary"; "L2 repos cannot weaken L1 constraints" | root:24; agent-kernel:27 | Both deleted. A new rule of the opposite kind appears in one lane only (contrib: "the files above it hold"). The proposal has no general statement left on which level holds. |
| L4 | File budgets are "brownfield ratchets, enforced by repo validation"; "repo-owned validation wins" | root:119-122 | Changed in meaning: "Keep files within: code 500 lines / 50 KB ..." is a hard limit, where today a file above the figure is tolerated and only may not grow (which files exceed the figures was not measured here). "Repo-owned checks win" is lost. |
| L5 | Before further legacy direction archive cleanup run `python3 scripts/ci/check-direction-legacy-markdown-readiness.py --require-ready` | agent-kernel:124 | Lost; the audit files 122-124 under history, but 124 is a precondition. |
| L6 | "Every pass/fail decision emits evidence" | agent-kernel:21, :29 | Narrowed to "every write returns or records evidence". |
| L7 | `./scripts/preflight-repo-census.sh [scope]` | softwareco:31; mathe:26 | Lost. Not in `softwareco/README.md` (`grep -i census` empty), not in the recipes skill. |
| L8 | Author task scope in AK, freeze with `ak task scope show|export`; `governance/task-scopes/AK-*.snapshot.json` are exports | owned:24; informatik:30; adoption-steward:12 | Only "task-scope snapshots ... are projections" remains in the root; the command and the path are in no proposed text and not in the recipes skill (`grep -i 'task scope'` empty). |
| L9 | Never-rules of recovery: do not source `.ak-env`, select a checkout binary or restore the main file alone; never combine a restored main file with a newer WAL; the `ak task release-expired` / `unclaim` commands | agent-kernel:299-319 | Not lost if moved first, as the audit says. Verified that the target documents do not carry them today (`grep` for `release-expired`, `.ak-env`, `unclaim` in `database-incident-response.md` and `database-backend-runtime.md`: empty). The move is a precondition of 5.6, not a follow-up. |
| L10 | Do not mirror directly queryable live DB state in docs; record why when an advisory close-check gap is accepted; read `docs/project/layer-12-protocol.md` for direction/packet/decision/wave work | agent-kernel:213, :164, :259 | Lost. |
| L11 | "Do not ... claim AK adoption from a document" | nodecode-cells:35-36 | Lost. |
| L12 | "you (human) executes real-world actions" | softwareco-agents:8 | Lost. Owner choice 2 covers only the route to `main`; the root's "ask before push, deploy, device actions" is weaker than "the human executes". |
| L13 | Engineering-core adoption scan `./scripts/engineering-core-adoption-scan.sh` | owned:30 | To move to the lane README per the audit; not there today (`grep -i adoption-scan owned/README.md`: empty). Precondition. |
| L14 | Small losses in the root: "or launch a target-root session" (23); "(Claude Code: ListAgents)" as the way to find peers (106); "since the last session" (105); "with their preflights" (85); "consumer policy is local adoption truth" (116); the card's BEGIN/END markers and "At most 25 lines" (40-43, 71), which are the anchor for the generator that comment announces | root | Lost. Keep the two marker lines; they cost 60 characters. |
| L15 | The decision reference of the xeno-lab exception (owner decision A, AK #8235) | nodecode-cells:19 | Dropped as history. An exception to a rule should keep the reference that grants it. |

Checked and not lost: the diary file-name convention (lives in `diary/README.md`, asserted at script line 438);
recursion policy (`softwareco/README.md:266-272`); templates and lane bootstrap (`softwareco/README.md:46-80`,
`teachingco/README.md:14-20, 39-68`); `pi -p "/establish-standard-justfile"` (in the Justfile contract, line 110);
the fence rule and "inspect copies" (agent-kernel 295, 382, both kept). For a session in nodecode-cells, every rule
I listed as needed in section 1 is present in the proposed chain except L2, L11 and L15.

## 4. One fact in one place; plain imperative (check e)

The proposal removes most duplication. It still states these facts more than once:

- The five company rules (prefer a repo command, inline Python, `docs/_core/**`, `.copier-answers.yml`, `diary/`)
  are word for word the same in the softwareco and teachingco texts. A rule that holds in every company belongs in
  the root; otherwise it will be copied into holdingco, tradingco, familyco and healthco as well.
- "Do a repo's work in that repo. Change here only what belongs to the whole lane." stands in all four lane texts,
  beside the root's "Work inside a component repo" and "Work in the repo of your start folder".
- The direction-docs sentence is identical in infra and fork.
- Choosing a repo: router skills in softwareco, `repo-capability-map.md` in owned and in infra. Three places, two
  mechanisms.
- Root: heavy-job, DB preflight and docs-list each stand once as a rule and once as a command; "release the claim"
  stands in the work loop and in the card.
- "Grants no authority and appoints nobody" stands in softwareco-agents and in the agent-repo pattern; under
  choice 1 B the agent repo loads both.

Wording: the texts are plain imperatives. One breach of the card the audit itself invokes (C7): proposed
agent-kernel text, Publication, "the gate, the policy" uses bare "gate". The softwareco text's sentence "Each lane
and each repo below it is its own git repo" is new and is not named as new.

## 5. Owner choices (check f)

- Choice 1 is a real owner choice. The supporting sentence for B is wrong: B is not "the only one that delivers
  added context for each company through the chain"; C (`softwareco/agents/`) lies below softwareco and delivers the
  same root and company text. The audit also does not cite `softwareco/README.md:44`, which calls `agents/` "a
  declared target lane" not yet materialized, so C is the written intent, not a stray line. B against C is then:
  no new folder and AK 8630 registered on `softwareco/softwareco-agents` (verified, `ak task show 8630`) against
  the declared lane. B also nests agent repos inside the `softwareco-agents` git repo, against
  `agent-registry.md:15` ("do not nest agents"). The recommendation may stand; its reasons need correcting.
- Choice 2 is real and complete; the recommendation is supported (the NAS GitLab is retired, `ontology/AGENTS.md:10`).
- Choice 3 reopens what D16, D22 and D26 decided; as a choice it is fair, the recommendation follows the decisions.
- Choice 4 is a request for a sentence, not a choice.
- Missing: which level holds when levels conflict (L3). It is a value choice, today answered by root:24, and the
  proposal answers it differently in one lane without asking.
- Missing: whether the company-common rules go to the root (section 4, first item).

## 6. Other differences

- D4. Audit section 1 item 3 says "five instructions contradict each other"; its section 4 lists eight (C1-C8), and
  the producer's AK evidence 21743 says `contradictions: 8`.
- D5. Removing the front matter was checked for side effects: no script found that requires front matter on an
  AGENTS.md (`docs-list.mjs` does not mention AGENTS; no `read_when` test in `softwareco/scripts`, `owned/scripts`,
  `nodecode-cells/scripts`). No objection.
- D6. The skill `agents-layering-and-codification` exists but does not hold the loading mechanics today (`grep` for
  Codex, 64 KiB, SessionStart: empty). Root lines 19-22 name the hook `scripts/claude-agents-chain-hook.mjs`; move
  the text before deleting it.

## 7. Not checked

- `teachingco/nt/AGENTS.md` and the tpl-agent-repo template were not read line by line; the agent-repo pattern (5.4)
  was not checked for lost rules against `copier/tpl-agent-repo/AGENTS.md.j2`.
- The proposed texts were not loaded into a session.
- What a copier update would actually do to a lane or repo file was read from `copier.yml`, not run.

## 8. Re-check of revision 2 (delta only)

Object: commit bb5ae1b, the audit and the new `2026-11-14-agents-chain-audit-ak8631-texts.md`. Requested by
s-338VQQGH; same boundaries. Only the delta against sections 2-6 was checked.

**Verdict on revision 2: CONFIRMED.** All fifteen lost rules are restored, L16-L21 are real, the order is
corrected, the choices are stated fairly, the figures measure as stated. Six small remarks (R1-R6) remain; none
blocks the owner choices.

### 8.1 L1-L15: all restored
Read against the blocks of the texts file (line numbers of that file):
L1 72-75; L2 39; L3 24-25 and agent-kernel 316-317; L4 98-100; L5 328-330; L6 317; L7 195 and 432; L8 49-50;
L9 324-325, 356-357; L10 334, 351-352, 339-340; L11 301; L12 252; L13 215-217; L14 26-27, 44-46, 69, 97,
119 and 147; L15 292. Each sits at the level where the rule holds. No removal was substituted for a
restoration. The "let go" table (audit section 7) names a reason and an approver for every row.
The duplicates of section 4 are gone except the one kept on purpose ("release the claim" in the card) and
R3 below; the bare "gate" is gone (the only hits left are the file name `ak-runtime-gate.sh`).

### 8.2 L16-L21: real
Each source line was read and each rule was absent from the revision 1 texts:
L16 informatik:35, adoption-steward:24, `copier/tpl-agent-repo/AGENTS.md.j2:28`; L17 informatik:38,
template:31; L18 informatik:29; L19 template:14, 17, 18; L20 informatik:30; L21 agent-kernel:25-26, 36-38,
59-65, nodecode-cells:12, contrib:25-28. All six now stand in the texts (root 51-55, 62-65, 92-93;
softwareco-agents 251-253; agent pattern 274-275; mathe 427; agent-kernel 316-317, 337-344; nodecode-cells
287-288).

### 8.3 Lost-rule search repeated over the new texts
Method: every line of the revision 1 blocks that is not verbatim in revision 2 was listed by script and traced;
the root, softwareco, owned, nodecode-cells, teachingco, informatik and agent-template rule lines were read
against the new blocks once more. Nothing a session needs is absent at every level. Remarks:

- R1. `docs-list.mjs --from-prompt <prompt-file> --paths-only --wikilink` (softwareco:29) is in no proposed text
  and not in the recipes skill (`grep -c from-prompt`: 0). It stands in `core/agent-scripts/README.md:52`, so it
  is not lost, but the "let go" table does not list it. Add a row.
- R2. `softwareco/ontology/AGENTS.md` has no proposed text and no sentence saying it stays as it is. The
  softwareco lane table names the folder. Say "unchanged" (or cut its last clause, audit 3.5).
- R3. The census line stands in the softwareco text and in the monorepo pattern, so four more times in
  teachingco. The script is a template copy in each (`teachingco/mathe/scripts/preflight-repo-census.sh`
  exists). One fact, five places; it could stand in the root section "In every repo" or stay out of the
  subject repos.
- R4. Narrowed in wording, no rule lost: `ak task scope show|export` became `export` only (owned:24);
  `ak direction export` (contrib:40-42) is not named; "read the route/open-frame status before inventing
  work" (informatik:33, template:26) stands only in the agent-kernel text.
- R5. Pointers the new texts introduce exist: `teachingco/CONTRIBUTING.md` (lines 39-41 carry the push rule),
  `owned/docs/project/standardized-justfile-contract.md`, `owned/scripts/engineering-core-adoption-scan.sh`,
  agent-kernel `layer-12-protocol.md`, `check-direction-legacy-markdown-readiness.py`,
  `render-direction-explorer-mvp.py`, the four router skills. The three softwareco routers do read
  `repo-capability-map.md` (`grep -l` in each SKILL.md), which supports letting owned:34 go.
  `scripts/propagate-template.sh`, named in the agent pattern, was not looked for in an agent repo.

### 8.4 Order of changes: corrected
Audit section 1 item 2 and section 9 now say what D1-D3 found: company files are company-owned and survive an
update; `scripts/**` and `copier/**` belong to the owner of `core/tpl-template-repo` and change by
propagation; no assertion reads a live file; the engineering assertions (1007-1008, 1272-1278) and the
`smoke.sh` check are named. The paths exist: `core/tpl-template-repo/copier-template/AGENTS.md.jinja` and
`copier-template/copier/tpl-*/AGENTS.md.j2` (five). The order (choices; skill; root, company and
softwareco-agents files; templates in parallel; lanes and repos) is the one of section 2 above, with the skill
step of D6 added. D4 is corrected ("eight").

### 8.5 Choices: stated fairly
- Choice 1 is an A/B/C table. Its facts hold: README:44 is quoted correctly; `softwareco/.gitignore:125-135`
  already ignores `agents/*`; `softwareco-agents/` has no `.gitignore`; registry and template say "do not
  nest". The wrong reason for B is withdrawn in so many words. The recommendation moved from B to C; that is
  the owner's to weigh, and the table gives him both costs (C: a lane to build first, AK 8630 registered
  elsewhere; B: nesting). Not verified: that s-U3SNXAYW holds AK 8630.
- Choice 5 (precedence between files) states today's two sentences correctly (root:24, agent-kernel:27) and
  says what B would add and settle. Fair.
- Choice 6 (company-common rules) is fair; "about 400 characters" measures 390 for the four rules.
- R6. Under choice 6 B the texts note covers "the first four"; the diary and TIP sentence would then stay in
  the root alone. Consistent, but say so in the choice.

### 8.6 Figures: confirmed by measuring
Blocks extracted between their fences, in characters: 8,709 / 1,251 / 396 / 92 / 128 / 685 / 501 / 1,324 /
5,539 / 458 / 628, as stated; the contrib file is the infra block with the lane name (94). All seven sums and
percentages of audit section 6 are arithmetically right (10,645; 11,146; 9,690; 11,680; 15,895; 9,167; 9,795).
The card section in the proposed root is 2,904 characters (stated 2,905); today's card with its comment 3,178.
Both documents are within the markdown budget (501 lines / 38,197 bytes; 443 / 25,785).

### 8.7 Not checked in this round
Sections 2-4 of the audit beyond the changed lines; the pattern texts for `nt`, `wib`, `informatik`, which are
not written out; loading the texts into a session.
