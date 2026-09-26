#!/usr/bin/env sh
# softwareco smoke additions (run by scripts/ci/smoke.sh): staged-file UBS helper tests
# (29c7647, 1f2d1ed).
set -eu
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_ubs_staged -q
