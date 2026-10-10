---
summary: "Engineering-core adoption coverage report."
read_when:
  - "Reviewing engineering-core adoption coverage across one or more repo scopes."
type: "generated-report"
---

# Engineering-core adoption coverage

Generated: 2026-10-01T17:05:44.217676+00:00

## Summary

- Scopes: `1`
- Repo discovery: `immediate`
- Completeness: `complete`
- Omissions: `0`
- Per-path failures: `0`
- Include scope root: `False`
- Package/member surfaces included: `False`
- Repos: `53`
- Packages/member surfaces: `0`
- Total records: `53`
- Structural status counts: `{"adopted": 44, "doc-only": 1, "legacy-mixed": 1, "legacy-only": 1, "missing": 3, "partial": 3}`
- Semantic status counts: `{"likely-incomplete": 2, "needs-review": 4, "ok": 47}`
- Loop validation status counts: `{"absent": 17, "complete": 36}`

## Scope summaries

| Scope | Repos | Packages | Total | Structural counts | Semantic counts | Loop validation counts |
|---|---:|---:|---:|---|---|---|
| /home/tryinget/ai-society/softwareco/owned | 53 | 0 | 53 | `{"adopted": 44, "doc-only": 1, "legacy-mixed": 1, "legacy-only": 1, "missing": 3, "partial": 3}` | `{"likely-incomplete": 2, "needs-review": 4, "ok": 47}` | `{"absent": 17, "complete": 36}` |

## Review candidates

| Scope | Path | Name | Kind | Structural | Semantic | Loop validation | Lanes | Disciplines | Policy | Docs | Legacy | Catalog/list | Justfile | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| owned | crawlgithub | crawlgithub | repo | partial | ok | complete | - | validation, security-privacy, documentation | yes | yes | no | yes | yes | no lane declared |
| owned | email-triage | email-triage | repo | legacy-only | needs-review | absent | - | - | no | no | yes | no | yes | legacy tech-stack surface still present; missing_engineering_doc_for_semantic_review |
| owned | experimentation | experimentation | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |
| owned | niri-desktop-continuity | niri-desktop-continuity | repo | partial | likely-incomplete | absent | py | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | no | yes | missing one or more catalog/list command fields; missing_expected_discipline:accessibility:ui_or_frontend_surface; missing_expected_discipline:design-system:ui_or_frontend_surface |
| owned | obsidian-plugins | obsidian-plugins | repo | legacy-mixed | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility | yes | yes | yes | yes | yes | legacy tech-stack surface still present |
| owned | pi-web | pi-web | repo | partial | likely-incomplete | absent | - | validation, security-privacy, documentation | yes | yes | no | yes | yes | no lane declared; missing_expected_discipline:accessibility:ui_or_frontend_surface; missing_expected_discipline:design-system:ui_or_frontend_surface |
| owned | taschenschach | taschenschach | repo | doc-only | ok | absent | - | - | no | yes | no | no | yes | docs/engineering.local.md exists without policy/engineering-lane.json |
| owned | to-sort | to-sort | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |
| owned | zufallsrad | zufallsrad | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |

## Full coverage

| Scope | Path | Name | Kind | Structural | Semantic | Loop validation | Lanes | Disciplines | Policy | Docs | Legacy | Catalog/list | Justfile | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| owned | agent-harness | agent-harness | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | no | - |
| owned | agent-kernel | agent-kernel | repo | adopted | ok | complete | rust, rust-build-graph | validation, testing, local-first-data, security-privacy, observability, documentation, dependency-governance, specification-and-dsls, engineering-reasoning, build-graph-acceleration | yes | yes | no | yes | yes | - |
| owned | apex-cathedral | apex-cathedral | repo | adopted | ok | complete | elixir, ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | appmapp-platform | appmapp-platform | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | blackwell-kernel-lab | blackwell-kernel-lab | repo | adopted | ok | complete | cpp, py | validation, testing, security-privacy, documentation, dependency-governance, observability, specification-and-dsls, engineering-reasoning, build-graph-acceleration | yes | yes | no | yes | yes | - |
| owned | calisthenics-ai-coach | calisthenics-ai-coach | repo | adopted | ok | complete | ts, ts-frontend, py | design-system, accessibility, validation, testing, local-first-data, security-privacy, documentation, specification-and-dsls, engineering-reasoning, dependency-governance, observability | yes | yes | no | yes | yes | - |
| owned | compass-c | compass-c | repo | adopted | ok | absent | py | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | crawlgithub | crawlgithub | repo | partial | ok | complete | - | validation, security-privacy, documentation | yes | yes | no | yes | yes | no lane declared |
| owned | dep-diet | dep-diet | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | dep-redteam | dep-redteam | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | dep-surgeon | dep-surgeon | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | dep-viz | dep-viz | repo | adopted | ok | complete | ts, go | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility, design-system | yes | yes | no | yes | yes | - |
| owned | designmd-foundry | designmd-foundry | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | dotfiles-managed | dotfiles-managed | repo | adopted | ok | complete | lane_status:no_language_lane | validation, testing, security-privacy, documentation, dependency-governance, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | dspx | dspx | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | email-copilot | email-copilot | repo | adopted | ok | complete | py, ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | email-triage | email-triage | repo | legacy-only | needs-review | absent | - | - | no | no | yes | no | yes | legacy tech-stack surface still present; missing_engineering_doc_for_semantic_review |
| owned | experimentation | experimentation | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |
| owned | feedbackApp | feedbackApp | repo | adopted | ok | complete | lane_status:no_first_class_android_kotlin_lane | validation, testing, local-first-data, security-privacy, observability, documentation, dependency-governance, specification-and-dsls, engineering-reasoning, accessibility | yes | yes | no | yes | yes | - |
| owned | german-tts-voice-lab | german-tts-voice-lab | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | kinetic-caption-studio | kinetic-caption-studio | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | learner-worlds | learner-worlds | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | lehrplan-viz | lehrplan-viz | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility, design-system | yes | yes | no | yes | yes | - |
| owned | leseOS | leseOS | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | local-ai-control-plane | local-ai-control-plane | repo | adopted | ok | complete | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance, local-first-data, security-privacy, observability, specification-and-dsls | yes | yes | no | yes | yes | - |
| owned | machraum | machraum | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | mathe-machraum | mathe-machraum | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | merkschatz | merkschatz | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | misegraph | misegraph | repo | adopted | ok | absent | rust | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | misegraph-kitchen | misegraph-kitchen | repo | adopted | ok | absent | lane_status:monorepo_control_plane | validation, testing, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | mittelschule-stadeln | mittelschule-stadeln | repo | adopted | ok | complete | py | validation, documentation, security-privacy | yes | yes | no | yes | yes | - |
| owned | nano-train | nano-train | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | nexus-workflow-platform | nexus-workflow-platform | repo | adopted | ok | complete | lane_status:no_primary_manifest | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | niri-desktop-continuity | niri-desktop-continuity | repo | partial | likely-incomplete | absent | py | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | no | yes | missing one or more catalog/list command fields; missing_expected_discipline:accessibility:ui_or_frontend_surface; missing_expected_discipline:design-system:ui_or_frontend_surface |
| owned | obsidian-plugins | obsidian-plugins | repo | legacy-mixed | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility | yes | yes | yes | yes | yes | legacy tech-stack surface still present |
| owned | pi-extensions | pi-extensions | repo | adopted | ok | complete | pi-ts | validation, testing, security-privacy, documentation, dependency-governance, observability, specification-and-dsls, engineering-reasoning, build-graph-acceleration | yes | yes | no | yes | yes | - |
| owned | pi-extensions-template | pi-extensions-template | repo | adopted | ok | complete | pi-ts | validation, testing, security-privacy, documentation, dependency-governance, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | pi-server | pi-server | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | pi-web | pi-web | repo | partial | likely-incomplete | absent | - | validation, security-privacy, documentation | yes | yes | no | yes | yes | no lane declared; missing_expected_discipline:accessibility:ui_or_frontend_surface; missing_expected_discipline:design-system:ui_or_frontend_surface |
| owned | project-xeno | project-xeno | repo | adopted | ok | absent | go, common-lisp | validation, testing, security-privacy, documentation, dependency-governance, specification-and-dsls | yes | yes | no | yes | yes | - |
| owned | reasoning-budget-proxy | reasoning-budget-proxy | repo | adopted | ok | absent | py | validation, testing, security-privacy, documentation, dependency-governance | yes | yes | no | yes | yes | - |
| owned | runtime-trace-insights | runtime-trace-insights | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | no | - |
| owned | semantic-code-intelligence | semantic-code-intelligence | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility, design-system | yes | yes | no | yes | yes | - |
| owned | semantic-flow-diff | semantic-flow-diff | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | taschenschach | taschenschach | repo | doc-only | ok | absent | - | - | no | yes | no | no | yes | docs/engineering.local.md exists without policy/engineering-lane.json |
| owned | test-capabilities | test-capabilities | repo | adopted | ok | complete | pi-ts | validation, testing, security-privacy, documentation, dependency-governance, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | no | - |
| owned | to-sort | to-sort | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |
| owned | ts-quality | ts-quality | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | no | - |
| owned | typREPL | typREPL | repo | adopted | ok | complete | lane_status:no_primary_manifest | validation, testing, security-privacy, documentation, dependency-governance, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | workspace-platform | workspace-platform | repo | adopted | ok | complete | ts, ts-frontend | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, design-system, accessibility | yes | yes | no | yes | yes | - |
| owned | workstation-capabilities | workstation-capabilities | repo | adopted | ok | complete | py | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning | yes | yes | no | yes | yes | - |
| owned | zotero-plugins | zotero-plugins | repo | adopted | ok | complete | ts | validation, testing, security-privacy, documentation, dependency-governance, local-first-data, observability, specification-and-dsls, engineering-reasoning, accessibility | yes | yes | no | yes | yes | - |
| owned | zufallsrad | zufallsrad | repo | missing | needs-review | absent | - | - | no | no | no | no | no | missing_engineering_doc_for_semantic_review |

## Stable diagnostics and ratchet

- Baseline supplied: `False`
- Current diagnostics: `20`
- Current counts: `{"advisory": 8, "error": 0, "warning": 12}`
- New diagnostics: `20`
- New counts: `{"advisory": 8, "error": 0, "warning": 12}`
- Resolved baseline issues: `0`

| Severity | Rule | Scope | Path | Confidence | New | Evidence |
|---|---|---|---|---:|---|---|
| warning | `adoption.partial` | `owned` | `crawlgithub` | 1.00 | yes | no lane declared |
| warning | `policy.missing-lane` | `owned` | `crawlgithub` | 1.00 | yes | - |
| warning | `legacy.surfaces` | `owned` | `email-triage` | 1.00 | yes | legacy tech-stack surface still present |
| warning | `adoption.missing` | `owned` | `experimentation` | 1.00 | yes | - |
| warning | `adoption.partial` | `owned` | `niri-desktop-continuity` | 1.00 | yes | missing one or more catalog/list command fields |
| warning | `policy.command-surface` | `owned` | `niri-desktop-continuity` | 1.00 | yes | - |
| warning | `legacy.surfaces` | `owned` | `obsidian-plugins` | 1.00 | yes | legacy tech-stack surface still present |
| warning | `adoption.partial` | `owned` | `pi-web` | 1.00 | yes | no lane declared |
| warning | `policy.missing-lane` | `owned` | `pi-web` | 1.00 | yes | - |
| warning | `adoption.surface-pair` | `owned` | `taschenschach` | 1.00 | yes | docs/engineering.local.md exists without policy/engineering-lane.json |
| warning | `adoption.missing` | `owned` | `to-sort` | 1.00 | yes | - |
| warning | `adoption.missing` | `owned` | `zufallsrad` | 1.00 | yes | - |
| advisory | `semantic.missing-engineering-doc-for-semantic-review` | `owned` | `email-triage` | 0.55 | yes | missing_engineering_doc_for_semantic_review |
| advisory | `semantic.missing-engineering-doc-for-semantic-review` | `owned` | `experimentation` | 0.55 | yes | missing_engineering_doc_for_semantic_review |
| advisory | `semantic.expected-discipline.accessibility` | `owned` | `niri-desktop-continuity` | 0.70 | yes | ui_or_frontend_surface |
| advisory | `semantic.expected-discipline.design-system` | `owned` | `niri-desktop-continuity` | 0.70 | yes | ui_or_frontend_surface |
| advisory | `semantic.expected-discipline.accessibility` | `owned` | `pi-web` | 0.70 | yes | ui_or_frontend_surface |
| advisory | `semantic.expected-discipline.design-system` | `owned` | `pi-web` | 0.70 | yes | ui_or_frontend_surface |
| advisory | `semantic.missing-engineering-doc-for-semantic-review` | `owned` | `to-sort` | 0.55 | yes | missing_engineering_doc_for_semantic_review |
| advisory | `semantic.missing-engineering-doc-for-semantic-review` | `owned` | `zufallsrad` | 0.55 | yes | missing_engineering_doc_for_semantic_review |
