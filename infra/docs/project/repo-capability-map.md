---
summary: "Capability map for softwareco/infra repos used for cross-repo routing from arbitrary working directories."
read_when:
  - "A task clearly belongs to softwareco/infra but the current cwd is elsewhere."
  - "You need to choose the right infra repo and minimal read-first docs before diving deeper."
type: "reference"
---

# softwareco/infra repo capability map

## Use
This document is the routing substrate for cross-repo discovery across `~/ai-society/softwareco/infra`.
It does not replace repo-local contracts.
Use it to select the right infra repo, the right first docs, and the next handoff.

Seeded scope in this first production-ready cut:
- the infra lane root itself
- the most frequently referenced active infra repos

Expand only when routing pressure becomes real.

## Cross-lane runtime-cell boundary

For k3s / Envoy / AI Society Runtime Cell work, start with the holding-level problem/intent note:

- `~/ai-society/holdingco/infra/docs/project/ai-society-runtime-cell-problem-intent.md`

Interpretation:

- `holdingco/infra` owns the Runtime Cell concept, intent, and source-owner boundary: k3s + Envoy are infrastructure substrate/service membrane, not society authority.
- `softwareco/infra` owns concrete implementation below that intent when the work becomes workstation runtime, provisioning, NAS administration, packaging, validation, or service operation.

## Repo map

| Repo | Owns | Trigger cues | Read first | Domain skill | Notes |
|---|---|---|---|---|---|
| `infra (root)` | lane-root infra docs, governance, shared direction, cross-repo infra boundaries | `softwareco/infra` root, infra lane, infra root docs, infra governance, lane-level infra planning | `~/ai-society/softwareco/infra/README.md`, `~/ai-society/softwareco/infra/AGENTS.md` | none | Use the root when the concern is lane-level infrastructure direction rather than one subrepo's implementation. |
| `home-devices` | household device/room catalogue, useful activity proposals and owner-linked computer/display overview | home devices, cinema, Optoma UHZ50, Panasonic DLNA, Marantz, Loxone scenes, music zones, solar overview, appliance catalogue, household device health, opt-in phone presence | `~/ai-society/softwareco/infra/home-devices/README.md`, `~/ai-society/softwareco/infra/home-devices/AGENTS.md`, `~/ai-society/softwareco/infra/home-devices/docs/project/catalogue.md`, `~/ai-society/softwareco/infra/home-devices/docs/project/boundaries.md` | none | Documentation-first, no controller/dashboard deployed. Network/security and historical AV records stay in home-network; machines/NAS/model runtimes keep their existing owners. No live actuation or presence collection implied. |
| `mele` | MeLE-specific identity, hardware observations, component provenance, access/recovery instructions and machine acceptance evidence | MeLE, melee, meleec4, melec4-arch, portable Arch computer, MeLE vs Steve, MeLE recovery | `~/ai-society/softwareco/infra/mele/README.md`, `~/ai-society/softwareco/infra/mele/AGENTS.md`, `~/ai-society/softwareco/infra/mele/docs/project/recovery.md` | none | Thin machine integration home, not a workstation clone. Shared desktop configuration stays in dotfiles-managed; package/bootstrap implementation stays in provisioning. Documentation bootstrap is not a verified rebuild or runtime deployment. |
| `pixel11pro` | Google Pixel 11 Pro device home: roles (personal phone + Pult device with pupil data), owner boundaries, identifier-free setup and acceptance evidence | Pixel 11 Pro, Pixel phone, new phone, Pult phone, third Pult device, Pixel Geräteanlage | `~/ai-society/softwareco/infra/pixel11pro/README.md`, `~/ai-society/softwareco/infra/pixel11pro/AGENTS.md`, `~/ai-society/softwareco/infra/pixel11pro/docs/project/model.md` | none | Documentation-first; nothing set up on the phone. No serials, IMEIs or account names in git. Geräteanlage belongs to teachingco-e8 in pult's datenschutz packet (AK7752); Pult device checks stay in pult AK6829/AK7071. The household Pixel 8a stays with home-network. |
| `workstation` | workstation build/run docs, milestone scripts, runtime services, promoted local runtime/control-plane surfaces, local model/runtime control-lane characterization and machine-bound local-model qualification | workstation build, runtime service, lane-op, local runtime, teacher-prep runtime, baseline text service, baseline vs canary, local model evaluation, common eval suite, model qualification, Pi reliability, Bolt/LFM comparison, Qwen3.6 MTP, vLLM grammar, DSPy XML/RLM, local model control lanes, Zotero bridge API packaging, backup/recovery lane | `~/ai-society/softwareco/infra/workstation/README.md`, `~/ai-society/softwareco/infra/workstation/AGENTS.md`, `~/ai-society/softwareco/infra/workstation/docs/project/2026-03-29-cross-repo-boundary-map.md`, `~/ai-society/softwareco/infra/workstation/docs/project/2026-11-01-local-model-evaluation-v1.md` | `workstation-runtime-operator` | Owns workstation runtime/control plane and packaging below `owned/workstation-capabilities`. Common eval entrypoint: `workstation/scripts/phasee/local-model-eval.py`; versioned cases/configurations: `workstation/evals/local-models/`. V1 is offline-tested source, not live-qualified model behavior or representative long-context proof; no automatic promotion. Empirical interpretation/evolution stays with Oracle/DSPx. Older control-lane context: [[qwen36-mtp-control-lanes]] and `workstation/runtime/m14-longcot-local-benchmark/README.md`. |
| `provisioning` | machine/bootstrap provisioning, Comtrya-based package install, secrets bootstrap, setup validation | provisioning, bootstrap, Comtrya, setup profile, package install, machine provisioning, `just setup`, first-run bootstrap | `~/ai-society/softwareco/infra/provisioning/README.md`, `~/ai-society/softwareco/infra/provisioning/AGENTS.md` | none | Owns reproducible machine provisioning, not product runtime semantics. |
| `ds1621-admin` | Synology DS1621+ administration, NAS-side backup target contract, SSH/account/admin runbooks | DS1621, Synology, NAS backup target, pi-ops, DSM admin, restic target contract, NAS SSH | `~/ai-society/softwareco/infra/ds1621-admin/README.md`, `~/ai-society/softwareco/infra/ds1621-admin/AGENTS.md` | none | Use when the concern is NAS/admin truth rather than workstation-side backup consumers. |
| `issue-tracker` | AK-backed external issue tracker, sequence manifests, import/export/sync workflows, machine-owned entry lifecycle (`issue-entry.sh` add/bind/set-status, `Justfile` forwarders), pre-submit and post-close verification helpers | issue tracker, sequencer, upstream issues, `STATE.json`, issue sync, verifier gate, sequence manifest, `just add`/`just bind`/`just set-status`, `issue-entry.sh` | `~/ai-society/softwareco/infra/issue-tracker/README.md`, `~/ai-society/softwareco/infra/issue-tracker/AGENTS.md` | none | DB live state wins over compatibility projections; `STATE.json` is machine-owned — never hand-edit it, mutate entries only via `scripts/issue-entry.sh`. Treat this as external issue workflow machinery. |
| `replay-fabric` | local-first replay and recovery ledger/viewer, hook ingest, bounded Pi/recovery milestones, replay desk UI | Replay Fabric, replay ledger, webhook ingest, Pi milestones, recovery milestones, replay desk, hook sidecar | `~/ai-society/softwareco/infra/replay-fabric/README.md`, `~/ai-society/softwareco/infra/replay-fabric/AGENTS.md` | none | Owns replayable history and bounded recovery guidance, not live Pi or restore authority. |
| `ts-quality-tools` | reusable TS/JS quality tooling monorepo (`ts-mutate`, `crap4ts`), validation and release-trust workflows | ts-mutate, crap4ts, mutation testing, CRAP metric, TS quality tooling, quality intelligence | `~/ai-society/softwareco/infra/ts-quality-tools/README.md`, `~/ai-society/softwareco/infra/ts-quality-tools/AGENTS.md` | none | Workflow-level quality intelligence repo, not one product repo's local quality gate. |
| `obsidian-vault-ops` | Obsidian vault sync across workstation, Galaxy Tab S8 and S21 Ultra; Termux `vault-sync`, sparse-checkout rules for Android, Git LFS layout and NAS LFS transfer | Obsidian vault, vault sync, mainVault, Termux sync, vault-sync, Android sparse checkout, vault LFS, Obsidian Git plugin on mobile | `~/ai-society/softwareco/infra/obsidian-vault-ops/README.md`, `~/ai-society/softwareco/infra/obsidian-vault-ops/docs/project/vault-sync-setup.md` | none | Owns the vault's sync mechanics on all three devices. NAS account/SSH truth stays with `ds1621-admin`; the local model endpoint stays with `workstation`. |
| `xenon` | XENON (Private transit): the operator's own WireGuard design (server control CLI, nftables policy, guarded installer, systemd units, read-only dashboard, Arch/Android/Termux client tools), its review and its adaptation plans | XENON, Private transit, own WireGuard, WireGuard gateway, xenonctl, WireGuard to steve, space peer, wg0 firewall | `~/ai-society/softwareco/infra/xenon/README.md`, `~/ai-society/softwareco/infra/xenon/AGENTS.md`, `~/ai-society/softwareco/infra/xenon/docs/project/2026-11-04-xenon-v1-review.md` | none | v1.0.0 imported unchanged under `xenon-wireguard/`; XENON's VM gateway is not deployed anywhere, but the steve `wg-space` artifacts (`xenon-wireguard/steve/`) run on steve under home-network AK8315. The home network's own routes, router and Tailscale truth stay in `home-network` (AK8315 owns the steve route for the Pixel Private Space); the phone side stays in `pixel11pro`; Pult's listener and sign-in stay in pult. No keys, addresses or identifiers in git. |

## Routing rule
1. If the operator names an exact repo or path, trust that first.
2. Otherwise match trigger cues conservatively.
3. Read only the top candidate repo's minimal read-first docs.
4. Do not widen to sibling infra repos unless the first repo clearly fails to own the concern.
