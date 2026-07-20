---
summary: "Softwareco L1 contract for the embedded tpl-project-repo output, freshness policy, and validation surface."
read_when:
  - "When changing the Softwareco tpl-project-repo structure or generated L2 output."
  - "When deciding whether a project document is living authority, a dated snapshot, or runtime-owned state."
type: "reference"
---

# `tpl-project-repo` file contract

This document describes the **current Softwareco L1 projection** of `tpl-project-repo`. The L0 authoring architecture remains owned by `core/tpl-template-repo`; changes made here must either remain an explicit L1 specialization or be promoted through that owner rather than being presented as L0 truth.

## Render boundary

| Layer | Role | Path |
|---|---|---|
| L0 | canonical template architecture and propagation owner | `core/tpl-template-repo/` |
| L1 | Softwareco company template and embedded L2 baselines | `softwareco/copier/tpl-project-repo/` |
| L2 | rendered standalone project repository | selected Softwareco lane/repository path |

The allowed render edges are `L0 -> L1` and `L1 -> L2`. A package generated inside an L2 monorepo is an internal member, not an additional repository layer.

## Output domains

### Repository control plane

- `.copier-answers.yml` — render provenance; committed.
- `AGENTS.md` — repository-specific operating rules.
- `CODEOWNERS` — review routing, not proof of a live appointment.
- `README.md` — human entrypoint.
- `next_session_prompt.md` — stable startup procedure, not a mutable status handoff.

### Delegation and flow contract

Generated `AGENTS.md` files are company-neutral and do not appoint organizational roles. They require accepted delegation discovery, scoped owner-native task admission, finite WIP, separation of validation from outcomes/effects, explicit authority for external and terminal actions, and fail-closed escalation on owner ambiguity. CTO/technical-steward packets remain freshness-bounded projections rather than task or authority stores.

Decision 68 authorizes this L1 source contract and fresh-render testing before the issue-tracker canary. It does not authorize production generation of new L2 repos or non-canary L2 updates; those remain frozen until a separate accepted template-owner AK decision.

### Product and organizational documentation

- `docs/project/purpose.md`, `mission.md`, and `vision.md` — durable narrative direction.
- `docs/project/product_posture.md` — stable living current/target maturity surface.
- `docs/project/model.md` — concise project-model navigation.
- `docs/org_context/` — inherited organizational context, selected by profile.
- `docs/decisions/` and `docs/learnings/` — human-readable decisions and crystallized learning; accepted runtime authority still belongs to the owning runtime.
- `diary/` — dated raw session capture, not canonical task or decision state.

The template does not scaffold `strategic_goals.md`, `tactical_goals.md`, `operating_plan.md`, or `operational_plan.md`. AK-native direction, waves, tasks, decisions, and evidence own live execution state where those surfaces are implemented and accepted.

### Governance and validation

- `governance/work-items.json` — checked-in AK projection, not live authority.
- `governance/work-items.cue` — projection validation contract.
- `governance/task-scopes/` — optional frozen AK exports.
- `scripts/check-task-scope-snapshots.sh` — snapshot drift check.
- `scripts/check-document-policy.sh` — posture freshness and dated-snapshot check.
- `scripts/ci/fast.sh` and `scripts/ci/full.sh` — staged validation.
- `scripts/rocs.sh` and `tools/rocs-cli/` — deterministic semantic tooling path.

## Product-posture freshness contract

`docs/project/product_posture.md` keeps a stable path because it is the living product-wide posture, not a serial status report. It requires:

```yaml
as_of: "YYYY-MM-DD"
last_validated: "YYYY-MM-DD"
last_validated_commit: "<full 40-character commit SHA>"
evidence_paths:
  - "README.md"
  - "src/"
  - "tests/"
```

Field meaning:

- `as_of` is the latest UTC date through which the current-posture claims intend to be accurate.
- `last_validated` is when an accountable owner checked those claims against all declared evidence paths.
- `last_validated_commit` is the exact reviewed evidence baseline.
- `evidence_paths` are repo-relative literal tracked files or directory prefixes that substantiate current-state claims.

The posture is stale when either:

1. more than 30 calendar days have passed since either `as_of` or `last_validated`; or
2. a reachable commit after `last_validated_commit` changes a declared evidence path.

Any baseline that is missing, not an ancestor of `HEAD`, or unavailable in a shallow clone makes freshness **unverifiable**. CI fails closed rather than claiming freshness.

CI also fails when declared evidence or the posture has uncommitted changes, when any intervening commit touched declared evidence even if later reverted, or when the commit sequence does not contain exactly one posture-validation commit after the evidence baseline. That last rule prevents later claim edits from inheriting an older validation stamp.

A commit cannot truthfully contain its own SHA. Refresh in two commits: first land the evidence state; then validate and update the posture metadata to point at that earlier commit.

## Dated time-bounded documents

Separate transition, migration, seam-specific current-vs-target, and status snapshots use:

```text
YYYY-MM-DD--transition--<scope>.md
YYYY-MM-DD--migration--<scope>.md
YYYY-MM-DD--current-vs-target--<scope>.md
YYYY-MM-DD--status--<scope>.md
```

The prefix is the snapshot/validation date, not a promise of continuing freshness. Newer relevant commits or the 30-day horizon require revalidation or a new dated snapshot. Old snapshots remain historical evidence and must not be routed as current truth.

This policy does not date:

- the stable living `product_posture.md` path;
- durable purpose, mission, vision, architecture, or accepted policy merely because they discuss transitions;
- diary files, which already follow their own dated naming contract.

The checker validates explicit `--transition--`, `--migration--`, `--current-vs-target--`, and `--status--` grammar plus a narrow set of unambiguously snapshot-shaped legacy names. It deliberately does not classify arbitrary prose filenames such as `database-migration-guide.md` or `http-status-codes.md`; owner review and the inventory process still govern semantic classification.

## Validation

From the Softwareco root, validate the embedded template with:

```bash
bash ./scripts/check-template-ci.sh
```

A rendered L2 project runs:

```bash
./scripts/check-document-policy.sh
./scripts/ci/full.sh
```

The generated product posture intentionally starts as `UNVALIDATED`; full validation must fail until a real owner supplies evidence-backed metadata.

## Change order

When changing the Softwareco L1 projection:

1. update `copier/tpl-project-repo/`;
2. update this contract when topology or semantics changed;
3. update adjacent README/AGENTS guidance by reference rather than copying volatile status;
4. run `bash ./scripts/check-template-ci.sh`;
5. promote reusable architecture changes to `core/tpl-template-repo` through its owner workflow when appropriate.

Do not cite removed L0-only fixture commands from this L1 repository, and do not imply that editing this rendered projection automatically changes L0 or existing L2 repositories.
