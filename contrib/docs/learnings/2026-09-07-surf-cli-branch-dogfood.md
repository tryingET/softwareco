# surf-cli branch dogfood: `feat/site-independent-mechanisms` against real pages, quick wins implemented

Follow-up to `2026-09-06-surf-cli-contribution-branch.md`. The 8-commit branch was cloned into scratch, built,
loaded into a throwaway Brave with the branch's own Node host on a private socket, and driven the way an agent
would drive it against public pages. Findings became a ranked backlog; the quick wins were implemented as five
more PR-shaped commits (branch is now 13 commits on top of v2.18.0 `15080ff`), verified (lint, tsc, 878 unit
tests, real-Chrome e2e), re-dogfooded, and pushed into `contrib/surf-cli` (`feat/site-independent-mechanisms`)
with the patch series regenerated. Nothing in `contrib/` was committed.

## 1. TL;DR

- All eight branch mechanisms work on real pages as designed: login bounce (GitHub), 404 (python.org, GitHub),
  `frame.diagnose` on YouTube/example.com/sandbox/srcdoc/shadow-DOM frames, `extract` on GitHub releases, Hacker
  News and PyPI (rows, Markdown, `--json`, zero rows, `--empty-text`, `--allow-empty`, transient retry, `--tab-id`),
  `js --options`, `js --file` statement scripts, and the native value setter on npmjs.com's React search box.
- Two upstream bugs found and fixed on the branch: (1) the native host stopped draining its stdin buffer after an
  `EXTENSION_HELLO`/`TARGET_EVENT` frame, so a reply sharing the chunk waited for the next message (the "first
  request hangs 60 s" seen in the previous session and again in the upstream control run); (2) `chrome.debugger`
  errors reached users as a JSON blob (`{"code":-32000,"message":"Inspected target navigated or closed"}`).
- Three branch gaps found and fixed: `frame.diagnose` missed every iframe inside an open shadow root (MDN: "0
  iframes" against 6 extension frames), never matched `srcdoc`/`about:blank` frames to their CDP frame although CDP
  names them after the iframe `name`/`id`, and did not say that out-of-process iframes are simply absent from the
  tab's CDP tree; error codes were not printed in text mode and `--json` errors were prose on stderr; transport
  keys (`id`, `_resolvedWindowId`) leaked into `page.readiness`/`frame.diagnose`/`extract --json`.
- One unexplained upstream/browser behaviour, measured but not fixed: `js` (CDP `Runtime.evaluate`) on a tab that is
  not the active tab stalls for seconds up to the 60 s client deadline in Brave 151 (25 s, 47 s, 60 s here; 31 s and
  34 s with the pristine upstream 2.18.0 stack in a fresh profile), while the same call on a freshly opened active
  tab takes 0.8 s and every content-script tool (`page.read`, `page.readiness`, `frame.diagnose`) answers in 50 ms.
  `extract` is unaffected because its owned tab is active. Documented; maintainer question added.
- Recommendation: upstream in this order: stdin-frames fix, CDP error fix, `js --file` CSP fix (three independent
  one-commit bug fixes), then native setter, readiness, frame.diagnose, extract+options+docs.

## 2. Environment

| Item | Value |
|---|---|
| Host | Arch Linux 7.1.11-arch1-1, niri (`WAYLAND_DISPLAY=wayland-1`), load average 1.7-2.3 |
| Node / npm | v26.8.1 / 12.0.2 |
| Browser used | `/usr/bin/brave` = Brave 151.1.93.129, throwaway profiles only (`--user-data-dir` under scratch, `--load-extension`, native-host manifest under a private `CHROME_CONFIG_HOME`/`XDG_CONFIG_HOME`) |
| Chromium 152.0.7977.64 | attempted as a second control; `/usr/bin/chromium` is an ELF launcher that dropped `CHROME_CONFIG_HOME`/`XDG_CONFIG_HOME`, so the extension loaded but never found the host manifest. Not pursued. |
| Branch clone | `$S/surf-dogfood` (clone of `contrib/surf-cli` branch `feat/site-independent-mechanisms`, start `008f3ab`, end `dfc7408`) |
| Upstream control | `$S/surf-cli-upstream` (v2.18.0 `15080ff`, built in the previous session), fresh profile `$S/brave-profile-c`; the previous session's `brave-profile-b` exits by itself after ~3 min (it carries a persisted `--ozone-platform=wayland` flag) |
| Pinned Chrome for e2e | 152.0.7977.54 in `$S/puppeteer-cache` (`PUPPETEER_CACHE_DIR`) |
| `$S` | `/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad` |
| Logs | `$S/dogfood/dogfood.log` (every `surf` call: time, args, exit, wall ms, output bytes, output; 123 calls), `$S/dogfood/upstream-control*.log`, `$S/dogfood/verify-{baseline,after}.log`, `$S/dogfood/run/surf-tmp/surf-host.log` |

Rules followed: `npm ci --ignore-scripts` (only `puppeteer`'s `postinstall` was skipped; it downloads Chrome and is
not needed because the pinned build already exists), no logins, public pages only, the user's Brave/Chromium
profiles and `/tmp/surf.sock` untouched (`pgrep -x brave` for the user's browser stayed at ~49; the throwaway
instances were killed by PID after checking `/proc/<pid>/cmdline` for the scratch profile path). Setup gotchas
from `2026-09-06-surf-cli-go-execution.md` §7 all held (manifest under `CHROME_CONFIG_HOME`, relative `surf.sock`
from `$S/dogfood/run`, stderr-only wrapper, no forced ozone flag). One new gotcha: after rebuilding `dist/`, a
restart of the same profile kept the old service worker (unpacked extension, unchanged manifest version); a fresh
profile directory was needed to load the new bundle.

Setup commands (abridged; full lines in `$S/dogfood/sf`, `host-wrapper.sh` and the manifest):

```bash
git clone -b feat/site-independent-mechanisms contrib/surf-cli $S/surf-dogfood
cd $S/surf-dogfood && npm ci --ignore-scripts --cache $S/npm-cache && npm run build       # 2.8 s / 0.7 s
EXTID=$(sha256 of "$S/surf-dogfood/dist" | first 32 hex | a-p)                            # cffjkmioeddadbhjoeddkhognjmkpbfa
# manifest -> $D/xdg-config/BraveSoftware/Brave-Browser/NativeMessagingHosts/surf.browser.host.json (path = $D/run/host-wrapper.sh)
CHROME_CONFIG_HOME=$D/xdg-config XDG_CONFIG_HOME=$D/xdg-config setsid -f brave --user-data-dir=$D/brave-profile \
  --load-extension=$S/surf-dogfood/dist --no-first-run --no-default-browser-check about:blank
# every call: cd $D/run; SURF_SOCKET=surf.sock node $S/surf-dogfood/native/cli.cjs <args>   (wrapper: $D/sf)
```

## 3. Baseline of unchanged upstream commands (branch build, before any change)

| Command | Result | Wall | Bytes |
|---|---|---|---|
| `tab.list --json` (first request after host start) | ok | 54 ms | 134 |
| `tab.new https://docs.python.org/3/library/asyncio.html` | `Created tab 1555385315: ...` (text even with `--json`) | 81 ms | 70 |
| `wait.load` | `Page loaded (readyState: complete)` | 53 ms | 74 |
| `page.read` | interactive tree + page text; the text includes the page's inline `<script>` source (upstream quirk) | 119 ms | 7,888 |
| `page.read --compact --max-bytes 3000` | | 115 ms | 4,826 |
| `js "return document.title"` (first CDP use on the tab) | `Request timed out (60s)` | 60,051 ms | 30 |
| `js "return {h1, links}"` | ok | 796 ms | 99 |
| `js --file stmt.js` (`const ...; return {...}`) | first try hung 60 s, second ok (the MV3 CSP fix works: statement script returned 5 titles) | 793 ms | 191 |

The 60 s stalls are analysed in §6; they are not caused by the branch (reproduced with the pristine upstream
stack) and did not recur on freshly opened active tabs.

## 4. Scenario results

### 4a. Readiness: `page.readiness` / `wait.ready`

| Page | Command | State / evidence (excerpt) | Wall |
|---|---|---|---|
| docs.python.org asyncio | `page.readiness` | `ready` - "document.readyState is complete"; `--json` adds `snapshot` (bodyTextLength 3647, headings, 0 password / 1 text input) | 48 ms |
| github.com/settings/profile (bounces to /login) | `page.readiness` | `login` - "1 visible password field(s); URL path /login looks like a login route; title 'Sign in to GitHub' mentions signing in" | 50 ms |
| same | `wait.ready --url-prefix https://github.com/settings` | exit 1, `Error: Page is not ready: login at ... left the expected prefix https://github.com/settings` (now suffixed `[page_login]`) | 50 ms |
| same | `wait.ready ... --accept login` | exit 0, `accepted: negative state returned because of --accept`, `waited: 1ms (1 poll)` | 46 ms |
| same | `wait.ready --selector .settings-content --timeout 3000` | fails fast with `login` instead of waiting 3 s | 45 ms |
| docs.python.org/3/library/does-not-exist.html | `wait.ready` | `not-found` - title "Page not found — Python 3.14.7 documentation" | 49 ms |
| github.com/.../blob/main/nope-nope.md | `wait.ready` | `not-found` - title "File not found · GitHub" | 50 ms |
| nowsecure.nl (Cloudflare challenge demo) | `page.readiness` | `ready`: Brave with a real UA was not challenged (body "NOWSECURE BY NODRIVER", 43 chars). No public page produced a challenge for this browser, so the `challenge` state was only exercised by unit tests. Not attempted to provoke one. | 52 ms |
| news.ycombinator.com (inside `extract`) | `wait.ready --selector tr.athing` | `ready` after 3 polls / 804 ms while `readyState` was still `interactive` (selector gate wins over readyState, as designed) | |
| pypi.org/search/?q=zzqq... | `wait.ready --empty-text "no results"` | `empty` after 2 polls / 403 ms | |

Judgement: detection is fast (one content-script round trip), the evidence lines are exactly what an agent needs
to explain a failure, and `--accept` gives the branching form. The `challenge` path remains validated only by
unit tests and the vendor-marker list; that is acceptable for a PR but should be stated.

### 4b. `frame.diagnose`

| Page | Before the quick wins | After |
|---|---|---|
| Own fixture `frames.html` (YouTube embed, srcdoc, example.com, `sandbox=""` iana.org, hidden about:blank, iframe inside an open shadow root) | DOM 5 iframes (shadow-hosted one missing), srcdoc/blank `cdp -` although CDP listed them with `name=srcdoc`/`name=hidden`, three out-of-process frames shown as `cdp -` with no explanation, mismatch warning "nested or detached frames account for the difference" (wrong: it was the shadow root) | DOM 6 iframes incl. `[5] https://example.org/ ... in shadow root of div#host`, `[1] srcdoc ... cdp 1E4F...`, `[4] about:blank ... cdp B9C8...`, four "is out-of-process: missing from this tab's CDP frame tree, so frame.js cannot reach it; its content script answers, so frame.switch, page.read and click by ref work there" warnings (the sandboxed one says "its content script is unreachable too"), no false mismatch warning. 62 ms, 3,851 bytes text / 10,218 bytes JSON |
| developer.mozilla.org `<iframe>` reference (live samples in `mdn-play-runner` shadow trees, each an OOPIF) | "DOM iframes: 0, extension frames: 7, CDP frames: 1"; ext-frame lines were 700+ chars each (mdnplay `state=` parameter); 3,185 bytes | "DOM iframes: 3" each `in shadow root of mdn-live-sample-result > mdn-play-runner`, URLs abbreviated (`runner.html?...(+527 chars)`), mismatch explained ("3 of them nested below another frame; the nested frames account for the difference"); 60 ms, 3,609 bytes (1,652 bytes with the CLI abbreviation before the shadow-root walk added the three entries) |
| w3schools HTML YouTube page | 1 DOM iframe (`__tcfapiLocator`, 0x0, about:blank, no content script); the YouTube embed on that page is only sample text, so nothing to diagnose | unchanged |

### 4c. `extract`

| Job | Command (abridged) | Result | Wall |
|---|---|---|---|
| GitHub releases | `extract https://github.com/nicobailon/surf-cli/releases --file gh-releases.js --options '{"limit":5}' --ready-selector 'a[href*="/releases/tag/"]'` | Markdown: `- page`, `- title`, `5 rows`, table `date | tag | title` (v2.18.0 ... v2.15.2). Columns come back alphabetically because `chrome.debugger` sorts dictionary keys | 1,057 ms end to end (tab.new, wait.ready, js, tab.close) |
| Hacker News front page | `... --file hn-front.js --options '{"limit":3}' --ready-selector tr.athing --json` | `{data, rows[3], readiness{state: ready, polls: 3, waited: 804}, rowCount: 3, attempts: 1, mode: owned-tab, tabId: null}` | 903 ms, 2,041 bytes |
| Docs TOC (my script) | `--file docs-toc.js --ready-selector .toctree-wrapper` | `empty_result` after 2 attempts (fresh tab each), exit 1, no leaked tab. Cause: my script picked the first match of a selector list, which was the page's top navigation, not the TOC. The zero-rows invariant caught an agent script bug within 1.5 s instead of returning an empty success | 1,486 ms |
| PyPI no-results search | `--code '...a.package-snippet...' --empty-text "no results" --json` | `readiness.state: "empty"`, `rowCount: 0`, exit 0. One run reported `attempts: 2` (first attempt saw `ready` with zero rows, second saw `empty`), the rerun `attempts: 1` | 499-1,474 ms |
| `--allow-empty` on example.com | | `# Extraction from https://example.com/` / `0 rows`, exit 0 | 504 ms |
| Transient failure (script reloads its own page) | `--code 'location.reload(); await ...; return [{a:1}]'` | attempt 1 fails, "retrying with a fresh tab", attempt 2 fails, exit 1 `[browser_error]`. Message was `{"code":-32000,"message":"Inspected target navigated or closed"}`; now `Inspected target navigated or closed` | 1,561 ms |
| `--rows rows` on `{things: 1}` | | `The script result has no array at "rows" [rows_key_missing]` | 510 ms |
| `--code 'document.title'` (no return) | | `The extraction script returned nothing. End it with return { rows: [...] } or return [...]. [no_output]` | 506 ms |
| `--code 'return "not json"'` | | prints ` ```json "not json" ``` `, exit 0: a scalar is accepted as a row-less result (see backlog) | 505 ms |
| `--ready-url-prefix https://example.org/` on example.com, `--ready-timeout 2500` | | `page_timeout` after two attempts (2 x 2.5 s + 500 ms), message names the prefix mismatch | 5,646 ms |

Tab accounting after each run: `tab.list` count unchanged (8 before and after the failing runs).

### 4d. `js --options`, `js --file`, error probes

- `js --file opts.js --options '{"limit": 2}'` on npmjs.com: `{frozen: true, limit: 2, items: []}` (891 ms on the
  active tab).
- `--options '{limit: 2}'` -> `--options is not valid JSON: Expected property name or '}' in JSON at position 1`;
  `--options '[1,2]'` -> `--options must be a JSON object, e.g. '{"limit": 20}'`. Both local, 40 ms.
- `js --file stmt.js` (`const items = ...; return {...}`) works in real Brave (the CSP fix); the pristine upstream
  2.18.0 stack fails every `return ...` script with `SyntaxError: Unexpected token 'return'` (control log), which
  means upstream's own `surf js "return document.title"` example never worked in the shipped extension.

### 4e. Native value setter on a React form (npmjs.com)

`wait.ready --selector 'input[name="q"]'` (48 ms) -> `type "surf-cli" --into 'input[name="q"]'` (811 ms, includes
upstream's auto-screenshot to `SURF_TMP`) -> `js` check: `{value: "surf-cli", trackerValue: "surf-cli", reactKeys: 3,
options: 5}` -> `page.read --no-text --compact`: five `option` rows ("surf-cli, version 2.18.0, ..."). React's
`_valueTracker` moved to the new value and the autocomplete rendered, i.e. the framework saw the change. An Angular
site was not tested (no public Angular form with a visible reaction found quickly); the unit test covers the
prototype-setter mechanism, which is framework-independent.

## 5. Measurements

Per command over the whole session (`$S/dogfood/dogfood.log`, 123 calls, wall = CLI process start to exit):

| Command | n | min | max | avg | avg bytes | Note |
|---|---|---|---|---|---|---|
| `tab.list` | 16 | 43 ms | 54 ms | 47 ms | 1,204 | |
| `tab.new` | 15 | 65 ms | 84 ms | 72 ms | 69 | |
| `tab.switch` | 4 | 62 ms | 73 ms | 66 ms | 53 | |
| `page.read` | 4 | 41 ms | 119 ms | 96 ms | 3,624 | |
| `page.readiness` | 9 | 43 ms | 52 ms | 48 ms | 638 | `--json` ~1 KB, text ~200 B |
| `wait.ready` | 13 | 42 ms | 51 ms | 47 ms | 426 | all pages already settled; polling cost is the 400 ms interval |
| `wait.element` | 3 | 599 ms | 1,895 ms | 1,132 ms | 217 | deliberate timeouts |
| `frame.diagnose` | 11 | 45 ms | 66 ms | 54 ms | 4,609 | text 1.3-3.9 KB, JSON 3-10 KB |
| `extract` | 17 | 43 ms | 5,646 ms | 1,168 ms | 488 | 0.5-1.1 s per successful job incl. tab open/close |
| `type --into` | 2 | 43 ms | 811 ms | 427 ms | 136 | |
| `js` | 27 | 40 ms | 60,051 ms | 20,007 ms | 92 | bimodal: 0.8-1.0 s on active tabs, 25-60 s on background tabs (§6) |

Verification (branch before / after the quick wins):

| Check | Branch at `008f3ab` | Branch at `dfc7408` |
|---|---|---|
| `npm run lint` (Biome, `test/**`) | 0 errors, 2 warnings, 1 info (pre-existing) | same |
| `npm run check` (tsc, both configs) | pass | pass |
| `npm test` | 68 files, 865 passed, 2 skipped | 69 files, 878 passed, 2 skipped |
| `npm run build` | ok, no `dist/chunks` | ok, service worker 130.8 -> 132.9 kB |
| `npm run test:e2e:chrome` (Chrome 152.0.7977.54) | pass, 4 frame warnings, 2 rows | pass, 3 frame warnings (srcdoc now matched by id), 5 fixture iframes incl. the shadow-hosted one, 2 rows; 5.3 s |

## 6. The `js` stall (measured, not fixed)

Sequence on the docs tab after it stopped being the active tab: `return ...` scripts 60,051 / 795 / 60,049 / 793
ms (alternating), expression scripts 60,049 / 60,050 / 60,050 ms, then 4,867 / 3,800 ms. Fresh active tabs: 0.8 s
every time; inside `extract` (owned active tab) 0.5-1.1 s for the whole sequence. `tab.switch <id>` then three
`js`: 795 / 820 / 792 ms; switch away again: 25,566 ms. MDN tab after other tabs had been opened: 47,107 ms.
Pristine upstream 2.18.0 extension + host in a fresh profile: foreground 800 / 792 / 789 / 766 ms, after two more
tabs 792 / 983 / 31,375 ms, after a `page.read` 33,997 ms. A concurrent `tab.list` during a stall (answered in 47
ms) did not release it, so it is not a host queue; the host's own stdin bug (§7, fixed) was ruled out by
re-measuring after the fix (47 s on MDN). Content-script tools on the same stalled tab answer in ~50 ms, so the
renderer is not frozen; the DevTools session for a non-active tab is. Both the CLI deadline (60 s) and Brave's
own timing (25-47 s) end the stall, and the result is correct when it arrives (`exit 0` at 60,049 ms).

Practical rule for agents (now in README/SKILL): use `extract` or `tab.switch` before `js` on an existing tab; prefer
`page.read`/`page.readiness`/`frame.diagnose` (content script) for reads. Open question for the maintainer: is
this Brave-only (Chromium control could not be completed here), and does `Runtime.enable` before every command or
the `awaitPromise` async wrapper matter?

## 7. Ranked backlog

### Quick wins (< 1 h each) - all implemented on the branch

| # | Item | Evidence | Commit |
|---|---|---|---|
| Q1 | Host stops draining stdin after `EXTENSION_HELLO`/`TARGET_EVENT` (early `return` inside the frame loop) | first `tab.list` after host start hung 60 s in the upstream control run (and in the previous session); `host.cjs` `processInput` | `89073e8` fix(host): `native/stdin-frames.cjs` (`takeFrames`/`encodeFrame`), `handleExtensionFrame`, 5 unit tests |
| Q2 | CDP errors printed as JSON blobs | transient `extract` run | `11e20aa` fix(cdp): `describeDebuggerError` in `CDPController.send`, keeps `cdpCode`/`cdpMethod`; 3 tests |
| Q3 | `frame.diagnose` misses shadow-hosted iframes, never matches blank frames by name, silent on OOPIFs, misleading mismatch text, kilobyte URLs in text mode | MDN, own fixture | `78702b5` feat(frame): shadow-root walk with `shadowHost`, name/id correlation, out-of-process warning with the working alternative, count explanation, URL abbreviation in the CLI; 3 new unit tests, e2e fixture + assertions |
| Q4 | Transport keys (`id`, `_resolvedWindowId`) in `page.readiness`/`frame.diagnose`/`extract --json` | every `--json` run | `91a7e33` feat(cli): `stripTransportKeys` for those tools, `cleanReadiness` in `extract`, `_resolvedWindowId` stripped in `formatToolContent` (upstream question 1 answered by doing it); tests |
| Q5 | Error code invisible in text mode; `--json` errors are prose on stderr | `wait.ready` on the GitHub bounce | same commit: first error line ends with `[code]` for every tool, `--json` also prints `{"error": {code, message, details}}` on stdout (details de-duplicated); verified on `wait.ready` (`page_login`) and upstream `wait.element` (`browser_error`) |
| Q6 | Docs for the above and for the background-tab `js` latency | | `dfc7408` docs (README, SKILL.md, CHANGELOG Unreleased, `--llm-context`) |

### Medium (hours) - deferred

- `js`/`frame.js`: investigate the non-active-tab stall (§6); candidates: skip the per-command `Runtime.enable`,
  `chrome.tabs.update({active: true})` behind an explicit `--activate` flag, or a CDP `Emulation`/`Page.setWebLifecycleState`
  probe. Needs Chromium-vs-Brave data first.
- `extract`: a scalar return value (`return "not json"`) is accepted as a row-less success; consider `invalid_output`
  unless `--allow-scalar`. `extract --json` should still emit the `[surf] attempt n/m` lines on stderr (it does; the
  report only noted that they are easy to miss).
- `extract` retries on `page_timeout` even when the timeout was a `--ready-url-prefix` mismatch that a fresh tab
  cannot change; classify "URL never matched prefix" as fatal like `page_login`.
- `frame.diagnose`: correlate out-of-process frames via `Target.getTargets`/`Target.attachToTarget` so `frame.js`
  can offer the OOPIF's own target id (upstream question 7); currently the report can only say "use frame.switch".
- `page.readiness`: a `challenge` fixture route in the e2e (vendor markup only) so the state is exercised in real
  Chrome, since no public page challenged a real-UA Brave.
- `type --into` auto-screenshot: the host writes `pi-auto-*.png` into `SURF_TMP` after the call and the CLI prints
  the path (upstream behaviour, independent of the CLI's opt-in `--auto-capture` flag); an agent running many form
  steps pays ~0.7 s each. Worth an opt-out or documenting.

### Design changes - deferred (unchanged from the previous note, plus one)

- `form.plan` / `form.apply --file plan.json [--submit]` prepare/apply split with safety defaults.
- `wait.element --count-stable <n>`, `downloads.wait --for <id|url>`, `extract --id-key <key>`.
- `--json` errors on stdout for *all* tools is now on the branch; if the maintainer prefers stderr-only, the change
  is one block in `handleResponse` (`native/cli.cjs`) and the CHANGELOG entry.
- `tab.new` still answers with prose under `--json` (upstream); `extract` parses the id from "Created tab N", which
  is brittle across hosts (the Go fork returned `{tabId}`); a structured `tab.new --json` would remove the regex.

## 8. Regressions vs upstream

None observed for unchanged commands (`tab.*`, `page.read`, `wait.*`, `type`, `js` expression form): same output
shapes and timings as the upstream control (`tab.list` 47 ms, `page.read` ~100 ms, foreground `js` 0.8 s).
Behaviour changes that upstream users will notice, all deliberate and in the CHANGELOG:

1. `Error:` lines end with ` [code]` (first line only; `Recovery:` lines untouched).
2. `--json` failures additionally print `{"error": ...}` on stdout (stderr line kept, exit code kept).
3. `formatToolContent` no longer emits `_resolvedWindowId` (nothing in `native/` read it).
4. `frame.diagnose` DOM indexes now include shadow-hosted iframes appended after the light-DOM ones (the e2e asserts
   by `id`, not by index; `frame.switch --index` uses extension frames, so unaffected).
5. Native host: replies that shared a stdin chunk with a `TARGET_EVENT` now arrive immediately instead of at the
   next message; the "first request after host start hangs 60 s" symptom disappears (verified: 52 ms and 51 ms on
   two cold starts after the fix).

## 9. Updated PR description (delta to the block in `2026-09-06-surf-cli-contribution-branch.md`)

Title unchanged. Add to "What's in it":

```markdown
- **Fix: native host stalled replies** – `processInput` returned from the frame loop after `EXTENSION_HELLO`
  and `TARGET_EVENT`, leaving any reply in the same stdin chunk unread until the next message from the extension
  (typically the 60 s client timeout on the first request after host start). Framing moved to
  `native/stdin-frames.cjs` with tests; every complete frame per chunk is now dispatched.
- **Fix: readable CDP errors** – `chrome.debugger` rejections carried the CDP error as a JSON string; `send()`
  now unwraps the message and keeps `cdpCode`/`cdpMethod` on the error.
- **`frame.diagnose` on real pages** – walks open shadow roots (`shadowHost` on each DOM entry), matches
  `srcdoc`/`about:blank` iframes to CDP frames by `name`/`id`, warns explicitly about out-of-process iframes and
  which commands still work there, explains count mismatches (nested/shadow-hosted), abbreviates long URLs in the
  text report.
- **Error codes for scripts** – every `Error:` first line ends with `[code]`; `--json` also prints
  `{"error": {"code", "message", "details"}}` on stdout. `page.readiness`, `wait.ready`, `frame.diagnose` and
  `extract --json` no longer leak the extension message `id` / `_resolved*` keys.
```

Replace the "Testing" numbers: 878 unit tests (+105 vs upstream), e2e extended with a shadow-hosted iframe and the
id-based srcdoc correlation. Add to the maintainer questions:

9. `js` on a non-active tab stalls 25-60 s in Brave 151 with both the branch and pristine 2.18.0 (content-script
   tools unaffected; the result is correct when it arrives). Known? Chromium-only data was not obtainable here.
10. `--json` errors now go to stdout as an object (stderr line kept). Preferred, or stderr-only?

## 10. Recommended upstreaming order

1. `89073e8` fix(host) stdin frames - independent, small, clearly a bug, affects every user (first-request hang).
2. `11e20aa` fix(cdp) error message - independent, small.
3. `17d2912` fix(js) MV3 CSP - independent, small; upstream's own `js "return ..."` example is broken without it.
4. `5dcab25` native value setter - independent behaviour fix.
5. `0e82d46` readiness -> 6. `91c3ea4` + `78702b5` frame.diagnose -> 7. `94bfd82` + `67987bd` extract/options ->
   8. `91a7e33` CLI error codes/transport keys -> 9. `7dcadf8` e2e -> 10. `008f3ab` + `dfc7408` docs.
   `extract` depends on readiness; the CLI-errors commit touches `handleResponse` and is the one most likely to
   get maintainer pushback (stdout JSON), so it is cut as its own commit and easy to drop or rework.

If one PR is too large, three PRs: (A) the three fixes, (B) native setter, (C) readiness + frame.diagnose + extract
+ CLI errors + docs.

## 11. Durable copies and cleanup

- `contrib/surf-cli` branch `feat/site-independent-mechanisms` force-updated to `dfc7408` (13 commits over
  `15080ff`; `git fetch <scratch clone> +feat/...:feat/...`). Working tree of that checkout untouched (still
  detached at v2.18.0).
- Patch series regenerated: `contrib/docs/learnings/patches/2026-09-06-surf-cli-site-independent-mechanisms/`
  now holds `0001`-`0013` (`git format-patch 15080ff..HEAD`); the old eight were deleted first. Not committed.
- Throwaway Brave instances (dogfood profiles 1 and 2, upstream control profiles B and C) and the fixture
  `http.server` on 127.0.0.1:45123 were terminated by PID after checking their command lines; the user's Brave and
  Chromium, `/tmp/surf.sock` and `~/.config/*/NativeMessagingHosts` were never touched. Scratch keeps
  `$S/surf-dogfood` (the clone, clean tree), `$S/dogfood/` (logs, wrappers, profiles, scripts, fixture) and can be
  deleted with the session.
