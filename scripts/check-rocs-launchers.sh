#!/usr/bin/env sh
# Fleet check for ROCS launcher drift across softwareco L2 repos.
#
# usage: scripts/check-rocs-launchers.sh [--strict] [REPO_DIR...]
#   no REPO_DIR: scan owned/*, infra/*, contrib/* under this repo.
#   --strict: exit 1 when any repo has a finding.
#
# Findings per repo (only repos with scripts/rocs.sh and ontology/manifest.yaml):
#   stale-vendor=<ver>   tools/rocs-cli is older than the tpl-project-repo vendored copy
#                        (old copies reject current ontology-kernel keys such as
#                        examples/anti_examples). Fix: drop tools/rocs-cli so rocs.sh
#                        falls back to ~/ai-society/core/rocs-cli. CI runners have
#                        neither that nor the <repo:...@ref> ontology layers; providing
#                        the workspace in CI is AK #5901, not a vendored copy.
#   no-workspace-root    scripts/rocs.sh does not default ROCS_WORKSPACE_ROOT, so
#                        <repo:...@ref> layers fail to resolve on direct calls (a
#                        default only in scripts/ci/full.sh does not cover them).
#                        Fix: port the default block from copier/tpl-project-repo/scripts/rocs.sh.j2.
#   unsafe-clean-build   scripts/ci/full.sh wipes ontology/dist (`rocs build --clean` or rm -rf)
#                        without both (a) refusing to build over uncommitted tracked dist
#                        edits (ROCS_ALLOW_DIRTY_DIST override) and (b) backing dist up and
#                        restoring it when the build fails. Fix: the ROCS dist guard
#                        prelude from copier/tpl-project-repo/scripts/rocs.sh.j2 (covers
#                        every `rocs.sh build --clean` caller), or the full.sh pattern when
#                        full.sh deletes ontology/dist itself.
#   tracked-receipts     ROCS authority receipts under ontology/dist are committed; every
#                        validate/build rewrites them. Fix: gitignore
#                        ontology/dist/authority-receipt*.json and .authority-receipt.lock,
#                        then `git rm --cached` them.
set -eu

l1_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
template_hashes="$l1_root/copier/tpl-project-repo/tools/rocs-cli/VENDORED_HASHES.json"

strict=0
if [ "${1:-}" = "--strict" ]; then
  strict=1
  shift
fi

vendored_version() {
  file="$1/tools/rocs-cli/VENDORED_HASHES.json"
  [ -f "$file" ] || return 1
  sed -n 's/^[[:space:]]*"upstream_version":[[:space:]]*"\([^"]*\)".*/\1/p' "$file" | head -n 1
}

# 0 when version $1 < $2 (dotted numeric).
version_lt() {
  [ "$1" != "$2" ] || return 1
  lowest="$(printf '%s\n%s\n' "$1" "$2" | sort -t. -k1,1n -k2,2n -k3,3n | head -n 1)"
  [ "$lowest" = "$1" ]
}

template_version="$(vendored_version "$l1_root/copier/tpl-project-repo" || true)"
[ -n "$template_version" ] || { echo "error: cannot read $template_hashes" >&2; exit 2; }

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

  if version="$(vendored_version "$dir")" && [ -n "$version" ]; then
    if version_lt "$version" "$template_version"; then
      findings="$findings stale-vendor=$version"
    fi
  fi

  if ! grep -Eqs 'ROCS_WORKSPACE_ROOT:[-=]' "$dir/scripts/rocs.sh"; then
    findings="$findings no-workspace-root"
  fi

  full="$dir/scripts/ci/full.sh"
  launcher_guard=0
  grep -q 'ROCS_DIST_GUARD_ACTIVE' "$dir/scripts/rocs.sh" && launcher_guard=1
  if [ -f "$full" ] \
    && grep -Eq 'build .*--clean|rm -rf .*ontology/dist' "$full" \
    && ! { grep -Eq 'dist[-_]backup' "$full" && grep -q 'ROCS_ALLOW_DIRTY_DIST' "$full"; } \
    && ! { [ "$launcher_guard" = 1 ] && ! grep -Eq 'rm -rf .*ontology/dist' "$full"; }; then
    findings="$findings unsafe-clean-build"
  fi

  if git -C "$dir" ls-files --error-unmatch ontology/dist/authority-receipt.json >/dev/null 2>&1; then
    findings="$findings tracked-receipts"
  fi

  if [ -n "$findings" ]; then
    findings_total=$((findings_total + 1))
    printf '%s:%s\n' "${dir#"$l1_root"/}" "$findings"
  fi
done

printf 'summary: %s of %s ROCS repo(s) with findings (template vendored rocs-cli %s)\n' \
  "$findings_total" "$scanned" "$template_version"

if [ "$strict" = 1 ] && [ "$findings_total" -gt 0 ]; then
  exit 1
fi
