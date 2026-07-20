---
summary: "Owner decision authorizing physical deletion of the retired fcos-proving-lane working repository after final recoverability capture."
read_when:
  - "Reviewing why fcos-proving-lane was physically removed after Factory Flow pilot 001."
type: "decision"
status: "accepted"
decision_id: 66
supersedes_deletion_limit_in_decision: 62
---

# Delete retired `fcos-proving-lane`

## Decision

The human operator explicitly instructed: **“just delete fcos-proving-lane repo.”**

Physical deletion of `softwareco/owned/fcos-proving-lane` is therefore authorized after a final recoverability capture and verification. This narrowly supersedes Decision 62's no-physical-deletion limit; it does not reactivate the repository or change native FCOS authority.

## Preconditions

1. Preserve the final repository state, Git refs, and dirty worktree in a new archive.
2. Verify the archive hashes and Git bundle.
3. Keep the earlier pilot-001 archive intact.
4. Do not run `ak repo delete`, because that command cascades historical tasks and evidence. The AK registration remains a historical locator.

## Execution effects

- remove the physical `owned/fcos-proving-lane/` directory;
- refresh owned engineering-core adoption projections;
- preserve current FCOS authority at `holdingco/fcos-control-board`;
- preserve Decision 62, task history, evidence, and both recovery archives.

## Recovery

Restore the final archive into `softwareco/owned/fcos-proving-lane`, verify its manifest and Git bundle, and re-run repository validation. Restoration does not itself reactivate the repo as a product.
