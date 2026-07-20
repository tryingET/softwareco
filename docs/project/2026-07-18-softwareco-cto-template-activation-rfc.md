---
summary: "RFC for activating Softwareco's Org Owner/CTO Agent delegation and strengthening L1 agent/project templates before an issue-tracker canary."
read_when:
  - "Reviewing or implementing Softwareco CTO Agent governance and L1 template activation."
type: "rfc"
status: "proposed"
date: "2026-07-18"
tier: "architecture"
---

# RFC — Activate Softwareco CTO Agent and L1 agent/project contracts

## Decision requested

Accept a bounded Softwareco governance and L1-template activation before the `infra/issue-tracker` canary. This RFC grants no authority by itself; activation begins only when an accepted Softwareco-scoped AK decision records the appointment, delegation, ADR, and linked execution task.

The decision creates an explicit exception to Decision 62's clauses that did not authorize a second pilot or automatic Factory Flow schema, L2-template, or L0 propagation. Decision 62 did not prohibit editing the Softwareco L1 source template, but its accepted learning and `docs/org/strategic_objectives.md` blocked treating such edits as a propagated contract before a materially different pilot and separate template-owner decision. This RFC narrowly overrides that ordering only to authorize pre-canary L1 source edits and one canary migration. The exception authorizes:

1. Softwareco L1 source-template changes;
2. fresh-render validation of those sources;
3. one reversible existing-L2 migration canary in `infra/issue-tracker`.

It does not claim factory-wide proof, change L0, update other existing L2 repos, or permit production generation of new L2 repos from the changed templates. New production L2 generation and every non-canary L2 update remain frozen before and after any canary outcome unless a separate accepted template-owner AK decision authorizes them. A terminal `stop`, `redirect`, `complete`, or `continue` decision does not itself lift that freeze.

## Governance activation record

### Accountable human appointment

On acceptance, the AK decision records:

- appointee: `human-operator`, the higher-level human directing this activation;
- accountable role: **Softwareco Org Owner**;
- domain: Softwareco company portfolio, boundaries, appointments, and cross-domain tradeoffs;
- reserved decisions: portfolio start/stop, owner appointment, terminal decisions, privacy, consent, ethics, licensing, security exceptions, irreversible/public/external effects, authority-boundary changes, and delegation revocation;
- review date: 30 days after acceptance or the issue-tracker canary terminal decision, whichever comes first;
- revocation: immediate instruction from `human-operator`, incident stop, or decision supersession;
- evidence: this RFC, its reviews/synthesis, ADR, implementation/rollback plans, and canary receipts;
- direction linkage: one active Softwareco strategic frame and one bounded implementation wave.

Until that accepted record exists, the proposed governance remains inactive.

### CTO Agent delegation contract

| Field | Delegation |
|---|---|
| Delegator and accountable owner | `human-operator` as Softwareco Org Owner |
| Delegatee | `softwareco-cto-agent` |
| Domain | bounded technical strategy, L1 template activation, and issue-tracker canary flow |
| May decide | reversible sequencing and technical implementation choices inside accepted AK task scope |
| May execute | scoped source changes, deterministic validation, evidence capture, cold-start tests, and owner handoffs |
| Must consult | affected project/template owner for source-contract changes; FCOS owner only for genuine cross-repo gates |
| Must escalate | owner ambiguity; privacy, consent, ethics, licensing, security, cross-domain, authority-changing, irreversible, public, release, publication, or external-effect decisions |
| Evidence required | scoped task, validation receipts, outcome evidence, rollback evidence, and explicit terminal human decision |
| Expiry | 30 days after acceptance, canary terminal decision, or immediate revocation—whichever comes first |
| Revocation/stop | human instruction, incident stop, expired delegation, or superseding AK decision |

“Enforce gates” means stop and escalate. It never means waive a gate, accept an architecture decision, appoint an owner, or mutate owner/external state without task scope and lawful authority. The CTO Agent may recommend—but not make—the terminal `continue`, `stop`, `redirect`, or `complete` decision.

## CTO operating packet

The CTO Agent maintains no shadow backlog. Its weekly packet is a freshness-bounded projection from owner-native state containing:

1. accepted delegation/decision reference and expiry;
2. active strategic frame and implementation wave;
3. accountable owner and current outcome metric;
4. WIP, blocked age, and displaced work;
5. source-owner and cross-owner handoffs;
6. validation and outcome evidence gaps;
7. human-reserved or external-effect decisions required;
8. one recommendation: `continue`, `stop`, `redirect`, or `complete`.

AK remains task/direction/decision/evidence authority. FCOS is used only for genuine cross-repo control-board coordination.

## Template contract

### Shared L1 contract

Both project and agent templates state:

- repository instructions do not appoint organizational roles or grant company delegation;
- delegation is discovered through accepted AK/governance state and fails closed when missing or expired;
- active work requires a scoped owner-native task and finite WIP admission;
- passing validation is not an outcome, release, external-effect, or lifecycle authorization;
- external effects and terminal decisions require explicit human/owner authority;
- agents stop and escalate owner ambiguity rather than inventing authority.

The contract remains company-neutral; Softwareco's named delegation stays in Softwareco governance.

### Project template delta

Preserve AK work-items, task-scope, product-posture, owner routing, and deterministic validation contracts. Add the shared delegation/flow contract and the minimum CTO-packet handoff fields without hardcoding Softwareco.

### Agent template delta

An agent repository is an agent product/capability source owner, not an organizational appointment. The generated output must:

- use main-first workflow with accepted repo-local exceptions;
- generate `governance/README.md`, `governance/work-items.cue`, `governance/work-items.json`, and `governance/task-scopes/`;
- generate `scripts/check-task-scope-snapshots.sh` plus its parser-backed helper;
- use `AK_CMD="${AK_CMD:-ak}"` and plain installed `ak` for work-items and task-scope checks;
- fail on work-items drift when AK and the registered repo are available, and fail clearly rather than silently substituting another authority when AK is required;
- document import/export/check and task-scope commands in README;
- provide generic engineering-core stack-contract guidance without pretending a language lane exists;
- remove the embedded `prompts/cognitive-tools/` catalog and route reusable procedures through Prompt Vault governance/read surfaces;
- retain persona, safety, learning, activity-prompt, and deterministic validation surfaces.

## Staged execution

1. Complete immutable authority and template reviews plus controlling synthesis.
2. Accept the AK decision/ADR, appointment, and bounded CTO delegation.
3. Track implementation and validation/rollout/rollback plans.
4. Mutate and validate L1 templates; keep new production L2 rendering paused.
5. Authorize an exact issue-tracker source-owner canary task.
6. Apply the reversible canary migration and run fixed cold-start scenarios.
7. Record effectiveness/conformance evidence and KES learning.
8. Obtain the human terminal decision.
9. Use a separate template-owner decision for broader L2 or L0 propagation.

## Issue-tracker canary exception

Authorize one existing-L2 migration canary at baseline `infra/issue-tracker` main commit `7f04a290ac9c9f14d3de3034755753ea5323cf6f`.

The canary may change only paths named in its AK task, expected to include repo-local `AGENTS.md`, `README.md`, projection/export validation scripts, and tests needed to exercise the shared contract. It follows Softwareco's main-first workflow, must preserve an exact baseline diff, and must provide a one-command restoration or revert path; a branch or PR is used only when the operator explicitly requests a review gate.

Fixed cold-start scenarios must classify:

- canonical AK state versus `STATE.json` projection;
- projection-valid, projection-drift, blocked, review-ready, and submission-ready states;
- external-effect commands that require explicit human approval.

No issue submission, comment, push, publication, release, or other external mutation occurs without a separate explicit human instruction. The preserved WIP branch is evidence/input, not merge authority.

The canary validates the project/operator boundary. Fresh-render tests validate the agent-template output; issue-tracker alone does not prove agent-template or customer-product effectiveness.

## Acceptance tests

Template CI must verify in source and rendered outputs:

- all six shared contract points;
- agent governance/work-items/task-scope files and executable checker;
- plain-AK import/export/check commands and full-CI invocation;
- failure on a stubbed work-items drift result;
- absence of “work via proposals + merge requests” and `prompts/cognitive-tools/`;
- presence of a concrete Prompt Vault route and generic engineering-core guidance;
- issue-tracker canary remains separately gated.

Also run strict docs validation, template CI, rendered full-CI with deterministic AK stubs where needed, and `git diff --check`.

## Rollback

- supersede/revoke the AK delegation record rather than rewriting history;
- revert isolated L1 template/governance commits;
- restore issue-tracker to its recorded baseline by reverting the isolated main-first canary commits;
- verify template CI, issue-tracker validation, AK projections, and absence of external effects;
- leave L0 and all non-canary L2 repos unchanged.

## Non-authorizations

- no L0 template change;
- no production generation or update of non-canary L2 repos before or after terminal review without a separate accepted template-owner AK decision;
- no customer-product factory claim;
- no permanent CTO Agent appointment;
- no external issue-tracker mutation;
- no FCOS authority change.
