---
name: softwareco-contrib-repo-router
description: Routes tasks to the right repo under /home/tryinget/ai-society/softwareco/contrib, the lane of upstream clones and forks kept as tools or sources, from any working directory. Use when the operator names a contrib repo or path, or a task needs an upstream tool kept there, such as Director for rendering video. Do not use for owned or infra repos (softwareco-owned-repo-router, softwareco-infra-repo-router) or for sending a fix upstream (softwareco-contrib-upstream).
---

# Softwareco Contrib Repo Router

## Boundary

- Contrib repos are upstream code. Use them; do not edit them in place. A change for upstream
  follows `softwareco-contrib-upstream`.
- This skill selects a repo and hands off. The repo's own docs and its domain skill own the work.

## Workflow

1. Read `/home/tryinget/ai-society/softwareco/contrib/docs/project/repo-capability-map.md`.
2. Pick the row whose cues match the task. Read the repo's `AGENTS.md`, `README.md` and the
   read-first files the row lists.
3. When the row names a domain skill, load it next.
4. The map lists only the contrib repos in use as tools; the lane holds about 300 clones. When no
   row matches, list `/home/tryinget/ai-society/softwareco/contrib`, read the README of the one or
   two best-named candidates, and say the choice was inferred.

## Verification

Name only paths you have seen exist. Report the selected repo, why it fits, the files read first,
and the skill handed off to, if any.
