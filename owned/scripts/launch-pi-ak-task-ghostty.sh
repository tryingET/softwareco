#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Legacy launcher: unavailable without positive DB-free outside-domain classification.
Affected or unknown requests (including batches/presets) refuse before effects.
Only compatible account-bound identity plus whole-request outside classification permits legacy use.
See docs/project/2026-09-07-visible-task-session-lane-custody.md.

For positively outside domains only, launch one Ghostty window per AK task and run:
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
declare -A SEEN_OPTIONS=()
declare -A SEEN_TASKS=()

refuse() {
  echo "error: legacy request refused: $*" >&2
  exit 2
}

once() {
  [ -z "${SEEN_OPTIONS[$1]+present}" ] || refuse "duplicate/conflicting option: $1"
  SEEN_OPTIONS[$1]=1
}

add_task() {
  [[ "$1" =~ ^[1-9][0-9]*$ ]] || refuse "expected a canonical positive task id"
  # Producer v1 task IDs are positive JavaScript safe integers; compare as
  # decimal strings rather than overflowing shell arithmetic on hostile input.
  # shellcheck disable=SC2071  # deliberate string compare of equal-length decimals (no overflow)
  if [ "${#1}" -gt 16 ] || { [ "${#1}" -eq 16 ] && [[ "$1" > 9007199254740991 ]]; }; then
    refuse "task id exceeds producer safe-integer limit"
  fi
  [ "${#TASK_IDS[@]}" -lt 256 ] || refuse "request exceeds producer 256-task limit"
  [ -z "${SEEN_TASKS[$1]+present}" ] || refuse "duplicate task id: $1"
  SEEN_TASKS[$1]=1
  TASK_IDS+=("$1")
}

# Help is standalone: it must not short-circuit a malformed/affected request.
if [ "$#" -eq 1 ] && { [ "$1" = "--help" ] || [ "$1" = "-h" ]; }; then
  usage
  exit 0
fi

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) once dry-run; DRY_RUN=1; shift ;;
    --focus-last) once focus-last; FOCUS_LAST=1; shift ;;
    --interactive|--print)
      once launch-mode; LAUNCH_MODE="${1#--}"; shift ;;
    --hold-open|--no-hold-open)
      once hold-open-mode
      if [ "$1" = --hold-open ]; then HOLD_OPEN_MODE=on; else HOLD_OPEN_MODE=off; fi
      shift ;;
    --log-dir)
      once log-dir
      [ "$#" -ge 2 ] || {
        echo "error: --log-dir requires a directory path" >&2
        exit 2
      }
      [ -n "$2" ] && [[ "$2" != --* ]] || refuse "invalid log directory"
      LOG_DIR="$2"
      shift 2
      ;;
    --justfile-rollout-pilots)
      once justfile-rollout-pilots
      for pilot_id in 609 610 611 612 613 614 615; do
        add_task "$pilot_id"
      done
      shift
      ;;
    -h|--help)
      refuse "help must be used alone"
      ;;
    -*)
      refuse "unknown option: $1"
      ;;
    *)
      add_task "$1"
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

classify_legacy_request() {
  command -v python3 >/dev/null || refuse "DB-free classification unavailable (python3 missing)"
  python3 -I -S -B - "${TASK_IDS[@]}" <<'CLASSIFIER'
# Embedded to keep the runtime consumer on its scoped owning surface.
import hashlib, json, os, re, selectors, shutil, subprocess, sys, time

MAX = 65536
SAFE = 9007199254740991
PRODUCER = {"package": "@tryinget/pi-little-helpers", "version": "0.9.0",
            "interface": "pi.task-session.classification.v1"}

def require(ok):
    if not ok:
        raise ValueError("incompatible classification")

def fields(value, keys):
    require(type(value) is dict and set(value) == set(keys.split()))
    return value

def ident(value):
    require(type(value) is str and re.fullmatch(r"[A-Za-z0-9._-]{1,128}", value))

def sha(value):
    require(type(value) is str and re.fullmatch(r"[a-f0-9]{64}", value))

def integer(value):
    require(type(value) is int and 1 <= value <= SAFE)

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def decode(raw):
    require(len(raw) <= MAX)
    def pairs(items):
        require(len(dict(items)) == len(items))
        return dict(items)
    def invalid(_):
        raise ValueError("invalid JSON number")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=invalid, parse_float=invalid)

def request(task_ids, cwd):
    require(1 <= len(task_ids) <= 256 and len(set(task_ids)) == len(task_ids))
    for task in task_ids:
        integer(task)
    require(os.path.isabs(cwd) and os.path.realpath(cwd) == cwd and os.path.isdir(cwd))
    require(len(cwd.encode("utf-8")) <= 4096 and "\0" not in cwd)
    value = {"schema": "pi.task-session.classify-installed-request.v1",
             "taskIds": task_ids, "cwd": cwd}
    # Stable per semantic classification request, not a launch/admission identity.
    value["requestId"] = "lane-legacy-" + digest(value)
    require(len(canonical(value)) <= MAX)
    return value

def namespace(value):
    fields(value, "id generation snapshotDigest")
    ident(value["id"]); integer(value["generation"]); sha(value["snapshotDigest"])

def identity(value):
    fields(value, "schema producer configured akInstance namespace classificationExport classificationRequestSchema identityDigest")
    require(value["schema"] == "pi.task-session.installed-identity.v1")
    require(value["producer"] == PRODUCER and value["configured"] is True)
    ident(value["akInstance"]); namespace(value["namespace"])
    require(value["classificationExport"] == "classifyInstalledTaskSessionRequest")
    require(value["classificationRequestSchema"] == "pi.task-session.classify-installed-request.v1")
    require(value["identityDigest"] == digest({k: v for k, v in value.items() if k != "identityDigest"}))
    return value

def classification(value, sent, binding):
    fields(value, "schema producer requestDigest namespace identityDigest classification reasons")
    require(value["schema"] == "pi.task-session.classification.v1")
    require(value["producer"] == PRODUCER)
    require(value["requestDigest"] == digest(sent))
    ns = value["namespace"]
    if ns is not None:
        namespace(ns)
        require(ns == binding["namespace"] and value["identityDigest"] == binding["identityDigest"])
    else:
        require(value["classification"] == "unknown" and value["identityDigest"] is None)
    reasons = value["reasons"]
    require(type(reasons) is list and len(reasons) <= 256)
    for reason in reasons:
        ident(reason)
    require(value["classification"] in ("outside", "enrolled", "unknown"))
    require(value["classification"] != "outside" or (ns is not None and reasons == []))
    return value["classification"]

def call(executable, operation, value=None):
    # Bounded pipes; never spill producer output or requests to an attempt file.
    payload = b"" if value is None else canonical(value)
    require(len(payload) <= MAX)
    env = {k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")}
    proc = subprocess.Popen([executable, operation], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
    output = bytearray()
    deadline = time.monotonic() + 3
    try:
        with selectors.DefaultSelector() as poll:
            for pipe in (proc.stdin, proc.stdout):
                os.set_blocking(pipe.fileno(), False)
            poll.register(proc.stdout, selectors.EVENT_READ)
            if payload:
                poll.register(proc.stdin, selectors.EVENT_WRITE)
            else:
                proc.stdin.close()
            while poll.get_map():
                require(time.monotonic() < deadline)
                for key, event in poll.select(min(0.1, max(0, deadline - time.monotonic()))):
                    if event == selectors.EVENT_WRITE:
                        payload = payload[os.write(key.fd, payload[:4096]):]
                        if not payload:
                            poll.unregister(key.fileobj); key.fileobj.close()
                    else:
                        chunk = os.read(key.fd, 4096)
                        if not chunk:
                            poll.unregister(key.fileobj)
                        output.extend(chunk); require(len(output) <= MAX)
            require(proc.wait(timeout=max(0.001, deadline - time.monotonic())) == 0)
        return decode(output)
    finally:
        if proc.poll() is None:
            proc.kill()  # Only this owned, DB-free classifier child, never a worker.
        proc.wait()
        proc.stdin.close(); proc.stdout.close()

def main():
    # One executable identity, no override/alternate command or ordinary AK fallback.
    executable = shutil.which("pi-task-session")
    require(executable is not None)
    executable = os.path.realpath(executable)
    sent = request([int(task) for task in sys.argv[1:]], os.getcwd())
    binding = identity(call(executable, "identity"))
    result = classification(call(executable, "classify-installed", sent), sent, binding)
    require(result == "outside")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("error: legacy request refused: DB-free classification unavailable, incompatible or affected; no fallback", file=sys.stderr)
        sys.exit(2)
CLASSIFIER
}

# This DB-free producer gate precedes legacy dependencies, AK access and log creation.
# Classify the expanded request as a whole, never one task inside the loop.
classify_legacy_request

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
