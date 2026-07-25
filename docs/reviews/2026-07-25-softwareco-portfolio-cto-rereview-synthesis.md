---
summary: "Controlling second review synthesis for Decision 74, requiring one more authority revision."
read_when:
  - "Determining the Decision 74 next move after the first revised candidate."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
reviewed_commit: "269035fcda9e2964ded86516ca6d7a471fd1acb1"
review_outcome: "revise_rfc"
---

# Decision 74 second review synthesis

## Inputs

- exact candidate: `269035fcda9e2964ded86516ca6d7a471fd1acb1`
- [Track A authority re-review](2026-07-25-softwareco-portfolio-cto-authority-rereview.md): `revise_rfc`
- [Track B runtime re-review](2026-07-25-softwareco-portfolio-cto-runtime-rereview.md): `ready_for_adr`
- synthesis rule: any material must-fix from either required track blocks ADR readiness.

## Synthesis

Runtime architecture is ready. The immutable Pi Modes dependency, trusted-root invocation, finite WIP membership, controller lease, source-owner task split, and FCOS boundary are sufficient for post-ADR implementation.

Constitutional attribution is not ready. Controller-authored owner identities could counterfeit consent; fallback and objection conflict; terminal acceptance is underspecified; and acceptance/activation/immediate-revocation events are not cleanly separated.

## Controlling outcome

- outcome: `revise_rfc`
- legal next move: revise the four authority defects, commit a new immutable candidate, repeat both required tracks against the exact new commit, and synthesize.
- blocked: Decision 74 acceptance, ADR, delegated `SF3` activation, workbench activation, portfolio admission, owner-repo mutation, and FCOS mutation.

The prior review attempts remain immutable history.
