N=$(python3 -c "import sys;sys.path.insert(0,'kod');import tl;print(tl.N)")
P=4; C=$(( (N + P - 1) / P ))
for k in $(seq 0 $((P-1))); do python3 kod/compose.py $((k*C)) $(((k+1)*C)) part$k.mp4 > v_$k.log 2>&1 & done
wait
printf "file 'part0.mp4'\nfile 'part1.mp4'\nfile 'part2.mp4'\nfile 'part3.mp4'\n" > parts.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i parts.txt -i mix.m4a -c:v copy -c:a copy -map 0:v -map 1:a -shortest final.mp4
ls -la final.mp4
