#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${PI_MODES_PACKAGE_DIR:-$HOME/.pi/agent/npm/node_modules/@tryinget/pi-modes}"
require_active=false
[[ "${1:-}" == "--require-active" ]] && require_active=true

fail() {
  printf 'cto-operator-surface: FAIL: %s\n' "$*" >&2
  exit 1
}

[[ -f "$package_dir/package.json" ]] || fail "immutable Pi Modes package not found at $package_dir"
[[ "$(node -p "require(process.argv[1]).version" "$package_dir/package.json")" == "0.3.0" ]] \
  || fail "Pi Modes package must be exactly 0.3.0"

mode="$root/.pi/modes/softwareco-cto.json"
preset="$root/.pi/mode-presets/softwareco-cto.json"
prompt="$root/.pi/prompts/cto.md"
for path in "$mode" "$preset" "$prompt"; do
  [[ -f "$path" ]] || fail "missing ${path#$root/}"
done

# Pi Modes 0.3.0 ships its TypeScript source in node_modules. Node 26 refuses
# native type stripping there. Copy the exact installed release to an ephemeral
# non-node_modules path and run its owner linter with Node; never fetch a runner.
lint_dir="$(mktemp -d)"
trap 'rm -rf "$lint_dir"' EXIT
cp -a "$package_dir"/. "$lint_dir"/
(
  cd "$lint_dir"
  node ./scripts/mode-lint.mjs "$mode" "$preset"
) || fail "Pi Modes owner linter rejected Softwareco artifacts"

jq -e '
  .schemaVersion == 2 and
  .key == "softwareco-cto" and
  .promptStrategy == "append" and
  (.systemPrompt | contains("grants no delegation")) and
  (.systemPrompt | contains("controller task 4182")) and
  (.systemPrompt | contains("two admitted waves")) and
  (.systemPrompt | contains("six outstanding")) and
  (.systemPrompt | contains("FCOS"))
' "$mode" >/dev/null || fail "mode contract mismatch"

jq -e '
  .schemaVersion == 1 and
  .key == "softwareco-cto" and
  .selection.baseKey == null and
  .selection.overlayKeys == ["softwareco-cto"]
' "$preset" >/dev/null || fail "preset contract mismatch"

grep -Fq 'argument-hint: "<objective>"' "$prompt" || fail "missing /cto argument hint"
grep -Fq '$ARGUMENTS' "$prompt" || fail "missing /cto argument interpolation"
for required in \
  'Decision 74' \
  'Controller task `4182`' \
  'advisory only' \
  'owner-originated' \
  'second-wave-checkpoint' \
  'FCOS writes require' \
  'Terminal `continue` still ends'; do
  grep -Fq "$required" "$prompt" || fail "prompt missing: $required"
done

# The local builder and every unspecified .pi artifact remain ignored.
git -C "$root" check-ignore -q .pi/modes/softwareco-builder.json \
  || fail "local softwareco-builder must remain ignored"
for path in .pi/modes/softwareco-cto.json .pi/mode-presets/softwareco-cto.json .pi/prompts/cto.md; do
  if git -C "$root" check-ignore -q "$path"; then
    fail "$path is still ignored"
  fi
done

tracked_pi="$(git -C "$root" ls-files '.pi/**' | sort)"
if [[ -n "$tracked_pi" ]]; then
  expected=$'.pi/mode-presets/softwareco-cto.json\n.pi/modes/softwareco-cto.json\n.pi/prompts/cto.md'
  [[ "$tracked_pi" == "$expected" ]] || fail "unexpected tracked .pi artifacts: $tracked_pi"
fi

org_docs=(docs/org/cto-agent-charter.md docs/org/governance.md docs/org/operating_model.md)
for doc in "${org_docs[@]}"; do
  grep -Fq 'Decision 74' "$root/$doc" || fail "$doc does not project Decision 74"
done

accepted_at="2026-07-25T08:11:27.729630885Z"
expires_at="2026-08-24T08:11:27.729630885Z"
to_ns() { date -u -d "$1" +%s%N 2>/dev/null; }
acceptance="$(ak governance show 8818 --json)"
jq -e '
  .id == 8818 and
  .concern == "architecture-decision" and
  .actor == "human-operator" and
  .status == "applied" and
  .details.decision_id == 74 and
  .details.outcome == "accepted"
' <<<"$acceptance" >/dev/null || fail "Decision 74 acceptance receipt 8818 mismatch"
receipt_accepted_at="$(jq -r '.created_at' <<<"$acceptance")"
[[ "$(to_ns "$receipt_accepted_at")" == "$(to_ns "$accepted_at")" ]] \
  || fail "Decision 74 acceptance timestamp mismatch"

ak decision get 74 --machine | jq -e '
  .ok == true and
  .payload.decision.state == "unblocked" and
  .payload.decision.outcome == "accepted"
' >/dev/null || fail "Decision 74 is not accepted and unblocked"

sf3="$(ak direction show --repo "$root" SF3 --machine)"
jq -e '.ok == true and .payload.node.state == "active"' <<<"$sf3" >/dev/null \
  || fail "SF3 is not active"
detail="$(jq -r '.payload.node.state_detail' <<<"$sf3")"
controller="$(ak task show 4182 --machine)"
jq -e '
  .ok == true and
  .payload.task.title == "Control Decision 74 portfolio admissions" and
  (.payload.task.scope.allowed_paths == []) and
  (.payload.task.scope.required_paths == []) and
  (.payload.task.scope.forbidden_paths == ["**"])
' <<<"$controller" >/dev/null || fail "controller task 4182 contract mismatch"

if ! $require_active; then
  [[ "$detail" == "decision_membrane_pending_no_cto_delegation" ]] \
    || fail "preactivation check requires exact pending SF3 detail"
  jq -e '.payload.task.status == "pending" and .payload.task.claimed_by == null' \
    <<<"$controller" >/dev/null || fail "preactivation controller task must be unclaimed"
  for doc in "${org_docs[@]}"; do
    grep -Fqx 'status: "accepted_preactivation"' "$root/$doc" \
      || fail "$doc is not an exact preactivation projection"
  done
  printf 'cto-operator-surface: PASS (preactivation)\n'
  exit 0
fi

# Active mode is a strict authority readback, not a broad state-prefix check.
prefix="delegated_active_decision_74;accepted_at_utc=$accepted_at;activated_at_utc="
suffix=";expires_at_utc=$expires_at"
[[ "$detail" == "$prefix"*"$suffix" ]] || fail "SF3 delegation detail is not active/exact"
activated_at="${detail#"$prefix"}"
activated_at="${activated_at%"$suffix"}"
[[ "$activated_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{9}Z$ ]] \
  || fail "SF3 activation timestamp is not exact nanosecond RFC3339 UTC"
[[ -n "$activated_at" && "$activated_at" != *';'* ]] || fail "SF3 activation timestamp is malformed"

accepted_ns="$(to_ns "$accepted_at")" || fail "accepted timestamp is invalid"
activated_ns="$(to_ns "$activated_at")" || fail "activation timestamp is invalid"
expires_ns="$(to_ns "$expires_at")" || fail "expiry timestamp is invalid"
now_ns="$(date -u +%s%N)"
(( activated_ns >= accepted_ns )) || fail "activation precedes Decision 74 acceptance"
(( now_ns >= activated_ns && now_ns < expires_ns )) || fail "Decision 74 is not inside its active time window"
(( expires_ns - accepted_ns == 2592000000000000 )) || fail "Decision 74 expiry is not exactly 30 days after acceptance"

for doc in "${org_docs[@]}"; do
  grep -Fqx 'status: "active_bounded"' "$root/$doc" \
    || fail "$doc is not an exact active projection"
done
grep -Fqx "activated_at: \"$activated_at\"" "$root/docs/org/cto-agent-charter.md" \
  || fail "charter activation timestamp does not match SF3"

for concern in \
  softwareco-portfolio-cto:decision74:revocation \
  softwareco-portfolio-cto:decision74:terminal \
  softwareco-portfolio-cto:decision74:supersession; do
  receipts="$(ak governance list --concern "$concern" --limit 100 --json)"
  jq -e 'map(select(.status == "applied")) | length == 0' <<<"$receipts" >/dev/null \
    || fail "applied termination receipt exists for $concern"
done

# Inspect every later accepted decision's title and readable RFC/ADR content.
# A missing readable primary artifact is ambiguous and therefore fails closed.
later_decisions="$(ak decision list --limit 500 --machine)"
supersession_re='(supersed(e|es|ed|ing)?.{0,240}(Decision[[:space:]#:._-]*)?74|(Decision[[:space:]#:._-]*74).{0,240}supersed(e|es|ed|ing)?)'
while IFS=$'\t' read -r decision_id repo_scope title rfc_ref adr_ref; do
  [[ -n "$decision_id" ]] || continue
  printf '%s' "$title $rfc_ref $adr_ref" | grep -Eiq "$supersession_re" \
    && fail "accepted decision $decision_id explicitly supersedes Decision 74"
  readable_primary=false
  for ref in "$rfc_ref" "$adr_ref"; do
    [[ -n "$ref" && "$ref" != "-" ]] || continue
    if [[ "$ref" == /* ]]; then
      decision_path="$ref"
    elif [[ -n "$repo_scope" && "$repo_scope" != "-" && "$ref" != *:* ]]; then
      decision_path="$repo_scope/$ref"
    else
      continue
    fi
    [[ -f "$decision_path" ]] || continue
    readable_primary=true
    tr '\n' ' ' <"$decision_path" | grep -Eiq "$supersession_re" \
      && fail "accepted decision $decision_id content explicitly supersedes Decision 74"
  done
  $readable_primary || fail "accepted decision $decision_id has no readable RFC/ADR for supersession inspection"
done < <(jq -r '
  .payload.decisions[] |
  select(.id > 74 and .outcome == "accepted") |
  [(.id|tostring), (.repo_scope // "-"), (.title // "-"), (.rfc_ref // "-"), (.adr_ref // "-")] |
  @tsv
' <<<"$later_decisions")

designations="$(ak governance list \
  --concern softwareco-portfolio-cto:decision74:controller-designation \
  --limit 100 --json)"
jq -e 'map(select(.status == "applied")) | length == 1' <<<"$designations" >/dev/null \
  || fail "controller designation receipts are missing or ambiguous"
valid_designations="$(jq '[.[] | select(
  .status == "applied" and
  .source_authority == "human-operator" and
  .actor == "human-operator" and
  .agreement_ref == "decision:74" and
  .to_state == "delegated" and
  .consent_mode == "explicit" and
  .task_id == 4182 and
  (.evidence_ref != null and .evidence_ref != "") and
  .details.schema == "softwareco.portfolio-controller-designation.v1" and
  (.details.claimant_id | type == "string" and length > 0) and
  (.details.lease_seconds | type == "number" and . > 0 and . <= 14400) and
  (.details.designated_at_utc | type == "string" and length > 0) and
  (.details.designation_expires_at_utc | type == "string" and length > 0)
)]' <<<"$designations")"
jq -e 'length == 1' <<<"$valid_designations" >/dev/null \
  || fail "exactly one valid direct human controller designation is required"
designation="$(jq '.[0]' <<<"$valid_designations")"
claimant="$(jq -r '.details.claimant_id' <<<"$designation")"
designated_at="$(jq -r '.details.designated_at_utc' <<<"$designation")"
designation_expires="$(jq -r '.details.designation_expires_at_utc' <<<"$designation")"
designation_lease="$(jq -r '.details.lease_seconds' <<<"$designation")"
designated_ns="$(to_ns "$designated_at")" || fail "designation timestamp is invalid"
designation_expires_ns="$(to_ns "$designation_expires")" || fail "designation expiry is invalid"
(( designated_ns >= accepted_ns && designated_ns <= now_ns && now_ns < designation_expires_ns )) \
  || fail "controller designation is not currently valid"
(( designation_expires_ns - designated_ns == designation_lease * 1000000000 )) \
  || fail "designation expiry does not equal its declared lease"

jq -e --arg claimant "$claimant" '
  .payload.task.status == "claimed" and
  .payload.task.claimed_by == $claimant and
  (.payload.task.claimed_at | type == "string" and length > 0) and
  (.payload.task.lease_expires_at | type == "string" and length > 0)
' <<<"$controller" >/dev/null || fail "controller task claim does not match the human designation"
claimed_at="$(jq -r '.payload.task.claimed_at' <<<"$controller")"
claim_expires="$(jq -r '.payload.task.lease_expires_at' <<<"$controller")"
claimed_ns="$(to_ns "$claimed_at")" || fail "controller claim timestamp is invalid"
claim_expires_ns="$(to_ns "$claim_expires")" || fail "controller claim expiry is invalid"
(( claimed_ns >= designated_ns && now_ns < claim_expires_ns )) \
  || fail "controller task lease is stale or predates designation"
(( claim_expires_ns - claimed_ns > 0 && claim_expires_ns - claimed_ns <= 14400000000000 )) \
  || fail "controller task lease exceeds 14,400 seconds"
(( claim_expires_ns <= designation_expires_ns )) \
  || fail "controller task lease outlives the human designation"

printf 'cto-operator-surface: PASS (active; claimant=%s)\n' "$claimant"
