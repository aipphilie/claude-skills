"""СДВГ-монтаж «Почему он не пускает близко»: чёрный кадр, заголовок, белая карточка-сцена, субтитр под ней.
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
@lru_cache(4000)
def text_img(text, sz, fill=INK, stroke=None, sw=0, sp=0):
    f = font(sz); lines = text.split('\n'); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bb = [d0.textbbox((0, 0), l, font=f, stroke_width=sw) for l in lines]
    lh = int(sz * 1.12); w = max(b[2] - b[0] for b in bb) + 8 + sw * 2; h = lh * len(lines) + int(sz * 0.3) + sw * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, b) in enumerate(zip(lines, bb)):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], i * lh + sw), l, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
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
def man(C, clip, u, cx, feet=FEET, s=0.36, flip=False, rot=0, alpha=1.0, frame=None, sx=1.0, sy=1.0):
    n = CLIPS[clip]; i = frame if frame is not None else int(max(0, u) * 24) % n
    im = _frame(clip, i); w, h = int(800 * s * sx), int(1460 * s * sy)
    if w < 2 or h < 2: return
    im = im.resize((w, h), Image.LANCZOS if s < 0.8 else Image.BICUBIC)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if alpha < 1: im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    if rot:
        big = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0)); big.alpha_composite(im, (w // 2, int(h - FY * s * sy)))   # центр вращения = ступни
        big = big.rotate(rot, Image.BICUBIC); C.alpha_composite(big, (int(cx - w), int(feet - h)))
    else: C.alpha_composite(im, (int(cx - w / 2), int(feet - FY * s * sy)))
HEAD = lambda s: 1040 * s      # высота макушки над ступнями (примерно)

# ================= СЦЕНЫ =================  fn(C, u, t): u — время от начала сцены, t — абсолютное
def s_zamechal(C, u, t):
    k = eo(u / 0.22); y = lerp(-200, FEET, k) if u < 0.22 else FEET - 26 * abs(s_((u - 0.22) * 14)) * math.exp(-(u - 0.22) * 6)
    hole(C, 210, FEET + 4, 150 * clamp(u / 0.2), 26); man(C, 'idle', u, 210, y, 0.37, sy=1 - 0.12 * math.exp(-max(0, u - 0.22) * 14) if u > 0.22 else 1)
    slam(C, u - 0.16, 'ЗАМЕЧАЛ', 640, 370, 124); pop(C, u - 0.42, '?', 850, 170, 230, YEL, rot=-14 + 6 * s_(u * 10), stroke=INK, sw=8)
def s_dolshe(C, u, t):
    ground(C); man(C, 'cross', u, 300, FEET, 0.37)
    txt(C, '«ЧЕМ ДОЛЬШЕ ОДИН…»', 640, 130, 74)
    yrs = ['1 ГОД', '2 ГОДА', '3 ГОДА', '5 ЛЕТ', '7 ЛЕТ', '10 ЛЕТ']; i = min(len(yrs) - 1, int(u / 0.22)); k = (u - i * 0.22) / 0.22
    d = ImageDraw.Draw(C); d.rounded_rectangle([470, 230, 830, 560], radius=22, fill=WHITE, outline=INK, width=8); d.rounded_rectangle([470, 230, 830, 300], radius=22, fill=RED, outline=INK, width=8)
    for x in (540, 760): d.rounded_rectangle([x - 10, 205, x + 10, 255], radius=8, fill=INK)
    txt(C, yrs[i], 650, 425, 118, INK, 1 + 0.5 * (1 - eo(k * 2.5)))
    for j in range(4):   # улетающие листки
        q = (u * 2.2 + j * 0.27) % 1; put(C, plate_img('  ', 40, WHITE, INK, border=INK, bw=4), 840 + q * 260, 330 - q * 260 + j * 30, 1 - q * 0.5, q * 300, 1 - q)
def big_arm(C, x0, y0, x1, y1, label=None, w=96):
    d = ImageDraw.Draw(C); d.line([x0, y0, x1, y1], fill=INK, width=w); d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=INK)
    d.arc([x1 - w * 1.5, y1 - w * 0.5, x1 + w * 0.3, y1 + w * 1.7], 90, 270, fill=INK, width=int(w * 0.55))
    if label: put(C, plate_img(label, 50, YEL, INK, pad=14, r=8), (x0 + x1) / 2 + 90, (y0 + y1) / 2, 1, math.degrees(math.atan2(y0 - y1, x1 - x0)) + 180)
def s_zatashit(C, u, t):
    speedlines(C, 540, 380, u, r0=420, col=LG); ground(C)
    k = eo(u / 0.18); pull = 40 * s_(u * 9) * clamp(u / 0.3); mx = 500 + pull + 60 * clamp(u / 1.2)
    big_arm(C, 1200, 250, lerp(1200, mx + 150, k), 390, 'ОТНОШЕНИЯ')
    man(C, 'scared', u, mx, FEET, 0.37, rot=14 + 5 * s_(u * 9))
    slam(C, u - 0.05, 'ТЕМ СЛОЖНЕЕ', 250, 80, 66); slam(C, t - T('затащить'), 'ЗАТАЩИТЬ', 250, 170, 86, RED)
def s_votn(C, u, t):
    ground(C); k = eo(u / 0.25)
    big_arm(C, 1200, 250, lerp(620, 1150, k), lerp(390, 300, k), 'ОТНОШЕНИЯ')
    man(C, 'jump' if u < 0.5 else 'hips', u, lerp(480, 250, k), FEET, 0.37)
    for j in range(7): a = j * 0.9; r = 60 + u * 520; put(C, plate_img(' ', 16, INK, INK, pad=5, r=5), 560 + math.cos(a) * r, 380 + math.sin(a) * r * 0.6, 1, u * 700 + j * 40, 1 - clamp(u / 0.7))
    burst(C, 590, 380, 120 * (1 - clamp(u / 0.35)) + 1, u) if u < 0.35 else None
    slam(C, u - 0.1, 'НЕ ДАЁТСЯ', 640, 150, 110)
def s_net(C, u, t):
    speedlines(C, 540, 360, u, r0=470, col=LG, n=34)
    man(C, 'net', u, 190, FEET + 60, 0.5); slam(C, u, 'И НЕТ.', 660, 320, 210, INK); strike(C, u - 0.3, 440, 450, 880, 450, YEL, 22)
def s_lyubov(C, u, t):
    ground(C); man(C, 'idle_smile', u, 200, FEET, 0.37)
    b = 1 + 0.12 * abs(s_(u * 9)); heart(C, 400, 200 - 20 * s_(u * 4), 62 * b * back(u / 0.25))
    slam(C, u - 0.05, 'ЛЮБОВЬ', 690, 250, 112, RED); slam(C, t - T('нужна'), 'НУЖНА', 650, 390, 130)
    v = t - T('нужна') - 0.15
    if v > 0:
        d = ImageDraw.Draw(C); k = eo(v / 0.2); pts = [(820, 520), (855, 560), (925, 460)]
        d.line([pts[0], (lerp(820, 855, clamp(k * 2)), lerp(520, 560, clamp(k * 2)))], fill=(40, 180, 90), width=22)
        if k > 0.5: d.line([pts[1], (lerp(855, 925, k * 2 - 1), lerp(560, 460, k * 2 - 1))], fill=(40, 180, 90), width=22)
def s_sloman(C, u, t):
    ground(C); v = t - T('сломанный')
    man(C, 'idle' if v < 0.25 else 'shrug', u, 300, FEET, 0.37)
    if v < 0.25: stamp(C, u - 0.05, 'СЛОМАН', 330, 330, 96, RED, -14)
    else:
        q = v - 0.25; put(C, text_img('СЛОМАН', 96, RED), 330 + q * 1500, 330 - q * 500, 1, -14 - q * 900, 1 - clamp(q / 0.5))
        slam(C, q, 'НЕ', 610, 250, 150, INK); slam(C, q - 0.08, 'СЛОМАННЫЙ', 700, 400, 104, INK); strike(C, q - 0.25, 480, 470, 920, 470, YEL, 20)
def s_blizost(C, u, t):
    ground(C); gx = lerp(-80, 330, eo(u / 0.6))
    man(C, 'g_walk' if u < 0.6 else 'g_wave', u, gx, FEET, 0.37, flip=u < 0.6); man(C, 'idle', u, 720, FEET, 0.37, flip=True)
    for j in range(3): q = (u * 1.3 + j / 3) % 1; heart(C, gx + 110 + q * 190, 360 - q * 150 - 20 * s_(q * 9 + j), 14 + 16 * q)
    slam(C, u - 0.1, 'БЛИЗОСТЬ', 520, 110, 120, PINK)
def s_radar(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); d = ImageDraw.Draw(C); cx, cy = 700, 340
    for r in (90, 170, 250): d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 200, 90), width=4)
    d.line([cx - 260, cy, cx + 260, cy], fill=(40, 200, 90), width=2); d.line([cx, cy - 260, cx, cy + 260], fill=(40, 200, 90), width=2)
    a = u * 7; d.pieslice([cx - 250, cy - 250, cx + 250, cy + 250], math.degrees(a) - 28, math.degrees(a), fill=(30, 120, 60))
    bl = 0.5 + 0.5 * s_(u * 26); r = 16 + 14 * bl; d.ellipse([cx + 110 - r, cy - 90 - r, cx + 110 + r, cy - 90 + r], fill=RED); heart(C, cx + 110, cy - 90, 12, WHITE)
    C.paste(CARD, [0, 0, 440, CH]); man(C, 'shock', u, 220, FEET + 20, 0.4)
    slam(C, u, 'ДЛЯ НЕГО', 220, 80, 84, INK); pop(C, u - 0.3, 'ОБНАРУЖЕНА ЦЕЛЬ', cx, 660, 44, (40, 200, 90))
def s_ugroza(C, u, t):
    if int(u * 14) % 2 == 0 and u < 0.45: C.paste((255, 225, 225), [0, 0, CW, CH])
    speedlines(C, 300, 420, u, r0=330); man(C, 'scared', u, 300, FEET + 40, 0.42, rot=6)
    tape(C, u, '⚠ УГРОЗА ⚠'.replace('⚠', '!'), 560, 120, -5); tape(C, u - 0.1, '! ! ! ! ! ! ! ! ! ! ! !', 80, 70, 4)
    slam(C, u - 0.12, 'БЛИЗОСТЬ', 690, 240, 104); slam(C, u - 0.25, '= УГРОЗА', 690, 370, 130, RED)
def s_godami(C, u, t):
    d = ImageDraw.Draw(C)
    for j in range(12):   # бегущие годы
        x = 60 + ((j * 190 - u * 900) % 1300) - 100; txt(C, str(2014 + j), x, 620, 60, LG)
    man(C, 'hips', u, 250, FEET - 70, 0.33)
    slam(C, u, 'ГОДАМИ', 640, 190, 170); slam(C, t - T('сам'), 'САМ', 640, 400, 210, YEL, stroke=INK, sw=8)
def rubble(C, cx, by, n, seed, spread=260, hgt=230, col=INK):
    rnd = random.Random(seed); d = ImageDraw.Draw(C)
    for j in range(n):
        x = cx + (rnd.random() - 0.5) * spread * 2; mh = hgt * (1 - abs(x - cx) / spread); y = by - rnd.random() * max(8, mh); r = 22 + rnd.random() * 30
        d.regular_polygon((x, y, r), 5 + j % 3, rotation=rnd.random() * 90, fill=col if j % 5 else (60, 60, 60))
def s_razgrebal(C, u, t):
    ground(C); k = clamp(u / 1.5); rubble(C, 240, FEET, int(60 * (1 - 0.6 * k)), 5, 230, 330 * (1 - 0.5 * k))
    put(C, plate_img('ПРОБЛЕМЫ', 44, WHITE, INK, pad=10, r=6, border=INK, bw=5), 230, 470 + 80 * k, 1, -8)
    man(C, 'dig', u, 420, FEET, 0.36, flip=True)
    d = ImageDraw.Draw(C); rnd = random.Random(2)
    for j in range(12):   # летящие куски
        q = (u * 1.7 + rnd.random()) % 1; x = 470 + q * (350 + rnd.random() * 250); y = 520 - s_(q * math.pi) * (260 + rnd.random() * 160) + q * 90
        d.regular_polygon((x, y, 14 + rnd.random() * 16), 5, rotation=q * 500, fill=INK)
    slam(C, u, 'САМ', 790, 100, 140); slam(C, u - 0.12, 'РАЗГРЕБАЛ', 790, 215, 72, RED)
def s_tashil(C, u, t):
    d = ImageDraw.Draw(C); d.polygon([(0, CH), (CW, 430), (CW, CH)], fill=INK)
    k = eio(clamp(u / 1.6)); x = lerp(260, 520, k); y = CH - (x / CW) * (CH - 430) + 4
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im, 'push', u, x, y, 0.33)
    C.alpha_composite(im)
    bx = x + 215; by = CH - (bx / CW) * (CH - 430) - 6; sh = 4 * s_(u * 22)
    box(C, bx, by, 190, 130, 'ДОЛГИ', -15); box(C, bx + 40 + sh, by - 138, 170, 115, 'РАБОТА', -12 + sh); box(C, bx + 70 - sh, by - 262, 150, 100, 'НЕРВЫ', -18 - sh)
    slam(C, u, 'САМ', 200, 90, 130); slam(C, u - 0.12, 'ТАЩИЛ ВСЁ', 200, 195, 70, RED)
def s_dno(C, u, t):
    C.paste(INK, [0, 430, CW, CH]); d = ImageDraw.Draw(C)
    k = eio(clamp(u / 1.5)); y = lerp(FEET + 420, FEET - 90, k)
    for j in range(9): xx = 180 + j * 12; d.line([300 + (j % 3 - 1) * 40, 0, 300 + (j % 3 - 1) * 40, 60 + ((u * 900 + j * 97) % 380)], fill=LG, width=5)
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im, 'climb', u, 300, y, 0.36); im.paste((0, 0, 0, 0), [0, 470, CW, CH]); C.alpha_composite(im)
    d.ellipse([130, 400, 470, 470], fill=INK); im2 = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im2, 'climb', u, 300, y, 0.36); im2.paste((0, 0, 0, 0), [0, 440, CW, CH]); C.alpha_composite(im2)
    txt(C, 'ДНО', 300, 600, 110, (50, 50, 50))
    slam(C, u, 'САМ', 730, 110, 150); slam(C, u - 0.12, 'ВЫТАСКИВАЛ', 730, 240, 84, RED); slam(C, t - T('дна'), 'СО ДНА', 730, 560, 110, WHITE)
def s_odin(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); d = ImageDraw.Draw(C); z = 1 - 0.12 * clamp(u / 0.75)
    d.polygon([(540 - 60, 0), (540 + 60, 0), (540 + 250 * z, FEET + 20), (540 - 250 * z, FEET + 20)], fill=(250, 249, 246)); d.ellipse([540 - 250 * z, FEET - 20, 540 + 250 * z, FEET + 60], fill=(250, 249, 246))
    man(C, 'sad', u, 540, FEET + 10, 0.27 * z); slam(C, u, 'ОДИН.', 540, 180, 170, YEL, stroke=INK, sw=10)
def s_snova(C, u, t):
    ground(C); d = ImageDraw.Draw(C); cx, cy, r = 320, 400, 235; a0 = u * 420
    for q in (0, 180):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0 + q, a0 + q + 140, fill=YEL, width=34)
        a = math.radians(a0 + q + 140); px, py = cx + math.cos(a) * r, cy + math.sin(a) * r; tx, ty = -math.sin(a), math.cos(a)
        d.polygon([(px + tx * 55, py + ty * 55), (px + math.cos(a) * 45, py + math.sin(a) * 45), (px - math.cos(a) * 45, py - math.sin(a) * 45)], fill=YEL)
    clip = ['dig', 'push', 'climb', 'carry'][int(u / 0.2) % 4]; man(C, clip, u, cx, FEET, 0.3)
    v = t - T('снова.', 0) if True else 0
    slam(C, u, 'СНОВА', 760, 200, 130); slam(C, t - T('и', 0 + 0) if False else u - 0.4, 'И', 760, 340, 110, GREY); slam(C, u - 0.56, 'СНОВА', 760, 480, 130, RED)
def s_norma(C, u, t):
    ground(C); man(C, 'hips', u, 230, FEET, 0.37)
    txt(C, 'ПОКА ЭТО НЕ СТАЛО', 650, 140, 66)
    v = t - T('нормой')
    if 0 < v < 0.3: burst(C, 650, 380, 300 * eo(v / 0.2), v, fill=YEL)
    stamp(C, v, 'НОРМА', 650, 380, 124, INK, -8)
def milo_card(C, cx, cy, sc=1.0, rot=0, alpha=1.0):
    im = Image.new('RGBA', (300, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([4, 4, 295, 355], radius=26, fill=(255, 226, 236), outline=INK, width=7)
    heart(im, 150, 150, 70, PINK); heart(im, 60, 60, 20, HRT); heart(im, 245, 80, 16, HRT); heart(im, 240, 250, 22, HRT)
    im.alpha_composite(text_img('«ОЙ, КАК\nМИЛО»', 46, INK), (150 - text_img('«ОЙ, КАК\nМИЛО»', 46, INK).width // 2, 245))
    put(C, im, cx, cy, sc, rot, alpha)
def s_milo(C, u, t):
    ground(C); man(C, 'idle_sad', u, 740, FEET, 0.37, flip=True)
    v = t - T('ой,');
    if v < 0.5: milo_card(C, 300, 380 + 8 * s_(u * 6), back(u / 0.25), -8 + 3 * s_(u * 5))
    else: q = v - 0.5; milo_card(C, 300 - q * 1300, 380 - q * 500, 1, -8 + q * 900, 1 - clamp(q / 0.5))
    txt(C, 'ЛЮБОВЬ — УЖЕ НЕ', 520, 90, 84); slam(C, v - 0.62, 'ЭТО РИСК', 300, 380, 120, RED, rot=-8)
    xcross(C, v - 0.15, 300, 380, 150, RED, 22) if v < 0.5 else None
def s_otkryt(C, u, t):
    # крупно: торс с сейфовой дверью
    C.paste(INK, [170, 0, 590, CH]); d = ImageDraw.Draw(C)
    v = t - T('открыться'); k = eio(clamp(v / 0.35)) if v > 0 else 0
    x0, y0, x1, y1 = 240, 200, 520, 560; HX = 380
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(40, 40, 40))
    if k > 0:
        heart(C, HX, 380, 80 * (1 + 0.1 * abs(s_(u * 10))))
        for j in range(10): a = j * 0.63; d.line([HX + math.cos(a) * 110, 380 + math.sin(a) * 110, HX + math.cos(a) * 150, 380 + math.sin(a) * 150], fill=YEL, width=7)
    w = (x1 - x0) * (1 - 0.82 * k)
    d.polygon([(x0, y0), (x0 + w, y0 - 30 * k), (x0 + w, y1 + 30 * k), (x0, y1)], fill=STEEL, outline=INK, width=7)
    for yy in (y0 + 40, y1 - 40): d.ellipse([x0 + w * 0.08, yy - 10, x0 + w * 0.08 + 20 * (1 - 0.8 * k), yy + 10], fill=STEEL2)
    cxw, r = x0 + w * 0.55, 62 * (1 - 0.3 * k); a0 = u * (5 if v < 0 else 0)
    d.ellipse([cxw - r * (1 - 0.8 * k), 380 - r, cxw + r * (1 - 0.8 * k), 380 + r], outline=INK, width=12, fill=STEEL2)
    for j in range(4): a = a0 + j * math.pi / 2; d.line([cxw, 380, cxw + math.cos(a) * r * 1.3 * (1 - 0.8 * k), 380 + math.sin(a) * r * 1.3], fill=INK, width=12)
    slam(C, u, 'ЭТО СНОВА', 770, 270, 80, INK); slam(C, v, 'ОТКРЫТЬСЯ', 770, 400, 84, RED)
    txt(C, 'СНОВА', 170, 390, 70, YEL, stroke=INK, sw=5) if False else None
def door(C, cx, k, open_=0.0, hgt=500, wdt=230):
    d = ImageDraw.Draw(C); top = FEET + 6 - hgt * k
    d.rectangle([cx - wdt / 2 - 14, top - 14, cx + wdt / 2 + 14, FEET + 6], fill=INK)
    d.rectangle([cx - wdt / 2, top, cx + wdt / 2, FEET + 6], fill=(255, 240, 180) if open_ > 0.05 else MID)
    ow = wdt * (1 - 0.8 * open_)
    d.polygon([(cx - wdt / 2, top), (cx - wdt / 2 + ow, top + 36 * open_), (cx - wdt / 2 + ow, FEET + 6 - 14 * open_), (cx - wdt / 2, FEET + 6)], fill=(232, 228, 220), outline=INK, width=6)
    d.ellipse([cx - wdt / 2 + ow - 40, top + hgt * 0.5, cx - wdt / 2 + ow - 18, top + hgt * 0.5 + 22], fill=INK)
def s_vpustit(C, u, t):
    ground(C); v = t - T('впустить'); o = eio(clamp((u - 0.1) / 0.5))
    door(C, 230, 1, o)
    if o > 0.3: im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im, 'g_wave', u, 270, FEET, 0.31, alpha=1); im.paste((0, 0, 0, 0), [0, 0, 150 + int(230 * (1 - 0.8 * o)) - 115 + 115, CH]) if False else None; C.alpha_composite(im)
    man(C, 'scared' if v > 0 else 'idle', u, 730, FEET, 0.33, flip=True)
    slam(C, u, 'СНОВА', 640, 70, 90, INK); slam(C, v, 'КОГО-ТО ВПУСТИТЬ', 660, 165, 60, RED)
def s_kusok(C, u, t):
    speedlines(C, 420, 380, u, r0=400, col=LG)
    man(C, 'carry', u, 300, FEET + 380, 0.8)
    v = t - T('кусок'); q = clamp(v / 0.5) if v > 0 else 0
    heart(C, 520, 400, 150, HRT, rot=-6 + 3 * s_(u * 14), bite=1 if v > 0 else 0)
    if v > 0:
        im = Image.new('RGBA', (360, 360), (0, 0, 0, 0)); heart(im, 180, 180, 150, HRT); m = Image.new('L', (360, 360), 0); c, r = 180, 150
        ImageDraw.Draw(m).polygon([(c + r * 0.15, c - r * 0.1), (c + r * 1.2, c - r * 0.9), (c + r * 1.2, c + r * 0.6), (c + r * 0.45, c + r * 0.5), (c + r * 0.6, c + r * 0.2)], fill=255)
        im.putalpha(ImageChops.multiply(im.getchannel('A'), m)); put(C, im, 520 + 40 + eo(q) * 230, 400 - eo(q) * 120, 1, -eo(q) * 40)
        burst(C, 640, 380, 90 * (1 - q) + 1, u, fill=WHITE) if q < 0.5 else None
    slam(C, u, 'СНОВА ОТДАТЬ', 730, 90, 80); slam(C, v, 'КУСОК СЕБЯ', 760, 620, 100, RED)
def s_gremliny(C, u, t):
    ground(C); man(C, 'idle_sad' if t < T('расставания') else 'scared', u, 480, FEET, 0.37)
    for nm, (x, y, r), lab in [('обиды', (190, 330, 62), 'ОБИДЫ'), ('ссоры', (790, 250, 66), 'ССОРЫ'), ('расставания', (760, 520, 58), 'РАССТАВАНИЯ')]:
        v = t - T(nm)
        if v > 0:
            sc = back(v / 0.2);
            if v < 0.25: burst(C, x, y, r * 2.4 * (1 - v / 0.25) + 1, v, fill=YEL)
            gremlin(C, x, y, r * sc, u, lab, seed=x)
    txt(C, 'А СТАРЫЕ…', 480, 70, 70)
def s_nedelis(C, u, t):
    speedlines(C, 480, 400, u, r0=420, col=LG); man(C, 'scared', u, 480, FEET, 0.37)
    for (x, y, r), lab in [((190, 330, 62), 'ОБИДЫ'), ((790, 250, 66), 'ССОРЫ'), ((760, 520, 58), 'РАССТАВАНИЯ')]:
        gremlin(C, x + 14 * s_(u * 30 + x), y + 10 * s_(u * 26 + y), r * (1.1 + 0.08 * s_(u * 20)), u, lab, seed=x)
    slam(C, u, 'НИКУДА НЕ ДЕЛИСЬ', 500, 90, 104, INK, stroke=WHITE, sw=10)
def s_upakoval(C, u, t):
    ground(C); man(C, 'carry', u, 480, FEET, 0.37)
    P = [(190, 0.0, 'НЕ ОТКРЫВАТЬ'), (780, 0.18, 'НЕ ТРОГАТЬ'), (480 + 300, 9, '')]
    for j, (x, dl, lab) in enumerate([(190, 0.0, 'НЕ ОТКРЫВАТЬ'), (790, 0.2, 'НЕ ТРОГАТЬ'), (640, 0.4, 'ХРУПКОЕ')]):
        v = u - dl
        if v < 0: gremlin(C, x, FEET - 90, 56, u, None, seed=x); continue
        k = eo(v / 0.16); y = lerp(-200, FEET, k);
        if v < 0.16: gremlin(C, x, FEET - 90, 56, u, None, seed=x)
        box(C, x, y, 230 if j < 2 else 170, 190 if j < 2 else 130, lab, 3 * s_(v * 30) * math.exp(-v * 5), sz=22)
        if 0.16 < v < 0.36: burst(C, x, FEET - 10, 190 * (v - 0.16) / 0.2 + 30, v, fill=LG, outline=LG, n=10)
    slam(C, t - T('упаковал'), 'УПАКОВАЛ', 480, 110, 120);
def s_ubral(C, u, t):
    ground(C); k = ei(clamp(u / 0.45)); man(C, 'point' if u > 0.3 else 'carry', u, 190, FEET, 0.37)
    for j, (x, lab) in enumerate([(430, 'НЕ ОТКРЫВАТЬ'), (520, 'НЕ ТРОГАТЬ'), (470, 'ХРУПКОЕ')]):
        kk = ei(clamp((u - j * 0.08) / 0.4)); bx = x + kk * 900; by = FEET - (j == 2) * 190 - s_(kk * math.pi) * 120
        sc = 1 - 0.6 * kk; box(C, bx, by, 210 * sc, 170 * sc, lab if kk < 0.3 else None, -kk * 200, sz=20)
    d = ImageDraw.Draw(C)
    for j in range(8): d.line([420 + j * 30, 300 + j * 38, 420 + j * 30 + 380 * clamp(u / 0.3), 300 + j * 38], fill=LG, width=8) if u < 0.6 else None
    slam(C, u - 0.1, 'И УБРАЛ', 650, 120, 100); slam(C, t - T('подальше'), 'ПОДАЛЬШЕ', 660, 250, 112, RED)
def s_novyi(C, u, t):
    ground(C); gx = lerp(1150, 720, eo(u / 0.7)); man(C, 'idle', u, 260, FEET, 0.37)
    man(C, 'g_walk' if u < 0.7 else 'g_wave', u, gx, FEET, 0.37)
    v = t - T('новый')
    if v > 0:
        plate(C, v, 'НОВЫЙ ЧЕЛОВЕК', 560, 95, 76, YEL); d = ImageDraw.Draw(C)
        for j in range(6): a = j * 1.05 + u * 3; r = 50 + 18 * s_(u * 12 + j); x, y = gx + math.cos(a) * 170, 330 + math.sin(a) * 200; d.regular_polygon((x, y, 16 + 6 * s_(u * 9 + j)), 4, rotation=45 + u * 200, fill=YEL, outline=INK)
        for j in range(3): q = (u * 1.4 + j / 3) % 1; heart(C, gx - 110 - q * 220, 330 - q * 120, 12 + 14 * q)
    else: txt(C, 'И КАК ТОЛЬКО…', 480, 95, 70)
def head_big(C, u, lid=0.0, cx=430, bg=CARD):
    """крупно макушка человечка внизу карточки, крышка откидывается"""
    d = ImageDraw.Draw(C); cy, r = 760, 300
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    if lid > 0:
        d.rectangle([cx - r, cy - r - 4, cx + r, cy - r * 0.62], fill=bg); d.ellipse([cx - r * 0.78, cy - r * 0.72, cx + r * 0.78, cy - r * 0.5], fill=(60, 60, 60))
        im = Image.new('RGBA', (int(r * 1.7), int(r * 0.5)), (0, 0, 0, 0)); ImageDraw.Draw(im).pieslice([0, 0, r * 1.7 - 1, r * 1.0], 180, 360, fill=INK)
        put(C, im, cx - r * 0.78 - 60 * lid, cy - r * 0.7 - 110 * lid, 1, 75 * lid)
def s_mozg(C, u, t):
    speedlines(C, 430, 300, u, r0=360, col=LG); l = back(clamp(u / 0.25)); head_big(C, u, l)
    k = back((u - 0.12) / 0.25);
    if u > 0.12: brain(C, 430, lerp(620, 380, k), 110, u)
    slam(C, u, 'МОЗГ', 800, 200, 130); slam(C, t - T('орёт'), 'ОРЁТ:', 800, 350, 130, RED)
def s_stop(C, u, t):
    bg = RED if int(u * 16) % 2 == 0 and u < 0.36 else CARD; C.paste(bg, [0, 0, CW, CH])
    slam(C, u, 'СТОП!', 590, 240, 270, INK, d=0.12); head_big(C, u, 1, 300, bg); brain(C, 300, 400, 110, u, sign='СТОП')
def cards(C, cx, by, u, wob=0.0, fall=0.0):
    d = ImageDraw.Draw(C); w = 74; h = 96; rows = 3
    for r in range(rows):
        n = rows - r; y = by - r * (h + 8)
        for j in range(n):
            x = cx + (j - (n - 1) / 2) * w * 1.5 + wob * s_(u * 30 + r) * (r + 1) * 3 + fall * (j - n / 2 + 0.3 * r) * 160; yy = y + fall * fall * 420 * (0.5 + 0.2 * r)
            for sd in (-1, 1):
                d.polygon([(x + sd * w * 0.62, yy), (x + sd * w * 0.52, yy), (x, yy - h), (x + sd * w * 0.1, yy - h)], fill=WHITE, outline=INK, width=4)
            if r < rows - 1: d.line([x - w * 0.7, yy - h - 4, x + w * 0.7, yy - h - 4], fill=INK, width=7)
def s_naladil(C, u, t):
    ground(C); head_big(C, u, 1); brain(C, 430, 380, 105, u)
    cards(C, 800, FEET, u); put(C, plate_img('МОЯ ЖИЗНЬ', 40, YEL, INK, pad=10, r=6), 800, 285, back(u / 0.2), -4)
    slam(C, u, 'ТЫ ТОЛЬКО ВСЁ', 660, 65, 70); slam(C, t - T('наладил'), 'НАЛАДИЛ!', 680, 160, 96, RED)
def s_nelomai(C, u, t):
    ground(C); speedlines(C, 780, 420, u, r0=420, col=LG)
    man(C, 'stop', u, 260, FEET, 0.36); cards(C, 780, FEET, u, wob=1.0)
    plate(C, u, 'НЕ ЛОМАЙ!', 560, 105, 104, YEL)
def s_nebegaet(C, u, t):
    ground(C); d = ImageDraw.Draw(C)
    for j in range(7): y = 200 + j * 55; x = ((j * 311 - u * 1700) % 1400) - 150; d.line([x, y, x + 200, y], fill=LG, width=8)
    v = t - T('любви')
    man(C, 'walkR' if v < 0.15 else 'net', u * 2.2 if v < 0.15 else u, 590 if v < 0.15 else 590, FEET, 0.36)
    hx = 330 + 30 * s_(u * 10) if v < 0.15 else 360; heart(C, hx, 380 + 20 * s_(u * 16), 60);
    for sd in (-1, 1): d.line([hx + sd * 20, 430, hx + sd * (34 + 26 * s_(u * 28 + sd)), 500], fill=INK, width=10)
    txt(C, 'БЕГАЕТ ОТ ЛЮБВИ?', 520, 90, 96); xcross(C, v, 520, 95, 330, RED, 20) if v > 0 else None
    slam(C, v - 0.2, 'НЕТ', 880, 330, 150, RED, rot=-10)
BR = [('РАБОТА', 0), ('ДОМ', 0), ('РЕЖИМ', 0), ('ЗАЛ', 1), ('ПОКОЙ', 1), ('ДЕНЬГИ', 1), ('СОН', 2), ('ПЛАНЫ', 2), ('ДРУЗЬЯ', 2), ('ТИШИНА', 3), ('ПОРЯДОК', 3)]
def wall(C, cx, by, n, u, shake=0.0):
    d = ImageDraw.Draw(C); bw, bh = 150, 76; cnt = [0, 0, 0, 0]
    for j, (lab, r) in enumerate(BR[:n]):
        per = 3 if r < 3 else 2; i = cnt[r]; cnt[r] += 1
        x = cx + (i - (per - 1) / 2) * (bw + 6) + (r % 2) * 0 + shake * s_(u * 40 + j) * 5; y = by - r * (bh + 6)
        v = u - j * 0.1 if n == len(BR) and False else 1
        d.rounded_rectangle([x - bw / 2, y - bh, x + bw / 2, y], radius=8, fill=INK)
        put(C, text_img(lab, 34, WHITE if lab != 'ПОКОЙ' else YEL), x, y - bh / 2)
def s_pokoi(C, u, t):
    ground(C); man(C, 'scared', u, 540, FEET - 330, 0.24); wall(C, 540, FEET, 11, u, shake=1.0)
    slam(C, u, 'БОИТСЯ', 160, 180, 84, INK); slam(C, u - 0.15, 'ПОТЕРЯТЬ', 160, 280, 68, INK)
    v = t - T('покой')
    if v > 0: burst(C, 160, 440, 135, u, fill=YEL); slam(C, v, 'ПОКОЙ', 160, 440, 64, INK, rot=-8)
def s_stroil(C, u, t):
    ground(C); n = min(11, 1 + int(u / 0.12)); d = ImageDraw.Draw(C)
    wall(C, 560, FEET, n, u); rows = BR[n - 1][1]
    man(C, 'hips', u, 560, FEET - (rows + 1) * 82 + 0, 0.24) if n >= 3 else man(C, 'carry', u, 560, FEET - 82, 0.24)
    k = (u % 0.12) / 0.12
    if n < 11: burst(C, 560, FEET - (BR[n][1] + 0.5) * 82, 60 * (1 - k) + 1, u, fill=LG, outline=LG)
    for j in range(8): txt(C, str(2017 + j), 870, 140 + ((j * 90 - u * 500) % 720) - 60, 54, LG)
    slam(C, u, 'СТРОИЛ', 165, 200, 84, INK); slam(C, t - T('годами', 0), 'ГОДАМИ', 165, 310, 84, RED)
def armor(C, cx, feet, s, u, k=1.0):
    """шлем и нагрудник поверх человечка"""
    d = ImageDraw.Draw(C); hy = feet - 1250 * s; hr = 150 * s; dy = lerp(-500, 0, eo(k))
    by0 = feet - 940 * s
    d.rounded_rectangle([cx - 165 * s, by0 + dy, cx + 165 * s, by0 + 420 * s + dy], radius=int(50 * s), fill=STEEL, outline=INK, width=7)
    d.line([cx, by0 + dy + 20, cx, by0 + 420 * s + dy - 10], fill=STEEL2, width=6)
    for sd in (-1, 1): d.ellipse([cx + sd * 175 * s - 60 * s, by0 + dy - 30 * s, cx + sd * 175 * s + 60 * s, by0 + dy + 90 * s], fill=STEEL, outline=INK, width=7)
    t_ = text_img('СВОБОДА', int(58 * s), INK); put(C, t_, cx, by0 + 230 * s + dy)
    d.rounded_rectangle([cx - hr * 1.15, hy - hr * 0.2 + dy * 1.4, cx + hr * 1.15, hy + hr * 2.25 + dy * 1.4], radius=int(hr * 0.9), fill=STEEL, outline=INK, width=7)
    d.rectangle([cx - hr * 0.95, hy + hr * 0.75 + dy * 1.4, cx + hr * 0.95, hy + hr * 1.05 + dy * 1.4], fill=INK)
    for j in range(5): d.line([cx - hr * 0.6 + j * hr * 0.3, hy + hr * 1.25 + dy * 1.4, cx - hr * 0.6 + j * hr * 0.3, hy + hr * 1.9 + dy * 1.4], fill=STEEL2, width=6)
    d.polygon([(cx - 14, hy - hr * 0.2 + dy * 1.4), (cx + 14, hy - hr * 0.2 + dy * 1.4), (cx + 50, hy - hr * 0.95 + dy * 1.4), (cx - 20, hy - hr * 0.7 + dy * 1.4)], fill=RED, outline=INK)
def s_bronya(C, u, t):
    v = t - T('броня'); ground(C)
    if v > 0: speedlines(C, 330, 380, u, r0=400, col=LG)
    man(C, 'hips', u, 330, FEET, 0.4)
    if v > 0:
        armor(C, 330, FEET, 0.4, u, clamp(v / 0.14))
        if 0.12 < v < 0.4: burst(C, 330, 330, 420 * (v - 0.12) / 0.28, v, fill=None, outline=YEL, n=16)
    slam(C, t - T('свобода'), 'СВОБОДА', 730, 200, 124); slam(C, v - 0.02, '= БРОНЯ', 730, 360, 150, RED)
def pbar(C, k, cx=540, y=110):
    d = ImageDraw.Draw(C); w = 620
    d.rounded_rectangle([cx - w / 2, y - 26, cx + w / 2, y + 26], radius=26, fill=WHITE, outline=INK, width=7)
    d.rounded_rectangle([cx - w / 2 + 8, y - 18, cx - w / 2 + 8 + (w - 16) * clamp(k), y + 18], radius=18, fill=HRT if k < 0.75 else RED)
    put(C, text_img('СИМПАТИЯ', 34, INK), cx - w / 2 + 80, y - 56); put(C, text_img('СЕРЬЁЗНО', 34, INK), cx + w / 2 - 80, y - 56)
    put(C, text_img(f'{int(clamp(k) * 100)}%', 34, INK if k < 0.5 else WHITE), cx, y - 2)
def s_simpatiya(C, u, t):
    ground(C); k = 0.1 + 0.55 * clamp(u / 1.3)
    pbar(C, k); man(C, 'idle_smile', u, 380, FEET, 0.37); man(C, 'g_hugR', u, 620, FEET, 0.37, flip=True)
    b = 1 + 0.15 * abs(s_(u * 9)); heart(C, 500, 250 + 10 * s_(u * 5), (30 + 40 * k) * b)
def s_slilsya(C, u, t):
    ground(C); k = 0.65 + 0.1 * clamp(u / 0.3); v = u - 0.3; pbar(C, k)
    d = ImageDraw.Draw(C)
    if v < 0: man(C, 'shock', u, 380, FEET, 0.37)
    else:
        x = 380 + ei(clamp(v / 0.45)) * 900
        for j in range(6): d.line([330 - j * 6, 300 + j * 55, 330 + min(x - 380, 700), 300 + j * 55], fill=LG, width=9)
        man(C, 'walkR', u * 3, x, FEET, 0.37)
        for j in range(5): r = 26 + j * 12 + v * 60; d.ellipse([400 + j * 34 - r, FEET - 30 - r - j * 10, 400 + j * 34 + r, FEET - 30 + r - j * 10], fill=LG) if v < 0.9 else None
        stamp(C, t - T('серьёзным') + 0.0, 'СЛИЛСЯ', 300, 420, 100, RED, -10)
    man(C, 'g_idle' if v < 0.4 else 'g_shrug', u, 620 if v < 0.4 else 700, FEET, 0.37, flip=True)
    heart(C, 500, 250, 55, HRT if v < 0.5 else GREY, crack=clamp((v - 0.5) / 0.3) if v > 0.5 else 0)
def s_holod(C, u, t):
    ground(C); man(C, 'idle', u, 300, FEET, 0.37); d = ImageDraw.Draw(C)
    v = t - T('холодный'); cx, cy = 700, 460
    if v < 0.25:
        d.rounded_rectangle([cx - 110, cy - 110, cx + 110, cy + 110], radius=20, fill=(170, 225, 250), outline=INK, width=8); d.line([cx - 70, cy - 60, cx - 20, cy - 60], fill=WHITE, width=12); d.line([cx - 70, cy - 60, cx - 70, cy - 10], fill=WHITE, width=12)
    else:
        q = v - 0.25; rnd = random.Random(4)
        for j in range(12): a = rnd.random() * 6.28; r = q * (400 + rnd.random() * 500); d.regular_polygon((cx + math.cos(a) * r, cy + math.sin(a) * r + q * q * 600, 30 * (1 - clamp(q))), 3, rotation=q * 900 + j * 30, fill=(170, 225, 250), outline=INK) if q < 1 else None
    txt(C, 'ХОЛОДНЫЙ?', 650, 150, 110);
    if v > 0: xcross(C, v, 650, 155, 250, RED, 20); slam(C, v - 0.2, 'НЕТ', 700, 440, 190, RED, rot=-8)
def s_trus(C, u, t):
    ground(C); v = t - T('трус'); man(C, 'idle' if v < 0.1 else 'hips', u, 720, FEET, 0.37, flip=True)
    txt(C, 'ТРУС?', 340, 170, 170)
    if v > 0: xcross(C, v, 340, 180, 230, RED, 24); slam(C, v - 0.2, 'НЕТ', 330, 450, 210, RED, rot=7)
def s_znaet(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); z = 1 + 0.25 * clamp(u / 1.1)
    d = ImageDraw.Draw(C); d.ellipse([650 - 250 * z, 370 - 250 * z, 650 + 250 * z, 370 + 250 * z], fill=CARD)
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(im, 'nod', u, 650, FEET + 210 * z, 0.55 * z); m = Image.new('L', (CW, CH), 0); ImageDraw.Draw(m).ellipse([650 - 250 * z, 370 - 250 * z, 650 + 250 * z, 370 + 250 * z], fill=255)
    im.putalpha(ImageChops.multiply(im.getchannel('A'), m)); C.alpha_composite(im)
    slam(C, u, 'А ПОТОМУ\nЧТО', 190, 250, 70, WHITE); slam(C, t - T('знает'), 'ЗНАЕТ', 195, 440, 116, YEL)
def s_cena(C, u, t):
    v = t - T('разбитое'); speedlines(C, 330, 380, u, r0=380, col=LG) if v > 0 else None
    sh = 8 * s_(u * 40) * math.exp(-max(0, v) * 6) if v > 0 else 0
    heart(C, 330 + sh, 380, 190, HRT, crack=clamp(v / 0.2) if v > 0 else 0)
    d = ImageDraw.Draw(C); d.line([470, 250, 600, 350], fill=INK, width=6)
    im = Image.new('RGBA', (360, 300), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.polygon([(0, 150), (70, 20), (355, 20), (355, 280), (70, 280)], fill=YEL, outline=INK, width=8); dd.ellipse([50, 132, 86, 168], fill=CARD, outline=INK, width=6)
    q = min(9_999_999, int(ei(clamp(u / 1.0)) * 9_999_999)); pr = f'{q:,}'.replace(',', ' ')
    im.alpha_composite(text_img('ЦЕНА:', 44, INK), (120, 50)); im.alpha_composite(text_img(pr, 50, INK), (108, 122)); im.alpha_composite(text_img('НЕРВОВ', 44, RED), (120, 205))
    put(C, im, 720, 390, back(u / 0.25), -8 + 4 * s_(u * 5))
    slam(C, u, 'СКОЛЬКО СТОИТ', 650, 90, 84); slam(C, v, 'РАЗБИТОЕ СЕРДЦЕ', 560, 640, 84, RED, stroke=CARD, sw=10)
def s_uznal(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 330, 420, u, r0=380, col=(240, 196, 0))
    z = 1 + 0.5 * (1 - eo(u / 0.2)); man(C, 'pointcam', u, 320, FEET + 540, 0.85 * z)
    slam(C, u - 0.05, 'УЗНАЛ', 720, 130, 130); slam(C, t - T('себя', 2), 'СЕБЯ?', 720, 290, 160, INK)
def s_komm(C, u, t):
    ground(C); man(C, 'point', u, 260, FEET, 0.37)
    bubble(C, 660, 300, 420 * back(u / 0.22), 230 * back(u / 0.22), u)
    slam(C, u - 0.1, 'ПИШИ В КОММЕНТЫ', 650, 540, 76, RED)
    d = ImageDraw.Draw(C); y = 640 + 14 * s_(u * 14); d.polygon([(620, y - 30), (680, y - 30), (650, y + 20)], fill=INK)
CROWD = [(90, .2, 'idle'), (210, .22, 'wave'), (330, .2, 'hips'), (450, .23, 'shrug'), (570, .2, 'g_wave'), (690, .22, 'idle_smile'), (810, .2, 'scratch'), (930, .22, 'armsup'),
         (150, .27, 'g_joy'), (290, .29, 'armsup'), (430, .27, 'wave'), (650, .29, 'g_wave'), (790, .27, 'jumpjoy'), (910, .28, 'idle_smile'), (60, .3, 'idle_smile'), (540, .36, 'armsup')]
def s_vse(C, u, t):
    C.paste(YEL, [0, 0, CW, CH])
    for j, (x, sc, cl) in enumerate(CROWD):
        v = u - j * 0.035
        if v < 0: continue
        row = 0 if j < 8 else 1 if j < 15 else 2; man(C, cl, u + j * 0.3, x, FEET - 110 + row * 75 + (1 - back(v / 0.2)) * 400, sc * 1.05)
    slam(C, u, 'МЫ ТУТ ВСЕ ТАКИЕ', 520, 90, 110, INK)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи.'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 250, FEET, 0.38)
    else: man(C, 'walkR', e, 250 - e * 420, FEET, 0.38, flip=True)
    slam(C, u, 'ВСЁ.', 660, 200, 190);
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 660, 430, 150, INK, YEL)
    ground(C, col=(230, 190, 0))

# t0 сцены, функция, переход, звук склейки
def SH(t0, fn, tr='zoom', sfx='whoosh'): return dict(t=t0, fn=fn, tr=tr, sfx=sfx)
SHOTS = [
 SH(0.0, s_zamechal, 'none', 'thud'), SH(T('Чем') - 0.05, s_dolshe, 'whipL', 'tick'), SH(T('тем') - 0.05, s_zatashit, 'zoom', 'bass'), SH(T('его') - 0.05, s_votn, 'shake', 'boing'),
 SH(T('И', 0) - 0.03, s_net, 'zoom', 'boom'), SH(T('любовь') - 0.05, s_lyubov, 'whipR', 'heart'), SH(T('И', 1) - 0.03, s_sloman, 'whipL', 'stamp'),
 SH(T('Просто') - 0.05, s_blizost, 'zoom', 'whoosh'), SH(T('для') - 0.05, s_radar, 'glitch', 'alarm'), SH(T('угроза') - 0.04, s_ugroza, 'shake', 'boom'),
 SH(T('Годами') - 0.05, s_godami, 'whipR', 'bass'), SH(T('разгребал') - 0.05, s_razgrebal, 'zoom', 'whoosh'), SH(T('Сам', 0) - 0.05, s_tashil, 'whipL', 'bass'),
 SH(T('Сам', 1) - 0.05, s_dno, 'whipU', 'riser'), SH(T('Один.') - 0.08, s_odin, 'cut', 'drop'), SH(T('Снова') - 0.05, s_snova, 'spin', 'tick2'),
 SH(T('Пока') - 0.05, s_norma, 'zoom', 'whoosh'),
 SH(T('И', 2) - 0.03, s_milo, 'whipR', 'pop'), SH(T('Это') - 0.05, s_otkryt, 'zoom', 'bass'), SH(T('Снова', 1) - 0.05, s_vpustit, 'whipL', 'whoosh'),
 SH(T('Снова', 2) - 0.05, s_kusok, 'zoom', 'bass'),
 SH(T('А', 0) - 0.03, s_gremliny, 'whipR', 'whoosh'), SH(T('никуда') - 0.05, s_nedelis, 'shake', 'boom'), SH(T('Он', 0) - 0.03, s_upakoval, 'zoom', 'whoosh'),
 SH(T('убрал') - 0.12, s_ubral, 'whipL', 'swipe'),
 SH(T('И', 3) - 0.03, s_novyi, 'whipR', 'bass'), SH(T('мозг') - 0.05, s_mozg, 'zoom', 'zoomin'), SH(T('Стоп!') - 0.04, s_stop, 'shake', 'boom'),
 SH(T('Ты') - 0.04, s_naladil, 'whipL', 'whoosh'), SH(T('Не', 0) - 0.04, s_nelomai, 'zoom', 'bass'),
 SH(T('Он', 1) - 0.03, s_nebegaet, 'whipR', 'whoosh'), SH(T('Он', 2) - 0.03, s_pokoi, 'zoom', 'bass'), SH(T('который') - 0.04, s_stroil, 'whipU', 'tick2'),
 SH(T('Его') - 0.05, s_bronya, 'zoom', 'whoosh'),
 SH(T('Поэтому') - 0.05, s_simpatiya, 'whipL', 'bass'), SH(T('чем', 0) - 0.25, s_slilsya, 'cut', 'pop'), SH(T('Не', 1) - 0.04, s_holod, 'zoom', 'whoosh'),
 SH(T('Не', 2) - 0.04, s_trus, 'whipR', 'bass'), SH(T('А', 1) - 0.03, s_znaet, 'zoom', 'riser'), SH(T('сколько') - 0.04, s_cena, 'whipL', 'kassa'),
 SH(T('Узнал') - 0.05, s_uznal, 'zoom', 'boom'), SH(T('Пиши') - 0.04, s_komm, 'whipR', 'msg'), SH(T('Мы') - 0.04, s_vse, 'zoom', 'bass'),
 SH(T('Всё.') - 0.05, s_netupi, 'shake', 'final'),
]
# акценты внутри сцен (время, звук)
ACC = [(T('затащить'), 'pop'), (T('нужна') + 0.15, 'ok'), (T('сломанный'), 'stamp'), (T('сломанный') + 0.25, 'swipe'), (T('сам'), 'boom'), (T('дна'), 'pop'),
       (T('нормой'), 'stamp'), (T('ой,') + 0.5, 'swipe'), (T('открыться'), 'click'), (T('впустить'), 'pop'), (T('кусок'), 'crack'),
       (T('обиды'), 'pop'), (T('ссоры'), 'pop'), (T('расставания'), 'pop'), (T('упаковал'), 'thud'), (T('упаковал') + 0.2, 'thud'), (T('подальше'), 'pop'),
       (T('новый'), 'ding'), (T('орёт'), 'alarm'), (T('наладил'), 'pop'), (T('любви'), 'error'), (T('покой'), 'pop'), (T('броня'), 'clang'),
       (T('серьёзным') - 0.4, 'swipe'), (T('серьёзным'), 'stamp'), (T('холодный'), 'error'), (T('трус'), 'error'), (T('знает'), 'pop'), (T('разбитое'), 'crack'),
       (T('себя', 2), 'pop'), (T('такие'), 'pop'), (T('тупи.'), 'stamp')]

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
            tw = sum(im.width for im, _ in ims) + 22 * (len(ims) - 1)
            sc0 = min(1, 780 / tw); x = 540 - tw * sc0 / 2; k0 = back((t - ch[0][1] + 0.04) / 0.14)
            for im, sc in ims:
                put(F, im, x + im.width * sc0 / 2, SUB_Y + (1 - k0) * 30, sc * sc0); x += (im.width + 22) * sc0
            return

# ---------- кадр ----------
@lru_cache(1)
def title_layer():
    L = Image.new('RGBA', (WD, HT), BLK + (255,))
    put(L, text_img('ПОЧЕМУ ОН НЕ ПУСКАЕТ', 68, WHITE), 540, 372); put(L, text_img('ТЕБЯ БЛИЗКО', 84, YEL), 540, 462)
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
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        lo, hi = (int(os.environ.get('F0', 0)), int(os.environ.get('F1', N)))
        for i in range(lo, hi):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 150 == 0: print(i, N, flush=True)
        p.stdin.close(); p.wait(); print('done')
