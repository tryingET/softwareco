---
summary: "Contribution workflow and guardrails for Softwareco's L1 company template/control-plane repository."
read_when:
  - "Contributing to the Softwareco root repository or embedded L2 templates."
  - "Choosing validation, review, and commit posture for a Softwareco control-plane change."
type: "procedure"
---

# Contributing to Softwareco

This repository is Softwareco's L1 company template/control-plane repo. Changes can affect company policy, operator navigation, embedded L2 templates, or generated descendants, so preserve source-owner and propagation boundaries.

## Workflow

1. Confirm the concern belongs at Softwareco root rather than a child owner repo.
2. Inspect the dirty worktree and avoid overwriting unrelated changes.
3. For architecture-significant or authority-changing work, follow the decision lifecycle before implementation.
4. Keep mutation bounded and reviewable; broad reasoning does not authorize broad file changes.
5. Run template checks:

   ```bash
   bash ./scripts/check-template-ci.sh
   ```

6. Use deterministic wrapper tooling before ad-hoc scripting:

   ```bash
   ./scripts/rocs.sh --doctor
   ./scripts/rocs.sh --which
   ```

7. Capture reusable evidence or learning through the owning AK/KES/source surface.
8. Commit directly to `main` for normal work. Use a PR only for releases or when the operator explicitly requests a review gate.
9. Commit only relevant files and include validation evidence.

## Required guardrails

- Keep render recursion bounded: `L0 -> L1 -> L2`.
- Treat packages/apps inside an L2 monorepo as internal monorepo members, not L3 or separate L2 repos.
- Keep `.copier-answers.yml` committed.
- Do not add nested Copier invocations in template `_tasks`.
- Keep `contracts/layer-contract.yml` aligned with README and AGENTS recursion sections.
- Preserve baseline skeleton folders for generated repos unless an accepted policy changes them.
- Keep organization-doc profiles explicit:
  - `l1_org_docs_profile=rich|compact`
  - `l2_org_docs_default=compact|rich` when a company default is accepted
- Preserve required git baseline files.
- Capability maps route; owner repos prove current support.
- Do not turn docs, review notes, or generated projections into shadow runtime authority.

## Propagation changes

For a change intended to reach descendants, identify:

- source layer;
- eligible target layer/entity kinds;
- exact file or feature unit;
- provenance requirements;
- validation contract;
- rollback unit.

Read [[/home/tryinget/ai-society/core/tpl-template-repo/docs/dev/architecture/layer-taxonomy-and-propagation-architecture.md|Layer Taxonomy and Propagation Architecture]] before propagation. Do not infer eligibility from path depth alone.

## Optional packs

Community, release, and trust-gate packs remain profile-controlled. Enabling one is a deliberate template/product decision and must include its validation and support obligations; do not add only decorative files.
