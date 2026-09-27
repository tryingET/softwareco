---
summary: "Accept infra/workstation as the accountable future owner of independent Agent Kernel build-provenance production/policy, while keeping implementation and P0-C separately gated."
read_when:
  - "Selecting or implementing Agent Kernel build provenance."
  - "Transferring Softwareco build-provenance ownership."
type: "decision"
status: "accepted"
as_of: "2026-09-01"
decision_id: 148
task_id: 5305
---

# Decision — workstation ownership of independent AK build provenance

## Status

Accepted by AK Decision 148 as an owner-selection decision only.

- RFC: `docs/project/2026-09-01-softwareco-build-provenance-owner-rfc.md`
- Reviewed RFC SHA-256:
  `e53d693bffafb8b904edeb93a02a3d452bdd3a284a7251b46860c7cb70a1e5fb`
- Review synthesis:
  `docs/project/2026-09-01-softwareco-build-provenance-owner-review.md`

## Context

Agent Kernel successor-transition P0 requires independent proof that exact running AK
bytes correspond to exact source/build identity. AK's embedded commit and unsigned
installer manifest are self-derived diagnostics. DSPx has a strong reference pattern
but owns only DSPx artifacts. A bounded owner search did not establish an accepted
generic Softwareco producer.

The first RFC draft prematurely specified signer/policy/launcher mechanics. Independent
review found unresolved trust-role, isolation, wire, currentness, immutable-execution,
rollback, and incident questions. The accepted RFC was narrowed so this decision
selects the accountable owner without pretending those implementation choices are
settled.

## Decision

Accept this owner split:

```text
softwareco/infra lane root
  cross-repo provenance owner-selection and owner-transfer decisions

softwareco/infra/workstation
  accountable future owner for the independent AK build-provenance producer-policy
  capability on the canonical workstation

softwareco/owned/agent-kernel
  running-image measurement and externally supplied provenance verification consumer
  only

softwareco/owned/dspx
  reference pattern only; no widened ownership or mutation
```

Workstation accountability means it must sponsor and operate a later accepted
implementation decision, proof, runbook, revocation, recovery, and consumer handoff.
It does not mean the capability exists today.

## Mandatory later decision

Workstation task `5306` owns the next Tier-1 implementation decision. It remains
deferred while existing workstation WIP tasks `5224` and `5298` are claimed and until
Decision 148 is accepted/unblocked.

Before implementation, that decision must independently resolve:

- compromise/threat model and separate producer/signer/policy-root/admission roles;
- credential-free build isolation and content-addressed signer handoff;
- exact build claim and source/material/toolchain/environment identities;
- complete signed wire format and parser/signature semantics;
- concrete signer route, custody, rotation, suspension, and recovery;
- policy/checkpoint hashing, currentness, anti-freeze, revocation, time, and root
  compromise recovery;
- immutable verified-byte execution and same-inode mutation defense;
- exact consumer receipt bound to process/campaign/database/connection identity;
- atomic install, startup reconciliation, rollback, and owner-loss handling;
- no-secret controls for logs/temp/core dumps/errors and publication credentials.

No implementation may treat this ADR as an answer to those questions.

## Independence invariant

Workstation is accountable but may not collapse all trust roles into one untrusted
process or credential. In particular:

- build code cannot access signer, policy-root, publication, or admission credentials;
- AK cannot sign or publish the policy that authorizes itself;
- DSPx signer/policy cannot be reused outside its accepted scope by convenience;
- owner/currentness verification cannot depend on the AK DB being admitted;
- repository separation alone is not proof of compromise independence.

The later implementation ADR must define the actual principals and threat model.

## Gate sequence

```text
O1 Decision 148 owner selection (this ADR)
O2 workstation task 5306 Tier-1 implementation RFC/review/ADR
O3 post-ADR implementation and validation/rollback plans
O4 synthetic disposable implementation/proof
O5 independent supply-chain/bootstrap/rollback review
O6 separate authorization for remote workflow, signer enrollment, trust-pin install,
   publication, or real artifact production
O7 one independently verified real AK provenance bundle
O8 replacement Agent Kernel P0-C task against that exact bundle
```

No gate implies the next. P0-C remains blocked after O1.

## Owner transfer

Transferring ownership requires a new infra-root decision binding successor owner,
history/trust/revocation custody, consumer migration, overlap/freeze, rollback, and
owner-loss handling. Copying a key, workflow, policy file, or repository does not
transfer authority.

## Consequences

### Positive

- Agent Kernel no longer needs to invent or self-appoint a provenance owner.
- Workstation ownership aligns producer/admission operations with canonical-machine
  packaging and rollback.
- DSPx and provisioning boundaries remain intact.
- All difficult implementation questions remain visible behind a decision membrane.

### Costs

- The repository move remains blocked while workstation WIP and provenance
  implementation proceed.
- A real provenance bundle requires new supply-chain machinery and independent review.
- Single-machine-first scope must not be presented as a fleet-wide platform.

## Explicit non-actions

This ADR does not:

- implement a producer, signer, policy, launcher, or AK verifier;
- select or enroll a key/OIDC workload/transparency service/trust pin;
- authorize remote mutation, publication, deployment, or installed-binary change;
- make any reproducibility or provenance claim for a real artifact;
- mutate workstation active files, Agent Kernel schema/capability/DB, or DSPx;
- pass Agent Kernel P0-C;
- materialize or move `dspy-lm-auth`;
- push, release, or publish.

## Follow-up

When workstation WIP capacity permits and Decision 148 is unblocked, resume task 5306
for the separately reviewed implementation decision. Agent Kernel successor work may
restart only after that implementation produces and independently proves the exact
owner bundle required by P0-C.
