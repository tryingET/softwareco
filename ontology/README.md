# ontology (softwareco)

This repository is the **company overlay** layer for `softwareco`.
It extends the core ontology with domain concepts, invariants, constraints, and risks.

## SOP references
For process docs and SOPs that need ontology concepts, use the reference block defined in:
`holdingco/org-handbook/docs/org/processes/ontology-references.md`.

## Repo hygiene
If a file named `NUL` appears in the repo root, delete it and do not commit it (typically a stray Windows artifact).

## Validation workflow
This repo is a layered ontology overlay over `core/ontology-kernel`, so the canonical local path is to resolve refs by default:

- `./scripts/ci/full.sh`
- `./scripts/rocs.sh --doctor`
- `./scripts/rocs.sh --which`
- `ROCS_WORKSPACE_ROOT=~/ai-society ROCS_WORKSPACE_REF_MODE=loose ./scripts/rocs.sh validate --repo . --resolve-refs`
- `ROCS_WORKSPACE_ROOT=~/ai-society ROCS_WORKSPACE_REF_MODE=loose ./scripts/rocs.sh build --repo . --resolve-refs --clean`

`scripts/rocs.sh` resolves ROCS from the workspace core (`~/ai-society/core/rocs-cli`) and falls back to `rocs` on `PATH`.
Running plain `rocs validate --repo .` without `--resolve-refs` will fail by design because the repo depends on the core ontology layer.

- `src/system4d.yaml` — domain boundaries/constraints/risks
- `src/reference/` — domain concepts
- `src/bridge/` — naming decisions/mappings (optional at company level)
