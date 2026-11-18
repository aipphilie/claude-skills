N=$(python3 -c "import json;print(len(json.load(open('track.json'))))")
P=3; C=$(( (N + P - 1) / P ))
for k in $(seq 0 $((P-1))); do node frames2.js track.json $((k*C)) $(((k+1)*C)) kadry > ch_$k.log 2>&1 & done
wait; ls kadry | wc -l
