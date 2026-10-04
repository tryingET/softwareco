---
summary: "D173 staged verification, receiver validation, rollout stops and phase-specific rollback; no runtime pass asserted."
read_when:
  - "Admitting a successor experiment or checking evidence before Principal birth/activation."
type: "reference"
decision_id: 173
task_id: 6662
as_of: "2026-10-04"
---
# D173 — verification, validation, rollout and rollback

Direction: [conditional ADR](../../../decisions/2026-10-04-principal-policy-settlement.md).
Decomposition: [implementation plan](implementation-plan.md).
Normative obligation map: [V01–V09 appendix](../contracts-r3.md#clause-verification).
Attach this plan only after native ADR recording. No proposed command below grants
permission, and no later-stage check is reported as run by writing this plan.

## Evidence contract

Each successor binds exact requirement/DoD row, issuer capacity, acting subject,
intended subject where relevant, current authority, task/claim, source/profile/input
hashes, version/fence/attempt correlation, command or boundary observation, expected
and actual result, exit status, receiver and disposition. Verification checks the
requirement/DoD row; the actual receiver judges fitness for purpose. Synthetic
construction, document integrity, real boundary qualification and receiver acceptance
are distinct evidence classes. Unknown execution/effects remain unknown, never a pass.

## Measuring points and owner stop conditions

| Stage | Required real checks / evidence | Refusal / stop / escape |
| --- | --- | --- |
| L0 lifecycle recording | unchanged RFC/appendix hashes; tracked memo; current required track covered; real owner answer/receipt; accepted outcome; tracked ADR/plans; explicit task verdicts; fresh passport | stop if subject drift, contrary current owner fact, missing closure, untracked custody or new pending execution link; do not bypass native guards |
| L1 authority/identity | V01–V04: issuer/actor/role/appointment/session distinctions, current admission/refusal, routine/reserved classification, continuity, permission expiry versus review date/lease | denied/unavailable/conflicting blocks dependent act; owner objection is not vacancy; due review alone is not invented expiry |
| L2 source/route/placement | V06–V07: actual two-stage pinned-L0 render, exact source/pin/answers adoption, lineage/refresh readers, installed discovery/lint, collisions and AGENTS/CLAUDE loader preflight | wrong pin, generated-only fix, source-only discovery, unadmitted path/route B or collision fails; preserve existing legacy/agent-owned bytes |
| L3 parent right/custody | V05: two distinct permits and aliases race on same canonical E; lost receipt/partial/cleanup/reissue; revocation; original-T recovery; fresh O3 versus O6-only replacement; independent start/write observations | at most one start, receipt before writes, held right blocks all siblings; absent receipt never defaults to unused; no fence/remaining-step proof means no recovery |
| L4 inert result | native render/provenance/content checks and designated receiver acceptance, exact correlated E/P/T/source/fence history | artifact existence alone fails; partial/unknown state retained inert; acceptance is not appointment or host activation |
| L5 host M0 | V09: actual frozen-resource confinement denial, provider egress, real cognition/choice/result, commit-before-first-render and disposition-commit-before-export crash cuts, custody/fenced takeover, accepted/rejected export | allowlist/types/reducer/summary/fixture flags alone fail; no complete-M0 claim until all duties and receiver result-or-blocker pass; no live XENO |
| L6 memory | V08: admitted control/candidate, correction/exception/supersession recall, denial canaries and metadata, filter-before-retrieval/release, derivative withdrawal and stale-reingestion denial | useful compression cannot waive disclosure/retention; no upstream reuse without permission; KES remains separately admitted; fail closed on missing profile |
| L7 active operation | current appointment/all active profiles; useful results, commitment custody and reserved-effect permissions under actual service/owner observations | revoke/hold affected admission; continue only unaffected admitted work; cancellation is not physical acknowledgment or rollback |

The retained 44 cases are author-created synthetic construction diagnostics, not
native scenarios. The inspection found G01 second-contender-count and G10 composite-
guard completeness gaps in the retained checker; its separate supplemental probes
reject malformed copies. Successors must close those real boundary test obligations,
not cite fixture counts as enforcement proof. Historical checker/fixtures stay frozen.

## Lifecycle document checks

From the workspace root, verify preserved manifests and exact bytes:

```sh
sha256sum -c softwareco/docs/project/principal-policy-resolution-2026-10-04/OUTPUTS-R3.sha256
sha256sum -c softwareco/docs/project/principal-policy-resolution-2026-10-04/inspection-01a106ff/OUTPUTS-INSPECTION.sha256
node core/agent-scripts/scripts/docs-list.mjs --docs softwareco/docs/project/principal-policy-resolution-2026-10-04 --strict --json
node core/agent-scripts/scripts/docs-ref-check.mjs --repo-root softwareco --path softwareco/docs/project/principal-policy-resolution-2026-10-04 --path softwareco/docs/decisions/2026-10-04-principal-policy-settlement.md --require-tracked --json
ak decision passport 173 -F json
```

Use ordinary repo smoke/pre-commit checks and scoped whitespace/budget checks.
The stored unapplied `.patch` has a single-space blank context line that `git diff
--check` reports as trailing whitespace when adding the patch file itself; preserve
its bound bytes and verify it with `git apply --check`, excluding only that patch
from ordinary document whitespace checking. This is not an operative-text exception.

UBS reporting no supported language on Markdown/JSON is **nothing scanned**, not a
security or implementation pass. The company full gate includes ROCS cleanup/build
that writes existing dirty ontology outputs. Do not erase or regenerate unrelated
owner changes to obtain a green lifecycle check. Full source/runtime gate evidence
belongs to separately scoped successor work before merge/adoption; targeted docs
checks cannot substitute for that contract.

## Rollout sequence

1. Record and verify the actual conditional policy ADR and plan/reevaluation chain.
2. Resolve and qualify actual owner/reference/source/route/custody/placement slices.
3. Issue the actual O3 right and exact O6 permit only after those native boundaries
   qualify; perform one separately admitted inert birth and receiver acceptance.
4. Admit and qualify each bounded host/M0 or memory experiment independently.
5. Admit actual appointment/active profiles and corresponding service/effect rights;
   expand only on real evidence, current permission and receiver validation.

No fixed speed figure, automatic global copy retirement, default language selection,
unbounded worker/process lifetime or permission expansion is invented. Receiver-
agreed finite fixture/capacity/failure/retention figures are successor inputs.

## Phase-specific rollback and recovery

| Phase | Authorized response | What is not undone |
| --- | --- | --- |
| Policy before execution | actual owner may suspend/revise/supersede policy through the native lifecycle; preserve ADR/history | acceptance history and separate owner records are not erased by editing prose |
| Source/adoption before birth | isolated owner-authorized revert/repin with lineage and consumers rechecked | another owner's source/adoption decisions cannot be silently reset |
| Start/partial/unknown birth | hold/revoke admissions, preserve parent/start/effect facts, fence, reconcile or quarantine under actual owner scope | source/directory rollback does not unspend E; cleanup never renews it |
| Same-attempt recovery | prove original E/P/T, fresh recovery permission, unchanged bindings, prior-executor fence and remaining step | adds zero starts; blind rerender with the same label is not recovery |
| Replacement attempt | fresh applicable O3 act issues distinct E2 and explicit old disposition, plus all collision/fence/source/effect guards | O6 reissue or a new string cannot renew E |
| Complete inert artifact | admitted repair/revision, retain provenance and accepted original result; keep inactive if profiles fail | no automatic rebirth, appointment or activation |
| Active host/data/effects | block future admissions under owner terms, retain uncertain commitments/effects and run qualified service/custody/data recovery | repo rollback cannot undo runtime state, provider disclosure or physical effects |

Deletion of unknown/possibly live state is forbidden. Retention/disposal needs actual
owner authority and evidence; a cache clear is not withdrawal/deletion of originals.

## Later closure

`unblocked` is the terminal normal state of the current native decision machine,
not proof of implementation or a `closed` rollout. Each admitted successor closes
against its own DoD and receiver evidence. Record surprising/reusable findings through
KES after actual work; Oracle/DSPx may analyze accumulated evidence later without
owning acceptance or activation. This lifecycle slice does not fabricate KES learning
closure or empirically proven rollout success.
