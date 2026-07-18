---
summary: "Softwareco company and L1 control-plane entrypoint: identity, operating model, architecture navigation, lanes, and template capabilities."
read_when:
  - "Starting at the Softwareco root."
  - "Looking for Softwareco identity, operating guidance, architecture anchors, or L2 template entrypoints."
type: "reference"
---

# softwareco

Softwareco's constitutional role is **AI Society's product-engineering company**. It builds these systems and operates them only where a named owner, support boundary, and runtime evidence prove that responsibility. Portfolio descriptions route intent; owner repositories prove current capability.

This repository is also Softwareco's **L1 company template/control-plane repo**, generated from `core/tpl-template-repo` (L0). Those roles are complementary: company policy and navigation live here, implementation belongs in owner repositories, and reusable L2 baselines are authored under `copier/`.

- Accountable company role: `Softwareco Org Owner` (appointment belongs in accepted governance/AK state)
- L1 organization docs profile: `rich`
- Baseline L2 standalone-repo templates: `agent`, `project`, `org`, `monorepo`
- Internal monorepo-member template: `package` (not a separate L2 layer)

## Start here

### Softwareco

- [[softwareco/docs/org/operating_model.md|Softwareco Operating Model]] — identity, lanes, ownership, flow, cadence, authority, and navigation hub.
- [[softwareco/docs/org/purpose.md|Purpose]]
- [[softwareco/docs/org/mission.md|Mission]]
- [[softwareco/docs/org/vision.md|Vision]]
- [[softwareco/docs/org/strategic_objectives.md|Strategic Objectives]]
- [[softwareco/docs/org/governance.md|Governance]]
- [[softwareco/docs/org/values_ethics.md|Values and Ethics]]
- [[softwareco/docs/project/2026-07-12--status--softwareco-company-claim-validation.md|2026-07-12 Company-Claim Validation]] — dated evidence snapshot; revalidate after relevant commits.
- [[softwareco/docs/project/2026-07-12--status--transition-document-inventory.md|2026-07-12 Transition-Document Inventory]] — owner-repo migration inventory, not current authority.

### AI Society architecture

- [[/home/tryinget/ai-society/README.md|AI Society Workspace Entrypoint]]
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/ai-society-stack-map.md|AI Society Stack Map]] — architectural/authority layer orientation.
- [[/home/tryinget/ai-society/holdingco/governance-kernel/docs/core/definitions/runtime-authority-matrix.md|Runtime Authority Matrix]] — current and target concern owners.
- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/ai-society-convergence-architecture.md|AI Society Convergence Architecture]] — system assembly.
- [[/home/tryinget/ai-society/softwareco/owned/agent-kernel/docs/project/layer-12-protocol.md|Layer-12 Protocol]] — purpose-to-publication workflow and traceability spine.
- [[/home/tryinget/ai-society/core/tpl-template-repo/docs/dev/architecture/layer-taxonomy-and-propagation-architecture.md|L0/L1/L2 Layer Taxonomy]] — render lineage; distinct from architectural layers and Layer 12.

## What this repo provides

Current lane note: `owned/`, `infra/`, `contrib/`, and `fork/` are materialized. `agents/` is a declared target lane but is not materialized as of 2026-07-12; the separate `softwareco-agents/` path currently exists and must not be silently treated as the target lane.

- **L2 standalone-repo templates**:
  - `copier/tpl-agent-repo/` — AI agent repositories
  - `copier/tpl-project-repo/` — delivery projects
  - `copier/tpl-org-repo/` — organization handbooks
  - `copier/tpl-monorepo/` — monorepo workspaces
- **Internal L2-monorepo member template**:
  - `copier/tpl-package/` — package/app members inside an L2 monorepo; not an L3 or separate L2 repo
- Opinionated local hooks (`.githooks/`) and CI lane scripts (`scripts/ci/`).
- Layer contract enforcement via `contracts/layer-contract.yml`.
- Baseline structure in this generated L1 repo: `docs/`, `examples/`, `external/`, `ontology/`, `policy/`, `src/`, `tests/`.
- Git hygiene in this L1 repo: `.github/`, `.githooks/`, `.gitignore`, `.gitattributes`.
- Generated L2 repositories are archetype/profile-specific and do not all share identical folder/git baselines; GitHub assets are profile-gated.
- **KES Infrastructure**: `tips/`, `governance/`, `metrics/` for knowledge evolution.
- **Repo-local diary contract**: `diary/README.md` in L1 and all generated L2 archetypes.

## Quickstart

Validate this L1 template repo:

```bash
bash ./scripts/check-template-ci.sh
```

Document freshness policy: living `product-posture.md` paths remain stable and carry `as_of`, `last_validated`, `last_validated_commit`, and `evidence_paths`. Separate transition, migration, current-vs-target, and status snapshots are date-prefixed. See [[softwareco/docs/dev/tpl-project-repo-file-contract.md|tpl-project-repo File Contract]].

Bootstrap a lane root before nesting child repos:

```bash
./scripts/bootstrap-lane-root.sh fork
git add .gitignore fork
git commit -m "chore: bootstrap fork lane baseline"
./scripts/bootstrap-lane-root.sh fork --init-lane-git
```

Generate an L2 **agent** repository:

```bash
./scripts/new-repo-from-copier.sh tpl-agent-repo /path/to/agent-<slug> \
  -d repo_slug=agent-<slug> \
  -d agent_owner_handle=@<owner> \
  --defaults --overwrite
```

Generate an L2 **project** repository:

```bash
./scripts/new-repo-from-copier.sh tpl-project-repo /path/to/<project> \
  -d repo_slug=<project> \
  -d project_owner_handle=@<owner> \
  --defaults --overwrite
```

Generate an L2 **org** handbook:

```bash
./scripts/new-repo-from-copier.sh tpl-org-repo /path/to/<org>-handbook \
  -d repo_slug=<org>-handbook \
  -d org_owner_handle=@<owner> \
  --defaults --overwrite
```

Generate an L2 **monorepo** workspace:

```bash
./scripts/new-repo-from-copier.sh tpl-monorepo /path/to/<monorepo> \
  -d repo_slug=<monorepo> \
  -d language=python \
  -d package_manager=uv \
  --defaults --overwrite
```

Generate an internal **monorepo member package** inside an L2 monorepo:

```bash
./scripts/new-repo-from-copier.sh tpl-package /path/to/packages/<name> \
  -d package_name=<name> \
  -d package_type=library \
  -d language=python \
  --defaults --overwrite
```

### Transition existing L2 repos (scaffold-first)

There is no automatic in-place migrator. Use this deterministic pattern:

1) Render baseline:
```bash
./scripts/new-repo-from-copier.sh tpl-project-repo /tmp/<repo>-template \
  -d repo_slug=<repo> \
  --defaults --overwrite
```

2) Diff against existing repo:
```bash
git diff --no-index -- /tmp/<repo>-template /absolute/path/to/<existing-repo>
```

3) Adopt control-plane first (`AGENTS.md`, `CODEOWNERS`, `scripts/`, `governance/`, `docs/`, `ontology/`), then reconcile product code.

4) Validate and commit the relevant changes to `main` for normal work. Use a PR only for releases or when the operator explicitly requests a review gate.

Install local hooks in a generated repo:

```bash
./scripts/install-hooks.sh
```

Deterministic ROCS launcher (use before ad-hoc scripting):

```bash
./scripts/rocs.sh --doctor
./scripts/rocs.sh --which
./scripts/rocs.sh version
```

## Multi-pass template suffix policy (`.jinja` vs `.j2`)

This L1 template repo has two template boundaries:

- **L0 -> L1 artifacts** in this repository use `.jinja` at authoring time (as rendered from L0).
- **L1 -> L2 artifacts** under `./copier/` use `_templates_suffix: .j2` in each L2 template `copier.yml`.

Pass-boundary rule:
- never place `.jinja` template files under `./copier/`
- never place `.j2` template files outside `./copier/`

`bash ./scripts/check-template-ci.sh` enforces this boundary so nested L2 templates cannot accidentally inherit the outer pass suffix, and fails if nested files contain Jinja markers without the `.j2` suffix.

Contribution workflow:
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Knowledge Evolution System (KES)

This L1 participates in KES for compound learning:

```
tips/
├── _templates/tip.yml     # TIP genome
├── domain/                # Domain TIPs (local)
└── meta/                  # Meta TIPs (→ L0)

governance/README.md       # Review process
metrics/README.md          # Effectiveness tracking
```

**TIP Flow**: L2 learns → TIP proposed → review → merge → propagate

- Domain TIPs improve this L1
- Meta TIPs escalate to L0
- Future L2 renders inherit accepted template improvements; existing L2 repositories require explicit propagation and validation

Diary contract (repo-local diary for KES):
- L1 logs in `./diary/`
- each generated L2 archetype logs in `./diary/`
- no workspace-global diary authority

See `tips/README.md` for TIP process.

## Archetype profile

- L2 standalone repos are generated through:
  - `tpl-agent-repo`
  - `tpl-project-repo`
  - `tpl-org-repo`
  - `tpl-monorepo`
- `tpl-package` generates internal package/app members inside an L2 monorepo; it does not create another render layer.
- Detailed project-template file map (canonical):
  - `docs/dev/tpl-project-repo-file-contract.md`
  - wikilink: `[[docs/dev/tpl-project-repo-file-contract.md]]`

## Organization docs profile

- This L1 repository currently ships **rich** organization docs in `docs/org/`.
- `.copier-answers.yml` currently leaves `l2_org_docs_default` unset. Until Softwareco accepts a company default, choose the profile explicitly for each generated L2 repo.
- Select at L2 generation time with:
  - `-d org_docs_profile=compact`
  - `-d org_docs_profile=rich`

## Governance layering

L2 governance is archetype-dependent:
- `tpl-project-repo`: `governance/work-items.*` + `docs/project/` + `docs/system4d/`.
- `tpl-org-repo`: governance-primary docs in `docs/org/` + `governance/`.
- `tpl-agent-repo`: lightweight local governance in persona/system docs.
- `tpl-monorepo`: repo-level delivery governance with package/app decomposition.
- `tpl-package`: package-local governance and quality controls inside a monorepo.

For `tpl-project-repo`, the canonical file-by-file contract is:
- `docs/dev/tpl-project-repo-file-contract.md`
- wikilink: `[[docs/dev/tpl-project-repo-file-contract.md]]`

## Community profile

- Community collaboration pack is currently **disabled**.
- When enabled, this repo includes:
  - `.github/ISSUE_TEMPLATE/`
  - `.github/pull_request_template.md`
  - `CODE_OF_CONDUCT.md`
  - `SUPPORT.md`
- L2 generation inherits `enable_community_pack` from this L1 unless you override with `-d enable_community_pack=true|false`.

## Release profile

- Release automation pack is currently **disabled**.
- When enabled, this repo includes:
  - `.github/workflows/release-please.yml`
  - `.github/workflows/release-check.yml`
  - `.github/workflows/publish.yml`
  - `.release-please-config.json`, `.release-please-manifest.json`
  - `CHANGELOG.md`, `SECURITY.md`
  - `scripts/release/check.sh`, `scripts/release/publish.sh`
- L2 generation inherits `enable_release_pack` from this L1 unless you override with `-d enable_release_pack=true|false`.

## Trust-gate profile

- Vouch trust gate baseline is currently **disabled**.
- Files are scaffolded at `.github/VOUCHED.td`, `.github/workflows/vouch-check-pr.yml`, `.github/workflows/vouch-manage.yml`.
- L2 generation inherits `enable_vouch_gate` from this L1 unless you override with `-d enable_vouch_gate=true|false`.

## Recursion policy (explicit)

Current layer: **L1**

Allowed edges:
- `L0 -> L1`
- `L1 -> L2`

Forbidden edges:
- `L1 -> L0`
- `L2 -> L1`
- any cycle

Answers-file policy:
- Keep `.copier-answers.yml` versioned in git for reproducibility.
- Do not invoke nested Copier runs from `_tasks`.
