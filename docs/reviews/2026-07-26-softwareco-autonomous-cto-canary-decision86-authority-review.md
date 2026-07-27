---
summary: "Decision 86 authority/security review of corrective commit 2c7659e; outcome revise_rfc."
read_when:
  - "Reviewing Decision 86 corrective review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-27"
decision_id: 86
review_track: "authority_security"
reviewed_commit: "2c7659ef74ef7cb4128f2c0defc860238e9eee74"
dispatch_id: "dispatch-1785173240783"
---

# Decision 86 corrective authority/security review

## Outcome

`revise_rfc`

## Material findings

1. The packet and watched-state gate hashed only the main DB, so WAL-only AK mutations could evade drift detection.
2. Runtime and stop used `chain[-1]` although AK governance lists newest-first.
3. Predecessor archiving did not require exact Decision 83 activation/stop receipts and full human receipt semantics.
4. The model service inherited a read-only bind of the whole `~/ai-society` workspace.

## Required correction

Fingerprint DB and WAL; use and test the newest control head; require exact predecessor receipts `9189`/`9201`; and separate narrow non-networked DB/WAL staging from the model service.
