# surf-cli-go execution report: building, testing and driving the Go fork against a throwaway Brave

Follow-up to the static deep dive (`2026-09-06-surf-cli-go-deep-dive.md`, section 9 "Experiments for a
follow-up session"). Everything here was executed in a sandbox copy; the two contrib checkouts were not modified,
the user's real Brave/Chromium profiles and `/tmp/surf.sock` were never touched, no site was logged into, and no
`libgen_*`, `annas_archive_*`, Upwork or freelancer.com verb was run.

Sandbox root (`$S` below): `/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad`

## 1. TL;DR

- **Go build**: `go build ./...` and `go vet ./...` are clean on go1.27 with the repo's go1.25.6 `go.mod`
  (~100 modules, 287 MB module cache). **The `CGO_ENABLED=0` build that the repo's own scripts prescribe produces a
  `surf-go` that dies at startup** (glazed's help system opens an in-memory sqlite store through cgo
  `mattn/go-sqlite3`). The tracked 52 MB binary was in fact built with `CGO_ENABLED=1` (go1.25.6, dirty tree at
  dc0bd6b). With cgo the CLI works. The host binary (`surf-host-go`, 5.7 MB) is fine without cgo.
- **Go tests**: 169/169 `Test*` functions pass (258 RUN incl. subtests) once two environmental blockers are removed:
  cgo for the `cmd/surf-go` package and a `TMPDIR` short enough for Unix-socket paths (108 bytes). In this
  session's default environment the run shows 150 pass / 2 fail / 1 package fatal, all environmental.
- **Extension build**: `npm ci --ignore-scripts` + `vite build` works for both the fork (vite 7) and upstream
  (vite 8). Neither `package.json` has lifecycle scripts; among installed deps only `esbuild`'s `postinstall`
  (fork) and `puppeteer`'s `postinstall` (upstream, downloads a Chrome) would have run, and neither is needed.
- **Trial A (fork CLI -> fork Go host -> fork extension, Brave 151)**: everything tried works: `tab list`, `js`,
  `page read`, `frame list`, `frame diagnose` (Markdown and JSON), `screenshot`, `tab new/close`, and on a public
  claude.ai page `frame diagnose` plus the unauthenticated error path of `claude sessions`/`claude export`
  (clean exit 1). The extension loads and attaches on current Brave/Chromium 152-line.
- **Trial B (fork CLI as pure client -> upstream v2.18 Node host + upstream extension)**: the socket protocol is
  accepted unchanged (`tab.list`, `page.read`, `frame.list`, `screenshot`, `tab.new/close`, `network`, `cookie`
  answer), but the fork's value-add breaks: `js` with bare `return` is a SyntaxError on 2.18, every structured
  response comes back as prose (`Created tab N: url`), `frame.diagnose` is "Unknown tool", and `claude sessions`
  aborts and leaks the tab it opened. Env var names differ too (`SURF_SOCKET_PATH` vs upstream `SURF_SOCKET`).
- **Trial C (logged-in claude.ai)**: prepared but not executed; exact manual steps for the operator in section 9.
- **Verdict unchanged, sharpened**: keep the archive, do not revive. Execution shows the fork is a coherent
  *stack* (CLI + Go host + 2.6.0-line extension) rather than a client: `surf-go` is useless against upstream's
  host for anything beyond the plain tool table. The claude.ai export verbs need re-probing against the live API
  before any port (section 10).

## 2. Environment

| Item | Value |
|---|---|
| Host | Arch Linux, kernel 7.1.11-arch1-1, x86_64, compositor niri (`NIRI_SOCKET=/run/user/1000/niri.wayland-1.5021.sock`, `WAYLAND_DISPLAY=wayland-1`) |
| Go | `go version go1.27.0-X:nodwarf5 linux/amd64` (`/usr/bin/go`, Arch build); `GOTOOLCHAIN=local` so no 1.25.6 auto-download; `go.mod` says `go 1.25.6` |
| gcc (for cgo) | GCC 16.2.1 20260810 |
| Node / npm | v26.8.1 / 12.0.2 |
| Python | 3.14.7 (`http.server` for the iframe fixture) |
| Browsers | `/usr/bin/brave` = Brave Browser 151.1.93.129 (`/opt/brave-bin/brave`); `/usr/bin/chromium` = Chromium 152.0.7977.64. Brave was used. |
| Fork checkout | `contrib/surf-cli-go` local `main` = 8f30b9e (2026-07-14, the former remote tip); cloned with `git clone --no-hardlinks` to `$S/surf-cli-go-exec` |
| Upstream checkout | `contrib/surf-cli` = 15080ff (v2.18.0); cloned to `$S/surf-cli-upstream` |
| Missing tools | `/usr/bin/time` does not exist (cost me the first timing numbers); `ls`/`cp` are aliased (eza, `cp -i`) |

Pre-existing state worth knowing (read-only observation): the user's real profiles already register a surf host:
`~/.config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json` (extension
`eimbgmhgkoioomogoclciddapelhaajo`, 2026-03-12) and `~/.config/chromium/NativeMessagingHosts/surf.browser.host.json`
(`dkicakjneagcmegjpjfgiplhjnijeoaa`, 2026-05-10), both pointing at `~/.local/share/surf-cli/host-wrapper.sh` ->
`~/.local/share/surf-cli/surf-host-go` (4.8 MB, 2026-05-10, i.e. the **Go host from this fork is already installed
for the real browsers**). `/tmp/surf-host-go.log` shows that host starting on 2026-08-31, 09-03 and 09-04/05.
No `/tmp/surf.sock` existed during this session. To avoid ever colliding with it, all throwaway hosts below used a
private socket.

## 3. Sandbox layout

```
$S/surf-cli-go-exec/        git clone of the fork (8f30b9e), node_modules + dist built here
$S/surf-cli-upstream/       git clone of upstream v2.18.0, node_modules + dist built here
$S/gomodcache, gocache      GOMODCACHE / GOCACHE (287 MB / 397 MB)
$S/npm-cache, npm-logs      npm cache and logs (nothing written to ~/.npm)
$S/bin/surf-go              CGO_ENABLED=0 CLI (51,337,160 B) - does not start, see 4
$S/bin/surf-go-cgo          CGO_ENABLED=1 CLI (53,428,696 B) - used for all trials
$S/bin/surf-host-go         CGO_ENABLED=0 Go host (5,729,675 B)
$S/www/                     iframe fixture (index.html -> inner/level1.html -> inner/level2.html, + srcdoc + about:blank)
$S/run/                     cwd for hosts and CLI; surf.sock lives here (relative path, see 7)
$S/run/host-wrapper-go.sh   wrapper for the fork Go host (SURF_SOCKET_PATH=surf.sock, SURF_HOST_LOG=$S/run/surf-host-go.log)
$S/run/host-wrapper-node.sh wrapper for upstream host.cjs (SURF_SOCKET=surf.sock, SURF_TMP=$S/run/surf-tmp)
$S/run/manifest-*.json      native-messaging manifests (Go host / Node host / Node host + upstream ext id)
$S/xdg-config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json   the manifest Brave actually reads (see 7)
$S/brave-profile/           throwaway user-data-dir A (fork extension)     $S/brave-profile-b/  throwaway B (upstream extension)
$S/go-build.log, npm-ci.log, ext-build.log, trial-a.log, trial-a-extras.log, trial-b.log, trial-b2.log, trial-b3.log, trial-b4.log
```

## 4. Go build results

Commands (from `$S/surf-cli-go-exec/go`, `GOFLAGS=-mod=mod GOTOOLCHAIN=local GOMODCACHE=$S/gomodcache GOCACHE=$S/gocache`):

```
CGO_ENABLED=0 go build ./...                                   # ok, no output
CGO_ENABLED=0 go build -trimpath -o $S/bin/surf-go ./cmd/surf-go          # 9.9 s wall (warm cache), 51.3 MB
CGO_ENABLED=0 go build -trimpath -o $S/bin/surf-host-go ./cmd/surf-host-go # 0.4 s, 5.7 MB
CGO_ENABLED=1 go build -trimpath -o $S/bin/surf-go-cgo ./cmd/surf-go      # 30 s wall (compiles sqlite3 C), 53.4 MB
go vet ./...                                                   # clean (only "go: downloading" noise)
```

Module download volume: 287 MB in `GOMODCACHE` (glazed drags chroma, bubbletea, excelize, mongo-driver, sqlite3, ...).
The `go mod download`/`go build ./...` wall times were lost to the missing `/usr/bin/time`; the whole
download+build+vet+test job finished inside a few minutes.

**Finding: the CGO_ENABLED=0 CLI is dead on arrival.**

```
$ $S/bin/surf-go --help
{"level":"fatal","error":"failed to create tables: failed to create sections table: Binary was compiled with
 'CGO_ENABLED=0', go-sqlite3 requires cgo to work. This is a stub", ... "message":"Failed to create in-memory store"}
exit=1
```

`cmd/surf-go/main.go:685` calls `help.NewHelpSystem()` (glazed v1.0.1), which backs the help store with
`github.com/mattn/go-sqlite3 v1.14.32` (`go.mod:59`, indirect). The deep dive's claim "Builds set `CGO_ENABLED=0` ...
producing a ~50 MB static binary" is only true for the *host* (`install_command.go`, `build-go-host-binaries.cjs`
build `surf-host-go`); nothing in the repo builds the CLI, and `owned/test-capabilities` runs it via `go run`, i.e.
with cgo on by default. `go version -m go/surf-go` on the tracked blob confirms `CGO_ENABLED=1`, `go1.25.6`,
`vcs.revision=dc0bd6b`, `vcs.modified=true`. Consequently the tracked binary is **not reproducible** from any commit
(dirty tree, older toolchain); sha256 of my cgo build `2045d135...` vs tracked `27a56fbc...` differ as expected.

With cgo the CLI works (`$S/bin/surf-go-cgo --help` prints the glazed help with the `annas-archive`, `chatgpt`,
`claude`, `freelancer`, `gmail`, `kagi`, `libgen`, `upwork`, ... groups).

## 5. Go test results

`go test -count=1 ./...` in the session's default environment (`CGO_ENABLED=0`, `TMPDIR=/home/tryinget/.local/state/pi-quests/tmp`):

| Package | Result | Reason |
|---|---|---|
| `cmd/surf-go` | **FAIL (fatal before any test)** | same sqlite/cgo fatal as above, from `newRootCommand(help.NewHelpSystem())` in `integration_test.go` |
| `internal/cli/commands` | 2 FAIL: `TestOpenOwnedTabClosesTabAfterReadinessFailure`, `TestFetchUpworkJobsRetriesWithFreshOwnedTab` | `listen unix .../TestOpenOwnedTab...2768604206/001/surf.sock: bind: invalid argument`: the `t.TempDir()` socket path is 112 bytes, over the 108-byte `sun_path` limit |
| 9 other packages | ok | |
| totals | PASS=150 FAIL=2 (+1 package fatal) | |

Re-run with the two blockers removed, `CGO_ENABLED=1` and a short private `TMPDIR` (`unshare -rm` + tmpfs on
`/mnt`, so nothing was written outside the sandbox):

```
ok  gohost/cmd/surf-go 1.863s   ok  cmd/surf-host-go   ok  internal/cli/commands   ok  internal/cli/transport
ok  internal/host/config   ok  nativeio   ok  pending   ok  providers 1.505s   ok  router   ok  socketbridge   ok  installer
RUN=258 PASS=169 FAIL=0 SKIP=0
```

Same run with `CGO_ENABLED=0` and short TMPDIR: everything ok except `cmd/surf-go` (cgo fatal). So: **169 test
functions, all green, but only with cgo and a short TMPDIR**; the repo never documents either requirement (and had
no Go CI job to notice).

Upstream/fork vitest suites were **not** run: the fork's `test/` includes native-host tests that bind the default
`/tmp/surf.sock`, which would be a write outside the sandbox and a collision risk with the real host.

## 6. Extension build notes (npm lifecycle scripts)

`npm ci --ignore-scripts` (npm cache/logs redirected into `$S`): fork 289 packages in 6 s, upstream 330 packages in
10 s. Both `package.json` files have **no** `preinstall`/`install`/`postinstall`/`prepare` entries (fork
`scripts:` dev/build/check/lint/test/build:go-host/install:native/...; upstream adds `test:e2e:chrome`).

Scan of every installed `node_modules/**/package.json` for install-time scripts:

| Tree | Would have run without `--ignore-scripts` | Verdict |
|---|---|---|
| fork | `esbuild` `postinstall: node install.js` (validates/downloads the platform binary; `@esbuild/linux-x64` was already installed as an optional dep, so `install.js` would only run `validateBinaryVersion`) | not needed: `vite build` succeeded without it |
| fork | `resolve/test/resolver/multirepo` `postinstall: lerna bootstrap` (a test fixture inside `resolve`, never executed by npm) | irrelevant |
| upstream | `puppeteer` `postinstall: node install.mjs` (downloads Chrome for Testing into `~/.cache/puppeteer`, only for `test/e2e/real-chrome.mjs`) | deliberately skipped: not needed for `native/host.cjs` or `vite build`, and it writes outside the sandbox |
| both | ~60 `prepublish`/`prepare` entries in deps (`tinyexec`, `rollup`, `eventsource`, `path-to-regexp`, `lightningcss` `prepare: patch-package`, ...) | `prepare`/`prepublish` do not run for registry dependencies; ignored |

Builds:

```
$ cd $S/surf-cli-go-exec && npx --no-install vite build      # vite v7.3.1, 12 modules, 333 ms
dist/service-worker/index.js 96.88 kB, content/accessibility-tree.js 38.79 kB, content/visual-indicator.js 8.45 kB,
options/options.js, manifest.json (version 2.6.0), icons; dist = 612 KB; FRAME_DIAGNOSE present in the service worker.
$ cd $S/surf-cli-upstream && npx --no-install vite build     # vite v8.2.2, 13 modules, 110 ms
dist/service-worker/index.js 121.58 kB, content/index.js 48.90 kB, ...; manifest.json version is still "2.6.0"
```

Oddity: upstream v2.18.0 still ships `manifest.json` `"version": "2.6.0"`; only `package.json` was bumped.
Warning in both builds: `src/native/port-manager.ts` is both statically and dynamically imported (harmless).

## 7. Throwaway profile setup (what actually works on Linux)

Two things in the task brief / deep dive turned out to be wrong on Linux and are worth recording:

1. **`--user-data-dir/NativeMessagingHosts` is not consulted.** Chromium resolves user-level native-messaging
   manifests from the *default* config location (`chrome::DIR_USER_NATIVE_MESSAGING` =
   `$XDG_CONFIG_HOME/BraveSoftware/Brave-Browser/NativeMessagingHosts`, honouring `CHROME_CONFIG_HOME`), regardless
   of `--user-data-dir`. With the manifest under `$S/brave-profile/NativeMessagingHosts/` the extension loaded but
   `connectNative` silently found nothing (no host spawned, no socket, nothing in `--enable-logging=stderr --v=1`).
   Fix used: launch the throwaway Brave with `CHROME_CONFIG_HOME=$S/xdg-config XDG_CONFIG_HOME=$S/xdg-config`
   and put the manifest at `$S/xdg-config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json`.
   The real `~/.config/BraveSoftware` is never read by that instance.
2. **The sandbox path is too long for a Unix socket** (`$S` is 119 bytes, limit 108 incl. filename). Both hosts
   accept a relative path (`net.Listen("unix","surf.sock")` in `socketbridge/listener_unix.go`, `server.listen({path})`
   in `host.cjs`), so the wrappers `cd $S/run` and export `SURF_SOCKET_PATH=surf.sock` (fork) or `SURF_SOCKET=surf.sock`
   (upstream); the CLI runs from `$S/run` with `--socket-path surf.sock`.

Other setup facts:

- Unpacked-extension id is `sha256(absolute dist path)[:32]` mapped `0-9a-f -> a-p`. Computed
  `bhmdgplfliclaohefihkocapieknmedk` for `$S/surf-cli-go-exec/dist` and `eepfdgilllkiffgcfcchgmghnmhemcoj` for
  `$S/surf-cli-upstream/dist`; both matched what Brave wrote to `Default/Preferences` (`location: 8`).
- `--load-extension` still works in Brave 151 (it is disabled in branded Google Chrome since ~137).
- Forcing `--ozone-platform=wayland` made the first instance exit silently after ~30 s
  (`'--ozone-platform=wayland' is not compatible with Vulkan` in the log, no window ever mapped). Letting Brave pick
  the backend gave a normal window (`niri msg --json windows` listed it under `app_id brave-browser` with the fixture
  title, alongside the user's own Brave window, PID 3594461, which was never touched).
- Native-messaging wrapper pitfall: my first Node wrapper redirected stdout into a log file. stdout *is* the native
  messaging channel, so `HOST_READY` frames landed in the log, the extension reconnected every 5 s and no socket
  appeared. Redirect stderr only.
- Launch line used (profile A / fork stack):

```
CHROME_CONFIG_HOME=$S/xdg-config XDG_CONFIG_HOME=$S/xdg-config brave --user-data-dir=$S/brave-profile \
  --load-extension=$S/surf-cli-go-exec/dist --no-first-run --no-default-browser-check http://127.0.0.1:44089/index.html
```

- Host log after launch (`$S/run/surf-host-go.log`): `Host starting... Socket server listening on surf.sock  Sent HOST_READY to extension`.
- Shutdown: `kill -TERM <main pid>` after verifying `/proc/<pid>/cmdline` contains the throwaway `--user-data-dir`;
  the user's real Brave (48 processes) stayed up throughout; `/tmp/surf.sock` never appeared.

## 8. Trials

All CLI invocations: `cd $S/run; $S/bin/surf-go-cgo <verb> ... --socket-path surf.sock`. Full transcripts in
`$S/trial-*.log`.

### 8a. Trial A: `surf-go` -> fork Go host -> fork extension (Brave 151), iframe fixture

Fixture `http://127.0.0.1:44089/index.html`: a same-origin `<iframe>` (`level1.html`) containing another
(`level2.html`), a `sandbox="allow-scripts"` `srcdoc` frame, and an `about:blank` frame that the parent writes into
(the "artifact widget" case from the R8 ticket).

| Command | Observed | Verdict |
|---|---|---|
| `tab list --output json` | 3 tabs (one per launch, session restore), ids like `1193190378`, `windowId 1193190375` | ok, exit 0 |
| `js 'return document.title'` | `content: '"surf-go frame diagnose fixture (top)"'` (YAML default) | ok |
| `js 'return {url: location.href, iframes: document.querySelectorAll("iframe").length}' --output json` | `{"iframes": 3, "url": ...}` | ok, objects become rows |
| `page read --args-json '{"filter":"interactive"}' --output json` | one `content` row; the 2.6.0-line snapshot includes the inline `<script>` source in the page text | ok (quirk noted) |
| `frame list --output json` | 4 CDP frames: top, level1, level2 (parent level1), blankframe; **srcdoc frame absent** | ok |
| `frame diagnose` | Markdown report, see below | ok |
| `frame diagnose --with-glaze-output --output json` | rows with `kind: summary / dom_iframe / extension_frame / cdp_frame / warning` | ok |
| `screenshot --output json` | `{base64: iVBORw0..., height: 1031, width: 936, screenshotId: screenshot_1_...}` | ok |
| `tab new --args-json '{"url":"https://claude.ai/"}' --output json` | `{"success": true, "tabId": 1193190380, "url": "https://claude.ai/"}` | ok |
| `tab close --tab-id 1193190380 --output json` | `{"success": true, "tabId": 1193190380}` | ok |

`frame diagnose` on the fixture (abridged):

```
## DOM Iframes            3 entries: f-level1 (src level1.html, rect 604x304), f-sandbox (sandbox=allow-scripts, src ""),
                          f-blank (src about:blank, allow=clipboard-read)
## Extension Frames       5 entries (chrome.webNavigation): 0 top [reachable], 7 level1 [reachable], 8 about:srcdoc
                          [contentScriptReachable:false "Could not establish connection. Receiving end does not exist."],
                          9 about:blank [unreachable, same error], 14 level2 (parent 7) [reachable]
## CDP Frames             4 entries: top, level1, level2, blankframe   (no srcdoc frame)
## Warnings               DOM iframe count (3) differs from extension child-frame count (4)
```

So the three inventories disagree in exactly the ways the tool was built to expose: the content script
(`all_frames: true`, `document_start`, no `match_about_blank`/`match_origin_as_fallback`) is not injected into
`srcdoc`/`about:blank` frames, `chrome.webNavigation` counts the nested level2 as a child (hence 4 vs 3), and CDP
`Page.getFrameTree` does not list the srcdoc frame at all. The `rect` values are rendered as Go `map[...]` in the
Markdown mode (cosmetic bug in `frame_diagnose.go`).

### 8a'. Trial A extras: public claude.ai page, no login

`tab new` to `https://claude.ai/` lands on `https://claude.ai/login` ("Sign in - Claude"), 5 DOM iframes (4 hCaptcha
frames + one blank 1x1). `frame diagnose --tab-id 1193190380`:

- DOM: 5 iframes (hcaptcha `checkbox-invisible` x2, `challenge` x2, one src-less 1x1).
- Extension frames: 6 (top + about:blank + 4 hcaptcha), **all hcaptcha frames reachable** by the content script
  (cross-origin but `<all_urls>`), the about:blank one not.
- CDP frames: **2** (top + about:blank). The cross-origin hcaptcha frames are out-of-process iframes and invisible to
  `Page.getFrameTree` on the tab's own target; warning "DOM iframe count (5) differs from CDP child-frame count (1)".

This is the claude.ai-artifact class of problem from the deep dive reproduced on a public page: the CDP view is the
least complete of the three.

Unauthenticated error path (no cookies, no login):

```
$ surf-go claude sessions --limit 1
Error: Error: no chat-capable organization found on this account
    at resolveOrg (<anonymous>:33:20) ... (line 32, column 21)
>   return chat.organization.uuid;
[exit=1]
$ surf-go claude export 00000000-0000-4000-8000-000000000000 --out $S/claude-export-test      # same error, exit 1
```

The verb opened its own claude.ai tab, ran the embedded `claude_sessions.js`, got an anonymous `/api/bootstrap`,
reported the mapped user line (the fork's exception line mapping at work) and closed the owned tab (`tab list`
afterwards showed only the fixture tabs). Nothing was written to `$S/claude-export-test`.

### 8b. Trial B: `surf-go` as pure client -> upstream v2.18 Node host + upstream extension

Setup: profile B, `$S/surf-cli-upstream/dist` (ext id `eepfdgil...`), manifest -> `host-wrapper-node.sh` ->
`/usr/bin/node $S/surf-cli-upstream/native/host.cjs` with `SURF_SOCKET=surf.sock`, `SURF_TMP=$S/run/surf-tmp`.
Host log (`$S/run/surf-tmp/surf-host.log`): `Host starting... Oracle adoption: 0 job(s) ... Sent HOST_READY ...
Received from extension: EXTENSION_HELLO ... Browser identity connected: 05d92139-... epoch=...`.

Raw frames captured with `--debug-socket` (request shape is byte-for-byte what upstream expects):

```
client->host {"id":"go-1788730980318447638","method":"execute_tool","params":{"args":{},"tool":"tab.list"},"type":"tool_request"}
host->client {"type":"tool_response","id":"go-...","result":{"content":[{"type":"text","text":"[\n  {\n    \"id\": 1429724128, ..."}]}}
```

| Command | Observed against upstream 2.18 | Verdict |
|---|---|---|
| `tab list --output json` | rows with id/title/url/active/windowId (host log: `SESSION {"event":"admission"...} ... scheduler acquired scope browser-read ... completed elapsedMs 2`) | **works** |
| `js 'return document.title'` | `Error: SyntaxError: Unexpected token 'return'`, exit 1 | **breaks** |
| `js 'document.title'` / `js '(() => ({...}))()' --output json` | `"Sign in - Claude"` / `{"n": 4, "title": ...}` | works (expression form only) |
| `tool-raw --tool js --args-json '{"code":"document.title"}'` | `{"content": "\"Sign in - Claude\""}` | works |
| `page read --args-json '{"filter":"interactive"}' --output json` | `button "Top button" [e1]\n\n[Viewport: 936x947]\n\n--- Page Text --- ...` (2.18 snapshot format, refs + viewport) | works |
| `frame list --output json` | 4 frames, same shape as trial A | works |
| `frame diagnose` | `Error: Unknown tool: frame.diagnose` (host log: request outcome error, elapsedMs 0) | **breaks** (fork-only tool) |
| `screenshot --output json` | `{"content": "Screenshot captured (936x947) - ID: screenshot_1_..."}` (prose, no base64) | degraded |
| `tab new --args-json '{"url":...}' --output json` | `{"content": "Created tab 1429724130: http://..."}` (prose; the fork returns `{success,tabId,url}`) | degraded: id must be parsed from text |
| `tab close --tab-id N --output json` | `{"content": "Closed tab N"}` | works (prose) |
| `network list --output json` | `{"content": "No network requests captured"}` | works |
| `cookie list --output json` | full cookie rows for the anonymous claude.ai tab (`anthropic-device-id`, `activitySessionId`, ...) | works (and shows how freely cookies leave the browser) |
| `tool-raw --tool session.info` | `Error: session name must be 1-64 characters ...` | 2.18 sessions API needs args surf-go has no verb for |
| `tool-raw --tool doctor` | `Error: Unknown tool: doctor` (`doctor` is CLI-side upstream) | n/a |
| `claude sessions --limit 1` | `Error: missing structured tab creation response`, exit 1; **the tab it created (url "") stayed open** | **breaks and leaks a tab** |
| `wait dom`, `wait element`, `console read`, `network stats`, `click` | not completed: the extension stopped answering after a Brave relaunch (all requests `abandoned` in the host log) and the instance was lost to my own tool timeout; see caveats | untested |
| control: `SURF_SOCKET=surf.sock node native/cli.cjs tab.list --json` | first call after host start: `Error: Request timed out (60s)` (host log: `hard-timeout`, the extension's reply arrived as `unknown id=1` right after); every later call 2 ms | upstream stack itself has a first-request warm-up hang in this ad-hoc setup |

Why the breaks (verified in source):

- **`return` semantics**: fork extension (`src/service-worker/index.ts:1938`) always wraps the code in
  `(async () => {\n'use strict';\n<code>\n})()`, so bare `return` is legal and every embedded extractor
  (`scripts/*.js`, `claude_sessions.js`, `kagi_search.js`, ...) relies on it. Upstream 2.18
  (`src/service-worker/index.ts:2233-2238`) first runs `codeWithExpressionReturn(code)` (expression mode) and only
  falls back to the raw IIFE `if (result.exceptionDetails && !scriptParses(body))`; a top-level `return` parses as a
  script, so the fallback never triggers and the SyntaxError is returned.
- **Structured vs prose results**: both extensions return `{success: true, tabId, url}` for `tab.new`
  (`fork index.ts:2311`, `upstream index.ts:3062`). The Go host forwards that object; upstream's Node host formats
  it through `host-helpers.cjs:408` `text(\`Created tab ${result.tabId}: ${result.url}\`)` (the fork's own
  `native/host-helpers.cjs:366` does the same). So `surf-go`'s "structured rows" depend on the **Go host**, not on the
  extension patch; running the fork's extension with the Node host would not help.
- **`frame.diagnose`**: only in `go/internal/host/router/toolmap.go` and the fork's service worker.
  Static diff of tool names: fork host knows 98, upstream host 145; fork-only = `frame.diagnose`, `up/down/left/right`.
- **`claude sessions` tab leak**: `kagi_search.go:333` (shared owned-tab helper) requires the structured `tabId`;
  when it gets prose it errors *after* `tab.new` succeeded and before registering the tab for cleanup.
- **Env var drift**: fork/CLI use `SURF_SOCKET_PATH` (`config/socket_path.go`, `native/socket-path.cjs` in the fork);
  upstream 2.18 uses `SURF_SOCKET`, plus `SURF_TMP` and `SURF_LISTEN`. `surf-go --socket-path` sidesteps this, but
  the fork's wrappers/docs would silently talk to the wrong socket.
- **surf-go CLI quirks seen** (host-independent): `wait` and `console` are groups (`wait dom|element|network|url`,
  `console read|stream`), so `surf-go wait 1` and `surf-go console list` fail with `unknown flag: --output`; the
  `--tab-id` flag rejects an empty string with a full help dump.

Caveats on trial B stability: of five throwaway Brave launches, two (A1 with forced Wayland ozone; B1 after ~3 min,
four `TARGET_EVENT`s then `stdin ended`) exited on their own with no crash report, no journal entry and only
viz/GPU warnings in their logs; B2 died when my Bash tool's 3-minute limit killed its process group; after that
relaunch the upstream extension answered nothing (`abandoned` x5). I did not chase this further; the fork stack (A2,
A3) ran until I terminated it.

### 8c. Trial C: logged-in claude.ai (not executed)

Everything up to the login is in place and proven: profile A + `manifest-go.json` + fork stack, `claude sessions`
reaches `/api/bootstrap` and `claude export` reaches the same resolver. What is missing is a claude.ai session in
the throwaway profile, which I was told not to create. Section 9 has the exact remaining steps.

## 9. What the operator must do by hand for the claude.ai trials

The scratch dir is session-specific; if it is gone, redo sections 3-7 (about 5 minutes) or copy `$S/bin`,
`$S/surf-cli-go-exec/dist`, `$S/run` and `$S/xdg-config` somewhere with a path under ~90 bytes (then absolute socket
paths work and the `cd`/relative-path trick is unnecessary).

```bash
S=/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad
# 1. make sure the manifest points at the fork Go host and its extension id
/bin/cp -f $S/run/manifest-go.json $S/xdg-config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json
# 2. start the throwaway Brave (NOT your real profile) with the fork extension
CHROME_CONFIG_HOME=$S/xdg-config XDG_CONFIG_HOME=$S/xdg-config brave --user-data-dir=$S/brave-profile \
  --load-extension=$S/surf-cli-go-exec/dist --no-first-run --no-default-browser-check https://claude.ai/login &
# 3. in THAT window: log in to claude.ai by hand (hCaptcha + e-mail code / SSO). Do not import cookies from the real profile.
#    Open one conversation that contains an artifact and leave its tab open. Note nothing else is needed.
# 4. verify the stack, find the artifact tab id
cd $S/run
$S/bin/surf-go-cgo tab list --socket-path surf.sock --output json
# 5. frame diagnose on the artifact tab (compare DOM vs extension vs CDP inventories; expect the artifact iframe to be
#    an about:blank/srcdoc-style frame that is content-script-unreachable and possibly absent from the CDP tree)
$S/bin/surf-go-cgo frame diagnose --tab-id <artifact tab id> --socket-path surf.sock
$S/bin/surf-go-cgo frame diagnose --tab-id <artifact tab id> --socket-path surf.sock --with-glaze-output --output json > $S/frame-diagnose-claude.json
# 6. list conversations (internal API: /api/bootstrap -> chat_conversations_v2, paged) and export one
$S/bin/surf-go-cgo claude sessions --limit 3 --socket-path surf.sock
$S/bin/surf-go-cgo claude sessions --limit 3 --socket-path surf.sock --with-glaze-output --output json
$S/bin/surf-go-cgo claude export <uuid> --out $S/claude-export --socket-path surf.sock        # add --include-thinking if wanted
/bin/ls -la $S/claude-export/<uuid>/ $S/claude-export/<uuid>/artifacts/
#    expected: conversation.md, conversation.json, meta.json, artifacts/* rebuilt from create_file/str_replace replay;
#    compare artifacts/* with the artifact as shown in the UI, and diff conversation.json keys against what
#    scripts/claude_export.js expects (tree=True&rendering_mode=messages&render_all_tools=true) to size the API drift.
# 7. shut down: close that Brave window (or kill -TERM its main pid, verify /proc/<pid>/cmdline first),
#    then delete $S/brave-profile (it now holds a live claude.ai session) and $S/claude-export when done.
```

What to record: whether `/api/bootstrap` still exposes `memberships[].organization.capabilities` containing
`chat` (the resolver error seen in 8a' is exactly that check failing on an anonymous bootstrap), whether
`chat_conversations_v2?limit=100&offset=` still pages, whether `render_all_tools=true` still returns `create_file` /
`str_replace` tool blocks (artifact reconstruction depends on them), and the wall time of `export` (the 40,000-char
base64 chunking should show as several `js` round trips in `--debug-socket`).

## 10. Protocol-compatibility findings (fork CLI vs upstream v2.18 host), condensed

1. Wire protocol unchanged: NDJSON over a Unix socket, `{"type":"tool_request","id","method":"execute_tool","params":{"tool","args"}}`
   -> `{"type":"tool_response","id","result":{"content":[{"type":"text","text"}]}}` or `error:{content:[...]}`.
   Upstream additionally logs `SESSION {...}` admission/scheduler/lane events per request and treats each
   connection as principal `local`.
2. Every entry of `surf-go`'s plain tool table that exists upstream works (tab, page, frame list, screenshot, network,
   cookie, navigation). `frame.diagnose` and the `up/down/left/right` scroll shortcuts do not exist upstream.
3. Result *shape* differs for every tool whose Node formatter emits prose: `tab.new`, `tab.close`, `screenshot`
   (no base64!), `wait`, etc. `surf-go`'s glazed rows then contain one `content` string. Only the Go host forwards
   structured results.
4. `js` semantics differ (bare `return` vs expression mode); all 29 embedded extractors and the claude/kagi/gmail
   verbs assume the fork's IIFE wrapper. A one-line client-side fix (wrap the code in `(async()=>{...})()` before
   sending) would make them run on 2.18.
5. Upstream's session model (`session.ensure`, `SURF_SESSION`, lanes) is invisible to `surf-go`; it works because
   2.18 still admits lease-less local requests (`skipLease: true`), and upstream's own `--json` / `--llm-context`
   outputs are the supported way to get structure.
6. Env var names: `SURF_SOCKET_PATH` (fork) vs `SURF_SOCKET` (upstream). `HOST_READY` payloads differ
   (fork adds `runtime`/`socketPath`); harmless.
7. Upstream 2.18 first-request hang (60 s) after host start was reproducible twice in this setup; the fork's Go host
   answered its first request in 4 ms. Not root-caused; possibly the service worker's warm-up before the debugger
   attaches.

## 11. Updated recommendation

Execution does **not** change the static verdict (keep the archive, do not revive) but changes the reasoning and
some of the "borrow as code" list:

- The fork is a **three-piece stack** (Go host + 2.6.0-line extension + CLI), not a drop-in client. Any plan that
  says "use surf-go as a client against upstream" is dead: 3 of its 5 selling points (structured rows, `js` with
  `return`, `frame diagnose`) live in the Go host or the extension patch, and the claude/kagi/gmail verbs break
  outright against 2.18. `owned/test-capabilities` must either pin the whole fork stack (rebuilt from source with
  `CGO_ENABLED=1`, plus the rebuilt `dist/`) or migrate to upstream `surf --json` + `session.ensure`. Given upstream's
  weekly releases and the first-request hang being the only rough edge I hit, migrate.
- The Go host's justification (Snap) is absent here, yet **it is already installed for the real Brave and Chromium
  profiles** (section 2). Whoever set that up in March/May should decide whether the real profiles should instead run
  upstream's host; the current manifests point at a May build of `surf-host-go` from this fork.
- Worth borrowing, now with evidence: `frame diagnose` (the three-inventory report was correct on both the fixture
  and claude.ai's login page and immediately shows OOPIF/srcdoc blind spots), the owned-tab pattern (it cleaned up
  correctly in trial A, and its failure mode in trial B is a good test case), and the `js` exception line mapping
  (the `resolveOrg (<anonymous>:33:20)` + quoted source line output is exactly what an agent needs).
- Before porting `claude_sessions.js`/`claude_export.js`, run section 9 once: the anonymous run proves the transport
  and the org-capability check, but nothing about `chat_conversations_v2` or `render_all_tools` on today's API.
- Reproducibility hygiene if anyone rebuilds: use cgo for the CLI, a short `TMPDIR` for tests, `GOTOOLCHAIN=local`
  works with go1.27, and never run the tracked `go/surf-go` (built from a dirty tree, unreviewable).
- Do not run the fork's vitest suite on a machine with a live surf host: it binds the default `/tmp/surf.sock`.

## 12. Cleanup state at the end of the session

Throwaway Brave instances terminated (verified `pgrep -f "user-data-dir=$S"` = 0), fork Go host and upstream Node
host exited with them, fixture `http.server` stopped. Nothing was written outside `$S` except this file. The user's
Brave (`pgrep -x brave` = 48 processes) and Chromium windows were untouched. `$S/brave-profile*` contain no logins
(only anonymous claude.ai cookies from the login page visit) and can be deleted with the scratch dir.
