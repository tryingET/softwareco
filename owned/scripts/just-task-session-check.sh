#!/usr/bin/env bash
# Bounded task5481 validation. Never delegates to scripts/ci or a live runtime.
set -euo pipefail
cd "$(dirname "$0")/.."

[ "$#" -eq 1 ] || { echo 'usage: just-task-session-check.sh lint|test|doctor|ci' >&2; exit 2; }
case "$1" in
  lint)
    bash -n scripts/launch-pi-ak-task-ghostty.sh scripts/just-task-session-check.sh
    python3 - <<'PY'
import ast
from pathlib import Path
for path in Path('tests').glob('*task_session*.py'):
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
PY
    git diff --check -- Justfile README.md scripts/launch-pi-ak-task-ghostty.sh \
      'scripts/just-*' 'tests/*task_session*' docs/project/ghostty-ak-task-launcher.md \
      'docs/project/2026-09-07-visible-task-session-*' 'diary/2026-09-07--decision151-*'
    ;;
  test)
    : "${TMPDIR:?TMPDIR must name owned scratch; no /tmp fallback}"
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p '*task_session*.py' -v
    ;;
  doctor)
    for tool in bash python3 git just; do
      command -v "$tool" >/dev/null || { echo "missing test tool: $tool" >&2; exit 2; }
    done
    : "${TMPDIR:?TMPDIR must name owned scratch; no /tmp fallback}"
    [ -d "$TMPDIR" ] && [ -w "$TMPDIR" ] || { echo 'TMPDIR is not writable' >&2; exit 2; }
    echo 'ok: local test tools and scratch; no installed/custody readiness assessed'
    ;;
  ci)
    echo 'blocked: full lane CI reaches network/AK/ROCS and is not authorized by task5481.' >&2
    echo 'Use just check for bounded syntax/whitespace and synthetic tests only.' >&2
    exit 2
    ;;
  *) echo "unknown check: $1" >&2; exit 2 ;;
esac
