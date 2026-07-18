---
summary: "Pilot-selection and authority packet for proving the Factory Flow Protocol through safe retirement of fcos-proving-lane."
read_when:
  - "Reviewing the first proposed Softwareco Factory Flow pilot."
  - "Preparing the Factory Flow RFC for a tracked review and ADR decision."
type: "evidence-and-selection"
status: "proposed_pre_adr"
as_of: "2026-07-18"
system4d:
  container:
    boundary: "Selection and pre-authorization design for one retirement pilot; no proving-lane mutation or retirement authority."
    edges:
      - "[Factory Flow RFC](2026-07-12-software-factory-operating-system-rfc.md)"
      - "[Operator packet](2026-07-18-factory-flow-pilot-operator-packet.md)"
  compass:
    driver: "Prove the factory protocol on a real, evidence-backed zombie-repository concern."
    outcome: "The estate no longer presents fcos-proving-lane as an active FCOS product while all unique evidence and dirty work are preserved or lawfully routed."
  engine:
    invariants:
      - "No destructive cleanup occurs before preservation, classification, review, and rollback proof."
      - "holdingco/fcos-control-board remains the native FCOS product owner."
      - "The CTO Agent is a bounded delegate, not the residual accountable human."
  fog:
    risks:
      - "Dirty work or historical evidence is lost during retirement."
      - "Retirement is mistaken for permission to mutate FCOS product authority."
      - "A self-referential process pilot proves paperwork rather than an operational outcome."
---

# Factory Flow pilot selection — safe retirement of `fcos-proving-lane`

## Status and non-authorization

This packet selects a **candidate pilot** and closes the RFC's missing problem/segment/risk/authority design questions. It does not authorize implementation, cleanup, archival, deletion, FCOS mutation, or AK direction activation. Those remain gated by tracked review, ADR, and post-ADR execution artifacts.

## Human direction and agent delegation

The current human operator explicitly selected:

- first pilot: safe retirement of the zombie `softwareco/owned/fcos-proving-lane` repository;
- company template correction: align Softwareco L2 templates with the accepted main-first policy;
- agent stewardship: appoint an agent in a CTO-like operating role.

The lawful interpretation under proposed Softwareco governance is:

| Role | Designation | Authority in this pilot |
|---|---|---|
| appointing and residual accountable authority | current higher-level human operator | grants/revokes delegation; accepts/rejects ADR; reserves irreversible retirement and final terminal decision |
| proposed post-ADR technical pilot steward | **Softwareco CTO Agent** | after human ADR acceptance: prepares evidence and options, coordinates bounded work, enforces accepted gates, may stop unsafe agent execution, and recommends terminal decision |
| source-owner executor | later AK assignee in `fcos-proving-lane` | executes only the post-ADR scoped task |
| FCOS product owner | `holdingco/fcos-control-board` owner surface | consulted only if retirement requires product-owner reference or compatibility changes |

Before ADR acceptance, `softwareco-cto-agent` acts only as the scoped assignee for AK task `#4028` under the operator's direct instruction to prepare the decision packet. The durable CTO-Agent delegation is proposed by Decision `#62` and becomes effective only if the human operator accepts its ADR. Decision `#62` is the canonical decision record; this packet is a supporting artifact, not the delegation source.

The CTO Agent may not appoint itself, accept the RFC/ADR, authorize destructive retirement, waive preservation, or become residual human accountability.

Proposed post-ADR delegation review/expiry:

- delegator and residual accountable authority: current higher-level human operator;
- scope: this pilot only;
- reserved decisions: ADR acceptance, irreversible retirement, physical deletion, and final terminal decision;
- review: at every terminal decision and before any destructive step;
- expiry: pilot terminal decision or human revocation, whichever comes first;
- revocation: immediate human operator instruction or evidence of authority drift;
- emergency stop: CTO Agent may stop automated mutation when preservation, scope, or owner boundaries are uncertain.

## Customer/internal-user evidence

### Segment

AI Society human operators and maintainers who must determine which repository owns FCOS and whether a repository is active, historical, or safe to change.

### Observed problem

The operator encountered both:

- `holdingco/fcos-control-board`; and
- `softwareco/owned/fcos-proving-lane`

and could not determine why both existed or which one was current. The proving lane's name, generic fleet updates, undated status material, and continuing task/engineering surfaces made a historical experiment appear operationally active.

### Current workaround

Operators must reconstruct history from repository contents, Git, capability maps, AK state, and memory. This is slow, error-prone, and does not survive session boundaries.

### Direct repository evidence

Read-only inspection on 2026-07-18 found:

- purpose: isolated Ring-0 FCOS canary and scorecard evidence;
- explicit non-goal: not a product/application and not policy authority;
- AK direction nodes: `0`;
- one ready generic adoption task: `#3455`, not an FCOS product direction;
- Git status entries: `48`;
- untracked paths: `5`;
- tracked files: `87`;
- source/test placeholders: one file each;
- widespread modified/deleted vendored ROCS and template-migration surfaces;
- historical FCOS scorecard evidence plus unrelated later evidence.

`holdingco/fcos-control-board` is the current native FCOS product owner. The proving lane therefore has historical value but no evidenced current product capability.

## Proposed outcome registration

| Field | Preregistered value |
|---|---|
| primary outcome | Operators can discover that `fcos-control-board` is the sole active FCOS product and that `fcos-proving-lane` is preserved historical evidence, without relying on private memory. |
| baseline | the initiating operator could not determine unaided why two FCOS-named repos existed or which was current; proving lane has 48 dirty status entries, no AK direction, one generic ready task, active-looking name/docs, and no explicit accepted retirement state |
| target | preservation manifest complete; every dirty/untracked path classified; unique evidence retained with hashes; misplaced work routed; active maps/scans no longer imply product activity; repository marked historical/retired through accepted owner surfaces; an independent cold-start operator identifies the native FCOS owner and proving-lane status without private coaching |
| horizon | one bounded implementation wave after ADR; no calendar promise overrides preservation safety |
| guardrails | zero unreviewed file loss; zero FCOS product-authority mutation; zero packet-only state changes; no physical deletion in the first pilot wave |
| evidence source | Git manifest/hashes, AK task/evidence, owner docs, capability/fleet projections, deterministic validation, and raw cold-start operator observation |
| discovery test | give an operator who did not author the packet only the AI Society root; record start/end timestamps, paths consulted, errors, escalation, and final owner/status answer |
| improved threshold | within 10 minutes, zero wrong-owner claims, zero unsafe mutation attempts, cites `fcos-control-board` owner evidence, and identifies `fcos-proving-lane` as preserved historical/non-product evidence |
| sampling | one pre-change observation is the initiating operator's recorded confusion; one independent post-change cold-start run is the minimum pilot test, with raw transcript/receipt retained |
| stop threshold | any unclassified dirty path, hash mismatch, unknown owner, failed restoration, or destructive step without tested recovery |
| redirect threshold | evidence shows unique active capability or a current owner dependency that requires continued canary operation |
| completion threshold | target evidence is satisfied and the human operator accepts the terminal decision |

## Risk tier

**R2 — shared/stateful evidence concern.**

The repository is not a production service, but its dirty worktree and historical evidence create shared lineage and data-loss risk. Required controls:

- immutable preservation manifest and patch/archive hashes;
- separate classification of historical FCOS evidence, template/ROCS migration, and misplaced work;
- restoration rehearsal into a disposable location;
- named human acceptance before retirement state or deletion;
- no physical repository deletion in the first pilot wave.

## Options considered

### A. Keep indefinitely as-is

Rejected: preserves ambiguity, zombie work, generic task pressure, and fleet noise.

### B. Merge into `fcos-control-board`

Rejected: there is no substantive product implementation to merge, and importing historical canary clutter would pollute the current owner.

### C. Delete or reset immediately

Rejected: the worktree is heavily dirty and includes untracked/historical/misplaced evidence. This risks irreversible loss.

### D. Safe evidence-preserving retirement — selected

Preserve and classify first; route unique facts; mark historical/retired; remove from active product/fleet interpretations; defer physical deletion to a later explicit decision.

## Capacity and WIP

- pilot review horizon: one post-ADR wave with an initial budget of four CTO-Agent execution hours and two 30-minute human decision gates; continuation beyond that budget requires an explicit `continue` decision;
- pilot constrained resource: human/CTO-Agent review attention for preservation and classification;
- available slots: one active retirement flow;
- total known competing load: proving-lane task `#3455` plus unrelated template modernization; both are deferred from the pilot and may not run concurrently on the same paths;
- exploration budget: zero during the preservation slice; new unknowns trigger `continue`/`redirect` rather than silent expansion;
- reserved maintenance/exception capacity: at most one urgent security or data-loss containment interrupt may pre-empt; it must be reconciled at the next review;
- displaced/deferred work:
  - broad Factory Flow template/schema propagation;
  - a second factory pilot;
  - physical repository deletion;
  - unrelated proving-lane template modernization;
- admission authority: human operator through the eventual accepted ADR and post-ADR task;
- causal constraint hypothesis: classification and owner-routing review, not file copying, limits safe retirement throughput;
- buffer signal: unclassified-path count; green at zero, warning at 1–5, stop above 5 or on any unknown owner;
- moved-constraint rule: after the unclassified count reaches zero, two consecutive blocked checks in restoration or owner acceptance shift the named constraint through an AK-recorded `continue` decision.

## Cross-repo boundary

The first wave should remain owner-repo execution plus Softwareco projection correction. Create an FCOS item only if multiple source owners require an active shared gate. Do not use FCOS merely because the repository name contains FCOS.

## Proposed terminal decisions

- `complete`: evidence safely preserved, repository made unambiguously historical/retired, and no active dependency remains;
- `redirect`: a real active dependency requires a narrower canary/consumer contract;
- `stop`: preservation or authority cannot be established safely;
- `continue`: another bounded evidence/classification slice is required.

The CTO Agent recommends; the human operator controls the final terminal decision.
