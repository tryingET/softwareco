---
summary: "Decision 74 Track B re-review of the revised Pi runtime, WIP, source-owner, and FCOS contract."
read_when:
  - "Reviewing the second Decision 74 runtime attempt."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
review_track: "pi-runtime-operator-wip-fcos"
reviewed_commit: "269035fcda9e2964ded86516ca6d7a471fd1acb1"
review_outcome: "ready_for_adr"
---

# Decision 74 Track B re-review

## Determination

All five prior runtime/operator blockers are materially resolved. The design is implementable without a project-local Pi extension and without treating Pi behavior, portfolio wrappers, governance metadata, or FCOS items as execution authority.

## Prior must-fix disposition

1. **Pi Modes dependency:** resolved. The RFC pins `@tryinget/pi-modes` `0.3.0`, tag `pi-modes-v0.3.0`, commit `173b508b0bea27550f061e252e1d86a0638d2d71`. Immutable release inspection and isolated validation passed 73 tests and the quick artifact gate. Installation, Softwareco artifact lint, and live Pi invocation remain truthful post-ADR activation gates.
2. **Authority-owned expiry:** resolved. Exact active/revoked/superseded/terminal `SF3` forms and per-operation checks are defined; charter remains a consistency projection.
3. **WIP membership/release:** resolved. Wave identity, coordinator task, append-only admission/release events, distinct owner-task identity, status counting, owner-approved release, overhead exclusions, and read/write/readback are specified.
4. **Single controller:** resolved. Human designation, bounded lease, atomic task claim, claimant/lease equality, handover, stale-session behavior, serialized admission, and advisory fallback are explicit. The contract correctly claims a procedural invariant rather than a global lock.
5. **`/cto` arguments/root invocation:** resolved. `argument-hint`, `$ARGUMENTS`, absent-objective stop, normalized objective/preflight output, and trusted Softwareco-root baseline match Pi's documented prompt-template behavior.

## FCOS and source-owner boundary

FCOS remains coordination-only/non-claimable. Real writes require exact FCOS-owner task and `--task <id> --json`. Close evidence is not owner acceptance. Declined cross-repo handoff blocks the wave unless genuinely redesigned and reaccepted. Owner-task lifecycle remains external to the portfolio wrapper.

## Remaining must-fixes

None for Track B ADR readiness.

## Material nice-to-haves

- Deterministically validate all `softwareco.*.v1` details schemas.
- Attach attributable owner evidence to governance receipts.
- Scan all coordinator histories until every owner task has a controlling release.
- Do not archive a wave so unreleased task membership becomes hidden.
- Record the release-tag merge commit and package-subtree equivalence.
- Add negative integration tests for every preflight and authority failure.
- Validate FCOS dry-run and real receipts separately.
- Report controller/coordinator/FCOS overhead beside owner-task WIP.

## Open questions

One non-blocking post-ADR usability question remains: descendant `/cto` discovery. Trusted Softwareco-root invocation is the accepted baseline.

## Outcome and legal next move

- outcome: `ready_for_adr` for Track B;
- controlling Decision 74 closure still requires Track A and synthesis;
- this review authorizes no activation or source-owner/FCOS mutation.

No files were mutated by the reviewer.
