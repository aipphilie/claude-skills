"""Озвучка «Что знает о тебе телефон»: рассказчик (2 куска) + кот отдельным голосом. Склейка в ../zvuk/voice.mp3 и общий align2.json."""
import json, os, base64, requests, subprocess, sys
key = os.environ['ELEVENLABS_API_KEY']
NARR = 'hU3rD0Yk7DoiYULTX1pD'      # Dmitry, голос канала
CAT = 'pM78bgjPVk0JXtaEnFoj'       # Nester Surovy: низкий хрипловатый, ленивый кот
SPEED = float(os.environ.get('SPEED', 1.12))
PARTS = [('text1.txt', NARR, SPEED), ('text_cat.txt', CAT, 1.0), ('text2.txt', NARR, SPEED)]
GAP = [0.35, 0.35]
TEMPO = float(os.environ.get('TEMPO', 1.1))   # ускорение рассказчика без смены тона (v4 игнорирует speed)                 # тишина до и после кота
only = sys.argv[1:]
for i, (fn, v, sp) in enumerate(PARTS):
    if only and str(i) not in only: continue
    r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{v}/with-timestamps?output_format=mp3_44100_128',
        headers={'xi-api-key': key}, json={'text': open(fn).read().strip(), 'model_id': 'eleven_v4', 'voice_settings': {'speed': sp}}, timeout=600)
    print(fn, r.status_code); j = r.json()
    open(f'../zvuk/p{i}.mp3', 'wb').write(base64.b64decode(j['audio_base64'])); json.dump(j['alignment'], open(f'align_p{i}.json', 'w'), ensure_ascii=False)
# склейка: wav-куски с паузами, общий тайминг
C, S, E = [], [], []; off = 0.0; wavs = []
for i in range(3):
    a = json.load(open(f'align_p{i}.json')); f = f'../zvuk/p{i}.wav'
    tp = TEMPO if PARTS[i][1] == NARR else 1.0
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'../zvuk/p{i}.mp3', '-af', f'atempo={tp}', '-ar', '44100', '-ac', '1', f], check=True)
    for kk in ('character_start_times_seconds', 'character_end_times_seconds'): a[kk] = [x / tp for x in a[kk]]
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
    end = a['character_end_times_seconds'][-1]; d = min(d, end + 0.25)
    if C: C.append(' '); S.append(off); E.append(off)
    C += a['characters']; S += [x + off for x in a['character_start_times_seconds']]; E += [x + off for x in a['character_end_times_seconds']]
    wavs.append((f, d)); off += d + (GAP[i] if i < 2 else 0)
fl = []; inp = []
for i, (f, d) in enumerate(wavs):
    inp += ['-i', f]; pad = GAP[i] if i < 2 else 0
    fl.append(f'[{i}:a]atrim=0:{d},apad=pad_dur={pad}[a{i}]')
fl.append(''.join(f'[a{i}]' for i in range(3)) + 'concat=n=3:v=0:a=1[o]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[o]', '-b:a', '192k', '../zvuk/voice.mp3'], check=True)
json.dump({'characters': C, 'character_start_times_seconds': S, 'character_end_times_seconds': E}, open('align2.json', 'w'), ensure_ascii=False)
json.dump({'cat': [wavs[0][1] + GAP[0], wavs[0][1] + GAP[0] + wavs[1][1]]}, open('cat_span.json', 'w'))
print('total', off)
