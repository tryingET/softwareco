from __future__ import annotations

import importlib.util
import base64
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/materialize-ontology.py"
SCRATCH = Path(os.environ.get("TMPDIR", str(ROOT)))
SPEC = importlib.util.spec_from_file_location("softwareco_ontology_materializer", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MATERIALIZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATERIALIZER)


def run(*args: str, cwd: Path, expect: int = 0, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, env=env)
    if result.returncode != expect:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expect}: {args}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def init_repo(path: Path) -> None:
    path.mkdir()
    run("git", "init", "--quiet", cwd=path)
    run("git", "config", "user.name", "ontology materializer test", cwd=path)
    run("git", "config", "user.email", "test@example.invalid", cwd=path)
    run("git", "branch", "-M", "main", cwd=path)


def commit_all(repo: Path, message: str) -> str:
    run("git", "add", ".", cwd=repo)
    run("git", "commit", "--quiet", "-m", message, cwd=repo)
    return run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()


def make_source(parent: Path, name: str = "source") -> tuple[Path, str]:
    source = parent / name
    init_repo(source)
    (source / "manifest.yaml").write_text("rocs:\n  id: test.ontology\n", encoding="utf-8")
    (source / "src").mkdir()
    (source / "src/concept.md").write_text("---\nid: test.Concept\n---\n", encoding="utf-8")
    return source, commit_all(source, "ontology source")


def make_parent(parent: Path, source: Path, oid: str, name: str = "parent") -> Path:
    repo = parent / name
    init_repo(repo)
    (repo / "README.md").write_text("parent\n", encoding="utf-8")
    (repo / ".gitmodules").write_text(
        f'[submodule "ontology"]\n\tpath = ontology\n\turl = {source}\n\tbranch = main\n', encoding="utf-8"
    )
    run("git", "add", "README.md", ".gitmodules", cwd=repo)
    run("git", "update-index", "--add", "--cacheinfo", f"160000,{oid},ontology", cwd=repo)
    run("git", "update-index", "--add", "--cacheinfo", f"160000,{oid},other-raw-gitlink", cwd=repo)
    run("git", "commit", "--quiet", "-m", "parent gitlinks", cwd=repo)
    return repo


def invoke(repo: Path, *extra: str, expect: int = 0, env: dict[str, str] | None = None) -> dict[str, object]:
    arguments = list(extra)
    if "--expected-oid" not in arguments:
        row = run("git", "ls-tree", "HEAD", "--", "ontology", cwd=repo).stdout.split()
        arguments.extend(("--expected-oid", row[2] if len(row) >= 3 else "0" * 40))
    if "--source" not in arguments:
        source = run(
            "git", "config", "-f", str(repo / ".gitmodules"), "--get", "submodule.ontology.url",
            cwd=repo, expect=0 if (repo / ".gitmodules").is_file() else 1,
        ).stdout.strip()
        arguments.extend(("--source", source or "missing-source-binding"))
    arguments.append("--allow-local-source")
    result = run(
        "python3",
        "-I",
        "-S",
        "-B",
        str(SCRIPT),
        "--repo-root",
        str(repo),
        *arguments,
        cwd=ROOT,
        expect=expect,
        env=env,
    )
    stream = result.stdout if expect == 0 else result.stderr
    return json.loads(stream)


class OntologyMaterializerTests(unittest.TestCase):
    def test_materializes_only_ontology_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            hostile = os.environ.copy()
            malicious_template = parent / "malicious-template/hooks"
            malicious_template.mkdir(parents=True)
            sentinel = parent / "hook-ran"
            hook = malicious_template / "post-checkout"
            hook.write_text(f"#!/bin/sh\ntouch '{sentinel}'\n", encoding="utf-8")
            hook.chmod(0o755)
            hostile.update(
                {
                    "GIT_DIR": str(source / ".git"),
                    "GIT_WORK_TREE": str(source),
                    "GIT_EXEC_PATH": str(parent / "invalid-git-exec"),
                    "GIT_TEMPLATE_DIR": str(malicious_template.parent),
                    "GIT_CONFIG_PARAMETERS": "'core.fsmonitor=!false'",
                }
            )
            unrelated_before = [
                line
                for line in run("git", "status", "--porcelain", cwd=repo).stdout.splitlines()
                if "other-raw-gitlink" in line
            ]

            first = invoke(repo, env=hostile)
            self.assertTrue(first["ok"])
            self.assertEqual(first["outcome"], "materialized")
            self.assertEqual(run("git", "rev-parse", "HEAD", cwd=repo / "ontology").stdout.strip(), oid)
            self.assertFalse(sentinel.exists())
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=repo).stdout.strip())
            common = (common if common.is_absolute() else repo / common).resolve()
            marker = (repo / "ontology/.git").read_text(encoding="utf-8")
            self.assertEqual(marker, f"gitdir: {common / 'modules/ontology'}\n")
            self.assertEqual(
                run(
                    "git", "--git-dir", str(common / "modules/ontology"),
                    "config", "--get", "core.worktree", cwd=repo,
                ).stdout.strip(),
                str(repo / "ontology"),
            )
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get", "submodule.ontology.url", cwd=repo
                ).stdout.strip(),
                str(source),
            )
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get", "submodule.ontology.active", cwd=repo
                ).stdout.strip(),
                "true",
            )
            self.assertTrue(
                run("git", "submodule", "status", "--", "ontology", cwd=repo).stdout.startswith(
                    " " + oid
                )
            )
            self.assertFalse((repo / "other-raw-gitlink").exists())
            status_after = run("git", "status", "--porcelain", cwd=repo).stdout.splitlines()
            self.assertEqual(
                [line for line in status_after if "other-raw-gitlink" in line], unrelated_before
            )
            self.assertFalse(any("ontology" in line and "other-raw" not in line for line in status_after))

            before = run("git", "status", "--porcelain=v2", cwd=repo).stdout
            second = invoke(repo)
            self.assertEqual(second["outcome"], "already_materialized")
            self.assertEqual(run("git", "status", "--porcelain=v2", cwd=repo).stdout, before)

    def test_unavailable_source_leaves_no_partial_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            missing = parent / "missing-source"
            (repo / ".gitmodules").write_text(
                f'[submodule "ontology"]\n\tpath = ontology\n\turl = {missing}\n\tbranch = main\n', encoding="utf-8"
            )
            run("git", "add", ".gitmodules", cwd=repo)
            run("git", "commit", "--quiet", "-m", "unavailable source", cwd=repo)
            status_before = run("git", "status", "--porcelain", cwd=repo).stdout

            result = invoke(repo, expect=2)
            self.assertFalse(result["ok"])
            self.assertIn("source unavailable", str(result["error"]))
            self.assertFalse((repo / "ontology").exists())
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=repo).stdout.strip())
            common = common if common.is_absolute() else repo / common
            self.assertFalse((common / "modules/ontology").exists())
            self.assertEqual(run("git", "status", "--porcelain", cwd=repo).stdout, status_before)

    def test_rejects_wrong_oid_source_and_partial_state(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            wrong = "0" * 40 if oid != "0" * 40 else "1" * 40
            self.assertIn("differs", str(invoke(repo, "--expected-oid", wrong, expect=2)["error"]))
            other_source, _ = make_source(parent, "other-source")
            self.assertIn(
                "differs", str(invoke(repo, "--source", str(other_source), expect=2)["error"])
            )

            (repo / "ontology").mkdir()
            (repo / "ontology/partial").write_text("partial\n", encoding="utf-8")
            self.assertIn("contains files", str(invoke(repo, expect=2)["error"]))
            self.assertEqual((repo / "ontology/partial").read_text(), "partial\n")

    def test_rejects_dirty_gitmodules_standalone_clone_and_partial_gitdir(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)

            dirty = make_parent(parent, source, oid, "dirty-modules")
            with (dirty / ".gitmodules").open("a", encoding="utf-8") as stream:
                stream.write("# untracked authority drift\n")
            self.assertIn("bytes differ", str(invoke(dirty, expect=2)["error"]))

            standalone = make_parent(parent, source, oid, "standalone")
            run("git", "clone", "--quiet", str(source), str(standalone / "ontology"), cwd=parent)
            self.assertIn("not the registered parent submodule", str(invoke(standalone, expect=2)["error"]))

            partial = make_parent(parent, source, oid, "partial-gitdir")
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=partial).stdout.strip())
            common = common if common.is_absolute() else partial / common
            (common / "modules/ontology").mkdir(parents=True)
            self.assertIn("partial ontology Git metadata", str(invoke(partial, expect=2)["error"]))

    def test_recovers_journaled_activation_before_rematerializing(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            self.assertEqual(invoke(repo)["outcome"], "materialized")
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=repo).stdout.strip())
            common = (common if common.is_absolute() else repo / common).resolve()
            recovery_scratch = Path(
                tempfile.mkdtemp(prefix="softwareco-ontology-materialize.", dir=SCRATCH)
            )
            journal = common / "softwareco-ontology-materialization.json"
            journal.write_text(
                json.dumps(
                    {
                        "schema": MATERIALIZER.SCHEMA,
                        "repo": str(repo),
                        "ontology": str(repo / "ontology"),
                        "gitdir": str(common / "modules/ontology"),
                        "scratch": str(recovery_scratch),
                        "oid": oid,
                        "source": str(source),
                        "had_empty": False,
                        "old_url": [],
                        "old_active": [],
                        "phase": "registered",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(invoke(repo)["outcome"], "materialized")
            self.assertFalse(journal.exists())
            self.assertFalse(recovery_scratch.exists())
            self.assertEqual(run("git", "rev-parse", "HEAD", cwd=repo / "ontology").stdout.strip(), oid)

    def test_lock_initial_journal_failure_and_signals_leave_no_partial_state(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=repo).stdout.strip())
            common = (common if common.is_absolute() else repo / common).resolve()

            with MATERIALIZER._lock(common):
                locked = invoke(repo, expect=2)
            self.assertIn("already in progress", str(locked["error"]))

            scratch_before = set(SCRATCH.glob("softwareco-ontology-materialize.*"))
            with mock.patch.object(
                MATERIALIZER, "_write_journal", side_effect=OSError("journal failure")
            ):
                with self.assertRaisesRegex(OSError, "journal failure"):
                    MATERIALIZER.materialize(repo, oid, str(source), True)
            self.assertEqual(set(SCRATCH.glob("softwareco-ontology-materialize.*")), scratch_before)
            self.assertFalse((common / "softwareco-ontology-materialization.json").exists())
            self.assertFalse((repo / "ontology").exists())

            real_write_journal = MATERIALIZER._write_journal

            def signal_after_journal(*args: object, **kwargs: object) -> None:
                real_write_journal(*args, **kwargs)
                os.kill(os.getpid(), MATERIALIZER.signal.SIGTERM)

            with mock.patch.object(
                MATERIALIZER, "_write_journal", side_effect=signal_after_journal
            ):
                with self.assertRaises(MATERIALIZER.MaterializationInterrupted):
                    MATERIALIZER.materialize(repo, oid, str(source), True)
            self.assertEqual(set(SCRATCH.glob("softwareco-ontology-materialize.*")), scratch_before)
            self.assertFalse((common / "softwareco-ontology-materialization.json").exists())

            real_activate = MATERIALIZER._activate

            def signal_after_activation(*args: object, **kwargs: object) -> Path | None:
                result = real_activate(*args, **kwargs)
                os.kill(os.getpid(), MATERIALIZER.signal.SIGTERM)
                return result

            with mock.patch.object(MATERIALIZER, "_activate", side_effect=signal_after_activation):
                with self.assertRaises(MATERIALIZER.MaterializationInterrupted):
                    MATERIALIZER.materialize(repo, oid, str(source), True)
            self.assertEqual(set(SCRATCH.glob("softwareco-ontology-materialize.*")), scratch_before)
            self.assertFalse((common / "softwareco-ontology-materialization.json").exists())
            self.assertFalse((common / "modules/ontology").exists())
            self.assertFalse((repo / "ontology").exists())

            for signum in (MATERIALIZER.signal.SIGINT, MATERIALIZER.signal.SIGTERM, MATERIALIZER.signal.SIGHUP):
                with self.subTest(signum=signum):
                    with self.assertRaises(MATERIALIZER.MaterializationInterrupted):
                        with MATERIALIZER._signals():
                            os.kill(os.getpid(), signum)

    def test_rejects_missing_metadata_and_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            (repo / ".gitmodules").unlink()
            self.assertIn(
                "missing .gitmodules",
                str(invoke(repo, "--expected-oid", oid, "--source", str(source), expect=2)["error"]),
            )

            (repo / ".gitmodules").write_text(
                f'[submodule "ontology"]\n\tpath = ontology\n\turl = {source}\n\tbranch = main\n', encoding="utf-8"
            )
            (repo / "outside").mkdir()
            (repo / "ontology").symlink_to(repo / "outside", target_is_directory=True)
            self.assertIn("symlink", str(invoke(repo, expect=2)["error"]))

    def test_rejects_missing_or_symlinked_owner_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, _ = make_source(parent)
            (source / "manifest.yaml").unlink()
            missing_oid = commit_all(source, "missing manifest")
            missing_parent = make_parent(parent, source, missing_oid, "missing-parent")
            self.assertIn("ontology manifest", str(invoke(missing_parent, expect=2)["error"]))
            self.assertFalse((missing_parent / "ontology").exists())

            outside = parent / "outside-manifest"
            outside.write_text("rocs: {}\n", encoding="utf-8")
            (source / "manifest.yaml").symlink_to(outside)
            symlink_oid = commit_all(source, "symlink manifest")
            symlink_parent = make_parent(parent, source, symlink_oid, "symlink-parent")
            self.assertIn("regular and non-symlink", str(invoke(symlink_parent, expect=2)["error"]))
            self.assertFalse((symlink_parent / "ontology").exists())

    def test_rejects_hostile_remote_helper_and_lock_types(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            helper_dir = parent / "helpers"
            helper_dir.mkdir()
            sentinel = parent / "remote-helper-ran"
            helper = helper_dir / "git-remote-evil"
            helper.write_text(f"#!/bin/sh\ntouch '{sentinel}'\nexit 1\n", encoding="utf-8")
            helper.chmod(0o755)
            hostile_source = "evil::payload"
            (repo / ".gitmodules").write_text(
                f'[submodule "ontology"]\n\tpath = ontology\n\turl = {hostile_source}\n\tbranch = main\n',
                encoding="utf-8",
            )
            commit_all(repo, "hostile source")
            env = os.environ.copy()
            env["PATH"] = f"{helper_dir}:{env['PATH']}"
            result = invoke(repo, "--source", hostile_source, expect=2, env=env)
            self.assertIn("protocol", str(result["error"]))
            self.assertFalse(sentinel.exists())

            safe_repo = make_parent(parent, source, oid, "lock-parent")
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=safe_repo).stdout.strip())
            common = (common if common.is_absolute() else safe_repo / common).resolve()
            lock = common / "softwareco-ontology-materialization.lock"
            target = parent / "lock-target"
            target.write_text("not a lock\n", encoding="utf-8")
            lock.symlink_to(target)
            self.assertFalse(invoke(safe_repo, expect=2)["ok"])
            lock.unlink()
            os.mkfifo(lock)
            fifo_result = invoke(safe_repo, expect=2)
            self.assertIn("regular", str(fifo_result["error"]))
            lock.unlink()

    def test_approved_https_uses_only_narrow_noninteractive_token(self) -> None:
        with mock.patch.dict(os.environ, {"SOFTWARECO_ONTOLOGY_TOKEN": ""}):
            with self.assertRaisesRegex(MATERIALIZER.MaterializationError, "token is unavailable"):
                MATERIALIZER._auth(
                    MATERIALIZER.APPROVED_SOURCE, "SOFTWARECO_ONTOLOGY_TOKEN", False
                )
        secret = "test-secret-token"
        with mock.patch.dict(os.environ, {"SOFTWARECO_ONTOLOGY_TOKEN": secret}):
            auth = MATERIALIZER._auth(
                MATERIALIZER.APPROVED_SOURCE, "SOFTWARECO_ONTOLOGY_TOKEN", False
            )
        self.assertEqual(auth["GIT_CONFIG_COUNT"], "1")
        self.assertEqual(auth["GIT_CONFIG_KEY_0"], "http.https://github.com/.extraheader")
        self.assertNotIn(secret, json.dumps(auth))
        encoded = auth["GIT_CONFIG_VALUE_0"].split()[-1]
        self.assertEqual(base64.b64decode(encoded).decode(), f"x-access-token:{secret}")
        with self.assertRaisesRegex(MATERIALIZER.MaterializationError, "requires --token-env"):
            MATERIALIZER._auth(MATERIALIZER.APPROVED_SOURCE, "OTHER_TOKEN", False)

    def test_mismatched_journal_and_relation_drift_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            parent = Path(temp)
            source, oid = make_source(parent)
            repo = make_parent(parent, source, oid)
            common = Path(run("git", "rev-parse", "--git-common-dir", cwd=repo).stdout.strip())
            common = (common if common.is_absolute() else repo / common).resolve()
            scratch = Path(tempfile.mkdtemp(prefix="softwareco-ontology-materialize.", dir=SCRATCH))
            journal = common / "softwareco-ontology-materialization.json"
            run(
                "git", "config", "--local", "--add", "submodule.ontology.url", "prior-url",
                cwd=repo,
            )
            run(
                "git", "config", "--local", "--add", "submodule.ontology.active", "false",
                cwd=repo,
            )
            journal.write_text(
                json.dumps(
                    {
                        "schema": MATERIALIZER.SCHEMA,
                        "repo": str(repo),
                        "ontology": str(repo / "ontology"),
                        "gitdir": str(common / "modules/ontology"),
                        "scratch": str(scratch),
                        "oid": oid,
                        "source": str(source),
                        "phase": "prepared",
                        "had_empty": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertIn("journal binding mismatch", str(invoke(repo, expect=2)["error"]))
            self.assertTrue(journal.exists())
            self.assertTrue(scratch.exists())
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get-all", "submodule.ontology.url", cwd=repo
                ).stdout.splitlines(),
                ["prior-url"],
            )
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get-all", "submodule.ontology.active", cwd=repo
                ).stdout.splitlines(),
                ["false"],
            )
            journal.unlink()
            scratch.rmdir()

            run(
                "git", "config", "--local", "--replace-all", "submodule.ontology.url",
                str(source), cwd=repo,
            )
            run(
                "git", "config", "--local", "--replace-all", "submodule.ontology.active",
                "true", cwd=repo,
            )
            transition_scratch = Path(
                tempfile.mkdtemp(prefix="softwareco-ontology-materialize.", dir=SCRATCH)
            )
            journal.write_text(
                json.dumps(
                    {
                        "schema": MATERIALIZER.SCHEMA,
                        "repo": str(repo),
                        "ontology": str(repo / "ontology"),
                        "gitdir": str(common / "modules/ontology"),
                        "scratch": str(transition_scratch),
                        "oid": oid,
                        "source": str(source),
                        "phase": "preparing",
                        "had_empty": False,
                        "old_url": ["attacker-prior-url"],
                        "old_active": ["false"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            transition = invoke(repo, expect=2)
            self.assertIn("config transition mismatch", str(transition["error"]))
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get", "submodule.ontology.url", cwd=repo
                ).stdout.strip(),
                str(source),
            )
            self.assertEqual(
                run(
                    "git", "config", "--local", "--get", "submodule.ontology.active", cwd=repo
                ).stdout.strip(),
                "true",
            )
            self.assertTrue(journal.exists())
            journal.unlink()
            transition_scratch.rmdir()

            (source / "second").write_text("second\n", encoding="utf-8")
            other_oid = commit_all(source, "second source commit")
            real_live = MATERIALIZER._live

            def drift_after_live(
                prepared: Path, expected: str, auth: dict[str, str]
            ) -> None:
                real_live(prepared, expected, auth)
                run(
                    "git", "update-index", "--add", "--cacheinfo",
                    f"160000,{other_oid},ontology", cwd=repo,
                )

            with mock.patch.object(MATERIALIZER, "_live", side_effect=drift_after_live):
                with self.assertRaisesRegex(MATERIALIZER.MaterializationError, "HEAD/index"):
                    MATERIALIZER.materialize(repo, oid, str(source), True)
            self.assertFalse((repo / "ontology").exists())
            self.assertFalse((common / "modules/ontology").exists())
            self.assertFalse(journal.exists())
            run("git", "reset", "--quiet", "HEAD", cwd=repo)

    def test_full_lane_rejects_symlink_manifest_before_rocs(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            repo = Path(temp) / "gate"
            (repo / "scripts/ci").mkdir(parents=True)
            (repo / "ontology").mkdir()
            (repo / "bin").mkdir()
            (repo / "scripts/ci/full.sh").write_bytes((ROOT / "scripts/ci/full.sh").read_bytes())
            (repo / "scripts/ci/full.sh").chmod(0o755)
            (repo / "scripts/ci/smoke.sh").write_text("#!/bin/sh\nexit 0\n")
            (repo / "scripts/ci/smoke.sh").chmod(0o755)
            sentinel = repo / "rocs-ran"
            (repo / "scripts/rocs.sh").write_text(f"#!/bin/sh\ntouch '{sentinel}'\n")
            (repo / "scripts/rocs.sh").chmod(0o755)
            (repo / "bin/python3").write_text("#!/bin/sh\nexit 0\n")
            (repo / "bin/python3").chmod(0o755)
            outside = repo / "outside-manifest"
            outside.write_text("rocs: {}\n")
            (repo / "ontology/manifest.yaml").symlink_to(outside)
            env = os.environ.copy()
            env["PATH"] = f"{repo / 'bin'}:{env['PATH']}"
            result = run("bash", "scripts/ci/full.sh", cwd=repo, expect=1, env=env)
            self.assertIn("may not be a symlink", result.stderr)
            self.assertFalse(sentinel.exists())

    def test_activation_compensates_every_forward_rename_failure(self) -> None:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temp:
            root = Path(temp)
            for had_empty, failure_points in ((False, (1, 2)), (True, (1, 2, 3))):
                for fail_at in failure_points:
                    with self.subTest(had_empty=had_empty, fail_at=fail_at):
                        parent = root / f"case-{int(had_empty)}-{fail_at}"
                        prepared_worktree = parent / "prepared-worktree"
                        prepared_gitdir = parent / "prepared-gitdir"
                        ontology = parent / "ontology"
                        final_gitdir = parent / "modules/ontology"
                        prepared_worktree.mkdir(parents=True)
                        prepared_gitdir.mkdir()
                        final_gitdir.parent.mkdir()
                        if had_empty:
                            ontology.mkdir()
                        real_replace = os.replace
                        calls = 0

                        def fail_selected(
                            source: os.PathLike[str] | str, target: os.PathLike[str] | str
                        ) -> None:
                            nonlocal calls
                            calls += 1
                            if calls == fail_at:
                                raise OSError("injected activation failure")
                            real_replace(source, target)

                        with mock.patch.object(
                            MATERIALIZER.os, "replace", side_effect=fail_selected
                        ):
                            with self.assertRaisesRegex(OSError, "injected activation failure"):
                                MATERIALIZER._activate(
                                    prepared_worktree, prepared_gitdir, ontology, final_gitdir
                                )
                        self.assertTrue(prepared_worktree.is_dir())
                        self.assertTrue(prepared_gitdir.is_dir())
                        self.assertEqual(ontology.exists(), had_empty)
                        if had_empty:
                            self.assertTrue(MATERIALIZER._empty_dir(ontology))
                        self.assertFalse(final_gitdir.exists())


if __name__ == "__main__":
    unittest.main()
