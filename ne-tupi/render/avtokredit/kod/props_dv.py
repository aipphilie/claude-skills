"""Предметы (из «Кредита»). Движок «Квартиры» (compose_k.py): кадр на весь экран 1080x1920, белый фон, без чёрных полос.
python3 compose_kr.py 1.5 12.3 -> prev_*.png;  python3 compose_kr.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from base_k import *
SKY = (214, 230, 240); BRICK = (203, 98, 74); BRICKD = (160, 70, 52); PANEL = (214, 217, 222); WIN = (176, 204, 224); WOOD = (196, 150, 100); WOODD = (150, 108, 66)
WALL = (244, 236, 220); PAPER = (250, 246, 232); SEAL = (60, 90, 170); DARK = (52, 58, 72)
G = FEET; TY = 420
def D(C): return ImageDraw.Draw(C)
def layer(): return Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
def src(C, text, y=1318): put(C, text_img(text, 30, GREY), 540, y)

# ---------- предметы ----------
def block(C, cx, by, w, h, cols=4, rows=6, col=PANEL, lit=0.0, seed=1, door=True):
    d = D(C); x0 = cx - w / 2; y0 = by - h
    d.rectangle([x0, y0, x0 + w, by], fill=col, outline=INK, width=8); d.rectangle([x0 - 10, y0 - 18, x0 + w + 10, y0], fill=INK)
    rnd = random.Random(seed); cw = w / cols; rh = h / (rows + 0.6)
    for r in range(rows):
        for c in range(cols):
            wx = x0 + c * cw + cw * 0.22; wy = y0 + rh * 0.35 + r * rh
            d.rectangle([wx, wy, wx + cw * 0.56, wy + rh * 0.5], fill=YEL if rnd.random() < lit else WIN, outline=INK, width=4)
    if door: d.rectangle([cx - cw * 0.3, by - rh * 0.62, cx + cw * 0.3, by], fill=INK)
@lru_cache(8)
def keys_img(s):
    w, h = int(300 * s), int(300 * s); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); L = max(4, int(10 * s))
    d.ellipse([w * 0.3, h * 0.02, w * 0.7, h * 0.42], outline=INK, width=L)
    for (ang, ln) in [(-20, 1.0), (18, 0.82)]:
        k = Image.new('RGBA', (w, h), (0, 0, 0, 0)); dk = ImageDraw.Draw(k); cx = w / 2; y0 = h * 0.36; l2 = max(3, L // 2)
        dk.rectangle([cx - w * 0.035, y0 + h * 0.2, cx + w * 0.035, y0 + h * (0.24 + 0.36 * ln)], fill=YEL, outline=INK, width=l2)
        for q in (0.7, 0.9): dk.rectangle([cx + w * 0.03, y0 + h * (0.24 + 0.36 * ln * q) - h * 0.025, cx + w * 0.1, y0 + h * (0.24 + 0.36 * ln * q) + h * 0.02], fill=YEL, outline=INK, width=l2)
        dk.ellipse([cx - w * 0.13, y0, cx + w * 0.13, y0 + h * 0.26], fill=YEL, outline=INK, width=L)
        dk.ellipse([cx - w * 0.04, y0 + h * 0.04, cx + w * 0.04, y0 + h * 0.12], fill=(0, 0, 0, 0), outline=INK, width=l2)
        im.alpha_composite(k.rotate(ang, Image.BICUBIC, center=(cx, h * 0.22)))
    return im
def keys(C, cx, cy, s=1.0, rot=0, scale=1.0): put(C, keys_img(round(s, 2)), cx, cy, scale, rot)
@lru_cache(8)
def flat_img(w, h, rooms):
    im = Image.new('RGBA', (w + 20, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0 = y0 = 10; x1 = x0 + w; y1 = y0 + h
    d.rectangle([x0, y0, x1, y1], fill=WALL, outline=INK, width=12)
    def sofa(x, y, ww, hh): d.rounded_rectangle([x, y, x + ww, y + hh], radius=14, fill=MID, outline=INK, width=5); d.rounded_rectangle([x, y, x + ww, y + hh * 0.4], radius=12, fill=GREY, outline=INK, width=5)
    def bed(x, y, ww, hh): d.rounded_rectangle([x, y, x + ww, y + hh], radius=10, fill=(200, 214, 230), outline=INK, width=5); d.rounded_rectangle([x + ww * 0.1, y + hh * 0.08, x + ww * 0.9, y + hh * 0.3], radius=8, fill=WHITE, outline=INK, width=4)
    def tbl(x, y, r): d.ellipse([x - r, y - r, x + r, y + r], fill=WOOD, outline=INK, width=5)
    if rooms == 3:
        mx = x0 + w * 0.55; my = y0 + h * 0.5
        d.line([mx, y0, mx, y0 + h * 0.28], fill=INK, width=10); d.line([mx, y0 + h * 0.5, mx, y1], fill=INK, width=10); d.line([mx, my, x1 - w * 0.14, my], fill=INK, width=10)
        sofa(x0 + w * 0.06, y0 + h * 0.1, w * 0.3, h * 0.2); tbl(x0 + w * 0.38, y0 + h * 0.72, h * 0.11)
        bed(x1 - w * 0.28, y0 + h * 0.08, w * 0.22, h * 0.34); bed(x1 - w * 0.28, my + h * 0.1, w * 0.22, h * 0.3)
        d.rectangle([mx + w * 0.04, y0 + h * 0.08, mx + w * 0.09, y0 + h * 0.3], fill=WOODD, outline=INK, width=4)
        for (tx, ty, n) in [(x0 + w * 0.12, y1 - h * 0.14, '1'), (mx + w * 0.07, my - h * 0.12, '2'), (mx + w * 0.07, y1 - h * 0.14, '3')]:
            t = plate_img(n, int(h * 0.09), INK, WHITE, pad=10, r=30); im.alpha_composite(t, (int(tx), int(ty)))
    else:
        bed(x0 + w * 0.08, y0 + h * 0.12, w * 0.36, h * 0.5); tbl(x1 - w * 0.24, y0 + h * 0.68, h * 0.13)
        d.rectangle([x1 - w * 0.34, y0 + h * 0.08, x1 - w * 0.08, y0 + h * 0.2], fill=WOODD, outline=INK, width=4)
    hx = x0 + w * 0.14; r = w * 0.13
    d.rectangle([hx, y1 - 8, hx + r, y1 + 8], fill=WALL); d.arc([hx - r, y1 - r, hx + r, y1 + r], 0, 90, fill=INK, width=5); d.line([hx, y1, hx, y1 + r], fill=INK, width=6)
    return im
def flat(C, cx, cy, w, h, rooms=3, k=1.0, rot=0): put(C, flat_img(int(w), int(h), rooms), cx, cy, k, rot)
def factory(C, cx, by, s, u):
    d = D(C); w = 760 * s; h = 300 * s; x0 = cx - w / 2; y0 = by - h
    for (px, ph) in [(0.68, 1.9), (0.84, 1.55)]:
        x = x0 + w * px
        for j in range(4):
            q = (u * 0.7 + j * 0.25) % 1; r = (36 + 70 * q) * s; c = int(150 + 85 * q)
            d.ellipse([x + w * 0.045 + 70 * s * q * s_(j * 2 + u) - r, by - h * ph - 30 * s - 230 * s * q - r, x + w * 0.045 + 70 * s * q * s_(j * 2 + u) + r, by - h * ph - 30 * s - 230 * s * q + r], fill=(c, c, c))
        d.rectangle([x, by - h * ph, x + w * 0.09, y0 + 10], fill=BRICKD, outline=INK, width=8); d.rectangle([x - 8, by - h * ph - 16, x + w * 0.09 + 8, by - h * ph + 10], fill=INK)
    sw = w * 0.6 / 4
    for j in range(4):
        xx = x0 + j * sw; p = [(xx, y0 + 4), (xx, y0 - 90 * s), (xx + sw, y0 + 4)]; d.polygon(p, fill=BRICK); d.line(p, fill=INK, width=8)
    d.rectangle([x0, y0, x0 + w, by], fill=BRICK, outline=INK, width=8)
    for j in range(5): d.rectangle([x0 + w * (0.06 + j * 0.115), y0 + h * 0.2, x0 + w * (0.14 + j * 0.115), y0 + h * 0.5], fill=WIN, outline=INK, width=5)
    d.rectangle([x0 + w * 0.72, y0 + h * 0.38, x0 + w * 0.92, by], fill=INK)
    put(C, plate_img('ЗАВОД', int(54 * s), INK, YEL, pad=14, r=6), x0 + w * 0.82, y0 + h * 0.18)
@lru_cache(16)
def doc_img(w, h, title, sub, seal, tsz):
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([4, 4, w + 4, h + 4], fill=PAPER, outline=INK, width=7)
    t = text_img(title, tsz or int(w * 0.17), INK); im.alpha_composite(t, ((w + 12 - t.width) // 2, int(h * 0.09))); y = int(h * 0.09) + t.height + 30
    if sub: t2 = text_img(sub, int(w * 0.075), GREY); im.alpha_composite(t2, ((w + 12 - t2.width) // 2, y)); y += t2.height + 30
    j = 0
    while y < h * 0.74: d.rectangle([w * 0.12, y, w * (0.88 if j % 3 else 0.7), y + 12], fill=LG); y += 38; j += 1
    if seal: d.ellipse([w * 0.6, h * 0.72, w * 0.6 + h * 0.2, h * 0.92], outline=SEAL, width=8); d.ellipse([w * 0.6 + 18, h * 0.72 + 18, w * 0.6 + h * 0.2 - 18, h * 0.92 - 18], outline=SEAL, width=4)
    return im
def doc(C, cx, cy, w, h, title, rot=0, scale=1.0, sub=None, seal=False, tsz=None): put(C, doc_img(int(w), int(h), title, sub, seal, tsz), cx, cy, scale, rot)
@lru_cache(8)
def cal_img(s, big, small):
    w, h = int(520 * s), int(560 * s); im = Image.new('RGBA', (w + 12, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 30, w + 4, h + 30], radius=int(30 * s), fill=WHITE, outline=INK, width=9)
    d.rounded_rectangle([4, 30, w + 4, 30 + h * 0.26], radius=int(30 * s), fill=RED, outline=INK, width=9); d.rectangle([12, 30 + h * 0.16, w - 4, 30 + h * 0.26], fill=RED); d.line([4, 30 + h * 0.26, w + 4, 30 + h * 0.26], fill=INK, width=9)
    for x in (0.25, 0.75): d.rounded_rectangle([w * x - 12, 4, w * x + 12, 76], radius=10, fill=INK)
    t = text_img(big, int(200 * s), INK); im.alpha_composite(t, ((w + 12 - t.width) // 2, int(30 + h * 0.34)))
    t2 = text_img(small, int(70 * s), GREY); im.alpha_composite(t2, ((w + 12 - t2.width) // 2, int(30 + h * 0.79)))
    return im
def calendar(C, cx, cy, s, big, small='ГОД', scale=1.0, rot=0): put(C, cal_img(s, big, small), cx, cy, scale, rot)
@lru_cache(8)
def lock_img(s, col):
    w, h = int(200 * s), int(260 * s); im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im); L = max(6, int(26 * s))
    d.arc([w * 0.2 + 6, 6, w * 0.8 + 6, h * 0.7], 180, 360, fill=INK, width=L)
    d.rectangle([w * 0.2 + 6, h * 0.34, w * 0.2 + 6 + L - 1, h * 0.5], fill=INK); d.rectangle([w * 0.8 + 6 - L + 1, h * 0.34, w * 0.8 + 6, h * 0.5], fill=INK)
    d.rounded_rectangle([6, h * 0.44, w + 6, h + 6], radius=int(26 * s), fill=col, outline=INK, width=max(5, int(9 * s)))
    d.ellipse([w / 2 - 18 * s + 6, h * 0.58, w / 2 + 18 * s + 6, h * 0.58 + 36 * s], fill=INK); d.rectangle([w / 2 - 7 * s + 6, h * 0.66, w / 2 + 7 * s + 6, h * 0.86], fill=INK)
    return im
def lock(C, cx, cy, s=1.0, scale=1.0, rot=0, col=YEL): put(C, lock_img(s, col), cx, cy, scale, rot)
@lru_cache(16)
def coin_img(r):
    im = Image.new('RGBA', (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([4, 4, r * 2 + 4, r * 2 + 4], fill=YEL, outline=INK, width=max(3, r // 7)); d.ellipse([4 + r * 0.25, 4 + r * 0.25, 4 + r * 1.75, 4 + r * 1.75], outline=(214, 170, 0), width=max(2, r // 10))
    d.text((r + 4, r + 4), '₽', font=font2(r), fill=INK, anchor='mm'); return im
def coin(C, cx, cy, r=40, rot=0, scale=1.0): put(C, coin_img(int(r)), cx, cy, scale, rot)
def coinstack(C, cx, by, n, r=60):
    d = D(C)
    for j in range(n):
        y = by - j * r * 0.34; d.ellipse([cx - r, y - r * 0.62, cx + r, y], fill=(226, 184, 0), outline=INK, width=5); d.ellipse([cx - r, y - r * 0.78, cx + r, y - r * 0.16], fill=YEL, outline=INK, width=5)
def wad(C, cx, cy, w=260, n=3, k=1.0):
    for j in range(n): bill(C, cx + (j - (n - 1) / 2) * 14, cy - (j - (n - 1) / 2) * 20, int(w * k), (j - (n - 1) / 2) * 6)
def tv(C, cx, cy, w, h):
    d = D(C); d.polygon([(cx - w * 0.08, cy + h / 2 - 4), (cx + w * 0.08, cy + h / 2 - 4), (cx + w * 0.13, cy + h / 2 + 54), (cx - w * 0.13, cy + h / 2 + 54)], fill=INK); d.rounded_rectangle([cx - w * 0.26, cy + h / 2 + 46, cx + w * 0.26, cy + h / 2 + 70], radius=8, fill=INK)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=26, fill=INK); d.rounded_rectangle([cx - w / 2 + 22, cy - h / 2 + 22, cx + w / 2 - 22, cy + h / 2 - 22], radius=10, fill=DARK)
def seat(C, cx, by, s, u, heat=1):
    d = D(C); col = (156, 100, 68); cd = (118, 72, 48)
    d.rectangle([cx - 30 * s, by - 550 * s, cx - 14 * s, by - 490 * s], fill=INK); d.rectangle([cx + 14 * s, by - 550 * s, cx + 30 * s, by - 490 * s], fill=INK)
    d.rounded_rectangle([cx - 75 * s, by - 650 * s, cx + 75 * s, by - 540 * s], radius=int(36 * s), fill=col, outline=INK, width=8)
    d.rounded_rectangle([cx - 155 * s, by - 510 * s, cx + 155 * s, by - 120 * s], radius=int(70 * s), fill=col, outline=INK, width=8)
    d.rounded_rectangle([cx - 95 * s, by - 460 * s, cx + 95 * s, by - 170 * s], radius=int(40 * s), fill=cd)
    d.rounded_rectangle([cx - 185 * s, by - 160 * s, cx + 185 * s, by], radius=int(50 * s), fill=col, outline=INK, width=8)
    d.rounded_rectangle([cx - 115 * s, by - 128 * s, cx + 115 * s, by - 40 * s], radius=int(30 * s), fill=cd)
    if heat:
        for j in range(3):
            x = cx + (j - 1) * 62 * s; pts = [(x + 20 * s * s_(q * 0.8 + (u * 9 if heat == 1 else 0) + j), by - 185 * s - q * 20 * s) for q in range(13)]
            d.line(pts, fill=RED if heat == 1 else GREY, width=int(14 * s), joint='curve')
def kiosk(C, cx, by, w, h, shut=0.0, sign='ВЫДАЧА КВАРТИР', u=0):
    d = D(C); x0 = cx - w / 2; y0 = by - h
    d.rectangle([x0, y0, x0 + w, by], fill=(226, 214, 190), outline=INK, width=10)
    d.rectangle([x0 - 16, y0 - 96, x0 + w + 16, y0 + 6], fill=INK); put(C, text_img(sign, 58, YEL), cx, y0 - 46)
    wx0, wy0, wx1, wy1 = x0 + w * 0.12, y0 + h * 0.12, x0 + w * 0.88, y0 + h * 0.64
    d.rectangle([wx0, wy0, wx1, wy1], fill=DARK, outline=INK, width=8)
    for j in range(3): bill(C, lerp(wx0, wx1, 0.25 + j * 0.25), (wy0 + wy1) / 2 + 6 * s_(u * 4 + j), 120, 6 * s_(u * 3 + j)) if sign == 'КРЕДИТЫ' else keys(C, lerp(wx0, wx1, 0.25 + j * 0.25), (wy0 + wy1) / 2 + 6 * s_(u * 4 + j), 0.5, 6 * s_(u * 3 + j))
    if shut > 0:
        yb = lerp(wy0, wy1, shut); d.rectangle([wx0, wy0, wx1, yb], fill=(170, 176, 186), outline=INK, width=8)
        for y in range(int(wy0) + 20, int(yb) - 4, 24): d.line([wx0 + 8, y, wx1 - 8, y], fill=STEEL, width=4)
    d.rectangle([wx0 - 16, wy1, wx1 + 16, wy1 + 24], fill=WOODD, outline=INK, width=5)
def safe(C, cx, by, s, label='ВКЛАД'):
    d = D(C); w, h = 300 * s, 340 * s; x0 = cx - w / 2; y0 = by - h
    d.rectangle([x0 + 30 * s, by - 24 * s, x0 + 70 * s, by], fill=INK); d.rectangle([x0 + w - 70 * s, by - 24 * s, x0 + w - 30 * s, by], fill=INK)
    d.rounded_rectangle([x0, y0, x0 + w, by - 20 * s], radius=int(24 * s), fill=STEEL, outline=INK, width=9)
    d.rounded_rectangle([x0 + 26 * s, y0 + 26 * s, x0 + w - 26 * s, by - 46 * s], radius=int(14 * s), fill=(160, 166, 176), outline=INK, width=6)
    d.ellipse([cx - 50 * s, y0 + h * 0.3, cx + 50 * s, y0 + h * 0.3 + 100 * s], fill=LG, outline=INK, width=7); d.line([cx, y0 + h * 0.3 + 50 * s, cx + 30 * s, y0 + h * 0.3 + 20 * s], fill=INK, width=7)
    put(C, plate_img(label, int(54 * s), YEL, INK, pad=12, r=8, border=INK, bw=5), cx, y0 - 40 * s)
def cloud(C, cx, cy, w, h, tail=-1):
    d = D(C); d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=WHITE, outline=INK, width=8)
    for j, (q, r) in enumerate([(0.55, 26), (0.8, 16)]): d.ellipse([cx + tail * w * 0.3 * (1 - q * 0.9) - r - tail * 60 * q, cy + h / 2 + 30 + 60 * q - r, cx + tail * w * 0.3 * (1 - q * 0.9) + r - tail * 60 * q, cy + h / 2 + 30 + 60 * q + r], fill=WHITE, outline=INK, width=6)
def speech(C, cx, cy, w, h, k=1.0, fill=WHITE):
    im = Image.new('RGBA', (int(w) + 16, int(h) + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(w * 0.42, h - 6), (w * 0.5, h + 70), (w * 0.6, h - 6)], fill=fill); d.line([(w * 0.42, h), (w * 0.5, h + 70), (w * 0.6, h)], fill=INK, width=9)
    d.rounded_rectangle([6, 6, w + 6, h + 6], radius=50, fill=fill, outline=INK, width=9); d.polygon([(w * 0.43, h - 8), (w * 0.5, h + 54), (w * 0.59, h - 8)], fill=fill)
    put(C, im, cx, cy + 36, k)
def cursor(C, x, y, s=1.0):
    p = [(0, 0), (0, 80), (20, 62), (36, 98), (52, 90), (36, 56), (62, 56)]; D(C).polygon([(x + a * s, y + b * s) for a, b in p], fill=WHITE, outline=INK); D(C).line([(x + a * s, y + b * s) for a, b in p + [p[0]]], fill=INK, width=6)
def note(C, cx, cy, s, col=INK):
    d = D(C); d.ellipse([cx - 60 * s, cy + 30 * s, cx, cy + 80 * s], fill=col); d.ellipse([cx + 40 * s, cy + 10 * s, cx + 100 * s, cy + 60 * s], fill=col)
    d.rectangle([cx - 14 * s, cy - 80 * s, cx, cy + 56 * s], fill=col); d.rectangle([cx + 86 * s, cy - 100 * s, cx + 100 * s, cy + 36 * s], fill=col); d.polygon([(cx - 14 * s, cy - 80 * s), (cx + 100 * s, cy - 100 * s), (cx + 100 * s, cy - 64 * s), (cx - 14 * s, cy - 44 * s)], fill=col)
def table(C, cx, y, w, h=190):
    d = D(C); d.rectangle([cx - w / 2 + 30, y, cx - w / 2 + 56, y + h], fill=WOODD, outline=INK, width=5); d.rectangle([cx + w / 2 - 56, y, cx + w / 2 - 30, y + h], fill=WOODD, outline=INK, width=5)
    d.rounded_rectangle([cx - w / 2, y - 30, cx + w / 2, y + 10], radius=8, fill=WOOD, outline=INK, width=7)
def dish(C, cx, cy, r):
    d = D(C); d.ellipse([cx - r, cy - r * 0.34, cx + r, cy + r * 0.34], fill=WHITE, outline=INK, width=7); d.ellipse([cx - r * 0.62, cy - r * 0.2, cx + r * 0.62, cy + r * 0.2], outline=LG, width=5)
def room(C, y0=640, col=(238, 232, 220), fl=(214, 196, 168)):
    d = D(C); d.rectangle([0, y0, CW, G + 6], fill=col); d.rectangle([0, G + 6, CW, G + 70], fill=fl); d.line([0, G + 6, CW, G + 6], fill=INK, width=6)
def sky(C, y0=600, col=SKY):
    d = D(C); d.rectangle([0, y0, CW, G + 6], fill=col); d.rectangle([0, G + 6, CW, G + 60], fill=LG); d.line([0, G + 6, CW, G + 6], fill=INK, width=6)
def phone_big(C, cx, cy, s, bg=WHITE):
    phone(C, cx, cy, s, 0, screen=bg); return (cx - 53 * s, cy - 98 * s, cx + 57 * s, cy + 96 * s)
def row(C, x0, x1, y, h, text, k=1.0, bg=LG, fg=INK, price=None):
    if k <= 0.02: return
    w = x1 - x0; im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=18, fill=bg, outline=INK, width=5)
    t = text_img(text, int(h * 0.42), fg); im.alpha_composite(t, (24, (int(h) - t.height) // 2))
    if price: t2 = text_img(price, int(h * 0.36), fg); im.alpha_composite(t2, (int(w) - t2.width - 22, (int(h) - t2.height) // 2))
    put(C, im, (x0 + x1) / 2, y, k)


# ---------- новые предметы «Кредит» ----------
STONE = (232, 226, 212); STONED = (196, 188, 170); FIRE = (255, 120, 30); FIRE2 = (255, 196, 40); BLUE = (52, 92, 170); GLOBE = (120, 180, 230); LAND = (90, 170, 100)
def bank(C, cx, by, s=1.0, crack=0.0, sink=0.0, rot=0, label='БАНК'):
    """банк с колоннами; crack 0..1 — трещина, sink — уходит вниз (px)"""
    w, h = int(640 * s), int(560 * s); im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0, y0 = 20, 20; L = max(5, int(9 * s))
    d.polygon([(x0, y0 + h * 0.28), (x0 + w / 2, y0), (x0 + w, y0 + h * 0.28)], fill=STONE, outline=INK, width=L)
    d.rectangle([x0 + w * 0.04, y0 + h * 0.28, x0 + w * 0.96, y0 + h * 0.36], fill=STONED, outline=INK, width=L)
    for j in range(5):
        cx_ = x0 + w * (0.14 + j * 0.18); d.rectangle([cx_ - w * 0.045, y0 + h * 0.36, cx_ + w * 0.045, y0 + h * 0.88], fill=STONE, outline=INK, width=L)
        for q in (0.4, 0.6): d.line([cx_ + w * 0.045 * (q * 2 - 1), y0 + h * 0.39, cx_ + w * 0.045 * (q * 2 - 1), y0 + h * 0.85], fill=STONED, width=max(2, L // 2))
    d.rectangle([x0, y0 + h * 0.88, x0 + w, y0 + h], fill=STONED, outline=INK, width=L)
    t = text_img(label, int(h * 0.1), INK); im.alpha_composite(t, (int(x0 + w / 2 - t.width / 2), int(y0 + h * 0.2 - t.height / 2)))
    if crack > 0:
        zz = [(x0 + w * 0.5, y0 + h * 0.02), (x0 + w * 0.44, y0 + h * 0.2), (x0 + w * 0.56, y0 + h * 0.36), (x0 + w * 0.42, y0 + h * 0.55), (x0 + w * 0.58, y0 + h * 0.75), (x0 + w * 0.48, y0 + h)]
        m = max(2, int(len(zz) * clamp(crack) + 0.99)); d.line(zz[:m], fill=INK, width=int(L * 1.6), joint='curve')
    if sink > 0: im = im.crop((0, 0, im.width, max(1, int(im.height - sink))))
    put(C, im, cx, by - (h + 40) / 2 + sink / 2 + (sink and 0), 1, rot) if not sink else C.alpha_composite(im.rotate(rot, Image.BICUBIC, expand=True), (int(cx - im.width / 2), int(by - im.height)))
def crowd(C, u, cx, by, n=9, s=0.17, mode='idle', spread=840, seed=1):
    rnd = random.Random(seed); kinds = ['', 'g_', 'd_', 'v_']
    for j in range(n):
        k = kinds[(j * 3 + seed) % 4]; clip = {'idle': ('idle' if k == '' else k + 'idle'), 'cheer': ('cheer' if k == '' else k + 'cheer'), 'shock': ('shock' if k in ('', 'v_') else k + 'shock'),
               'sad': ('idle_sad' if k == '' else k + 'sad')}[mode]
        x = cx - spread / 2 + spread * (j + 0.5) / n + rnd.uniform(-14, 14)
        man(C, clip, u + j * 0.31, x, by + (j % 2) * 10, s * rnd.uniform(0.92, 1.08), flip=j % 3 == 0)
def flames(C, cx, by, w, h, u, seed=0):
    d = D(C); rnd = random.Random(seed)
    for layer_, (col, k) in enumerate([(FIRE, 1.0), (FIRE2, 0.62)]):
        for j in range(7):
            x = cx - w / 2 + w * (j + 0.5) / 7; hh = h * k * (0.6 + 0.4 * abs(s_(u * 9 + j * 1.7 + layer_))) * (0.7 + 0.3 * rnd.random()); ww = w / 7 * 1.25 * k
            d.polygon([(x - ww / 2, by), (x - ww * 0.3, by - hh * 0.55), (x + ww * 0.1 * s_(u * 7 + j), by - hh), (x + ww * 0.3, by - hh * 0.5), (x + ww / 2, by)], fill=col)
def atm(C, cx, by, s=1.0, screen='', scol=(60, 130, 200), cash=0.0):
    d = D(C); w, h = 300 * s, 520 * s; x0 = cx - w / 2; y0 = by - h
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=int(24 * s), fill=(206, 210, 216), outline=INK, width=9)
    d.rectangle([x0 - 10, y0 - 70 * s, x0 + w + 10, y0 + 10], fill=INK); put(C, text_img('БАНКОМАТ', int(40 * s), YEL), cx, y0 - 30 * s)
    d.rounded_rectangle([x0 + 34 * s, y0 + 40 * s, x0 + w - 34 * s, y0 + 200 * s], radius=int(12 * s), fill=scol, outline=INK, width=7)
    if screen: put(C, text_img(screen, int(34 * s), WHITE), cx, y0 + 120 * s)
    for r in range(3):
        for c in range(3): d.rounded_rectangle([x0 + (60 + c * 66) * s, y0 + (232 + r * 50) * s, x0 + (104 + c * 66) * s, y0 + (266 + r * 50) * s], radius=6, fill=WHITE, outline=INK, width=4)
    d.rectangle([x0 + 50 * s, y0 + 410 * s, x0 + w - 50 * s, y0 + 430 * s], fill=INK)
    if cash > 0: bill(C, cx, y0 + 420 * s + 60 * s * cash, 160 * s, 0)
def gavel(C, cx, cy, s, ang):
    im = Image.new('RGBA', (int(520 * s), int(520 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 260 * s
    d.rounded_rectangle([c - 22 * s, c - 40 * s, c + 22 * s, c + 230 * s], radius=int(14 * s), fill=WOOD, outline=INK, width=7)
    d.rounded_rectangle([c - 140 * s, c - 110 * s, c + 140 * s, c - 10 * s], radius=int(24 * s), fill=WOODD, outline=INK, width=8)
    for x in (-110, 100): d.rectangle([c + (x - 6) * s, c - 112 * s, c + (x + 16) * s, c - 8 * s], fill=YEL, outline=INK, width=5)
    put(C, im.rotate(ang, Image.BICUBIC, center=(c, c + 220 * s)), cx, cy)
def press(C, cx, by, s, u):
    """печатный станок: выплёвывает купюры"""
    d = D(C); w, h = 560 * s, 380 * s; x0 = cx - w / 2; y0 = by - h
    d.rectangle([x0 + 30 * s, by - 40 * s, x0 + 90 * s, by], fill=INK); d.rectangle([x0 + w - 90 * s, by - 40 * s, x0 + w - 30 * s, by], fill=INK)
    d.rounded_rectangle([x0, y0, x0 + w, by - 30 * s], radius=int(26 * s), fill=STEEL, outline=INK, width=9)
    for j, xx in enumerate((0.3, 0.7)):
        r = 70 * s; cxx = x0 + w * xx; cyy = y0 + h * 0.4; d.ellipse([cxx - r, cyy - r, cxx + r, cyy + r], fill=STEEL2, outline=INK, width=8)
        a = u * 14 * (1 if j else -1); d.line([cxx, cyy, cxx + math.cos(a) * r * 0.85, cyy + math.sin(a) * r * 0.85], fill=YEL, width=int(12 * s))
    d.rectangle([x0 + w * 0.2, y0 + h * 0.72, x0 + w * 0.8, y0 + h * 0.8], fill=INK)
    put(C, plate_img('ЦБ', int(50 * s), YEL, INK, pad=10, r=8, border=INK, bw=4), cx, y0 + h * 0.4)
def pricetag(C, cx, cy, s, name, price, rot=0, col=YEL, scale=1.0):
    w, h = int(330 * s), int(180 * s); im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(5, 5 + h * 0.5), (5 + h * 0.4, 5), (w + 5, 5), (w + 5, h + 5), (5 + h * 0.4, h + 5)], fill=col, outline=INK, width=7); d.ellipse([h * 0.3 - 12, h * 0.5 - 12 + 5, h * 0.3 + 12, h * 0.5 + 12 + 5], fill=CARD, outline=INK, width=5)
    t = text_img(name, int(h * 0.26), INK); im.alpha_composite(t, (int(h * 0.5), int(h * 0.12)))
    t2 = text_img(price, int(h * 0.42), INK); im.alpha_composite(t2, (int(h * 0.5), int(h * 0.45)))
    put(C, im, cx, cy, scale, rot)
def globe_(C, cx, cy, r, u, crack=0.0):
    d = D(C); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GLOBE, outline=INK, width=10); off = (u * 60) % (r * 2)
    for (ox, oy, rx, ry) in [(-0.4, -0.3, 0.32, 0.22), (0.3, 0.1, 0.28, 0.4), (-0.2, 0.5, 0.2, 0.14), (0.55, -0.5, 0.18, 0.12)]:
        x = cx + ox * r; y = cy + oy * r; d.ellipse([x - rx * r, y - ry * r, x + rx * r, y + ry * r], fill=LAND, outline=INK, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=10)
    if crack > 0:
        for a0 in (0.3, 2.2, 4.0):
            pts = [(cx, cy)]; rr = 0
            for q in range(1, 6): rr = r * q / 5 * clamp(crack); a = a0 + 0.25 * s_(q * 3 + a0); pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            d.line(pts, fill=INK, width=12, joint='curve')
def house(C, cx, by, s, col=WALL, roof=BRICK, sign=None, u=0, tilt=0):
    d = D(C); w, h = 260 * s, 210 * s; x0 = cx - w / 2
    d.rectangle([x0, by - h, x0 + w, by], fill=col, outline=INK, width=7); d.polygon([(x0 - 24 * s, by - h), (cx, by - h - 140 * s), (x0 + w + 24 * s, by - h)], fill=roof, outline=INK, width=7)
    d.rectangle([cx - 34 * s, by - 110 * s, cx + 34 * s, by], fill=WOODD, outline=INK, width=6); d.rectangle([x0 + 22 * s, by - 160 * s, x0 + 78 * s, by - 110 * s], fill=WIN, outline=INK, width=5); d.rectangle([x0 + w - 78 * s, by - 160 * s, x0 + w - 22 * s, by - 110 * s], fill=WIN, outline=INK, width=5)
    if sign:
        put(C, plate_img(sign, int(40 * s), RED, WHITE, pad=10, r=6, border=INK, bw=4), cx, by - h - 200 * s, 1, 6 * s_(u * 6 + cx))
def pocket(C, cx, cy, s, u):
    d = D(C); w, h = 460 * s, 400 * s; x0 = cx - w / 2; y0 = cy - h / 2; DEN = (70, 104, 160); DEN2 = (50, 80, 130)
    d.rectangle([x0 - 80 * s, y0 - 120 * s, x0 + w + 80 * s, y0 + h + 60 * s], fill=DEN)
    d.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h * 0.7), (cx, y0 + h), (x0, y0 + h * 0.7)], fill=DEN2, outline=INK, width=8)
    d.line([(x0 + 20 * s, y0 + 16 * s), (x0 + w - 20 * s, y0 + 16 * s)], fill=YEL, width=5)
    d.arc([x0 + w * 0.1, y0 - h * 0.25, x0 + w * 0.9, y0 + h * 0.25], 0, 180, fill=INK, width=8)
    # моль вылетает
    k = (u * 0.8) % 1; mx, my = cx + 120 * s * s_(u * 3), y0 - 40 * s - 260 * s * k; f = abs(s_(u * 30))
    d.ellipse([mx - 10 * s, my - 22 * s, mx + 10 * s, my + 22 * s], fill=GREY)
    d.ellipse([mx - 50 * s, my - 30 * s * f - 8, mx - 6 * s, my + 10 * s], fill=MID, outline=INK, width=3); d.ellipse([mx + 6 * s, my - 30 * s * f - 8, mx + 50 * s, my + 10 * s], fill=MID, outline=INK, width=3)
def scissors(C, cx, cy, s, op):
    d = D(C); a = 0.25 + 0.35 * op
    for sg in (-1, 1):
        ex, ey = cx + math.cos(math.pi + sg * a) * 260 * s, cy + math.sin(math.pi + sg * a) * 260 * s
        fx, fy = cx + math.cos(-sg * a) * 180 * s, cy + math.sin(-sg * a) * 180 * s
        d.polygon([(cx, cy - 10 * s), (ex, ey), (cx, cy + 10 * s)], fill=STEEL, outline=INK); d.line([(cx, cy), (ex, ey)], fill=INK, width=4)
        d.line([(cx, cy), (fx, fy)], fill=INK, width=int(14 * s)); d.ellipse([fx - 50 * s, fy - 34 * s, fx + 50 * s, fy + 34 * s], outline=RED, width=int(16 * s))
    d.ellipse([cx - 12 * s, cy - 12 * s, cx + 12 * s, cy + 12 * s], fill=YEL, outline=INK, width=4)
def usflag(C, cx, cy, w, u=0):
    h = w * 0.55; im = Image.new('RGBA', (int(w) + 10, int(h) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for j in range(7): d.rectangle([5, 5 + j * h / 7, w + 5, 5 + (j + 0.5) * h / 7], fill=RED)
    d.rectangle([5, 5, 5 + w * 0.42, 5 + h * 0.54], fill=BLUE)
    for r in range(3):
        for c in range(4): d.ellipse([5 + w * (0.05 + c * 0.1) - 8, 5 + h * (0.1 + r * 0.17) - 8, 5 + w * (0.05 + c * 0.1) + 8, 5 + h * (0.1 + r * 0.17) + 8], fill=WHITE)
    d.rectangle([5, 5, w + 5, h + 5], outline=INK, width=8)
    put(C, im, cx, cy, 1, 3 * s_(u * 4))
def arrow(C, x0, y0, x1, y1, col=INK, w=12, k=1.0):
    if k <= 0: return
    d = D(C); xe, ye = lerp(x0, x1, k), lerp(y0, y1, k); d.line([x0, y0, xe, ye], fill=col, width=w); a = math.atan2(ye - y0, xe - x0)
    d.polygon([(xe + math.cos(a) * w * 1.6, ye + math.sin(a) * w * 1.6), (xe + math.cos(a + 2.4) * w * 2.6, ye + math.sin(a + 2.4) * w * 2.6), (xe + math.cos(a - 2.4) * w * 2.6, ye + math.sin(a - 2.4) * w * 2.6)], fill=col)
def coinflow(C, u, x0, y0, x1, y1, n=5, r=30, hgt=160, stop=None):
    for j in range(n):
        q = (u * 1.2 + j / n) % 1
        if stop is not None and u > stop: q = min(q, 0.0); continue
        coin(C, lerp(x0, x1, q), lerp(y0, y1, q) - hgt * s_(math.pi * q), r, q * 360)

