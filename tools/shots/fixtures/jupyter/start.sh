#!/usr/bin/env bash
# Start the JupyterLab that the book's Jupyter screenshots show. See README.md.
#
#   bash tools/shots/fixtures/jupyter/start.sh     # then capture; stop.sh when done
#
# It installs the pinned JupyterLab into .venv here, copies project/ to a scratch
# folder under tools/shots/out/ (so a run never changes the committed files),
# runs and trusts the notebooks there, and serves them on 127.0.0.1 with no token.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$(cd "$HERE/../.." && pwd)"                     # tools/shots
WORK="${SHOTS_OUT:-$TOOL/out}/fixtures/jupyter"
PORT="${SHOTS_JUPYTER_PORT:-8899}"
VENV="$HERE/.venv"

if [[ -f "$WORK/jupyter.pid" ]]; then bash "$HERE/stop.sh"; fi

# 1. The pinned JupyterLab, and its settings: light theme, no news or update prompts.
[[ -x "$VENV/bin/python" ]] || python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install -q --disable-pip-version-check -r "$HERE/requirements.txt"
mkdir -p "$VENV/share/jupyter/lab/settings"
cp "$HERE/overrides.json" "$VENV/share/jupyter/lab/settings/overrides.json"

# 2. A fresh copy of the project, with Jupyter's own state kept beside it.
rm -rf "$WORK/Project" "$WORK/state"
mkdir -p "$WORK/state"
cp -R "$HERE/project" "$WORK/Project"
export JUPYTER_CONFIG_DIR="$WORK/state/config" JUPYTER_DATA_DIR="$WORK/state/data"
export JUPYTER_RUNTIME_DIR="$WORK/state/runtime"

# 3. Run each notebook, so its outputs are what this pandas produces, and trust it.
for nb in "$WORK/Project/notebooks/"*.ipynb; do
  (cd "$(dirname "$nb")" && "$VENV/bin/jupyter" nbconvert --to notebook --execute --inplace "$(basename "$nb")" \
     > "$WORK/state/nbconvert.log" 2>&1)
  "$VENV/bin/jupyter" trust "$nb" > /dev/null 2>&1
done

# 4. Serve it: this machine only, no token, a workspace and settings of its own.
root_flag=()
[[ $(id -u) == 0 ]] && root_flag=(--allow-root)
nohup "$VENV/bin/jupyter" lab --no-browser "${root_flag[@]}" \
  --ServerApp.ip=127.0.0.1 --ServerApp.port="$PORT" --ServerApp.port_retries=0 \
  --IdentityProvider.token='' --ServerApp.password='' \
  --ServerApp.root_dir="$WORK/Project" \
  --LabApp.workspaces_dir="$WORK/state/workspaces" \
  --LabApp.user_settings_dir="$WORK/state/settings" \
  > "$WORK/jupyter.log" 2>&1 &
echo $! > "$WORK/jupyter.pid"

for _ in $(seq 60); do
  if curl -fsS --noproxy '*' "http://127.0.0.1:$PORT/lab" > /dev/null 2>&1; then
    echo "JupyterLab is up: http://localhost:$PORT/lab (serving $WORK/Project)"
    exit 0
  fi
  sleep 1
done
echo "JupyterLab did not start; see $WORK/jupyter.log" >&2
exit 1
