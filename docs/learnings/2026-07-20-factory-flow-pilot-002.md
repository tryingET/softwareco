---
summary: "Factory Flow pilot 002 learning: safe observability can expose canonical drift quickly, but validation and a non-halted cursor do not establish readiness."
read_when:
  - "Designing external-issue operator loops or Factory Flow propagation."
  - "Interpreting passing validation, sequence cursors, or projection coherence as readiness."
type: "learning"
status: "accepted_pilot_learning_pending_terminal_decision"
date: "2026-07-20"
decision_id: 68
pilot_id: "SOFTWARECO-FACTORY-PILOT-002"
terminal_decision: "pending"
---

# Learning — truthful observability must precede authorized reconciliation

## Observation

A clean operator reached the correct issue-tracker authority and readiness conclusion in 48 seconds with zero errors, wrong-authority claims, unsafe effects, or manual repair. The repo-local validator and canonical-export dry-run both passed, yet the operator correctly classified the sequence as blocked because candidate index 0 was already bound to submitted GitHub issue `#30` while the canonical sequence cursor remained at zero.

The canary therefore improved truthfulness without claiming end-to-end readiness:

```text
contract-coherent projection
!= reconciled canonical cursor
!= review-ready
!= submission-ready
!= external-effect authority
```

## What worked

- **Main-first source truth was restored.** Stale MR-only wording was removed, issue-tracker landed on local `main` at `518ab43`, and Softwareco recorded the gitlink at `3456898`.
- **AK stayed canonical.** The sequencer exports canonical state to a temporary projection and never imports checked-in `STATE.json`.
- **Observation was separated from mutation.** The canary command cannot apply, rebuild, submit, or advance state.
- **Validation and outcome remained separate.** Passing structure/hash/reference checks did not become a readiness claim.
- **Cold-start evidence found the real blocker.** Existing issue `#30` and cursor index 0 require an explicitly reviewed reconciliation procedure.
- **Failure paths became legible.** Missing sequence status blocks without inventing a candidate; ROCS CI restores generated output after failure.

## Comparative evidence from pilots 001 and 002

| Shared invariant | Pilot 001 | Pilot 002 |
|---|---|---|
| canonical owner truth wins | native FCOS owner + AK | AK issue/sequence state |
| projections are non-authoritative | retirement packet/status projections | `STATE.json` |
| bounded mutation after broad reasoning | owner-doc retirement slice | observation-only canary + main-first correction |
| independent cold-start required | 56 seconds | 48 seconds |
| wrong-authority claims / external effects | 0 / 0 | 0 / 0 |
| validation is not outcome | archive/docs did not prove discoverability | contract coherence did not prove readiness |
| residual human authority | terminal completion and deletion limits | reconciliation/external effects and terminal decision |

These invariants are candidates for later template-owner review. Issue-tracker commands, sequence schema, GitHub identity, a permanent CTO identity, and observation-only implementation details are not general template requirements.

## Reusable rule

For operator workflows backed by canonical state, prefer:

```text
inspect authority
→ export canonical state
→ validate projections and authored inputs
→ classify readiness truthfully
→ stop on identity/cursor drift
→ obtain human authority for a reviewed reconciliation
→ rerun the same observation
```

Never infer readiness from `halted=false`, a zero-exit validator, a clean worktree, or a self-authored approval assertion.

## Limit and recommendation

Pilot 002 proves safe, rapid detection of a blocked external-issue workflow. It does not yet prove a review-ready or submission-ready end-to-end loop. The recommended terminal choice is **redirect** to a bounded, separately reviewed reconciliation/dedupe procedure for existing issue `#30`, followed by another cold-start run.

Broader L2/L0 propagation remains gated by the human terminal decision and a separate template-owner decision.

## Evidence

- Decision `#68`;
- tasks `#4088`, `#4093`, `#4094`, and `#4096`;
- issue-tracker commits `a0ebbd9` and `518ab43`;
- Softwareco gitlink commit `3456898`;
- AK correction evidence `#4971`–`#4975`;
- cold-start peer `scoutpeer-mrtk5n7j-b8934ad1`;
- `docs/project/2026-07-20-factory-flow-pilot-002-cold-start-receipt.md`.
