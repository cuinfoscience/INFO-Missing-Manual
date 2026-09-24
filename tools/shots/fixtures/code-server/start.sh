#!/usr/bin/env bash
# Start the code-server (VS Code in the browser) that the book's editor screenshots show.
# See README.md.
#
#   bash tools/shots/fixtures/code-server/start.sh     # then capture; stop.sh when done
#
# It downloads the pinned code-server release once, installs the pinned extensions from
# Open VSX, copies project/ to a scratch folder under tools/shots/out/ with its own .venv,
# and serves it on 127.0.0.1 with no password.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$(cd "$HERE/../.." && pwd)"                     # tools/shots
WORK="${SHOTS_OUT:-$TOOL/out}/fixtures/code-server"
PORT="${SHOTS_CODE_SERVER_PORT:-8898}"
# shellcheck source=versions.env
source "$HERE/versions.env"

if [[ -f "$WORK/code-server.pid" ]]; then bash "$HERE/stop.sh"; fi
mkdir -p "$WORK"

# 1. The pinned release, downloaded once.
CS="$WORK/code-server-$CODE_SERVER_VERSION-linux-amd64"
if [[ ! -x "$CS/bin/code-server" ]]; then
  url="https://github.com/coder/code-server/releases/download/v$CODE_SERVER_VERSION/code-server-$CODE_SERVER_VERSION-linux-amd64.tar.gz"
  curl -fsSL "$url" | tar -xz -C "$WORK"
fi

# 2. A fresh profile: settings (light theme, no welcome page, tips, telemetry, or AI panels)
#    and the pinned extensions. Its own config file, so nothing is written to ~/.config.
rm -rf "$WORK/data" "$WORK/Project" "$WORK/home"
mkdir -p "$WORK/data/User" "$WORK/extensions" "$WORK/home"
cp "$HERE/bashrc" "$WORK/home/.bashrc"
cp "$HERE/settings.json" "$WORK/data/User/settings.json"
printf 'bind-addr: 127.0.0.1:%s\nauth: none\ncert: false\n' "$PORT" > "$WORK/config.yaml"
# code-server's own `--install-extension id@version` misses Open VSX's per-platform builds
# (Ruff's), so fetch each pinned .vsix by its API record and install the file.
mkdir -p "$WORK/vsix"
: > "$WORK/extensions.log"
for ext in "$PYTHON_EXTENSION" "$RUFF_EXTENSION"; do
  id="${ext%@*}"; version="${ext#*@}"; publisher="${id%%.*}"; name="${id#*.}"
  vsix="$WORK/vsix/$id-$version.vsix"
  if [[ ! -s "$vsix" ]]; then
    record=$(curl -fs "https://open-vsx.org/api/$publisher/$name/linux-x64/$version" \
             || curl -fsS "https://open-vsx.org/api/$publisher/$name/$version")
    url=$(printf '%s' "$record" | python3 -c 'import json, sys; print(json.load(sys.stdin)["files"]["download"])')
    curl -fsSL "$url" -o "$vsix"
  fi
  "$CS/bin/code-server" --config "$WORK/config.yaml" --extensions-dir "$WORK/extensions" \
    --user-data-dir "$WORK/data" --install-extension "$vsix" >> "$WORK/extensions.log" 2>&1
done

# 3. A fresh copy of the project, with the .venv its terminal activates.
cp -R "$HERE/project" "$WORK/Project"
python3 -m venv "$WORK/Project/.venv"
"$WORK/Project/.venv/bin/python" -m pip install -q --disable-pip-version-check -r "$HERE/requirements.txt"

# 4. Serve it: this machine only, no password.
# Its own HOME, so the terminal reads the fixture's .bashrc, not the capture machine's.
HOME="$WORK/home" nohup "$CS/bin/code-server" --config "$WORK/config.yaml" \
  --user-data-dir "$WORK/data" --extensions-dir "$WORK/extensions" \
  --disable-telemetry --disable-update-check --disable-workspace-trust \
  --disable-getting-started-override "$WORK/Project" > "$WORK/code-server.log" 2>&1 &
echo $! > "$WORK/code-server.pid"

for _ in $(seq 60); do
  if curl -fsS --noproxy '*' "http://127.0.0.1:$PORT/healthz" > /dev/null 2>&1; then
    echo "code-server is up: http://localhost:$PORT/ (serving $WORK/Project)"
    exit 0
  fi
  sleep 1
done
echo "code-server did not start; see $WORK/code-server.log" >&2
exit 1
