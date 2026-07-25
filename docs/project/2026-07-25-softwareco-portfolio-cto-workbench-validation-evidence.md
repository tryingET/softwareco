---
summary: "Observed package, checker, cold-start Pi/RPC, advisory, trust, and rollback evidence for the preactivation Decision 74 CTO workbench."
read_when:
  - "Reviewing whether the Decision 74 CTO workbench is ready for human controller designation and SF3 activation."
  - "Reproducing the tracked mode, preset, /cto entrypoint, or rollback proof."
type: "evidence"
status: "preactivation_validated"
date: "2026-07-25"
decision_id: 74
execution_task_id: 4156
controller_task_id: 4182
---

# Decision 74 CTO workbench validation evidence

## Scope and claim

This evidence establishes that the tracked Softwareco workbench is discoverable, composable, fail-closed before delegation, and reversible in a fresh Pi process. It does **not** establish an active CTO delegation, controller designation, controller claim, `SF3` activation, portfolio thesis, admitted wave, or completed outcome.

All live behavioral runs used ephemeral `--no-session` Pi RPC processes from `/home/tryinget/ai-society/softwareco`. No owner repository, AK authority state, FCOS state, external system, or source file was mutated. Mode selection changed only ephemeral session prompt state.

## Runtime and package identity

Observed runtime:

- Pi: `0.80.10` at `/home/tryinget/.npm-global/bin/pi`;
- configured package source: `npm:@tryinget/pi-modes@0.3.0`;
- installed package: `/home/tryinget/.pi/agent/npm/node_modules/@tryinget/pi-modes`;
- installed package manifest: `name=@tryinget/pi-modes`, `version=0.3.0`;
- registry tarball SHA-1: `ad0c25c61200dba413016e8d23a9f67e1853f9fe`;
- registry integrity: `sha512-YuoxRKBKBVVXwNVr7gwco4jW6MYhkFxYWtsEXmY5saquR4HA6aT2Ed0g/Lre2gX4+t7v8qMp923840ios7eesg==`;
- downloaded tarball SHA-256: `aec5c64b5520ec78ddde4e03af682299d87eaecf79ccda03881fe754afac75af`;
- an extracted registry tarball compared byte-for-byte equal to the installed package tree.

The earlier source-tree `npm pack` digest in `2026-07-25-softwareco-portfolio-cto-evidence.md` is release-source evidence, not the registry distribution digest above. Runtime identity uses the exact configured registry release and observed registry integrity.

## Deterministic preactivation check

Command:

```bash
./scripts/check-cto-operator-surface.sh
```

Observed result:

```text
OK /home/tryinget/ai-society/softwareco/.pi/modes/softwareco-cto.json (mode)
OK /home/tryinget/ai-society/softwareco/.pi/mode-presets/softwareco-cto.json (preset)
cto-operator-surface: PASS (preactivation)
```

The checker copies the exact installed package to an ephemeral non-`node_modules` directory and invokes its owner linter with Node. It performs no runner fetch or implicit package installation. The checker also observed Decision 74 acceptance receipt `8818`, Decision 74 accepted/unblocked, `SF3` active with exact `decision_membrane_pending_no_cto_delegation`, all three projections at `accepted_preactivation`, and controller task `4182` pending with source mutation forbidden. Its separate `--require-active` branch fails closed unless exact active timestamps, termination/supersession absence, direct human designation, claimant equality, and both leases pass.

## Fresh trusted-root Pi/RPC proof

A fresh trusted-root process discovered:

| Command | Source | Exact owner path |
|---|---|---|
| `/mode` | extension | installed `@tryinget/pi-modes@0.3.0/extensions/mode.ts` |
| `/mode-status` | extension | installed `@tryinget/pi-modes@0.3.0/extensions/mode.ts` |
| `/mode-preview` | extension | installed `@tryinget/pi-modes@0.3.0/extensions/mode.ts` |
| `/cto` | project prompt | `/home/tryinget/ai-society/softwareco/.pi/prompts/cto.md` |

Observed command sequence:

```text
/mode-preview --json softwareco-cto
/mode use softwareco-cto
/mode-status --json
/mode off
/mode-status --json
```

Reproduction host command and ordered RPC payloads:

```bash
cd /home/tryinget/ai-society/softwareco
pi --mode rpc --no-session --approve --offline --no-skills --no-tools
```

```jsonl
{"id":"commands","type":"get_commands"}
{"id":"preview","type":"prompt","message":"/mode-preview --json softwareco-cto"}
{"id":"activate","type":"prompt","message":"/mode use softwareco-cto"}
{"id":"status-active","type":"prompt","message":"/mode-status --json"}
{"id":"off","type":"prompt","message":"/mode off"}
{"id":"status-off","type":"prompt","message":"/mode-status --json"}
```

Each prompt response reported `success=true`. Pi Modes emits deterministic status/preview JSON on stderr under the Pi RPC host limitation documented by the package; both stdout and stderr must be captured.

Results:

- preview selected native host plus only `softwareco-cto`;
- project component path was `.pi/modes/softwareco-cto.json`;
- effective component digest was `81064c945cfca72701a3f78dfb285551ce7c89129a22e7530d1ee695e20f64b3`;
- composed prompt SHA-256 was `29157a51510ae997063f53e3c834489af9db5468493f3d36756a3ef6350418f5`;
- host delta was `2019` bytes;
- preset activation reported `source=preset`, `blocked=false`, no drift, and no diagnostics;
- `/mode off` returned to native host with zero components and host delta `0`;
- native composition SHA-256 was `f0f6a73c271ee54288b1484fa81ef1cd76a28d2b022c058f0eeb83d4045bc8d9`.

No `pi-modes` extension error occurred. A separate snapshot-edit extension reported an expected startup refusal in the deliberately `--no-tools` smoke process because no built-in read owner was available; it was unrelated to mode discovery, composition, or rollback.

Ephemeral raw receipt hashes:

- RPC stdout JSONL: `29676d4042f5b4b35ba299a93c036a159a51aebda6b2dff8b9a367f9bebb1822`;
- Pi Modes stderr JSON: `372b90dc86c877d769fdca32610028d57cce0e5618ebf6910a1fb94a1c135bf9`.

## `/cto` fail-closed behavior

### Missing objective

A fresh trusted-root process activated the preset and invoked `/cto` without arguments. The settled response was:

```text
Advisory only: The normalized objective is empty. No CTO preflight or execution was performed.
Please invoke: /cto <objective>
```

### Objective present but authority readback unavailable

A second fresh process activated the preset and invoked:

```text
/cto Assess the next owned-portfolio technical thesis without mutating authority or owner state
```

The process deliberately exposed no tools. The settled response normalized the objective, marked each of the ten preflight conditions `Unverified — fail closed`, concluded `advisory only`, and stated that no authority or owner state was mutated. This is negative behavior proof; it is not an active-delegation canary.

Ephemeral RPC stdout JSONL SHA-256: `b9e385565f64c1a288021acd46984b5445f432c5a30a56adc8a517e1687a0afb`.

Reproduction uses the same trusted-root host command above, then sends `/mode use softwareco-cto`, the `/cto ...` prompt, waits for `agent_settled`, reads `get_last_assistant_text`, and sends `/mode off`. `--no-tools --thinking low` intentionally makes owner-native readback unavailable so fail-closed behavior is the only lawful result.

### Untrusted project

A fresh process from the Softwareco root with `--no-approve` discovered 204 commands and no `/cto` project prompt. This proves the project entrypoint is withheld when project-local files are untrusted.

Reproduction host command is `pi --mode rpc --no-session --no-approve --offline --no-skills --no-tools`, followed by `{"id":"commands","type":"get_commands"}`.

## Remaining activation gate

## Independent cold-start review correction

Independent reviewer dispatch `dispatch-1784968306119` initially returned `not ready` because the first checker version could accept a broad active `SF3` prefix without proving designation, claim, leases, termination absence, or active projections, and because its linter path could fetch `tsx`. The checker was revised to close both issues before commit. The review also requested reproducible RPC inputs; the exact host commands and payloads are recorded above. This correction is evidence of review response, not proof that delegation is active.

The workbench is ready for the separately required human step, but the CTO delegation remains inactive. Activation still requires, in order:

1. a direct `human-operator` controller-designation governance receipt naming the exact claimant, evidence ref, and expiry;
2. atomic claim/readback of controller task `4182` with lease no longer than 14,400 seconds;
3. pre/post-read and exact `SF3` activation detail reconciliation;
4. `./scripts/check-cto-operator-surface.sh --require-active`;
5. a fresh active preflight canary before any portfolio admission.
