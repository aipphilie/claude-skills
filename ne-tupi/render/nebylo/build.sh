#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export NETUPI_ROOT=$(cd "$here/../.." && pwd)
export NETUPI_WORK=${NETUPI_WORK:-/tmp/ne-tupi-nebylo-work}
export NETUPI_OUTPUT=${NETUPI_OUTPUT:-/tmp/ne-tupi-nebylo-out}
mkdir -p "$NETUPI_WORK" "$NETUPI_OUTPUT"
NETUPI_WORK=$(cd "$NETUPI_WORK" && pwd)
NETUPI_OUTPUT=$(cd "$NETUPI_OUTPUT" && pwd)
export PYTHONDONTWRITEBYTECODE=1

cp "$NETUPI_ROOT/render/avtokredit/kod/"{base_k.py,words.py} "$NETUPI_WORK/"
ln -sfn "$NETUPI_ROOT/render/avtokredit/kod/fonts" "$NETUPI_WORK/fonts"
cp "$NETUPI_ROOT/render/divan/kod/3d/index.html" "$NETUPI_WORK/model.html"
cp "$here/"{engine.py,film.py,mix.py,poses.cjs,poses.py,scenariy.json,tts.py} "$NETUPI_WORK/"
cd "$NETUPI_WORK"
if [[ ! -s three.module.js ]]; then
    curl -fsSL https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js -o three.module.js
fi
if [[ ! -s voice.mp3 || ! -s align2.json ]]; then
    python tts.py
fi
python poses.py
node poses.cjs
python film.py --sheet
python film.py --output silent.mp4
python mix.py "$NETUPI_ROOT/zvuki" "$NETUPI_OUTPUT/vy-dazhe-ne-vstrechalis.mp4" silent.mp4
cp "$here/opisanie.txt" "$NETUPI_OUTPUT/nebylo-opisanie.txt"
