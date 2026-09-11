---
summary: "Successor proposal to Decision 144: author Softwareco ontology in the parent repository without a permanent nested Git or publication boundary."
read_when:
  - "Reviewing or implementing Softwareco ontology consolidation."
type: "rfc"
status: "proposed"
date: "2026-09-11"
decision_id: 157
governance_task_id: 5650
---

# RFC — parent-owned Softwareco ontology

## Decision requested and operator intent

Supersede Decision 144's requirement that the company ontology remain an independent Git source.
Make `softwareco/ontology/` an ordinary parent-tracked component. Softwareco becomes its sole
ongoing Git authoring owner; ROCS retains semantic validation authority and AK retains runtime,
task, decision, registration and evidence authority. This transfers source ownership, not the
meaning of existing ontology definitions.

The operator explicitly rejected the separate-repository requirement and clarified that keeping
`softwareco-ontology` private was an uninformed decision, not a confidentiality requirement.
Proceed with local consolidation design and owner-bounded implementation. The earlier explicit
**no-push** selection remains: no remote visibility change, publication, secret provisioning,
force push, remote deletion or archival is authorized by this packet. Before any later publication,
review the exact imported tree for secrets and unintended disclosure; do not import private Git
history into the public parent as a shortcut.

This proposal does not itself supersede live AK authority. The existing topology remains effective
until accepted successor authority and exact execution tasks admit the cutover.

## First-principles diagnosis

The actual requirements are one authored source, deliberate access control, reproducible source
binding, safe generated-output ownership, preserved history, and manageable operation.
A separate Git repository is one possible implementation, not an axiom of semantic ownership.

Decision 144 repaired real overlapping indexes under a fixed independent-owner constraint.
Its parent-only candidate was rejected for contradicting that constraint. The operator now permits
changing it. This is not a claim that the earlier constrained implementation was defective.
Evidence 8040 already corrected the false attribution of downstream receipt changes to owner CI;
do not revive that claim. Old documents saying the parent has no remote are historical, not current.

## Observed inputs and confidence boundary

Read-only inspection on 2026-09-11 established:

- Parent HEAD: `6eb1542e7f742dc3dfe29503503e140c4ce56362`.
- Parent `ontology` gitlink and clean nested HEAD:
  `07d4b8b89f6ca436618adb42827885e9a45289c7`.
- Nested metadata is in parent `.git/modules/ontology`; refs include five local branches,
  tag `v0.1.0`, and stash `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`.
- GitHub Softwareco is PUBLIC and its ontology repository PRIVATE. Both collaborator listings
  showed the same sole administrator and no deploy keys. This is bounded metadata, not proof of
  every installed integration, historic exposure, or absence of secrets.
- Parent contains unrelated dirty files, including modified/deleted `governance/ontology-dist/**`.
  These are operator/other-session state, not migration inputs or permission to regenerate them.
- A fixed-depth consumer census found 30 physical exact-old manifests, of which 27 are tracked by
  their actual owner; additional prefixed, legacy and path-based variants exist. This is a lower
  bound, not an exhaustive workspace census. See the implementation plan.
- Source inspection: `core/rocs-cli/src/rocs_cli/workspace.py` requires a direct `.git` marker for
  workspace locators. Removing it makes `<repo:softwareco/ontology@main>` fail closed, even in loose
  mode. `<repo:softwareco@main>` already supports the standard `ontology/manifest.yaml` layout.
- ROCS snapshots include ref locator and resolved revision. Changing the repository changes
  provenance despite identical definitions. Unrelated parent revisions can consequently change
  downstream snapshot identity. Strict receipts alone do not prove clean trees or byte equivalence.
- Source inspection: `core/tpl-template-repo/scripts/lib/l1_template_transitions.py`,
  `validate_git_delta`, admits tree-to-gitlink collapse but rejects the reverse ancestor overlap.
  Reverse transition needs owner implementation and end-to-end proof, not a direct state/hash edit.

These are observations and source-based inferences, not executed consolidation proof.

## Proposed architecture

1. `ontology/manifest.yaml` and `ontology/src/**` are ordinary Softwareco source. Retain the exact
   semantic corpus from the bound old OID; no concept, relation, invariant or layer-content rewrite.
2. Preserve root ontology `index.md` as documentation. Rewrite `ontology/README.md` only to describe
   parent-owned invocation and source identity. Enumerate these retained paths exactly in the
   reviewed transition manifest before apply.
3. Preserve all old tracked files, branches, tags, stash and Git configuration in verified external
   backups and an inert archived repository. Do not import standalone-owner `AGENTS.md`, GitLab CI,
   old scripts or vendored ROCS as active nested machinery. Their exclusion must be classified and
   consumer-checked. The archive is recovery data, not a second authoring or resolution source.
4. Parent source ownership classifies `ontology/**` as company/agent-owned; it must not accidentally
   become upstream-template-owned. Change the established ownership map/state using a new receipted
   transition, preserving historical Decision-144 provenance rather than editing its hashes.
5. Keep parent receipts at `governance/ontology-dist/`, bound to the canonical Softwareco parent.
   Do not move outputs back beside semantic source just because the submodule disappears.
6. Migrate live consumers and persisted Copier inputs to an explicitly selected parent locator.
   Preserve strict resolution. No old-locator alias, nested `.git` compatibility shim, loose-mode
   bypass, symlink redirection, dual authoring, or permanent synchronization mirror.
7. Generation must produce the selected company locator, including reruns. Use the existing
   `company_ontology_ref` input where sufficient; if a generator-default change is required, use
   the L0 source owner and an explicit company policy, not a global change for unrelated companies.
8. Fresh full-history parent checkouts contain the ontology without a second ontology fetch or
   credential. Remove the active ontology-materialization dependency; retain fail-closed missing,
   symlinked or malformed source checks. Core ontology dependencies remain unchanged.
9. AK repository/task/source registration at the former nested path must be explicitly reconciled
   through the AK owner surface. Do not rewrite the workspace database or historical evidence and
   do not silently allow a stale registration to identify the enclosing parent as the former repo.

## Alternatives and many-perspective adjudication

- **Retain the submodule:** preserves independent release/adoption and access selection. It loses
  under the clarified single-company ownership objective, unless implementation discovers an
  actual indispensable independent consumer/access promise. A tag or old locator alone is not
  such a promise.
- **Tracked directory:** selected. Atomic parent changes, simpler clone/CI and fewer operator state
  transitions dominate now that privacy is not a requirement. Accept changed provenance and the
  loss of an independent Git-revision axis; do not pretend this is a path-only rename.
- **Publicize the ontology repo:** could remove one credential problem, but preserves the split
  and is an unauthorized external effect in this pass. Not the selected outcome.
- **Live export/mirror or old-locator shim:** rejected absent a demonstrated external contract.
  They risk moving complexity into synchronizers and recreating dual authority.
- **Single private parent:** unnecessary privacy-policy change and broader external impact; not
  selected or authorized.

Second-order cost: manifests, persisted answers, templates, receipts, snapshot-bound requests and
AK repo identity must converge. Third-order cost: parent revision churn may invalidate downstream
snapshot-bound caches/evidence even when ontology bytes are unchanged. Accept correct invalidation
initially; do not weaken binding or invent a distribution/cache subsystem before measuring a need.

## Acceptance, boundaries and stop conditions

The companion plan defines source-first prerequisites, owner-decomposed consumer migration,
receipted cutover, fresh-checkout tests, restart recovery and rollback. Design acceptance is not
permission to skip those gates. Stop on a required independent access/release promise, incomplete
consumer census, unsupported reverse transition, ownership/AK identity ambiguity, source/ref/stash
or parent-base drift, unclassified import, secret finding, conflicting WIP or failed proof.

No canonical ontology conversion, consumer rewrite, receipt regeneration, nested metadata move,
remote publication, Healthco propagation or global template-policy change is performed by task 5650.

## Related owner artifacts

- Prior ADR: `../decisions/2026-08-31-softwareco-ontology-topology.md`.
- Prior transition learning: `../learnings/2026-09-01-softwareco-ontology-topology-transition.md`.
- Proposed execution/validation/rollback: `2026-09-11-softwareco-ontology-consolidation-plan.md`.
