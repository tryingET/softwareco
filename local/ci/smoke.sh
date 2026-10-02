#!/usr/bin/env sh
# softwareco smoke additions (run by scripts/ci/smoke.sh): CI dependency pins (#5786) and
# staged-file UBS helper tests (29c7647, 1f2d1ed), and DB-free census fixtures (#6451).
set -eu
# The CI pin test must also run without a materialized private ontology checkout.
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_ci_dependency_pins tests.test_ubs_staged tests.test_decision157_consumer_census -q
