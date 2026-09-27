# Pic (cv/pic v0.2.37) execution follow-up: install, CI suite, kill -9 restore, `typescript` tool spike

Companion to the static deep dive [`2026-09-06-pic-deep-dive.md`](2026-09-06-pic-deep-dive.md) (§9(d) follow-ups 1, 3, 4 partially, 6). Everything below was executed on 2026-09-06 in a sandbox copy; the archived clone `/home/tryinget/ai-society/softwareco/contrib/pic` (HEAD `d40e694`) was never modified (`git status` clean, no `.pic/` created).

## 1. Environment

| Item | Value |
|---|---|
| Workstation | Linux 7.1.11-arch1-1, niri desktop |
| Node / npm | v26.8.1 / 12.0.2 (Pic wants `>=24`; CI uses 24) |
| Chrome | `/usr/bin/chromium` 152.0.7977.64 (Pic's candidate list; `/usr/bin/brave` would need `PIC_CHROME_PATH`) |
| `fd` | 10.5.0 on PATH (Pi's find tool) |
| Sandbox | `cp -a` of the clone to `<scratchpad>/pic-exec/` (scratchpad = `/tmp/claude-1000/-home-tryinget-…/f2e78a27-…/scratchpad`) |
| Pi in Pic's lock | `@earendil-works/pi-{agent-core,ai,coding-agent}` 0.84.1, TypeScript 6.0.3 |
| Local model | `http://127.0.0.1:1234/v1`, alias `baseline-text-visible` → `local/Qwen3.8-27B-AEON-NVFP4-FP8` on vLLM 0.27.1 (canonical baseline-text lane, `enable_thinking=false`); `/v1/models` also lists `baseline-text`, `baseline-text-small[-visible]` (Qwen3.5-4B llama-cpp). A tool-call probe returned `finish_reason: tool_calls` with well-formed `tool_calls`, so the lane can drive Pic's single `typescript` tool. No paid provider key was used anywhere. |

Two environment quirks that cost time and are worth knowing:

- **tsx IPC socket vs long `TMPDIR`**: tsx creates `$TMPDIR/tsx-<uid>/<pid>.pipe`; with the 130-character scratchpad path as `TMPDIR` every `tsx` invocation dies with `listen EINVAL … .pipe` (Unix socket `sun_path` limit, 108 bytes). Fix used: a short symlink `/tmp/claude-1000/pt -> <scratchpad>/tmp` as `TMPDIR`. Pic's Chrome temp profiles (`mkdtemp(tmpdir()/pic-chrome-…)`) then land under the scratchpad as intended.
- **`page.ts` bundles `markdown-it` relative to `process.cwd()`** (esbuild in-memory build, no `resolveDir`). Running `tsx src/index.ts` from a workspace directory that is not the repo fails with `Could not resolve "markdown-it"`; the workaround for an isolated workspace is a `node_modules` symlink in that workspace (Pic's own `npm run dev` always runs from the repo root, so the author never hit it).

## 2. Install and lifecycle scripts

`npm ci --ignore-scripts`: 598 packages added, 599 audited, **0 vulnerabilities, 6.2 s wall** (registry, warm cache). Deprecation warnings only: `node-domexception@1.0.0`, `glob@10.5.0`, `recharts@2.15.4`.

Lifecycle scripts npm *would* have run for registry dependencies (only `preinstall`/`install`/`postinstall` count; the many `prepare`/`prepublish` scripts in the tree — `tshy`, `husky`, `npm run compile` in `google-auth-library`, `gaxios`, `undici`, `lru-cache`, `glob`, … — never run for registry installs). All read; none executed:

| Package (lock `hasInstallScript`) | Script | What it does | Needed? |
|---|---|---|---|
| `esbuild@0.28.1` | `postinstall: node install.js` | `checkAndPreparePackage()`: `require.resolve('@esbuild/linux-x64/bin/esbuild')`; if missing, tries `npm install` into a private dir, then a direct registry download; then `validateBinaryVersion`. Optional-dep binary is present, so it would have been a no-op check. | No — `esbuild.transformSync` and Pic's page bundling work without it. |
| `protobufjs@7.6.5` (2 copies: top-level and under `pi-coding-agent`) | `postinstall: node scripts/postinstall` | Reads its own `package.json`; **returns immediately** because `versionScheme` is absent (it only prints a dependency-range warning). | No. |
| `@google/genai@1.52.0` (2 copies, via `pi-coding-agent`) | `preinstall: echo 'preinstall: no-op'` (plus a `prepare` that does not run for deps; `scripts/prepare.js` is not even shipped) | Nothing. | No. |
| `@openuidev/lang-core@0.2.11` | `postinstall: node ./postinstall.cjs` → `dist/postinstall.cjs` | **Installation telemetry to PostHog**: random install id, salted SHA-256 of the git origin, Node/OS/arch/package-manager versions, CI/Docker flags; honours `DO_NOT_TRACK`/`OPENUI_TELEMETRY`-style opt-outs; wrapped in `try {} catch {}` so it "never fails installation". | No — and a good reason to keep `--ignore-scripts` (or set the opt-out) for this dependency. |
| `fsevents@2.3.3` | `install: node-gyp rebuild` | macOS only, marked optional, not installed on Linux. | n/a |

Verdict: nothing in the tree needs its install hook on Linux; `--ignore-scripts` is the right default for this repo, and the only script with side effects beyond the package directory is OpenUI's telemetry.

## 3. `npm run check` and the test suite

**`npm run check`** (CI job `check`): passes in **7.5 s** — ultracite (oxfmt + oxlint, 79 files), `tsc --noEmit`, `check-capabilities` ("33 model methods reflected from declarations"), `check-structure` ("31 source files, no static relative-import cycles, size budgets satisfied"), `check-anti-slop-sync` (12 mirrored files), `check-openui-size` (2,420,182 B JS, 223,195 B CSS).

**`npm test`** (`tsx scripts/run-tests.ts`, the same test files CI runs per-file under c8), `PIC_CHROME_PATH=/usr/bin/chromium`, headless (`--headless=new --disable-gpu` is what the tests pass; no GPU process on the desktop, so nothing to admit in `gpu-admission.yaml`):

| Batch | Files | Tests | Result | Duration |
|---|---|---|---|---|
| regular (parallel `--test`) | 28 | 83 | 83 pass | 31.8 s |
| `test/concurrency.test.ts` (isolated) | 1 | 1 | pass | 18.8 s |
| `test/typescript.test.ts` (isolated) | 1 | 5 | pass | 24.5 s |
| **total** | 30 | **89** | **89 pass, 0 fail, 0 skipped** | **1 min 15.5 s wall** |

Peak concurrently running Chromium **processes** carrying a `--user-data-dir=…/pic-chrome-*` argument: **85** (≈ 15 browser instances × 5–6 helper processes, because the regular batch runs 28 files in parallel and 15 of them launch Chrome). After the run: 0 Chrome processes, 0 leftover `pic-chrome-*` profiles. One run only, so no flakiness statement beyond "green first time"; the slowest single tests were the artifact explorers (7.5–7.8 s each) and the context-compaction DOM test (7.4 s).

Failures encountered were **environment**, not product: (1) the tsx socket-path `EINVAL` above (fixed with the short `TMPDIR`); (2) one run started from the wrong cwd (my mistake). No real test failure.

`npm run coverage` (CI's merged c8 + `Profiler.startPreciseCoverage` + ratchet): see §7 addendum.

## 4. Kill -9 restore trial

Setup (all throwaway, all under the scratchpad):

- Host: `tsx <sandbox>/src/index.ts` run with cwd `<scratchpad>/kill9/workspace/` (with a `node_modules` symlink, see §1), `PIC_SESSION_HTML=<workspace>/.pic/session.html`.
- Model: `PIC_MODEL=local-baseline/baseline-text-visible` (strict) with **`PI_CODING_AGENT_DIR=<scratchpad>/kill9/pi-agent-dir`** containing only a `models.json` for the `local-baseline` provider (`baseUrl http://127.0.0.1:1234/v1`, `api openai-completions`, literal `apiKey`, `compat.supportsDeveloperRole=false`…). Pi's `ModelRuntime` therefore had no access to the user's `~/.pi/agent/auth.json` — `getAvailable()` listed exactly the local model, and Pic's 24-token tool-title side requests also went to it (`data-model-title="List Current Directory Contents"` appeared on the tool card).
- Chrome: `PIC_CHROME_PATH` → a 3-line wrapper `exec /usr/bin/chromium --headless=new --disable-gpu "$@"`, so Pic's own args (`--user-data-dir=<mkdtemp>`, `--remote-debugging-port=0`, `about:blank`) still apply. The user's running Chromium (`--remote-debugging-port=9222 --user-data-dir=/tmp/chromium-agent`) and Brave were never touched.
- Driver: a 20-line CDP script (`ws` from Pic's `node_modules`) that `Runtime.evaluate`s in the Pic page; prompts were submitted exactly as the composer does, `globalThis.__picSendHost({type:"prompt", text, baseLeafId: <pi-session active-leaf>})`; state read back from the DOM (`pi-message` count, `pi-entry[data-run-status]`, last message `status`/text length).

Transcript (times are local, 2026-09-06):

| Time | Action | Observation |
|---|---|---|
| 23:35:05 | run 1 start | `PIC_RUNNER {"devtoolsPort":36549,"pid":3378784,"sessionHtml":…,"targetId":…}`; empty session checkpoint written immediately: **290,174 B** (the archive baseline: inlined CSS, read-only viewer script, object browser). |
| 23:35:38 | turn 1 "Reply with exactly PING-ONE" | complete in <1 s; 2 messages; checkpoint 292,616 B (+2.4 KB), `session.backup.html` appears. |
| 23:35:40 | turn 2 "call `pi.ls({path:"."})` once…" | model emitted one `typescript` tool call → `pi-tool-call name="typescript" status="complete"`, `toolResult is-error="false"`, final answer; 6 messages; checkpoint 296,339 B (+3.7 KB). |
| 23:35:41–58 | turn 3 "700-word essay" | streamed to 4,859 chars, run complete in DOM; checkpoint 310,377 B (+14 KB for 4.9 KB of text: Markdown source + rendered HTML + usage JSON). |
| 23:36:19 | **`kill -9` host (tsx wrapper + node)** ~20 s after the run finished | host dead instantly; **10 Chromium processes orphaned**, profile `…/pt/pic-chrome-DxZqHR` left on disk (as predicted: cleanup lives only in `ChromeRuntime.close`). `session.html` on disk: 3 `pi-entry` objects with `data-run-status` = complete, complete, **running**. |
| 23:37:24 | run 2 start (same `PIC_SESSION_HTML`) | Restored **8 messages, all text intact (essay 4,859 chars, tool call + result)**, runs shown as `complete, complete, interrupted`. The finished essay run is labelled *interrupted* — see finding F1. |
| 23:37:31 | turn 4 "900-word essay", then poll | user message checkpointed at 23:37:31.48 (311,229 B). Assistant text stayed at 0 chars for ~7 s, then jumped to 3,430 chars in one update. |
| 23:37:38.878 | **`kill -9` host ~10 ms after that first chunk arrived** | checkpoint mtime still 23:37:31.48 → the partial answer (3,430 chars) was **not** on disk. 11 Chromium processes orphaned, second profile leaked. |
| 23:37:41 | run 3 start | Restored 9 messages: everything up to and including the turn-4 *user* message; no assistant stub for turn 4; runs `complete, complete, interrupted, interrupted`; the interrupted entries have `data-run-id` removed. |
| 23:37:46 | turn 5 "Reply with exactly PING-FIVE" on top of the interrupted branch | works: `PING-FIVE`, run complete, 11 messages, 313,306 B. Context compilation over an ancestry containing an interrupted run is fine. |
| 23:37:47 | `SIGTERM` | "Stopping active runs, checkpointing, and closing Pic…", final checkpoint 313,089 B, **0 Chrome processes, 0 profiles left**. |
| 23:37:53 | run 4 after truncating `session.html` to 120,000 B | Startup **quarantined** it as `session.invalid-2026-09-06T21-37-53-104Z.html` (120,000 B), restored the **backup** (313,306 B → 11 messages, `PING-FIVE` present) and continued; turn-5 run shows as interrupted because the backup predates the SIGTERM checkpoint. |
| 23:39:49 | run 5, streaming observation only (canal essay), SIGTERM | mtime trace: user message checkpoint 23:39:51.00; assistant text 0 chars until 23:39:58.5 then 2,966 chars; **checkpoint at 23:39:59.32** (317,763 B, i.e. ~0.8 s after the update); next chunk to 5,372 chars at 23:40:03.7, `message_end` checkpoint 23:40:03.93 (326,682 B). |

Findings:

- **F0 — the checkpoint/restore path does what the deep dive says.** Messages, tool calls/results, model metadata, titles, the object tree and `active-leaf` survive `kill -9`; invalid primaries are quarantined and the backup is used; a session continues after an interrupted run; clean shutdown leaves nothing behind. Restore output in the page is a `Restored N messages … from the DOM checkpoint.` notice.
- **F1 — a normally finished run restores as `interrupted` if the process dies before the *next* checkpoint.** `index.ts startPrompt` sets `data-run-status="complete"` in `branch.finish()` inside the `finally` *after* `agent.prompt()` resolves, i.e. after the `agent_end` checkpoint; `finish()` itself does not checkpoint (`dom-session.ts:689-691`). So the last checkpoint of every run says `running`. Cosmetic (no data loss), but it makes the UI lie after any crash, and the deep dive's "interrupted runs are marked" reads better than reality: *every* last run is marked interrupted. One-line fix: `await this.root.setRunStatus(...); await this.checkpoint();`.
- **F2 — streaming durability is bounded by the provider's chunking, not by Pic's 1 s timer.** `scheduleStreamingCheckpoint` is armed by `message_update` events (`dom-session.ts:391-394`) and fires 1 s after the *first* update since the last checkpoint. It did fire (run 5: 0.8 s after the 2,966-char chunk). But the workstation adapter in front of vLLM delivered the answer in ~3 KB chunks 5–7 s apart, so the loss window after `kill -9` was "everything since the previous chunk", not "≤1 s of tokens". With a token-streaming provider the window is ≤1 s; with this lane it is one chunk. Not a Pic bug, but the durability claim is provider-dependent.
- **F3 — `kill -9` leaks Chrome.** Each hard kill left ~10 Chromium processes and one `pic-chrome-*` profile (`--headless=new`, so invisible on the desktop). A supervisor would need `pkill -f -- "--user-data-dir=$TMPDIR/pic-chrome-"` or a `prctl(PR_SET_PDEATHSIG)`-style launcher. Pic prints the profile path nowhere; it is only recoverable from `/proc/<chrome>/cmdline`.
- **F4 — checkpoint growth**: ~290 KB fixed archive overhead, then roughly 2.9× the visible text per assistant message (Markdown + sanitised HTML + JSON blobs), ~3.7 KB per tool call/result pair for a small result. The 50 MB cap corresponds to a very long session; the per-checkpoint I/O (0.3 MB temp write + fsync + copy backup + rename) is trivial at this size.
- **F5 — isolation recipe that works**: `PI_CODING_AGENT_DIR` with a models-only `models.json` is a clean way to run Pic (or any Pi embedding) against the local lane without exposing paid keys; Pic created `auth.json`/`models-store.json` inside that directory on its own.

## 5. Spike: the typed `typescript` tool as a Pi extension

- **Repo/branch**: `/home/tryinget/ai-society/softwareco/owned/pi-extensions`, branch **`spike/pic-typescript-tool`**, commit **`a0411c361`** ("spike(pi-typescript-tool): typed `typescript` tool prototype derived from cv/pic v0.2.37"), 42 files, package `packages/pi-typescript-tool/` only. The checkout was returned to `main` afterwards; the foreign uncommitted changes in other packages were not staged. Nothing was pushed.
- **Scaffold**: `uvx copier copy --trust --defaults -d scaffold_mode=simple-package -d repo_name=pi-typescript-tool -d command_name=typescript-tool -d release_config_mode=none <pi-extensions-template>` (repo convention per `AGENTS.md`); `.copier-answers.yml` committed; `private: true`.
- **Files that matter** (313 lines of source + 98 lines of tests; the rest is template boilerplate):
  - `src/capability-contract.d.ts` (28 lines) — script-scoped globals `ToolCapabilities { fs: { list(path?), read(path, maxBytes?) } }` and `type ToolProgram = (capabilities: ToolCapabilities) => unknown`. Header: derived from Pic's `capability-contract.d.ts`, Apache-2.0.
  - `src/typescript-gate.ts` (170 lines) — `analyzeSnippet` (exactly one top-level expression statement; imports/declarations rejected on the AST before any checker runs), `checkSnippet` (in-memory `ts.createProgram` over `[contract, "const __tool_program = (<src>) satisfies ToolProgram"]`, `strict`, `lib.es2022` only, no DOM, `types: []`), `compileSnippet` (`ts.transpileModule` to an `(async (capabilities) => …)` factory), `runSnippet` (`vm.runInNewContext` with a null-prototype sandbox so `process`, `require`, `globalThis` of the host are unreachable, plus a wall-clock `Promise.race` timeout and `AbortSignal` hook). Header: derived from Pic's `compiler.ts`.
  - `extensions/typescript-tool.ts` (115 lines) — `pi.registerTool({ name: "typescript", parameters: Type.Object({ code }), execute })`; the tool description embeds the contract text; `createCapabilities(root)` is the read-only fs capability rooted at `ctx.cwd` with a path-escape guard, 500-entry listing cap, 16 KB read cap; results bounded to 16k chars; validation failures `throw` (Pi's way of flagging `isError`). Header: derived from Pic's `tool.ts`.
  - `tests/typescript-gate.test.mjs` (7 `node:test` cases): accepts a clean program and an expression; rejects undeclared capabilities (`bash`, `fs.write`), wrong argument types, implicit `any`; rejects imports/declarations/multi-statement/unparseable input without executing; compiled programs run against a fake capability; timeout and host-global hiding (`process is not defined`); path-escape guard and read truncation; registration through a fake `pi` and end-to-end `execute` with `ctx.cwd`.
- **Gate results**: package `npm test` (root `package-quality-gate.sh`: biome lint, `tsc --noEmit`, `node --test`, structure/file-budget validation, host-contract test, `npm pack`) **green**; 9/9 tests pass in 0.76 s. `tsconfig` needed `allowImportingTsExtensions` because the extension imports `../src/typescript-gate.ts` (jiti at runtime and Node's native type stripping in tests both want the `.ts` suffix).
- **Live**: `PI_CODING_AGENT_DIR=<isolated> pi -ne -e packages/pi-typescript-tool/extensions/typescript-tool.ts --model local-baseline/baseline-text-visible -p "…"` against a 3-file directory.
  - "list the files here": one tool call, correct answer, **1.4 s** end to end.
  - "list recursively and read alpha.txt": first attempt with the initial description **looped**: the model wrote `const out = { files: [], dirs: [] }` and an unannotated `(dir) =>`, the gate answered `Parameter 'dir' implicitly has an 'any' type` / `Argument of type 'string' is not assignable to parameter of type 'never'`, the model retried three times then sent `{}` and kept going until my 180 s timeout. After adding one sentence to the tool description ("Strict mode is on: annotate empty arrays and parameters…"), the same prompt passed the gate **first try** (`(dir: string): Promise<string[]>`, `const files: string[] = []`), one tool call, recursive listing + file content, **2.9 s**. Lesson: the gate is only as usable as the prompt guidance around it; Pic's saved functions and `help` paging exist for this reason.
- **How to try it**: `cd owned/pi-extensions && git checkout spike/pic-typescript-tool && cd packages/pi-typescript-tool && npm install && npm test`, then either the `pi -e …` line above or `pi install $PWD` + `/reload`.
- **What works**: Pi's `ExtensionAPI.registerTool` is sufficient — nothing in Pic's mechanism needed the `Agent`-level embedding; the contract-gated, in-process tool is ~300 lines and runs inside a normal Pi session with all other extensions present.
- **What is missing** (deliberately): saved-function registry with `directDependencies`/topological order and the session/project/user scopes (Pic `functions.ts`, `function-storage.ts`); Pi's own tools (`read/grep/find/bash/edit/write`) as capabilities with the run-scoped `AbortSignal.any` + settle-before-return discipline (`pi-tools.ts`); `onUpdate` streaming of partial results; a real sandbox (Node `vm` is not a security boundary — the capability object is the only thing exposed, but a hostile snippet can still spin CPU until the timeout); per-call compiler cost (a fresh `createProgram` with `lib.es2022` each call: ~160 ms for the first four checks in the unit tests, ~40 ms each once the lib is warm; Pic pays the same and caches nothing either); comparison of tool-call counts on a read-heavy task vs Pi's default tools (§9(d).6 second half) — not measured.

## 6. Does execution change the static verdict?

No. The static verdict — do not resurrect Pic as a product; keep the clone frozen; borrow mechanisms — stands, and execution sharpens it:

- Positive: the repo is exactly as healthy as it looked. Clean install (0 vulnerabilities), `check` and all 89 tests green on Node 26 + Chromium 152 without a single code change; the checkpoint store, quarantine, backup fallback, restore, and continue-after-interrupt all behave as documented; running it against the local lane needs only `PIC_MODEL` and an isolated `PI_CODING_AGENT_DIR`.
- Corrections to the static picture: F1 (every crash-restored last run is labelled interrupted, even finished ones — a missing checkpoint after `finish()`), F2 (streaming durability is one provider chunk, not one second, with our adapter), F3 (hard kills leak headless Chromium processes and profiles; there is no supervisor story), plus the two environment facts in §1 (`markdown-it` resolved from cwd; tsx socket path length) that make "run it from an arbitrary workspace" less turnkey than `PIC_SESSION_HTML` suggests. Also new: `@openuidev/lang-core` phones home on `postinstall`, and the all-files-in-parallel `npm run coverage` script wedges on this box (CI's per-file matrix is the only coverage path that works here).
- The spike confirms the single most valuable borrow is cheap: the contract-gated `typescript` tool ports to a Pi extension in an afternoon, and the interesting remaining work is prompt/registry ergonomics (saved functions, guidance against strict-mode traps), not plumbing.

## 7. Addenda

- Artefacts kept under the scratchpad (session-scoped, not committed): `npm-ci.log`, `npm-check.log`, `npm-test.log`, `chrome-count.log`, `kill9/trial-run{1,2,5}.log`, `kill9/session-after-run1.html`, `kill9/session-after-kill9-midstream.html`, `kill9/session-backup-after-kill9-midstream.html`, `kill9/session-clean-final.html`, `kill9/workspace/.pic/session.invalid-2026-09-06T21-37-53-104Z.html`, `spike-live-run{2,3}.log`, the isolated `kill9/pi-agent-dir/` with its `sessions/` JSONL for the pi one-shots.
- Cleanup done: orphaned Chromium processes from the two `kill -9`s were killed by their profile argument; leaked `pic-chrome-*` profiles removed; the spike's `node_modules` removed from the `main` working tree after switching back.
- Not done from §9(d): 2 (`pi-workstation-inference-provider` route — the models.json route was used instead), 5 (`document.title` / `session-capture.py` correlation under niri; needs a non-headless window and a GPU-admission decision), 7 (pi-mono `web-ui` + `server` against a live session).
- Coverage job: see below.

### Coverage job (`npm run coverage`)

`npm run coverage` = `PIC_BROWSER_COVERAGE=1 c8 tsx scripts/run-tests.ts && tsx scripts/check-coverage.ts`, i.e. all 28 regular files in parallel under c8 with Chrome precise coverage — which is *not* what CI does (CI runs one file per job under c8, then merges). Result here: **did not complete**. Under instrumentation the Chrome-backed tests ran 5–10× slower (trade-off/timeline explorers 39.7 s vs 7.8 s plain, `FunctionService filters malformed restored entries` 88 s, OpenUI 62 s), 74/89 tests had passed after 13 min, and `test/session-browser.test.ts` sat for >12 min with one idle headless Chromium (0.2 % CPU) and no output; I terminated the run at 13 m 16 s. c8 printed a partial report from the dumps already written (`All files 96.96 % stmts / 90.52 % branch / 98.1 % funcs / 96.96 % lines`, above the ratchet floors 95/90/98/95 but not comparable because incomplete); `check-coverage.ts` never ran.

Re-running the stuck file alone with CI's exact per-file command (`c8 --reporter=none --temp-directory .coverage/sb tsx --test test/session-browser.test.ts`, `PIC_BROWSER_COVERAGE=1`) passes in **7.5 s** (test body 5.3 s). Verdict: **environment/parallelism, not a product failure** — the combined coverage script with ~15 instrumented Chromes on one box wedges a CDP-heavy test; CI's per-file matrix sidesteps it, and so would `--test-concurrency` in `run-tests.ts`. Treat `npm run coverage` as a "one file at a time" tool on this workstation.
