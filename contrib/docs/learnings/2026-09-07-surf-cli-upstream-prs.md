# surf-cli upstream PRs: the site-independent branch split into eight reviewable PRs

Follow-up to `2026-09-06-surf-cli-contribution-branch.md` and `2026-09-07-surf-cli-branch-dogfood.md`. The
13-commit branch `feat/site-independent-mechanisms` (on v2.18.0 = `15080ff`) was split into eight PRs against
`nicobailon/surf-cli` `main`, opened from a fork under the operator's GitHub account. Upstream `main` had not
moved past `15080ff` at the time (checked 2026-09-07 08:00 CEST), so no rebase was needed. Nothing in `contrib/`
was modified or committed; all work happened in a scratch clone.

## Fork and locations

| Item | Value |
|---|---|
| Fork | https://github.com/tryingET/surf-cli (created with `gh repo fork nicobailon/surf-cli --clone=false`; account `tryingET`) |
| Scratch clone | `$S/surf-upstream` (`$S` = `/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad`), remotes `origin` = upstream, `fork` = the fork; our branch fetched as local ref `ours` |
| Build tooling | `$S/prtools/` (branch builders, e2e variant generator, docs applier, verify script, PR bodies `pr-*.md`, verification logs `verify-pr-*.log`) |
| Pinned Chrome for e2e | 152.0.7977.54 in `$S/puppeteer-cache` (`PUPPETEER_CACHE_DIR`); the harness launches it headless with `--user-data-dir` under `os.tmpdir()` and terminates only processes whose command line contains that profile path |
| Source branch | `contrib/surf-cli` `feat/site-independent-mechanisms` at `dfc7408` (unchanged); patches in `contrib/docs/learnings/patches/2026-09-06-surf-cli-site-independent-mechanisms/` |

Upstream conventions found (no `CONTRIBUTING.md`, no PR template): conventional-commit subjects (`fix:`,
`feat:`, `docs:`), squash merges, PR bodies with `## Summary` and `## Validation` (a command list with test
counts), a `## [Unreleased]` section in `CHANGELOG.md` that PRs fill, Biome lint on `test/**` only, CI jobs
lint / typecheck / vitest / real-Chrome e2e / `npm audit`. Nothing asks for draft PRs, so all eight are regular.

## The PRs

Branches are `pr/<letter>-<slug>` on the fork. "Base" is the branch the PR is logically stacked on; GitHub
cross-fork PRs can only target upstream branches, so every PR targets `main` and the stacked ones state their
base in the first paragraph of the body. Every branch was verified with `npm run lint` (only the pre-existing
`FakeNode` warning), `npm run check`, `npm test`, `npm run build` and `npm run test:e2e:chrome` (pinned Chrome,
throwaway profile), all green; upstream baseline is 60 files / 773 tests.

| PR | Branch (tip) | Base | Commits (oldest first) | Unit tests | E2E additions |
|---|---|---|---|---|---|
| A [#251](https://github.com/nicobailon/surf-cli/pull/251) `fix: process every framed stdin message in a chunk` | `pr/a-host-stdin-frames` (`d3523c4`) | main | `82dfffe` fix(host) (re-cut: `takeFrames` + `for` loop + `return`->`continue`, so `host.cjs` changes ~30 lines instead of the 510-line re-indent on the branch), `d3523c4` docs(changelog) | 778 (+5) | none (unchanged suite passes) |
| B [#252](https://github.com/nicobailon/surf-cli/pull/252) `fix: surface CDP error messages instead of the JSON envelope` | `pr/b-cdp-error-message` (`755da48`) | main | `0246962` fix(cdp), `755da48` docs(changelog) | 776 (+3) | none |
| C [#253](https://github.com/nicobailon/surf-cli/pull/253) `fix: run js --file statement scripts under the MV3 CSP` | `pr/c-js-file-csp` (`575276f`) | main | `dbecce9` fix(js) (unit test refactored: shared debugger mock with an injectable `Function`, to avoid a new Biome complexity warning), `24631b9` test(e2e), `575276f` docs(changelog) | 774 (+1) | statement script with a leading `const` on the fixture tab |
| D [#254](https://github.com/nicobailon/surf-cli/pull/254) `feat: set form values through the native value setter` | `pr/d-native-value-setter` (`2b764e5`) | main | `9c59e4c` feat(content), `09defdf` test(e2e), `2b764e5` docs | 781 (+8) | `/list` fixture with a framework-style value tracker; `type --into` updates the page's mirror (gated with `wait.element`, not `wait.ready`) |
| E [#255](https://github.com/nicobailon/surf-cli/pull/255) `feat: typed page readiness (page.readiness, wait.ready)` | `pr/e-page-readiness` (`545bd69`) | main | `b291c50` feat(page) (content-script `PING` handler removed here, it belongs to F), `d077e58` test(e2e), `545bd69` docs | 819 (+46) | `/login` fixture; `page.readiness`, `wait.ready --selector/--text`, login bounce under `--url-prefix`, `--accept login` |
| F [#256](https://github.com/nicobailon/surf-cli/pull/256) `feat: frame.diagnose` | `pr/f-frame-diagnose` (`05b0596`) | main | `408e28d` feat(frame) (+ the `PING` handler), `09a0828` feat(frame) follow-up (applied without its `--llm-context` hunk, which the docs commit recreates), `9fcc02e` test(e2e), `05b0596` docs | 789 (+16) | `/frames` fixture with same-origin, srcdoc, cross-origin (second server), sandboxed and shadow-hosted iframes |
| G [#257](https://github.com/nicobailon/surf-cli/pull/257) `feat: surf extract + js --options` | `pr/g-extract-options` (`b9ed788`) | E (#255), carries C's fix commit | `ce82826` fix(js) (= C's fix), `ce58b92` feat(cli) extract, `ae460ce` feat(js) --options, `869e340` test(e2e), `b9ed788` docs | 845 (+25 over E+C) | `/list` items + empty variant, `test/e2e/fixtures/list-items.js`; `js --file --options`, `extract` JSON/Markdown/accepted empty/rejected empty/no leaked tab |
| H [#258](https://github.com/nicobailon/surf-cli/pull/258) `feat(cli): error codes in every error line, JSON error objects` | `pr/h-cli-error-codes` (`bdbf5c6`) | G (#257) | `adcf066` feat(cli), `bdbf5c6` docs | 847 (+2 over G) | none new (the extract e2e asserts the `{"error": ...}` stdout object) |

Cherry-picked commits keep the original author (`tryinget <markus@team-wangler.de>`) and trailers; commits
created during the split (e2e and docs commits, the re-cut A commit) carry the same author and the
`Co-Authored-By: Claude Fable 5.1` / `Claude-Session` trailers. Cross-cutting branch commits were split per
feature: `7dcadf8` (e2e) by generating per-PR variants of `test/e2e/real-chrome.mjs` from the union file with
byte-identical helper/fixture text so later rebases merge cleanly; `008f3ab` + `dfc7408` (docs) by applying
README / SKILL.md / CHANGELOG / `--llm-context` hunks per PR (the empty ```` ```bash ```` block that `dfc7408`
left in the README was dropped; the Brave background-tab `js` note went into G's docs).

## Dependencies that forced the shape

- **G needs C as well as E.** `js --options` prepends `const SURF_OPTIONS = ...` to the script, so it only
  runs in real Chrome once statement mode works (C). The first G build failed its e2e with
  `SyntaxError: Unexpected token 'const'`; G now carries C's fix commit and says so in its body.
- **F needs the content-script `PING` handler**, which the branch had introduced in the readiness commit.
  The first F build failed its e2e with every frame "content-script unreachable". `PING` moved to F's first
  commit and was removed from E (E's commit message adjusted accordingly).
- **D and F gate on `wait.element`** in their e2e sections instead of `wait.ready`, so they do not depend on E.
- **H stacks on G** because it edits `handleResponse` in `native/cli.cjs` and `native/extract.cjs`; its
  `stripTransportKeys` set also names `frame.diagnose` (F), which is a no-op until F lands.
- The cherry-picks of E and F onto `main` conflicted where the branch had readiness and frame hunks side by
  side (import blocks, `tool-scope.cjs`, `handleResponse`, two test files); resolved by keeping only what each
  commit added relative to its parent (`$S/prtools/resolve_theirs_minus_base.py`).

## Expected merge friction

The PRs are independent against today's `main`, but they touch the same files, so after the first one merges
the others need a rebase: `CHANGELOG.md` `[Unreleased]` (each PR adds its own bullets), `README.md` /
`skills/surf/SKILL.md` (adjacent insertions), the `--llm-context` block and `ALL_SOCKET_TOOLS` / `SEE_ALSO` in
`native/cli.cjs`, `native/tool-scope.cjs` (`TAB_TOOLS`), `src/service-worker/index.ts` (import block, handler
switch), and `test/e2e/real-chrome.mjs` (identical helper blocks, which git usually merges on its own). When
#255 or #253 merge, rebase #257 and #258 onto `main` and drop the duplicated commits (`git rebase --onto
origin/main <old-base>`); the fixture `/list` route is identical in D and G on purpose.

## How to update a PR after review

```bash
S=/tmp/claude-1000/-home-tryinget-ai-society-softwareco-infra-workstation/f2e78a27-2565-4cf0-8648-637f8772bc4a/scratchpad
cd $S/surf-upstream                      # or: git clone https://github.com/tryingET/surf-cli && git remote add origin-upstream https://github.com/nicobailon/surf-cli
git fetch origin main                    # upstream
git checkout pr/e-page-readiness         # the PR branch
# ... edit, commit as the operator with the trailers ...
git -c user.name=tryinget -c user.email=markus@team-wangler.de commit -a -m "..."   # + Co-Authored-By / Claude-Session trailers
export PATH=$HOME/.local/bin:$HOME/.npm-global/bin:$PATH PUPPETEER_CACHE_DIR=$S/puppeteer-cache
npm run lint && npm run check && npm test && npm run build && npm run test:e2e:chrome
git push fork pr/e-page-readiness        # plain push for new commits; --force-with-lease after a rebase
# stacked PRs: after changing E, rebase G and H on top and push both:
git rebase --onto pr/e-page-readiness <old-E-tip> pr/g-extract-options && git push --force-with-lease fork pr/g-extract-options
```

`gh pr edit <n> --repo nicobailon/surf-cli --body-file ...` updates a description; `gh pr checks <n>` shows CI.
The scratch directory is session-scoped: to keep the branches beyond it, the fork already holds every commit
(`git clone https://github.com/tryingET/surf-cli`), and `$S/prtools/` can be copied if the generators are wanted.

## Rules kept

`npm ci --ignore-scripts` (skipped hooks reviewed: `prepare` scripts of published packages, which ship their
build output, and puppeteer's Chrome download, replaced by the pinned build already in scratch); no browser other
than the harness's own headless Chrome with a throwaway profile under `os.tmpdir()` was started or stopped; the
operator's Brave/Chromium, `/tmp/surf.sock` and `~/.config/*/NativeMessagingHosts` were not touched; nothing was
committed in `contrib/`.
