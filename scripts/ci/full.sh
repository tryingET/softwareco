#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
AK_CMD="${AK_CMD:-ak}"

# Parent-owned ROCS outputs must never be generated beneath the ontology owner.
required_output_root="governance/ontology-dist"
if [ "${ROCS_OUTPUT_ROOT:-$required_output_root}" != "$required_output_root" ]; then
  echo "error: ROCS_OUTPUT_ROOT must be $required_output_root for the Softwareco parent" >&2
  exit 2
fi
export ROCS_OUTPUT_ROOT="$required_output_root"
export ROCS_AUTHORITY_AGGREGATE=1
export ROCS_CI_PROFILE="${ROCS_CI_PROFILE:-main-strict}"

preflight_managed_outputs() {
  output_dir="$repo_root/$required_output_root"
  [ -d "$output_dir" ] || return 0
  for path in "$output_dir"/* "$output_dir"/.[!.]* "$output_dir"/..?*; do
    [ -e "$path" ] || [ -L "$path" ] || continue
    name="${path##*/}"
    case "$name" in
      .rocs-output-root.json|.authority-receipt.lock|authority-receipt.json|authority-receipt.validate.json|authority-receipt.build.json|resolve.json|summary.json|id_index.json)
        ;;
      *)
        echo "error: refusing ROCS cleanup with unknown managed output: $name" >&2
        exit 1
        ;;
    esac
  done
}

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
python3 -m unittest tests.test_ontology_materializer -q

if [ -f "$repo_root/scripts/check-task-scope-snapshots.sh" ]; then
  "$repo_root/scripts/check-task-scope-snapshots.sh"
fi

if [ "$deep" -eq 1 ]; then
  "$repo_root/scripts/check-template-ci.sh"
fi

if [ ! -x "$repo_root/scripts/rocs.sh" ]; then
  echo "error: missing executable scripts/rocs.sh" >&2
  exit 1
fi
if [ -L "$repo_root/ontology/manifest.yaml" ]; then
  echo "error: ontology manifest may not be a symlink" >&2
  exit 1
fi
if [ ! -f "$repo_root/ontology/manifest.yaml" ]; then
  echo "error: ontology is not materialized; run ./scripts/materialize-ontology.sh" >&2
  exit 1
fi
ROCS_REPO="$repo_root" "$repo_root/scripts/rocs.sh" version
preflight_managed_outputs
ROCS_REPO="$repo_root" "$repo_root/scripts/rocs.sh" cleanup --repo "$repo_root"
ROCS_REPO="$repo_root" "$repo_root/scripts/rocs.sh" validate --repo "$repo_root" --resolve-refs
ROCS_REPO="$repo_root" "$repo_root/scripts/rocs.sh" build --repo "$repo_root" --resolve-refs
python3 -m unittest tests.test_ontology_receipts -q

echo "ok: ci full"
