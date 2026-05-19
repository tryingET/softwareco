---
summary: "Softwareco root handoff: repair the L1 control-plane drift bundle before broader template/lane work."
read_when:
  - "Starting work from ~/ai-society/softwareco"
  - "Before trying to fix root template CI drift"
---

# Next Session Prompt — softwareco (root)

## Mission
Repair the **root L1 control-plane drift** so the repo contents, top-level docs, and `scripts/check-template-ci.sh` agree again.

## Drift to fix
`bash ./scripts/check-template-ci.sh` expects a lane-bootstrap bundle that root currently lacks or does not document consistently:

- `scripts/bootstrap-lane-root.sh`
- top-level `AGENTS.md` mention of the helper
- top-level `README.md` mention of the helper
- `scripts/install-hooks.sh` alignment with the helper

Important: root `AGENTS.md` / `README.md` in softwareco are company-policy flavored, so **do not blindly overwrite them**. Reconcile them with the expected L1 control-plane contract.

## Read first
- `AGENTS.md`
- `README.md`
- `scripts/check-template-ci.sh`
- `scripts/bootstrap-lane-root.sh`
- `scripts/install-hooks.sh`
- `copier/tpl-project-repo/next_session_prompt.md`

## Canonical references
Use these as the source of truth / passing reference:

- canonical fixture: `~/ai-society/core/tpl-template-repo/fixtures/l1/template-repo/`
- passing sibling repo: `~/ai-society/holdingco/`

Focus only on this bundle:

- `scripts/bootstrap-lane-root.sh`
- `scripts/install-hooks.sh`
- `AGENTS.md`
- `README.md`

## Preflight
From `~/ai-society/softwareco`:

```bash
git status --short
bash ./scripts/check-template-ci.sh || true
rg -n "bootstrap-lane-root\.sh" AGENTS.md README.md scripts/install-hooks.sh scripts/check-template-ci.sh
ls scripts | sort
```

## Repair slice
- Sync only the control-plane bundle above.
- Prefer copying/adapting from the L0 fixture or `holdingco` reference.
- Keep company-specific lane wording intact where intentional.
- Do **not** mix this with unrelated lane-root churn or helper propagation.
- Do **not** broad-recopy the whole repo for this task.

## Validate
Run:

```bash
bash ./scripts/check-template-ci.sh
```

Then confirm the helper is now wired end-to-end:

```bash
rg -n "bootstrap-lane-root\.sh" AGENTS.md README.md scripts/install-hooks.sh scripts/check-template-ci.sh
```

## After root is healthy
Only then continue into lane-level work:
- `owned/next_session_prompt.md`
- `infra/next_session_prompt.md`
- `contrib/next_session_prompt.md`
