---
summary: "Commit-bound census and authority evidence for Softwareco's parent/ontology dual-tracked repository topology."
read_when:
  - "Reviewing the Softwareco ontology topology RFC."
  - "Reproducing the parent-versus-owner path census or remote/stash constraints."
type: "evidence"
status: "proposed"
date: "2026-08-31"
governance_task_id: 5228
---

# Evidence — Softwareco ontology repository topology

## Observation boundary

This evidence was captured read-only on 2026-08-31 before decision-packet authoring.

| Surface | Observed value |
|---|---|
| Softwareco parent | `/home/tryinget/ai-society/softwareco` |
| Parent commit | `712c336b0f7f777f72df2235a61d998352aa902d` |
| Parent `ontology` tree | `cb602fe162b19beb562bcdc687a36e89a83d3624` |
| Ontology owner repository | `/home/tryinget/ai-society/softwareco/ontology` |
| Owner commit | `07d4b8b89f6ca436618adb42827885e9a45289c7` |
| Owner tree | `b16319d608885089c9d04369b820347ce23418d0` |
| Live GitHub `origin/main` | `07d4b8b89f6ca436618adb42827885e9a45289c7` |
| Preserved blocked stash | `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` |

The owner worktree and index were clean. `gitlab-lan` was configured but a bounded live
`ls-remote` failed to connect to `192.168.161.10:8929`; this is a time-bounded availability fact,
not an authority decision. GitHub `origin/main` returned the exact owner commit above.

## Reproducible census

The census compares the parent commit's `ontology/` tree to the owner commit's tracked paths:

```bash
export LC_ALL=C
parent=712c336b0f7f777f72df2235a61d998352aa902d
owner=07d4b8b89f6ca436618adb42827885e9a45289c7
git ls-tree -r --name-only "$parent" -- ontology/ \
  | sed 's#^ontology/##' | sort > outer.paths
git -C ontology ls-tree -r --name-only "$owner" | sort > inner.paths
comm -12 outer.paths inner.paths > common.paths
comm -13 outer.paths inner.paths > inner-only.paths
comm -23 outer.paths inner.paths > outer-only.paths
```

| Set | Count | Sorted-list SHA-256 |
|---|---:|---|
| Parent tracked | 22 | `24278709dbd32908b51e444e89f2940f77be5e3752c30d88b0c2085e6a01d9e4` |
| Owner tracked | 46 | `ca59475967d34edb3e4af1b9dbf3d76f0beacd9bdce44fc0cc9c0690e0495cbc` |
| Common | 16 | `01ff162226ebafe8dfd21b9c934b9576204c72ed68c12cf8de94c724e33de2f0` |
| Owner-only | 30 | `147ce9d612895a0eab795d483649c307619c4b512d44f58285e1843c7e3ca932` |
| Parent-only | 6 | `0c4c4b7953655f17311dc18b836d330c0712947d8f0d45ac4c56bd2172a4325f` |

Blob comparison across the 16 common paths found exactly one mismatch:

```text
gitlab/ci/rocs.yml
parent blob: aecad63ff695870a2fe32aa7682b187c2b885770
owner blob:  2b189c872b5eed834e76c98d3f217ab7958886cb
```

## Owner-only paths

The 30 owner-only paths are:

```text
.gitignore
tools/rocs-cli/README.md
tools/rocs-cli/VENDORED_HASHES.json
tools/rocs-cli/pyproject.toml
tools/rocs-cli/src/rocs_cli/__init__.py
tools/rocs-cli/src/rocs_cli/__main__.py
tools/rocs-cli/src/rocs_cli/authority.py
tools/rocs-cli/src/rocs_cli/cache.py
tools/rocs-cli/src/rocs_cli/cli.py
tools/rocs-cli/src/rocs_cli/cli_signature.py
tools/rocs-cli/src/rocs_cli/env.py
tools/rocs-cli/src/rocs_cli/errors.py
tools/rocs-cli/src/rocs_cli/fleet_preflight.py
tools/rocs-cli/src/rocs_cli/frontmatter.py
tools/rocs-cli/src/rocs_cli/graph.py
tools/rocs-cli/src/rocs_cli/id_index.py
tools/rocs-cli/src/rocs_cli/index_cache.py
tools/rocs-cli/src/rocs_cli/inverses.py
tools/rocs-cli/src/rocs_cli/layers.py
tools/rocs-cli/src/rocs_cli/lint.py
tools/rocs-cli/src/rocs_cli/managed_surface.py
tools/rocs-cli/src/rocs_cli/model.py
tools/rocs-cli/src/rocs_cli/normalize.py
tools/rocs-cli/src/rocs_cli/pack.py
tools/rocs-cli/src/rocs_cli/repo_view.py
tools/rocs-cli/src/rocs_cli/rules.py
tools/rocs-cli/src/rocs_cli/rulesets.py
tools/rocs-cli/src/rocs_cli/validate.py
tools/rocs-cli/src/rocs_cli/vendored.py
tools/rocs-cli/src/rocs_cli/workspace.py
```

These files are not loose unknown bytes: all are tracked by the clean owner commit
`07d4b8b89f6ca436618adb42827885e9a45289c7`.

## Parent-only paths

The six parent-only paths are generated integration outputs:

```text
dist/.authority-receipt.lock
dist/authority-receipt.json
dist/authority-receipt.validate.json
dist/id_index.json
dist/resolve.json
dist/summary.json
```

The owner commit's `.gitignore` contains `/dist/`. Existing AK evidence deliberately separates
owner `dist/` ignore policy from parent generated-output ownership.

## Physical receipt collision

That logical separation is not physically enforced in the current co-located checkout. The owner
[CI script](../../ontology/scripts/ci/full.sh):

- defaults `ROCS_REPO` to `.`;
- calls `clean_dist` before validation/build;
- removes both `$ROCS_REPO/ontology/dist` and `$ROCS_REPO/dist`.

When invoked from the owner root at `softwareco/ontology`, `$ROCS_REPO/dist` is the same physical
directory as the six parent-tracked `ontology/dist/**` paths. Because owner `.gitignore` ignores
`/dist/`, deletion or regeneration can leave the owner worktree clean while changing parent-owned
bytes. The current parent output set is path-bound in two observed ways: `resolve.json` and
`summary.json` bind the Softwareco parent root, while both authority receipts bind the verified AK
`5197` integration scratch checkout. Owner-native regeneration would bind the ontology owner root;
these identities are not interchangeable.

This collision is observed behavior and a decision blocker. Isolated validation avoids ambient
mutation for one run but does not make ordinary canonical owner operation safe.

## Worktree manifestation

At the observation boundary, the Softwareco parent reported 33 total porcelain entries:

- 31 under `ontology/`;
- two unrelated held entries under `fork/`.

The 31 ontology entries were the one differing common file plus the 30 owner-only files. Baseline
fingerprints before packet authoring were:

| Projection | SHA-256 |
|---|---|
| Parent porcelain text | `d95e4754533acefa55d037f6362c5bf75567973c2a1e9deaa925a50e5ea66cff` |
| Parent porcelain NUL stream | `853f1e53a0aa849a6d5656271a452c88476ee8a985e11fc3319f34989146b79f` |
| Parent binary diff | `4f9d613e24d8fbaebf0bba1a05df1c36dd1ae66638a3b6dca0e5f538de01435e` |

The exact fingerprint commands were:

```bash
git status --porcelain=v1 --untracked-files=all | sha256sum
git status --porcelain=v1 -z --untracked-files=all | sha256sum
git diff --binary | sha256sum
```

These fingerprints describe observed worktree state. They are preservation checks, not canonical
runtime authority.

## AK authority and exclusion evidence

### AK 4960 / evidence 7577

AK `4960` allowed parent `ontology/dist/**`, [ontology/manifest.yaml](../../ontology/manifest.yaml), template consumers, and
strict CI. Evidence `7577` records that strict root ontology build/validate receipts were retained.
It does not authorize owner GitLab/tool synchronization.

### AK 4962 / evidence 7579

AK `4962` was bound to the ontology owner and allowed `.gitignore`, README/index, and launcher/CI
files. Evidence `7579` records:

- owner commits `5ba8c8d` and `07d4b8b` published;
- nested `dist` ignored;
- stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` preserved;
- the stash contains unproven GitLab CI de-vendoring plus 29 vendored-file deletions;
- current GitLab CI intentionally retains its known vendored provider.

The stash changes 30 paths, with four insertions and 4,907 deletions. It is not part of the clean
owner commit and must not be popped, dropped, or inferred into a parent refresh.

### AK 4973 / evidence 7603

AK `4973` synchronized selected owner fixes into parent lane baselines. Evidence `7603` explicitly
records:

- nested ontology retains `dist` ignore ownership;
- parent retains generated output ownership;
- GitLab/tools WIP was excluded;
- unrelated fork governance, issue tracker, projects, and agents drift was excluded.

This is a preserved boundary, not a permanent topology choice.

## Facts not proved

This evidence does not prove:

- that every consumer can tolerate a gitlink or submodule;
- that every consumer requires a complete subtree projection;
- that the unavailable GitLab remote is permanently unavailable;
- that the preserved de-vendoring proposal should be accepted or rejected;
- that document recommendation is accepted architecture authority.

Those questions remain governed decision inputs. Any implementation must re-read live Git, AK,
remote, path-census, and validation state rather than replaying this packet mechanically.
