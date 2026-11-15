"""СДВГ-монтаж «Последний барабан» (дропы), движок «Автобуса» v2: переходы через действие, смена темпа (паузы), глубина (параллакс, тени, зерно): чёрный кадр, заголовок, белая карточка-сцена, субтитр под ней.
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

# ================= СЦЕНЫ «Последний барабан» (дропы) =================  fn(C, u, t)
GREEN = (40, 170, 90); BILL = (150, 200, 140); BILLD = (90, 140, 85); MUD = (120, 84, 48); MUD2 = (150, 110, 70)
WASH = (244, 244, 246); GLASS = (180, 200, 214)
def num(v): return f'{int(round(v)):,}'.replace(',', ' ')
def roll(u, a, b, d=0.6): return lerp(a, b, eo(u / d))
def src(C, text, y=CH - 26, x=None): put(C, text_img(text, 26, GREY), x or 470, y)
def tag(C, u, text, cx, cy, sz=40, bg=YEL, fg=INK, rot=0):
    if u < 0: return
    put(C, plate_img(text, sz, bg, fg, pad=12, r=10, border=INK, bw=4), cx, cy, back(u / 0.2), rot)

@lru_cache(64)
def bill_img(w, dirty=0, seed=0):
    h = int(w * 0.5); im = Image.new('RGBA', (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([3, 3, w + 3, h + 3], radius=max(2, w // 18), fill=BILL, outline=INK, width=max(2, w // 30))
    d.ellipse([w / 2 - h * 0.28 + 3, h * 0.22 + 3, w / 2 + h * 0.28 + 3, h * 0.78 + 3], outline=BILLD, width=max(2, w // 40))
    d.text((w * 0.08 + 3, h * 0.08), '₽', font=font2(max(8, h * 0.32)), fill=BILLD)
    if dirty:
        rnd = random.Random(seed)
        for j in range(dirty):
            x = rnd.uniform(0.1, 0.9) * w; y = rnd.uniform(0.15, 0.85) * h; r = rnd.uniform(0.12, 0.25) * h
            d.ellipse([x - r * 1.3, y - r, x + r * 1.3, y + r], fill=MUD)
    return im
def bill(C, cx, cy, w=120, rot=0, dirty=0, seed=0, alpha=1.0): put(C, bill_img(int(w), dirty, seed), cx, cy, 1, rot, alpha)

@lru_cache(16)
def card_img(w, dirty=0):
    h = int(w * 0.63); im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w + 4, h + 4], radius=w // 14, fill=(40, 40, 44), outline=INK, width=max(3, w // 60))
    d.rounded_rectangle([w * 0.1 + 4, h * 0.3 + 4, w * 0.27 + 4, h * 0.52 + 4], radius=w // 60, fill=YEL)
    d.text((w * 0.1 + 4, h * 0.62), '••••  ••••  ••••  1234', font=font2(max(8, w * 0.06)), fill=(220, 220, 220))
    if dirty:
        rnd = random.Random(3)
        for j in range(dirty):
            x = rnd.uniform(0.2, 0.9) * w; y = rnd.uniform(0.2, 0.8) * h; r = rnd.uniform(0.08, 0.16) * w
            d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=MUD2)
    return im
def card(C, cx, cy, w=260, rot=0, dirty=0, scale=1.0): put(C, card_img(int(w), dirty), cx, cy, scale, rot)

def washer(C, cx, cy, s, u, content='bills', spin=1.0, dirty=0, label=None, lit=False, hl=False):
    """стиральная машина: корпус, панель, круглое окно-барабан с содержимым"""
    d = ImageDraw.Draw(C); w, h = 300 * s, 360 * s; x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(26 * s), fill=YEL if hl else WASH, outline=INK, width=max(3, int(8 * s)))
    d.line([x0, y0 + h * 0.2, x0 + w, y0 + h * 0.2], fill=INK, width=max(2, int(6 * s)))
    d.ellipse([x0 + w * 0.68, y0 + h * 0.06, x0 + w * 0.84, y0 + h * 0.06 + w * 0.16], fill=MID, outline=INK, width=max(2, int(4 * s)))
    d.rounded_rectangle([x0 + w * 0.12, y0 + h * 0.08, x0 + w * 0.5, y0 + h * 0.14], radius=int(6 * s), fill=RED if lit and int(u * 6) % 2 else LG)
    r = w * 0.36; ox, oy = cx, y0 + h * 0.58
    d.ellipse([ox - r - 14 * s, oy - r - 14 * s, ox + r + 14 * s, oy + r + 14 * s], fill=LG, outline=INK, width=max(3, int(8 * s)))
    # содержимое барабана в маске
    L = Image.new('RGBA', (int(r * 2), int(r * 2)), GLASS + (255,)); dl = ImageDraw.Draw(L)
    a0 = u * 6 * spin
    if content == 'bills':
        for j in range(6):
            a = a0 + j * 1.05; px = r + math.cos(a) * r * 0.45; py = r + math.sin(a) * r * 0.45 + r * 0.15
            put(L, bill_img(int(r * 0.9), dirty, j), px, py, 1, math.degrees(-a) % 360)
    elif content == 'card':
        put(L, card_img(int(r * 1.3)), r + math.cos(a0) * r * 0.15, r + math.sin(a0) * r * 0.15, 1, math.degrees(-a0 * 0.5) % 360)
    elif content == 'water':
        dl.rectangle([0, r * (1.1 + 0.08 * s_(u * 5)), r * 2, r * 2], fill=(150, 185, 205))
    for j in range(3):   # пузырьки
        bx = r + math.cos(a0 * 0.7 + j * 2) * r * 0.7; by = r + math.sin(a0 * 0.7 + j * 2) * r * 0.7
        dl.ellipse([bx - r * 0.07, by - r * 0.07, bx + r * 0.07, by + r * 0.07], outline=WHITE, width=max(2, int(4 * s)))
    dl.pieslice([r * 0.2, r * 0.2, r * 1.6, r * 1.6], 200, 250, fill=(225, 235, 242))   # блик
    M = Image.new('L', L.size, 0); ImageDraw.Draw(M).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255); L.putalpha(M)
    C.alpha_composite(L, (int(ox - r), int(oy - r)))
    d.ellipse([ox - r, oy - r, ox + r, oy + r], outline=INK, width=max(3, int(6 * s)))
    if label: put(C, plate_img(label, max(18, int(34 * s)), INK, YEL, pad=8, r=6), cx, y0 + h + 30 * s)

def stains(C, cx, cy, r, k, seed=1):
    """пятна грязи проступают (k 0..1)"""
    if k <= 0: return
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(seed)
    for j in range(9):
        x = cx + rnd.uniform(-1, 1) * r * 0.6; y = cy + rnd.uniform(-1, 1) * r; rr = rnd.uniform(0.12, 0.22) * r * eo(clamp(k * 1.6 - j * 0.08))
        if rr > 1: d.ellipse([x - rr * 1.3, y - rr, x + rr * 1.3, y + rr], fill=MUD2 + (235,))
    C.alpha_composite(L)

def phone(C, cx, cy, s=1.0, rot=0, ring=0.0, screen=None):
    im = Image.new('RGBA', (int(130 * s) + 10, int(240 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 130 * s + 4, 240 * s + 4], radius=int(22 * s), fill=INK)
    d.rounded_rectangle([12 * s, 22 * s, 122 * s, 216 * s], radius=int(12 * s), fill=WHITE if not screen else screen)
    put(C, im, cx + (6 * s_(ring * 60) if ring else 0), cy, 1, rot)
    if ring:
        dd = ImageDraw.Draw(C)
        for j in range(3):
            rr = (60 + j * 34) * s; dd.arc([cx - rr, cy - rr, cx + rr, cy + rr], -50, 50, fill=INK, width=max(3, int(6 * s))); dd.arc([cx - rr, cy - rr, cx + rr, cy + rr], 130, 230, fill=INK, width=max(3, int(6 * s)))

def msgbox(C, u, x, y, w, lines):
    """карточка сообщения: lines = [(t_появления, текст, стиль)]"""
    d = ImageDraw.Draw(C); k = back(u / 0.25)
    if u < 0: return
    h = 90 + 70 * sum(1 for tt, _, _ in lines if u >= tt)
    im = Image.new('RGBA', (w + 20, h + 40), (0, 0, 0, 0)); di = ImageDraw.Draw(im)
    di.rounded_rectangle([6, 6, w, h], radius=30, fill=WHITE, outline=INK, width=6)
    di.polygon([(30, h - 4), (10, h + 30), (80, h - 4)], fill=WHITE, outline=None); di.line([(30, h - 2), (10, h + 30), (78, h - 2)], fill=INK, width=6)
    di.ellipse([28, 24, 72, 68], fill=MID); di.text((88, 26), 'НЕИЗВЕСТНЫЙ', font=font(34), fill=GREY)
    yy = 92
    for tt, text, st in lines:
        if u < tt: continue
        if st == 'y': t_ = plate_img(text, 44, YEL, INK, pad=10, r=8)
        else: t_ = text_img(text, 46, INK)
        im.alpha_composite(t_, (30, int(yy))); yy += 70
    put(C, im, x, y, k)

def atm(C, cx, by, s=1.0, cash=0.0):
    d = ImageDraw.Draw(C); w, h = 300 * s, 520 * s; x0, y0 = cx - w / 2, by - h
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=int(20 * s), fill=(214, 218, 224), outline=INK, width=max(3, int(8 * s)))
    d.rounded_rectangle([x0 + w * 0.12, y0 + h * 0.08, x0 + w * 0.88, y0 + h * 0.36], radius=int(10 * s), fill=(60, 90, 110), outline=INK, width=max(2, int(5 * s)))
    put(C, text_img('НАЛИЧНЫЕ', int(30 * s), WHITE), cx, y0 + h * 0.22)
    for j in range(3):
        for q in range(3): d.rounded_rectangle([x0 + w * (0.22 + q * 0.2), y0 + h * (0.44 + j * 0.07), x0 + w * (0.36 + q * 0.2), y0 + h * (0.49 + j * 0.07)], radius=4, fill=MID, outline=INK, width=2)
    sy = y0 + h * 0.72; d.rounded_rectangle([x0 + w * 0.15, sy, x0 + w * 0.85, sy + 22 * s], radius=6, fill=INK)
    if cash > 0:
        for j in range(3): bill(C, cx + (j - 1) * 8, sy + 10 * s + 70 * s * eo(cash) - j * 6, 150 * s, 90 + (j - 1) * 6)
    d.ellipse([cx - 14 * s, y0 - 30 * s, cx + 14 * s, y0 - 2 * s], fill=INK)   # камера сверху

def cctv(C, cx, cy, s, u):
    d = ImageDraw.Draw(C)
    d.line([cx + 160 * s, cy - 120 * s, cx + 160 * s, cy - 10 * s], fill=INK, width=int(18 * s))
    d.rounded_rectangle([cx + 120 * s, cy - 150 * s, cx + 260 * s, cy - 110 * s], radius=8, fill=INK)
    im = Image.new('RGBA', (int(420 * s), int(200 * s)), (0, 0, 0, 0)); di = ImageDraw.Draw(im)
    di.rounded_rectangle([60 * s, 30 * s, 400 * s, 170 * s], radius=int(30 * s), fill=(230, 232, 236), outline=INK, width=int(10 * s))
    di.rectangle([10 * s, 50 * s, 70 * s, 150 * s], fill=INK); di.ellipse([20 * s, 70 * s, 60 * s, 130 * s], fill=(60, 90, 110))
    if int(u * 3) % 2 == 0: di.ellipse([340 * s, 55 * s, 370 * s, 85 * s], fill=RED)
    put(C, im, cx, cy, 1, -12 + 4 * s_(u * 1.5))

def corners(C, x0, y0, x1, y1, col=RED, L=60, w=10):
    d = ImageDraw.Draw(C)
    for (x, y, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([x, y, x + sx * L, y], fill=col, width=w); d.line([x, y, x, y + sy * L], fill=col, width=w)

def clipping(C, u, city, age, verdict, src_txt, t_v):
    """газетная вырезка без фото и имён: город, возраст, приговор-штамп"""
    d = ImageDraw.Draw(C); k = back(u / 0.25); rnd = random.Random(len(city))
    im = Image.new('RGBA', (720, 560), (0, 0, 0, 0)); di = ImageDraw.Draw(im)
    pts = [(20 + rnd.uniform(-8, 8), 20 + rnd.uniform(-8, 8)) for _ in range(1)]
    poly = [(20, 24), (180, 14), (360, 26), (540, 12), (700, 22), (708, 200), (698, 380), (706, 540), (520, 548), (340, 536), (160, 550), (14, 540), (22, 360), (12, 180)]
    di.polygon(poly, fill=(246, 242, 228), outline=INK); di.line(poly + [poly[0]], fill=INK, width=4)
    di.rectangle([60, 70, 660, 80], fill=INK)
    t1 = text_img('ПРИГОВОР', 44, GREY); im.alpha_composite(t1, (60, 96))
    t2 = text_img(city, 110, INK); im.alpha_composite(t2, (60, 160))
    t3 = text_img(age, 70, INK); im.alpha_composite(t3, (60, 300))
    for j in range(3): di.rectangle([60, 410 + j * 34, 60 + [560, 480, 380][j], 428 + j * 34], fill=LG)
    put(C, im, 470, 345, k, -2)
    if t_v is not None: stamp(C, t_v, verdict, 470, 545, 70 if len(verdict) <= 15 else 50, RED, -6)
    src(C, src_txt, 690)

def bars(C, k, x0=60, x1=900, col=INK):
    d = ImageDraw.Draw(C); y = lerp(-CH, 0, eo(k))
    d.rectangle([x0 - 20, y + 30, x1 + 20, y + 60], fill=col)
    for x in range(int(x0), int(x1) + 1, 84): d.rectangle([x, y + 30, x + 22, y + CH], fill=col)

# ---------------- сцены ----------------
def s_divan(C, u, t):
    ground(C); d = ImageDraw.Draw(C)
    d.rounded_rectangle([60, FEET - 150, 520, FEET - 40], radius=30, fill=MID, outline=INK, width=6)   # диван
    d.rounded_rectangle([60, FEET - 260, 520, FEET - 140], radius=30, fill=LG, outline=INK, width=6)
    man(C, 'phone', u, 290, FEET - 30, 0.34)
    phone(C, 385, FEET - 330, 0.42, -10, ring=(0.6 if t - T('пишут:') < 0.6 and t > T('пишут:') else 0))
    msgbox(C, t - T('пишут:'), 700, 300, 420,
           [(T('Подработка.') - T('пишут:'), 'ПОДРАБОТКА', 'n'), (T('Примешь') - T('пишут:'), 'ПРИМИ ПЕРЕВОД', 'n'), (T('снимешь,') - T('пишут:'), 'СНИМИ', 'n'), (T('пять') - T('пишут:'), '5 000 ₽ ТВОИ', 'y')])
    if t < T('пишут:'): slam(C, u, '20 ЛЕТ', 720, 280, 160, INK)
def s_think(C, u, t):
    ground(C); man(C, 'shrug', u, 250, FEET, 0.37)
    v = t - T('Это'); card(C, 700, 330 - 14 * s_(u * 3), 380, -8 + 3 * s_(u * 2))
    slam(C, u, 'А ЧТО ТАКОГО?', 680, 90, 80)
    if v > 0: plate(C, v, 'ПРОСТО КАРТА', 700, 560, 56)
def s_stop(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); man(C, 'stop', u, 260, FEET, 0.38); slam(C, u, 'СТОП.', 650, 280, 210)
def s_tupish(C, u, t):
    ground(C); man(C, 'idle_sad', u, 250, FEET, 0.37); plate(C, u, 'ТУТ ТЫ ТУПИШЬ', 640, 300, 84, YEL)
def s_nepodrab(C, u, t):
    ground(C); man(C, 'net', u, 220, FEET, 0.36)
    slam(C, u, 'ПОДРАБОТКА', 640, 300, 110); strike(C, t - T('подработка.', 0) - 0.2, 390, 330, 900, 270, RED, 20)
def s_prachka(C, u, t):
    washer(C, 300, 380, 1.15, u, 'bills', 1.2)
    slam(C, u, 'ЭТО', 720, 200, 90); slam(C, u - 0.12, 'ПРАЧЕЧНАЯ', 720, 320, 100, INK)
    plate(C, u - 0.3, 'ДЛЯ ДЕНЕГ', 720, 450, 54)
def s_babushka(C, u, t):
    ground(C); d = ImageDraw.Draw(C)
    phone(C, 280, 340, 1.9, 0, ring=1 if t < T('украли') else 0, screen=(255, 255, 255))
    put(C, text_img('ВХОДЯЩИЙ', 24, GREY), 280, 250); put(C, text_img('«БАНК»', 50, INK), 280, 305)
    v = t - T('украли')
    if v > 0:
        for j in range(7):
            q = clamp((v - j * 0.06) / 0.7); bill(C, lerp(330, 700 + j * 40, eo(q)), lerp(420, 120 + (j % 3) * 120, eo(q)) - 120 * s_(math.pi * q), 130, q * 200 + j * 30)
        slam(C, v, 'УКРАЛИ', 700, 560, 100, RED)
    else: slam(C, u, 'У БАБУШКИ', 720, 140, 76)
def s_gryaz(C, u, t):
    for j in range(9):
        q = clamp((u - j * 0.03) / 0.3); bill(C, 160 + (j % 3) * 300, lerp(-100, 200 + (j // 3) * 160, back(q)), 220, (j * 23) % 30 - 15, dirty=4, seed=j)
    slam(C, u, 'ГРЯЗНЫЕ', 470, 640, 100, MUD)
def s_postirat(C, u, t):
    washer(C, 470, 360, 1.1, u, 'bills', 1.0, dirty=3)
    for j in range(4):
        q = clamp((u - j * 0.15) / 0.5)
        if q < 1: bill(C, lerp(900, 470, eo(q)), lerp(80, 420, eo(q)), 140 * (1 - 0.5 * q), q * 360, dirty=3, seed=j)
    slam(C, u, 'ПОСТИРАТЬ', 470, 60, 84)
def s_cep(C, u, t):
    """цепочка машин: на каждом «перевод» камера едет к следующей, купюра прыгает"""
    marks = [T('Перевод.'), T('Ещё.'), T('ещё.', 0) if False else T('И', 1)]
    step = sum(1 for m in marks if t >= m) - 1; step = max(0, step)
    k = eio(clamp((t - marks[step]) / 0.35)); pos = step - 1 + k if step > 0 else 0
    pan = pos * 330
    for j in range(5):
        x = 200 + j * 330 - pan
        if -250 < x < CW + 250: washer(C, x, 380, 0.75, u + j, 'bills', 1.4, dirty=max(0, 3 - j), hl=(j == step), label=f'ПЕРЕВОД {j + 1}')
    if step >= 0 and k < 1 and step > 0:
        bx = lerp(200 + (step - 1) * 330 - pan, 200 + step * 330 - pan, k); by = 200 - 140 * s_(math.pi * k)
        bill(C, bx, by, 120, k * 360, dirty=max(0, 3 - step))
    put(C, plate_img(['ПЕРЕВОД', 'ЕЩЁ', 'И ЕЩЁ'][step], 64, INK, YEL, pad=14, r=10), 470, 70, back((t - marks[step]) / 0.2))
def s_sled(C, u, t):
    d = ImageDraw.Draw(C)
    for j in range(9):
        x = 80 + j * 100; y = 420 + (40 if j % 2 else 0); a = clamp(1 - (j / 9) * eo(u / 0.8) * 1.4)
        if a <= 0.05: continue
        S = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); ds = ImageDraw.Draw(S)
        ds.ellipse([x - 26, y - 44, x + 26, y + 30], fill=MUD + (int(230 * a),)); ds.ellipse([x - 18, y + 36, x + 18, y + 64], fill=MUD + (int(230 * a),))
        if j > 3: S = S.filter(ImageFilter.GaussianBlur(int(2 + j * eo(u / 0.8) * 3)))
        C.alpha_composite(S)
    slam(C, u, 'СЛЕД', 470, 140, 110); slam(C, t - T('размылся.'), 'РАЗМЫЛСЯ', 470, 260, 90, MUD)
def s_posledniy(C, u, t):
    v = t - T('твоя'); washer(C, 300, 380, 1.15, u, 'card' if v > -0.3 else 'bills', 0.8, dirty=1, lit=True)
    slam(C, u, 'ПОСЛЕДНИЙ', 720, 200, 84); slam(C, u - 0.12, 'БАРАБАН', 720, 310, 96)
    if v > 0: plate(C, v, 'ТВОЯ КАРТА', 720, 450, 66)
def s_atm(C, u, t):
    ground(C); v = t - T('снимаешь,'); atm(C, 700, FEET, 1.0, cash=clamp(v / 0.4) if v > 0 else 0)
    man(C, 'reach', u, 330, FEET, 0.37)
    w = t - T('пятна'); stains(C, 330, FEET - 230, 160, clamp(w / 0.6) if w > 0 else 0, seed=4)
    if w > 0: slam(C, w, 'ПЯТНА — НА ТЕБЕ', 470, 70, 76, MUD)
def s_camera(C, u, t):
    d = ImageDraw.Draw(C); z = 1 + 0.04 * u
    man(C, 'idle_sad', u, 395, FEET + 330, 0.72 * z)
    corners(C, 150, 60, 640, 660, RED, 70, 10)
    if int(u * 3) % 2 == 0: d.ellipse([180, 90, 214, 124], fill=RED)
    put(C, text_img('REC', 40, RED), 260, 108)
    cctv(C, 830, 220, 0.8, u)
    slam(C, t - T('твоё'), 'ТВОЁ ЛИЦО', 790, 480, 76)
    v = t - T('Не', 0)
    if v > 0: plate(C, v, 'НЕ ИХ', 790, 600, 56, RED, WHITE)
def s_podvoh(C, u, t):
    ground(C); man(C, 'scratch', u, 230, FEET, 0.37); tape(C, u, 'А ВОТ И ПОДВОХ', 250, 130, -4)
    pop(C, u - 0.25, '?!', 760, 470, 200, YEL, rot=12, stroke=INK, sw=8)
def s_mln(C, u, t):
    d = ImageDraw.Draw(C); n = int(clamp(u / 1.6) * 900); rnd = random.Random(5)
    for j in range(n):
        x = 5 + (j % 60) * 15.5 + rnd.random() * 4; y = 300 + (j // 60) * 24
        if y > 690: break
        d.rounded_rectangle([x - 5, y, x + 5, y + 7], radius=2, fill=(40, 40, 44)); d.rectangle([x - 3, y + 2, x - 1, y + 4], fill=YEL)
    v = t - T('миллион'); val = roll(v, 0, 1_200_000, 0.9) if v > 0 else 0
    slam(C, u, 'ТАКИХ, КАК ТЫ', 470, 60, 60, GREY)
    if v > 0: txt(C, num(val), 470, 170, 140, INK, 1 + 0.2 * (1 - eo(v / 0.15)))
    src(C, 'выявленные дропы, Банк России, сентябрь 2025', 260)
def s_ivanovo(C, u, t):
    clipping(C, u, 'ИВАНОВО', '21 ГОД', '3 ГОДА КОЛОНИИ', 'по данным СМИ, апрель 2026', t - T('три') if t > T('три') else None)
def s_tolyatti(C, u, t):
    clipping(C, u, 'ТОЛЬЯТТИ', '20 ЛЕТ', '1 ГОД 2 МЕС. КОЛОНИИ', 'по данным СМИ, сентябрь 2026', t - T('год', 1) if t > T('год', 1) else None)
def s_statya(C, u, t):
    ground(C); man(C, 'reach', u, 220, FEET, 0.36)
    v = t - T('отдал'); k = eo(clamp(v / 0.5)) if v > 0 else 0
    card(C, lerp(400, 820, k), lerp(380, 300, k), 220, -10 + 20 * k)
    d = ImageDraw.Draw(C)   # чужая тёмная рука справа
    d.rounded_rectangle([900 - 40 * k, 270, 1100, 330], radius=30, fill=(60, 60, 64))
    slam(C, u, 'ДАЖЕ ЕСЛИ ПРОСТО', 600, 70, 64, INK)
    w = t - T('статья.')
    if w > 0: stamp(C, w, 'СТ. 187 УК РФ', 560, 520, 84, RED, -8)
def s_5000(C, u, t):
    d = ImageDraw.Draw(C); v = t - T('подработка.', 1); k = back(u / 0.25)
    cr = clamp(v / 0.25) if v > 0 else 0
    put(C, plate_img('5 000 ₽', 150, YEL, INK, pad=40, r=40, border=INK, bw=10), 470, 300, k, 4 * s_(u * 9) * (1 - cr) + (8 if cr else 0))
    if cr > 0:
        zz = [(360, 160), (420, 240), (390, 300), (470, 360), (440, 430), (520, 470)]; m = max(2, int(len(zz) * cr))
        d.line(zz[:m], fill=INK, width=12, joint='curve'); d.line([(520, 200), (560, 280), (600, 300)][:max(2, int(3 * cr))], fill=INK, width=10)
    slam(C, u, 'ЗА ПЕРЕВОД', 470, 560, 80, INK)
def s_cena(C, u, t):
    ground(C); man(C, 'sad', u, 300, FEET, 0.37)
    bars(C, clamp((u - 0.1) / 0.35), 120, 520)
    slam(C, u - 0.3, 'ЦЕНА', 760, 220, 100); slam(C, t - T('судимости.'), 'СУДИМОСТИ', 760, 340, 80, RED)
def s_nikomu(C, u, t):
    ground(C); man(C, 'cross', u, 250, FEET, 0.37)
    card(C, 700, 300, 300, 6)
    d = ImageDraw.Draw(C)   # замок
    d.arc([660, 370, 760, 470], 180, 360, fill=INK, width=18); d.rounded_rectangle([640, 420, 780, 540], radius=14, fill=YEL, outline=INK, width=8)
    slam(C, u, 'КАРТУ И КОДЫ', 680, 70, 70); v = t - T('никому.')
    if v > 0: plate(C, v, 'НИКОМУ', 700, 620, 60, RED, WHITE)
def s_bank(C, u, t):
    ground(C); man(C, 'stop' if t > T('не', 2) else 'idle', u, 250, FEET, 0.37)
    for j in range(3):
        q = clamp((u - j * 0.1) / 0.4); bill(C, lerp(1000, 640 + j * 50, eo(q)), 250 + j * 30, 150, -10 + j * 8)
    put(C, text_img('?', 150, MUD), 860, 180, back(u / 0.3))
    v = t - T('не', 2)
    if v > 0: plate(C, v, 'НЕ ТРОГАЙ', 700, 430, 64, RED, WHITE)
    w = t - T('звони')
    if w > 0: phone(C, 520, 300, 0.6, 10, ring=1); plate(C, w, 'ЗВОНИ В БАНК', 700, 560, 60)
def s_gde(C, u, t):
    washer(C, 300, 380, 1.1, u, 'water', 0.5)
    pop(C, u - 0.1, '?', 300, 450, 220, YEL, stroke=INK, sw=10)
    slam(C, u, 'А ГДЕ САМА', 720, 230, 80); slam(C, u - 0.15, 'ПРАЧЕЧНАЯ?', 720, 350, 84, INK)
def s_tc(C, u, t):
    d = ImageDraw.Draw(C); z = 1 + 0.05 * u
    d.rectangle([0, 600, CW, CH], fill=LG)
    d.rectangle([90, 120, 850, 600], fill=(236, 238, 240), outline=INK, width=10)       # витрина
    d.rectangle([90, 60, 850, 130], fill=INK); put(C, text_img('БУТИК', 44, YEL), 470, 96)
    for x in (300, 640): d.line([x, 130, x, 600], fill=INK, width=8)
    d.rectangle([660, 300, 830, 600], fill=(200, 205, 210), outline=INK, width=6)       # дверь
    for (x, y) in [(150, 260), (190, 260), (230, 260)]: d.line([x, y - 60, x, y + 60], fill=MID, width=4); d.line([x - 20, y - 60, x + 20, y - 60], fill=MID, width=4)
    d.line([130, 200, 280, 200], fill=INK, width=6)
    v = t - T('никогда')
    if v > 0:   # в витрине мерцает барабан
        a = 0.5 + 0.5 * s_(v * 10); S = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); washer(S, 470, 380, 0.7, u, 'bills', 1.5, dirty=3)
        S.putalpha(S.getchannel('A').point(lambda q: int(q * (0.35 + 0.5 * a)))); C.alpha_composite(S)
        plate(C, v, 'НИКОГДА НЕТ ЛЮДЕЙ', 470, 660, 52)
    man(C, 'walkR', u, lerp(-80, 140, clamp(u / 1.5)), 700, 0.2)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи.'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 250, FEET, 0.38)
    else: man(C, 'walkR', e, 250 - e * 420, FEET, 0.38, flip=True)
    slam(C, u, 'ВСЁ.', 660, 200, 190)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 660, 430, 150, INK, YEL)
    ground(C, col=(230, 190, 0))

def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_divan, 'none', 'thud'),
 SH(T('И', 0) - 0.05, s_think, 'push', 'bass'),
 SH(T('Стоп.') - 0.05, s_stop, 'drop', 'scratch'), SH(T('Тут') - 0.05, s_tupish, 'zoom', 'error'),
 SH(T('Это', 1) - 0.05, s_nepodrab, 'cut', 'swipe'), SH(T('Это', 2) - 0.05, s_prachka, 'zoomthru', 'boom', (640, 300)),
 SH(T('Где-то') - 0.05, s_babushka, 'bodywipe', 'whoosh'), SH(T('Грязные.') - 0.05, s_gryaz, 'drop', 'thud'),
 SH(T('Их') - 0.05, s_postirat, 'zoomthru', 'zoomin', (470, 360)),
 SH(T('Перевод.') - 0.05, s_cep, 'push', 'bass'),
 SH(T('Чтобы') - 0.05, s_sled, 'whipR', 'whoosh'),
 SH(T('А', 0) - 0.03, s_posledniy, 'zoomthru', 'boom', (470, 300)), SH(T('Ты', 0) - 0.05, s_atm, 'door', 'thud'),
 SH(T('Потому') - 0.05, s_camera, 'zoom', 'zoomin'),
 SH(T('А', 1) - 0.03, s_podvoh, 'glitch', 'scratch'), SH(T('Таких,') - 0.05, s_mln, 'push', 'bass'),
 SH(T('Иваново,') - 0.05, s_ivanovo, 'drop', 'thud'), SH(T('Тольятти,') - 0.05, s_tolyatti, 'whipL', 'whoosh'),
 SH(T('Даже') - 0.05, s_statya, 'bodywipe', 'whoosh'),
 SH(T('Пять', 0) - 0.05, s_5000, 'zoomthru', 'boom', (560, 520)), SH(T('Это', 3) - 0.05, s_cena, 'drop', 'thud'),
 SH(T('Карту') - 0.05, s_nikomu, 'push', 'whoosh'), SH(T('Пришли') - 0.05, s_bank, 'zoom', 'bass'),
 SH(T('А', 2) - 0.03, s_gde, 'door', 'thud'), SH(T('Посмотри') - 0.05, s_tc, 'zoomthru', 'zoomin', (300, 450)),
 SH(T('Всё.') - 0.05, s_netupi, 'zoomthru', 'final', (470, 400)),
]
ACC = [(T('пишут:'), 'msg'), (T('Подработка.'), 'pop'), (T('Примешь'), 'pop'), (T('снимешь,', 0), 'pop'), (T('пять'), 'coins'),
       (T('Это'), 'pop'), (T('подработка.', 0) + 0.2, 'swipe'), (T('прачечная.'), 'pop'), (T('украли'), 'whoosh'),
       (T('Ещё.'), 'tick'), (T('И', 1), 'tick'), (T('размылся.'), 'swipe'), (T('твоя'), 'ding'), (T('снимаешь,'), 'kassa'),
       (T('пятна'), 'crack'), (T('твоё'), 'click'), (T('Не', 0), 'error'), (T('миллион'), 'tick2'), (T('три'), 'stamp'), (T('год', 1), 'stamp'),
       (T('отдал'), 'swipe'), (T('статья.'), 'stamp'), (T('подработка.', 1), 'crack'), (T('судимости.'), 'clang'), (T('никому.'), 'error'),
       (T('не', 2), 'error'), (T('звони'), 'notif'), (T('никогда'), 'shine'), (T('тупи.'), 'stamp')]
PAUZY = []; BX, BY, BW_, BH = 60, 250, 860, 330
def in_pause(t): return None
ACTION = {'push', 'zoomthru', 'door', 'bodywipe', 'drop'}; PRE, POST = 0.10, 0.30
@lru_cache(4)
def disc_img(text):
    lines = text.split('\n'); ims = [text_img(l, 30, (40, 40, 40)) for l in lines]
    w = max(i.width for i in ims) + 40; h = sum(i.height + 8 for i in ims) + 24
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=12, fill=YEL)
    y = 14
    for i in ims: im.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height + 8
    return im
D1 = 'ВСЕ ПЕРСОНАЖИ ВЫМЫШЛЕНЫ. РОЛИК ОСНОВАН НА ОТКРЫТЫХ\nИСТОЧНИКАХ И НЕ ЯВЛЯЕТСЯ ИНСТРУКЦИЕЙ'
D2 = 'ВИДЕО ПРЕДУПРЕЖДАЕТ О МОШЕННИЧЕСКИХ СХЕМАХ.\nИСТОЧНИКИ — В ОПИСАНИИ'
def disclaimer(F, t):
    if t < 5.0: a = clamp(t / 0.3) * clamp((5.0 - t) / 0.4); put(F, disc_img(D1), 540, 1478, 1, 0, a)
    elif t > DUR - 3.0: a = clamp((t - DUR + 3.0) / 0.3); put(F, disc_img(D2), 540, 1478, 1, 0, a)
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
    put(L, text_img('ПОДРАБОТКА ЗА 5 000 ₽', 68, WHITE), 540, 372); put(L, text_img('ИЛИ СУДИМОСТЬ?', 84, YEL), 540, 462)
    return L

# ================= v2: глубина (параллакс, тени, наезд), переходы через действие, зерно =================
CARD_RGB = Image.new('RGB', (CW, CH), CARD)
BUS_SC = set()
GRID_SC = {s_cep, s_mln, s_ivanovo, s_tolyatti, s_5000}
def _pattern(kind, layer):
    W2 = CW * 2; im = Image.new('RGBA', (W2, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(7 + layer)
    if kind == 'city':
        if layer == 0:
            x = 0
            while x < W2:
                w = rnd.randint(70, 150); h = rnd.randint(120, 300); d.rectangle([x, BY + BH + 50 - h, x + w - 8, BY + BH + 50], fill=(236, 234, 228))
                for wy in range(BY + BH + 50 - h + 20, BY + BH + 30, 34):
                    for wx in range(x + 12, x + w - 20, 26): d.rectangle([wx, wy, wx + 10, wy + 14], fill=(244, 242, 238))
                x += w
        else:
            for x in range(0, W2, 300): d.rectangle([x, 120, x + 12, BY + BH + 55], fill=(222, 219, 212)); d.rectangle([x - 40, 120, x + 52, 132], fill=(222, 219, 212))
    elif kind == 'grid':
        col = (238, 236, 231) if layer == 0 else (233, 231, 225); st = 54 if layer == 0 else 160
        for x in range(0, W2, st): d.line([x, 0, x, CH], fill=col, width=2 if layer == 0 else 3)
        for y in range(0, CH, st): d.line([0, y, W2, y], fill=col, width=2 if layer == 0 else 3)
    else:
        if layer == 0:
            for x in range(0, W2, 46):
                for y in range(0, CH, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
        else:
            for j in range(14):
                x = rnd.randint(0, W2); y = rnd.randint(0, CH); r = rnd.randint(60, 150); d.ellipse([x - r, y - r, x + r, y + r], fill=(241, 239, 234))
    return im
PAT = {(k, l): _pattern(k, l) for k in ('city', 'grid', 'dots') for l in (0, 1)}
SPEED = {'city': (40, 150), 'grid': (18, 45), 'dots': (14, 50)}
def depth(C, fn, u):
    """сцена на белом → фон с параллаксом + мягкая тень + лёгкий наезд переднего плана"""
    rgb = C.convert('RGB'); diff = ImageChops.difference(rgb, CARD_RGB).convert('L')
    small = diff.resize((CW // 4, CH // 4), Image.BILINEAR)
    if small.point(lambda v: 255 if v > 8 else 0).histogram()[255] > 0.8 * (CW // 4) * (CH // 4): return C      # жёлтый/чёрный фон — без параллакса
    m = diff.point(lambda v: 0 if v < 2 else min(255, v * 60))
    kind = 'city' if fn in BUS_SC else 'grid' if fn in GRID_SC else 'dots'
    out = Image.new('RGBA', (CW, CH), CARD + (255,))
    for l in (0, 1):
        off = int(u * SPEED[kind][l]) % CW; out.alpha_composite(PAT[(kind, l)].crop((off, 0, off + CW, CH)))
    z = 1 + 0.03 * clamp(u / 1.5)
    sh = m.resize((CW // 4, CH // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((CW, CH), Image.BILINEAR)
    shadow = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.2)))
    fg = C.copy(); fg.putalpha(m)
    if z > 1.001:
        w, h = int(CW * z), int(CH * z); ox, oy = (w - CW) // 2, (h - CH) // 2
        fg = fg.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH)); shadow = shadow.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH))
    out.alpha_composite(shadow, (14, 16)); out.alpha_composite(fg); return out
SHIFT = 70   # сцены рисовались вокруг x=470; сдвиг ставит их строго по центру кадра (540)
def center(C):
    out = Image.new('RGBA', (CW, CH)); out.paste(C, (SHIFT, 0))
    out.paste(C.crop((0, 0, 1, CH)).resize((SHIFT, CH)), (0, 0)); return out
def card_of(j, t):
    sh = SHOTS[j]; u = max(0.0, t - sh['t']); tt = max(t, sh['t'])
    C = Image.new('RGBA', (CW, CH), CARD + (255,)); sh['fn'](C, u, tt); return depth(center(C), sh['fn'], u)

def tr_push(A, B, k, t):
    e = eio(k); v = s_(math.pi * k); out = Image.new('RGBA', (CW, CH), CARD + (255,)); x = int(CW * (1 - e))
    out.alpha_composite(hblur(A, 1 + 24 * v), (x - CW, 0)); out.alpha_composite(hblur(B, 1 + 24 * v), (x, 0))
    man(out, 'push', t * 1.4, x + 120, FEET, 0.4); return out
def tr_zoomthru(A, B, k, p):
    s = 1 + 11 * ei(clamp(k / 0.75)); cx, cy = lerp(p[0], CW / 2, eo(k)), lerp(p[1], CH / 2, eo(k))
    box = (p[0] - cx / s, p[1] - cy / s, p[0] + (CW - cx) / s, p[1] + (CH - cy) / s)
    a = A.crop(tuple(int(b) for b in box)).resize((CW, CH), Image.BILINEAR)
    if s > 1.5:   # размытие движения: два слоя с разным зумом
        s2 = s * 0.82; box2 = (p[0] - cx / s2, p[1] - cy / s2, p[0] + (CW - cx) / s2, p[1] + (CH - cy) / s2)
        a = Image.blend(a, A.crop(tuple(int(b) for b in box2)).resize((CW, CH), Image.BILINEAR), 0.45)
    zb = 0.7 + 0.3 * eo(k); w, h = int(CW * zb), int(CH * zb)
    out = Image.new('RGBA', (CW, CH), BLK + (255,)); out.alpha_composite(B.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2))
    al = 1 - clamp((k - 0.4) / 0.3)
    if al > 0: a = a.copy(); a.putalpha(int(255 * al)); out.alpha_composite(a)
    return out
def door_panel(w, left):
    im = Image.new('RGBA', (w + 30, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0 = 0 if left else 30
    d.rectangle([x0, 0, x0 + w, CH], fill=(214, 226, 236), outline=INK, width=12)
    d.rounded_rectangle([x0 + 50, 60, x0 + w - 50, 400], radius=20, fill=(176, 196, 214), outline=INK, width=8)
    d.polygon([(x0 + 80, 380), (x0 + 200, 80), (x0 + 250, 80), (x0 + 130, 380)], fill=(205, 220, 232))
    ex = x0 + w - 14 if left else x0 + 14; d.rectangle([ex - 14, 0, ex + 14, CH], fill=INK)
    d.rounded_rectangle([x0 + w / 2 - 70, 470, x0 + w / 2 + 70, 494], radius=12, fill=INK)
    sh = Image.new('RGBA', (30, CH), (0, 0, 0, 70)); im.alpha_composite(sh, (w if left else 0, 0)); return im
DP = (door_panel(CW // 2, True), door_panel(CW // 2, False))
def tr_door(A, B, k):
    c = eo(k / 0.42) if k < 0.5 else 1 - eio((k - 0.58) / 0.42) if k > 0.58 else 1
    out = (A if k < 0.5 else B).copy(); w = int(CW / 2 * c)
    if w > 0:
        out.alpha_composite(DP[0], (w - CW // 2, 0)); out.alpha_composite(DP[1], (CW - w - 30, 0))
    return out
def tr_bodywipe(A, B, k, t):
    x = int(lerp(-260, CW + 260, eio(k))); out = A.copy()
    if x > 0: out.paste(B.crop((0, 0, min(CW, x), CH)), (0, 0))
    man(out, 'walkR', t, x, CH + 520, 1.25); return out
def tr_drop(A, B, k):
    y = int(-CH * (1 - back(k))); out = Image.new('RGBA', (CW, CH), BLK + (255,))
    z = 1 - 0.06 * k; w, h = int(CW * z), int(CH * z); a = A.resize((w, h), Image.BILINEAR)
    out.alpha_composite(a, ((CW - w) // 2, (CH - h) // 2)); out.alpha_composite(Image.new('RGBA', (CW, CH), (0, 0, 0, int(120 * k))))
    v = abs(s_(math.pi * min(1, k * 1.3))); b = vblur(B, 1 + 26 * v)
    out.alpha_composite(b, (0, y)); return out

def card_at(t):
    i, sh = shot_at(t); j = None
    W_ = lambda q: {'door': (0.18, 0.42)}.get(SHOTS[q]['tr'], (PRE, POST))
    if i + 1 < len(SHOTS) and SHOTS[i + 1]['tr'] in ACTION and SHOTS[i + 1]['t'] - t < W_(i + 1)[0]: j = i + 1
    elif sh['tr'] in ACTION and t - sh['t'] < W_(i)[1] and i > 0: j = i
    if j is not None:
        pr, po = W_(j); k = clamp((t - (SHOTS[j]['t'] - pr)) / (pr + po)); A, B = card_of(j - 1, t), card_of(j, t); tr = SHOTS[j]['tr']
        if tr == 'push': C = tr_push(A, B, k, t)
        elif tr == 'zoomthru': C = tr_zoomthru(A, B, k, SHOTS[j]['p'])
        elif tr == 'door': C = tr_door(A, B, k)
        elif tr == 'bodywipe': C = tr_bodywipe(A, B, k, t)
        else: C = tr_drop(A, B, k)
        return C, i, sh, True
    C = card_of(i, t); C = transform(C, t - sh['t'], sh['tr'], i); return C, i, sh, False
rndg = random.Random(11)
GRAIN = []
for g in range(6):
    n = Image.effect_noise((WD // 2, HT // 2), 40).resize((WD, HT), Image.NEAREST)
    L = Image.merge('RGBA', (n, n, n, Image.new('L', (WD, HT), 16))); GRAIN.append(L)
VIG = Image.new('L', (CW, CH), 0); ImageDraw.Draw(VIG).rectangle([0, 0, CW, CH], fill=0)
_v = Image.new('L', (CW // 8, CH // 8), 255); ImageDraw.Draw(_v).ellipse([-10, -10, CW // 8 + 10, CH // 8 + 10], fill=0); VIG = _v.resize((CW, CH), Image.BILINEAR).filter(ImageFilter.GaussianBlur(20))
def frame(t):
    F = title_layer().copy(); C, i, sh, act = card_at(t); u = t - sh['t']
    pz = in_pause(t)
    if pz is not None:   # пауза: медленный наезд и виньетка, всё затихает
        z = 1 + 0.08 * eio(pz); w, h = int(CW * z), int(CH * z); C = C.resize((w, h), Image.BICUBIC).crop(((w - CW) // 2, (h - CH) // 2, (w - CW) // 2 + CW, (h - CH) // 2 + CH))
        dark = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); dark.putalpha(VIG.point(lambda v: int(v * 0.4 * min(1, pz * 3)))); C.alpha_composite(dark)
    elif not act and i + 1 < len(SHOTS):
        r = SHOTS[i + 1]['t'] - t
        if r < 0.07 and SHOTS[i + 1]['tr'] not in {'cut', 'none'} | ACTION:
            z = 1 + 0.1 * (1 - r / 0.07); w, h = int(CW * z), int(CH * z); C2 = Image.new('RGBA', (CW, CH)); C2.paste(C.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2)); C = C2
    F.paste(C.convert('RGB'), (0, CY0))
    if not act and u < 0.07 and sh['tr'] not in ('none', 'cut'):
        fl = Image.new('RGBA', (CW, CH), (255, 255, 255, int(150 * (1 - u / 0.07)))); F.alpha_composite(fl, (0, CY0))
    subs(F, t)
    disclaimer(F, t)
    if t < 0.35:
        k = eo(t / 0.35); F2 = Image.new('RGBA', (WD, HT), BLK + (255,)); F2.paste(F.crop((0, 250, WD, 530)), (0, int(250 - 60 * (1 - k)))); F2.paste(F.crop((0, 530, WD, HT)), (0, 530)); F = Image.blend(Image.new('RGBA', (WD, HT), BLK + (255,)), F2, 0.3 + 0.7 * k)
    F.alpha_composite(GRAIN[int(t * FPS) % 6])
    out = F.convert('RGB')
    if not act and u < 0.1 and sh['tr'] in ('shake', 'glitch', 'zoom'): out = rgbsplit(out, 10 * (1 - u / 0.1))
    return out

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        frac = float(a[1]) if len(a) > 1 else 0.6; ims = []
        for j, sh in enumerate(SHOTS):
            t1 = SHOTS[j + 1]['t'] if j + 1 < len(SHOTS) else DUR - 0.8; tt = sh['t'] + (t1 - sh['t']) * frac
            ims.append(card_of(j, tt).convert('RGB').resize((360, 240)))
        cols = 5; rows = (len(ims) + cols - 1) // cols
        for part in range(0, rows, 5):
            S = Image.new('RGB', (cols * 364, min(5, rows - part) * 244), (90, 90, 90))
            for j, im in enumerate(ims[part * cols:(part + 5) * cols]): S.paste(im, ((j % cols) * 364, (j // cols) * 244))
            S.save(f'sheet_{frac}_{part // 5}.png')
    elif a:
        for x in a: frame(float(x)).save(f'prev_{x}.png')
    else:
        ev = [(round(s['t'], 3), s['sfx']) for s in SHOTS if s['sfx']] + [(round(t, 3), n) for t, n in ACC]
        json.dump(dict(dur=DUR, ev=sorted(ev)), open('sfx.json', 'w'))
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', os.environ.get('OUT', 'video_noaudio.mp4')], stdin=subprocess.PIPE)
        lo, hi = (int(os.environ.get('F0', 0)), int(os.environ.get('F1', N)))
        for i in range(lo, hi):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 150 == 0: print(i, N, flush=True)
        p.stdin.close(); p.wait(); print('done')
