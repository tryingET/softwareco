#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
core_project_default="${ROCS_CORE_PROJECT:-$HOME/ai-society/core/rocs-cli}"
workspace_root="${ROCS_WORKSPACE_ROOT:-$HOME/ai-society}"
workspace_ref_mode="${ROCS_WORKSPACE_REF_MODE:-loose}"

export ROCS_WORKSPACE_ROOT="$workspace_root"
export ROCS_WORKSPACE_REF_MODE="$workspace_ref_mode"
export ROCS_AUTHORITY_AGGREGATE="${ROCS_AUTHORITY_AGGREGATE:-1}"

say() {
  printf '%s\n' "$*"
}

err() {
  printf '%s\n' "$*" >&2
}

die() {
  err "error: $*"
  exit 1
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

usage() {
  cat <<'EOF'
usage: scripts/rocs.sh [--doctor|--which|--help] [rocs args...]

Portable ROCS launcher with deterministic resolution order:
  1) ROCS_BIN override
  2) workspace core ~/ai-society/core/rocs-cli (or ROCS_CORE_PROJECT)
  3) rocs on PATH

Examples:
  ./scripts/rocs.sh version
  ./scripts/rocs.sh validate --repo . --resolve-refs
  ./scripts/rocs.sh --doctor
  ./scripts/rocs.sh --which
EOF
}

select_runner() {
  if [ -n "${ROCS_BIN:-}" ]; then
    printf '%s\n' "rocs-bin"
    return
  fi

  if [ -d "$core_project_default" ] && [ -f "$core_project_default/pyproject.toml" ] && has_cmd uv; then
    printf '%s\n' "workspace-core-uv"
    return
  fi

  if has_cmd rocs; then
    printf '%s\n' "path-rocs"
    return
  fi

  printf '%s\n' "missing"
}

runner_desc() {
  case "$1" in
    rocs-bin)
      printf 'ROCS_BIN=%s\n' "${ROCS_BIN}"
      ;;
    workspace-core-uv)
      printf 'workspace core via uv --project %s\n' "$core_project_default"
      ;;
    path-rocs)
      printf 'rocs on PATH (%s)\n' "$(command -v rocs)"
      ;;
    missing)
      printf 'unresolved (set ROCS_BIN, install rocs on PATH, or make %s available)\n' "$core_project_default"
      ;;
    *)
      printf 'unknown runner token: %s\n' "$1"
      ;;
  esac
}

doctor() {
  runner="$(select_runner)"

  say "rocs launcher doctor"
  say "- repo_root: $repo_root"
  say "- core_project_default: $core_project_default"
  say "- ROCS_WORKSPACE_ROOT: $ROCS_WORKSPACE_ROOT"
  say "- ROCS_WORKSPACE_REF_MODE: $ROCS_WORKSPACE_REF_MODE"
  say "- has uv: $(has_cmd uv && printf yes || printf no)"
  say "- has rocs on PATH: $(has_cmd rocs && printf yes || printf no)"
  say "- workspace core project present: $([ -f "$core_project_default/pyproject.toml" ] && printf yes || printf no)"
  say "- selected runner: $(runner_desc "$runner")"

  [ "$runner" != "missing" ]
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

if [ "${1:-}" = "--doctor" ]; then
  doctor
  exit $?
fi

runner="$(select_runner)"

if [ "${1:-}" = "--which" ]; then
  runner_desc "$runner"
  [ "$runner" != "missing" ]
  exit $?
fi

case "$runner" in
  rocs-bin)
    exec "$ROCS_BIN" "$@"
    ;;
  workspace-core-uv)
    exec uv --project "$core_project_default" run rocs "$@"
    ;;
  path-rocs)
    exec rocs "$@"
    ;;
  *)
    die "unable to locate rocs runner; install rocs, set ROCS_BIN, or make $core_project_default available"
    ;;
esac
