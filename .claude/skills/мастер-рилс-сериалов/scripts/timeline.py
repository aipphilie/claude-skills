#!/usr/bin/env python3
"""Lay voice-over chunks on one timeline and compute phrase + word timings.

usage: python3 timeline.py voice_config.json OUT_DIR

voice_config.json:
{
  "vo_dir": "vo",                      # folder with 01.mp3, 02.mp3 ... (one file per scene chunk)
  "tail": 4.5,                         # seconds of end card after the last phrase
  "chunks": [
    {"id": "01", "start": 1.0,         # absolute start (first chunk) ...
     "phrases": ["Этот приёмник выключен.", "Шнур выдернут…", "Но он только что принял сигнал."]},
    {"id": "02", "gap": 0.8,           # ... or a gap after the previous chunk
     "phrases": ["..."], "pauses": {"3": 0.9}}   # extra silence inserted AFTER phrase index 3
  ]
}

Each chunk is split on silences (-38 dB, >=0.15 s). The number of speech segments must equal
the number of phrases you list — if the assert fires, split/merge phrases to match what the
narrator actually did (print the segments, listen, adjust). Word times inside a phrase are
estimated from vowel (syllable) counts, which is close enough for karaoke captions.

Writes OUT_DIR/voice.wav, OUT_DIR/timeline.json and OUT_DIR/timeline.js (const TOTAL, const PH).
"""
import subprocess, re, json, wave, sys, os
import numpy as np

SR = 48000

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-af', 'loudnorm=I=-16:TP=-1.5', '-ac', '1',
                          '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def segments(path, dur):
    err = subprocess.run(['ffmpeg', '-i', path, '-af', 'silencedetect=n=-38dB:d=0.15', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', err)]
    en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', err)]
    segs, cur = [], 0.0
    for s, e in zip(st, en):
        if s - cur > .08: segs.append([cur, s])
        cur = e
    if dur - cur > .08: segs.append([cur, dur])
    return segs

def syl(w):
    return max(1, len(re.findall('[аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouyAEIOUY]', w)))

def main(cfg_path, out):
    cfg = json.load(open(cfg_path)); base = os.path.dirname(os.path.abspath(cfg_path))
    vo = os.path.join(base, cfg.get('vo_dir', 'vo'))
    phrases, track, cursor = [], [], 0.0
    for ch in cfg['chunks']:
        cid = ch['id']; path = next(os.path.join(vo, f) for f in sorted(os.listdir(vo)) if f.startswith(cid + '.'))
        a = load(path); dur = len(a) / SR; segs = segments(path, dur); texts = ch['phrases']
        if len(segs) != len(texts):
            sys.exit(f'chunk {cid}: {len(segs)} speech segments {[[round(x,2) for x in s] for s in segs]} but {len(texts)} phrases')
        g0 = ch['start'] if 'start' in ch else cursor + ch.get('gap', .8)
        extra = {int(k): v for k, v in ch.get('pauses', {}).items()}; shift = 0.0
        for i, ((s, e), txt) in enumerate(zip(segs, texts)):
            a0 = 0 if i == 0 else (segs[i-1][1] + s) / 2          # cut mid-silence so breaths stay natural
            a1 = dur if i == len(segs) - 1 else (e + segs[i+1][0]) / 2
            track.append((g0 + shift + a0, a[int(a0*SR):int(a1*SR)]))
            gs, ge = g0 + shift + s, g0 + shift + e
            words = txt.split(); tot = sum(syl(w) for w in words); acc = 0; W = []
            for w in words:
                W.append([w, round(gs + (ge - gs) * acc / tot, 3)]); acc += syl(w)
            phrases.append({'id': f'{cid}.{i}', 's': round(gs, 3), 'e': round(ge, 3), 'text': txt, 'w': W})
            shift += extra.get(i, 0)
        cursor = g0 + shift + dur
    total = round(cursor + cfg.get('tail', 4.5), 2)
    buf = np.zeros(int(total * SR), np.float32)
    for t0, piece in track:
        i = int(t0 * SR); buf[i:i+len(piece)] += piece[:len(buf)-i]
    os.makedirs(out, exist_ok=True)
    with wave.open(os.path.join(out, 'voice.wav'), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(buf, -1, 1) * 32767).astype(np.int16).tobytes())
    P = {p['id']: p for p in phrases}
    with open(os.path.join(out, 'timeline.js'), 'w') as f:
        f.write('const TOTAL=%s;\nconst PH=%s;\n' % (total, json.dumps(P, ensure_ascii=False)))
    json.dump({'total': total, 'ph': P}, open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
    for p in phrases: print(p['id'], p['s'], p['e'], p['text'])
    print('TOTAL', total)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '.')
