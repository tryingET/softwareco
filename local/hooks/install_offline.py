#!/usr/bin/env python3
"""Install the qualified AK7597 chain in ONE allowed repository's Git metadata."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
OWNER = HERE.parents[1]
PROTOCOL = "softwareco-offline-index-v1"
ROOT_CONTRACTS = {
    ".githooks/pre-commit": "84032adb16acd572fce7ad9055b03d2768113d671767fb1bf78e8f1188b0eee4",
    "local/githooks/pre-commit": "c6a3c78596dcb57baea465b6e9af0882a69e7dcc558853c9c65b3e7478a04ecd",
}


def git(root, *args):
    # Installer must target the named repository even when called inside a hook.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.check_output(["git", "--no-lazy-fetch", "-C", str(root), *args], env=env)


def sha(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"required regular source missing or symlinked: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_file(root, rel):
    entries = [entry for entry in git(root, "ls-files", "--stage", "-z", "--", rel).split(b"\0") if entry]
    if len(entries) != 1:
        raise RuntimeError(f"native entry must be one executable stage-0 blob: {rel}")
    header, path = entries[0].split(b"\t", 1)
    mode, _, stage = header.split()
    if mode != b"100755" or stage != b"0" or path != os.fsencode(rel):
        raise RuntimeError(f"native entry must be executable and stage-0 in index: {rel}")
    return git(root, "show", f":{rel}")


def atomic(path, data, executable=False):
    path = Path(path)
    if path.is_symlink():
        raise RuntimeError(f"refusing generated metadata symlink: {path}")
    if path.exists() and path.read_bytes() == data and (not executable or os.access(path, os.X_OK)):
        return
    fd, temporary = tempfile.mkstemp(prefix=".install-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, 0o755 if executable else 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def install(args):
    root = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()).resolve()
    workspace = Path.home() / "ai-society/softwareco"
    allowed = [workspace, *(workspace / "owned" / name for name in
                            ("dep-viz", "dep-diet", "dep-surgeon", "dep-redteam"))]
    if common not in [(path / ".git").resolve() for path in allowed]:
        raise RuntimeError("target is outside exact AK7597 root/four-repository adoption scope")
    if args.mode == "softwareco" and common != (workspace / ".git").resolve():
        raise RuntimeError("Softwareco native mode is root-only")
    runner = HERE / "offline_commit.py"
    ubs = OWNER / "scripts/ubs-staged.sh"
    scanner = workspace / "contrib/ultimate_bug_scanner-local/ubs"
    hashes = {str(path): sha(path) for path in (Path(__file__).resolve(), runner, ubs)}
    if not os.access(ubs, os.X_OK) or not os.access(scanner, os.X_OK):
        raise RuntimeError("real UBS service executable or staged wrapper unavailable")
    scanner_sha = sha(scanner)
    # Refuse before changing any config if this host cannot enforce offline use.
    subprocess.run(["unshare", "--user", "--map-current-user", "--net", "--", sys.executable,
                    "-c", "import socket; assert all(n == 'lo' for _, n in socket.if_nameindex())"], check=True)
    git(root, "merge-base", "HEAD", args.base_ref)
    smoke_sha = hashlib.sha256(index_file(root, "scripts/ci/smoke.sh")).hexdigest()
    native_hook_sha = hashlib.sha256(index_file(root, ".githooks/pre-commit")).hexdigest()
    if args.mode == "native-v1" and (smoke_sha != args.native_sha256 or native_hook_sha != args.native_hook_sha256):
        raise RuntimeError("native SHA arguments must match independently qualified indexed smoke AND pre-commit")
    if args.mode == "softwareco":
        for rel, expected in ROOT_CONTRACTS.items():
            if hashlib.sha256(index_file(root, rel)).hexdigest() != expected:
                raise RuntimeError(f"unrecognized Softwareco native contract: {rel}")
    destination = common / "softwareco-offline-hooks-v1"
    if destination.is_symlink():
        raise RuntimeError("refusing symlinked managed hook directory")
    existing = subprocess.run(["git", "-C", str(root), "config", "--get", "core.hooksPath"],
                              capture_output=True, text=True,
                              env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    if existing.returncode not in (0, 1):
        raise RuntimeError("cannot inspect existing hooks configuration")
    prior = existing.stdout.strip()
    if prior not in ("", ".githooks", ".git/ubs-chain-hooks", str(destination)):
        raise RuntimeError(f"unrecognized prior hooksPath; preserve and seek owner disposition: {prior}")
    worktree_config = subprocess.run(["git", "-C", str(root), "config", "--bool", "--get", "extensions.worktreeConfig"],
                                     capture_output=True, text=True,
                                     env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    worktrees = [Path(line[9:]) for line in git(root, "worktree", "list", "--porcelain").decode().splitlines()
                 if line.startswith("worktree ")]
    if worktree_config.stdout.strip() == "true":
        for worktree in worktrees:
            override = subprocess.run(["git", "-C", str(worktree), "config", "--worktree", "--get", "core.hooksPath"],
                                      capture_output=True, text=True,
                                      env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
            if override.returncode not in (0, 1) or (override.returncode == 0 and override.stdout.strip() != str(destination)):
                raise RuntimeError(f"conflicting worktree hooks override; owner disposition required: {worktree}")
    # Preserve every hook obligation; refuse an unmodeled hook instead of losing it.
    prior_dir = common / "ubs-chain-hooks" if prior == ".git/ubs-chain-hooks" else root / (prior or str(common / "hooks"))
    if prior != str(destination) and prior_dir.is_dir():
        extras = [p.name for p in prior_dir.iterdir()
                  if not p.name.endswith(".sample") and p.name not in ("pre-commit", "pre-push")]
        if extras:
            raise RuntimeError(f"additional hooks require owner integration: {extras}")
    if not prior and ((prior_dir / "pre-commit").exists() or (prior_dir / "pre-commit").is_symlink()):
        raise RuntimeError("unknown default pre-commit obligation; owner integration required")
    if prior == ".git/ubs-chain-hooks" and (prior_dir / "pre-commit").exists():
        canonical = common.parent
        original_ubs = workspace / "scripts/ubs-staged.sh"
        old = (f'#!/usr/bin/env sh\nset -eu\n"{original_ubs}" || exit $?\n'
               f'if [ -x "{canonical}/.githooks/pre-commit" ]; then\n'
               f'  exec "{canonical}/.githooks/pre-commit"\nfi\nexit 0\n')
        if (prior_dir / "pre-commit").read_text() != old:
            raise RuntimeError("unrecognized legacy pre-commit obligations; owner integration required")
    prepush = root / ".githooks/pre-push"
    preserve_push = prepush.is_file() and os.access(prepush, os.X_OK)
    prior_push = prior_dir / "pre-push"
    if (prior_push.exists() or prior_push.is_symlink()) and not preserve_push:
        raise RuntimeError("existing pre-push obligation has no executable worktree-native counterpart")
    if prior != str(destination) and prior_push.exists() and prior_push.resolve() != prepush.resolve():
        canonical_push = common.parent / ".githooks/pre-push"
        if not (prior == ".git/ubs-chain-hooks" and prior_push.is_symlink()
                and prior_push.resolve() == canonical_push.resolve()
                and prior_push.read_bytes() == prepush.read_bytes()):
            raise RuntimeError("non-native existing pre-push requires owner integration")
    metadata = {
        "protocol": PROTOCOL, "common_dir": str(common), "base_ref": args.base_ref,
        "native_mode": args.mode, "native_sha256": smoke_sha, "native_hook_sha256": native_hook_sha,
        "ubs_staged": str(ubs), "scanner": str(scanner), "scanner_sha256": scanner_sha,
        "source_hashes": hashes, "root_contracts": ROOT_CONTRACTS if args.mode == "softwareco" else {},
        "preserve_pre_push": preserve_push,
    }
    destination.mkdir(mode=0o700, exist_ok=True)
    config = destination / "config.json"
    hook = ("#!/bin/sh\nset -eu\nexec " + shlex.quote(sys.executable) + " " +
            shlex.quote(str(runner)) + " " + shlex.quote(str(config)) + "\n")
    atomic(config, (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode())
    atomic(destination / "pre-commit", hook.encode(), True)
    if preserve_push:
        push = ('#!/bin/sh\nset -eu\nroot="$(git rev-parse --show-toplevel)"\n'
                'test -x "$root/.githooks/pre-push" || exit 2\n'
                'exec "$root/.githooks/pre-push" "$@"\n')
        atomic(destination / "pre-push", push.encode(), True)
    elif (destination / "pre-push").exists():
        raise RuntimeError("prior installed pre-push obligation cannot be removed implicitly")
    git(root, "config", "--local", "core.hooksPath", str(destination))
    for worktree in worktrees:
        discovered = git(worktree, "rev-parse", "--path-format=absolute", "--git-path", "hooks/pre-commit").decode().strip()
        if Path(discovered) != destination / "pre-commit":
            raise RuntimeError(f"Git hook discovery did not activate qualified chain: {worktree}")
    print(json.dumps({"protocol": PROTOCOL, "hooks_path": str(destination),
                      "config_sha256": sha(config), "source_hashes": hashes,
                      "scanner_sha256": scanner_sha, "native_sha256": smoke_sha,
                      "native_hook_sha256": native_hook_sha,
                      "worktree": str(root)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--mode", choices=("native-v1", "softwareco"), required=True)
    parser.add_argument("--native-sha256")
    parser.add_argument("--native-hook-sha256")
    parser.add_argument("--base-ref", default="refs/heads/main")
    try:
        install(parser.parse_args())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"offline-install: REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
