# Ontology Index (company overlay)

Start here when browsing manually.

- `manifest.yaml` — company overlay metadata + dependency on core
- `src/system4d.yaml` — company-level System4D boundaries/constraints
- `src/reference/concepts/` — company concepts
- `src/bridge/mapping.yaml` — concept-to-artifact mappings
- `dist/` — generated artifacts

Tip: Use `./scripts/rocs.sh pack <concept_id> --resolve-refs --workspace-ref-mode loose` instead of opening many files.
