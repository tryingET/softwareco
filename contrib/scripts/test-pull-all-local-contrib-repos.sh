#!/usr/bin/env bash
# Requires Bash, Git, and the same Unix tools as the updater. No gh/network needed.
# Usage: test-pull-all-local-contrib-repos.sh [updater-path [baseline-path]]
# Only copies inputs; all execution/mutation is inside a fresh owned TMPDIR tree.
set -Eeuo pipefail
umask 077
fail() { echo "FAIL: $*" >&2; exit 1; }
[[ $# -le 2 ]] || fail 'expected [updater [baseline]]'
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UPDATER="${1:-$SCRIPT_DIR/pull-all-local-contrib-repos.sh}"
BASELINE="${2:-}"
[[ -f "$UPDATER" ]] || fail "missing updater: $UPDATER"
[[ -z "$BASELINE" || -f "$BASELINE" ]] || fail "missing baseline: $BASELINE"
[[ ${TMPDIR:-} == /* && -d "$TMPDIR" ]] || fail 'set TMPDIR to an owned scratch directory'
REAL_GIT="$(command -v git)"
export REAL_GIT
SANDBOX="$(mktemp -d "$TMPDIR/updater tests.XXXXXXXX")"
export SANDBOX
# Retain fixtures/evidence, including on failure; never delete caller-owned data.
trap 'echo "Evidence: $SANDBOX"' EXIT
cp "$UPDATER" "$SANDBOX/updater under test.sh"
if [[ -n "$BASELINE" ]]; then cp "$BASELINE" "$SANDBOX/baseline.sh"; fi
# Discard inherited Git routing/config/trace/hooks/provider settings.
for var in ${!GIT_@}; do unset "$var"; done
unset GH_TOKEN GITHUB_TOKEN GH_HOST GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN
export HOME="$SANDBOX/home" XDG_CONFIG_HOME="$SANDBOX/home/config"
export GH_CONFIG_DIR="$SANDBOX/home/gh" GIT_CONFIG_GLOBAL="$SANDBOX/home/gitconfig"
export GIT_CONFIG_NOSYSTEM=1 GIT_ALLOW_PROTOCOL=file GIT_TERMINAL_PROMPT=0
export GIT_OPTIONAL_LOCKS=0 GIT_ATTR_NOSYSTEM=1 LC_ALL=C
export GIT_AUTHOR_NAME=Fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=Fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
export GIT_TEMPLATE_DIR="$SANDBOX/empty template" TMPDIR="$SANDBOX/tmp"
mkdir -p "$HOME" "$GIT_TEMPLATE_DIR" "$TMPDIR" "$SANDBOX/bin"
: > "$GIT_CONFIG_GLOBAL"
export LOCAL_ORIGIN="$SANDBOX/local origin.git" TRACE="$SANDBOX/trace"
export META_MODE='' META_TARGET='' NO_RELEASE=0
cat > "$SANDBOX/bin/gh" <<'GH'
#!/usr/bin/env bash
set -Eeuo pipefail
case "$PWD" in "$SANDBOX"/*) ;; *) exit 90;; esac
case "$*" in
  'auth status -h github.com'|'auth setup-git') printf 'auth %s\n' "$*" >> "$TRACE" ;;
  'release list --repo fixture/example --limit 1 --exclude-drafts --exclude-pre-releases --json tagName --jq .[0].tagName // ""')
    echo release >> "$TRACE"
    if [[ "$NO_RELEASE" == 0 ]]; then echo v1.0.0; fi ;;
  *) echo "BLOCKED gh $*" >> "$TRACE"; exit 91 ;;
esac
GH
cat > "$SANDBOX/bin/git" <<'GIT'
#!/usr/bin/env bash
set -Eeuo pipefail
repo="$PWD"
if [[ ${1:-} == -C ]]; then repo="$2"; shift 2; fi
case "$repo" in "$SANDBOX"/*) ;; *) echo 'BLOCKED git path' >> "$TRACE"; exit 90;; esac
printf 'git %q ' "$repo" >> "$TRACE"; printf '%q ' "$@" >> "$TRACE"; echo >> "$TRACE"
if [[ "$repo" == "$META_TARGET" && ${1:-} == rev-parse && ${2:-} == --path-format=absolute ]]; then
  case "$META_MODE:$3" in
    fail-dir:--git-dir|fail-common:--git-common-dir) exit 1 ;;
    empty-dir:--git-dir|empty-common:--git-common-dir) exit 0 ;;
  esac
fi
case "${1:-}" in
  fetch)
    remote="$2"; shift 2
    [[ "$remote" == origin || "$remote" == upstream ]] || exit 92
    case "$*" in
      '--prune --no-tags --quiet'|'--quiet --no-tags refs/tags/v1.0.0:refs/tags/v1.0.0') ;;
      *) echo 'BLOCKED fetch args' >> "$TRACE"; exit 92 ;;
    esac
    echo "fetch $remote" >> "$TRACE"
    # Stored GitHub URL drives release policy; ONLY the transport is mapped locally.
    exec "$REAL_GIT" -C "$repo" -c "url.$LOCAL_ORIGIN.insteadOf=https://github.com/fixture/example.git" fetch "$remote" "$@" ;;
  config)
    [[ "$*" == 'config --global --get-all credential.helper' || "$*" == 'config --get remote.origin.url' || "$*" == 'config --local --get-all contrib.syncMode' ]] || exit 93 ;;
  remote) [[ "$*" == 'remote get-url origin' ]] || exit 94 ;;
  rev-parse|for-each-ref|check-ref-format|show-ref|merge-base|status) ;;
  symbolic-ref) [[ ${2:-} == -q ]] || exit 95 ;;
  checkout|merge) echo "mutation $1" >> "$TRACE" ;;
  *) echo "BLOCKED git $*" >> "$TRACE"; exit 96 ;;
esac
exec "$REAL_GIT" -C "$repo" "$@"
GIT
chmod +x "$SANDBOX/bin/"*
export PATH="$SANDBOX/bin:$PATH"
g() { "$REAL_GIT" "$@"; }
# The release really predates two maintained commits (not mocked rev-parse output).
g init -q -b main "$SANDBOX/seed"
printf 'release\n' > "$SANDBOX/seed/tracked file"
g -C "$SANDBOX/seed" add .
GIT_AUTHOR_DATE=2001-01-01T00:00:00Z GIT_COMMITTER_DATE=2001-01-01T00:00:00Z g -C "$SANDBOX/seed" commit -qm release
g -C "$SANDBOX/seed" tag v1.0.0
RELEASE="$(g -C "$SANDBOX/seed" rev-parse HEAD)"
for n in 2 3; do
  printf 'maintained %s\n' "$n" >> "$SANDBOX/seed/tracked file"
  g -C "$SANDBOX/seed" add .
  GIT_AUTHOR_DATE="200$n-01-01T00:00:00Z" GIT_COMMITTER_DATE="200$n-01-01T00:00:00Z" g -C "$SANDBOX/seed" commit -qm "maintained $n"
done
MAINTAINED="$(g -C "$SANDBOX/seed" rev-parse HEAD)"
[[ $(g -C "$SANDBOX/seed" rev-list --count v1.0.0..HEAD) == 2 ]] || fail 'release ancestry'
g clone -q --bare "$SANDBOX/seed" "$LOCAL_ORIGIN"
clone_repo() {
  g clone -q --no-hardlinks --no-tags "$LOCAL_ORIGIN" "$1"
  g -C "$1" remote set-url origin https://github.com/fixture/example.git
}
new_linked() {
  CASE="$SANDBOX/$1"; ROOT="$CASE/scan root"; REPO="$ROOT/linked tree"
  mkdir -p "$ROOT"
  clone_repo "$CASE/primary tree"
  g -C "$CASE/primary tree" worktree add -q -b maintained "$REPO"
  if [[ "$2" == dirty ]]; then
    echo staged >> "$REPO/tracked file"; g -C "$REPO" add .
    echo unstaged >> "$REPO/tracked file"
    echo untracked > "$REPO/untracked file"
    mkdir "$REPO/untracked directory"; echo nested > "$REPO/untracked directory/file"
    ln -s 'tracked file' "$REPO/untracked link"
  elif [[ "$2" == detached ]]; then
    g -C "$REPO" checkout -q --detach
  fi
}
snapshot() {
  local dest="$CASE/$1" common
  common="$(g -C "$REPO" rev-parse --path-format=absolute --git-common-dir)"
  mkdir "$dest"
  cp -a "$common" "$dest/common"
  cp -a "$REPO" "$dest/tree"
  # Existing updater bookkeeping is NOT part of the topology guard guarantee.
  rm -rf "$dest/tree/.logs" "$dest/tree/.locks"
}
unchanged() {
  snapshot after
  diff -r "$CASE/before" "$CASE/after" > "$CASE/state.diff" || fail "state changed: $CASE"
}
run_updater() {
  local script="$1" root="$2" expected="$3" rc=0; shift 3
  : > "$TRACE"
  (cd "$SANDBOX"; bash "$script" --root "$root" --jobs 1 --jitter-ms 0 --no-pi-compat-relay --strict "$@") > "$CASE/output" 2>&1 || rc=$?
  cp "$TRACE" "$CASE/trace"
  [[ "$rc" == "$expected" ]] || fail "exit $rc expected $expected: $CASE/output"
  ! grep -q BLOCKED "$TRACE" || fail "unexpected command: $CASE/trace"
  LOG="$(find "$root/.logs/github-sync" -type f -name '*.log' -print)"
  [[ -f "$LOG" ]] || fail "missing/ambiguous log: $CASE"
}
assert_result() { grep -Fq "$1"$'\t'"$(basename "$REPO")"$'\t'"$2" "$LOG" || fail "missing $1 $2: $LOG"; }
no_repo_mutation_calls() {
  ! grep -Eq '^(fetch |release$|mutation )' "$TRACE" || fail "mutation/release attempted: $CASE"
}
passed=0
pass() { passed=$((passed + 1)); echo "PASS $*"; }
# Full cross product: clean, staged+unstaged+untracked dirty, detached;
# discovered child vs include-root; execution vs dry-run.
for state in clean dirty detached; do
  for placement in child root; do
    for mode in live dry; do
      new_linked "$state $placement $mode" "$state"
      args=(); scan="$ROOT"
      if [[ "$placement" == root ]]; then scan="$REPO"; args+=(--include-root); fi
      if [[ "$mode" == dry ]]; then args+=(--dry-run); fi
      snapshot before
      run_updater "$SANDBOX/updater under test.sh" "$scan" 0 "${args[@]}"
      assert_result SKIP 'linked worktree'
      no_repo_mutation_calls
      unchanged
      pass "linked $state $placement $mode: common Git metadata + worktree byte-unchanged"
    done
  done
done
# A normal clone AND a .git-file standalone separate-git-dir must remain eligible.
for topology in directory separate explicit-release; do
  CASE="$SANDBOX/ordinary $topology"; ROOT="$CASE/scan root"; REPO="$ROOT/ordinary tree"
  mkdir -p "$ROOT"; clone_repo "$REPO"
  if [[ "$topology" == explicit-release ]]; then g -C "$REPO" config --local contrib.syncMode release; fi
  if [[ "$topology" == separate ]]; then
    g -C "$REPO" init -q --separate-git-dir "$CASE/separate metadata"
    [[ -f "$REPO/.git" ]] || fail 'expected .git file'
  fi
  [[ $(g -C "$REPO" rev-parse --path-format=absolute --git-dir) == "$(g -C "$REPO" rev-parse --path-format=absolute --git-common-dir)" ]] || fail 'not standalone'
  run_updater "$SANDBOX/updater under test.sh" "$ROOT" 0
  assert_result OK 'fetched=origin; release=v1.0.0:checked-out'
  [[ $(g -C "$REPO" rev-parse HEAD) == "$RELEASE" ]] || fail 'release not checked out'
  ! g -C "$REPO" symbolic-ref -q HEAD >/dev/null || fail 'release not detached'
  grep -qx 'fetch origin' "$TRACE"; grep -qx release "$TRACE"
  pass "standalone $topology updates via local fetch to older release"
done
# Keep the no-release branch fast-forward and different-upstream policy exercised.
CASE="$SANDBOX/no release upstream"; ROOT="$CASE/scan root"; REPO="$ROOT/ordinary tree"
mkdir -p "$ROOT"; clone_repo "$REPO"
g -C "$REPO" reset -q --hard "$RELEASE"
g -C "$REPO" remote add upstream https://github.com/fixture/example.git
g -C "$REPO" config branch.main.remote upstream
export NO_RELEASE=1
run_updater "$SANDBOX/updater under test.sh" "$ROOT" 0
export NO_RELEASE=0
assert_result OK 'fetched=origin,upstream; release=none; default=main:checked-out-fast-forwarded'
[[ $(g -C "$REPO" rev-parse HEAD) == "$MAINTAINED" ]] || fail 'no fast-forward'
grep -qx 'fetch origin' "$TRACE"; grep -qx 'fetch upstream' "$TRACE"
pass 'no-release default fast-forward and distinct upstream fetch preserved'
# Explicit branch mode must ignore available releases, retain safety guards,
# and stay on main across repeated runs (including HEAD equal to release).
for state in clean detached dirty diverged release-head; do
  CASE="$SANDBOX/branch policy $state"; ROOT="$CASE/scan root"; REPO="$ROOT/ordinary tree"
  mkdir -p "$ROOT"; clone_repo "$REPO"
  g -C "$REPO" config --local contrib.syncMode branch
  g -C "$REPO" reset -q --hard "$RELEASE"
  case "$state" in
    detached) g -C "$REPO" checkout -q --detach ;;
    dirty) echo retained >> "$REPO/tracked file" ;;
    diverged)
      echo local >> "$REPO/tracked file"; g -C "$REPO" add .
      g -C "$REPO" commit -qm local ;;
    release-head) g -C "$REPO" checkout -q main ;;
  esac
  before_head="$(g -C "$REPO" rev-parse HEAD)"
  before_bytes="$(g -C "$REPO" hash-object 'tracked file')"
  run_updater "$SANDBOX/updater under test.sh" "$ROOT" 0
  ! grep -qx release "$TRACE" || fail 'branch policy queried GitHub releases'
  case "$state" in
    dirty|diverged)
      assert_result WARN "fetched=origin; policy=branch | warnings=default=main:$(if [[ "$state" == dirty ]]; then echo blocked-dirty; else echo diverged; fi)"
      [[ $(g -C "$REPO" rev-parse HEAD) == "$before_head" ]] || fail 'unsafe HEAD change'
      [[ $(g -C "$REPO" hash-object 'tracked file') == "$before_bytes" ]] || fail 'unsafe file change'
      ! grep -q '^mutation ' "$TRACE" || fail 'blocked branch attempted checkout/merge' ;;
    *)
      assert_result OK 'fetched=origin; policy=branch; default=main:checked-out-fast-forwarded'
      [[ $(g -C "$REPO" symbolic-ref --short HEAD) == main ]] || fail 'branch mode detached HEAD'
      [[ $(g -C "$REPO" rev-parse HEAD) == "$MAINTAINED" ]] || fail 'branch mode not current'
      # Separate log directory avoids timestamp-dependent ambiguity on rerun.
      mv "$ROOT/.logs" "$CASE/first-run-logs"
      run_updater "$SANDBOX/updater under test.sh" "$ROOT" 0
      assert_result OK 'fetched=origin; policy=branch; default=main:current'
      [[ $(g -C "$REPO" symbolic-ref --short HEAD) == main ]] || fail 'repeat run detached HEAD'
      ! grep -qx release "$TRACE" || fail 'repeat branch run queried releases' ;;
  esac
  pass "branch policy $state with release available"
done
for policy in branch release invalid duplicate empty valid-empty trailing-newline embedded-newline; do
  CASE="$SANDBOX/policy dry $policy"; ROOT="$CASE/scan root"; REPO="$ROOT/ordinary tree"
  mkdir -p "$ROOT"; clone_repo "$REPO"
  value="$policy"
  case "$policy" in
    empty) value='' ;;
    duplicate|valid-empty) value=release ;;
    trailing-newline) value=$'release\n' ;;
    embedded-newline) value=$'branch\nrelease' ;;
  esac
  g -C "$REPO" config --local contrib.syncMode "$value"
  if [[ "$policy" == duplicate ]]; then g -C "$REPO" config --local --add contrib.syncMode release; fi
  if [[ "$policy" == valid-empty ]]; then g -C "$REPO" config --local --add contrib.syncMode ''; fi
  snapshot before
  for mode in live dry; do
    # Valid policy live behavior was tested above; this block checks dry-run.
    [[ "$mode" != live || ( "$policy" != branch && "$policy" != release ) ]] || continue
    args=(); [[ "$mode" != dry ]] || args+=(--dry-run)
    expected=2; [[ "$policy" != branch && "$policy" != release ]] || expected=0
    if [[ -d "$ROOT/.logs" ]]; then mv "$ROOT/.logs" "$CASE/$mode-previous-logs"; fi
    run_updater "$SANDBOX/updater under test.sh" "$ROOT" "$expected" "${args[@]}"
    if [[ "$expected" == 2 ]]; then
      assert_result FAIL 'invalid local contrib.syncMode (expected one branch or release value)'
    else
      assert_result DRYRUN "policy=$policy;"
    fi
    no_repo_mutation_calls
  done
  unchanged
  pass "policy $policy validation/dry-run preserves Git state"
done
# Each metadata query fails independently, both nonzero and successful-empty.
# Also exercise a real malformed .git file, without wrapper fault injection.
for fault in fail-dir empty-dir fail-common empty-common malformed; do
  for mode in live dry; do
    CASE="$SANDBOX/metadata $fault $mode"; ROOT="$CASE/scan root"; REPO="$ROOT/ordinary tree"
    mkdir -p "$ROOT"; clone_repo "$REPO"
    if [[ "$fault" == malformed ]]; then
      printf 'gitdir: %s\n' "$CASE/nonexistent metadata" > "$REPO/.git-broken"
      mv "$REPO/.git" "$CASE/retained metadata"; mv "$REPO/.git-broken" "$REPO/.git"
    fi
    cp -a "$REPO" "$CASE/before"
    export META_TARGET="$REPO" META_MODE="$fault"
    args=(); if [[ "$mode" == dry ]]; then args+=(--dry-run); fi
    run_updater "$SANDBOX/updater under test.sh" "$ROOT" 2 "${args[@]}"
    assert_result FAIL 'cannot determine Git worktree topology'
    no_repo_mutation_calls
    diff -r "$CASE/before" "$REPO" > "$CASE/state.diff" || fail 'metadata failure mutated repo'
    export META_TARGET='' META_MODE=''
    pass "metadata $fault $mode fails closed"
  done
done
if [[ -n "$BASELINE" ]]; then
  new_linked 'baseline regression' clean
  [[ $(g -C "$REPO" rev-parse HEAD) == "$MAINTAINED" ]] || fail 'baseline precondition'
  run_updater "$SANDBOX/baseline.sh" "$ROOT" 0
  assert_result OK 'fetched=origin; release=v1.0.0:checked-out'
  [[ $(g -C "$REPO" rev-parse HEAD) == "$RELEASE" ]] || fail 'baseline did not reproduce regression'
  ! g -C "$REPO" symbolic-ref -q HEAD >/dev/null || fail 'baseline not detached'
  printf 'baseline HEAD: %s -> %s (detached)\n' "$MAINTAINED" "$RELEASE"
  pass 'baseline changes clean linked HEAD; candidate clean-child-live fixture stays unchanged'
fi
[[ ! -s "$GIT_CONFIG_GLOBAL" ]] || fail 'isolated global config unexpectedly changed'
echo "PASS total=$passed; real Git, local-only transport, fake gh, retained evidence"
