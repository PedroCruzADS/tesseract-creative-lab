#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
PROJECT="$ROOT/outputs/leforzz-premium-motion/projeto/cloud"
OUT="$ROOT/.cloud-render"
if [ "${CREATIVE_FORMAT:-9x16}" != "9x16" ]; then
  echo "leforzz-premium-motion currently supports 9x16 only" >&2
  exit 2
fi
mkdir -p "$OUT"
cd "$PROJECT"
npm install --no-audit --no-fund
npx playwright install --with-deps chromium
npm run capture
rm -rf "$OUT/assets"
cp -R assets "$OUT/assets"
cp assets/capture.json "$OUT/asset-capture.json"
QUALITY="${CREATIVE_QUALITY:-preview}" npm run render
python "$ROOT/scripts/motion_quality.py" "$OUT/preview.mp4" --json-out "$OUT/motion-qa.json"
test -s "$OUT/preview.mp4"
