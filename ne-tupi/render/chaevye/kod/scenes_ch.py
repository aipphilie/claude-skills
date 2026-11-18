"""Предметы и персонажи рилса «Чаевые — это налог». Движок «Привычек богатых» (весь экран, белый фон, переходы через действие)."""
from scenes_bg import *
GREENB = (60, 150, 90); SHIP = (60, 64, 76); TRAIN = (120, 40, 40); TRAIND = (84, 26, 26); HAND = INK

# ---------- персонажи ----------
def waiter(C, clip, u, cx, s=0.4, feet=None, flip=False, rot=0): man(C, 'w_' + clip, u, cx, feet or G, s, flip=flip, rot=rot)
def aristo(C, clip, u, cx, s=0.4, feet=None, flip=False): man(C, 'h_' + clip, u, cx, feet or G, s, flip=flip)

# ---------- предметы ----------
@lru_cache(16)
def dcoin_img(r):
    im = Image.new('RGBA', (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([4, 4, r * 2 + 4, r * 2 + 4], fill=YEL, outline=INK, width=max(3, r // 7)); d.ellipse([4 + r * 0.25, 4 + r * 0.25, 4 + r * 1.75, 4 + r * 1.75], outline=(214, 170, 0), width=max(2, r // 10))
    d.text((r + 4, r + 6), '$', font=font(int(r * 1.15)), fill=INK, anchor='mm'); return im
def dcoin(C, cx, cy, r=40, rot=0, scale=1.0): put(C, dcoin_img(int(r)), cx, cy, scale, rot)
def dflow(C, u, x0, y0, x1, y1, n=5, r=30, hgt=160):
    for j in range(n):
        q = (u * 1.2 + j / n) % 1; dcoin(C, lerp(x0, x1, q), lerp(y0, y1, q) - hgt * s_(math.pi * q), r, q * 360)
def dstack(C, cx, by, n, r=60):
    d = D(C)
    for j in range(n):
        y = by - j * r * 0.34; d.ellipse([cx - r, y - r * 0.62, cx + r, y], fill=(226, 184, 0), outline=INK, width=5); d.ellipse([cx - r, y - r * 0.78, cx + r, y - r * 0.16], fill=YEL, outline=INK, width=5)
@lru_cache(32)
def check_img(w, lines, total, tsz, hl):
    rows = len(lines); h = int(w * 0.32 + rows * w * 0.16 + (w * 0.42 if total else 0)); im = Image.new('RGBA', (w + 12, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    zz = [(6, 6)]; n = 12
    for j in range(n + 1): zz.append((6 + w * j / n, h + (18 if j % 2 else 0)))
    zz.append((w + 6, 6)); d.polygon(zz, fill=WHITE, outline=INK); d.line(zz + [zz[0]], fill=INK, width=7)
    t = text_img('ЧЕК', int(w * 0.12), INK); im.alpha_composite(t, ((w + 12 - t.width) // 2, int(w * 0.06)))
    y = int(w * 0.24); d.line([w * 0.08, y, w * 0.92, y], fill=LG, width=5); y += int(w * 0.04)
    for k, (a, b) in enumerate(lines):
        if hl is not None and k == hl: d.rounded_rectangle([w * 0.05, y - 4, w * 0.95, y + w * 0.13], radius=10, fill=YEL)
        ta = text_img(a, int(w * 0.075), INK); im.alpha_composite(ta, (int(w * 0.09), y + int(w * 0.02)))
        tb = text_img(b, int(w * 0.085), INK); im.alpha_composite(tb, (int(w * 0.91) - tb.width + 6, y + int(w * 0.015))); y += int(w * 0.16)
    if total:
        d.line([w * 0.08, y + 6, w * 0.92, y + 6], fill=INK, width=5); tt = text_img(total, tsz or int(w * 0.26), RED); im.alpha_composite(tt, ((w + 12 - tt.width) // 2, y + int(w * 0.06)))
    return im
def check(C, cx, cy, w, lines=(), total=None, rot=0, scale=1.0, tsz=None, hl=None): put(C, check_img(int(w), tuple(lines), total, tsz, hl), cx, cy, scale, rot)
def tray(C, cx, cy, w=150):
    d = D(C); d.ellipse([cx - w / 2, cy - w * 0.1, cx + w / 2, cy + w * 0.1], fill=STEEL, outline=INK, width=5)
    d.pieslice([cx - w * 0.3, cy - w * 0.45, cx + w * 0.3, cy + w * 0.15], 180, 360, fill=(200, 204, 210), outline=INK, width=5); d.ellipse([cx - 8, cy - w * 0.32, cx + 8, cy - w * 0.32 + 16], fill=INK)
def bowler(C, cx, cy, w=170, up=True):
    """шляпа-котелок дном вниз — в неё кидают монеты"""
    d = D(C); h = w * 0.55
    if up:
        d.chord([cx - w * 0.38, cy - h * 0.2, cx + w * 0.38, cy + h], 0, 180, fill=(70, 62, 56), outline=INK, width=6)
        d.ellipse([cx - w / 2, cy - h * 0.25, cx + w / 2, cy + h * 0.25], fill=(90, 80, 72), outline=INK, width=6); d.ellipse([cx - w * 0.36, cy - h * 0.15, cx + w * 0.36, cy + h * 0.15], fill=(40, 36, 32))
def kassa(C, cx, by, s=1.0, locked=0.0, val='$'):
    d = D(C); w, h = 300 * s, 200 * s
    d.rounded_rectangle([cx - w / 2, by - h, cx + w / 2, by], radius=int(16 * s), fill=STEEL, outline=INK, width=8)
    d.rectangle([cx - w / 2 - 14 * s, by - 50 * s, cx + w / 2 + 14 * s, by], fill=STEEL2, outline=INK, width=7)
    d.rounded_rectangle([cx - w * 0.3, by - h - 90 * s, cx + w * 0.3, by - h + 6], radius=int(10 * s), fill=INK); put(C, text_img(val, int(56 * s), YEL), cx, by - h - 42 * s)
    for r in range(2):
        for c in range(4): d.rounded_rectangle([cx - w * 0.38 + c * w * 0.2, by - h + 30 * s + r * 50 * s, cx - w * 0.38 + c * w * 0.2 + w * 0.14, by - h + 62 * s + r * 50 * s], radius=6, fill=WHITE, outline=INK, width=4)
    if locked > 0: lock(C, cx, by - 30 * s, 0.6 * s, back(locked / 0.25), -6)
def steamer(C, cx, by, s=1.0, u=0):
    d = D(C); w = 620 * s; bob = 8 * s_(u * 4) * s; by = by + bob
    d.polygon([(cx - w / 2, by - 140 * s), (cx + w / 2 + 40 * s, by - 140 * s), (cx + w / 2 - 30 * s, by), (cx - w / 2 + 40 * s, by)], fill=SHIP, outline=INK)
    d.line([(cx - w / 2, by - 140 * s), (cx + w / 2 + 40 * s, by - 140 * s), (cx + w / 2 - 30 * s, by), (cx - w / 2 + 40 * s, by), (cx - w / 2, by - 140 * s)], fill=INK, width=8)
    d.rectangle([cx - w / 2 + 10, by - 110 * s, cx + w / 2 + 20 * s, by - 96 * s], fill=RED)
    d.rectangle([cx - w * 0.32, by - 240 * s, cx + w * 0.3, by - 140 * s], fill=WHITE, outline=INK, width=7)
    for j in range(6): d.ellipse([cx - w * 0.27 + j * w * 0.095, by - 205 * s, cx - w * 0.27 + j * w * 0.095 + 30 * s, by - 175 * s], fill=WIN, outline=INK, width=4)
    for x in (-0.12, 0.12):
        d.rectangle([cx + w * x - 30 * s, by - 380 * s, cx + w * x + 30 * s, by - 240 * s], fill=RED, outline=INK, width=7); d.rectangle([cx + w * x - 30 * s, by - 380 * s, cx + w * x + 30 * s, by - 350 * s], fill=INK)
        for j in range(3):
            q = (u * 0.7 + j / 3) % 1; r = (30 + 50 * q) * s; d.ellipse([cx + w * x - r + q * 120 * s, by - 400 * s - q * 260 * s - r, cx + w * x + r + q * 120 * s, by - 400 * s - q * 260 * s + r], fill=(220, 220, 220))
def railcar(C, cx, by, w=900, u=0, label='ПОЕЗД'):
    d = D(C); h = 330; y0 = by - h - 60
    d.rounded_rectangle([cx - w / 2, y0, cx + w / 2, by - 60], radius=30, fill=TRAIN, outline=INK, width=9)
    d.rectangle([cx - w / 2, y0 + 40, cx + w / 2, y0 + 56], fill=YEL)
    for j in range(5): d.rounded_rectangle([cx - w / 2 + 50 + j * (w - 100) / 5, y0 + 80, cx - w / 2 + 50 + j * (w - 100) / 5 + (w - 100) / 5 - 40, y0 + 190], radius=12, fill=WIN, outline=INK, width=6)
    put(C, text_img(label, 50, YEL), cx, y0 + 250)
    for x in (-0.36, -0.22, 0.22, 0.36):
        r = 46; xc = cx + w * x; d.ellipse([xc - r, by - 60 - r + 10, xc + r, by - 60 + r + 10], fill=INK); a = u * 9; d.line([xc, by - 50, xc + math.cos(a) * r * 0.8, by - 50 + math.sin(a) * r * 0.8], fill=GREY, width=8)
    d.line([0, by, CW, by], fill=STEEL2, width=12)
def placard(C, cx, cy, w, text, rot=0, tear=0.0, u=0):
    """плакат на палке; tear>0 — рвётся пополам, половинки улетают"""
    h = w * 0.62; im = Image.new('RGBA', (int(w) + 12, int(h) + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([6, 6, w + 6, h + 6], fill=WHITE, outline=INK, width=8); t = text_img(text, int(h * 0.36), RED); im.alpha_composite(t, ((im.width - t.width) // 2, (im.height - t.height) // 2))
    if tear <= 0:
        D(C).line([cx, cy + h * 0.4, cx, cy + h * 1.6], fill=WOODD, width=16); put(C, im, cx, cy, 1, rot); return
    k = eo(tear); L = im.crop((0, 0, im.width // 2, im.height)); R = im.crop((im.width // 2, 0, im.width, im.height))
    put(C, L, cx - im.width / 4 - 360 * k, cy - 500 * k * k, 1, rot + 60 * k); put(C, R, cx + im.width / 4 + 420 * k, cy - 380 * k * k, 1, rot - 80 * k)
    rnd = random.Random(5)
    for j in range(10):
        a = rnd.uniform(0, 6.28); dd = 600 * k * rnd.uniform(0.5, 1.2); x = cx + math.cos(a) * dd + 500 * k; y = cy + math.sin(a) * dd * 0.6 - 200 * k
        D(C).polygon([(x, y), (x + 30, y + 8), (x + 10, y + 34)], fill=WHITE, outline=INK)
def bighand(C, x0, y0, x1, y1, w=120):
    """огромная рука клиента в стиле человечка: толстый столбик с полукруглым концом"""
    d = D(C); d.line([x0, y0, x1, y1], fill=HAND, width=int(w)); d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=HAND)
def qmark(C, cx, cy, sz, u, col=INK): txt(C, '?', cx, cy + 10 * s_(u * 6), sz, col, 1, 8 * s_(u * 4))
def capitol(C, cx, by, s=1.0, u=0):
    d = D(C); w = 700 * s
    d.rectangle([cx - w / 2, by - 40 * s, cx + w / 2, by], fill=STONE, outline=INK, width=8)
    d.rectangle([cx - w * 0.42, by - 300 * s, cx + w * 0.42, by - 40 * s], fill=WHITE, outline=INK, width=8)
    for j in range(7): x = cx - w * 0.36 + j * w * 0.12; d.rectangle([x - 14 * s, by - 290 * s, x + 14 * s, by - 50 * s], fill=STONE, outline=INK, width=4)
    d.polygon([(cx - w * 0.46, by - 300 * s), (cx + w * 0.46, by - 300 * s), (cx, by - 400 * s)], fill=STONE, outline=INK); d.line([(cx - w * 0.46, by - 300 * s), (cx + w * 0.46, by - 300 * s), (cx, by - 400 * s), (cx - w * 0.46, by - 300 * s)], fill=INK, width=8)
    d.rectangle([cx - w * 0.16, by - 470 * s, cx + w * 0.16, by - 400 * s], fill=WHITE, outline=INK, width=7)
    d.pieslice([cx - w * 0.2, by - 640 * s, cx + w * 0.2, by - 330 * s], 180, 360, fill=WHITE, outline=INK, width=8)
    d.rectangle([cx - 6 * s, by - 720 * s, cx + 6 * s, by - 640 * s], fill=INK); usflag(C, cx + 60 * s, by - 690 * s, 110 * s, u)
