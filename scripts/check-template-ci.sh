#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

check_copier() {
  local template="$1"
  local dest_root
  dest_root="$(mktemp -d)"

  echo "==> copier: $template"
  "$repo_root/scripts/new-repo-from-copier.sh" "$template" "$dest_root/$template-test" -d repo_slug="$template-test" --defaults --overwrite >/dev/null 2>&1

  pushd "$dest_root/$template-test" >/dev/null
  git init -b main >/dev/null
  git add .
  git commit -m init >/dev/null
  git checkout -b feature >/dev/null
  echo "# change" >> docs/_local_ci_check.md
  git add docs/_local_ci_check.md
  git commit -m "ci check" >/dev/null
  ./scripts/ci/smoke.sh
  popd >/dev/null
}

echo "checking copier templates..."
check_copier tpl-agent-repo
check_copier tpl-org-repo
check_copier tpl-project-repo

echo "ok: templates ci"
