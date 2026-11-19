#!/usr/bin/env bash
# contrib-integrate.sh - keep a contrib checkout on OUR integration branch: upstream plus the
# patch branches we carry (proposed upstream, or local-only), rebuilt from scratch on every run.
#
#   contrib-integrate.sh [--dry-run] <repo>     rebuild and move the integration branch when safe
#   contrib-integrate.sh --check <repo>         offline: on the branch? how far behind the last fetch?
#   contrib-integrate.sh --superseded SHA ... <repo>
#                                               this run only: these commits on the old tip are knowingly
#                                               replaced (a patch branch was rebased and changed), not lost
#
# Repo-local git config (nothing else is read):
#   contrib.integration.patch    one per patch branch, merged in order (required; multi-valued)
#   contrib.integration.branch   the integration branch (default main)
#   contrib.integration.base     what it is built on (default origin's default branch)
#   contrib.integration.check    a command run in the rebuilt tree before the branch moves (optional)
# Scratch: CONTRIB_INTEGRATE_SCRATCH, else TMPDIR; a /tmp one yields to /data/ai-society-scratch.
#
# Safety, in order: the rebuild happens in a throwaway worktree; a merge conflict that rerere does
# not already know stops the run; the check must pass; the branch never moves when its current
# tip holds a commit no patch branch carries (it would be lost) or when the checkout is dirty.
# The previous tip is kept as refs/contrib/integration/previous (git reset --keep it to roll back).
# A patch branch upstream has merged contributes nothing and can be dropped from the config.
# Exit: 0 moved or current, 3 not configured, 4 conflict, 5 check failed, 6 would lose commits,
# 7 dirty checkout, 2 usage or git failure.
set -Eeuo pipefail
mode=run
superseded=()
while [[ $# -gt 1 ]]; do
  case "$1" in
    --check) mode=check; shift ;;
    --dry-run) mode=dry; shift ;;
    --superseded) superseded+=("$2"); shift 2 ;;
    *) break ;;
  esac
done
repo=${1:?usage: contrib-integrate.sh [--check|--dry-run] <repo>}
g() { git -C "$repo" "$@"; }
g rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repo: $repo" >&2; exit 2; }
mapfile -t patches < <(g config --local --get-all contrib.integration.patch || true)
[[ ${#patches[@]} -gt 0 ]] || { echo "$repo: no contrib.integration.patch configured"; exit 3; }
branch=$(g config --local --get contrib.integration.branch || echo main)
base=$(g config --local --get contrib.integration.base || true)
if [[ -z "$base" ]]; then
  head_ref=$(g symbolic-ref -q refs/remotes/origin/HEAD || true)
  base=${head_ref#refs/remotes/}
  [[ -n "$base" ]] || base=origin/main
fi
current=$(g branch --show-current || true)

if [[ $mode == check ]]; then
  behind=$(g rev-list --count "$branch..$base" 2>/dev/null || echo '?')
  echo "$repo: checkout ${current:-detached at $(g rev-parse --short HEAD)}; $branch behind $base: $behind"
  [[ "$current" == "$branch" ]] || { echo "not on $branch" >&2; exit 1; }
  exit 0
fi

g fetch --all --prune --no-tags --quiet
g config rerere.enabled true
g config rerere.autoupdate true
# The rebuild is a worktree and its check may build: never under /tmp (workspace rule). The hourly
# timer runs with TMPDIR=/tmp, so a /tmp TMPDIR yields to the /data scratch root when it exists.
scratch_parent=${CONTRIB_INTEGRATE_SCRATCH:-${TMPDIR:-/tmp}}
case $scratch_parent in
  /tmp | /tmp/*) [[ -d /data/ai-society-scratch && -w /data/ai-society-scratch ]] &&
    scratch_parent=/data/ai-society-scratch/contrib-integrate ;;
esac
mkdir -p "$scratch_parent"
scratch=$(mktemp -d "$scratch_parent/contrib-integrate.XXXXXX")
tree="$scratch/tree"
cleanup() { g worktree remove --force "$tree" >/dev/null 2>&1 || true; rm -rf "$scratch"; }
trap cleanup EXIT
g worktree add -q --detach "$tree" "$base"
for p in "${patches[@]}"; do
  if ! git -C "$tree" merge -q --no-edit "$p" >/dev/null 2>&1; then
    if [[ -z "$(git -C "$tree" diff --name-only --diff-filter=U)" ]]; then
      git -C "$tree" commit -q --no-edit   # rerere replayed a known resolution
    else
      echo "$repo: merging $p onto $base conflicts in: $(git -C "$tree" diff --name-only --diff-filter=U | tr '\n' ' ')"
      echo "  resolve once by hand (git merge in a worktree; rerere records it), then run again; $branch is unchanged"
      git -C "$tree" merge --abort >/dev/null 2>&1 || true
      exit 4
    fi
  fi
done
check=$(g config --local --get contrib.integration.check || true)
if [[ -n "$check" ]] && ! (cd "$tree" && bash -c "$check") >"$scratch/check.log" 2>&1; then
  # keep the whole log where the lane keeps its sync logs; the first error is rarely in the last lines
  logdir="$(cd "$(dirname "$0")/.." && pwd)/.logs/integrate"
  mkdir -p "$logdir"
  keep="$logdir/$(basename "$repo")-$(date +%Y%m%d-%H%M%S).log"
  cp "$scratch/check.log" "$keep"
  echo "$repo: check failed on the rebuilt tree ($check); $branch is unchanged; full log: $keep"
  grep -n -m 5 -E 'caught (ERROR|FATAL)|^error|Error:|unhandled|fatal' "$scratch/check.log" | cut -c1-240 || true
  tail -5 "$scratch/check.log"
  exit 5
fi
new=$(git -C "$tree" rev-parse HEAD)
old=$(g rev-parse -q --verify "refs/heads/$branch" || true)
if [[ -n "$old" ]]; then
  if [[ "$(g rev-parse "$old^{tree}")" == "$(g rev-parse "$new^{tree}")" ]]; then
    echo "$repo: $branch current ($(g rev-parse --short "$old"))"; exit 0
  fi
  lost=$(g log --no-merges --cherry-pick --right-only --format='  %h %s' "$new...$old" || true)
  for sha in "${superseded[@]}"; do   # named by the caller as replaced: not lost
    full=$(g rev-parse -q --verify "$sha^{commit}" || true)
    [[ -n "$full" ]] || { echo "$repo: --superseded $sha is no commit"; exit 2; }
    lost=$(printf '%s\n' "$lost" | grep -v "^  $(g rev-parse --short "$full") " || true)
    echo "$repo: superseded on purpose: $(g log -1 --format='%h %s' "$full")"
  done
  if [[ -n "$lost" ]]; then
    echo "$repo: $branch holds commits no patch branch carries; put them on a patch branch first:"
    echo "$lost"
    exit 6
  fi
fi
if [[ $mode == dry ]]; then echo "$repo: would move $branch ${old:0:9} -> ${new:0:9}"; exit 0; fi
if [[ "$current" == "$branch" ]]; then
  [[ -z "$(g status --porcelain --untracked-files=no)" ]] || { echo "$repo: checkout is dirty; $branch is unchanged"; exit 7; }
  [[ -n "$old" ]] && g update-ref refs/contrib/integration/previous "$old"
  g reset -q --keep "$new"
else
  [[ -n "$old" ]] && g update-ref refs/contrib/integration/previous "$old"
  g branch -q -f "$branch" "$new"
  echo "$repo: note: the checkout is on ${current:-a detached HEAD}, not $branch"
fi
echo "$repo: $branch ${old:0:9} -> ${new:0:9} = $base + ${patches[*]}"
