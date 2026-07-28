---
summary: "Correcting Decision 86 review: native FrankenSQLite invalidates the raw DB+WAL snapshot design; outcome revise_rfc."
read_when:
  - "Determining whether Decision 86 may advance after the native-fsqlite architecture correction."
type: "review"
status: "revise_rfc"
date: "2026-07-28"
decision_id: 86
review_track: "native_fsqlite_corrective"
reviewed_commit: "d1c6a59e0795cb76b5bb5a628db2bb18506e65b3"
review_outcome: "revise_rfc"
---

# Decision 86 native-fsqlite correcting review

## Outcome

`revise_rfc`

Decision 86 must not advance to ADR, acceptance, installation, or activation. The prior `ready_for_adr` synthesis did not validate its authority-read boundary against Agent Kernel's native FrankenSQLite (`fsqlite`) runtime.

## Findings that invalidate the prior closure

1. Agent Kernel uses native `fsqlite`, not stock SQLite. The installed AK commit `a97812c21e612a2b607e82a7e51dc5c87a9c9403` pins FrankenSQLite revision `2447135a9ff30016485919b17922413437615efb`.
2. The two Decision 83 failures prove only that AK's ordinary native open path hit a read-only filesystem. They do not prove the narrower claim that stock SQLite or private `-shm` creation was the exact cause.
3. `cto-canary/snapshot_authority.py` hashes and copies the live main file and WAL sequentially without an engine-native lock, coherent read transaction, or generation/snapshot identity. Stable before/after hashes are drift detection, not an fsqlite snapshot proof.
4. The helper validates the private copy with Python's stock `sqlite3`. That is not the owner runtime or a sufficient native-fsqlite verifier, and the target is not re-fingerprinted after that open.
5. The canary invokes a generic `ak` path rather than an exact approved absolute AK binary with bounded environment and manifest identity.
6. Agent Kernel currently has engine-enforced query-only opening for narrow owner paths, but no verified general bounded portfolio observation export and no concurrent live-WAL snapshot proof. Existing `ak backup` checkpoints/truncates the WAL and therefore does not satisfy the canary's zero-source-mutation contract.

## Agent Kernel owner confirmation

The active Agent Kernel peer session `session-019fa8a3-f6d3-761f-881f-e55e27ad5fc0` reported no objection to correction and confirmed:

- ordinary AK read command families are not a safe zero-source-mutation boundary merely because their CLI semantics are reads;
- raw DB+WAL copying has no AK/fsqlite ownership proof;
- the correct cross-owner outcome is a Softwareco-to-Agent-Kernel `source_owner_handoff`;
- the next Agent Kernel stage is a `design_packet` for an AK-owned one-shot bounded observation export;
- Decision 86 must return to `revise_rfc` until that owner boundary and its concurrency/zero-delta proofs exist.

## Required owner route

- Agent Kernel design task `4326`: design a native-fsqlite bounded, noncanonical observation export for downstream canaries.
- Agent Kernel repair task `4327`: add an exact-pair governed `ak decision unlink-task` surface before repairing the accidentally linked `(decision 86, task 86, decision_support)` row.
- Softwareco correction task `4325`: record this correcting review and route Decision 86 back to revision.
- The accidental link is contained by evidence `5572` and blocked governance receipt `9274`; it must not be repaired through direct SQL, task deletion, role relabeling, or fake reevaluation.

## Proof required before a future READY outcome

- engine-enforced query-only source access with no ordinary open, checkpoint, migration, or reconciliation;
- one coherent read transaction or a proven native snapshot generation;
- concurrent writer, WAL growth/checkpoint/rotation, and failure-injection coverage;
- byte and metadata zero-delta on the source DB, WAL, and SHM;
- exact AK binary and fsqlite revision identity in the derived packet;
- bounded completeness/gap semantics and deterministic packet digest;
- final verification through the exact native AK pin, never Python `sqlite3`;
- no source DB or sidecar visibility in the canary sandbox.

## Preserved history and non-authorizations

Decision 83 remains accepted-and-human-stopped immutable history. No model call occurred. This review does not authorize an ADR, acceptance, installation, activation, live-link repair, source database mutation, or implementation of Agent Kernel internals from the Softwareco canary task.
