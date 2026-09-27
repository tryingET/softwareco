---
summary: "Evidence for selecting infra/workstation as the independent Agent Kernel build-provenance producer-policy owner."
read_when:
  - "Reviewing Decision 148."
type: "evidence-note"
status: "current"
as_of: "2026-09-01"
task_id: 5305
decision_id: 148
---

# Evidence note — independent AK build-provenance owner

## Trigger

Agent Kernel Decisions 146/147 require an independently verified mapping from running
AK executable bytes to exact source commit before a sensitive successor-transition
campaign can be admitted.

P0 task 5304 stopped at this prerequisite. Its tracked evaluation is:

```text
softwareco/owned/agent-kernel/docs/project/2026-09-01-repository-successor-prerequisite-feasibility.md
SHA-256 = bdb2bd866232864c0439a93ee94f6ed624dea9af46693082d90a9caaa7a6f8c3
AK evidence = evidence:8171 (fail-closed prerequisite result)
```

## Bounded owner search

Read-only provenance feasibility review:
`dispatch:dispatch-1788260696260`.

Observed:

- AK embeds its own checkout commit and writes an unsigned installer pin manifest;
  neither is independent source provenance.
- AK runtime gate hashes a named path before execution and does not bind mapped bytes
  through a retained executable descriptor.
- DSPx has a strong accepted DSSE/Sigstore policy-chain pattern, but its owner and
  subjects are explicitly DSPx-specific.
- provisioning owns machine bootstrap and package install, not release custody.
- engineering-core owns guidance, not artifact production/currentness.
- no accepted generic Softwareco build-provenance producer was established by the
  bounded inspected capability maps and owner docs.

This is not an exhaustive claim that no possible owner exists. It is sufficient to
fail closed until an accepted owner decision names one.

## Why workstation is the selected owner

The infra capability map assigns `infra/workstation` concrete workstation runtime,
packaging, validation, service operation, and promoted control-plane ownership.
Workstation AGENTS requires plan-first, approval-gated, validation-backed mutation and
single-machine-first delivery.

A workstation-owned producer is:

- independent of Agent Kernel's self-report;
- aligned with installed-binary admission and rollback on the canonical machine;
- narrower than creating a universal build service;
- able to consume DSPx as a reference pattern without mutating or appropriating DSPx;
- governed by the infra lane root for cross-repo owner-boundary decisions.

## Technical feasibility

The P0 review found:

- mapped/running executable bytes can be safely measured from a retained
  `/proc/self/exe` descriptor under `forbid(unsafe_code)`;
- existing SHA-256 and Ed25519 verification dependencies are sufficient for an AK
  consumer;
- signed DSSE/in-toto statements can bind artifact hash to source/build identity;
- currentness/revocation must come from an independent append-only owner policy, not
  the AK DB being admitted;
- retained descriptor measurement closes pathname replacement but not same-inode
  mutation; the later implementation decision must select a sealed/immutable verified
  execution object.

Technical feasibility does not prove that a signer/workflow is enrolled or that a
real artifact has been produced.

## First RFC review and scope correction

The tracked first candidate had SHA-256
`8702f974fe4e76f0862161f79d6da5adfecb23c34d3530f57ed0cd0805dbc367`.
Independent reviews:

- supply-chain/bootstrap: `dispatch:dispatch-1788261763493`;
- operational/rollback: `dispatch:dispatch-1788261763494`.

Both returned `revise_rfc`. Material findings covered trust-role separation,
credential-free build isolation, incomplete DSSE/policy semantics, bootstrap/
currentness/rotation/revocation, source/build claim ambiguity, same-inode mutation,
consumer receipt binding, atomic installation/rollback, and incident recovery.

Those findings showed that the owner-selection decision was prematurely accepting an
implementation protocol. The revised RFC narrows Decision 148 to accountable owner
selection and converts every unresolved technical area into a mandatory separately
reviewed workstation implementation-decision input. No first-review finding is
silently called resolved as implementation; it is explicitly deferred behind that
new decision membrane.

## Source-owner boundary

```text
infra root = cross-repo policy/owner decision
workstation = producer, signer policy, policy chain, launcher, runbook, evidence
agent-kernel = mapped-image measurement and verification consumer only
DSPx = reference pattern only
```

## Current non-effects

- No workstation or Agent Kernel file was modified by this evidence note.
- No signer, key, workload, workflow, remote, transparency entry, or release was
  created.
- No installed AK binary or policy pin was changed.
- No AK database schema/capability/repository transition occurred.
- `dspy-lm-auth` was not moved.

## Evidence limits

- Remote workflow/signing state was not inspected or changed.
- Private signer/credential state was not read.
- The decision still requires independent supply-chain/bootstrap/rollback review.
- Owner selection does not complete Agent Kernel P0-C; workstation implementation and
  synthetic proof must land first.
