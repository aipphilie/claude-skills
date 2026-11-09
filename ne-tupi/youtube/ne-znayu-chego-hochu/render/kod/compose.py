"""Монтаж 16:9: фон + графика шота (PIL 2x) + персонаж (multiply) + субтитры под персонажем."""
import json, sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import gfx
from gfx import WD, HT, SS, BG, YEL, INK, WHITE, eo, S
from tl import W, DUR, N, FPS, GAPS, O, TITLES, NCH, wt
from scenes import SHOTS
xoff = json.load(open('xoff.json'))
SIDE_X = {'L': 420, 'R': 1500, 'C': 960}; GFX_X = {'L': 1250, 'R': 670, 'C': 960}; GFX_Y = 470
FEET = 880; CROP = (0, 40, 720, 1107); FEET_IN_CROP = 1020
STARTS = [sh['t'] for sh in SHOTS]
import bisect
def shot_idx(t): return max(0, bisect.bisect_right(STARTS, t) - 1)
def chapter_of(t): return max(i for i in range(NCH) if O[i] - 1.7 <= t or i == 0)
def in_gap(t):
    for k, (g0, g1) in enumerate(GAPS):
        if g0 <= t < g1: return k + 1, g0, g1
    return None

def layout(t):
    k = shot_idx(t); cur = SHOTS[k]
    c = (SIDE_X[cur['side']], cur['s'])
    if k == 0: return c
    p = SHOTS[k - 1]; e = eo((t - cur['t']) / 0.5)
    return tuple(a + (b - a) * e for a, b in zip((SIDE_X[p['side']], p['s']), c))

def graphics(t):
    G = Image.new('RGBA', (WD * SS, HT * SS), (0, 0, 0, 0))
    g = in_gap(t)
    k = shot_idx(t); sh = SHOTS[k]; gx = GFX_X[sh['side']]
    if not g or t >= g[1] - 0.05:
        for kind, ta, te, kw in sh['els']:
            kw = dict(kw)
            for a in ('x', 'x0', 'x1'):
                if a in kw: kw[a] += gx
            for a in ('y', 'y0', 'y1'):
                if a in kw: kw[a] += GFX_Y
            gfx.ELS[kind](G, t, ta, te, **kw)
    ch = chapter_of(t)
    if 1 <= ch <= 8 and not g: gfx.badge(G, f'ГЛАВА {ch}', TITLES[ch])
    if g and g[0] <= 8: gfx.chapter_card(G, t, g[1] - 1.6, g[2], g[0], TITLES[g[0]])
    if g and g[0] == 9: gfx.chapter_card(G, t, g[1] - 1.6, g[2], 'ИТОГ', 'План на сегодня') if False else None
    return G.reduce(SS)

# ---- субтитры: до 2 строк, под персонажем ----
SUBF = ImageFont.truetype(gfx.FB, 46); SP = 12; MAXW = 820
_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
def clean(w): return w.upper().strip('«»')
def wlen(w): return _d.textbbox((0, 0), clean(w[0]), font=SUBF)[2]
def wrap(ws):
    lines, cur, cw = [], [], 0
    for w in ws:
        l = wlen(w)
        if cur and cw + SP + l > MAXW: lines.append(cur); cur, cw = [], 0
        cw = l if not cur else cw + SP + l; cur.append(w)
    if cur: lines.append(cur)
    return lines
groups, cur = [], []
for w in W:
    if cur and (len(wrap(cur + [w])) > 2 or len(cur) >= 8 or w[3] != cur[-1][3]): groups.append(cur); cur = []
    cur.append(w)
    if w[0][-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 4): groups.append(cur); cur = []
if cur: groups.append(cur)
GST = [g[0][1] - 0.05 for g in groups]
def subs(img, t, cx):
    i = bisect.bisect_right(GST, t) - 1
    if i < 0: return
    g = groups[i]; tend = GST[i + 1] if i + 1 < len(groups) else g[-1][2] + 0.4
    if t >= min(tend, g[-1][2] + 0.6): return
    d = ImageDraw.Draw(img); lines = wrap(g)
    widths = [sum(wlen(w) for w in ln) + SP * (len(ln) - 1) for ln in lines]
    cx = max(max(widths) / 2 + 30, min(WD - max(widths) / 2 - 30, cx))
    y = 930
    hb = 64 * len(lines)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle([cx - max(widths) / 2 - 22, y - 14, cx + max(widths) / 2 + 22, y + hb + 4], radius=18, fill=BG + (225,))
    img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
    for ln, lw in zip(lines, widths):
        x = cx - lw / 2
        for w in ln:
            wd = wlen(w)
            if w[1] <= t < w[2] + 0.12: d.rounded_rectangle([x - 8, y - 5, x + wd + 8, y + 58], radius=10, fill=YEL)
            d.text((x, y), clean(w[0]), font=SUBF, fill=INK); x += wd + SP
        y += 64

TPOL = wt(0, 'Тебе') - 0.2
KADRY = os.environ.get('KADRY', 'kadry')
def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    if t < TPOL + 0.5:   # вечер: приглушённый синеватый фон, светлеет к «Тебе тридцать»
        ov = Image.new('RGB', (WD, HT), (70, 82, 120))
        bg = Image.blend(bg, ov, 0.22 * (1 - eo((t - TPOL) / 0.5)))
    cx, s = layout(t)
    G = graphics(t); bg.paste(G, (0, 0), G)
    subs(bg, t, cx)
    cw, chh = int(720 * s), int(1067 * s)
    fp = f'{KADRY}/{i:05d}.png'
    if not os.path.exists(fp): fp = f'{KADRY}/00000.png'
    ch = Image.open(fp).convert('RGB').crop(CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), WHITE)
    layer.paste(ch, (int(cx - cw / 2 + xoff[i]), int(FEET - FEET_IN_CROP * s)))
    out = (np.asarray(bg, np.uint16) * np.asarray(layer, np.uint16) // 255).astype(np.uint8)
    return Image.fromarray(out)

if __name__ == '__main__':
    if sys.argv[1] == 'prev':
        for s in sys.argv[2:]: frame(int(float(s) * FPS)).save(f'prev2/p_{float(s):07.2f}.png')
    else:
        a, b = int(sys.argv[1]), min(int(sys.argv[2]), N); outf = sys.argv[3]
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', outf], stdin=subprocess.PIPE)
        for i in range(a, b):
            p.stdin.write(frame(i).tobytes())
            if i % 500 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
