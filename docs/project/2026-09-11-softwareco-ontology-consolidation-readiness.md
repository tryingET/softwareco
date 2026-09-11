---
summary: "Decision 157 readiness: reverse-transition code is verified; consumer closure and safe AK identity retirement still block canonical ontology cutover."
read_when:
  - "Continuing Decision 157 or executing its AK-owner prerequisite."
type: "reference"
status: "blocked"
date: "2026-09-11"
decision_id: 157
governance_task_id: 5651
---

# Decision 157 readiness — no canonical cutover yet

## Verified progress

- Decision157 is accepted with independent current-track review and designated synthesis. ADR:
  `../decisions/2026-09-11-softwareco-ontology-consolidation.md`; architecture evidence 9086.
- L0 task5652 implemented narrow receipted gitlink-to-regular-files transitions in source commit
  `84d6c81e0b1146940ded9bf1bf6ede222acf67f8`, evidence **9103**. Full tested tree
  `e1accdb510e0604775496742bbc2f4161705fd2a` equals the entire committed source tree.
- Seventeen focused tests pass, including actual plan/apply/finalize, generated history checking,
  receipted forward inverse and byte-exact rollback. Independent source review
  `dispatch-1789116491752` returned GO and checked 1,152 valid mode/order combinations; only four
  intended reverse admissions changed. This is not Softwareco runtime migration proof.
- All seven declared L0 gates passed, with zero failures/skips/warnings, in a clean no-hardlinks
  private validation clone. This avoids pre-existing unowned Python cache residue and protected
  source WIP without deleting either. The source diary describes the earlier scope-blocked direct
  run; evidence9103 records the later isolated full acceptance.
- Parent and ontology full-ref bundles were created/verified. An isolated ontology mirror restored
  all 17 listed ref OIDs; `git fsck --full --no-reflogs` passed. This proves object/ref restoration,
  not complete configuration, symbolic-ref, reflog, ignored/untracked or writer-fenced restoration.
  Those preservation requirements remain open before cutover.

The canonical parent still has the mode-160000 ontology entry and clean nested owner at
`07d4b8b89f6ca436618adb42827885e9a45289c7`. No consumer locator, receipt, source bytes, nested
metadata, GitHub visibility, credential or remote publication was changed by this work.

## Registered-consumer census: membership complete, migration closure incomplete

Read-only inventory provenance: `dispatch-1789115684516`; observed AK-source revision `232ab7a`.
The exact sorted Softwareco registration paths, newline-delimited including a final newline, hash to
`10fff7c3b10e3033640e47ab6169b89e3d548b66fed94b797df80129168d9a6b`.
The parent independently recomputed this digest. Counts are observation-time facts, not permanent
registration truth.

| Observation | Count / disposition |
|---|---|
| All AK repository rows | 380 |
| Rows with company Softwareco | 345 |
| Under current Softwareco checkout | 344 |
| Additional row | Missing historical alternate-home agent-kernel path |
| Existing / missing Softwareco registration paths | 328 / 17 |
| Existing registrations sharing enclosing Git roots | Two L3 package registrations |
| Non-null ontology_ref/copier_answers/generated_from registration metadata | Zero; not proof of no dependency |

Exact membership must compare the returned registration path, not just successful `ak repo show`.
CLI path normalization can select an enclosing Git root. Three non-independent directories returned
the owned-lane row. Source evidence: `agent-kernel/crates/ak-cli/src/main.rs:4031–4055,25434–25445`.

### Reconcile the initial 30 physical / 27 tracked count

- Registered root inputs: 28 physical exact-old manifests, 26 tracked.
- Unregistered `owned/reasoning-budget-proxy`: one tracked exact-old manifest.
- Non-independent `owned/email-triage`: one untracked exact-old manifest.
- The other untracked exact-old manifests are `contrib/pi-mono` and
  `contrib/local/pilot-contrib-strict-l2-20260212`.

Together these reproduce 30/27 but do not define the full migration denominator.
Registered variants also include prefixed old locator `owned/dspx`, relative paths in
`owned/nexus-workflow-platform` and `infra/{ds1621-admin,workstation}`, and ten already-parent
manifests. Untracked non-independent `owned/{experimentation,to-sort}` still have legacy GitLab
locators. Observe untracked/operator pre-state; do not bulk-replace or stage it.

### Generation inputs materially enlarge the impact

Of 61 registration-root Copier files: 31 retain exact-old Softwareco input, 19 retain the legacy
GitLab example, seven select the parent, one selects Healthco, and three omit the input. These are
classifications, not authorization to normalize all companies or historical examples.

Twelve registered roots have exact-old Copier input but no root ontology manifest:
`owned/{leseOS,kinetic-caption-studio,zotero-plugins,workspace-platform,semantic-code-intelligence,
calisthenics-ai-coach,local-ai-control-plane,agent-harness,misegraph-kitchen,appmapp-platform,
niri-desktop-continuity,merkschatz}`.

Tracked-index inspection found 43 additional nested exact-old Copier inputs, excluding duplicate
parent-tracked lane files: leseOS10, email-copilot5, zotero-plugins2, local-ai-control-plane5,
misegraph-kitchen2, learner-worlds2, appmapp-platform17. These are generation dependencies, not proven
active semantic consumers; owners must classify active, fixture, archived and unrelated inputs.

Project templates default to the separate company locator. Monorepo/package templates retain legacy
GitLab defaults. Prefer the existing explicit `company_ontology_ref` input where it suffices; do not
blindly rewrite source-owned templates or unrelated companies. Prove generation and update behavior.

Remaining census work: missing registrations, nonstandard/unregistered/external consumers, receipt
readers/writers, active-versus-fixture classification, exact owner task scopes and explicit exclusions.
Already-parent consumers still need source/corpus and provenance validation.

## Hard blocker: AK historical identity and stale-path retirement

The exact old ontology registration exists. Its observed operational-status output was
`unclassified`, `include_with_warning`, `projection_only=true`, `exclusion_authorizing=false`.
An inert Git archive preserves custody but does not retire that runtime path.

Source-owner inspection found:

| Surface | Why it does not provide the required transition |
|---|---|
| `ak repo rebind-path` | Alias repair requires the same canonical Git working-tree root and compatible metadata; a separate restored archive is not equivalent. It also rewrites attribution. |
| `ak repo delete` | Cascades live task/model/ontology/lineage/tracker deletion; unacceptable historical loss. |
| `ak repo register` | New/upserted path is not a lifecycle retirement, attribution-preserving move or old-path refusal. |
| operational-status | Observation-only; production dependency graph excludes a live transition writer. |

Evidence locations in `agent-kernel/crates/ak-core/src/repo.rs`: alias eligibility533–606,
lexical/database resolution883–945, register965–998, list1235–1271, attribution-rewriting rebind
1438–1658, delete1663–1675. `repository_operational.rs:1–5` excludes production transitions.
CLI nearest-registration selection at `main.rs:3932–3951` and Git-root preprocessing differ from
core exact-path resolution. De-nesting without a proved owner protocol can therefore leave ambiguous
runtime selection. This is source-grounded risk, not an executed destructive experiment.

Existing accepted Decisions146/147 and ADR-0038/0039 cover successor architecture but retain the
predecessor root and defer general retirement/corrections. Do not assume an implemented writer.
Task5304/evidence8171 ended at a feasibility stop. Its missing-provenance-owner statement is now
stale: task5305/Decision148 selected workstation; task5306/Decision150 accepted its implementation
design. Those outcomes explicitly claim no implementation, signer, installed binary or P0 pass.

**Owner route:** AK task **5653** now has an exact documentation/review scope, done contract and
guardrails. It must establish the smallest lawful reversible retirement/source-transfer route,
reconcile the existing successor decisions, preserve historical attribution, and prove stale-path
refusal. It must not expand the entire successor system unless necessary, exploit rebind after
removing `.git`, delete data, invent aliases or mutate the active DB. Actual production support
requires separately scoped implementation/proof following owner decision gates.

ADR157 invariant7 controls: bind and rehearse a reversible AK lifecycle operation, or leave
irreversible retirement unperformed with safe stale-path behavior until rollback retention ends.
Restoring `.git` does not establish AK rollback. Task5651 is blocked on this route and its eventual
executable proof; task5653 documentation completion alone is not the trigger for cutover.

## Preservation limits and operational corrections

The initial scratch restore used a no-checkout clone and attempted to fetch directly over its
checked-out main; Git correctly refused. No canonical repository was affected. A new separate
mirror clone restored all advertised source ref OIDs and passed fsck. Neither the failed attempt nor
bundle presence alone was treated as successful full preservation.

Current unrelated parent receipt changes remain protected. No canonical cleanup or validation
writer has run. Source-template operator dirt and old cache residue remain untouched. No stash,
reset, force, remote change or broad staging was used. Artifact-only design commits and the exact
source-template capability commit do not admit parent integration.

## Next legal action and completion boundary

Continue the concrete AK-owner protocol task5653; keep S0 census and preservation evidence current.
After accepted and executable identity support, complete owner dispositions, promote source tooling,
prepare exact consumer changes and run isolated/canonical cutover gates from the accepted plan.
Do not mass-create mutation scopes from a textual search count.

Task5502 is now bound to Decision157 local consolidation plus separately authorized publication and
fresh hosted verification, deferral341. The old credential-provisioning remedy is no longer planned.
No-push remains in force; local acceptance cannot close the hosted-CI obligation.
