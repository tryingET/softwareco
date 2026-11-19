---
summary: "AK8039 routes common local-model evaluation to workstation's source-tested v1 and records the observed LFM2.5 cache subset; no LFM3 snapshots found in checked locations."
read_when:
  - "Finding the common local-model evaluation entrypoint through the infra capability map."
  - "Checking which LiquidAI model artifacts were observed locally on 2026-11-01."
type: "reference"
---

# Local-model evaluation routing and LiquidAI inventory

Operator requested discoverability after workstation AK8022 and asked whether the LFM3 series
had been downloaded. Authority: task:8039; documentation and metadata inspection only.

## Map change

The workstation row in `docs/project/repo-capability-map.md` now includes local-model evaluation,
common suite, Pi reliability and Bolt/LFM comparison routing cues. It links the canonical
`workstation/docs/project/2026-11-01-local-model-evaluation-v1.md`, CLI and versioned cases.
The map explicitly says offline-tested source, not live-qualified behavior or representative
long-context proof. No promotion or empirical-authority migration is implied.

## Cache observation, not an integrity or serving certificate

Configured cache: `/data/models/hf-cache/hub`. Checked model-cache names there, its parent,
`~/.cache/huggingface/hub`, the documented legacy cache if present, and bounded model aliases
under `/data/models`. **No LFM3 cache/snapshot was found in those locations.** This does not prove
that LFM3 was never downloaded historically or exists nowhere outside the checked locations.

Observed older artifacts:

| Repository | Present weights | Snapshot revision |
| --- | --- | --- |
| LiquidAI/LFM2.5-2.6B | Two safetensors shards | dca1825886789bd40b94368f53b1d9ada4c94598 |
| LiquidAI/LFM2.5-8B-A1B | model.safetensors | 826e5ff23b398a1f46f1a50b926b5c79666f8505 |
| LiquidAI/LFM2.5-8B-A1B-GGUF | Q4_K_M | dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0 |
| LiquidAI/LFM2.5-24B-A2B | Ten safetensors shards | 1769516ac588c4c558089c94f27d96b0dc67b183 |
| LiquidAI/LFM2.5-Audio-1.5B-GGUF | F16 and Q8_0 main model, matching projector/tokenizer/vocoder files | 7d525f883a077e20afb782f2ff618edcae0e39e4 |

Symlink targets were statted successfully, and no `.incomplete` blobs were found in those five
repo caches. This inspection did not hash the weights or compare complete remote manifests.
Aliases under `by-task`, `by-format`, `by-consumer`, `by-lifecycle` and `by-modalities` are not
additional model downloads.

The current official LiquidAI HF metadata lists four LFM3 task variants: LFM3-1.7B text,
LFM3-VL-2B vision-language, LFM3-Audio-2B and LFM3-Omni-2B, plus separate format/base exports.
Source: `https://huggingface.co/api/models?author=LiquidAI&search=LFM3&limit=100`.
No download, runtime action, dependency change or model evaluation was performed by this slice.

## Checks and retained unrelated issue

- `git diff --check`: passed for the scoped update.
- All three new workstation runbook/CLI/suite path targets exist.
- `./scripts/ci/full.sh`: passed (CI smoke plus ROCS build/check).
- `node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs docs --strict`:
  failed only at existing `docs/learnings/README.md` (missing front matter/read_when), already
  tracked under task:7179. That file was not changed; the map update does not repair or hide it.
