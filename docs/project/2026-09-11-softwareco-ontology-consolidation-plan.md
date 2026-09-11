---
summary: "Proposed source-first execution, validation and rollback contract for parent-owned Softwareco ontology."
read_when:
  - "Planning or validating Softwareco ontology consolidation and consumer migration."
type: "plan"
status: "proposed"
date: "2026-09-11"
decision_id: 157
governance_task_id: 5650
---

# Softwareco ontology consolidation — ordered execution contract

This is a proposed companion to `2026-09-11-softwareco-ontology-consolidation-rfc.md`, not execution
proof. AK remains authoritative. No source migration is admitted until accepted successor decision,
current continuation artifacts, exact owner task scopes and phase-specific preflights exist.

## S0 — baseline, complete census and preservation

Owner: Softwareco controller, with explicit source-owner inspection/handoffs.

- Bind fresh parent HEAD/index/worktree and ontology HEAD/tree, all refs (including remote-tracking
  and stash refs), remotes/configuration, gitdir/common-dir layout, and every ignored/untracked path.
- Current planning inputs are parent `6eb1542e7f742dc3dfe29503503e140c4ce56362` and ontology
  `07d4b8b89f6ca436618adb42827885e9a45289c7`; rebind on any drift, never mechanically replay.
- Create verified full-ref parent and ontology bundles plus separate configuration/reflog/untracked
  preservation as required. Prove restore, not file presence. Keep backups outside tracked parent
  content, private, under approved storage; use the heavy-job runner if multi-GiB.
- Fingerprint unrelated tracked and untracked state before/after each integration action. Parent
  receipt WIP is not scratch. Root gates clean and regenerate outputs, so do not run them in the
  dirty canonical checkout.
- Build a bounded machine-readable census across the registered Softwareco repo set and their
  source-owned generators. Record exact Git root, tracked/untracked class, source ref, manifest,
  persisted Copier input, receipt readers/writers, generation path and whether migration is required.
- Identify all external or separately operated consumers and test whether they require independent
  access, release or rollback. A real conflicting contract returns to design; do not silently widen
  scope or access. Untracked operator manifests are observed, not authorized mutation targets.
- Specify the exact retained semantic corpus/doc paths and every excluded standalone-owner file.
  Compare bytes/modes to the bound old OID. Scan the import for secrets before any publication
  proposal. No historical private refs/stashes/config are imported into public parent history.

### Initial census — lower bound, not final execution scope

Parent tracked live authoring inputs: `.copier-answers.yml` and `ontology/manifest.yaml` in each of
`contrib`, `fork`, and `owned` (six inputs). Parent-tracked generated references exist in their
receipts/resolve/summary artifacts; regenerate in the proper owner, do not string-replace evidence.

Fixed-depth physical old-locator census: 30 exact `<repo:softwareco/ontology@main>` manifests,
27 tracked by their actual owners:

- `contrib`: lane root; untracked manifests in `pi-mono` and
  `local/pilot-contrib-strict-l2-20260212` (observe only).
- `fork`: lane root, `dspy-lm-auth`, `pi-mono`.
- `owned`: lane root and tracked children `agent-kernel`, `blackwell-kernel-lab`, `compass-c`,
  `dep-diet`, `dep-redteam`, `dep-surgeon`, `designmd-foundry`, `email-copilot`, `feedbackApp`,
  `german-tts-voice-lab`, `lehrplan-viz`, `misegraph`, `nano-train`, `pi-extensions`, `project-xeno`,
  `reasoning-budget-proxy`, `runtime-trace-insights`, `taschenschach`, `test-capabilities`,
  `ts-quality`; untracked/non-independent `email-triage` (observe only).
- `infra`: `pilot-infra-strict-l2-20260212`, `replay-fabric`.

Review separately: prefixed old locator in `owned/dspx`; legacy GitLab locators in non-independent
`owned/experimentation` and `owned/to-sort`; relative-path consumers in
`owned/nexus-workflow-platform` and `infra/{ds1621-admin,workstation}`. Already-parent consumers
include infra root, `infra/{issue-tracker,provisioning}` and seven owned children. Do not normalize
unrelated historical drift as a side effect; classify its effect on this cutover and bind only new
migration work to the proper owner.

Generator input: `copier/tpl-project-repo/copier.yml` defines `company_ontology_ref` with default
`<repo:{{ company_slug }}/ontology@main>`. The canonical L0 source is under
`core/tpl-template-repo/copier-template/copier/tpl-project-repo/`. This is not permission to edit the
vendored copy. Explicit input may suffice; prove every supported generation and rerun path.

## S1 — reversible ownership-transition capability (L0 owner)

Create a separate scoped `core/tpl-template-repo` task. Read its engineering/process chain first.
Use the existing transition owner surface, not a consumer-local fork:

- CLI: `scripts/lib/l1_template_ownership.py --transition-action plan|apply|finalize`.
- Engine: `scripts/lib/l1_template_transitions.py`.
- Generated history checker: `copier-template/scripts/lib/check-l1-ownership-state.py`.
- Tests: `tests/test_l1_template_transitions.py`, plus declared L0 gates.

The existing ancestor-overlap validator allows tree-to-gitlink collapse only. Prove the entire
reverse path, not just a symmetric conditional: exact deletion of an old mode-160000 path plus
classified additions below it, mode/OID/payload checks, no ambiguous ancestor writes, authority and
scope checks, symlink/nested/hardlink safety, old-byte binding, pending apply and evidence-finalize,
interruption/retry, rollback, and history verification. Reject generalized overlaps. Preserve
existing forward-transition and all negative tests. Generated checker fresh bootstrap and existing
consumer convergence are both required. If a schema/release change is needed, its owner governs it.

Only promote verified owner-generated tooling to Softwareco through the supported L0-to-L1 path.
No global ontology locator default or unrelated-company behavior change is implied.

## S2 — source/registry and consumer cutover preparation

Owners: Softwareco, each affected lane/repository, AK for registry lifecycle.

- Define the accepted parent source locator/revision and preserve the ontology ID/content contract.
  `@main` now refers to Softwareco's revision, not the former nested repository. Never downgrade to
  loose mode or treat ordinary authority receipts as proof of byte/commit equivalence.
- Bind exact per-owner migration tasks after final census. Update manifests and persisted Copier
  answers together; test fresh generation and update/rerun convergence. Source-owned templates go
  through L0; unrelated company defaults stay unchanged.
- Prepare and test consumers against an isolated complete parent candidate. Keep the canonical
  old owner usable until the coordinated cutover; do not detach `.git` first and break consumers.
- Determine and prove the AK owner-supported retirement/source-transfer operation for the old
  registered repo identity. Preserve task/evidence history. If no lawful operation exists, record
  the exact gap and obtain AK-owner support before canonical de-nesting. No SQLite edits, invented
  aliases or silent re-registration.
- Define an explicit local cutover window: pause affected writers, land required owner consumer
  changes in the reviewed order, then switch parent topology before resuming. Intermediate states
  must fail closed and must not be announced as usable. Roll back the wave if convergence fails.
- Do not pre-publish consumer changes against a parent commit that is unavailable remotely.
  Remote publication order remains a separate owner-authorized operation, not part of local proof.

## S3 — isolated parent transition and proofs

Owner: Softwareco, exact transition task distinct from this design task.

- Use a clean registered target worktree/verified isolated context and owner-supported transition
  contracts. Do not widen tool allowlists, create unowned scratch, or mutate canonical WIP.
- Bind the accepted ADR commit, predecessor ownership state/map, full old owner OID/tree, exact
  import/exclusion classification, new parent `ontology/**` agent ownership, and exact Git delta.
- Replace the gitlink with ordinary files; remove only its `.gitmodules` section. Unrelated raw
  gitlinks and submodule registrations are out of scope. No recursive initialization or blanket
  deletion. Preserve inert `.git/modules/ontology` metadata/refs until verified rollback retention
  and AK identity reconciliation permit any later retirement action.
- Remove the active ontology-fetch/token dependency from root workflow/gates and obsolete standalone
  materializer entrypoints/tests. Add positive normal-tree and negative unexpected-gitlink/metadata,
  missing/symlink/malformed-source tests. Do not remove the core ontology dependency or weaken
  semantic, output-custody, supply-chain or full-history checks.
- Keep `governance/ontology-dist/`; regenerate exact planned outputs under canonical parent identity.
  Never copy old snapshots/receipts and relabel them. Account for revision-bound snapshot changes.
- Apply pending ownership state, commit its exact delta, obtain external AK evidence, then finalize
  in the required state-only commit. No inline state/map hash repair or rewriting prior evidence.

Required matrix:

1. Fresh full-history parent checkout has ordinary tracked source and passes root gates without
   ontology token, nested `.git`, submodule initialization or access to the old ontology remote.
2. Old locator fails after genuine de-nesting; selected parent locator succeeds in strict mode.
3. Every tracked in-scope consumer resolves the intended corpus; variant/untracked exclusions have
   explicit owner disposition rather than disappearing from the denominator.
4. Retained semantic bytes/modes equal the selected old source; content changes are separately
   reviewed ontology-owner work, not folded into the transport.
5. Source identities/snapshots/receipts re-baseline correctly; an unrelated parent commit changes
   revision-bound provenance as expected. No claim of identical snapshot identity.
6. New and existing checkouts converge; interruption/retry and rollback preserve refs/stashes,
   ownership lineage, staged scope and unrelated work. Preserved archives restore successfully.
7. Declared parent census, smoke, template-CI, full/deep, transition/checker and each affected owner
   gate pass on the exact candidate. Run writers in isolated outputs, not canonical receipt WIP.

## S4 — canonical integration and final verification

- Stop on any reviewed-input drift. Dirty receipt paths must be preserved outside mutation or receive
  explicit owner disposition; their mere generated nature does not authorize overwriting them.
- Recheck before/after fingerprints, scope, parent/source refs, stash/configuration and AK identity.
  Do not stash, clean, reset, force, stage all, or silently absorb another session's changes.
- Integrate only exact reviewed commits/transition actions with all proof and rollback artifacts.
  Make the agreed cutover, then verify all affected actual owners before resuming normal operation.
- Independent final review must distinguish local acceptance from hosted behavior. No push,
  visibility change, credential action or remote deletion occurs in this wave.
- Re-evaluate task 5502: local removal of the credential dependency is not hosted-CI success.
  Keep a properly bound publication/hosted-verification gate until authorized publication and a
  fresh hosted run prove the replacement. Do not claim the existing red run repaired by documents.

## Rollback and claim limits

Before canonical cutover, discard only proven task-owned inactive candidate state. After cutover,
use a separately scoped ordered forward/revert transition restoring the prior parent map/state,
gitlink, exact owner metadata/OID, consumer locators and generated receipts through their owners.
Rehearse dependent-consumer rollback as well as parent rollback; never restore just the pointer and
leave consumers bound to the other identity. Restore from verified bundles/config archives without
rewriting live remote refs, activating stashes or restoring AK from stale files.

A reviewed plan is not reverse-transition support, an isolated pass is not canonical adoption,
canonical adoption is not remote publication, and a local pass is not hosted-CI proof.
