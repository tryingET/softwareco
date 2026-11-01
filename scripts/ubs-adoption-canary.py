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
import math
import os
import shutil
import stat
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


class SetupError(Exception):
    """A canary could not be set up; this is not an adoption verdict."""


def write_report(path: str | None, report: dict) -> None:
    if not path:
        return
    target = Path(path)
    try:
        target.write_text(json.dumps(report, indent=1) + "\n")
    except OSError as error:
        # A failed write must not leave an earlier pass looking current.
        try:
            target.unlink(missing_ok=True)
        except OSError as cleanup:
            raise SetupError(f"cannot write report {path}: {error}; cannot remove stale report: "
                             f"{cleanup}; any existing report is NOT current") from error
        raise SetupError(f"cannot write report {path}: {error}") from error


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.stat().st_mode)
    except FileNotFoundError:
        return False  # tracked files deleted from the working tree are not scanned


def discover(root: Path, depth: int) -> list[Path]:
    """Git repos under root whose pre-commit runs the service scanner."""
    found = []

    def walk(directory: Path, level: int) -> None:
        if (directory / ".git").exists():
            for rel in HOOK_FILES:
                hook = directory / rel
                try:
                    text = hook.read_text(errors="replace")
                except (FileNotFoundError, NotADirectoryError):
                    continue
                if any(marker in text for marker in HOOK_MARKERS):
                    found.append(directory)
                    break
        if level >= depth:
            return
        children = sorted(entry for entry in directory.iterdir()
                          if entry.is_dir() and not entry.is_symlink() and entry.name not in SKIP_DIRS)
        for child in children:
            walk(child, level + 1)

    walk(root, 0)
    return found


def tracked(repo: Path, exts: tuple[str, ...], limit: int) -> list[str]:
    listing = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True)
    if listing.returncode:
        detail = listing.stderr.decode("utf-8", "replace").strip()
        raise SetupError(f"git ls-files failed for {repo} (exit {listing.returncode}): {detail}")
    paths = [p for p in listing.stdout.decode("utf-8", "surrogateescape").split("\0")
             if p.endswith(exts) and regular_file(repo / p)]
    # Over the cap, keep the largest files: analysis cost grows with size.
    paths.sort(key=lambda p: (-(repo / p).stat().st_size, p))
    return sorted(paths[:limit])


def stage(repo: Path, paths: list[str], target: Path) -> None:
    extras = [".ubsignore"] if regular_file(repo / ".ubsignore") else []
    for rel in paths + extras:
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / rel, destination)


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


def run(args: argparse.Namespace, report: dict) -> None:
    for name in ("timeout", "max_slowdown", "floor"):
        raw = getattr(args, name)
        bound = "nonnegative" if name == "floor" else "positive"
        diagnostic = f"--{name.replace('_', '-')} must be finite and {bound} (got {raw!r})"
        try:
            value = float(raw)
        except ValueError as error:
            raise SetupError(diagnostic) from error
        if not math.isfinite(value) or (value < 0 if name == "floor" else value <= 0):
            raise SetupError(diagnostic)
        setattr(args, name, value)
        report["thresholds"][name] = value

    for ubs in (args.incumbent, args.candidate):
        if not os.access(ubs, os.X_OK):
            raise SetupError(f"not executable: {ubs}")
    langs = [lang for lang in args.langs.split(",") if lang]
    if not langs:
        raise SetupError("--langs must select at least one language")
    unknown = [lang for lang in langs if lang not in LANGS]
    if unknown:
        raise SetupError(f"unknown language(s) {unknown}; known {sorted(LANGS)}")
    if args.max_files <= 0:
        raise SetupError("--max-files must be positive")
    repos = [Path(r).resolve() for r in args.repo] or discover(Path(args.root), args.depth)
    report["repos"] = [str(r) for r in repos]
    if not repos:
        raise SetupError(f"no consumer repos under {args.root}")
    scratch = Path(args.scratch) if args.scratch else Path(tempfile.mkdtemp(prefix="ubs-adoption-canary-"))
    scratch.mkdir(parents=True, exist_ok=True)

    scans = report["scans"]
    for index, repo in enumerate(repos):
        for lang in langs:
            paths = tracked(repo, LANGS[lang], args.max_files)
            if not paths:
                continue
            row = {"repo": str(repo), "lang": lang, "files": len(paths)}
            scans.append(row)  # keep any actual results if a later setup step fails
            files = scratch / f"{index:03d}-{repo.name}-{lang}" / "files"
            stage(repo, paths, files)
            incumbent = scan(args.incumbent, lang, files, args.timeout)
            row["incumbent"] = {k: v for k, v in incumbent.items() if k != "criticals"}
            candidate = scan(args.candidate, lang, files, args.timeout)
            row["candidate"] = {k: v for k, v in candidate.items() if k != "criticals"}
            report["executed_pairs"] += 1
            refusals = judge(incumbent, candidate, args)
            dropped = (sorted(incumbent["criticals"] - candidate["criticals"])
                       if incumbent.get("criticals") is not None and candidate.get("criticals") is not None
                       else [])
            row.update({"refusals": refusals, "criticals_dropped": len(dropped),
                        "dropped_examples": [list(item) for item in dropped[:5]]})
            mark = "REFUSE" if refusals else "ok"
            note = f" dropped {len(dropped)} critical(s)" if dropped else ""
            print(f"{mark:6} {repo.name}/{lang}: {len(paths)} files, incumbent "
                  f"{incumbent['seconds']:g} s, candidate {candidate['seconds']:g} s{note}", flush=True)
            for reason in refusals:
                print(f"       - {reason}", flush=True)

    if not report["executed_pairs"]:
        raise SetupError("no repo/language pairs executed (no tracked files for selected languages)")


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
    # Parse thresholds inside handled setup so invalid values still replace stale reports.
    parser.add_argument("--timeout", default="300", help="per scan; the pre-commit module timeout")
    parser.add_argument("--max-slowdown", default="5")
    parser.add_argument("--floor", default="2", help="seconds below which ratios do not matter")
    parser.add_argument("--scratch", help="scratch directory (default: under $TMPDIR)")
    parser.add_argument("--report", help="write the JSON report here")
    args = parser.parse_args()

    report = {"verdict": "setup_error", "error": "run has not completed",
              "incumbent": args.incumbent, "candidate": args.candidate,
              # Keep unchecked input as text: NaN/Infinity are not standard JSON numbers.
              "thresholds": {"timeout": args.timeout, "max_slowdown": args.max_slowdown, "floor": args.floor},
              "repos": [], "scans": [], "executed_pairs": 0}
    try:
        write_report(args.report, report)  # invalidate an old pass before any setup work
        run(args, report)
        scans = report["scans"]
        verdict = "refuse" if any(row["refusals"] for row in scans) else "pass"
        report.update(verdict=verdict)
        del report["error"]
        write_report(args.report, report)
    except (SetupError, OSError) as error:
        report.update(verdict="setup_error", error=str(error))
        print(f"ubs-adoption-canary: {error}", file=sys.stderr)
        try:
            write_report(args.report, report)
        except SetupError as report_error:
            print(f"ubs-adoption-canary: {report_error}", file=sys.stderr)
        return 2

    print(f"verdict: {verdict} ({sum(bool(row['refusals']) for row in scans)} of "
          f"{report['executed_pairs']} executed pairs refused)")
    return 1 if verdict == "refuse" else 0


if __name__ == "__main__":
    sys.exit(main())
