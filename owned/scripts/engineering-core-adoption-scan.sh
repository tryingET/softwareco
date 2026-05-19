#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
default_engineering_core_root="$(CDPATH='' cd -- "$repo_root/../../core/engineering-core" && pwd)"
engineering_core_root="${ENGINEERING_CORE_ROOT:-$default_engineering_core_root}"

args=("scan-adoption" "--scope" "$repo_root" "--repo-root" "$engineering_core_root" "--prefer-repo")

has_write=0
has_json_out=0
has_markdown_out=0
for arg in "$@"; do
  case "$arg" in
    --write) has_write=1 ;;
    --json-out|--json-out=*) has_json_out=1 ;;
    --markdown-out|--markdown-out=*) has_markdown_out=1 ;;
  esac
done

args+=("$@")

if [[ "$has_write" -eq 1 && "$has_json_out" -eq 0 ]]; then
  args+=("--json-out" "$repo_root/governance/engineering-core-adoption-scan.json")
fi
if [[ "$has_write" -eq 1 && "$has_markdown_out" -eq 0 ]]; then
  args+=("--markdown-out" "$repo_root/docs/project/engineering-core-adoption-dashboard.md")
fi

exec uv tool -n run --from "$engineering_core_root" engineering-core "${args[@]}"
