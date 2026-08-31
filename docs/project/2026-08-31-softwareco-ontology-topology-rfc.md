---
summary: "RFC requesting a governed choice of one physically safe Git ownership topology for Softwareco ontology files and receipts."
read_when:
  - "Reviewing or deciding the durable Git ownership topology for Softwareco ontology files."
  - "Planning a parent ontology projection refresh, checkout relocation, or receipt relocation."
type: "rfc"
status: "proposed"
date: "2026-08-31"
governance_task_id: 5228
---

# RFC — choose a physically safe Softwareco ontology topology

## Decision requested

Choose one durable Git ownership topology for `/home/tryinget/ai-society/softwareco/ontology` and
its six parent-generated receipts.

The current evidence does **not** support selecting a final outcome yet. Governed review must first
compare consumer/materialization impact and resolve a physical ownership collision:

- the ontology owner repository and parent projection occupy the same directory;
- owner CI defaults `ROCS_REPO=.`;
- owner CI removes both `$ROCS_REPO/ontology/dist` and `$ROCS_REPO/dist` before rebuilding;
- from the co-located owner root, that includes the six parent-tracked `ontology/dist/**` files;
- the owner ignores `/dist/`, so it can delete or regenerate those parent files while still
  reporting a clean owner worktree.

A decision that merely labels those receipts “parent-owned” does not enforce the membrane. The
accepted outcome must make ordinary owner operation physically safe, not only validate from an
isolated candidate worktree.

Document presence is not operative authority. The architecture decision must complete governed
review, record an ADR, and link exact post-ADR tasks before any `ontology/**` mutation.

## Decision drivers

1. **One source owner:** authored ontology bytes originate only from the ontology repository.
2. **Physical safety:** ordinary owner commands cannot invisibly mutate parent-owned outputs.
3. **Current consumer compatibility:** parent CI/templates currently expect files and strict
   receipts under `ontology/`.
4. **Fresh materialization:** a fresh checkout has a deterministic route to every required byte.
5. **Clean operation:** parent and owner states cannot falsely report clean while damaging the
   other owner’s bytes.
6. **Fail-closed refresh:** path/source/remote/generated-output drift stops before writes.
7. **No stash activation:** stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3` remains preserved,
   un-applied evidence.
8. **Reversible adoption:** owner history and publication remain intact through migration/rollback.

## Non-negotiable ownership invariants

- **I1 — source authority:** the ontology repository remains source/semantic owner for authored
  ontology files unless a later explicit owner decision moves that authority.
- **I2 — complete classification:** every parent `ontology/**` path is source projection,
  parent-generated, repository metadata, or unclassified/fail.
- **I3 — physical membrane:** owner-native commands cannot delete/replace parent-owned files while
  owner status remains clean.
- **I4 — source binding:** copied/projected bytes bind a full source commit/tree and live authorized
  publication proof.
- **I5 — byte/mode identity:** every projected source path equals source Git byte and mode.
- **I6 — no ambient mutation:** planning/validation never pops/drops a stash or cleans another
  owner’s worktree.
- **I7 — no shadow authority:** parent copy, gitlink, manifest, docs, and receipts do not replace AK,
  ROCS, or source Git authority.
- **I8 — reversible history:** rollback uses bounded forward/revert history, never owner-history or
  remote-ref rewriting.

## Required pre-decision measurements

Review must add evidence for:

1. every root/template/CI consumer of the 46 owner paths and six parent receipts;
2. which consumers require the complete owner tree versus a selective projection;
3. the migration cost of relocating parent receipts and updating their repo identity/path bindings;
4. the AK repo-registration and operator impact of relocating the canonical owner checkout;
5. fresh-checkout behavior for raw gitlink, `.gitmodules`, complete projection, and selective
   projection;
6. ordinary owner edit/build/validate behavior after each candidate adoption;
7. how unavailable authorized remotes fail closed without making one remote semantic authority.

Until these measurements exist, “least disruptive” is a hypothesis, not a finding.

## Candidate outcomes

### A. Relocate parent receipts, then maintain a complete source-owned subtree projection

Move the six parent-generated outputs to a parent-owned path outside the owner checkout. Keep an
exact parent projection of all source-owner tracked paths under `ontology/`, bound to source commit,
manifest, plan, state, and receipt.

**Advantages**

- fresh parent checkout contains all source bytes;
- no submodule materialization dependency;
- owner changes become visible parent drift until explicitly adopted;
- complete projection avoids selective-path ambiguity.

**Costs/open questions**

- every receipt consumer/path/repo binding must migrate;
- duplicate Git storage remains explicit maintenance debt;
- consumer evidence must show complete projection is needed;
- parent root has no remote, so verified bundles remain required.

### B. Physically separate the owner checkout, then maintain a parent projection

Move the canonical owner worktree/repository out of the parent-projection directory. Leave a
parent-owned projection at `softwareco/ontology`, complete or selective according to measured
consumers.

**Advantages**

- strongest filesystem-level separation;
- ordinary owner CI cannot touch parent files;
- parent receipts may remain under the projection if their consumer contract remains valid.

**Costs/open questions**

- changes the owner repository’s canonical path and AK repo binding;
- requires operator/tool/docs/remote/workspace reference migration;
- needs a no-gap transition preserving Git objects, branches, stashes, and remote state;
- a copied projection still requires deterministic refresh and no-shadow-authority checks.

### C. Adopt a gitlink/submodule and relocate parent receipts

Replace the parent subtree with a mode-`160000` owner pointer. A true submodule adds
`.gitmodules`; a metadata-less gitlink would follow existing local Softwareco pointer convention.

**Advantages**

- parent commit directly binds one owner commit;
- eliminates duplicate source files from parent history.

**Costs/open questions**

- parent cannot track receipts beneath the gitlink, so relocation is mandatory;
- metadata-less gitlink lacks fresh-checkout remote/materialization information;
- true submodule introduces network/submodule lifecycle into templates and CI;
- publication-remote policy must fail closed while `gitlab-lan` is unavailable;
- all current path consumers require migration proof.

### D. Enforce isolated owner operation while retaining co-location

Keep the co-located owner repository and parent outputs, but change owner tooling so every operation
that can write `dist` refuses the canonical co-located directory and uses an isolated worktree/output
root. Add guards/checkers proving the physical parent paths are untouched.

**Advantages**

- avoids immediate path and receipt relocation;
- can preserve current consumer paths.

**Costs/open questions**

- safety depends on complete command coverage, not just `scripts/ci/full.sh`;
- direct ROCS/build commands may bypass the guard;
- ordinary owner operation becomes less ergonomic;
- review must prove no clean-status invisible writer remains.

### E. Maintain a deterministic selective projection

Project only source-owner paths proven necessary to parent consumers, rather than all 46. Combine
this with receipt relocation, physical owner separation, or enforceable write isolation.

**Advantages**

- smaller duplicate surface and parent history;
- can preserve only stable integration interfaces.

**Costs/open questions**

- requires a complete consumer census and explicit exclusions;
- excluded owner changes may not be visible in parent status;
- selection can become a second API/ownership contract requiring versioning and compatibility
  review.

### F. Parent-only ontology tree

Remove the independent owner and author solely in the parent.

**Rejected:** this absorbs owner history/authority into company integration, risks remote/stash/ref
loss, and violates current source-owner evidence.

### G. Keep the current partial, hand-copied dual tree

**Rejected:** this preserves recurrent dirty state, invisible receipt mutation, and unclassified
path drift.

## Conditional projection contract

If the accepted outcome includes a complete or selective parent projection, implementation must
introduce parent-owned machine-readable artifacts (exact paths/schemas selected during review):

- ownership manifest classifying projected, parent-generated, metadata, and forbidden paths;
- plan binding source repo/commit/tree/remote proof, path-set hashes, parent commit, additions,
  replacements, removals, modes, and unchanged paths;
- applied state binding accepted decision/ADR and source commit;
- receipt binding plan/manifest hashes, before/after commits, validation, and executor.

### Observe

- require owner and parent index/worktree posture declared by the accepted outcome;
- prove the selected source commit on an authorized live remote ref;
- enumerate source paths from the selected Git commit, not the live index/filesystem;
- enumerate parent projection/generated classes;
- reject symlinks, case collisions, metadata, unclassified paths, and destination escapes;
- record but never mutate owner stash/ref state.

### Plan and apply

- produce a deterministic reviewed plan before writes;
- copy exact source Git bytes/modes only for classified projection paths;
- remove stale projection paths only when previous state and current plan both authorize removal;
- never copy `.git`, stashes, ignored/untracked owner files, or local-only refs;
- never overwrite/delete a generated class unless the accepted outcome explicitly relocates it;
- stage only the exact task/plan set.

The observed 31 dirty entries are evidence, not an automatic apply plan. In particular, no task may
copy the 30 owner-only files and replace [ontology/gitlab/ci/rocs.yml](../../ontology/gitlab/ci/rocs.yml)
until the physical receipt membrane and projection completeness are decided.

## Validation required for any accepted outcome

- reproduce commit-bound 22/46/16/30/1/6 census or explain authorized drift;
- prove source-owner commit/tree and live remote containment;
- exercise ordinary owner build/validate from the post-adoption canonical owner path;
- prove parent-tracked receipts/outputs are unchanged unless the plan updates/relocates them;
- prove parent status detects source drift or an explicit checker detects excluded drift;
- run owner strict CI and parent census/smoke/template/deep CI in governed isolated overlays;
- verify owner stash OID and unrelated parent WIP unchanged;
- verify exact staged scope and post-commit full-ref bundle;
- prove fresh-checkout materialization without relying on ambient nested `.git` state.

## Review and authority boundary

Review may close only after it selects one physically enforceable outcome and records why the other
safe candidates lose under measured consumer/operational evidence. The decision then needs:

- review memo(s) and synthesis satisfying configured closure;
- accepted ADR;
- implementation plan and validation/rollout/rollback artifacts;
- task re-evaluation and exact outcome-specific owner/parent tasks.

Until then, all 31 ontology worktree entries remain held. AK `5197` must not be finalized by ad-hoc
normalization, temporary cleaning, or reinterpretation of existing AK `4960`/`4962`/`4973` scope.
