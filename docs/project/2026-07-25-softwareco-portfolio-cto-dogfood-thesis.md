---
summary: "Decision 74 proposal-only portfolio thesis comparing three owned-repo dogfood investments and proposing one bounded first outcome wave."
read_when:
  - "Reviewing or accepting the first Decision 74 Softwareco portfolio dogfood wave."
type: "proposal"
status: "owner_acceptance_pending"
date: "2026-07-25"
decision_id: 74
strategic_frame: "SF3"
controller_task_id: 4182
corrective_task_id: 4184
---

# Decision 74 dogfood portfolio thesis

## Classification and authority

This is **sensing / proposal-only** output from the active Decision 74 CTO workbench. The corrected zero-state preflight proved no admitted waves, owner tasks, membership receipts, or FCOS refs at `2026-07-25T12:16:03.681691691Z`.

No investment is selected, admitted, or executable until direct owner-originated acceptance receipts and exact source-owner task scope pass the Decision 74 selection/admission gates.

## Portfolio question

Which single bounded owned-repo investment can produce a real operator outcome today, exercise owner-native execution and evidence, avoid external effects, and close with deterministic proof?

## Evaluated options

### A — Context Packer bounded excerpts for explicit oversized Markdown seeds

- **Owner:** `softwareco/owned/pi-extensions/packages/pi-context-packer`.
- **Observed problem:** the Decision 74 RFC was explicitly seeded but wholly omitted because its ~30KB size exceeded the effective item/provider budget; the provider cannot emit a partial range.
- **Outcome:** return a labeled, objective-relevant bounded excerpt rather than a whole-file omission.
- **Strategic leverage:** high; advances trustworthy agent/local-AI operator journeys and reduces residual retrieval.
- **Readiness:** package path clean, but owner repo is heavily dirty and local history is ahead 91 / behind 136 with unresolved package divergence.
- **Decision:** defer. The outcome is valuable but cannot truthfully complete today without owner-approved baseline reconciliation.
- **Evidence:** explorer dispatch `dispatch-1784981876273`.

### B — Pi Server explicit replay fingerprint export schema

- **Owner:** `softwareco/owned/pi-server`.
- **Observed problem:** `get_command_history` consumers infer replay fingerprint semantics from a `v2:sha256:` string rather than an explicit response schema.
- **Outcome:** additive self-describing fingerprint schema for audit/export tooling.
- **Strategic leverage:** medium-high; improves governed execution auditability.
- **Readiness:** AK task `48` is pending, but unscoped; the worktree has broad pre-existing changes and validation requires Node 22 rather than the current Node 26.
- **Decision:** defer. Good follow-up after dirty-tree coordination and owner acceptance of the public response shape.
- **Evidence:** explorer dispatch `dispatch-1784981876274`.

### C — DesignMD Foundry stage-aware loop impact planning

- **Owner:** `softwareco/owned/designmd-foundry`, CODEOWNER `@softwareco-owners`.
- **Observed problem:** `just loop-impact-plan` checks unstaged and untracked changes but omits `git diff --cached`; staged runtime/design changes can therefore be misclassified as `impact=normal` instead of `impact=wide`.
- **Outcome:** operators receive the correct full-validation recommendation for staged risk-bearing changes.
- **Strategic leverage:** focused but real; advances `SOFT-O5` evidence-led engineering and protects a human-facing design product's validation loop.
- **Readiness:** owner worktree is clean; AK task `3425` is pending with `Justfile` already in scope; the implementation is one bounded command-surface correction plus alternate-index dogfood.
- **Decision:** proposed first wave.
- **Evidence:** current `Justfile` line 51, AK task `3425`, explorer dispatch `dispatch-1784981876275`.

## Proposed first outcome wave

- **Wave key:** `dmf-stage-aware-loop-impact`.
- **Outcome envelope:** staged runtime/design changes in DesignMD Foundry deterministically produce `impact=wide` and `next=just loop-impact-wide`; clean/docs-only changes remain `impact=normal`.
- **Capacity envelope:** one admitted owner task (`designmd-foundry` AK `3425`), one implementation file (`Justfile`), and only the owner-required AK projection/scope artifacts needed for truthful task closeout.
- **Displacement:** defer Context Packer excerpting until clean-baseline reconciliation; defer Pi Server fingerprint schema until dirty-tree and Node 22 coordination.
- **Guardrails:** no product code, UI, `DESIGN.md`, dependencies, release, publication, FCOS write, or external effect.
- **Proof:** alternate Git-index staged-runtime and docs-only cases; repo fast/full loop gates; AK projection/scope checks; owner-native task completion and terminal receipt.
- **Stop:** any pre-existing owner worktree change, scope ambiguity, failed full gate, or mismatch between staged classification and declared outcome.

## Owner decision required

`@softwareco-owners` must directly accept the outcome, capacity, displacement, and exact task-scope envelope through owner-originated applied governance receipts with owner-native evidence refs. Until then, this thesis remains proposal-only.
