#!/usr/bin/env sh
# Scan git-staged files with the contrib UBS checkout (not ~/.local/bin/ubs).
# Uses `ubs --staged` rather than an explicit file list: UBS scans explicitly
# named files even when .ubsignore excludes them, so a repo's ignore list (for
# example intentionally buggy test fixtures) only applies in --staged mode.
# Exit 0 if nothing staged or UBS detects no language to scan in the staged files.
# Exit 1 if UBS reports criticals. Missing scanner -> 2.
set -eu

# The hooks run the service worktree (branch `local`: upstream plus local
# adoptions), a linked worktree that contrib-all-repos-pull.timer skips. The
# primary checkout is the upstream mirror the timer keeps fresh (see
# contrib/docs/project/2026-09-25-contrib-fork-service-branch-many-of-the-greats.md).
contrib_dir="$HOME/ai-society/softwareco/contrib"
if [ -n "${UBS_BIN:-}" ]; then
	ubs_bin="$UBS_BIN"
elif [ -x "$contrib_dir/ultimate_bug_scanner-local/ubs" ]; then
	ubs_bin="$contrib_dir/ultimate_bug_scanner-local/ubs"
else
	ubs_bin="$contrib_dir/ultimate_bug_scanner/ubs"
	echo "ubs-staged: service worktree $contrib_dir/ultimate_bug_scanner-local missing; using the upstream mirror checkout (no local adoptions)" >&2
fi
if [ ! -x "$ubs_bin" ]; then
	echo "ubs-staged: scanner not executable: $ubs_bin" >&2
	exit 2
fi

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
	echo "ubs-staged: not a git work tree" >&2
	exit 2
}

cd "$(git rev-parse --show-toplevel)"

staged_count="$(git diff --cached --name-only --diff-filter=ACMR | grep -c . || true)"
if [ "$staged_count" -eq 0 ]; then
	exit 0
fi

echo "ubs-staged: scanning $staged_count staged file(s) with $ubs_bin --staged"
# UBS exits 3 for "nothing scanned: no supported language detected", which for
# staged files is the same case as nothing staged (e.g. a docs-only commit).
# But 3 can also propagate from a failing module or tool, so pass only when
# UBS's machine-readable result confirms that no language was detected.
rc=0
"$ubs_bin" --ci --staged || rc=$?
if [ "$rc" -eq 3 ]; then
	result="$("$ubs_bin" --ci --staged --format=json 2>/dev/null || true)"
	case "$result" in
	*'"result":"no-supported-languages"'*)
		echo "ubs-staged: UBS detected no language to scan in the staged files; nothing to check"
		exit 0
		;;
	esac
fi
exit "$rc"
