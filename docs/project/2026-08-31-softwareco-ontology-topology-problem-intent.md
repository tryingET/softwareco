---
summary: "Problem and intent for choosing a physically safe owner topology for Softwareco's ambiguous dual-tracked ontology tree."
read_when:
  - "Reviewing why the Softwareco parent and ontology owner repository report the same physical files differently."
  - "Planning any change to the parent ontology snapshot, ontology git topology, or generated ontology receipts."
type: "problem"
status: "proposed"
date: "2026-08-31"
governance_task_id: 5228
---

# Problem and intent — Softwareco ontology repository topology

## Trigger

`/home/tryinget/ai-society/softwareco/ontology` is simultaneously:

1. a clean independent Git repository whose published `main` is
   `07d4b8b89f6ca436618adb42827885e9a45289c7`; and
2. an ordinary tracked subtree in the Softwareco parent repository.

The parent does not record `ontology` as a gitlink and has no `.gitmodules` contract. The two
indexes overlap without declaring which bytes are source-owned, which are a parent projection,
and which are generated only by the parent.

At the observed parent commit `712c336b0f7f777f72df2235a61d998352aa902d`:

- the parent tracks 22 paths under `ontology/`;
- the ontology owner tracks 46 paths;
- 16 paths are common;
- 30 owner paths are absent from the parent index;
- one common path, [gitlab/ci/rocs.yml](../../ontology/gitlab/ci/rocs.yml), differs;
- six parent-only `dist/**` receipts are intentionally ignored by the ontology owner.

That produces 31 parent worktree entries even though the ontology owner worktree is clean. A
naive parent cleanup would either delete owner bytes, absorb them without an ownership contract,
or overwrite the owner's published CI behavior.

## Why this is an ownership problem

The ontology repository owns its authored files and Git history. The Softwareco parent owns its
company-level integration, generated receipts, and any explicit projection it chooses to retain.
Neither repository may silently become the other's authority.

Prior bounded work preserved this membrane rather than resolving the topology:

- AK `4960` retained strict parent-generated ontology outputs;
- AK `4962` published owner launcher fixes while preserving blocked stash
  `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` and excluding GitLab/tool de-vendoring;
- AK `4973` synchronized selected parent baselines while expressly excluding GitLab/tools drift
  and keeping nested `dist/` ignore ownership separate from parent output ownership.

Those results are historical constraints, not authorization to stage the current 31 paths.

## Failure modes to prevent

- **Shadow authority:** treating parent-copied ontology bytes as independently authored truth.
- **Owner deletion:** using parent `git clean`, reset, checkout, or subtree replacement against
  clean files owned by the nested repository.
- **Unreachable pointer:** replacing the subtree with a gitlink without a materialization and
  publication contract.
- **Receipt loss:** moving to a gitlink while leaving no lawful home for the six parent-generated
  `ontology/dist/**` files.
- **Invisible receipt mutation:** ordinary owner CI defaults to the co-located repository, removes
  `dist`, and can replace parent-tracked receipts while owner `.gitignore` still reports clean.
- **Blocked-WIP activation:** popping, dropping, deleting, or accidentally applying stash
  `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`.
- **Ad-hoc synchronization:** copying only the paths that happen to appear dirty and leaving the
  two indexes to drift again.
- **Remote conflation:** treating the temporarily unavailable `gitlab-lan` remote as authority
  over the observed exact GitHub `origin/main` publication.

## Intent

Adopt one explicit, testable owner topology that:

1. names the ontology repository as source owner for authored ontology bytes;
2. names the Softwareco parent as owner of company integration and generated receipts;
3. classifies every path before mutation;
4. makes parent refresh plan-first, deterministic, commit-bound, and receipted;
5. preserves owner history, remote publication evidence, and blocked stash state;
6. makes ordinary owner commands physically unable to mutate parent-owned outputs invisibly;
7. leaves both repositories independently truthful and clean after an authorized refresh;
8. fails closed on source drift, path-classification drift, remote ambiguity, generated-output
   drift, symlinks, or validation failure;
9. does not require semantic authority to decide Git repository topology.

## Decision gate, not proposed outcome

The current evidence does not establish a least-disruptive outcome. Co-locating a complete
projection with parent receipts is unsafe as currently implemented: owner
`ontology/scripts/ci/full.sh` removes `dist` before building while owner `.gitignore` ignores that
path, so owner-native validation can mutate parent-tracked outputs without dirtying the owner.

Governed review must compare at least:

- relocating parent receipts before complete projection;
- physically separating the owner checkout from a complete or selective parent projection;
- adopting a gitlink/submodule plus receipt relocation and materialization contract;
- enforceable isolated owner-operation guards;
- a measured selective projection based on a consumer census.

A deterministic subtree projection remains a candidate only when paired with a physical receipt
membrane. It is not recommended as the outcome until consumer and ordinary-operation evidence
selects it over the other safe candidates.

## Non-goals

This packet does not:

- change ontology concepts, relations, manifests, or controlled semantics;
- stage or edit any `ontology/**` path;
- pop, drop, rewrite, or adopt the preserved de-vendoring stash;
- select a new ROCS provider or change GitLab CI behavior;
- create or advance the architecture decision by document presence alone;
- change L0/L1 template ownership contracts or Healthco;
- claim that GitHub or GitLab availability determines semantic authority.

## Completion boundary

Decision authoring is complete when the problem, evidence, alternatives, recommended contract,
validation, rollout, and rollback are committed and registered for governed review. Repository
cleanup requires a later accepted decision and outcome-specific implementation tasks. AK `5197`
finalization remains blocked until the canonical Softwareco checkout is clean; this proposal does
not itself satisfy that condition.
