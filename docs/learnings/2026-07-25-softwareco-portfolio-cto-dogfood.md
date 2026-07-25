---
summary: "Decision 74 dogfood learning: separate sensing from admission, prove zero state explicitly, execute through owner tasks, and reduce human-receipt interaction friction."
read_when:
  - "Designing or operating future Softwareco CTO portfolio waves or human-origin governance gates."
type: "learning"
status: "accepted_local_learning"
date: "2026-07-25"
decision_id: 74
wave_key: "IW-SF3-DMF-LOOP-IMPACT"
---

# Softwareco portfolio CTO dogfood learning

## What the dogfood proved

The first Decision 74 workbench implementation was constitutionally safe but operationally inert. `/cto` required wave/admission evidence before it could bootstrap a portfolio thesis from an empty portfolio.

The corrective contract separated four lanes:

```text
authority baseline
-> complete portfolio-state readback
-> read-only sensing / proposal
-> owner-accepted selection
-> admission
-> owner-native execution and outcome proof
```

A proved empty set is a valid sensing result. It is never owner consent. This distinction allowed the active CTO to compare investments without weakening selection or mutation gates.

## Portfolio selection learning

Readiness dominated nominal leverage for the first wave:

- Context Packer excerpting had high strategic leverage but a divergent, heavily dirty integration baseline.
- Pi Server fingerprint metadata was useful but carried dirty-tree, public-contract, and Node-version coordination risk.
- DesignMD Foundry's staged-impact defect was smaller but clean, owner-local, already task-anchored, reversible, and directly dogfoodable.

The CTO therefore selected the smallest **outcome-complete** investment, not the smallest diff or the most ambitious proposal.

## Owner execution learning

The successful wave preserved distinct facts:

- Product/Project owners accepted the outcome, capacity, displacement, and exact task scope through receipts `8838` and `8839`.
- Controller evidence `5167` admitted owner task `3425` without changing its lifecycle.
- DesignMD Foundry executed and completed task `3425` under its own scope and gates.
- Terminal receipts `8851` and `8852` accepted outcome and implementation evidence.
- Release receipt `8854` and event `5175` freed portfolio WIP without rewriting owner task state.
- Outcome evidence `5176` closed the portfolio wrapper.

This is the intended federal architecture: portfolio sequencing does not absorb source-owner execution.

## Dogfood behavior learning

The staged-index test must be behavioral, not only static. A disposable clone showed:

```text
old recipe + staged src/cli.ts -> impact=normal   # defect
new recipe + staged src/cli.ts -> impact=wide
new recipe + staged docs       -> impact=normal
```

The final committed owner outcome is DesignMD Foundry commits `3c65773` and `33ff05b`, owner evidence `5169`, `5172`, and `5174`, with the full landing gate passing.

## Human interaction learning

A human-origin receipt requires direct human execution, but it does **not** require an interview form or manually pasted stdout as the normal UX.

For a single exact governance command, prefer:

1. prefill the Pi editor with `!<exact command>` when the host supports it, or present one plain shell block when it does not;
2. let the human review and execute directly;
3. fresh-read the exact governance concern/receipt from AK afterward;
4. ask for pasted output only when readback is ambiguous.

The repeated interview-and-paste flow in this dogfood created avoidable operator friction and should not be repeated.

## Promotion posture

Promote these local rules into future CTO/operator guidance:

- partition sensing, selection, admission, and execution gates;
- treat complete empty readback as zero, not missingness;
- choose first waves for outcome completeness and clean owner execution;
- use owner-native receipts at acceptance, terminal acceptance, and release;
- use low-friction direct-command handoffs for human-origin gates.
