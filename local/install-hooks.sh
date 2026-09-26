#!/usr/bin/env sh
# softwareco install-hooks addition (run by scripts/install-hooks.sh): normalize the
# executable bit of company helpers and the other local/ hooks (b46f03a, 29c7647).
set -eu
chmod +x \
	scripts/ubs-staged.sh \
	scripts/install-ubs-pre-commit.sh \
	scripts/materialize-ontology.sh \
	scripts/materialize-ontology.py \
	local/ci/smoke.sh \
	local/ci/full.sh \
	local/ci/check-template-ci.sh \
	local/githooks/pre-commit
