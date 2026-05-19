---
summary: "Standardized repo-local Justfile command surface for softwareco/owned repos."
read_when:
  - "You are adding or normalizing a repo-local Justfile in a softwareco/owned repo."
  - "You want the standard command names operators and agents should prefer across Rust, TypeScript, Python, and mixed-stack repos."
  - "A repo under softwareco/owned does not yet expose the standard Justfile surface and needs transition guidance."
---

# Standardized Justfile contract

## Intent

Give every `softwareco/owned` repo a stable operator/agent command surface independent of implementation language.

Standardize the **outer command names**, not the internal toolchain.
A Rust repo may delegate to `cargo`, a TypeScript repo to `pnpm`, and a Python repo to `uv` or `pytest`, while operators and agents still use the same top-level `just` vocabulary.

## Preferred target vocabulary

### Core targets

These should exist whenever they are meaningful for the repo:

- `just help` — show the supported local command surface
- `just test` — default repo test suite
- `just check` — fast local validation gate, lighter than full CI
- `just build` — build distributable or runnable artifacts
- `just lint` — run non-formatting linters
- `just fmt` — apply formatting
- `just ci` — full local CI-equivalent gate
- `just doctor` — toolchain/runtime/environment sanity checks

### Conditional targets

Use these only when they describe a real repo surface:

- `just run` — execute the repo's primary operator-facing entrypoint once
- `just dev` — dev server, watch mode, or normal local iteration entrypoint

Distinction:
- `run` = one normal execution of the main entrypoint
- `dev` = long-running iterative/watch/server mode

Do **not** invent fake `run` or `dev` behavior for repos that do not have a meaningful surface for them.

## Semantics

- Keep target meaning stable across repos.
- Prefer thin delegation to existing repo-local scripts or native package-manager commands.
- Prefer existing deterministic wrappers when present (`./scripts/...`, repo-local validation wrappers, package scripts).
- Keep success output low-noise when practical; on failure, show useful command/test output.
- Preserve existing good repo-specific commands; add standardized aliases or wrappers with minimal churn.
- Treat `run` as the canonical one-shot execution surface when the repo has one; prefer a truthful `--help`/smoke entrypoint over a fake long-running mode.
- Do not hide large amounts of custom logic inside `Justfile` recipes if an existing script already owns that behavior.

## Recommended implementation pattern

Good:

- `just test` -> existing canonical repo test command
- `just check` -> existing fast validation command
- `just run` -> existing primary CLI/app entrypoint
- `just ci` -> existing full validation/CI command
- `just doctor` -> existing environment/runtime sanity command

Prefer this shape:

```just
help:
    just --list

test:
    cargo test

check:
    ./scripts/validate.sh --quiet-success fast

ci:
    ./scripts/ci/full.sh --quiet-success
```

The exact delegated commands vary by repo and stack.

## Transition rule

During the transition period, if a `softwareco/owned` repo does **not** yet expose the standardized Justfile surface:

1. read this file completely
2. from that repo root, run:

```bash
pi -p "/establish-standard-justfile"
```

The prompt template is expected to:
- read this contract
- inspect the current repo first
- load a lane-specific Justfile addendum only when `Justfile` is missing or the standard surface is absent/drifting
- create or reconcile the repo-local `Justfile`
- preserve valid existing behavior
- add the standardized target surface with minimal churn
- validate the meaningful targets it added or changed

## Operator/agent rule

Inside `softwareco/owned` repos:
- prefer the standardized repo-local `just` targets over stack-specific raw commands when those targets exist
- fall back to stack-native commands only when the repo does not yet expose the standard surface or when a repo-specific command is explicitly required

## What this contract does not require

This contract does **not** require:
- identical internal implementation across languages
- a fake `run` target when the repo has no truthful primary execution surface
- a fake `dev` target in non-server/non-watch repos
- replacing existing canonical repo scripts with large Justfile logic
- one monolithic CI/test command shape across all repos

It only requires a stable outer operator surface.
