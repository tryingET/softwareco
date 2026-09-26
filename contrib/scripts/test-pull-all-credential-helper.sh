#!/usr/bin/env bash
# Feature: the contrib sync recognises gh's credential helper and does not rewrite
# ~/.gitconfig on every run (softwareco AK #5930).
#
# `gh auth setup-git` writes URL-scoped helpers (credential.https://github.com.helper).
# The old check read only the plain credential.helper, never matched, and re-ran
# setup-git hourly. Scenarios are Given/When/Then; no gh or network needed.
set -euo pipefail

here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
script="$here/pull-all-local-contrib-repos.sh"
sandbox="$(mktemp -d "${TMPDIR:-/tmp}/cred-helper-test.XXXXXX")"
trap 'rm -rf "$sandbox"' EXIT
fails=0

# Load only the check function from the updater (it runs gh and git at top level otherwise).
sed -n '/^gh_credential_helper_configured()/,/^}/p' "$script" > "$sandbox/check.sh"
if [[ ! -s "$sandbox/check.sh" ]]; then
	echo "FAIL: pull-all-local-contrib-repos.sh defines no gh_credential_helper_configured()"
	exit 1
fi
# shellcheck source=/dev/null
. "$sandbox/check.sh"

scenario() { # name, gitconfig body, expected exit
	local name="$1" body="$2" want="$3" got=0
	# Given a global git config with the example credential helpers
	printf '%b' "$body" > "$sandbox/gitconfig"
	# When the updater checks for gh's helper
	GIT_CONFIG_GLOBAL="$sandbox/gitconfig" gh_credential_helper_configured || got=$?
	# Then it is recognised exactly when gh's helper applies to github.com
	if [[ "$got" != "$want" ]]; then
		echo "FAIL: $name: exit $got, want $want"
		fails=$((fails + 1))
	else
		echo "ok: $name"
	fi
}

scenario "gh setup-git URL-scoped helpers" '[credential "https://github.com"]\n\thelper = \n\thelper = !/usr/bin/gh auth git-credential\n[credential]\n\thelper = cache --timeout=3600\n' 0
scenario "only a cache helper" '[credential]\n\thelper = cache --timeout=3600\n' 1
scenario "no helper at all" '' 1

[[ "$fails" == 0 ]]
