---
summary: "Coordination-only post-ADR task fanout for Decision 144 candidate C."
read_when:
  - "Creating or sequencing Decision 144 implementation tasks."
type: "plan"
status: "accepted"
date: "2026-08-31"
decision_id: 144
governance_task_id: 5251
---

# Candidate C owner-task fanout

## Contract

This artifact coordinates exact future tasks. It creates no task, delegation, mutation, publication,
or completion authority. AK remains canonical. Materialize each task separately with bounded scope,
link it to Decision 144 as `post_adr_execution`, and stop on any prerequisite drift.

## Ordered task A — targeted materializer and hard CI gate

**Owner:** Softwareco parent integration.

**Outcome:** an atomic ontology-only materializer plus hard missing-manifest/fresh-checkout gates.

**Typical scope:** parent materializer script/library, exact tests, `scripts/ci/full.sh`,
`check-template-ci.sh`, `../../.github/workflows/ci.yml`, and narrowly required docs/contracts. It must not
stage `ontology/**` or receipt paths.

**Required evidence:**

- exact source/OID/remote verification;
- targeted activation only;
- unavailable/wrong/interrupted/no-partial failures;
- generic recursive initialization never invoked;
- uninitialized root gate fails;
- idempotent rerun and rollback;
- unrelated WIP and owner refs/stashes preserved.

## Ordered task B — parent receipt identity and consumer migration

**Depends on:** task A.

**Owner:** Softwareco parent receipt/CI integration; ROCS semantics remain unchanged unless a separate
ROCS-owner task is proven necessary.

**Outcome:** regenerate and relocate the six parent receipts to
`governance/ontology-dist/`, with every producer/consumer/path/identity/rollback binding migrated.

**Typical scope:** six old/new receipt paths, parent producer/gates, exact consumers, fixtures/docs,
and receipt tests. It must not convert the ontology tree to a gitlink.

**Required evidence:** parent identity, no old active consumer, owner CI leaves parent outputs
unchanged, consumer validations update only their own pairs, and evidence `8040` remains the causal
record.

## Ordered task C — ownership transition and exact C adoption

**Depends on:** tasks A and B.

**Owner:** Softwareco parent topology/ownership integration.

**Outcome:** execute a new post-AK-5197 ownership map/state plan and adopt true candidate C.

**Required scope classes:**

- `.gitmodules` and mode-`160000` `ontology` relation;
- deterministic ownership manifest/plan/state/receipt artifacts;
- narrowed `../../contracts/template-ownership.yml` and its externally receipted state transition;
- reviewed removal of ordinary parent ontology paths;
- only plan-classified receipt/materializer/gate updates not already landed.

**Required evidence:** exact published owner OID/tree, complete path/mode/deletion plan, no ambient
`.git`/stash/local refs, strict gates, pending/external/final state binding, pre/post bundles, and
exact preservation of unrelated issue-tracker/owner WIP. Current 31 ontology WIP entries are compared
against source and plan; they are not staged ad hoc. Scratch commit `016cf156…` is never
cherry-picked.

## Ordered task D — independent fresh-checkout review and closeout

**Depends on:** task C candidate commit.

**Owner:** independent review/validation with Softwareco owner closeout.

**Outcome:** prove fresh uninitialized failure, targeted exact materialization, strict owner/root and
all consumer gates, unavailable-source atomicity, receipt identity, ownership receipt, rollback, and
clean parent/owner truth.

**Required evidence:** independent verdict, complete logs/hashes, current AK/Decision readback,
verified bundles, root candidate ancestry, and explicit claim limits. Only an accountable operator
may authorize terminal task/rollout closeout.

## Separate, non-blocking surfaces

- Issue-tracker publication/pointer updates remain separate exact tasks.
- Root remote publication is separately authorized; the root currently has no remote.
- Healthco stays held unless separately released.
- Template-wide submodule conventions and unrelated raw gitlinks are outside this fanout.
- E selective projection requires a successor review; it is not a fallback command path.

## Global stop conditions

Stop the fanout on source/remote/owner drift, unavailable authority, ambiguous consumer or receipt
identity, non-atomic materialization, ownership hash mismatch, unexpected staged path, failed gate,
unrelated WIP mutation, missing bundle, or any proposal to force/clean/stash/rewrite owner state.
