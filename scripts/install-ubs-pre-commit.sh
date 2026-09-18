#!/usr/bin/env sh
# Install a pre-commit hook in the current git repo that runs ubs-staged.sh.
# Does not overwrite an existing hook; prints the line to add instead.
set -eu

script_dir="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
staged="$script_dir/ubs-staged.sh"
[ -x "$staged" ] || chmod +x "$staged"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
	echo "error: run this from a git repository" >&2
	exit 2
}

hook="$(git rev-parse --git-path hooks/pre-commit)"
mkdir -p "$(dirname -- "$hook")"

if [ -e "$hook" ]; then
	if grep -F "$staged" "$hook" >/dev/null 2>&1; then
		echo "ubs-staged already referenced from $hook"
		exit 0
	fi
	echo "error: $hook already exists. Add this line before other checks:" >&2
	echo "  \"$staged\" || exit \$?" >&2
	exit 2
fi

cat >"$hook" <<EOF
#!/usr/bin/env sh
set -eu
exec "$staged"
EOF
chmod +x "$hook"
echo "Installed $hook -> $staged"
