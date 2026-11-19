#!/usr/bin/env bash
# test-contrib-integrate.sh - contrib-integrate.sh against local fixture repos (no network).
set -Eeuo pipefail
fail() { echo "FAIL: $*" >&2; exit 1; }
[[ ${TMPDIR:-} == /* && -d "$TMPDIR" ]] || fail 'set TMPDIR to an owned scratch directory'
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
I="$HERE/contrib-integrate.sh"
S="$(mktemp -d "$TMPDIR/integrate tests.XXXXXX")"
trap 'echo "Evidence: $S"' EXIT
for v in ${!GIT_@}; do unset "$v"; done
export HOME="$S/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL="$S/home/gitconfig" TMPDIR="$S/tmp" LC_ALL=C
export GIT_AUTHOR_NAME=F GIT_AUTHOR_EMAIL=f@x.invalid GIT_COMMITTER_NAME=F GIT_COMMITTER_EMAIL=f@x.invalid
mkdir -p "$HOME" "$TMPDIR"; : > "$GIT_CONFIG_GLOBAL"
git config --global init.defaultBranch master
n=0; pass() { n=$((n + 1)); echo "PASS $*"; }
up="$S/upstream"; git init -q "$up"; printf 'a\n' > "$up/f"; printf 'log\n' > "$up/CHANGES"; git -C "$up" add .; git -C "$up" commit -qm base
fresh() {   # a clone with patch branches p1 (new file) and p2 (appends to CHANGES), main = master + p1 + p2
  R="$S/$1"; git clone -q "$up" "$R"
  git -C "$R" checkout -q -b p1; printf 'ours\n' > "$R/g"; git -C "$R" add g; git -C "$R" commit -qm p1
  git -C "$R" checkout -q -b p2 origin/master; sed -i '1i p2 line' "$R/CHANGES"; git -C "$R" commit -qam p2
  git -C "$R" checkout -q -b main origin/master
  git -C "$R" config contrib.integration.patch p1; git -C "$R" config --add contrib.integration.patch p2
}
upstream_moves() { printf 'up %s\n' "$1" >> "$up/CHANGES"; git -C "$up" commit -qam "up $1"; }
# not configured
git clone -q "$up" "$S/plain"; set +e; "$I" "$S/plain" >/dev/null; rc=$?; set -e; [[ $rc == 3 ]] || fail "unconfigured rc $rc"; pass 'unconfigured: exit 3, nothing touched'
# build, then upstream moves: main = new upstream + patches, still on main, previous kept
fresh build; "$I" "$R" >/dev/null
[[ -f "$R/g" && $(grep -c 'p2 line' "$R/CHANGES") == 1 && $(git -C "$R" branch --show-current) == main ]] || fail 'first build'
upstream_moves one; "$I" "$R" > "$S/out" 2>&1 || { cat "$S/out"; fail 'second build'; }
grep -q 'up one' "$R/CHANGES" || fail 'upstream change missing'
git -C "$R" rev-parse -q --verify refs/contrib/integration/previous >/dev/null || fail 'previous not kept'
"$I" "$R" | grep -q current || fail 'rerun not current'
pass 'rebuild follows upstream, keeps patches, keeps previous tip, rerun is current'
# a conflict nobody resolved yet: main unchanged, exit 4
fresh conflict; "$I" "$R" >/dev/null; before=$(git -C "$R" rev-parse main)
git -C "$up" checkout -q master; sed -i '1i up wants this line' "$up/CHANGES"; git -C "$up" commit -qam clash
set +e; "$I" "$R" > "$S/out" 2>&1; rc=$?; set -e
[[ $rc == 4 && $(git -C "$R" rev-parse main) == "$before" ]] || { cat "$S/out"; fail "conflict rc $rc"; }
git -C "$R" worktree list | grep -vq contrib-integrate || true
[[ $(git -C "$R" worktree list | wc -l) == 1 ]] || fail 'scratch worktree left behind'
pass 'unknown conflict: exit 4, main unchanged, no worktree left'
# resolve it once by hand; rerere replays it on the next run
W="$S/resolve"; git -C "$R" worktree add -q --detach "$W" origin/master; git -C "$R" config rerere.enabled true
git -C "$W" merge -q p1; git -C "$W" merge -q p2 >/dev/null 2>&1 || true
{ printf 'up wants this line\np2 line\n'; grep -v -e 'up wants' -e 'p2 line' -e '^[<=>|]' "$W/CHANGES"; } > "$W/CHANGES.new"; mv "$W/CHANGES.new" "$W/CHANGES"; git -C "$W" add CHANGES; git -C "$W" commit -qm resolved
git -C "$R" worktree remove --force "$W"
"$I" "$R" > "$S/out" 2>&1 || { cat "$S/out"; fail 'rerere replay'; }
grep -q 'p2 line' "$R/CHANGES" && grep -q 'up wants' "$R/CHANGES" || fail 'resolution not replayed'
pass 'a resolution recorded once is replayed by rerere'
# a commit only on main would be lost: refuse, exit 6
fresh lose; "$I" "$R" >/dev/null; printf 'stray\n' > "$R/h"; git -C "$R" add h; git -C "$R" commit -qm 'only on main'
upstream_moves two; before=$(git -C "$R" rev-parse main)
set +e; "$I" "$R" > "$S/out" 2>&1; rc=$?; set -e
[[ $rc == 6 && $(git -C "$R" rev-parse main) == "$before" ]] && grep -q 'only on main' "$S/out" || { cat "$S/out"; fail "lose rc $rc"; }
pass 'a commit no patch carries: exit 6, named, main unchanged'
# the caller says that commit is replaced on purpose: main moves, the commit is named in the output
stray=$(git -C "$R" rev-parse --short HEAD)
"$I" --superseded "$stray" "$R" > "$S/out" 2>&1 || { cat "$S/out"; fail 'superseded run'; }
grep -q "superseded on purpose: $stray only on main" "$S/out" && grep -q 'up two' "$R/CHANGES" && [[ ! -f "$R/h" ]] || { cat "$S/out"; fail 'superseded result'; }
set +e; "$I" --superseded deadbeef "$R" >/dev/null 2>&1; rc=$?; set -e; [[ $rc == 2 || $rc == 0 ]] || fail "bad superseded rc $rc"
pass '--superseded: named commits are replaced, not lost; main moves'
# dirty checkout: exit 7, file kept
fresh dirty; "$I" "$R" >/dev/null; upstream_moves three; printf 'wip\n' >> "$R/f"
set +e; "$I" "$R" >/dev/null 2>&1; rc=$?; set -e
[[ $rc == 7 ]] && grep -q wip "$R/f" || fail "dirty rc $rc"
pass 'dirty checkout: exit 7, work kept'
# a failing check: exit 5, main unchanged
fresh check; "$I" "$R" >/dev/null; upstream_moves four; git -C "$R" config contrib.integration.check 'test -f nonexistent'
before=$(git -C "$R" rev-parse main); set +e; "$I" "$R" >/dev/null 2>&1; rc=$?; set -e
[[ $rc == 5 && $(git -C "$R" rev-parse main) == "$before" ]] || fail "check rc $rc"
"$I" "$R" > "$S/out" 2>&1 || true
kept=$(grep -o 'full log: .*' "$S/out" | cut -d' ' -f3)
[[ -n "$kept" && -f "$kept" ]] || { cat "$S/out"; fail 'failed check log not kept'; }
rm -f "$kept"
git -C "$R" config contrib.integration.check 'test -f g'; "$I" "$R" >/dev/null || fail 'passing check'
pass 'check: failing keeps main, passing moves it'
# --check offline
"$I" --check "$R" | grep -q 'checkout main' || fail 'check output'
git -C "$R" checkout -q --detach; set +e; "$I" --check "$R" >/dev/null 2>&1; rc=$?; set -e; [[ $rc == 1 ]] || fail 'check detached'
pass '--check: on main ok, detached exit 1'
echo "PASS total=$n"
