#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

build_spec=main-macos-arm64.spec
build_output=SecretCouncil-arm64
case "${1:-}" in
    '') ;;
    --app)
        build_spec=main-macos-arm64-app.spec
        build_output=SecretCouncil.app
        ;;
    *) echo "Usage: $0 [--app]" >&2; exit 1 ;;
esac
if [ "$#" -gt 1 ]; then
    echo "Usage: $0 [--app]" >&2
    exit 1
fi

# Keep the macOS environment separate from the Windows .venv.
python_bin="${PYTHON:-python3}"
validate_python() {
    "$1" - <<'PY'
import platform
import sys

if sys.platform != 'darwin' or platform.machine() != 'arm64':
    raise SystemExit('Build requires native arm64 Python on Apple Silicon macOS (not Rosetta).')
if sys.version_info < (3, 10):
    raise SystemExit('Build requires Python 3.10 or newer.')
PY
}

validate_python "$python_bin"
if [ ! -d .venv-macos-arm64 ]; then
    "$python_bin" -m venv .venv-macos-arm64
fi
venv_python="$PWD/.venv-macos-arm64/bin/python"
validate_python "$venv_python"
"$venv_python" -m pip install -r requirements-build.txt
bash ./create-macos-icon.sh
"$venv_python" -m PyInstaller --noconfirm --clean "$build_spec"
if [ "$build_output" = SecretCouncil-arm64 ]; then
    osascript -l JavaScript ./set-macos-file-icon.js \
        "$PWD/assets/icons/SecretCouncil.icns" "$PWD/dist/$build_output"
fi
echo "Built: $PWD/dist/$build_output"
