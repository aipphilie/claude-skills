# python3 tools/assemble.py tools/lines.json public/voice src/timeline.json public/voice.wav
# Раскладывает реплики подряд с паузой GAP, пишет общий голос, тайминги слов (ASR) и амплитуду по кадрам для липсинка.
import json, sys, re, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
FPS, SR, GAP, LEAD, TAIL = 30, 48000, 0.12, 0.35, 0.9
GAPS = {"p2": 0.18, "a2": 0.45}       # доп. пауза перед репликой (шок держим чуть дольше)
lines = json.load(open(sys.argv[1])); vdir = sys.argv[2]
try:
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
except Exception as e:
    print("no ASR, слова по длине", e); asr = None
t = LEAD; clips = []; out_lines = []
for L in lines:
    t += GAPS.get(L["id"], 0)
    sr, x = wavfile.read(f"{vdir}/{L['id']}.wav"); x = x.astype(np.float32) / 32768
    dur = len(x) / SR
    words = [w for w in re.sub(r"\[[a-z -]+\]", "", L["text"]).replace("́", "").split()]
    timing = None
    if asr:
        segs, _ = asr.transcribe(resample_poly(x, 1, 3).astype(np.float32), language="ru", word_timestamps=True, vad_filter=False)
        aw = [w for s in segs for w in s.words]
        if len(aw) == len(words): timing = [(w.start, w.end) for w in aw]
        elif aw:  # другое число слов: растянуть по длине букв между началом и концом речи
            a0, a1 = aw[0].start, aw[-1].end
    if timing is None:
        a0, a1 = (a0, a1) if asr and aw else (0.0, dur)
        n = np.array([len(w) + 2 for w in words], float); c = np.concatenate([[0], np.cumsum(n)]) / n.sum()
        timing = [(a0 + (a1 - a0) * c[i], a0 + (a1 - a0) * c[i + 1]) for i in range(len(words))]
    out_lines.append({"id": L["id"], "who": L["who"].split("_")[0], "start": round(t, 3), "end": round(t + dur, 3),
        "words": [{"w": w, "s": round(t + s, 3), "e": round(t + e, 3)} for w, (s, e) in zip(words, timing)]})
    clips.append((t, x)); t += dur + GAP
total = t + TAIL; N = int(total * SR); voice = np.zeros(N, np.float32)
amp = {"ashot": np.zeros(int(total * FPS) + 1), "passenger": np.zeros(int(total * FPS) + 1)}
for (t0, x), L in zip(clips, out_lines):
    i = int(t0 * SR); voice[i:i + len(x)] += x
    hop = SR // FPS
    for k in range(len(x) // hop):
        f = int(t0 * FPS) + k
        if f < len(amp[L["who"]]): amp[L["who"]][f] = np.sqrt(np.mean(x[k * hop:(k + 1) * hop] ** 2))
for k in amp:
    a = amp[k]; m = np.percentile(a[a > 0], 95) if (a > 0).any() else 1
    amp[k] = [round(float(min(1, v / m)), 3) for v in a]
wavfile.write(sys.argv[4], SR, (voice / max(1e-6, np.abs(voice).max()) * 0.9 * 32767).astype(np.int16))
json.dump({"fps": FPS, "total": round(total, 3), "frames": int(np.ceil(total * FPS)), "lines": out_lines, "amp": amp},
          open(sys.argv[3], "w"), ensure_ascii=False)
for L in out_lines: print(L["id"], L["start"], L["end"], " ".join(f"{w['w']}@{w['s']}" for w in L["words"]))
print("total", round(total, 2))
