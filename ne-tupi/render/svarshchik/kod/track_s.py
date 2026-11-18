"""Трек двух человечков: Дима (main) и сварщик (svar, каска, шире/ниже). Рот по таймингам ElevenLabs у того, кто говорит в сцене."""
import json, sys, os, subprocess, numpy as np
sys.path.insert(0, '/home/user/claude-skills/ne-tupi')
import anim3d, anim
from words import C, S, E, B, END, DUR
FPS = 24; N = int(DUR * FPS)
VOW = {'а': 'A', 'я': 'A', 'о': 'O', 'ё': 'O', 'у': 'U', 'ю': 'U', 'е': 'E', 'э': 'E', 'и': 'E', 'ы': 'E'}
LAB = set('мбп'); SMALL = {'A': 'E', 'O': 'U', 'E': 'E', 'U': 'U'}
spans = []; intag = False
for i, ch in enumerate(C):
    if ch == '[': intag = True; continue
    if ch == ']': intag = False; continue
    if intag or not ch.isalpha(): continue
    spans.append((S[i], E[i], ch.lower()))
vowels = [(s, e, VOW[c]) for s, e, c in spans if c in VOW]
pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'voice.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = 16000 // FPS
rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2) + 1e-9) if i*hop < len(x) else 0 for i in range(N)])
thr = np.percentile(rms[rms > 1e-4], 25) * 0.6
def mouth_at(i):
    t = (i + 0.5) / FPS
    cur = [sp for sp in spans if sp[0] - 0.02 <= t <= sp[1] + 0.02]
    if not cur or rms[min(i, N-1)] < thr: return None
    c = cur[0][2]
    if c in VOW: return VOW[c]
    if c in LAB: return 'M'
    near = min(vowels, key=lambda v: abs((v[0]+v[1])/2 - t))
    return SMALL[near[2]] if abs((near[0]+near[1])/2 - t) < 0.12 else 'E'
lip = [mouth_at(i) for i in range(N)]
for i in range(1, N - 1):
    if lip[i] != lip[i-1] and lip[i] != lip[i+1]: lip[i] = lip[i-1]
# кто говорит в сцене k
SPEAK = ['svar', 'main', 'svar', 'main', 'main', 'main', 'main', 'main', 'main', 'svar', 'svar', 'svar', 'main', 'main', 'main', 'main', 'main', 'main']
def speaker(t): return SPEAK[max(j for j in range(len(B)) if B[j] <= t)]
# позы по сценам
SEG = {
 'main': [(B[0], 'cheshet-golovu'), (B[1], 'obyasnyaet'), (B[2], 'dyhanie'), (B[3], 'net'), (B[3] + 1.9, 'pozhimaet-plechami'), (B[4], 'pozhimaet-plechami'),
          (B[5], 'ukazyvaet-vverh'), (B[6], 'kivok'), (B[7], 'razgovor-zhesty'), (B[8], 'dyhanie'), (B[9], 'dyhanie'), (B[12], 'cheshet-golovu'),
          (B[13], 'net'), (B[14], 'obyasnyaet'), (B[15], 'razgovor-zhesty'), (B[16], 'mashet'), (B[17], 'kivok'), (END + 0.1, 'povorot_short'), (END + 0.75, 'walk')],
 'svar': [(B[0], 'ruki-v-boki'), (B[1], 'dyhanie'), (B[2], 'kivok'), (B[3], 'ruki-v-boki'), (B[4], 'dyhanie'), (B[9], 'ruki-v-boki'), (B[9] + 2.2, 'mashet'),
          (B[10], 'ukazyvaet-vverh'), (B[11], 'cheshet-golovu'), (B[12], 'dyhanie'), (B[13] + 2.0, 'ruki-v-boki'), (B[14], 'dyhanie'), (B[16], 'kivok'),
          (B[17], 'dyhanie'), (END + 0.1, 'povorot_short'), (END + 0.75, 'walk')]}
BUILD = {'main': {}, 'svar': dict(bw=1.22, th=0.92, lh=0.85, helmet=1)}
def frames_of(name):
    if name == 'povorot_short':
        p, m = anim3d.ANIMS['povorot'][1](); return [anim3d.to3d(q, 'rest', 'povorot') for q in p[:16]], ['rest']*16
    if name == 'walk':
        p, m = anim3d.ANIMS['shag-profil'][1](); fr = [anim3d.to3d(q, 'rest', 'shag-profil') for q in p]
        return fr * 4, ['rest'] * len(fr) * 4
    p, m = anim3d.ANIMS[name][1](); return [anim3d.to3d(q, mm, name) for q, mm in zip(p, m)], m
def stretch(fr, ms, k):
    n = max(1, int(round(len(fr) * k))); idx = [min(len(fr)-1, int(j / k)) for j in range(n)]
    return [fr[j] for j in idx], [ms[j] for j in idx]
jobs = {}; segs = {}
for who, seg in SEG.items():
    out, amouth, seg_of = [], [], []
    for si, (t0, nm) in enumerate(seg):
        t1 = seg[si+1][0] if si + 1 < len(seg) else DUR
        L = int(round(t1 * FPS)) - len(out)
        if L <= 0: continue
        fr, ms = frames_of(nm)
        if nm not in ('walk', 'povorot_short'):
            if len(fr) > L: fr, ms = stretch(fr, ms, L / len(fr))
            else: fr, ms = stretch(fr, ms, min(1.6, L / len(fr)))
            k = 0
            while len(fr) < L:
                a, b = frames_of('dyhanie' if who != speaker(t0) else ('razgovor' if k % 2 == 0 else 'pokachivanie')); fr += a; ms += b; k += 1
        else:
            while len(fr) < L: fr.append(fr[-1]); ms.append(ms[-1])
        out += fr[:L]; amouth += ms[:L]; seg_of += [nm] * L
    for i in range(N):
        t = i / FPS
        m = lip[i] if speaker(t) == who else None
        if m is None: m = amouth[i] if amouth[i] in ('smile', 'sad', 'wow') else ('smile' if who == 'svar' and B[3] <= t < B[4] else 'rest')
        out[i] = dict(out[i], mouth=m, **BUILD[who])
    jobs[who] = out; segs[who] = seg_of
json.dump(jobs, open('track.json', 'w')); json.dump(segs, open('seg.json', 'w'))
print({k: len(v) for k, v in jobs.items()}, N)
