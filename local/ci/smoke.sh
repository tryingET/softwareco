#!/usr/bin/env sh
# softwareco smoke additions (run by scripts/ci/smoke.sh): CI dependency pins (#5786) and
# staged-file UBS helper tests (29c7647, 1f2d1ed), DB-free census fixtures (#6451), and
# stub-ak task-scope checker / template TMPDIR fixtures (#7893).
set -eu
# The CI pin test must also run without a materialized private ontology checkout.
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_ci_dependency_pins tests.test_ubs_staged tests.test_decision157_consumer_census tests.test_offline_hooks tests.test_tpl_task_scope_snapshots -q
