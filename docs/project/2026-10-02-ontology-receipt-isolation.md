---
summary: "AK6452 corrects receipt tests for isolated parent checkouts and canonical core aliases while preserving wrong-source and scratch-snapshot rejection."
read_when:
  - "Running Softwareco full validation in a TMPDIR checkout with a fresh HOME."
type: "reference"
status: "verified-isolated"
date: "2026-10-02"
governance_task_id: 6452
---

# Receipt tests in isolated checkouts

Task6451's isolated full gate passed ROCS cleanup/strict validation/build and the materializer
suite, then failed an existing receipt assertion. The test compared the core checkout to its
fresh-HOME symlink spelling rather than the actual canonical path; with canonical HOME it then
rejected the valid isolated parent path merely because it contained the workstation TMPDIR name.

AK6452 changes only the receipt test, not runtime, source, output policy or receipt production:

- Resolve the expected core checkout to its canonical filesystem identity.
- Retain exact parent, company, workspace-core and receipt/ref/tree assertions.
- Exempt only whole JSON string values equal to the independently asserted parent/company paths,
  plus the independently asserted workspace-core path. Do not strip arbitrary path prefixes.
- Continue rejecting unrelated scratch references and hash-named scratch snapshots. A suffix alone
  does not bind a snapshot's root; the previous scratch-snapshot rejection is unchanged.

Independent inspection `dispatch-1790966572098` first rejected an overbroad snapshot exemption.
After correction it returned GO: three synthetic tests and 42 mocked full identity checks passed,
including the original wrong-source snapshot reproduction. No runtime/source effect was claimed.
An existing limitation remains: non-scratch snapshot paths are suffix-checked, not newly proven
by this test change.

Independent tester `dispatch-1790965971854` recopied the exact candidate into the isolated clone:
the declared full gate then exited 0, including strict ROCS validation/build and active receipt
tests. Thirty focused tests passed with TMPDIR present and absent. Three optional real-UBS tests
and one obsolete-bundle test remain skipped; no deep or hosted result is claimed.

Private retained execution reports, deliberately outside Git:

```text
/home/tryinget/.local/state/pi-quests/tmp/ak6451-verify.TA804GBE/REPORT.md
/home/tryinget/.local/state/pi-quests/tmp/ak6451-verify.TA804GBE/rerun-ak6452/REPORT.md
```

Earlier failure evidence remains unchanged.
No generated canonical receipts, ontology source, private credential, repository visibility or
consumer configuration was changed.
