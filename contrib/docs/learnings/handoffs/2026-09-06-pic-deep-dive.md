# Handoff: deep dive into `pic` (cv/pic), upstream deleted

You are starting a fresh session. Goal: squeeze everything learnable and reusable out of the archived repo
`~/ai-society/softwareco/contrib/pic` ("Pic — a Pi agent with a browser-native, durable session", Carlos Villela,
last release v0.2.37 on 2026-08-13; the GitHub repo cv/pic disappeared before 2026-09-06, the local clone is the
only copy; its remote is kept as `dead-origin-20260906`).

Why we care: our own agent stack is Pi (`~/ai-society/softwareco/contrib/pi-mono`, packages/coding-agent + tui) and
our extensions in `~/ai-society/softwareco/owned/pi-extensions` (pi-little-helpers: sidequests, Ghostty launch,
session presence; pi-society-orchestrator). Pic wraps the same Pi agent in a browser-native, durable session. We want
to know what it did better, what to borrow, and whether anything is worth resurrecting or forking.

Rules: static analysis only in this session. Do NOT run `npm install`, build, tests or any repo script; do not
execute repo code. Read package.json scripts and lockfiles and report what running it would require and whether
any install-time hook exists. Do not modify the repo. Read as much of the source as needed (it is small enough).

Produce `~/ai-society/softwareco/contrib/docs/learnings/2026-09-06-pic-deep-dive.md` with these sections:
1. Summary (10 lines max: what it is, maturity, verdict).
2. What it is: purpose, user story, release history (git log, CHANGELOG), size (files/LOC by area), licence.
3. Architecture map: processes, browser side vs server side, how the Pi agent is embedded/driven (which Pi APIs,
   RPC, session file format, hooks), durability model (what survives a reload/restart and how), transport
   (websocket/SSE), auth/security model, storage.
4. Key ideas worth stealing: concrete mechanisms with file:line references, why they matter for us.
5. Comparison with our stack: overlap and gaps vs pi-mono's coding-agent/tui and pi-little-helpers (session
   presence, sidequest launch, Ghostty-bound sessions). Where Pic's browser session model would replace or
   complement Ghostty-hosted Pi sessions (see workstation docs/project/2026-04-12* and the ghostty runtime pin doc
   in ~/ai-society/softwareco/infra/workstation/docs/project/2026-09-06-ghostty-runtime-pin-design.md).
6. Quality: tests present and what they cover, CI, typing, error handling, dependency footprint and versions
   (pin against the Pi version it targets vs our current pi-mono HEAD; list APIs it uses that changed).
7. Risks: anything security-relevant (exposed ports, eval, secrets handling), anything that would break on
   current Pi.
8. How to run it (not executed): exact commands, prerequisites, ports, env vars.
9. Recommendations: (a) borrow-as-idea list, (b) borrow-as-code list with licence note, (c) fork/resurrect
   yes/no with the first three steps, (d) experiments to run in a follow-up session that IS allowed to execute.
10. Open questions.
Finish with a 15-line summary in your final message. Cite files as path:line.
