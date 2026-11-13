#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INDEX_SCRIPT="$REPO_ROOT/scripts/pi-mono-compatibility-evidence-index.mjs"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

require_cmd node

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CONTRIB_ROOT="$TMP_DIR/contrib"
RECEIPTS_DIR="$CONTRIB_ROOT/.logs/pi-mono-compatibility-relay"
OUTPUT_PATH="$CONTRIB_ROOT/.state/pi-mono-compatibility-relay/evidence-index.json"
FAKE_BIN="$TMP_DIR/bin"
mkdir -p "$RECEIPTS_DIR" "$FAKE_BIN"

cat > "$FAKE_BIN/gh" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
run_id="${3:-}"
case "$run_id" in
  101)
    printf '%s\n' '{"databaseId":101,"status":"completed","conclusion":"success","url":"https://example.test/runs/101","workflowName":"compatibility-canary","headSha":"upstream-a","createdAt":"2026-03-14T08:00:00Z","updatedAt":"2026-03-14T08:01:00Z"}'
    ;;
  102)
    printf '%s\n' '{"databaseId":102,"status":"in_progress","conclusion":null,"url":"https://example.test/runs/102","workflowName":"compatibility-canary","headSha":"upstream-b","createdAt":"2026-03-14T08:02:00Z","updatedAt":"2026-03-14T08:03:00Z"}'
    ;;
  *)
    echo "unknown run id: $run_id" >&2
    exit 1
    ;;
esac
EOF
chmod +x "$FAKE_BIN/gh"

cat > "$RECEIPTS_DIR/receipt-20260314T080000Z-1.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:00:00Z",
  "status": "local-passed",
  "reason": "head-changed",
  "mode": "local",
  "profile": "upgrade",
  "candidate_contract": {
    "package": "@earendil-works/pi-coding-agent",
    "version": "1.5.0",
    "review_anchor": "https://github.com/earendil-works/pi/releases/tag/v1.5.0",
    "source": "explicit",
    "target": "published-npm-package"
  },
  "dry_run": false,
  "sync_status": "OK",
  "contrib_root": "/tmp/contrib",
  "upstream_repo": {
    "path": "/tmp/contrib/pi-mono",
    "branch": "main",
    "before_head": "aaa",
    "after_head": "bbb",
    "changed_paths": ["packages/coding-agent/CHANGELOG.md"]
  },
  "downstream_repo": {
    "path": "/tmp/owned/pi-extensions",
    "repo_slug": null,
    "workflow_file": null,
    "workflow_ref": null,
    "dispatch_output": "local pass",
    "run_url": null,
    "run_id": null
  }
}
EOF

cat > "$RECEIPTS_DIR/receipt-20260314T080100Z-2.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:01:00Z",
  "status": "dispatch-failed",
  "reason": "head-changed",
  "mode": "workflow",
  "profile": "upgrade",
  "dry_run": false,
  "sync_status": "OK",
  "contrib_root": "/tmp/contrib",
  "upstream_repo": {
    "path": "/tmp/contrib/pi-mono",
    "branch": "main",
    "before_head": "bbb",
    "after_head": "ccc",
    "changed_paths": ["packages/coding-agent/src/index.ts"]
  },
  "downstream_repo": {
    "path": "/tmp/owned/pi-extensions",
    "repo_slug": "tryingET/pi-extensions",
    "workflow_file": "compatibility-canary.yml",
    "workflow_ref": "main",
    "dispatch_output": "HTTP 500 dispatch failure",
    "run_url": null,
    "run_id": null
  }
}
EOF

cat > "$RECEIPTS_DIR/receipt-20260314T080200Z-3.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:02:00Z",
  "status": "workflow-dispatched",
  "reason": "head-changed",
  "mode": "workflow",
  "profile": "upgrade",
  "candidate_contract": {
    "package": "@earendil-works/pi-coding-agent",
    "version": "1.5.0",
    "review_anchor": "https://github.com/earendil-works/pi/blob/1111111111111111111111111111111111111111/packages/coding-agent/CHANGELOG.md",
    "source": "upstream-manifest",
    "target": "published-npm-package"
  },
  "dry_run": false,
  "sync_status": "OK",
  "contrib_root": "/tmp/contrib",
  "upstream_repo": {
    "path": "/tmp/contrib/pi-mono",
    "branch": "main",
    "before_head": "ccc",
    "after_head": "ddd",
    "changed_paths": ["packages/tui/src/app.ts"]
  },
  "downstream_repo": {
    "path": "/tmp/owned/pi-extensions",
    "repo_slug": "tryingET/pi-extensions",
    "workflow_file": "compatibility-canary.yml",
    "workflow_ref": "main",
    "dispatch_output": "dispatched",
    "run_url": "https://github.com/tryingET/pi-extensions/actions/runs/101",
    "run_id": "101",
    "run_identity_source": "dispatch-output"
  }
}
EOF

cat > "$RECEIPTS_DIR/receipt-20260314T080300Z-4.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:03:00Z",
  "status": "workflow-dispatched",
  "reason": "head-changed",
  "mode": "workflow",
  "profile": "upgrade",
  "candidate_contract": {
    "package": "@earendil-works/pi-coding-agent",
    "version": "1.5.0",
    "review_anchor": "https://github.com/earendil-works/pi/releases/tag/v1.5.0",
    "source": "explicit",
    "target": "published-npm-package"
  },
  "dry_run": false,
  "sync_status": "WARN",
  "contrib_root": "/tmp/contrib",
  "upstream_repo": {
    "path": "/tmp/contrib/pi-mono",
    "branch": "main",
    "before_head": "ddd",
    "after_head": "eee",
    "changed_paths": ["packages/coding-agent/docs/extensions.md"]
  },
  "downstream_repo": {
    "path": "/tmp/owned/pi-extensions",
    "repo_slug": "tryingET/pi-extensions",
    "workflow_file": "compatibility-canary.yml",
    "workflow_ref": "main",
    "dispatch_output": "dispatched",
    "run_url": "https://github.com/tryingET/pi-extensions/actions/runs/102",
    "run_id": "102",
    "run_identity_source": "dispatch-output"
  }
}
EOF

cat > "$RECEIPTS_DIR/receipt-20260314T080400Z-5.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:04:00Z",
  "status": "local-passed",
  "upstream_repo": {"after_head": "legacy-local"}
}
EOF

cat > "$RECEIPTS_DIR/receipt-20260314T080500Z-6.json" <<'EOF'
{
  "timestamp": "2026-03-14T08:05:00Z",
  "status": "workflow-dispatched",
  "upstream_repo": {"after_head": "legacy-workflow"},
  "downstream_repo": {"repo_slug": "tryingET/pi-extensions", "run_id": "101"}
}
EOF

# A historical contract receipt may carry a run guessed from the latest-run list.
# Its successful lookup must not certify this candidate without correlation.
node --input-type=module - "$RECEIPTS_DIR" <<'EOF'
import fs from 'node:fs';
const dir = process.argv[2];
const old = JSON.parse(fs.readFileSync(`${dir}/receipt-20260314T080200Z-3.json`, 'utf8'));
old.timestamp = '2026-03-14T08:06:00Z';
old.upstream_repo.after_head = 'uncorrelated';
old.candidate_contract.version = '1.6.0';
delete old.downstream_repo.run_identity_source;
fs.writeFileSync(`${dir}/receipt-20260314T080600Z-7.json`, JSON.stringify(old));
EOF

PATH="$FAKE_BIN:$PATH" node "$INDEX_SCRIPT" rebuild \
  --contrib-root "$CONTRIB_ROOT" \
  --receipts-dir "$RECEIPTS_DIR" \
  --output "$OUTPUT_PATH" \
  --max-online-lookups 5 \
  >/dev/null

[[ -f "$OUTPUT_PATH" ]] || fail "evidence index output was not written"

node --input-type=module - "$OUTPUT_PATH" <<'EOF'
import assert from 'node:assert/strict';
import fs from 'node:fs';
const indexPath = process.argv[2];
const data = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
if (data.summary.totalEntries !== 7) throw new Error(`expected 7 entries, got ${data.summary.totalEntries}`);
if (data.summary.unresolvedCount !== 3) throw new Error(`expected 3 unresolved entries, got ${data.summary.unresolvedCount}`);
const byHead = new Map(data.entries.map((entry) => [entry.upstream.afterHead, entry]));
if (byHead.get('bbb').resolution.state !== 'safe') throw new Error('local-passed should classify as safe');
if (byHead.get('ccc').resolution.followUp !== 'retry_dispatch') throw new Error('dispatch-failed should require retry_dispatch');
if (byHead.get('ddd').resolution.state !== 'safe') throw new Error('completed success workflow should classify as safe');
if (byHead.get('eee').resolution.state !== 'pending') throw new Error('in-progress workflow should classify as pending');
const explicitContract = {
  packageName: '@earendil-works/pi-coding-agent',
  version: '1.5.0',
  reviewAnchor: 'https://github.com/earendil-works/pi/releases/tag/v1.5.0',
  source: 'explicit',
  target: 'published-npm-package',
};
assert.deepEqual(byHead.get('bbb').candidateContract, explicitContract);
assert.deepEqual(byHead.get('ddd').candidateContract, {
  ...explicitContract,
  reviewAnchor: 'https://github.com/earendil-works/pi/blob/1111111111111111111111111111111111111111/packages/coding-agent/CHANGELOG.md',
  source: 'upstream-manifest',
});
for (const head of ['bbb', 'ddd']) {
  assert.match(byHead.get(head).resolution.rationale, /published npm package @earendil-works\/pi-coding-agent@1\.5\.0/);
  assert.match(byHead.get(head).resolution.rationale, /trigger context, not a tested checkout/);
}
for (const head of ['legacy-local', 'legacy-workflow']) {
  assert.equal(byHead.get(head).resolution.state, 'safe');
  assert.equal(byHead.get(head).candidateContract, null);
  assert.match(byHead.get(head).resolution.rationale, /does not record an exact package contract/);
}
assert.deepEqual(data.summary.unresolvedEntries.find((entry) => entry.afterHead === 'eee').candidateContract, explicitContract);
assert.equal(byHead.get('uncorrelated').resolution.state, 'pending');
assert.match(byHead.get('uncorrelated').resolution.rationale, /correlat/);
EOF

UNRESOLVED_JSON="$TMP_DIR/unresolved.json"
PATH="$FAKE_BIN:$PATH" node "$INDEX_SCRIPT" unresolved \
  --contrib-root "$CONTRIB_ROOT" \
  --receipts-dir "$RECEIPTS_DIR" \
  --output "$OUTPUT_PATH" \
  --max-online-lookups 5 \
  --json > "$UNRESOLVED_JSON"

node --input-type=module - "$UNRESOLVED_JSON" <<'EOF'
import assert from 'node:assert/strict';
import fs from 'node:fs';
const unresolvedPath = process.argv[2];
const unresolved = JSON.parse(fs.readFileSync(unresolvedPath, 'utf8'));
if (unresolved.length !== 3) throw new Error(`expected 3 unresolved entries, got ${unresolved.length}`);
const states = unresolved.map((entry) => entry.resolution.state).sort();
if (states.join(',') !== 'needs_attention,pending,pending') {
  throw new Error(`unexpected unresolved states: ${states.join(',')}`);
}
assert.equal(unresolved.find((entry) => entry.upstream.afterHead === 'eee').candidateContract.version, '1.5.0');
EOF

printf 'ok: pi-mono compatibility evidence index\n'
