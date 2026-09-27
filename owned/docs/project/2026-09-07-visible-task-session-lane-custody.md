---
summary: "Decision151 lane task5481: legacy support withdrawal, positive checkout nomination/custody and safe reinstatement gates; no live domain certified."
read_when:
  - "Nominating an existing checkout for visible task-session canaries."
  - "Withdrawing legacy launch support or evaluating safe reinstatement."
type: runbook
---

# Decision151 — lane custody and reinstatement

## Status and authority

This is a runbook, **not an enrollment record or permission to launch**. No live
checkout, account, installed artifact, trigger suspension or effect disposition
is certified here. Parent/controller owns canonical AK task5481 evidence and
mutations; Pi task5480 owns classification/state/inspection and AK task5479 owns
authority intervals. Do not invent a lane registry or an alternate namespace.

Accepted basis and controlling owner plans:

- [ADR](../../pi-extensions/docs/adr/2026-09-06-visible-task-session-authority-startup.md)
- [Implementation](../../pi-extensions/docs/project/2026-09-07-visible-task-session-implementation-plan.md)
- [Validation/rollout/rollback](../../pi-extensions/docs/project/2026-09-07-visible-task-session-validation-rollout-rollback.md)
- [Lane source/test and producer status](2026-09-07-visible-task-session-lane-implementation.md)

The current task authorizes source and isolated synthetic testing only. Do not
run live Ghostty/Pi/provider/AK commands, probe secrets/config/fleets, enroll,
disable triggers, recover effects/claims or clean namespaces under this runbook.
Later staged installation/canaries require all owner gates below to pass.
Failed visible forks are historical startup-only effect uncertainty, not fresh
child-origin tasks. Never retry/resume those forks or infer retirement from the
idle debugging shells they left.

## Support withdrawal: now versus later custody

The checked-in `scripts/launch-pi-ak-task-ghostty.sh` is a **legacy** route, not
the accepted visible task-session operation. Its help remains discoverable;
README no longer advertises batch/preset launch recipes as the supported route.
The gate refuses the complete expanded request before log mkdir, AK, terminal
launch or focus unless the actual compatible producer positively classifies
it outside affected domains. Missing/unknown/incompatible classification cannot
fall back to ordinary AK `task show`. Dry-run is gated too.

This does not intercept private copies, shell aliases/functions, editor commands,
automation, already queued work or direct Pi/Ghostty invocations. The controller
must obtain positive withdrawal acknowledgments from their owners before any
nomination becomes eligible. A clean Git tree, absent PID, empty namespace,
candidate permit or the existence of this script is not custody evidence.

## Existing-checkout nomination packet (all facts required)

Controller and existing repo owner jointly nominate **one existing checkout**;
no checkout is nominated by this document. Record attestations in the canonical
owner evidence flow, with immutable evidence references in a rollout receipt.
Do not place operational truth in this lane document.

| Required fact | Accountable owner / evidence required | Current state |
|---|---|---|
| Existing canonical checkout identity | Repo owner: physical path, common-Git identity, overlapping checkouts and declared shared-effect domains; reconcile aliases/symlinks | Unprovided |
| Controller/session/manual custody | Controller and repo owner: all known sessions/controllers, manual shell/editor routes, prior launch history and descendants; observation-only commitment throughout occupied/unresolved/recovery custody | Unprovided |
| Lane/direct/copied recipes | Lane and actual users: installed gate identity, alias/function/private-copy inventory and explicit support withdrawal/acknowledgments | Source-only gate; actual routes unprovided |
| Editor/watch/build/automation | Actual owners: triggers, queued/in-flight/restart paths, owner-authorized stop/drain/disposition and disabled readback; named reinstatement owner | Unprovided |
| Candidate common-Git participation | Candidate owner: native inventory, admissions withheld, prior work drained/disposed; no borrowed permit | Unprovided |
| AK affected authority writers | AK owner: mutation/maintenance/import/policy/identity/recovery routes, stop-and-dispose-before-change throughout affected attempts | Unprovided |
| DB-wide recovery triggering | AK/trigger owners: actual trigger inventory including queue/restart/in-flight paths; authorized suspension/readback and explicit reinstatement owner; source code is not proof of a daemon | Unprovided |
| Tool/descendant/external effects | Each effect owner: prior/current started effects and retained uncertainty; closure/disposition evidence independent of terminal/PID state | Unprovided |
| Installed producer and inspector | Pi/AK owners: exact immutable package/runtime/native/SDK/provider/adapter identities, compatible DB-free inspector, tested canonical account/namespace/policy identity | Unprovided |
| Budgets and rollback | Controller and owners: useful explicit task/context/lease/credential budgets; compatible withdrawal/inspection/recovery route rehearsed | Unprovided |

Unknown owner, missing fact or inseparable competing route blocks eligibility.
Same task in another checkout, another task/profile in the same common-Git
family, or a new worktree is not an escape. This is cooperative local custody,
not hostile same-UID interception. Genuine independent work can continue only
outside the actual conflict predicates.

## Gated activation sequence (not executed)

1. Finish owner source, independent negative/fault/concurrency tests and exact
   producer/consumer agreement. No source fixture alone proves installation.
2. Freeze clean immutable release artifacts and verify package/dependency/ABI
   closure and canonical installed identity through owner-approved procedures.
   Keep compatible DB-free inspection available independently of admission.
3. Complete every nomination fact above with actual named owners. Obtain
   positive authorization/readback for competing-route restrictions; this
   document must not itself disable anything.
4. Confirm rollback readiness and positive custody before staged owner install,
   approved pin publication/reload and canary admission. Installation is not
   enrollment, and enrollment is not task admission.
5. Controller verifies fresh ordinary unclaimed explicit-scope task plus exact
   installed provider/model/reasoning/account and runs separately authorized
   useful canaries. Record real outputs, effects and stakeholder usefulness,
   not just window/ACK/FINAL/fixture success. Do not mechanically retry an
   indeterminate attempt.

## Withdrawal and safe reinstatement

On incompatibility or failure, stop **new admissions** through the owning
capability. Retain compatible inspector, immutable history and all custody for
occupied, denied-with-effects or unresolved attempts. Do not restore the old
launcher as a fallback, unlink/recreate a lockfile, clear reservations, kill
workers, release/reclaim tasks or infer recovery from time/PID/window absence.
A Git/package rollback is not operational retirement.

Before relaxing **any** affected route, obtain three distinct correlated proofs:

1. Host owner: future dispatch is irreversibly closed for the exact attempt and
   incarnation (not simply UI exit or lost transport).
2. Each effect owner: all started subprocess/tool/external effects are disposed
   or retained under explicit owner custody; unknown effects still block.
3. AK owner: exact task/claim tuple resolved through the accepted owner-native
   recovery interval after host/effect disposition; drift/reassignment/unknown
   commit stops, without automatic unclaim/retry.

The named route owner must additionally prove no other protected or unresolved
attempt is affected before reinstating queued/restarting/editor/automation
routes. **DB-wide recovery** reinstatement requires AK plus actual trigger-owner
approval across every potentially affected attempt, not just this checkout.
Record who reinstated what, actual readback, retained restrictions/history and
inspection compatibility in the canonical evidence flow. Absent facts retain
custody and escalate the exact blocked action to that owner.

## Coverage limits

The lane supplies a checked-in refusal gate, bounded tests and documentation.
It does not implement the new host, AK protocol, private-copy interception,
provider enforcement, custody certification, enrollment, live cancellation or
recovery. Those owner proofs remain independent prerequisites.
