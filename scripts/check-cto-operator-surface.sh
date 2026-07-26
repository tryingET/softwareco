#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${PI_MODES_PACKAGE_DIR:-$HOME/.pi/agent/npm/node_modules/@tryinget/pi-modes}"
mode_arg="${1:-}"

fail() { printf 'cto-operator-surface: FAIL: %s\n' "$*" >&2; exit 1; }
to_ns() { date -u -d "$1" +%s%N 2>/dev/null; }
to_ns_strict() {
  [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{9}Z$ ]] || return 1
  to_ns "$1"
}

# Emit the applied epoch-index receipts in predecessor order. The raw query uses
# 101 as an overflow sentinel because AK has no applied-only count surface.
validate_epoch_graph() {
  python3 -c '
import json, sys
rows = json.load(sys.stdin)
if len(rows) >= 101:
    raise SystemExit("epoch-index overflow sentinel reached")
applied = [row for row in rows if row.get("status") == "applied"]
if not applied:
    print("[]")
    raise SystemExit(0)
by_id = {row.get("id"): row for row in applied}
if len(by_id) != len(applied):
    raise SystemExit("duplicate epoch-index receipt id")
roots = [row for row in applied if row.get("details", {}).get("prior_epoch_receipt_id") is None]
if len(roots) != 1:
    raise SystemExit("epoch-index must have exactly one root")
successors = {}
for row in applied:
    prior = row.get("details", {}).get("prior_epoch_receipt_id")
    if prior is None:
        continue
    if prior not in by_id:
        raise SystemExit("epoch-index predecessor missing")
    if prior in successors:
        raise SystemExit("epoch-index fork")
    successors[prior] = row["id"]
ordered, seen, current = [], set(), roots[0]["id"]
while current is not None:
    if current in seen:
        raise SystemExit("epoch-index cycle")
    seen.add(current)
    ordered.append(by_id[current])
    current = successors.get(current)
if len(seen) != len(applied):
    raise SystemExit("epoch-index has unreachable receipts")
heads = [row for row in applied if row["id"] not in successors]
if len(heads) != 1:
    raise SystemExit("epoch-index must have exactly one head")
json.dump(ordered, sys.stdout, separators=(",", ":"))
'
}

validate_d79_controller() {
  jq -e '
   .payload.task.status=="pending" and .payload.task.claimed_by==null and .payload.task.claimed_at==null and
   .payload.task.lease_expires_at==null and .payload.task.entity_version==1 and
   .payload.task.scope.allowed_paths==[] and .payload.task.scope.required_paths==[] and .payload.task.scope.forbidden_paths==["**"] and
   .payload.task.active_deferral.id==182 and .payload.task.active_deferral.state=="active" and
   .payload.task.active_deferral.kind=="until_decision" and .payload.task.active_deferral.trigger_ref=="decision:79" and
   .payload.task.active_deferral.defer_until==null and .payload.task.active_deferral.resolved_at==null and
   .payload.task.active_deferral.reason=="Receipt 8967 exceeds Decision 77 hard epoch maximum; controller is quarantined pending accepted Decision 79 recovery and explicit human invalidation."
  '
}

validate_d79_invalidation_pair() {
  jq -e '
   length>=2 and .[0].id==8967 and .[0].details.epoch_id=="d77-e1-20260725" and
   .[0].details.controller_task_id==4220 and .[0].details.claimant_id=="pi-session-softwareco-cto-d77-epoch1" and
   .[0].details.authorized_at_utc=="2026-07-26T02:42:39.056097206Z" and
   .[0].details.authorization_expires_at_utc=="2026-07-26T06:42:39.057171386Z" and
   .[1].id>8973 and .[1].concern=="softwareco-portfolio-cto:decision77:epoch-index" and .[1].status=="applied" and
   (.[1].created_at|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{9}\\+00:00$")) and
   .[1].source_authority=="human-operator" and .[1].actor=="human-operator" and
   .[1].agreement_ref=="decision:77" and .[1].from_state=="epoch:d77-e1-20260725" and .[1].to_state=="inactive" and
   .[1].consent_mode=="explicit" and .[1].evidence_ref=="evidence:5309" and .[1].task_id==4220 and
   .[1].repo_scope=="/home/tryinget/ai-society/softwareco" and
   .[1].details.schema=="softwareco.portfolio-cto-epoch-invalidation.v1" and
   (.[1].details.invalidated_at_utc|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{9}Z$")) and
   .[1].details.decision_id==77 and .[1].details.amendment_decision_id==79 and
   .[1].details.amendment_acceptance_receipt_id==8973 and .[1].details.invalidated_receipt_id==8967 and
   .[1].details.epoch_id=="d77-e1-20260725" and .[1].details.controller_task_id==4220 and
   .[1].details.claimant_id=="pi-session-softwareco-cto-d77-epoch1" and
   .[1].details.reason=="authorization_interval_exceeds_hard_maximum" and
   .[1].details.observed_interval_ns==14400001074180 and .[1].details.declared_lease_seconds==14400 and
   .[1].details.excess_ns==1074180 and .[1].details.controller_entity_version==1 and
   .[1].details.controller_claim_fields_null==true and .[1].details.controller_quarantine_deferral_id==182 and
   .[1].details.zero_operation_evidence_id==5309 and .[1].details.authority_dependent_effects==0 and
   .[1].details.external_effects_attested==0 and .[1].details.wip_handoff_refs==[] and
   .[1].details.prior_epoch_receipt_id==8967 and
   .[1].details.evidence_refs==["governance:8967","task:4220@entity-version:1","decision:79","governance:8973","evidence:5309"]
  '
}

validate_d79_raw_candidates() {
  jq -e '
   ([.[]|select(.details.schema?=="softwareco.portfolio-cto-epoch-invalidation.v1")]|length)<=1 and
   all(.[]|select(.details.schema?=="softwareco.portfolio-cto-epoch-invalidation.v1"); .status=="applied")
  '
}

validate_d79_retired_identities() {
  jq -e 'all(.[]; if (.to_state|startswith("epoch:")) and .id!=8967 then .details.epoch_id!="d77-e1-20260725" and .details.controller_task_id!=4220 and .details.claimant_id!="pi-session-softwareco-cto-d77-epoch1" else true end)'
}

validate_active_controller() {
  local claimant="$1"
  jq -e --arg c "$claimant" '
   .payload.task.status=="claimed" and .payload.task.claimed_by==$c and
   .payload.task.scope.allowed_paths==[] and .payload.task.scope.required_paths==[] and
   .payload.task.scope.forbidden_paths==["**"] and
   (.payload.task.claimed_at|type=="string") and (.payload.task.lease_expires_at|type=="string")
  '
}

validate_d79_zero_evidence() {
  jq -e '
   .task_id==4226 and .check_type=="decision77_invalid_epoch_zero_operation" and .result=="pass" and
   .details.schema=="softwareco.decision77-invalid-epoch-zero-operation.v1" and
   .details.decision_id==79 and .details.amends_decision_id==77 and
   .details.malformed_receipt_id==8967 and .details.acceptance_receipt_id==8973 and
   .details.controller_task_id==4220 and .details.controller_entity_version==1 and
   .details.controller_claim_fields_null==true and .details.controller_quarantine_deferral_id==182 and
   .details.controller_evidence_count==0 and .details.objective_task_id==4221 and
   .details.objective_evidence_count==0 and .details.thesis_head_evidence_id==null and
   .details.decision77_child_keys==["IW-SF3-CTO77-RECURRING"] and
   .details.decision77_owner_wave_receipt_count==0 and .details.epoch_index_receipt_ids==[8967] and
   .details.authority_dependent_effects==0 and .details.off_system_effects=="direct-human-attested-zero-in-governance:8973"
  '
}

self_test_77_recovery() {
  local valid fork gap cycle overflow controller pair bad replacement zero
  valid='[{"id":1,"status":"applied","details":{"prior_epoch_receipt_id":null}},{"id":2,"status":"applied","details":{"prior_epoch_receipt_id":1}}]'
  fork='[{"id":1,"status":"applied","details":{"prior_epoch_receipt_id":null}},{"id":2,"status":"applied","details":{"prior_epoch_receipt_id":1}},{"id":3,"status":"applied","details":{"prior_epoch_receipt_id":1}}]'
  gap='[{"id":1,"status":"applied","details":{"prior_epoch_receipt_id":null}},{"id":2,"status":"applied","details":{"prior_epoch_receipt_id":99}}]'
  cycle='[{"id":1,"status":"applied","details":{"prior_epoch_receipt_id":null}},{"id":2,"status":"applied","details":{"prior_epoch_receipt_id":3}},{"id":3,"status":"applied","details":{"prior_epoch_receipt_id":2}}]'
  validate_epoch_graph <<<"$valid" >/dev/null || return 1
  ! validate_epoch_graph <<<"$fork" >/dev/null 2>&1 || return 1
  ! validate_epoch_graph <<<"$gap" >/dev/null 2>&1 || return 1
  ! validate_epoch_graph <<<"$cycle" >/dev/null 2>&1 || return 1
  overflow="$(jq -nc '[range(0;101)|{id:(.+1),status:"ignored",details:{prior_epoch_receipt_id:null}}]')"
  ! validate_epoch_graph <<<"$overflow" >/dev/null 2>&1 || return 1

  controller='{"payload":{"task":{"status":"pending","claimed_by":null,"claimed_at":null,"lease_expires_at":null,"entity_version":1,"scope":{"allowed_paths":[],"required_paths":[],"forbidden_paths":["**"]},"active_deferral":{"id":182,"state":"active","kind":"until_decision","trigger_ref":"decision:79","defer_until":null,"resolved_at":null,"reason":"Receipt 8967 exceeds Decision 77 hard epoch maximum; controller is quarantined pending accepted Decision 79 recovery and explicit human invalidation."}}}}'
  validate_d79_controller <<<"$controller" >/dev/null || return 1
  bad="$(jq '.payload.task.entity_version=2' <<<"$controller")"
  ! validate_d79_controller <<<"$bad" >/dev/null 2>&1 || return 1
  bad="$(jq '.payload.task.active_deferral.state="resolved"' <<<"$controller")"
  ! validate_d79_controller <<<"$bad" >/dev/null 2>&1 || return 1

  zero='{"task_id":4226,"check_type":"decision77_invalid_epoch_zero_operation","result":"pass","details":{"schema":"softwareco.decision77-invalid-epoch-zero-operation.v1","decision_id":79,"amends_decision_id":77,"malformed_receipt_id":8967,"acceptance_receipt_id":8973,"controller_task_id":4220,"controller_entity_version":1,"controller_claim_fields_null":true,"controller_quarantine_deferral_id":182,"controller_evidence_count":0,"objective_task_id":4221,"objective_evidence_count":0,"thesis_head_evidence_id":null,"decision77_child_keys":["IW-SF3-CTO77-RECURRING"],"decision77_owner_wave_receipt_count":0,"epoch_index_receipt_ids":[8967],"authority_dependent_effects":0,"off_system_effects":"direct-human-attested-zero-in-governance:8973"}}'
  validate_d79_zero_evidence <<<"$zero" >/dev/null || return 1
  ! validate_d79_zero_evidence <<<"$(jq '.details.thesis_head_evidence_id=999' <<<"$zero")" >/dev/null 2>&1 || return 1
  ! validate_d79_zero_evidence <<<"$(jq '.details.decision77_owner_wave_receipt_count=1' <<<"$zero")" >/dev/null 2>&1 || return 1
  ! validate_d79_zero_evidence <<<"$(jq '.details.authority_dependent_effects=1' <<<"$zero")" >/dev/null 2>&1 || return 1

  pair="$(jq -nc '[
    {id:8967,status:"applied",from_state:"inactive",to_state:"epoch:d77-e1-20260725",details:{prior_epoch_receipt_id:null,epoch_id:"d77-e1-20260725",controller_task_id:4220,claimant_id:"pi-session-softwareco-cto-d77-epoch1",authorized_at_utc:"2026-07-26T02:42:39.056097206Z",authorization_expires_at_utc:"2026-07-26T06:42:39.057171386Z"}},
    {id:9000,concern:"softwareco-portfolio-cto:decision77:epoch-index",status:"applied",created_at:"2026-07-26T03:30:01.000000000+00:00",source_authority:"human-operator",actor:"human-operator",agreement_ref:"decision:77",from_state:"epoch:d77-e1-20260725",to_state:"inactive",consent_mode:"explicit",evidence_ref:"evidence:5309",task_id:4220,repo_scope:"/home/tryinget/ai-society/softwareco",details:{schema:"softwareco.portfolio-cto-epoch-invalidation.v1",invalidated_at_utc:"2026-07-26T03:30:00.000000000Z",decision_id:77,amendment_decision_id:79,amendment_acceptance_receipt_id:8973,invalidated_receipt_id:8967,epoch_id:"d77-e1-20260725",controller_task_id:4220,claimant_id:"pi-session-softwareco-cto-d77-epoch1",reason:"authorization_interval_exceeds_hard_maximum",observed_interval_ns:14400001074180,declared_lease_seconds:14400,excess_ns:1074180,controller_entity_version:1,controller_claim_fields_null:true,controller_quarantine_deferral_id:182,zero_operation_evidence_id:5309,authority_dependent_effects:0,external_effects_attested:0,wip_handoff_refs:[],prior_epoch_receipt_id:8967,evidence_refs:["governance:8967","task:4220@entity-version:1","decision:79","governance:8973","evidence:5309"]}}
  ]')"
  validate_d79_invalidation_pair <<<"$pair" >/dev/null || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[0:1]' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.prior_epoch_receipt_id=9999' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].from_state="epoch:wrong"' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.schema="softwareco.portfolio-cto-epoch-handback.v1"' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.amendment_decision_id=80' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].evidence_ref="evidence:wrong"' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.authority_dependent_effects=1' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.external_effects_attested=1' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_invalidation_pair <<<"$(jq '.[1].details.zero_operation_evidence_id=5310' <<<"$pair")" >/dev/null 2>&1 || return 1
  validate_d79_raw_candidates <<<"$pair" >/dev/null || return 1
  ! validate_d79_raw_candidates <<<"$(jq '.+.[1:2]' <<<"$pair")" >/dev/null 2>&1 || return 1
  ! validate_d79_raw_candidates <<<"$(jq '.[1].status="rejected"' <<<"$pair")" >/dev/null 2>&1 || return 1

  # State matrix: exact pair is recovered/inactive but not active. A distinct
  # replacement authorization is framework-valid, not inactive, and becomes
  # active only with a matching claimed controller (tested by production mode).
  jq -e '.[-1].to_state=="inactive"' <<<"$pair" >/dev/null || return 1
  replacement="$(jq '. + [{id:9001,status:"applied",from_state:"inactive",to_state:"epoch:d77-e2-fixture",details:{prior_epoch_receipt_id:9000,epoch_id:"d77-e2-fixture",controller_task_id:5000,claimant_id:"fixture-d77-e2"}}]' <<<"$pair")"
  validate_epoch_graph <<<"$replacement" >/dev/null || return 1
  validate_d79_retired_identities <<<"$replacement" >/dev/null || return 1
  ! validate_d79_retired_identities <<<"$(jq '.[-1].details.controller_task_id=4220' <<<"$replacement")" >/dev/null 2>&1 || return 1
  jq -e '.[-1].to_state=="epoch:d77-e2-fixture" and .[-1].details.epoch_id!="d77-e1-20260725" and .[-1].details.controller_task_id!=4220 and .[-1].details.claimant_id!="pi-session-softwareco-cto-d77-epoch1"' <<<"$replacement" >/dev/null || return 1
  bad='{"payload":{"task":{"status":"pending","claimed_by":null,"claimed_at":null,"lease_expires_at":null,"scope":{"allowed_paths":[],"required_paths":[],"forbidden_paths":["**"]}}}}'
  ! validate_active_controller fixture-d77-e2 <<<"$bad" >/dev/null 2>&1 || return 1
  bad='{"payload":{"task":{"status":"claimed","claimed_by":"fixture-d77-e2","claimed_at":"2026-07-26T03:31:00.000000000Z","lease_expires_at":"2026-07-26T04:31:00.000000000Z","scope":{"allowed_paths":[],"required_paths":[],"forbidden_paths":["**"]}}}}'
  validate_active_controller fixture-d77-e2 <<<"$bad" >/dev/null || return 1
  printf 'cto-operator-surface: PASS (Decision 79 recovery graph, quarantine, and state fixtures)\n'
}

case "$mode_arg" in
  --require-terminal|--require-active|--require-77-preactivation|--require-77-framework|--require-77-epoch-active|--require-77-epoch-inactive|--require-77-framework-terminal|--require-77-thesis-current|--require-77-objective-complete|--self-test-77-recovery) ;;
  "") fail 'explicit check mode required' ;;
  *) fail "unknown mode: $mode_arg" ;;
esac

if [[ "$mode_arg" == --self-test-77-recovery ]]; then
  self_test_77_recovery || fail "Decision 79 recovery fixtures failed"
  exit 0
fi

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

# Decision 79 is a one-time, non-precedential amendment that can quarantine
# malformed receipt 8967 only after explicit human acceptance and invalidation.
accept79="$(ak governance show 8973 --json)"
jq -e '
 .id==8973 and .concern=="architecture-decision" and .status=="applied" and
 .source_authority=="human-operator" and .actor=="human-operator" and
 .mito_layer=="Design & Configuration" and .s3_domain_ref=="softwareco" and
 .agreement_ref=="decision:79" and .from_state=="decision_pending" and .to_state=="accepted" and
 .consent_mode=="explicit" and .evidence_ref=="git:698b293cce306c681155d07580ed6843ed9b17b9" and
 .rollback_ref=="docs/project/2026-07-26-softwareco-decision77-invalid-epoch-recovery-validation-rollout-rollback.md" and
 .task_id==4226 and .repo_scope=="/home/tryinget/ai-society/softwareco" and
 .details.schema=="softwareco.architecture-decision-amendment-acceptance.v1" and
 .details.decision_id==79 and .details.amends_decision_id==77 and .details.outcome=="accepted" and
 .details.rfc_commit=="0dc276f5e8208e251029d93c40ad704b30049eec" and
 .details.review_closure_commit=="19a872c2455ad4811d22538abb4c7c604f1b2f9e" and
 .details.adr_plan_commit=="698b293cce306c681155d07580ed6843ed9b17b9" and
 .details.accepted_at_utc=="2026-07-26T03:12:10.430629943Z" and
 .details.invalidated_receipt_id==8967 and .details.malformed_epoch_id=="d77-e1-20260725" and
 .details.malformed_controller_task_id==4220 and .details.controller_entity_version==1 and
 .details.controller_quarantine_deferral_id==182 and .details.observed_interval_ns==14400001074180 and
 .details.declared_lease_seconds==14400 and .details.excess_ns==1074180 and
 .details.zero_ak_authority_dependent_effects_attested==true and
 .details.zero_unenumerated_off_system_effects_attested==true and
 .details.invalidation_authorized==true and .details.epoch_authorized==false and .details.external_effects==0
' <<<"$accept79" >/dev/null || fail "Decision 79 acceptance receipt mismatch"
ak decision get 79 --machine | jq -e '.payload.decision.state=="unblocked" and .payload.decision.outcome=="accepted" and .payload.decision.evidence_ref=="governance:8973"' >/dev/null || fail "Decision 79 is not accepted/unblocked"

zero79="$(ak evidence show 5309 --json)"
validate_d79_zero_evidence <<<"$zero79" >/dev/null || fail "Decision 79 zero-operation evidence mismatch"

accepted79_at="$(jq -r '.details.accepted_at_utc' <<<"$accept79")"
accepted79_ns="$(to_ns_strict "$accepted79_at")" || fail "invalid Decision 79 acceptance timestamp"
zero79_at="$(jq -r '.details.observed_at_utc' <<<"$zero79")"
zero79_ns="$(to_ns_strict "$zero79_at")" || fail "invalid Decision 79 evidence timestamp"
(( zero79_ns > accepted79_ns )) || fail "Decision 79 evidence must strictly follow acceptance"

controller79="$(ak task show 4220 --machine)"
validate_d79_controller <<<"$controller79" >/dev/null || fail "Decision 79 controller quarantine drift"

malformed8967="$(ak governance show 8967 --json)"
jq -e '
 .id==8967 and .concern=="softwareco-portfolio-cto:decision77:epoch-index" and
 .source_authority=="human-operator" and .mito_layer=="Operations & Evaluation" and
 .s3_domain_ref=="softwareco/portfolio-cto" and .agreement_ref=="decision:77" and
 .from_state=="inactive" and .to_state=="epoch:d77-e1-20260725" and .guard_ref==null and
 .consent_mode=="explicit" and .evidence_ref=="evidence:5274" and
 .rollback_ref=="docs/project/2026-07-25-softwareco-recurring-portfolio-cto-validation-rollout-rollback.md" and
 .task_id==4220 and .repo_scope=="/home/tryinget/ai-society/softwareco" and
 .actor=="human-operator" and .status=="applied" and
 .created_at=="2026-07-26T02:42:40.202294225+00:00" and
 .details=={
   schema:"softwareco.portfolio-cto-epoch-authorization.v1",decision_id:77,
   epoch_id:"d77-e1-20260725",controller_task_id:4220,
   claimant_id:"pi-session-softwareco-cto-d77-epoch1",
   authorized_at_utc:"2026-07-26T02:42:39.056097206Z",
   authorization_expires_at_utc:"2026-07-26T06:42:39.057171386Z",
   lease_seconds:14400,jurisdiction:"softwareco/owned",prior_epoch_receipt_id:null,
   framework_review_receipt_id:null,evidence_refs:["governance:8932","evidence:5274"]
 }
' <<<"$malformed8967" >/dev/null || fail "receipt 8967 immutable payload mismatch"

epoch_receipts="$(ak governance list --concern softwareco-portfolio-cto:decision77:epoch-index --limit 101 --json)"
validate_d79_raw_candidates <<<"$epoch_receipts" >/dev/null || fail "malformed or duplicate Decision 79 invalidation candidate"
applied_epochs="$(validate_epoch_graph <<<"$epoch_receipts")" || fail "epoch-index graph invalid"
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
      ($e.value.details.framework_review_receipt_id==null or ($e.value.details.framework_review_receipt_id|type=="number")) and
      ($e.value.details.authorized_at_utc|type=="string" and length>0) and ($e.value.details.authorization_expires_at_utc|type=="string" and length>0) and
      $e.value.details.lease_seconds>0 and $e.value.details.lease_seconds<=14400 and $e.value.to_state==("epoch:"+$e.value.details.epoch_id)
    elif $e.value.details.schema=="softwareco.portfolio-cto-epoch-invalidation.v1" then
      $e.key==1 and $a[0].id==8967 and $e.value.id!=8967 and
      $e.value.concern=="softwareco-portfolio-cto:decision77:epoch-index" and
      $e.value.source_authority=="human-operator" and $e.value.actor=="human-operator" and
      $e.value.mito_layer=="Operations & Evaluation" and $e.value.s3_domain_ref=="softwareco/portfolio-cto" and
      $e.value.consent_mode=="explicit" and $e.value.evidence_ref=="evidence:5309" and
      $e.value.rollback_ref=="docs/project/2026-07-26-softwareco-decision77-invalid-epoch-recovery-validation-rollout-rollback.md" and
      $e.value.from_state=="epoch:d77-e1-20260725" and $e.value.to_state=="inactive" and $e.value.task_id==4220 and
      $e.value.details.decision_id==77 and $e.value.details.amendment_decision_id==79 and
      $e.value.details.amendment_acceptance_receipt_id==8973 and $e.value.details.epoch_id=="d77-e1-20260725" and
      $e.value.details.controller_task_id==4220 and $e.value.details.claimant_id=="pi-session-softwareco-cto-d77-epoch1" and
      $e.value.details.invalidated_receipt_id==8967 and $e.value.details.reason=="authorization_interval_exceeds_hard_maximum" and
      $e.value.details.observed_interval_ns==14400001074180 and $e.value.details.declared_lease_seconds==14400 and
      $e.value.details.excess_ns==1074180 and $e.value.details.controller_entity_version==1 and
      $e.value.details.controller_claim_fields_null==true and $e.value.details.controller_quarantine_deferral_id==182 and
      $e.value.details.zero_operation_evidence_id==5309 and $e.value.details.authority_dependent_effects==0 and
      $e.value.details.external_effects_attested==0 and $e.value.details.wip_handoff_refs==[] and
      ($e.value.details.invalidated_at_utc|type=="string" and length>0) and
      $e.value.details.evidence_refs==["governance:8967","task:4220@entity-version:1","decision:79","governance:8973","evidence:5309"]
    elif $e.value.to_state=="inactive" then
      ($e.value.evidence_ref|type=="string" and length>0) and
      $e.value.details.schema=="softwareco.portfolio-cto-epoch-handback.v1" and $e.value.details.decision_id==77 and
      $e.value.details.epoch_id==($e.value.from_state|sub("^epoch:";"")) and
      $e.value.task_id==$e.value.details.controller_task_id and $e.value.details.controller_task_id==$a[$e.key-1].details.controller_task_id and
      ($e.value.details.handed_back_at_utc|type=="string" and length>0) and
      ($e.value.details.wip_handoff_refs|type=="array") and ($e.value.details.external_effects|type=="number") and
      (($e.value.source_authority=="human-operator" and $e.value.actor=="human-operator") or
       ($e.value.source_authority=="decision77-epoch-controller" and $e.value.actor==$a[$e.key-1].details.claimant_id))
    else false end)
   )
  ' <<<"$applied_epochs" >/dev/null || fail "epoch-index chain invalid"

  invalidation_count="$(jq '[.[]|select(.details.schema=="softwareco.portfolio-cto-epoch-invalidation.v1")]|length' <<<"$applied_epochs")"
  (( invalidation_count <= 1 )) || fail "duplicate Decision 79 invalidation"
  quarantine_valid=false
  if (( invalidation_count == 1 )); then
    validate_d79_invalidation_pair <<<"$applied_epochs" >/dev/null || fail "Decision 79 invalidation is not exact immediate successor"
    invalidation_id="$(jq -r '.[1].id' <<<"$applied_epochs")"
    (( invalidation_id > 8973 )) || fail "Decision 79 invalidation receipt does not follow acceptance"
    invalidated_at="$(jq -r '.[1].details.invalidated_at_utc' <<<"$applied_epochs")"
    invalidated_ns="$(to_ns_strict "$invalidated_at")" || fail "invalid Decision 79 invalidation timestamp"
    invalidation_created_at="$(jq -r '.[1].created_at' <<<"$applied_epochs")"
    [[ "$invalidation_created_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{9}\+00:00$ ]] || fail "invalid Decision 79 receipt creation timestamp"
    invalidation_created_ns="$(to_ns "$invalidation_created_at")" || fail "invalid Decision 79 receipt creation timestamp"
    (( invalidated_ns > zero79_ns && zero79_ns > accepted79_ns && invalidation_created_ns >= invalidated_ns )) || fail "Decision 79 invalidation chronology mismatch"
    quarantine_valid=true
  fi

  while IFS=$'\t' read -r id authorized expires lease review_ref; do
    [[ "$authorized" != "-" ]] || continue
    authorized_ns="$(to_ns_strict "$authorized")" || fail "invalid historical epoch authorization"
    expires_ns="$(to_ns_strict "$expires")" || fail "invalid historical epoch expiry"
    (( authorized_ns >= accepted_ns && expires_ns <= review_until_ns )) || fail "historical epoch outside framework bounds"
    if [[ "$review_ref" == null ]]; then
      (( authorized_ns < initial_review_until_ns )) || fail "initial framework review did not cover authorization"
    else
      review_for_epoch="$(jq --argjson rid "$review_ref" '[.[]|select(.id==$rid)]|if length==1 then .[0] else null end' <<<"$applied_reviews")"
      [[ "$review_for_epoch" != null ]] || fail "authorization references missing framework review"
      epoch_reviewed_ns="$(to_ns_strict "$(jq -r '.details.reviewed_at_utc' <<<"$review_for_epoch")")" || fail "invalid referenced review start"
      epoch_review_until_ns="$(to_ns_strict "$(jq -r '.details.valid_until_utc' <<<"$review_for_epoch")")" || fail "invalid referenced review expiry"
      (( authorized_ns >= epoch_reviewed_ns && expires_ns <= epoch_review_until_ns )) || fail "referenced framework review did not cover epoch"
    fi
    if [[ "$quarantine_valid" == true && "$id" != 8967 ]]; then
      (( authorized_ns >= invalidated_ns )) || fail "replacement authorization predates invalidation"
    fi
    if (( expires_ns-authorized_ns != lease*1000000000 )); then
      [[ "$id" == 8967 && "$quarantine_valid" == true ]] || fail "historical epoch duration mismatch"
      (( expires_ns-authorized_ns == 14400001074180 )) || fail "receipt 8967 measured interval mismatch"
    fi
  done < <(jq -r '.[]|if (.to_state|startswith("epoch:")) then [(.id|tostring),.details.authorized_at_utc,.details.authorization_expires_at_utc,(.details.lease_seconds|tostring),(.details.framework_review_receipt_id|tostring)] else ["-","-","-","0","null"] end|@tsv' <<<"$applied_epochs")

  while IFS= read -r handback_at; do
    [[ "$handback_at" != "-" ]] || continue
    to_ns_strict "$handback_at" >/dev/null || fail "invalid epoch handback timestamp"
  done < <(jq -r '.[]|if .details.schema=="softwareco.portfolio-cto-epoch-handback.v1" then .details.handed_back_at_utc else "-" end' <<<"$applied_epochs")

  validate_d79_retired_identities <<<"$applied_epochs" >/dev/null || fail "retired Decision 79 identity reused"
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
  validate_active_controller "$claimant" <<<"$controller" >/dev/null || fail "epoch controller mismatch"
  claimed_at="$(jq -r '.payload.task.claimed_at' <<<"$controller")"; claimed_at_ns="$(to_ns "$claimed_at")" || fail "invalid controller claim time"
  claim_exp="$(jq -r '.payload.task.lease_expires_at' <<<"$controller")"; claim_exp_ns="$(to_ns "$claim_exp")" || fail "invalid controller expiry"
  (( claimed_at_ns >= authorized_ns && now_ns < claim_exp_ns && claim_exp_ns <= expires_ns )) || fail "controller lease invalid"
  printf 'cto-operator-surface: PASS (Decision 77 epoch active; claimant=%s; controller=%s)\n' "$claimant" "$controller_id"
  exit 0
fi

if [[ "$mode_arg" == --require-77-framework-terminal ]]; then
  fail "Decision 77 framework has no terminal/revocation/supersession receipt"
elif [[ "$mode_arg" == --require-77-thesis-current ]]; then
  TMPDIR="${TMPDIR:-$HOME/.cache/pi-cto-check-tmp}" "$0" --require-77-epoch-active >/dev/null 2>&1 || fail "Decision 77 active epoch prerequisite failed"
  detail="$(jq -r '.payload.node.state_detail' <<<"$projection")"
  [[ "$detail" =~ ^decision77_recurring_framework\;phase=([^\;]+)\;objective_task_id=([0-9]+)\;thesis_task_ids=([0-9]+(,[0-9]+)*)\;thesis_head_evidence_id=([0-9]+)$ ]] || fail "Decision 77 thesis projection detail invalid"
  objective_task_id="${BASH_REMATCH[2]}"
  thesis_task_ids_csv="${BASH_REMATCH[3]}"
  head_evidence_id="${BASH_REMATCH[5]}"
  [[ "$objective_task_id" == 4221 ]] || fail "Decision 77 objective task mismatch"
  IFS=, read -r -a thesis_task_ids <<<"$thesis_task_ids_csv"
  (( ${#thesis_task_ids[@]} > 0 && ${#thesis_task_ids[@]} <= 100 )) || fail "thesis task count invalid"
  [[ "$(printf '%s\n' "${thesis_task_ids[@]}" | sort -n -u | paste -sd, -)" == "$thesis_task_ids_csv" ]] || fail "thesis task IDs are not sorted unique"

  epoch="$(jq '.[-1]' <<<"$applied_epochs")"
  epoch_id="$(jq -r '.details.epoch_id' <<<"$epoch")"
  claimant="$(jq -r '.details.claimant_id' <<<"$epoch")"
  authorized_ns="$(to_ns_strict "$(jq -r '.details.authorized_at_utc' <<<"$epoch")")" || fail "invalid thesis epoch authorization"
  expires_ns="$(to_ns_strict "$(jq -r '.details.authorization_expires_at_utc' <<<"$epoch")")" || fail "invalid thesis epoch expiry"

  thesis_chain='[]'
  for thesis_task_id in "${thesis_task_ids[@]}"; do
    jq -e --argjson task "$thesis_task_id" '
     ([.payload.task_links[]|select(.link.task_id==$task and .link.link_role=="existing_anchor")]|length)==1
    ' <<<"$projection" >/dev/null || fail "thesis task link missing"
    thesis_task="$(ak task show "$thesis_task_id" --machine)"
    jq -e --argjson task "$thesis_task_id" --arg root "$root" '
     .payload.task.id==$task and .payload.task.repo==$root and
     .payload.task.scope.allowed_paths==["docs/learnings/2026-07-25-softwareco-recurring-portfolio-cto-*","docs/project/2026-07-25-softwareco-recurring-portfolio-cto-*","scripts/check-cto-operator-surface.sh"] and
     .payload.task.scope.required_paths==["docs/project/2026-07-25-softwareco-recurring-portfolio-cto-recurrence-evidence.md"] and
     .payload.task.scope.forbidden_paths==[]
    ' <<<"$thesis_task" >/dev/null || fail "thesis task scope invalid"
    thesis_collection="$(ak evidence task "$thesis_task_id" --machine)"
    thesis_chain="$(jq -n --argjson prior "$thesis_chain" --argjson collection "$thesis_collection" '
     $prior + [$collection.payload.evidence[]|select(.check_type=="portfolio_thesis_v2" and .result=="pass" and .details.schema=="softwareco.portfolio-thesis.v2" and .details.decision_id==77)]
    ')"
  done
  thesis_chain="$(jq 'sort_by(.details.revision)' <<<"$thesis_chain")"
  linked_task_ids="$(jq '[.payload.task_links[].link.task_id]|unique' <<<"$projection")"
  jq -e 'length<=500' <<<"$linked_task_ids" >/dev/null || fail "linked task census exceeds thesis orphan-check bound"
  while IFS= read -r linked_task_id; do
    [[ ",$thesis_task_ids_csv," == *",$linked_task_id,"* ]] && continue
    linked_collection="$(ak evidence task "$linked_task_id" --machine)"
    jq -e '[.payload.evidence[]|select(.check_type=="portfolio_thesis_v2" and .result=="pass" and .details.schema=="softwareco.portfolio-thesis.v2" and .details.decision_id==77)]|length==0' <<<"$linked_collection" >/dev/null || fail "thesis evidence exists on an unprojected linked task"
  done < <(jq -r '.[]' <<<"$linked_task_ids")
  jq -e --argjson head "$head_evidence_id" --arg epoch "$epoch_id" --argjson objective "$objective_task_id" '
   . as $a | length>0 and length<=100 and .[-1].id==$head and .[-1].task_id==$objective and .[-1].details.epoch_id==$epoch and
   ([.[].id]|length)==([.[].id]|unique|length) and
   (to_entries|all(. as $e |
     $e.value.details.revision==($e.key+1) and
     $e.value.details.prior_thesis_evidence_id==(if $e.key==0 then null else $a[$e.key-1].id end) and
     ($e.value.details.epoch_id|type=="string" and length>0) and
     ($e.value.details.observed_at_utc|type=="string") and ($e.value.details.valid_until_utc|type=="string") and
     ($e.value.details.census_basis|type=="array" and length>0) and
     ($e.value.details.membership|type=="object") and
     ($e.value.details.observations|type=="array" and length>0) and
     ($e.value.details.inferences|type=="array") and ($e.value.details.uncertainties|type=="array") and
     ($e.value.details.ranked_proposals|type=="array") and ($e.value.details.deferred_or_displaced|type=="array") and
     ($e.value.details.fact_refs|type=="array" and length>0) and
     $e.value.details.worker_trace.fresh_process==true and $e.value.details.worker_trace.no_session==true and
     $e.value.details.worker_trace.read_only==true and $e.value.details.worker_trace.prior_transcript_supplied==false and
     $e.value.details.worker_trace.prior_thesis_supplied==false and $e.value.details.worker_trace.controller_independent_verification==true
   ))
  ' <<<"$thesis_chain" >/dev/null || fail "thesis chain invalid"

  head_task="$(ak task show "$objective_task_id" --machine)"
  jq -e --arg claimant "$claimant" '
   .payload.task.status=="claimed" and .payload.task.claimed_by==$claimant
  ' <<<"$head_task" >/dev/null || fail "current thesis task claim invalid"
  thesis_claim_ns="$(to_ns "$(jq -r '.payload.task.claimed_at' <<<"$head_task")")" || fail "invalid thesis task claim time"
  thesis_claim_exp_ns="$(to_ns "$(jq -r '.payload.task.lease_expires_at' <<<"$head_task")")" || fail "invalid thesis task lease"
  (( thesis_claim_ns >= authorized_ns && now_ns < thesis_claim_exp_ns && thesis_claim_exp_ns <= expires_ns )) || fail "thesis task lease outside epoch"

  valid_thesis_authorizations="$(jq '
   . as $epochs |
   [ .[] as $candidate |
     select($candidate.details.schema=="softwareco.portfolio-cto-epoch-authorization.v1") |
     select(([ $epochs[] | select(.details.schema=="softwareco.portfolio-cto-epoch-invalidation.v1") | .details.invalidated_receipt_id ] | index($candidate.id))==null) |
     $candidate
   ]
  ' <<<"$applied_epochs")"
  while IFS=$'\t' read -r thesis_epoch observed valid; do
    thesis_authorization="$(jq --arg epoch "$thesis_epoch" '[.[]|select(.details.epoch_id==$epoch)]' <<<"$valid_thesis_authorizations")"
    jq -e 'length==1' <<<"$thesis_authorization" >/dev/null || fail "thesis epoch authorization missing or ambiguous"
    thesis_authorized_ns="$(to_ns_strict "$(jq -r '.[0].details.authorized_at_utc' <<<"$thesis_authorization")")" || fail "invalid thesis epoch authorization"
    thesis_expires_ns="$(to_ns_strict "$(jq -r '.[0].details.authorization_expires_at_utc' <<<"$thesis_authorization")")" || fail "invalid thesis epoch expiry"
    observed_ns="$(to_ns_strict "$observed")" || fail "invalid thesis observation timestamp"
    valid_ns="$(to_ns_strict "$valid")" || fail "invalid thesis validity timestamp"
    (( observed_ns >= thesis_authorized_ns && observed_ns <= now_ns && valid_ns > observed_ns && valid_ns-observed_ns <= 86400000000000 && valid_ns <= thesis_expires_ns )) || fail "thesis validity outside its epoch bounds"
  done < <(jq -r '.[]|[.details.epoch_id,.details.observed_at_utc,.details.valid_until_utc]|@tsv' <<<"$thesis_chain")
  head_valid_ns="$(to_ns_strict "$(jq -r '.[-1].details.valid_until_utc' <<<"$thesis_chain")")" || fail "invalid thesis head validity"
  (( now_ns < head_valid_ns )) || fail "thesis head expired"
  printf 'cto-operator-surface: PASS (Decision 77 thesis current; head=%s; revisions=%s)\n' "$head_evidence_id" "$(jq 'length' <<<"$thesis_chain")"
  exit 0
elif [[ "$mode_arg" == --require-77-objective-complete ]]; then
  objective_task="$(ak task show 4221 --machine)"
  jq -e '
   .payload.task.status=="done" and .payload.task.claimed_by==null and .payload.task.claimed_at==null and .payload.task.lease_expires_at==null and
   .payload.task.scope.allowed_paths==["docs/learnings/2026-07-25-softwareco-recurring-portfolio-cto-*","docs/project/2026-07-25-softwareco-recurring-portfolio-cto-*","scripts/check-cto-operator-surface.sh"] and
   .payload.task.scope.required_paths==["docs/project/2026-07-25-softwareco-recurring-portfolio-cto-recurrence-evidence.md"] and
   .payload.task.scope.forbidden_paths==[] and
   .payload.task.result.schema=="softwareco.portfolio-cto-recurrence-objective-closeout.v1" and
   (.payload.task.result.objective_evidence_id|type=="number") and
   .payload.task.result.run_a_thesis_evidence_id==5378 and .payload.task.result.run_c_thesis_evidence_id==5407 and
   .payload.task.result.wave_outcome_evidence_id==5406 and
   .payload.task.result.framework_terminal_receipt_created==false and
   .payload.task.result.framework_revocation_receipt_created==false and
   .payload.task.result.framework_supersession_receipt_created==false and .payload.task.result.external_effects==0
  ' <<<"$objective_task" >/dev/null || fail "Decision 77 objective task closeout invalid"
  objective_evidence_id="$(jq -r '.payload.task.result.objective_evidence_id' <<<"$objective_task")"

  objective_collection="$(ak evidence task 4221 --machine)"
  objective_evidence="$(jq '[.payload.evidence[]|select(.check_type=="portfolio_cto_recurrence_objective_v1" and .result=="pass" and .details.schema=="softwareco.portfolio-cto-recurrence-objective.v1" and .details.decision_id==77)]' <<<"$objective_collection")"
  jq -e --argjson objective "$objective_evidence_id" '
   length==1 and .[0].id==$objective and .[0].task_id==4221 and
   .[0].details.objective_task_id==4221 and .[0].details.epoch_id=="d77-e3-20260726" and
   .[0].details.run_a_thesis_evidence_id==5378 and .[0].details.run_c_thesis_evidence_id==5407 and
   .[0].details.thesis_evidence_chain==[5326,5378,5407] and
   .[0].details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .[0].details.owner_task_id==4225 and
   .[0].details.owner_acceptance_receipt_ids==[9063,9064] and
   .[0].details.terminal_acceptance_receipt_ids==[9087,9088] and .[0].details.owner_release_receipt_id==9089 and
   .[0].details.admission_evidence_id==5383 and .[0].details.controller_release_evidence_id==5405 and .[0].details.wave_outcome_evidence_id==5406 and
   .[0].details.owner_validation_evidence_ids==[5397,5400,5401,5402,5403] and
   .[0].details.run_a_trace.fresh_process==true and .[0].details.run_a_trace.no_session==true and .[0].details.run_a_trace.read_only==true and
   .[0].details.run_a_trace.prior_transcript_supplied==false and .[0].details.run_a_trace.prior_thesis_supplied==false and
   .[0].details.run_a_trace.pid==3377969 and .[0].details.run_a_trace.started_at_utc=="2026-07-26T08:32:15.471831824Z" and
   .[0].details.run_a_trace.runner_sha256=="bb9670c515aff9e6215a7eb60dfcd4db41d713f5c8f48cde268e80544329e9cc" and
   .[0].details.run_a_trace.stdout_sha256=="8735224fcec27cef481de82200804f21a356d3abb9a59e55f88afacc1764dae0" and
   .[0].details.run_c_trace.fresh_process==true and .[0].details.run_c_trace.no_session==true and .[0].details.run_c_trace.read_only==true and
   .[0].details.run_c_trace.prior_transcript_supplied==false and .[0].details.run_c_trace.prior_thesis_supplied==false and
   .[0].details.run_c_trace.pid==3986608 and .[0].details.run_c_trace.started_at_utc=="2026-07-26T10:06:04.806358186Z" and
   .[0].details.run_c_trace.runner_sha256=="c95c977799ff44db39b9df21e58251332428bc8c1506e6027105e3dbe4165c34" and
   .[0].details.run_c_trace.stdout_sha256=="6d737119bf0c3617888c7fca48232b04c1dd1cad9c43ac04014856a51545e221" and
   .[0].details.run_a_trace.pid!=.[0].details.run_c_trace.pid and
   .[0].details.run_a_trace.started_at_utc!=.[0].details.run_c_trace.started_at_utc and
   .[0].details.run_a_trace.runner_sha256!=.[0].details.run_c_trace.runner_sha256 and
   .[0].details.run_a_trace.stdout_sha256!=.[0].details.run_c_trace.stdout_sha256 and
   (.[0].details.checker_results|type=="array" and length>0) and (.[0].details.known_limitations|type=="array") and
   .[0].details.documentation_ref=="docs/project/2026-07-25-softwareco-recurring-portfolio-cto-recurrence-evidence.md" and
   .[0].details.framework_terminal_receipt_created==false and .[0].details.framework_revocation_receipt_created==false and
   .[0].details.framework_supersession_receipt_created==false and .[0].details.external_effects==0
  ' <<<"$objective_evidence" >/dev/null || fail "Decision 77 recurrence objective evidence invalid"

  jq -e '
   .payload.node.state=="active" and
   .payload.node.state_detail=="decision77_recurring_framework;phase=objective_complete;objective_task_id=4221;thesis_task_ids=4221;thesis_head_evidence_id=5407"
  ' <<<"$projection" >/dev/null || fail "Decision 77 objective-complete projection invalid"
  wave="$(ak direction show --repo "$root" IW-SF3-CTO77-AK-SCHEMA-STATUS --machine)"
  jq -e '
   .payload.node.state=="done" and
   .payload.node.state_detail=="portfolio_completed_decision_77;admission_evidence_id=5383;release_evidence_ids=5405;outcome_evidence_id=5406" and
   ([.payload.decision_links[]|select(.link.decision_id==77 and .link.link_role=="governs")]|length)==1
  ' <<<"$wave" >/dev/null || fail "Decision 77 completed owner wave invalid"

  sf3_objective="$(ak direction show --repo "$root" SF3 --machine)"
  jq -e '
   [.payload.children[]|select((.key|startswith("IW-SF3-CTO77-")) and .key!="IW-SF3-CTO77-RECURRING")] as $waves |
   ($waves|length)==1 and $waves[0].key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and $waves[0].state=="done" and
   $waves[0].state_detail=="portfolio_completed_decision_77;admission_evidence_id=5383;release_evidence_ids=5405;outcome_evidence_id=5406"
  ' <<<"$sf3_objective" >/dev/null || fail "Decision 77 global wave census invalid"
  membership_census='[]'
  while IFS= read -r objective_controller_id; do
    controller_evidence="$(ak evidence task "$objective_controller_id" --machine)"
    membership_census="$(jq -n --argjson prior "$membership_census" --argjson collection "$controller_evidence" '
     $prior + [$collection.payload.evidence[]|select(
       .check_type=="portfolio_wave_admission_v2" or .check_type=="portfolio_owner_release_v2" or .check_type=="portfolio_wave_outcome_v2"
     )]
    ')"
  done < <(jq -r '[.[]|select(.details.schema=="softwareco.portfolio-cto-epoch-authorization.v1")|.details.controller_task_id]|unique|.[]' <<<"$applied_epochs")
  jq -e '
   sort_by(.id) as $events |
   ($events|map(.id))==[5383,5405,5406] and
   $events[0].details.schema=="softwareco.portfolio-wave-admission.v2" and
   $events[1].details.schema=="softwareco.portfolio-owner-release-event.v2" and
   $events[1].details.prior_owner_task_event_evidence_id==5383 and
   $events[2].details.schema=="softwareco.portfolio-wave-outcome.v2" and
   $events[2].details.controller_release_evidence_ids==[5405] and
   $events[2].details.outstanding_owner_task_ids==[]
  ' <<<"$membership_census" >/dev/null || fail "Decision 77 global membership/WIP census invalid"

  ak task show 4225 --machine | jq -e '.payload.task.status=="done" and .payload.task.result.commit=="b2548196cb8994f5388293b26918d454c41a4138" and .payload.task.result.external_effects==0' >/dev/null || fail "Decision 77 owner task outcome invalid"
  ak evidence show 5383 --json | jq -e '.result=="pass" and .details.schema=="softwareco.portfolio-wave-admission.v2" and .details.owner_task_ids==[4225]' >/dev/null || fail "Decision 77 admission evidence invalid"
  ak evidence show 5405 --json | jq -e '.result=="pass" and .details.schema=="softwareco.portfolio-owner-release-event.v2" and .details.owner_release_receipt_id==9089 and .details.post_outstanding_owner_task_count==0' >/dev/null || fail "Decision 77 controller release evidence invalid"
  ak evidence show 5406 --json | jq -e '.result=="pass" and .details.schema=="softwareco.portfolio-wave-outcome.v2" and .details.success_criteria_satisfied==true and .details.portfolio_wip_released==true and .details.outstanding_owner_task_ids==[]' >/dev/null || fail "Decision 77 wave outcome evidence invalid"
  run_a="$(ak evidence show 5378 --json)"
  jq -e '
   .task_id==4221 and .check_type=="portfolio_thesis_v2" and .result=="pass" and .details.schema=="softwareco.portfolio-thesis.v2" and
   .details.decision_id==77 and .details.epoch_id=="d77-e3-20260726" and .details.revision==2 and .details.prior_thesis_evidence_id==5326 and
   .details.worker_trace.run=="A-epoch3" and .details.worker_trace.fresh_process==true and .details.worker_trace.no_session==true and
   .details.worker_trace.read_only==true and .details.worker_trace.prior_transcript_supplied==false and .details.worker_trace.prior_thesis_supplied==false and
   .details.worker_trace.controller_independent_verification==true and .details.worker_trace.pid==3377969 and
   .details.worker_trace.started_at_utc=="2026-07-26T08:32:15.471831824Z" and
   .details.worker_trace.runner_sha256=="bb9670c515aff9e6215a7eb60dfcd4db41d713f5c8f48cde268e80544329e9cc" and
   .details.worker_trace.stdout_sha256=="8735224fcec27cef481de82200804f21a356d3abb9a59e55f88afacc1764dae0"
  ' <<<"$run_a" >/dev/null || fail "Decision 77 Run A thesis invalid"
  run_c="$(ak evidence show 5407 --json)"
  jq -e '
   .task_id==4221 and .check_type=="portfolio_thesis_v2" and .result=="pass" and .details.schema=="softwareco.portfolio-thesis.v2" and
   .details.decision_id==77 and .details.epoch_id=="d77-e3-20260726" and .details.revision==3 and .details.prior_thesis_evidence_id==5378 and
   .details.worker_trace.run=="C" and .details.worker_trace.fresh_process==true and .details.worker_trace.no_session==true and
   .details.worker_trace.read_only==true and .details.worker_trace.prior_transcript_supplied==false and .details.worker_trace.prior_thesis_supplied==false and
   .details.worker_trace.controller_independent_verification==true and .details.worker_trace.pid==3986608 and
   .details.worker_trace.started_at_utc=="2026-07-26T10:06:04.806358186Z" and
   .details.worker_trace.runner_sha256=="c95c977799ff44db39b9df21e58251332428bc8c1506e6027105e3dbe4165c34" and
   .details.worker_trace.stdout_sha256=="6d737119bf0c3617888c7fca48232b04c1dd1cad9c43ac04014856a51545e221" and
   .details.membership.state=="proved_released" and .details.membership.admitted_wave_count==0 and
   .details.membership.outstanding_owner_task_count==0 and .details.membership.unresolved_objection_count==0
  ' <<<"$run_c" >/dev/null || fail "Decision 77 Run C thesis invalid"
  jq -e --argjson a "$run_a" '
   .details.worker_trace.pid!=$a.details.worker_trace.pid and
   .details.worker_trace.started_at_utc!=$a.details.worker_trace.started_at_utc and
   .details.worker_trace.runner_sha256!=$a.details.worker_trace.runner_sha256 and
   .details.worker_trace.stdout_sha256!=$a.details.worker_trace.stdout_sha256
  ' <<<"$run_c" >/dev/null || fail "Decision 77 fresh runs are not distinct"

  ak governance show 9063 --json | jq -e '
   .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .consent_mode=="explicit" and .from_state=="proposed" and .to_state=="envelope_accepted" and .task_id==4225 and
   .repo_scope=="/home/tryinget/ai-society/softwareco/owned/agent-kernel" and
   .details.schema=="softwareco.portfolio-owner-envelope-acceptance.v2" and .details.decision_id==77 and
   .details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .details.role=="product-domain" and .details.owner_id=="human-operator" and
   .details.scope_id=="task-4225" and .details.epoch_id=="d77-e3-20260726" and .details.prior_receipt_id==null and
   .details.owner_evidence_refs==["evidence:5378","task:4225","git:agent-kernel:8b449ee"] and
   .details.observed_at_utc=="2026-07-26T08:45:25.248593859Z" and .details.external_effects==0
  ' >/dev/null || fail "Decision 77 product acceptance receipt invalid"
  ak governance show 9064 --json | jq -e '
   .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .consent_mode=="explicit" and .from_state=="proposed" and .to_state=="task_scope_accepted" and .task_id==4225 and
   .repo_scope=="/home/tryinget/ai-society/softwareco/owned/agent-kernel" and
   .details.schema=="softwareco.portfolio-owner-task-scope-acceptance.v2" and .details.decision_id==77 and
   .details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .details.role=="project-source" and .details.owner_id=="human-operator" and
   .details.scope_id=="task-4225" and .details.owner_task_ids==[4225] and .details.epoch_id=="d77-e3-20260726" and .details.prior_receipt_id==null and
   .details.owner_evidence_refs==["evidence:5378","task:4225","governance:9063","git:agent-kernel:8b449ee"] and
   .details.observed_at_utc=="2026-07-26T08:45:25.248593859Z" and .details.external_effects==0
  ' >/dev/null || fail "Decision 77 project acceptance receipt invalid"
  ak governance show 9087 --json | jq -e '
   .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .consent_mode=="explicit" and .from_state=="admitted" and .to_state=="terminal_accepted" and .task_id==4225 and
   .repo_scope=="/home/tryinget/ai-society/softwareco/owned/agent-kernel" and
   .details.schema=="softwareco.portfolio-terminal-acceptance.v2" and .details.decision_id==77 and .details.epoch_id=="d77-e3-20260726" and
   .details.role=="product-domain" and .details.owner_id=="human-operator" and .details.scope_id=="task-4225" and .details.prior_receipt_id==null and
   .details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .details.owner_task_ids==[4225] and .details.acceptance_receipt_id==9063 and
   .details.owner_evidence_refs==["task:4225","evidence:5400","evidence:5401","evidence:5402","evidence:5403","evidence:5397","git:agent-kernel:b2548196cb8994f5388293b26918d454c41a4138","git:agent-kernel:8c84ba5b5dfbaf6102f4f0f8e0804ee067a5aaa8"] and
   .details.observed_at_utc=="2026-07-26T09:47:35.009747233Z" and .details.external_effects==0
  ' >/dev/null || fail "Decision 77 product terminal receipt invalid"
  ak governance show 9088 --json | jq -e '
   .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .consent_mode=="explicit" and .from_state=="admitted" and .to_state=="terminal_accepted" and .task_id==4225 and
   .repo_scope=="/home/tryinget/ai-society/softwareco/owned/agent-kernel" and
   .details.schema=="softwareco.portfolio-terminal-acceptance.v2" and .details.decision_id==77 and .details.epoch_id=="d77-e3-20260726" and
   .details.role=="project-source" and .details.owner_id=="human-operator" and .details.scope_id=="task-4225" and .details.prior_receipt_id==null and
   .details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .details.owner_task_ids==[4225] and .details.acceptance_receipt_id==9064 and
   .details.product_terminal_acceptance_receipt_id==9087 and
   .details.owner_evidence_refs==["task:4225","evidence:5400","evidence:5401","evidence:5402","evidence:5403","evidence:5397","git:agent-kernel:b2548196cb8994f5388293b26918d454c41a4138","git:agent-kernel:8c84ba5b5dfbaf6102f4f0f8e0804ee067a5aaa8"] and
   .details.observed_at_utc=="2026-07-26T09:47:35.009747233Z" and .details.external_effects==0
  ' >/dev/null || fail "Decision 77 project terminal receipt invalid"
  ak governance show 9089 --json | jq -e '
   .status=="applied" and .source_authority=="human-operator" and .actor=="human-operator" and .agreement_ref=="decision:77" and
   .consent_mode=="explicit" and .from_state=="admitted" and .to_state=="released_terminal" and .task_id==4225 and
   .repo_scope=="/home/tryinget/ai-society/softwareco/owned/agent-kernel" and
   .details.schema=="softwareco.portfolio-owner-release.v2" and .details.decision_id==77 and .details.epoch_id=="d77-e3-20260726" and
   .details.role=="project-source" and .details.owner_id=="human-operator" and .details.scope_id=="task-4225" and .details.prior_receipt_id==null and
   .details.wave_key=="IW-SF3-CTO77-AK-SCHEMA-STATUS" and .details.owner_task_ids==[4225] and
   .details.owner_evidence_refs==["task:4225:done","evidence:5400","evidence:5401"] and
   .details.observed_at_utc=="2026-07-26T09:47:35.009747233Z" and .details.terminal_acceptance_receipt_ids==[9087,9088] and
   .details.disposition=="released_terminal" and .details.continuing_owner_lifecycle==false and .details.external_effects==0
  ' >/dev/null || fail "Decision 77 owner release receipt invalid"

  manifest_task="$(ak task show 4273 --machine)"
  jq -e '
   .payload.task.status=="done" and .payload.task.result.schema=="softwareco.portfolio-cto-recurrence-proof-hardening.v1" and
   .payload.task.result.objective_evidence_id==5412 and (.payload.task.result.manifest_evidence_id|type=="number") and
   .payload.task.result.run_a_manifest_sha256=="fe706a37db971c9844aa69c9f3b0b3c1238afeccf10a83e59163cfcea1726352" and
   .payload.task.result.run_c_manifest_sha256=="00bb3ffce11fa4c195456f2ddc86c0ebfb9cd12167389128919dbf31dae59ee5"
  ' <<<"$manifest_task" >/dev/null || fail "Decision 77 manifest hardening task invalid"
  manifest_evidence_id="$(jq -r '.payload.task.result.manifest_evidence_id' <<<"$manifest_task")"
  manifest_collection="$(ak evidence task 4273 --machine)"
  jq -e --argjson manifest "$manifest_evidence_id" '
   [.payload.evidence[]|select(.check_type=="portfolio_cto_worker_manifest_v1" and .result=="pass")] as $matches |
   ($matches|length)==1 and $matches[0].id==$manifest and
   $matches[0].details.schema=="softwareco.portfolio-cto-worker-manifest-bundle.v1" and
   $matches[0].details.decision_id==77 and $matches[0].details.objective_evidence_id==5412 and
   $matches[0].details.run_a_manifest_sha256=="fe706a37db971c9844aa69c9f3b0b3c1238afeccf10a83e59163cfcea1726352" and
   $matches[0].details.run_c_manifest_sha256=="00bb3ffce11fa4c195456f2ddc86c0ebfb9cd12167389128919dbf31dae59ee5" and
   $matches[0].details.run_a_stdout_sha256=="8735224fcec27cef481de82200804f21a356d3abb9a59e55f88afacc1764dae0" and
   $matches[0].details.run_c_stdout_sha256=="6d737119bf0c3617888c7fca48232b04c1dd1cad9c43ac04014856a51545e221" and
   $matches[0].details.distinct_processes==true and $matches[0].details.prior_context_excluded==true and
   $matches[0].details.raw_artifacts_hash_verified==true
  ' <<<"$manifest_collection" >/dev/null || fail "Decision 77 worker manifest evidence invalid"
  [[ "$(sha256sum "$root/docs/project/2026-07-25-softwareco-recurring-portfolio-cto-run-a-manifest.json" | cut -d' ' -f1)" == fe706a37db971c9844aa69c9f3b0b3c1238afeccf10a83e59163cfcea1726352 ]] || fail "Decision 77 Run A manifest hash mismatch"
  [[ "$(sha256sum "$root/docs/project/2026-07-25-softwareco-recurring-portfolio-cto-run-c-manifest.json" | cut -d' ' -f1)" == 00bb3ffce11fa4c195456f2ddc86c0ebfb9cd12167389128919dbf31dae59ee5 ]] || fail "Decision 77 Run C manifest hash mismatch"
  jq -e '
   .schema=="softwareco.portfolio-cto-worker-manifest.v1" and .decision_id==77 and .run=="A-epoch3" and
   .fresh_process==true and .no_session==true and .session_persistence==false and .prior_session_id==null and
   .prior_transcript_supplied==false and .prior_thesis_content_supplied==false and .read_only==true and
   .process.pid==3377969 and .process.started_at_utc=="2026-07-26T08:32:15.471831824Z" and
   .process.argv==["pi","--mode","rpc","--no-session","--approve","--offline","--no-skills","--no-tools","--thinking","low"] and
   [.rpc_input_manifest[].id]==["mode","pre","ask","last"] and
   .artifact_manifest.runner_source.sha256=="bb9670c515aff9e6215a7eb60dfcd4db41d713f5c8f48cde268e80544329e9cc" and
   .artifact_manifest.rpc_event_output.sha256=="8735224fcec27cef481de82200804f21a356d3abb9a59e55f88afacc1764dae0" and
   .artifact_manifest.bounded_readback_output.sha256=="e672de9b52182c3bc42b6ee441b789e8db52c004de5d3754407b37105863d062" and
   .artifact_manifest.candidate_response.sha256=="e8f61efb144ddd80da25929e03802df45a6a5d90cc652d5a33390bc7591df87a"
  ' "$root/docs/project/2026-07-25-softwareco-recurring-portfolio-cto-run-a-manifest.json" >/dev/null || fail "Decision 77 Run A manifest invalid"
  jq -e '
   .schema=="softwareco.portfolio-cto-worker-manifest.v1" and .decision_id==77 and .run=="C" and
   .fresh_process==true and .no_session==true and .session_persistence==false and .prior_session_id==null and
   .prior_transcript_supplied==false and .prior_thesis_content_supplied==false and .read_only==true and
   .process.pid==3986608 and .process.started_at_utc=="2026-07-26T10:06:04.806358186Z" and
   .process.argv==["pi","--mode","rpc","--no-session","--approve","--offline","--no-skills","--no-tools","--thinking","low"] and
   [.rpc_input_manifest[].id]==["mode","pre","ask","last"] and
   .artifact_manifest.runner_source.sha256=="c95c977799ff44db39b9df21e58251332428bc8c1506e6027105e3dbe4165c34" and
   .artifact_manifest.rpc_event_output.sha256=="6d737119bf0c3617888c7fca48232b04c1dd1cad9c43ac04014856a51545e221" and
   .artifact_manifest.bounded_readback_output.sha256=="f8380d94d8987a219ef09158f2c12a6910c569f6b0c33fd2b34c8d1423f8b032" and
   .artifact_manifest.candidate_response.sha256=="f440c0cd70331bf6340b2c5a73d95a642fb2c22da8c253b0c9599ed47e231731"
  ' "$root/docs/project/2026-07-25-softwareco-recurring-portfolio-cto-run-c-manifest.json" >/dev/null || fail "Decision 77 Run C manifest invalid"
  grep -Fqx "objective_evidence_id: $objective_evidence_id" "$root/docs/project/2026-07-25-softwareco-recurring-portfolio-cto-recurrence-evidence.md" || fail "Decision 77 recurrence evidence projection missing objective evidence ID"
  ak direction check --repo "$root" --json | jq -e '.ok==true and (.issues|length==0)' >/dev/null || fail "Decision 77 objective direction topology invalid"
  printf 'cto-operator-surface: PASS (Decision 77 recurrence objective complete; evidence=%s; framework remains nonterminal)\n' "$objective_evidence_id"
  exit 0
fi
fail "unhandled mode: $mode_arg"
