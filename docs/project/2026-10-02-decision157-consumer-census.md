---
summary: "AK6451 bounded Decision157 consumer/generation inventory: 347 registrations, indexed old-owner inputs in 44 Git roots, explicit gaps and nine index/worktree differences; no cutover authority."
read_when:
  - "Preparing the Decision157 ontology consumer migration wave."
  - "Reconciling task5651's stale consumer inventory."
type: "reference"
status: "observed-partial"
date: "2026-10-02"
decision_id: 157
governance_task_id: 6451
---

# Decision157 consumer inventory — parallel prerequisite, not cutover

## Purpose and authority

AK6451 refreshes the bounded registration/declaration inventory while another session owns
AK5664. It does not resume deferred AK5651, deploy AK5665, authorize owner edits or close
AK5502. The accepted architecture and migration requirements remain in
[ADR157](../decisions/2026-09-11-softwareco-ontology-consolidation.md) and its
[ordered plan](2026-09-11-softwareco-ontology-consolidation-plan.md).

Initial collection used parent HEAD `6a7bb88f884224a5856c5d8098e67a70b8f9e3a4`; final clean-environment
collection used its receipt-test-only successor `988d512`. The ontology gitlink remained
`b2e42daf61a889c08745b922056b627753f45a2c`. AK5663 was done, AK5664 claimed and AK5665
pending. The earlier [readiness note](2026-09-11-softwareco-ontology-consolidation-readiness.md)
remains historical: its initial OIDs, counts and missing-implementation explanation are not current.
No ontology, consumer, receipt, Git metadata, credential or remote changes are part of this task.

## Reproducible tool and retained evidence

Company-specific tooling lives at `local/scripts/decision157-consumer-census.py`, outside the
L1 template-owned script replacement surface. DB-free fixture tests are in
`tests/test_decision157_consumer_census.py`, invoked by `local/ci/smoke.sh`.

```bash
ak repo list --company softwareco -F json > "$owned_scratch/registrations.json"
PYTHONDONTWRITEBYTECODE=1 python3 local/scripts/decision157-consumer-census.py \
  --registrations "$owned_scratch/registrations.json" \
  --workspace "$PWD" > "$owned_scratch/census.json"
```

`owned_scratch` must be an explicitly owned private directory under `TMPDIR`. The collector itself
never calls AK. It reads root declarations and selected indexed Copier inputs, ontology manifests
and resolution projections. It emits only paths, hashes, locator references and coverage status,
not source bodies or complete Git configuration. Observations retain their index/worktree origin.

Retained packet: `/home/tryinget/.local/state/pi-quests/tmp/ak6451-census.ssPPINO8/`.
Accepted snapshot: `census-clean-env.json`, SHA-256
`e228566a6c3b4b76293a0fa6fb587c3b4ed0f87c8997542a7a646d255c63c4e4`.
Registration export SHA-256:
`070d06e0199c083e001b91a6916b9424f6ad71b03d311cba30fa21deb396fe73`.
Sorted unique registration paths with terminal newline SHA-256:
`1c8855264a1e8f0c1f06d2512239490281757b16c7fe9c7635820f5584db7bee`.
Collector SHA-256 recorded in that snapshot:
`91fe628fdf13a26cf4672e70d0e53cb3dac3c207cd9e5e0f950993df2ddc417f`.

Earlier `census.json`, `census-reviewed.json`, `census-final.json` and `census-accepted.json` are superseded diagnostic
snapshots, not the accepted routing input. Independent review `dispatch-1790964799218` exposed
and then verified fixes for hook execution, metadata escapes, malformed inputs, omitted absences,
misclassification, blocked reads and replacement-object provenance. Its exact-byte acceptance
preceded the YAML `path:` observation addition. Independent tester
`dispatch-1790965971854` subsequently bound the final collector, test and smoke bytes in an
isolated full-history clone: 20 tests passed with TMPDIR both present and absent; seven additional
edge-case fixtures passed. Smoke passed with 37 tests and three pre-existing optional UBS skips.
The normal commit hook then identified inherited-process environment reaching Git subprocesses.
The collector and fixtures now use fixed `/usr/bin/git` and an explicit clean environment, with
no inherited loader, interpreter, credential or PATH configuration. A dedicated poison-environment
regression raises the collector suite to 21 tests; the fresh live rerun retained the same counts.

## Observed denominator

| Observation | Count |
|---|---:|
| Softwareco registrations | 347 |
| Independent existing Git roots | 328 |
| Registrations sharing an enclosing Git root | 2 |
| Missing registration directories | 16 |
| Outside-workspace registration, deliberately not inspected | 1 |
| Index/worktree input observations | 417 |
| Distinct `(Git root, relative path)` input keys | 210 |
| Normalized worktree locations represented by those keys | 202 |
| Explicit absent declaration candidates | 881 |
| Read omissions among admitted roots | 0 |
| Index/worktree pairs with differing content hashes | 9 |

All admitted roots had equal before/after HEAD and index-list digests. This is not a writer fence
or worktree-preservation proof. Index/worktree duplicate views and parent/lane overlapping indexes
must not be counted as different physical consumers. `closure_complete` is always false.

Indexed old-owner candidates: **112 declaration/generation input keys across 44 Git roots**:
80 Copier-answer files and 32 manifests. They represent 106 physical targets because the parent
also indexes six lane declarations. Eight indexed resolution projections are separate observations,
not source-edit targets. Across both origins there are 241 old-owner locator occurrences.

## Owner routing table

Counts are indexed old-owner candidate paths, not confirmed active consumers. Paths are relative
to the Softwareco root. A = Copier answers, M = manifests, P = resolution projections. Owners must
classify active, fixture, archived, excluded or already migrated before exact mutation tasks exist.

| Observed Git root | A | M | P |
|---|---:|---:|---:|
| `.` | 3 | 3 | 0 |
| `contrib` | 1 | 1 | 0 |
| `fork` | 1 | 1 | 0 |
| `fork/dspy-lm-auth` | 1 | 1 | 0 |
| `infra/home-network` | 1 | 1 | 0 |
| `infra/obsidian-vault-ops` | 1 | 1 | 1 |
| `infra/provisioning` | 0 | 1 | 1 |
| `infra/replay-fabric` | 1 | 1 | 0 |
| `owned` | 1 | 1 | 0 |
| `owned/agent-harness` | 1 | 0 | 0 |
| `owned/agent-kernel` | 0 | 1 | 1 |
| `owned/appmapp-platform` | 18 | 0 | 0 |
| `owned/blackwell-kernel-lab` | 1 | 1 | 0 |
| `owned/calisthenics-ai-coach` | 1 | 0 | 0 |
| `owned/compass-c` | 1 | 1 | 0 |
| `owned/dep-diet` | 0 | 1 | 1 |
| `owned/dep-redteam` | 1 | 1 | 0 |
| `owned/dep-surgeon` | 1 | 1 | 0 |
| `owned/designmd-foundry` | 1 | 1 | 1 |
| `owned/dspx` | 0 | 1 | 0 |
| `owned/email-copilot` | 6 | 1 | 0 |
| `owned/feedbackApp` | 1 | 1 | 0 |
| `owned/german-tts-voice-lab` | 1 | 1 | 0 |
| `owned/kinetic-caption-studio` | 1 | 0 | 0 |
| `owned/learner-worlds` | 2 | 0 | 0 |
| `owned/lehrplan-viz` | 1 | 1 | 0 |
| `owned/leseOS` | 11 | 0 | 0 |
| `owned/local-ai-control-plane` | 6 | 0 | 0 |
| `owned/mathe-machraum` | 1 | 0 | 0 |
| `owned/merkschatz` | 1 | 0 | 0 |
| `owned/misegraph` | 1 | 1 | 0 |
| `owned/misegraph-kitchen` | 3 | 0 | 0 |
| `owned/nano-train` | 1 | 1 | 0 |
| `owned/niri-desktop-continuity` | 1 | 0 | 0 |
| `owned/pi-extensions` | 0 | 1 | 1 |
| `owned/project-xeno` | 1 | 1 | 0 |
| `owned/runtime-trace-insights` | 0 | 1 | 1 |
| `owned/semantic-code-intelligence` | 1 | 0 | 0 |
| `owned/semantic-flow-diff` | 0 | 1 | 0 |
| `owned/taschenschach` | 1 | 1 | 1 |
| `owned/test-capabilities` | 0 | 1 | 0 |
| `owned/ts-quality` | 1 | 1 | 0 |
| `owned/workspace-platform` | 1 | 0 | 0 |
| `owned/zotero-plugins` | 3 | 0 | 0 |

The packet supplies every exact relative path, source origin, blob/content hash and locator line.
It includes DSPx's prefixed locator and legacy GitLab spellings for the old Softwareco owner.
Additional relative company-layer inputs occur in `infra/{ds1621-admin,workstation}` and
`owned/nexus-workflow-platform`; workstation also has a relative core-layer input. Class `relative`
does not resolve its destination or authorize normalizing it.

## Nine worktree/index differences needing owner disposition

Root-relative observation keys (not document-relative links):

```text
fork/.copier-answers.yml                                 byte drift; same old-owner locator
fork/pi-mono/ontology/manifest.yaml                      legacy index; old-owner worktree
infra/pilot-infra-strict-l2-20260212/ontology/manifest.yaml legacy index; old-owner worktree
infra/provisioning/.copier-answers.yml                   legacy index; parent worktree
infra/provisioning/ontology/manifest.yaml                old-owner index; parent worktree
infra/provisioning/ontology/dist/resolve.json             old-owner index; parent worktree
owned/dep-viz/ontology/dist/resolve.json                  byte drift; both parent
owned/pi-extensions/ontology/dist/resolve.json            byte drift; both old-owner
owned/semantic-flow-diff/ontology/manifest.yaml           old-owner index; parent worktree
```

Do not announce migration merely from the working files.

Regenerate projections through their owners; never string-replace old receipts. Three root worktree
inputs are untracked: the parent ontology manifest (normal current gitlink topology) and manifests
under `contrib/{pi-mono,local/pilot-contrib-strict-l2-20260212}`. None are staging authorization.

## Validation boundary

Private retained execution reports, deliberately outside Git:

```text
/home/tryinget/.local/state/pi-quests/tmp/ak6451-verify.TA804GBE/REPORT.md
/home/tryinget/.local/state/pi-quests/tmp/ak6451-verify.TA804GBE/rerun-ak6452/REPORT.md
/home/tryinget/.local/state/pi-quests/tmp/ak6451-verify.TA804GBE/final-clean-env/REPORT.md
```

The first isolated full gate exited 1 on pre-existing receipt assertions depending on HOME spelling
and forbidding a valid TMPDIR parent identity. The separately scoped
[AK6452 test correction](2026-10-02-ontology-receipt-isolation.md) preserved strict bindings and
wrong-source rejection. Independent rerun then **passed the declared full gate, exit 0**. The clone's
exact ontology OID matched the parent gitlink; read-only core/ROCS inputs were bound. Thirty focused
tests passed with TMPDIR present and absent. Three optional real-UBS and one obsolete-bundle test
were skipped. No deep or hosted result is claimed. Both candidate docs passed strict metadata and
default reference checks; broader historical docs findings remain outside scope. The final clean-
environment source delta was independently inspected and the full gate rerun passed again; its
focused suite covered all 21 collector tests plus three receipt-path tests, with TMPDIR present
and absent. The receipt doc's final delta was documentary only and passed tracked reference checks.
The real staged commit hook is separate from the isolated scan with optional analyzers unavailable.

## Explicit exclusions and still-open obligations

Missing registrations: `contrib/{automatic_log_collector_and_analyzer,eidetic-engine-docs,
eidetic-engine-website-project,fast_vector_similarity,ffn,gonode,llm-docs,llm_docs,swiss_army_llama,
textract-py3,tsap_mcp_server,visual_astar_python}` and
`owned/{clj-mutate,crap4clj,fcos-proving-lane,voice-dictation}`.
External registration `/home/lightningralf/ai-society/softwareco/owned/agent-kernel` was not inspected.
No registration deletion or historical retirement is authorized by absence.
Shared-root registrations are the packages `owned/obsidian-plugins/packages/obsidian-excalidraw-layer-manager`
and `owned/pi-extensions/packages/pi-vault-client`; their enclosing Git roots, not fictitious
independent repositories, govern tracked source.

Still needed for AK5651:

1. Accountable owner dispositions for the indexed/generation candidates, differences and exclusions;
   account for nonregistered, external and arbitrary-untracked variants not covered here.
2. Close receipt-reader/writer and generator-consumer contracts beyond these selected declarations;
   test fresh generation and update convergence, not only locator spelling.
3. Refresh and prove full refs/configuration/reflog/ignored/untracked preservation and restoration.
4. Complete and separately admit AK5664/5665's runtime route; rehearse history-preserving stale-path
   refusal and whole-wave rollback before the canonical source cutover.
5. Admit exact per-owner migration tasks and verify hosted CI under AK5502. Task6270 tracks this
   cutover rather than a separate implementation. Evidence11643 already grants publication of the
   tree at the Decision157 cutover, conditional on a fresh exact-tree disclosure/secret check;
   evidence11624 forbids private-history import. Do not request redundant permission, publish
   before the cutover prerequisites, or confuse that conditional permission with completed rollout.

These obligations remain open; this artifact and its passing fixture tests are not completed
consumer closure, migration, runtime deployment, remote publication or hosted-CI recovery.
