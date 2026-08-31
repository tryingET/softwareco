---
summary: "Decision 144 evidence selecting true-submodule candidate C as the reviewable topology while preserving implementation gates."
read_when:
  - "Reviewing candidate C for Softwareco ontology ownership."
  - "Planning targeted ontology materialization, receipt relocation, or ownership-state migration."
type: "evidence"
status: "reviewed"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5244
---

# Decision 144 candidate-C evidence

## Current boundary

| Surface | Bound value |
|---|---|
| Softwareco current review base | `2f7653dc618bb6e7ffe26b4b724e50055c972ed0` |
| Established ownership finalization | `74cc0a59786d2450f172ee87a249f327a044ff07` / evidence `8033` |
| Ontology owner | `07d4b8b89f6ca436618adb42827885e9a45289c7` |
| Preserved owner stash | `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` |
| Candidate C scratch commit | `016cf156e15fdd88675f47bed05ea670bb44c444` |
| Candidate E scratch commit | `aeea561621185366290f831c74fdf52cde7f5fa8` |
| Canonical ontology WIP | 31 entries, held and unstaged |

All candidate mutations occurred in independent scratch repositories. Canonical parent/owner Git,
AK, stashes, and remotes were not mutated.

## Consumer result

Commit-bound inspection classifies the 46 owner paths as:

- eight ROCS semantic paths required by parent and layered consumers: `manifest.yaml` plus seven
  `src/**` files;
- one parent template marker, `.gitkeep`;
- eight owner control/docs/CI paths;
- 29 owner vendored-tool paths.

The last 37 paths are owner-active but not parent runtime inputs. This rejects the claim that a
complete 46-path parent projection is required. It does not make a selective projection preferable:
selection would create a second versioned API, overlapping indexes, custom excluded-drift logic, and
custom Git materialization.

## Candidate comparison

### C — true submodule: selected for ADR consideration

Observed in scratch:

- `.gitmodules` plus mode-`160000` `ontology` bound the exact owner OID;
- an uninitialized checkout with the proposed guard failed non-zero;
- the current conditional gate silently skipped missing ontology and exited zero, proving the guard
  is mandatory;
- generic `git submodule update --init` failed because unrelated raw gitlinks have no module mapping;
- exact `git submodule update --init --checkout ontology` succeeded;
- strict ROCS validation succeeded for root, infra, owned, contrib, and fork;
- owner full CI passed;
- relocated parent receipts stayed byte-identical during owner CI;
- unavailable source failed without leaving ontology Git metadata;
- bounded revert restored the exact parent tree.

C supplies native parent-to-owner OID binding, removes overlapping source indexes, and avoids E's
custom excluded-path API. It is the strongest fit for RFC invariants I1–I8.

### E — selective projection: not selected

E proved nine-path materialization and useful drift checks, but it retains overlapping parent/owner
indexes for those paths, needs ignore/classification/checker contracts for 37 excluded paths, and its
prototype left partial `.git` metadata after unavailable-source failure. Its JSON/source pin is
weaker than a native mode-`160000` parent binding. E remains a rollback alternative, not the chosen
architecture.

### Other candidates

- A duplicates 37 unneeded paths and retains overlapping indexes.
- B requires canonical owner path and AK registration migration without a resolver mapping layer.
- D relies on complete command coverage while fresh parent checkout still lacks truthful owner
  materialization.

## Corrected causality

The first C-vs-E report incorrectly attributed six downstream receipt changes to ontology-owner CI.
The timestamps show owner CI ran before separate consumer validations and status was captured only
after those validations.

A fresh isolated audit proved:

- owner-only strict CI exited zero;
- parent and owner remained clean;
- all six downstream receipts were byte-identical;
- contrib validation changed only the contrib receipt pair;
- fork validation changed only the fork pair;
- infra validation changed only the infra pair.

Therefore no ROCS-core cross-owner writer fix is required by Decision 144. Evidence `8040` and the
sealed causal artifact supersede that one claim; all other independently reproduced C/E results
remain usable.

## Required ADR invariants for C

1. **True source binding:** parent records `.gitmodules` and mode-`160000` `ontology` at a full,
   live-published owner OID. Metadata-less gitlink is forbidden.
2. **Targeted materialization:** automation initializes exactly `ontology`; generic recursive
   submodule initialization is forbidden until unrelated raw gitlinks are governed.
3. **Atomic failure:** missing/unavailable/mismatched source fails before activation and leaves no
   partial `.git`, changed index, or receipt mutation.
4. **Receipt relocation:** all six parent receipts move outside the gitlink and are regenerated with
   parent identity. Every consumer/path binding is migrated before old paths are removed.
5. **Ownership transition:** narrow the `ontology/**` template wildcard and execute a new post-AK-5197
   manifest/plan/state/receipt transition. Inline map-hash editing is forbidden.
6. **Gate truth:** missing [ontology/manifest.yaml](../../ontology/manifest.yaml) is a hard failure,
   never a skip.
7. **Owner safety:** ordinary owner CI runs from the materialized owner and cannot mutate relocated
   parent receipts.
8. **Reversibility:** pre/post bundles preserve owner refs/history/stashes; rollback is a bounded
   parent revert plus exact rematerialization, never ref rewriting.
9. **Held WIP:** the current 31 ontology entries are evidence only and remain unstaged until exact
   post-ADR tasks authorize the migration.

## Evidence limitation

The scratch candidate is not production implementation. Atomic materializer, receipt generator,
ownership transition engine, CI changes, and fresh-current-base proof remain post-ADR deliverables
with stop conditions. Architecture acceptance authorizes those exact tasks; it does not authorize
copying the present worktree bytes or adopting the scratch commit.
