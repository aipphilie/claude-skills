"""Трек персонажа на весь ролик: позы по сегментам сценария + рот по таймингам ElevenLabs."""
import json, sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anim3d, anim
from words import C, S, E, tags, B, END, DUR
FPS = 24; N = int(DUR * FPS)

# --- рот ---
VOW = {'а': 'A', 'я': 'A', 'о': 'O', 'ё': 'O', 'у': 'U', 'ю': 'U', 'е': 'E', 'э': 'E', 'и': 'E', 'ы': 'E'}
LAB = set('мбп'); SMALL = {'A': 'E', 'O': 'U', 'E': 'E', 'U': 'U'}
spans = []; intag = False
for i, ch in enumerate(C):
    if ch == '[': intag = True; continue
    if ch == ']': intag = False; continue
    if intag or not ch.isalpha(): continue
    spans.append((S[i], E[i], ch.lower()))
for name, s, e in tags():
    if name == 'laughs': spans.append((s, e, '#smile'))
    if name == 'gasps': spans.append((s, e, '#wow'))
spans.sort()
vowels = [(s, e, VOW[c]) for s, e, c in spans if c in VOW]

# громкость голоса по кадрам (чтобы закрывать рот в паузах)
pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', 'voice.wav', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = 16000 // FPS
rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2) + 1e-9) for i in range(N)])
thr = np.percentile(rms[rms > 1e-4], 25) * 0.6

def mouth_at(i):
    t = (i + 0.5) / FPS
    cur = [sp for sp in spans if sp[0] - 0.02 <= t <= sp[1] + 0.02]
    if not cur or rms[min(i, N-1)] < thr: return None
    c = cur[0][2]
    if c.startswith('#'): return c[1:]
    if c in VOW: return VOW[c]
    if c in LAB: return 'M'
    near = min(vowels, key=lambda v: abs((v[0]+v[1])/2 - t))
    return SMALL[near[2]] if abs((near[0]+near[1])/2 - t) < 0.12 else 'E'

lip = [mouth_at(i) for i in range(N)]
for i in range(1, N - 1):      # убираем одиночные кадры (дрожание)
    if lip[i] != lip[i-1] and lip[i] != lip[i+1]: lip[i] = lip[i-1]

# --- позы по сегментам (время начала, [анимации]) ---
from tm import T
SEG = [(B[0], ['tashit']), (T['desyatyy'] - 0.1, ['ruki-v-boki']), (B[1], ['obyasnyaet']),
       (B[2], ['kivok']), (B[3], ['walkR']), (B[4], ['net']), (B[5], ['tashit']), (B[6], ['legkoR']), (T['kom'] - 0.05, ['ruki-v-boki']),
       (B[7], ['tashit']), (T['itogo'] - 0.1, ['pryzhok']), (B[9], ['ukazyvaet-vbok']), (B[10], ['ruki-v-boki']), (T['raza'], ['kivok']),
       (B[11], ['tashit']), (T['sdayutsya'] - 0.1, ['pozhimaet-plechami']), (B[12], ['mashet']), (T['poschitayu'], ['obyasnyaet']),
       (B[13], ['kivok']), (END + 0.1, ['povorot_short']), (END + 0.75, ['walk'])]
LOOP = {'tashit': 'tashit-v-goru', 'legkoR': 'tashit-legko', 'walkR': 'shag-profil'}
WALK0 = END + 0.75
def frames_of(name):
    if name in LOOP:
        nm = LOOP[name]; p, m = anim3d.ANIMS[nm][1](); fr = [anim3d.to3d(q, 'rest', nm) for q in p]
        if name == 'walkR': fr = [dict(q, yaw=90) for q in fr]
        return fr * 12, ['rest'] * len(fr) * 12
    if name == 'povorot_short':
        p, m = anim3d.ANIMS['povorot'][1](); return [anim3d.to3d(q, 'rest', 'povorot') for q in p[:16]], ['rest']*16
    if name == 'walk':
        p, m = anim3d.ANIMS['shag-profil'][1](); fr = [anim3d.to3d(q, 'rest', 'shag-profil') for q in p]
        return fr * 4, ['rest'] * len(fr) * 4
    p, m = anim3d.ANIMS[name][1](); return [anim3d.to3d(q, mm, name) for q, mm in zip(p, m)], m
def stretch(fr, ms, k):
    n = max(1, int(round(len(fr) * k))); idx = [min(len(fr)-1, int(j / k)) for j in range(n)]
    return [fr[j] for j in idx], [ms[j] for j in idx]

out, amouth, seg_of = [], [], []
for si, (t0, names) in enumerate(SEG):
    t1 = SEG[si+1][0] if si + 1 < len(SEG) else DUR
    L = int(round(t1 * FPS)) - len(out)
    fr, ms = [], []
    for nm in names:
        a, b = frames_of(nm); fr += a; ms += b
    if names[0] not in ('walk', 'povorot_short') and names[0] not in LOOP:
        if len(fr) > L: fr, ms = stretch(fr, ms, L / len(fr))
        elif len(names) == 1: fr, ms = stretch(fr, ms, min(1.6, L / len(fr)))
        k = 0
        while len(fr) < L:   # добивка: разговор с покачиванием головы
            a, b = frames_of('razgovor' if k % 2 == 0 else 'pokachivanie'); fr += a; ms += b; k += 1
    else:
        while len(fr) < L: fr.append(fr[-1]); ms.append(ms[-1])
    out += fr[:L]; amouth += ms[:L]; seg_of += [names[0]] * L

xoff = [0.0] * N
for i in range(N):
    m = lip[i]
    if m is None: m = amouth[i] if amouth[i] in ('smile', 'sad', 'wow') else 'rest'
    out[i] = dict(out[i], mouth=m)
    if seg_of[i] == 'walk':
        xoff[i] = -(i - int(round(WALK0 * FPS))) * 16.0   # уходит влево, px за кадр (в масштабе финального кадра)
json.dump({'main': out}, open('track.json', 'w'))
json.dump(xoff, open('xoff.json', 'w')); json.dump(seg_of, open('seg.json', 'w'))
print(len(out), sum(1 for m in lip if m) / N)
