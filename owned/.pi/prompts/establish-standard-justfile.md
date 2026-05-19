---
description: Establish the standardized repo-local Justfile command surface for a softwareco/owned repo
---
Read `/home/tryinget/ai-society/softwareco/owned/docs/project/standardized-justfile-contract.md` completely.

Then inspect the current repo root before loading any extra stack guidance:
- detect whether `Justfile` exists
- detect whether the standardized target surface is already present and healthy
- detect the repo's stack/lane from direct repo evidence

Only if `Justfile` is missing or the standardized surface is absent/drifting, read the matching lane-specific Justfile addendum from `engineering-core` by exact path:
- Python: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-py.justfile.md`
- Go: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-go.justfile.md`
- Rust: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-rust.justfile.md`
- TypeScript/Bun: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-ts.justfile.md`
- TypeScript for pi extensions: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-pi-ts.justfile.md`
- Elixir: `/home/tryinget/ai-society/core/engineering-core/src/engineering_core/lanes/engineering-elixir.justfile.md`

Do not load unrelated lane addenda.
If the standardized surface is already present and healthy, make no unnecessary changes; summarize the assessment and stop.

When changes are needed, establish or reconcile the repo-local `Justfile` so it satisfies the owned-lane contract.

Requirements:
- keep the standardized target vocabulary and semantics from the contract
- prefer thin delegation to existing repo-local scripts or native package-manager commands
- preserve existing valid behavior and minimize churn
- add missing standardized targets when they are meaningful for this repo
- do not invent fake `dev` behavior if this repo has no natural long-running dev/watch surface
- if a target is intentionally omitted because it is not meaningful, state that explicitly in the final summary and add a brief repo-local note only if needed
- validate the meaningful targets you changed or added
- summarize the lane detected, whether the lane addendum was loaded, the final target mapping, validations run, and any intentional omissions
