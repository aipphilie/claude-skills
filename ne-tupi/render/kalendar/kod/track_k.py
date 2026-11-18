"""Трек «Листок на 66 тысяч»: main (весь ролик), svar (сцена с девятиэтажкой), t1–t3 (триптих). Рот по таймингам ElevenLabs у main."""
import json, sys, math, subprocess, numpy as np
sys.path.insert(0, '/home/user/claude-skills/ne-tupi')
import anim3d
from words import C, S, E, B, END, DUR
from tm import T
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

BASE = anim3d.to3d(anim3d.ANIMS['dyhanie'][1]()[0][0], 'rest', 'dyhanie')
def custom(name, n):
    out = []
    for j in range(n):
        u = j / FPS; p = dict(BASE)
        if name == 'paint':      # левая рука в сторону, кругами «закрашивает»
            p.update(la=[100 + 14 * math.sin(u * 13), 12 + 16 * math.cos(u * 13)], ra=[18, 4], lean=-4, head=-6, dy=0)
        elif name == 'holdup':   # обе руки вверх, держит предмет над головой
            b = math.sin(u * 7)
            p.update(la=[160 + 4 * b, 8], ra=[160 + 4 * b, 8], dy=-0.04 * abs(b))
        elif name == 'holdjump':
            b = abs(math.sin(u * 6))
            p.update(la=[165, 6], ra=[165, 6], dy=-0.9 * b, sink=0.15 * (1 - b) if b < 0.2 else 0)
        elif name == 'paintup':  # сварщик: правая рука с валиком вверх-вниз
            p.update(ra=[150 + 22 * math.sin(u * 8), 8], la=[25, 4], yaw=-10)
        out.append(p)
    return out, ['rest'] * n
CUSTOM = {'paint', 'holdup', 'holdjump', 'paintup'}
def frames_of(name, L=48):
    if name in CUSTOM: return custom(name, L)
    if name == 'povorot_short':
        p, m = anim3d.ANIMS['povorot'][1](); return [anim3d.to3d(q, 'rest', 'povorot') for q in p[:16]], ['rest']*16
    if name == 'walk':
        p, m = anim3d.ANIMS['shag-profil'][1](); fr = [anim3d.to3d(q, 'rest', 'shag-profil') for q in p]
        return fr * 4, ['rest'] * len(fr) * 4
    p, m = anim3d.ANIMS[name][1](); return [anim3d.to3d(q, mm, name) for q, mm in zip(p, m)], m
def stretch(fr, ms, k):
    n = max(1, int(round(len(fr) * k))); idx = [min(len(fr)-1, int(j / k)) for j in range(n)]
    return [fr[j] for j in idx], [ms[j] for j in idx]
def build(seg, t_end, talk=True, fill_talk=True):
    out, amouth, seg_of = [], [], []
    t_start = seg[0][0]; f0 = int(round(t_start * FPS))
    for si, (t0, nm) in enumerate(seg):
        t1 = seg[si+1][0] if si + 1 < len(seg) else t_end
        L = int(round(t1 * FPS)) - f0 - len(out)
        if L <= 0: continue
        fr, ms = frames_of(nm, L)
        if nm in CUSTOM: pass
        elif nm not in ('walk', 'povorot_short'):
            if len(fr) > L: fr, ms = stretch(fr, ms, L / len(fr))
            else: fr, ms = stretch(fr, ms, min(1.6, L / len(fr)))
            k = 0
            while len(fr) < L:
                a, b = frames_of(('razgovor' if k % 2 == 0 else 'pokachivanie') if fill_talk else 'dyhanie'); fr += a; ms += b; k += 1
        else:
            while len(fr) < L: fr.append(fr[-1]); ms.append(ms[-1])
        out += fr[:L]; amouth += ms[:L]; seg_of += [nm] * L
    for j in range(len(out)):
        i = f0 + j
        m = lip[i] if talk and i < N else None
        if m is None: m = amouth[j] if amouth[j] in ('smile', 'sad', 'wow') else 'rest'
        out[j] = dict(out[j], mouth=m)
    return out, seg_of, f0
MAIN = [(0, 'paint'), (B[2], 'holdup'), (B[3], 'ruki-v-boki'), (B[4], 'dyhanie'), (B[5], 'dyhanie'), (B[6], 'ukazyvaet-vverh'),
        (B[7], 'pozhimaet-plechami'), (T['mozg'], 'net'), (B[8], 'razgovor-zhesty'), (T['kalendar'], 'ukazyvaet-vbok'), (B[9], 'obyasnyaet'),
        (B[10], 'paint'), (B[11], 'pozhimaet-plechami'), (T['zakras1'], 'paint'), (B[12], 'mashet'), (B[13], 'ukazyvaet-vverh'),
        (B[14], 'cheshet-golovu'), (T['brosish'] - 0.1, 'net'), (B[15], 'holdup'), (B[16], 'obyasnyaet'), (B[17], 'ruki-v-boki'),
        (B[18], 'razgovor'), (T['odna'], 'kivok'), (B[19], 'ukazyvaet-vbok'), (B[20], 'paint'), (T['pervyy'] + 0.45, 'holdjump'),
        (END + 0.1, 'povorot_short'), (END + 0.75, 'walk')]
jobs, segs, offs = {}, {}, {}
jobs['main'], segs['main'], offs['main'] = build(MAIN, DUR)
jobs['svar'], segs['svar'], offs['svar'] = build([(B[12], 'paintup')], B[13] + 0.1, talk=False)
jobs['svar'] = [dict(p, bw=1.22, th=0.92, lh=0.85, helmet=1) for p in jobs['svar']]
for k, nm in (('t1', 'kivok'), ('t2', 'mashet'), ('t3', 'net')):
    jobs[k], segs[k], offs[k] = build([(B[5], nm)], B[6] + 0.1, talk=False, fill_talk=False)
json.dump(jobs, open('track.json', 'w')); json.dump(dict(seg=segs, off=offs), open('seg.json', 'w'))
print({k: len(v) for k, v in jobs.items()}, N)
