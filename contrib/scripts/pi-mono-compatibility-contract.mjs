#!/usr/bin/env node
import { execFileSync } from "node:child_process";

const HOST_PACKAGE = "@earendil-works/pi-coding-agent";
const SEMVER_NUMBER = "(?:0|[1-9]\\d*)";
const SEMVER_PRERELEASE = "(?:0|[1-9]\\d*|\\d*[A-Za-z-][0-9A-Za-z-]*)";
const EXACT_VERSION = new RegExp(`^${SEMVER_NUMBER}\\.${SEMVER_NUMBER}\\.${SEMVER_NUMBER}(?:-${SEMVER_PRERELEASE}(?:\\.${SEMVER_PRERELEASE})*)?(?:\\+[0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*)?$`);
const VERSION_ENV = "PI_HOST_COMPAT_HOST_VERSION";
const ANCHOR_ENV = "PI_HOST_COMPAT_CHANGELOG_REF";

function exactVersion(value) {
  if (typeof value !== "string" || /\s/u.test(value) || !EXACT_VERSION.test(value)) {
    throw new Error(`${VERSION_ENV} must be an exact npm semantic version`);
  }
  return value;
}

function reviewAnchor(value) {
  if (typeof value !== "string" || !value || /\s/u.test(value)) {
    throw new Error(`${ANCHOR_ENV} must be a non-empty, single-line HTTPS changelog URL`);
  }
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password) {
    throw new Error(`${ANCHOR_ENV} must be an HTTPS changelog URL without credentials`);
  }
  if (url.hostname === "github.com") {
    const parts = url.pathname.split("/").filter(Boolean);
    const pinnedRef = (ref) => /^[a-f0-9]{40}$/i.test(ref) || EXACT_VERSION.test(ref.replace(/^v/, ""));
    const [owner, repo, kind, ref, tag] = parts;
    const pinned = owner && repo && (
      (["blob", "tree", "commit"].includes(kind) && ref && pinnedRef(ref)) ||
      (kind === "releases" && ref === "tag" && tag && pinnedRef(tag)) ||
      (kind === "compare" && ref && ref.split("...").length === 2 && ref.split("...").every(pinnedRef))
    );
    if (!pinned) throw new Error(`${ANCHOR_ENV} must pin a tag, commit, or comparison, not a moving branch`);
  }
  return value;
}

function git(repo, ...args) {
  return execFileSync("git", ["-C", repo, ...args], { encoding: "utf8", maxBuffer: 1024 * 1024 }).trim();
}

function upstreamContract(repo, head) {
  const manifest = JSON.parse(git(repo, "show", `${head}:packages/coding-agent/package.json`));
  if (manifest.name !== HOST_PACKAGE) {
    throw new Error(`upstream packages/coding-agent/package.json must name ${HOST_PACKAGE}`);
  }
  const version = exactVersion(manifest.version);
  git(repo, "cat-file", "-e", `${head}:packages/coding-agent/CHANGELOG.md`);
  const remote = git(repo, "remote", "get-url", "origin");
  const match = remote.match(/^(?:https?:\/\/github\.com\/|ssh:\/\/git@github\.com\/|git@github\.com:)([A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+?)(?:\.git)?$/);
  if (!match) {
    throw new Error("upstream origin must be a GitHub repository, or supply both explicit host contract overrides");
  }
  const slug = match[1];
  return {
    version,
    reviewAnchor: reviewAnchor(`https://github.com/${slug}/blob/${head}/packages/coding-agent/CHANGELOG.md`),
    source: "upstream-manifest",
  };
}

function checkPublished(version) {
  let metadata;
  try {
    const output = execFileSync("npm", [
      "view", `${HOST_PACKAGE}@${version}`, "name", "version", "--json",
      "--registry=https://registry.npmjs.org/", "--fetch-retries=0", "--fetch-timeout=10000",
    ], { encoding: "utf8", timeout: 20000, maxBuffer: 1024 * 1024, stdio: ["ignore", "pipe", "pipe"] });
    metadata = JSON.parse(output);
  } catch {
    throw new Error(`cannot confirm published ${HOST_PACKAGE}@${version}; no canary was dispatched; retry when the exact release is available`);
  }
  if (Array.isArray(metadata) && metadata.length === 1) metadata = metadata[0];
  if (!metadata || metadata.name !== HOST_PACKAGE || metadata.version !== version) {
    throw new Error(`registry metadata did not identify exactly ${HOST_PACKAGE}@${version}; no canary was dispatched`);
  }
}

try {
  const [repo, head, availability, ...extra] = process.argv.slice(2);
  if (!repo || !/^[a-f0-9]{40}$/i.test(head || "") || !["--check-published", "--preview"].includes(availability) || extra.length) {
    throw new Error("usage: pi-mono-compatibility-contract.mjs <upstream-repo> <commit-sha> <--check-published|--preview>");
  }
  const hasVersion = Object.hasOwn(process.env, VERSION_ENV);
  const hasAnchor = Object.hasOwn(process.env, ANCHOR_ENV);
  if (hasVersion !== hasAnchor) {
    throw new Error(`provide both ${VERSION_ENV} and ${ANCHOR_ENV}, or neither; partial overrides are not combined with upstream metadata`);
  }
  const contract = hasVersion ? {
    version: exactVersion(process.env[VERSION_ENV]),
    reviewAnchor: reviewAnchor(process.env[ANCHOR_ENV]),
    source: "explicit",
  } : upstreamContract(repo, head);
  if (availability === "--check-published") checkPublished(contract.version);
  // Validated fields cannot contain tabs or newlines; the shell reads one record.
  process.stdout.write(`${contract.version}\t${contract.reviewAnchor}\t${contract.source}\n`);
} catch (error) {
  console.error(`pi-compat-relay: ${error.message}`);
  process.exitCode = 1;
}
