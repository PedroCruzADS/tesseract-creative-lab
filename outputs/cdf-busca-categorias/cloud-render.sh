#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
PROJECT="$ROOT/outputs/cdf-busca-categorias/projeto/cloud"
ASSETS="$PROJECT/assets"
OUT="$ROOT/.cloud-render"

if [ "${CREATIVE_FORMAT:-9x16}" != "9x16" ]; then
  echo "cdf-busca-categorias cloud master currently supports 9x16 only."
  exit 2
fi

mkdir -p "$ASSETS" "$OUT"
cd "$PROJECT"

download() {
  local url="$1"
  local dest="$2"
  if [ ! -s "$dest" ]; then
    curl -L --fail --retry 3 --retry-delay 2 "$url" -o "$dest"
  fi
}

download "https://casadofitness.vtexassets.com/arquivos/ids/156677/01.jpg.jpg?v=639235439616630000" "$ASSETS/treadmill.jpg"
download "https://casadofitness.vtexassets.com/arquivos/ids/163567/bicicleta-spinning-mormaii-motion-s-conexao-bluetooth_0.jpg.jpg?v=639219659714430000" "$ASSETS/bike.jpg"
download "https://casadofitness.vtexassets.com/arquivos/ids/155823/estacao-de-musculacao-speedo-multi-3-com-leg-press_0.jpg.jpg?v=639250034319330000" "$ASSETS/station.jpg"
download "https://casadofitness.vtexassets.com/arquivos/ids/158619/remomormaii1000.jpg.jpg?v=639131598806230000" "$ASSETS/rower.jpg"

npm install --no-audit --no-fund
npx playwright install --with-deps chromium

QUALITY="${CREATIVE_QUALITY:-preview}" npm run render

test -s "$OUT/preview.mp4"
