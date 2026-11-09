"""Отрывки «Кофе» v4 со стеклом: стеклянная плашка субтитров + стеклянная линза.
Запуск из ne-tupi-render/zvuk-v2 (там align.json):  python3 clips.py [секунда для превью]"""
import sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, '../../ne-tupi-render/kod')]
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import compose as C
from PIL import Image, ImageDraw
from glass import glass, spring, ease

SRC = os.path.join(HERE, '../../ne-tupi-render/kofe-test-v4.mp4')
OUT = os.path.join(HERE, '..')
FPS, WD, HT = 24, 1080, 1920
YEL = (255, 212, 0); INK = (17, 17, 17)
LH = 78; PADX, PADY = 38, 16


def group_at(t):
    gs = C.groups
    for i, g in enumerate(gs):
        end = gs[i + 1][0][1] - 0.05 if i + 1 < len(gs) else g[-1][2] + 0.4
        if g[0][1] - 0.05 <= t < end: return i
    return None


def geom(gi):
    """строки, позиции слов и размер плашки для группы"""
    lines = C.wrap(C.groups[gi]); y = C.SUB_Y - 6 if len(lines) == 1 else C.SUB_Y - 43
    words, mw = [], 0
    for ln in lines:
        ws = [C.wlen(w) for w in ln]; tw = sum(ws) + C.SP * (len(ws) - 1); mw = max(mw, tw); x = (WD - tw) / 2
        for w, wd in zip(ln, ws): words.append((w, x, y, wd)); x += wd + C.SP
        y += LH
    top = words[0][2] - PADY; bot = words[-1][2] + 64 + PADY
    return words, (WD / 2, (top + bot) / 2, mw + 2 * PADX, bot - top)


def subtitle(img, t, t_in):
    gi = group_at(t)
    if gi is None: return img, None
    words, (cx, cy, w, h) = geom(gi)
    g0 = C.groups[gi][0][1] - 0.05
    # плашка: при смене группы размер «перетекает» с перелётом, при первом появлении — желе из точки
    if gi > 0 and group_at(g0 - 0.01) == gi - 1 and g0 > t_in:
        _, (_, pcy, pw, ph) = geom(gi - 1); s = spring(t - g0, 9, 16)
        w = w + (pw - w) * s; h = h + (ph - h) * s; cy = cy + (pcy - cy) * s
    else:
        a = t - max(g0, t_in); sc = 1 - spring(a, 8, 13)
        sq = 0.12 * np.exp(-6 * a) * np.sin(18 * a)
        w *= sc * (1 + sq); h *= sc * (1 - sq)
    glass(img, cx, cy, w, h, r=min(h / 2, 46), zoom=1.04, refr=38, bevel=34, blur=7, tint=0.42, shadow=0.10, spec=0.9)
    # жёлтая «капля»: переползает со слова на слово, передний край быстрее заднего
    lay = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    started = [k for k, (wd, *_) in enumerate(words) if wd[1] <= t]
    if started:
        k = started[-1]; cw = words[k]; pw_ = words[k - 1] if k > 0 else cw
        p = (t - cw[0][1]) / 0.22
        if cw[2] != pw_[2]: pw_ = (pw_[0], cw[1] - 40, cw[2], 0)   # новая строка: вытекает слева
        fwd = cw[1] >= pw_[1]
        ef, es = ease(p * 1.7), ease(p)
        x0 = pw_[1] + (cw[1] - pw_[1]) * (es if fwd else ef)
        x1 = pw_[1] + pw_[3] + (cw[1] + cw[3] - pw_[1] - pw_[3]) * (ef if fwd else es)
        stretch = 1 - 0.18 * np.sin(np.pi * min(max(p, 0), 1))      # в полёте капля тоньше
        yc = cw[2] + 32; hh = 38 * stretch
        if words[0][0][1] - 0.05 <= t: d.rounded_rectangle([x0 - 10, yc - hh, x1 + 10, yc + hh], radius=int(hh), fill=YEL + (245,))
        d.rounded_rectangle([x0 + 4, yc - hh + 5, x1 - 4, yc - hh + 13], radius=4, fill=(255, 255, 255, 110))
    fa = int(255 * min(1, (t - max(C.groups[gi][0][1] - 0.05, t_in)) / 0.1))
    for (wd, x, y, _) in words: d.text((x, y), wd[0].upper().strip('«»'), font=C.SUBF, fill=INK + (fa,))
    return img, lay


# --- линзы по сценам --------------------------------------------------------
def lens_number(img, t):
    """сцена «91 250 ₽ в год»: линза выплёскивается на сумму и увеличивает её"""
    t0 = C.wt('девяносто')
    if t < t0 - 0.1: return
    a = t - (t0 - 0.1); sc = 1 - spring(a, 6, 12); sq = 0.10 * np.exp(-5 * a) * np.sin(16 * a)
    glass(img, 540, 612, 650 * sc * (1 + sq), 250 * sc * (1 - sq), zoom=1.22, refr=46, bevel=44, tint=0.05, shadow=0.14, chroma=0.18)


ROWS = [490, 604, 720, 836, 950]
def lens_rows(img, t):
    """сцена «первые три строчки»: стеклянная линза едет по строкам трат и тянется в движении"""
    keys = [(C.wt('Первые') - 0.15, 0), (C.wt('три', 2), 1), (C.wt('строчки'), 2), (C.wt('настоящий'), 4), (C.wt('кофе»'), 0)]
    if t < keys[0][0]: return
    def pos(tt):
        k = max(i for i, (ts, _) in enumerate(keys) if ts <= tt) if tt >= keys[0][0] else 0
        ts, r = keys[k]; prev = ROWS[keys[k - 1][1]] if k else ROWS[r]
        return ROWS[r] + (prev - ROWS[r]) * spring(tt - ts, 8, 11)
    y = pos(t); v = (pos(t + 1 / FPS) - pos(t - 1 / FPS)) * FPS / 2
    st = min(abs(v) / 2500, 0.45)
    a = t - keys[0][0]; sc = 1 - spring(a, 7, 12)
    glass(img, 680, y, 560 * sc * (1 - 0.12 * st), 104 * sc * (1 + 0.9 * st), zoom=1.16, refr=30, bevel=30, tint=0.04, shadow=0.12, chroma=0.18)


SEGS = [('steklo-1-91tysyacha', 11.8, 17.0, lens_number), ('steklo-2-traty', 46.2, 54.0, lens_rows)]
SUB_ERASE = (1350, 1532)
GLASS_SUBS = False   # Ярослав: субтитры обычные, стекло только для линз на второстепенном


def render(frame, t, t_in, lens):
    img = frame.astype(np.float32)
    if GLASS_SUBS: img[SUB_ERASE[0]:SUB_ERASE[1]] = img[SUB_ERASE[0] - 8:SUB_ERASE[0] - 4, :60].reshape(-1, 3).mean(0)  # убираем старые субтитры
    lens(img, t)
    img, lay = subtitle(img, t, t_in) if GLASS_SUBS else (img, None)
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
    if lay is not None: out.alpha_composite(lay)
    return out.convert('RGB')


def frames(t0, t1):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    i = 0
    while True:
        b = p.stdout.read(WD * HT * 3)
        if len(b) < WD * HT * 3: break
        yield t0 + i / FPS, np.frombuffer(b, np.uint8).reshape(HT, WD, 3); i += 1


if __name__ == '__main__':
    if ARGS:
        for s in ARGS:
            s = float(s); name, t0, t1, lens = next(x for x in SEGS if x[1] <= s < x[2])
            _, f = next(frames(s, s + 0.05)); render(f, s, t0, lens).save(f'/tmp/claude-0/s/prev_{s}.png')
        sys.exit()
    for name, t0, t1, lens in SEGS:
        out = f'{OUT}/{name}.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-ss', str(t0), '-t', str(t1 - t0), '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '19',
                              '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out], stdin=subprocess.PIPE)
        for t, f in frames(t0, t1): p.stdin.write(render(f, t, t0, lens).tobytes())
        p.stdin.close(); p.wait(); print('ok', out)
