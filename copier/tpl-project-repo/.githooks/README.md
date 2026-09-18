# Git hooks

Enable in a new clone:

```bash
./scripts/install-hooks.sh
```

`pre-commit` runs `softwareco/scripts/ubs-staged.sh` on staged files when that
script exists. It does not replace repo-specific checks you add later.
