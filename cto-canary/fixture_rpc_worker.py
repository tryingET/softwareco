#!/usr/bin/env python3
"""Deterministic no-model proposal used only by implementation tests."""
from __future__ import annotations

import json
import sys

PROPOSAL = {
    "schema_version": 1,
    "classification": "proposal_only",
    "authority_claimed": False,
    "attempted_effects": [],
    "coverage": {"complete": True, "registered_repos_expected": 2,
                 "registered_repos_observed": 2, "gaps": []},
    "observations": [{"claim": "Fixture portfolio packet was readable.",
                      "evidence_refs": ["snapshot://portfolio.json#/coverage"]}],
    "drift_blockers": [],
    "theses": [{"rank": 1, "thesis": "Keep the canary observational.",
                 "evidence_refs": ["snapshot://portfolio.json#/authority"],
                 "inference": "A proposal membrane preserves owner authority.",
                 "displaced_options": ["self-dispatch"]}],
    "drafts": {"ak_tasks": [], "owner_envelopes": [], "decision_commands": [],
               "recommendations": ["Request direct-human review."]},
    "escalation": {"recommendation": "deep_review", "rationale": "Acceptance is reserved.",
                   "self_dispatched": False},
    "uncertainty": [],
}


def main() -> int:
    for line in sys.stdin:
        command = json.loads(line)
        kind = command.get("type")
        if kind == "prompt":
            print(json.dumps({"id": command.get("id"), "type": "response", "command": "prompt", "success": True}), flush=True)
            print(json.dumps({"type": "agent_start"}), flush=True)
            print(json.dumps({"type": "agent_settled"}), flush=True)
        elif kind == "get_last_assistant_text":
            print(json.dumps({"id": command.get("id"), "type": "response", "command": kind, "success": True,
                              "data": {"text": json.dumps(PROPOSAL, sort_keys=True)}}), flush=True)
        elif kind == "get_state":
            print(json.dumps({"id": command.get("id"), "type": "response", "command": kind, "success": True,
                              "data": {"sessionFile": None}}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
