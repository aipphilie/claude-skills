#!/usr/bin/env python3
"""Synthesised sound design under the voice, then the final mix at Instagram loudness.

usage: python3 mix_audio.py sound.json OUT_DIR      (OUT_DIR must contain voice.wav + timeline.json)

sound.json:
{
  "ambience": [   # beds; overlapping beds crossfade because every bed has soft, centred ramps
    {"type": "wind",  "start": 8.85, "end": 19.1, "gain": 1.0, "fade_in": 1.3, "fade_out": 0.45},
    {"type": "room",  "start": 1.0,  "end": 8.85},              # muffled wind through walls + stove crackle
    {"type": "storm", "start": 22.9, "end": 35.5},              # strong wind
    {"type": "hum",   "start": 35.5, "end": 43.3, "hz": 50},     # generator / mains hum
    {"type": "drone", "start": 43.3, "end": 120, "gain": 0.8},   # low tension pad
    {"type": "rotor", "start": 38.4, "end": 40.9},               # helicopter
    {"type": "office", ...}  # computers/fans + mains hum (dispatch room, office)
    {"type": "line", ...}    # old phone line: band-limited hiss + crackle (under a voice on the phone)
    {"type": "fire", ...}    # fire roar + crackle (smoke/fire scenes, a crackling silent call)
    {"type": "siren", ...}   # distant ambulance wail;  {"type": "rumble", ...} engine rising toward a crash
  ],
  "events": [     # one-shots
    {"type": "beep", "t": 0.15}, {"type": "thump", "t": 1.0}, {"type": "whoosh", "t": 10.75},
    {"type": "ping", "t": 13.0}, {"type": "paper", "t": 9.0}, {"type": "knock", "t": 59.5},
    {"type": "tick", "t": 80.0}, {"type": "step", "t": 24.0}, {"type": "pop", "t": 74.2},
    {"type": "marker", "t": 102.2}, {"type": "creak", "t": 23.1},
    {"type": "ring"}, {"type": "busy"}, {"type": "click"}, {"type": "stamp"}, {"type": "crash"}   # phone/console/impact
  ]
}
Times may also be written as "@<phrase id>" (phrase start) or "@<phrase id>+0.3".

Mixing rules baked in (learned the hard way — see references/sound_design.md):
 * beds crossfade over ~1–1.5 s and sound may lead the picture (J-cut): set "start" a little early;
 * everything that is not voice (beds AND one-shots) dips by ~35% while the narrator speaks,
   with a soft attack/release so nothing "pumps";
 * one-shots are kept modest; put loud accents in the pauses between phrases;
 * BED: the whole non-voice bus sits 2.5× lower than it used to (author, «112» ep.1: "background hurts the ears");
 * final loudness is normalised to −14 LUFS, true peak −1.5 dB.
"""
import json, wave, sys, os, re, subprocess
import numpy as np
try:
    from scipy.signal import lfilter
    def onepole(x, k): return lfilter([k], [1, -(1 - k)], x)
except ImportError:  # slow fallback
    def onepole(x, k):
        y = np.empty_like(x); acc = 0.
        for i in range(len(x)): acc += k * (x[i] - acc); y[i] = acc
        return y

SR = 48000
DUCK = 0.35          # how much non-voice sound dips under speech (0.30–0.40 sounds right)
BED = 0.55 / 2.5    # background level vs voice: author asked for 2.5× quieter beds and effects (they hurt the ears)

def main(cfg_path, out):
    cfg = json.load(open(cfg_path)); TL = json.load(open(os.path.join(out, 'timeline.json')))
    P = TL['ph']; total = TL['total']; N = int(total * SR); t = np.arange(N) / SR; rng = np.random.default_rng(7)

    def T(v):
        if isinstance(v, (int, float)): return float(v)
        m = re.match(r'@([\w.]+)([+-][0-9.]+)?$', v); return P[m.group(1)]['s'] + float(m.group(2) or 0)

    def seg(a, b, fi, fo):
        r1 = np.clip((t - (a - fi / 2)) / fi, 0, 1); r2 = np.clip(((b + fo / 2) - t) / fo, 0, 1)
        return r1 * r1 * (3 - 2 * r1) * r2 * r2 * (3 - 2 * r2)

    w = rng.standard_normal(N); hi, lo = onepole(w, .07), onepole(w, .012)
    gust = .55 + .45 * np.sin(t * .7) * np.sin(t * .23 + 1) + .2 * np.sin(t * 2.3)
    bus = np.zeros(N)
    def add(at, sig, gain=1.):
        i = int(at * SR); n = min(len(sig), N - i)
        if n > 0 and i >= 0: bus[i:i+n] += sig[:n] * gain
    def tone(f, d, decay=0., att=.004):
        tt = np.arange(int(d * SR)) / SR; return np.sin(2*np.pi*f*tt) * np.minimum(1, tt/att) * np.exp(-tt*decay)
    def noise(d, k=.2, decay=10.):
        n = int(d * SR); return onepole(rng.standard_normal(n), k) * np.exp(-np.arange(n) / SR * decay)
    def thump(d=.7, f0=46):
        tt = np.arange(int(d * SR)) / SR; return np.sin(2*np.pi*(f0 + 40*np.exp(-tt*18))*tt) * np.exp(-tt*5)

    for b in cfg.get('ambience', []):
        a, e, g = T(b['start']), T(b['end']), b.get('gain', 1.)
        env = seg(a, e, b.get('fade_in', 1.2), b.get('fade_out', 1.2)) * g; ty = b['type']
        if ty in ('wind', 'storm'):
            k = 1.9 if ty == 'storm' else 1.0
            # the whistle (highs) leaves faster than the body — reads like a door closing
            env_hi = seg(a, e, b.get('fade_in', 1.2), b.get('fade_out', 1.2) * .6) * g
            bus += (hi * .5 * env_hi + lo * 1.5 * env) * gust * k
        elif ty == 'room':
            bus += lo * gust * env * .55
            for c in rng.uniform(a, e, max(1, int((e - a) * 1.3))):
                add(c, rng.standard_normal(int(.006*SR)) * np.exp(-np.arange(int(.006*SR)) / 70), .2 * g)
        elif ty == 'hum':
            hz = b.get('hz', 50); bus += (np.sin(2*np.pi*hz*t)*.5 + np.sin(4*np.pi*hz*t)*.3 + np.sin(6*np.pi*hz*t)*.15) * env * .09
        elif ty == 'drone':
            bus += (np.sin(2*np.pi*55*t) + .5*np.sin(2*np.pi*82.4*t) + .25*np.sin(2*np.pi*110.3*t)) * env * .08
        elif ty == 'office':
            fan = onepole(w, .02) * 1.2; bus += (fan + (np.sin(2*np.pi*50*t)*.5 + np.sin(2*np.pi*100*t)*.25) * .06) * env * .55
        elif ty == 'line':
            band = hi - onepole(hi, .02); bus += band * env * 1.4
            for c in rng.uniform(a, e, max(1, int((e - a) * 3))):
                add(c, rng.standard_normal(int(.004*SR)) * np.exp(-np.arange(int(.004*SR)) / 40), .25 * g)
        elif ty == 'fire':      # burning room behind a door / in the receiver: low roar + dry crackle pops ("rate" pops per second)
            bus += lo * 1.1 * env * (.8 + .2 * np.sin(t * 3.1))
            for c in rng.uniform(a, e, max(1, int((e - a) * b.get('rate', 9)))):
                n = int(rng.uniform(.002, .009) * SR); add(c, rng.standard_normal(n) * np.exp(-np.arange(n) / (n / 4)), rng.uniform(.08, .35) * g)
        elif ty == 'siren':
            f = 750 + 280*np.sin(2*np.pi*.35*t); ph = np.cumsum(2*np.pi*f/SR); bus += onepole(np.sin(ph), .08) * env * .12
        elif ty == 'rumble':
            ramp = np.clip((t - a) / max(.1, e - a), 0, 1) ** 2; bus += onepole(w, .004) * 6 * ramp * env
        elif ty == 'rotor':
            bus += (.5 + .5*np.sign(np.sin(2*np.pi*4.6*t))) * onepole(w, .05) * 3 * np.sin(np.clip((t-a)/(e-a), 0, 1)*np.pi) * env * .5

    for ev in cfg.get('events', []):
        at, g, ty = T(ev['t']), ev.get('gain', 1.), ev['type']
        if ty == 'beep':
            s = tone(1150, .13) + .25*tone(2300, .13); s *= np.minimum(1, (.13 - np.arange(len(s))/SR)/.006); add(at, s, .35*g)
        elif ty == 'ring':
            n = int(.42*SR); tt = np.arange(n)/SR; f = np.where(np.sin(2*np.pi*22*tt) > 0, 1020, 1280)
            sig = np.sin(np.cumsum(2*np.pi*f/SR)) * np.minimum(1, tt/.01) * np.minimum(1, (.42-tt)/.02); add(at, sig, .22*g)
        elif ty == 'busy': s = tone(425, .35); s *= np.minimum(1, (.35 - np.arange(len(s))/SR)/.01); add(at, s, .22*g)
        elif ty == 'click': add(at, noise(.015, .7, 300), .5*g); add(at, tone(2400, .01), .1*g)
        elif ty == 'stamp': add(at, thump(.35, 70), .7*g); add(at, noise(.05, .3, 60), .4*g)
        elif ty == 'crash':
            add(at, thump(1.2, 38), 1.2*g); add(at, noise(1.0, .3, 4), 1.0*g)
            for k in range(26): add(at + .05 + rng.uniform(0, .9), tone(rng.uniform(2500, 6000), .12, 40), .05*g)
        elif ty == 'thump': add(at, thump(), .6*g)
        elif ty == 'whoosh':
            n = int(.5*SR); add(at, onepole(rng.standard_normal(n), .15) * np.sin(np.pi*np.arange(n)/n)**2, 1.1*g)
        elif ty == 'ping': add(at, tone(740, 1.2, 4), .13*g)
        elif ty == 'paper': add(at, noise(.05, .5, 80), .2*g)
        elif ty == 'knock': add(at, noise(.08, .25, 60), .55*g); add(at, thump(.15, 120), .35*g)
        elif ty == 'tick': add(at, noise(.02, .6, 200), .3*g)
        elif ty == 'step': add(at, noise(.09, .35, 40), .3*g)
        elif ty == 'pop': add(at, noise(.15, .5, 25), .55*g); add(at, tone(180, .08, 40), .4*g)
        elif ty == 'marker': add(at, noise(.4, .6, 6) * .5, .22*g)
        elif ty == 'creak':
            n = int(.9*SR); add(at, noise(.9, .02, 2) * np.sin(2*np.pi*np.linspace(90, 60, n)*np.arange(n)/SR), .45*g)

    vw = wave.open(os.path.join(out, 'voice.wav')); v = np.frombuffer(vw.readframes(vw.getnframes()), np.int16).astype(np.float64) / 32767
    v = np.pad(v, (0, max(0, N - len(v))))[:N]
    # speech envelope -> smooth ducking curve (fast-ish attack, slow release, small look-ahead)
    lvl = onepole(np.abs(v), .002); speech = np.clip(lvl / (np.percentile(lvl[lvl > 1e-4], 60) + 1e-9), 0, 1)
    look = int(.12 * SR); speech = np.concatenate([speech[look:], np.zeros(look)])
    rel = onepole(speech, 1 / (.4 * SR)); duck = 1 - DUCK * np.clip(np.maximum(speech, rel), 0, 1)
    mix = v + bus * BED * duck
    tmp = os.path.join(out, '_mix_raw.wav')
    with wave.open(tmp, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(mix * .7, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ac', '2', '-ar', str(SR),
                    os.path.join(out, 'mix.wav')], check=True)
    os.remove(tmp); print('mix.wav ready', total)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '.')
