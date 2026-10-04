---
summary: "Incorporated R3 contracts: parent exception start-right consumption across permits, creator/subject separation, retained decision rights and executable verification obligations."
read_when:
  - "Checking exact operational semantics of the proposed R3 Principal policy."
type: "reference"
status: "proposed-contract-not-owner-record-or-implemented-interface"
task: "AK6635"
decision_id: 173
as_of: "2026-10-04"
---
# R3 contract appendix

Incorporated by [R3 RFC](resolution-rfc-r3.md). This appendix specifies required
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

**Creator versus subject:** the bootstrap creator/executor uses its own current
identity, authenticated principal and birth-execution authority. The prospective
Principal is the intended artifact/role subject of that creation, not permission
for an executor. These binding categories remain separate even if an already owner-
identified actor holds both roles under independently current creator authority.
No different-person/actor requirement is imposed merely by the diagram. An owner-
approved intended association/reference is sufficient
to name the inert artifact; it is not proof of an already appointed Principal.
The creator's current authority must resolve before writes. The Principal's D24
bridge/actual actor binding and appointment resolve before its own activation.
No unborn actor must sign, appoint itself or authorize its birth.

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
| O3 | applicable template authority dispositions D68 and issues one canonical exception start right; names authoritative consumption custodian and any renewal/replacement act | before right/permit issue; fresh explicit O3 disposition before replacement start entitlement | company D173 scope, old consumed O3 record, new O6 permit ID, artifact cleanup or canary success |
| O4 | L0 source owner and company adoption owner admit exact source correction, commit/pin/answers and governed consumption | source repair/adoption before birth | changing copied/generated instructions or using corrected bytes under old pin |
| O5 | fleet-policy owner admits company placement; runtime/deployment owner verifies installed discovery/lint contract | qualified birth/discovery; deployment admission as applicable | source DEFAULT_AGENT_REPO_PATTERNS or a chosen directory |
| O6 | birth admission/execution owner issues child permits and, only under O3 delegation, atomically consumes the parent start right, fences execution and accepts native birth result | birth issue/start/completion/recovery | per-permit locking alone, O6 reissuance as renewal of O3 right, task existence or fixture compiler pass |
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
| Subject | actual acting creator/executor's identity/role/grant and authenticated principal; session attribution separate. Intended artifact/role subject is a distinct binding and need not have Principal appointment before inert birth. Active Principal operations require its actual actor/appointment binding. |
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

### Units and authoritative identity

**Policy:** D173's accepted conditional rule, if eventually adopted; not itself a
live birth grant. **O3 exception start right:** one source-owned permission to admit
one exact birth attempt, identified by the issuer's canonical right reference and
O3 authorization-act identity. **O6 permit:** execution admission material referring
to that right, not a new right. **Attempt:** one start admitted against the parent.
**Artifact disposition:** absent, partial, complete or unknown, independently evidenced.

Caller permit IDs, aliases, task/controller IDs or destination cleanup cannot change
the right's identity. O3's owner surface must resolve aliases to the SAME underlying
one-use authority slot. A merely new string/reference pointing to the same O3 act is
not a replacement authorization. Actual O3 issuance must specify that slot and its
count of one; O6 cannot carve more slots from it. These are logical binding obligations,
not a proposed global key algorithm, schema or new permissions database.

### Relationship diagram

```text
Existing creator C --current execution authority--> O6 admission boundary
                                                     |
O3 actual template-owner exception act              | delegated consumption only
  |                                                  v
  +-- canonical start right E --constrains--> permits P1, P2, ...
             |                                  |
             +-- at most ONE durable start ----+--> original attempt T
                                                        |
Intended Principal artifact/role S <--bound subject------+--> artifact A

Same-attempt recovery: E stays spent; P/T remain correlated; zero new starts.
New attempt: fresh explicit O3 disposition -> distinct right E2, not P2 under E.
C's acting-authority binding is not S's intended-subject binding, even if one
already identified actor can occupy both roles. A is not appointment or active host.
```

### Consumption owner and receipt

O3 names the authoritative consumption custodian and source-native read/record
mechanism before issue. O6 may be that custodian only under explicit O3 delegation;
that delegation permits reservation/consumption, **not issuance or renewal** of the
O3 exception. Actual source-owned authenticity, canonical alias resolution, current
revocation and receipt custody must be established, not inferred from JSON labels.
If no owner adapter can establish them, no birth profile is qualified.

Durable start admission must atomically reserve the **parent E**, regardless of which
permit/controller/process is used. The authoritative start receipt joins E's canonical
identity, O3 act/reference/version, P, T, creator/principal, intended subject, exact
path/source/pin/answers/task/profile and executor fence. Birth writes require the
committed receipt. Parent reservation and start correlation have one proven owner
linearization; a child-permit lock alone fails V05. One consumption custodian owns
that record; no atomic transaction across arbitrary owner databases is assumed.

A child local record may lag or be lost. That cannot make E unused: the parent receipt
controls. Status permission is separate from start/recovery permission. If receipt
settlement or current owner state is inaccessible/ambiguous, all E-linked permits
are held for further start, never defaulted to available from not_found.

### Parent consumption and admission are separate facts

Required parent facts: canonical identity/O3 act; consumption `unused | spent | unknown`;
admission `open | held | revoked`; original start/attempt association when established;
explicit validity/revocation and lineage. These are semantic facts, not shipped fields.
`spent` and `revoked` may both be true: revocation cannot erase historical consumption.

| Event | Parent consequence | Permission consequence |
| --- | --- | --- |
| proved pre-start refusal, no reservation/write | unused remains unused under current issuer terms | no attempt; an actually open right may be offered again only through actual admission |
| durable parent reservation/start receipt | unused/open -> spent; associate original P/T | no later NEW start under E through ANY permit ID |
| start settlement/current state unknown | consumption unknown, admission held in supervisory projection; actual owner state not invented | ALL E-linked permits blocked from further start pending disposition |
| matching original start reconciled | original spent association established; no new start | same-T recovery may be considered only with separate fresh recovery authority and actual fence/phase proof |
| revocation/expiry | admission revoked; consumption/history retained as spent/unused/unknown according to evidence | no new start/write/recovery under revoked authority; no physical rollback inference |
| artifact fails, is partial, absent again, quarantined or source reverts | does not change known spent parent to unused | no new start from filesystem cleanup or source rollback |
| explicit fresh applicable O3 replacement disposition | links old E/P/T and their actual dispositions; issues distinct E2 with its own scope/validity | E remains immutable history; E2 is not a reset or O6 renewal; all other binding/safety conditions still required |

Unknown is a knowledge limitation, not proof of consumption or nonexecution. Even
if later no-start evidence resolves the uncertainty, R3's conservative recovery rule
requires explicit O3 disposition before a different attempted start/new permit path:
O6 cannot clear the hold and retry by itself. Known pre-start refusal is distinct and
does not pretend to consume E. This is reserved birth admission, not a routine-task
CEO checkpoint or operating budget for the future Principal.

### Child permit/attempt phases

The five R2 phases remain a **local execution projection**, never the source of E's
availability. Every start checks parent identity/current facts, exact creator versus
intended-subject bindings and all required O2/O4/O5/O6/collision/source conditions.

| From -> to | Additional guard/event | Consequence |
| --- | --- | --- |
| available -> started | parent E proved unused/open; qualified atomic parent reservation and correlated receipt; exclusive fence before writes | E spent, one original T; local P becoming started alone is insufficient |
| available -> uncertain_partial | original attempted start settlement unknown | hold E across all P aliases; no repeat; actual start stays unknown |
| available -> available | known pre-start rejection without parent reservation/write | no attempt; refusal evidence retained, no assertion of start |
| available -> revoked | actual issuer revocation/expiry | no start; parent admission also checked independently |
| started -> completed | native conformant inert result and designated receiver acceptance | E remains spent; no activation/second start |
| started -> uncertain_partial | interruption/partial or unestablished terminal/effect evidence | original E/P/T retained; no overwrite or new-ID retry |
| uncertain_partial -> started | parent spent with CONFIRMED ORIGINAL T; fresh current recovery permission; prior executor fenced; unchanged subject/path/code/pin/answers; proved remaining step | same T only; zero additional start admissions |
| uncertain_partial -> completed | original parent/start proved and conformant artifact/receiver acceptance established without new writes | original result reconciled, E still spent |
| started/uncertain_partial -> revoked | actual revocation/expiry at owner boundary | no future writes; artifact/effect facts independently retained |
| completed -> completed | permitted original status read | no start/write; consumed history unchanged |
| revoked -> revoked | separate current status-read permission | no start/write; a complete artifact can be discovered without reviving authority |

Every other child transition is forbidden, particularly reset to available or return
from revoked/completed to a new start. A different unused child P2 referencing spent,
held or revoked E has no effective start right, even if P2 says available. Multiple
permits issued before E is spent still contend on E and can yield at most one start.

### New attempt versus recovery

Recovery uses the original authoritative E/P/T association, unchanged bindings,
current recovery permission and known remaining effects. Merely keeping T's label
while rerendering blindly is not recovery. If original start is not proved, same-T
recovery cannot be admitted; if fences/remaining effects cannot be established, it
stays blocked. Caller cancellation is not owner withdrawal/acknowledgment or rollback.

A replacement attempt after spent/held/revoked E requires **fresh applicable O3
exception authorization**, explicitly binding old E/attempt disposition and distinct
E2. The O3 act must grant a NEW one-start right, not refresh/duplicate the old consumed
record or delegate arbitrary renewals to O6. Same human may act in both roles, but the
reserved O3 act and execution O6 act must remain separately attributable. Actual
owner-native decision/authorization procedure governs the fresh act; this contract
neither mandates a whole new architecture RFC for each recovery nor grants routine
retry authority. If mandatory safety/collision/fence facts remain unknown, E2 alone
cannot admit birth. A complete inert artifact is repaired/revised under its own task,
not routinely reborn under another permit.

**Adapter proof required:** simultaneous DIFFERENT permits under one E; alias/reissue
and post-partial-birth cases; parent-level durable exclusivity/current revocation,
original-T recovery fencing and independent write/start evidence. SQL/per-permit
locking, stable task numbers, expired leases, fixture flags or a pure reducer do not
prove these. Current native authorization APIs/consumption custody are not claimed
implemented; fake/construction checks cannot qualify actual birth.

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
| P05 / V05 | different permits/aliases under SAME O3 canonical right; post-partial and cleanup reissue; fresh O3 vs O6-only replacement; unknown parent receipt; original-T recovery and parent no-reset across crash/revocation; independent start/write evidence | O3 issuer + delegated consumption/O6 execution custodian; template/result receiver | before parent right/permit/birth qualification; native result afterward |
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
