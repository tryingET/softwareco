#!/bin/sh
set -eu

script_dir="$(cd "$(dirname "$0")" && pwd)"

"$script_dir/smoke.sh"

repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "error: not a git repo" >&2; exit 1; }
AK_CMD="${AK_CMD:-ak}"
cd "$repo_root"

if [ -x "./scripts/check-task-scope-snapshots.sh" ]; then
  ./scripts/check-task-scope-snapshots.sh
fi

if [ -x "./scripts/rocs.sh" ] && [ -f "./ontology/manifest.yaml" ]; then
  # A build overwrites ontology/dist; refuse to clobber uncommitted projection edits.
  # Receipts are excluded: every validate/build rewrites them.
  dist_dirty="$(git status --porcelain --untracked-files=no -- ontology/dist \
    ':(exclude)ontology/dist/authority-receipt*.json' \
    ':(exclude)ontology/dist/.authority-receipt.lock')"
  if [ -n "$dist_dirty" ] && [ "${ROCS_ALLOW_DIRTY_DIST:-0}" != 1 ]; then
    echo "error: ontology/dist has uncommitted changes; commit or stash them before the" >&2
    echo "ROCS build, or set ROCS_ALLOW_DIRTY_DIST=1 to overwrite them:" >&2
    echo "$dist_dirty" >&2
    exit 1
  fi
  ./scripts/rocs.sh version
  ./scripts/rocs.sh validate --repo . --resolve-refs
  # build --clean removes ontology/dist first; restore it if the build fails.
  dist_backup="$(mktemp -d "${TMPDIR:-/tmp}/rocs-dist-backup.XXXXXX")"
  trap 'rm -rf "$dist_backup"' EXIT INT TERM
  if [ -d ./ontology/dist ]; then
    cp -a ./ontology/dist "$dist_backup/dist"
  fi
  if ! ./scripts/rocs.sh build --repo . --resolve-refs --clean; then
    if [ -d "$dist_backup/dist" ]; then
      rm -rf ./ontology/dist
      cp -a "$dist_backup/dist" ./ontology/dist
    fi
    echo "error: rocs build failed; ontology/dist restored" >&2
    exit 1
  fi
fi
