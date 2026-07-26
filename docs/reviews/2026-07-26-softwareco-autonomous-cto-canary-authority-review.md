---
summary: "Decision 83 authority/security review attempt 1 of commit 3c551c4; revision required."
read_when:
  - "Reviewing Decision 83 authority/security review lineage."
type: "review"
status: "revise_rfc"
date: "2026-07-26"
decision_id: 83
reviewed_commit: "3c551c4f8ded86487bef10b2d52f385aab13bc8e"
dispatch_id: "dispatch-1785087681543"
---

# Decision 83 authority/security review — attempt 1

## Verdict

**REVISE.** Commit `3c551c4f8ded86487bef10b2d52f385aab13bc8e` was not ready for acceptance or activation.

## Blocking findings

1. Bundle manifest and rendered user units were self-attested and mutable rather than compared with accepted Git objects.
2. Activation could write a human-attributed receipt without fresh decision/acceptance readback.
3. In-flight workers could continue after expiry or direct-human stop.
4. raw prefix matching allowed a registered path/symlink to resolve outside `softwareco/owned`.
5. worker process inherited broad environment/home/network capability and pinned only a self-reported Pi version.
6. mode proof did not bind project source path, semantic fingerprint, or composed prompt identity.
7. required installer, activation, tamper, expiry, path-escape, and mode-source negative controls were absent.

Nonblocking findings covered unrestricted draft semantics, subprocess output memory, and fixture runs that did not actually spawn the fixture RPC worker.

## Required correction

Bind the honest runtime's files and units to accepted Git objects; reread authority before activation; cap/kill in-flight workers at the authority deadline; resolve every owner path under the real owned root; hide general home state and filter environment; pin Pi and Pi Modes trees; prove exact preview source/fingerprint/dynamic context; stream probe output to bounded files; spawn true fixture workers; and add negative tests.

This memo records attempt-1 review lineage only. Later source changes require a new review; they do not change this verdict.
