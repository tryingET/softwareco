# Handoff: deep dive into `surf-cli-go` (wesen/surf-cli), upstream deleted

You are starting a fresh session. Goal: squeeze everything learnable and reusable out of the archived repo
`~/ai-society/softwareco/contrib/surf-cli-go` — Manuel Odendahl's (wesen, go-go-golems) port/rework of surf-cli
("the CLI for AI agents to control Chrome"), last upstream commit 2026-04-25 ("Fix libgen download error"); the
GitHub repo wesen/surf-cli disappeared before 2026-09-06, the local clone is the only copy (remote kept as
`dead-origin-20260906`). The original project lives on: `~/ai-society/softwareco/contrib/surf-cli`
(nicobailon/surf-cli, TypeScript, v2.18.0, active).

Why we care: our agents drive Chrome today through the Claude-in-Chrome extension and through Pi tooling; we run
Brave/Chromium windows under niri (workstation repo ~/ai-society/softwareco/infra/workstation). We want to know what
this port added over nicobailon's surf-cli (the diary entries in the repo mention "extraction", "libgen", cobra
groups), what is worth borrowing, and whether anything justifies keeping or reviving it.

Rules: static analysis only in this session. Do NOT run `go build`, `go test`, `npm install`, or any repo script;
do not execute repo code. Read go.mod/package.json/Makefiles and report what running it would require and any
install-time hooks. Do not modify either repo. Read as much source as needed.

Produce `~/ai-society/softwareco/contrib/docs/learnings/2026-09-06-surf-cli-go-deep-dive.md` with:
1. Summary (10 lines max: what it is, relation to nicobailon/surf-cli, maturity, verdict).
2. What it is: purpose, history (git log, diary/ docs inside the repo), languages and size by area, licence.
3. Relationship to the original: is it a fork (shared history? compare `git log` roots and file overlap with
   ../surf-cli), a rewrite, or a wrapper; what it adds (features, commands, "libgen", extraction pipeline) and what
   it drops.
4. Architecture map: how Chrome is controlled (CDP, extension, remote debugging), command structure (cobra
   groups), session/tab model, output formats for agents, config.
5. Key ideas worth stealing with file:line references and why they matter for us.
6. Comparison with what we use now (Claude-in-Chrome extension, nicobailon/surf-cli v2.18): capability matrix.
7. Quality: tests, CI, error handling, dependency footprint, anything security-relevant (remote debugging ports,
   credentials, downloading from libgen and the legal/abuse angle of that feature).
8. How to run it (not executed): commands, prerequisites, env.
9. Recommendations: borrow-as-idea, borrow-as-code (licence), keep/revive yes/no with first steps, experiments
   for a follow-up session that IS allowed to execute.
10. Open questions.
Finish with a 15-line summary in your final message. Cite files as path:line.
