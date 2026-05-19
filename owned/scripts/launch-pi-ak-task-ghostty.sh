#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Launch one Ghostty window per AK task and run:
  pi -p "read next_session_prompt.md and attend next ak task #<id> and then proceed with the workflow until completed and commited."

Usage:
  ./scripts/launch-pi-ak-task-ghostty.sh [--dry-run] [--focus-last] [--interactive|--print] [--hold-open|--no-hold-open] [--log-dir <dir>] <task-id>...
  ./scripts/launch-pi-ak-task-ghostty.sh [--dry-run] [--focus-last] [--interactive|--print] [--hold-open|--no-hold-open] [--log-dir <dir>] --justfile-rollout-pilots

Options:
  --dry-run                Print the resolved launches without opening windows
  --focus-last             Best-effort focus the final launched Ghostty window via niri
  --interactive            Force interactive `pi "<prompt>"` launches
  --print                  Force non-interactive `pi -p "<prompt>"` launches
  --hold-open              Keep each launched Ghostty shell open after `pi -p` exits
  --no-hold-open           Close each launched Ghostty shell immediately after `pi -p` exits
  --log-dir <dir>          Directory for per-task stdout/stderr logs (print mode)
  --justfile-rollout-pilots
                           Launch the current Justfile rollout pilot task set (609-615)
  -h, --help               Show this help
EOF
}

DRY_RUN=0
FOCUS_LAST=0
LAUNCH_MODE="auto"
HOLD_OPEN_MODE="auto"
LOG_DIR=""
TASK_IDS=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --focus-last)
      FOCUS_LAST=1
      shift
      ;;
    --interactive)
      LAUNCH_MODE="interactive"
      shift
      ;;
    --print)
      LAUNCH_MODE="print"
      shift
      ;;
    --hold-open)
      HOLD_OPEN_MODE="on"
      shift
      ;;
    --no-hold-open)
      HOLD_OPEN_MODE="off"
      shift
      ;;
    --log-dir)
      [ "$#" -ge 2 ] || {
        echo "error: --log-dir requires a directory path" >&2
        exit 2
      }
      LOG_DIR="$2"
      shift 2
      ;;
    --justfile-rollout-pilots)
      TASK_IDS+=(609 610 611 612 613 614 615)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      TASK_IDS+=("$1")
      shift
      ;;
  esac
done

if [ "${#TASK_IDS[@]}" -eq 0 ]; then
  usage >&2
  exit 2
fi

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: missing dependency: $1" >&2
    exit 2
  }
}

need_cmd ghostty
need_cmd pi
need_cmd python3

AK_WRAPPER="${AK_WRAPPER:-$HOME/ai-society/softwareco/owned/agent-kernel/scripts/ak.sh}"
[ -x "$AK_WRAPPER" ] || {
  echo "error: missing AK wrapper: $AK_WRAPPER" >&2
  exit 2
}

LAST_CLASS=""
LAST_REPO_BASENAME=""

launch_mode_for_task_count() {
  case "$LAUNCH_MODE" in
    interactive|print)
      echo "$LAUNCH_MODE"
      ;;
    auto)
      if [ "${#TASK_IDS[@]}" -eq 1 ]; then
        echo "interactive"
      else
        echo "print"
      fi
      ;;
    *)
      echo "error: unexpected launch mode: $LAUNCH_MODE" >&2
      exit 2
      ;;
  esac
}

hold_open_for_launch() {
  case "$HOLD_OPEN_MODE" in
    on)
      echo 1
      ;;
    off)
      echo 0
      ;;
    auto)
      if [ "$(launch_mode_for_task_count)" = "interactive" ]; then
        echo 0
      elif [ "${#TASK_IDS[@]}" -eq 1 ]; then
        echo 1
      else
        echo 0
      fi
      ;;
    *)
      echo "error: unexpected hold-open mode: $HOLD_OPEN_MODE" >&2
      exit 2
      ;;
  esac
}

resolve_task_json() {
  "$AK_WRAPPER" task show "$1" -F json
}

json_field() {
  python3 -c 'import json,sys; print(json.load(sys.stdin).get(sys.argv[1], ""))' "$1"
}

find_niri_window_id_by_app_id() {
  python3 - "$1" <<'PY'
import json, subprocess, sys
app_id = sys.argv[1]
rows = json.loads(subprocess.check_output(["niri", "msg", "-j", "windows"], text=True))
for row in rows:
    if row.get("app_id") == app_id:
        print(row.get("id"))
        break
PY
}

find_niri_window_id_by_title_suffix() {
  python3 - "$1" <<'PY'
import json, subprocess, sys
suffix = sys.argv[1]
rows = json.loads(subprocess.check_output(["niri", "msg", "-j", "windows"], text=True))
# Prefer the most recently listed matching window when multiple titles collide.
for row in reversed(rows):
    title = row.get("title") or ""
    if title == f"π - {suffix}" or title.endswith(f"/{suffix}") or title.endswith(suffix):
        print(row.get("id"))
        break
PY
}

if [ -z "$LOG_DIR" ]; then
  timestamp="$(date +%Y%m%dT%H%M%S)"
  LOG_DIR="${PI_AK_TASK_GHOSTTY_LOG_ROOT:-$HOME/.pi/agent/ghostty-ak-task-launches}/$timestamp"
fi
mkdir -p "$LOG_DIR"

LAUNCH_MODE_DEFAULT="$(launch_mode_for_task_count)"
HOLD_OPEN_DEFAULT="$(hold_open_for_launch)"
echo "log_dir=$LOG_DIR launch_mode_default=$LAUNCH_MODE_DEFAULT hold_open_default=$HOLD_OPEN_DEFAULT"

for task_id in "${TASK_IDS[@]}"; do
  task_json="$(resolve_task_json "$task_id")"
  repo_path="$(printf '%s' "$task_json" | json_field repo)"
  task_title="$(printf '%s' "$task_json" | json_field title)"
  task_status="$(printf '%s' "$task_json" | json_field status)"

  if [ -z "$repo_path" ] || [ ! -d "$repo_path" ]; then
    echo "error: task #$task_id resolved to missing repo path: $repo_path" >&2
    exit 1
  fi

  prompt="read next_session_prompt.md and attend next ak task #${task_id} and then proceed with the workflow until completed and commited."
  unique_class="com.tryinget.pi.ak-task.${task_id}.$(date +%s%N)"

  stdout_log="$LOG_DIR/task-${task_id}.stdout.log"
  stderr_log="$LOG_DIR/task-${task_id}.stderr.log"
  launch_mode="$LAUNCH_MODE_DEFAULT"
  hold_open="$HOLD_OPEN_DEFAULT"

  echo "task=#${task_id} status=${task_status} repo=${repo_path} title=${task_title} class=${unique_class} launch_mode=${launch_mode} hold_open=${hold_open}"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "  prompt=${prompt}"
    if [ "$launch_mode" = "print" ]; then
      echo "  stdout_log=${stdout_log}"
      echo "  stderr_log=${stderr_log}"
    fi
    LAST_CLASS="$unique_class"
    continue
  fi

  if [ "$launch_mode" = "interactive" ]; then
    env \
      PI_TARGET_REPO="$repo_path" \
      PI_LAUNCH_PROMPT="$prompt" \
      PI_TASK_ID="$task_id" \
      PI_TASK_TITLE="$task_title" \
      ghostty --class="$unique_class" -e bash -lc '
        cd "$PI_TARGET_REPO"
        printf "Launching interactive Pi session for task #%s — %s\n" "$PI_TASK_ID" "$PI_TASK_TITLE"
        printf "Repo: %s\n\n" "$PI_TARGET_REPO"
        if pi "$PI_LAUNCH_PROMPT"; then
          status=0
        else
          status=$?
        fi
        printf "\ninteractive pi exit status: %s\n" "$status"
        printf "Task: #%s — %s\n" "$PI_TASK_ID" "$PI_TASK_TITLE"
        printf "Repo: %s\n" "$PI_TARGET_REPO"
        printf "\nPress Enter to close this launcher shell..."
        read -r _
        exit "$status"
      ' >/dev/null 2>&1 &
  else
    env \
      PI_TARGET_REPO="$repo_path" \
      PI_LAUNCH_PROMPT="$prompt" \
      PI_TASK_ID="$task_id" \
      PI_TASK_TITLE="$task_title" \
      PI_TASK_STDOUT_LOG="$stdout_log" \
      PI_TASK_STDERR_LOG="$stderr_log" \
      PI_TASK_HOLD_OPEN="$hold_open" \
      ghostty --class="$unique_class" -e bash -lc '
        set -uo pipefail
        mkdir -p "$(dirname "$PI_TASK_STDOUT_LOG")"
        cd "$PI_TARGET_REPO"
        printf "pi task launcher\n"
        printf "task: #%s — %s\n" "$PI_TASK_ID" "$PI_TASK_TITLE"
        printf "repo: %s\n" "$PI_TARGET_REPO"
        printf "stdout log: %s\n" "$PI_TASK_STDOUT_LOG"
        printf "stderr log: %s\n\n" "$PI_TASK_STDERR_LOG"
        if pi -p "$PI_LAUNCH_PROMPT" \
            > >(tee "$PI_TASK_STDOUT_LOG") \
            2> >(tee "$PI_TASK_STDERR_LOG" >&2); then
          status=0
        else
          status=$?
        fi
        printf "\npi exit status: %s\n" "$status"
        printf "stdout log: %s\n" "$PI_TASK_STDOUT_LOG"
        printf "stderr log: %s\n" "$PI_TASK_STDERR_LOG"
        if [ "$PI_TASK_HOLD_OPEN" = "1" ] || [ "$status" -ne 0 ]; then
          printf "\nPress Enter to close this launcher shell..."
          read -r _
        fi
        exit "$status"
      ' >/dev/null 2>&1 &
  fi

  LAST_CLASS="$unique_class"
  LAST_REPO_BASENAME="$(basename "$repo_path")"
  sleep 0.5
done

if [ "$DRY_RUN" -eq 0 ] && [ "$FOCUS_LAST" -eq 1 ] && command -v niri >/dev/null 2>&1; then
  sleep 1
  window_id="$(find_niri_window_id_by_app_id "$LAST_CLASS" || true)"
  focus_basis="app_id=${LAST_CLASS}"
  if [ -z "$window_id" ] && [ -n "$LAST_REPO_BASENAME" ]; then
    window_id="$(find_niri_window_id_by_title_suffix "$LAST_REPO_BASENAME" || true)"
    focus_basis="title_suffix=${LAST_REPO_BASENAME}"
  fi
  if [ -n "$window_id" ]; then
    niri msg action focus-window --id "$window_id" >/dev/null 2>&1 || true
    echo "focused_last_window=${window_id} basis=${focus_basis}"
  else
    echo "warning: could not resolve last window via niri for app_id=${LAST_CLASS} or repo basename=${LAST_REPO_BASENAME}" >&2
  fi
fi
