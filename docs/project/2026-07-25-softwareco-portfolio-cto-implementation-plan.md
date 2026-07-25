---
summary: "Post-ADR implementation plan for Decision 74's Softwareco portfolio CTO workbench and activation gates."
read_when:
  - "Implementing Decision 74 after ADR acceptance."
type: "plan"
status: "active"
date: "2026-07-25"
decision_id: 74
execution_task_id: 4156
---

# Decision 74 — implementation plan

## Accepted baseline

- Decision: `74`, accepted and ADR-recorded through governance receipt `8818` / ADR receipt `8819`;
- accepted at: `2026-07-25T08:11:27.729630885Z`;
- hard expiry: `2026-08-24T08:11:27.729630885Z`;
- ADR: `docs/decisions/2026-07-25-softwareco-portfolio-cto-workbench.md`;
- execution task: `4156`;
- direction: `SF3`, active as a decision/implementation frame but not yet delegated;
- immutable Pi Modes dependency: `@tryinget/pi-modes@0.3.0`, commit `173b508b0bea27550f061e252e1d86a0638d2d71`.

Acceptance does not activate the CTO. Activation follows only after every stage below passes.

## Stage 1 — project operator surfaces

1. Selectively unignore and track only:
   - `.pi/modes/softwareco-cto.json`;
   - `.pi/mode-presets/softwareco-cto.json`;
   - `.pi/prompts/cto.md`.
2. Keep all other `.pi/` local state ignored.
3. Create a schema-v2 `append` overlay that explicitly grants no authority.
4. Create a native-base preset selecting only the CTO overlay.
5. Create root-only `/cto <objective>` with `$ARGUMENTS`, missing-objective stop, compact preflight, repeated pre-operation authority checks, owner-origin receipt stops, and no descendant-discovery claim.

## Stage 2 — deterministic structural checks

Create `scripts/check-cto-operator-surface.sh` to fail closed on:

- wrong or mutable Pi Modes package identity;
- mode/preset owner-lint failure;
- wrong strategy/base/overlay composition;
- missing `/cto` frontmatter or `$ARGUMENTS`;
- missing Decision 74, `SF3`, owner-origin, WIP, FCOS, terminal, or human-reserved language;
- broad `.pi` tracking;
- stale Decision 68 active projections;
- missing Decision 74 projection fields.

The script validates structure and policy text. It does not claim model compliance or active delegation.

## Stage 3 — post-decision projections

Update:

- `docs/org/cto-agent-charter.md`;
- `docs/org/governance.md`;
- `docs/org/operating_model.md`.

Each projection must name Decision 74, accepted time, hard expiry, jurisdiction, finite governance delta, owner-origin receipts, objections, terminal acceptance, two-wave/six-task limits, second-wave human checkpoint, controller lease, FCOS owner boundary, revocation path, and reserved human powers. Decision 68 remains historical and expired.

## Stage 4 — immutable Pi runtime

1. Install exact `npm:@tryinget/pi-modes@0.3.0` rather than the mutable local checkout.
2. Run the package's full available release validation.
3. Reload or launch a fresh Pi process.
4. Verify exact package/version provenance.
5. Run live trusted-root proofs:
   - `/mode-preview --json softwareco-cto` or equivalent preset preview;
   - `/mode use softwareco-cto`;
   - `/mode-status --json`;
   - `/cto` discovery and missing-objective advisory behavior;
   - `/mode off` rollback.
6. Treat command transport acceptance without extension error/stderr inspection as insufficient.

## Stage 5 — controller task and direct human designation

1. Create one Softwareco controller task linked to `SF3`, with all source mutation forbidden and a task contract for admission control/readback only.
2. Put the exact controller task id into `/cto` and the charter projection.
3. Prepare—but do not execute—the exact `ak governance record` command for `softwareco-portfolio-cto:decision74:controller-designation`.
4. Show the unique claimant, lease no longer than 14,400 seconds, designation expiry, evidence ref, and rollback/handover path to `human-operator`.
5. Pause until the human directly records the designation receipt.
6. Read back the receipt and atomically claim the controller task with the exact claimant/lease.

## Stage 6 — delegation activation

After all prior stages pass:

1. fresh-read Decision 74, `SF3`, controller task/receipt, projections, mode provenance, and live proof;
2. verify no revocation, terminal, or superseding decision;
3. verify current UTC is before hard expiry;
4. set `SF3 state_detail` to:

```text
delegated_active_decision_74;accepted_at_utc=2026-07-25T08:11:27.729630885Z;activated_at_utc=<actual RFC3339>;expires_at_utc=2026-08-24T08:11:27.729630885Z
```

5. post-read and stop for manual reconciliation on conflict;
6. run one advisory `/cto` preflight and record evidence.

## Stage 7 — portfolio proof handoff

Activation unlocks only the portfolio thesis and canary workflow:

1. produce an evidence-backed ranking of `softwareco/owned`;
2. obtain role-specific owner-origin admission receipts;
3. admit one first wave and no more than six owner tasks;
4. use FCOS only through its owner if genuinely cross-repo;
5. execute and measure one outcome wave;
6. obtain all terminal acceptances and the human mandate terminal decision;
7. require another direct human checkpoint before any second concurrent wave.

The portfolio thesis and outcome wave are separate execution leaves after this workbench task; task `4156` does not select them by implication.
