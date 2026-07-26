---
summary: "RFC candidate for a separately authorized 24-hour autonomous CTO observational canary."
read_when:
  - "Reviewing, accepting, installing, or operating the autonomous CTO canary."
type: "rfc"
status: "candidate_for_multi_lane_review"
date: "2026-07-26"
task_id: 4284
decision_id: 83
review_mode: "strict-adversarial-multi-lane"
review_closure_mode: "multi_lane_requires_synthesis"
system4d:
  container: "Softwareco company-level observational canary."
  compass: "Learn whether continuous CTO sensing is useful without transferring owner authority."
  engine: "Human acceptance -> commit-addressed install -> human activation -> 24 fresh cycles -> expiry -> synthesis."
  fog: "Prompt identity, hidden session state, authority drift, incomplete census, model cost, and scheduler persistence."
---

# RFC — 24-hour autonomous Softwareco CTO observational canary

## Proposal

Authorize one separately governed, 24-hour observational canary. A user-level systemd supervisor starts at most 24 hourly cycles. Every cycle starts a fresh, ephemeral Pi RPC worker, supplies a newly collected bounded portfolio snapshot, validates one proposal-only result, and exits. The service cannot continue past the receipt-bound deadline or cycle count.

This is not an amendment, continuation, or supersession of Decisions 74 or 77. Decision 74 remains terminal under receipt `8870`. Decision 77 remains the finite-epoch recurring workbench. The canary requires a new architecture decision and direct-human activation receipt.

## Prompt contract

Pi supports the native CLI option:

```bash
pi --system-prompt <text-or-file>
```

The canary deliberately uses the reviewed Pi Modes `replace_base` strategy instead. `replace_base` replaces Pi's static native base while retaining append-system content, trusted AGENTS/CLAUDE context, visible skills, date, cwd, and explicitly selected overlays. It adds fingerprints, drift blocking, mode status, and exact composition preview that a loose flag does not provide.

The accepted mode is `.pi/modes/softwareco-cto-canary.json`; the preset selects it as the sole base with no overlays. Production workers start with structured `PI_MODES`, then prove through `/mode-preview --json` that the effective component has the accepted project path and semantic fingerprint, uses `replace_base`, has no diagnostics, and composes the accepted base with current dynamic context.

The production worker intentionally selects no tools, skills, prompt templates, themes, or extensions except the pinned `@tryinget/pi-modes` extension. The replace-base composition mechanism still preserves those dynamic slots; their selected skill/tool sets are empty for this first canary.

## Runtime architecture

```text
systemd hourly timer
-> commit-addressed accepted bundle/run_cycle.py
-> live AK decision, acceptance, activation-chain, expiry, bundle, Pi, and mode checks
-> bounded read-only AK/Git portfolio snapshot
-> fresh pi --mode rpc --no-session worker
-> exact replace_base mode-preview proof
-> tool-free model proposal
-> strict schema/reference/coverage validation
-> watched AK/Git before-after comparison
-> noncanonical local result
```

A separate 24-hour stop timer disables future triggers. Runtime independently rejects execution after the exact activation deadline or after 24 run directories, even if timer shutdown is delayed. A worker timeout is capped to the remaining authorized interval with a guard margin. Expiry or direct-human stop terminates the main service cgroup, so an in-flight worker is not allowed to continue model effects after authority ends.

## Commit-addressed installation and activation

`activate_candidate.py` may run only by direct human after the new AK decision is accepted. It requires:

- a separate decision ID, never `74` or `77`;
- `accepted/unblocked` AK state and exact RFC reference;
- a direct-human architecture-acceptance receipt binding the full accepted commit;
- exact accepted `HEAD`, installer blob, and clean scoped candidate paths.

It installs blobs read from the accepted Git object into a commit-addressed bundle and writes a digest manifest. It installs but does not enable or start systemd units.

`start_candidate.py` with repeated exact decision/receipt/commit arguments and `--start` is a second direct-human action. It fresh-reads the decision, acceptance receipt, accepted Git blobs, installed bundle, rendered units, runtime package digests, and requires an empty decision-specific control chain, records one direct-human activation receipt, writes a local activation membrane, and enables the hourly and expiry timers. The receipt binds an exact start, exact 24-hour expiry, 24-cycle maximum, accepted commit, and activity envelope. The script's flags and attribution fields do not technically prove a person is present; the transition is lawful only when the accountable human directly invokes the reviewed command. Automation is forbidden from invoking this activation path.

Every production cycle fresh-reads the decision, acceptance receipt, control-chain head, activation receipt, bundle and rendered units against accepted Git objects, trusted-root mode source/fingerprint/composed preview, pinned Pi package digest/version, and pinned Pi Modes package digest. Any drift fails closed.

## Allowed autonomous activity

The worker may only:

1. observe the supplied AK-registered `softwareco/owned` snapshot;
2. identify evidence-linked drift, blockers, and uncertainty;
3. rank proposal-only portfolio theses and displaced options;
4. draft text for AK tasks, owner envelopes, decisions, and operator recommendations;
5. recommend exactly one next execution form.

The escalation vocabulary is:

- `ordinary_bounded_task` — one-owner executable work;
- `deep_review` — adversarial correctness or acceptance review;
- `visible_loop` — inspect/act/verify work needing human-visible checkpoints;
- `nexus_coordination` — one cross-owner intervention with compounding effects;
- `transcendent_iteration` — explicit ceiling-breaking iterative research;
- `none` — insufficient evidence or no warranted action.

The worker may recommend but never self-dispatch any orchestrator.

## Forbidden autonomous activity

The worker and supervisor may not create, claim, update, close, or mutate AK tasks, evidence, direction, governance, or decisions; mutate Git or owner repos; write FCOS; publish or release; cause public/irreversible effects; treat a draft as consent; or use a Pi transcript/result as authority. Installation, architecture acceptance, activation, and early stop are direct-human operations, not canary operations.

Model API calls and private local canary state are explicit operational effects of activation. The verifier does not overclaim proof of all external effects: it proves prompt/runtime gates, disabled capabilities, output/reference contracts, and watched AK/Git before-after equality.

The service hides the general home directory and read-only binds only the Softwareco tree, accepted bundle, required Pi authentication/configuration, pinned Pi Modes package, and AK binary. The worker receives a filtered environment, no tools, and only the pinned Pi Modes extension. Pi and Pi Modes package trees are digest-pinned. Provider networking remains necessary and is not destination-restricted; the canary does not defend against a malicious same-UID operator who can rewrite user services or Git. Its threat model is autonomous-process containment and fail-closed drift detection, not protection from the accountable workstation owner.

## Portfolio and proposal contract

AK repository registration defines portfolio membership. The collector enumerates every registered path under `softwareco/owned`, records missing repos, and gathers bounded Git state, nonterminal AK task classes, and direction exports. Filesystem Git roots not in AK are surfaced but never silently admitted.

Oversized, timed-out, invalid, or failed probes become coverage gaps. An oversized whole packet fails rather than truncating model input. The model must reproduce coverage exactly and cite resolvable `snapshot://portfolio.json#/...` references for every observation, blocker, and thesis.

Output is always `classification=proposal_only`, `authority_claimed=false`, `attempted_effects=[]`, and `canonical=false`.

## D2E and durable state

```text
portfolio observation
-> evidence-cited inference
-> ranked proposal
-> proposed execution form
-> human review
-> AK decision/task/owner envelope through its owning surface
-> execution and evidence only after separate authority
```

The canary creates no backlog. AK remains task, decision, direction, evidence, and lineage authority. Prompt Vault remains procedure authority. FCOS remains its owner surface. Pi files define runtime behavior but grant no consent.

## Rollout

1. Land and review the inactive candidate.
2. Create the separate AK architecture decision and attach problem/RFC/review/plan artifacts.
3. Obtain controlling multi-lane `ready_for_adr` synthesis.
4. Prepare candidate ADR and exact accepted commit.
5. Pause for direct-human architecture acceptance.
6. Direct human installs the commit-addressed accepted bundle.
7. Direct human separately activates the exact 24-hour window.
8. Observe hourly results and fail-closed behavior.
9. Expire automatically or stop early by direct human.
10. Review usefulness, cost, failures, and any proposed successor. Do not infer expansion.

## Alternatives

- **One persistent Pi conversation:** rejected because transcript/compaction becomes hidden mutable state.
- **Plain `--system-prompt`:** viable for experiments but rejected for the governed canary because it lacks mode fingerprints and drift observability.
- **`replace_final`:** rejected because it would require manually rebuilding dynamic host context and still cannot control later extension handlers.
- **Decision 77 epoch:** rejected because Decision 77 explicitly forbids this scheduler/continuous posture.
- **Immediate autonomous execution:** rejected until observational evidence supports a separately reviewed authority envelope.
