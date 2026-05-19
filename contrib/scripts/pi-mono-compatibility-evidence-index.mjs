#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const CONTRIB_ROOT_DEFAULT = path.resolve(SCRIPT_DIR, "..");
const DEFAULT_RECEIPTS_DIR = path.join(
  CONTRIB_ROOT_DEFAULT,
  ".logs",
  "pi-mono-compatibility-relay",
);
const DEFAULT_OUTPUT_PATH = path.join(
  CONTRIB_ROOT_DEFAULT,
  ".state",
  "pi-mono-compatibility-relay",
  "evidence-index.json",
);
const DEFAULT_MAX_ONLINE_LOOKUPS = 10;

function usage() {
  console.error(`Usage:
  node ./scripts/pi-mono-compatibility-evidence-index.mjs rebuild [--contrib-root <path>] [--receipts-dir <path>] [--output <path>] [--offline] [--max-online-lookups <n>] [--json]
  node ./scripts/pi-mono-compatibility-evidence-index.mjs summary [--contrib-root <path>] [--receipts-dir <path>] [--output <path>] [--offline] [--max-online-lookups <n>] [--json]
  node ./scripts/pi-mono-compatibility-evidence-index.mjs unresolved [--contrib-root <path>] [--receipts-dir <path>] [--output <path>] [--offline] [--max-online-lookups <n>] [--limit <n>] [--json]`);
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const options = {
    command,
    contribRoot: CONTRIB_ROOT_DEFAULT,
    receiptsDir: DEFAULT_RECEIPTS_DIR,
    outputPath: DEFAULT_OUTPUT_PATH,
    offline: false,
    json: false,
    limit: 20,
    maxOnlineLookups: DEFAULT_MAX_ONLINE_LOOKUPS,
  };

  for (let index = 0; index < rest.length; index += 1) {
    const arg = rest[index];
    switch (arg) {
      case "--contrib-root": {
        const value = rest[index + 1];
        if (!value) throw new Error("--contrib-root requires a value");
        options.contribRoot = path.resolve(value);
        index += 1;
        break;
      }
      case "--receipts-dir": {
        const value = rest[index + 1];
        if (!value) throw new Error("--receipts-dir requires a value");
        options.receiptsDir = path.resolve(value);
        index += 1;
        break;
      }
      case "--output": {
        const value = rest[index + 1];
        if (!value) throw new Error("--output requires a value");
        options.outputPath = path.resolve(value);
        index += 1;
        break;
      }
      case "--offline":
        options.offline = true;
        break;
      case "--json":
        options.json = true;
        break;
      case "--limit": {
        const value = Number(rest[index + 1]);
        if (!Number.isFinite(value) || value < 1) throw new Error("--limit must be >= 1");
        options.limit = Math.floor(value);
        index += 1;
        break;
      }
      case "--max-online-lookups": {
        const value = Number(rest[index + 1]);
        if (!Number.isFinite(value) || value < 0) {
          throw new Error("--max-online-lookups must be >= 0");
        }
        options.maxOnlineLookups = Math.floor(value);
        index += 1;
        break;
      }
      case "-h":
      case "--help":
        options.help = true;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (options.command && !["rebuild", "summary", "unresolved"].includes(options.command)) {
    throw new Error(`Unknown command: ${options.command}`);
  }

  return options;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function listReceiptPaths(receiptsDir) {
  if (!fs.existsSync(receiptsDir)) return [];
  return fs
    .readdirSync(receiptsDir)
    .filter((entry) => entry.endsWith(".json"))
    .map((entry) => path.join(receiptsDir, entry))
    .sort();
}

function safeReadJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    return {
      __invalid: true,
      filePath,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

function nonEmpty(value) {
  return typeof value === "string" && value.trim().length > 0 ? value.trim() : undefined;
}

function asArray(value) {
  return Array.isArray(value) ? value.map((entry) => String(entry)) : [];
}

function excerpt(value, max = 240) {
  if (typeof value !== "string") return undefined;
  return value.length <= max ? value : `${value.slice(0, max)}…`;
}

function buildWorkflowLookupPlan(entries, maxOnlineLookups) {
  return entries
    .filter((entry) => entry.status === "workflow-dispatched")
    .filter((entry) => nonEmpty(entry?.downstream?.runId) && nonEmpty(entry?.downstream?.repoSlug))
    .sort((left, right) => String(right.timestamp).localeCompare(String(left.timestamp)))
    .slice(0, maxOnlineLookups);
}

function fetchWorkflowRuns(entries, options) {
  if (options.offline || entries.length === 0) return new Map();

  const cache = new Map();
  for (const entry of entries) {
    const runId = nonEmpty(entry?.downstream?.runId);
    const repoSlug = nonEmpty(entry?.downstream?.repoSlug);
    if (!runId || !repoSlug) continue;

    const cacheKey = `${repoSlug}#${runId}`;
    if (cache.has(cacheKey)) continue;

    try {
      const output = execFileSync(
        "gh",
        [
          "run",
          "view",
          runId,
          "--repo",
          repoSlug,
          "--json",
          "databaseId,status,conclusion,url,workflowName,headSha,createdAt,updatedAt",
        ],
        { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] },
      );
      const parsed = JSON.parse(output);
      cache.set(cacheKey, {
        databaseId: parsed.databaseId == null ? null : String(parsed.databaseId),
        status: parsed.status == null ? null : String(parsed.status),
        conclusion: parsed.conclusion == null ? null : String(parsed.conclusion),
        url: parsed.url == null ? null : String(parsed.url),
        workflowName: parsed.workflowName == null ? null : String(parsed.workflowName),
        headSha: parsed.headSha == null ? null : String(parsed.headSha),
        createdAt: parsed.createdAt == null ? null : String(parsed.createdAt),
        updatedAt: parsed.updatedAt == null ? null : String(parsed.updatedAt),
      });
    } catch (error) {
      cache.set(cacheKey, {
        status: null,
        conclusion: null,
        url: nonEmpty(entry?.downstream?.runUrl) ?? null,
        lookupError: error instanceof Error ? error.message : String(error),
      });
    }
  }

  return cache;
}

function classifyResolution(entry, workflowRun) {
  switch (entry.status) {
    case "initialized":
      return {
        state: "not_applicable",
        followUp: "none",
        rationale: "Baseline receipt recorded before any actionable upstream delta was evaluated.",
      };
    case "skipped":
      if (entry.reason === "no-relevant-path-change") {
        return {
          state: "not_applicable",
          followUp: "none",
          rationale: "Upstream pi-mono moved, but none of the watched host surfaces changed.",
        };
      }
      if (entry.reason === "relay-disabled") {
        return {
          state: "needs_attention",
          followUp: "manual_review",
          rationale: "Relevant upstream surfaces changed while the compatibility relay was disabled.",
        };
      }
      return {
        state: "pending",
        followUp: "manual_review",
        rationale: `Skip receipt requires review (${entry.reason || "unspecified reason"}).`,
      };
    case "dry-run":
      return {
        state: "pending",
        followUp: "manual_review",
        rationale: "Dry-run receipt captured a relevant upstream delta without executing downstream validation.",
      };
    case "local-passed":
      return {
        state: "safe",
        followUp: "none",
        rationale: "Local downstream canary passed for the recorded upstream delta.",
      };
    case "local-failed":
      return {
        state: "needs_attention",
        followUp: "investigate_failure",
        rationale: "Local downstream canary failed for the recorded upstream delta.",
      };
    case "dispatch-failed":
      return {
        state: "needs_attention",
        followUp: "retry_dispatch",
        rationale: "Downstream compatibility workflow dispatch failed and should be retried or repaired.",
      };
    case "failed":
      return {
        state: "needs_attention",
        followUp: "investigate_failure",
        rationale: `Relay failed before downstream validation completed (${entry.reason || "unspecified reason"}).`,
      };
    case "workflow-dispatched": {
      const status = nonEmpty(workflowRun?.status);
      const conclusion = nonEmpty(workflowRun?.conclusion);
      if (status === "completed" && conclusion === "success") {
        return {
          state: "safe",
          followUp: "none",
          rationale: "Downstream compatibility workflow completed successfully.",
        };
      }
      if (status === "completed") {
        return {
          state: "needs_attention",
          followUp: "investigate_failure",
          rationale: `Downstream compatibility workflow completed with conclusion=${conclusion || "unknown"}.`,
        };
      }
      if (status === "queued" || status === "in_progress" || status === "requested" || status === "waiting") {
        return {
          state: "pending",
          followUp: "wait_for_downstream",
          rationale: `Downstream compatibility workflow is still ${status}.`,
        };
      }
      return {
        state: "pending",
        followUp: "wait_for_downstream",
        rationale: workflowRun?.lookupError
          ? `Downstream workflow was dispatched, but current run status could not be refreshed (${workflowRun.lookupError}).`
          : "Downstream compatibility workflow was dispatched and is awaiting a known conclusion.",
      };
    }
    default:
      return {
        state: "pending",
        followUp: "manual_review",
        rationale: `Unknown receipt status '${entry.status}'.`,
      };
  }
}

function normalizeEntry(receiptPath, rawReceipt, workflowRuns) {
  if (rawReceipt.__invalid) {
    return {
      timestamp: null,
      receiptPath,
      invalid: true,
      parseError: rawReceipt.error,
    };
  }

  const downstream = rawReceipt.downstream_repo && typeof rawReceipt.downstream_repo === "object"
    ? rawReceipt.downstream_repo
    : {};
  const upstream = rawReceipt.upstream_repo && typeof rawReceipt.upstream_repo === "object"
    ? rawReceipt.upstream_repo
    : {};

  const repoSlug = nonEmpty(downstream.repo_slug);
  const runId = nonEmpty(downstream.run_id);
  const workflowRun = repoSlug && runId ? workflowRuns.get(`${repoSlug}#${runId}`) ?? null : null;
  const normalized = {
    timestamp: nonEmpty(rawReceipt.timestamp) ?? path.basename(receiptPath),
    receiptPath,
    status: nonEmpty(rawReceipt.status) ?? "unknown",
    reason: nonEmpty(rawReceipt.reason) ?? "unknown",
    mode: nonEmpty(rawReceipt.mode) ?? "unknown",
    profile: nonEmpty(rawReceipt.profile) ?? "unknown",
    syncStatus: nonEmpty(rawReceipt.sync_status) ?? "unknown",
    dryRun: Boolean(rawReceipt.dry_run),
    upstream: {
      path: nonEmpty(upstream.path) ?? null,
      branch: nonEmpty(upstream.branch) ?? null,
      beforeHead: nonEmpty(upstream.before_head) ?? null,
      afterHead: nonEmpty(upstream.after_head) ?? null,
      changedPaths: asArray(upstream.changed_paths),
    },
    downstream: {
      path: nonEmpty(downstream.path) ?? null,
      repoSlug,
      workflowFile: nonEmpty(downstream.workflow_file) ?? null,
      workflowRef: nonEmpty(downstream.workflow_ref) ?? null,
      runId,
      runUrl: nonEmpty(downstream.run_url) ?? null,
      dispatchOutputSnippet: excerpt(downstream.dispatch_output),
      workflowRun,
    },
  };

  normalized.upstream.changedPathCount = normalized.upstream.changedPaths.length;
  normalized.resolution = classifyResolution(normalized, workflowRun);
  normalized.followUpRequired = ![
    "safe",
    "not_applicable",
  ].includes(normalized.resolution.state);

  return normalized;
}

function buildSummary(entries, invalidReceipts, options) {
  const resolutionCounts = {};
  const statusCounts = {};
  for (const entry of entries) {
    resolutionCounts[entry.resolution.state] = (resolutionCounts[entry.resolution.state] ?? 0) + 1;
    statusCounts[entry.status] = (statusCounts[entry.status] ?? 0) + 1;
  }

  const unresolved = entries.filter((entry) => entry.followUpRequired);
  const latest = entries.at(-1) ?? null;

  return {
    generatedAt: new Date().toISOString(),
    receiptsDir: options.receiptsDir,
    outputPath: options.outputPath,
    offline: options.offline,
    totalEntries: entries.length,
    invalidReceipts: invalidReceipts.length,
    resolutionCounts,
    statusCounts,
    unresolvedCount: unresolved.length,
    latestTimestamp: latest?.timestamp ?? null,
    latestUpstreamHead: latest?.upstream?.afterHead ?? null,
    unresolvedEntries: unresolved.slice(-10).reverse().map((entry) => ({
      timestamp: entry.timestamp,
      status: entry.status,
      reason: entry.reason,
      state: entry.resolution.state,
      followUp: entry.resolution.followUp,
      afterHead: entry.upstream.afterHead,
      changedPaths: entry.upstream.changedPaths,
      repoSlug: entry.downstream.repoSlug,
      runUrl: entry.downstream.runUrl ?? entry.downstream.workflowRun?.url ?? null,
    })),
  };
}

function buildIndex(options) {
  const receiptPaths = listReceiptPaths(options.receiptsDir);
  const rawReceipts = receiptPaths.map((receiptPath) => ({
    receiptPath,
    receipt: safeReadJson(receiptPath),
  }));

  const invalidReceipts = rawReceipts.filter((entry) => entry.receipt.__invalid).map((entry) => ({
    receiptPath: entry.receiptPath,
    error: entry.receipt.error,
  }));

  const provisionalEntries = rawReceipts
    .filter((entry) => !entry.receipt.__invalid)
    .map((entry) => normalizeEntry(entry.receiptPath, entry.receipt, new Map()));

  const workflowLookupPlan = buildWorkflowLookupPlan(provisionalEntries, options.maxOnlineLookups);
  const workflowRuns = fetchWorkflowRuns(workflowLookupPlan, options);

  const entries = rawReceipts
    .filter((entry) => !entry.receipt.__invalid)
    .map((entry) => normalizeEntry(entry.receiptPath, entry.receipt, workflowRuns))
    .sort((left, right) => {
      if (left.timestamp === right.timestamp) return left.receiptPath.localeCompare(right.receiptPath);
      return String(left.timestamp).localeCompare(String(right.timestamp));
    });

  const summary = buildSummary(entries, invalidReceipts, options);
  return {
    schemaVersion: 1,
    generatedAt: summary.generatedAt,
    receiptsDir: options.receiptsDir,
    outputPath: options.outputPath,
    offline: options.offline,
    entries,
    invalidReceipts,
    summary,
  };
}

function writeIndex(index, outputPath) {
  ensureDir(path.dirname(outputPath));
  fs.writeFileSync(outputPath, `${JSON.stringify(index, null, 2)}\n`, "utf8");
}

function printHumanSummary(index) {
  console.log(`# pi-mono compatibility evidence index`);
  console.log("");
  console.log(`- entries: ${index.summary.totalEntries}`);
  console.log(`- invalid_receipts: ${index.summary.invalidReceipts}`);
  console.log(`- unresolved: ${index.summary.unresolvedCount}`);
  console.log(`- latest_timestamp: ${index.summary.latestTimestamp ?? "none"}`);
  console.log(`- latest_upstream_head: ${index.summary.latestUpstreamHead ?? "none"}`);
  console.log(`- output: ${index.outputPath}`);
  console.log("");
  console.log(`## resolution counts`);
  for (const [state, count] of Object.entries(index.summary.resolutionCounts)) {
    console.log(`- ${state}: ${count}`);
  }
  if (index.summary.unresolvedEntries.length > 0) {
    console.log("");
    console.log(`## latest unresolved`);
    for (const entry of index.summary.unresolvedEntries) {
      console.log(
        `- ${entry.timestamp} | ${entry.state} | ${entry.followUp} | ${entry.afterHead ?? "no-head"}`,
      );
    }
  }
}

function printHumanUnresolved(entries) {
  if (entries.length === 0) {
    console.log("No unresolved compatibility entries.");
    return;
  }
  console.log(`# unresolved pi-mono compatibility entries`);
  console.log("");
  for (const entry of entries) {
    console.log(`- ${entry.timestamp} | ${entry.resolution.state} | ${entry.resolution.followUp}`);
    console.log(`  status=${entry.status} reason=${entry.reason}`);
    if (entry.upstream.afterHead) {
      console.log(`  after_head=${entry.upstream.afterHead}`);
    }
    if (entry.upstream.changedPaths.length > 0) {
      console.log(`  changed_paths=${entry.upstream.changedPaths.join(", ")}`);
    }
    if (entry.downstream.runUrl ?? entry.downstream.workflowRun?.url) {
      console.log(`  run=${entry.downstream.runUrl ?? entry.downstream.workflowRun?.url}`);
    }
  }
}

async function main(argv) {
  const options = parseArgs(argv);
  if (options.help || !options.command) {
    usage();
    return 0;
  }

  const index = buildIndex(options);

  switch (options.command) {
    case "rebuild": {
      writeIndex(index, options.outputPath);
      if (options.json) {
        console.log(JSON.stringify(index, null, 2));
      } else {
        printHumanSummary(index);
      }
      return 0;
    }
    case "summary": {
      writeIndex(index, options.outputPath);
      if (options.json) {
        console.log(JSON.stringify(index.summary, null, 2));
      } else {
        printHumanSummary(index);
      }
      return 0;
    }
    case "unresolved": {
      writeIndex(index, options.outputPath);
      const unresolved = index.entries
        .filter((entry) => entry.followUpRequired)
        .sort((left, right) => String(right.timestamp).localeCompare(String(left.timestamp)))
        .slice(0, options.limit);
      if (options.json) {
        console.log(JSON.stringify(unresolved, null, 2));
      } else {
        printHumanUnresolved(unresolved);
      }
      return 0;
    }
    default:
      throw new Error(`Unknown command: ${options.command}`);
  }
}

main(process.argv.slice(2)).then(
  (code) => {
    process.exitCode = code;
  },
  (error) => {
    console.error(`error: ${error instanceof Error ? error.message : String(error)}`);
    process.exitCode = 1;
  },
);
