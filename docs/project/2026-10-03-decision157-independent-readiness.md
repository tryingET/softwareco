---
summary: "AK6562 proves bounded parent/ontology archive restoration and refreshes ten registered consumer roots; owner dispositions, excluded WIP and cutover readiness remain open."
read_when:
  - "Continuing Decision157 consumer classification or preservation and restore work."
  - "Binding fresh source identities before the Softwareco ontology cutover."
type: "reference"
status: "verified-bounded"
date: "2026-10-03"
decision_id: 157
governance_task_id: 6562
---

# Decision157 independent readiness — bounded proof, not cutover

## Scope and authority

The operator selected independent consumer classification and preservation/restore work. AK6562
is a parallel prerequisite, not a release of AK5651 deferral346. It changes only this note in the
canonical checkout. AK6451/6452 are done; their existing implementations were not duplicated.

[ADR157](../decisions/2026-09-11-softwareco-ontology-consolidation.md) and its
[ordered plan](2026-09-11-softwareco-ontology-consolidation-plan.md) still control cutover. The
[AK6451 inventory](2026-10-02-decision157-consumer-census.md) remains historical evidence, not
current complete consumer coverage. AK owns lifecycle/decisions; Git binds source; source owners
retain semantic, runtime, template and publication authority.

No source de-nesting, consumer edit, admission, receipt generation, publication, push, stash,
reset, recursive submodule update or dirty-work cleanup was performed by this controller.

## Exact captured source identities

| Identity | Captured value |
|---|---|
| Parent HEAD | `29215ab1ffab272aa1e75a27d09f27664ee0b283` |
| Parent tree | `d2f3b53dc3e19588e01907584ad2844ee8b76d6d` |
| Parent ontology gitlink | `b2e42daf61a889c08745b922056b627753f45a2c` |
| Nested ontology HEAD | `6f6ae61bc70d8cf4dbd0f0c2b9b44609b736b74e` |
| Nested ontology tree | `51fb4ad233dd1e0ba6db6a0f79df94eec0d1f432` |

The nested source is not the parent's pinned source. AK6533 independently completed the nested
system4d correction; its changed source was preserved, not absorbed into the fold. This report's
later commit changes parent identity again. Rebind exact inputs before any future integration.

## Private preservation and isolated restore

Evidence is outside Git in task-owned private storage. Raw Git configuration, reflogs, objects,
ignored data and private history must not be imported into the public parent.

```text
/home/tryinget/.local/state/pi-quests/tmp/AK6562preservation.bXiI6glR/
  rebound/                 final strengthened capture/restore cohort
  rebound/run-proof.sh     exact private launcher, not a live restore runbook
  rebound/RESULT.json
  rebound/RESTORE-RESULT.json
  rebound/SYNTHETIC-RESULT.json
  owner-responses.json
```

The final cohort captured the entire physically contained parent gitdir, including the ontology
module gitdir; parent tracked non-gitlink paths plus admitted parent-local ignored roots; and the
ontology worktree, including its ignored output directory. Archive entries restored with equal
content hashes, modes and types. Raw configs and external linked-worktree pointers stayed byte
exact; explicit Git arguments relocated only the isolated verification invocation.

| Captured family | Manifest members | Regular files | Bytes |
|---|---:|---:|---:|
| Parent gitdir, including ontology metadata | 632 | 404 | 5,335,696 |
| Admitted parent working files | 1,354 | 1,343 | 14,064,680 |
| Ontology worktree | 69 | 54 | 238,562 |

Results:

- **2,055** manifest rows agree with archives and raw/active restore trees.
- Exact HEAD/tree, index, HEAD symbolic ref and all listed refs restore: **19 parent**, **18 ontology**.
- Both repositories pass fsck with and without reflog roots. Complete all-ref bundles verify;
  independent mirror restores retain every listed ref OID and pass fsck.
- The dirty parent adoption dashboard and scan JSON restore byte-exactly; they were not staged,
  replaced or treated as disposable generated data.
- Restore verification ran with the canonical parent and recorded external linked worktree hidden,
  in a distinct network namespace. Launcher, mount evidence and assertions are retained. The host
  root mount was read-only; this proves the selected command/path isolation, not arbitrary-code
  whole-host containment through every mount.
- A separate disposable fixture proves eight positive controls: staged index bytes distinct from
  worktree bytes, unstaged tracked data, untracked data, ignored data, symlink target, executable
  mode, status equality and fsck. These controls are not additional live-WIP coverage.

Final archive SHA-256 values:

| Archive | SHA-256 |
|---|---|
| Metadata | `d76895e1bedda4a26e6aee92b8fc57037a1c88688a0cf07b3db9b5fd7176ad40` |
| Parent worktree | `82289438885e30e6389e7b98aa2732d8f9c43773e138521c1b2ee29d66d989f6` |
| Ontology worktree | `3c0bf3eed75c203032582fd20afe14b7534221d554a77be4c77c93876d23f907` |

### Preservation exclusions and freshness

**389 parent ignored candidates** remain outside this archive. These include independently
operated repositories and large retained scratch. Other gitlink child worktrees and an external
linked worktree's WIP are not restored. Their metadata pointers remain inert. No exclusion is
permission to delete or retire its owner. The private result lists every omitted candidate.

Before/after hashes, membership checks and source-state comparisons are optimistic observations,
not a writer fence. Parent object members grew from 224 to 272 between the earlier and final
cohorts despite equal HEAD/ref/index/WIP observations. The cohorts are deliberately not equated.

After capture, the separate AK6515 worker reported creating a clean linked task worktree and branch.
It retained that state inert and moved candidate execution to a standalone no-hardlinks clone.
Consequently this archive is **not current full-ref/metadata freshness**. No blanket rollback or
metadata cleanup was attempted. Rebind and pause affected writers for an actual cutover window.

This proves restoration of the captured Git/file cohort, not full ignored/external custody,
AK lifecycle recovery or parent-plus-consumer whole-wave rollback.

## Fresh bounded consumer packet

```text
/home/tryinget/.local/state/pi-quests/tmp/AK6562consumer.Pf1tkkN4/
  MAP.md
  census.json
  owner-path-map.json
  owner-routing.json
  disposition.observations.json
  coverage.json
  SHA256SUMS
```

Fresh AK export at 2026-10-03T09:35:12Z contains **354 registrations**. Eleven exact roots were
selected: parent; contrib/fork/infra/owned lanes; agent-kernel, pi-extensions, dep-diet, ts-quality,
test-capabilities; and workstation. Instruction chains were projected before admitted source reads.

Ten roots were collected: **142 origin observations**, **71 Gitroot/path identities**, **63 physical
paths**. The remaining 343 registrations were not source-inspected. Workstation source inspection
was omitted under its exact-path context rule. The parent ontology-manifest working read was
blocked at the nested-repository boundary; the separate preservation proof is not a replacement
consumer-contract inspection.

Eight parent/lane shadow input pairs must retain separate index attribution. Seven indexes match;
the fork Copier-answer pair differs. Parent/lane duplication does not create two physical consumers
or establish which owner executes the generation input.

Two differing generations require hash-bound owner disposition:

| Path | Observed difference, not authorization |
|---|---|
| Fork Copier answers | Kernel ontology ref field differs; locator class sets unchanged |
| Pi-extensions resolution projection | Version field differs; locator records/classes unchanged |

All 142 origin disposition rows remain unresolved. No scanner pattern, path shape or unchanged
locator class establishes active use, fixture status, migration approval or exclusion. Receipt
readers/writers, executable entrypaths and generator convergence were not closed by this subset.

### Attributed owner responses

| Responding route | Established observation | Still unresolved |
|---|---|---|
| Agent-kernel coordinator, session01a1003e | Manifest configures the old company layer in repo-dev and guiding-circle profiles; manifest/projection hashes match the packet | Current resolution, normative accepted migration disposition, rebind permission |
| Pi AK6427 worker, session01a0f87e | Explicitly not monorepo/ontology owner; paths outside current scope | Accountable consumer owner and both-generation disposition |
| Workstation AK6477 controller, session01a100e7 | Audit outside current cleanup scope; no exact file set supplied | Exact owner-admitted source paths and consumer contracts |
| Ts-quality worker, session01a100cd | Exact manifest/Copier hashes and index OIDs match packet; no input drift | Active/lineage/fixture/archive classification; separate AK6547 witness scope remains protected |

The agent-kernel response is useful **configured-use technical evidence**, not a verified current
ROCS resolution or accepted migration decision. Its author explicitly retains normative disposition
as unclassified. Peer responses confer no mutation permission.

The collector itself is unchanged. Its guarded subset runner is a retained experiment, not a new
production utility: the runner loads the collector before checking its hash and does not itself
establish bytecode-write prevention. The proposed disposition schema is not adopted policy; schema
conformance was not checked, and its retained derivation has a replay field omission. Final packet
rows do contain false mutation-authorization values. Do not mechanically replay these scripts.

## Verification and inspection boundaries

Independent inspection `dispatch-1791020886023` accepts both preservation cohorts and the bounded
consumer packet. It independently checked archive/file/bundle hashes and performed a read-only
source-hidden Git inspection on the earlier restore. Follow-up checked final artifacts, launcher,
mount evidence and 27 retained successful Git commands; it did not rerun final restoration.

Inspection first identified missing launcher provenance and traversal/config preflight weaknesses.
The final retained cohort adds fail-on-error traversal, pre-Git config-include rejection, repeated
membership checks, end-to-end rehash and asserted isolation; it passed afresh. Generic config.worktree
handling and adversarial race/error tests remain outside coverage. The live cohorts contain no
symlinks/hardlinks; only the separate synthetic fixture exercises a symlink.

The inspector reported an initial status probe under owned/ontology outside the selected roots,
without optional-lock suppression. Incidental index refresh cannot be excluded. This deviation is
retained in the private response ledger; no canonical cleanup or no-incidental-write assertion is
inferred from that inspection. Follow-up was restricted to private artifacts.

The existing collector's **21 fixtures pass afresh** under read-only-host/private-scratch execution,
with bytecode writes disabled. No receipt-generating full/deep or hosted gate was run for this
readiness task; there is no source implementation delta requiring those gates by implication.

## Remaining execution obligations

1. **AK5651:** accountable dispositions for all actual consumer/generator variants, omissions,
   index generations and parent/lane shadows; fresh generator/update and receipt contracts.
2. **AK5651:** custody of excluded ignored/external/other-owner WIP and a writer-fenced fresh
   preservation binding, then AK-owner lifecycle and whole-wave rollback rehearsal.
3. **AK6471/5665:** separately reviewed runtime promotion and install/schema/campaign admission.
   Source publication or synthetic proof alone is not installation or campaign consent.
4. **AK6270:** exact owner-supported transition, retained corpus/exclusions, disclosure check,
   coordinated source/consumer cutover and verification. Publication permission already exists
   in evidence11643/11644, conditional on the fresh exact tree; private history remains excluded.
5. **AK5502:** actual publication followed by fresh hosted verification. Credential restoration
   remains superseded, not an instruction to provision secrets.

AK6515 is separate ROCS consumer CI adoption. Verification evidence12893 found the committed and
working CI still pinned to v0.4.4 and both ba73f466 bindings despite public v0.4.6 availability.
Evidence12903 subsequently authorized its isolated candidate only. Its worker owns a separate scope;
this task performs no pin change, landing or fleet rollout and does not claim candidate success.
