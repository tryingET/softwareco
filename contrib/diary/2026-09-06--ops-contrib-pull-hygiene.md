---
summary: "Contrib pull hygiene: sandboxed the hourly pull, parked diverged histories and loose edits on local/ branches, kept two dead-upstream repos (pic, surf-cli-go) with their remote renamed, deleted twelve dormant Dicklesworthstone repos."
read_when:
  - "The hourly contrib pull reports FAIL/WARN for a repo and you wonder whether that is new."
  - "You look for local edits or pre-rewrite history of a contrib repo."
type: "diary"
---

# Contrib pull hygiene (2026-09-06)

- `contrib-all-repos-pull.service` runs sandboxed (`scripts/systemd/contrib-all-repos-pull.service.d/hardening.conf`,
  copy next to the unit under `~/.config/systemd/user`); git globally fsck-checks fetched objects and allows only
  https/ssh/file transports. Baseline after hardening: identical ok/warn/fail to before.
- Upstream force-pushes had left `main` "diverged" in agent_flywheel_clawdbot_skills_and_integrations, dot314,
  frankentorch, misc_coding_agent_tips_and_scripts: old history kept on `local/pre-upstream-rewrite-20260906`, main
  reset to origin. obsbot-camera-control's own commit (issue 61 hardware baseline) lives on
  `local/issue-61-hardware-baseline`.
- Uncommitted edits on main in btop, codemapper, homebrew-tap, surf-cli are committed on `local/parked-edits-20260906`;
  main is clean and fast-forwards again. agnt's only remote was `upstream`; renamed to `origin`.
- Repos on feature branches with live work (OpenDeck, ddtree, pi-mono, pi-output-edquot-loop, pi-sub-maintained,
  procesio-cli) and easyllama (detached, models/) stay as they are; the pull fetches them and refuses to move them.
- `pic` (cv/pic) and `surf-cli-go` (wesen/surf-cli) vanished from GitHub; the clones stay as the only copies, remote
  renamed `dead-origin-20260906`. Deep-dive handoffs: `docs/learnings/handoffs/2026-09-06-*.md`, reports in
  `docs/learnings/2026-09-06-*-deep-dive.md`.
- Deleted (clean, no local commits, nothing running): swiss_army_llama, fast_vector_similarity, visual_astar_python,
  automatic_log_collector_and_analyzer, eidetic-engine-website-project, eidetic-engine-docs, llm_docs, llm-docs,
  tsap_mcp_server, gonode, ffn, textract-py3. 266 repos remain.
