---
summary: "Adversarial re-review of the revised Software Factory Flow Protocol RFC after the first four-track synthesis."
read_when:
  - "Determining what remains before the revised RFC can become ADR-ready."
type: "review-attempt"
---

# Re-review — revised Software Factory Flow Protocol RFC

## Review chain status

- review kind: re-review after `revise_rfc`
- reviewed artifact: `docs/project/2026-07-12-software-factory-operating-system-rfc.md`
- reviewed SHA-256: `c38781f27f95b2d9bd85dc9a8996a89307ae4ac7fa06f661df283e28bdaf6a04`
- method: Prompt Vault `layer12-070-decision-rfc-review`
- supporting docs: problem/evidence notes, four v0 attempts, v0 synthesis, canonical decision lifecycle
- ADR legal now?: no

## Lenses

1. blocker resolution, authority, and falsifiability;
2. operator and reliability viability;
3. lifecycle legality and remaining evidence.

## Resolution assessment

| v0 blocker | Status in reviewed revision |
|---|---|
| Authority | partial: matrix added, but appointments and some field ownership remained conditional |
| Projection safety | resolved in design |
| Flow economics | resolved in design |
| Customer/outcomes | partial: preregistration exists; selected pilot/evidence absent |
| Reliability | resolved in design; operational proof absent by design |
| Measurement | resolved in design |
| Rollback | resolved in design |
| Lifecycle legality | unresolved: artifacts are untracked |

## Remaining blockers

1. Select the pilot and provide direct segment/problem/workaround/outcome evidence.
2. Identify the lawful appointing authority and record delegation for steward, outcome owner, product/service owner, release authority, and incident authority.
3. Provide a worked packet and command/path operator journey.
4. Track the artifact chain and conduct a new immutable review/synthesis against that tracked revision.

The review also found residual terminal-token and canonical-record inconsistencies. Those textual defects were corrected immediately after this reviewed hash; that follow-up does not change the controlling outcome because pilot evidence, authority grants, operator proof, and tracked lifecycle artifacts remain absent.

## Workflow result

- review_outcome: `revise_rfc`
- next legal move: `gather_missing_artifacts`, then revise/track/re-review
- controlling rationale:
  - generic protocol architecture is materially stronger and directionally viable;
  - the requested ADR would authorize a concrete pilot that has not been selected or lawfully staffed;
  - operability is specified as a gate but not yet demonstrated;
  - untracked artifacts cannot establish ADR legality.

## Final recommendation

Keep the RFC in draft. Produce the pilot-selection evidence and authority/delegation packet, add the worked operator journey, track the chain, and run a new controlling review synthesis.
