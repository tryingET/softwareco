---
summary: "ADR candidate for Decision 79's one-time quarantine of malformed Decision 77 epoch receipt 8967."
read_when:
  - "Accepting, implementing, or validating Decision 79."
type: "adr"
status: "proposed"
date: "2026-07-26"
decision_id: 79
amends_decision_id: 77
system4d:
  container:
    boundary: "One malformed Decision 77 epoch receipt and its append-only recovery; all ordinary epoch and owner authority remains outside."
  compass:
    driver: "Recover the accepted recurring CTO framework without weakening its hard epoch maximum or rewriting immutable history."
  engine:
    invariants:
      - "Receipt 8967 never passes authorization validation."
      - "Only one direct-human invalidation may quarantine receipt 8967."
      - "Every other Decision 77 duration and authority rule remains exact."
      - "Any later operation requires a new controller, epoch, claimant, and human authorization."
  fog:
    risks:
      - "A special case becomes a general timestamp tolerance."
      - "Current task state is mistaken for complete external-effect proof."
      - "Amendment acceptance is mistaken for epoch authority."
---

# ADR — one-time quarantine of Decision 77 receipt 8967

## Status

Proposed. Direct accountable-human acceptance is required. This document grants no invalidation or epoch authority.

## Decision

Adopt Decision 79's exact RFC at commit `0dc276f` and controlling review closure at commit `19a872c`:

- [RFC](../project/2026-07-26-softwareco-decision77-invalid-epoch-recovery-rfc.md)
- [Problem](../project/2026-07-26-softwareco-decision77-invalid-epoch-recovery-problem-intent.md)
- [Evidence](../project/2026-07-26-softwareco-decision77-invalid-epoch-recovery-evidence.md)
- [Review synthesis](../reviews/2026-07-26-softwareco-decision77-invalid-epoch-recovery-synthesis.md)

Authorize implementation of one append-only invalidation branch that applies only to receipt `8967`, epoch `d77-e1-20260725`, controller `4220`, claimant `pi-session-softwareco-cto-d77-epoch1`, and the measured `1,074,180` nanosecond excess.

## Non-retroactivity

Receipt `8967` remains immutable malformed history and never validates as authority. The amendment does not rewrite or retroactively revoke it. A later direct-human invalidation prospectively quarantines it and returns the chain head to `inactive` after proving the accepted Decision-79 membrane and zero-operation envelope.

## Authority

Decision-79 acceptance authorizes only checker implementation and preparation of the exact invalidation. The invalidation itself requires a distinct direct-human receipt. Neither authorizes a Decision-77 epoch. A later epoch remains optional and requires a new task, epoch ID, claimant, direct-human receipt, and exact claim.

Off-system effect absence is a direct-human attestation, not a machine inference. AK evidence proves only the bounded task, evidence, direction, and governance facts it enumerates.

## Runtime consequence

The checker gains graph-complete, overflow-safe epoch history validation; preserves every Decision-77 branch; recognizes one exact invalidation; fresh-reads deferral `182` and task `4220` on every pass; and keeps all modes fail-closed until invalidation. Mutation-free fixtures prove malformed and valid states.

## Alternatives rejected

Ignoring the discrepancy, shortening only the task lease, ordinary handback, receipt mutation/deletion, checker-only exception, and unnecessary framework supersession are rejected for the reasons in the RFC.

## Validation and rollback

Implementation and rollback follow the linked Decision-79 plans. Decision 74 terminal receipt `8870`, Decision 77's nonterminal framework, owner boundaries, and the unrelated capability-map modification remain untouched.
