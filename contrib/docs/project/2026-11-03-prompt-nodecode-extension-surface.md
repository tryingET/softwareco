---
summary: "Prompt for designing Nodecode's long-term extension surface for operator helpers; use with the RFC 2026-11-03-rfc-nodecode-little-helpers.md."
read_when:
  - "Before revising the little-helpers RFC or proposing Nodecode hooks upstream."
---

# Prompt: design Nodecode's extension surface for operator helpers

You design the smallest lasting extension surface of Nodecode (upstream
nodecode-ai/nodecode) that lets operator helpers be built as cells.

## Read first, and cite file:line for every claim about code

- The RFC: `docs/project/2026-11-03-rfc-nodecode-little-helpers.md`,
  including section 10.
- Upstream main at a stated SHA: `docs/cell-api.mdx`,
  `src/organism/cell-dsl.lisp`, `src/gateway/gateway.lisp` (the slash and
  session routes), `src/gateway/protocol.lisp`, `src/tui/keys.lisp`,
  `src/tui/frame.lisp`, `src/engine/turn.lisp` (tools per turn),
  `src/organism/fork.lisp`, and `docs/{gateway,channels,rpc}.mdx`.
- The helper catalogue: `pi-extensions/packages/pi-little-helpers/README.md`
  and its `extensions/`.
- `upstreams/nodecode-ai--nodecode.md` in issue-tracker, and the fate of our
  earlier PRs (#4 to #11, #95).

## Goal

Find the fewest stable primitives such that:

1. Every helper in the catalogue, and the four the operator named (sidequest,
   /btw, stash, codeblocks), can be built as a cell with no further core
   change.
2. Each primitive works on, or degrades cleanly on, every front end: the TUI
   shell, the web page, the channels and rpc.
3. No cell holds more authority than its helper needs. The draft, the
   clipboard, process launch and tools are authorities.
4. The upstream maintainer would want to keep each primitive for its own
   sake.

## Constraints

- Two processes: gateway and shell. Name the process where each effect runs.
- Accretive only: open data maps, unknown keys ignored, nothing existing
  changes meaning.
- Policy (Ghostty, key choices, storage) lives in our cell, never upstream.
- Reuse existing machinery before proposing new mechanism. A documented
  export of something that exists beats a new hook.

## Method

1. **Coverage matrix:** helpers × candidate primitives. A helper that needs
   a bespoke primitive is a design smell. Merge or generalise until none
   does.
2. **Many-of-the-greats** (`~/.pi/agent/prompts/many-of-the-greats.md`) over
   at least: Emacs malleability, effects as data (Elm), object capabilities,
   mechanism not policy, accretion (Hickey), and maintainer economics
   (worse-is-better, Hyrum's law). Decide, do not balance.
3. **Pre-mortem at two years:** which primitive was regretted, which helper
   could not be built, and which front end was left behind? Revise.
4. **Adversarial check:** a fresh reviewer with no history tries to name a
   plausible helper that the set cannot build, and tries to misuse each
   primitive.
5. **Maintainer view:** write the upstream issue as needs plus the coverage
   table, offering the primitives as one candidate shape.

## Output

- **Primitives,** each with its data shape, the process where it runs, the
  authority it needs, its failure mode and its degrade rule per front end.
- **The coverage matrix.**
- **Rejected options,** each with the fact that rejects it.
- **The upstream issue draft**, in Summary, Problem, Proposal, Context.
- **The first PR:** its scope, a failing test that names the need, and a
  live proof on an isolated instance.

## Done when

- The matrix covers the whole catalogue with at most four primitives plus
  documented exports.
- Every primitive has a degrade rule for each front end.
- The fresh reviewer finds no helper that needs a core change, and no
  primitive that grants more than it declares.
