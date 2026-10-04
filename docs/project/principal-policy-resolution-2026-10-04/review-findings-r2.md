---
summary: "Preserved R2 author self-inspection findings: parent-exception consumption scope and cross-permit verification, plus three improvements and four questions."
read_when:
  - "Tracing the targeted R3 revision without rewriting R2 or claiming independent inspection."
type: "reference"
status: "historical-author-self-inspection-not-legal-review-outcome"
task: "AK6635"
decision_id: 173
as_of: "2026-10-04"
---
# R2 findings preserved

The operator requested a second architecture review. The same author/controller
reviewed R2, its incorporated contract, evidence and the V05 fixture rows, and reported
**revise before ADR** in chat. This is author self-inspection, not an independent
native review attempt/closure. No legal review outcome was recorded from it.

Subject remains [R2 RFC](resolution-rfc-r2.md), [R2 contract](contracts-r2.md) and
`OUTPUTS-R2.sha256`. Their bytes are retained. The R2 direction and identity/rights
improvements were accepted by the self-inspection as substantially sound; the
remaining blocker was narrow, not a request to redesign the architecture.

## Must-fix findings

- M1: name the authoritative exception/start-right unit and its relationship to
  permits/attempts; per-permit atomic reservation is insufficient.
- M2: a new permit ID cannot renew the consumed O3 right or hide another start.
- M3: a replacement attempt needs fresh applicable O3 template-owner disposition,
  not only O6 execution material or the same person acting in the wrong capacity.
- M4: add different-permit/shared-parent and post-partial-birth counterexamples,
  including clear original recovery versus new-start expectations.

## Nice-to-have improvements

- N1: distinguish current creator/executor identity from prospective Principal subject.
- N2: retain an exact reproducible construction-check command/artifact, not only its result.
- N3: show exception -> permit -> attempt -> artifact in one compact diagram.

## Four reviewer questions

- Q1: Which owner record says the exception's start entitlement is spent?
- Q2: Can O6 issue another permit against that same O3 disposition?
- Q3: What exact authority permits a new attempt after an interrupted admitted birth?
- Q4: How does verification distinguish original recovery from another start?

[R3 evidence](evidence-r3.md) dispositions these proposal findings and distinguishes
construction checks from actual owner/admission/fencing proof. No expert-school
argument, file hash or self-inspection is accepted policy or independent closure.
