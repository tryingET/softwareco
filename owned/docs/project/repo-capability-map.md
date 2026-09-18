---
summary: "Capability map for softwareco/owned repos used for cross-repo routing from arbitrary working directories."
read_when:
  - "A task clearly belongs to softwareco/owned but the current cwd is elsewhere."
  - "You need to choose the right owned repo and minimal read-first docs before diving deeper."
type: "reference"
---

# softwareco/owned repo capability map

## Use
This document is the routing substrate for cross-repo discovery across `~/ai-society/softwareco/owned`.
It does not replace repo `AGENTS.md`, `README.md`, or any repo-specific domain skill.
Its job is to help a router select the right repo, the right first docs, and the next handoff.

This map is a **selection surface**, not a capability-truth authority.

It may answer:
- which owned repo likely owns this concern?
- what should a fresh-context Pi agent session read first?
- which domain skill should be loaded next?

It must not answer by itself:
- whether a runtime capability is fully supported today,
- whether a feature has passed owner-repo proof,
- whether an implementation is socially safe to promote as current capability truth.

Treat the `Owns` and `Trigger cues` columns as conservative routing hints, not as a substitute for the target repo's own capability proof.
When a cue touches runtime-control-plane ownership or cross-repo integration, confirm the selected repo's read-first docs before acting.

## Vocabulary and ROCS note

In this document, **agent** means a harnessed LLM agent session unless the wording says otherwise: an LLM running inside a tool/runtime harness such as Pi, with context, tools, session state, and bounded execution rules.

Use narrower terms when useful:
- **Pi agent session** / **Pi session**: a harnessed LLM agent session inside Pi.
- **Subagent**: a delegated child LLM session spawned by a parent session/tool.
- **Execution host** / **harness**: Pi, Claude Code, Cursor, or another runtime that runs the agent session.
- **Model**: the raw LLM/provider/model, not the whole acting system.
- **Operator**: the human giving intent/control.
- **Steward**: the governed human-facing interface role, not a generic LLM agent.

These terms should not become a parallel glossary here. If the vocabulary needs durable semantic authority, promote it through ROCS/ontology workflow and let this map remain the compact routing projection that uses those terms.

## Claim-strength rule

Rows in this map are routing claims, not production capability claims.

If a row says a repo "owns" a concern, that means:
- route there first,
- read its owner docs,
- verify capability truth at the owner layer.

Do not promote implementation hints from this map into supported capability claims unless owner-repo tests, docs, schemas, validators, and operator paths prove them.

Seeded scope in this production-ready cut:
- the owned lane root itself
- the most frequently referenced tooling/plugin/runtime repos

Expand conservatively when routing pressure becomes real.

## Repo map

| Repo | Owns | Trigger cues | Read first | Domain skill | Notes |
|---|---|---|---|---|---|
| `owned (lane root)` | lane-root docs, repo-census helpers, shared contracts such as the standardized Justfile surface, and generated engineering-core adoption coverage for owned repos/packages | `softwareco/owned` root, owned lane, repo census, lane-root governance, standardized Justfile, Ghostty AK launcher, engineering-core adoption scanner, adoption dashboard | `~/ai-society/softwareco/owned/README.md`, `~/ai-society/softwareco/owned/AGENTS.md`, `~/ai-society/softwareco/owned/docs/project/engineering-core-adoption-scanner.md` | none | Keep implementation work in child repos; the lane root is a control plane, not a dumping ground. Reusable scanner semantics live in `core/engineering-core`; owned keeps generated adoption snapshots and rollout interpretation. |
| `zotero-plugins` | Zotero plugin family, safe-update bridge, installed add-on runtime contract, request/receipt/readback loop, bounded existing-parent attachment import | zotero plugin, Zotero add-on, safe-update bridge, request loop, receipt/readback, local Zotero API, existing-parent attachment import, profile `extensions/`, bridge root | `~/ai-society/softwareco/owned/zotero-plugins/README.md`, `~/ai-society/softwareco/owned/zotero-plugins/docs/project/README.md`, `~/ai-society/softwareco/owned/zotero-plugins/docs/project/zotero-safe-update-runtime.md`, `~/ai-society/softwareco/owned/zotero-plugins/packages/zotero-safe-update-bridge/README.md` | `zotero-plugin-operator` | Route here for the currently documented safe-update/runtime surface. Structured child-note upsert is still a separate missing feature and should not be inferred from generic child-attachment wording. |
| `pi-extensions` | Pi extension monorepo root, package selection, extension install/reload workflow, read-only context planning and bounded packet assembly through `pi-context-packer`, ASC subagent runtime, orchestrator control-plane composition, Prompt Vault client, ontology workflows, Level-4 prompt-runner matrix orchestration, and related Pi integration surfaces | pi extension, extension package, extension install, `/reload`, compatibility canary, `pi-context-packer`, `context_plan`, `context_pack`, context packet, source-selection ablation, source-list adoption, Prompt Vault client, ontology workflows, society orchestrator, ASC, subagent, `dispatch_subagent`, `candidate_peer_spawn`, `cognitive_dispatch`, `workflow_execute`, `loop_execute`, `autoresearch_live_supervision`, `level4_autoresearch_campaign_runner`, `promptRunnerBundle`, `level4_visible_launch_watch_blockers`, `/workflow`, `/workflows`, context overlay, interaction, prompt-template accelerator | `~/ai-society/softwareco/owned/pi-extensions/README.md`, `~/ai-society/softwareco/owned/pi-extensions/packages/pi-context-packer/README.md`, `~/ai-society/softwareco/owned/pi-extensions/packages/pi-context-packer/docs/project/product-posture.md`, `~/ai-society/softwareco/owned/pi-extensions/docs/project/root-capabilities.md`, `~/ai-society/softwareco/owned/pi-extensions/packages/pi-society-orchestrator/README.md` | `pi-extensions-operator` | Root docs adjudicate package selection and repo-owned prompts/skills. `pi-context-packer` owns read-only provider planning, bounded packet assembly, consumer-side ranking/fusion, and adoption evaluation without becoming provider or runtime authority. `pi-autonomous-session-control` owns subagent execution/runtime behavior; `pi-society-orchestrator` owns higher-level control-plane coordination (`cognitive_dispatch`, loops, workflows, and Level-4 prompt-runner matrix orchestration over visible candidate peers). Do not collapse those surfaces into DSPx empirical evolution, SCI semantics, Agent Scripts inventory, or AK/FCOS canonical authority. |
| `semantic-code-intelligence` | local-first semantic code intelligence workbench: snapshot-aware code search, AST/symbol navigation, rename planning, semantic graph/ontology enrichment, and MCP/LSP/HTTP/CLI adapters for developers and harnessed LLM coding sessions | semantic code intelligence, code brain, MCP code tools, LSP server, HTTP code intelligence API, symbol search, find definition, references, rename planning, AST query, graph expand, snapshot overlay, pattern learning | `~/ai-society/softwareco/owned/semantic-code-intelligence/README.md`, `~/ai-society/softwareco/owned/semantic-code-intelligence/VISION.md`, `~/ai-society/softwareco/owned/semantic-code-intelligence/AGENTS.md`, `~/ai-society/softwareco/owned/semantic-code-intelligence/docs/IMPLEMENTATION_PLAN_CODE_BRAIN.md` | none | Route here for repository code-intelligence behavior and tool adapters that make a codebase queryable/edit-plannable. Do not route general Pi harness/tool exposure here; Pi extension wiring belongs in `pi-extensions`, while canonical tasks/evidence/decisions belong in `agent-kernel`. |
| `obsidian-plugins` | Obsidian plugin family, Excalidraw/workbench plugin family, host-native support packages, thin sidecar boundary | Obsidian plugin, Excalidraw, graph workbench, sidecar bridge, plugin family, lab vault, plugin kit | `~/ai-society/softwareco/owned/obsidian-plugins/README.md`, `~/ai-society/softwareco/owned/obsidian-plugins/docs/project/problem-statement.md`, `~/ai-society/softwareco/owned/obsidian-plugins/docs/project/2026-04-07-plugin-family-topology.md` | none | Monorepo family home, not a single-plugin repo. |
| `dspx` | local DSPy toolkit, native signature generation/refinement, module/program generation, GEPA optimization, replay/explainability, and local-first empirical development/runtime artifacts for DSPy systems | DSPx, DSPy toolkit, signature gen, signature refine, module generation, program generation, GEPA, optimize gepa, replay, explainability, compile/eval, empirical evolution, receipt bundle, local DSPy runtime | `~/ai-society/softwareco/owned/dspx/README.md`, `~/ai-society/softwareco/owned/dspx/docs/project/vision.md`, `~/ai-society/softwareco/owned/dspx/docs/project/program-synthesis-boundary.md` | none | Route here when the real concern is program-shaped cognition, optimization/search, replayable evidence, or empirical evolution of DSPy systems. Do not collapse this into simple Pi loop/workflow wrapper semantics; that belongs with `pi-society-orchestrator` / ASC routing unless the work is actually about DSPy/DSPx runtime behavior. |
| `crawlgithub` | GitHub starred crawling, Obsidian note generation, watch candidates, snapshot export for downstream consumers | CrawlGitHub, starred repos, watch candidates, repo notes, README sync, starred snapshot export, watch export | `~/ai-society/softwareco/owned/crawlgithub/README.md` | none | Local-first and bounded GitHub discovery/export tool. |
| `designmd-foundry` | DESIGN.md-centered design memory, linting, token/export generation, local browser workspace, and optional Penpot/OpenPencil/Pigmnts/Oat adapter handoffs | DESIGN.md, design tokens, design memory, design lint, agent prompt pack, Penpot tokens, OpenPencil prompt, Pigmnts palette, Oat theme, UI token export | `~/ai-society/softwareco/owned/designmd-foundry/README.md`, `~/ai-society/softwareco/owned/designmd-foundry/AGENTS.md`, `~/ai-society/softwareco/owned/designmd-foundry/docs/project/model.md`, `~/ai-society/softwareco/owned/designmd-foundry/docs/project/architecture.md` | none | Local-first Node project. Route here when the concern is the portable DESIGN.md contract or its lint/export/adaptation workflow; external visual tools remain optional adapters, not owned runtimes. |
| `workstation-capabilities` | workstation-dependent capability apps and libraries above machine/bootstrap concerns: teacher-prep media, voice dictation, OCR, and multimodal local capability tooling | workstation capability, teacher-prep media, voice dictation, OCR pipeline, local multimodal tooling, school ASR, capability app | `~/ai-society/softwareco/owned/workstation-capabilities/README.md` | none | Route here for capability-layer apps and libraries. `softwareco/infra/workstation` owns packaging, runtime bridges, machine/runtime control plane, and promotion/orchestration below this layer. |
| `local-ai-control-plane` | standalone local AI control-plane monorepo: capability surfaces, native/composed/omni modality contracts, upstream substrate governance, CLI/JSON contracts, testkit, and runtime-adapter extraction targets | local AI control plane, ai-control, capability surface, LocalAI substrate, PrivateGPT substrate, native omni, any-to-any, ASR/TTS/image/video/OCR lane contract, modality control plane, baseline-text extraction, runtime capability CLI | `~/ai-society/softwareco/owned/local-ai-control-plane/README.md`, `~/ai-society/softwareco/owned/local-ai-control-plane/AGENTS.md`, `~/ai-society/softwareco/owned/local-ai-control-plane/docs/project/architecture.md`, `~/ai-society/softwareco/owned/local-ai-control-plane/docs/project/substrate-strategy.md` | none | Greenfield product/model owner. LocalAI and PrivateGPT are candidate substrates/providers, not replacements for control-plane authority. `softwareco/infra/workstation` remains live runtime authority for services, ports, systemd units, GPU pressure, receipts, and promoted workstation truth until an explicit migration lands. |
| `german-tts-voice-lab` | curated German Qwen3-TTS VoiceDesign profiles and a local render CLI for classroom/readback voice canaries | German TTS, Qwen3-TTS, VoiceDesign, German classroom voice, German child voice, German teacher voice, synthetic voice profile, text-to-speech canary | `~/ai-society/softwareco/owned/german-tts-voice-lab/README.md`, `~/ai-society/softwareco/owned/german-tts-voice-lab/AGENTS.md`, `~/ai-society/softwareco/owned/german-tts-voice-lab/docs/project/purpose.md` | none | Capability-code repo only; `infra/workstation` still owns model download windows, GPU/runtime orchestration, service packaging, and any canonical TTS lane publication. |
| `agent-kernel` | AK DB-first local coordination runtime, task/evidence/decision/model surfaces, local-first governance substrate | Agent Kernel, `ak` DB, task ready, evidence ledger, decision runtime, local-first coordination, society DB | `~/ai-society/softwareco/owned/agent-kernel/README.md`, `~/ai-society/softwareco/owned/agent-kernel/AGENTS.md`, `~/ai-society/softwareco/owned/agent-kernel/docs/project/database-backend-runtime.md` | none | DB state is canonical; `governance/work-items.json` is projection only. |
| `runtime-trace-insights` | normalized runtime observation evidence and runtime trace bundle contracts | runtime trace bundle, runtime observations, observed packages, runtime import evidence, runtime-only dependency evidence | `~/ai-society/softwareco/owned/runtime-trace-insights/README.md`, `~/ai-society/softwareco/owned/runtime-trace-insights/AGENTS.md`, `~/ai-society/softwareco/owned/runtime-trace-insights/docs/project/runtime-trace-bundle-contract.md` | none | Route here for runtime evidence capture/contract truth. It does not own static graph centrality, dependency fusion, visualization, or removal authority. |
| `dep-diet` | dependency evidence fusion, actionability-adjacent classification, Gardener static evidence consumption, and `depmodel.v1` production | dep-diet, dependency diet, static/runtime evidence, Gardener output, `--gardener-output`, `--runtime-bundle`, `--out-depmodel`, depmodel producer, prune/remove planning boundary, replacement intent | `~/ai-society/softwareco/owned/dep-diet/README.md`, `~/ai-society/softwareco/owned/dep-diet/docs/operations/static-runtime-greenfield-how-to.md`, `~/ai-society/softwareco/owned/dep-diet/docs/operations/static-runtime-brownfield-how-to.md`, `~/ai-society/softwareco/owned/dep-diet/docs/project/static-runtime-evidence-corridor.md` | none | Consumes Gardener static evidence and runtime bundles. Static/runtime classifications are evidence context, not removal authority. Gardener provider behavior itself lives under `softwareco/contrib/gardener`; dependency replacement execution belongs in `dep-surgeon`. |
| `dep-surgeon` | evidence-gated dependency replacement/remediation execution, replacement plans, reversible candidate patches, and replacement-result evidence | dep-surgeon, dependency replacement, dependency remediation, codemod, replace dependency, remove dependency, upgrade dependency, replacement plan, replacement result, impact-scoped validation handoff | `~/ai-society/softwareco/owned/dep-surgeon/README.md`, `~/ai-society/softwareco/owned/dep-surgeon/docs/project/product-posture.md`, `~/ai-society/softwareco/owned/dep-surgeon/docs/project/model.md`, `~/ai-society/softwareco/owned/dep-surgeon/contracts/dep-surgeon-contract.md` | none | Executes bounded candidate patches from upstream replacement intent. It does not own dep-diet actionability, runtime-trace evidence, test-capabilities validation, dep-viz explanation, dep-redteam exploitability validation, or ts-quality trust proof. |
| `dep-viz` | depmodel consumption, report UI, operator explanation surfaces, static/runtime evidence display | dep-viz, depmodel report, static/runtime report, dependency visualization, explain dependency evidence, evidence context not removal authority | `~/ai-society/softwareco/owned/dep-viz/README.md`, `~/ai-society/softwareco/owned/dep-viz/docs/operations/static-runtime-operator-path.md`, `~/ai-society/softwareco/owned/dep-viz/docs/depmodel-contract.md` | none | Route here for report/UI/operator explanation behavior after a depmodel exists. It does not produce dependency-fusion evidence or replacement patches. |
| `ts-quality` | public-package proof harness and durable adoption evidence docs for cross-repo slices | ts-quality adoption evidence, public package proof, dependency-intelligence evidence docs, static/runtime adoption record | `~/ai-society/softwareco/owned/ts-quality/README.md`, `~/ai-society/softwareco/owned/ts-quality/AGENTS.md`, `~/ai-society/softwareco/owned/ts-quality/docs/adoption/` | none | Route here for durable adoption/proof records only. Do not treat ts-quality evidence docs as owner truth for runtime traces, dep-diet fusion, or dep-viz UI behavior. |
| `dotfiles-managed` | dotfiles, chezmoi-style environment management, public + private layer split, developer-environment convergence | dotfiles, chezmoi, shell config, managed dotfiles, multi-OS environment, WSL-first environment | `~/ai-society/softwareco/owned/dotfiles-managed/README.md`, `~/ai-society/softwareco/owned/dotfiles-managed/AGENTS.md` | none | Owns dotfiles/env convergence, not workstation runtime control planes. |
| `pi-server` | standalone Pi session multiplexer/server, WebSocket + stdio transports, session lifecycle, remote UI protocol | pi server, session multiplexer, websocket server, stdio transport, protocol versioning, AgentSession server | `~/ai-society/softwareco/owned/pi-server/README.md`, `~/ai-society/softwareco/owned/pi-server/AGENTS.md`, `~/ai-society/softwareco/owned/pi-server/PROTOCOL.md` | none | Standalone server package, not an extension bundle. |
| `misegraph` | recipe workflow DSL, canonical IR, graph-aware linter, and deterministic renderers for web, print, and e-ink | misegraph, `.mise`, recipe IR, e-ink renderer, Cooklang importer, recipe schema | `~/ai-society/softwareco/owned/misegraph/README.md`, `~/ai-society/softwareco/owned/misegraph/AGENTS.md`, `~/ai-society/softwareco/owned/misegraph/docs/project/vision.md`, `~/ai-society/softwareco/owned/misegraph/docs/eink.md` | none | Renderer/language owner. Physical E1001 canary evidence lives here; permanent kitchen serving does not. |
| `misegraph-kitchen` | local kitchen product around Misegraph: recipe catalog, current selection, Android-friendly PWA, NAS frame serving, atomic replace, ETag/304, device previous/next | kitchen PWA, NAS recipe frame, e-paper serving, previous/next recipe, Android recipe editor, kitchen catalog | `~/ai-society/softwareco/owned/misegraph-kitchen/README.md`, `~/ai-society/softwareco/owned/misegraph-kitchen/AGENTS.md`, `~/ai-society/softwareco/owned/misegraph-kitchen/docs/project/owner-boundaries.md`, `~/ai-society/softwareco/owned/misegraph-kitchen/docs/project/architecture.md` | none | Consumes Misegraph as a renderer. Do not implement `.mise` parsing or renderers here. NAS/PWA/device apps are not implemented at bootstrap; contracts live in `packages/kitchen-contracts`. |
| `lehrplan-viz` | LehrplanPLUS (Bayern: Grundschule, Mittelschule, Förderschule with 7 Förderschwerpunkten) curriculum toolkit: plain-HTTP snapshot scraper, reproducible SQLite build (items, Teilbereiche, Kompetenz tags, Querverweis graph with internal targets, section anchors/badges, Jahrgangsstufenprofile, Fachprofil text, Übergreifende Ziele, Servicematerial details with downloads, Stundentafel), FastAPI + static tree browser on Cloudflare Pages (`lehrplanplus.pages.dev`), the read-only `lehrplan_query` CLI for harnessed LLM agents (`slice`, `crossrefs`, `profile`, `fachprofil`, `stundentafel`, `material`, `neu`, `--progression`, `--ref-depth`) and `snapshot_diff.py` for what changed between snapshots | LehrplanPLUS, Lehrplan, Lernbereich, Teilbereich, Kompetenzerwartungen, Querverweise, Servicematerialien, Jahrgangsstufenprofil, grundlegende Kompetenzen, Fachprofil, Stundentafel, Stoffverteilung, Sequenzplan, Klassenlehrplan, Unterrichtsentwurf, Probe, Förderschule, Förderschwerpunkt, Inklusion, Grundschule/Mittelschule curriculum, `lehrplan_query`, `lehrplanplus.pages.dev`, curriculum scrape/snapshot | `~/ai-society/softwareco/owned/lehrplan-viz/README.md`, `~/ai-society/softwareco/owned/lehrplan-viz/AGENTS.md`, `~/ai-society/softwareco/owned/lehrplan-viz/.pi/skills/lehrplanplus-query/SKILL.md` | `lehrplanplus-query` (lookup / planning packets), `lehrplan-viz-maintainer` (scrape, DB build, deploy) | Deploys are manual (`scripts/deploy.sh`, Cloudflare account of the operator); GitHub Actions is billing-blocked by design. Scraped snapshots and the DB stay under `output/` (never committed); the derived static export `api/static/data/` is committed as the deploy artifact. |

## Common ambiguity edges

### `pi-extensions` vs `dspx`
Choose `pi-extensions` for Pi commands, extension wiring, harness behavior, tool exposure, ASC, orchestrator, and Pi-side operator surfaces.

Choose `dspx` for DSPy program generation, GEPA/search, optimization, replay receipts, empirical behavior analysis, and Oracle-style analysis.

### `pi-extensions` vs `agent-kernel`
Choose `pi-extensions` for Pi-side execution/coordination surfaces.

Choose `agent-kernel` for canonical task, evidence, decision, model, and DB runtime state.

### Level-4 prompt-runner matrix vs AI Society runtime authority
Route Level-4 prompt-runner matrix concerns (`level4_autoresearch_campaign_runner`, `promptRunnerBundle`, visible `candidate_peer_spawn`, ACK/FINAL watch, controller lineage verification, and `level4_visible_launch_watch_blockers`) to `pi-extensions/packages/pi-society-orchestrator` first.

Use this capability inside AI Society as an execution-parallelism / implementation-wave dogfood pattern: it can generate visible lanes, watch communication, preserve lineage checks, and prepare bind/measure/export/review handoffs. It is not, by itself, canonical task/evidence/decision authority, FCOS control-board authority, semantic authority, or DSPx empirical-analysis authority. Promote durable facts through the owning layer: AK for task/evidence/decision lineage, FCOS for Layer-5 control-board meaning, ROCS for semantics, Prompt Vault for reusable procedures, and DSPx/Oracle for empirical behavior analysis.

### `agent-kernel` vs FCOS Control Board
Choose `agent-kernel` for AK task/evidence/decision/direction/runtime substrate concerns.

Choose `~/ai-society/holdingco/fcos-control-board` for FCOS product identity, `fcos ...` commands, native board model, archive manifest, and Layer-5 control-board operator UX. FCOS should not be routed to `ak work-items *-fcos` or `ak fcos ...` by default.

### Prompt Vault authority vs Pi Vault integration
Choose the Prompt Vault authority owner for schema, governed vocabulary, template authority, visibility, and execution/feedback facts.

Choose `pi-extensions/packages/pi-vault-client` only for Pi-side integration, picker UX, command behavior, tool wiring, and extension packaging.

### `workstation-capabilities` vs `softwareco/infra/workstation`
Choose `workstation-capabilities` for user-facing capability apps/libraries such as teacher-prep media, OCR, ASR, and multimodal local tooling.

Choose `softwareco/infra/workstation` for packaging, runtime bridges, service lifecycle, machine/runtime control plane, and promotion/orchestration below the capability layer.

### `zotero-plugins` vs runtime/service packaging owners
Choose `zotero-plugins` for add-on mutation semantics, request contracts, receipt/readback, safe-update behavior, and plugin runtime behavior.

Choose runtime/service packaging owners when the concern is persistent localhost service packaging, systemd, ports, publication, or workstation runtime productization.

### `misegraph` vs `misegraph-kitchen`
Choose `misegraph` for the recipe language, IR, lint, schema, and deterministic renderers, including e-ink profile proof.

Choose `misegraph-kitchen` for catalog browsing, current-recipe selection, Android-friendly editing, NAS frame serving, atomic replacement, conditional HTTP, and device previous/next semantics. Invoke Misegraph as an external renderer; do not parse `.mise` in the kitchen repo.

### Dependency-intelligence vertical corridor
Use this map to route to the owner layer, not to restate the corridor's detailed proof history:

```text
runtime-trace-insights + Gardener (softwareco/contrib) -> dep-diet -> dep-surgeon (when replacement execution is selected) -> test-capabilities/runtime re-observation -> dep-viz -> dep-redteam (when vulnerability validation is needed) -> ts-quality evidence docs
```

Owner split:
- `runtime-trace-insights`: runtime observation bundle contract;
- `softwareco/contrib/gardener`: static dependency graph / centrality provider;
- `dep-diet`: static + runtime evidence fusion, depmodel production, and replacement intent/actionability context;
- `dep-surgeon`: dependency replacement/remediation execution and replacement-result evidence;
- `test-capabilities`: impact-scoped behavioral validation for candidate replacements;
- `dep-viz`: depmodel report/UI consumption, before/after explanation, and operator explanation;
- `dep-redteam`: vulnerability-specific validation/review packet layer when replacement is security-driven;
- `ts-quality`: durable adoption/proof evidence for the cross-repo slice.

Boundary: static importance, runtime observation, declared-unobserved status, and runtime-only status are evidence context, not automatic prune/remove authority.

## Routing rule
1. If the operator names an exact repo or path, trust that first.
2. Otherwise classify the cue by layer before choosing a repo: authority, semantics, runtime state, execution host behavior, integration/package wiring, or user-facing product behavior.
3. Match trigger cues conservatively in this map.
4. Read only the top candidate repo's minimal read-first docs.
5. If a domain skill exists, load it next.
6. Resolve owner-repo boundaries from the owner docs before making strong capability claims.
7. Do not widen to sibling repos unless the first repo clearly fails to own the concern.
