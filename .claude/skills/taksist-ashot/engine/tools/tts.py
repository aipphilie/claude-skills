# python3 tools/tts.py tools/lines.json public/voice/
# ELEVENLABS_API_KEY задан -> ElevenLabs (голоса из VOICES_11), иначе edge-tts (ru-RU-DmitryNeural с разным тоном)
# Уже готовые mp3 не перегенерируются (экономим символы). Перегенерировать реплику: удалить её mp3.
# Скорость Ашота: EL_SPEED_ASHOT (по умолчанию 1.1, решение автора 1.1–1.15).
import json, os, sys, ssl, asyncio, subprocess, time, urllib.request
lines = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
EDGE = {  # голос, скорость, высота
  "ashot":           ("ru-RU-DmitryNeural", "+12%", "-14Hz"),
  "passenger":       ("ru-RU-DmitryNeural", "+28%", "+22Hz"),
  "passenger_shock": ("ru-RU-DmitryNeural", "+15%", "+50Hz"),
}
# id голосов из ElevenLabs (аккаунт автора, Voice Design): Ашот и Тимур (пассажир серии «Ипотека»)
VOICES_11 = {"ashot": os.environ.get("EL_ASHOT", "aiETsjwAyUVKjNepebct"), "passenger": os.environ.get("EL_PASS", "Inof0Um2Sd8Y9OYSblWu")}
SPEED = {"ashot": float(os.environ.get("EL_SPEED_ASHOT", "1.1")), "passenger": 1.05}
def edge(text, who, dst):
    import edge_tts.communicate as c
    c._SSL_CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
    v, r, p = EDGE[who]; text = text.replace("́", "")
    for i in range(15):
        try:
            asyncio.run(c.Communicate(text, v, rate=r, pitch=p).save(dst))
            if os.path.getsize(dst) > 1000: return
        except Exception as e: print("retry", i, e)
        time.sleep(1.5)
    raise SystemExit("tts failed: " + text)
def eleven(text, who, dst):
    k = "ashot" if who == "ashot" else "passenger"
    body = json.dumps({"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": SPEED[k]}}).encode()
    vid = VOICES_11[k]
    rq = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}", body,
        {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    open(dst, "wb").write(urllib.request.urlopen(rq).read())
for L in lines:
    mp3 = f"{out}/{L['id']}.mp3"; wav = f"{out}/{L['id']}.wav"
    if not (os.path.exists(mp3) and os.path.getsize(mp3) > 1000):
        (eleven if os.environ.get("ELEVENLABS_API_KEY") else edge)(L["text"], L["who"], mp3)
    # обрезать тишину по краям, 48 кГц моно
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-42dB:stop_silence=0.18",
        "-ar", "48000", "-ac", "1", wav], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]))
    print(L["id"], round(d, 2), L["text"])
