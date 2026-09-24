#!/usr/bin/env bash
# Stop the JupyterLab that start.sh started. See README.md.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$(cd "$HERE/../.." && pwd)"
WORK="${SHOTS_OUT:-$TOOL/out}/fixtures/jupyter"
if [[ -f "$WORK/jupyter.pid" ]] && kill "$(cat "$WORK/jupyter.pid")" 2> /dev/null; then
  echo "stopped JupyterLab"
else
  echo "JupyterLab was not running"
fi
rm -f "$WORK/jupyter.pid"
