#!/usr/bin/env bash
# Stop the code-server that start.sh started. See README.md.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$(cd "$HERE/../.." && pwd)"
WORK="${SHOTS_OUT:-$TOOL/out}/fixtures/code-server"
if [[ -f "$WORK/code-server.pid" ]] && kill "$(cat "$WORK/code-server.pid")" 2> /dev/null; then
  echo "stopped code-server"
else
  echo "code-server was not running"
fi
rm -f "$WORK/code-server.pid"
