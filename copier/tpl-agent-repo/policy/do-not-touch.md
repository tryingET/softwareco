---
summary: "Hard rules: data + files this agent must not touch."
read_when:
  - "When the agent is about to edit core/governance paths"
---

# Do Not Touch

- Never commit secrets or tokens.
- `docs/_core/**` is immutable (core snapshot/submodule).

