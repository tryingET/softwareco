---
summary: "Authority and constitutional review of Decision 77 recurring CTO RFC at commit 7f02483."
read_when:
  - "Revising or assessing the first Decision 77 RFC candidate."
type: "review"
status: "complete"
date: "2026-07-25"
decision_id: 77
reviewed_commit: "7f024832046f98c4c67beb95304f7a49aed7e27c"
review_outcome: "revise_rfc"
---

# Decision 77 authority review — attempt 1

## Identity

- Track: authority, constitutional legality, and owner federalism.
- Reviewed artifact: `docs/project/2026-07-25-softwareco-recurring-portfolio-cto-rfc.md`.
- Exact reviewed commit: `7f024832046f98c4c67beb95304f7a49aed7e27c`.
- Reviewer dispatch: `dispatch-1784988042987`.
- Method: strict adversarial, read-only.
- Outcome: `revise_rfc`.

The unrelated modification at `owned/docs/project/repo-capability-map.md` was excluded.

## Blocking findings

### A1 — Indefinite delegated office

The RFC creates a standing constitutional delegation with no hard expiry. Four-hour epochs limit current mutation but the appointed office survives indefinitely and can be reauthorized repeatedly. A 30-day review has no automatic suspension effect, so human silence preserves the office.

**Required correction:** make Decision 77 a durable framework while actual delegated authority exists only inside affirmative finite human-authorized epochs, or impose a hard mandate sunset. Between epochs the role is advisory and unappointed. A missed review must block new epochs.

### A2 — Incomplete epoch state machine

The epoch concern is only conceptual and omits the mandatory governance envelope, duplicate/conflict handling, exact lease relationship, handback, recovery, and claimant-transfer law.

**Required correction:** define exact authorization, activation, expiry, handback, stale-recovery, revocation, and terminal receipt contracts. Epoch duration is a hard non-renewable ceiling. Claimant replacement requires a new epoch/controller/authorization unless a separately reviewed equivalent protocol exists.

### A3 — Unresolved strategic-root projection

`SF3` is structurally active but retains exact Decision 74 terminal detail and a finite-mandate summary. The RFC hardcodes `SF3` without deciding how Decision 77 receives an exact direction projection while preserving receipt `8870`.

**Required correction:** adopt a distinct Decision-77 direction projection or successor strategic frame. Never infer authority from generic `SF3 state=active`, an arbitrary latest decision, or the Decision 74 terminal frame.

### A4 — Weaker owner federalism

The RFC does not restore exact owner-originated acceptance, objection, terminal-acceptance, return-to-owner, and release contracts. A controller-authored release could be inferred from owner task status.

**Required correction:** define exact concerns, accountable actors, evidence, applicability, blocking effects, vacancy boundary, and conflict resolution. Portfolio WIP is never freed solely from controller interpretation. A substantive owner objection blocks further control until lawfully resolved.

### A5 — Human reservations incomplete

The successor does not normatively carry all reserved powers: durable product/portfolio commitments; privacy, consent, ethics, licensing, and security exceptions; owner-accountability conflict; appointment/transfer; architecture acceptance; mandate-level redirect/stop/complete; and irreversible/public/release/external effects.

**Required correction:** add an operative stop-and-escalate section. Repeated ordinary waves cannot cumulatively bootstrap any reserved decision.

### A6 — Terminal, review, and supersession law incomplete

Decision-specific concerns lack complete schemas, transitions, actors, evidence, conflict handling, active-epoch invalidation, authoritative superseding-decision relation, and periodic-review consequences.

**Required correction:** define exact review, revocation, terminal, and supersession state machines. Revocation/terminal action invalidates every epoch immediately. Missing or adverse review blocks new epochs. Remove ambiguous terminal `continue` semantics from ordinary recurrence.

## Preserved facts

Decision 74, receipt `8870`, controller task `4182`, and terminal evidence remain immutable. Decision 77 is `review_pending`; task `4205` is governance-only.

## Legal next move

1. Do not accept Decision 77 or write an ADR.
2. Revise the RFC at a new immutable commit.
3. Rerun both required review tracks against that commit.
4. Attach both reviews and a controlling synthesis.
5. Proceed only if the latest synthesis says `ready_for_adr`.
