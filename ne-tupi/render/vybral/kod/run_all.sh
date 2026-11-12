#!/bin/bash
cd "$(dirname "$0")"
while [ "$(ls kadry/zhena | wc -l)" -lt 1008 ]; do sleep 5; done
python3 compose_v.py && ffmpeg -y -loglevel error -i video_noaudio.mp4 -i ../mix.m4a -c:v copy -c:a copy -shortest ../vybral-v1.mp4 && echo DONE
