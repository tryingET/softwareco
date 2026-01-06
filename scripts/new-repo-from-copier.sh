#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
usage: new-repo-from-copier.sh <tpl-agent-repo|tpl-org-repo|tpl-project-repo> <dest-dir> [copier args...]

Notes:
  - Requires `uv` (uses `uvx copier`).
  - Generated repos will include `.copier-answers.yml` (git versioned).
EOF
}

template_name="${1:-}"
dest_dir="${2:-}"
shift 2 || true

if [[ -z "$template_name" || -z "$dest_dir" ]]; then
  usage
  exit 2
fi

copier_cmd=()
if command -v uvx >/dev/null 2>&1; then
  copier_cmd=(uvx copier)
elif command -v uv >/dev/null 2>&1; then
  copier_cmd=(uv tool run copier)
else
  echo "error: missing dependency: uv (or uvx)" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template_dir="$repo_root/copier/$template_name"

if [[ ! -d "$template_dir" ]]; then
  echo "error: unknown copier template: $template_name" >&2
  echo "available:" >&2
  (cd "$repo_root/copier" && ls -1) >&2
  exit 2
fi

"${copier_cmd[@]}" copy "$template_dir" "$dest_dir" "$@"
