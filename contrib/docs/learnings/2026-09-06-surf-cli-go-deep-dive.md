# surf-cli-go (wesen/surf-cli) deep dive: a Go host + Glazed CLI fork of nicobailon/surf-cli

Static analysis only (nothing built, run or installed). Repo under study: `contrib/surf-cli-go`
(local `main` = c524c08, 2026-04-25; remote `dead-origin-20260906/main` = 8f30b9e, 2026-07-14, **28 commits
ahead of the local checkout**). Comparison target: `contrib/surf-cli` (nicobailon/surf-cli v2.18.0, 2026-09-04).
Unless stated otherwise, `go/...` and `src/...` line numbers below refer to the remote tip
(`git -C contrib/surf-cli-go show dead-origin-20260906/main:<path>`), because that is the most complete copy.

## 1. Summary

- It is a **true fork** of nicobailon/surf-cli (shared root commit d75948f, fork point 55aca58 = upstream v2.6.0,
  2026-02-21) by Manuel Odendahl (wesen). 114 commits, 2026-02-25 to 2026-07-14, never re-merged upstream.
- It keeps the upstream MV3 extension (CDP via `chrome.debugger`) and socket protocol untouched, but adds a
  **Go native-messaging host** (`surf-host-go`, motivated by Snap-Chromium confinement) and a **Go CLI**
  (`surf-go`, cobra + go-go-golems/glazed) with YAML/JSON/Markdown output.
- On top it adds ~30 "browser-side verbs": ChatGPT/Claude/Kagi/Gmail/Freelancer/Upwork extraction, claude.ai bulk
  export, and libgen (1lib.sk) / Anna's Archive search+download.
- Maturity: prototype-to-beta. 169 Go test funcs against a mock socket host, no Go job in CI, no real-browser
  tests, a 52 MB binary committed to git, one stray personal note at the repo root.
- Verdict: **keep the archive, do not revive.** Upstream v2.18 has since gained sessions, a scheduler, doctor,
  remote access and real-Chrome E2E; the Go host solves a Snap problem we do not have (Arch + native Brave).
  Borrow the ideas (owned-tab retry, embedded extractor scripts, dual output, frame diagnose, claude.ai export);
  never run or port the libgen/Anna's Archive downloaders. Migrate `owned/test-capabilities` off `surf-go`.

## 2. What it is

**Purpose.** Same as upstream: "the CLI for AI agents to control Chrome" (`package.json:3`). Manuel's goal, per
`ttmp/2026/02/25/SURF-20260225-R1.../design-doc/01-...md:38-47`, was to make surf work with **Snap Chromium**,
whose strict confinement cannot exec `~/.nvm/.../node` (EXIT 126) and sees a different `/tmp` (socket inode
split-brain, `:172-173`). The fix path chosen (`design-doc/02-node-native-host-scope-and-go-migration-feasibility.md`,
R2 plan) was a static Go host with no Node dependency, plus a Go CLI because he already had the `glazed` command
framework. Later the repo became his personal automation toolbox (Kagi, Gmail, Upwork bidding, claude.ai archiving,
shadow-library downloads).

**History** (`git log`):

| Period | Author | Commits | What |
|---|---|---|---|
| 2025-12-28..2026-02-21 | Nico Bailon + contributors (Austin, Carlos, Aliou, dependabot) | 136 | upstream history up to v2.6.0 |
| 2026-02-25 (39 commits in one day) | Manuel | | socket path env, R1/R2/R3 research tickets, Go host phases 1-6, Glazed CLI, installer profiles |
| 2026-04-07..04-17 | Manuel | 43 | ChatGPT Go provider + file upload + model listing, `surf-go js`, Kagi search/assistant, Gmail, Claude ask/transcript, frame diagnose, Anna's Archive, libgen |
| 2026-04-25 | Manuel | 1 | "Fix libgen download error" (local `main` tip) |
| 2026-05-31..07-14 (remote only) | Manuel | 28 | ChatGPT cookie fix, Kagi redesign fix, freelancer.com + Upwork verbs, claude.ai sessions/export/rename/move, host error-propagation fix (HOSTERR), owned-tab retry, tracked binary |

The fork never pulled upstream after 55aca58: `package.json` still says 2.6.0 while upstream went to 2.18.0
(126 upstream commits since the fork point). Upstream contains no trace of the Go work (no `.go` files,
`grep wesen|surf-go|core-go` empty).

**In-repo documentation.** `ttmp/` (18,457 lines, 294 files) is a docmgr-style ticket tree: 21 tickets
(`SURF-20260225-R1` ... `SURF-20260714-HOSTERR`), each with `index.md`, `design-doc/`, `reference/01-...diary.md`,
`tasks.md`, `changelog.md`, and numbered probe scripts (e.g. 54 `scripts/NN-claude-*.js` DOM probes in R7). Plus
`README.go.md` (Go runtime install/troubleshooting), `go/pkg/doc/tutorials/01-building-browser-side-verbs.md`
(883 lines, an "intern guide" to writing extractor verbs) and `02-building-stateful-gmail-verbs.md`.
`ttmp/2026/07/14/claude-bulk-export-playbook.md` is a copy-paste runbook for `claude export-all`.

**Size by area** (remote tip for `go/`, local for the rest):

| Area | Lines | Notes |
|---|---|---|
| `go/cmd` (surf-go, surf-host-go, install) | ~2.6k + 1.8k tests | `surf-go/main.go` 697, `surf-host-go/main.go` 672 |
| `go/internal/cli/commands` | ~14k Go | 50+ files; upwork_* 3.3k, libgen_* 1.9k, claude_* 1.9k |
| `go/internal/cli/commands/scripts/*.js` | ~5k JS | 29 embedded page-side extractors |
| `go/internal/host` | ~3.4k | router/toolmap.go 740, providers/chatgpt.go 1,198 |
| `src/` (TS extension, from upstream) | 7.9k | fork touched ~330 lines |
| `native/` (Node host/CLI, from upstream) | 14.3k | fork touched ~900 lines |
| `test/` (vitest) | 3.4k | 10 files / 252 cases (upstream now 60 / 719) |
| `ttmp/` | 18.5k | tickets, diaries, probe scripts |

Fork-point diff (local main): 410 files, +38,786 / -160. Languages: Go, JavaScript (embedded + Node cjs),
TypeScript (extension), Markdown.

**Licence.** MIT, `LICENSE:1-3` "Copyright (c) 2025 Nico Bailon", unchanged by the fork. Manuel's additions carry
no separate notice, so they are MIT under the repo licence by implication; there is no CLA or explicit statement.
Oddities: a file literally named `" "` at the repo root (21 KB, Manuel's unrelated Nemotron-ASR article notes,
committed 2026-04-17); `.envrc:1` hardcodes `/home/manuel/snap/chromium/common/surf-cli/surf.sock`.

## 3. Relationship to the original

- **Fork with shared history**, not a rewrite or wrapper. Root commit identical (d75948f "Initial commit: Pi Chrome
  Extension with native messaging"); last shared commit 55aca58. (`git merge-base` fails only because the two
  clones have separate object stores; walking upstream's log and `git cat-file -e` finds 55aca58.)
- **File overlap**: `src/`, `native/`, `test/`, `scripts/`, `skills/`, `manifest.json`, build config are upstream's
  as of v2.6.0 plus small patches. The fork's JS-side changes are limited to: `native/socket-path.cjs` (new, 15
  lines, `SURF_SOCKET_PATH` env), the same env in `cli.cjs`/`host.cjs`/`mcp-server.cjs`/`do-executor.cjs`, a
  snap hint on socket errors (`native/cli.cjs:20-36`), `HOST_READY` carrying `runtime`/`socketPath`
  (`native/host.cjs:1717`), ChatGPT `--list-models` + multi-file upload in `native/chatgpt-client.cjs` (+372 lines),
  and in the extension: `FRAME_DIAGNOSE` + `PING` (`src/service-worker/index.ts:14-120,1879`,
  `src/content/accessibility-tree.ts:1484`), JS exception line mapping (`src/service-worker/index.ts:125`), CDP async
  evaluate timeout 10 s -> 35 s (`src/cdp/controller.ts:8`), and verbose native-port debug logging
  (`src/native/port-manager.ts:10-112`).
- **What it adds** (all under `go/`): `surf-host-go` (Go native host, core tools + ChatGPT provider), `surf-go`
  (Go CLI), `surf-go install` (Go installer incl. snap target), provider groups `chatgpt`, `claude`, `kagi`, `gmail`,
  `freelancer`, `upwork` (with `portfolio` subgroup), `annas-archive`, `libgen`, plus `frame diagnose`, `js --file`,
  `tool-raw`, network/console `stream`. The "extraction pipeline" mentioned in commit messages is the
  owned-tab -> readiness probe -> embedded JS extractor -> parse-once -> rows/Markdown pattern (section 4).
- **What it drops / never had**: everything upstream shipped after 2.6.0: Gemini image gen (2.7), `doctor`, `record`,
  `perf-audit`, browser request lock (2.8), real-Chrome E2E, Tailnet remote, `tab.move` (2.9), playbooks (2.10),
  oracle jobs (2.11), Pi extension, `page.html/save` (2.12), Kimi (2.13), **durable sessions and concurrent tab
  lanes** (2.15), video recording, socket group sharing (2.18). In the Go host, provider tools other than `chatgpt`
  and a "deferred" set (`smoke`, `batch`, `health`, `perf.*`, `bookmark.*`, `history.*`) are refused
  (`go/internal/host/router/toolmap.go:13-43`). `surf-go` also has no `do` workflows, no MCP server, no config
  file, no Windows transport (`go/internal/cli/transport/client.go:29-31`).

## 4. Architecture map

**Chrome control.** Unchanged from upstream: an MV3 extension attaches the DevTools protocol per tab with
`chrome.debugger.attach(target, "1.3")` (`src/cdp/controller.ts:166`) and uses content scripts for the
accessibility tree / element refs. No `--remote-debugging-port`, no Playwright. Chrome launches the native host
named `surf.browser.host` via a NativeMessagingHosts manifest (`chrome.runtime.connectNative`,
`src/native/port-manager.ts:158`); the host speaks length-prefixed JSON on stdio and exposes a **Unix socket**
(`/tmp/surf.sock`, or `SURF_SOCKET_PATH`) speaking newline-delimited JSON to any CLI.

```
surf-go / surf (Node) / nc  --NDJSON over unix socket-->  surf-host-go | native/host.cjs
        --native messaging (4-byte LE length + JSON, 16 MiB cap)-->  extension service worker
        --chrome.debugger (CDP) / chrome.tabs.sendMessage-->  page
```

**Go host** (`go/cmd/surf-host-go/main.go`): listens on the socket (`socketbridge/listener_unix.go:16-29`: removes
stale path, `chmod 0600`), reads native frames (`nativeio/codec.go:33-49`, `DefaultMaxFrameSize` 16 MiB at `:13`),
and correlates requests through a `pending.Store` keyed by a host-allocated id while preserving the client's
original id (`main.go:242-257`, `:396-424`). `tool_request` is mapped to extension message types by
`router.MapToolToMessage` (`toolmap.go:45-431`, a 60-case switch mirroring `native/host-helpers.cjs`);
`wait` is served locally (`LOCAL_WAIT`, `main.go:227-240`); streams (`STREAM_CONSOLE`/`STREAM_NETWORK`) are fanned
out per session (`router/stream_registry.go`). The ChatGPT provider runs **inside the host** as a state machine of
`CHATGPT_EVALUATE` CDP evaluations (`providers/chatgpt.go:78-204`: cookies -> new tab -> Cloudflare check ->
`/backend-api/me` login check -> model select -> upload -> `Input.insertText` -> poll assistant turn), talking to the
extension through a `NativeCaller` interface (`:23-26`) that makes it unit-testable with a fake. When the
extension disconnects, all CLI sessions get `extension_disconnected` (`socketbridge/session.go:88-98`).
Host log: `/tmp/surf-host-go.log`, mode 0600 (`main.go:662-672`).

**CLI** (`go/cmd/surf-go/main.go`). Cobra root with glazed help system (`:21-36`). Two command kinds:

1. `SimpleToolCommand` (`go/internal/cli/commands/tool_simple.go:34-118`): thin wrapper; all tool args come in as
   `--args-json '{...}'` (`:49`), plus the universal flags `--socket-path`, `--timeout-ms`, `--tab-id`,
   `--window-id`, `--debug-socket`. ~60 of these are registered from tables in `main.go:510-682`, grouped as
   `page`, `wait`, `tab`, `window`, `frame`, `dialog`, `network`, `console`, `cookie`, `emulate`, and root-level
   `click/type/key/scroll/hover/drag/select/screenshot/back/forward/reload`. `tool-raw --tool X` is the escape hatch
   (`tool_raw.go:43-59`).
2. Hand-written **browser-side verbs** (`kagi search`, `claude export`, `upwork jobs`, ...): a `//go:embed`ded JS
   extractor is prefixed with `const SURF_OPTIONS = {...};` (`kagi_search.go:24,83-92`), executed through the `js`
   tool, parsed once (`format.go:51-95` tries to JSON-decode the text block), then rendered either as glazed rows
   (`RunIntoGlazeProcessor`) or Markdown (`RunIntoWriter`). `buildDualModeCommand` (`main.go:478-487`) exposes
   Markdown by default and rows with `--with-glaze-output`; simple tools default to **YAML** rows
   (`glazed_defaults.go:14-21`, decided in R2 "output format investigation").

**Session/tab model.** No sessions. Every invocation opens a fresh socket connection (`transport/client.go:33-38`)
and either targets `--tab-id/--window-id` explicitly or uses the **owned-tab** discipline (`tab_ready.go`):
`tab.new` -> poll `location.href/readyState` via `js` until URL matches (`:137-168`) -> run -> `tab.close`
unless `--keep-tab-open`. Read-only verbs wrap this in `withOwnedTabRetry` (`:66-114`), which closes the failed tab
and opens a fresh one on transient CDP errors ("navigated or closed", "Detached while handling command",
"Cannot find default execution context", `:49-64`). Tab identity is the extension's numeric tab id; the fork
deliberately removed the `_resolvedTabId` echo from responses (commit 3bf2cd1, `main.go:588-602`).

**Output for agents.** Rows -> glazed formatters (`--output yaml|json|table|csv|markdown`, plus glazed field
selection/filters); the Markdown mode is written for LLM consumption (headings, bullet metadata, numbered
results, e.g. `kagi_search.go:259-324`). Errors: host wraps them as
`{"type":"tool_response","error":{"content":[{"type":"text","text":...}]}}` (`main.go:497-510`), the CLI turns
them into non-zero exits (`format.go:97-122`; fixed to propagate in b24c6d2).

**Config.** Env only: `SURF_SOCKET_PATH` (`go/internal/host/config/socket_path.go:8-25`, `native/socket-path.cjs`),
`SURF_HOST_LOG`, `SURF_GO_PATH`, `SURF_NODE_PATH`, `SURF_HOST_PATH`, `SURF_HOST_PROFILE=node-full|core-go`
(consumed by the generated wrapper script, `scripts/install-native-host.cjs` `createWrapper`). The Go installer
(`go/internal/installer/native_host.go:71-185`) copies the host binary to `~/.local/share/surf-cli/`, writes
`host-wrapper.sh` and the manifest for chrome/chromium/**brave**/edge (`:25-50`), and for Snap Chromium a second
target under `~/snap/chromium/common/` whose wrapper exports the snap-visible socket path (`:157-181`).

## 5. Key ideas worth stealing (with why they matter for us)

1. **Embedded, versioned page-side extractor scripts with an options prelude.** Each site verb owns one plain JS
   file (`go/internal/cli/commands/scripts/*.js`, 29 files) that only extracts and returns JSON; the Go side only
   shapes output. Contract: `const SURF_OPTIONS = ...` prefix (`kagi_search.go:91`), `waitForCondition` polling
   helpers (`scripts/upwork_jobs.js:10-20`), logged-in / Cloudflare detection (`:28-36`). These scripts are
   host-agnostic: they would run unchanged through Claude-in-Chrome's `javascript_tool` or a Pi tool. Today our
   agents re-derive DOM logic every session; a small library of such scripts is directly reusable.
2. **Owned-tab lifecycle + readiness probe + transient retry** (`tab_ready.go:33-135`). The doc comment at `:33-36`
   ("Do not use it for mutations ... replaying could apply the side effect more than once") is the important
   guardrail. `openOwnedTab` closes the tab itself when readiness fails (`:126-133`) so no tab leaks. Applies to any
   CDP driver we write.
3. **Dual-mode output** (Markdown for humans/LLMs, structured rows for pipelines, YAML default) with one shared fetch
   function (`tutorial 01`, Step 7-10 at `go/pkg/doc/tutorials/01-...md:451-585`). Cheap to copy in Python.
4. **Host error classification lesson** (`SURF-20260714-HOSTERR` design doc §1-3; fix at
   `go/cmd/surf-host-go/main.go:588-627`): bookkeeping keys the extension appended to every response
   (`_resolvedTabId`, `_hint`) made every data-error look like success and exit 0. Rule: strip transport metadata
   before classifying, and never let "row with an `error` field" exit 0. Relevant to every tool wrapper we build.
5. **`frame diagnose`** (`src/service-worker/index.ts:14-120,1879-1890`; `commands/frame_diagnose.go:97-163`):
   three inventories side by side: DOM `<iframe>` elements with src/sandbox/allow/rect, `chrome.webNavigation`
   frames with a content-script `PING` reachability check, and the CDP frame tree; plus warnings. Motivated by
   Claude artifact widgets that show up only as `about:blank` frames (R8 design doc §"Problem Statement"). We hit
   exactly this class of problem with claude.ai artifacts and MCP app iframes.
6. **claude.ai internal-API verbs run as same-origin `fetch` from a claude.ai tab** (`claude_api.go:13-16`,
   `scripts/claude_sessions.js`, `claude_export.js`): org auto-detect via `/api/bootstrap` memberships with the
   `chat` capability (`claude_export.js:26-33`), paged `chat_conversations_v2?limit=100&offset=` in bounded batches
   per JS call (`claude_sessions.js:36-49`, because one long call was truncated), conversation fetch with
   `?tree=True&rendering_mode=messages&render_all_tools=true` (`claude_export.js:79-80`), **base64 chunking at
   40,000 chars** to dodge the ~50 KB result-channel truncation (`:3-7`, Go loop `claude_export.go:100-120`), and
   **artifact reconstruction by replaying `create_file`/`str_replace`/heredoc `bash` writes**
   (`claude_artifacts.go:22-32,273,316,389`). `export-all` is resumable via `updated_at` and writes
   `export-all.jsonl` (`claude_export_all.go:79,207-230`). This is the most directly useful code for us: a
   backup/archive path for our own claude.ai conversations and artifacts.
7. **Cookie-based login checks are brittle**: ChatGPT moved to chunked NextAuth cookies (`__Secure-next-auth.session-token.0`),
   causing "login required" false positives (`skills/surf/SKILL.md` diff, ticket CG1; `providers/chatgpt.go:1045`).
   Same false positive on 1lib.sk from hidden login links, fixed by a visibility check
   (`libgen_download.go:177-192`). Lesson: check visible UI state, not DOM presence or cookie names.
8. **User-line mapping for JS exceptions** (`src/service-worker/index.ts:125-160`): subtracts the async-IIFE wrapper
   offset and quotes the offending source line. Small, worth copying into any "run JS in page" tool.
9. **Snap/Flatpak confinement handling**: socket under `$SNAP_USER_COMMON`, wrapper exporting `SURF_SOCKET_PATH`,
   `HOST_READY` announcing runtime + socket path (`native/host.cjs:1717`, `surf-host-go/main.go:96-100`), CLI hint
   on connection refusal (`native/cli.cjs:20-36`). If we ever run Flatpak Brave, the `/tmp` split-brain is the same.
10. **Unsafe-operation gating**: `upwork bid-prepare` only reads the form and writes an editable template
    (`upwork_bid.go:300-344`), `bid-apply` fills without submitting unless `--submit` (`:186-192,424-435`);
    claude `rename`/`move` are separate "gated mutation" verbs (`scripts/claude_mutate.js:1-3`). Good pattern for
    any agent-driven form submission.
11. **Zero-rows-is-failure invariant** (`upwork_jobs.go:402-413`, `--allow-empty-results`): distinguishes "empty
    market" from "blocked/logged-out page". Our `test-capabilities` proposal asks for the same
    (`contrib/surf-cli-go/docs/proposals/test-capabilities-surf-go-standard.md`, "Non-goals").
12. **Research trail per feature** (ttmp tickets with numbered probe scripts, diary, tasks): the R7 Claude ticket
    keeps 54 DOM probes that document how claude.ai's TipTap editor (`[data-testid="chat-input"].editor`,
    `scripts/claude_ask.js:21-28`) and model menu (`:17-18,71`) were reverse-engineered. Worth mirroring in our
    `diary/` convention when reverse-engineering a UI.

## 6. Comparison with what we use now

| Capability | Claude-in-Chrome (MCP ext.) | surf-cli v2.18 (upstream, Node) | surf-go / surf-host-go (fork) |
|---|---|---|---|
| Agent-agnostic entry point | No (Claude only, MCP tools) | Yes: CLI, socket API, MCP server, Pi extension | Yes: CLI + socket; no MCP server |
| Chrome control | extension, site-permission gated | extension + CDP via native host | same extension (2.6.0-era build) |
| Structured output | tool results (JSON to the model) | `--json`, `--llm-context` | glazed rows (yaml/json/csv/table) + Markdown dual mode |
| Durable sessions / named targets | tabs in current window | `session.new/ensure/info/rebind`, `SURF_SESSION`, named tabs, concurrent tab lanes (2.15) | none; `--tab-id`/owned tabs only |
| Concurrency safety | single agent | per-socket request lock (2.8), scheduler (2.15) | none (each CLI call = new connection) |
| Frames | limited | `frame.list/switch/js` | + `frame diagnose` (3 inventories, PING reachability) |
| Screenshots / recording | screenshot, GIF | screenshot, GIF `record`, WebM `video` (2.18) | screenshot only |
| Network capture / console | read requests, console | full capture store, export, curl, streams | list/get/body/stream (via host) |
| Workflows | none | `do` inline/named workflows, playbooks (2.10) | none |
| Provider chat via browser login | n/a | ChatGPT (+oracle jobs, GPT-6), Gemini, Perplexity, Grok, AI Studio, Kimi | ChatGPT (in Go host), **Claude (ask/transcript/list-models/thinking-mode)**, Kagi search/assistant |
| Site verbs | none | none | Gmail list/search, freelancer.com, Upwork jobs/bid/proposals/portfolio, libgen, Anna's Archive |
| claude.ai archive/export | none | `page.html/save` of rendered page | `claude sessions/projects/export/export-all/rename/move` (internal API, artifacts rebuilt) |
| Diagnostics | none | `doctor`, real-Chrome E2E in CI | `--debug-socket`, host log, mock-host tests only |
| Remote | none | authenticated Tailnet remote (2.9) | none |
| Windows / Snap | n/a | Windows named pipes | Linux/macOS only; Snap Chromium first-class |
| Maintenance | Anthropic | active (weekly releases) | dead (repo deleted; last commit 2026-07-14) |

Where surf-go is *ahead* of both: Claude-in-browser verbs, claude.ai export, frame diagnose, Kagi, Gmail, dual
output. Everywhere else upstream v2.18 is ahead, and the Go host's original justification (no Node inside Snap)
does not apply to our Arch/niri/Brave setup (`infra/workstation/scripts/session-capture.py:24,270` tracks
`brave-browser` windows; Brave is a native package here).

## 7. Quality

**Tests.** Go: 169 `Test*` functions in 36 files. `go/cmd/surf-go/integration_test.go:18-72` spins a fake socket
host per test and drives the real cobra root; 17 such tests cover each verb group. Provider logic is tested against
a fake `NativeCaller` (`providers/chatgpt_test.go`). Nothing touches a real browser. Node side: fork kept upstream's
10 vitest files (252 cases) and added `chatgpt-client`/`socket-path` tests; upstream is now at 60 files / 719 cases
plus a pinned real-Chrome E2E lane.

**CI.** `.github/workflows/ci.yml` runs only `npm run lint|test|check|audit` on Node 25; `codeql.yml` scans
JavaScript/TypeScript only; `gitleaks.yml`. **No `go build`/`go test`/`go vet` job exists**, so Go regressions were
only caught locally. Manual "compare Node vs Go output" scripts exist (`scripts/compare-go-node-output.cjs`).

**Error handling.** Reasonable after HOSTERR: errors propagate to non-zero exit, internal keys stripped,
`extension_disconnected` broadcast, context cancellation wired through `signal.NotifyContext` (`surf-go/main.go:691`)
and into ChatGPT polling. Weak spots: fixed `time.Sleep(2 * time.Second)` before extraction
(`libgen_download.go:292`), `_ = closeOwnedTab(...)` swallowed in several verbs, CDP async-evaluate timeout raised
globally to 35 s for one extractor (`src/cdp/controller.ts:5-8`), `annas_archive_download.go:42` has a broken
indent (still compiles). Windows transport is a stub.

**Dependency footprint.** `go/go.mod:1-8`: module path `github.com/nicobailon/surf-cli/gohost` (not go-gettable;
build from checkout only), `go 1.25.6`, direct deps only `spf13/cobra v1.10.2` and `go-go-golems/glazed v1.0.1`,
but glazed drags ~100 indirect modules: bubbletea/lipgloss/glamour, excelize, mongo-driver, gojq, sqlite3 (cgo),
bluemonday, mailru/easyjson, etc. (`go.mod:11-102`). Builds set `CGO_ENABLED=0` (`install_command.go:129`,
`scripts/build-go-host-binaries.cjs:44`), producing a ~50 MB static binary (`go/surf-go` at the remote tip is
52,238,512 bytes). Node: upstream's `@google/generative-ai`, `@modelcontextprotocol/sdk`, `zod`, browser polyfills;
dev: vite 7, vitest 4, biome, typescript 5.7. **No install-time hooks**: `package.json:41-56` has no
`postinstall`/`prepare`; `.npmignore`/`files` only. `.envrc` exports one variable (direnv would ask to allow it).

**Security-relevant.**
- No remote debugging port; control is a `0600` Unix socket at a predictable path (`/tmp/surf.sock`). Any process
  running as the user can drive the logged-in browser, run arbitrary JS in any tab (`js`), read cookies
  (`GET_CHATGPT_COOKIES`, `src/service-worker/index.ts:2781`) and mutate accounts (`claude_mutate.js` PUTs to the
  claude.ai API; Upwork `bid-apply --submit` spends Connects). Same trust model as upstream, without upstream's
  later request lock/session guards.
- Cookie values leave the browser: the extension ships ChatGPT cookies to the host over native messaging, the host
  only checks presence (`providers/chatgpt.go:86-95,1045`). The extension debug path logs cookie *counts* and
  120-char previews of evaluate results to the service-worker console (`src/native/port-manager.ts:88-112`);
  the host log `/tmp/surf-host-go.log` records poll states, not prompts.
- A **52 MB unreviewable binary is committed** (`go/surf-go`, commit dc0bd6b "refresh tracked surf-go binary").
  Treat as untrusted; never execute it, rebuild from source instead.
- The git remote is gone; nothing can be verified against upstream releases.
- **libgen / Anna's Archive downloaders.** `libgen search|download|suggestions|collections|collection` target
  1lib.sk, described in-code as "a Z-Library mirror" (`libgen.go:22-23`); `download --save-to` navigates the
  browser to the `/dl/` link, watches `~/Downloads` for `.crdownload` files and moves the result
  (`libgen_download.go:349-428`), and recognises "daily limit" / "login required" pages (`:363-377`).
  `annas-archive download --doi` resolves a DOI via `annas-archive.gl/scidb/`, picks a random "slow partner
  server" (`annas_archive_download.go:108-127`, fast mirrors refused because they need paid membership `:409-412`)
  and fetches the PDF with a 300 s `http.Client` (`:723`). Both sites distribute copyrighted books and papers
  without authorisation; Z-Library domains were seized by the US DOJ in 2022, and in Germany §53(1) UrhG excludes
  private copies from "obviously unlawfully made available" sources. Running these verbs from company machines
  creates legal and reputational exposure and would put our IP egress on lists we do not want to be on. The
  automation also strips the sites' rate limiting intent ("daily limit" handling). Recommendation: **never run,
  never port, and do not ship these files in any derived tool**; the only defensible reuse is the generic
  metadata-extraction technique (`z-bookcard` shadow-DOM reading, `libgen_search.go:74-101`).
- Upwork/freelancer.com automation (job scraping, bid submission, portfolio create/update/delete) most likely
  violates those platforms' ToS on automated access and bidding; treat as a research artifact, not a tool.

## 8. How to run it (NOT executed)

Prerequisites: Go >= 1.25.6 (`go.mod:3`; an older toolchain would trigger `GOTOOLCHAIN` auto-download), Node
(CI uses 25) + npm for the extension build, a Chromium-family browser (Brave is supported by the Go installer,
`installer/native_host.go:38-43`), network access for `go mod download` (~100 modules) and `npm ci`.

```bash
cd ~/ai-society/softwareco/contrib/surf-cli-go
# 0. optionally bring the checkout to the complete remote tip (mutates the repo; not done in this session)
git merge --ff-only dead-origin-20260906/main

# 1. build the extension (upstream toolchain; dist/ already exists locally from a 2026-05-10 build)
npm ci && npm run build                     # vite build -> dist/
# 2. load dist/ as an unpacked extension in a dedicated Brave profile, copy the extension id

# 3. build the Go binaries from source (do NOT use the tracked go/surf-go)
cd go && CGO_ENABLED=0 go build -o /tmp/surf-go ./cmd/surf-go \
      && CGO_ENABLED=0 go build -o /tmp/surf-host-go ./cmd/surf-host-go
go test ./...                               # mock-host tests, no browser needed

# 4. register the Go host for Brave (writes ~/.local/share/surf-cli/{surf-host-go,host-wrapper.sh} and
#    ~/.config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json)
/tmp/surf-go install <extension-id> --browser brave --host-binary /tmp/surf-host-go
#    alternative: keep upstream's Node host and use surf-go only as a client (same socket protocol):
#    node scripts/install-native-host.cjs <extension-id> --browser brave   (profile node-full)

# 5. restart Brave, then:
export SURF_SOCKET_PATH=/tmp/surf.sock      # default; snap users need ~/snap/chromium/common/surf-cli/surf.sock
/tmp/surf-go tab list
/tmp/surf-go page read --args-json '{"filter":"interactive"}' --output json
/tmp/surf-go js 'return document.title' --tab-id <id>
/tmp/surf-go frame diagnose --tab-id <id>
/tmp/surf-go claude sessions --limit 3      # needs a claude.ai-logged-in browser
/tmp/surf-go claude export <uuid> --out /tmp/claude-export
```

Env: `SURF_SOCKET_PATH`, `SURF_HOST_LOG` (default `/tmp/surf-host-go.log`), `SURF_GO_PATH`, `SURF_NODE_PATH`,
`SURF_HOST_PATH`, `SURF_HOST_PROFILE`. Logs: `/tmp/surf-host-go.log`, `/tmp/surf-host.log` (Node host), the
extension's service-worker console. Uninstall: `node scripts/uninstall-native-host.cjs --browser brave --all`.
Note our downstream `owned/test-capabilities` resolves this checkout automatically
(`owned/test-capabilities/src/core/surf-runtime.ts:99-199`: `TEST_CAPABILITIES_SURF_GO_BIN`,
`TEST_CAPABILITIES_SURF_GO_REPO`, or `go -C <repo>/go run ./cmd/surf-go`) and passes tool args as `--args-json`
(`:199`).

## 9. Recommendations

**Borrow as idea (no code needed):** owned-tab lifecycle with readiness probe and read-only retry; "extractor
script extracts, wrapper presents" split with a `SURF_OPTIONS` prelude; dual Markdown/rows output with YAML
default; strip transport metadata before error classification and make data-errors exit non-zero; zero-rows
invariant with an explicit `--allow-empty-results`; prepare/apply split with `--submit` for anything that spends
money or mutates accounts; per-feature research tickets with numbered DOM probe scripts; check visible UI state
rather than cookie names for login detection.

**Borrow as code (MIT, attribute "Nico Bailon / Manuel Odendahl, surf-cli"):**
- `go/internal/cli/commands/tab_ready.go` (whole file) and `format.go:51-122` -> port to a Python helper for our
  Pi/Claude-in-Chrome tools.
- `go/internal/cli/commands/scripts/claude_sessions.js`, `claude_export.js`, `claude_mutate.js` and
  `claude_artifacts.go` (heredoc/`str_replace` replay) -> a "claude.ai archive" Pi tool or a Claude-in-Chrome
  `javascript_tool` snippet. Expect API drift since 2026-07; re-probe first.
- `src/service-worker/index.ts:14-160` (`collectDomIframeInventory`, `collectExtensionFrameDiagnostics`,
  `formatJavaScriptException`) -> only if we ever maintain our own extension; otherwise the *idea* of a frame
  inventory as a JS snippet (DOM part only) is portable.
- `scripts/kagi_search.js`, `scripts/gmail_list.js`, `scripts/chatgpt_transcript.js`, `scripts/claude_transcript.js`
  as page-side extractors (host-agnostic).
- Do **not** copy: `libgen_*`, `annas_archive_*` and their scripts; `upwork_*`/`freelancer_*` (ToS); the tracked
  binary.

**Keep / revive?** Keep the archive (only copy in existence) at its current path, fast-forward the local `main` to
`dead-origin-20260906/main` in a session allowed to mutate, and leave it read-only. **Do not revive** as a
maintained tool: upstream v2.18 supersedes the Go host on every axis we care about, and the fork froze the extension
at the 2.6.0 line (Chrome MV3 and provider UIs have drifted since). The one live dependency is
`owned/test-capabilities`, which standardised on `surf-go` (README.md:76, `src/core/surf-runtime.ts`,
`contrib/surf-cli-go/docs/proposals/test-capabilities-surf-go-standard.md`, untracked, 2026-05-10). First steps:
1. Decide test-capabilities' runtime: migrate its `SurfClient` adapter to upstream `surf` v2.18 (`--json`,
   `session.ensure`) or pin it to a locally built `surf-go` from this archive; the proposal's "machine-readable
   command contract" ask is unmet upstream too and should be re-filed against nicobailon/surf-cli.
2. Extract the claude.ai export scripts into a small standalone tool of ours (Python or Pi tool), validated against
   the current claude.ai API.
3. Record the borrowed patterns as a TIP ("browser verb authoring": owned tabs, extractor scripts, dual output,
   error classification).

**Experiments for a follow-up session that may execute:**
1. In a throwaway shell: `cd go && go vet ./... && go test ./...` (mock host only) and `go build` both binaries;
   record build time, binary size, module download volume; diff the rebuilt `surf-go` against the tracked blob.
2. Dedicated Brave profile under niri with the fork's `dist/` (rebuilt) and the Go host: `tab list`, `page read`,
   `screenshot`, `frame diagnose` on a claude.ai artifact page; note what broke since 2.6.0.
3. `claude sessions --limit 3` then `claude export <uuid>` into scratch; verify artifact reconstruction against the
   UI; measure how far the internal API drifted.
4. Run the same `dist/` against upstream's Node host v2.18 to confirm surf-go works as a pure client (it should:
   the socket protocol is upstream's).
5. Feed `scripts/kagi_search.js` (with a hand-written `SURF_OPTIONS` prelude) through Claude-in-Chrome's
   `javascript_tool` to confirm the extractor library is usable without any host.
6. Run `owned/test-capabilities`' surf contract tests against (a) this checkout, (b) upstream v2.18 with a shim, to
   size the migration.

## 10. Open questions

- Why was wesen/surf-cli deleted (2026-07-14 last commit, gone before 2026-09-06)? Related to the Upwork/libgen
  content, or just housekeeping? No issue tracker survives.
- Did any of Manuel's work go upstream? Upstream has its own `native/socket-path.cjs` and `SURF_SOCKET_PATH`
  (credited to @aliou in CHANGELOG 2.6.0) but at the fork point `native/host.cjs:19` still hardcoded
  `/tmp/surf.sock` (R1 report §3.4); provenance is unclear.
- Who built `dist/` and `node_modules/` in this checkout on 2026-05-10 and wrote `docs/proposals/...` (untracked)?
  Presumably a test-capabilities session; if so, that session already executed repo code here.
- Does the 2.6.0-line extension still load and attach on current Brave/Chrome (manifest V3 changes, CDP 1.3)?
- Does the claude.ai internal API (`/api/bootstrap`, `chat_conversations_v2`, `render_all_tools`) still respond as
  the July scripts expect?
- Is the tracked `go/surf-go` reproducible from source (same Go version, `CGO_ENABLED=0`)? Until checked, treat it
  as opaque.
- Should the local `main` be fast-forwarded to the remote tip (28 commits) and the stray `" "` file and binary be
  purged in our archive copy, or is the archive meant to stay byte-identical?
- Does `owned/test-capabilities` currently pass with this checkout, and is anyone running it?
