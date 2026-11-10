"""Озвучка: голосовое «мамы» (Зина, телефонный фильтр) + диктор. Итог: voice.mp3, align.json (со сдвигом), mama_words.json."""
import json, os, base64, requests, subprocess, sys
key = os.environ['ELEVENLABS_API_KEY']
def tts(voice, text, name):
    if os.path.exists(name + '.json') and '--force' not in sys.argv: return json.load(open(name + '.json'))
    r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128',
                      headers={'xi-api-key': key}, json={'text': text, 'model_id': 'eleven_v3'}, timeout=600)
    print(name, r.status_code); j = r.json()
    open(name + '.mp3', 'wb').write(base64.b64decode(j['audio_base64'])); json.dump(j['alignment'], open(name + '.json', 'w'), ensure_ascii=False)
    return j['alignment']
am = tts('BjDHBEonUBpXPayXKk4C', open('mama.txt').read().strip(), 'raw_mama')
an = tts('hU3rD0Yk7DoiYULTX1pD', open('text.txt').read().strip(), 'raw_dik')
M0 = 0.45                                  # когда начинает играть голосовое
mend = M0 + am['character_end_times_seconds'][-1]
OFF = round(mend + 0.55, 3)                # когда вступает диктор
# слова мамы для субтитров
C, S, E = am['characters'], am['character_start_times_seconds'], am['character_end_times_seconds']
ws, cur, intag = [], None, False
for i, ch in enumerate(C):
    if ch == '[': intag = True; cur = None; continue
    if ch == ']': intag = False; continue
    if intag: continue
    if ch in ' \n': cur = None; continue
    if cur is None:
        if not ch.isalnum(): continue
        cur = [ch, S[i] + M0, E[i] + M0]; ws.append(cur)
    else: cur[0] += ch; cur[2] = E[i] + M0
json.dump([[w, round(a, 3), round(b, 3)] for w, a, b in ws], open('mama_words.json', 'w'), ensure_ascii=False)
json.dump({'characters': an['characters'], 'character_start_times_seconds': [round(x + OFF, 3) for x in an['character_start_times_seconds']],
           'character_end_times_seconds': [round(x + OFF, 3) for x in an['character_end_times_seconds']]}, open('align.json', 'w'), ensure_ascii=False)
ms = lambda t: int(t * 1000)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'raw_mama.mp3', '-i', 'raw_dik.mp3', '-filter_complex',
    f'[0:a]highpass=f=350,lowpass=f=3300,acompressor=threshold=-18dB:ratio=4,volume=2.3,alimiter=limit=0.89,adelay={ms(M0)}|{ms(M0)}[m];'
    f'[1:a]adelay={ms(OFF)}|{ms(OFF)}[d];[m][d]amix=inputs=2:normalize=0[o]', '-map', '[o]', '-ar', '44100', '-b:a', '192k', 'voice.mp3'], check=True)
json.dump({'off': OFF, 'm0': M0, 'mend': mend, 'draft': False}, open('meta.json', 'w'))
print('mama end', mend, 'OFF', OFF, 'end', an['character_end_times_seconds'][-1] + OFF)
