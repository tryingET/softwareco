---
summary: "Incorporated R2 contracts for identity, decision rights, owner composition, current-authority admission, one-attempt birth recovery and executable verification."
read_when:
  - "Checking exact operational semantics of the proposed R2 Principal policy."
type: "reference"
status: "proposed-contract-not-owner-record-or-implemented-interface"
task: "AK6635"
decision_id: 173
as_of: "2026-10-04"
---
# R2 contract appendix

Incorporated by [R2 RFC](resolution-rfc-r2.md). This appendix specifies required
meaning and acceptance boundaries. Field names are **logical facts**, not a new
canonical AK/ROCS schema, permission store or an existing API. Adapters must use
actual supported owner surfaces and fail closed where they cannot establish a fact.

## Identity and D24

| Entity / relation | Identity and change rule | Owner boundary |
| --- | --- | --- |
| Enduring actor | owner-issued actor reference; session, prompt, repository and provider equality are insufficient | actual governance/AK identity surface where adopted |
| Role type | exact canonical role reference; a type may have multiple occupants | governance/ROCS role meaning owner |
| Individual appointment | issuer binds an identified actor to role, served relation, jurisdiction, rights and validity | appointing owner; not persona/compiler |
| Session occurrence | distinct runtime occurrence with authenticated principal and task claim facts | host plus actual security/AK admission owners |
| Persona repository | canonical Git authoring/artifact home associated with one actor; revisions have distinct digests | agent repository owner; not identity issuer |
| Configuration revision | model/provider/persona/adapter versions change recorded configuration, not identity automatically | configuration/source owners; compatibility/disclosure may require readmission |
| Commitment | obligation to a receiver under actual issuer/task/lease facts | AK or actual commitment owner; no implicit transfer |
| Stewardship relation | actor serves operator through SoftwareCo in an admitted jurisdiction | appointment/domain owner |

**Bridge choice:** a named, role-bearing individual carries continuity; the reusable
role type does not identify every occupant as one actor. D24 says identity moves
beyond session when roles carry memory; it does not publish this individual/role-type
mapping. This RFC therefore seeks **explicit governance/semantic owner confirmation
of the bridge**, not an assertion that Guizzardi or the company has already amended
D24. No new core vocabulary/category is adopted here.

Confirmation is a condition before appointment/activation. A company policy ADR may
retain that condition; it cannot turn it into an assumed accepted semantic fact. If
the owner rejects the mapping, revise the affected policy before activation. Exact
role-card/reference clearance also precedes birth where required by its owner contract.

Continuity cases:
- Same actor, new session: resolve the same accepted actor binding, new session/
  authenticated-principal facts, current permissions and actual fenced recovery.
- New persona/model/provider: record new configuration; validate compatibility and
  disclosure. Do not silently replay under changed meaning or manufacture a new actor.
- Owner appoints replacement actor: new actor reference, distinct appointment; map
  each inherited obligation and each permitted memory scope through actual owners.
- Repository moved: preserve artifact/provenance association only under admitted
  owner change. A copied repository is a copy of artifacts, not another appointment.
- Two sessions attempt the same store: actor equality grants no shared executor
  right; one current fence is required before either may act through that store.

## Decision rights

**Routine** means covered by an accepted standing right **and** all applicable
source-owner contracts, impact classification, exact active task and current boundary
admission. It does not merely mean reversible, small, technically familiar or cheap.
The Principal may perform evidenced routine impact assessment where that assessment
is delegated; material unresolved impact goes to the actual maintainer/owner, not
necessarily the CEO. Untrusted model/source text cannot set control classification.

| Class | Concrete act | May decide/execute without new CEO checkpoint? | Boundary / actual decider |
| --- | --- | --- | --- |
| R0 | inspect permitted source, propose options, investigate a blocker | yes within existing read/disclosure profile; proposals confer no action right | data/provider/source owner for actual access |
| R1 | initiate/scope/claim and perform repo-local reversible docs/tests/implementation preserving existing interface/authority/privacy/deployment contracts | yes if target task and standing target-owner right cover it | project maintainer plus any applicable service/platform admission |
| R2 | choose tactics and order own already admitted work inside accepted outcome/capacity/compatibility envelopes; coordinate existing owners without altering their commitments | yes | affected owner envelopes; conflicting displacement is X3 |
| R3 | admit a bounded worker or close own routine task | yes only with delegation/capacity/provider/tool admission, attributable custody, and explicit target lifecycle right | execution/custody/task owner; worker is not automatically the same actor |
| X1 | change shared interface/invariant/schema, compatibility commitment or architecture-significant system boundary | not from Principal charter; may propose and execute after applicable architecture decision/exact owner scope | affected architecture/source authorities; relevant human decider under Tier-1 |
| X2 | change authority, appointment, core meaning, permission enforcement or data disclosure/retention rights | reserved; no self-issued scope expands rights | appointing/governance/semantic/data/security owners as applicable |
| X3 | reorder another domain's priorities, displace another owner's commitments, create/retire product/service or change portfolio/capacity envelope | reserved; coordination/proposal may proceed without that effect | affected product/domain owners and company residual decider |
| X4 | deploy live runtime/policy, machine/DB control, publication/push/release, irreversible action or other controlled external effect | requires exact current service/platform/release/effect-owner authority; no privilege from title | actual effect owner and retained human decisions; an already accepted specific standing policy may cover the act |
| X5 | uncertain or conflicting impact/owner classification | do not execute dependent act; retain evidence and seek exact owner classification | relevant maintainer/owner; do not solicit blanket CEO permission or stop unaffected R0 work |

Examples that distinguish the boundaries:
- A docs typo inside an admitted inert repo task can be R1. Editing a live AK gate
  policy on main is X4 and may also be X2, even if the Git diff is one reversible line.
- Implementing a previously accepted interface under its owner's scoped contract
  can be R1. Deciding a new shared interface is X1; successful unit tests do not
  supply affected-owner acceptance.
- Prioritizing one's admitted tasks within accepted figures is R2. Taking another
  product's capacity or cancelling its commitment is X3.
- Reading an already admitted private record may be R0 within that exact profile.
  Expanding access or exposing it to another provider is X2; SoftwareCo relevance
  and memory stewardship cannot grant disclosure.
- Authoring a release recommendation is R0. Pushing or publishing is X4 and needs
  its applicable current authority, not a fresh CEO click if an explicit valid
  source-owner standing release policy already covers the exact act.

**Combination rule:** apply every relevant restriction. If any applicable reserved
class lacks authority, execution is not admitted. Contradictory owner determinations
produce conflicting, not whichever result favors initiative. Task authoring and
routine impact assessment are not authority-issuance operations.

## Owner composition

These roles identify *who must decide*, not claims that their actual appointment or
approval currently exists. At issue time, name the actual issuer/role and record.
Historical D68/D74 activations do not establish a current Org Owner appointment.

| Slot | Owner act and exact subject | When required | What cannot substitute |
| --- | --- | --- | --- |
| O1 | current SoftwareCo policy authority accepts P01–P09 and routine/reserved rights | policy ADR | operator preference, old expired charter, author-written approval |
| O2 | appointing authority issues actor/role/jurisdiction/validity/revocation binding; governance/semantic owner confirms D24 bridge and role reference | actual appointment/activation; role clearance at birth when required | P01 alone, persona, prompt compiler, same memory |
| O3 | applicable template authority explicitly dispositions D68 for exact subject/path/one attempt/validity | before birth permit issue | company D173 scope alone, D167 architecture, canary success |
| O4 | L0 source owner and company adoption owner admit exact source correction, commit/pin/answers and governed consumption | source repair/adoption before birth | changing copied/generated instructions or using corrected bytes under old pin |
| O5 | fleet-policy owner admits company placement; runtime/deployment owner verifies installed discovery/lint contract | qualified birth/discovery; deployment admission as applicable | source DEFAULT_AGENT_REPO_PATTERNS or a chosen directory |
| O6 | birth admission/execution owner issues and enforces permit/start/fence and accepts native birth result | birth issue/start/completion | task existence or fixture compiler pass |
| O7 | host/custody/data/provider/service owners admit each active profile and runtime proof | corresponding M0, memory or effect activation | inert birth, accepted policy, local artifact, recalled permission |

Conjunction, not delegation absorption: accepting O1 does not fill O2–O7. A current
owner-native agreement may validly cover multiple subjects, but each covered subject,
issuer capacity, scope and validity must be explicit. Genuine vacancy uses the
accepted owner fallback procedure; substantive objections remain objections and
cannot be bypassed by vacancy labeling. SoftwareCo cannot waive another company's
or core owner's constraints.

## Current authority binding

Minimum semantic facts for an actual admission boundary:

| Fact | Required content / source |
| --- | --- |
| Issuer/record identity | actual authorized issuer capacity, immutable reference/version/digest and authenticity established by its owner's mechanism; no new signing root assumed |
| Subject | actor, appointment, canonical role and authenticated security-principal binding; session attribution separate |
| Served domain/scope | served relation, jurisdiction, exact resource/target and permitted/excluded actions, delegation/lifecycle rights |
| Act/content | classified action, exact task/current claim where required, canonical content/argument/source/profile identities, specific reserved grants if applicable |
| Validity/revocation | current owner state, explicit expiry if any, review obligation separately, actual access/effect ordering and revocation semantics |
| Constraints | applicable source-owner policy, disclosure, capacity, retention and effect limitations with attributable identities |
| Decision/evidence | owner-boundary admission or refusal with reason, operation/attempt/fence correlation and supported provenance |

Boundary responses:
- **admit:** all required applicable facts established and current at the owner's
  defined admission point; records exact content/profile identity, not just a task ID.
- **denied:** owner establishes explicit refusal, expiry or revocation; no new effect.
- **unavailable:** fact/service/authenticity/freshness cannot be established; block
  the dependent admission without asserting the owner refused or the effect never ran.
- **conflicting:** subject/content or owner facts disagree; preserve disagreement,
  do not synthesize a more permissive grant. Unknown prior effect is separately tracked.

These are required meanings, not a shipped endpoint. On inspected native schema 46,
`ak decision record 173` reports records_available=false for the newer consent/
authorization surfaces. Legacy consent_mode is invocation history, not consent or a
new grant. Do not invent a native grant API or convert this RFC into a shadow store.
Actual accepted owner receipts/read adapters must be bound before activation. A cache
or snapshot never supplies undefined freshness/linearization guarantees; if current
admission cannot be enforced, do not activate that action profile.

## Birth-state contract

**Permit:** one exact owner-issued birth authorization. **Attempt:** one admitted
execution correlated to it. **Artifact disposition:** absent, partial, complete or
unknown, established from actual owner evidence. Permit state does not erase artifact
or effect facts. Review-date/expiry and execution lease are separate owner terms.

Required binding before issue: issuer/validity/revocation, accepted O3 disposition,
subject/role/artifact association, exact destination and collision/absence evidence,
route A, source commit/pin/answers/manifest identities, semantically accepted creation
task, permitted write scope, required native checks and result receiver. If the issuer
cannot establish these or O4/O5/O6, no usable permit exists. This policy ADR itself
is not the permit.

| From → to | Admission/event and guard | Consequence |
| --- | --- | --- |
| available → started | owner durably and atomically reserves the exact permit for one attempt after all preconditions; destination/input identity and exclusive fence bound before any birth write | consumes the right to start; one attempt only |
| available → uncertain_partial | settlement of attempted start cannot be established | close the local authorization projection to further starts; actual owner admission/consumption stays unknown until reconciliation, not invented as true or false |
| available → available | preflight rejected before durable start and before any authorized birth write | no attempt; preserve refusal evidence; current permit may later be withdrawn/expire |
| available → revoked | issuer revokes or owner establishes explicit expiry before start | no birth admission; revocation history retained |
| started → completed | required native generation/persona/lineage checks and actual designated receiver disposition establish complete inert artifact | attempt closed, permit consumed; no activation or second birth |
| started → uncertain_partial | interruption, uncertain admission settlement, partial writes, failed terminal evidence or unestablished artifact disposition | no automatic repeat/overwrite; retain known phase and missing evidence |
| uncertain_partial → started | original durable start is confirmed; explicit recovery authorization for SAME attempt; prior executor fenced; exact unchanged subject/path/code/pin/answers; trustworthy phase/effect evidence establishes permissible next writes | resume only admitted remaining work, not rerender from ignorance |
| uncertain_partial → completed | original durable start is confirmed; owner reconciliation proves complete conformant artifact and receiver acceptance without further birth writes | records original attempt result, never a second start |
| started/uncertain_partial → revoked | issuer revocation/expiry blocks new admissions/writes at defined boundary | preserve last attempt state plus partial/complete/unknown artifact/effect facts; not rollback proof |
| completed → completed | status/reconciliation of original accepted result | no new writes/start; subsequent activation has distinct permissions |
| revoked → revoked | status/read permission separately admitted; artifact disposition may be refined | no writes/restart; completed artifact may still exist and remain inert |

Every unlisted transition is forbidden, especially started/uncertain/completed/revoked
→ available. A new actor/path/pin/route or new attempt requires new exact owner
admission and disposition of the old partial/unknown obligation. Relabeling IDs cannot
hide a repeat attempt. Cancellation requested by caller is not issuer acknowledgment
or permission withdrawal; physical effects remain separately recorded.

**Interrupted birth consumes the start right if start was admitted.** If whether start
was committed is unknown, reconcile; do not infer available from absence of a reply.
A known pre-start refusal consumes nothing. Uncertain supervisory state is a projection,
not a fabricated native admission receipt. If reconciliation proves no start occurred,
the old uncertain projection still grants no retry: the issuer explicitly dispositions
it and issues new admission authority before another attempt. This conservative
choice preserves no-reset semantics without claiming the old right was physically
consumed; no-action evidence and permission to try again are different facts. Same-attempt recovery is not a second
birth: it is an owner-admitted remaining step under fenced identity/phase evidence.
If the remaining-step contract cannot be proved, recovery is blocked; an operator
may authorize a distinct repair/disposal/new attempt, not automatic overwrite.

A revoked attempt cannot return to started or completed as permit state. Its artifact
facts can later show complete creation, but permission stays revoked and no activation
is inferred. Completed birth is immutable historical result; revoking future active
permissions does not rewrite it. Do not promise interruption or teardown stronger
than the actual owner boundary supports.

**Adapter proof required:** cross-process exclusive reservation and fencing at actual
write admission; not just SQL serialization, an expired lease or a pure state reducer.
This capability is a prerequisite for birth admission and has not been observed in
the current task-existence wrapper. Fake state tests do not qualify the real adapter.

## Clause verification

Each V row is an executable acceptance obligation under a later admitted checker/
profile, not an assertion that the mechanism already exists. A test must record exact
inputs, native boundary observations, expected result, actual result and provenance.
Use synthetic fixtures for abstract policy first; then real owner/consumer evidence.

| Clause / check | Executable obligation / decisive negatives | Accountable issuer; evidence receiver | Stage |
| --- | --- | --- | --- |
| P01 / V01 | resolve distinct actor/role/appointment/session/repo association; reject repo-copy/prompt/role-type equality as appointment or identity proof | governance/semantic + identity adapter owner; appointment receiver | bridge/reference before appointment; actual binding before activation |
| P02 / V02 | admit R1/R2 inside valid standing/task/owner envelope without another CEO action; refuse task closure/delegation missing explicit right | task/source/execution owner; receiver/maintainer | before corresponding active profile |
| P03 / V03 | exercise X1–X5, forged routine label, changed payload and denied/unavailable/conflicting/revoked current authority; observe no new dependent effect | actual authority/effect adapter owner; accountable policy/source receiver | before profile activation |
| P04 / V04 | new-session same actor with fenced recovery; distinct actor without commitment transfer; due review vs actual expiry; reject stale lease/approval | identity/AK/host owners; commitment/custody receiver | before continuity claim |
| P05 / V05 | two contenders one permit; crash before/after start; partial recovery, revoked state and no reset/second attempt; independent write/admission trace | birth admission/execution owner; template/result receiver | before permit/birth; native result afterward |
| P06 / V06 | actual two-stage pinned-L0 render plus native lineage/refresh/discovery/lint checks; pin mismatch, role/name collision and unauthorized route B refused | L0/company/fleet/lineage owners; template/fleet receiver | before birth route qualified |
| P07 / V07 | real rendered AGENTS posture matches company main-first/location and owner authority; loader projection checked; generated-only fix/contradictory policy fails; preserve ownership | L0/company instruction/adoption owners; affected consumer receiver | source correction/adoption before birth |
| P08 / V08 | recall control/candidate fixtures preserve corrections/exceptions; deny canaries/metadata, stale reingestion/policy release and KES auto-promotion | data/retrieval/provider/KES owners; data/learning receiver | before memory/data profile expansion |
| P09 / V09 | actual M0 cognition and resource denial/egress; native first-render and final accepted/rejected export crash cuts, custody/fenced takeover; result-or-blocker observed | host/deployment/custody/provider owners; operator result receiver | before complete M0/long-running-runtime claim |

Policy fixtures and document checks can establish internal contract consistency and
text/reference integrity. They cannot establish authenticity, atomic reservation,
resource confinement, provider egress, physical no-effect, custody or crash safety.
No runtime test pass is declared before those boundary observations exist.

## Migration and rollback envelope

- Before birth: preserve current source/company/agent-owned bytes; qualify correction,
  exact new pin/answers and admitted adoption. Revert isolated changes through their
  actual owners and recheck readers/checks if qualification fails. No blanket fleet
  update or company-copy deletion follows.
- After partial birth: block repeat admission, keep last actual artifact/effect state,
  retain records and fence/reconcile. Source rollback does not undo directory writes.
  Repair/quarantine/disposal needs exact owner scope; do not delete unknown or live
  state. Resume only proven remaining work under the original attempt contract.
- After complete inert birth: preserve artifact/provenance and accepted result;
  refrain from activation when current qualification fails. Owner-authorized source/
  persona repair records a new revision, not historical rebirth under the old permit.
- After active operation: revoke future admission under the actual owner semantics,
  retain unknown effects/commitments and use separately qualified runtime recovery.
  Repository rollback is not a host-state, provider-disclosure or external-effect rollback.

Actual rollout/revert commands and affected file sets are post-ADR owner task work;
this envelope fixes the contract without inventing permissions or a deployment plan.
