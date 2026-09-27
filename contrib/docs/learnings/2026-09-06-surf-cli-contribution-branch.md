# surf-cli contribution branch: site-independent browser-automation mechanisms

Fresh TypeScript/CommonJS re-implementation, in upstream's style, of the generic mechanisms identified in
`2026-09-06-surf-cli-go-restricted-verbs-research.md` (section 3, 16 mechanisms) and
`2026-09-06-surf-cli-go-deep-dive.md` (section 5). Nothing from the Go fork was copied; nothing site-specific
was ported. Nothing was pushed or forked; both `contrib/surf-cli` and `contrib/surf-cli-go` are unmodified.

## Branch location

- Scratch clone: `/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad/surf-cli-contrib`
  (cloned from `contrib/surf-cli`, upstream nicobailon/surf-cli v2.18.0 = `15080ff`).
- Branch: `feat/site-independent-mechanisms`, 8 commits on top of `15080ff`, working tree clean.
- The scratch directory is session-scoped. To keep the work, copy the clone or export the commits now:
  `git -C <clone> format-patch 15080ff..HEAD -o <somewhere>/surf-cli-patches` (or `git bundle create`).
- Pinned Chrome for Testing 152.0.7977.54 was downloaded into `<scratchpad>/puppeteer-cache` for the E2E run;
  it is not needed to review the branch.

## Commit list (oldest first)

| # | Commit | Subject | Files |
|---|---|---|---|
| 1 | `5dcab25` | feat(content): set form values through the native value setter | `src/content/native-value.ts` (new), `src/content/accessibility-tree.ts`, `src/service-worker/index.ts` (piHelpers.setValue), `test/unit/native-value.test.ts` |
| 2 | `0e82d46` | feat(page): typed page readiness (page.readiness, wait.ready) | `src/utils/page-readiness.ts`, `src/utils/readiness-poll.ts`, `src/content/page-readiness-probe.ts` (new); content script (`PING`, `PAGE_READINESS`), service worker (`PAGE_READINESS`, `WAIT_FOR_READY`), `native/host-helpers.cjs`, `native/tool-scope.cjs`, `native/mcp-server.cjs`, `native/cli.cjs`; 4 test files |
| 3 | `91c3ea4` | feat(frame): frame.diagnose compares DOM, extension and CDP frame views | `src/utils/frame-diagnose.ts` (new), service worker (`FRAME_DIAGNOSE`), host mapping, tool-scope, MCP, CLI; 2 test files |
| 4 | `94bfd82` | feat(cli): surf extract runs a read-only script in an owned tab | `native/extract.cjs`, `native/script-options.cjs` (new), `native/cli.cjs`; `test/unit/extract.test.ts`, `test/unit/script-options.test.ts` |
| 5 | `67987bd` | feat(js): --options prelude for js and frame.js scripts | `native/cli.cjs` |
| 6 | `17d2912` | fix(js): run statement scripts under the MV3 extension CSP | `src/cdp/controller.ts` (`compileScript`), service worker, `test/unit/service-worker/javascript-handlers.test.ts` |
| 7 | `7dcadf8` | test(e2e): cover readiness, frame.diagnose, extract and controlled inputs in real Chrome | `test/e2e/real-chrome.mjs`, `test/e2e/fixtures/list-items.js` |
| 8 | `008f3ab` | docs: describe wait.ready, page.readiness, frame.diagnose, extract and js --options | `README.md`, `skills/surf/SKILL.md`, `CHANGELOG.md` (Unreleased), `--llm-context` in `native/cli.cjs` |

Every commit ends with the `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` and
`Claude-Session: https://claude.ai/code/session_01PpyRJ9kNJBQ5JiqeYjxkTF` trailers. Git author is the operator
(`tryinget <markus@team-wangler.de>`, set per command with `-c`, not written to the clone's config).

Diff vs upstream: 30 files, +3,907 / -41 lines (`git diff 15080ff HEAD --stat`); the three commits touching `src/service-worker/index.ts`
were re-ordered with `git rebase --autosquash` (two import-block conflicts resolved by hand; the final tree was
verified byte-identical to the pre-rebase tree).

## Verification

| Check | Baseline (upstream 15080ff) | Branch |
|---|---|---|
| `npm run lint` (Biome, `test/**` only) | 0 errors, 1 warning (`noStaticOnlyClass`, pre-existing) | 0 errors, same warning |
| `npm run check` (tsc strict, both tsconfigs) | pass | pass |
| `npm test` (vitest) | 60 files / 773 passed, 2 skipped | 68 files / 865 passed, 2 skipped (+92 tests) |
| `npm run build` | pass | pass; verified that `dist/` has no shared chunk (see "Lessons") |
| `npm run test:e2e:chrome` (pinned Chrome 152.0.7977.54, throwaway profile and HOME under `os.tmpdir()`) | pass | pass, with the new assertions (`"result": "pass"`, 4 frame warnings, 2 extracted rows) |

Dependencies were installed with `npm ci --ignore-scripts`; the skipped hooks were reviewed (all `prepare`
scripts of published packages plus puppeteer's Chrome download) and none was run. The user's browser profiles and
processes were not touched: the harness launches its own Chrome with `--user-data-dir` under the temp dir and only
terminates processes whose command line contains that profile path.

## Per-mechanism status

Numbers refer to the table in section 3 of the restricted-verbs research note; "DD-n" to section 5 of the deep dive.

| # | Mechanism | Status | Where it lives | API | Tests |
|---|---|---|---|---|---|
| 1 / DD-2 | Readiness gate with typed negative states (challenge, login bounce, not-found, explicit no-results) | done | `src/utils/page-readiness.ts` (pure classifier + patterns), `src/content/page-readiness-probe.ts` (DOM snapshot), service worker `PAGE_READINESS` / `WAIT_FOR_READY`, `src/utils/readiness-poll.ts` (states, codes, `--accept`, poll loop) | `surf page.readiness [--selector --text --url-prefix --empty-text] [--json]`; `surf wait.ready [same] [--timeout --interval --accept a,b]`; socket tools `page.readiness`, `wait.ready`; result `{state, evidence[], href, title, readyState, tabStatus, polls, waited}`; error codes `page_login`, `page_challenge`, `page_not_found`, `page_error`, `page_timeout` | `test/unit/page-readiness.test.ts` (25), `readiness-poll.test.ts` (8), `service-worker/readiness-handlers.test.ts` (8), host mapping tests, E2E (login bounce with `--url-prefix`, `--accept login`) |
| 9 / DD-7 | Visible-UI-state login detection (not DOM presence, not cookies) | done (part of 1) | `collectReadinessSnapshot` counts only visible password/text fields (computed style + offset size, same rule as `wait.element`); `classifyLogin` requires a second signal (login route, login title, or URL outside `--url-prefix`) | see 1 | classifier tests: bounce, route+title, lone password field stays `ready` |
| 11 | Wait-page polling with a bounded budget and per-poll evidence | done (part of 1) | `pollReadiness` (timeout <= 120 s, interval >= 50 ms, always one probe, never sleeps past the deadline, `onPoll` hook); the CLI prints `waited`/`polls` and evidence lines | `wait.ready --timeout --interval` | `readiness-poll.test.ts` with a fake clock |
| 2 / DD-2 / DD-11 | Owned-tab lifecycle + readiness probe + read-only transient retry + "never retry mutations" + zero-rows invariant with `--allow-empty` | done | `native/extract.cjs` (`runExtraction`, `isTransientTabError`, `isRetryableExtractionError`, `selectRows`, `enforceRowsInvariant`, `tabIdFromResponse`), CLI block `surf extract` in `native/cli.cjs` | `surf extract <url> --file s.js [--code] [--options JSON | --options-file] [--ready-selector/--ready-text/--ready-url-prefix/--empty-text/--ready-timeout/--ready-interval] [--rows key] [--retry N --retry-delay-ms N] [--allow-empty] [--keep-tab] [--json]`; error codes `empty_result`, `no_output`, `invalid_output`, `rows_key_missing`, `no_tab`, plus readiness codes | `test/unit/extract.test.ts` (19; scripted fake host asserts the exact open -> ready -> js -> close -> open -> ... sequence), E2E (rows, Markdown, accepted empty, rejected empty with 2 attempts, no leaked tab) |
| 6 | Never re-navigate a caller-supplied tab | done (part of 2) | `runExtraction({target: true})`: with `--tab-id`/`--session` no `tab.new`/`tab.close`, no retry, `navigate` only when a URL is given | `surf extract --tab-id N [--code ...]` | unit: target mode navigates once and never retries; reads in place without URL |
| 16 / DD-1 | Page-side script contract: `SURF_OPTIONS` prelude, explicit `return`, plain file usable elsewhere | done | `native/script-options.cjs` (`parseScriptOptions`, `buildOptionsPrelude`, `applyOptionsPrelude`), wired into `js`, `frame.js` and `extract` | `surf js --file s.js --options '{"limit": 20}'` | `test/unit/script-options.test.ts` (6), E2E (`js --file` with a `const`-leading script) |
| 3 | Native value setter with `input`/`change` dispatch for React/Angular/Vue inputs | done | `src/content/native-value.ts` (`findNativeValueSetter`, `setNativeValue`); used by `setFormValue` (`type --ref`), `smartType` (`type --into`), `FORM_FILL` (`form.fill`); `piHelpers.setValue(el, value, events?)` for `surf js` | no new flags; behaviour change of existing commands | `test/unit/native-value.test.ts` (8; prototype setter bypasses an instance tracker), E2E (`type --into` on a tracked input updates the page's own mirror) |
| DD-5 | `frame diagnose`: DOM iframes + extension frames (content-script PING) + CDP frame tree with warnings | done | `src/utils/frame-diagnose.ts` (`buildFrameDiagnosis`, `DOM_IFRAME_INVENTORY_EXPRESSION`), service worker `FRAME_DIAGNOSE` + `collectExtensionFrames`, content-script `PING` | `surf frame.diagnose [--json]`; result `{mainPage, counts, domIframes[], extensionFrames[], cdpFrames[], warnings[]}` with per-frame `extensionFrameIds`/`cdpFrameIds`, `blank`, `crossOrigin`, `scriptsBlocked`, `zeroSize`, `contentScriptReachable` | `test/unit/frame-diagnose.test.ts` (8), `service-worker/frame-diagnose-handlers.test.ts` (3), E2E (same-origin, srcdoc, cross-origin via a second server, sandboxed) |
| DD-3 | Dual Markdown / rows output from one fetch | done (part of 2) | `renderExtractionMarkdown` (metadata bullets + table with escaped cells; scalar rows as bullets; row-less results as fenced JSON); `--json` gives `{data, rows, rowCount, attempts, readiness, mode, url, tabId}` | `surf extract ... [--json]` | unit rendering tests, E2E table check |
| DD-4 | Strip transport metadata before error classification; a row with an `error` field must not exit 0 | already upstream / partly done | Upstream's host already classifies `isPureError` on data keys and `formatToolContent` strips `_resolvedTabId`/`_hint` (`test/unit/host-helpers.test.ts:492`). Added a regression test that a readiness result renders as JSON rather than the generic "Page loaded" line, and `extract` exits 1 on any `{error}` step and on `empty_result`. Not done: `_resolvedWindowId` is not stripped by `formatToolContent` (see open questions). | - | `host-helpers.test.ts` addition |
| 4 | Form-settle heuristic (fixed settle + "field count stable for N samples") and label walk-up classification | design only | Upstream `wait.dom --stable <ms>` already implements mutation-quiet stability, and `locate.label` / the accessibility tree compute accessible names from `<label>`, `aria-label` and ancestors. The remaining gap is a *count-based* settle (`wait.element --count-stable`), useful when a form appends fields a few seconds after the first one. Proposed API in the PR description; not implemented to avoid duplicating `wait.dom`. | - | - |
| 5 / DD-10 | Prepare/apply split with `--submit` gate, editable template between read and write, "refuse on empty required", "click only the button whose text matches", post-click verification | design only | Upstream already has `type --submit` (opt-in) and workflows/playbooks. A generic form verb would be `form.plan` (writes `{fields[], requiredEmpty[], submitButton}` to a file) and `form.apply --file plan.json [--submit]` (fills through the native setter, refuses when required fields are empty, clicks only the named button, waits for a URL change or confirmation text). Design in the PR description; deliberately not implemented in the same PR because the safety semantics deserve a separate review. | - | - |
| 7 | Anchored-regex extraction where no stable attributes exist, labelled "best-effort" | design only | Inherently per-script; the `extract` output keeps whatever the script returns. Recommendation for script authors documented in the README Extraction section ("script extracts, wrapper presents"). | - | - |
| 8 | Stable ids across snapshots (upsert-able row ids) | design only | Upstream refs (`e5`) are regenerated per `page.read`; row ids are the script's responsibility (`--rows` selects the array, nothing is invented). A `--id-key` option that fails when a row lacks the key would be a small follow-up. | - | - |
| 10 | Browser-session download watcher (`.crdownload` polling, then move) | design only | Upstream already has `downloads.search` (chrome.downloads). A `downloads.wait --for <id|url>` that polls `chrome.downloads.search` for the specific item (never "newest file in ~/Downloads") is the safe form; not implemented here. | - | - |
| 12 | Validate server-honoured URL parameters as typed flags | design only | Per-site by nature; the generic part (typed flags with validation errors) is how `extract`'s CLI block validates its own flags. | - | - |
| 13 | Custom-element / shadow-DOM attribute reading with light-DOM slot preference | design only | Page-side helper (`piHelpers.attr(el, name)` reading light-DOM slot first, then `el.shadowRoot`); small, but adds surface to the injected helper bundle. Not implemented. | - | - |
| 14 | Scroll + "Load more" loop bounded by a stop condition | design only | Fits `surf do` loops (`repeat` + `until`) which upstream already has; a script-side `loadMore({buttonText, maxRounds, stopWhen})` helper would be the page-side complement. Not implemented. | - | - |
| 15 / DD-12 | Research trail per feature (numbered probes + diary) | n/a for upstream | Process, not code; this document is our trail. | - | - |

Additional finding fixed on the way (not in either report):

- **`js --file` statement scripts were broken in real Chrome** (commit 6). The `js` tool tries `return (<code>)` first and falls back to
  statement mode only if `scriptParses` (which used `new Function`) reports a syntax error; the extension CSP
  (`script-src 'self'`) makes `new Function` throw an `EvalError` in the service worker, so the fallback never ran and
  any script beginning with `const` failed with `SyntaxError: Unexpected token 'const'`. Unit tests passed because
  Node allows eval. Fixed with CDP `Runtime.compileScript`; a unit test emulates the blocked `Function`, the E2E runs a
  real statement script.

## Lessons for the next contributor

- The extension has two bundle entries (content script, service worker). Any runtime module imported by both is
  emitted as `dist/chunks/*.js` and the classic content script silently fails to load it (`Receiving end does not
  exist`). Share only types across the boundary; that is why the classifier (`page-readiness.ts`, content) and the
  state list / poll loop (`readiness-poll.ts`, service worker) are separate files.
- `chrome.debugger` results come back with dictionary keys sorted, so output produced through CDP (`js`, the DOM
  iframe inventory) does not preserve object key order; never assert on column order.
- `formatToolContent` renders any `{success: true, readyState}` result as the fixed string "Page loaded" and any
  `{success: true, frames}` as the bare frame list; new tools must not set `success` on data results.
- `tab.new` replies with text ("Created tab <id>: <url>") even under `--json`; `--json` with an explicit target wraps
  the payload as `{result, target, notice}`.
- Tools not listed in `native/tool-scope.cjs` are scheduled as exclusive browser-wide writers; read-only tab tools
  must be added to `TAB_TOOLS`.
- Biome lints `test/**` only (`biome.json` `files.includes`); `src/` is only type-checked and `native/*.cjs` neither.
  `biome check --write` applies safe fixes only; `useBlockStatements` needs a manual edit.
- The shell aliases `cp` to `cp -i`; use `/bin/cp -f` in scripted chains.

## Ready-to-paste PR description

Title: `feat: typed page readiness, frame.diagnose, owned-tab extract, native value setter (+ js --file CSP fix)`

Body:

```markdown
## Motivation

Agents driving Surf keep re-deriving the same four things by hand: "did the page actually load, or did I land on a
login form / anti-bot interstitial / 404?", "why does my selector never match (which iframe is that widget in)?",
"open a tab, wait, run an extractor, close the tab, retry once if the target went away, and don't call an empty
result a success", and "why does React revert the value I just typed?". This PR adds site-independent building
blocks for each, in the existing tool/handler/CLI structure, plus one bug fix found on the way.

## What's in it

- **`wait.ready` / `page.readiness`** – a readiness classifier with typed states (`ready`, `empty`, `loading`,
  `login`, `challenge`, `not-found`, `error`). `wait.ready` polls with a bounded budget and fails fast with
  `page_login` / `page_challenge` / `page_not_found` / `page_error` / `page_timeout` (`--accept` returns a negative
  state instead). Detection uses visible UI state and the caller's expectations (`--selector`, `--text`,
  `--url-prefix`, `--empty-text`), never site selectors. Pure classifier + poll loop are unit-tested; the DOM
  snapshot is collected in the content script.
- **`frame.diagnose`** – DOM `<iframe>`s, `chrome.webNavigation` frames with a content-script PING, and the CDP
  frame tree side by side, correlated by URL, with warnings (srcdoc/blank frames, sandbox without `allow-scripts`,
  cross-origin, out-of-process, unreachable content script, count mismatches), each naming the frame command that
  still works.
- **`surf extract <url> --file script.js`** – read-only extraction in an owned tab: `tab.new -> wait.ready -> js ->
  tab.close`, bounded fresh-tab retry on transient target failures/timeouts/zero rows (never on login/challenge/
  not-found), zero-rows-is-failure unless `--allow-empty` or the page's own empty state, `--options` exposed as a
  frozen `SURF_OPTIONS`, Markdown table or `--json`. With `--tab-id`/`--session` it reads in place with no retry
  and no close. Documented as read-only because the sequence may replay.
- **`js --options`** – the same `SURF_OPTIONS` prelude for `js`/`frame.js` scripts.
- **Native value setter** – `type --ref`, `type --into`, `form.fill` write text inputs/textareas through the
  prototype setter so React/Angular/Vue trackers see the change; `piHelpers.setValue` exposes it to `js`.
- **Fix: `js --file` statement scripts under the MV3 CSP** – the statement-mode fallback relied on `new Function`,
  which `script-src 'self'` blocks in the service worker, so any script starting with a declaration failed in real
  Chrome (`SyntaxError: Unexpected token 'const'`) while unit tests passed. Now uses `Runtime.compileScript`.

## Design notes (not implemented, happy to follow up)

- `form.plan` / `form.apply --file plan.json [--submit]`: prepare/apply split for form mutations (refuse on empty
  required fields, click only the named button, verify a post-condition). Kept out of this PR so the safety
  semantics get their own review.
- `wait.element --count-stable <n>`: count-based settle for forms that append fields after the first render
  (`wait.dom` covers mutation-quiet stability already).
- `downloads.wait --for <id|url>`: poll `chrome.downloads.search` for a specific item rather than watching a folder.
- `extract --id-key <key>`: fail when a row lacks an upsert key.

## Attribution

Inspired by the surf-cli Go fork by Manuel Odendahl (MIT); the mechanisms were studied there and re-implemented
from scratch in TypeScript/CommonJS for this codebase. No code was copied and nothing site-specific was ported.

## Testing

- `npm run lint`, `npm run check`, `npm test`: green (865 passed, +92 new unit tests: classifier, poll loop, frame
  correlation, extract lifecycle with a scripted fake host asserting the open/ready/js/close/reopen sequence,
  native setter, options prelude, service-worker handlers, host mapping, tool-scope, CSP fallback).
- `npm run test:e2e:chrome` with the pinned Chrome 152.0.7977.54: extended with fixture routes (login page, frames
  page with same-origin/srcdoc/cross-origin/sandboxed iframes, list page with a framework-style value tracker and
  an empty variant) covering `page.readiness`, `wait.ready` (login bounce, `--accept`), `frame.diagnose`,
  `js --file --options`, `extract` (rows, Markdown, accepted/rejected empty, no leaked tab) and `type --into` on a
  tracked input.

Co-authored with Claude Code.
```

## How the operator pushes it (not executed)

```bash
# 0. keep the work outside the session-scoped scratch dir
CLONE=/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad/surf-cli-contrib
git -C "$CLONE" format-patch 15080ff..HEAD -o ~/surf-cli-patches      # or: cp -r "$CLONE" ~/src/surf-cli-contrib

# 1. fork upstream (once) and add the fork as a remote
gh repo fork nicobailon/surf-cli --clone=false                          # creates <you>/surf-cli on GitHub
git -C "$CLONE" remote add fork git@github.com:<you>/surf-cli.git

# 2. review, then push the branch
git -C "$CLONE" log --oneline 15080ff..HEAD
git -C "$CLONE" push -u fork feat/site-independent-mechanisms

# 3. open the PR against upstream main with the description above
gh pr create --repo nicobailon/surf-cli --base main \
  --head <you>:feat/site-independent-mechanisms \
  --title "feat: typed page readiness, frame.diagnose, owned-tab extract, native value setter (+ js --file CSP fix)" \
  --body-file pr-body.md                                                  # paste the block above into pr-body.md
```

Consider splitting into smaller PRs if the maintainer prefers: (a) the `js --file` CSP fix (one commit, clearly a bug),
(b) native value setter, (c) readiness, (d) frame.diagnose, (e) extract + js --options + docs. The commits are already
cut along those lines; `git rebase --onto` or `cherry-pick` per group works without conflicts except that (e) depends
on (c) (`extract` calls `wait.ready`) and the docs commit spans all of them.

## Open questions for the upstream maintainer

1. `formatToolContent` strips `_resolvedTabId` and `_hint` but not `_resolvedWindowId`, which therefore appears in
   `--json` output of every tool (seen in `page.readiness --json`). Intentional?
2. Should `wait.ready` negative states be errors (current: non-zero exit with `page_*` codes, `--accept` to opt out)
   or results with exit 0 like `page.readiness`? The error form suits `surf do` pipelines and `extract`; the result
   form suits agents that branch on the state.
3. Is `chrome.debugger`'s key-sorting of returned dictionaries known/accepted? It affects `js` output order and any
   Markdown table derived from it.
4. `extract` is a client-side compound command like `do`; would the maintainer rather see it as a `do` step type or
   a playbook `read` op strategy (`using: "extract"`) than a top-level verb?
5. The MV3 CSP finding means `js --file` with declarations never worked in the shipped extension; is there a known
   workaround users rely on (e.g. wrapping in an IIFE) that the fix should keep behaving identically for?
6. Tool scope: `wait.ready`, `page.readiness` and `frame.diagnose` are registered as tab-lane tools; `extract` is
   not a socket tool (it composes others). Should compound commands declare their scope somewhere for the scheduler?
7. `frame.diagnose` correlates by exact URL; frames that navigated after load, or several frames with the same URL,
   are reported as ambiguous rather than guessed. Would `documentId` (webNavigation) to CDP `frameId` mapping via
   `Target.getTargets` be worth the extra CDP round-trips?
8. The prepare/apply form design above: wanted as a follow-up, and if so with what safety defaults?
