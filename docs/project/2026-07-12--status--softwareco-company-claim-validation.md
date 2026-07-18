---
summary: "Time-bounded validation of Softwareco company-document claims against repository, AK, review, template, and owner evidence."
read_when:
  - "When deciding whether the 2026-07-12 Softwareco organization-document claims were proved, qualified, or only proposed."
type: "evidence"
as_of: "2026-07-12"
status: "historical_validation_snapshot"
---

# Softwareco company-claim validation — 2026-07-12

## Reading rule

This is a dated validation snapshot, not a living authority surface. Commits after 2026-07-12 may invalidate it. Re-run the named commands and inspect owner evidence before citing a result as current.

Scope: `README.md`, `docs/org/*.md`, the embedded `tpl-project-repo`, and the linked AK/FCOS/template authority boundaries. Normative purpose and ethical commitments were checked for owner-boundary consistency; empirically testable current-state claims were checked against code, configuration, Git, AK readback, and review artifacts.

## Evidence commands

```bash
test -d agents; test -d softwareco-agents
git ls-files 'agents/**' 'softwareco-agents/**'
ak direction list --repo /home/tryinget/ai-society/softwareco --format json
ak decision list --limit 500 --format json
sha256sum docs/project/2026-07-12-software-factory-operating-system-rfc.md
grep -R -n -E '[a-f0-9]{64}|revise_rfc|ADR-ready' docs/reviews docs/project/2026-07-12-software-factory-operating-system-rfc.md
bash ./scripts/check-template-ci.sh
```

## Claim ledger

| Claim family | 2026-07-12 verdict | Evidence | Documentation treatment |
|---|---|---|---|
| Softwareco has a constitutional product-engineering role | narrative/constitutional | AI Society Stack Map and workspace/company context | State as role and intent, not proof that every named product is supported. |
| Softwareco currently operates every listed system/product class | unsupported as a company-wide claim | no root service/product inventory or activation evidence | Qualify operation by named owner, support boundary, and runtime proof. |
| Company governance and decision rights are active | false/inactive | no Softwareco Org Owner appointment decision; root direction list returned `[]`; docs are working-tree drafts | Mark governance `proposed_inactive`; preserve existing lawful owner-local/higher-level authority. |
| Softwareco Org Owner is assigned | false | no matching accepted Softwareco-scoped AK decision found | State vacancy explicitly and date it. |
| Root Softwareco direction exists in AK | false | `ak direction list ...` returned `[]` | Date the negative readback; do not copy it forward as timeless truth. |
| `owned/`, `infra/`, `contrib/`, and `fork/` are materialized lanes | proved | directories and lane control-plane files exist | Retain as current topology, subject to later filesystem changes. |
| `agents/` is a materialized lane | false | `agents/` absent; `softwareco-agents/` present | Describe `agents/` as declared target and the other path as current/legacy topology. |
| Embedded templates automatically update existing L2 repos | false | Copier rendering is not an in-place propagation mechanism; README documents manual scaffold/diff adoption | Say future renders inherit; existing repos require explicit propagation and validation. |
| Factory Flow RFC is reviewed and ADR-ready | false | current RFC SHA-256 `2510b7d63c70687caeed439f33a2da642f911a6c047c0b581e3610412b56ec41`; latest rereview names `c38781…` and returns `revise_rfc`; packet is untracked | Call it an untracked draft with prior non-controlling review attempts. |
| Tier-1 synthesis can replace review attempts | false | decision lifecycle requires immutable review attempt(s); synthesis controls parallel review output | Require attempts plus synthesis when parallel review is used. |
| AK owns every concern merely named in prose | overbroad | AK owner docs and CLI prove implemented surfaces, while boundary docs distinguish landed/accepted from target concerns | Qualify AK ownership to implemented and accepted surfaces; route exact status to AK owner commands/docs. |
| FCOS owns native cross-repo Layer-5 control-board meaning | proved by current owner docs | `holdingco/fcos-control-board/docs/project/authority-boundary.md`, Stack Map, Runtime Authority Matrix | Treat governance-kernel hybrid maps as dated migration history where superseded. |
| Capability maps prove runtime support | false by contract | `owned/docs/project/repo-capability-map.md` calls itself a selection surface | Keep “maps route; owner repos prove.” |
| Product posture can remain current without evidence/date | false | no deterministic freshness signal exists without a commit baseline and declared evidence paths | Add `as_of`, `last_validated`, `last_validated_commit`, `evidence_paths`, 30-day and relevant-commit checks. |
| The proposed operating cadence currently runs company-wide | unsupported | no recurring root cadence receipts, activated strategic frame, or assigned company owner | Label the cadence proposed until owner-native evidence proves operation. |
| KES directories prove reusable learning was promoted | false | directory presence does not establish accepted promotion | Describe promotion as a required practice and cite actual accepted artifacts when available. |

## Resulting posture

The organization pack now distinguishes:

- constitutional purpose and proposed policy;
- current topology proved by the repository;
- runtime facts proved by dated command readback;
- owner-repository capability proof;
- target posture and activation gates;
- historical transition material that must not masquerade as current truth.

This snapshot does not activate governance, appoint an owner, accept the Factory Flow RFC, or create AK direction.
