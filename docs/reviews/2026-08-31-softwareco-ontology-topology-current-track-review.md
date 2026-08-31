---
summary: "Current-track review selects Decision 144 candidate C and finds the bounded architecture ready for ADR."
read_when:
  - "Reviewing or synthesizing Decision 144."
type: "review-memo"
status: "ready_for_adr"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5244
review_track: "current_track"
review_outcome: "ready_for_adr"
---

# Decision 144 current-track review

Reviewed artifact: [Decision 144 ontology topology RFC](../project/2026-08-31-softwareco-ontology-topology-rfc.md)

Registered identity:

- commit `d71750ab1b13f169f352f6b47fff916c7e28dd0f`;
- blob `06004e55467d61bf098933eebb537c59399a5558`;
- SHA-256 `98c79db2df614dae35aa64781717639c4373cc608328949c5c811cc0f9290c01`.

Outcome: **`ready_for_adr`**

Selected outcome: **C — true submodule with targeted materialization and relocated parent receipts**.

## Review conclusion

The RFC intentionally delegates candidate selection to governed review. Commit-bound consumer
census, C-vs-E experiments, unavailable-source/rollback trials, and corrected causal audit now
supply enough architecture evidence to choose C. The design is ready for ADR only with the exact
invariants below; its prototype is not adoption authority or completed implementation.

C is selected because it creates one native parent-to-owner OID binding, eliminates overlapping
source indexes, preserves the canonical ontology path used by ROCS locators, and needs less custom
state machinery than E. A true `.gitmodules` contract and exact ontology-only initializer are
mandatory. A metadata-less gitlink or generic recursive submodule operation is not C.

## Findings

### R1 — source ownership and binding

The owner repository at `07d4b8b89f6ca436618adb42827885e9a45289c7` remains the sole authored
ontology source. Parent adoption records that exact full OID as a mode-`160000` entry and records the
materialization source in `.gitmodules`. Parent receipts, plans, and docs do not become semantic or
source authority.

### R2 — targeted, atomic materialization

The current repository contains unrelated raw gitlinks without `.gitmodules`; generic
`git submodule update --init` failed in scratch. Post-ADR automation must initialize exactly
`ontology`, verify the expected OID and authorized publication, and fail atomically when source is
missing, unavailable, or mismatched. An uninitialized ontology must make root CI fail, not skip ROCS.

### R3 — receipt identity and physical membrane

A gitlink cannot contain parent-owned files. The six existing `ontology/dist/**` outputs must move to
a parent-owned path before the subtree is replaced. They must be regenerated with canonical parent
identity and all producer/consumer/path bindings migrated; copying scratch-bound receipt bytes is
invalid. Ordinary owner CI must leave relocated parent outputs unchanged.

### R4 — governed ownership-state transition

AK 5197 established the current map at `74cc0a59786d2450f172ee87a249f327a044ff07`.
Candidate adoption must narrow the broad `ontology/**` template classification and use a new exact
manifest, deterministic plan, applied state, external evidence, and final receipt. Directly editing
the established map hash or treating 31 dirty entries as an apply plan is forbidden.

### R5 — corrected aggregate-receipt claim

The earlier C-vs-E report's cross-owner-writer claim is rejected. Focused evidence proves owner CI
leaves the six downstream receipts unchanged; later consumer validations each update only their own
receipt pair. No ROCS-core aggregate-writer task follows from the false attribution. This correction
does not weaken the real local receipt collision or materialization requirements.

### R6 — candidate disposition

| Candidate | Review disposition |
|---|---|
| A complete projection | Reject: duplicates 37 unneeded paths and retains overlapping indexes. |
| B separate owner + projection | Reject: breaks canonical locator/AK/operator path without a mapping layer. |
| C true submodule | Select for ADR with R1–R9. |
| D guarded co-location | Reject: command-coverage membrane and fresh-materialization truth remain weak. |
| E selective projection | Retain only as rollback alternative; custom overlap/exclusion/materializer debt exceeds C. |

### R7 — no pre-ADR normalization

Current ontology owner HEAD, clean status, remote binding, and stash OIDs remain protected. The 31
canonical parent WIP entries remain unstaged. Scratch commits `016cf156...` and `aeea5616...` are
evidence only and must not be cherry-picked or replayed mechanically.

## Required ADR invariants

The ADR must carry all of these without dilution:

1. `.gitmodules` + exact mode-`160000` ontology owner OID; no raw gitlink.
2. Exact ontology-only atomic materializer; generic recursive initialization forbidden.
3. Missing/unavailable/mismatched source fails before activation with no partial metadata.
4. Six parent receipts relocated and regenerated under parent identity with complete consumer
   migration before old-path removal.
5. New post-AK-5197 ownership map/state plan and externally receipted transition.
6. Missing ontology manifest is a hard CI failure; strict root/infra/owned/contrib/fork resolution.
7. Owner ordinary CI leaves parent outputs unchanged.
8. Full pre/post bundle, owner ref/stash preservation, fresh checkout, and bounded forward/revert
   rollback proof.
9. Exact post-ADR owner/parent tasks; no staging of the existing 31 WIP entries beforehand.

If ADR drafting cannot preserve these controls, return to `revise_rfc` rather than weakening the
closure.

## Evidence limits and post-ADR work

`ready_for_adr` means the architecture is closed enough to commission implementation. It does not
claim that the atomic materializer, receipt relocation, ownership transition, or current-base
candidate exists. Those are required post-ADR tasks and must pass fresh-current-base review before
canonical adoption.

The unavailable GitHub/GitLab state must be re-read at execution time. Passing scratch gates does
not authorize network publication, root push, ontology stash mutation, or Healthco propagation.

## Recommendation to designated synthesis

Return `ready_for_adr` only if synthesis selects C and preserves R1–R9. Then record an accepted ADR,
implementation/validation artifacts, and exact post-ADR tasks. Otherwise return `revise_rfc`.
