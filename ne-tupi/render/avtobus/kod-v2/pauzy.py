"""v2: темп 1.1 + паузы в тишине перед главными фразами. Сдвигает тайминги align2.json."""
import json, subprocess
TEMPO = 1.10
PAUSES = [('Миллион', 0.75), ('Вот', 0.95), ('Это', 0.65)]   # тишина перед этим словом (первое вхождение с заглавной)
a = json.load(open('align_raw.json')); C = a['characters']
S = [x / TEMPO for x in a['character_start_times_seconds']]; E = [x / TEMPO for x in a['character_end_times_seconds']]
txt = ''.join(C); cuts = []
for w, d in PAUSES:
    i = txt.index(' ' + w + ' ') + 1 if ' ' + w + ' ' in txt else txt.index(w)
    j = i - 1
    while not C[j].isalnum(): j -= 1
    cuts.append(((E[j] + S[i]) / 2, d, i))
cuts.sort()
shift = 0; S2, E2 = S[:], E[:]
for at, d, i in cuts:
    for k in range(i, len(C)): S2[k] += d; E2[k] += d
a['character_start_times_seconds'] = S2; a['character_end_times_seconds'] = E2
json.dump(a, open('align2.json', 'w'), ensure_ascii=False)
json.dump([[round(at + sum(c[1] for c in cuts if c[0] < at), 3), d] for at, d, i in cuts], open('pauzy.json', 'w'))
# аудио: atempo, потом вставка тишины
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '../zvuk/voice_raw.mp3', '-af', f'atempo={TEMPO}', '-ar', '44100', '-ac', '1', 'tmp_fast.wav'], check=True)
fl = []; prev = 0; segs = []
for n, (at, d, i) in enumerate(cuts):
    fl.append(f'[0:a]atrim={prev}:{at},asetpts=PTS-STARTPTS[a{n}]'); fl.append(f'anullsrc=r=44100:cl=mono,atrim=0:{d}[z{n}]'); segs += [f'[a{n}]', f'[z{n}]']; prev = at
fl.append(f'[0:a]atrim={prev},asetpts=PTS-STARTPTS[al]'); segs.append('[al]')
fl.append(''.join(segs) + f'concat=n={len(segs)}:v=0:a=1[o]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'tmp_fast.wav', '-filter_complex', ';'.join(fl), '-map', '[o]', '-ar', '44100', '-b:a', '192k', '../zvuk/voice.mp3'], check=True)
print(cuts, E2[-1])
