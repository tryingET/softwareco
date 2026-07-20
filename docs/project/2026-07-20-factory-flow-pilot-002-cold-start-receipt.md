---
summary: "Independent cold-start receipt for Factory Flow pilot 002: contract-coherent issue-tracker state was classified correctly as operationally blocked."
read_when:
  - "Auditing the pilot 002 operator outcome or readiness classification."
  - "Designing a reviewed reconciliation path for an already-submitted external issue."
type: "validation-receipt"
status: "pass_truthful_blocked_classification"
date: "2026-07-20"
decision_id: 68
pilot_id: "SOFTWARECO-FACTORY-PILOT-002"
peer_run_id: "scoutpeer-mrtk5n7j-b8934ad1"
---

# Factory Flow pilot 002 — independent cold-start receipt

## Test contract

A clean read-only scout started in `softwareco/infra/issue-tracker` on local `main` without the controller conversation. It used only repo-local `README.md` / `AGENTS.md` guidance and documented read-only commands to determine:

1. canonical authority and projection boundaries;
2. tracker/manifests/authored-body coherence;
3. the next sequencer action and truthful readiness class;
4. whether any AK or GitHub mutation was authorized or performed;
5. the escalation/manual path.

The scout was forbidden from running apply, rebuild, sync/import, `gh`, push, comments, publication, full CI, or any mutation.

## Measurements

| Metric | Result |
|---|---:|
| start | `2026-07-20T18:28:46Z` |
| end | `2026-07-20T18:29:34Z` |
| elapsed | **48 seconds** |
| command/validation errors | **0** |
| manual repair steps | **0** |
| incorrect readiness claims | **0** |
| wrong-authority claims | **0** |
| external GitHub effects | **0** |
| canonical AK mutations | **0** |
| persistent workspace mutations | **0** |
| confidence | **97/100** |

The confidence reduction reflects the intentional absence of a live GitHub query and the distinction between structural/reference validation and complete semantic equivalence of every body.

## Raw scout report

> **VERDICT:** contract-coherent but operationally blocked on canonical reconciliation/manual authority; not review-ready or submission-ready. Measured start `2026-07-20T18:28:46Z`; end `2026-07-20T18:29:34Z`; elapsed 48s.
>
> **Authority:** README says canonical live truth is `~/ai-society/society.v2.db` via `ak issue`; repo markdown/manifests are Git-authored inputs; `STATE.json` is compatibility projection and loses to DB on disagreement. AGENTS says delegation is bounded by accepted Decision 68/CTO charter and missing/ambiguous authority fails closed. External issues/comments/push/publication and terminal decisions require explicit accountable-human authority.
>
> **Coherence:** `./scripts/validate-tracker-contract.sh` EXIT 0: checked-in `STATE.json` and all default manifests passed structural/file-reference checks. Dry-run EXIT 0 also exported canonical AK state to a temporary projection and validated it with `frankensqlite-sequence.json`/authored body references. However, operational cursor/status are unreconciled: canonical sequence has `next_index=0`, `halted=false`, no prior cursor event, while candidate 0 already has `gh_issue #30` and status `submitted`. Thus artifacts satisfy contract but sequence is not ready to advance automatically.
>
> **Current action/readiness:** runner states: `reconcile/dedupe canonical issue #30 (status=submitted) through a separately authorized procedure.` Classification: BLOCKED for canary execution/external effect, not review-ready and not submission-ready. `halted=false` is cursor data, not authorization/readiness. Incorrect readiness claims observed: 0; claiming validation means submission-ready would itself be incorrect.
>
> **Effects/authority metrics:** external GitHub effects 0; canonical AK mutations 0; persistent workspace mutations 0; wrong-authority claims 0. Final `git status --short --branch` remained `## main`; no `.issue-state.*.json` leftovers. Runner’s permitted temporary export was cleaned. No `gh`, apply, import/sync, push, comment, publication, or CI invoked.
>
> **Escalation/manual path:** accountable human must explicitly authorize a separately reviewed reconciliation/dedupe procedure for existing #30; that procedure should reconcile cursor/canonical issue identity, then rerun the same dry-run. The allowed docs do not specify an executable reconciliation command, so do not improvise one. Expected impact: canonical cursor aligns with already-submitted issue and the runner can truthfully classify the following item. Risk: an import/apply could overwrite authority or advance incorrectly; rollback posture is fail closed and make no effect until procedure/approval are reviewed.
>
> **Evidence files:** `README.md`, `AGENTS.md`, `STATE.json`, `frankensqlite-sequence.json`, `scripts/validate-tracker-contract.sh`, `scripts/issue-sequence-runner.sh`. Commands: UTC date/elapsed; `git status --short --branch`; `git rev-parse HEAD`=`518ab43777af2c6bed4232db6a8beeb4a7013fe0`; `git log -1`=`518ab43`; validator; runner `--manifest ./frankensqlite-sequence.json --dry-run`; documented read-only `./scripts/issue-sequence-status.sh --format json frankensqlite-dolt-equivalence-sequence`; leftover-temp check. Command/validation errors: 0.
>
> **Confidence 97/100:** direct local-main files, passing validators, and canonical AK-backed status agree; reduced 3 points because GitHub was intentionally not queried and validation establishes structural/reference coherence, not full semantic equivalence of every body.
>
> **Concrete controller action:** obtain human decision on reviewed reconciliation/dedupe for #30, execute only via an approved manual path, then repeat dry-run. What not to try again: do not use `--apply`, `--rebuild-state`, sync/import, raw GitHub mutation, self-authored approval receipts, or infer readiness from validation alone.

## Controller verification

Intercom supervision recorded exactly one `PEER_ACK`, exactly one `PEER_FINAL`, zero duplicate acknowledgements/finals, and zero protocol violations for `scoutpeer-mrtk5n7j-b8934ad1`. AK evidence `#4976` records the peer identity, timestamps, metrics, classification, protocol counts, and tested commit. No controller coaching was sent after acknowledgement.

## Evidence and commands

Files consulted:

- `README.md`
- `AGENTS.md`
- `STATE.json`
- `frankensqlite-sequence.json`
- `scripts/validate-tracker-contract.sh`
- `scripts/issue-sequence-runner.sh`

Commands included:

```bash
git status --short --branch
./scripts/validate-tracker-contract.sh
./scripts/issue-sequence-runner.sh \
  --manifest ./frankensqlite-sequence.json \
  --dry-run
./scripts/issue-sequence-status.sh \
  --format json \
  frankensqlite-dolt-equivalence-sequence
```

The scout observed local `main` at `518ab43777af2c6bed4232db6a8beeb4a7013fe0`. The tracker validator and dry-run exited zero. No temporary `.issue-state.*.json` remained and final Git status stayed clean on `main`.

## Authority conclusion

- Canonical live issue and sequence state: `~/ai-society/society.v2.db` through `ak issue`.
- Git-authored inputs: issue markdown bodies and sequence manifests.
- Compatibility projection: `STATE.json`; it loses to AK on disagreement.
- Missing or ambiguous delegation fails closed.
- External issue actions, pushes/publication, and terminal decisions require explicit accountable-human authority.

## Readiness conclusion

The checked-in projection, default manifests, and authored-file references are contract-coherent. The canonical cursor is nevertheless unreconciled:

- sequence `next_index=0`;
- sequence `halted=false`;
- candidate index 0 already has `gh_issue=#30` and status `submitted`;
- no prior canonical cursor event establishes safe advancement.

The documented runner therefore reported:

> reconcile/dedupe canonical issue #30 (status=submitted) through a separately authorized procedure.

Truthful classification: **blocked** for canary execution or external effect; **not review-ready** and **not submission-ready**. `halted=false` is cursor data, not authorization or readiness.

## Escalation path

The accountable human must decide whether to authorize a separately reviewed reconciliation/dedupe procedure for existing issue `#30`. That procedure must reconcile canonical cursor and issue identity before the same dry-run is repeated. Current operator docs intentionally do not provide an executable mutation command, so operators must not improvise one.

## Verdict

Cold-start discoverability and truthful blocked classification: **pass**.

End-to-end review-ready operator outcome: **not yet achieved**.

No rollback is required because no mutation occurred.
