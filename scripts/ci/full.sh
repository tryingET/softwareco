#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"

deep=0
case "${1:-}" in
  "") ;;
  --deep) deep=1 ;;
  *)
    echo "usage: full.sh [--deep]" >&2
    exit 2
    ;;
esac

"$repo_root/scripts/ci/smoke.sh"

cd "$repo_root"

if [ -f "$repo_root/governance/work-items.json" ] && [ -f "$repo_root/crates/ak-cli/Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
  (
    cd "$repo_root"
    cargo run --quiet --bin ak -- work-items check --repo "$repo_root" --path "./governance/work-items.json"
  )
fi

if [ -x "$repo_root/scripts/rocs.sh" ] && [ -f "$repo_root/ontology/manifest.yaml" ]; then
  workspace_root="${ROCS_WORKSPACE_ROOT:-$HOME/ai-society}"
  workspace_ref_mode="${ROCS_WORKSPACE_REF_MODE:-strict}"
  if [ "$workspace_ref_mode" != strict ]; then
    echo "error: full CI requires ROCS_WORKSPACE_REF_MODE=strict" >&2
    exit 1
  fi
  ROCS_AUTHORITY_AGGREGATE=1
  export ROCS_AUTHORITY_AGGREGATE
  ROCS_WORKSPACE_ROOT="$workspace_root" ROCS_WORKSPACE_REF_MODE="$workspace_ref_mode" "$repo_root/scripts/rocs.sh" version
  rm -rf "$repo_root/ontology/dist"
  ROCS_WORKSPACE_ROOT="$workspace_root" ROCS_WORKSPACE_REF_MODE="$workspace_ref_mode" "$repo_root/scripts/rocs.sh" validate --repo . --resolve-refs
  ROCS_WORKSPACE_ROOT="$workspace_root" ROCS_WORKSPACE_REF_MODE="$workspace_ref_mode" "$repo_root/scripts/rocs.sh" build --repo . --resolve-refs
fi

if [ "$deep" -eq 1 ]; then
  "$repo_root/scripts/check-template-ci.sh"
fi

echo "ok: ci full"
