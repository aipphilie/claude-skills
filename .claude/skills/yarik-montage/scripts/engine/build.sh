#!/usr/bin/env bash
# Собирает scenes.js из частей движка + сцен серии.
# ./build.sh ep-moya-seriya.part   (по умолчанию ep-primer.part — серия «Пьяный мозг Ярика»)
# Потом: node render.js preview prev/   |   TIMING=timing.json AUDIO=mix.wav node render.js video out.mp4
set -e; cd "$(dirname "$0")"
EP=${1:-ep-primer.part}
cat lib.part ep11helpers.part ep12helpers.part ep13helpers.part "$EP" tail.part > scenes.js
echo "scenes.js собран из $EP"
