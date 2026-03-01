# ontology (softwareco)

This repository is the **company overlay** layer for `softwareco`.
It extends the core ontology with domain concepts, invariants, constraints, and risks.

## SOP references
For process docs and SOPs that need ontology concepts, use the reference block defined in:
`holdingco/org-handbook/docs/org/processes/ontology-references.md`.

## Repo hygiene
If a file named `NUL` appears in the repo root, delete it and do not commit it (typically a stray Windows artifact).

- `ontology/src/system4d.yaml` — domain boundaries/constraints/risks
- `ontology/src/reference/` — domain concepts
- `ontology/src/bridge/` — naming decisions/mappings (optional at company level)
