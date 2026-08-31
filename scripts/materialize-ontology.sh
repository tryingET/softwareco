#!/usr/bin/env sh
set -eu
repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec python3 -I -S -B "$repo_root/scripts/materialize-ontology.py" --repo-root "$repo_root" "$@"
