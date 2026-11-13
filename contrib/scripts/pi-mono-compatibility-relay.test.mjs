import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const RELAY = fileURLToPath(new URL("./pi-mono-compatibility-relay.sh", import.meta.url));
const PACKAGE = "@earendil-works/pi-coding-agent";
const EXPLICIT_ANCHOR = "https://github.com/earendil-works/pi/compare/v1.5.0...v1.6.0";

function fixture(t) {
  const root = mkdtempSync(path.join(tmpdir(), "pi-relay-contract-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const upstream = path.join(root, "upstream");
  const downstream = path.join(root, "downstream");
  const bin = path.join(root, "bin");
  const state = path.join(root, "state");
  const receipts = path.join(root, "receipts");
  const logs = Object.fromEntries(["npm", "gh", "local", "lookups"].map((name) => [name, path.join(root, `${name}.jsonl`)]));
  const git = (repo, ...args) => execFileSync("git", ["-C", repo, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
  const put = (repo, name, content) => {
    const file = path.join(repo, name);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, content);
  };
  const commit = (repo) => { git(repo, "add", "-A"); git(repo, "commit", "-qm", "fixture"); return git(repo, "rev-parse", "HEAD"); };
  mkdirSync(bin);
  for (const repo of [upstream, downstream]) {
    mkdirSync(repo);
    git(repo, "init", "-q");
    git(repo, "config", "user.name", "Relay Test");
    git(repo, "config", "user.email", "relay-test@example.test");
  }
  git(upstream, "remote", "add", "origin", "https://github.com/earendil-works/pi.git");
  git(downstream, "remote", "add", "origin", "https://github.com/tryingET/pi-extensions.git");
  put(upstream, "packages/coding-agent/package.json", JSON.stringify({ name: PACKAGE, version: "1.5.0" }));
  put(upstream, "packages/coding-agent/CHANGELOG.md", "initial\n");
  const before = commit(upstream);
  writeFileSync(state, `head=${before}\nbranch=main\n`);
  put(upstream, "packages/coding-agent/CHANGELOG.md", "candidate\n");
  let head = commit(upstream);
  put(downstream, "scripts/pi-host-compatibility-canary.mjs", `
import { appendFileSync } from 'node:fs';
appendFileSync(process.env.RELAY_LOCAL_LOG, JSON.stringify({args:process.argv.slice(2),version:process.env.PI_HOST_COMPAT_HOST_VERSION ?? null,anchor:process.env.PI_HOST_COMPAT_CHANGELOG_REF ?? null,legacy:process.env.PI_HOST_VERSION ?? null})+'\\n');
process.exit(Number(process.env.RELAY_LOCAL_EXIT || 0));
`);
  commit(downstream);
  for (const [command, source] of Object.entries({
    npm: `
import { appendFileSync } from 'node:fs';
const args=process.argv.slice(2);
appendFileSync(process.env.RELAY_NPM_LOG,JSON.stringify(args)+'\\n');
if(process.env.RELAY_NPM_EXIT) process.exit(1);
if(process.env.RELAY_NPM_JSON) { console.log(process.env.RELAY_NPM_JSON); process.exit(0); }
console.log(JSON.stringify({name:${JSON.stringify(PACKAGE)},version:args[1].split('@').at(-1)}));
`,
    gh: `
import { appendFileSync } from 'node:fs';
const args=process.argv.slice(2);
if(args[0]==='run' && ['list', 'view'].includes(args[1])) {
  appendFileSync(process.env.RELAY_LOOKUP_LOG,JSON.stringify(args)+'\\n');
  const output = args[1]==='list' ? process.env.RELAY_RUN_LIST : process.env.RELAY_RUN_VIEW;
  if(output) console.log(output);
  process.exit(0);
}
appendFileSync(process.env.RELAY_GH_LOG,JSON.stringify(args)+'\\n');
if(process.env.RELAY_DISPATCH_OUTPUT) console.log(process.env.RELAY_DISPATCH_OUTPUT);
process.exit(Number(process.env.RELAY_GH_EXIT || 0));
`,
  })) writeFileSync(path.join(bin, command), `#!${process.execPath}\n${source}`, { mode: 0o755 });
  const baseEnv = { ...process.env };
  for (const key of ["PI_HOST_COMPAT_HOST_VERSION", "PI_HOST_COMPAT_CHANGELOG_REF", "PI_HOST_VERSION"]) delete baseEnv[key];
  const run = (env = {}, args = []) => spawnSync("bash", [RELAY, ...args], { encoding: "utf8", env: {
    ...baseEnv, PATH: `${bin}:${process.env.PATH}`, PI_COMPAT_RELAY_CONTRIB_ROOT: root,
    PI_COMPAT_RELAY_PI_MONO_DIR: upstream, PI_COMPAT_RELAY_PI_EXTENSIONS_DIR: downstream,
    PI_COMPAT_RELAY_STATE_FILE: state, PI_COMPAT_RELAY_RECEIPTS_DIR: receipts,
    PI_COMPAT_EVIDENCE_SCRIPT: path.join(root, "no-evidence-script"), PI_COMPAT_RELAY_MODE: "workflow",
    PI_COMPAT_PROFILE: "upgrade", RELAY_NPM_LOG: logs.npm, RELAY_GH_LOG: logs.gh, RELAY_LOCAL_LOG: logs.local, RELAY_LOOKUP_LOG: logs.lookups,
    ...env,
  } });
  return {
    root, upstream, bin, before, run, git, put,
    get head() { return head; },
    get anchor() { return `https://github.com/earendil-works/pi/blob/${head}/packages/coding-agent/CHANGELOG.md`; },
    commit() { head = commit(upstream); },
    state: () => readFileSync(state, "utf8"),
    receipts: () => readdirSync(receipts).map((file) => JSON.parse(readFileSync(path.join(receipts, file), "utf8"))),
    log: (name) => { try { return readFileSync(logs[name], "utf8").trim().split("\n").filter(Boolean).map(JSON.parse); } catch (error) { if (error.code === "ENOENT") return []; throw error; } },
  };
}

function passed(result) { assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`); }
function blocked(f, result, { registry = false, dispatched = false } = {}) {
  assert.notEqual(result.status, 0);
  assert.equal(f.log("gh").length, Number(dispatched));
  assert.equal(f.log("local").length, 0);
  assert.equal(f.log("npm").length, Number(registry));
  assert.match(f.state(), new RegExp(`head=${f.before}`));
}

test("workflow uses the committed package version and pinned changelog, even with a dirty working tree", (t) => {
  const f = fixture(t);
  f.put(f.upstream, "packages/coding-agent/package.json", JSON.stringify({ name: PACKAGE, version: "99.0.0" }));
  // Startup diagnostics must stay off the contract's machine-readable stdout.
  writeFileSync(path.join(f.bin, "node"), `#!/usr/bin/env bash\necho 'node startup warning' >&2\nexec '${process.execPath}' "$@"\n`, { mode: 0o755 });
  const result = f.run();
  passed(result);
  assert.match(result.stderr, /node startup warning/);
  assert.deepEqual(f.log("gh"), [["workflow", "run", "compatibility-canary.yml", "--repo", "tryingET/pi-extensions", "--ref", "main", "-f", "profile=upgrade", "-f", "host_version=1.5.0", "-f", `changelog_ref=${f.anchor}`]]);
  assert.deepEqual(f.log("npm"), [["view", `${PACKAGE}@1.5.0`, "name", "version", "--json", "--registry=https://registry.npmjs.org/", "--@earendil-works:registry=https://registry.npmjs.org/", "--fetch-retries=0", "--fetch-timeout=10000"]]);
  assert.deepEqual(f.receipts()[0].candidate_contract, { package: PACKAGE, version: "1.5.0", review_anchor: f.anchor, source: "upstream-manifest", target: "published-npm-package" });
  assert.equal(f.receipts()[0].upstream_repo.after_head, f.head);
  assert.match(f.state(), new RegExp(`head=${f.head}`));
  passed(f.run());
  assert.equal(f.log("gh").length, 1, "unchanged upstream head is not redispatched");
});

test("accepted dispatch without a returned run URL never borrows an older workflow run", (t) => {
  const f = fixture(t);
  passed(f.run({ RELAY_RUN_LIST: "101\thttps://github.com/tryingET/pi-extensions/actions/runs/101" }));
  assert.equal(f.log("lookups").length, 0);
  assert.equal(f.receipts()[0].downstream_repo.run_id, null);
  assert.match(f.state(), new RegExp(`head=${f.head}`), "accepted handoff still advances state");
});

test("only an unambiguous same-repository URL returned by dispatch binds the workflow", async (t) => {
  const url = "https://github.com/tryingET/pi-extensions/actions/runs/202";
  for (const [label, output, expectedId] of [
    ["returned URL", url, "202"],
    ["other repository", "https://github.com/other/repo/actions/runs/202", null],
    ["ambiguous URLs", `${url}\nhttps://github.com/tryingET/pi-extensions/actions/runs/203`, null],
    ["malformed ID", `${url}junk`, null],
    ["no identity", "dispatch accepted", null],
  ]) await t.test(label, (t) => {
    const f = fixture(t);
    passed(f.run({ RELAY_DISPATCH_OUTPUT: output, RELAY_RUN_LIST: "101\thttps://github.com/tryingET/pi-extensions/actions/runs/101" }));
    const downstream = f.receipts()[0].downstream_repo;
    assert.equal(downstream.run_id, expectedId);
    assert.equal(downstream.run_url, expectedId ? url : null);
    assert.equal(downstream.run_identity_source, expectedId ? "dispatch-output" : null);
    assert.equal(f.log("lookups").length, 0);
    assert.match(f.state(), new RegExp(`head=${f.head}`));
  });
});

test("integrated evidence uses only the returned dispatch identity for candidate safety", async (t) => {
  for (const correlated of [false, true]) await t.test(correlated ? "correlated success" : "uncorrelated handoff", (t) => {
    const f = fixture(t);
    const url = "https://github.com/tryingET/pi-extensions/actions/runs/202";
    const output = path.join(f.root, "index.json");
    passed(f.run({
      PI_COMPAT_EVIDENCE_SCRIPT: fileURLToPath(new URL("./pi-mono-compatibility-evidence-index.mjs", import.meta.url)),
      PI_COMPAT_EVIDENCE_OUTPUT_PATH: output, PI_COMPAT_EVIDENCE_OFFLINE: "0",
      RELAY_DISPATCH_OUTPUT: correlated ? url : "dispatch accepted",
      RELAY_RUN_LIST: "101\thttps://github.com/tryingET/pi-extensions/actions/runs/101",
      RELAY_RUN_VIEW: JSON.stringify({ databaseId: 202, status: "completed", conclusion: "success", url }),
    }));
    const index = JSON.parse(readFileSync(output, "utf8"));
    assert.equal(index.entries[0].resolution.state, correlated ? "safe" : "pending");
    assert.equal(index.summary.unresolvedCount, correlated ? 0 : 1);
    assert.deepEqual(f.log("lookups").map((args) => args.slice(0, 3)), correlated ? [["run", "view", "202"]] : []);
    assert.match(f.state(), new RegExp(`head=${f.head}`));
  });
});

test("local upgrades receive the same explicit host contract, never a Git SHA as the version", (t) => {
  const f = fixture(t);
  passed(f.run({ PI_COMPAT_RELAY_MODE: "local", PI_HOST_COMPAT_HOST_VERSION: "1.6.0", PI_HOST_COMPAT_CHANGELOG_REF: EXPLICIT_ANCHOR }));
  assert.deepEqual(f.log("local"), [{ args: ["run", "--profile", "upgrade"], version: "1.6.0", anchor: EXPLICIT_ANCHOR, legacy: null }]);
  assert.equal(f.log("gh").length, 0);
  assert.equal(f.receipts()[0].candidate_contract.source, "explicit");
});

test("workflow forwards paired overrides and accepts npm's singleton-array metadata", (t) => {
  const f = fixture(t);
  passed(f.run({ PI_HOST_COMPAT_HOST_VERSION: "1.6.0", PI_HOST_COMPAT_CHANGELOG_REF: EXPLICIT_ANCHOR, RELAY_NPM_JSON: JSON.stringify([{ name: PACKAGE, version: "1.6.0" }]) }));
  assert.deepEqual(f.log("gh")[0].slice(-6), ["-f", "profile=upgrade", "-f", "host_version=1.6.0", "-f", `changelog_ref=${EXPLICIT_ANCHOR}`]);
});

test("partial, blank, floating and malformed explicit contracts stop before metadata or dispatch", async (t) => {
  const valid = { PI_HOST_COMPAT_HOST_VERSION: "1.6.0", PI_HOST_COMPAT_CHANGELOG_REF: EXPLICIT_ANCHOR };
  for (const [label, env] of [
    ["version only", { PI_HOST_COMPAT_HOST_VERSION: "1.6.0" }],
    ["anchor only", { PI_HOST_COMPAT_CHANGELOG_REF: EXPLICIT_ANCHOR }],
    ["blank pair", { PI_HOST_COMPAT_HOST_VERSION: "", PI_HOST_COMPAT_CHANGELOG_REF: "" }],
    ...["latest", "^1.6.0", "01.6.0", "1.6.0-beta..1", "1.6.0\n", "a".repeat(40)].map((version) => [version, { ...valid, PI_HOST_COMPAT_HOST_VERSION: version }]),
    ["multiline anchor", { ...valid, PI_HOST_COMPAT_CHANGELOG_REF: `${EXPLICIT_ANCHOR}\ninjected` }],
    ["moving branch", { ...valid, PI_HOST_COMPAT_CHANGELOG_REF: "https://github.com/earendil-works/pi/blob/main/packages/coding-agent/CHANGELOG.md" }],
    ["DNS-absolute GitHub moving branch", { ...valid, PI_HOST_COMPAT_CHANGELOG_REF: "https://github.com./earendil-works/pi/blob/main/packages/coding-agent/CHANGELOG.md" }],
    ...[1, 8, 12, 27, 31, 127].map((code) => [`control ${code}`, { ...valid, PI_HOST_COMPAT_CHANGELOG_REF: `${EXPLICIT_ANCHOR}#note${String.fromCharCode(code)}` }]),
  ]) await t.test(label, (t) => {
    const f = fixture(t); blocked(f, f.run(env));
    assert.equal(f.receipts()[0].reason, "invalid-or-unavailable-host-contract");
  });
});

test("missing or malformed committed host metadata never becomes a dispatch", async (t) => {
  for (const [label, change] of [
    ["wrong package", (f) => f.put(f.upstream, "packages/coding-agent/package.json", JSON.stringify({ name: "wrong-package", version: "1.5.0" }))],
    ["floating version", (f) => f.put(f.upstream, "packages/coding-agent/package.json", JSON.stringify({ name: PACKAGE, version: "latest" }))],
    ["missing manifest", (f) => rmSync(path.join(f.upstream, "packages/coding-agent/package.json"))],
    ["invalid JSON", (f) => f.put(f.upstream, "packages/coding-agent/package.json", "{invalid}")],
    ["missing changelog", (f) => rmSync(path.join(f.upstream, "packages/coding-agent/CHANGELOG.md"))],
  ]) await t.test(label, (t) => { const f = fixture(t); change(f); f.commit(); blocked(f, f.run()); });
  await t.test("relative local origin is not invented as a GitHub URL", (t) => {
    const f = fixture(t); f.git(f.upstream, "remote", "set-url", "origin", "owner/repo"); blocked(f, f.run());
  });
});

test("unpublished, unavailable or mismatched registry replies preserve the delta for retry", async (t) => {
  for (const [label, env] of [
    ["unavailable or unpublished", { RELAY_NPM_EXIT: "1" }],
    ["malformed JSON", { RELAY_NPM_JSON: "invalid" }],
    ["empty metadata", { RELAY_NPM_JSON: "[]" }],
    ["multiple versions", { RELAY_NPM_JSON: JSON.stringify([{ name: PACKAGE, version: "1.5.0" }, { name: PACKAGE, version: "1.6.0" }]) }],
    ["wrong identity", { RELAY_NPM_JSON: JSON.stringify({ name: "wrong", version: "1.5.0" }) }],
    ["wrong version", { RELAY_NPM_JSON: JSON.stringify({ name: PACKAGE, version: "1.4.0" }) }],
  ]) await t.test(label, (t) => {
    const f = fixture(t); blocked(f, f.run(env), { registry: true });
    passed(f.run()); assert.equal(f.log("gh").length, 1); assert.match(f.state(), new RegExp(`head=${f.head}`));
  });
});

test("public npm registry overrides a conflicting scoped configuration (real npm, offline)", (t) => {
  const f = fixture(t);
  const npm = execFileSync("sh", ["-c", "command -v npm"], { encoding: "utf8" }).trim();
  const config = path.join(f.root, "npmrc");
  const stderr = path.join(f.root, "npm.stderr");
  writeFileSync(config, "@earendil-works:registry=https://registry.audit.invalid/\n");
  writeFileSync(path.join(f.root, "global-npmrc"), "");
  writeFileSync(path.join(f.root, "package.json"), JSON.stringify({ name: "offline-registry-test", version: "1.0.0" }));
  writeFileSync(path.join(f.bin, "npm"), `#!${process.execPath}
import { spawnSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const result = spawnSync(${JSON.stringify(npm)}, [...process.argv.slice(2), '--offline',
  ${JSON.stringify(`--cache=${path.join(f.root, "cache")}`)},
  ${JSON.stringify(`--userconfig=${config}`)},
  ${JSON.stringify(`--globalconfig=${path.join(f.root, "global-npmrc")}`)}],
  { cwd: ${JSON.stringify(f.root)}, env: process.env, encoding: 'utf8' });
writeFileSync(${JSON.stringify(stderr)}, result.stderr ?? '');
process.stdout.write(result.stdout ?? '');
process.exit(result.status ?? 1);
`, { mode: 0o755 });
  const result = f.run();
  blocked(f, result);
  assert.match(readFileSync(stderr, "utf8"), /request to https:\/\/registry\.npmjs\.org\//);
  assert.doesNotMatch(readFileSync(stderr, "utf8"), /registry\.audit\.invalid/);
  assert.equal(f.receipts()[0].reason, "invalid-or-unavailable-host-contract");
});

test("failed workflow dispatch is retried without losing the upstream delta", (t) => {
  const f = fixture(t); blocked(f, f.run({ RELAY_GH_EXIT: "1" }), { registry: true, dispatched: true });
  passed(f.run()); assert.equal(f.log("gh").length, 2); assert.match(f.state(), new RegExp(`head=${f.head}`));
});

test("current, off and dry-run retain their behavior without candidate registry effects", async (t) => {
  await t.test("current profile", (t) => {
    const f = fixture(t); passed(f.run({ PI_COMPAT_PROFILE: "current", PI_HOST_COMPAT_HOST_VERSION: "invalid-ignored-override" }));
    assert.deepEqual(f.log("gh")[0].slice(-2), ["-f", "profile=current"]);
    assert.equal(f.log("npm").length, 0); assert.equal(f.receipts()[0].candidate_contract, null);
  });
  await t.test("off", (t) => {
    const f = fixture(t); passed(f.run({ PI_COMPAT_RELAY_MODE: "off", PI_HOST_COMPAT_HOST_VERSION: "invalid-ignored-override" }));
    assert.equal(f.log("npm").length + f.log("gh").length, 0); assert.match(f.state(), new RegExp(`head=${f.before}`));
  });
  await t.test("dry-run", (t) => {
    const f = fixture(t); passed(f.run({}, ["--dry-run"]));
    assert.equal(f.log("npm").length + f.log("gh").length, 0); assert.match(f.state(), new RegExp(`head=${f.before}`));
    assert.equal(f.receipts()[0].candidate_contract.version, "1.5.0");
  });
  await t.test("unknown profile", (t) => { const f = fixture(t); blocked(f, f.run({ PI_COMPAT_PROFILE: "unknown" })); });
});
