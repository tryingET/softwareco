---
summary: "How to refresh and interpret engineering-core adoption coverage across softwareco/owned."
read_when:
  - "You need to refresh the engineering-core adoption dashboard."
  - "You are planning the next engineering-core adoption wave across owned repos."
type: "reference"
---

# Engineering-core adoption scanner

`core/engineering-core` owns the reusable adoption scanner semantics and CLI. The owned lane root owns this lane's generated adoption snapshot and operator dashboard.

## Command

From `softwareco/owned`:

```bash
./scripts/engineering-core-adoption-scan.sh --include-packages --write
```

The wrapper delegates to:

```bash
uv tool -n run --from ../../core/engineering-core \
  engineering-core scan-adoption \
  --scope . \
  --repo-root ../../core/engineering-core \
  --prefer-repo
```

Outputs owned by this lane root:

- `governance/engineering-core-adoption-scan.json` — machine-readable scan result.
- `docs/project/engineering-core-adoption-dashboard.md` — generated operator dashboard.

Read-only preview modes:

```bash
./scripts/engineering-core-adoption-scan.sh
./scripts/engineering-core-adoption-scan.sh --format json
./scripts/engineering-core-adoption-scan.sh --include-packages
```

## What it checks

For each discovered child repo, and optionally nested package/app/member surfaces, the scanner checks structural adoption:

- `docs/engineering.local.md`
- `policy/engineering-lane.json`
- legacy `docs/tech-stack.local.md`
- legacy `policy/stack-lane.json`
- declared lane(s) or explicit `lane_status`
- selected disciplines
- `catalog_command`, `list_disciplines_command`, and `list_templates_command`
- declared lanes/disciplines against the engineering-core catalog
- `Justfile` / `justfile` presence as a repo hygiene signal

It also performs a heuristic semantic audit for expected discipline coverage. Semantic flags are advisory review signals, not runtime authority.

## Status meanings

Structural statuses:

- `adopted` — engineering docs and policy exist, catalog/list commands are present, lanes or lane status are declared, disciplines are declared, catalog ids are known, and legacy tech-stack files are absent.
- `partial` — engineering docs and policy exist but one or more recognition fields, catalog ids, lanes, or disciplines are missing.
- `doc-only` — only `docs/engineering.local.md` exists.
- `policy-only` — only `policy/engineering-lane.json` exists.
- `legacy-only` — legacy tech-stack surfaces exist without current engineering-core surfaces.
- `legacy-mixed` — current engineering-core and legacy tech-stack surfaces coexist.
- `invalid-policy` — policy JSON could not be parsed.
- `missing` — no current or legacy adoption surface exists for the discovered repo/package root.

Semantic statuses:

- `ok` — no heuristic semantic gaps found.
- `likely-incomplete` — expected discipline coverage appears missing for the repo/package shape.
- `needs-review` — a semantic concern exists that may be intentional but should be reviewed.

## Interpretation

The scanner output is a planning surface, not a mutation order. Before editing any repo, read that repo's `AGENTS.md`, inspect existing engineering/legacy files, and preserve rich repo-local guidance.

The richer core scanner may report more records than the earlier owned-only scanner because package/member discovery includes both policy-driven and doc-driven adoption surfaces. Set `ENGINEERING_CORE_ROOT=/path/to/engineering-core` when running the wrapper outside the standard workspace layout.
