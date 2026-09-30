#!/usr/bin/env sh
# softwareco template-check additions, run first by scripts/check-template-ci.sh:
# owner-gitlink ontology preconditions (Decision 144; 1d71fd6, e220516), the parent ROCS
# output contract (f950a4e) and the targeted ontology materializer wiring.
set -eu

fail() {
	echo "error: $*" >&2
	exit 1
}
assert_file() {
	[ -f "$1" ] || fail "missing file: $1"
}
assert_not_file() {
	[ ! -e "$1" ] || fail "unexpected file: $1"
}
assert_exec() {
	[ -x "$1" ] || fail "expected executable: $1"
}
assert_contains() {
	grep -qF -- "$2" "$1" || fail "$3 (missing '$2' in $1)"
}
assert_not_contains() {
	if grep -qF -- "$2" "$1"; then
		fail "$3 (found '$2' in $1)"
	fi
}

if [ -L ontology/manifest.yaml ]; then
	echo "error: ontology manifest may not be a symlink" >&2
	exit 1
fi
if [ ! -f ontology/manifest.yaml ]; then
	[ -f .gitmodules ] && [ ! -L .gitmodules ] || {
		echo "error: unmaterialized ontology lacks regular .gitmodules" >&2
		exit 1
	}
	expected_oid=b2e42daf61a889c08745b922056b627753f45a2c
	expected_source=https://github.com/tryingET/softwareco-ontology.git
	[ "$(git rev-parse HEAD:.gitmodules)" = "$(git rev-parse :.gitmodules)" ] || {
		echo "error: indexed .gitmodules differs from HEAD" >&2
		exit 1
	}
	[ "$(git hash-object .gitmodules)" = "$(git rev-parse HEAD:.gitmodules)" ] || {
		echo "error: worktree .gitmodules differs from HEAD" >&2
		exit 1
	}
	[ "$(git config -f .gitmodules --get submodule.ontology.path)" = ontology ] || exit 1
	[ "$(git config -f .gitmodules --get submodule.ontology.url)" = "$expected_source" ] || exit 1
	[ "$(git config -f .gitmodules --get submodule.ontology.branch)" = main ] || exit 1
	expected_entry="$(printf '160000 commit %s\tontology' "$expected_oid")"
	[ "$(git ls-tree HEAD -- ontology)" = "$expected_entry" ] || {
		echo "error: HEAD ontology gitlink does not match the accepted OID" >&2
		exit 1
	}
fi

# Parent ROCS contract: outputs live in governance/ontology-dist, only the parent is a target.
assert_contains "local/rocs.env" 'ROCS_OUTPUT_ROOT must be $softwareco_output_root' "company ROCS env must enforce the exact parent-owned output root"
assert_contains "local/rocs.env" 'softwareco_output_root="governance/ontology-dist"' "company ROCS env must route outputs outside ontology"
assert_contains "local/rocs.env" "ROCS_AUTHORITY_AGGREGATE=1" "company ROCS env must preserve validate/build authority receipts"
assert_contains "local/rocs.env" "--repo must be the Softwareco parent" "company ROCS env must reject non-parent command targets"
assert_contains "local/rocs.env" "ROCS_REPO must be the Softwareco parent" "company ROCS env must reject non-parent environment targets"
assert_contains "local/ci/full.sh" "tests.test_ontology_receipts" "company full gate must verify the parent ROCS receipts"
assert_contains "local/ci/full.sh" "tests.test_ontology_materializer" "company full gate must execute ontology materializer behavior tests"
assert_file "tests/test_ontology_receipts.py"
for legacy_receipt in \
	ontology/dist/.authority-receipt.lock \
	ontology/dist/authority-receipt.json \
	ontology/dist/authority-receipt.validate.json \
	ontology/dist/id_index.json \
	ontology/dist/resolve.json \
	ontology/dist/summary.json; do
	assert_not_file "$legacy_receipt"
done

# Targeted ontology materializer.
assert_file "scripts/materialize-ontology.py"
assert_file "scripts/materialize-ontology.sh"
assert_file "tests/test_ontology_materializer.py"
assert_exec "scripts/materialize-ontology.py"
assert_exec "scripts/materialize-ontology.sh"
assert_contains "scripts/materialize-ontology.py" "submodule.ontology.path" "ontology materializer must bind the exact declared submodule path"
assert_contains "scripts/materialize-ontology.py" "--git-common-dir" "ontology materializer must prepare metadata in the parent Git common directory"
assert_contains "scripts/materialize-ontology.py" "softwareco-ontology-materialization.json" "ontology materializer must journal interrupted activation"
assert_contains "scripts/materialize-ontology.py" "required=True" "ontology materializer must require independent source and OID bindings"
assert_not_contains "scripts/materialize-ontology.py" "--recursive" "ontology materializer must never initialize unrelated raw gitlinks recursively"

# Root CI workflow (company-owned) wiring for the private ontology owner.
ci_workflow=".github/workflows/ci.yml"
assert_contains "$ci_workflow" "./scripts/materialize-ontology.sh" "root CI must use the targeted ontology materializer when declared"
assert_contains "$ci_workflow" "SOFTWARECO_ONTOLOGY_TOKEN" "root CI must use the narrowly scoped noninteractive ontology credential"
assert_contains "$ci_workflow" "github.ref == 'refs/heads/main'" "manual token-bearing lanes must be restricted to main"
if awk '/^  smoke:/{inside=1} /^  full:/{inside=0} inside{print}' "$ci_workflow" | grep -qF SOFTWARECO_ONTOLOGY_TOKEN; then
	fail "pull-request smoke job must not receive the private ontology token"
fi
if ! awk '/^  smoke:/{inside=1} /^  full:/{inside=0} inside{print}' "$ci_workflow" | grep -qF 'ontology manifest may not be a symlink'; then
	fail "pull-request smoke job must reject a symlinked ontology manifest"
fi
assert_contains "$ci_workflow" "ontology manifest may not be a symlink" "root CI must reject a symlinked ontology manifest"
assert_contains "$ci_workflow" "if [ ! -f ontology/manifest.yaml ]" "root CI must materialize or fail when ontology is absent"
assert_contains "$ci_workflow" "ROCS_OUTPUT_ROOT: governance/ontology-dist" "root CI must route ROCS outputs outside ontology"
assert_contains "$ci_workflow" 'ROCS_AUTHORITY_AGGREGATE: "1"' "root CI must preserve validate/build authority receipts"
assert_contains "$ci_workflow" "https://github.com/tryingET/core_ontology-kernel.git" "root CI must materialize the strict core dependency"
assert_contains "$ci_workflow" "a6d38f56dd9b91e0a03b96444385402aecf1b9b0" "root CI must verify the exact strict core dependency OID"
assert_not_contains "$ci_workflow" "submodules: recursive" "root CI must not initialize unrelated raw gitlinks recursively"

# Staged-file UBS wiring (29c7647, 1f2d1ed, b46f03a).
assert_contains "local/githooks/pre-commit" "scripts/ubs-staged.sh" "company pre-commit must scan staged files with the contrib UBS checkout"
assert_contains "local/ci/smoke.sh" "tests.test_ubs_staged" "company smoke lane must run the UBS helper tests"
assert_contains "local/install-hooks.sh" "scripts/ubs-staged.sh" "company install-hooks must normalize the UBS helper executable bit"

echo "ok: softwareco template-check additions"
