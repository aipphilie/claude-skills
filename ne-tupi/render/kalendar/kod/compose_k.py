"""Монтаж «Листок на 66 тысяч» (календарь-копилка). Формат как у присланного рилса: календарь сквозной нитью,
коллаж-карточки «мелко + КРУПНО», триптих, штамп, карточка-кубок. Человечки RGBA с белой «стикерной» обводкой."""
import json, math, sys, random, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from words import W, B, END, DUR
from tm import T
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920
BG = (247, 245, 240); YEL = (255, 214, 10); YEL2 = (240, 180, 0); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (225, 222, 215); MID = (196, 192, 184); BOARD = (24, 24, 26)
L1 = (228, 224, 216); L2 = (205, 200, 191); CARD = (214, 220, 228); DOT = (198, 205, 215)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
@lru_cache(None)
def font(sz): return ImageFont.truetype(FB, int(sz))
ONLY = sys.argv[1:]
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return t * t * (3 - 2 * t)
FEET = 1335; SUB_Y = 1410
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)

# ---------- текст ----------
@lru_cache(None)
def text_img(text, sz, fg, squeeze=0.8, stroke=0, sc=None):
    f = font(sz); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lines = text.split('\n'); bbs = [d0.textbbox((0, 0), l, font=f, stroke_width=stroke) for l in lines]
    lh = int(sz * 1.0); w = max(b[2] - b[0] for b in bbs) + stroke * 2 + 8; h = lh * len(lines) + int(sz * 0.25) + stroke * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, b) in enumerate(zip(lines, bbs)):
        d.text((stroke + 4 - b[0], stroke + i * lh - b[1] + int(sz * 0.05)), l, font=f, fill=fg, stroke_width=stroke, stroke_fill=sc)
    if squeeze != 1: im = im.resize((max(1, int(w * squeeze)), h), Image.LANCZOS)
    return im
def put(img, im, x, y, anchor='lt', scale=1.0, rot=0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    ox = {'l': 0, 'm': im.width / 2, 'r': im.width}[anchor[0]]; oy = {'t': 0, 'm': im.height / 2, 'b': im.height}[anchor[1]]
    img.alpha_composite(im, (int(x - ox), int(y - oy)))
def typed(s, t, t0, cps=22):
    if t < t0: return ''
    return s[:max(1, int((t - t0) * cps) + 1)]
def title(img, t, t0, small, big, x=70, y=270, bsz=190, fg=INK, small_fg=None, typing=True):
    """Заголовок как в оригинале: мелкая строка + ОГРОМНОЕ слово, слово печатается по буквам."""
    if t < t0: return
    a = eo((t - t0) / 0.15)
    s_im = text_img(small, 64, small_fg or fg, 0.82)
    put(img, s_im, x, y + 12 * (1 - a), alpha=a)
    bt = typed(big, t, t0 + 0.12, 26) if typing else big
    if bt:
        put(img, text_img(bt, bsz, fg, 0.78), x - 6, y + 70)
def plate_img(text, sz, bg, fg, pad=26, border=None):
    ti = text_img(text, sz, fg, 0.86)
    w, h = ti.width + pad * 2, ti.height + pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=18, fill=bg, outline=border, width=6 if border else 0)
    im.alpha_composite(ti, (pad, int(pad * 0.45)))
    return im
plate_img = lru_cache(None)(plate_img)
def plate(img, t, t0, text, cx, cy, sz=84, bg=YEL, fg=INK, rot=0, t1=None, border=None):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28); a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    put(img, plate_img(text, sz, bg, fg, border=border), cx, cy, 'mm', sc, rot, a)
def stamp(img, t, t0, text, cx, cy, rot=14, sz=110):
    """Красный штамп, бьёт сверху (масштаб 2.2 → 1)."""
    if t < t0: return
    u = clamp((t - t0) / 0.16); s = 2.2 - 1.2 * eo(u)
    ti = text_img(text, sz, RED, 0.85); w, h = ti.width + 60, ti.height + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w - 7, h - 7], radius=14, outline=RED, width=12)
    im.alpha_composite(ti, (30, 10))
    rnd = np.random.RandomState(3).rand(h, w) > 0.18   # «потёртость» печати
    a = np.array(im.getchannel('A')) * rnd; im.putalpha(Image.fromarray(a.astype(np.uint8)))
    put(img, im, cx, cy, 'mm', s, rot, clamp(u * 3))

# ---------- фоны ----------
def bg_room(img):
    d = ImageDraw.Draw(img)
    d.rectangle([600, 430, 960, 820], fill=L1, outline=L2, width=6); d.line([780, 430, 780, 820], fill=L2, width=5); d.line([600, 625, 960, 625], fill=L2, width=5)
    d.line([80, 560, 400, 560], fill=L2, width=7)
    for j, (h, w) in enumerate(((110, 34), (90, 28), (120, 40), (80, 30))):
        x = 100 + j * 50; d.rectangle([x, 560 - h, x + w, 560], fill=L1, outline=L2, width=4)
    d.ellipse([280, 470, 360, 558], fill=L1, outline=L2, width=4)
    d.line([0, FEET + 8, WD, FEET + 8], fill=L2, width=5)
@lru_cache(None)
def card_bg():
    """Фон карточки как в оригинале: серо-голубой с полутоновыми точками (коллаж)."""
    im = Image.new('RGBA', (WD, HT), CARD + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, HT, 22):
        for x in range((y // 22) % 2 * 11, WD, 22):
            r = 2.2 + 1.6 * (y / HT)
            d.ellipse([x - r, y - r, x + r, y + r], fill=DOT)
    return im
def bg_kitchen(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 960, WD, 990], fill=L1, outline=L2, width=4)   # столешница
    for x in (60, 240): d.rectangle([x, 990, x + 170, FEET + 8], fill=L1, outline=L2, width=4); d.line([x + 70, 1030, x + 100, 1030], fill=L2, width=6)
    for x in (60, 240): d.rectangle([x, 520, x + 170, 760], fill=L1, outline=L2, width=4)
    d.line([0, FEET + 8, WD, FEET + 8], fill=L2, width=5)
FR = (650, 470, 930, FEET)   # холодильник
def fridge(img):
    d = ImageDraw.Draw(img); x0, y0, x1, y1 = FR
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=WHITE, outline=INK, width=7)
    d.line([x0, y0 + 300, x1, y0 + 300], fill=INK, width=6)
    d.rounded_rectangle([x0 + 22, y0 + 90, x0 + 38, y0 + 230], radius=8, fill=INK)
    d.rounded_rectangle([x0 + 22, y0 + 340, x0 + 38, y0 + 520], radius=8, fill=INK)

# ---------- календарь ----------
COLS, ROWS = 19, 20
@lru_cache(None)
def chalk(sz):
    """Жёлтая заливка с фактурой мелка/маркера (вместо розового мелка оригинала)."""
    S = 160; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([6, 6, S - 6, S - 6], fill=YEL)
    rnd = random.Random(7)
    for k in range(26):
        y = 14 + k * 5.0; x0 = 10 + rnd.random() * 18; x1 = S - 10 - rnd.random() * 18
        d.line([x0, y, x1, y + rnd.uniform(-10, 10)], fill=YEL2 if k % 2 else (255, 228, 80), width=2)
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).ellipse([8, 8, S - 8, S - 8], fill=255)
    im.putalpha(Image.composite(im.getchannel('A'), m, m))
    return im.resize((max(1, sz), max(1, sz)), Image.LANCZOS)
def cal_geom(cell, anchor):
    """anchor = (n, px, py): круг n окажется в точке (px, py)."""
    pad = cell * 0.55; head = cell * 1.25
    n, px, py = anchor; c = (n - 1) % COLS; r = (n - 1) // COLS
    bx0 = px - pad - (c + 0.5) * cell; by0 = py - head - (r + 0.5) * cell
    return bx0, by0, pad, head
def cal_center(n, bx0, by0, pad, head, cell):
    c = (n - 1) % COLS; r = (n - 1) // COLS
    return bx0 + pad + (c + 0.5) * cell, by0 + head + (r + 0.5) * cell
def draw_cal(img, cell, anchor, fillf, t, ring=None, flash=None, header=True):
    d = ImageDraw.Draw(img)
    bx0, by0, pad, head = cal_geom(cell, anchor)
    bw = COLS * cell + pad * 2; bh = ROWS * cell + pad * 2 + head
    d.rounded_rectangle([bx0 + cell * 0.12, by0 + cell * 0.18, bx0 + bw + cell * 0.12, by0 + bh + cell * 0.18], radius=cell * 0.4, fill=(200, 196, 188))
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=cell * 0.4, fill=BOARD, outline=WHITE, width=max(2, int(cell * 0.08)))
    if header and cell >= 26:
        d.text((bx0 + bw / 2, by0 + head * 0.55), 'КАЛЕНДАРЬ-КОПИЛКА  ·  66 795 ₽', font=font(int(cell * 0.55)), fill=WHITE, anchor='mm')
    r = cell * 0.4; lw = max(1, int(cell * 0.045)); fs = int(cell * 0.33)
    f = font(fs) if fs >= 7 else None
    for n in range(1, 366):
        x, y = cal_center(n, bx0, by0, pad, head, cell)
        if x < -cell or x > WD + cell or y < -cell or y > HT + cell: continue
        fl = fillf(n, t)
        col = WHITE
        if ring and ring(n, t): col = RED
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=lw if col == WHITE else lw * 2)
        if fl > 0.02:
            s = int(2 * r * 1.04 * back(fl));
            if s > 1: img.alpha_composite(chalk(s), (int(x - s / 2), int(y - s / 2)))
        if flash and flash(n, t):
            d.ellipse([x - r * 0.9, y - r * 0.9, x + r * 0.9, y + r * 0.9], fill=(255, 255, 255))
        if f: d.text((x, y), str(n), font=f, fill=INK if fl > 0.5 or (flash and flash(n, t)) else WHITE, anchor='mm')
    return bx0, by0, pad, head
def fill_at(times):
    """times: dict n -> момент заливки."""
    def f(n, t):
        t0 = times.get(n)
        return 0 if t0 is None or t < t0 else clamp((t - t0) / 0.25)
    return f
rnd = random.Random(11)
PRE = {n for n in range(1, 366) if rnd.random() < 0.42}
PRE -= {162, 161, 160, 159, 158, 157, 47, 1}
def fill_intro(n, t):
    if n in PRE: return 1
    tt = {162: T['listok'] - 0.1, 161: T['shest'] - 0.05, 160: T['tysyach'] - 0.05, 159: B[1] + 0.15, 158: B[1] + 0.5, 157: B[1] + 0.85}.get(n)
    return 0 if tt is None or t < tt else clamp((t - tt) / 0.25)
SPARSE = {n for n in range(1, 366) if random.Random(n * 7).random() < 0.07} - {47, 1, 300}

# ---------- предметы ----------
def suitcase(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img); w, h = 300 * k, 200 * k
    x0, y0 = cx - w / 2, by - h
    # пальма торчит из чемодана
    d.line([cx + 30 * k, y0, cx + 60 * k, y0 - 170 * k], fill=(120, 90, 40), width=int(16 * k))
    for a in (-150, -110, -60, -20, 20):
        rr = math.radians(a); ex, ey = cx + 60 * k + math.cos(rr) * 120 * k, y0 - 170 * k + math.sin(rr) * 70 * k + 30 * k
        d.line([cx + 60 * k, y0 - 170 * k, ex, ey], fill=(40, 170, 80), width=int(22 * k))
    d.rounded_rectangle([cx - 40 * k, y0 - 40 * k, cx + 40 * k, y0 + 10 * k], radius=12 * k, outline=INK, width=int(10 * k))
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=22 * k, fill=YEL, outline=INK, width=int(8 * k))
    for x in (x0 + 70 * k, x0 + w - 70 * k): d.line([x, y0, x, by], fill=INK, width=int(8 * k))
def phone(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img); w, h = 300 * k, 600 * k; x0, y0 = cx - w / 2, by - h
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=46 * k, fill=INK)
    d.rounded_rectangle([x0 + 16 * k, y0 + 16 * k, x0 + w - 16 * k, by - 16 * k], radius=34 * k, fill=YEL)
    d.rounded_rectangle([cx - 50 * k, y0 + 30 * k, cx + 50 * k, y0 + 56 * k], radius=13 * k, fill=INK)
    for j in range(3):
        for i in range(3):
            xx = x0 + 52 * k + i * 76 * k; yy = y0 + 110 * k + j * 90 * k
            d.rounded_rectangle([xx, yy, xx + 52 * k, yy + 52 * k], radius=14 * k, fill=WHITE, outline=INK, width=int(4 * k))
def pillow(img, cx, cy, k=1.0):
    d = ImageDraw.Draw(img); w, h = 640 * k, 200 * k
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=90 * k, fill=WHITE, outline=INK, width=8)
    d.rounded_rectangle([cx - 120 * k, cy - 45 * k, cx + 120 * k, cy + 45 * k], radius=14 * k, fill=YEL, outline=INK, width=5)
    d.text((cx, cy), '5000 ₽', font=font(int(52 * k)), fill=INK, anchor='mm')
def weight(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img); w = 360 * k; h = 260 * k
    d.polygon([(cx - w * 0.36, by - h), (cx + w * 0.36, by - h), (cx + w / 2, by), (cx - w / 2, by)], fill=INK)
    d.rounded_rectangle([cx - 70 * k, by - h - 70 * k, cx + 70 * k, by - h + 10 * k], radius=30 * k, outline=INK, width=int(20 * k))
    d.text((cx, by - h * 0.45), '10 000 ₽', font=font(int(62 * k)), fill=YEL, anchor='mm')
def jar(img, cx, by, n_coins, k=1.0):
    d = ImageDraw.Draw(img); w, h = 210 * k, 260 * k; x0 = cx - w / 2; y0 = by - h
    d.rounded_rectangle([x0 - 6, y0 - 6, x0 + w + 6, by + 6], radius=40 * k, fill=WHITE)
    for j in range(n_coins):
        yy = by - 18 * k - j * 16 * k; d.ellipse([x0 + 30 * k, yy - 14 * k, x0 + w - 30 * k, yy + 10 * k], fill=YEL, outline=INK, width=3)
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=40 * k, outline=INK, width=int(8 * k))
    d.rectangle([x0 + 24 * k, y0 - 30 * k, x0 + w - 24 * k, y0 + 4 * k], fill=YEL, outline=INK, width=int(6 * k))
def coin(img, cx, cy, k=1.0, label=''):
    d = ImageDraw.Draw(img); r = 56 * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YEL, outline=INK, width=6)
    if label: d.text((cx, cy), label, font=font(int(34 * k)), fill=INK, anchor='mm')
def piggy(img, cx, cy, k=1.0, crack=0.0, t=0.0):
    """Свинья-копилка; crack 0..1 — трескается и разлетается (как цепь в оригинале)."""
    d = ImageDraw.Draw(img)
    if crack < 0.35:
        sh = 6 * math.sin(t * 80) * (crack > 0.05)
        x = cx + sh
        d.ellipse([x - 230 * k, cy - 160 * k, x + 230 * k, cy + 160 * k], fill=(255, 190, 200), outline=INK, width=8)
        d.ellipse([x + 170 * k, cy - 50 * k, x + 290 * k, cy + 60 * k], fill=(255, 170, 185), outline=INK, width=8)
        for xx in (x + 215 * k, x + 245 * k): d.ellipse([xx - 9, cy - 12, xx + 9, cy + 12], fill=INK)
        d.polygon([(x - 120 * k, cy - 150 * k), (x - 60 * k, cy - 230 * k), (x - 20 * k, cy - 150 * k)], fill=(255, 170, 185), outline=INK)
        for lx in (x - 140 * k, x + 100 * k): d.rectangle([lx, cy + 140 * k, lx + 50 * k, cy + 220 * k], fill=(255, 170, 185), outline=INK, width=6)
        d.rectangle([x - 60 * k, cy - 168 * k, x + 60 * k, cy - 150 * k], fill=INK)
        if crack > 0.05:
            pts = [(x - 30 * k, cy - 160 * k), (x + 10 * k, cy - 80 * k), (x - 20 * k, cy - 20 * k), (x + 30 * k, cy + 50 * k), (x, cy + 150 * k)]
            d.line(pts[:2 + int(crack / 0.35 * 3)], fill=INK, width=8)
    else:
        u = (crack - 0.35) / 0.65; rr = random.Random(5)
        for j in range(14):
            a = rr.uniform(0, 6.28); sp = rr.uniform(250, 600) * k
            x = cx + math.cos(a) * sp * u; y = cy + math.sin(a) * sp * u * 0.7 + 500 * u * u
            s = rr.uniform(40, 90) * k
            pts = [(x + math.cos(a + q) * s, y + math.sin(a + q) * s * 0.8) for q in (0, 2.1, 4.0)]
            d.polygon(pts, fill=(255, 190, 200), outline=INK)
        for j in range(10):
            a = rr.uniform(0, 6.28); sp = rr.uniform(150, 450) * k
            coin(img, cx + math.cos(a) * sp * u, cy - 200 * u + math.sin(a) * sp * u + 700 * u * u, 0.5 * k, '₽')
def cup(img, cx, by, k=1.0, t=0.0):
    d = ImageDraw.Draw(img); w, h = 300 * k, 300 * k; x0 = cx - w / 2; y0 = by - h
    for j in range(3):
        xs = cx - 70 * k + j * 70 * k
        pts = [(xs + 18 * k * math.sin(t * 5 + q * 0.5 + j), y0 - 30 * k - q * 22 * k) for q in range(7)]
        d.line(pts, fill=GREY, width=int(12 * k))
    d.ellipse([x0 + w - 60 * k, y0 + 60 * k, x0 + w + 80 * k, y0 + 200 * k], outline=INK, width=int(22 * k))
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=60 * k, fill=YEL, outline=INK, width=8)
    d.rectangle([x0, y0, x0 + w, y0 + 60 * k], fill=YEL, outline=INK, width=8)
    d.text((cx, by - h * 0.45), '183 ₽', font=font(int(74 * k)), fill=INK, anchor='mm')
def mini_sheet(img, cx, cy, w, filled_k=0.0, first=0.0, rot=0):
    """Маленький листок-календарь (на холодильнике, в руках на финале)."""
    h = w * 1.12; S = 2
    im = Image.new('RGBA', (int(w * S) + 20, int(h * S) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w * S + 4, h * S + 4], radius=16, fill=BOARD, outline=WHITE, width=8)
    cols, rows = 10, 11; cs = (w * S - 40) / cols
    for j in range(rows):
        for i in range(cols):
            k = j * cols + i; x = 24 + (i + 0.5) * cs; y = 40 + (j + 0.5) * cs; r = cs * 0.38
            on = (k / (rows * cols)) < filled_k or (k == 0 and first > 0)
            d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE, width=3)
            if on:
                s = int(2 * r * (back(first) if k == 0 and filled_k == 0 else 1))
                if s > 1: im.alpha_composite(chalk(s), (int(x - s / 2), int(y - s / 2)))
    im = im.resize((int(im.width / S), int(im.height / S)), Image.LANCZOS)
    put(img, im, cx, cy, 'mm', 1.0, rot)
def building(img, t, z=1.0, focus=(540, 900)):
    """Фасад девятиэтажки с плакатом-календарём. Рисуется в 1x, затем при z>1 приближение к плакату."""
    im = Image.new('RGBA', (WD, HT), BG + (255,)); d = ImageDraw.Draw(im)
    for x, w, h in ((-40, 160, 520), (930, 190, 600)):
        d.rectangle([x, FEET - h, x + w, FEET + 8], fill=L1, outline=L2, width=4)
    bx0, bx1, by0 = 130, 950, 500
    d.rectangle([bx0, by0, bx1, FEET + 8], fill=L1, outline=L2, width=6)
    for r in range(9):
        for c in range(6):
            x = bx0 + 30 + c * 128; y = by0 + 20 + r * 86
            d.rectangle([x, y, x + 60, y + 50], fill=BG, outline=L2, width=3)
    return im, (bx0, bx1, by0)

# ---------- субтитры (числа цифрами) ----------
SUBF = ImageFont.truetype(FB, 56); SP = 14; MAXW = 780
_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
NUMS = [(['шестьдесят', 'шесть', 'тысяч.'], '66 ТЫСЯЧ.'), (['десять', 'тысяч.'], '10 000.'), (['триста', 'шестьдесят', 'пять'], '365'),
        (['триста!'], '300!'), (['шестьдесят', 'шесть', 'тысяч', 'семьсот', 'девяносто', 'пять.'], '66 795 ₽.'),
        (['сто', 'восемьдесят', 'три', 'рубля'], '183 ₽')]
def merge_nums(ws):
    out = []; i = 0
    while i < len(ws):
        for pat, rep in NUMS:
            seg = ws[i:i + len(pat)]
            if len(seg) == len(pat) and all(a[0].lower() == b for a, b in zip(seg, pat)):
                out.append((rep, seg[0][1], seg[-1][2])); i += len(pat); break
        else:
            out.append(ws[i]); i += 1
    return out
WS = merge_nums(W)
def wlen(w): return _d.textbbox((0, 0), w[0].upper().strip('«»'), font=SUBF)[2]
def wrap(ws):
    lines, cur, cw = [], [], 0
    for w in ws:
        l = wlen(w)
        if cur and cw + SP + l > MAXW: lines.append(cur); cur, cw = [], 0
        cw = l if not cur else cw + SP + l; cur.append(w)
    if cur: lines.append(cur)
    return lines
groups, cur = [], []
for w in WS:
    if cur and (len(wrap(cur + [w])) > 2 or len(cur) >= 6): groups.append(cur); cur = []
    cur.append(w)
    if w[0].rstrip('»')[-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 3): groups.append(cur); cur = []
if cur: groups.append(cur)
def subs(img, t, y0=SUB_Y):
    g = next((g for i, g in enumerate(groups) if g[0][1] - 0.05 <= t < (groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else g[-1][2] + 0.4)), None)
    if not g: return
    d = ImageDraw.Draw(img); lines = wrap(g); y = y0 if len(lines) == 1 else y0 - 37
    for ln in lines:
        ws = [wlen(w) for w in ln]; x = (WD - (sum(ws) + SP * (len(ws) - 1))) / 2
        for w, wd in zip(ln, ws):
            on = w[1] <= t < w[2] + 0.15
            d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=YEL if on else WHITE)
            d.text((x, y), w[0].upper().strip('«»'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

# ---------- человечки ----------
CH_CROP = (0, 60, 1080, 1660)
SEGI = json.load(open('seg.json')); SEG = SEGI['seg']; OFF = SEGI['off']
WALK0 = END + 0.75
@lru_cache(maxsize=64)
def sprite_raw(who, j):
    return Image.open(f'kadry/{who}/{j:03d}.png').convert('RGBA').crop(CH_CROP)
def sprite(who, i, s, sticker=True, sq=1.0, rot=0):
    """Возвращает (RGBA, ширина, высота) + точки руки. sticker — белая обводка как у вырезок в оригинале."""
    j = i - OFF[who]; n = len(SEG[who])
    j = max(0, min(n - 1, j))
    im = sprite_raw(who, j)
    cw, chh = max(1, int(1080 * s)), max(1, int(1600 * s * sq))
    im = im.resize((cw, chh), Image.LANCZOS)
    if sticker:
        a = im.getchannel('A'); r = max(3, int(14 * s))
        big = a.filter(ImageFilter.MaxFilter(r * 2 + 1 if r * 2 + 1 <= 31 else 31))
        if r * 2 + 1 > 31: big = big.filter(ImageFilter.MaxFilter(r * 2 + 1 - 30 if (r * 2 + 1 - 30) % 2 else r * 2 - 30))
        st = Image.new('RGBA', im.size, WHITE + (0,)); st.putalpha(big)
        st.alpha_composite(im); im = st
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    return im
def place(img, who, i, cx, s, feet=FEET, **kw):
    im = sprite(who, i, s, **kw)
    if SEG[who][max(0, min(len(SEG[who]) - 1, i - OFF[who]))] == 'walk': cx -= (i - int(round(WALK0 * FPS))) * 22.0
    x0 = int(cx - im.width / 2); y0 = int(feet + 70 * s * kw.get('sq', 1.0) - im.height)
    img.alpha_composite(im, (x0, y0))
    return x0, y0, im
def tips(who, i, s, cx, feet=FEET):
    """Крайняя левая и верхняя точки силуэта (кончик руки) в координатах кадра."""
    j = max(0, min(len(SEG[who]) - 1, i - OFF[who]))
    a = np.array(sprite_raw(who, j).getchannel('A')) > 128
    ys, xs = np.nonzero(a)
    if len(xs) == 0: return (cx, feet), (cx, feet)
    k = np.argmin(xs); left = (xs[k], ys[k]); k2 = np.argmin(ys); top = (xs[k2], ys[k2])
    x0 = cx - 1080 * s / 2; y0 = feet + 70 * s - 1600 * s
    return (x0 + left[0] * s, y0 + left[1] * s), (x0 + top[0] * s, y0 + top[1] * s)

def rtip(who, i, s, cx, feet=FEET):
    j = max(0, min(len(SEG[who]) - 1, i - OFF[who]))
    a = np.array(sprite_raw(who, j).getchannel('A')) > 128
    a[:, :540] = False
    ys, xs = np.nonzero(a); k = np.argmin(ys - 0.0 * xs) if len(xs) else 0
    # кончик правой руки: самая верхняя точка правее головы
    ys2, xs2 = ys[xs > 600], xs[xs > 600]
    if len(xs2): k = np.argmin(ys2); px, py = xs2[k], ys2[k]
    else: px, py = 540, 800
    x0 = cx - 1080 * s / 2; y0 = feet + 70 * s - 1600 * s
    return (x0 + px * s, y0 + py * s)

# ---------- сцены ----------
def zoom_of(t):
    for ta, dur, amp in ((T['shest'], 0.6, 0.07), (T['mozg'], 0.8, 0.06), (T['trista2'], 0.9, 0.08), (T['pyat'] + 0.2, 0.7, 0.06), (T['brosish'], 0.6, 0.05)):
        if ta <= t < ta + dur: return 1 + amp * (1 - eo((t - ta) / dur))
    return 1.0
def shake(t):
    for ta in (T['trista2'], T['pyat'] + 0.2, T['desyat'] + 0.35):
        if ta <= t < ta + 0.25: u = (t - ta) / 0.25; return int(14 * (1 - u) * math.sin(t * 160)), int(10 * (1 - u) * math.cos(t * 140))
    return 0, 0

def shade(img):
    """Тёмная подложка под заголовком поверх календаря."""
    a = np.zeros((HT, WD), np.uint8); ys = np.arange(HT)
    col = np.clip(np.where(ys < 560, 225, 225 - (ys - 560) * 2.2), 0, 225).astype(np.uint8)
    a[:] = col[:, None]; sh = Image.new('RGBA', (WD, HT), BOARD + (0,)); sh.putalpha(Image.fromarray(a)); img.alpha_composite(sh)
def cal_scene(img, i, t, cell, anchor_n, fillf, cx=770, s=0.52, title_fn=None, **kw):
    """Календарь крупно: человечек справа «закрашивает» круг anchor_n кончиком левой руки."""
    who = 'main'
    j0 = OFF[who]
    left, _ = tips(who, int(round(B[line_of(t)] * FPS)) + 2, s, cx)
    draw_cal(img, cell, (anchor_n, left[0] - cell * 0.15, left[1]), fillf, t, **kw)
    if title_fn: title_fn(img)
    place(img, who, i, cx, s)

def frame(i):
    t = i / FPS; L = line_of(t)
    img = Image.new('RGBA', (WD, HT), BG + (255,))
    sub_y = SUB_Y
    if L == 0:
        img.paste(BOARD, [0, 0, WD, HT])
        cal_scene(img, i, t, 128, 162, fill_intro); shade(img)
        if t >= T['listok'] - 0.1:
            title(img, t, T['listok'] - 0.1, 'ЭТОТ ЛИСТОК НАКОПИТ', '', fg=WHITE, y=262)
            if t >= T['shest'] - 0.1:
                put(img, text_img(typed('66 795 ₽', t, T['shest'] - 0.1, 18), 200, YEL, 0.78, 6, INK), 64, 332)
    elif L == 1:
        img.paste(BOARD, [0, 0, WD, HT])
        cal_scene(img, i, t, 175, 159, fill_intro)
        plate(img, t, T['zametish'] - 0.1, 'НЕ ЗАМЕТИШЬ', 380, 330, 80, YEL, INK, rot=-3)
    elif L in (2, 3, 4):
        img.alpha_composite(card_bg())
        if L == 2:
            title(img, t, B[2], 'НАКОПИТЬ НА', 'МОРЕ')
            _, top = tips('main', i, 0.46, 540)
            k = back((t - B[2]) / 0.3)
            place(img, 'main', i, 540, 0.46)
            if k > 0.05: suitcase(img, top[0], top[1] + 10, 0.95 * k)
        elif L == 3:
            title(img, t, B[3], 'НА НОВЫЙ', 'ТЕЛЕФОН')
            k = back((t - B[3]) / 0.3)
            if k > 0.05: phone(img, 360, FEET + 10 - 30 * (1 - k), k)
            place(img, 'main', i, 730, 0.46)
        else:
            title(img, t, B[4], 'НА', 'ПОДУШКУ')
            pillow(img, 540, 1180, 1.0)
            im = sprite('main', i, 0.4, rot=-90); bb = im.getbbox()
            img.alpha_composite(im, (int(560 - (bb[0] + bb[2]) / 2), int(1100 - bb[3])))
            d = ImageDraw.Draw(img)
            for q in range(3):
                u = ((t - B[4]) * 0.9 + q / 3) % 1
                d.text((330 - 60 * u + q * 10, 960 - 260 * u), 'Z', font=font(int(60 + 50 * u)), fill=INK + (int(255 * (1 - u)),))
    elif L == 5:   # триптих: три полосы, как «бросали всё на полпути» в оригинале
        img.paste(WHITE, [0, 0, WD, HT])
        bands = [(250, 625), (633, 1008), (1016, 1391)]
        starts = [B[5], T['kopit'] + 0.25, T['pyatnice'] - 0.25]
        for b, ((y0, y1), st) in enumerate(zip(bands, starts)):
            if t < st: continue
            u = eo((t - st) / 0.25)
            band = Image.new('RGBA', (WD, y1 - y0), (BG if b != 1 else (240, 238, 232)) + (255,)); d = ImageDraw.Draw(band)
            hb = y1 - y0; ft = hb - 30
            d.line([0, ft + 4, WD, ft + 4], fill=L2, width=4)
            if b == 0:
                d.rounded_rectangle([90, 40, 470, 300], radius=14, fill=WHITE, outline=INK, width=5)
                for k2, dn in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ']):
                    d.text((130 + k2 * 72, 90), dn, font=font(30), fill=INK, anchor='mm')
                d.ellipse([92, 55, 168, 125], outline=RED, width=6)
                d.text((280, 210), 'НАЧИНАЮ\nКОПИТЬ!', font=font(46), fill=INK, anchor='mm', align='center')
            elif b == 1:
                for q in range(9):
                    v = ((t - st) * 1.3 + q * 0.13) % 1
                    x = 640 + q * 40 + 360 * v; y = ft - 150 - 320 * v + 40 * math.sin(q + t * 6)
                    d.rounded_rectangle([x - 50, y - 26, x + 50, y + 26], radius=6, fill=YEL, outline=INK, width=4)
                    d.text((x, y), '₽', font=font(32), fill=INK, anchor='mm')
                d.rounded_rectangle([110, ft - 170, 330, ft], radius=10, fill=L1, outline=L2, width=5)
                d.text((220, ft - 120), 'СКИДКИ', font=font(36), fill=L2, anchor='mm')
            else:
                d.rectangle([520, ft - 150, 1000, ft - 125], fill=L1, outline=L2, width=4)
                for x in (560, 960): d.line([x, ft - 125, x, ft], fill=L2, width=6)
                d.rounded_rectangle([110, 40, 330, 180], radius=14, fill=INK)
                d.text((220, 110), 'ПТ', font=font(80), fill=WHITE, anchor='mm')
            who = ['t1', 't2', 't3'][b]
            cxs = [740, 470, 700][b]
            im = sprite(who, i, 0.215)
            band.alpha_composite(im, (int(cxs - im.width / 2), int(ft + 70 * 0.215 - im.height)))
            img.alpha_composite(band, (int(-WD * (1 - u)) if b % 2 == 0 else int(WD * (1 - u)), y0))
        stamp(img, t, T['vsyo1'] - 0.05, 'ВСЁ.', 760, 1210, rot=-10, sz=150)
    elif L == 6:
        bg_room(img)
        place(img, 'main', i, 540, 0.46)
        plate(img, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 420, 96, YEL, INK, rot=-3)
    elif L == 7:
        bg_room(img)
        hit = T['desyat'] + 0.35
        sq = 1.0
        if t >= hit:
            u = (t - hit); sq = 0.68 + 0.05 * math.exp(-u * 6) * math.cos(u * 30)
        x0, y0, im = place(img, 'main', i, 540, 0.46, sq=sq)
        if t >= T['desyat'] - 0.15:
            fall = clamp((t - T['desyat'] + 0.15) / 0.5)
            _, hd = tips('main', i, 0.46, 540); hy = FEET - (FEET - hd[1]) * sq
            topy = hy + 32 if t >= hit else -300 + (FEET - 0.46 * 1500 + 300) * fall * fall
            weight(img, 540, topy, 1.0)
        plate(img, t, B[7] + 0.1, 'СРАЗУ 10 000 ₽?', 540, 330, 76, INK, WHITE, rot=-2, t1=T['mozg'] - 0.1)
        plate(img, t, T['mozg'] - 0.05, 'МОЗГ: НЕ ТЯНЕТ', 540, 330, 88, YEL, INK, rot=3)
    elif L == 8:
        if t < T['kalendar'] - 0.05:
            img.alpha_composite(card_bg())
            title(img, t, B[8], 'НАС ЭТОМУ', 'НЕ УЧИЛИ')
            place(img, 'main', i, 560, 0.46)
            plate(img, t, T['priyom'] - 0.1, 'НО ЕСТЬ ПРИЁМ', 560, 720, 70, INK, WHITE, rot=-3)
        else:
            img.paste(BG, [0, 0, WD, HT])
            k = back((t - T['kalendar'] + 0.05) / 0.35)
            draw_cal(img, 40, (181, 510, 922 + 500 * (1 - k)), lambda n, tt: 1 if n in SPARSE else 0, t)
            title(img, t, T['kalendar'] - 0.05, 'ПРИЁМ НАЗЫВАЕТСЯ', '«КАЛЕНДАРЬ-КОПИЛКА»', bsz=86, x=60, y=255)
            place(img, 'main', i, 930, 0.3)
    elif L == 9:
        img.paste(BG, [0, 0, WD, HT])
        u = eio((t - B[9]) / 0.9); cell = 150 + (40 - 150) * u
        fl = lambda n, tt: 1 if n in SPARSE else 0
        flash = lambda n, tt: tt >= T['kazhdom'] - 0.1 and (n * 37 + int(tt * 12) * 11) % 23 == 0
        draw_cal(img, cell, (181, 510, 922), fl, t, flash=flash)
        plate(img, t, T['trista'] - 0.05, '365 КРУЖКОВ', 470, 290, 84, YEL, INK, rot=-3)
        place(img, 'main', i, 920, 0.30)
    elif L == 10:
        img.paste(BOARD, [0, 0, WD, HT])
        times = {n: 0 for n in SPARSE}; times[47] = T['lyuboy'] - 0.05
        cal_scene(img, i, t, 160, 47, fill_at(times))
        if t >= T['otkladyvaesh']:
            u = eo((t - T['otkladyvaesh']) / 0.5)
            jar(img, 230, 1290, 3 + (1 if u >= 1 else 0))
            if u < 1: coin(img, 430 + (230 - 430) * u, 760 + (1080 - 760) * u - 220 * math.sin(u * 3.14), 1.0, '47 ₽')
        else: jar(img, 230, 1290, 3)
        shade(img); title(img, t, T['lyuboy'] - 0.1, 'ЗАКРАСЬ', 'ЛЮБОЙ', fg=WHITE, y=262, bsz=170)
        if t >= T['rubley'] - 0.1: plate(img, t, T['rubley'] - 0.1, '47 → 47 ₽', 700, 520, 76, YEL, INK, rot=3)
    elif L == 11:
        img.paste(BOARD, [0, 0, WD, HT])
        times = {n: 0 for n in SPARSE}; times[1] = T['zakras1'] + 0.15
        cal_scene(img, i, t, 190, 1, fill_at(times))
        shade(img); title(img, t, T['deneg'] - 0.05, 'ДЕНЕГ НЕТ?', 'ЕДИНИЧКА', fg=WHITE, y=262, bsz=170)
        plate(img, t, T['byvaet'] - 0.05, 'БЫВАЕТ', 420, 1150, 80, LG, INK, rot=-4)
    elif L == 12:   # «ебанутый» отъезд: листок = плакат на всю девятиэтажку, сварщик красит валиком
        bim, (bx0, bx1, by0) = building(img, t)
        cell = 25
        px0 = 540 - (COLS * cell + cell * 1.1) / 2; py0 = by0 + 90
        c300 = cal_center(300, px0, py0, cell * 0.55, cell * 1.25, cell)
        hit = T['trista2'] - 0.05
        def fl(n, tt):
            if n in SPARSE: return 1
            c = (n - 1) % COLS; r = (n - 1) // COLS
            if tt >= hit and c in (13, 14, 15) and 6 <= r <= 15: return clamp((tt - hit - (15 - r) * 0.04) / 0.2)
            return 0
        draw_cal(bim, cell, (300, c300[0], c300[1]), fl, t)
        d = ImageDraw.Draw(bim)
        # люлька на тросах
        cy = c300[1] + 70 + 60 * math.sin(clamp((t - B[12]) / 1.5) * 1.2)
        crx = c300[0] - 10
        for x in (crx - 95, crx + 95): d.line([x, by0 - 400, x, cy], fill=INK, width=4)
        d.rectangle([crx - 115, cy, crx + 115, cy + 22], fill=YEL, outline=INK, width=5)
        d.line([crx - 115, cy - 50, crx + 115, cy - 50], fill=INK, width=5)
        for x in (crx - 115, crx + 115): d.line([x, cy - 50, x, cy], fill=INK, width=5)
        s = 0.15
        x0, y0, im = place(bim, 'svar', i, crx + 40, s, feet=cy + 2, sticker=False)
        top = rtip('svar', i, s, crx + 40, feet=cy + 2)
        rx, ry = top[0] + 10, top[1] - 55   # валик на палке
        d.line([top[0], top[1], rx, ry], fill=WHITE, width=10); d.line([top[0], top[1], rx, ry], fill=INK, width=5)
        d.rounded_rectangle([rx - 40, ry - 14, rx + 40, ry + 14], radius=10, fill=YEL, outline=WHITE, width=4)
        place(bim, 'main', i, 250, 0.14, sticker=False)
        z = 1 + 5.0 * (1 - eio((t - B[12]) / 0.55))
        if z > 1.001:
            fx, fy = c300
            w, h = WD / z, HT / z; x0c = clamp(fx - w / 2, 0, WD - w); y0c = clamp(fy - h / 2, 0, HT - h)
            bim = bim.crop((int(x0c), int(y0c), int(x0c + w), int(y0c + h))).resize((WD, HT), Image.BILINEAR)
        img = bim
        if t >= B[12] + 0.35: title(img, t, B[12] + 0.35, 'ПРИШЛА ЗАРПЛАТА?', 'ЗАКРАСЬ 300' if t >= T['trista2'] - 0.5 else '', y=262, bsz=150, typing=False)
        if t >= hit: put(img, text_img('300!', 190, YEL, 0.8, 8, INK), 830, 640, 'mm', back((t - hit) / 0.3), 8)
    elif L == 13:
        bg_room(img)
        place(img, 'main', i, 540, 0.46)
        plate(img, t, T['podvoh'] - 0.45, 'А ВОТ И ПОДВОХ', 540, 420, 100, YEL, INK, rot=-3)
    elif L == 14:
        if t < T['brosish'] - 0.15:
            img.paste(BG, [0, 0, WD, HT])
            def fl(n, tt):
                if n > 280: return 0
                return clamp((tt - B[14] - 0.15 - n * 0.0045) / 0.2)
            ring = lambda n, tt: n > 280 and tt >= T['dekabre'] - 0.1 and int(tt * 6) % 2 == 0
            draw_cal(img, 40, (181, 510, 922), fl, t, ring=ring)
            if t < T['dekabre'] - 0.1: plate(img, t, B[14] + 0.1, 'ТОЛЬКО МАЛЕНЬКИЕ', 510, 290, 76, INK, WHITE, rot=-2)
            else: plate(img, t, T['dekabre'] - 0.1, 'В ДЕКАБРЕ: 281–365', 510, 290, 76, RED, WHITE, rot=2)
            place(img, 'main', i, 930, 0.28)
        else:
            img.alpha_composite(card_bg())
            title(img, t, T['brosish'] - 0.15, 'КОПИЛКА', 'РАЗБИТА', typing=False)
            piggy(img, 540, 860, 1.0, clamp((t - T['brosish'] + 0.15) / 0.7), t)
            place(img, 'main', i, 800, 0.32)
    elif L == 15:
        img.alpha_composite(card_bg())
        title(img, t, B[15], 'ПРАВИЛО: ЗАРПЛАТА =', 'САМЫЙ\nБОЛЬШОЙ', bsz=170)
        _, top = tips('main', i, 0.4, 600)
        place(img, 'main', i, 600, 0.4)
        k = back((t - T['samyy'] + 0.3) / 0.35)
        if k > 0.05:
            r = 150 * k; x, y = top[0], top[1] - r + 20
            img.alpha_composite(chalk(int(2 * r)), (int(x - r), int(y - r)))
            ImageDraw.Draw(img).ellipse([x - r, y - r, x + r, y + r], outline=INK, width=8)
            ImageDraw.Draw(img).text((x, y), '365', font=font(int(110 * k)), fill=INK, anchor='mm')
    elif L in (16, 17):
        img.paste(WHITE, [0, 0, WD, HT])
        d = ImageDraw.Draw(img)
        if L == 16:
            s = typed('1 + 2 + 3 + … + 365 =', t, T['slozhi'] - 0.1, 16)
            put(img, text_img(s, 92, INK, 0.82), 540, 560, 'mm')
            for q in range(12):   # мелькающие числа
                if t > T['chisla']:
                    rr = random.Random(q + int(t * 10)); d.text((rr.randint(80, 900), rr.randint(700, 1000)), str(rr.randint(1, 365)), font=font(54), fill=LG)
            place(img, 'main', i, 820, 0.34)
        else:
            put(img, text_img('1 + 2 + 3 + … + 365 =', 92, GREY, 0.82), 540, 470, 'mm')
            u = eio((t - T['summa']) / (T['pyat'] - T['summa'] + 0.2)); v = int(66795 * u)
            put(img, text_img(f'{v:,}'.replace(',', ' ') + ' ₽', 220, INK, 0.78), 540, 720, 'mm')
            stamp(img, t, T['pyat'] + 0.2, 'ПОСЧИТАНО', 600, 760, rot=12)
            place(img, 'main', i, 820, 0.34)
    elif L == 18:
        img.alpha_composite(card_bg())
        if t < T['sto'] - 0.1:
            title(img, t, B[18], 'И ВОТ', 'ЦЕНА ВОПРОСА', bsz=150)
            place(img, 'main', i, 560, 0.42)
        elif t < T['odna'] - 0.1:
            put(img, text_img('66 795 ₽ ÷ 365 =', 90, GREY, 0.82), 540, 380, 'mm')
            k = back((t - T['sto'] + 0.1) / 0.3)
            put(img, text_img('183 ₽', 260, INK, 0.8), 540, 590, 'mm', k)
            plate(img, t, T['den'] - 0.1, 'В ДЕНЬ', 760, 760, 70, YEL, INK, rot=4)
            place(img, 'main', i, 820, 0.34)
        else:
            title(img, t, T['odna'] - 0.1, 'ЭТО ОДНА', 'ЧАШКА КОФЕ', bsz=150, typing=False)
            k = back((t - T['odna'] + 0.1) / 0.35)
            if k > 0.05: cup(img, 360, FEET, 1.15 * k, t)
            place(img, 'main', i, 790, 0.42)
    elif L == 19 or (L == 20 and t < T['pervyy'] + 0.45):
        bg_kitchen(img); fridge(img)
        u = eo((t - T['raspechatay'] - 0.25) / 0.4)
        first = clamp((t - T['pervyy'] + 0.1) / 0.25)
        if u > 0: mini_sheet(img, 790, 700 - 500 * (1 - u), 200, 0.0, first, rot=-3)
        d = ImageDraw.Draw(img)
        if t >= T['holodilnik'] - 0.1: d.ellipse([775, 590, 805, 620], fill=RED, outline=INK, width=3)
        place(img, 'main', i, 470, 0.44)
        if L == 19: plate(img, t, T['raspechatay'] - 0.05, 'РАСПЕЧАТАЙ', 470, 330, 84, INK, WHITE, rot=-3)
        else: plate(img, t, T['zakras_perv'] - 0.05, 'ЗАКРАСЬ ПЕРВЫЙ', 470, 330, 84, YEL, INK, rot=3)
    else:   # финальная карточка (их «кубок») + «Всё. Не тупи.»
        img.alpha_composite(card_bg())
        t0 = T['pervyy'] + 0.45
        d = ImageDraw.Draw(img)
        for q in range(16):   # лучи
            a = q * math.pi / 8 + t * 0.6
            d.polygon([(540, 900), (540 + math.cos(a) * 1300, 900 + math.sin(a) * 1300), (540 + math.cos(a + 0.12) * 1300, 900 + math.sin(a + 0.12) * 1300)], fill=(232, 236, 241))
        title(img, t, t0, 'ЛИСТОК, КОТОРЫЙ ЕСТЬ У ТЕХ, КТО', 'НАКОПИЛ', typing=True)
        _, top = tips('main', i, 0.42, 540)
        place(img, 'main', i, 540, 0.42)
        fk = clamp((t - t0) / 0.9)
        mini_sheet(img, top[0], top[1] - 115, 220, fk)
        if t >= T['netupi'] - 0.75:
            plate(img, t, T['netupi'] - 0.75, 'ВСЁ.\nНЕ ТУПИ', 540, 700, 120, YEL, INK, rot=-4)
    subs(img, t, sub_y)
    img = img.convert('RGB')
    z = zoom_of(t); dx, dy = shake(t)
    if z != 1 or dx or dy:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5) + dx, int((h - HT) * 0.47) + dy
        im3 = Image.new('RGB', (WD, HT), BG); im3.paste(im2, (-ox, -oy)); img = im3
    return img

if __name__ == '__main__':
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        import os
        part, parts = int(os.environ.get('PART', 0)), int(os.environ.get('PARTS', 1))
        a, b = N * part // parts, N * (part + 1) // parts
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', f'part{part}.mp4' if parts > 1 else 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        for i in range(a, b):
            p.stdin.write(frame(i).tobytes())
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
