#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRIB_ROOT_DEFAULT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTRIB_ROOT="${PI_COMPAT_RELAY_CONTRIB_ROOT:-$CONTRIB_ROOT_DEFAULT}"
PI_MONO_DIR="${PI_COMPAT_RELAY_PI_MONO_DIR:-}"
PI_EXTENSIONS_DIR="${PI_COMPAT_RELAY_PI_EXTENSIONS_DIR:-}"
STATE_FILE="${PI_COMPAT_RELAY_STATE_FILE:-}"
RECEIPTS_DIR="${PI_COMPAT_RELAY_RECEIPTS_DIR:-}"
MODE="${PI_COMPAT_RELAY_MODE:-workflow}"
PROFILE="${PI_COMPAT_PROFILE:-upgrade}"
WORKFLOW_FILE="${PI_COMPAT_RELAY_WORKFLOW_FILE:-compatibility-canary.yml}"
WORKFLOW_REF="${PI_COMPAT_RELAY_WORKFLOW_REF:-}"
SYNC_STATUS="${PI_COMPAT_RELAY_SYNC_STATUS:-unknown}"
DRY_RUN=0

usage() {
  cat <<'EOF'
Relay relevant upstream pi-mono changes into the pi-extensions compatibility canary.

Behavior:
  - reads the current pi-mono HEAD and compares it with a persisted last-processed HEAD
  - filters for relevant upstream paths (default: packages/coding-agent, packages/tui)
  - triggers the downstream pi-extensions compatibility canary when relevant changes appear
  - writes a machine-readable receipt for initialization, skips, and triggered runs

Usage:
  pi-mono-compatibility-relay.sh [options]

Options:
  --contrib-root <path>         contrib root (default: parent of this script)
  --pi-mono-dir <path>          local pi-mono checkout path
  --pi-extensions-dir <path>    local pi-extensions checkout path
  --state-file <path>           persisted last-processed HEAD file
  --receipts-dir <path>         directory for JSON receipts
  --mode <workflow|local|off>   trigger mode (default: workflow)
  --profile <current|upgrade>   downstream canary profile (default: upgrade)
  --workflow-file <name>        workflow file name for gh dispatch (default: compatibility-canary.yml)
  --workflow-ref <ref>          workflow ref to dispatch (default: pi-extensions origin/HEAD or main)
  --sync-status <value>         optional upstream sync status annotation
  --watch-path <path>           path prefix to watch; repeatable
  --dry-run                     print and receipt only; do not advance state or trigger downstream work
  -h, --help                    show this help

Environment overrides:
  PI_COMPAT_RELAY_CONTRIB_ROOT
  PI_COMPAT_RELAY_PI_MONO_DIR
  PI_COMPAT_RELAY_PI_EXTENSIONS_DIR
  PI_COMPAT_RELAY_STATE_FILE
  PI_COMPAT_RELAY_RECEIPTS_DIR
  PI_COMPAT_RELAY_MODE
  PI_COMPAT_PROFILE
  PI_COMPAT_RELAY_WORKFLOW_FILE
  PI_COMPAT_RELAY_WORKFLOW_REF
  PI_COMPAT_RELAY_SYNC_STATUS
  PI_COMPAT_RELAY_WATCH_PATHS   colon-separated path prefixes
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: missing required command: $1" >&2
    exit 1
  fi
}

json_escape() {
  local value="${1-}"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  value=${value//$'\t'/\\t}
  printf '%s' "$value"
}

join_by() {
  local sep="$1"
  shift || true
  local first=1
  local item
  for item in "$@"; do
    if [[ $first -eq 0 ]]; then
      printf '%s' "$sep"
    fi
    printf '%s' "$item"
    first=0
  done
}

trim() {
  local value="${1-}"
  value="${value#${value%%[![:space:]]*}}"
  value="${value%${value##*[![:space:]]}}"
  printf '%s' "$value"
}

resolve_repo_slug() {
  local repo_dir="$1"
  local remote_url
  remote_url="$(git -C "$repo_dir" remote get-url origin 2>/dev/null || true)"
  remote_url="$(trim "$remote_url")"
  if [[ -z "$remote_url" ]]; then
    return 1
  fi

  remote_url="${remote_url%.git}"
  remote_url="${remote_url#ssh://git@github.com/}"
  remote_url="${remote_url#https://github.com/}"
  remote_url="${remote_url#http://github.com/}"
  remote_url="${remote_url#git@github.com:}"

  if [[ "$remote_url" == */* ]]; then
    printf '%s' "$remote_url"
    return 0
  fi

  return 1
}

resolve_workflow_ref() {
  local repo_dir="$1"
  if [[ -n "$WORKFLOW_REF" ]]; then
    printf '%s' "$WORKFLOW_REF"
    return 0
  fi

  local origin_head
  origin_head="$(git -C "$repo_dir" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  origin_head="${origin_head#origin/}"
  if [[ -n "$origin_head" ]]; then
    printf '%s' "$origin_head"
  else
    printf '%s' "main"
  fi
}

write_state() {
  local head="$1"
  local branch="$2"
  local state_dir
  state_dir="$(dirname "$STATE_FILE")"
  mkdir -p "$state_dir"
  printf 'head=%s\nbranch=%s\n' "$head" "$branch" > "$STATE_FILE"
}

load_state() {
  LAST_PROCESSED_HEAD=""
  LAST_PROCESSED_BRANCH=""
  if [[ -f "$STATE_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$STATE_FILE"
    LAST_PROCESSED_HEAD="${head:-}"
    LAST_PROCESSED_BRANCH="${branch:-}"
  fi
}

write_receipt() {
  local status="$1"
  local reason="$2"
  local before_head="$3"
  local after_head="$4"
  local branch="$5"
  local repo_slug="$6"
  local dispatch_output="$7"
  local run_url="$8"
  local run_id="$9"
  shift 9 || true
  local changed_paths=("$@")

  mkdir -p "$RECEIPTS_DIR"
  local timestamp
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  local receipt_path="$RECEIPTS_DIR/receipt-$(date -u +%Y%m%dT%H%M%SZ)-$$.json"

  {
    printf '{\n'
    printf '  "timestamp": "%s",\n' "$(json_escape "$timestamp")"
    printf '  "status": "%s",\n' "$(json_escape "$status")"
    printf '  "reason": "%s",\n' "$(json_escape "$reason")"
    printf '  "mode": "%s",\n' "$(json_escape "$MODE")"
    printf '  "profile": "%s",\n' "$(json_escape "$PROFILE")"
    printf '  "dry_run": %s,\n' "$([[ "$DRY_RUN" == "1" ]] && echo true || echo false)"
    printf '  "sync_status": "%s",\n' "$(json_escape "$SYNC_STATUS")"
    printf '  "contrib_root": "%s",\n' "$(json_escape "$CONTRIB_ROOT")"
    printf '  "upstream_repo": {\n'
    printf '    "path": "%s",\n' "$(json_escape "$PI_MONO_DIR")"
    printf '    "branch": "%s",\n' "$(json_escape "$branch")"
    printf '    "before_head": %s,\n' "$([[ -n "$before_head" ]] && printf '"%s"' "$(json_escape "$before_head")" || printf 'null')"
    printf '    "after_head": "%s",\n' "$(json_escape "$after_head")"
    printf '    "changed_paths": ['
    local index
    for index in "${!changed_paths[@]}"; do
      if [[ "$index" -gt 0 ]]; then
        printf ', '
      fi
      printf '"%s"' "$(json_escape "${changed_paths[$index]}")"
    done
    printf ']\n'
    printf '  },\n'
    printf '  "downstream_repo": {\n'
    printf '    "path": "%s",\n' "$(json_escape "$PI_EXTENSIONS_DIR")"
    printf '    "repo_slug": %s,\n' "$([[ -n "$repo_slug" ]] && printf '"%s"' "$(json_escape "$repo_slug")" || printf 'null')"
    printf '    "workflow_file": %s,\n' "$([[ "$MODE" == "workflow" ]] && printf '"%s"' "$(json_escape "$WORKFLOW_FILE")" || printf 'null')"
    printf '    "workflow_ref": %s,\n' "$([[ "$MODE" == "workflow" ]] && printf '"%s"' "$(json_escape "$(resolve_workflow_ref "$PI_EXTENSIONS_DIR" 2>/dev/null || echo main)")" || printf 'null')"
    printf '    "dispatch_output": %s,\n' "$([[ -n "$dispatch_output" ]] && printf '"%s"' "$(json_escape "$dispatch_output")" || printf 'null')"
    printf '    "run_url": %s,\n' "$([[ -n "$run_url" ]] && printf '"%s"' "$(json_escape "$run_url")" || printf 'null')"
    printf '    "run_id": %s\n' "$([[ -n "$run_id" ]] && printf '"%s"' "$(json_escape "$run_id")" || printf 'null')"
    printf '  }\n'
    printf '}\n'
  } > "$receipt_path"

  echo "$receipt_path"
}

refresh_evidence_index() {
  local evidence_script="${PI_COMPAT_EVIDENCE_SCRIPT:-$CONTRIB_ROOT/scripts/pi-mono-compatibility-evidence-index.mjs}"
  local evidence_output_path="${PI_COMPAT_EVIDENCE_OUTPUT_PATH:-$CONTRIB_ROOT/.state/pi-mono-compatibility-relay/evidence-index.json}"

  if [[ ! -f "$evidence_script" ]]; then
    return 0
  fi
  if ! command -v node >/dev/null 2>&1; then
    echo "pi-compat-evidence: skipped (node unavailable)" >&2
    return 0
  fi

  local -a evidence_args=(
    "$evidence_script"
    rebuild
    --contrib-root "$CONTRIB_ROOT"
    --receipts-dir "$RECEIPTS_DIR"
    --output "$evidence_output_path"
    --max-online-lookups "${PI_COMPAT_EVIDENCE_MAX_ONLINE_LOOKUPS:-5}"
  )

  if [[ "${PI_COMPAT_EVIDENCE_OFFLINE:-0}" == "1" ]]; then
    evidence_args+=(--offline)
  fi

  set +e
  local output
  output="$(node "${evidence_args[@]}" 2>&1)"
  local status=$?
  set -e

  if [[ $status -ne 0 ]]; then
    echo "pi-compat-evidence: warning (failed to rebuild evidence index)" >&2
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output" >&2
    fi
    return 0
  fi

  return 0
}

record_receipt() {
  local receipt_path
  receipt_path="$(write_receipt "$@")"
  refresh_evidence_index
  printf '%s\n' "$receipt_path"
}

lookup_recent_workflow_run() {
  local repo_slug="$1"
  local workflow_ref="$2"
  local line
  line="$(gh run list --repo "$repo_slug" --workflow "$WORKFLOW_FILE" --branch "$workflow_ref" --limit 1 --json databaseId,url --jq '.[0] | [.databaseId, .url] | @tsv' 2>/dev/null || true)"
  if [[ -n "$line" ]]; then
    printf '%s\n' "$line"
  fi
}

declare -a WATCH_PATHS=()
if [[ -n "${PI_COMPAT_RELAY_WATCH_PATHS:-}" ]]; then
  IFS=':' read -r -a WATCH_PATHS <<< "$PI_COMPAT_RELAY_WATCH_PATHS"
fi
if [[ ${#WATCH_PATHS[@]} -eq 0 ]]; then
  WATCH_PATHS=("packages/coding-agent" "packages/tui")
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --contrib-root)
      CONTRIB_ROOT="$(cd "$2" && pwd)"
      shift 2
      ;;
    --pi-mono-dir)
      PI_MONO_DIR="$(cd "$2" && pwd)"
      shift 2
      ;;
    --pi-extensions-dir)
      PI_EXTENSIONS_DIR="$(cd "$2" && pwd)"
      shift 2
      ;;
    --state-file)
      STATE_FILE="$2"
      shift 2
      ;;
    --receipts-dir)
      RECEIPTS_DIR="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --workflow-file)
      WORKFLOW_FILE="$2"
      shift 2
      ;;
    --workflow-ref)
      WORKFLOW_REF="$2"
      shift 2
      ;;
    --sync-status)
      SYNC_STATUS="$2"
      shift 2
      ;;
    --watch-path)
      WATCH_PATHS+=("$2")
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "$MODE" in
  workflow|local|off) ;;
  *)
    echo "error: invalid relay mode: $MODE" >&2
    exit 1
    ;;
esac

if [[ -z "$PI_MONO_DIR" ]]; then
  PI_MONO_DIR="$CONTRIB_ROOT/pi-mono"
fi
if [[ -z "$PI_EXTENSIONS_DIR" ]]; then
  PI_EXTENSIONS_DIR="$CONTRIB_ROOT/../owned/pi-extensions"
fi
if [[ -z "$STATE_FILE" ]]; then
  STATE_FILE="$CONTRIB_ROOT/.state/pi-mono-compatibility-relay/pi-mono.current-head"
fi
if [[ -z "$RECEIPTS_DIR" ]]; then
  RECEIPTS_DIR="$CONTRIB_ROOT/.logs/pi-mono-compatibility-relay"
fi

require_cmd git

if [[ ! -d "$PI_MONO_DIR/.git" ]]; then
  echo "pi-compat-relay: skip (pi-mono repo not found at $PI_MONO_DIR)"
  exit 0
fi

current_head="$(git -C "$PI_MONO_DIR" rev-parse HEAD)"
current_branch="$(git -C "$PI_MONO_DIR" symbolic-ref -q --short HEAD 2>/dev/null || echo detached-head)"

load_state
previous_head="$LAST_PROCESSED_HEAD"

if [[ -z "$previous_head" ]]; then
  receipt="$(record_receipt "initialized" "baseline-recorded" "" "$current_head" "$current_branch" "" "" "" "")"
  echo "pi-compat-relay: initialized baseline at $current_head"
  echo "pi-compat-relay: receipt $receipt"
  if [[ "$DRY_RUN" != "1" ]]; then
    write_state "$current_head" "$current_branch"
  fi
  exit 0
fi

if [[ "$current_head" == "$previous_head" ]]; then
  echo "pi-compat-relay: no upstream pi-mono head change"
  exit 0
fi

comparison_reason="head-changed"
if ! git -C "$PI_MONO_DIR" cat-file -e "${previous_head}^{commit}" 2>/dev/null; then
  comparison_reason="previous-head-unavailable"
fi

changed_paths=()
if [[ "$comparison_reason" == "head-changed" ]]; then
  while IFS= read -r path; do
    [[ -n "$path" ]] || continue
    changed_paths+=("$path")
  done < <(git -C "$PI_MONO_DIR" diff --name-only "$previous_head" "$current_head" -- "${WATCH_PATHS[@]}")
fi

if [[ "$comparison_reason" == "head-changed" && ${#changed_paths[@]} -eq 0 ]]; then
  receipt="$(record_receipt "skipped" "no-relevant-path-change" "$previous_head" "$current_head" "$current_branch" "" "" "" "")"
  echo "pi-compat-relay: upstream changed but no watched pi surface moved"
  echo "pi-compat-relay: receipt $receipt"
  if [[ "$DRY_RUN" != "1" ]]; then
    write_state "$current_head" "$current_branch"
  fi
  exit 0
fi

if [[ "$MODE" == "off" ]]; then
  receipt="$(record_receipt "skipped" "relay-disabled" "$previous_head" "$current_head" "$current_branch" "" "" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: relevant upstream change detected, but relay mode is off"
  echo "pi-compat-relay: receipt $receipt"
  exit 0
fi

if [[ "$DRY_RUN" == "1" ]]; then
  receipt="$(record_receipt "dry-run" "$comparison_reason" "$previous_head" "$current_head" "$current_branch" "" "" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: dry-run would trigger downstream compatibility canary"
  echo "pi-compat-relay: receipt $receipt"
  exit 0
fi

if [[ "$MODE" == "local" ]]; then
  require_cmd node
  if [[ ! -f "$PI_EXTENSIONS_DIR/scripts/pi-host-compatibility-canary.mjs" ]]; then
    receipt="$(record_receipt "failed" "missing-local-canary-runner" "$previous_head" "$current_head" "$current_branch" "" "" "" "" "${changed_paths[@]}")"
    echo "pi-compat-relay: local canary runner missing at $PI_EXTENSIONS_DIR/scripts/pi-host-compatibility-canary.mjs" >&2
    echo "pi-compat-relay: receipt $receipt"
    exit 1
  fi

  set +e
  dispatch_output="$(cd "$PI_EXTENSIONS_DIR" && PI_HOST_VERSION="$current_head" node ./scripts/pi-host-compatibility-canary.mjs run --profile "$PROFILE" 2>&1)"
  dispatch_status=$?
  set -e

  if [[ $dispatch_status -eq 0 ]]; then
    receipt="$(record_receipt "local-passed" "$comparison_reason" "$previous_head" "$current_head" "$current_branch" "" "$dispatch_output" "" "" "${changed_paths[@]}")"
    echo "pi-compat-relay: local downstream canary passed"
    echo "pi-compat-relay: receipt $receipt"
    write_state "$current_head" "$current_branch"
    exit 0
  fi

  receipt="$(record_receipt "local-failed" "$comparison_reason" "$previous_head" "$current_head" "$current_branch" "" "$dispatch_output" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: local downstream canary failed" >&2
  echo "pi-compat-relay: receipt $receipt" >&2
  exit 1
fi

require_cmd gh
if [[ ! -d "$PI_EXTENSIONS_DIR/.git" ]]; then
  receipt="$(record_receipt "failed" "missing-pi-extensions-repo" "$previous_head" "$current_head" "$current_branch" "" "" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: pi-extensions repo not found at $PI_EXTENSIONS_DIR" >&2
  echo "pi-compat-relay: receipt $receipt" >&2
  exit 1
fi

repo_slug="$(resolve_repo_slug "$PI_EXTENSIONS_DIR" || true)"
if [[ -z "$repo_slug" ]]; then
  receipt="$(record_receipt "failed" "missing-pi-extensions-origin" "$previous_head" "$current_head" "$current_branch" "" "" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: could not resolve pi-extensions origin repo slug" >&2
  echo "pi-compat-relay: receipt $receipt" >&2
  exit 1
fi

workflow_ref="$(resolve_workflow_ref "$PI_EXTENSIONS_DIR")"
set +e
dispatch_output="$(gh workflow run "$WORKFLOW_FILE" --repo "$repo_slug" --ref "$workflow_ref" -f profile="$PROFILE" 2>&1)"
dispatch_status=$?
set -e

if [[ $dispatch_status -ne 0 ]]; then
  receipt="$(record_receipt "dispatch-failed" "$comparison_reason" "$previous_head" "$current_head" "$current_branch" "$repo_slug" "$dispatch_output" "" "" "${changed_paths[@]}")"
  echo "pi-compat-relay: failed to dispatch downstream canary workflow" >&2
  if [[ "$dispatch_output" == *"workflow ${WORKFLOW_FILE} not found"* ]]; then
    echo "pi-compat-relay: hint: the workflow file is not yet available on the target remote branch; use local mode for pre-merge verification." >&2
  fi
  echo "pi-compat-relay: receipt $receipt" >&2
  exit 1
fi

run_id=""
run_url=""
recent_run="$(lookup_recent_workflow_run "$repo_slug" "$workflow_ref" || true)"
if [[ -n "$recent_run" ]]; then
  run_id="${recent_run%%$'\t'*}"
  run_url="${recent_run#*$'\t'}"
fi

receipt="$(record_receipt "workflow-dispatched" "$comparison_reason" "$previous_head" "$current_head" "$current_branch" "$repo_slug" "$dispatch_output" "$run_url" "$run_id" "${changed_paths[@]}")"
echo "pi-compat-relay: dispatched downstream canary workflow ($repo_slug:$workflow_ref profile=$PROFILE)"
if [[ -n "$run_url" ]]; then
  echo "pi-compat-relay: run $run_url"
fi
echo "pi-compat-relay: receipt $receipt"
write_state "$current_head" "$current_branch"
