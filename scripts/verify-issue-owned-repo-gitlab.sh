#!/usr/bin/env bash
set -euo pipefail

need() { command -v "$1" >/dev/null 2>&1 || { echo "error: missing dependency: $1" >&2; exit 2; }; }
need git
need python3
need gl-nas
need gl-nas-git
need tar

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

template="${1:-tpl-owned-repo}"

namespace_path="${NAMESPACE_PATH:-ai-society/softwareco/owned}"
namespace_id="${NAMESPACE_ID:-}"
if [ -z "$namespace_id" ]; then
  namespace_id="$(gl-nas -- -o json group get --id "$namespace_path" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
fi

slug="${SLUG:-tmp-verify-owned-repo-$(date +%Y%m%d-%H%M%S)}"

echo "==> create temp project: $slug (namespace_path=$namespace_path namespace_id=$namespace_id)"
proj_json="$(gl-nas -- -o json project create \
  --namespace-id "$namespace_id" \
  --name "$slug" \
  --path "$slug" \
  --initialize-with-readme false \
  --default-branch main)"

proj_id="$(printf '%s' "$proj_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
repo_http="$(printf '%s' "$proj_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["http_url_to_repo"])')"
web_url="$(printf '%s' "$proj_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["web_url"])')"
echo "project_id=$proj_id"
echo "repo=$repo_http"
echo "web=$web_url"

echo "==> create default branch (API commit; needed when developer_can_initial_push=false)"
if ! gl-nas -- project-commit create \
  --project-id "$proj_id" \
  --branch main \
  --commit-message "init: create default branch" \
  --actions '[{"action":"create","file_path":"README.md","content":"temp repo for verifying tpl-owned-repo GitLab CI\\n"}]' \
  >/dev/null 2>&1; then
  echo "error: could not create default branch via API commit (likely insufficient role in $namespace_path)." >&2
  echo "hint: run with a token that has Owner/Maintainer in $namespace_path (or run from a protected CI job with CI_JOB_TOKEN if allowed)." >&2
  echo "temp_project_web=$web_url" >&2
  exit 1
fi

workdir="$(mktemp -d)"
repo_dir="$workdir/$slug"
render_dir="$workdir/rendered-$slug"

echo "==> clone empty project -> $repo_dir"
gl-nas-git -- git clone "$repo_http" "$repo_dir" >/dev/null 2>&1

echo "==> render: $template -> $render_dir"
./scripts/new-repo-from-copier.sh "$template" "$render_dir" -d repo_slug="$slug" --defaults --overwrite >/dev/null 2>&1

echo "==> sync rendered files into repo"
cd "$repo_dir"
(cd "$render_dir" && tar -cf - .) | (cd "$repo_dir" && tar -xf -)
git add -A
git commit -m "init from $template" >/dev/null || true

echo "==> push main"
can_push_main=1
if ! gl-nas-git -- git push -u origin main >/dev/null 2>&1; then
  can_push_main=0
  echo "warn: could not push to main (likely protected branch or insufficient role)." >&2
  echo "warn: will still open an MR and print MR job runner tags; protected-pipeline verification may be skipped." >&2
fi

echo "==> protect main (so protected pipeline runs)"
gl-nas -- project-protected-branch create --project-id "$proj_id" --name main \
  --push-access-level 40 --merge-access-level 40 >/dev/null 2>&1 || true

echo "==> create MR branch"
git checkout -b feature/ci-smoke >/dev/null
echo "# mr change" >> _mr_change.md
git add -A
git commit -m "mr change" >/dev/null
gl-nas-git -- git push -u origin feature/ci-smoke >/dev/null

echo "==> open MR"
mr_json="$(gl-nas -- -o json project-merge-request create \
  --project-id "$proj_id" \
  --source-branch feature/ci-smoke \
  --target-branch main \
  --title "verify tpl-owned-repo GitLab CI tags")"
mr_iid="$(printf '%s' "$mr_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["iid"])')"
mr_url="$(printf '%s' "$mr_json" | python3 -c 'import sys,json; print(json.load(sys.stdin)["web_url"])')"
echo "mr_iid=$mr_iid"
echo "mr=$mr_url"

wait_for_pipeline() {
  local project_id="$1"
  local ref="$2"
  local tries="${3:-60}"
  local sleep_s="${4:-2}"

  for _ in $(seq 1 "$tries"); do
    local pipeline_id
    pipeline_id="$(gl-nas -- -o json project-pipeline list --project-id "$project_id" --ref "$ref" --get-all \
      | python3 -c 'import sys,json; a=json.load(sys.stdin); print(max([p["id"] for p in a]) if a else "")')"
    if [ -n "$pipeline_id" ]; then
      echo "$pipeline_id"
      return 0
    fi
    sleep "$sleep_s"
  done
  return 1
}

main_pipeline_id=""
if [ "$can_push_main" -eq 1 ]; then
  echo "==> create protected pipeline on main (expect ci:full tagged runner::protected)"
  main_pipeline_id="$(gl-nas -- -o json project-pipeline create --project-id "$proj_id" --ref main \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"
  echo "main_pipeline_id=$main_pipeline_id"
else
  echo "==> skip protected pipeline on main (main push not permitted)"
fi

echo "==> wait MR pipeline"
mr_ref="refs/merge-requests/$mr_iid/head"
mr_pipeline_id="$(wait_for_pipeline "$proj_id" "$mr_ref" 60 2 || true)"
if [ -z "$mr_pipeline_id" ]; then
  echo "error: could not find MR pipeline for $mr_ref" >&2
  exit 1
fi
echo "mr_pipeline_id=$mr_pipeline_id"

print_jobs_and_runners() {
  local project_id="$1"
  local pipeline_id="$2"
  gl-nas -- -o json project-pipeline-job list --project-id "$project_id" --pipeline-id "$pipeline_id" --get-all \
    | python3 -c 'import sys,json; jobs=json.load(sys.stdin); print("\n".join(f"{j[\"id\"]}\t{j[\"name\"]}\t{j[\"status\"]}" for j in jobs))'
  for jid in $(gl-nas -- -o json project-pipeline-job list --project-id "$project_id" --pipeline-id "$pipeline_id" --get-all \
    | python3 -c 'import sys,json; print(" ".join(str(j["id"]) for j in json.load(sys.stdin)))'); do
    gl-nas -- -o json project-job get --project-id "$project_id" --id "$jid" \
      | python3 -c 'import sys,json; j=json.load(sys.stdin); print(f"{j[\"name\"]}\ttags={j.get(\"tag_list\")}\trunner={j.get(\"runner\",{}).get(\"description\")}")'
  done
}

echo "==> MR pipeline jobs (expect ci:smoke tagged runner::mr; no ci:full)"
print_jobs_and_runners "$proj_id" "$mr_pipeline_id"

if [ -n "$main_pipeline_id" ]; then
  echo "==> main pipeline jobs (expect ci:full tagged runner::protected)"
  print_jobs_and_runners "$proj_id" "$main_pipeline_id"
else
  echo "==> note: protected pipeline verification skipped (need push/merge rights on main)"
fi

echo "==> done"
echo "temp_project_web=$web_url"
echo "note: cleanup requires maintainer; project delete not automated here"
