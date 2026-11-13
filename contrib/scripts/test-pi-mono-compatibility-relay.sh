#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RELAY_SCRIPT="$REPO_ROOT/scripts/pi-mono-compatibility-relay.sh"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_eq() {
  local expected="$1"
  local actual="$2"
  local message="$3"
  if [[ "$expected" != "$actual" ]]; then
    fail "$message (expected='$expected' actual='$actual')"
  fi
}

assert_contains() {
  local needle="$1"
  local haystack_file="$2"
  local message="$3"
  if ! grep -Fq "$needle" "$haystack_file"; then
    fail "$message (missing '$needle' in $haystack_file)"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

create_git_repo() {
  local dir="$1"
  git init -q "$dir"
  git -C "$dir" config user.name "Pi Relay Test"
  git -C "$dir" config user.email "pi-relay-test@example.com"
}

commit_all() {
  local dir="$1"
  local message="$2"
  git -C "$dir" add -A
  git -C "$dir" commit -q -m "$message"
}

write_local_canary_runner() {
  local pi_extensions_dir="$1"
  mkdir -p "$pi_extensions_dir/scripts"
  cat > "$pi_extensions_dir/scripts/pi-host-compatibility-canary.mjs" <<'EOF'
import { appendFileSync } from "node:fs";
const logPath = process.env.PI_COMPAT_RELAY_TEST_LOG;
if (logPath) {
  appendFileSync(logPath, JSON.stringify({ args: process.argv.slice(2), hostVersion: process.env.PI_HOST_COMPAT_HOST_VERSION || null, changelogRef: process.env.PI_HOST_COMPAT_CHANGELOG_REF || null }) + "\n", "utf8");
}
process.exit(Number(process.env.PI_COMPAT_RELAY_LOCAL_EXIT_CODE || 0));
EOF
}

run_relay() {
  local contrib_root="$1"
  local pi_mono_dir="$2"
  local pi_extensions_dir="$3"
  local state_file="$4"
  local receipts_dir="$5"
  PI_COMPAT_RELAY_CONTRIB_ROOT="$contrib_root" \
  PI_COMPAT_RELAY_PI_MONO_DIR="$pi_mono_dir" \
  PI_COMPAT_RELAY_PI_EXTENSIONS_DIR="$pi_extensions_dir" \
  PI_COMPAT_RELAY_STATE_FILE="$state_file" \
  PI_COMPAT_RELAY_RECEIPTS_DIR="$receipts_dir" \
  PI_COMPAT_EVIDENCE_SCRIPT="$REPO_ROOT/scripts/pi-mono-compatibility-evidence-index.mjs" \
  PI_COMPAT_EVIDENCE_OFFLINE=1 \
  PI_COMPAT_RELAY_MODE=local \
  PI_COMPAT_PROFILE=upgrade \
  "$RELAY_SCRIPT"
}

require_cmd git
require_cmd node

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CONTRIB_ROOT="$TMP_DIR/contrib"
PI_MONO_DIR="$CONTRIB_ROOT/pi-mono"
PI_EXTENSIONS_DIR="$TMP_DIR/owned/pi-extensions"
STATE_FILE="$CONTRIB_ROOT/.state/pi-mono-compatibility-relay/pi-mono.current-head"
EVIDENCE_INDEX_PATH="$CONTRIB_ROOT/.state/pi-mono-compatibility-relay/evidence-index.json"
RECEIPTS_DIR="$CONTRIB_ROOT/.logs/pi-mono-compatibility-relay"
TEST_LOG="$TMP_DIR/canary-invocations.log"
FAKE_BIN="$TMP_DIR/bin"

mkdir -p "$CONTRIB_ROOT" "$TMP_DIR/owned" "$FAKE_BIN"
cat > "$FAKE_BIN/npm" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == view && "$2" == '@earendil-works/pi-coding-agent@1.5.0' ]] || exit 1
printf '%s\n' '{"name":"@earendil-works/pi-coding-agent","version":"1.5.0"}'
EOF
chmod +x "$FAKE_BIN/npm"
export PATH="$FAKE_BIN:$PATH"
create_git_repo "$PI_MONO_DIR"
git -C "$PI_MONO_DIR" remote add origin https://github.com/earendil-works/pi.git
create_git_repo "$PI_EXTENSIONS_DIR"
write_local_canary_runner "$PI_EXTENSIONS_DIR"
: > "$TEST_LOG"

pushd "$PI_MONO_DIR" >/dev/null
mkdir -p docs
printf 'seed\n' > docs/README.md
commit_all "$PI_MONO_DIR" "seed"
popd >/dev/null

pushd "$PI_EXTENSIONS_DIR" >/dev/null
printf 'seed\n' > README.md
commit_all "$PI_EXTENSIONS_DIR" "seed"
popd >/dev/null

run_relay "$CONTRIB_ROOT" "$PI_MONO_DIR" "$PI_EXTENSIONS_DIR" "$STATE_FILE" "$RECEIPTS_DIR"
[[ -f "$STATE_FILE" ]] || fail "state file should be created on initialization"
[[ -f "$EVIDENCE_INDEX_PATH" ]] || fail "evidence index should be rebuilt on initialization"
assert_eq "0" "$(wc -l < "$TEST_LOG" | tr -d ' ')" "initialization should not invoke downstream canary"
assert_contains '"status": "initialized"' "$(find "$RECEIPTS_DIR" -type f | sort | tail -1)" "initial receipt should be recorded"

pushd "$PI_MONO_DIR" >/dev/null
mkdir -p docs/project
printf 'irrelevant\n' > docs/project/notes.md
commit_all "$PI_MONO_DIR" "irrelevant"
popd >/dev/null

run_relay "$CONTRIB_ROOT" "$PI_MONO_DIR" "$PI_EXTENSIONS_DIR" "$STATE_FILE" "$RECEIPTS_DIR"
assert_eq "0" "$(wc -l < "$TEST_LOG" | tr -d ' ')" "irrelevant change should not invoke downstream canary"
assert_contains '"reason": "no-relevant-path-change"' "$(find "$RECEIPTS_DIR" -type f | sort | tail -1)" "irrelevant receipt should be recorded"

pushd "$PI_MONO_DIR" >/dev/null
mkdir -p packages/coding-agent
printf '%s\n' '{"name":"@earendil-works/pi-coding-agent","version":"1.5.0"}' > packages/coding-agent/package.json
printf 'relevant\n' > packages/coding-agent/CHANGELOG.md
commit_all "$PI_MONO_DIR" "relevant"
relevant_head="$(git rev-parse HEAD)"
popd >/dev/null

PI_COMPAT_RELAY_TEST_LOG="$TEST_LOG" run_relay "$CONTRIB_ROOT" "$PI_MONO_DIR" "$PI_EXTENSIONS_DIR" "$STATE_FILE" "$RECEIPTS_DIR"
assert_eq "1" "$(wc -l < "$TEST_LOG" | tr -d ' ')" "relevant change should invoke downstream canary exactly once"
assert_contains '"status": "local-passed"' "$(find "$RECEIPTS_DIR" -type f | sort | tail -1)" "successful local receipt should be recorded"
assert_contains 'packages/coding-agent/CHANGELOG.md' "$(find "$RECEIPTS_DIR" -type f | sort | tail -1)" "receipt should include watched changed path"
assert_contains '"hostVersion":"1.5.0"' "$TEST_LOG" "downstream invocation should receive an exact package version"
assert_contains "$relevant_head" "$TEST_LOG" "downstream changelog anchor should pin the upstream trigger head"
node --input-type=module - "$EVIDENCE_INDEX_PATH" "$relevant_head" <<'EOF'
import fs from 'node:fs';
const indexPath = process.argv[2];
const relevantHead = process.argv[3];
const data = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const match = data.entries.find((entry) => entry.upstream.afterHead === relevantHead);
if (!match) throw new Error(`missing evidence entry for ${relevantHead}`);
if (match.resolution.state !== 'safe') throw new Error(`expected safe state for ${relevantHead}`);
EOF

pushd "$PI_MONO_DIR" >/dev/null
mkdir -p packages/tui
printf 'retry\n' > packages/tui/README.md
commit_all "$PI_MONO_DIR" "retry-failure"
failed_head="$(git rev-parse HEAD)"
popd >/dev/null

set +e
PI_COMPAT_RELAY_TEST_LOG="$TEST_LOG" PI_COMPAT_RELAY_LOCAL_EXIT_CODE=1 run_relay "$CONTRIB_ROOT" "$PI_MONO_DIR" "$PI_EXTENSIONS_DIR" "$STATE_FILE" "$RECEIPTS_DIR"
relay_status=$?
set -e
assert_eq "1" "$relay_status" "local relay failure should propagate non-zero status"
assert_contains '"status": "local-failed"' "$(find "$RECEIPTS_DIR" -type f | sort | tail -1)" "failure receipt should be recorded"

PI_COMPAT_RELAY_TEST_LOG="$TEST_LOG" run_relay "$CONTRIB_ROOT" "$PI_MONO_DIR" "$PI_EXTENSIONS_DIR" "$STATE_FILE" "$RECEIPTS_DIR"
assert_eq "3" "$(wc -l < "$TEST_LOG" | tr -d ' ')" "failed relay should retry same upstream delta on the next successful run"
assert_contains "$failed_head" "$TEST_LOG" "retry invocation should include latest upstream head"

printf 'ok: pi-mono compatibility relay\n'
# The Node suite includes real npm configuration resolution, forced offline.
PATH="${PATH#"$FAKE_BIN:"}" node --test "$SCRIPT_DIR/pi-mono-compatibility-relay.test.mjs"
