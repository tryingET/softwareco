#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="."
MAX_PARALLEL="${MAX_PARALLEL:-4}"
JITTER_MAX_MS="${JITTER_MAX_MS:-500}"
PI_COMPAT_RELAY_MODE="${PI_COMPAT_RELAY_MODE:-workflow}"
PI_COMPAT_PROFILE="${PI_COMPAT_PROFILE:-upgrade}"
DRY_RUN=0
STRICT_FAILURE=0
INCLUDE_ROOT_REPO=0

usage() {
  cat <<'EOF'
Pull all git repos directly inside a folder in parallel, with safe defaults.

Behavior:
  - always fetch origin when present
  - also fetch the current branch's upstream remote when different from origin
  - fetch branch refs with `--no-tags` so conflicting local tags do not block branch freshness
  - prefer the latest stable GitHub Release tag from origin when one exists
  - checkout the latest release in detached HEAD only when the worktree is clean
  - if no release exists, checkout and fast-forward origin's default branch (origin/HEAD, fallback main) when safe

Usage:
  pull-github-user-repos.sh [options]

Options:
  --root <path>                   Directory containing repo checkouts (default: .)
  --jobs <n>                      Parallel pulls (default: 4)
  --jitter-ms <n>                 Per-repo random startup delay in ms (default: 500)
  --include-root                  Also pull the root directory itself if it is a git repo
  --pi-compat-relay-mode <mode>   Downstream relay mode: workflow|local|off (default: workflow)
  --pi-compat-profile <profile>   Downstream pi-extensions canary profile (default: upgrade)
  --no-pi-compat-relay            Disable the pi-mono -> pi-extensions compatibility relay
  --dry-run                       Print what would be done, no git mutations
  --strict                        Exit non-zero if any repo fails
  -h, --help                      Show this help

Environment overrides:
  MAX_PARALLEL, JITTER_MAX_MS, PI_COMPAT_RELAY_MODE, PI_COMPAT_PROFILE
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT_DIR="$2"
      shift 2
      ;;
    --jobs)
      MAX_PARALLEL="$2"
      shift 2
      ;;
    --jitter-ms)
      JITTER_MAX_MS="$2"
      shift 2
      ;;
    --include-root)
      INCLUDE_ROOT_REPO=1
      shift
      ;;
    --pi-compat-relay-mode)
      PI_COMPAT_RELAY_MODE="$2"
      shift 2
      ;;
    --pi-compat-profile)
      PI_COMPAT_PROFILE="$2"
      shift 2
      ;;
    --no-pi-compat-relay)
      PI_COMPAT_RELAY_MODE="off"
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --strict)
      STRICT_FAILURE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! [[ "$MAX_PARALLEL" =~ ^[0-9]+$ ]] || [[ "$MAX_PARALLEL" -lt 1 ]]; then
  echo "--jobs must be an integer >= 1" >&2
  exit 1
fi

if ! [[ "$JITTER_MAX_MS" =~ ^[0-9]+$ ]]; then
  echo "--jitter-ms must be an integer >= 0" >&2
  exit 1
fi

case "$PI_COMPAT_RELAY_MODE" in
  workflow|local|off) ;;
  *)
    echo "--pi-compat-relay-mode must be one of: workflow, local, off" >&2
    exit 1
    ;;
esac

require_cmd gh
require_cmd git
require_cmd xargs
require_cmd flock
require_cmd awk
require_cmd find
require_cmd sort
require_cmd mktemp

run_pi_compat_relay() {
  local relay_script="$ROOT_DIR/scripts/pi-mono-compatibility-relay.sh"
  local sync_status="unknown"

  if [[ ! -x "$relay_script" ]]; then
    echo "pi-compat-relay: skipped (missing executable $relay_script)"
    return 0
  fi

  if [[ -f "$RESULTS_FILE" ]]; then
    sync_status="$(awk -F'\t' '$2=="pi-mono"{print $1; exit}' "$RESULTS_FILE")"
    if [[ -z "$sync_status" ]]; then
      sync_status="missing"
    fi
  fi

  local -a relay_args=(
    --contrib-root "$ROOT_DIR"
    --mode "$PI_COMPAT_RELAY_MODE"
    --profile "$PI_COMPAT_PROFILE"
    --sync-status "$sync_status"
  )

  if [[ "$DRY_RUN" == "1" ]]; then
    relay_args+=(--dry-run)
  fi

  set +e
  relay_output="$(PI_COMPAT_RELAY_MODE="$PI_COMPAT_RELAY_MODE" PI_COMPAT_PROFILE="$PI_COMPAT_PROFILE" "$relay_script" "${relay_args[@]}" 2>&1)"
  relay_status=$?
  set -e

  if [[ -n "$relay_output" ]]; then
    printf '%s\n' "$relay_output"
  fi

  if [[ $relay_status -ne 0 ]]; then
    echo "pi-compat-relay: warning (exit=${relay_status})" >&2
  fi

  return 0
}

ROOT_DIR="$(cd "$ROOT_DIR" && pwd)"
cd "$ROOT_DIR"

if ! gh auth status -h github.com >/dev/null 2>&1; then
  echo "gh is not authenticated for github.com. Run: gh auth login" >&2
  exit 1
fi

# Ensure git uses gh's credential helper (idempotent)
if ! git config --global --get-all credential.helper | grep -q "gh auth git-credential"; then
  gh auth setup-git >/dev/null 2>&1 || true
fi

mkdir -p "$ROOT_DIR/.locks" "$ROOT_DIR/.logs/github-sync"
LOCK_FILE="$ROOT_DIR/.locks/git-pull-all.lock"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "Another run is already in progress (${LOCK_FILE}). Exiting."
  exit 0
fi

mapfile -d '' -t CANDIDATES < <(find "$ROOT_DIR" -mindepth 1 -maxdepth 1 -type d -print0)

REPO_PATHS=()
for dir in "${CANDIDATES[@]}"; do
  if [[ -e "$dir/.git" ]]; then
    REPO_PATHS+=("$dir")
  fi
done

if [[ "$INCLUDE_ROOT_REPO" == "1" && -e "$ROOT_DIR/.git" ]]; then
  REPO_PATHS+=("$ROOT_DIR")
fi

if [[ ${#REPO_PATHS[@]} -eq 0 ]]; then
  echo "No git repos found directly inside ${ROOT_DIR}."
  exit 0
fi

mapfile -d '' -t REPO_PATHS < <(printf '%s\0' "${REPO_PATHS[@]}" | sort -z)

WORKER_SCRIPT="$(mktemp)"
RESULTS_FILE="$(mktemp)"
cleanup() {
  rm -f "$WORKER_SCRIPT" "$RESULTS_FILE"
}
trap cleanup EXIT

cat > "$WORKER_SCRIPT" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail

repo_dir="$1"
root="$2"
dry_run="$3"
jitter_max_ms="$4"

repo="${repo_dir#${root}/}"
if [[ "$repo" == "$repo_dir" ]]; then
  repo="$(basename "$repo_dir")"
fi

emit() {
  printf "%s\t%s\t%s\n" "$1" "$repo" "$2"
}

join_with() {
  local sep="$1"
  shift
  local out=""
  local item
  for item in "$@"; do
    if [[ -n "$out" ]]; then
      out+="$sep"
    fi
    out+="$item"
  done
  printf '%s' "$out"
}

add_remote() {
  local remote="$1"
  local existing
  for existing in "${fetch_remotes[@]}"; do
    if [[ "$existing" == "$remote" ]]; then
      return 0
    fi
  done
  fetch_remotes+=("$remote")
}

github_slug_from_url() {
  local url="$1"
  local slug=""

  case "$url" in
    https://github.com/*)
      slug="${url#https://github.com/}"
      ;;
    http://github.com/*)
      slug="${url#http://github.com/}"
      ;;
    git@github.com:*)
      slug="${url#git@github.com:}"
      ;;
    ssh://git@github.com/*)
      slug="${url#ssh://git@github.com/}"
      ;;
    *)
      return 1
      ;;
  esac

  slug="${slug%.git}"
  slug="${slug%/}"

  if [[ "$slug" =~ ^([^/]+)/([^/]+)$ ]]; then
    printf '%s/%s' "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
    return 0
  fi

  return 1
}

if [[ "$jitter_max_ms" =~ ^[0-9]+$ ]] && (( jitter_max_ms > 0 )); then
  delay_ms=$(( RANDOM % (jitter_max_ms + 1) ))
  delay="$(awk -v ms="$delay_ms" 'BEGIN { printf "%.3f", ms/1000 }')"
  sleep "$delay"
fi

if [[ ! -e "${repo_dir}/.git" ]]; then
  emit "SKIP" "no .git"
  exit 0
fi

if [[ "$dry_run" == "1" ]]; then
  emit "DRYRUN" "would fetch origin/current upstream, prefer latest stable GitHub release tag, else checkout/fast-forward origin default branch when safe"
  exit 0
fi

if ! git -C "$repo_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  emit "SKIP" "not a git worktree"
  exit 0
fi

current_branch="$(git -C "$repo_dir" symbolic-ref -q --short HEAD 2>/dev/null || true)"
current_upstream_ref=""
current_upstream_remote=""
if [[ -n "$current_branch" ]]; then
  current_upstream_ref="$(git -C "$repo_dir" for-each-ref --format='%(upstream)' "refs/heads/${current_branch}" 2>/dev/null)"
  if [[ -n "$current_upstream_ref" ]]; then
    current_upstream_remote="${current_upstream_ref#refs/remotes/}"
    current_upstream_remote="${current_upstream_remote%%/*}"
  fi
fi

declare -a fetch_remotes=()
declare -a details=()
declare -a warnings=()

if git -C "$repo_dir" remote get-url origin >/dev/null 2>&1; then
  add_remote "origin"
fi
if [[ -n "$current_upstream_remote" ]]; then
  add_remote "$current_upstream_remote"
fi

if [[ ${#fetch_remotes[@]} -eq 0 ]]; then
  emit "WARN" "no origin or current-branch upstream remote configured"
  exit 0
fi

for remote in "${fetch_remotes[@]}"; do
  if ! git -C "$repo_dir" fetch "$remote" --prune --no-tags --quiet >/dev/null 2>&1; then
    emit "FAIL" "fetch failed for remote=${remote}"
    exit 0
  fi
done

details+=("fetched=$(join_with , "${fetch_remotes[@]}")")

worktree_status="$(git -C "$repo_dir" status --porcelain 2>/dev/null || true)"
latest_release_tag=""
release_lookup_failed=0
origin_url=""
origin_slug=""

if origin_url="$(git -C "$repo_dir" config --get remote.origin.url 2>/dev/null)"; then
  if origin_slug="$(github_slug_from_url "$origin_url")"; then
    set +e
    latest_release_tag="$(gh release list --repo "$origin_slug" --limit 1 --exclude-drafts --exclude-pre-releases --json tagName --jq '.[0].tagName // ""' 2>/dev/null)"
    gh_release_status=$?
    set -e

    if [[ $gh_release_status -ne 0 ]]; then
      warnings+=("release:lookup-failed")
      release_lookup_failed=1
      latest_release_tag=""
    elif [[ -n "$latest_release_tag" && "$latest_release_tag" != "null" ]]; then
      if ! git -C "$repo_dir" check-ref-format "refs/tags/${latest_release_tag}" >/dev/null 2>&1; then
        warnings+=("release:invalid-tag=${latest_release_tag}")
        release_lookup_failed=1
        latest_release_tag=""
      fi
    else
      details+=("release=none")
      latest_release_tag=""
    fi
  else
    warnings+=("release:origin-not-github")
  fi
else
  warnings+=("release:no-origin-url")
fi

if [[ -n "$latest_release_tag" ]]; then
  release_ref="refs/tags/${latest_release_tag}"
  if git -C "$repo_dir" fetch origin --quiet --no-tags "$release_ref:$release_ref" >/dev/null 2>&1; then
    release_oid="$(git -C "$repo_dir" rev-parse -q --verify "${release_ref}^{commit}" 2>/dev/null || true)"
    head_oid="$(git -C "$repo_dir" rev-parse -q --verify HEAD^{commit} 2>/dev/null || true)"

    if [[ -z "$release_oid" ]]; then
      warnings+=("release=${latest_release_tag}:unresolvable")
    elif [[ "$head_oid" == "$release_oid" ]]; then
      details+=("release=${latest_release_tag}:current")
    elif [[ -n "$worktree_status" ]]; then
      warnings+=("release=${latest_release_tag}:blocked-dirty")
    elif git -C "$repo_dir" checkout --detach --quiet "$release_ref" >/dev/null 2>&1; then
      details+=("release=${latest_release_tag}:checked-out")
    else
      warnings+=("release=${latest_release_tag}:checkout-failed")
    fi
  else
    warnings+=("release=${latest_release_tag}:fetch-tag-failed")
  fi
elif [[ "$release_lookup_failed" == "1" ]]; then
  :
else
  origin_head_ref=""
  default_branch=""
  default_remote_ref=""
  if git -C "$repo_dir" remote get-url origin >/dev/null 2>&1; then
    origin_head_ref="$(git -C "$repo_dir" symbolic-ref -q refs/remotes/origin/HEAD 2>/dev/null || true)"
    if [[ -n "$origin_head_ref" ]]; then
      default_remote_ref="$origin_head_ref"
      default_branch="${origin_head_ref#refs/remotes/origin/}"
    elif git -C "$repo_dir" show-ref --verify --quiet refs/remotes/origin/main; then
      default_remote_ref="refs/remotes/origin/main"
      default_branch="main"
    fi
  fi

  if [[ -n "$default_branch" ]]; then
    if ! git -C "$repo_dir" show-ref --verify --quiet "$default_remote_ref"; then
      warnings+=("origin-default:stale-ref=${default_remote_ref#refs/remotes/}")
    else
      local_default_ref="refs/heads/${default_branch}"
      remote_default_oid="$(git -C "$repo_dir" rev-parse "$default_remote_ref")"
      head_oid="$(git -C "$repo_dir" rev-parse -q --verify HEAD^{commit} 2>/dev/null || true)"

      if git -C "$repo_dir" show-ref --verify --quiet "$local_default_ref"; then
        local_default_oid="$(git -C "$repo_dir" rev-parse "$local_default_ref")"
        if ! git -C "$repo_dir" merge-base --is-ancestor "$local_default_ref" "$default_remote_ref" >/dev/null 2>&1; then
          warnings+=("default=${default_branch}:diverged")
        elif [[ "$head_oid" == "$remote_default_oid" && "$current_branch" == "$default_branch" ]]; then
          details+=("default=${default_branch}:current")
        elif [[ -n "$worktree_status" ]]; then
          warnings+=("default=${default_branch}:blocked-dirty")
        else
          if [[ "$current_branch" != "$default_branch" ]]; then
            if ! git -C "$repo_dir" checkout --quiet "$default_branch" >/dev/null 2>&1; then
              warnings+=("default=${default_branch}:checkout-failed")
            fi
          fi

          if [[ ${#warnings[@]} -eq 0 || "$(join_with , "${warnings[@]}")" != *"default=${default_branch}:checkout-failed"* ]]; then
            if git -C "$repo_dir" merge --ff-only --quiet "$default_remote_ref" >/dev/null 2>&1; then
              new_default_oid="$(git -C "$repo_dir" rev-parse "$local_default_ref")"
              if [[ "$new_default_oid" == "$local_default_oid" ]]; then
                details+=("default=${default_branch}:checked-out")
              else
                details+=("default=${default_branch}:checked-out-fast-forwarded")
              fi
            else
              warnings+=("default=${default_branch}:fast-forward-failed")
            fi
          fi
        fi
      else
        if [[ -n "$worktree_status" ]]; then
          warnings+=("default=${default_branch}:missing-blocked-dirty")
        elif git -C "$repo_dir" checkout --track -b "$default_branch" "origin/${default_branch}" --quiet >/dev/null 2>&1; then
          details+=("default=${default_branch}:created-checked-out")
        else
          warnings+=("default=${default_branch}:missing")
        fi
      fi
    fi
  else
    warnings+=("origin-default:unavailable")
  fi
fi

message_parts=()
if [[ ${#details[@]} -gt 0 ]]; then
  message_parts+=("$(join_with '; ' "${details[@]}")")
fi
if [[ ${#warnings[@]} -gt 0 ]]; then
  message_parts+=("warnings=$(join_with , "${warnings[@]}")")
  emit "WARN" "$(join_with ' | ' "${message_parts[@]}")"
else
  emit "OK" "$(join_with ' | ' "${message_parts[@]}")"
fi
EOF
chmod +x "$WORKER_SCRIPT"

printf '%s\0' "${REPO_PATHS[@]}" \
  | xargs -0 -P "$MAX_PARALLEL" -I{} "$WORKER_SCRIPT" "{}" "$ROOT_DIR" "$DRY_RUN" "$JITTER_MAX_MS" \
  >> "$RESULTS_FILE"

RUN_TS="$(date +%Y-%m-%dT%H:%M:%S%z)"
LOG_FILE="$ROOT_DIR/.logs/github-sync/all-repos-$(date +%Y%m%d-%H%M%S).log"

OK_COUNT="$(awk -F'\t' '$1=="OK"{c++} END{print c+0}' "$RESULTS_FILE")"
WARN_COUNT="$(awk -F'\t' '$1=="WARN"{c++} END{print c+0}' "$RESULTS_FILE")"
FAIL_COUNT="$(awk -F'\t' '$1=="FAIL"{c++} END{print c+0}' "$RESULTS_FILE")"
SKIP_COUNT="$(awk -F'\t' '$1=="SKIP"{c++} END{print c+0}' "$RESULTS_FILE")"
DRYRUN_COUNT="$(awk -F'\t' '$1=="DRYRUN"{c++} END{print c+0}' "$RESULTS_FILE")"

{
  echo "timestamp=${RUN_TS}"
  echo "root=${ROOT_DIR}"
  echo "jobs=${MAX_PARALLEL}"
  echo "repos_total=${#REPO_PATHS[@]}"
  echo "ok=${OK_COUNT} warn=${WARN_COUNT} fail=${FAIL_COUNT} skip=${SKIP_COUNT} dryrun=${DRYRUN_COUNT}"
  echo "---"
  sort "$RESULTS_FILE"
} > "$LOG_FILE"

echo "Sync complete for local repos in ${ROOT_DIR}."
echo "Total: ${#REPO_PATHS[@]} | ok=${OK_COUNT} warn=${WARN_COUNT} fail=${FAIL_COUNT} skip=${SKIP_COUNT} dryrun=${DRYRUN_COUNT}"
echo "Log: ${LOG_FILE}"

run_pi_compat_relay

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  echo "Failed repos:"
  awk -F'\t' '$1=="FAIL"{print " - " $2 ": " $3}' "$RESULTS_FILE"
  if [[ "$STRICT_FAILURE" == "1" ]]; then
    exit 2
  fi
fi
