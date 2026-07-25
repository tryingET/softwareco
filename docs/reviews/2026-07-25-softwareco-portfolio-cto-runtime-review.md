---
summary: "Decision 74 Track B review of Pi runtime, operator UX, WIP, source-owner, and FCOS implementability."
read_when:
  - "Reviewing Decision 74 runtime and operator closure."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 74
review_track: "pi-runtime-operator-wip-fcos"
reviewed_commit: "bcce0340812163042f45876932141f4ce62de0c1"
review_outcome: "revise_rfc"
---

# Decision 74 review — Pi runtime, operator UX, WIP, and FCOS

## Reviewed artifact

- RFC: `docs/project/2026-07-25-softwareco-portfolio-cto-rfc.md`
- exact Softwareco commit: `bcce0340812163042f45876932141f4ce62de0c1`
- cited Pi Extensions revision: `891a8fd51e6ec004bce35f3c11d6a8d673ceec2e`
- FCOS authority revision: `b5efb2502608c6973ffabd3667f245bc1bbf342f`

## Determination

The direction is implementable without inventing authority and does not require a Softwareco-local Pi extension. The RFC correctly separates AK delegation, Pi prompt behavior, source-owner execution, and FCOS coordination.

Revision is required because the pinned Pi Modes revision does not immutably establish the required schema-v2/preset command surface, expiry readback depends on a projection, and WIP/controller admission lacks precise membership and serialization semantics.

## Must-fixes

1. **Pin an immutable Pi Modes dependency:** require a committed Pi Extensions owner revision or release that proves schema v2, presets, `/mode use`, JSON status/preview, and ancestor preset discovery. Run its linter/release gate and a fresh installed-artifact invocation. Do not create a local extension to bypass the owner dependency.
2. **Authority-owned expiry:** accepted AK decision/`SF3` state must carry exact `expires_at_utc`, decision identity, active delegation detail, revocation/supersession state, and terminal decision. Charter is consistency projection only. Missing, malformed, elapsed, or mismatched values leave the session advisory.
3. **Exact WIP membership/release:** define admission relation, coordinator references, owner acceptance evidence, counting states, distinct/duplicate/shared task handling, overhead exclusions, and capacity release. Portfolio pause/displacement never changes owner-task state. Use read → owner acceptance → fresh read → admission write → post-write readback; stop on ambiguity or limit breach.
4. **Truthful single controller:** require a human-designated controller identity, one Softwareco controller task, serialized admissions, recorded designation/attestation, and post-write readback. Describe this as procedural deployment invariant, not a deterministic lock.
5. **Bind `/cto` arguments and root invocation:** use `argument-hint: "<objective>"`, interpolate `$ARGUMENTS`, stop advisory when missing, and echo normalized objective/preflight result. Normative invocation begins at trusted Softwareco root until descendant prompt discovery is proved.

## FCOS clarification

The proposed owner handoff is aligned with FCOS: current items are coordination-only/non-claimable; source-owner execution remains external; real writes require exact `--task <id> --json`. Add that FCOS close evidence validation is not owner approval. A declined cross-repo handoff blocks the wave unless it is genuinely redesigned and reaccepted as single-owner.

## Material nice-to-haves

- Emit a compact preflight table with decision, `SF3`, expiry, cwd/trust, controller, objective, WIP, refs, and failures.
- Add negative cold-start tests for untrusted cwd, missing objective, expiry, inactive `SF3`, stale refs, WIP limit, and uncertain controller.
- Validate FCOS dry-run and real-write receipts separately.
- Record Pi mode hashes/provenance as diagnostics only.
- Report coordinator/FCOS task overhead even when excluded from the six-task limit.

## Open questions

Seven questions remain. Five are decision-blocking: committed Pi Modes revision, authority-owned expiry field, AK admission relation, counted task states/owner acceptance, and explicit human serialization. Two are implementation UX: descendant `/cto` support and whether paused/displaced waves continue counting until owner release/terminality.

## Outcome and legal next move

- review outcome: `revise_rfc`
- legal next move: revise and commit a new immutable RFC candidate resolving all must-fixes, then re-run Track B and controlling synthesis.
- prohibited next moves: FCOS write, `SF3` delegated activation, CTO representation, owner-task admission, local extension, or source-owner mutation from this candidate.

No files were mutated by the reviewer.
