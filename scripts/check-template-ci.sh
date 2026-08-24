#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$repo_root"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: missing dependency: $1" >&2
    exit 2
  }
}

need_cmd awk
need_cmd find
need_cmd git
need_cmd grep
need_cmd mktemp
need_cmd sort
need_cmd python3

fail() {
  echo "error: $*" >&2
  exit 1
}

assert_file() {
  path="$1"
  [ -f "$path" ] || fail "missing file: $path"
}

assert_not_file() {
  path="$1"
  [ ! -f "$path" ] || fail "unexpected file present: $path"
}

assert_exec() {
  path="$1"
  [ -x "$path" ] || fail "missing executable bit: $path"
}

assert_dir() {
  path="$1"
  [ -d "$path" ] || fail "missing directory: $path"
}

assert_not_dir() {
  path="$1"
  [ ! -d "$path" ] || fail "unexpected directory present: $path"
}

assert_contains() {
  path="$1"
  needle="$2"
  label="$3"
  grep -qF -- "$needle" "$path" || fail "$label (missing '$needle' in $path)"
}

assert_not_contains() {
  path="$1"
  needle="$2"
  label="$3"
  if grep -qF -- "$needle" "$path"; then
    fail "$label (found '$needle' in $path)"
  fi
}

assert_line_precedes() {
  path="$1"
  first="$2"
  second="$3"
  label="$4"

  first_line="$(grep -nF -- "$first" "$path" | awk -F ':' 'NR == 1 { print $1 }')"
  second_line="$(grep -nF -- "$second" "$path" | awk -F ':' 'NR == 1 { print $1 }')"

  [ -n "$first_line" ] || fail "$label (missing '$first' in $path)"
  [ -n "$second_line" ] || fail "$label (missing '$second' in $path)"
  [ "$first_line" -lt "$second_line" ] || fail "$label (expected '$first' before '$second' in $path)"
}

assert_command_succeeds() {
  label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    return 0
  fi
  fail "$label"
}

check_document_policy_regressions() {
  policy_source="$repo_root/copier/tpl-project-repo/scripts/check-document-policy.sh"
  tmp_dir="$(mktemp -d)"

  if (
    set -eu
    cd "$tmp_dir" || exit 1
    git init -q || exit 1
    git config user.name template-check || exit 1
    git config user.email template-check@example.invalid || exit 1
    mkdir -p docs/project scripts || exit 1
    cp "$policy_source" scripts/check-document-policy.sh || exit 1
    chmod +x scripts/check-document-policy.sh || exit 1
    printf '# Evidence\n' > README.md || exit 1
    git add README.md scripts/check-document-policy.sh || exit 1
    git commit -qm baseline || exit 1
    baseline="$(git rev-parse HEAD)" || exit 1
    today="$(date -u +%F)" || exit 1

    cat > docs/project/product_posture.md <<EOF
---
summary: "test posture"
read_when:
  - "testing document policy"
type: "reference"
as_of: "$today"
last_validated: "$today"
last_validated_commit: "$baseline"
evidence_paths:
  - "README.md"
---
EOF
    git add docs/project/product_posture.md || exit 1
    git commit -qm valid-posture || exit 1
    PRODUCT_POSTURE_TEST_MODE=1 PRODUCT_POSTURE_TODAY="$today" ./scripts/check-document-policy.sh >/dev/null || exit 1

    git reset -q --hard "$baseline" || exit 1
    mkdir -p docs/project || exit 1
    cat > docs/project/product_posture.md <<EOF
---
summary: "pathspec injection"
read_when:
  - "testing document policy"
type: "reference"
as_of: "$today"
last_validated: "$today"
last_validated_commit: "$baseline"
evidence_paths:
  - ":(exclude,glob)docs/**"
---
EOF
    git add docs/project/product_posture.md || exit 1
    git commit -qm pathspec-injection || exit 1
    if PRODUCT_POSTURE_TEST_MODE=1 PRODUCT_POSTURE_TODAY="$today" ./scripts/check-document-policy.sh >/dev/null 2>&1; then
      exit 1
    fi

    git reset -q --hard "$baseline" || exit 1
    mkdir -p docs/project || exit 1
    cat > docs/project/product_posture.md <<EOF
# Missing frontmatter delimiters
as_of: "$today"
last_validated: "$today"
last_validated_commit: "$baseline"
evidence_paths:
  - "README.md"
EOF
    git add docs/project/product_posture.md || exit 1
    git commit -qm malformed-frontmatter || exit 1
    if PRODUCT_POSTURE_TEST_MODE=1 PRODUCT_POSTURE_TODAY="$today" ./scripts/check-document-policy.sh >/dev/null 2>&1; then
      exit 1
    fi
  ); then
    rm -rf "$tmp_dir"
    return 0
  fi

  rm -rf "$tmp_dir"
  fail "document-policy regression: valid posture must pass while pathspec injection and body-only metadata fail closed"
}

suffix_policy_lib="$repo_root/scripts/lib/suffix-policy.sh"
[ -f "$suffix_policy_lib" ] || fail "missing file: $suffix_policy_lib"
# shellcheck source=/dev/null
. "$suffix_policy_lib"

check_multi_pass_suffix_policy() {
  self_test_untemplated_jinja_matcher || fail "suffix-policy matcher regression: expected to ignore GitHub expressions and detect unsuffixed Jinja markers"

  for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo tpl-package; do
    tpl_suffix="$(yaml_scalar_value "copier/$tpl/copier.yml" "_templates_suffix")"
    [ "$tpl_suffix" = ".j2" ] || fail "L2 template $tpl copier config must use .j2 suffix (found ${tpl_suffix:-<missing>})"
  done

  nested_jinja="$(first_suffix_match "copier" "*.jinja")"
  [ -z "$nested_jinja" ] || fail "pass-boundary suffix policy violated: nested L2 templates must not use .jinja (found $nested_jinja)"

  outer_j2="$(first_suffix_match "." "*.j2" "./copier/*")"
  [ -z "$outer_j2" ] || fail "pass-boundary suffix policy violated: L1 surface must not use .j2 outside copier/ (found $outer_j2)"

  nested_untemplated_jinja="$(first_untemplated_jinja_match "copier" ".j2")"
  [ -z "$nested_untemplated_jinja" ] || fail "pass-boundary suffix policy violated: nested L2 template file contains Jinja markers but is not suffixed .j2 (found $nested_untemplated_jinja)"
}

list_template_files() {
  template_dir="$1"

  find "$template_dir" -type f | while IFS= read -r abs_path; do
    rel_path="${abs_path#$template_dir/}"
    case "$rel_path" in
      */__pycache__/*|*.pyc)
        continue
        ;;
    esac
    printf '%s\n' "$rel_path"
  done | LC_ALL=C sort
}

value_from_answers() {
  answers_file="$1"
  key="$2"

  awk -F':' -v key="$key" '
    $1 ~ "^" key "$" {
      v=$2
      gsub(/^[ \t]+|[ \t]+$/, "", v)
      gsub(/"/, "", v)
      gsub(/\047/, "", v)
      print tolower(v)
      exit
    }
  ' "$answers_file"
}

bool_from_answers() {
  value_from_answers "$1" "$2"
}

# L1-level required files
required_files="
README.md
AGENTS.md
CONTRIBUTING.md
.gitattributes
.copier-answers.yml
contracts/layer-contract.yml
contracts/provenance-seal.yml
scripts/new-repo-from-copier.sh
scripts/bootstrap-lane-root.sh
scripts/rocs.sh
scripts/check-template-ci.sh
scripts/install-hooks.sh
scripts/lib/suffix-policy.sh
scripts/ci/smoke.sh
scripts/ci/full.sh
.github/VOUCHED.td
.github/workflows/template-check.yml
.github/workflows/ci.yml
.github/workflows/vouch-check-pr.yml
.github/workflows/vouch-manage.yml
.githooks/pre-commit
.githooks/pre-push
docs/.gitkeep
docs/dev/tpl-project-repo-file-contract.md
docs/org/operating_model.md
examples/.gitkeep
external/.gitkeep
ontology/.gitkeep
policy/.gitkeep
src/.gitkeep
tests/.gitkeep
diary/README.md
"

for path in $required_files; do
  assert_file "$path"
done

assert_contains "ontology/manifest.yaml" '<repo:core/ontology-kernel@v0.2.0>' "Softwareco ontology manifest must pin the protected core release"
for output in   ontology/dist/authority-receipt.build.json   ontology/dist/authority-receipt.validate.json   ontology/dist/authority-receipt.json   ontology/dist/resolve.json   ontology/dist/summary.json; do
  assert_contains "$output" '<repo:core/ontology-kernel@v0.2.0>' "Softwareco ontology output must match the protected core release pin"
done

# L2 embedded templates required
for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo tpl-package; do
  assert_dir "copier/$tpl"
  assert_file "copier/$tpl/copier.yml"
  assert_file "copier/$tpl/AGENTS.md.j2"
  assert_file "copier/$tpl/CODEOWNERS.j2"
  assert_file "copier/$tpl/scripts/rocs.sh.j2"
  assert_exec "copier/$tpl/scripts/rocs.sh.j2"
  assert_file "copier/$tpl/scripts/ci/smoke.sh"
  if [ "$tpl" = "tpl-project-repo" ]; then
    assert_file "copier/$tpl/{{ _copier_conf.answers_file }}.j2"
    assert_not_file "copier/$tpl/.copier-answers.yml.j2"
    assert_file "copier/$tpl/contracts/layer-contract.yml"
    assert_not_file "copier/$tpl/ontology/manifest.yaml"
    assert_not_dir "copier/$tpl/ontology/dist"
    assert_file "copier/$tpl/scripts/check-task-scope-snapshots.sh"
    assert_file "copier/$tpl/scripts/check-document-policy.sh"
    assert_exec "copier/$tpl/scripts/check-document-policy.sh"
    assert_contains "copier/$tpl/scripts/ci/full.sh" "check-document-policy.sh" "tpl-project-repo full CI should enforce document freshness policy"
    assert_contains "copier/$tpl/copier.yml" 'default: "<repo:core/ontology-kernel@v0.2.0>"' "tpl-project-repo should default core ontology refs to the protected release tag"
    assert_file "copier/$tpl/scripts/preflight-repo-census.sh.j2"
    assert_file "copier/$tpl/scripts/lib/check-task-scope-snapshots.py"
    assert_file "copier/$tpl/scripts/lib/copier-answers.sh"
    assert_file "copier/$tpl/scripts/lib/repo-surface.sh.j2"
    assert_file "copier/$tpl/scripts/ci/fast.sh"
  fi
  if [ "$tpl" = "tpl-monorepo" ]; then
    assert_file "copier/$tpl/{{ _copier_conf.answers_file }}.j2"
    assert_not_file "copier/$tpl/.copier-answers.yml.j2"
    assert_file "copier/$tpl/contracts/layer-contract.yml"
    assert_file "copier/$tpl/docs/org_context/README.md"
    assert_file "copier/$tpl/docs/org_context/org-summary.md"
    assert_file "copier/$tpl/governance/work-items.json.j2"
    assert_file "copier/$tpl/scripts/check-task-scope-snapshots.sh"
    assert_file "copier/$tpl/scripts/preflight-repo-census.sh.j2"
    assert_file "copier/$tpl/scripts/lib/check-task-scope-snapshots.py"
    assert_file "copier/$tpl/scripts/lib/copier-answers.sh"
    assert_file "copier/$tpl/scripts/lib/repo-surface.sh.j2"
  fi
  if [ "$tpl" = "tpl-package" ]; then
    assert_file "copier/$tpl/{{ _copier_conf.answers_file }}.j2"
    assert_not_file "copier/$tpl/.copier-answers.yml.j2"
    assert_file "copier/$tpl/contracts/layer-contract.yml"
  fi
  assert_file "copier/$tpl/scripts/ci/full.sh"
  if [ "$tpl" = "tpl-agent-repo" ]; then
    assert_file "copier/$tpl/governance/README.md"
    assert_file "copier/$tpl/governance/work-items.json.j2"
    assert_dir "copier/$tpl/governance/task-scopes"
    assert_file "copier/$tpl/scripts/check-task-scope-snapshots.sh"
    assert_exec "copier/$tpl/scripts/check-task-scope-snapshots.sh"
    assert_file "copier/$tpl/scripts/lib/check-task-scope-snapshots.py"
    assert_not_dir "copier/$tpl/prompts/cognitive-tools"
  fi
  assert_file "copier/$tpl/diary/README.md"
  assert_contains "copier/$tpl/diary/README.md" "YYYY-MM-DD--type-scope-summary.md" "L2 template $tpl diary README should enforce descriptive filename convention"
  assert_not_dir "copier/$tpl/docs/diary"
  assert_contains "copier/$tpl/AGENTS.md.j2" "Deterministic tooling policy" "L2 template $tpl AGENTS should include deterministic tooling policy"
  assert_contains "copier/$tpl/AGENTS.md.j2" "scripts/rocs.sh" "L2 template $tpl AGENTS should reference scripts/rocs.sh"
  assert_contains "copier/$tpl/AGENTS.md.j2" "diary/" "L2 template $tpl AGENTS should reference repo-local diary"
  assert_contains "copier/$tpl/README.md.j2" "ROCS command flow" "L2 template $tpl README should include ROCS command flow section"
  assert_contains "copier/$tpl/scripts/ci/full.sh" "scripts/rocs.sh" "L2 template $tpl full CI should use scripts/rocs.sh when ontology is present"
  if [ "$tpl" = "tpl-project-repo" ]; then
    assert_not_file "copier/$tpl/.gitlab-ci.yml"
    assert_not_dir "copier/$tpl/gitlab"
  fi
done
for tpl in tpl-agent-repo tpl-project-repo; do
  agents="copier/$tpl/AGENTS.md.j2"
  assert_contains "$agents" "does not appoint organizational roles or grant company delegation" "$tpl must not infer organizational appointment"
  assert_contains "$agents" "missing, expired, or ambiguous, stop and escalate" "$tpl must fail closed on delegation ambiguity"
  assert_contains "$agents" "scoped owner-native task and finite-WIP" "$tpl must require finite-WIP task admission"
  assert_contains "$agents" "Passing validation is not an outcome" "$tpl must separate validation from outcomes"
  assert_contains "$agents" "External effects and terminal" "$tpl must reserve effects and terminal decisions"
  assert_contains "$agents" "never a shadow backlog" "$tpl must keep steward packets non-authoritative"
done
assert_not_contains "copier/tpl-agent-repo/AGENTS.md.j2" "work via proposals + merge requests" "agent template must not contradict main-first policy"
assert_contains "copier/tpl-agent-repo/AGENTS.md.j2" "Prompt Vault query/retrieve surfaces" "agent template must route reusable procedures through Prompt Vault"
assert_contains "copier/tpl-agent-repo/AGENTS.md.j2" "engineering-core" "agent template must provide generic engineering-core guidance"
assert_contains "copier/tpl-agent-repo/README.md.j2" "Prompt Vault query/retrieve surfaces" "agent README must route reusable procedures through Prompt Vault"
assert_contains "copier/tpl-agent-repo/README.md.j2" "engineering-core" "agent README must provide generic engineering guidance"
assert_not_contains "copier/tpl-agent-repo/README.md.j2" "Softwareco's L1 template" "generic agent template must not leak Softwareco identity"
assert_contains "copier/tpl-agent-repo/scripts/ci/full.sh" 'AK_CMD="${AK_CMD:-ak}"' "agent full CI must use plain configurable AK"

if [ -f "next_session_prompt.md" ]; then
  assert_command_succeeds "canonical docs-list should parse repo next-session prompt" node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --from-prompt next_session_prompt.md --paths-only --wikilink
fi
assert_file "copier/tpl-project-repo/docs/project/product_posture.md"
assert_contains "copier/tpl-project-repo/docs/project/product_posture.md" "last_validated_commit:" "tpl-project-repo posture should declare a commit evidence baseline"
assert_contains "copier/tpl-project-repo/docs/project/product_posture.md" "evidence_paths:" "tpl-project-repo posture should declare evidence paths"
assert_contains "copier/tpl-project-repo/docs/project/product_posture.md" "YYYY-MM-DD--current-vs-target--<scope>.md" "tpl-project-repo posture should document dated snapshot naming"
assert_contains "copier/tpl-project-repo/next_session_prompt.md" "Do not store an active handoff window" "tpl-project-repo next-session prompt should remain procedural rather than carry status"
assert_not_file "copier/tpl-project-repo/docs/project/strategic_goals.md"
assert_not_file "copier/tpl-project-repo/docs/project/tactical_goals.md"
assert_not_file "copier/tpl-project-repo/docs/project/operating_plan.md"
assert_not_file "copier/tpl-project-repo/docs/project/operational_plan.md"
assert_command_succeeds "canonical docs-list should parse tpl-project-repo next-session prompt" node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --from-prompt copier/tpl-project-repo/next_session_prompt.md --paths-only --wikilink
check_document_policy_regressions
assert_not_contains "copier/tpl-project-repo/scripts/ci/full.sh" "./scripts/ak.sh" "tpl-project-repo CI should use plain installed ak via AK_CMD"
assert_not_contains "copier/tpl-project-repo/scripts/ci/full.sh" "uvx -n --from ./tools/rocs-cli rocs" "tpl-project-repo CI should not hardcode uvx vendored invocation"

main_first_policy='Main-first workflow: commit directly to `main` for normal work.'
for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo; do
  assert_contains "copier/$tpl/AGENTS.md.j2" "$main_first_policy" "L2 template $tpl AGENTS should match Softwareco main-first policy"
  assert_not_contains "copier/$tpl/AGENTS.md.j2" 'Never push to `main`' "L2 template $tpl AGENTS should not contradict Softwareco main-first policy"
  assert_not_contains "copier/$tpl/AGENTS.md.j2" 'No direct pushes to `main`' "L2 template $tpl AGENTS should not retain stale branch-only policy"
done


check_multi_pass_suffix_policy

required_exec="
scripts/new-repo-from-copier.sh
scripts/bootstrap-lane-root.sh
scripts/rocs.sh
scripts/check-template-ci.sh
copier/tpl-project-repo/scripts/check-document-policy.sh
scripts/install-hooks.sh
scripts/ci/smoke.sh
scripts/ci/full.sh
.githooks/pre-commit
.githooks/pre-push
"

for path in $required_exec; do
  assert_exec "$path"
done

for doc in README.md AGENTS.md; do
  assert_contains "$doc" "Recursion policy" "L1 docs must contain recursion policy section"
  assert_contains "$doc" "L1 -> L2" "L1 docs must allow L1 -> L2"
  assert_contains "$doc" "L1 -> L0" "L1 docs must forbid L1 -> L0"
  assert_contains "$doc" "L2 -> L1" "L1 docs must forbid L2 -> L1"
done
assert_contains "CONTRIBUTING.md" "check-template-ci.sh" "L1 contributing guide should reference template checks"
assert_contains "CONTRIBUTING.md" "scripts/rocs.sh --doctor" "L1 contributing guide should include deterministic ROCS wrapper usage"
assert_contains "AGENTS.md" "Deterministic tooling policy" "L1 AGENTS should document deterministic tooling policy"
assert_contains "AGENTS.md" "core/agent-scripts/scripts/docs-list.mjs" "L1 AGENTS should reference canonical docs-list implementation"
assert_contains "AGENTS.md" "Do not add company-, repo-, or package-local docs-list wrappers" "L1 AGENTS should prohibit consumer docs-list wrappers"
assert_contains "AGENTS.md" "scripts/rocs.sh" "L1 AGENTS should reference scripts/rocs.sh"
assert_contains "AGENTS.md" "diary/" "L1 AGENTS should require repo-local diary"
assert_contains "AGENTS.md" "L2 Templates" "L1 AGENTS should document L2 templates"
assert_contains "AGENTS.md" "bootstrap-lane-root.sh" "L1 AGENTS should document lane bootstrap helper"
assert_contains "README.md" "Organization docs profile" "L1 README should describe organization docs profile"
assert_contains "README.md" "Governance layering" "L1 README should describe governance layering"
assert_contains "README.md" "Community profile" "L1 README should describe community profile toggle"
assert_contains "README.md" "Release profile" "L1 README should describe release profile toggle"
assert_contains "README.md" "Baseline structure" "L1 README should describe baseline directory structure"
assert_contains "README.md" "Deterministic ROCS launcher" "L1 README should document deterministic ROCS launcher"
assert_contains "README.md" "Multi-pass template suffix policy" "L1 README should document multi-pass suffix policy"
assert_contains "README.md" "repo-local diary" "L1 README should document repo-local diary contract"
assert_contains "README.md" "no automatic in-place migrator" "L1 README should describe deterministic migration limitation"
assert_contains "README.md" ".gitattributes" "L1 README should mention git baseline files"
assert_contains "README.md" "tpl-project-repo-file-contract.md" "L1 README should link canonical tpl-project-repo file contract"
assert_contains "README.md" "bootstrap-lane-root.sh" "L1 README should document lane bootstrap workflow"
assert_contains ".gitignore" "!owned/.gitignore" "L1 parent .gitignore must unignore owned lane-root .gitignore"
assert_contains ".gitignore" "!contrib/.gitignore" "L1 parent .gitignore must unignore contrib lane-root .gitignore"
assert_contains ".gitignore" "!infra/.gitignore" "L1 parent .gitignore must unignore infra lane-root .gitignore"
assert_contains ".gitignore" "!agents/.gitignore" "L1 parent .gitignore must unignore agents lane-root .gitignore"
assert_contains "diary/README.md" "YYYY-MM-DD--type-scope-summary.md" "L1 diary README should enforce descriptive filename convention"

contract="contracts/layer-contract.yml"
assert_contains "$contract" "layer: L1" "L1 contract layer mismatch"
assert_contains "$contract" "L0 -> L1" "L1 contract must include L0 -> L1"
assert_contains "$contract" "L1 -> L2" "L1 contract must include L1 -> L2"
assert_contains "$contract" "L1 -> L0" "L1 contract must include forbidden reverse edge"
assert_contains "$contract" "L2 -> L1" "L1 contract must include forbidden reverse edge"
assert_contains "$contract" "nested_copier_tasks_allowed: false" "L1 contract must forbid nested copier tasks"

provenance="contracts/provenance-seal.yml"
assert_contains "$provenance" "schema: ai-society.template-provenance.v1" "L1 provenance seal schema mismatch"
assert_contains "$provenance" "layer: L1" "L1 provenance seal layer mismatch"
assert_contains "$provenance" "source_sha:" "L1 provenance seal must include source sha"
if grep -q "__RENDER_HASH__" "$provenance"; then
  fail "L1 provenance seal must not retain hash placeholder"
fi

assert_contains ".copier-answers.yml" "l0_source_sha:" "L1 answers file should persist L0 source sha"
assert_contains ".copier-answers.yml" "l1_org_docs_profile:" "L1 answers file should persist L1 org docs profile"

# Check L2 template copier configs
for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo; do
  assert_contains "copier/$tpl/copier.yml" "company_slug" "L2 template $tpl must expose company_slug"
  assert_contains "copier/$tpl/copier.yml" "repo_slug" "L2 template $tpl must expose repo_slug"
  assert_contains "copier/$tpl/copier.yml" "enable_community_pack" "L2 template $tpl must expose community pack toggle"
  assert_contains "copier/$tpl/copier.yml" "enable_release_pack" "L2 template $tpl must expose release pack toggle"
  assert_contains "copier/$tpl/copier.yml" "enable_vouch_gate" "L2 template $tpl must expose vouch gate toggle"
done
assert_contains "copier/tpl-project-repo/copier.yml" "org_docs_profile" "tpl-project-repo must expose org-context profile"
assert_contains "copier/tpl-monorepo/copier.yml" "org_docs_profile" "tpl-monorepo must expose org-context profile"
assert_contains "copier/tpl-package/copier.yml" "package_owner_handle" "tpl-package must expose package owner handle"
assert_contains "copier/tpl-package/copier.yml" "template_source_sha" "tpl-package must expose template source sha"

assert_contains "scripts/new-repo-from-copier.sh" "tpl-agent-repo" "L1 wrapper must list tpl-agent-repo template"
assert_contains "scripts/new-repo-from-copier.sh" "tpl-org-repo" "L1 wrapper must list tpl-org-repo template"
assert_contains "scripts/new-repo-from-copier.sh" "tpl-project-repo" "L1 wrapper must list tpl-project-repo template"
assert_contains "scripts/new-repo-from-copier.sh" "tpl-monorepo" "L1 wrapper must list tpl-monorepo template"
assert_contains "scripts/new-repo-from-copier.sh" "tpl-package" "L1 wrapper must list tpl-package template"
assert_contains "scripts/bootstrap-lane-root.sh" "--init-lane-git" "lane bootstrap helper must support lane git initialization"
assert_contains "scripts/bootstrap-lane-root.sh" "tpl-project-repo" "lane bootstrap helper must render tpl-project-repo baseline"

expected_pin='COPIER_VERSION="${COPIER_VERSION:-9.11.1}"'
expected_uvx='uvx --from "copier==${COPIER_VERSION}" copier'
expected_uvtool='uv tool run --from "copier==${COPIER_VERSION}" copier'
fallback_warning='warning: uvx/uv not found; falling back to unpinned copier on PATH'
uvx_guard='if command -v uvx >/dev/null 2>&1; then'
uv_guard='if command -v uv >/dev/null 2>&1; then'
copier_guard='if command -v copier >/dev/null 2>&1; then'

assert_contains "scripts/new-repo-from-copier.sh" "$expected_pin" "L1 wrapper must pin Copier version"
assert_contains "scripts/new-repo-from-copier.sh" "$expected_uvx" "L1 wrapper must use pinned uvx invocation"
assert_contains "scripts/new-repo-from-copier.sh" "$expected_uvtool" "L1 wrapper must use pinned uv tool invocation"
assert_contains "scripts/new-repo-from-copier.sh" "$fallback_warning" "L1 wrapper must surface unpinned fallback warning"
assert_not_contains "scripts/new-repo-from-copier.sh" "uvx copier" "L1 wrapper must not call unpinned uvx copier"
assert_line_precedes "scripts/new-repo-from-copier.sh" "$uvx_guard" "$uv_guard" "L1 wrapper must prefer uvx before uv tool run"
assert_line_precedes "scripts/new-repo-from-copier.sh" "$uv_guard" "$copier_guard" "L1 wrapper must prefer pinned runtimes before unpinned copier"

workflow=".github/workflows/template-check.yml"
assert_contains "$workflow" "pull_request:" "template-check workflow must run on pull requests"
assert_contains "$workflow" "push:" "template-check workflow must run on pushes"
assert_contains "$workflow" "./scripts/check-template-ci.sh" "template-check workflow must run template checks"

ci_workflow=".github/workflows/ci.yml"
assert_contains "$ci_workflow" "Setup uv (full lane)" "ci full lane must provision uv before running full checks"
assert_contains "$ci_workflow" "Run full lane" "ci workflow must expose full lane"

assert_contains ".githooks/pre-commit" "scripts/ci/smoke.sh" "pre-commit must run smoke lane"
assert_contains ".githooks/pre-push" "scripts/ci/full.sh" "pre-push must run full lane"
assert_contains "scripts/ci/full.sh" "scripts/rocs.sh" "L1 full CI should use scripts/rocs.sh when ontology is present"
assert_not_contains "scripts/install-hooks.sh" "copier/template-repo" "install-hooks must not reference removed legacy template-repo path"
assert_contains "scripts/install-hooks.sh" "scripts/bootstrap-lane-root.sh" "install-hooks must normalize executable bit for lane bootstrap helper"
for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo tpl-package; do
  assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/rocs.sh.j2" "install-hooks must include executable bit normalization for $tpl rocs wrapper"
  assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/ci/smoke.sh" "install-hooks must include executable bit normalization for $tpl smoke lane"
  if [ "$tpl" = "tpl-project-repo" ]; then
    assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/check-task-scope-snapshots.sh" "install-hooks must include executable bit normalization for $tpl task-scope checker"
    assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/preflight-repo-census.sh.j2" "install-hooks must include executable bit normalization for $tpl census wrapper"
    assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/ci/fast.sh" "install-hooks must include executable bit normalization for $tpl fast lane"
  fi
  if [ "$tpl" = "tpl-monorepo" ]; then
    assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/check-task-scope-snapshots.sh" "install-hooks must include executable bit normalization for $tpl task-scope checker"
    assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/preflight-repo-census.sh.j2" "install-hooks must include executable bit normalization for $tpl census wrapper"
  fi
  assert_contains "scripts/install-hooks.sh" "copier/$tpl/scripts/ci/full.sh" "install-hooks must include executable bit normalization for $tpl full lane"
done
assert_not_contains "scripts/ci/smoke.sh" "copier/template-repo/copier.yml" "L1 smoke lane must not lint removed legacy template-repo path"
assert_contains "scripts/ci/smoke.sh" "copier.yml copier/*/copier.yml" "L1 smoke lane should lint nested copier configs"

vouch_enabled="$(bool_from_answers .copier-answers.yml enable_vouch_gate || true)"
if [ "$vouch_enabled" = "true" ]; then
  assert_contains ".github/workflows/vouch-check-pr.yml" "pull_request_target" "vouch-check-pr must be active when enable_vouch_gate=true"
  assert_contains ".github/workflows/vouch-check-pr.yml" "mitchellh/vouch/action/check-pr@5713ce1baedf75e2f830afa3dac813a9c48bff12" "vouch-check-pr action must be SHA pinned"
  assert_contains ".github/workflows/vouch-check-pr.yml" "require-vouch: \"true\"" "vouch-check-pr must enforce vouched contributors"
  assert_contains ".github/workflows/vouch-manage.yml" "issue_comment" "vouch-manage must be active when enable_vouch_gate=true"
  assert_contains ".github/workflows/vouch-manage.yml" "mitchellh/vouch/action/manage-by-issue@5713ce1baedf75e2f830afa3dac813a9c48bff12" "vouch-manage action must be SHA pinned"
else
  assert_contains ".github/workflows/vouch-check-pr.yml" "workflow_dispatch:" "vouch-check-pr should be inactive when enable_vouch_gate=false"
  assert_contains ".github/workflows/vouch-check-pr.yml" "vouch gate disabled" "vouch-check-pr disabled workflow should explain status"
  assert_contains ".github/workflows/vouch-manage.yml" "workflow_dispatch:" "vouch-manage should be inactive when enable_vouch_gate=false"
  assert_contains ".github/workflows/vouch-manage.yml" "vouch manage workflow disabled" "vouch-manage disabled workflow should explain status"
fi

community_enabled="$(bool_from_answers .copier-answers.yml enable_community_pack || true)"
if [ "$community_enabled" = "true" ]; then
  assert_file "CODE_OF_CONDUCT.md"
  assert_file "SUPPORT.md"
  assert_file ".github/pull_request_template.md"
  assert_file ".github/ISSUE_TEMPLATE/config.yml"
  assert_file ".github/ISSUE_TEMPLATE/bug-report.yml"
  assert_file ".github/ISSUE_TEMPLATE/feature-request.yml"
  assert_contains ".github/ISSUE_TEMPLATE/config.yml" "blank_issues_enabled: false" "community issue-template config should disable blank issues"
else
  assert_not_file "CODE_OF_CONDUCT.md"
  assert_not_file "SUPPORT.md"
  assert_not_file ".github/pull_request_template.md"
  assert_not_file ".github/ISSUE_TEMPLATE/config.yml"
  assert_not_file ".github/ISSUE_TEMPLATE/bug-report.yml"
  assert_not_file ".github/ISSUE_TEMPLATE/feature-request.yml"
fi

release_enabled="$(bool_from_answers .copier-answers.yml enable_release_pack || true)"
if [ "$release_enabled" = "true" ]; then
  assert_file ".release-please-config.json"
  assert_file ".release-please-manifest.json"
  assert_file "CHANGELOG.md"
  assert_file "SECURITY.md"
  assert_file ".github/workflows/release-please.yml"
  assert_file ".github/workflows/release-check.yml"
  assert_file ".github/workflows/publish.yml"
  assert_exec "scripts/release/check.sh"
  assert_exec "scripts/release/publish.sh"
  assert_contains ".github/workflows/release-please.yml" "googleapis/release-please-action@v4" "release-please workflow should use release-please action"
  assert_contains ".github/workflows/publish.yml" "softprops/action-gh-release@v2" "publish workflow should upload release artifacts"
else
  assert_not_file ".release-please-config.json"
  assert_not_file ".release-please-manifest.json"
  assert_not_file "CHANGELOG.md"
  assert_not_file "SECURITY.md"
  assert_not_file ".github/workflows/release-please.yml"
  assert_not_file ".github/workflows/release-check.yml"
  assert_not_file ".github/workflows/publish.yml"
  assert_not_file "scripts/release/check.sh"
  assert_not_file "scripts/release/publish.sh"
fi

l1_org_docs_profile="$(value_from_answers .copier-answers.yml l1_org_docs_profile || true)"
[ -n "$l1_org_docs_profile" ] || l1_org_docs_profile="rich"

if [ "$l1_org_docs_profile" = "rich" ]; then
  assert_file "docs/org/purpose.md"
  assert_file "docs/org/mission.md"
  assert_file "docs/org/vision.md"
  assert_file "docs/org/strategic_objectives.md"
  assert_file "docs/org/values_ethics.md"
  assert_file "docs/org/governance.md"
  assert_file "docs/org/glossary.md"
else
  assert_not_file "docs/org/purpose.md"
  assert_not_file "docs/org/mission.md"
  assert_not_file "docs/org/vision.md"
  assert_not_file "docs/org/strategic_objectives.md"
  assert_not_file "docs/org/values_ethics.md"
  assert_not_file "docs/org/governance.md"
  assert_not_file "docs/org/glossary.md"
fi

# Ensure no generated Python build/cache artifacts are committed in embedded templates
if find copier -type d \( -name '__pycache__' -o -name '*.egg-info' \) | grep -q .; then
  fail "embedded template source contains generated python cache/metadata directories"
fi
if find copier -type f -name '*.pyc' | grep -q .; then
  fail "embedded template source contains generated python bytecode files"
fi
if find copier -type d -path '*/tools/rocs-cli/build' | grep -q .; then
  fail "embedded template source contains rocs-cli build output directory"
fi

# Test L2 generation for each template
tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

for tpl in tpl-agent-repo tpl-org-repo tpl-project-repo tpl-monorepo; do
  l2_dir="$tmp_root/$tpl"
  ./scripts/new-repo-from-copier.sh "$tpl" "$l2_dir" \
    -d repo_slug="$tpl" \
    --defaults --overwrite >/dev/null

  # Basic L2 checks
  assert_file "$l2_dir/.copier-answers.yml"
  assert_file "$l2_dir/AGENTS.md"
  assert_file "$l2_dir/CODEOWNERS"
  assert_file "$l2_dir/scripts/rocs.sh"
  assert_file "$l2_dir/scripts/ci/smoke.sh"
  if [ "$tpl" = "tpl-project-repo" ]; then
    assert_file "$l2_dir/contracts/layer-contract.yml"
    assert_file "$l2_dir/ontology/manifest.yaml"
    assert_not_dir "$l2_dir/ontology/dist"
    assert_file "$l2_dir/scripts/check-task-scope-snapshots.sh"
    assert_file "$l2_dir/scripts/preflight-repo-census.sh"
    assert_file "$l2_dir/scripts/lib/check-task-scope-snapshots.py"
    assert_file "$l2_dir/scripts/lib/copier-answers.sh"
    assert_file "$l2_dir/scripts/lib/repo-surface.sh"
    assert_file "$l2_dir/scripts/ci/fast.sh"
  fi
  if [ "$tpl" = "tpl-monorepo" ]; then
    assert_file "$l2_dir/contracts/layer-contract.yml"
    assert_file "$l2_dir/policy/engineering-lane.json"
    assert_contains "$l2_dir/policy/engineering-lane.json" '"lane_status": "monorepo_control_plane"' "generated tpl-monorepo root should declare monorepo control-plane engineering posture"
    assert_contains "$l2_dir/policy/engineering-lane.json" '"disciplines"' "generated tpl-monorepo root should declare scanner-visible disciplines"
    assert_file "$l2_dir/docs/org_context/README.md"
    assert_file "$l2_dir/docs/org_context/org-summary.md"
    assert_file "$l2_dir/governance/work-items.json"
    assert_file "$l2_dir/scripts/check-task-scope-snapshots.sh"
    assert_file "$l2_dir/scripts/preflight-repo-census.sh"
    assert_file "$l2_dir/scripts/lib/check-task-scope-snapshots.py"
    assert_file "$l2_dir/scripts/lib/copier-answers.sh"
    assert_file "$l2_dir/scripts/lib/repo-surface.sh"
  fi
  assert_file "$l2_dir/scripts/ci/full.sh"
  if [ "$tpl" = "tpl-agent-repo" ]; then
    assert_file "$l2_dir/governance/README.md"
    assert_file "$l2_dir/governance/work-items.json"
    assert_dir "$l2_dir/governance/task-scopes"
    assert_file "$l2_dir/scripts/check-task-scope-snapshots.sh"
    assert_exec "$l2_dir/scripts/check-task-scope-snapshots.sh"
    assert_file "$l2_dir/scripts/lib/check-task-scope-snapshots.py"
    assert_exec "$l2_dir/scripts/lib/check-task-scope-snapshots.py"
    assert_contains "$l2_dir/README.md" "Prompt Vault query/retrieve surfaces" "generated agent README must route through Prompt Vault"
    assert_contains "$l2_dir/README.md" "engineering-core" "generated agent README must provide engineering guidance"
    assert_not_contains "$l2_dir/README.md" "Softwareco's L1 template" "generated agent README must remain company-neutral"
    assert_not_contains "$l2_dir/AGENTS.md" "work via proposals + merge requests" "generated agent instructions must not retain stale MR-only intent"
    assert_not_dir "$l2_dir/prompts/cognitive-tools"
  fi
  assert_file "$l2_dir/diary/README.md"
  assert_contains "$l2_dir/diary/README.md" "YYYY-MM-DD--type-scope-summary.md" "generated $tpl diary README should enforce descriptive filename convention"
  assert_not_dir "$l2_dir/docs/diary"
  assert_exec "$l2_dir/scripts/rocs.sh"
  assert_contains "$l2_dir/AGENTS.md" "Deterministic tooling policy" "generated $tpl AGENTS should include deterministic tooling policy"
  assert_contains "$l2_dir/AGENTS.md" "scripts/rocs.sh" "generated $tpl AGENTS should reference scripts/rocs.sh"
  assert_contains "$l2_dir/AGENTS.md" "diary/" "generated $tpl AGENTS should reference repo-local diary"
  assert_contains "$l2_dir/README.md" "ROCS command flow" "generated $tpl README should include ROCS command flow section"
  if [ "$tpl" = "tpl-agent-repo" ] || [ "$tpl" = "tpl-project-repo" ]; then
    assert_contains "$l2_dir/AGENTS.md" "does not appoint organizational roles or grant company delegation" "generated $tpl must not infer appointment"
    assert_contains "$l2_dir/AGENTS.md" "missing, expired, or ambiguous, stop and escalate" "generated $tpl must fail closed on delegation ambiguity"
    assert_contains "$l2_dir/AGENTS.md" "scoped owner-native task and finite-WIP" "generated $tpl must require finite-WIP admission"
    assert_contains "$l2_dir/AGENTS.md" "Passing validation is not an outcome" "generated $tpl must separate validation from outcome"
    assert_contains "$l2_dir/AGENTS.md" "External effects and terminal" "generated $tpl must reserve effects"
    assert_contains "$l2_dir/AGENTS.md" "never a shadow backlog" "generated $tpl must keep packets non-authoritative"
  fi
  if [ "$tpl" = "tpl-project-repo" ]; then
    assert_not_file "$l2_dir/.gitlab-ci.yml"
    assert_not_dir "$l2_dir/gitlab"
  fi

  # Initialize git for smoke + idempotency test (smoke requires git repo)
  (
    cd "$l2_dir"
    git init -b main >/dev/null
    git config user.name "l1-template ci" >/dev/null
    git config user.email "ci@l1-template.local" >/dev/null
    git add . >/dev/null
    git commit -m "initial L2 render" >/dev/null
    ./scripts/ci/smoke.sh >/dev/null
  )

  ./scripts/new-repo-from-copier.sh "$tpl" "$l2_dir" \
    -d repo_slug="$tpl" \
    --defaults --overwrite >/dev/null

  (
    cd "$l2_dir"
    if [ -n "$(git status --porcelain)" ]; then
      echo "error: non-idempotent L1 -> L2 generation ($tpl)" >&2
      git status --short >&2
      exit 1
    fi
  )
done

# Test tpl-package separately (different parameters, no git required)
adversarial_agent_dir="$tmp_root/tpl-agent-repo-adversarial-json"
./scripts/new-repo-from-copier.sh tpl-agent-repo "$adversarial_agent_dir" \
  -d 'repo_slug=agent-"quoted\\slug' \
  -d 'agent_owner_handle=@owner"\\name' \
  --defaults --overwrite >/dev/null
python3 -m json.tool "$adversarial_agent_dir/governance/work-items.json" >/dev/null || \
  fail "generated agent work-items JSON must escape unrestricted Copier string inputs"

# Test tpl-package separately (different parameters, no git required)
tpl="tpl-package"
l2_dir="$tmp_root/$tpl"
./scripts/new-repo-from-copier.sh "$tpl" "$l2_dir" \
  -d package_name="$tpl" \
  -d package_type=library \
  -d language=python \
  --defaults --overwrite >/dev/null

assert_file "$l2_dir/.copier-answers.yml"
assert_file "$l2_dir/contracts/layer-contract.yml"
assert_file "$l2_dir/AGENTS.md"
assert_file "$l2_dir/CODEOWNERS"
assert_file "$l2_dir/scripts/rocs.sh"
assert_file "$l2_dir/scripts/ci/smoke.sh"
assert_file "$l2_dir/scripts/ci/full.sh"
assert_file "$l2_dir/diary/README.md"
assert_contains "$l2_dir/diary/README.md" "YYYY-MM-DD--type-scope-summary.md" "generated $tpl diary README should enforce descriptive filename convention"
assert_not_dir "$l2_dir/docs/diary"
assert_exec "$l2_dir/scripts/rocs.sh"
assert_contains "$l2_dir/AGENTS.md" "Deterministic tooling policy" "generated $tpl AGENTS should include deterministic tooling policy"
assert_contains "$l2_dir/AGENTS.md" "scripts/rocs.sh" "generated $tpl AGENTS should reference scripts/rocs.sh"
assert_contains "$l2_dir/AGENTS.md" "diary/" "generated $tpl AGENTS should reference repo-local diary"
assert_contains "$l2_dir/README.md" "ROCS command flow" "generated $tpl README should include ROCS command flow section"
assert_not_contains "$l2_dir/CODEOWNERS" "@package-owners" "generated tpl-package CODEOWNERS should not use hardcoded package owner placeholder"
assert_contains "$l2_dir/CODEOWNERS" "@project-owners" "generated tpl-package CODEOWNERS should use the package owner handle surface"

# tpl-package idempotency check (no git required)
./scripts/new-repo-from-copier.sh "$tpl" "$l2_dir" \
  -d package_name="$tpl" \
  -d package_type=library \
  -d language=python \
  --defaults --overwrite >/dev/null

# Elixir stack-contract smoke for project + package templates.
elixir_project_dir="$tmp_root/tpl-project-repo-elixir"
./scripts/new-repo-from-copier.sh tpl-project-repo "$elixir_project_dir" \
  -d repo_slug=fixture-project-elixir \
  -d language=elixir \
  -d enable_software_pack=true \
  --defaults --overwrite >/dev/null
assert_file "$elixir_project_dir/mix.exs"
assert_file "$elixir_project_dir/policy/engineering-lane.json"
assert_file "$elixir_project_dir/docs/engineering.local.md"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"lane": "elixir"' "generated elixir project should declare the elixir stack lane"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"ref": "workspace-local-unpinned"' "generated elixir project should record honest workspace-local provenance"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"catalog_command"' "generated elixir project should declare catalog command for adoption scans"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"list_disciplines_command"' "generated elixir project should declare discipline-list command for adoption scans"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"list_templates_command"' "generated elixir project should declare template-list command for adoption scans"
assert_contains "$elixir_project_dir/policy/engineering-lane.json" '"disciplines"' "generated elixir project should declare scanner-visible selected disciplines"
assert_contains "$elixir_project_dir/docs/engineering.local.md" "engineering_core.command" "generated elixir project should point operators to the declared lane command"
assert_not_contains "$elixir_project_dir/docs/engineering.local.md" "pins the upstream lane" "generated elixir project docs should not overstate lane pinning"
assert_not_contains "$elixir_project_dir/docs/engineering.local.md" "--prefer-repo" "generated elixir project docs should not hardcode repo-preferred lane resolution"

elixir_package_dir="$tmp_root/tpl-package-elixir"
./scripts/new-repo-from-copier.sh tpl-package "$elixir_package_dir" \
  -d package_name=fixture-elixir-core \
  -d package_type=library \
  -d language=elixir \
  --defaults --overwrite >/dev/null
assert_file "$elixir_package_dir/policy/engineering-lane.json"
assert_file "$elixir_package_dir/docs/engineering.local.md"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"lane": "elixir"' "generated elixir package should declare the elixir stack lane"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"ref": "workspace-local-unpinned"' "generated elixir package should record honest workspace-local provenance"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"catalog_command"' "generated elixir package should declare catalog command for adoption scans"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"list_disciplines_command"' "generated elixir package should declare discipline-list command for adoption scans"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"list_templates_command"' "generated elixir package should declare template-list command for adoption scans"
assert_contains "$elixir_package_dir/policy/engineering-lane.json" '"disciplines"' "generated elixir package should declare scanner-visible selected disciplines"
assert_contains "$elixir_package_dir/docs/engineering.local.md" "engineering_core.command" "generated elixir package should point operators to the declared lane command"
assert_not_contains "$elixir_package_dir/docs/engineering.local.md" "pins the upstream lane" "generated elixir package docs should not overstate lane pinning"
assert_not_contains "$elixir_package_dir/docs/engineering.local.md" "--prefer-repo" "generated elixir package docs should not hardcode repo-preferred lane resolution"

compact_project_dir="$tmp_root/tpl-project-repo-compact"
./scripts/new-repo-from-copier.sh tpl-project-repo "$compact_project_dir" \
  -d repo_slug=fixture-project-compact \
  -d org_docs_profile=compact \
  --defaults --overwrite >/dev/null
assert_file "$compact_project_dir/docs/org_context/org-summary.md"
assert_not_file "$compact_project_dir/docs/org_context/mission.md"
assert_not_file "$compact_project_dir/docs/org_context/purpose.md"
assert_not_file "$compact_project_dir/docs/org_context/vision.md"
assert_not_file "$compact_project_dir/docs/org_context/strategic_objectives.md"
assert_not_file "$compact_project_dir/docs/org_context/governance.md"

rich_project_dir="$tmp_root/tpl-project-repo-rich"
./scripts/new-repo-from-copier.sh tpl-project-repo "$rich_project_dir" \
  -d repo_slug=fixture-project-rich \
  -d org_docs_profile=rich \
  --defaults --overwrite >/dev/null
assert_file "$rich_project_dir/docs/org_context/org-summary.md"
assert_file "$rich_project_dir/docs/org_context/mission.md"
assert_file "$rich_project_dir/docs/org_context/purpose.md"
assert_file "$rich_project_dir/docs/org_context/vision.md"
assert_file "$rich_project_dir/docs/org_context/strategic_objectives.md"
assert_file "$rich_project_dir/docs/org_context/governance.md"

node_project_dir="$tmp_root/tpl-project-repo-node"
./scripts/new-repo-from-copier.sh tpl-project-repo "$node_project_dir" \
  -d repo_slug=fixture-project-node \
  -d language=node \
  -d enable_software_pack=true \
  --defaults --overwrite >/dev/null
assert_file "$node_project_dir/package.json"
assert_not_file "$node_project_dir/tsconfig.json"
assert_file "$node_project_dir/policy/engineering-lane.json"
assert_file "$node_project_dir/docs/engineering.local.md"

typescript_project_dir="$tmp_root/tpl-project-repo-typescript"
./scripts/new-repo-from-copier.sh tpl-project-repo "$typescript_project_dir" \
  -d repo_slug=fixture-project-typescript \
  -d language=typescript \
  -d enable_software_pack=true \
  --defaults --overwrite >/dev/null
assert_file "$typescript_project_dir/package.json"
assert_file "$typescript_project_dir/tsconfig.json"
assert_file "$typescript_project_dir/policy/engineering-lane.json"
assert_file "$typescript_project_dir/docs/engineering.local.md"

# Detailed check for tpl-project-repo (primary template)
l2_dir="$tmp_root/tpl-project-repo"
assert_contains "$l2_dir/AGENTS.md" "Recursion policy" "generated L2 AGENTS.md must include recursion section"
assert_contains "$l2_dir/AGENTS.md" "Deterministic tooling policy" "generated L2 AGENTS.md must include deterministic tooling policy"
assert_contains "$l2_dir/AGENTS.md" "scripts/rocs.sh" "generated L2 AGENTS.md must reference scripts/rocs.sh"
assert_contains "$l2_dir/AGENTS.md" "diary/" "generated L2 AGENTS.md must reference repo-local diary"

echo "ok: template ci"
