#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${PI_MODES_PACKAGE_DIR:-$HOME/.pi/agent/npm/node_modules/@tryinget/pi-modes}"
mode_arg="${1:-}"

fail() { printf 'cto-operator-surface: FAIL: %s\n' "$*" >&2; exit 1; }
to_ns() { date -u -d "$1" +%s%N 2>/dev/null; }

case "$mode_arg" in
  --require-terminal|--require-active|--require-77-preactivation|--require-77-framework|--require-77-epoch-active|--require-77-epoch-inactive|--require-77-framework-terminal|--require-77-thesis-current|--require-77-objective-complete) ;;
  "") fail 'explicit check mode required' ;;
  *) fail "unknown mode: $mode_arg" ;;
esac

[[ -f "$package_dir/package.json" ]] || fail "immutable Pi Modes package missing"
[[ "$(node -p "require(process.argv[1]).version" "$package_dir/package.json")" == "0.3.0" ]] || fail "Pi Modes must be 0.3.0"

mode="$root/.pi/modes/softwareco-cto.json"
preset="$root/.pi/mode-presets/softwareco-cto.json"
prompt="$root/.pi/prompts/cto.md"
for path in "$mode" "$preset" "$prompt"; do [[ -f "$path" ]] || fail "missing ${path#$root/}"; done

lint_dir="$(mktemp -d)"; trap 'rm -rf "$lint_dir"' EXIT
cp -a "$package_dir"/. "$lint_dir"/
(cd "$lint_dir" && node ./scripts/mode-lint.mjs "$mode" "$preset") || fail "Pi Modes owner lint failed"

jq -e '
 .schemaVersion==2 and .key=="softwareco-cto" and .promptStrategy=="append" and
 (.systemPrompt|contains("Decision 74 is terminal")) and
 (.systemPrompt|contains("Decision 77 establishes a dormant framework")) and
 (.systemPrompt|contains("no CTO is appointed between epochs")) and
 (.systemPrompt|contains("zero-state sensing")) and
 (.systemPrompt|contains("Proved emptiness never supplies selection, admission, or execution consent")) and
 (.systemPrompt|contains("two admitted waves")) and
 (.systemPrompt|contains("six outstanding")) and
 (.systemPrompt|contains("A portfolio wrapper never mutates an owner task"))
' "$mode" >/dev/null || fail "mode contract mismatch"

for phrase in \
 'Decision 74 negative control' \
 'Decision 77 framework gate' \
 'Decision 77 epoch gate' \
 'No CTO is appointed between epochs' \
 'A fresh sensing worker is read-only' \
 'emptiness never supplies selection, admission, or execution consent' \
 'portfolio_thesis_v2' \
 'Owner selection and mutation gates' \
 'A wrapper never mutates owner-task lifecycle' \
 'Objective completion'; do
  grep -Fq "$phrase" "$prompt" || fail "prompt missing: $phrase"
done

# Decision 74 immutable negative control.
receipt74="$(ak governance show 8870 --json)"
jq -e '.status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:74" and .to_state=="complete" and .details.completed_wave=="IW-SF3-DMF-LOOP-IMPACT" and .details.outcome_evidence_ref=="evidence:5176"' <<<"$receipt74" >/dev/null || fail "Decision 74 terminal receipt mismatch"
sf3="$(ak direction show --repo "$root" SF3 --machine)"
terminal74='delegation_terminal_decision_74;terminal_action=complete;decided_at_utc=2026-07-25T13:19:10.466752718Z;governance_receipt_id=8870'
jq -e --arg d "$terminal74" '
 .payload.node.state=="active" and .payload.node.state_detail==$d and
 ([.payload.children[]|select(.key=="IW-SF3-DMF-LOOP-IMPACT" and .state=="done" and (.state_detail|contains("outcome_evidence_id=5176")))]|length==1) and
 ([.payload.task_links[]|select((.link.task_id==4156 or .link.task_id==4184 or .link.task_id==4191 or .link.task_id==4199) and .link.link_role=="completed_by")]|length==4) and
 ([.payload.task_links[]|select(.link.task_id==4182 and .link.link_role=="existing_anchor")]|length==1)
' <<<"$sf3" >/dev/null || fail "Decision 74 direction terminal mismatch"
controller74="$(ak task show 4182 --machine)"
jq -e '.payload.task.status=="done" and .payload.task.result.terminal_receipt_id==8870' <<<"$controller74" >/dev/null || fail "Decision 74 controller mismatch"

if [[ "$mode_arg" == --require-terminal ]]; then
  ak direction check --repo "$root" --json | jq -e '.ok==true and (.issues|length==0)' >/dev/null || fail "direction topology invalid"
  printf 'cto-operator-surface: PASS (Decision 74 terminal; receipt=8870; outcome_evidence=5176)\n'
  exit 0
fi
if [[ "$mode_arg" == --require-active ]]; then
  fail "Decision 74 is terminal and has no active delegation"
fi

# Decision 77 accepted dormant framework.
accept77="$(ak governance show 8932 --json)"
jq -e '
 .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and
 .agreement_ref=="decision:77" and .from_state=="decision_pending" and .to_state=="accepted" and
 .details.schema=="softwareco.architecture-decision-acceptance.v1" and .details.decision_id==77 and
 .details.outcome=="accepted" and .details.rfc_commit=="d2a372e388a990231160e1d8bd9b0360d10ab262" and
 .details.epoch_authorized==false
' <<<"$accept77" >/dev/null || fail "Decision 77 acceptance receipt mismatch"
ak decision get 77 --machine | jq -e '.payload.decision.state=="unblocked" and .payload.decision.outcome=="accepted" and .payload.decision.evidence_ref=="governance:8932"' >/dev/null || fail "Decision 77 is not accepted/unblocked"

accepted77="$(jq -r '.details.accepted_at_utc' <<<"$accept77")"
now_ns="$(date -u +%s%N)"; accepted_ns="$(to_ns "$accepted77")" || fail "invalid Decision 77 acceptance time"
initial_review_until_ns=$((accepted_ns + 2592000000000000))
review_until_ns=$initial_review_until_ns
review_head_id=null
review_receipts="$(ak governance list --concern softwareco-portfolio-cto:decision77:framework-review --limit 100 --json)"
applied_reviews="$(jq '[.[]|select(.status=="applied")]|sort_by(.id)' <<<"$review_receipts")"
if jq -e 'length>0' <<<"$applied_reviews" >/dev/null; then
  jq -e '
   . as $a | to_entries | all(. as $e |
    $e.value.source_authority=="human-operator" and $e.value.actor=="human-operator" and
    $e.value.agreement_ref=="decision:77" and $e.value.repo_scope=="/home/tryinget/ai-society/softwareco" and
    $e.value.consent_mode=="explicit" and ($e.value.evidence_ref|type=="string" and length>0) and
    $e.value.details.schema=="softwareco.portfolio-cto-framework-review.v1" and $e.value.details.decision_id==77 and
    ($e.value.details.reviewed_at_utc|type=="string" and length>0) and ($e.value.details.valid_until_utc|type=="string" and length>0) and
    ($e.value.from_state==(if $e.key==0 then "review_due" else $a[$e.key-1].to_state end)) and
    ($e.value.to_state=="framework_valid" or $e.value.to_state=="framework_paused") and
    ($e.value.details.prior_review_receipt_id==(if $e.key==0 then null else $a[$e.key-1].id end)) and
    (($e.value.to_state=="framework_valid" and $e.value.details.outcome=="continue_framework") or ($e.value.to_state=="framework_paused" and $e.value.details.outcome=="pause_framework"))
   )
  ' <<<"$applied_reviews" >/dev/null || fail "framework review chain invalid"
  while IFS=$'\t' read -r reviewed valid; do
    reviewed_ns="$(to_ns "$reviewed")" || fail "invalid framework reviewed_at"
    valid_ns="$(to_ns "$valid")" || fail "invalid framework valid_until"
    (( valid_ns > reviewed_ns && valid_ns-reviewed_ns <= 2592000000000000 )) || fail "framework review duration exceeds 30 days"
  done < <(jq -r '.[]|[.details.reviewed_at_utc,.details.valid_until_utc]|@tsv' <<<"$applied_reviews")
  review_head="$(jq '.[-1]' <<<"$applied_reviews")"
  review_head_id="$(jq -r '.id' <<<"$review_head")"
  jq -e '.to_state=="framework_valid" and .details.outcome=="continue_framework"' <<<"$review_head" >/dev/null || fail "framework review is paused"
  review_until="$(jq -r '.details.valid_until_utc' <<<"$review_head")"; review_until_ns="$(to_ns "$review_until")" || fail "invalid framework review expiry"
fi
(( now_ns >= accepted_ns && now_ns < review_until_ns )) || fail "Decision 77 framework review window is not valid"

projection="$(ak direction show --repo "$root" IW-SF3-CTO77-RECURRING --machine)"
jq -e '
 .payload.node.kind=="work_wave" and .payload.node.parent_key=="SF3" and
 (.payload.node.state=="pending" or .payload.node.state=="active") and
 (.payload.node.state_detail|startswith("decision77_recurring_framework;")) and
 ([.payload.decision_links[]|select(.link.decision_id==77 and .link.link_role=="governs")]|length==1)
' <<<"$projection" >/dev/null || fail "Decision 77 direction projection mismatch"

for concern in softwareco-portfolio-cto:decision77:revocation softwareco-portfolio-cto:decision77:terminal softwareco-portfolio-cto:decision77:supersession; do
  ak governance list --concern "$concern" --limit 100 --json | jq -e '[.[]|select(.status=="applied")]|length==0' >/dev/null || fail "Decision 77 terminating event exists: $concern"
done

for doc in docs/org/cto-agent-charter.md docs/org/governance.md docs/org/operating_model.md; do
  grep -Fqx 'status: "accepted_framework_no_epoch"' "$root/$doc" || fail "$doc projection mismatch"
  grep -Fq 'Decision 77' "$root/$doc" || fail "$doc missing Decision 77"
done

epoch_receipts="$(ak governance list --concern softwareco-portfolio-cto:decision77:epoch-index --limit 100 --json)"
applied_epochs="$(jq '[.[]|select(.status=="applied")]|sort_by(.id)' <<<"$epoch_receipts")"
if jq -e 'length>0' <<<"$applied_epochs" >/dev/null; then
  jq -e --argjson review_head_id "$review_head_id" '
   . as $a | to_entries | all(. as $e |
    $e.value.agreement_ref=="decision:77" and $e.value.repo_scope=="/home/tryinget/ai-society/softwareco" and
    ($e.value.details.prior_epoch_receipt_id==(if $e.key==0 then null else $a[$e.key-1].id end)) and
    ($e.value.from_state==(if $e.key==0 then "inactive" else $a[$e.key-1].to_state end)) and
    (if ($e.value.to_state|startswith("epoch:")) then
      $e.value.source_authority=="human-operator" and $e.value.actor=="human-operator" and
      $e.value.consent_mode=="explicit" and ($e.value.evidence_ref|type=="string" and length>0) and
      $e.value.details.schema=="softwareco.portfolio-cto-epoch-authorization.v1" and $e.value.details.decision_id==77 and
      $e.value.task_id==$e.value.details.controller_task_id and ($e.value.details.claimant_id|type=="string" and length>0) and
      $e.value.details.jurisdiction=="softwareco/owned" and ($e.value.details.evidence_refs|type=="array" and length>0) and
      $e.value.details.framework_review_receipt_id==$review_head_id and
      ($e.value.details.authorized_at_utc|type=="string" and length>0) and ($e.value.details.authorization_expires_at_utc|type=="string" and length>0) and
      $e.value.details.lease_seconds>0 and $e.value.details.lease_seconds<=14400 and $e.value.to_state==("epoch:"+$e.value.details.epoch_id)
     else
      $e.value.to_state=="inactive" and ($e.value.evidence_ref|type=="string" and length>0) and
      $e.value.details.schema=="softwareco.portfolio-cto-epoch-handback.v1" and $e.value.details.decision_id==77 and
      $e.value.details.epoch_id==($e.value.from_state|sub("^epoch:";"")) and
      $e.value.task_id==$e.value.details.controller_task_id and $e.value.details.controller_task_id==$a[$e.key-1].details.controller_task_id and
      ($e.value.details.handed_back_at_utc|type=="string" and length>0) and
      ($e.value.details.wip_handoff_refs|type=="array") and ($e.value.details.external_effects|type=="number") and
      (($e.value.source_authority=="human-operator" and $e.value.actor=="human-operator") or
       ($e.value.source_authority=="decision77-epoch-controller" and $e.value.actor==$a[$e.key-1].details.claimant_id))
     end)
   )
  ' <<<"$applied_epochs" >/dev/null || fail "epoch-index chain invalid"
  while IFS=$'\t' read -r authorized expires lease; do
    [[ "$authorized" != "-" ]] || continue
    authorized_ns="$(to_ns "$authorized")" || fail "invalid historical epoch authorization"
    expires_ns="$(to_ns "$expires")" || fail "invalid historical epoch expiry"
    (( expires_ns-authorized_ns == lease*1000000000 )) || fail "historical epoch duration mismatch"
  done < <(jq -r '.[]|if (.to_state|startswith("epoch:")) then [.details.authorized_at_utc,.details.authorization_expires_at_utc,(.details.lease_seconds|tostring)] else ["-","-","0"] end|@tsv' <<<"$applied_epochs")
  while IFS= read -r handed_back; do
    [[ "$handed_back" != "-" ]] || continue
    to_ns "$handed_back" >/dev/null || fail "invalid epoch handback timestamp"
  done < <(jq -r '.[]|if .to_state=="inactive" then .details.handed_back_at_utc else "-" end' <<<"$applied_epochs")
fi

if [[ "$mode_arg" == --require-77-framework ]]; then
  ak direction check --repo "$root" --json | jq -e '.ok==true and (.issues|length==0)' >/dev/null || fail "direction topology invalid"
  printf 'cto-operator-surface: PASS (Decision 77 framework valid; receipt=8932)\n'
  exit 0
fi
if [[ "$mode_arg" == --require-77-preactivation || "$mode_arg" == --require-77-epoch-inactive ]]; then
  jq -e 'length==0 or (.[-1].to_state=="inactive")' <<<"$applied_epochs" >/dev/null || fail "an active or ambiguous Decision 77 epoch exists"
  ak direction check --repo "$root" --json | jq -e '.ok==true and (.issues|length==0)' >/dev/null || fail "direction topology invalid"
  printf 'cto-operator-surface: PASS (Decision 77 framework accepted; epoch inactive; receipt=8932)\n'
  exit 0
fi

if [[ "$mode_arg" == --require-77-epoch-active ]]; then
  jq -e 'length>0 and (.[-1].to_state|startswith("epoch:"))' <<<"$applied_epochs" >/dev/null || fail "no active epoch-index head"
  epoch="$(jq '.[-1]' <<<"$applied_epochs")"
  jq -e '
   .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .from_state=="inactive" and (.to_state|startswith("epoch:")) and .consent_mode=="explicit" and
   (.evidence_ref|type=="string" and length>0) and .details.schema=="softwareco.portfolio-cto-epoch-authorization.v1" and
   .details.decision_id==77 and .details.lease_seconds>0 and .details.lease_seconds<=14400
  ' <<<"$epoch" >/dev/null || fail "epoch authorization mismatch"
  controller_id="$(jq -r '.details.controller_task_id' <<<"$epoch")"; claimant="$(jq -r '.details.claimant_id' <<<"$epoch")"
  jq -e --argjson cid "$controller_id" '.task_id==$cid and .details.controller_task_id==$cid and .repo_scope=="/home/tryinget/ai-society/softwareco"' <<<"$epoch" >/dev/null || fail "epoch controller/receipt identity mismatch"
  authorized="$(jq -r '.details.authorized_at_utc' <<<"$epoch")"; authorized_ns="$(to_ns "$authorized")" || fail "invalid epoch authorization time"
  expires="$(jq -r '.details.authorization_expires_at_utc' <<<"$epoch")"; expires_ns="$(to_ns "$expires")" || fail "invalid epoch expiry"
  lease="$(jq -r '.details.lease_seconds' <<<"$epoch")"
  (( expires_ns-authorized_ns == lease*1000000000 && now_ns >= authorized_ns && now_ns < expires_ns && expires_ns <= review_until_ns )) || fail "epoch duration/expiry invalid"
  controller="$(ak task show "$controller_id" --machine)"
  jq -e --arg c "$claimant" '.payload.task.status=="claimed" and .payload.task.claimed_by==$c and .payload.task.scope.allowed_paths==[] and .payload.task.scope.required_paths==[] and .payload.task.scope.forbidden_paths==["**"]' <<<"$controller" >/dev/null || fail "epoch controller mismatch"
  claimed_at="$(jq -r '.payload.task.claimed_at' <<<"$controller")"; claimed_at_ns="$(to_ns "$claimed_at")" || fail "invalid controller claim time"
  claim_exp="$(jq -r '.payload.task.lease_expires_at' <<<"$controller")"; claim_exp_ns="$(to_ns "$claim_exp")" || fail "invalid controller expiry"
  (( claimed_at_ns >= authorized_ns && now_ns < claim_exp_ns && claim_exp_ns <= expires_ns )) || fail "controller lease invalid"
  printf 'cto-operator-surface: PASS (Decision 77 epoch active; claimant=%s; controller=%s)\n' "$claimant" "$controller_id"
  exit 0
fi

if [[ "$mode_arg" == --require-77-framework-terminal ]]; then
  fail "Decision 77 framework has no terminal/revocation/supersession receipt"
elif [[ "$mode_arg" == --require-77-thesis-current ]]; then
  detail="$(jq -r '.payload.node.state_detail' <<<"$projection")"
  [[ "$detail" != *'thesis_head_evidence_id=none'* ]] || fail "Decision 77 thesis head does not exist"
  fail "Decision 77 thesis validation requires recorded thesis evidence"
elif [[ "$mode_arg" == --require-77-objective-complete ]]; then
  fail "Decision 77 recurrence objective evidence does not exist"
fi
fail "unhandled mode: $mode_arg"
