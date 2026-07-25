---
summary: "Evidence establishing the gap between Decision 68's expired bounded CTO role and an operable Softwareco owned-portfolio CTO."
read_when:
  - "Reviewing the evidence for the Softwareco portfolio CTO proposal."
type: "evidence"
status: "decision_pending"
date: "2026-07-25"
---

# Evidence — Softwareco owned-portfolio CTO gap

## Accepted historical baseline

Decision 68 accepted a bounded `softwareco-cto-agent` delegation for L1 template activation and an issue-tracker canary. The charter states that the delegation expires at the earliest of 30 days, canary terminal decision, revocation, or supersession.

The canary reached a human terminal stop after Gate A remained unsatisfied. AK records:

- `SF2`: all child waves terminal;
- `IW4`: `stopped_blocked_no_effect_gate_a_unsatisfied_hold`;
- zero AK cursor mutation and zero GitHub mutation;
- no broader template propagation;
- no remaining open Softwareco execution task for Decision 68.

On 2026-07-25, `SF2` was reconciled to `done` with state detail `completed_delegation_expired_at_canary_terminal_stop` before opening the new decision frame.

Reproducible anchors:

| Claim | Stable reference |
|---|---|
| Decision 68 accepted bounded delegation | `ak decision get 68 --machine` and `docs/decisions/2026-07-18-softwareco-cto-agent-template-activation.md` |
| Terminal stop and zero effects | AK task `4099`, result refs `evidence:5061`, `evidence:5065`, `evidence:5066` |
| Gate A unsatisfied/hold | AK task `4134`; `infra/issue-tracker` commit `fa7719ed30a2f6ff3e67feb338ae3dd48d07c579`; evidence `5056`–`5058` |
| Parent pointer and terminal baseline | Softwareco commit `e66ccec993f19cd7546cb53ef52ef1916a26ef10` |
| SF2 reconciliation and SF3 pending decision frame | `ak direction show --repo . SF2 --machine`; `ak direction show --repo . SF3 --machine` |

## Runtime and repository inspection

Inspection found:

1. no generated CTO agent repository from `copier/tpl-agent-repo`;
2. no tracked `softwareco-cto` Pi mode or preset;
3. no `/cto` command or prompt template;
4. one ignored machine-local `.pi/modes/softwareco-builder.json`, which is a general builder prompt and grants no CTO authority;
5. Pi Modes explicitly states that mode activation changes prompt policy only and grants no tools, mutation, publication, promotion, continuation, or organizational authority;
6. the agent-repository template explicitly separates an agent product/capability repository from organizational appointment;
7. AK currently has decision/direction/task/evidence surfaces but no first-class general delegation command; the accepted decision plus active direction state and bounded charter must therefore form the current delegation readback;
8. native FCOS authorizes only `fcos new` and `fcos close` against its own board, requires an exact AK task for real writes, and keeps every current item coordination-only and non-claimable.

Inspection revisions:

- Softwareco: `e66ccec993f19cd7546cb53ef52ef1916a26ef10`;
- `owned/pi-extensions`: `891a8fd51e6ec004bce35f3c11d6a8d673ceec2e`;
- `holdingco/fcos-control-board`: `b5efb2502608c6973ffabd3667f245bc1bbf342f`;
- Pi Modes contract: `owned/pi-extensions/packages/pi-modes/README.md` at the revision above;
- FCOS authority contract: `holdingco/fcos-control-board/docs/project/authority-boundary.md` at the revision above.

## Operator correction and selection

The accountable human corrected two prior assumptions:

- `infra/issue-tracker` is for downstream-dependency issue filing, not Softwareco's portfolio backlog;
- the intended CTO should manage technical portfolio sequencing across `softwareco/owned`, guided by AI Society principles, Softwareco vision/posture, and owner-repo product postures.

The human selected:

- technical portfolio sequencing within accepted postures;
- at most two active portfolio waves and six active owner-repo tasks;
- FCOS Layer 5 for genuine cross-repo coordination;
- a 30-day-or-earlier finite delegation;
- proof through a portfolio thesis and one completed outcome wave;
- a Pi mode plus `/cto` prompt-template entrypoint.

## Architectural inference

The evidence supports four separate layers:

```text
AK accepted decision + active SF3 = delegation authority
tracked Pi mode/preset = repeatable behavioral policy
/cto prompt template = operator entrypoint and preflight procedure
owner-repo AK tasks + source evidence = executable work and proof
```

A mode alone is insufficient. A separate agent repository is premature until a reusable CTO capability develops its own code, interface, test, release, and maintenance boundary.
