---
summary: "Designated synthesis for Decision 144 selecting true-submodule candidate C and controlling ready-for-ADR closure."
read_when:
  - "Closing Decision 144 governed review or preparing its ADR."
type: "review-synthesis"
status: "ready_for_adr"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5246
review_outcome: "ready_for_adr"
cited_input_attempt_ids:
  - 592
---

# Decision 144 designated review synthesis

Reviewed artifact: [Softwareco ontology topology RFC](../project/2026-08-31-softwareco-ontology-topology-rfc.md)

Registered identity:

- commit `d71750ab1b13f169f352f6b47fff916c7e28dd0f`;
- blob `06004e55467d61bf098933eebb537c59399a5558`;
- SHA-256 `98c79db2df614dae35aa64781717639c4373cc608328949c5c811cc0f9290c01`.

Controlling outcome: **`ready_for_adr`**

Selected RFC outcome: **C — a true submodule with targeted atomic materialization and relocated
parent receipts**.

## Synthesis authority and evidence

Decision 144 uses `multi_lane_requires_synthesis`; its active profile names a designated
synthesizer and makes synthesis control ADR legality. This artifact synthesizes:

- the deterministic review-set plan at
  `../project/2026-08-31-softwareco-ontology-topology-review-set-plan.md`;
- the original problem, evidence, RFC, and validation packet committed at `d71750ab` under AK
  `5228` / evidence `8005`;
- the superseding candidate-C evidence at
  `../project/2026-08-31-softwareco-ontology-topology-candidate-c-evidence.md`;
- current-track review attempt **592**, artifact
  `2026-08-31-softwareco-ontology-topology-current-track-review.md`, outcome
  `ready_for_adr`;
- C-vs-E scratch artifact
  `/home/tryinget/.local/state/pi-quests/evidence/decision144-c-vs-e-20260831T063519Z`, whose
  manifest-file SHA-256 is
  `5216f88bb26188cb7a5b6e24b1ba547cf5cad341a74744c6cfb5cab9e8d90b11`;
- corrected causal artifact
  `/home/tryinget/.local/state/pi-quests/evidence/decision144-owner-ci-causality-20260831T142438Z`,
  manifest-file SHA-256
  `056444d49e68d8f407de8f441bdffde39d49e4ec77f45126e42eb576924e4953`, recorded as AK evidence
  `8040`;
- current-track evidence `8044`, candidate C `016cf156e15fdd88675f47bed05ea670bb44c444`,
  candidate E `aeea561621185366290f831c74fdf52cde7f5fa8`, established AK-5197 finalization
  `74cc0a59786d2450f172ee87a249f327a044ff07`, ontology owner
  `07d4b8b89f6ca436618adb42827885e9a45289c7`, and preserved stash
  `c66f2e06151acfcc0eb4bc4f26581c2f25d3ffa3`.

The exact RFC blob is unchanged. The required current track is covered and aligned. No conflicting
current review outcome exists. The RFC explicitly delegates candidate selection to governed review,
so selecting C does not require an RFC revision when every RFC invariant and measurement gate is
preserved.

This file does not itself close AK review state. Legal closure exists only after the owning AK
workflow attaches this exact committed artifact as `review_synthesis`. Even then,
`ready_for_adr` is not an accepted ADR, implementation, ontology mutation, receipt migration,
ownership-state transition, materialization, publication, or lifecycle completion.

## Why C controls

### One native source binding

C replaces overlapping ordinary-tree ownership with one parent mode-`160000` pointer at a full
ontology-owner OID plus a true `.gitmodules` source contract. It preserves the canonical
`softwareco/ontology` locator used by ROCS while eliminating parent and owner indexes over the same
source files. A metadata-less raw gitlink is not C and is rejected.

### Measured materialization behavior

Scratch evidence proved that exact ontology-only initialization succeeds at owner OID `07d4b8b`,
strict ROCS resolution passes for root, infra, owned, contrib, and fork, owner full CI passes, and a
bounded revert restores the exact parent tree. The current missing-manifest conditional silently
skips ROCS and exits zero when the submodule is absent; the proposed guard fails non-zero. Generic
recursive initialization fails because unrelated raw gitlinks have no `.gitmodules` mapping.
Therefore C requires an exact, atomic `ontology` materializer and a hard missing-manifest gate.

### Lower shadow-contract debt than E

Static census shows only eight ontology semantic paths plus the parent `.gitkeep` marker are parent
consumers; the other 37 owner paths do not justify a complete projection. E can project those nine
paths, but it retains overlapping indexes and introduces a second versioned selection API, ignore
contract, excluded-drift checker, and custom nested-Git activation. Its first unavailable-source
prototype left partial `.git` metadata. C uses Git's native OID relation and fewer custom authority
surfaces. E remains a bounded rollback alternative, not the selected architecture.

### Corrected causal record

The first C-vs-E report incorrectly attributed six downstream receipt changes to ontology-owner CI.
The command chronology ran owner CI before separate consumer validations and captured parent status
after those validations. Focused evidence `8040` proved:

- owner-only strict CI exits zero;
- the parent remains clean immediately afterward;
- all six downstream receipt hashes remain byte-identical;
- contrib, fork, and infra validation each update only their own two receipt files.

The cross-owner aggregate-writer claim is therefore falsified and superseded. No ROCS-core writer
change is a Decision-144 prerequisite. This correction does not weaken the real local collision:
parent-owned receipts cannot remain beneath a source-owner submodule.

## Required ADR invariants

The ADR may select C only if it preserves **R1–R9** without dilution. If ADR drafting cannot preserve
them, return to `revise_rfc` rather than weakening review closure.

### R1 — true Git source binding

The parent records a true `.gitmodules` entry and mode-`160000` `ontology` pointer at an exact,
full, live-published ontology-owner OID. Metadata-less gitlinks, copied source trees, and ambient
nested `.git` state are forbidden as the canonical relation.

### R2 — targeted atomic materialization

All automation initializes exactly `ontology`; generic recursive submodule initialization remains
forbidden while unrelated raw gitlinks are unmapped. Materialization verifies expected OID and
authorized publication before activation. Missing, unavailable, mismatched, or interrupted source
leaves no partial Git metadata, changed parent index, activated wrong OID, or receipt mutation.

### R3 — fail-closed gate truth

An uninitialized or missing `../../ontology/manifest.yaml` is a hard root-CI failure, never a skip. Fresh
checkout and unavailable-source tests must exercise that failure before canonical adoption. Strict
root, infra, owned, contrib, fork, and owner gates remain required.

### R4 — parent receipt relocation and identity

All six parent-owned `ontology/dist/**` files move outside the submodule path before the ordinary
subtree is replaced. They are regenerated under canonical Softwareco-parent identity; scratch-bound
or owner-root-bound bytes cannot be copied as authority. Every producer, consumer, path, repo
binding, artifact reference, and rollback path migrates before old-path deletion. Ordinary ontology
owner CI must leave relocated parent outputs unchanged.

### R5 — new post-AK-5197 ownership transition

AK `5197` established the current ownership map at `74cc0a5`. C adoption narrows the broad
`ontology/**` template classification through a new exact manifest, deterministic plan, applied
state, external evidence, and final receipt. Inline map-hash editing and reinterpretation of the
existing established state are forbidden.

### R6 — physical owner membrane

The ontology repository remains sole authored semantic/source owner. Parent `.gitmodules`, gitlink,
materializer, plans, receipts, docs, and tests do not become semantic or Git-source authority. Owner
HEAD, refs, remote binding, clean status, and stashes are preserved through adoption.

### R7 — bounded rollback

Pre/post full-ref bundles and exact artifact hashes are mandatory. Rollback is a bounded parent
forward/revert operation plus exact owner rematerialization; it never rewrites owner refs, pops or
drops stashes, restores canonical AK from stale files, or uses the scratch candidate as authority.
E may be reconsidered only through a new reviewed decision revision if C cannot satisfy atomic
materialization.

### R8 — no pre-ADR normalization

The current 31 ontology WIP entries are evidence only. They remain unstaged and uncommitted until
accepted ADR, current continuation artifacts, and exact post-ADR owner/parent tasks authorize the
migration. Scratch commits `016cf156...` and `aeea5616...` must not be cherry-picked or replayed
mechanically.

### R9 — owner-decomposed implementation

Post-ADR work separates at least: targeted materializer and fail-closed CI; receipt
identity/consumer migration; ownership-map/state plan+receipt transition; exact C adoption and fresh
checkout proof; and independent final review. Each task stages only its declared paths and excludes
unrelated issue-tracker or other owner WIP. Passing scratch or local gates is not rollout,
publication, or lifecycle authority.

## Candidate disposition

| Candidate | Controlling disposition |
|---|---|
| A — complete projection | Rejected: duplicates 37 unneeded paths and retains overlapping indexes. |
| B — separate owner plus projection | Rejected: breaks canonical locator, AK, and operator path contracts without a governed mapping layer. |
| C — true submodule | **Selected for ADR**, subject to R1–R9. |
| D — guarded co-location | Rejected: command-coverage and fresh-materialization boundaries remain weaker than physical Git separation. |
| E — selective projection | Retained only as rollback alternative; custom overlap, selection API, checker, and activation debt exceed C. |

## Evidence limits and legal next move

The prototype is feasibility evidence, not production code. Atomic materializer, receipt generator
and migration, ownership-state transition, CI changes, and fresh-current-base adoption remain
post-ADR deliverables. Their absence is not an unresolved candidate choice because R1–R9 close the
architecture and define fail-closed implementation acceptance.

Attach this exact committed synthesis to Decision 144 with outcome `ready_for_adr`, citing current
track attempt **592**. Re-run the passport and advance only when AK reports legal closure
`ready_for_adr`.

Then an explicit accountable-owner decision may accept or reject the direction. If accepted, record
an ADR carrying R1–R9 plus current implementation and validation/rollout/rollback artifacts before
creating or executing ontology tasks. No transition authorizes issue-tracker publication, root
push, Healthco propagation, or mutation of unrelated committed lineage such as
`b5db90079cc2f08928086a79d58308efa421a206`.

## Claim limit

This synthesis controls only governed review outcome for the exact registered RFC. It does not:

- accept or record an ADR;
- implement or activate candidate C;
- authorize staging the canonical ontology WIP;
- relocate or regenerate receipts;
- change ownership state or template classification;
- mutate ontology refs, stashes, remotes, or the issue-tracker pointer;
- authorize push, publication, Healthco work, or lifecycle completion.
