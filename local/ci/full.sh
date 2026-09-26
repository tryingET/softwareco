#!/usr/bin/env sh
# softwareco full-gate additions, run by scripts/ci/full.sh after its ROCS
# cleanup -> validate -> build gate (settings in local/rocs.env). The template gate
# already fails on a symlinked or unmaterialized owner-gitlink ontology (e220516).
set -eu
python3 -m unittest tests.test_ontology_materializer -q
python3 -m unittest tests.test_ontology_receipts -q
