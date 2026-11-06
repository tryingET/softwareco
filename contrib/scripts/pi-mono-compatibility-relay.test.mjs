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
  const logs = Object.fromEntries(["npm", "gh", "local"].map((name) => [name, path.join(root, `${name}.jsonl`)]));
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
if(args[0]==='run' && args[1]==='list') process.exit(0);
appendFileSync(process.env.RELAY_GH_LOG,JSON.stringify(args)+'\\n');
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
    PI_COMPAT_PROFILE: "upgrade", RELAY_NPM_LOG: logs.npm, RELAY_GH_LOG: logs.gh, RELAY_LOCAL_LOG: logs.local,
    ...env,
  } });
  return {
    upstream, bin, before, run, git, put,
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
  assert.deepEqual(f.log("npm"), [["view", `${PACKAGE}@1.5.0`, "name", "version", "--json", "--registry=https://registry.npmjs.org/", "--fetch-retries=0", "--fetch-timeout=10000"]]);
  assert.deepEqual(f.receipts()[0].candidate_contract, { package: PACKAGE, version: "1.5.0", review_anchor: f.anchor, source: "upstream-manifest", target: "published-npm-package" });
  assert.equal(f.receipts()[0].upstream_repo.after_head, f.head);
  assert.match(f.state(), new RegExp(`head=${f.head}`));
  passed(f.run());
  assert.equal(f.log("gh").length, 1, "unchanged upstream head is not redispatched");
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
  ]) await t.test(label, (t) => { const f = fixture(t); blocked(f, f.run(env)); });
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
