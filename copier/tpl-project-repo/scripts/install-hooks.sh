#!/usr/bin/env sh
set -eu
repo_root="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
chmod +x "$repo_root/.githooks/pre-commit" 2>/dev/null || true
if git -C "$repo_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
	git -C "$repo_root" config core.hooksPath .githooks
	echo "Configured git hooks path: .githooks"
else
	echo "warning: not inside a git repository; hook path not configured" >&2
fi
