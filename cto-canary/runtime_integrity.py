#!/usr/bin/env python3
"""Accepted-Git and pinned-runtime integrity checks for the CTO canary."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / "config.json").read_text())
ROOT = Path(CONFIG["cwd"])
UNIT_NAMES = (
    "softwareco-cto-canary.service", "softwareco-cto-canary.timer",
    "softwareco-cto-canary-stop.service", "softwareco-cto-canary-stop.timer",
)


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def directory_digest(root: Path) -> str:
    root = root.resolve(strict=True)
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix().encode()
        if path.is_symlink():
            target = os.readlink(path).encode()
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(root):
                raise RuntimeError(f"runtime package symlink escapes pinned root: {path} -> {resolved}")
            marker, data = b"L", target
        elif path.is_file():
            marker, data = b"F", path.read_bytes()
        else:
            continue
        h.update(marker); h.update(len(relative).to_bytes(8, "big")); h.update(relative)
        h.update(len(data).to_bytes(8, "big")); h.update(data)
    return h.hexdigest()


def runtime_packages(bundle_root: Path | None = None) -> tuple[Path, Path, Path]:
    bundle_root = bundle_root or HERE.parent
    installed_pi = bundle_root / CONFIG["runtime_pi_package_relative"]
    installed_modes = bundle_root / CONFIG["runtime_pi_modes_package_relative"]
    installed_entrypoint = bundle_root / CONFIG["runtime_pi_entrypoint_relative"]
    if bundle_root.resolve() == ROOT.resolve():
        # Development-only path in the canonical source checkout before installation.
        return Path(CONFIG["pi_package"]), Path(CONFIG["pi_modes_package"]), Path(CONFIG["pi_entrypoint"])
    if not (bundle_root / "manifest.json").is_file():
        raise RuntimeError("installed runtime location has no accepted bundle manifest")
    if not installed_pi.is_dir() or not installed_modes.is_dir() or not installed_entrypoint.is_file():
        raise RuntimeError("installed bundle is missing an isolated Pi/Pi-Modes runtime or entrypoint")
    return installed_pi, installed_modes, installed_entrypoint


def git_blob(commit: str, relative: str) -> bytes:
    cp = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=ROOT, capture_output=True, check=False)
    if cp.returncode:
        raise RuntimeError(f"accepted Git blob is unavailable: {relative}: {cp.stderr.decode(errors='replace').strip()}")
    return cp.stdout


def rendered_unit(commit: str, name: str, bundle: Path) -> bytes:
    text = git_blob(commit, f"cto-canary/systemd/{name}").decode()
    text = text.replace("@BUNDLE_DIR@", str(bundle / "cto-canary")).replace("@ROOT@", str(ROOT))
    return text.encode()


def verify_bundle(activation: dict[str, Any], unit_dir: Path | None = None, verify_runtime: bool = True) -> list[str]:
    """Bind bundle, manifest, project mode, and installed units to accepted Git objects."""
    errors: list[str] = []
    bundle = Path(activation["bundle_dir"])
    commit = activation["accepted_commit"]
    manifest_path = bundle / "manifest.json"
    if sha256(manifest_path) != activation["bundle_manifest_sha256"]:
        errors.append("installed bundle manifest digest differs from activation")
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError):
        return errors + ["installed bundle manifest is unreadable"]
    try:
        accepted_config = json.loads(git_blob(commit, "cto-canary/config.json"))
        expected_files = accepted_config["accepted_bundle_files"]
    except (RuntimeError, KeyError, json.JSONDecodeError) as exc:
        return errors + [f"accepted Git config/file set is unreadable: {exc}"]
    if (manifest.get("accepted_commit") != commit or manifest.get("decision_id") != activation["decision_id"] or
            manifest.get("acceptance_receipt_id") != activation["acceptance_receipt_id"] or
            set(manifest.get("files", {})) != set(expected_files)):
        errors.append("installed bundle manifest identity/file set is invalid")
    expected_runtime = {
        accepted_config["runtime_pi_package_relative"]: accepted_config["pi_package_digest"],
        accepted_config["runtime_pi_modes_package_relative"]: accepted_config["pi_modes_package_digest"],
    }
    if manifest.get("runtime_digests") != expected_runtime:
        errors.append("installed runtime manifest differs from accepted Git config")
    if verify_runtime:
        try:
            pi_package, modes_package, entrypoint = runtime_packages(bundle)
            if directory_digest(pi_package) != accepted_config["pi_package_digest"]:
                errors.append("isolated Pi runtime differs from accepted digest")
            if directory_digest(modes_package) != accepted_config["pi_modes_package_digest"]:
                errors.append("isolated Pi Modes runtime differs from accepted digest")
            if not entrypoint.is_file() or not entrypoint.resolve().is_relative_to(pi_package.resolve()):
                errors.append("isolated Pi entrypoint is missing or escapes its runtime tree")
        except (OSError, RuntimeError) as exc:
            errors.append(f"isolated runtime verification failed closed: {exc}")
    for relative in expected_files:
        try:
            accepted = git_blob(commit, relative)
        except RuntimeError as exc:
            errors.append(str(exc)); continue
        accepted_sha = hashlib.sha256(accepted).hexdigest()
        if manifest.get("files", {}).get(relative) != accepted_sha:
            errors.append(f"manifest is not bound to accepted Git blob: {relative}")
        if sha256(bundle / relative) != accepted_sha:
            errors.append(f"installed artifact differs from accepted Git blob: {relative}")
    try:
        accepted_mode_sha = hashlib.sha256(git_blob(commit, ".pi/modes/softwareco-cto-canary.json")).hexdigest()
    except RuntimeError as exc:
        errors.append(str(exc)); accepted_mode_sha = None
    if sha256(ROOT / ".pi/modes/softwareco-cto-canary.json") != accepted_mode_sha:
        errors.append("trusted-root CTO canary mode differs from accepted Git blob")
    unit_dir = unit_dir or Path.home() / ".config/systemd/user"
    for name in UNIT_NAMES:
        try:
            expected = rendered_unit(commit, name, bundle)
        except RuntimeError as exc:
            errors.append(str(exc)); continue
        installed = unit_dir / name
        if not installed.is_file() or installed.read_bytes() != expected:
            errors.append(f"installed systemd unit differs from accepted rendered template: {name}")
    return errors
