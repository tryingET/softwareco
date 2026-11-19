---
summary: "Capability map for softwareco/contrib repos in use as tools, for routing from any working directory."
read_when:
  - "A task needs an upstream tool kept in softwareco/contrib and the cwd is elsewhere."
  - "You choose which contrib repo to read first, or which domain skill to load for it."
type: "reference"
---

# softwareco/contrib repo capability map

## Use

The `softwareco-contrib-repo-router` skill reads this map. It lists the contrib repos in use as
tools, the cues that point to each, the files to read first and the domain skill to load. The lane
holds about 300 upstream clones; a repo that is not listed is not necessarily missing, only not yet
vetted as a tool here.

Rows are routing claims, not capability claims: route to the repo, then verify what it can do in
its own docs. Contrib repos are upstream code; use them and do not edit them in place.

## Adding a row

Add a row when a session uses a contrib repo as a working tool, with read-first files that exist
and a domain skill that loads. Keep each row to what a router needs.

## Repo map

| Repo | Owns | Trigger cues | Read first | Domain skill | Notes |
|---|---|---|---|---|---|
| `director` | Rendering video from HTML and CSS (GSAP, CSS keyframes, SVG, Lottie, Rhai) without a browser: native compiler, Taffy layout, Skia paint, FFmpeg export, and an agent CLI (`check`, `sheet`, `still`, `render`) and MCP server | video, announcement video, release video, reel, demo reel, product tour, motion graphic, render HTML to MP4, social clip for X, HyperFrames, Remotion alternative | `~/ai-society/softwareco/contrib/director/README.md`, `~/ai-society/softwareco/contrib/director/crates/director-html/README.md`, `~/ai-society/softwareco/contrib/director/.agent/skills/director-agent-loop/SKILL.md` | `director-video` | Upstream `stepupgaming/director` (MIT). Build `director-engine` on /data through the heavy-job runner and delete the target afterwards. Its root AGENTS.md holds the upstream maintainer's Windows preferences, which do not apply here. Worked example: `~/ai-society/softwareco/owned/niri-desktop-continuity/docs/announce`. When the video tool is not chosen yet, load `make-video` first: it routes between Director, FrankenManim, Manim CE, Pillow and Chromium capture, and adds narration timing and the audio pass. |
