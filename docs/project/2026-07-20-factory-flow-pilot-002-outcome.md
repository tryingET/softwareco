---
summary: "Redirected Factory Flow pilot 002 outcome: protocol and cold-start truthfulness passed, but canonical issue #30/cursor reconciliation blocks review readiness."
read_when:
  - "Choosing the terminal action for Factory Flow pilot 002."
  - "Reviewing whether the issue-tracker canary justifies broader template propagation."
type: "pilot-outcome"
status: "redirected"
as_of: "2026-07-20T18:41:25Z"
decision_id: 68
pilot_id: "SOFTWARECO-FACTORY-PILOT-002"
terminal_decision: "redirect"
terminal_evidence_id: 4981
---

# Factory Flow pilot 002 — redirected outcome

## Verdicts

| Verdict | Result | Basis |
|---|---|---|
| governance/template ordering | **pass** | Decision 68 activated bounded governance and L1 template contracts before the canary |
| main-first source policy | **pass after correction** | stale MR-only exception removed; issue-tracker `main=518ab43`; Softwareco pointer commit `3456898` |
| projection/authored-input coherence | **pass** | default manifests, file references, 40 canonical body hashes, and byte-idempotent AK export validate |
| default external-effect safety | **pass** | observation-only runner; apply/rebuild disabled; systemd dry-run; no external or canonical mutation in tests |
| independent cold-start truthfulness | **pass** | correct authority and blocked classification in 48 seconds; zero errors, wrong-authority claims, unsafe effects, or manual repair |
| review-ready operator outcome | **blocked / not achieved** | candidate index 0 is already GitHub issue `#30` with status `submitted`, while canonical sequence cursor remains at zero |
| broad template propagation | **not yet justified** | two pilots establish shared invariants, but pilot 002 has not completed a reconciled review-ready loop |

## Step 1 — direction reconciliation

The stale active wave text incorrectly described an MR-only canary and used malformed key `IW-SF2-ISSUE-TRACKER-CANARY`, producing a duplicate display identity `AK.V5.SF02.WW02`.

Reconciliation performed:

- replaced MR-only meaning with main-first canary truth;
- preserved the malformed wave as done with `state_detail=superseded_by_IW3_key_normalization`;
- created canonical successor `IW3`, displayed uniquely as `AK.V5.SF02.WW03`;
- linked completed Softwareco integration task `#4094`, active closeout task `#4096`, and Decision 68;
- `ak direction check` passes.

The accountable human selected `redirect`; `IW3` is archived during terminal reconciliation and a separately bounded successor slice owns any design/review follow-up.

## Step 2 — independent cold-start

Clean scout: `scoutpeer-mrtk5n7j-b8934ad1`.

Tracked receipt: `docs/project/2026-07-20-factory-flow-pilot-002-cold-start-receipt.md`.

- start: `2026-07-20T18:28:46Z`;
- end: `2026-07-20T18:29:34Z`;
- elapsed: 48 seconds;
- command/validation errors: 0;
- manual repair steps: 0;
- incorrect readiness claims: 0;
- wrong-authority claims: 0;
- external effects: 0;
- canonical AK mutations: 0;
- confidence: 97/100.

The scout correctly distinguished three facts:

1. projection/manifests/authored bodies are coherent;
2. sequence cursor and existing issue identity are not reconciled;
3. neither validation success nor `halted=false` authorizes advancement.

## Step 3 — learning and comparative evidence

Crystallized learning: `docs/learnings/2026-07-20-factory-flow-pilot-002.md`.

Across pilots 001 and 002, the supported general invariants are:

- owner-native canonical truth wins;
- projections do not become authority;
- bounded mutation follows broad/adversarial reasoning;
- independent cold-start evidence is required;
- validation/conformance remains separate from outcome/readiness;
- residual human authority controls irreversible, external, and terminal actions.

Pilot-specific details must not propagate as universal template requirements: issue-tracker commands, GitHub sequence schemas, repository identity, observation-only implementation, or a hard-coded CTO identity.

## Operational blocker

The next documented action is:

> reconcile/dedupe canonical issue #30 (status=submitted) through a separately authorized procedure.

No reviewed executable procedure currently exists in the operator docs, and AK evidence assertions do not authenticate non-replayable human consent. The canary therefore stops rather than improvising an import, sequence advancement, GitHub query, or external mutation.

## Human terminal decision

At `2026-07-20T18:41:25Z`, the accountable human explicitly selected:

> **Redirect — design and review a bounded reconciliation/dedupe path for issue #30, then rerun the cold start.**

AK evidence `#4981` is controlling. The authorization covers only the follow-on design/review slice. It does **not** authorize AK issue/cursor mutation, GitHub mutation, external effects, or template propagation.

## Step 5 — propagation gate result

Because the terminal action is `redirect`, not `complete`, broader L2/L0 propagation is **not authorized**. The comparative invariants remain candidate evidence only. A future propagation attempt requires both:

1. a reconciled review-ready follow-on outcome; and
2. a separate accepted template-owner decision.

The immediate successor is a bounded design/review slice for issue `#30`, followed by another independent cold-start test before any renewed terminal or propagation decision.
