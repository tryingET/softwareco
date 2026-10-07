#!/usr/bin/env python3
"""Refuse a UBS candidate that real consumer files stall, before it becomes every repo's gate.

The service worktree contrib/ultimate_bug_scanner-local is the scanner every repo's pre-commit
runs (scripts/ubs-staged.sh, workstation's quality gate). Re-pinning it changes all of them at
once. UBS 5.4.18 passed its own suite and the refusal-count checks, and within hours livelocked
on ordinary find-first loops in workstation and test-capabilities files (AK6750, AK6781).

For every consumer repo (a repo whose pre-commit runs ubs-staged.sh or the service worktree),
this copies the tracked JS/TS and Python files to scratch, scans each language as one batch with
the incumbent and with the candidate (`ubs --ci --no-cargo --only=<lang> --format=json .`), and
refuses the candidate when, where the incumbent finished:
  - the candidate does not finish within --timeout (the pre-commit would time out), or
  - the candidate reports a partial scan or failed modules (ubs-staged refuses those), or
  - the candidate is more than --max-slowdown times slower, past an absolute --floor.
Criticals the candidate no longer reports are listed but do not refuse: findings change across
releases, yet a solver that stops early also drops findings (AK6781).

Exit 0 pass, 1 refuse, 2 usage or setup error. Read-only toward every consumer repo.
Runbook: docs/project/2026-10-07-ubs-service-adoption-gate.md.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LANGS = {
    "js": (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts"),
    "python": (".py",),
}
HOOK_FILES = (".git/hooks/pre-commit", ".git/ubs-chain-hooks/pre-commit", ".githooks/pre-commit",
              "scripts/git/hooks/pre-commit", "scripts/quality-gate.sh")
HOOK_MARKERS = ("ubs-staged", "ultimate_bug_scanner-local")
SKIP_DIRS = {"node_modules", ".worktrees", ".venv", ".git", "dist", "target"}


def discover(root: Path, depth: int) -> list[Path]:
    """Git repos under root whose pre-commit runs the service scanner."""
    found = []

    def walk(directory: Path, level: int) -> None:
        if (directory / ".git").exists():
            for rel in HOOK_FILES:
                hook = directory / rel
                try:
                    text = hook.read_text(errors="replace")
                except OSError:
                    continue
                if any(marker in text for marker in HOOK_MARKERS):
                    found.append(directory)
                    break
        if level >= depth:
            return
        try:
            children = sorted(entry for entry in directory.iterdir()
                              if entry.is_dir() and not entry.is_symlink() and entry.name not in SKIP_DIRS)
        except OSError:
            return
        for child in children:
            walk(child, level + 1)

    walk(root, 0)
    return found


def tracked(repo: Path, exts: tuple[str, ...], limit: int) -> list[str]:
    listing = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True)
    paths = [p for p in listing.stdout.decode("utf-8", "surrogateescape").split("\0")
             if p.endswith(exts) and (repo / p).is_file()]
    # Over the cap, keep the largest files: analysis cost grows with size.
    paths.sort(key=lambda p: (-(repo / p).stat().st_size, p))
    return sorted(paths[:limit])


def stage(repo: Path, paths: list[str], target: Path) -> None:
    for rel in paths + [".ubsignore"]:
        source = repo / rel
        if source.is_file():
            destination = target / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def scan(ubs: str, lang: str, files: Path, timeout: float) -> dict:
    cache = files.parent / f"cache-{Path(ubs).name}"
    cache.mkdir(exist_ok=True)
    env = {**os.environ, "UBS_NO_CACHE": "1", "XDG_CACHE_HOME": str(cache)}
    started = time.monotonic()
    try:
        result = subprocess.run([ubs, "--ci", "--no-cargo", f"--only={lang}", "--format=json", "."],
                                cwd=files, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"finished": False, "seconds": round(time.monotonic() - started, 2)}
    seconds = round(time.monotonic() - started, 2)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"finished": True, "seconds": seconds, "status": f"unparsable (exit {result.returncode})",
                "criticals": set()}
    criticals = {(os.path.relpath(f.get("file", ""), files), f.get("rule_id"), f.get("line"))
                 for f in data.get("findings", [])
                 if f.get("severity") == "critical" and not f.get("suppressed")}
    status = data.get("status", "")
    if data.get("failed_modules"):
        status = f"{status}; failed modules {data['failed_modules']}"
    return {"finished": True, "seconds": seconds, "status": status, "criticals": criticals}


def judge(incumbent: dict, candidate: dict, args: argparse.Namespace) -> list[str]:
    refusals = []
    if not incumbent["finished"]:
        return refusals  # nothing to compare against; the report shows both
    if not candidate["finished"]:
        return [f"candidate did not finish within {args.timeout:g} s "
                f"(incumbent {incumbent['seconds']:g} s)"]
    if candidate["status"] != "ok" and incumbent["status"] == "ok":
        refusals.append(f"candidate scan is not complete ({candidate['status'] or 'no status'}; "
                        "a partial scan is refused by ubs-staged)")
    limit = args.max_slowdown * max(incumbent["seconds"], args.floor)
    if candidate["seconds"] > limit:
        refusals.append(f"candidate {candidate['seconds']:g} s is more than {args.max_slowdown:g}x "
                        f"slower than incumbent {incumbent['seconds']:g} s (floor {args.floor:g} s)")
    return refusals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--candidate", required=True, help="ubs of the build to adopt")
    parser.add_argument("--incumbent", default=str(Path.home() / "ai-society/softwareco/contrib/"
                                                   "ultimate_bug_scanner-local/ubs"))
    parser.add_argument("--root", default=str(Path.home() / "ai-society"), help="where consumer repos live")
    parser.add_argument("--repo", action="append", default=[], help="scan these repos instead of discovering")
    parser.add_argument("--depth", type=int, default=6)
    parser.add_argument("--langs", default="js,python")
    parser.add_argument("--max-files", type=int, default=400, help="per repo and language; largest first")
    parser.add_argument("--timeout", type=float, default=300, help="per scan; the pre-commit module timeout")
    parser.add_argument("--max-slowdown", type=float, default=5)
    parser.add_argument("--floor", type=float, default=2, help="seconds below which ratios do not matter")
    parser.add_argument("--scratch", help="scratch directory (default: under $TMPDIR)")
    parser.add_argument("--report", help="write the JSON report here")
    args = parser.parse_args()

    for ubs in (args.incumbent, args.candidate):
        if not os.access(ubs, os.X_OK):
            print(f"ubs-adoption-canary: not executable: {ubs}", file=sys.stderr)
            return 2
    langs = [lang for lang in args.langs.split(",") if lang]
    unknown = [lang for lang in langs if lang not in LANGS]
    if unknown:
        print(f"ubs-adoption-canary: unknown language(s) {unknown}; known {sorted(LANGS)}", file=sys.stderr)
        return 2
    repos = [Path(r).resolve() for r in args.repo] or discover(Path(args.root), args.depth)
    if not repos:
        print(f"ubs-adoption-canary: no consumer repos under {args.root}", file=sys.stderr)
        return 2
    scratch = Path(args.scratch) if args.scratch else Path(tempfile.mkdtemp(prefix="ubs-adoption-canary-"))
    scratch.mkdir(parents=True, exist_ok=True)

    scans = []
    for index, repo in enumerate(repos):
        for lang in langs:
            paths = tracked(repo, LANGS[lang], args.max_files)
            if not paths:
                continue
            files = scratch / f"{index:03d}-{repo.name}-{lang}" / "files"
            stage(repo, paths, files)
            incumbent = scan(args.incumbent, lang, files, args.timeout)
            candidate = scan(args.candidate, lang, files, args.timeout)
            refusals = judge(incumbent, candidate, args)
            dropped = (sorted(incumbent["criticals"] - candidate["criticals"])
                       if incumbent.get("criticals") is not None and candidate.get("criticals") is not None
                       else [])
            row = {"repo": str(repo), "lang": lang, "files": len(paths),
                   "incumbent": {k: v for k, v in incumbent.items() if k != "criticals"},
                   "candidate": {k: v for k, v in candidate.items() if k != "criticals"},
                   "refusals": refusals, "criticals_dropped": len(dropped),
                   "dropped_examples": [list(item) for item in dropped[:5]]}
            scans.append(row)
            mark = "REFUSE" if refusals else "ok"
            note = f" dropped {len(dropped)} critical(s)" if dropped else ""
            print(f"{mark:6} {repo.name}/{lang}: {len(paths)} files, incumbent "
                  f"{incumbent['seconds']:g} s, candidate {candidate['seconds']:g} s{note}", flush=True)
            for reason in refusals:
                print(f"       - {reason}", flush=True)

    verdict = "refuse" if any(row["refusals"] for row in scans) else "pass"
    report = {"verdict": verdict, "incumbent": args.incumbent, "candidate": args.candidate,
              "thresholds": {"timeout": args.timeout, "max_slowdown": args.max_slowdown, "floor": args.floor},
              "repos": [str(r) for r in repos], "scans": scans}
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=1) + "\n")
    print(f"verdict: {verdict} ({sum(bool(row['refusals']) for row in scans)} of {len(scans)} scans refused)")
    return 1 if verdict == "refuse" else 0


if __name__ == "__main__":
    sys.exit(main())
