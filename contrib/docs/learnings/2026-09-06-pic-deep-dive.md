# Pic (cv/pic) deep dive: a Pi agent whose session is a durable Chrome DOM

Static analysis only (no install, build, test or repo script executed). Repo: `/home/tryinget/ai-society/softwareco/contrib/pic`, HEAD `d40e694` "Release v0.2.37" (2026-08-13), remote `dead-origin-20260906` → `https://github.com/cv/pic` (gone). All paths below are relative to that repo unless prefixed.

## 1. Summary

- Pic is a ~6k-line Node host plus a ~9k-line single-page Chrome app that embeds Pi's low-level `Agent` (pi-agent-core 0.84.1) and Pi's official tools, and makes **the browser DOM the authoritative conversation state**: a `pi-session` tree of nested `pi-entry` elements is both the UI and the provider context, checkpointed atomically to `.pic/session.html` as a self-contained read-only archive.
- One author (Carlos Villela), 171 commits in 8 days (2026-08-06 → 08-13), 21 tags, heavily agent-authored (AGENTS.md, `.agents/functions`, anti-slop lint plugin, "release patch" workflow functions). Apache-2.0.
- Maturity: an intense, well-engineered prototype. Real-Chrome integration tests (89 test cases, 15 files launch headless Chrome), a per-file CI matrix with merged Node+Chrome coverage and a coverage ratchet; but explicitly "experimental, do not use with untrusted prompts".
- It bypasses Pi's `AgentSession`/JSONL sessions/extensions/compaction entirely; it is Pi-the-model-loop, not Pi-the-product.
- Verdict: do **not** resurrect or fork as a product; pi-mono itself now has `packages/server` + `protocol` + `client` + `web-ui`, which is the right base for a browser front end. Keep the clone as a frozen reference and borrow mechanisms: fail-closed context compilation, run-scoped RPC with settlement and cancellation, atomic checkpoint store with backup/quarantine, page-reload recovery, reversible context "lens", the typed single `typescript` tool with a contract `.d.ts` and saved-function registry, and the engineering hygiene scripts.

## 2. What it is

**Purpose** (README.md:3-9, docs/architecture.md:3): a Pi agent whose live session and interface are one Chrome document. The user talks to an agent in a browser window; every user request becomes a "session object" in a tree; branches can run in parallel; results can be interactive artifacts (forms, trade-off explorers, timeline explorers, OpenUI React programs) that update locally without another model request; the whole thing persists as one HTML file that opens standalone.

**User story** (README.md:44-176): `npm run dev` opens Chrome; type prompts in the composer; select an earlier object in the session browser to branch from it; type `#` to reference other objects as bounded context; run up to three branches concurrently with per-run Stop; toggle between full and compact provider context; restart the process and get everything back from `.pic/session.html`; open that file directly as an archive.

**Release history** (no CHANGELOG file exists; `git log` and tags only):

| Date | Commits | Milestones |
|---|---|---|
| 2026-08-06 | 9 | "Build DOM-native Pic prototype" (2092656), context lenses + archives, artifacts, Markdown, CDP access, timeline explorers, OpenUI, automatic branch titles |
| 2026-08-07 | 22 | Apache licence + CI (3b2d5c8), Chrome CI hardening, v0.1.1 … v0.1.10 same day, coverage ratchet |
| 2026-08-08 | 36 | v0.1.11, v0.2.0 |
| 2026-08-09 | 21 | v0.2.1 … v0.2.8 |
| 2026-08-10 | 41 | v0.2.12 … v0.2.30; three-pane tool-detail workspace; isolated runner sessions (`PIC_SESSION_HTML`); "safer Pic workflow functions" |
| 2026-08-11 | 25 | v0.2.35; project functions; UI polish, a11y landmarks |
| 2026-08-12 | 4 | anti-slop Oxlint plugin installed and applied |
| 2026-08-13 | 13 | v0.2.36, v0.2.37: boundary parsing hardening, bounded lifecycle drains, "anti-slop source synchronization" check |

Pi dependency: `^0.83.0` at the first commit, `^0.84.1` from v0.1.4 (084aef6, 2026-08-07) onward; lockfile resolves 0.84.1 for pi-agent-core, pi-ai, pi-coding-agent, pi-telemetry.

**Size** (`find`/`wc -l`, lines of .ts/.js/.css/.html):

| Area | Files | Lines | Notes |
|---|---|---|---|
| `src/*.ts` (Node host) | 16 | 5,821 | artifacts.ts 1,664; chrome.ts 732; dom-session.ts 696; browser-rpc.ts 629 |
| `src/typescript/` | 5 | 1,651 | compiler.ts 378, functions.ts 536, capability-contract.d.ts 448 |
| `src/page/` (browser) | 11 | 9,155 | app.js 4,196; styles.css 2,838; app-model.js 601; react-ui-runtime.js 333; capability-runtime.js 299; archive.js 271; session-model.js 194; index.html 204 |
| `test/` | 30 | 8,702 | node:test, 89 `test(` cases |
| `scripts/` | 7 | 1,012 | test runner, coverage ratchet, structure/capability/anti-slop/bundle-size checks, README screenshots |
| `tools/oxlint/anti-slop` | 12 | 1,755 | vendored lint plugin (duplicated under `.agents/skills/install-anti-slop/assets`) |
| `.agents/` | 25 | 2,273 | 9 project "functions" + 2 skills |
| `docs/` | 4 | — | architecture.md + 3 PNG screenshots (336 KB) |
| `package-lock.json` | 1 | 358 KB | 668 `node_modules/` entries |

**Licence**: Apache-2.0 (LICENSE, package.json:6). No NOTICE file. The vendored anti-slop rules come from `dmmulroy/anti-slop` (skills-lock.json:4-9) and carry no licence header of their own — treat separately (see §9b).

## 3. Architecture map

### Processes and transport

- **Two processes**: `tsx src/index.ts` (Node ≥24) and one Chrome it spawns with a throw-away profile (`mkdtemp("pic-chrome-")`), `--remote-debugging-port=0`, `--no-first-run`, background networking off (src/chrome.ts:231-247). The DevTools port is read from `<profile>/DevToolsActivePort` (chrome.ts:124-153); page and browser targets are found via `http://127.0.0.1:<port>/json/list` and `/json/version` (chrome.ts:155-193).
- **No HTTP/WebSocket server of Pic's own; no SSE.** All transport is CDP over two `ws` sockets (page target + browser target, chrome.ts:262-265), wrapped by a 185-line `CdpClient` (src/cdp-client.ts) with per-request timeout, `AbortSignal` cancellation and socket-close rejection.
- Host → page: `Runtime.evaluate("globalThis.picApp.<method>(json…)")` (src/dom-session.ts:465-474). Page → host: a CDP binding `picHost` (`Runtime.addBinding`, chrome.ts:277; `Runtime.bindingCalled` listener chrome.ts:298-313). Two message families share the binding: UI "host requests" (`prompt`, `abort`, `artifact_submit`, `artifact_change`, `new_session`; src/index.ts:20-31, 104-161) and agent RPC envelopes (`rpc` / `rpc_cancel`; src/browser-rpc.ts:14-27). RPC responses are pushed back by evaluating `globalThis.__picResolveRpc(id, response)` in the *originating execution context* (chrome.ts:315-326), so a reloaded or replaced page can never receive a stale answer.
- The page is assembled at start: `src/page.ts` bundles markdown-it and the OpenUI React runtime with esbuild in-memory (page.ts:8-51) and inlines all scripts into `src/page/index.html` (placeholders at index.html:181-202). CSP is `default-src 'none'; script-src 'unsafe-inline'; connect-src 'none' …` (index.html:7-10), so the session document cannot reach the network at all.
- **Agent programs run in a separate isolated world** `pic-agent` (`Page.createIsolatedWorld`, chrome.ts:639-658) into which `src/page/capability-runtime.js` is injected. It shares the DOM with the UI world but not JS globals, so agent code cannot touch `picApp` internals. Programs are evaluated with `Runtime.evaluate` + `replMode` (chrome.ts:676-704) so `const` declarations persist across tool calls.

### How the Pi agent is embedded

- Uses Pi at the **agent-core level, not the coding-agent session level**: `new Agent({ initialState: { model, systemPrompt, thinkingLevel: "off", tools: [typescriptTool] }, streamFn, toolExecution: "sequential", transformContext })` (src/agent.ts:203-222). One `Agent` per run/branch (`createAgent`, agent.ts:193-279).
- Providers/auth come from pi-coding-agent's `ModelRuntime.create()` + `streamSimple`/`completeSimple`/`getAvailable` (agent.ts:173, 214, 239) and `SettingsManager.create(cwd).getDefaultProvider()/getDefaultModel()` (agent.ts:334-337). `PIC_MODEL=provider/id` overrides strictly (agent.ts:292-343).
- Pi's official tools (`createBashTool`, `createEditTool`, `createFindTool`, `createGrepTool`, `createLsTool`, `createReadTool`, `createWriteTool`) are instantiated once per run in `PiToolService` (src/pi-tools.ts:48-65) and exposed **not as model tools** but as the `pi.*` capability inside the TypeScript tool (`tool.execute(id, prepared, signal, undefined)`, pi-tools.ts:147). The model sees exactly one tool: `typescript` (src/typescript/tool.ts:17-70).
- Event bridge: `agent.subscribe` (agent.ts:224-266) forwards `message_start/update/end`, `tool_execution_start/end`, `agent_end` into the DOM (dom-session.ts:63-124 for the root session, 516-588 for a branch cursor). On `tool_execution_start` it fires a side request (`completeSimple`, `maxTokens: 24`, agent.ts:238-262) to title the tool card.
- Not used from Pi: `AgentSession`, `SessionManager` (JSONL), extensions/ExtensionAPI, compaction, skills, prompt templates, TUI, `pi-telemetry`. Hooks used: only `transformContext` and `streamFn`.

### Session format (Pic's own, not Pi JSONL)

`<pi-session version="1" session-id created-at updated-at active-leaf context-mode>` containing `<pi-state context="exclude">` and nested `<pi-entry id type>` → `<pi-payload>` + `<pi-children>` (app.js:1143-1173; initialised app.js:105-131). Messages are `<pi-message role status timestamp …>` with `<pi-text>`, `<pi-thinking>`, `<pi-tool-call id name status>` children and JSON blobs stored as `<script type="application/json" data-kind="arguments|usage|details|definition">` (app.js:133-155). Other entry types: `function` changes, `artifact` changes, `context-checkpoint`, `context-clear`. Provider messages are compiled back from the ancestry of a leaf (`compileMessagesAt`, app.js:1965-1996; `compileMessage`, app.js:1356-1412). The DOM contract the model is told about is in the system prompt (agent.ts:48-60).

### Durability model

- **What survives a process restart**: all messages (tree + branches), artifacts and their state, session-scoped saved functions, context checkpoints and the full/compact mode, object titles/summaries, `pi-state` contents. Restored via `restoreSession` (app.js:3412-3450), which marks runs that were `running|stopping` as `interrupted` (app.js:3428-3433).
- **What does not survive**: agent-world JS globals, CDP subscriptions and external target connections (chrome.ts:531-565), in-flight runs/tool calls, project/user function *changes* not yet written (they are files, so they do).
- **When it checkpoints**: after every `message_end`, `agent_end`, artifact/function/context change, object select/rename, and every 1 s during streaming (`scheduleStreamingCheckpoint`, dom-session.ts:436-449). Writes are coalesced to one in flight plus one follow-up (dom-session.ts:335-373).
- **How**: the page serialises a *standalone archive document* (src/page/archive.js:150-268: fresh `HTMLDocument`, same CSP, styles inlined, archived object browser, all artifact controls disabled, a read-only viewer script) after re-validating the live session (`validateRestoredSession`, src/page/session-model.js:47-90). `SessionStore.save` writes to a 0600 temp file, `fsync`s, copies the previous primary to `session.backup.html`, then `rename`s (src/session-store.ts:46-72); 50 MB cap (session-store.ts:13). Startup restores the primary, quarantines an invalid one as `session.invalid-<stamp>.html` and falls back to the backup (src/index.ts:55-92).
- **Page reload** (user hits F5 or Chrome navigates): `Page.loadEventFired` → if `globalThis.picApp` is missing, re-inject the document, re-restore from the last checkpoint, re-run `setReady` (src/page-recovery.ts:17-50), single in-flight recovery.
- **Isolated runners**: `PIC_SESSION_HTML=<path>` gives a process its own checkpoint (index.ts:191-196, 379-387); at readiness it prints one `PIC_RUNNER {"pid","devtoolsPort","targetId","sessionHtml"}` JSON line (index.ts:356-368) so a controller can drive it over CDP.

### Branches and concurrency

`startPrompt` (index.ts:261-323) refuses more than `PIC_MAX_CONCURRENT_RUNS` (default 3) and refuses a second run on an object already being worked on; each run gets a `BranchSession` that captures its leaf cursor (dom-session.ts:494-696), its own `Agent` and its own `FunctionService`/`ContextService`/`ArtifactService`/`PiToolService` (agent.ts:194-199). Browser RPC from agent code carries the `runId`; the host resolves services per run and fails closed for unknown/stale runs (browser-rpc.ts:94-101). In the page, capability proxies are created per run (`__picCapabilitiesFor(runId)`, capability-runtime.js:125-287) and every compiled program ends with `await __picWaitForRpcIdle(runId)` (compiler.ts:211-215; capability-runtime.js:114-123) so floating calls settle before the tool result returns. Runs share Chrome, the agent JS realm and the filesystem (docs/architecture.md:41-49).

### Context management

`transformContext` recompiles provider messages from the run's DOM ancestry before every request (agent.ts:219-222 → `compileAuthoritativeContext`, agent.ts:93-110). On failure it does not fall back silently: `streamFn` returns a synthetic error `AssistantMessage` stream (`contextFailureStream`, agent.ts:145-171), so the provider is never called with stale history (docs/architecture.md:29). A `context.checkpoint({label, summary})` from the model is only committed after `agent_end` (context.ts:65-90, 122-146) so tool-call/result pairs stay intact; `compact` mode replaces everything up to `through` with one summary user message (app.js:1965-1996) and is reversible via the header toggle (`context.use`, context.ts:148-156). `ensureBudget` estimates tokens from the last reported usage plus ~4 chars/token for trailing messages (context.ts:170-199) and writes a deterministic digest checkpoint before an oversized prompt (context.ts:92-120, 201-225).

### Auth / security model

None beyond "local single user". The DevTools port is loopback-only but **unauthenticated**; any local process can attach and evaluate JS in the page, submit prompts through `picHost`, or use the `cdp` capability path. Agent code is in an isolated world (globals protected) but has full DOM access; `pi.bash`/`edit`/`write` run with the host's permissions with no confirmation prompt; the `cdp` capability is unrestricted (`cdp.send` accepts any `Domain.command`, chrome.ts:403-422). Persisted HTML is validated for passivity before `importNode` (session-model.js:23-45 rejects `on*`, `srcdoc`, `javascript:` URLs, `<base|embed|iframe|link|meta|object>`, non-JSON scripts, >10,000 entries). Assistant Markdown is rendered through a strict tag/attribute allow-list (app.js:1030-1067). Secrets: Pic stores none; it relies on Pi's auth store via `ModelRuntime`. The README (line 9) and architecture doc (lines 51-60) are honest about all of this.

### Storage

`.pic/session.html`, `.pic/session.backup.html`, `.pic/session.invalid-*.html`, `.pic/.session-<pid>-<uuid>.tmp` (cwd); `.agents/functions/<name>.ts` (project functions, `@pic project` marker) and `~/.agents/functions/` (user, `@pic user`) (src/typescript/function-storage.ts:26-60); Chrome temp profile under `$TMPDIR/pic-chrome-*` removed on close; `.pi/` (Pi settings) is gitignored.

## 4. Key ideas worth stealing

1. **Fail-closed context compilation through `transformContext` + a synthetic error stream** (agent.ts:93-110, 145-171, 211-222). Reusable with pi-mono's `Agent` unchanged (same option names at HEAD, `pi-mono/packages/agent/src/agent.ts:101-102`). Any of our context-shaping extensions (pi-context-packer, pi-session-compaction) could adopt "if the transform fails, the model must not be called with the untransformed history".
2. **Run-scoped RPC with composed cancellation and settlement**: `AbortSignal.any([runSignal, perCallSignal])` (browser-rpc.ts:102-109; pi-tools.ts:130-133), browser-side timeout that sends `rpc_cancel` (capability-runtime.js:57-71), `settlePending` loops until no new work was enqueued (pi-tools.ts:167-172), stale run IDs fail closed (browser-rpc.ts:94-101). Directly relevant to the "one hung handler must not freeze the pipeline" work in pi-mono (d0164cb18) and to sidequest peer tooling.
3. **Atomic checkpoint store with backup + quarantine + size cap** (session-store.ts:46-94) and **coalesced streaming checkpoints** (dom-session.ts:335-373, 436-457). A 120-line pattern worth reusing for our own sidecars, receipts and session-restore state, where we currently mostly write JSON directly.
4. **Page-reload recovery as a tiny idempotent state machine** (page-recovery.ts:17-50; tests page-recovery.test.ts:36, 59). Applies to any browser UI we host for agents (pi-mono `web-ui`, ASC observer renderer).
5. **Session tree as nested DOM with "follow" semantics**: appending to a branch only moves the UI selection if the user was looking at that leaf (`selectIfLeaf`/`followObjectId`, app.js:1143-1173), so a background run never hijacks the view. Also the `#` object references that inject a bounded supplement from another branch into a user message (app.js:1300-1355) — cross-branch synthesis without copying transcripts.
6. **Reversible context "lens" instead of destructive compaction** (context.ts; app.js:1965-1996, 2055-2100): the checkpoint is an entry in the tree, `compact`/`full` is a mode attribute, the omitted history stays queryable. pi-mono has compaction/branch-summary entries in JSONL (`packages/coding-agent/src/core/session-manager.ts:69-90`) but the *mode toggle* idea is worth carrying into pi-session-compaction.
7. **One typed tool with a capability contract `.d.ts`** (src/typescript/capability-contract.d.ts; compiler.ts:89-185): each submission is type-checked as `(source) satisfies PicProgram` inside an in-memory `ts.createProgram`, saved functions are declared with inferred signatures, dependencies are found via the type checker's symbol table (compiler.ts:226-300) and ordered topologically (302-334), the registry is rebuilt from an append-only change log (functions.ts:526-536) with invalid entries pruned (355-377). Bounds: 64 functions, 100 KB each, 1 MB total (functions.ts:25-27). Scopes session → project → user with `@pic project|user` JSDoc markers and filename = function name (function-storage.ts:26-44, 62-154). This is the strongest single idea in the repo for reducing tool-call count and context size.
8. **Paged tool documentation on demand**: `artifacts.help(topic, {offset,limit})` with `nextOffset`/`complete` (artifacts.ts:381-418) keeps a 10k+ character OpenUI guide out of every prompt; the system prompt tells the model to page through it once per task (agent.ts:32).
9. **Cheap side-model titles**: 24-token `completeSimple` request per tool call for UI titles (agent.ts:238-262), and object titles/summaries settled after the run (app.js:1611-1660) with user-authored title locks winning. Cheap, and exactly the kind of thing our activity strip / session insights could use.
10. **Bound every growing thing, with the unit named**: RPC result 32k chars (browser-rpc.ts:12, 611-629), Pi tool text 24k + details 4k (pi-tools.ts:15, 193-212), CDP event buffer 500 events / 256 KB with a `dropped` counter (chrome.ts:424-490), CDP params preview 16k (chrome.ts:706-716), checkpoint 50 MB / 10,000 entries, help page 12k. Architecture invariant 7 (docs/architecture.md:35).
11. **"One authoritative source" enforced by CI**: `scripts/check-capabilities.ts` parses the `.d.ts` contract, the browser proxy object literals and the host dispatch switch, and fails when any method is missing from any of the three; `scripts/check-structure.ts:13-19, 132` enforces per-file line budgets (700 default, four explicit exceptions) and rejects runtime import cycles while ignoring type-only edges; `scripts/check-anti-slop-sync.ts` fails when the vendored plugin drifts from the skill asset.
12. **Coverage ratchet with a changed-lines gate** (coverage-ratchet.json; scripts/check-coverage.ts:33-60): floors may only rise; changed executable lines must hit 98%. Coverage merges Node c8 with Chrome `Profiler.startPreciseCoverage` dumps (chrome.ts:278-284, 588-604), and CI runs each test file as a matrix job then merges (`.github/workflows/ci.yml` jobs `test-plan`/`test`/`coverage`).
13. **Machine-readable readiness line + explicit isolation env** (`PIC_RUNNER`, `PIC_SESSION_HTML`, index.ts:356-368) — the same shape as our session-presence sidecar and sidequest handshake, but printed once on stdout.
14. **Self-contained HTML archive of a session** (archive.js) — a shareable, network-free, read-only rendering with the object browser and disabled artifacts. We have nothing equivalent for Pi JSONL sessions.

## 5. Comparison with our stack

### vs pi-mono `packages/coding-agent` + `packages/tui`

| Concern | Pic | pi-mono HEAD (d0164cb18, 2026-08-26, 0.84.3) |
|---|---|---|
| Session store | Pic HTML tree (`pi-session`) in `.pic/` | JSONL tree with `id/parentId`, `compaction`, `branch_summary`, `label`, `custom` entries (`session-manager.ts:46-156`) under `~/.pi/agent/sessions/` |
| Branching | Tree in UI, parallel runs on sibling branches, per-run Stop | Tree in file, `/fork`, `--session`, one interactive run per process |
| Context shaping | `transformContext` from DOM ancestry, reversible lens, budget digest | Compaction entries, extension hooks, "cache-friendly compaction primitives" (added and reverted between 0.84.1 and HEAD) |
| Tools | One `typescript` tool wrapping Pi tools + cdp/dom/artifacts/context/functions | Full tool set exposed to the model, extensions can add tools, configurable default tools (4d9aa837c), PowerShell tool (80e62761f) |
| UI | Chrome SPA, three panes, artifacts, OpenUI React | Terminal TUI; **`packages/web-ui`** (React `ChatPanel`, `MessageList`, `SandboxIframe`, artifact/attachment/console runtime providers — `web-ui/dist/index.d.ts`) |
| Remote/durable session | Only via CDP + `PIC_SESSION_HTML` | `packages/server` (`PiServer`, Unix transport), `packages/protocol` (CBOR framed), `packages/client`, `session-backends/sqlite-node` — all marked experimental |
| Extensions, skills, prompt templates, presence | none | yes |

Pic predates (or ignores) the server/protocol/web-ui direction; those packages are the upstream-blessed way to get a browser front end with the *same* AgentSession, extensions and JSONL sessions we already depend on. Pic's genuine differentiators over them are: DOM-as-context (navigation = context selection), parallel branch runs in one document, the typed single tool with saved functions, interactive local artifacts, and the standalone archive.

### vs pi-little-helpers (session presence, sidequest launch, Ghostty-bound sessions)

- **Session presence** (`owned/pi-extensions/packages/pi-little-helpers/extensions/session-presence.ts`, doc `docs/project/2026-04-12-session-presence-for-steve-hot-restore.md`): publishes `$XDG_RUNTIME_DIR/pi-session-presence/<pid>.json` with `sessionFile`, `resumeArgv`, Ghostty ancestry/surface and a title suffix so the workstation capture/plan/restore scripts can relaunch `pi --session <exact file>` in the right Ghostty tab. Pic's analogue is the `PIC_RUNNER` stdout line (pid, DevTools port, target id, session HTML). Gap: Pic has no sidecar file, no title binding (`<title>Pic</title>`, index.html:11 never changes), no cleanup of dead entries. Its *restore* story, however, is stronger than ours: the checkpoint is self-contained and validated, restore is `PIC_SESSION_HTML=<file> npm run dev`, and interrupted runs are marked rather than lost.
- **Sidequest / Ghostty launch** (`docs/project/2026-04-16-sidequest-ghostty-launch-contract.md`; `extensions/sidequestGhostty.ts`): tab-attach via D-Bus `new-tab --surface-id`, capability probe instead of a version gate, handshake file for launch admission, effect-indeterminate discipline. A Pic session is a **Chrome window with a temp profile**, not a Ghostty surface: under niri it would be captured as a Chromium window with a fixed title. To fit our restore stack it would need (a) a presence sidecar written by the host, (b) `document.title` carrying the session-id token so `session-capture.py` can correlate, (c) a restore recipe `cd <cwd> && PIC_SESSION_HTML=<file> npm run dev` instead of `pi --session`, and (d) admission through `core/lane-authority/gpu-admission.yaml`, since `chrome.ts:243` only adds `--disable-gpu` in headless mode. The Ghostty runtime-pin design (`infra/workstation/docs/project/2026-09-06-ghostty-runtime-pin-design.md`) shows how much of our recovery investment is Ghostty-specific (probe, D-Bus targeting, journald filter); a Chrome-hosted session would sidestep all of it but also lose tab topology, `/sidequest` peers, `fresh_handoff_spawn` and every extension.
- **Replace or complement?** Complement only. Ghostty-hosted Pi stays the primary because it carries the extension ecosystem (presence, sidequests, orchestrator, compaction, telemetry). A Pic-style browser session would make sense as a *viewer/branch workbench* on top of an existing Pi session (via pi-mono server/protocol), not as a second runtime.
- Curiosity: Pic's own `.agents/functions/*.ts` destructure `{ npm, shell, workspace, git, gh }` capabilities that are **not** in Pic's contract (`PicCapabilities` = artifacts/cdp/context/dom/functions/pi, capability-contract.d.ts:434-441). Pic would prune them at load (function-storage.ts:137-152) and never report the errors (functions.ts:333-353 drops `errors`). They were written for another runtime of the author's; the convention (`.agents/functions/<name>.ts` with a JSDoc marker, called by name with injected capabilities) is the interesting part.

## 6. Quality

**Tests**: 30 files, 89 cases, `node:test` via `tsx --test` (scripts/run-tests.ts); `concurrency` and `typescript` files run alone afterwards (run-tests.ts:4-7, 52-55). 15 files launch real headless Chrome. Coverage areas: DOM authority and restore across a fresh Chrome process (dom-session.test.ts:14, 47), archive byte limit (146), malformed checkpoint rejection (177), store atomicity/quarantine (session-store.test.ts:17-73), object selection with scoped context (session-browser.test.ts:61), parallel branch isolation (concurrency.test.ts:34), page recovery (page-recovery.test.ts:36, 59), TypeScript validation/saved functions/floating-call settlement (typescript.test.ts:15-214), Pi tool service cancellation and bounds (pi-tools.test.ts), agent fail-closed context (agent.test.ts:116, 162), RPC dispatch/cancellation/stale runs (browser-rpc.test.ts), artifacts (1,031 + 845 lines), Markdown sanitising (836 lines), OpenUI, CDP. Pure-unit tests inject `Pick<…>` service shapes rather than mocks (e.g. function-scopes.test.ts:18-50).

**CI**: `.github/workflows/ci.yml` — Node 24, `npm ci`, `npm run check` (ultracite/oxlint + `tsc --noEmit` + capabilities/structure/anti-slop-sync/openui-bundle-size checks), then a per-test-file matrix with `c8` + `PIC_BROWSER_COVERAGE=1`, then a merge job enforcing `coverage-ratchet.json` (lines 95 / branches 90 / functions 98 / statements 95, changed lines 98). Installs `fd` because Pi's find tool needs it.

**Typing/style**: `strict`, `NodeNext`, TypeScript 6.0.3 pinned exactly; `zod` 4 at every boundary (host requests index.ts:20-31, RPC envelopes browser-rpc.ts:14-27, CDP messages cdp-client.ts:7-19); branded `JsonValue`/`JsonInput` types (json.ts:3-25); browser JS uses a tiny `__picParse` boundary parser instead of `typeof` (capability-runtime.js:2-35). Ten custom "anti-slop" lint rules (oxlint.config.ts:11-22).

**Error handling**: centralised Error conversion and best-effort delivery (browser-rpc.ts:48-62, dom-session.ts:476-482), explicit timeouts (host RPC 9 s / 120 s instrumented, chrome.ts:83-90; CDP 30 s, evaluate 10 s), fail-closed on unknown runs/methods, quarantine on invalid state. Shutdown aborts runs, waits for idle, checkpoints, closes Chrome (index.ts:208-226).

**Dependencies** (package.json): runtime — `@earendil-works/pi-agent-core`, `pi-ai`, `pi-coding-agent` ^0.84.1 (locked 0.84.1); `@openuidev/react-ui` 0.13.5, `react-lang` 0.2.11 (public npm); `react`/`react-dom` 19.2.8; `esbuild` 0.28.1; `markdown-it` 15; `typebox` 1.3.11; `typescript` 6.0.3; `ws` 8.21.3; `zod` 4.4.3; `zustand` 4.5.7 (declared but never imported in src, scripts or test). Dev — oxlint/oxfmt/ultracite, c8 10.1.3, tsx, @types. 668 lockfile entries. **Install hooks**: none in Pic's own package.json (no preinstall/postinstall/prepare). Transitive packages flagged `hasInstallScript` in the lock: `esbuild`, `fsevents` (macOS only), `protobufjs` (twice), `@google/genai` (twice, via pi-coding-agent), `@openuidev/lang-core`. `engines.node >= 24`.

**Pi version drift (0.84.1 → pi-mono HEAD 0.84.3+25)**: every API Pic uses still exists with the same signature at HEAD — `Agent` options `initialState/transformContext/streamFn/toolExecution` (`pi-mono/packages/agent/src/agent.ts:99-122`), `AgentTool.{label,prepareArguments,execute(id,params,signal,onUpdate),executionMode}` (`packages/agent/src/types.ts:386-408`), `agent.subscribe/abort/waitForIdle/prompt/state`, `ModelRuntime.create/getAvailable/streamSimple/completeSimple` (`packages/coding-agent/src/core/model-runtime.ts:172, 404, 636, 643`), `SettingsManager.create/getDefaultProvider/getDefaultModel` (`settings-manager.ts:333, 713, 717`), `create{Bash,Edit,Find,Grep,Ls,Read,Write}Tool(cwd, options?)`, `createAssistantMessageEventStream` (`packages/ai/src/utils/event-stream.ts:86`). Changes in the window that touch Pic's surface: `fix: single edit input (#8011)` (edit tool argument shape — Pic forwards the model's object verbatim and documents the shape in capability-contract.d.ts:422-433, so the contract text may now be stale), "configurable default tools", optional PowerShell tool (not in Pic's fixed list, capabilities.ts:1-9), and an `expose provider context construction` feature that was added and reverted. Bumping to 0.84.3 should be a lock update, not a port.

## 7. Risks

- **Unauthenticated loopback DevTools port** (chrome.ts:234): any process on the machine can attach, evaluate in the page, submit prompts via `picHost`, and thereby reach `pi.bash` with the host user's permissions. Same class of exposure as our Claude-in-Chrome/surf-cli debugging ports, but here it is the agent's control plane.
- **Unrestricted `cdp` capability** (chrome.ts:403-422): the model can open, navigate or close any target and change browser state; only the system prompt asks it not to.
- **Host-permission tools without confirmation**; agent JS shares the DOM; prompt injection from page content/tool output is mitigated only by prompt text (agent.ts:15-19). The README says so.
- **Project functions are trusted input**: a cloned repo's `.agents/functions/*.ts` with `@pic project` become callable by the model with full capabilities (function-storage.ts:62-154). User-scope mutations require `confirmUserMutation`, which `index.ts`/`agent.ts:194-197` never wire, so they fail closed (good).
- **Checkpoint contents**: the full transcript including bash output lands in `.pic/session.html`. The primary is written 0600 (session-store.ts:58) but the backup is made with `copyFile` (session-store.ts:113-121), so it takes the umask default. Minor.
- **Temp Chrome profile** leaks on SIGKILL (cleanup only in `close`, chrome.ts:564).
- **Runtime prerequisites**: Node ≥ 24 (uses `AbortSignal.any`, `toReversed`, `z.json()`); workstation has Node v26.8.1, `/usr/bin/chromium`, `/usr/bin/brave` (not in Pic's candidate list — needs `PIC_CHROME_PATH`), `fd` on PATH. `pi` is not on PATH in the analysis shell; auth must exist in Pi's store for `ModelRuntime.getAvailable()` to return anything (agent.ts:295-299).
- **Breakage on current Pi**: nothing API-level found; residual risk is the edit-tool input change (#8011) and pinned early OpenUI packages. `zustand` is declared but unused. Trivia: `grantUniveralAccess` (chrome.ts:644) is the actual CDP parameter spelling, not a bug.

## 8. How to run it (not executed)

Prerequisites: Node ≥ 24 and npm; Chrome/Chromium (search order chrome.ts:96-104; on this box set `PIC_CHROME_PATH=/usr/bin/chromium` or brave); a configured Pi provider (`pi` then `/login`, or provider API key in the environment Pi recognises); `fd` on PATH for the `find` tool. Pic reads `.pi/settings.json` in cwd for the default model.

```bash
cd /home/tryinget/ai-society/softwareco/contrib/pic
npm ci                                   # lockfile-exact install; ~668 packages; no Pic-owned hooks
PIC_CHROME_PATH=/usr/bin/chromium npm run dev        # tsx src/index.ts → spawns Chrome, opens the Pic page
# variants
PIC_MODEL=anthropic/claude-sonnet-4-6 npm run dev     # strict provider/model selection
PIC_MAX_CONCURRENT_RUNS=5 npm run dev
PIC_SESSION_HTML=/tmp/pic-verification/session.html npm run dev   # isolated checkpoint, prints PIC_RUNNER line
npm run dev:watch                        # tsx watch
npm run check                            # lint, tsc, capabilities/structure/anti-slop/bundle checks
npm test                                 # node:test, launches headless Chrome repeatedly
npm run coverage                         # c8 + Chrome precise coverage, ratchet enforced
npm run docs:screenshots                 # regenerates README PNGs
```

Ports: Pic listens on nothing. Chrome opens a random loopback DevTools port; the host prints `Pic is running in Chrome on DevTools port <n>` and `PIC_RUNNER {...}` (index.ts:362-368). Files: `.pic/session.html` (+ backup/invalid), Chrome profile in `$TMPDIR/pic-chrome-*`. Stop with Ctrl-C (abort runs → wait idle → checkpoint → `Browser.close`, index.ts:208-226). Env vars: `PIC_MODEL`, `PIC_CHROME_PATH`, `PIC_MAX_CONCURRENT_RUNS`, `PIC_SESSION_HTML`, `PIC_BROWSER_COVERAGE` (+`NODE_V8_COVERAGE`), `COVERAGE_BASE` (CI ratchet). On this workstation a non-headless Chrome is a GPU desktop process; check `core/lane-authority/gpu-admission.yaml` before launching, and prefer `PIC_SESSION_HTML` under the scratchpad so `.pic/` is not created in the contrib checkout.

## 9. Recommendations

### (a) Borrow as idea

1. Fail-closed `transformContext` with a synthetic error stream for pi-context-packer / pi-session-compaction.
2. Run-scoped cancellation (`AbortSignal.any`) + settle-before-return for sidequest peer tools and orchestrator handlers.
3. Atomic write + backup + quarantine + size cap for presence sidecars, receipts, restore state.
4. Reversible context lens (mode toggle over a checkpoint entry) in pi-session-compaction.
5. A `typescript` Pi extension tool: contract `.d.ts` type-checked per call, saved functions with dependency ordering, session/project/user scopes with markers — reduces tool-call round trips for read-heavy work.
6. Paged `help(topic, offset)` for large tool guides instead of prompt bloat.
7. 24-token side requests for tool/object titles in pi-activity-strip / pi-session-insights.
8. Contract-sync, structure-budget and coverage-ratchet CI checks for pi-little-helpers.
9. A "session → standalone HTML archive" exporter for Pi JSONL sessions.
10. `PIC_RUNNER`-style readiness line and `PIC_SESSION_HTML`-style explicit isolation for anything we spawn as a peer.

### (b) Borrow as code (Apache-2.0: keep the LICENSE text and a "derived from cv/pic v0.2.37" attribution; no NOTICE file exists upstream)

- `src/cdp-client.ts` (185 lines; deps `ws`, `zod`) — bounded CDP client with cancellation.
- `src/session-store.ts` (122 lines; node:fs only).
- `src/page-recovery.ts` (50 lines; interface-only dependency).
- `src/typescript/compiler.ts` (378 lines; dep `typescript`) + `capability-contract.d.ts` as a template.
- `src/context.ts:170-225` token estimate and digest.
- `scripts/check-coverage.ts` + `coverage-ratchet.json`; `scripts/check-structure.ts` (cycle detector `importCycles`, 79-106).
- Do **not** lift `tools/oxlint/anti-slop/**`: it is `dmmulroy/anti-slop` content (skills-lock.json) with no licence header in the vendored copy; take it from its own source if wanted.

### (c) Fork / resurrect?

**No.** Not as a product: single-author 8-day prototype, no extension surface, no Pi session compatibility, and pi-mono now ships server/protocol/client/web-ui for the browser direction. Keep the clone frozen (tag `archive/v0.2.37`) as reference. If someone insists on reviving it, the first three steps are: (1) mirror the clone into our forge with the dead-remote note and the archive tag; (2) in an execute-allowed session, `npm ci` against the lock and get `npm run check` + `npm test` green with `PIC_CHROME_PATH=/usr/bin/chromium` (baseline before touching anything); (3) bump `@earendil-works/pi-*` to 0.84.3, re-check the edit-tool input contract (capability-contract.d.ts:422-433) and the OpenUI pins, then re-run the suite and decide.

### (d) Experiments for a follow-up session that may execute

1. `npm ci && npm run check && npm test` headless; record duration, flakiness, Chrome count.
2. Boot Pic against our workstation inference provider (`pi-workstation-inference-provider` / `.pi/settings.json` default model) and confirm `ModelRuntime.getAvailable()` lists it.
3. Kill `-9` mid-stream, restart, verify `interrupted` marking and backup fallback; corrupt `session.html` and verify quarantine.
4. Measure checkpoint size growth per turn and the 1 s streaming-checkpoint I/O on a long answer.
5. Set `document.title` to include a session token from the host, run under niri, and see whether `scripts/session-capture.py` can correlate the Chrome window like a Ghostty one.
6. Prototype the `typescript` tool as a pi-mono extension (register a tool via ExtensionAPI, compile with `compiler.ts`, execute in a Node `vm` or a Chrome isolated world) and compare tool-call counts on a read-heavy task.
7. Try pi-mono `packages/web-ui` + `packages/server` against a live session to see how much of Pic's UI (branch tree, artifacts) is already covered.

## 10. Open questions

- Why did cv/pic disappear (licensing, abandonment, moved private)? Are there forks or an npm publish? (package is `private: true`, so probably not.)
- Which runtime consumes `.agents/functions/*.ts` with `{ npm, shell, workspace, git, gh }` capabilities? It is not Pic and not pi-mono (no `agents/functions` references). If it is a Pi-adjacent tool, its "project functions" convention is relevant to us.
- Does pi-mono's ExtensionAPI expose anything equivalent to `transformContext`/`streamFn` so the fail-closed pattern can live in an extension rather than a fork?
- Does `fix: single edit input (#8011)` change the model-facing edit schema in a way Pic's contract text (capability-contract.d.ts `PicPiCapability`) would now misdescribe?
- Does pi-mono `web-ui` render session branches, and what does `session-backends/sqlite-node` store — is there already a durable multi-branch UI story upstream?
- Is `pi` on PATH for the user shell (it was absent in the analysis shell), and where is its auth store — needed before any run.
- Licence of the vendored `dmmulroy/anti-slop` rules.
- Would a non-headless Chromium launched by Pic need a row in `gpu-admission.yaml` given the residency scheduler, or is it admitted as an ordinary desktop process?
