#!/bin/bash
# рендер 4 кусками параллельно + склейка + звук
cd "$(dirname "$0")"
cat scenes_tf.py engine_tf.py > compose_tf.py
N=$(python3 -c "import base_k;print(base_k.N)")
for i in 0 1 2 3; do F0=$((N*i/4)) F1=$((N*(i+1)/4)) OUT=part$i.mp4 python3 compose_tf.py > run$i.log 2>&1 & done; wait
printf "file part0.mp4\nfile part1.mp4\nfile part2.mp4\nfile part3.mp4\n" > parts.txt
ffmpeg -y -loglevel error -f concat -i parts.txt -c copy video_noaudio.mp4
python3 mix_tf.py
ffmpeg -y -loglevel error -i video_noaudio.mp4 -i ../mix-v1.m4a -c:v copy -c:a copy -shortest -movflags +faststart ../telefon-v1.mp4
echo DONE
