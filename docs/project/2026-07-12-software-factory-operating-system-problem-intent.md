---
summary: "Problem/intent note for turning Softwareco's existing components into one operated, outcome-driven software factory."
read_when:
  - "Evaluating why Softwareco has strong tooling but lacks a routinely operated end-to-end value stream."
  - "Reviewing the Software Factory Operating Protocol RFC."
type: "problem-intent"
system4d:
  container:
    boundary: "Softwareco company operating flow across existing AI Society owner surfaces; not a new runtime or authority layer."
    edges:
      - "[Evidence note](2026-07-12-software-factory-operating-system-evidence.md)"
      - "[RFC](2026-07-12-software-factory-operating-system-rfc.md)"
  compass:
    driver: "Convert abundant local capabilities into repeated delivery of measurable outcomes."
    outcome: "One paved, governed value stream from demand to outcome learning."
  engine:
    invariants:
      - "AK remains canonical for direction, tasks, decisions, evidence, and lineage."
      - "FCOS remains cross-repo control-board authority rather than repo-local execution authority."
      - "The proposal adds an operating protocol, not another platform or database."
  fog:
    risks:
      - "Adding ceremony without changing selection, flow, release, or learning behavior."
      - "Treating engineering completion as evidence of product outcome."
---

# Software Factory Operating System — problem and intent

## Trigger

Softwareco contains substantial delivery, quality, orchestration, runtime, evidence, and learning capabilities, yet it does not presently expose one routinely operated company flow that answers:

1. what demand matters now;
2. who owns the intended outcome;
3. what finite capacity has been committed;
4. how work reaches a safely operated release;
5. whether the user or organizational outcome improved; and
6. what decision follows from the evidence.

The live Softwareco AK direction export reports zero direction nodes. Softwareco purpose, vision, strategic objectives, governance, and operating-model drafts now exist, but the proposed company governance is inactive: no accepted Softwareco-scoped appointment/delegation or active strategic frame makes those drafts an operated company loop. Company program guidance remains planning-oriented rather than an active portfolio scheduler. Release and service-operation behavior is predominantly repo-specific.

## Problem

Softwareco is currently closer to a federation of capable repositories than a coherent software factory. Its paved roads mostly begin after work has already been selected. This creates four systemic failure modes:

- **selection opacity:** locally attractive work can progress without a comparable company-level reason for doing it now;
- **flow fragmentation:** intake, discovery, execution, cross-repo coordination, release, operation, and learning use strong but disconnected surfaces;
- **completion substitution:** task or CI completion can be mistaken for safe promotion or improved outcomes;
- **evidence without steering:** receipts, traces, diaries, and learnings can accumulate without an accountable continue/stop/redirect decision.

## Intent

Establish the smallest coherent Softwareco operating protocol over existing AI Society owner surfaces.

The desired loop is:

```text
sense demand
-> discover and frame an outcome
-> make a finite portfolio commitment
-> execute through owner repos
-> promote safely
-> operate with named ownership
-> measure technical and product outcomes
-> continue, stop, redirect, or learn
```

## Why this is Tier 1

The proposal affects company direction, cross-repo coordination, release and operational expectations, evidence contracts, and the relationship between AK, FCOS, Pi, KES, and product owners. It must therefore proceed through RFC review before any ADR or broad implementation.

## Non-authorization

This note does not:

- appoint a steward or product owner;
- create or alter AK direction, tasks, decisions, or evidence;
- create or alter FCOS board items;
- define new ROCS semantics;
- authorize rollout, migration, or implementation;
- treat the accompanying RFC as an accepted decision.
