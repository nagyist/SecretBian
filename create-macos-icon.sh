#!/bin/bash
# Regenerate the macOS icon from the original PNG using native macOS tools.
set -euo pipefail
cd "$(dirname "$0")"

icon_source="$PWD/assets/icons/SecretCouncil.png"
icon_output="$PWD/assets/icons/SecretCouncil.icns"
icon_tmp="$(mktemp -d)"
trap 'rm -rf "$icon_tmp"' EXIT
iconset="$icon_tmp/SecretCouncil.iconset"
mkdir -p "$iconset"

for size in 16 32 128 256 512; do
    sips -z "$size" "$size" "$icon_source" \
        --out "$iconset/icon_${size}x${size}.png" >/dev/null
    retina_size=$((size * 2))
    sips -z "$retina_size" "$retina_size" "$icon_source" \
        --out "$iconset/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$iconset" -o "$icon_output"
echo "Created: $icon_output"
