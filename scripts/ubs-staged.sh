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

# --no-cargo: the cargo phases (fmt, clippy, check, test, audit) cannot run on staged files alone.
# A staged Cargo.toml made the Rust module report a partial scan (exit 2) and blocked every
# dependency change (agent-kernel AK5021, 2026-09-28). Builds, lints and tests are the repo's own
# validation; the hook keeps the static rules.
echo "ubs-staged: scanning $staged_count staged file(s) with $ubs_bin --staged --no-cargo"
# UBS exits 3 for "nothing scanned: no supported language detected", which for
# staged files is the same case as nothing staged (e.g. a docs-only commit).
# But 3 can also propagate from a failing module or tool, so pass only when
# UBS's machine-readable result confirms that no language was detected.
rc=0
"$ubs_bin" --ci --staged --no-cargo || rc=$?
# UBS scans whole staged files, so a one-line change to a large file failed on criticals nobody
# introduced (agent-kernel main.rs carried 93 in untouched code, 2026-09-28). When the staged scan
# reports criticals, compare per-file, per-rule critical counts between HEAD's versions and the staged
# versions, and fail on any increase. Counts, not `--new-only`: that flag also hides a new instance of
# a rule the file already had. UBS_STAGED_STRICT=1 keeps the whole-file result; without HEAD, TMPDIR
# or a parseable report it stays strict.
if [ "$rc" -eq 1 ] && [ "${UBS_STAGED_STRICT:-0}" != "1" ] && [ -n "${TMPDIR:-}" ] \
	&& git rev-parse --verify --quiet HEAD >/dev/null; then
	work="$(mktemp -d "$TMPDIR/ubs-staged.XXXXXX")"
	trap 'rm -rf "$work"' EXIT
	mkdir -p "$work/head" "$work/staged"
	if [ -f .ubsignore ]; then
		cp .ubsignore "$work/head/.ubsignore"
		cp .ubsignore "$work/staged/.ubsignore"
	fi
	git diff --cached --name-only --diff-filter=ACMR | while IFS= read -r path; do
		mkdir -p "$work/head/$(dirname "$path")" "$work/staged/$(dirname "$path")"
		git show ":$path" >"$work/staged/$path"
		git show "HEAD:$path" >"$work/head/$path" 2>/dev/null || rm -f "$work/head/$path"
	done
	(cd "$work/head" && "$ubs_bin" --ci --no-cargo --format=json . >"$work/head.json" 2>/dev/null) || true
	(cd "$work/staged" && "$ubs_bin" --ci --no-cargo --format=json . >"$work/staged.json" 2>/dev/null) || true
	echo "ubs-staged: comparing critical counts per file and rule with HEAD's versions of the staged files"
	new_rc=0
	python3 - "$work" <<'PY' || new_rc=$?
import collections, json, os, sys
work = sys.argv[1]
def criticals(side):
    try:
        with open(os.path.join(work, side + ".json"), encoding="utf-8") as handle:
            report = json.load(handle)
    except (OSError, ValueError):
        if side == "head":
            return collections.Counter()  # no HEAD versions to scan: every staged critical is new
        print("ubs-staged: the staged scan produced no readable report; keeping the whole-file result", file=sys.stderr)
        sys.exit(1)
    root = os.path.join(work, side)
    counts = collections.Counter()
    for finding in report.get("findings", []):
        if finding.get("severity") == "critical" and not finding.get("suppressed"):
            counts[(os.path.relpath(finding["file"], root), finding["rule_id"])] += 1
    return counts
head, staged = criticals("head"), criticals("staged")
added = {key: staged[key] - head[key] for key in staged if staged[key] > head[key]}
for (path, rule), count in sorted(added.items()):
    print(f"ubs-staged: new critical: {path} {rule} (+{count})", file=sys.stderr)
if added:
    sys.exit(1)
print(f"ubs-staged: all {sum(staged.values())} critical findings are pre-existing in the staged files; "
      "none is new (UBS_STAGED_STRICT=1 restores the whole-file result)")
PY
	exit "$new_rc"
fi
if [ "$rc" -eq 3 ]; then
	result="$("$ubs_bin" --ci --staged --no-cargo --format=json 2>/dev/null || true)"
	case "$result" in
	*'"result":"no-supported-languages"'*)
		echo "ubs-staged: UBS detected no language to scan in the staged files; nothing to check"
		exit 0
		;;
	esac
fi
exit "$rc"
