---
summary: "Narrow RFC selecting infra/workstation as the accountable independent producer-policy owner for Agent Kernel build provenance while deferring signer and protocol implementation to a separate workstation decision."
read_when:
  - "Selecting ownership for Agent Kernel build provenance."
  - "Preparing the later workstation implementation decision or Agent Kernel P0-C restart."
type: "rfc"
status: "proposed"
as_of: "2026-09-01"
task_id: 5305
decision_id: 148
---

# RFC: owner selection for independent Agent Kernel build provenance

## Decision requested

Select the technical owner boundary only:

```text
softwareco/infra lane root
  owns cross-repo provenance owner-selection and future owner-transfer decisions

softwareco/infra/workstation
  becomes accountable owner for the independent Agent Kernel build-provenance
  producer-policy capability on the canonical workstation

softwareco/owned/agent-kernel
  remains a verification consumer and running-image measurer only

softwareco/owned/dspx
  remains a reference pattern only; no DSPx ownership or implementation is widened
```

“Accountable owner” means workstation must sponsor, design, implement, validate,
operate, revoke, recover, and document the producer-policy capability through its own
later accepted decision and tasks. It does not mean the current workstation repository
already contains that capability.

This RFC intentionally does **not** accept a DSSE schema, signer route, trust root,
policy chain, launcher design, transparency service, reproducibility claim, or live
rollout. Those are architecture-significant implementation choices and require a
separate workstation-owned RFC/review/ADR before Agent Kernel P0-C can pass.

## Trigger

Agent Kernel Decisions 146/147 require independently owned proof binding the exact
running AK executable bytes to exact source/build identity before a sensitive
successor-transition campaign can be admitted.

Agent Kernel P0 task 5304 found:

- running/mapped executable byte measurement is technically feasible;
- AK's embedded commit and unsigned installer manifest are self-derived diagnostics,
  not independent provenance;
- DSPx has a strong artifact-specific reference pattern but is not the AK owner;
- a bounded search did not establish an accepted generic Softwareco producer owner.

P0 therefore stopped and routed task 5305. Owner selection is necessary but not
sufficient to restart P0.

## Why workstation is selected

The infra capability map assigns:

- infra lane root: lane-level governance and cross-repo boundaries;
- workstation: canonical-machine runtime packaging, validation, hardening, rollback,
  promoted local control-plane surfaces, and operator runbooks.

Independent AK artifact admission is a workstation packaging/runtime membrane, not an
AK coordination fact. Workstation can own the producer-policy capability without AK
self-authorizing. Its single-machine-first contract also prevents premature invention
of a fleet-wide provenance platform.

Other candidates are less aligned:

- Agent Kernel self-ownership is circular for bootstrap trust.
- provisioning owns machine/package bootstrap, not artifact release/currentness.
- engineering-core owns guidance, not producer runtime truth.
- DSPx custody is explicitly scoped to DSPx artifacts.

## Owner contract

### Infra lane root responsibilities

- preserve the cross-repo owner map;
- record acceptance, supersession, or transfer of the provenance owner;
- require explicit consumer handoff and rollback boundaries;
- never become the signer or artifact producer by implication.

### Workstation responsibilities

Through a later accepted implementation decision, workstation must own:

- exact producer/build isolation contract;
- source/material/toolchain identity and claim semantics;
- artifact-attestation format and verification rules;
- signer/workload admission and credential custody;
- policy/checkpoint currentness and revocation;
- bootstrap trust-root installation, rotation, and compromise recovery;
- immutable verified-byte launch/admission;
- operator runbook, availability, incident handling, rollback, and evidence;
- synthetic proof before any real signer or remote effect;
- a separately gated handoff contract consumed by Agent Kernel.

### Agent Kernel responsibilities

After workstation implementation is accepted and proven, AK may own only:

- safe running/mapped executable measurement;
- verification of workstation-produced signed artifacts/policy/receipts against an
  externally supplied pin;
- binding verified provenance into a cooperative campaign;
- fail-stop/indeterminate handling when provenance becomes unavailable or mismatched.

AK must not:

- build or sign the artifact it trusts;
- mint signer/policy/trust-root authority;
- publish or revoke workstation policy;
- use embedded commit, caller hash, unsigned manifest, or AK DB self-report as
  bootstrap provenance.

### DSPx responsibilities

None are added. DSPx release custody may be studied as a pattern; no DSPx signer,
registry, policy, provider, file, or owner state is modified.

## Mandatory independence invariant for the next decision

Workstation accountability is not permission to collapse all trust roles into one
credential or process. The later implementation RFC must define separate compromise
and credential boundaries for at least:

```text
build producer execution
artifact-attestation signer workload
policy/checkpoint signer or approver
trust-root update authority
workstation admission/launcher operation
```

One repository may contain reviewed code for multiple roles, but the same untrusted
build execution must not hold signer, policy-root, publication, or admission
credentials. AK source/build code cannot mint the statement or policy that authorizes
itself.

The later decision must state its threat model for repository compromise, workflow
compromise, signer compromise, policy/root compromise, same-UID workstation
compromise, clock rollback, publication freeze/split-view, and owner loss. If the first
slice protects only a narrower single-machine threat model, its claims must say so.

## Required later implementation decision

Before workstation mutates implementation or signer state, create a workstation-owned
Tier-1 decision packet that resolves and independently reviews:

1. **Build claim:** provenance versus repeatability versus independent reproducibility;
   canonical source/material/recipe/toolchain/environment identities.
2. **Build isolation:** credential-free build execution and content-addressed handoff
   to a separate signer job after build code exits.
3. **Wire format:** exact DSSE/in-toto types, canonical bytes, duplicate handling,
   payload limits, digest domains, signature threshold, and parser behavior.
4. **Signer route:** one concrete first-slice signer/workload identity, OIDC/audience/
   lifetime if applicable, transparency requirements, custody, rotation, suspension,
   and recovery.
5. **Policy lifecycle:** non-self-referential policy hashing, immutable signer policy
   versus currentness state, contiguous generations, cumulative revocation, expiry,
   trusted time, anti-rollback, and compromise recovery.
6. **Availability/currentness:** head discovery, signed checkpoints, freshness lease,
   online/offline behavior, freeze/split-view defense, cache semantics, and outage
   recovery.
7. **Immutable execution:** sealed verified bytes such as a sealed executable memfd,
   fs-verity, or equivalently proven mechanism; same-inode mutation and crash windows.
8. **Consumer receipt:** exact binding between verified artifact/policy, process
   incarnation, mapped bytes, campaign nonce, DB generation, and AK connection.
9. **Atomic installation/rollback:** filesystem layout, fsync/rename order, startup
   reconciliation, rollback-eligible set under latest policy, and root/signer loss.
10. **No-secret boundary:** build code cannot access signer/publication/root credentials;
    logs/temp/core dumps/errors are bounded and synthetic canaries are tested.

The first-slice implementation remains exact to Agent Kernel on Linux x86-64 and the
canonical workstation unless the later review earns broader scope.

## Admission and execution gates

The owner-selection sequence is:

```text
O1 accept this owner decision
O2 create workstation implementation task and Tier-1 decision
O3 accept implementation ADR and post-ADR plan
O4 implement with synthetic keys/workloads and disposable artifacts
O5 independent supply-chain/bootstrap/rollback review
O6 separately authorize any remote workflow, signer enrollment, trust-pin install,
   publication, or real artifact production
O7 produce and independently verify one real AK provenance bundle
O8 restart Agent Kernel P0-C against the exact bundle
```

No gate implies the next. O1 alone does not make P0-C pass.

## Consumer handoff requirement

The later workstation implementation must publish a closed versioned handoff containing
only verified facts needed by AK, including exact artifact and policy identities,
verification result, freshness/currentness, signer/workload identity, process/launch
binding, and explicit non-authorizations.

AK must fail closed if the handoff is missing, stale, cached beyond its accepted lease,
unknown-version, signature-invalid, revoked, mismatched, or unavailable. The handoff
cannot authorize AK schema migration, repository transition, capability activation,
or consumer exclusion.

## Owner transfer and rollback

Transferring provenance ownership away from workstation requires a new infra-root
cross-repo decision that names:

- successor owner;
- exact policy/attestation history custody;
- trust-root and revocation continuity;
- consumer migration;
- overlap/freeze period;
- rollback and owner-loss handling.

No implementation may silently move trust authority through a copied key, workflow,
or repository.

Until the workstation capability exists, rollback is simply to preserve current AK
admission behavior and keep successor P0 blocked. After implementation, rollback and
incident behavior follow the separately accepted workstation decision; this RFC does
not pre-authorize them.

## Required evidence for closing this owner decision

- bounded source-owner search and P0 trigger;
- infra/workstation capability-map and AGENTS alignment;
- independent review that workstation is a legitimate accountable owner;
- independent review that the owner split avoids AK/DSPx authority absorption;
- explicit workstation implementation follow-up task;
- no-live-effect verification.

## Alternatives rejected

- **AK owns producer and verifier:** circular bootstrap authority.
- **DSPx becomes generic owner:** violates its artifact-specific custody.
- **Provisioning owns provenance:** confuses machine bootstrap with artifact trust.
- **No named owner; ad-hoc signed manifest:** leaves currentness/revocation/incident
  responsibility undefined.
- **Accept the full protocol in this owner decision:** hides unresolved security and
  operational choices under premature precision.
- **Create a universal service now:** unsupported by first-use evidence.

## Explicit non-actions

This RFC does not:

- implement producer, signer, policy, launcher, or AK verifier code;
- select/enroll a signer, key, OIDC workload, transparency service, or trust pin;
- claim a reproducible build;
- modify remote workflow, credentials, installed binary, system service, or policy;
- mutate workstation or Agent Kernel files outside this decision packet;
- mutate AK schema/capability/repository transition state;
- move `dspy-lm-auth`;
- change DSPx;
- push, publish, release, or deploy.

## Decision consequence

If accepted, infra/workstation becomes the accountable independent owner surface for
future Agent Kernel build-provenance production/policy on the canonical workstation.
The immediate next action is a separately scoped workstation Tier-1 implementation
decision. Agent Kernel P0-C and the `dspy-lm-auth` move remain blocked until that
implementation is accepted, built, and proven.
