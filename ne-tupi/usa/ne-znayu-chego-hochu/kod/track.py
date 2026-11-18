"""Трек персонажа на весь ролик: позы по шотам + рот по таймингам ElevenLabs."""
import json, sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import anim3d
from tl import spans, END, DUR, N, FPS, GAPS, wt
from scenes import SHOTS
VOW = {'a': 'A', 'o': 'O', 'u': 'U', 'e': 'E', 'i': 'E', 'y': 'E'}
LAB = set('mbp'); SMALL = {'A': 'E', 'O': 'U', 'E': 'E', 'U': 'U'}
sp, tg = spans()
for name, s, e in tg:
    if name == 'laughs': sp.append((s, e, '#smile'))
    if name == 'gasps': sp.append((s, e, '#wow'))
sp.sort(); vowels = [(s, e, VOW[c]) for s, e, c in sp if c in VOW]
pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'zvuk/voice.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; hop = 16000 // FPS
rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-9) if i * hop < len(x) else 0 for i in range(N)])
thr = np.percentile(rms[rms > 1e-4], 25) * 0.6
import bisect
starts = [s[0] for s in sp]
def mouth_at(i):
    t = (i + 0.5) / FPS
    j = bisect.bisect_right(starts, t + 0.02)
    cur = [s for s in sp[max(0, j - 6):j] if s[0] - 0.02 <= t <= s[1] + 0.02]
    if not cur or rms[i] < thr: return None
    c = cur[0][2]
    if c.startswith('#'): return c[1:]
    if c in VOW: return VOW[c]
    if c in LAB: return 'M'
    k = bisect.bisect_left([v[0] for v in vowels], t)
    near = min(vowels[max(0, k - 2):k + 2], key=lambda v: abs((v[0] + v[1]) / 2 - t))
    return SMALL[near[2]] if abs((near[0] + near[1]) / 2 - t) < 0.12 else 'E'
lip = [mouth_at(i) for i in range(N)]
for i in range(1, N - 1):
    if lip[i] != lip[i - 1] and lip[i] != lip[i + 1]: lip[i] = lip[i - 1]

TEND = wt(9, 'тупи', end=True)
def _ingap(t):
    for g0, g1 in GAPS:
        if g0 - 0.01 <= t < g1: return g1
    return t
SEG = [(_ingap(sh['t']), sh['anim'] or ['razgovor']) for sh in SHOTS]
for g0, g1 in GAPS: SEG.append((g0, ['dyhanie']))   # в заставке главы — дышит
SEG.sort(key=lambda s: s[0])
# переносим анимации шота на начало главы (после заставки)
fixed = []
for t0, names in SEG:
    fixed.append((t0, names))
SEG = fixed + [(TEND + 0.2, ['povorot_short']), (TEND + 0.85, ['walk'])]
SEG = sorted(SEG, key=lambda s: s[0])
WALK0 = TEND + 0.85
def frames_of(name):
    if name == 'povorot_short':
        p, m = anim3d.ANIMS['povorot'][1](); return [anim3d.to3d(q, 'rest', 'povorot') for q in p[:16]], ['rest'] * 16
    if name == 'walk':
        p, m = anim3d.ANIMS['shag-profil'][1](); fr = [anim3d.to3d(q, 'rest', 'shag-profil') for q in p]
        return fr * 6, ['rest'] * len(fr) * 6
    p, m = anim3d.ANIMS[name][1](); return [anim3d.to3d(q, mm, name) for q, mm in zip(p, m)], m
def stretch(fr, ms, k):
    n = max(1, int(round(len(fr) * k))); idx = [min(len(fr) - 1, int(j / k)) for j in range(n)]
    return [fr[j] for j in idx], [ms[j] for j in idx]
out, amouth, seg_of = [], [], []
for si, (t0, names) in enumerate(SEG):
    t1 = SEG[si + 1][0] if si + 1 < len(SEG) else DUR
    L = int(round(t1 * FPS)) - len(out)
    if L <= 0: continue
    fr, ms = [], []
    for nm in names:
        a, b = frames_of(nm); fr += a; ms += b
    if names[0] not in ('walk', 'povorot_short'):
        if len(fr) > L: fr, ms = stretch(fr, ms, L / len(fr))
        k = 0
        while len(fr) < L:
            a, b = frames_of('razgovor' if k % 2 == 0 else 'pokachivanie'); fr += a; ms += b; k += 1
    else:
        while len(fr) < L: fr.append(fr[-1]); ms.append(ms[-1])
    out += fr[:L]; amouth += ms[:L]; seg_of += [names[0]] * L
out = out[:N]; xoff = [0.0] * N
for i in range(N):
    m = lip[i]
    if m is None: m = amouth[i] if amouth[i] in ('smile', 'sad', 'wow') else 'rest'
    out[i] = dict(out[i], mouth=m)
    if seg_of[i] == 'walk': xoff[i] = -(i - int(round(WALK0 * FPS))) * 13.0
json.dump(out, open('track.json', 'w')); json.dump(xoff, open('xoff.json', 'w'))
print(len(out), N, sum(1 for m in lip if m) / N)
