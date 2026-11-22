"""База движка (из compose_d.py): рисовалки, человечек, простые переходы. Кадр 1080x1920 целиком, без чёрных полос."""
import json, math, sys, subprocess, random, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from words import W, END, wt
FPS = 30; DUR = round(END + 2.6, 2); N = int(DUR * FPS); WD, HT = 1080, 1920
CW, CH, CY0 = 1080, 1920, 0            # карточка
FEET = 1270
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
FB_ = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; ALT = set('₽→✓₿≈…')
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
CROP = (0, 200, 1080, 1660); FY = 1412      # ноги в кропе
@lru_cache(90)
def _frame(clip, i): return Image.open(f'{HERE}/kadry/{clip}/{i:03d}.png').convert('RGBA').crop(CROP)
@lru_cache(260)
def _scaled(clip, i, w, h, flip):
    im = _frame(clip, i).resize((w, h), Image.LANCZOS if w < 640 else Image.BICUBIC)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
def man(C, clip, u, cx, feet=FEET, s=0.36, flip=False, rot=0, alpha=1.0, frame=None, sx=1.0, sy=1.0):
    n = CLIPS[clip]; i = frame if frame is not None else int(max(0, u) * 24) % n
    w, h = int(1080 * s * sx), int(1460 * s * sy)
    if w < 2 or h < 2: return
    im = _scaled(clip, i, w, h, flip)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    if rot:
        big = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0)); big.alpha_composite(im, (w // 2, int(h - FY * s * sy)))   # центр вращения = ступни
        big = big.rotate(rot, Image.BICUBIC); C.alpha_composite(big, (int(cx - w), int(feet - h)))
    else: C.alpha_composite(im, (int(cx - w / 2), int(feet - FY * s * sy)))
HEAD = lambda s: 1040 * s      # высота макушки над ступнями (примерно)

GREEN = (40, 170, 90); BILL = (150, 200, 140); BILLD = (90, 140, 85); MUD = (120, 84, 48); MUD2 = (150, 110, 70)
def num(v): return f'{int(round(v)):,}'.replace(',', ' ')
def roll(u, a, b, d=0.6): return lerp(a, b, eo(u / d))
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

def phone(C, cx, cy, s=1.0, rot=0, ring=0.0, screen=None):
    im = Image.new('RGBA', (int(130 * s) + 10, int(240 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 130 * s + 4, 240 * s + 4], radius=int(22 * s), fill=INK)
    d.rounded_rectangle([12 * s, 22 * s, 122 * s, 216 * s], radius=int(12 * s), fill=WHITE if not screen else screen)
    put(C, im, cx + (6 * s_(ring * 60) if ring else 0), cy, 1, rot)
    if ring:
        dd = ImageDraw.Draw(C)
        for j in range(3):
            rr = (60 + j * 34) * s; dd.arc([cx - rr, cy - rr, cx + rr, cy + rr], -50, 50, fill=INK, width=max(3, int(6 * s))); dd.arc([cx - rr, cy - rr, cx + rr, cy + rr], 130, 230, fill=INK, width=max(3, int(6 * s)))

def corners(C, x0, y0, x1, y1, col=RED, L=60, w=10):
    d = ImageDraw.Draw(C)
    for (x, y, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([x, y, x + sx * L, y], fill=col, width=w); d.line([x, y, x, y + sy * L], fill=col, width=w)

# ---------- переход: трансформация карточки в первые ~0.2 сек сцены ----------
def hblur(im, k):
    if k < 2: return im
    w, h = im.size; return im.resize((max(1, int(w / k)), h), Image.BILINEAR).resize((w, h), Image.BILINEAR)
def vblur(im, k):
    if k < 2: return im
    w, h = im.size; return im.resize((w, max(1, int(h / k))), Image.BILINEAR).resize((w, h), Image.BILINEAR)
def transform(C, u, tr, seed):
    D = 0.2; out = Image.new('RGBA', (CW, CH), CARD + (255,)); k = clamp(u / D); rnd = random.Random(seed * 100 + int(u * FPS))
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

