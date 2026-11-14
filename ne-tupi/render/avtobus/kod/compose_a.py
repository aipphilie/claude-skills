"""СДВГ-монтаж «Зарплаты в автобусе» (движок из odin/compose_o.py): чёрный кадр, заголовок, белая карточка-сцена, субтитр под ней.
Склейка каждые 1–1,5 сек, на каждой: зум-удар / свип с размытием / тряска / вспышка / RGB-сдвиг.
python3 compose_o.py 1.5 12.3 ...  -> превью prev_*.png;  python3 compose_o.py sheet -> лист всех сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
import json, math, sys, subprocess, random, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from words import W, END, wt
FPS = 30; DUR = round(END + 2.2, 2); N = int(DUR * FPS); WD, HT = 1080, 1920
CW, CH, CY0 = 1080, 720, 540            # карточка
FEET = 640
BLK = (12, 12, 12); CARD = (250, 249, 246); YEL = (255, 214, 10); RED = (228, 44, 52); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (226, 223, 216); MID = (190, 186, 178); PINK = (255, 79, 139); HRT = (232, 52, 74); BRAIN = (255, 140, 165)
BOXC = (214, 170, 110); BOXD = (170, 126, 72); STEEL = (120, 126, 136); STEEL2 = (78, 84, 94)
HERE = os.path.dirname(os.path.abspath(__file__))
FO = os.path.join(HERE, 'fonts', 'Oswald-Bold.ttf')
CLIPS = {k: len(v) for k, v in json.load(open(os.path.join(HERE, 'clips.json'))).items()}
@lru_cache(None)
def font(sz): return ImageFont.truetype(FO, int(sz))
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def ei(t): t = clamp(t); return t ** 3
def eio(t): t = clamp(t); return t * t * (3 - 2 * t)
def lerp(a, b, k): return a + (b - a) * k
s_ = math.sin
def T(sub, k=0):
    sub = sub.strip('«».,!?:…'); hits = [w for w in W if w[0].strip('«».,!?:…') == sub]
    return hits[k][1]

# ---------- базовые рисовалки ----------
FB_ = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; ALT = set('₽→✓')
@lru_cache(None)
def font2(sz): return ImageFont.truetype(FB_, int(sz))
def runs(l):
    out = []
    for ch in l:
        a = ch in ALT
        if out and out[-1][1] == a: out[-1][0] += ch
        else: out.append([ch, a])
    return out
def line_w(d0, l, sz, sw):
    return sum(d0.textlength(r, font=font2(sz * 0.8) if a else font(sz)) for r, a in runs(l)) + sw * 2
@lru_cache(4000)
def text_img(text, sz, fill=INK, stroke=None, sw=0, sp=0):
    f = font(sz); lines = text.split('\n'); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    ws = [line_w(d0, l, sz, sw) for l in lines]
    lh = int(sz * 1.12); w = int(max(ws)) + 8 + sw * 2; h = lh * len(lines) + int(sz * 0.4) + sw * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, lw) in enumerate(zip(lines, ws)):
        x = (w - lw) / 2 + sw
        for r, a in runs(l):
            ff = font2(sz * 0.8) if a else f
            d.text((x, i * lh + sw + (sz * 0.33 if a else 0)), r, font=ff, fill=fill, stroke_width=sw, stroke_fill=stroke); x += d.textlength(r, font=ff)
    return im.crop(im.getbbox())
def put(C, im, cx, cy, scale=1.0, rot=0, alpha=1.0):
    if scale <= 0.02 or alpha <= 0.02: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    C.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def txt(C, text, cx, cy, sz=90, fill=INK, scale=1.0, rot=0, alpha=1.0, stroke=None, sw=0):
    put(C, text_img(text, sz, fill, stroke, sw), cx, cy, scale, rot, alpha)
def slam(C, u, text, cx, cy, sz=90, fill=INK, rot=0, stroke=None, sw=0, d=0.16):
    """текст влетает из 2.6x в 1x с отскоком"""
    if u < 0: return
    k = u / d; sc = 1 + 1.6 * (1 - eo(k)) if k < 1 else 1 + 0.05 * math.exp(-(k - 1) * 3) * math.cos((k - 1) * 9)
    txt(C, text, cx, cy, sz, fill, sc, rot, clamp(k * 3), stroke, sw)
def pop(C, u, text, cx, cy, sz=90, fill=INK, rot=0, d=0.22, stroke=None, sw=0):
    if u < 0: return
    txt(C, text, cx, cy, sz, fill, back(u / d), rot, 1, stroke, sw)
@lru_cache(2000)
def plate_img(text, sz, bg=YEL, fg=INK, pad=22, r=14, border=None, bw=6):
    t = text_img(text, sz, fg); w, h = t.width + pad * 2, t.height + int(pad * 1.5)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=bg, outline=border, width=bw if border else 0)
    im.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2)); return im
def plate(C, u, text, cx, cy, sz=70, bg=YEL, fg=INK, rot=0, mode='slam', border=None):
    if u < 0: return
    k = u / 0.16
    sc = (1 + 1.6 * (1 - eo(k)) if k < 1 else 1) if mode == 'slam' else back(u / 0.22)
    put(C, plate_img(text, sz, bg, fg, border=border), cx, cy, sc, rot, clamp(k * 3))
def stamp(C, u, text, cx, cy, sz=80, col=RED, rot=-12):
    if u < 0: return
    t = text_img(text, sz, col); w, h = t.width + 50, t.height + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10, outline=col, width=10); d.rounded_rectangle([14, 14, w - 15, h - 15], radius=6, outline=col, width=3)
    im.alpha_composite(t, (25, 20)); k = u / 0.12
    put(C, im, cx, cy, 1 + 2.2 * (1 - eo(k)), rot, clamp(k * 2.5))
def strike(C, u, x0, y0, x1, y1, col=RED, w=14, d=0.14):
    if u <= 0: return
    k = eo(u / d); ImageDraw.Draw(C).line([x0, y0, lerp(x0, x1, k), lerp(y0, y1, k)], fill=col, width=w)
def xcross(C, u, cx, cy, r, col=RED, w=16):
    strike(C, u, cx - r, cy - r * 0.6, cx + r, cy + r * 0.6, col, w); strike(C, u - 0.08, cx + r, cy - r * 0.6, cx - r, cy + r * 0.6, col, w)
def speedlines(C, cx, cy, u, n=46, r0=260, col=INK, seed=1):
    d = ImageDraw.Draw(C); rnd = random.Random(seed + int(u * 15))
    for j in range(n):
        a = j / n * 2 * math.pi + rnd.random() * 0.1; rr = r0 * (0.85 + rnd.random() * 0.5); wd = 0.012 + rnd.random() * 0.03
        d.polygon([(cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.7), (cx + math.cos(a - wd) * 1500, cy + math.sin(a - wd) * 1500), (cx + math.cos(a + wd) * 1500, cy + math.sin(a + wd) * 1500)], fill=col)
def burst(C, cx, cy, r, u=0, n=14, fill=YEL, outline=INK, seed=3):
    rnd = random.Random(seed); pts = []
    for j in range(n * 2):
        a = j / (n * 2) * 2 * math.pi + u * 0.6; rr = r * (1.0 + rnd.random() * 0.25) if j % 2 == 0 else r * 0.62
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.8))
    ImageDraw.Draw(C).polygon(pts, fill=fill, outline=outline, width=6)
def heart(C, cx, cy, r, col=HRT, rot=0, crack=0, bite=0):
    im = Image.new('RGBA', (int(r * 2.4), int(r * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = []; c = r * 1.2
    for j in range(70):
        a = j / 70 * 2 * math.pi; x = 16 * math.sin(a) ** 3; y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((c + x * r / 16, c - y * r / 16))
    d.polygon(pts, fill=col); d.ellipse([c - r * 0.62, c - r * 0.6, c - r * 0.3, c - r * 0.3], fill=(255, 150, 160))
    if bite: d.polygon([(c + r * 0.15, c - r * 0.1), (c + r * 1.2, c - r * 0.9), (c + r * 1.2, c + r * 0.6), (c + r * 0.45, c + r * 0.5), (c + r * 0.6, c + r * 0.2)], fill=(0, 0, 0, 0))
    if crack > 0:
        zz = [(c, c - r * 0.55), (c - r * 0.2, c - r * 0.2), (c + r * 0.15, c), (c - r * 0.12, c + r * 0.3), (c + r * 0.05, c + r * 0.62), (c, c + r * 0.95)]
        m = max(2, int(len(zz) * clamp(crack))); d.line(zz[:m], fill=CARD, width=max(4, int(r * 0.1)), joint='curve')
    put(C, im, cx, cy, 1, rot)
def box(C, cx, by, w, h, label=None, rot=0, tape=True, sz=30):
    im = Image.new('RGBA', (int(w + 12), int(h + 12)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([4, 4, w + 4, h + 4], fill=BOXC, outline=INK, width=6)
    if tape: d.rectangle([4 + w * 0.42, 4, 4 + w * 0.58, h + 4], fill=(236, 212, 160)); d.rectangle([4, 4, w + 4, 4 + h * 0.16], fill=BOXD, outline=INK, width=5)
    if label:
        t = plate_img(label, sz, WHITE, INK, pad=8, r=4, border=INK, bw=4); im.alpha_composite(t, (int(4 + w / 2 - t.width / 2), int(4 + h * 0.56 - t.height / 2)))
    put(C, im, cx, by - h / 2, 1, rot)
def hole(C, cx, cy, rx, ry=None):
    ry = ry or rx * 0.22; ImageDraw.Draw(C).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=INK)
def ground(C, y=FEET + 6, x0=0, x1=CW, col=LG): ImageDraw.Draw(C).line([x0, y, x1, y], fill=col, width=6)
def gremlin(C, cx, cy, r, u, label=None, seed=0):
    d = ImageDraw.Draw(C); j = s_(u * 22 + seed) * r * 0.06; cy = cy + j
    pts = []
    for q in range(22):
        a = q / 22 * 2 * math.pi; rr = r * (1.25 if q % 2 == 0 else 0.92); pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=INK)
    d.polygon([(cx - r * 0.75, cy - r * 0.6), (cx - r * 1.1, cy - r * 1.7), (cx - r * 0.25, cy - r * 0.95)], fill=INK); d.polygon([(cx + r * 0.75, cy - r * 0.6), (cx + r * 1.1, cy - r * 1.7), (cx + r * 0.25, cy - r * 0.95)], fill=INK)
    m = [(cx - r * 0.55, cy + r * 0.05)] + [(cx - r * 0.55 + q * r * 0.22, cy + r * (0.42 if q % 2 else 0.1)) for q in range(1, 5)] + [(cx + r * 0.55, cy + r * 0.05)]
    d.polygon(m + [(cx + r * 0.4, cy + r * 0.55), (cx - r * 0.4, cy + r * 0.55)], fill=WHITE)
    for sd in (-1, 1):
        d.line([cx + sd * r * 0.9, cy + r * 0.2, cx + sd * r * 1.6, cy - r * 0.5 + s_(u * 18 + seed) * r * 0.4], fill=INK, width=max(5, int(r * 0.16)))
        d.line([cx + sd * r * 0.4, cy + r * 0.9, cx + sd * r * 0.6, cy + r * 1.5], fill=INK, width=max(5, int(r * 0.16)))
    if label: put(C, plate_img(label, max(20, int(r * 0.5)), YEL, INK, pad=8, r=6), cx, cy + r * 1.95)
def brain(C, cx, cy, r, u, angry=True, sign=None):
    d = ImageDraw.Draw(C); b = s_(u * 20) * r * 0.05
    for sd in (-1, 1):   # ручки и ножки
        d.line([cx + sd * r * 0.9, cy, cx + sd * r * 1.65, cy - r * (0.9 + 0.25 * s_(u * 16 + sd))], fill=INK, width=int(r * 0.13))
        d.line([cx + sd * r * 0.4, cy + r * 0.7, cx + sd * r * 0.5, cy + r * 1.25], fill=INK, width=int(r * 0.13))
    for (ox, oy, rr) in [(-0.55, -0.2, 0.62), (0.55, -0.2, 0.62), (0, -0.45, 0.66), (-0.5, 0.3, 0.55), (0.5, 0.3, 0.55), (0, 0.25, 0.6)]:
        d.ellipse([cx + (ox - rr) * r, cy + b + (oy - rr) * r, cx + (ox + rr) * r, cy + b + (oy + rr) * r], fill=BRAIN, outline=INK, width=5)
    for (ox, oy, rr) in [(-0.55, -0.2, 0.55), (0.55, -0.2, 0.55), (0, -0.45, 0.6), (-0.5, 0.3, 0.48), (0.5, 0.3, 0.48), (0, 0.25, 0.55)]:
        d.ellipse([cx + (ox - rr) * r, cy + b + (oy - rr) * r, cx + (ox + rr) * r, cy + b + (oy + rr) * r], fill=BRAIN)
    for (ox, oy, a0) in [(-0.55, -0.35, 200), (0.5, -0.4, 300), (-0.1, -0.7, 240), (0.6, 0.25, 20), (-0.65, 0.3, 120)]:
        d.arc([cx + (ox - 0.3) * r, cy + b + (oy - 0.3) * r, cx + (ox + 0.3) * r, cy + b + (oy + 0.3) * r], a0, a0 + 170, fill=(215, 90, 120), width=max(3, int(r * 0.06)))
    d.line([cx, cy + b - r * 0.95, cx, cy + b - r * 0.1], fill=(215, 90, 120), width=max(3, int(r * 0.05)))
    mo = 0.22 + 0.12 * abs(s_(u * 24))
    d.ellipse([cx - r * 0.3, cy + b + r * 0.12, cx + r * 0.3, cy + b + r * (0.12 + mo * 2)], fill=INK)
    d.rectangle([cx - r * 0.2, cy + b + r * 0.14, cx + r * 0.2, cy + b + r * 0.24], fill=WHITE)
    # фуражка с мигалкой
    d.pieslice([cx - r * 0.75, cy + b - r * 1.75, cx + r * 0.75, cy + b - r * 0.55], 180, 360, fill=INK)
    d.rounded_rectangle([cx - r * 0.95, cy + b - r * 1.2, cx + r * 0.95, cy + b - r * 1.02], radius=6, fill=INK)
    on = int(u * 10) % 2 == 0
    d.rounded_rectangle([cx - r * 0.16, cy + b - r * 2.05, cx + r * 0.16, cy + b - r * 1.7], radius=8, fill=RED if on else YEL, outline=INK, width=4)
    if on:
        for a in (-150, -90, -30): d.line([cx + math.cos(math.radians(a)) * r * 0.35, cy + b - r * 1.9 + math.sin(math.radians(a)) * r * 0.35, cx + math.cos(math.radians(a)) * r * 0.6, cy + b - r * 1.9 + math.sin(math.radians(a)) * r * 0.6], fill=RED, width=6)
    if sign:
        sx, sy = cx + r * 1.7, cy - r * 1.3
        d.line([sx, sy, sx, cy - r * 0.2], fill=INK, width=int(r * 0.1)); put(C, plate_img(sign, int(r * 0.55), RED, WHITE, pad=10, r=8, border=INK, bw=5), sx, sy - r * 0.2, 1, 8 * s_(u * 14))
def tape(C, u, text, cy, h=110, rot=-4):
    """жёлто-чёрная лента на всю ширину"""
    if u < 0: return
    im = Image.new('RGBA', (1500, h), YEL + (255,)); d = ImageDraw.Draw(im)
    for x in range(-200, 1700, 90): d.polygon([(x, 0), (x + 45, 0), (x + 45 - h, h), (x - h, h)], fill=INK)
    t = plate_img(text, int(h * 0.62), INK, YEL, pad=18, r=0); im.alpha_composite(t, (750 - t.width // 2, (h - t.height) // 2))
    k = eo(u / 0.14); put(C, im, lerp(-900, 540, k), cy, 1, rot)
def bubble(C, cx, cy, w, h, u, fill=INK):
    d = ImageDraw.Draw(C); d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h * 0.3, fill=fill)
    d.polygon([(cx - w * 0.25, cy + h * 0.45), (cx - w * 0.36, cy + h * 0.85), (cx - w * 0.02, cy + h * 0.45)], fill=fill)
    for j in range(3):
        k = 0.5 + 0.5 * s_(u * 12 - j * 1.2); r = h * 0.1 * (0.8 + 0.5 * k)
        d.ellipse([cx + (j - 1) * w * 0.22 - r, cy - r - k * h * 0.08, cx + (j - 1) * w * 0.22 + r, cy + r - k * h * 0.08], fill=WHITE)

# ---------- человечек ----------
CROP = (140, 200, 940, 1660); FY = 1412      # ноги в кропе
@lru_cache(300)
def _frame(clip, i): return Image.open(f'{HERE}/kadry/{clip}/{i:03d}.png').convert('RGBA').crop(CROP)
@lru_cache(3000)
def _scaled(clip, i, w, h, flip):
    im = _frame(clip, i).resize((w, h), Image.LANCZOS if w < 640 else Image.BICUBIC)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
def man(C, clip, u, cx, feet=FEET, s=0.36, flip=False, rot=0, alpha=1.0, frame=None, sx=1.0, sy=1.0):
    n = CLIPS[clip]; i = frame if frame is not None else int(max(0, u) * 24) % n
    w, h = int(800 * s * sx), int(1460 * s * sy)
    if w < 2 or h < 2: return
    im = _scaled(clip, i, w, h, flip)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    if rot:
        big = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0)); big.alpha_composite(im, (w // 2, int(h - FY * s * sy)))   # центр вращения = ступни
        big = big.rotate(rot, Image.BICUBIC); C.alpha_composite(big, (int(cx - w), int(feet - h)))
    else: C.alpha_composite(im, (int(cx - w / 2), int(feet - FY * s * sy)))
HEAD = lambda s: 1040 * s      # высота макушки над ступнями (примерно)


# ================= СЦЕНЫ «Зарплаты в автобусе» =================  fn(C, u, t): u — время от начала сцены, t — абсолютное
GREEN = (40, 170, 90); GOLD = (255, 196, 0); BUSW = (255, 255, 255)
def num(v): return f'{int(round(v)):,}'.replace(',', ' ')
def roll(u, a, b, d=0.6): return lerp(a, b, eo(u / d))
def src(C, text, y=CH - 26, x=None):   # мелкая подпись-источник внизу карточки
    put(C, text_img(text, 26, GREY), x or 500, y)

# ---- фигурки-человечки для очереди и горы ----
def fig(d, x, y, w, col):
    h = w * 2.3; r = w * 0.45
    d.ellipse([x - r, y - h, x + r, y - h + 2 * r], fill=col)
    d.rounded_rectangle([x - w / 2, y - h + 2 * r + max(1, w * 0.12), x + w / 2, y], radius=max(1, int(w * 0.38)), fill=col)
MU, SG = math.log(73871), 0.646          # логнормаль под Росстат-2025: медиана 73 871, доля >100 тыс. ≈ 32%
def pdf(v): return 0 if v <= 0 else math.exp(-(math.log(v) - MU) ** 2 / (2 * SG * SG)) / v
PEAK = pdf(math.exp(MU - SG * SG))
X0, X1, AX = 70, 900, 600                # ось x на карточке, y оси
def columns(xmax, fw, hmax):
    """список колонок (x, value, count) — гора по логнормали + редкий хвост до 1 млн+"""
    out = []; n = int((X1 - X0) / (fw + 2))
    for j in range(n):
        x = X0 + j * (fw + 2) + fw / 2; v = xmax * (x - X0) / (X1 - X0)
        c = int(round(hmax * pdf(v) / PEAK))
        if c == 0 and v > 200_000:   # хвост: изредка по одному-два, до самого конца
            c = 1 if (j * 7919) % 5 < (3 if v < 500_000 else 2) else 0
        out.append((x, v, c))
    return out
COL300 = columns(300_000, 8, 24); COL1M = columns(1_050_000, 6, 40)
def xval(v, xmax): return X0 + (X1 - X0) * v / xmax
def mountain(C, u, xmax=300_000, rule='all', grow=0.0, axis=True, ticks=(100_000,), alpha_right=None):
    d = ImageDraw.Draw(C); cols = COL300 if xmax == 300_000 else COL1M; fw = 8 if xmax == 300_000 else 6; fh = fw * 2.3 + 1
    for j, (x, v, c) in enumerate(cols):
        k = 1 if grow <= 0 else eo((u - j * grow * 0.012) / grow)
        m = int(round(c * k))
        if rule == 'lt100': col = INK if v < 100_000 else MID
        elif rule == 'gt1m': col = YEL if v >= 950_000 else (LG if v < 950_000 else INK)
        elif rule == 'tail': col = MID if v < 250_000 else INK
        else: col = INK
        for q in range(m): fig(d, x, AX - 2 - q * fh, fw, col)
        if rule == 'gt1m' and v >= 950_000 and c:
            for q in range(m): d.ellipse([x - 12, AX - 2 - q * fh - 30, x + 12, AX - 2 - q * fh - 6], outline=INK, width=3)
    if axis:
        d.line([X0 - 10, AX + 4, X1 + 10, AX + 4], fill=INK, width=5)
        for tv in ticks:
            x = xval(tv, xmax); d.line([x, AX - 4, x, AX + 18], fill=INK, width=4)
            lab = '1 МЛН ₽' if tv >= 1_000_000 else f'{tv // 1000} ТЫС. ₽'
            put(C, text_img(lab, 30, INK), x, AX + 42)
def vline(C, x, label, col=INK, y0=150, lab_dx=0):
    d = ImageDraw.Draw(C)
    for y in range(int(y0), AX, 22): d.line([x, y, x, min(AX, y + 12)], fill=col, width=5)
    put(C, plate_img(label, 32, col, WHITE if col != YEL else INK, pad=10, r=8), x + lab_dx, y0 - 22)

# ---- миллионер: цилиндр и золотое свечение ----
def tophat(C, cx, top, s):
    d = ImageDraw.Draw(C); w = 210 * s; h = 190 * s
    d.rounded_rectangle([cx - w * 0.36, top - h, cx + w * 0.36, top], radius=int(10 * s), fill=INK)
    d.rectangle([cx - w * 0.36, top - h * 0.32, cx + w * 0.36, top - h * 0.12], fill=YEL)
    d.rounded_rectangle([cx - w * 0.62, top - h * 0.08, cx + w * 0.62, top + h * 0.06], radius=int(8 * s), fill=INK)
def glow(C, cx, cy, r, u=0, col=YEL):
    d = ImageDraw.Draw(C)
    for j in range(12):
        a = j / 12 * 2 * math.pi + u * 0.8
        d.polygon([(cx, cy), (cx + math.cos(a - 0.12) * r, cy + math.sin(a - 0.12) * r), (cx + math.cos(a + 0.12) * r, cy + math.sin(a + 0.12) * r)], fill=col)
def rich(C, clip, u, cx, feet=FEET, s=0.37, flip=False, shine=True, hat_dx=0):
    if shine: glow(C, cx, feet - 560 * s, 900 * s, u)
    man(C, clip, u, cx, feet, s, flip=flip)
    tophat(C, cx + hat_dx * s, feet - 1215 * s, s * 1.5)
def tag(C, u, text, cx, cy, sz=40, bg=YEL, fg=INK, rot=0):
    if u < 0: return
    put(C, plate_img(text, sz, bg, fg, pad=12, r=10, border=INK, bw=4), cx, cy, back(u / 0.2), rot)

# ---- автобус ----
BX, BY, BW_, BH = 60, 250, 860, 330      # кузов
WIN = [(BX + 70 + j * 104, BY + 50, 88, 120) for j in range(7)]       # окна
DOOR = (BX + BW_ - 150, BY + 40, 96, 250)
PAX = ['idle', 'g_idle', 'idle_smile', 'v_idle', 'idle', 'g_smile', 'idle_sad', 'idle', 'v_idle', 'g_idle']
def bus(C, u, dx=0, pax=30, door=0.0, faces=None, rich_in=None, tags=0.0, shake=0.0):
    """автобус сбоку: пассажиры в окнах (2 ряда голов), справа дверь. door 0..1 — открыта"""
    d = ImageDraw.Draw(C); ox = dx; oy = 3 * s_(u * 30) * shake
    # пассажиры: 30 = 7 окон × 4 + 2 у двери
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); M = Image.new('L', (CW, CH), 0); dm = ImageDraw.Draw(M)
    n = 0
    for wi, (x, y, w, h) in enumerate(WIN):
        dm.rounded_rectangle([x + ox, y + oy, x + w + ox, y + h + oy], radius=14, fill=255)
        for r_, (fx, fs) in enumerate([(0.27, 0.115), (0.73, 0.115), (0.12, 0.13), (0.62, 0.13)]):
            if n >= min(pax, 28): break
            cl = (faces or PAX)[n % len(faces or PAX)]
            row = r_ // 2; man(L, cl, u + n * 0.37, x + w * fx + ox + (w * 0.25 if row else 0), y + h + 70 + row * 34 + oy, fs, frame=None)
            n += 1
    L.putalpha(ImageChops.multiply(L.getchannel('A'), M))
    # кузов
    B = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); db = ImageDraw.Draw(B)
    db.rounded_rectangle([BX + ox, BY + oy, BX + BW_ + ox, BY + BH + oy], radius=46, fill=BUSW, outline=INK, width=8)
    db.rectangle([BX + 8 + ox, BY + BH - 92 + oy, BX + BW_ - 8 + ox, BY + BH - 60 + oy], fill=YEL)
    for (x, y, w, h) in WIN: db.rounded_rectangle([x + ox, y + oy, x + w + ox, y + h + oy], radius=14, fill=(0, 0, 0, 0), outline=INK, width=6)
    dx_, dy_, dw, dh = DOOR; op = clamp(door)
    db.rectangle([dx_ + ox, dy_ + oy, dx_ + dw + ox, dy_ + dh + oy], fill=(232, 236, 240), outline=INK, width=6)
    if op > 0: db.rectangle([dx_ + 6 + ox, dy_ + 6 + oy, dx_ + dw - 6 + ox, dy_ + dh - 6 + oy], fill=(70, 70, 70))
    lw = dw / 2 * (1 - op * 0.8)
    db.rectangle([dx_ + ox, dy_ + oy, dx_ + lw + ox, dy_ + dh + oy], fill=(214, 226, 236), outline=INK, width=5)
    db.rectangle([dx_ + dw - lw + ox, dy_ + oy, dx_ + dw + ox, dy_ + dh + oy], fill=(214, 226, 236), outline=INK, width=5)
    db.rounded_rectangle([BX + BW_ - 30 + ox, BY + 60 + oy, BX + BW_ + 8 + ox, BY + 150 + oy], radius=10, fill=(214, 226, 236), outline=INK, width=6)  # лобовое
    db.rounded_rectangle([BX + 30 + ox, BY + 12 + oy, BX + 220 + ox, BY + 42 + oy], radius=8, fill=INK)
    db.text((BX + 52 + ox, BY + 10 + oy), '№ 2026', font=font(26), fill=YEL)
    for wx in (BX + 170, BX + BW_ - 250):   # колёса
        a = u * 14; db.ellipse([wx - 58 + ox, BY + BH - 58 + oy, wx + 58 + ox, BY + BH + 58 + oy], fill=INK)
        db.ellipse([wx - 26 + ox, BY + BH - 26 + oy, wx + 26 + ox, BY + BH + 26 + oy], fill=MID)
        db.line([wx + math.cos(a) * 24 + ox, BY + BH + math.sin(a) * 24 + oy, wx - math.cos(a) * 24 + ox, BY + BH - math.sin(a) * 24 + oy], fill=INK, width=6)
    C.alpha_composite(B); C.alpha_composite(L)
    if tags > 0:
        for wi, (x, y, w, h) in enumerate(WIN):
            tag(C, tags - wi * 0.05, '70 000', x + w / 2 + ox, y - 26 + oy, 26)
def road(C, u, speed=0):
    d = ImageDraw.Draw(C); d.rectangle([0, BY + BH + 50, CW, BY + BH + 60], fill=LG)
    for j in range(8):
        x = (j * 170 - u * speed) % 1360 - 140; d.rectangle([x, BY + BH + 90, x + 90, BY + BH + 100], fill=MID)
def avgbar(C, v, label='СРЕДНЯЯ В АВТОБУСЕ', col=YEL, y=110):
    put(C, text_img(label, 34, GREY), 470, y - 62); put(C, plate_img(num(v) + ' ₽', 78, col, INK, pad=18, r=12), 470, y + 10)

# ---------------- сцены ----------------
def s_srednyaya(C, u, t):
    ground(C); k = eo(u / 0.22)
    y = lerp(-300, FEET, k) if u < 0.22 else FEET
    man(C, 'pointup', u, 200, y, 0.37)
    slam(C, u - 0.1, 'СРЕДНЯЯ', 640, 180, 120); slam(C, u - 0.3, 'ЗАРПЛАТА', 640, 320, 120)
    slam(C, t - T('России'), 'В РОССИИ', 640, 450, 80, YEL, stroke=INK, sw=8)
def s_103(C, u, t):
    speedlines(C, 470, 330, u, r0=330, col=LG)
    v = roll(u, 0, 103_014, 0.5); txt(C, num(v) + ' ₽', 470, 300, 170, INK, 1 + 0.3 * (1 - eo(u / 0.2)))
    plate(C, u - 0.3, 'СРЕДНЯЯ ЗАРПЛАТА', 470, 470, 52)
    src(C, 'Росстат, август 2026, до вычета НДФЛ', 610)
def s_dvoih(C, u, t):
    ground(C); xs = (130, 330, 530)
    for j, x in enumerate(xs):
        bad = j < 2; v = t - T('нет.')
        man(C, 'idle_sad' if bad and v > 0 else 'idle', u + j * 0.3, x, FEET, 0.29)
        tag(C, u - 0.1 - j * 0.08, '103 000 ₽', x, 230, 32, YEL if not (bad and v > 0) else LG)
        if bad: xcross(C, v - j * 0.1, x, 230, 90)
        if not bad and v > 0: put(C, text_img('✓', 90, GREEN), x, 140)
    slam(C, t - T('двоих'), '2 ИЗ 3', 770, 300, 130, RED, stroke=CARD, sw=10)
    slam(C, t - T('нет.'), 'НЕТ ТАКОЙ', 770, 450, 70, INK)
def s_prostite(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 470, 360, u, r0=360, col=(240, 196, 0))
    man(C, 'shrug', u, 200, FEET, 0.3); man(C, 'g_shrug', u, 760, FEET, 0.28, flip=True)
    slam(C, u, 'ПРОСТИТЕ,', 480, 110, 100); slam(C, t - T('за'), 'А ЗА ЧТО?', 480, 240, 120, INK)
def s_zamer(C, u, t):
    d = ImageDraw.Draw(C)
    for j in range(5):   # пачка листов
        q = clamp((u - j * 0.05) / 0.2); ox = 330 + j * 10; oy = 120 - j * 8 + (1 - eo(q)) * 500
        d.rounded_rectangle([ox, oy, ox + 380, oy + 480], radius=14, fill=WHITE, outline=INK, width=6)
    ox, oy = 370, 88
    put(C, text_img('РОССТАТ', 60, INK), ox + 190, oy + 70)
    for j in range(6): d.rounded_rectangle([ox + 40, oy + 140 + j * 50, ox + 40 + [300, 220, 280, 180, 260, 240][j], oy + 162 + j * 50], radius=8, fill=LG)
    stamp(C, u - 0.35, 'АПРЕЛЬ 2025', ox + 200, oy + 380, 52, RED, -10)
    man(C, 'explain', u, 170, FEET, 0.34)
    src(C, 'обследование раз в 2 года, следующее — апрель 2027', 640, 520)
def s_28(C, u, t):
    d = ImageDraw.Draw(C); n = int(clamp(u / 1.0) * 1200)
    rnd = random.Random(5)
    for j in range(n):
        x = 40 + (j % 60) * 15.5 + rnd.random() * 4; y = 260 + (j // 60) * 21
        if y > 690: break
        fig(d, x, y + 18, 7, INK if (j * 13) % 9 else MID)
    d.rectangle([0, 0, CW, 250], fill=CARD)
    v = roll(u, 0, 28_400_000, 0.7); txt(C, num(v), 470, 110, 130, INK, 1 + 0.2 * (1 - eo(u / 0.15)))
    plate(C, u - 0.25, 'ЗАРПЛАТ', 470, 215, 44)
def queue_x(j, n, k):   # из толпы в одну линию
    return lerp(60 + (j * 37) % 860, 60 + j * (860 / n), k)
def s_ochered(C, u, t):
    d = ImageDraw.Draw(C); n = 70; k = eio(u / 0.8)
    for j in range(n):
        x = queue_x(j, n, k); y = lerp(220 + (j * 53) % 360, AX, k)
        fig(d, x, y, 9, INK)
    d.line([40, AX + 6, 930, AX + 6], fill=INK, width=5)
    slam(C, u - 0.05, 'В ОДНУ ОЧЕРЕДЬ', 470, 110, 100)
def s_sleva(C, u, t):
    d = ImageDraw.Draw(C); n = 70
    for j in range(n): fig(d, 60 + j * (860 / n), AX, 9, INK)
    d.line([40, AX + 6, 930, AX + 6], fill=INK, width=5)
    v = t - T('справа')
    a = eo(u / 0.2); d.polygon([(70, 380), (150, 330), (150, 360), (380 * a + 150 * (1 - a), 360), (380 * a + 150 * (1 - a), 400), (150, 400), (150, 430)], fill=RED)
    slam(C, u - 0.05, 'МАЛО', 240, 230, 110, RED)
    if v > 0:
        b = eo(v / 0.2); d.polygon([(870, 380), (790, 330), (790, 360), (790 - 230 * b, 360), (790 - 230 * b, 400), (790, 400), (790, 430)], fill=GREEN)
        slam(C, v, 'МНОГО', 700, 230, 110, GREEN)
    man(C, 'point', u, 470, AX - 30, 0.2, flip=v <= 0)
def s_gora(C, u, t):
    mountain(C, u, 300_000, 'all', grow=0.5, ticks=(100_000, 200_000, 300_000))
    slam(C, u - 0.1, 'ПОЛУЧИЛАСЬ ГОРА', 470, 90, 90)
    src(C, 'иллюстрация по распределению Росстата, апрель 2025', 690, 470)
def s_dvoe(C, u, t):
    mountain(C, u, 300_000, 'lt100', ticks=(100_000, 200_000, 300_000))
    x = xval(100_000, 300_000); vline(C, x, '100 000 ₽', RED, 150)
    pop(C, u - 0.05, '2/3', 190, 230, 150, YEL, stroke=INK, sw=10)
    plate(C, t - T('левее'), '68% — МЕНЬШЕ 100 ТЫС.', 590, 90, 46)
    src(C, 'Росстат, апрель 2025', 690, 470)
def s_napravo(C, u, t):
    pan = eio(u / 1.2)
    S = Image.new('RGBA', (CW * 2, CH), CARD + (255,))
    # растягиваем гору 1М на двойную ширину: рисуем дважды по половинам
    T1 = Image.new('RGBA', (CW, CH), CARD + (255,)); mountain(T1, 0, 1_050_000, 'tail', ticks=(100_000, 1_000_000))
    T1 = T1.resize((CW * 2, CH), Image.BILINEAR); S.alpha_composite(T1)
    C.alpha_composite(S.crop((int(pan * CW * 0.85), 0, int(pan * CW * 0.85) + CW, CH)))
    man(C, 'walkR', u, 300 + 200 * pan, AX, 0.2)
    slam(C, u - 0.05, 'СМОТРИ НАПРАВО →', 470, 90, 90)
def s_hvost(C, u, t):
    mountain(C, u, 1_050_000, 'tail', ticks=(100_000, 1_000_000))
    tape(C, u - 0.1, 'ХВОСТ', 300, 110, -3)
def s_konec(C, u, t):
    z = 1 + 0.6 * eo(u / 0.5)
    T1 = Image.new('RGBA', (CW, CH), CARD + (255,)); mountain(T1, u, 1_050_000, 'gt1m', ticks=(100_000, 1_000_000))
    w, h = int(CW * z), int(CH * z); T1 = T1.resize((w, h), Image.BILINEAR); fx = xval(1_000_000, 1_050_000)
    C.alpha_composite(T1.crop((int(fx * z - fx * 0.85), int(AX * z - AX), int(fx * z - fx * 0.85) + CW, int(AX * z - AX) + CH)))
    v = t - T('сорок'); vv = roll(v, 0, 45_428, 0.6) if v > 0 else 0
    if v > 0: txt(C, num(vv), 470, 150, 150, INK, 1 + 0.25 * (1 - eo(v / 0.2)))
    plate(C, t - T('больше'), 'ЗАРПЛАТА ОТ 1 000 000 ₽', 470, 300, 50)
def s_vmesyac(C, u, t):
    speedlines(C, 250, 420, u, r0=260, col=LG); ground(C)
    man(C, 'shock', u, 250, FEET, 0.37)
    stamp(C, u, 'В МЕСЯЦ!', 640, 180, 110, RED, -8)
    slam(C, u - 0.35, '1 ИЗ 625', 640, 400, 100)
    src(C, '0,16% работников, Росстат, апрель 2025', 640, 520)
def s_podvoh(C, u, t):
    ground(C); man(C, 'scratch', u, 230, FEET, 0.37)
    tape(C, u, 'А ВОТ И ПОДВОХ', 250, 130, -4)
    pop(C, u - 0.25, '?!', 760, 470, 200, YEL, rot=12, stroke=INK, sw=8)
def s_bus_in(C, u, t):
    k = eo(u / 0.45); road(C, u, 900 * (1 - k)); bus(C, u, dx=lerp(1000, 0, k), pax=30, shake=1 - k)
    for j in range(5):   # линии скорости
        if k < 1: ImageDraw.Draw(C).line([1000 * (1 - k) + 960, 300 + j * 50, 1000 * (1 - k) + 1100 + j * 40, 300 + j * 50], fill=MID, width=6)
    plate(C, u - 0.3, 'АВТОБУС', 470, 120, 60)
def s_pax(C, u, t):
    road(C, u); bus(C, u, pax=30, tags=t - T('семьдесят'))
    slam(C, u, '30 ПАССАЖИРОВ', 470, 110, 84)
    if t > T('семьдесят'): slam(C, t - T('семьдесят'), 'У КАЖДОГО 70 000 ₽', 470, 660, 56, INK)
def s_zahodit(C, u, t):
    road(C, u); bus(C, u, pax=30, door=eo(u / 0.25))
    k = eo((u - 0.15) / 0.5); x = lerp(1060, DOOR[0] + DOOR[2] / 2, k)
    rich(C, 'walk', u, x, BY + BH + 50, 0.24, flip=True)
    slam(C, u - 0.05, 'ЗАХОДИТ ОН', 470, 110, 90)
def s_million(C, u, t):
    speedlines(C, 330, 380, u, r0=300, col=(255, 236, 150))
    rich(C, 'boss', u, 330, FEET, 0.42)
    v = roll(u, 0, 1_000_000, 0.4); slam(C, u, num(v) + ' ₽', 680, 260, 96, INK)
    plate(C, u - 0.25, 'В МЕСЯЦ', 680, 400, 56)
def s_sred(C, u, t):
    road(C, u); bus(C, u, pax=30, tags=1.0)
    rich(C, 'boss', u, DOOR[0] + DOOR[2] / 2, BY + BH + 50, 0.22, shine=False)
    v = t - T('ровно'); val = roll(u - 0.5, 70_000, 100_000, 1.4) if v < 0 else 100_000
    avgbar(C, val, y=110 if v < 0 else 110)
    if v > 0: stamp(C, v, 'РОВНО', 800, 60, 44, RED, 10)
def s_formula(C, u, t):
    d = ImageDraw.Draw(C)
    slam(C, u, '30 × 70 000', 470, 130, 100); slam(C, u - 0.15, '+ 1 000 000', 470, 260, 100, INK)
    d.line([170, 340, 770, 340], fill=INK, width=8) if u > 0.3 else None
    slam(C, u - 0.3, '÷ 31 ПАССАЖИР', 470, 430, 90, INK)
    if u > 0.55: put(C, plate_img('= 100 000 ₽', 100, YEL, INK, pad=16, r=12), 470, 590, back((u - 0.55) / 0.2))
def s_bogache(C, u, t):
    road(C, u); bus(C, u, pax=30, tags=1.0, faces=['shrug', 'g_shrug', 'v_shrug'])
    rich(C, 'boss', u, DOOR[0] + DOOR[2] / 2, BY + BH + 50, 0.22, shine=False)
    slam(C, u, 'БОГАЧЕ', 470, 70, 80); slam(C, u - 0.2, 'НИКТО НЕ СТАЛ', 470, 170, 70, RED)
def s_vyidet(C, u, t):
    road(C, u); bus(C, u, pax=30, door=1 - eo((u - 0.8) / 0.3), tags=1.0)
    k = eo(u / 0.6); x = lerp(DOOR[0] + DOOR[2] / 2, 1100, k)
    rich(C, 'walkR', u, x, BY + BH + 50, 0.22, shine=False)
    avgbar(C, roll(u - 0.15, 100_000, 70_000, 0.6))
def s_obedneli(C, u, t):
    road(C, u); bus(C, u, pax=30, faces=['idle_sad', 'g_sad', 'idle_sad', 'v_idle'])
    avgbar(C, 70_000); stamp(C, u - 0.1, '«ОБЕДНЕЛИ»', 470, 420, 96, RED, -8)
def s_strana(C, u, t):
    mountain(C, u, 1_050_000, 'all', ticks=(100_000, 1_000_000))
    slam(C, u, 'СО СТРАНОЙ', 560, 120, 90); slam(C, u - 0.2, 'ТОТ ЖЕ ФОКУС', 560, 240, 90, RED)
def s_tyanet(C, u, t):
    mountain(C, u, 300_000, 'all', ticks=(100_000, 200_000, 300_000))
    k = eo((u - 0.15) / 0.9); xm = xval(73_871, 300_000); xa = xval(lerp(73_871, 103_014, k), 300_000)
    vline(C, xa, 'СРЕДНЯЯ', YEL, 140, 40)
    d = ImageDraw.Draw(C); d.line([xa, 330, 860, 330 + 6 * s_(u * 20)], fill=INK, width=6)   # верёвка к хвосту
    man(C, 'point', u, 880, AX, 0.24)
    slam(C, u - 0.05, 'ХВОСТ ТЯНЕТ ВВЕРХ', 470, 70, 70)
def s_stop(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); man(C, 'stop', u, 260, FEET, 0.38)
    slam(C, u, 'СТОП.', 650, 280, 210)
def s_tupish(C, u, t):
    ground(C); man(C, 'idle_sad', u, 250, FEET, 0.37)
    plate(C, u, 'ВОТ ТУТ ТЫ ТУПИШЬ', 470, 110, 74, YEL)
    d = ImageDraw.Draw(C); k = eo((t - T('меряешь')) / 0.3) if t > T('меряешь') else 0
    if k > 0:   # линейка-мерка «средняя»
        top = FEET - 440 * k; d.rectangle([420, top, 500, FEET], fill=YEL, outline=INK, width=5)
        for j in range(int((FEET - top) / 40)): d.line([420, FEET - j * 40, 450 if j % 2 else 470, FEET - j * 40], fill=INK, width=4)
        put(C, plate_img('103 000 ₽', 40, INK, YEL, pad=10, r=8), 620, top + 30)
        put(C, plate_img('ТЫ', 40, LG, INK, pad=10, r=8), 120, FEET - 330)
def s_mediana(C, u, t):
    mountain(C, u, 300_000, 'all', ticks=(100_000, 200_000, 300_000))
    xm = xval(73_871, 300_000); xa = xval(103_014, 300_000)
    vline(C, xa, 'СРЕДНЯЯ', MID, 230, 70)
    k = eo(u / 0.3); vline(C, xm, 'МЕДИАНА', GREEN, lerp(600, 150, k), -60)
    slam(C, u, 'МЕДИАНА', 560, 70, 80, GREEN)
def s_seredina(C, u, t):
    d = ImageDraw.Draw(C); n = 41; mid = n // 2
    for j in range(n):
        x = 60 + j * (840 / (n - 1)); fig(d, x, AX, 12, (GREEN if j == mid else INK if j < mid else MID))
    xm = 60 + mid * (840 / (n - 1)); d.ellipse([xm - 40, AX - 120, xm + 40, AX + 10], outline=GREEN, width=6)
    d.line([40, AX + 6, 930, AX + 6], fill=INK, width=5)
    plate(C, u - 0.2, '50% МЕНЬШЕ', 250, 360, 44, LG); plate(C, u - 0.35, '50% БОЛЬШЕ', 690, 360, 44, LG)
    slam(C, u, 'РОВНО ПОСЕРЕДИНЕ', 470, 110, 84)
def s_74(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); d = ImageDraw.Draw(C); r = 240 * eo(u / 0.25)
    d.ellipse([260 - r, 400 - r, 260 + r, 400 + r], fill=CARD)
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im, 'idle_smile', u, 260, FEET + 60, 0.45)
    m = Image.new('L', (CW, CH), 0); ImageDraw.Draw(m).ellipse([260 - r, 400 - r, 260 + r, 400 + r], fill=255); im.putalpha(ImageChops.multiply(im.getchannel('A'), m)); C.alpha_composite(im)
    v = roll(u - 0.1, 0, 73_871, 0.5); txt(C, num(v) + ' ₽', 700, 300, 100, YEL)
    put(C, text_img('МЕДИАНА', 50, WHITE), 700, 410)
    put(C, text_img('Росстат, апрель 2025, до НДФЛ', 26, GREY), 700, 470)
def s_naruki(C, u, t):
    ground(C); man(C, 'idle_smile', u, 200, FEET, 0.36)
    d = ImageDraw.Draw(C); k = back(u / 0.25); cx, cy = 600, 330
    w, h = 300 * k, 560 * k
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(40 * k) + 1, fill=INK)
    d.rounded_rectangle([cx - w / 2 + 14, cy - h / 2 + 14, cx + w / 2 - 14, cy + h / 2 - 14], radius=int(30 * k) + 1, fill=WHITE)
    if u > 0.25:
        q = back((u - 0.25) / 0.2); put(C, plate_img('ЗАРПЛАТА', 30, LG, INK, pad=10, r=10), cx, cy - 110, q)
        put(C, text_img('+64 268 ₽', 62, GREEN), cx, cy - 30, q)
    src(C, '73 871 − 13% НДФЛ', 690, 600)
def s_neproval(C, u, t):
    ground(C); man(C, 'shrug', u, 230, FEET, 0.37)
    slam(C, u, 'МЕНЬШЕ 100 000 ₽', 600, 150, 74)
    stamp(C, t - T('не', 1) if t > T('не', 1) - 0.1 else -1, 'ПРОВАЛ', 620, 360, 110, RED, -6)
    strike(C, t - T('провал.') - 0.15, 430, 400, 820, 320, INK, 18)
def s_bolsh(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); d = ImageDraw.Draw(C)
    for j in range(140):
        v = u - (j % 14) * 0.02
        if v < 0: continue
        row = j // 14; x = 40 + (j % 14) * 64 + (row % 2) * 30; y = 330 + row * 38 + (1 - back(v / 0.2)) * 300 - 10 * abs(s_(u * 9 + j))
        fig(d, x, y, 16 if row > 3 else 12, INK)
    man(C, 'armsup', u, 470, FEET + 20, 0.3)
    slam(C, u, 'ЭТО БОЛЬШИНСТВО', 470, 110, 100)
def s_sravni(C, u, t):
    d = ImageDraw.Draw(C); d.line([470, 40, 470, 680], fill=LG, width=6)
    man(C, 'idle_smile', u, 230, FEET, 0.33); put(C, plate_img('74 000 ₽', 44, GREEN, WHITE, pad=10, r=8), 230, 130, back(u / 0.2))
    v = t - T('парнем')
    rich(C, 'boss', u, 710, FEET, 0.33, shine=v < 0)
    put(C, plate_img('1 000 000 ₽', 44, YEL, INK, pad=10, r=8), 710, 130, back(u / 0.2))
    if u > 0.2: put(C, text_img('✓', 160, GREEN), 380, 400, back((u - 0.2) / 0.2))
    if v > 0: xcross(C, v, 710, 380, 170)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи.'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 250, FEET, 0.38)
    else: man(C, 'walkR', e, 250 - e * 420, FEET, 0.38, flip=True)
    slam(C, u, 'ВСЁ.', 660, 200, 190)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 660, 430, 150, INK, YEL)
    ground(C, col=(230, 190, 0))

def SH(t0, fn, tr='zoom', sfx='whoosh'): return dict(t=t0, fn=fn, tr=tr, sfx=sfx)
SHOTS = [
 SH(0.0, s_srednyaya, 'none', 'thud'), SH(T('сто') - 0.05, s_103, 'zoom', 'boom'), SH(T('Но') - 0.05, s_dvoih, 'whipL', 'bass'),
 SH(T('Простите,') - 0.05, s_prostite, 'shake', 'boing'), SH(T('Берём') - 0.05, s_zamer, 'whipR', 'whoosh'), SH(T('двадцать') - 0.05, s_28, 'zoom', 'bass'),
 SH(T('И', 0) - 0.03, s_ochered, 'whipL', 'whoosh'), SH(T('Слева') - 0.05, s_sleva, 'zoom', 'swipe'), SH(T('Получилась') - 0.05, s_gora, 'whipU', 'riser'),
 SH(T('Двое') - 0.05, s_dvoe, 'zoom', 'boom'), SH(T('А', 0) - 0.03, s_napravo, 'whipR', 'whoosh'), SH(T('Там') - 0.05, s_hvost, 'zoom', 'bass'),
 SH(T('И', 1) - 0.03, s_konec, 'zoom', 'zoomin'), SH(T('В', 0) - 0.05, s_vmesyac, 'shake', 'boom'),
 SH(T('А', 1) - 0.03, s_podvoh, 'glitch', 'scratch'), SH(T('Садимся') - 0.05, s_bus_in, 'whipL', 'whoosh'), SH(T('Тридцать') - 0.05, s_pax, 'zoom', 'bass'),
 SH(T('Заходит') - 0.05, s_zahodit, 'whipR', 'whoosh'), SH(T('Миллион') - 0.05, s_million, 'zoom', 'boom'),
 SH(T('И', 2) - 0.03, s_sred, 'whipL', 'bass'), SH(T('ровно') - 0.05, s_formula, 'zoom', 'boom'), SH(T('Богаче') - 0.05, s_bogache, 'whipR', 'whoosh'),
 SH(T('Он') - 0.05, s_vyidet, 'whipL', 'swipe'), SH(T('и', 1) - 0.03, s_obedneli, 'shake', 'drop'),
 SH(T('Со') - 0.05, s_strana, 'zoom', 'bass'), SH(T('хвост', 1) - 0.05, s_tyanet, 'whipR', 'whoosh'),
 SH(T('Стоп.') - 0.05, s_stop, 'shake', 'scratch'), SH(T('Вот') - 0.05, s_tupish, 'zoom', 'error'),
 SH(T('Смотри') - 0.05, s_mediana, 'whipL', 'whoosh'), SH(T('человека') - 0.05, s_seredina, 'zoom', 'bass'),
 SH(T('У') - 0.03, s_74, 'cut', 'zoomin'), SH(T('на', 2) - 0.05, s_naruki, 'whipR', 'whoosh'),
 SH(T('Так') - 0.05, s_neproval, 'zoom', 'bass'), SH(T('Это') - 0.05, s_bolsh, 'zoom', 'boom'), SH(T('Сравнивай') - 0.05, s_sravni, 'whipL', 'whoosh'),
 SH(T('Всё.') - 0.05, s_netupi, 'shake', 'final'),
]
ACC = [(T('России'), 'pop'), (T('нет.'), 'error'), (T('за'), 'pop'), (T('Берём') + 0.35, 'stamp'), (T('очередь.'), 'swipe'), (T('справа'), 'swipe'),
       (T('левее'), 'pop'), (T('хвост.'), 'swipe'), (T('сорок'), 'tick'), (T('больше', 0), 'pop'), (T('В', 0) + 0.35, 'pop'),
       (T('семьдесят'), 'pop'), (T('семьдесят') + 0.3, 'pop'), (T('Заходит') + 0.05, 'ding'), (T('Миллион'), 'coins'), (T('теперь', 1) + 0.4, 'tick2'),
       (T('ровно') + 0.55, 'shine'), (T('стал.'), 'error'), (T('выйдет'), 'swipe'), (T('обеднеют»'), 'stamp'),
       (T('среднюю', 0), 'swipe'), (T('медиану'), 'ding'), (T('посередине'), 'pop'), (T('семьдесят', 1), 'tick'), (T('руки'), 'notif'),
       (T('не', 1), 'stamp'), (T('провал.') + 0.15, 'swipe'), (T('парнем'), 'error'), (T('тупи.'), 'stamp')]

def shot_at(t):
    i = max(j for j in range(len(SHOTS)) if SHOTS[j]['t'] <= t); return i, SHOTS[i]
def render_card(t):
    i, sh = shot_at(t); C = Image.new('RGBA', (CW, CH), CARD + (255,)); sh['fn'](C, t - sh['t'], t); return C, i, sh

# ---------- переход: трансформация карточки в первые ~0.2 сек сцены ----------
def hblur(im, k):
    if k < 2: return im
    w, h = im.size; return im.resize((max(1, int(w / k)), h), Image.BILINEAR).resize((w, h), Image.BILINEAR)
def vblur(im, k):
    if k < 2: return im
    w, h = im.size; return im.resize((w, max(1, int(h / k))), Image.BILINEAR).resize((w, h), Image.BILINEAR)
def transform(C, u, tr, seed):
    D = 0.2; out = Image.new('RGBA', (CW, CH), BLK + (255,)); k = clamp(u / D); rnd = random.Random(seed * 100 + int(u * FPS))
    if tr in ('none', 'cut') or u >= D + 0.15: return C
    if tr == 'zoom':
        z = 1 + 0.55 * (1 - eo(k)); w, h = int(CW * z), int(CH * z); im = C.resize((w, h), Image.BILINEAR); out.paste(im, ((CW - w) // 2, (CH - h) // 2)); return out
    if tr in ('whipL', 'whipR'):
        sgn = 1 if tr == 'whipL' else -1; dx = int(sgn * CW * 0.9 * (1 - eo(k))); im = hblur(C, 1 + 40 * (1 - k) ** 2); out = Image.new('RGBA', (CW, CH), CARD + (255,)); out.paste(im, (dx, 0)); return out
    if tr == 'whipU':
        dy = int(CH * 0.9 * (1 - eo(k))); im = vblur(C, 1 + 30 * (1 - k) ** 2); out = Image.new('RGBA', (CW, CH), CARD + (255,)); out.paste(im, (0, dy)); return out
    if tr == 'shake':
        a = 34 * (1 - clamp(u / (D + 0.15))) ; z = 1.12; w, h = int(CW * z), int(CH * z); im = C.resize((w, h), Image.BILINEAR)
        out.paste(im, ((CW - w) // 2 + int((rnd.random() - 0.5) * 2 * a), (CH - h) // 2 + int((rnd.random() - 0.5) * 2 * a))); return out
    if tr == 'spin':
        z = 1 + 0.5 * (1 - eo(k)); im = C.resize((int(CW * z), int(CH * z)), Image.BILINEAR).rotate(-25 * (1 - eo(k)), Image.BILINEAR, fillcolor=CARD + (255,))
        out.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2)); return out
    if tr == 'glitch':
        out = C.copy()
        for j in range(7):
            if k < 1: y = rnd.randrange(0, CH - 60); hh = rnd.randrange(20, 90); out.paste(C.crop((0, y, CW, y + hh)), (rnd.randrange(-120, 120), y))
        return out
    return C
def rgbsplit(im, a):
    if a < 1: return im
    r, g, b = im.split(); r = ImageChops.offset(r, int(a), 0); b = ImageChops.offset(b, -int(a), 0); return Image.merge('RGB', (r, g, b))

# ---------- субтитры: 1–3 слова, текущее слово жёлтое ----------
def chunks():
    out, cur = [], []
    for w in W:
        cur.append(w); txtc = ' '.join(x[0] for x in cur)
        if w[0][-1] in '.!?…:»' or (w[0][-1] == ',' and len(txtc) > 7) or len(cur) == 3 or len(txtc) > 15: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CHK = chunks(); SUB_Y = 1372
def clean(w): return w.replace('«', '').replace('»', '').upper()
def subs(F, t):
    for ci, ch in enumerate(CHK):
        t1 = CHK[ci + 1][0][1] if ci + 1 < len(CHK) else ch[-1][2] + 0.6
        if ch[0][1] - 0.04 <= t < t1:
            ims = []
            for (w, a, b) in ch:
                act = a - 0.03 <= t; cur = act and (t < b + 0.08 or w is ch[-1][0] and False)
                nxt = [x for x in ch if x[1] > a]; cur = a - 0.03 <= t and (not nxt or t < nxt[0][1] - 0.03)
                ims.append((text_img(clean(w), 86, YEL if cur else WHITE, INK, 6), 1 + 0.14 * (1 - eo((t - a) / 0.12)) if cur else 1))
            tw = sum(im.width for im, _ in ims) + 36 * (len(ims) - 1)
            sc0 = min(1, 780 / tw); x = 540 - tw * sc0 / 2; k0 = back((t - ch[0][1] + 0.04) / 0.14)
            for im, sc in ims:
                put(F, im, x + im.width * sc0 / 2, SUB_Y + (1 - k0) * 30, sc * sc0); x += (im.width + 36) * sc0
            return

# ---------- кадр ----------
@lru_cache(1)
def title_layer():
    L = Image.new('RGBA', (WD, HT), BLK + (255,))
    put(L, text_img('ПОЧЕМУ У ТЕБЯ НЕТ', 68, WHITE), 540, 372); put(L, text_img('СРЕДНЕЙ ЗАРПЛАТЫ', 84, YEL), 540, 462)
    return L
def frame(t):
    F = title_layer().copy(); C, i, sh = render_card(t); u = t - sh['t']
    C = transform(C, u, sh['tr'], i)
    # хвост предыдущей сцены: за 2 кадра до склейки лёгкий наезд
    if i + 1 < len(SHOTS):
        r = SHOTS[i + 1]['t'] - t
        if r < 0.07 and SHOTS[i + 1]['tr'] not in ('cut', 'none'):
            z = 1 + 0.1 * (1 - r / 0.07); w, h = int(CW * z), int(CH * z); C2 = Image.new('RGBA', (CW, CH)); C2.paste(C.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2)); C = C2
    F.paste(C.convert('RGB'), (0, CY0))
    if u < 0.07 and sh['tr'] not in ('none', 'cut'):   # вспышка на склейке
        fl = Image.new('RGBA', (CW, CH), (255, 255, 255, int(150 * (1 - u / 0.07)))); F.alpha_composite(fl, (0, CY0))
    subs(F, t)
    if t < 0.35:   # вход заголовка
        k = eo(t / 0.35); F2 = Image.new('RGBA', (WD, HT), BLK + (255,)); F2.paste(F.crop((0, 250, WD, 530)), (0, int(250 - 60 * (1 - k)))); F2.paste(F.crop((0, 530, WD, HT)), (0, 530)); F = Image.blend(Image.new('RGBA', (WD, HT), BLK + (255,)), F2, 0.3 + 0.7 * k)
    out = F.convert('RGB')
    if u < 0.1 and sh['tr'] in ('shake', 'glitch', 'zoom'): out = rgbsplit(out, 10 * (1 - u / 0.1))
    return out

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        frac = float(a[1]) if len(a) > 1 else 0.6; ims = []
        for j, sh in enumerate(SHOTS):
            t1 = SHOTS[j + 1]['t'] if j + 1 < len(SHOTS) else DUR - 0.8; tt = sh['t'] + (t1 - sh['t']) * frac
            C, _, _ = render_card(tt); ims.append(C.convert('RGB').resize((360, 240)))
        cols = 5; rows = (len(ims) + cols - 1) // cols
        for part in range(0, rows, 5):
            S = Image.new('RGB', (cols * 364, min(5, rows - part) * 244), (90, 90, 90))
            for j, im in enumerate(ims[part * cols:(part + 5) * cols]): S.paste(im, ((j % cols) * 364, (j // cols) * 244))
            S.save(f'sheet_{frac}_{part // 5}.png')
    elif a:
        for x in a: frame(float(x)).save(f'prev_{x}.png')
    else:
        ev = [(round(s['t'], 3), s['sfx']) for s in SHOTS] + [(round(t, 3), n) for t, n in ACC]
        json.dump(dict(dur=DUR, ev=sorted(ev)), open('sfx.json', 'w'))
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', os.environ.get('OUT', 'video_noaudio.mp4')], stdin=subprocess.PIPE)
        lo, hi = (int(os.environ.get('F0', 0)), int(os.environ.get('F1', N)))
        for i in range(lo, hi):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 150 == 0: print(i, N, flush=True)
        p.stdin.close(); p.wait(); print('done')
