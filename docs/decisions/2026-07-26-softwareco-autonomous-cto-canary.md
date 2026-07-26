---
summary: "ADR candidate for Decision 83's one-time 24-hour autonomous CTO observational canary."
read_when:
  - "Accepting, operating, reviewing, or stopping the autonomous CTO canary."
type: "decision"
status: "candidate_pending_human_acceptance"
date: "2026-07-26"
decision_id: 83
task_id: 4284
system4d:
  container: "One Softwareco observational service canary."
  compass: "Continuous CTO-shaped sensing without owner-authority transfer."
  engine: "Accepted bundle -> human activation -> 24 fresh hourly workers -> expiry -> review."
  fog: "Prompt drift, incomplete evidence, hidden state, cost, scheduler persistence, and authority confusion."
---

# ADR candidate — 24-hour autonomous CTO observational canary

## Status

Candidate only. Decision `83` is `decision_pending` with controlling `ready_for_adr` closure. Authority review `dispatch-1785093118453` and runtime review `dispatch-1785093118453-1` both returned `READY` for source commit `f36547935826bbf8f4597f928b545127cff10003`. No direct-human architecture acceptance exists, so this document grants no installation, activation, service, model-call, or autonomous authority.

## Context

Decision 77 proved fresh-session recurring CTO operation inside finite direct-human epochs but intentionally forbids a scheduler and continuous appointment. The operator now wants a bounded test of an always-available CTO-shaped observer and a stronger system prompt that replaces Pi's static native base while retaining the rest of the dynamic host envelope.

## Candidate decision

Authorize exactly one 24-hour, at-most-24-cycle Softwareco observational canary under the reviewed RFC and validation plan.

Each cycle uses a fresh `pi --mode rpc --no-session` worker. The `softwareco-cto-canary` Pi Mode uses `replace_base`; it owns the static base prompt while preserving dynamic AGENTS/CLAUDE context, selected skills/overlays, append-system content, date, and cwd. The first canary intentionally disables tools, skills, prompt templates, themes, and all extensions except a pinned Pi Modes package.

The worker may sense bounded AK-registered portfolio facts, detect drift/blockers, rank evidence-cited theses, draft human-review text, and recommend—but not dispatch—an ordinary task, deep review, visible loop, Nexus coordination, transcendent iteration, or no action.

The worker and supervisor may not mutate AK, direction, evidence, governance, decisions, Git, owner repos, FCOS, publication, release, or external systems. Model API calls and private local canary state are the only accepted operational effects. Outputs are proposal-only and noncanonical.

Architecture acceptance does not start the canary. A direct human separately installs the exact accepted Git bundle and separately records an exact activation receipt before enabling timers. Runtime rereads authority and compares bundle, units, prompt source, and runtime packages against accepted Git/digest facts every cycle. Authority ends at the exact 24-hour deadline even if timer cleanup fails.

## Relationship to existing decisions

- Decision 74 remains terminal under receipt `8870`.
- Decision 77 remains accepted as a separate finite-epoch recurring framework.
- Decision 83 neither amends nor supersedes either decision.
- Any autonomous execution beyond observation requires a later separately reviewed decision.

## Consequences

Positive:

- tests continuous operational usefulness without transferring owner authority;
- avoids persistent Pi transcript state;
- proves a stronger prompt identity using reviewed `replace_base` semantics;
- produces comparable cycle evidence and explicit escalation recommendations.

Costs and risks:

- up to 24 model calls and bounded local operational state;
- USD 2 per-cycle and USD 25 cumulative thresholds are supervisory stop thresholds, not provider-side billing caps; one call can overrun and that residual risk requires direct-human acceptance;
- current AGENTS policy enters each dynamic prompt and can affect output;
- portfolio snapshots may be incomplete or too large and must fail visibly;
- provider failure, proposal noise, and timer/service faults may make the canary useless;
- operators may mistake drafts for commitments unless proposal membranes remain explicit.

## Rollback

Before acceptance, revert candidate source only. After install but before activation, remove disabled units and the commit-addressed bundle. After activation, use the direct-human stop path, preserve receipts/results, disable timers, and review discrepancies. Never delete AK history or mutate owner tasks as rollback.
