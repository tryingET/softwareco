#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
AK_CMD="${AK_CMD:-ak}"

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
"$repo_root/scripts/rocs.sh" version
"$repo_root/scripts/rocs.sh" validate --repo . --resolve-refs

echo "ok: ci full"
