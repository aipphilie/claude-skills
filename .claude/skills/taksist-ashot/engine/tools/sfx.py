# python3 tools/sfx.py src/story.json src/timeline.json public/voice.wav public/mix.wav
# Звуки монтажа и музыка синтезом (без чужих сэмплов), приглушение под голос, -14 LUFS.
import json, sys, subprocess, numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile
story, tl = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
SR = 48000; total = tl['total']; N = int(total * SR)
rng = np.random.default_rng(3)
L = {l['id']: l for l in tl['lines']}
def cue(name):
    c = story['cues'][name] if isinstance(name, str) else name
    if isinstance(c, (int, float)): return c
    i, w, off = c; l = L[i]
    return (l['end'] if w == 'end' else l['start'] if w == 'start' else l['words'][w]['s']) + (off or 0)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x)
def lp(x, hi): b, a = butter(2, hi / (SR / 2), 'low'); return lfilter(b, a, x)
def env(n, a=.005, r=.1): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
def noise(s): return rng.standard_normal(int(s * SR))
def tone(f, s, r=.1, a=.002):
    n = int(s * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * env(n, a, r)
sfx = np.zeros(N); mus = np.zeros(N)
def put(buf, t, x, g=1.0):
    i = int(t * SR)
    if i >= N: return
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g

def tick(hi=True):  # щелчок поворотника: «тик» и «так»
    n = int(.05 * SR); x = bp(noise(.05), 1800 if hi else 1200, 6000) * env(n, .0005, .006)
    return x + tone(2400 if hi else 1700, .05, .01) * .3
def whoosh(s=.32):
    n = int(s * SR); t = np.arange(n) / SR; x = noise(s)
    lo = bp(x, 400, 2500); hi = bp(x, 2500, 8000); k = t / s
    return (lo * (1 - k) + hi * k) * np.sin(np.pi * k) ** 1.5
def kaching():  # касса: механический стук + звонок
    k = bp(noise(.06), 500, 4000) * env(int(.06 * SR), .001, .012)
    bell = sum(tone(f, 1.0, .35) * g for f, g in ((2093, 1), (2637, .6), (3136, .4), (4186, .25)))
    out = np.zeros(int(1.1 * SR)); out[:len(k)] += k * 1.2; out[int(.07 * SR):int(.07 * SR) + len(bell)] += bell[:len(out) - int(.07 * SR)] * .5
    for d in (.0, .05, .1):  # монетки
        c = tone(5200 + d * 4000, .12, .03); i = int((.15 + d) * SR); out[i:i + len(c)] += c * .3
    return out
def thump():
    n = int(.3 * SR); t = np.arange(n) / SR; f = 45 + 100 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) + bp(noise(.3), 100, 800) * env(n, .001, .03) * .5
def pop():
    n = int(.12 * SR); t = np.arange(n) / SR; f = 500 + 900 * t / .12
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .04)
def click(): return bp(noise(.03), 1500, 7000) * env(int(.03 * SR), .0005, .006) + tone(900, .03, .02) * .5
def shutter():
    a = bp(noise(.04), 1000, 9000) * env(int(.04 * SR), .0005, .008); out = np.zeros(int(.2 * SR))
    out[:len(a)] += a; out[int(.09 * SR):int(.09 * SR) + len(a)] += a * .8; return out
def scratch():  # «чего?!» — стоп-скретч
    n = int(.25 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 9) + 150
    return bp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) + noise(.25) * .3, 200, 4000) * env(n, .002, .08) * .4

def squeal(s):  # визг тормозов: два «поющих» тона с дрожью + шорох резины
    n = int(s * SR); t = np.arange(n) / SR; wob = 1 + .015 * np.sin(2 * np.pi * 23 * t)
    x = sum(np.sin(2 * np.pi * np.cumsum(f * wob * (1 - .08 * t / s)) / SR) * g for f, g in ((2350, 1), (3420, .5), (4700, .25)))
    x += bp(noise(s), 1500, 7000) * .6
    return x * np.minimum(1, t / .04) * np.minimum(1, (s - t) / .08)
intro = story.get('intro')
if intro == 'brake':  # хук: визг тормозов, удар, рывок, телефон
    tb, ts = intro_t = (cue('brakeAt'), cue('stopAt'))
    put(sfx, 0.0, bp(noise(tb), 60, 400) * .8, .25)           # гул мотора на ходу
    put(sfx, tb, squeal(ts - tb + .05), .38)
    put(sfx, ts, thump(), .7); put(sfx, ts + .02, bp(noise(.15), 300, 3000) * env(int(.15 * SR), .002, .04), .4)
    put(sfx, cue('joltIn') + .05, whoosh(.3), .32)
    put(sfx, cue('phoneLand'), click(), .7); put(sfx, cue('phoneLand') + .07, click(), .4)
else:
    # поворотник на старте
    for i in range(4): put(sfx, 0.05 + i * 0.42, tick(i % 2 == 0), .55)
# вжух на зумах/перебивках
for s in story['shots'][1:]:
    if s.get('whoosh') or s.get('move', 0) >= 6:
        put(sfx, cue(s['at']) - .12, whoosh(), .30 if s.get('whoosh') else .17)
# вжух на каждую врезку-ракурс
for x in story.get('inserts', []):
    if x['from'] != 0 and x['shot'] not in ('brake', 'jolt'): put(sfx, cue(x['from']) - .1, whoosh(.26), .28)
# звуки сцен вне такси: inserts[].sfx = [[сдвиг от начала, 'thump'|'kaching'|'pop'|'click'|'whoosh'], …]
SND = {'thump': (thump, .5), 'kaching': (kaching, .35), 'pop': (pop, .25), 'click': (click, .35), 'whoosh': (lambda: whoosh(.4), .25)}
for x in story.get('inserts', []):
    for off, name in x.get('sfx', []):
        f, g = SND[name]; put(sfx, cue(x['from']) + off, f(), g)
put(sfx, cue('n5'), pop(), .25)
put(sfx, cue('cross'), bp(noise(.18), 1500, 6000) * env(int(.18 * SR), .01, .06), .22)
put(sfx, cue('n12'), kaching(), .42)
put(sfx, cue('shock') + .02, thump(), .55); put(sfx, cue('shock'), scratch(), .5)
put(sfx, cue('explain'), pop(), .2); put(sfx, cue('years'), whoosh(.6), .15)
for i in range(10): put(sfx, cue('years') + .05 + i * .085, click(), .08)  # листаются годы
put(sfx, cue('buttons'), pop(), .22); put(sfx, cue('buttons') + .12, pop(), .2)
put(sfx, cue('poke'), click(), .5); put(sfx, cue('poke') + .03, tone(1568, .4, .12) + tone(2093, .4, .1) * .6, .18)
put(sfx, cue('less'), pop(), .2)
put(sfx, cue('n400'), kaching(), .5)
put(sfx, cue('freeze'), shutter(), .5); put(sfx, cue('freeze'), thump(), .3)

# лёгкая музыка: тёплые аккорды (электропиано), мягкий бочка/шейкер, 96 bpm
bpm = 96; beat = 60 / bpm
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7], [164.8, 207.7, 246.9]]  # Am F G E
def ep(f, s):
    n = int(s * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6)) * np.exp(-t * 1.8) * np.minimum(1, t / .01)
t = 0.0; bar = 0
while t < cue('freeze'):
    for f in chords[bar % 4]: put(mus, t, ep(f, beat * 4), .10)
    put(mus, t, ep(chords[bar % 4][0] / 2, beat * 4), .14)
    for b in range(4):
        tb = t + b * beat
        if b in (0, 2): put(mus, tb, thump()[:int(.25 * SR)], .10)
        put(mus, tb + beat / 2, bp(noise(.04), 5000, 12000) * env(int(.04 * SR), .002, .01), .05)
        if b in (1, 3): put(mus, tb, bp(noise(.1), 1200, 6000) * env(int(.1 * SR), .002, .03), .06)
    t += beat * 4; bar += 1
# после стоп-кадра музыка затухает за 0.3 сек
fi = int(cue('freeze') * SR); fo = int(.3 * SR)
mus[fi:fi + fo] *= np.linspace(1, 0, len(mus[fi:fi + fo])); mus[fi + fo:] = 0
mus = lp(mus, 6000)

sr, v = wavfile.read(sys.argv[3]); v = v.astype(np.float64) / 32768
v = np.pad(v, (0, max(0, N - len(v))))[:N]
# приглушение под голос: огибающая с атакой ~80 мс и отпусканием ~400 мс
e = np.abs(v); win = int(.05 * SR); e = np.convolve(e, np.ones(win) / win, 'same'); on = (e > .02).astype(float)
duck = np.zeros(N); a, r = 1 / (0.08 * SR), 1 / (0.4 * SR); d = 0
idx = np.arange(N)
# быстро: сглаживаем ступенчатый сигнал разными окнами
on_lead = np.convolve(on, np.ones(int(.12 * SR)), 'same') > 0
duck = np.convolve(on_lead.astype(float), np.ones(int(.4 * SR)) / int(.4 * SR), 'same')
mix = v * 1.0 + sfx * (1 - .35 * duck) * .9 + mus * (1 - .6 * duck)
mix /= max(1e-9, np.abs(mix).max()) / .9
wavfile.write('/tmp/_premix.wav' if False else sys.argv[4] + '.raw.wav', SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', sys.argv[4] + '.raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', sys.argv[4]], check=True)
print('ok', round(total, 2), 'cues:', {k: round(cue(k), 2) for k in story['cues']})
