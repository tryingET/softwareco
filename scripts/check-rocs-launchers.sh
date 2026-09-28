#!/usr/bin/env sh
# Fleet check for ROCS launcher drift across softwareco L2 repos.
#
# usage: scripts/check-rocs-launchers.sh [--strict] [REPO_DIR...]
#   no REPO_DIR: scan owned/*, infra/*, contrib/* under this repo.
#   --strict: exit 1 when any repo has a finding.
#
# Findings per repo (only repos with scripts/rocs.sh and ontology/manifest.yaml).
# Target model (AK #5891): no vendored rocs-cli; scripts/rocs.sh runs ~/ai-society/core/rocs-cli
# only when it satisfies the repo's pinned `rocs_cli_pin` (same major.minor, patch >= pin).
#   legacy-launcher      scripts/rocs.sh has no rocs_cli_pin. Fix: install the launcher from
#                        copier/tpl-project-repo.
#   stale-pin=<ver>      the pin is older than the tpl-project-repo default.
#   vendored-copy        tools/rocs-cli is still committed. Fix: `git rm -r tools/rocs-cli`.
#   unsafe-clean-build   scripts/ci/full.sh runs `rocs build --clean` or deletes ontology/dist
#                        instead of `rocs.sh cleanup` -> validate -> build.
#   tracked-dist         files under ontology/dist are committed. Fix: gitignore ontology/dist/
#                        and `git rm -r --cached ontology/dist`.
set -eu

l1_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
template_copier="$l1_root/copier/tpl-project-repo/copier.yml"

strict=0
if [ "${1:-}" = "--strict" ]; then
  strict=1
  shift
fi

launcher_pin() {
  sed -n 's/^rocs_cli_pin="\([0-9][0-9.]*\)".*/\1/p' "$1/scripts/rocs.sh" | head -n 1
}

# 0 when version $1 < $2 (dotted numeric).
version_lt() {
  [ "$1" != "$2" ] || return 1
  lowest="$(printf '%s\n%s\n' "$1" "$2" | sort -t. -k1,1n -k2,2n -k3,3n | head -n 1)"
  [ "$lowest" = "$1" ]
}

template_version="$(sed -n '/^rocs_cli_version:/,/^[^[:space:]]/s/^[[:space:]]*default:[[:space:]]*"\{0,1\}\([0-9][0-9.]*\)"\{0,1\}.*/\1/p' "$template_copier" | head -n 1)"
[ -n "$template_version" ] || { echo "error: no rocs_cli_version default in $template_copier" >&2; exit 2; }

if [ "$#" -eq 0 ]; then
  set -- "$l1_root"/owned/*/ "$l1_root"/infra/*/ "$l1_root"/contrib/*/
fi

findings_total=0
scanned=0
for dir in "$@"; do
  dir="${dir%/}"
  [ -f "$dir/scripts/rocs.sh" ] && [ -f "$dir/ontology/manifest.yaml" ] || continue
  scanned=$((scanned + 1))
  findings=""

  pin="$(launcher_pin "$dir")"
  if [ -z "$pin" ]; then
    findings="$findings legacy-launcher"
  elif version_lt "$pin" "$template_version"; then
    findings="$findings stale-pin=$pin"
  fi

  if [ -e "$dir/tools/rocs-cli" ]; then
    findings="$findings vendored-copy"
  fi

  full="$dir/scripts/ci/full.sh"
  if [ -f "$full" ] && grep -Eq 'build .*--clean|rm -rf .*ontology/dist' "$full"; then
    findings="$findings unsafe-clean-build"
  fi

  if [ -n "$(git -C "$dir" ls-files -- ontology/dist 2>/dev/null)" ]; then
    findings="$findings tracked-dist"
  fi

  if [ -n "$findings" ]; then
    findings_total=$((findings_total + 1))
    printf '%s:%s\n' "${dir#"$l1_root"/}" "$findings"
  fi
done

printf 'summary: %s of %s ROCS repo(s) with findings (template rocs-cli pin %s)\n' \
  "$findings_total" "$scanned" "$template_version"

if [ "$strict" = 1 ] && [ "$findings_total" -gt 0 ]; then
  exit 1
fi
