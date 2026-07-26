---
summary: "Decision 83 authority/security review attempt 2 of commit 443d45e; remaining revision required."
read_when:
  - "Reviewing Decision 83 authority/security review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-26"
decision_id: 83
reviewed_commit: "443d45e9465d9c1c0daf08ea64ef2b4cea5359b9"
dispatch_id: "dispatch-1785089589502"
---

# Decision 83 authority/security rereview — attempt 2

## Verdict

**REVISE.** Accepted-Git binding, fresh activation authority readback, and resolved owner-path containment were corrected. Four blockers remained:

1. stop ignored failure to terminate an in-flight main service;
2. runtime-tree digest omitted symlink identity/containment and still executed shared `/tmp` Pi code;
3. composed-prompt proof accepted prefix/substrings rather than exact dynamic prompt bytes;
4. activation, unit/package tamper, termination, and prompt-drift negative controls remained incomplete.

## Required correction

Verify main-service inactivity before stopped state; copy digest-pinned Pi/Pi Modes trees into the accepted bundle and hash/reject escaping symlinks; independently reconstruct and byte-compare the complete prompt; and add executable negative tests for these boundaries.

This attempt's verdict remains `REVISE` regardless of later corrections.
