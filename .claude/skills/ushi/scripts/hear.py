"""Уши для Claude: PANNs (AudioSet, 527 классов) слушает звук и говорит словами, что в нём.

  python3 hear.py FILE                      # что звучит во всём файле (топ-10 тегов)
  python3 hear.py FILE --timeline           # + что звучит в каждом окне (по умолчанию 0.5 с)
  python3 hear.py FILE --at 1.2 3.5 6.7     # что слышно в эти секунды (±0.25 с)
  python3 hear.py FILE --cues audio/cues.json   # проверить каждый cue из mix.py:
                                            #   есть ли в эту секунду всплеск и какой звук там слышен
  python3 hear.py FILE --png audio/hear.png # картинка: волна + тепловая карта классов во времени

FILE — любой wav/mp3/mp4 (звук достаётся через ffmpeg).
Ставится один раз: bash .claude/skills/ushi/scripts/setup.sh
Модели лежат в ~/panns_data (Cnn14 для тегов, Cnn14_DecisionLevelMax для событий по времени).
"""
import argparse, json, os, subprocess, sys
import numpy as np

SR = 32000
HOME = os.path.expanduser("~/panns_data")
TAG_CKPT = os.path.join(HOME, "Cnn14_mAP=0.431.pth")
SED_CKPT = os.path.join(HOME, "Cnn14_DecisionLevelMax_mAP=0.385.pth")
FPS_SED = 100  # PANNs SED даёт 100 кадров в секунду


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def quiet():
    """panns_inference печатает служебные строки в stdout: глушим их."""
    return open(os.devnull, "w")


def tagger():
    import contextlib
    from panns_inference import AudioTagging
    with contextlib.redirect_stdout(quiet()):
        return AudioTagging(checkpoint_path=TAG_CKPT, device="cpu")


def detector():
    import contextlib
    from panns_inference import SoundEventDetection
    with contextlib.redirect_stdout(quiet()):
        return SoundEventDetection(checkpoint_path=SED_CKPT, device="cpu")


def labels():
    from panns_inference.config import labels as L
    return L


def top(probs, n=5, floor=0.05):
    L = labels()
    idx = np.argsort(probs)[::-1][:n]
    return [(L[i], float(probs[i])) for i in idx if probs[i] >= floor]


def fmt(tags):
    return ", ".join(f"{name} {p:.2f}" for name, p in tags) or "— тишина / ничего уверенного"


def rms_db(y):
    return max(-90.0, 20 * np.log10(np.sqrt(np.mean(y * y)) + 1e-9)) if len(y) else -90.0


def window_tags(at, y, t0, t1, n=5):
    a, b = max(0, int(t0 * SR)), min(len(y), int(t1 * SR))
    seg = y[a:b]
    if len(seg) < SR // 2:          # Cnn14 нужно хотя бы ~0.5 с: дополняем тишиной по центру
        pad = SR // 2 - len(seg); seg = np.pad(seg, (pad // 2, pad - pad // 2))
    clip, _ = at.inference(seg[None, :])
    return top(clip[0], n), rms_db(y[a:b])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--n", type=int, default=10, help="сколько тегов на весь файл")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--win", type=float, default=0.5, help="окно таймлайна, с")
    ap.add_argument("--at", type=float, nargs="*", help="секунды, которые проверить")
    ap.add_argument("--cues", help="cues.json из mix.py: проверить каждый cue")
    ap.add_argument("--png", help="нарисовать волну и тепловую карту событий")
    ap.add_argument("--json", help="сохранить всё в json")
    a = ap.parse_args()

    y = load(a.file)
    dur = len(y) / SR
    at = tagger()
    out = dict(file=a.file, duration_s=round(dur, 2))

    clip, _ = at.inference(y[None, :])
    out["overall"] = top(clip[0], a.n, 0.02)
    print(f"{a.file}  {dur:.2f} с,  громкость {rms_db(y):.1f} dBFS")
    print("ВЕСЬ ФАЙЛ:", fmt(out["overall"]))

    if a.timeline:
        print(f"\nТАЙМЛАЙН (окно {a.win} с):")
        out["timeline"] = []
        t = 0.0
        while t < dur:
            tags, db = window_tags(at, y, t, min(dur, t + a.win), 3)
            print(f"  {t:6.2f}–{min(dur, t + a.win):6.2f}  {db:6.1f} dB  {fmt(tags)}")
            out["timeline"].append(dict(t=round(t, 2), db=round(db, 1), tags=tags))
            t += a.win

    points = []
    if a.at: points += [(f"{s:.2f}s", s) for s in a.at]
    if a.cues:
        cs = json.load(open(a.cues)); fps = cs.get("fps", 30)
        for c in cs.get("cues", []):
            s = c["t"] if "t" in c else c["frame"] / fps
            points.append((f"{c.get('id', '?')} [{c.get('sound', '')}]", s))
    if points:
        print("\nТОЧКИ (±0.25 с; всплеск = насколько громче, чем 0.5 с до точки):")
        out["points"] = []
        for name, s in points:
            tags, db = window_tags(at, y, s - 0.25, s + 0.25, 3)
            _, before = window_tags(at, y, s - 0.75, s - 0.25, 1)
            jump = db - before
            mark = "OK " if jump >= 3 else "?? "
            print(f"  {mark}{s:6.2f} с  {name:34s} всплеск {jump:+5.1f} dB  слышно: {fmt(tags)}")
            out["points"].append(dict(name=name, t=s, jump_db=round(jump, 1), tags=tags))

    if a.png:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        sed = detector()
        fw = sed.inference(y[None, :])[0]          # (кадры, 527)
        L = labels()
        keep = np.argsort(fw.max(0))[::-1][:12]
        fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw=dict(height_ratios=[1, 2]))
        tt = np.arange(len(y)) / SR
        ax[0].plot(tt, y, lw=0.3, color="k"); ax[0].set_yticks([]); ax[0].set_title(os.path.basename(a.file), loc="left", fontsize=9)
        ax[1].imshow(fw[:, keep].T, aspect="auto", origin="lower", cmap="magma", vmin=0, vmax=1,
                     extent=[0, fw.shape[0] / FPS_SED, -0.5, len(keep) - 0.5])
        ax[1].set_yticks(range(len(keep))); ax[1].set_yticklabels([L[i] for i in keep], fontsize=7)
        for _, s in points:
            for x in ax: x.axvline(s, color="c", lw=0.8)
        ax[1].set_xlabel("секунды"); fig.tight_layout()
        os.makedirs(os.path.dirname(a.png) or ".", exist_ok=True); fig.savefig(a.png, dpi=100)
        print("\nкартинка:", a.png)

    if a.json:
        json.dump(out, open(a.json, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
