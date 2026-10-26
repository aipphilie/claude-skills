# procedural sound design for episode 1 (numpy only) -> sfx.wav (stereo 48k)
import numpy as np, json, subprocess
SR = 48000
T = json.load(open('times.json'))
END = T['end'] + 0.1
N = int(END * SR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def band(n, lo, hi, tilt=0.0, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    X = np.fft.rfft(r.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    m = ((f >= lo) & (f <= hi)).astype(float)
    if tilt: m *= (np.maximum(f, 20) / 100.0) ** (-tilt)
    y = np.fft.irfft(X * m, n)
    return y / (np.abs(y).max() + 1e-9)

def env(n, a, d, shape=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * shape / max(d, 1e-4))
    return e

def put(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    L[i:i + len(s)] += s * np.sqrt((1 - pan) / 2) * 1.41
    R[i:i + len(s)] += s * np.sqrt((1 + pan) / 2) * 1.41

def db(x): return 10 ** (x / 20)
t_all = np.arange(N) / SR

# ---- beds ----
rumble = band(N, 20, 140, tilt=1.0, seed=1)          # tunnel rumble
vent = band(N, 300, 2500, tilt=0.6, seed=2)           # air / ventilation
hum = 0.6 * np.sin(2 * np.pi * 50 * t_all) + 0.3 * np.sin(2 * np.pi * 100 * t_all) + 0.15 * np.sin(2 * np.pi * 150 * t_all)
bed = rumble * db(-24) + vent * db(-38)
# emergency hum after the lights die
bed += hum * db(-40) * np.clip((t_all - 11.5) * 3, 0, 1)
# smoke "wind" grows from the smoke shot and in the visibility scene
smk = band(N, 150, 900, tilt=0.4, seed=3)
smk_amt = np.clip((t_all - 12.0) / 2, 0, 1) * 0.5 + np.clip((t_all - 69.5) / 5, 0, 1) * 0.6 - np.clip((t_all - 80) / 3, 0, 1) * 0.4
bed += smk * db(-30) * np.clip(smk_amt, 0, 1)
L += bed; R += bed * 0.97 + np.roll(bed, 300) * 0.03

# ---- music pad: dark D-minor drone, swelling ----
def pad(freqs, n):
    t = np.arange(n) / SR; y = np.zeros(n)
    for f in freqs:
        for det in (-0.6, 0.0, 0.7):
            ph = rng.random() * 6.28
            y += np.sin(2 * np.pi * (f + det) * t + ph) + 0.35 * np.sin(2 * np.pi * 2 * (f + det) * t + ph) + 0.15 * np.sin(2 * np.pi * 3 * (f + det) * t)
    return y / np.abs(y).max()
padsig = pad([36.7, 73.4, 87.3, 110.0], N)
pad_amt = (0.5 + 0.5 * np.sin(2 * np.pi * t_all / 13.0)) * 0.6 + 0.4
pad_amt *= np.clip(t_all / 1.5, 0, 1)
pad_amt *= 1 - 0.7 * ((t_all > 46.3) & (t_all < 51.0))      # silence of the driver
pad_amt *= 1 + 0.8 * np.clip((t_all - 87.4) / 4, 0, 1) * (t_all < 97.0)  # tension when the speaker wakes
pad_amt *= 1 + 0.6 * (t_all > 105.4)
put(padsig * pad_amt * db(-27), 0)

# high tension tone during the voice in the speaker and the eyes-up beat
tens = np.sin(2 * np.pi * 1760 * t_all) * 0.5 + np.sin(2 * np.pi * 1767 * t_all) * 0.5
tamt = np.clip((t_all - T['alive']) / 2, 0, 1) * np.clip((100.0 - t_all) / 0.5, 0, 1)
L += tens * tamt * db(-44); R += tens * tamt * db(-44)

# ---- one-shots ----
def thump(dur=0.9, f0=55, gain=0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t * 18))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, dur, 5)
    y += band(n, 40, 400, seed=11) * env(n, 0.001, 0.15, 6) * 0.4
    return y * db(gain)
def whoosh(dur=0.6, rev=False):
    n = int(dur * SR); y = band(n, 300, 6000, tilt=0.5) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y[::-1] if rev else y
def click(f=2500, dur=0.04):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * 0.5 + band(n, 1000, 8000) * 0.5) * env(n, 0.0005, dur, 8)
def knock(f=750):
    n = int(0.18 * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 2.3 * t) + 0.4 * np.sin(2 * np.pi * 180 * t)) * env(n, 0.0008, 0.18, 9)
    return y + band(n, 500, 5000) * env(n, 0.0005, 0.03, 8) * 0.6
def screech(dur, f0, f1, gain=0, seed=0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.linspace(f0, f1, n) * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.51) / SR)
    y = y * (0.6 + 0.4 * band(n, 2, 40, seed=seed + 50)) + band(n, 1500, 7000, seed=seed) * 0.5
    a = np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.15)
    return y * a * db(gain)
def crackle(dur, dens=60, gain=0):
    n = int(dur * SR); y = np.zeros(n)
    for _ in range(int(dens * dur)):
        i = rng.integers(0, max(1, n - 400)); k = rng.integers(40, 400)
        y[i:i + k] += band(k, 800, 9000) * np.exp(-np.arange(k) / (k / 4)) * rng.random()
    return y * db(gain)
def beep(f=425, dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.minimum(1, np.minimum(t, dur - t) / 0.01)
def heartbeat():
    n = int(0.25 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 48 * t) * env(n, 0.005, 0.25, 9)

# cold open: low hit at start, glitch whooshes
put(thump(1.6, 45, -6), 0.02)
put(whoosh(0.5, True), 2.55, db(-16)); put(crackle(0.25, 200, -14), 2.92)
put(whoosh(0.8, True), 6.5, db(-14))
# rewind blip
for k in range(10): put(click(1800 + k * 120, 0.03), 7.25 + k * 0.07, db(-24))
# brakes: squeal then clunk
put(screech(1.05, 2600, 1500, -14, 1), 9.85, pan=-0.2)
put(band(int(1.0 * SR), 200, 3000) * env(int(1.0 * SR), 0.05, 1.0, 3), 9.9, db(-18))
put(thump(0.8, 60, -4), 10.82)
for k in range(6): put(knock(300 + 40 * k) * 0.4, 10.85 + k * 0.05, db(-20), pan=0.3)
# lights die: buzz + click
n = int(0.35 * SR); zz = np.sign(np.sin(2 * np.pi * 50 * np.arange(n) / SR)) * band(n, 100, 4000) * 0.6
put(zz * env(n, 0.005, 0.35, 3), 11.32, db(-16)); put(click(900, 0.06), 11.62, db(-10))
# smoke hiss
put(band(int(2 * SR), 2000, 9000) * np.linspace(0, 1, int(2 * SR)) ** 2, 12.0, db(-28))
# logo sting
put(whoosh(1.2, True), 15.0, db(-12)); put(thump(2.2, 40, -2), 16.15)
put(screech(1.6, 880, 870, -30, 3), 16.15)

# shot cuts: soft low thumps / whooshes
for s in T['shots']:
    put(thump(0.4, 70, -22), s)
    put(whoosh(0.35), s - 0.15, db(-30))

# cane taps
for a in T['taps']: put(knock(820), a, db(-8), pan=-0.15)
# stream / chat ticks
for a in np.arange(36.75, 41.0, 0.55): put(click(1400, 0.03), a, db(-30), pan=0.4)
for a in np.arange(74.6, 77.6, 0.55): put(click(1400, 0.03), a, db(-30), pan=0.4)
put(crackle(0.35, 400, -12), T['chatKey']); put(thump(0.6, 80, -10), T['chatKey'])
# radio squelch, LED off
put(band(int(0.4 * SR), 600, 5000) * env(int(0.4 * SR), 0.005, 0.4, 3), 41.3, db(-22), pan=0.3)
put(band(int(0.25 * SR), 600, 5000) * env(int(0.25 * SR), 0.005, 0.25, 3), T['radioHide'] + 1.2, db(-26), pan=0.3)
# dead speaker: faint static
put(band(int(4.6 * SR), 1000, 8000) * 0.6, 46.3, db(-40))
# button press + unanswered call tones
put(click(1200, 0.05), T['press'], db(-6)); put(knock(400) * 0.5, T['press'], db(-14))
for a in np.arange(T['press'] + 0.35, 57.3, 0.9): put(beep(), a, db(-26))
for a in np.arange(67.75, 69.5, 0.9): put(beep(), a, db(-28))
# check, stamp
put(click(2000, 0.05), T['check'], db(-18)); put(thump(0.6, 65, -6), T['stamp']); put(knock(220), T['stamp'], db(-10))
# contact rail: arc + mains buzz
put(crackle(2.3, 120, -10), T['volt'], pan=0.2)
nb = int(2.3 * SR); tb = np.arange(nb) / SR
buzz = np.tanh(3 * np.sin(2 * np.pi * 100 * tb)) * env(nb, 0.05, 2.3, 1.5)
put(buzz, T['volt'], db(-20)); put(thump(1.0, 50, -6), T['volt'])
# visibility glitch
put(crackle(0.25, 300, -16), T['a20'])
# prying the doors: heavy metal creaks
for k, a in enumerate(T['jerks']):
    d = 0.7 + 0.2 * k
    put(screech(d, 420 + 60 * k, 300 + 40 * k, -10, 20 + k), a - 0.05)
    put(band(int(d * SR), 80, 900) * env(int(d * SR), 0.02, d, 3), a - 0.05, db(-12))
    put(thump(0.5, 60, -12), a + d - 0.2)
put(band(int(1.2 * SR), 200, 6000, tilt=0.4) * env(int(1.2 * SR), 0.6, 0.6, 2), 86.0, db(-20))  # tunnel air rushes in
# speaker wakes: switch-on pop + static bed until the voice ends
put(thump(0.3, 120, -10), T['alive']); put(crackle(0.6, 300, -12), T['alive'])
put(band(int(9.5 * SR), 1500, 7000) * 0.5 + crackle(9.5, 25, -6), T['alive'] + 0.1, db(-34))
# heartbeat under the "name" beat
for a in np.arange(97.1, 100.0, 0.75):
    put(heartbeat(), a, db(-8)); put(heartbeat(), a + 0.22, db(-12))
put(thump(1.2, 42, -4), T['eyesUp'])
# footsteps on ballast going away
n = int(0.12 * SR)
for k, a in enumerate(np.arange(100.6, 103.3, 0.42)):
    put(band(n, 400, 6000, seed=100 + k) * env(n, 0.003, 0.12, 6), a, db(-12 - k * 2.2), pan=0.1)
put(thump(0.7, 55, -10), 100.55)
# choice stingers + end
put(thump(1.2, 50, -6), T['plA']); put(whoosh(0.6, True), T['plA'] - 0.6, db(-16))
put(thump(1.2, 45, -4), T['plB']); put(screech(1.0, 660, 640, -30, 9), T['plB'])
put(whoosh(0.8, True), T['fork'] - 0.8, db(-14)); put(thump(1.4, 48, -6), T['fork'])
put(whoosh(1.2, True), T['endCard'] - 1.2, db(-12)); put(thump(2.5, 38, -2), T['endCard'])
fade = np.clip((END - 0.1 - t_all) / 1.2, 0, 1)
L *= fade; R *= fade

# ---- duck under the voice ----
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'voice.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, np.float32).astype(np.float64)
v = np.pad(v, (0, max(0, N - len(v))))[:N]
hop = 480; e = np.sqrt(np.convolve(v ** 2, np.ones(hop * 4) / (hop * 4), 'same'))
act = np.clip(e / 0.03, 0, 1)
# smooth (attack/release ~ 120 ms) by simple box blur in the 100 Hz domain
a2 = act[::hop]; k = np.ones(12) / 12; a2 = np.convolve(a2, k, 'same'); a2 = np.maximum(a2, np.roll(a2, 6))
act = np.interp(np.arange(N), np.arange(len(a2)) * hop, a2)
duck = 1 - 0.45 * act
L *= duck; R *= duck
st = np.stack([L, R], 1)
st = st / np.abs(st).max() * 0.7
pcm = (st * 32767).astype('<i2').tobytes()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', 'sfx.wav'], input=pcm)
print('ok', N / SR)
