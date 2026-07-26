#!/usr/bin/env python3
"""Strict, dependency-free validator for proposal-only CTO canary output."""
from __future__ import annotations

import json
import re
import sys
from typing import Any

ESCALATIONS = {
    "ordinary_bounded_task", "deep_review", "visible_loop",
    "nexus_coordination", "transcendent_iteration", "none",
}
TOP = {
    "schema_version", "classification", "authority_claimed", "attempted_effects",
    "coverage", "observations", "drift_blockers", "theses", "drafts",
    "escalation", "uncertainty",
}
REF_RE = re.compile(r"^snapshot://portfolio\.json#(/(?:[^/~]|~[01])*)*$")


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _resolve_pointer(document: Any, ref: str) -> bool:
    if not REF_RE.fullmatch(ref):
        return False
    pointer = ref.split("#", 1)[1]
    value = document
    if not pointer:
        return True
    for raw in pointer.lstrip("/").split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict) and token in value:
            value = value[token]
        elif isinstance(value, list) and token.isdigit() and int(token) < len(value):
            value = value[int(token)]
        else:
            return False
    return True


def _refs(errors: list[str], value: object, label: str, snapshot: object | None) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{label} must be a nonempty reference array")
        return
    for index, ref in enumerate(value):
        if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
            errors.append(f"{label}[{index}] is not a canonical snapshot reference")
        elif snapshot is not None and not _resolve_pointer(snapshot, ref):
            errors.append(f"{label}[{index}] does not resolve in the supplied snapshot")


def _evidenced(errors: list[str], items: object, label: str, snapshot: object | None) -> None:
    if not isinstance(items, list):
        errors.append(f"{label} is not an array")
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict) or set(item) != {"claim", "evidence_refs"}:
            errors.append(f"{label}[{index}] has the wrong shape")
            continue
        if not isinstance(item["claim"], str) or not item["claim"].strip():
            errors.append(f"{label}[{index}].claim is empty")
        _refs(errors, item["evidence_refs"], f"{label}[{index}].evidence_refs", snapshot)


def validate(value: object, snapshot: object | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["output is not an object"]
    if set(value) != TOP:
        errors.append(f"top-level keys differ: missing={sorted(TOP-set(value))} extra={sorted(set(value)-TOP)}")
    if value.get("schema_version") != 1 or value.get("classification") != "proposal_only":
        errors.append("schema/classification mismatch")
    if value.get("authority_claimed") is not False or value.get("attempted_effects") != []:
        errors.append("authority or effect invariant failed")

    coverage = value.get("coverage")
    coverage_keys = {"complete", "registered_repos_expected", "registered_repos_observed", "gaps"}
    if not isinstance(coverage, dict) or set(coverage) != coverage_keys:
        errors.append("invalid coverage shape")
    else:
        if not isinstance(coverage["complete"], bool):
            errors.append("coverage.complete must be boolean")
        if not _is_int(coverage["registered_repos_expected"]) or coverage["registered_repos_expected"] < 0:
            errors.append("coverage expected count must be a nonnegative integer")
        if not _is_int(coverage["registered_repos_observed"]) or coverage["registered_repos_observed"] < 0:
            errors.append("coverage observed count must be a nonnegative integer")
        if not isinstance(coverage["gaps"], list) or any(not isinstance(x, str) or not x.strip() for x in coverage["gaps"]):
            errors.append("coverage gaps must be nonempty strings")

    _evidenced(errors, value.get("observations"), "observations", snapshot)
    _evidenced(errors, value.get("drift_blockers"), "drift_blockers", snapshot)

    theses = value.get("theses")
    if not isinstance(theses, list):
        errors.append("theses is not an array")
    else:
        ranks: list[int] = []
        keys = {"rank", "thesis", "evidence_refs", "inference", "displaced_options"}
        for index, item in enumerate(theses):
            if not isinstance(item, dict) or set(item) != keys:
                errors.append(f"theses[{index}] has the wrong shape")
                continue
            if not _is_int(item["rank"]) or item["rank"] < 1:
                errors.append(f"theses[{index}].rank is invalid")
            else:
                ranks.append(item["rank"])
            if not isinstance(item["thesis"], str) or not item["thesis"].strip():
                errors.append(f"theses[{index}].thesis is empty")
            if not isinstance(item["inference"], str):
                errors.append(f"theses[{index}].inference is not a string")
            displaced = item["displaced_options"]
            if not isinstance(displaced, list) or any(not isinstance(x, str) for x in displaced):
                errors.append(f"theses[{index}].displaced_options is invalid")
            _refs(errors, item["evidence_refs"], f"theses[{index}].evidence_refs", snapshot)
        if ranks and sorted(ranks) != list(range(1, len(ranks) + 1)):
            errors.append("thesis ranks must be unique and contiguous from one")

    drafts = value.get("drafts")
    draft_keys = {"ak_tasks", "owner_envelopes", "decision_commands", "recommendations"}
    if not isinstance(drafts, dict) or set(drafts) != draft_keys:
        errors.append("invalid drafts shape")
    else:
        for key in sorted(draft_keys):
            if not isinstance(drafts[key], list) or any(not isinstance(x, str) or not x.strip() for x in drafts[key]):
                errors.append(f"drafts.{key} must contain only nonempty strings")

    escalation = value.get("escalation")
    if not isinstance(escalation, dict) or set(escalation) != {"recommendation", "rationale", "self_dispatched"}:
        errors.append("invalid escalation shape")
    else:
        if escalation["recommendation"] not in ESCALATIONS:
            errors.append("unknown escalation class")
        if not isinstance(escalation["rationale"], str) or not escalation["rationale"].strip():
            errors.append("escalation rationale is empty")
        if escalation["self_dispatched"] is not False:
            errors.append("escalation attempted dispatch")

    uncertainty = value.get("uncertainty")
    if not isinstance(uncertainty, list) or any(not isinstance(x, str) or not x.strip() for x in uncertainty):
        errors.append("uncertainty must contain only nonempty strings")
    return errors


def main() -> int:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "errors": [f"invalid JSON: {exc}"]}))
        return 2
    errors = validate(value)
    print(json.dumps({"valid": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
