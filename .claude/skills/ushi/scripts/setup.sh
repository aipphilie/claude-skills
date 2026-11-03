#!/usr/bin/env bash
# Ставит «уши» в облачную сессию. Повторный запуск ничего не качает заново.
#   bash .claude/skills/ushi/scripts/setup.sh          # всё
#   bash .claude/skills/ushi/scripts/setup.sh panns    # только PANNs
#   bash .claude/skills/ushi/scripts/setup.sh kit      # только библиотеку звуков
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="${USHI_KIT:-$HOME/.cache/ushi/kit}"
export SSL_CERT_FILE="${SSL_CERT_FILE:-/root/.ccr/ca-bundle.crt}" UV_SYSTEM_CERTS=1
what="${1:-all}"

command -v ffmpeg >/dev/null || { echo "нужен ffmpeg"; exit 1; }
command -v uv >/dev/null || pip install -q --break-system-packages uv

if [ "$what" = all ] || [ "$what" = panns ]; then
  python3 -c "import torch" 2>/dev/null || pip install -q --break-system-packages torch --index-url https://download.pytorch.org/whl/cpu
  python3 -c "import panns_inference, librosa" 2>/dev/null || pip install -q --break-system-packages panns_inference librosa matplotlib
  mkdir -p "$HOME/panns_data"
  for f in "Cnn14_mAP=0.431.pth" "Cnn14_DecisionLevelMax_mAP=0.385.pth"; do
    p="$HOME/panns_data/$f"
    if [ ! -s "$p" ] || [ "$(stat -c %s "$p")" -lt 300000000 ]; then
      echo "качаю $f (~320 МБ)"
      curl -sSL -o "$p.part" "https://zenodo.org/record/3987831/files/${f/=/%3D}?download=1" && mv "$p.part" "$p"
    fi
  done
  [ -s "$HOME/panns_data/class_labels_indices.csv" ] || curl -sSL -o "$HOME/panns_data/class_labels_indices.csv" \
    http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv
  echo "PANNs готов: python3 $HERE/hear.py FILE"
fi

if [ "$what" = all ] || [ "$what" = kit ]; then
  if [ -s "$KIT/catalog.json" ]; then echo "библиотека уже есть: $KIT"
  else (cd "$HERE/.." && uv run scripts/sfx.py kit --out "$KIT"); fi
fi
