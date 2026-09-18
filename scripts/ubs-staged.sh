#!/usr/bin/env sh
# Scan git-staged files with the contrib UBS checkout (not ~/.local/bin/ubs).
# Exit 0 if nothing staged. Exit 1 if UBS reports criticals. Missing scanner -> 2.
set -eu

ubs_bin="${UBS_BIN:-$HOME/ai-society/softwareco/contrib/ultimate_bug_scanner/ubs}"
if [ ! -x "$ubs_bin" ]; then
	echo "ubs-staged: scanner not executable: $ubs_bin" >&2
	exit 2
fi

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
	echo "ubs-staged: not a git work tree" >&2
	exit 2
}

cd "$(git rev-parse --show-toplevel)"

set --
while IFS= read -r file; do
	[ -n "$file" ] || continue
	[ -f "$file" ] || continue
	set -- "$@" "$file"
done <<EOF
$(git diff --cached --name-only --diff-filter=ACMR)
EOF

if [ "$#" -eq 0 ]; then
	exit 0
fi

echo "ubs-staged: scanning $# staged file(s) with $ubs_bin"
exec "$ubs_bin" --ci "$@"
