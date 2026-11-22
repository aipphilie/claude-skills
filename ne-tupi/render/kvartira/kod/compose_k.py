"""СДВГ-монтаж «Отцу квартиру дали» (почему отец с квартирой, а ты нет). Кадр на весь экран 1080x1920, белый фон, БЕЗ чёрных полос.
Склейка каждые ~1,3 сек, переходы через действие (push/zoomthru/door/bodywipe/drop) + глубина (параллакс, тени, зерно).
python3 compose_k.py 1.5 12.3 -> prev_*.png;  python3 compose_k.py sheet [доля] -> лист всех сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
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
    for j in range(3): keys(C, lerp(wx0, wx1, 0.25 + j * 0.25), (wy0 + wy1) / 2 + 6 * s_(u * 4 + j), 0.5, 6 * s_(u * 3 + j))
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

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_otec30(C, u, t):
    ground(C); man(C, 'd_hips', u, 540, G, 0.56)
    slam(C, u, 'ТВОЙ ОТЕЦ', 540, TY, 150); plate(C, t - T('тридцать'), 'В 30 ЛЕТ', 540, 585, 80)
def s_treshka(C, u, t):
    flat(C, 540, 900, 800, 560, 3, back(u / 0.25)); man(C, 'd_armsup', u, 350, 1010, 0.22)
    v = t - T('трёшке'); plate(C, u, 'СВОЯ ТРЁШКА', 540, TY + 30, 104)
    if v > 0: keys(C, 860, 640, 0.8, 10 * s_(v * 12) * math.exp(-v * 3), back(v / 0.2)); burst(C, 860, 640, 60, v, fill=YEL) if v < 0.1 else None
def s_ty30(C, u, t):
    ground(C); man(C, 'idle', u, 540, G, 0.56)
    slam(C, u, 'А ТЫ', 540, TY, 150); plate(C, t - T('тридцать', 1), 'В 30 ЛЕТ', 540, 585, 80)
def s_platish(C, u, t):
    ground(C); man(C, 'give', u, 250, G, 0.46)
    v = t - T('чужую'); flat(C, 760, 960, 400, 330, 1)
    for j in range(5):
        q = ((u * 1.3 + j * 0.2) % 1); bill(C, lerp(400, 700, q), 880 - 110 * s_(math.pi * q), 110, q * 300 + j * 40)
    slam(C, u, 'ПЛАТИШЬ', 540, TY, 150)
    if v > 0: plate(C, v, 'ЗА ЧУЖУЮ', 540, 585, 80, RED, WHITE); tag(C, t - T('однушку'), 'НЕ ТВОЯ', 760, 760, 54, INK, YEL, -6)
def s_dumaesh(C, u, t):
    ground(C); man(C, 'think', u, 540, G, 0.46)
    v1 = t - T('он'); v2 = t - T('я')
    if v1 > 0:
        k = back(v1 / 0.2); L = layer(); cloud(L, 290, 560, 400, 330, 1); man(L, 'd_idle', u, 230, 690, 0.2); keys(L, 370, 560, 0.5); put(C, L.crop((60, 360, 520, 800)), 290, 580, k)
        tag(C, v1 - 0.15, 'ОН СМОГ', 290, 800, 52)
    if v2 > 0:
        k = back(v2 / 0.2); L = layer(); cloud(L, 790, 560, 400, 330, -1); man(L, 'sad', u, 790, 700, 0.2); put(C, L.crop((560, 360, 1020, 800)), 790, 580, k)
        xcross(C, v2 - 0.1, 790, 560, 110); tag(C, v2 - 0.15, 'А Я НЕТ', 790, 800, 52, RED, WHITE)
def s_netak(C, u, t):
    ground(C); man(C, 'sad', u, 540, G, 0.56)
    slam(C, u, 'ЧТО СО МНОЙ', 540, 400, 104); slam(C, u - 0.1, 'НЕ ТАК?', 540, 530, 130, RED)
    for j, (x, y, r) in enumerate([(200, 820, -14), (880, 760, 12), (240, 1080, 8), (850, 1050, -8)]): pop(C, u - 0.25 - j * 0.18, '?', x, y + 10 * s_(u * 5 + j), 150, YEL, r, stroke=INK, sw=10)
def s_stop(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=620, col=(246, 200, 0)); man(C, 'stop', u, 540, G + 40, 0.6); slam(C, u, 'СТОП.', 540, 440, 280)
def s_tupish(C, u, t):
    ground(C); man(C, 'idle_sad', u, 540, G, 0.56); plate(C, u, 'ТУТ ТЫ ТУПИШЬ', 540, 470, 124, YEL)
def s_nekupil(C, u, t):
    ground(C); man(C, 'd_shrug', u, 540, G, 0.52)
    v = t - T('не', 1); slam(C, u, 'КУПИЛ', 540, 440, 230, GREY if v > 0.15 else INK); strike(C, v, 250, 500, 830, 400, RED, 30)
    if v > 0.1: plate(C, v - 0.1, 'НЕ', 190, 370, 110, RED, WHITE, -10, 'pop')
def s_dali(C, u, t):
    ground(C); v = t - T('дали'); k = eo(u / 0.5)
    man(C, 'd_reach', u, 380, G, 0.54); d = D(C); hx = lerp(1300, 800, k); hy = 700
    d.rounded_rectangle([hx + 40, hy - 70, hx + 700, hy + 70], radius=20, fill=(70, 78, 96), outline=INK, width=8); d.rectangle([hx + 20, hy - 78, hx + 70, hy + 78], fill=WHITE, outline=INK, width=6)
    d.ellipse([hx - 90, hy - 62, hx + 40, hy + 62], fill=INK); keys(C, hx - 70, hy + 150, 0.9, 12 * s_(u * 7))
    slam(C, u, 'ЕМУ ЕЁ', 540, 390, 110)
    if v > 0: plate(C, v, 'ДАЛИ', 540, 540, 150)
def s_zavod(C, u, t):
    sky(C); factory(C, 540, G + 6, 1.05, u); man(C, 'd_wave', u, 250, G + 6, 0.2)
    slam(C, u, 'ЗАВОД', 540, TY, 170)
def s_ochered(C, u, t):
    sky(C); kiosk(C, 820, G + 6, 420, 520, 0, 'КВАРТИРЫ', u)
    for j in range(5):
        dad = j == 2; x = 560 - j * 115 + 14 * max(0, s_(u * 6 - j * 0.7))
        man(C, 'd_idle' if dad else 'idle', u + j * 0.37, x, G + 6 + (j % 2) * 8, 0.27)
        if dad: D(C).polygon([(x - 28, 880), (x + 28, 880), (x, 925)], fill=YEL, outline=INK); tag(C, u - 0.2, 'ОТЕЦ', x, 840, 44)
    slam(C, u, 'ОЧЕРЕДЬ', 540, TY, 170)
def s_order(C, u, t):
    k = back(u / 0.22); doc(C, 540, 880, 620, 760, 'ОРДЕР', -5, k, 'НА КВАРТИРУ', True, 150)
    stamp(C, u - 0.25, 'ВЫДАНО', 620, 1120, 96, RED, -14); keys(C, 250, 1150, 0.9, -20, back((u - 0.15) / 0.2))
def s_potom(C, u, t):
    room(C); man(C, 'd_keys', u, 330, G, 0.5); doc(C, 760, 900, 400, 520, 'ЖИЛЬЁ', 5 + 2 * s_(u * 3), back(u / 0.25), 'ГОСУДАРСТВЕННОЕ', False, 84)
    slam(C, u, 'А ПОТОМ', 540, TY, 130); plate(C, t - T('разрешили'), 'РАЗРЕШИЛИ ЗАБРАТЬ', 540, 570, 70)
def s_besplatno(C, u, t):
    v = t - T('собственность')
    flat(C, 540, 960, 720, 500, 3, 1.0, -2); burst(C, 540, 520, 250, u, n=16); slam(C, u, '0 ₽', 540, 510, 230)
    plate(C, u - 0.15, 'БЕСПЛАТНО', 540, 690, 80, INK, YEL, -3)
    stamp(C, v, 'СОБСТВЕННОСТЬ', 540, 1010, 100, RED, -8)
def s_nesmog(C, u, t):
    ground(C); man(C, 'd_shrug', u, 540, G, 0.52); v = t - T('не', 2)
    slam(C, u, 'КУПИТЬ?', 540, 400, 150)
    if v > 0: plate(C, v, 'НЕ СМОГ БЫ', 540, 560, 100, RED, WHITE, -3)
    for j, (x, y) in enumerate([(210, 900), (870, 880)]):
        d = D(C); d.rounded_rectangle([x - 90, y - 60, x + 90, y + 70], radius=20, fill=WOODD, outline=INK, width=7); d.rounded_rectangle([x - 90, y - 60, x + 90, y - 6], radius=20, fill=WOOD, outline=INK, width=7)
        pop(C, u - 0.2 - j * 0.1, 'ПУСТО', x, y + 110, 46, GREY)
def s_2000(C, u, t):
    for j in range(6):
        q = clamp((u - j * 0.05) / 0.6); doc(C, lerp(540, 120 + j * 170, eo(q)), lerp(900, 380 + (j % 2) * 900, eo(q)) , 150, 190, str(2026 - j * 5), q * 200 + j * 30, 1, None, False, 54) if 0 < q < 1 else None
    calendar(C, 540, 860, 1.25, '2000', 'ГОД', 1 + 0.5 * (1 - eo(u / 0.18)), -3)
def s_zp(C, u, t):
    v = t - T('две'); slam(C, u, 'ЗАРПЛАТА', 540, TY, 150)
    wad(C, 540, 840, 420, 3, back(u / 0.25))
    if v > -0.25: put(C, plate_img(num(roll(v + 0.25, 0, 2000, 0.4)) + ' ₽', 190, YEL, INK, pad=30, r=22, border=INK, bw=9), 540, 1110, 1 + 0.2 * (1 - eo((v + 0.25) / 0.2)), -3)
    src(C, 'СРЕДНЯЯ ПО РОССИИ, 2000 ГОД · РОССТАТ')
def s_metr(C, u, t):
    v = t - T('три'); slam(C, u, 'МЕТР ЖИЛЬЯ', 540, TY, 140); d = D(C); k = back(u / 0.22); a = 150 * k
    d.rectangle([540 - a, 740 - a, 540 + a, 740 + a], fill=WOOD, outline=INK, width=10)
    for j in range(1, 4): d.line([540 - a, 740 - a + j * a / 2, 540 + a, 740 - a + j * a / 2], fill=WOODD, width=5)
    put(C, plate_img('1 м²', 100, WHITE, INK, pad=18, r=14, border=INK, bw=7), 540, 740, k)
    if v > -0.3:
        for j in range(3): wad(C, 280 + j * 260, 1090, 190, 3, back((v + 0.3 - j * 0.1) / 0.2))
        txt(C, '=', 540, 950, 110, INK, back((v + 0.3) / 0.2))
    if v > 0.15: plate(C, v - 0.15, '3 ЗАРПЛАТЫ', 540, 1250, 84)
def s_15let(C, u, t):
    v = t - T('пятнадцать'); plate(C, u, 'НА ТРЁШКУ', 540, TY, 110, INK, YEL)
    flat(C, 540, 760, 560, 380, 3, back(u / 0.22))
    if v > -0.2:
        n = int(roll(v + 0.2, 0, 15, 0.5)); put(C, text_img(f'{n} ЛЕТ', 250, RED, WHITE, 12), 540, 1140, 1 + 0.25 * (1 - eo((v + 0.2) / 0.5)) + (0.06 * abs(s_(v * 9)) if v > 0.3 else 0), -3)
    src(C, 'ЕСЛИ ОТКЛАДЫВАТЬ ВСЮ ЗАРПЛАТУ ЦЕЛИКОМ')
def s_golod(C, u, t):
    room(C); man(C, 'd_shrug', u, 540, G - 20, 0.5, frame=14); table(C, 540, 1090, 640); dish(C, 540, 1050, 130)
    d = D(C); d.rectangle([360, 1000, 372, 1090], fill=STEEL, outline=INK, width=3); d.rectangle([708, 1000, 720, 1090], fill=STEEL, outline=INK, width=3)
    slam(C, u, 'И НЕ ЕСТЬ', 540, TY + 30, 170, RED)
def s_podvoh(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); slam(C, u, 'А ВОТ И', 540, 720, 130, WHITE); slam(C, t - T('подвох'), 'ПОДВОХ', 540, 930, 260, YEL)
def s_nikto(C, u, t):
    sky(C); v = t - T('никто'); w = t - T('даст')
    kiosk(C, 540, G + 6, 640, 520, eo(clamp(v / 0.25)) if v > 0 else 0, 'ВЫДАЧА КВАРТИР', u); man(C, 'reach' if v < 0.2 else 'idle_sad', u, 130, G + 6, 0.34)
    slam(C, u, 'ТЕБЕ', 540, 370, 120)
    if v > 0.1: plate(C, v - 0.1, 'НИКТО НЕ ДАСТ', 540, 500, 84, RED, WHITE)
    if w > 0: stamp(C, w, 'ЗАКРЫТО', 540, 960, 84, RED, -8)
def s_pokolenie(C, u, t):
    ground(C); v = t - T('первое')
    for j, (x, cl, lab) in enumerate([(220, 'd_idle', 'ДЕД'), (540, 'd_hips', 'ОТЕЦ'), (860, 'idle_sad', 'ТЫ')]):
        me = j == 2
        if me and v > 0: burst(C, x, 760, 150, u, fill=YEL)
        man(C, cl, u + j * 0.3, x, G, 0.36 if not me else 0.4)
        put(C, plate_img(lab, 54, YEL if me else INK, INK if me else WHITE, pad=14, r=10, border=INK, bw=5), x, 760 if not me else 720, back((u - j * 0.08) / 0.2))
        if not me: keys(C, x, 630, 0.55, 8 * s_(u * 4 + j), back((u - 0.1 - j * 0.08) / 0.2)); tag(C, u - 0.2 - j * 0.08, 'ДАЛИ', x, 1320, 40, WHITE)
        else: pop(C, u - 0.3, '?', x, 590, 150, RED)
    if v > 0: plate(C, v, 'ПЕРВОЕ ПОКОЛЕНИЕ', 540, TY + 20, 96)
def s_snulya(C, u, t):
    sky(C); block(C, 850, G + 6, 230, 420, 3, 5, lit=0.3); d = D(C)
    for j in range(7):
        if u * 12 > j: d.rounded_rectangle([330 + j * 58, G - 34, 364 + j * 58, G - 22], radius=6, fill=INK)
    man(C, 'walkR', u, 210 + 40 * u, G + 6, 0.36)
    slam(C, u, 'С НУЛЯ', 540, TY, 170); v = t - T('жильё')
    if v > -0.6: tag(C, v + 0.6, 'ЗА СВОИ', 850, 760, 56, YEL, INK, 5)
def s_priuchili(C, u, t):
    ground(C); man(C, 'phone', u, 540, G, 0.5); v = t - T('не', 5)
    slam(C, u, 'ВЛАДЕТЬ', 540, 410, 190, GREY if v > 0.15 else INK); strike(C, v, 200, 470, 880, 370, RED, 28)
    if v > 0.15: plate(C, v - 0.15, 'ПОДПИСЫВАТЬСЯ', 540, 590, 90)
def s_muzyka(C, u, t):
    v = t - T('подписке'); x0, y0, x1, y1 = phone_big(C, 540, 860, 3.3, (30, 32, 40))
    d = D(C); d.rounded_rectangle([x0 + 50, y0 + 60, x1 - 50, y0 + 330], radius=30, fill=GREEN); note(C, 525, y0 + 200 + 10 * s_(u * 8), 1.1, WHITE)
    put(C, text_img('МУЗЫКА', 70, WHITE), 545, y0 + 400)
    for j in range(14): hh = 16 + 50 * abs(s_(u * 9 + j * 1.3)); d.rounded_rectangle([x0 + 50 + j * 19, y0 + 480 - hh / 2, x0 + 60 + j * 19, y0 + 480 + hh / 2], radius=5, fill=GREEN)
    if v > -0.1: lock(C, 545, y0 + 200, 1.0, 1 + 1.5 * (1 - eo((v + 0.1) / 0.14))); plate(C, v + 0.1, 'ПО ПОДПИСКЕ', 545, y1 - 60, 58)
    for j in range(3): note(C, 160 + j * 380, 560 + 40 * s_(u * 4 + j * 2) + (j % 2) * 500, 0.5, MID)
def s_kino(C, u, t):
    v = t - T('подписке', 1); tv(C, 540, 840, 860, 520); d = D(C)
    for j in range(3): d.rectangle([150 + j * 270, 640, 380 + j * 270, 1040], fill=(70 + j * 12, 76 + j * 12, 92 + j * 12))
    d.polygon([(490, 760), (490, 920), (620, 840)], fill=WHITE)
    slam(C, u, 'КИНО', 540, TY, 170)
    if v > -0.1: d.rectangle([132, 602, 948, 1078], fill=(20, 22, 28)); lock(C, 540, 810, 1.1, 1 + 1.5 * (1 - eo((v + 0.1) / 0.14))); plate(C, v + 0.1, 'ПО ПОДПИСКЕ', 540, 1010, 62)
def s_sidenie(C, u, t):
    v = t - T('подписке', 2) + 0.08; w = t - T('машине')
    seat(C, 540, G - 10, 0.95, u, 1 if v < 0 else 2)
    slam(C, u, 'ДАЖЕ ПОДОГРЕВ', 540, 380, 100); slam(C, t - T('сидений'), 'СИДЕНИЙ', 540, 500, 120)
    if w > 0 and v < 0: tag(C, w, 'В МАШИНЕ', 240, 1000, 50, INK, WHITE, -8)
    if v > 0: lock(C, 540, 930, 1.2, 1 + 1.6 * (1 - eo(v / 0.14))); plate(C, v, 'ПО ПОДПИСКЕ', 540, 1160, 90, YEL, INK, -3)
def s_arenda(C, u, t):
    v = t - T('подписка'); flat(C, 540, 900, 620, 440, 1, back(u / 0.22)); man(C, 'idle_sad', u, 640, 1020, 0.2)
    slam(C, u, 'АРЕНДА', 540, TY, 190)
    if v > -0.5: tag(C, v + 0.5, '₽ / МЕС', 800, 700, 60, YEL, INK, 8)
    if v > 0: plate(C, v, 'ТА ЖЕ ПОДПИСКА', 540, 1230, 92, INK, YEL, -2)
def s_dorogaya(C, u, t):
    ground(C); d = D(C); k = eo(u / 0.5)
    for j, (lab, h, col) in enumerate([('МУЗЫКА', 26, MID), ('КИНО', 40, MID), ('АРЕНДА', 540, YEL)]):
        x = 270 + j * 270; hh = h * (k if j == 2 else 1); d.rectangle([x - 80, G - hh, x + 80, G], fill=col, outline=INK, width=8)
        put(C, text_img(lab, 44, INK), x, G + 46)
    if u > 0.3: block(C, 810, G - 540 * k, 150, 110, 2, 1, seed=3, door=False)
    slam(C, u, 'САМАЯ', 540, 370, 110); plate(C, u - 0.15, 'ДОРОГАЯ', 540, 500, 100)
def s_otmena(C, u, t):
    v = t - T('нельзя') + 0.25; sh = 14 * s_(v * 70) * math.exp(-v * 6) if v > 0.12 else 0; d = D(C)
    slam(C, u, 'И ОТМЕНИТЬ', 540, TY, 130)
    d.rounded_rectangle([170 + sh, 720, 910 + sh, 920], radius=50, fill=LG, outline=INK, width=9); put(C, text_img('ОТМЕНИТЬ ПОДПИСКУ', 66, GREY), 540 + sh, 820)
    cx, cy = lerp(900, 700, eo(clamp(u / 0.5))), lerp(1200, 850, eo(clamp(u / 0.5))) + (12 if 0 < v < 0.12 else 0); cursor(C, cx, cy, 1.5)
    if v > 0.12: xcross(C, v - 0.12, 540, 820, 150, RED, 26); plate(C, v - 0.12, 'НЕЛЬЗЯ', 540, 1100, 170, RED, WHITE, -4)
def s_esche(C, u, t):
    v = t - T('ещё'); slam(C, u, 'ЗАВЕДИ ЕЩЁ ОДНУ', 540, 400, 100); x0, y0, x1, y1 = phone_big(C, 540, 950, 3.0); put(C, text_img('МОИ ПОДПИСКИ', 44, GREY), 546, y0 + 60)
    for j, lab in enumerate(['МУЗЫКА', 'КИНО', 'АРЕНДА']): row(C, x0 + 20, x1 - 20, y0 + 140 + j * 96, 82, lab, back((u - j * 0.07) / 0.18), LG, INK, '₽/МЕС')
    if v > 0: burst(C, 546, y0 + 446, 120, v, fill=YEL) if v < 0.12 else None; row(C, x0 - 30, x1 + 30, y0 + 446, 112, '+ СЕБЕ', back(v / 0.2), YEL, INK, '₽/МЕС')
def s_nasebya(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=620, col=(246, 200, 0)); man(C, 'self', u, 540, G + 40, 0.6); plate(C, u, 'НА СЕБЯ', 540, 450, 190, INK, YEL)
def s_zarplata(C, u, t):
    x0, y0, x1, y1 = phone_big(C, 540, 880, 3.3, (232, 236, 242)); k = back(u / 0.22); d = D(C)
    L = layer(); dl = D(L); dl.rounded_rectangle([170, y0 + 90, 910, y0 + 330], radius=36, fill=WHITE, outline=INK, width=8)
    dl.ellipse([210, y0 + 140, 350, y0 + 280], fill=GREEN); put(L, text_img('₽', 90, WHITE), 280, y0 + 210)
    put(L, text_img('ЗАРПЛАТА', 84, INK), 620, y0 + 165); put(L, text_img('ЗАЧИСЛЕНА', 54, GREEN), 620, y0 + 268)
    C.alpha_composite(L, (0, int(-60 * (1 - k)))) if u > 0.03 else None
    for j in range(8):
        q = (u * 1.1 + j * 0.13) % 1; coin(C, 140 + (j * 137) % 820, lerp(300, 1300, q), 34 + (j % 3) * 8, q * 300)
def s_avto(C, u, t):
    ground(C); slam(C, u, 'АВТОПЛАТЁЖ', 540, TY, 140); card(C, 240, 1000, 300, -8); safe(C, 820, G, 1.0); d = D(C)
    pts = [(lerp(300, 780, q / 20), 900 - 200 * s_(math.pi * q / 20)) for q in range(21)]; d.line(pts[:int(2 + 19 * eo(u / 0.4))], fill=INK, width=10, joint='curve')
    if u > 0.35: d.polygon([(770, 850), (830, 905), (750, 915)], fill=INK)
    for j in range(4):
        q = (u * 1.4 + j * 0.25) % 1; coin(C, lerp(300, 790, q), 900 - 200 * s_(math.pi * q), 40, q * 360)
    tag(C, u - 0.3, 'В ДЕНЬ ЗАРПЛАТЫ', 540, 600, 50, INK, YEL)
def s_snachala(C, u, t):
    ground(C); v = t - T('потом', 1); slam(C, u, 'СНАЧАЛА — СЕБЕ', 540, TY, 116)
    burst(C, 250, 900, 190, u, fill=YEL); man(C, 'self', u, 250, G, 0.44); put(C, plate_img('1', 70, INK, YEL, pad=22, r=60), 250, 730, back(u / 0.2)); coin(C, 250, 1010 + 8 * s_(u * 8), 54)
    if v > 0:
        plate(C, v, 'ПОТОМ — ВСЕМ', 540, 560, 76, INK, WHITE)
        for j, lab in enumerate(['АРЕНДА', 'ЕДА', 'КИНО']):
            k = back((v - j * 0.14) / 0.2); x = 530 + j * 190; d = D(C)
            if k > 0.02: put(C, plate_img(str(j + 2), 60, LG, INK, pad=18, r=50, border=INK, bw=5), x, 860, k); put(C, text_img(lab, 40, GREY), x, 1170, k)
            if k > 0.5:
                if j == 0: block(C, x, 1110, 110, 150, 2, 2, door=False)
                elif j == 1: d.arc([x - 50, 960, x + 50, 1060], 180, 360, fill=INK, width=8); d.rounded_rectangle([x - 60, 1010, x + 60, 1110], radius=12, fill=WOOD, outline=INK, width=7)
                else: tv(C, x, 1010, 120, 76)
def s_vydali(C, u, t):
    ground(C); man(C, 'd_keys', u, 400, G, 0.54); v = t - T('выдали')
    burst(C, 770, 760, 170, u, fill=YEL); keys(C, 770, 760, 1.1, 10 * s_(u * 6))
    slam(C, u, 'ОТЦУ КЛЮЧИ', 540, 390, 120)
    if v > 0: plate(C, v, 'ВЫДАЛИ', 540, 540, 110)
def s_vykupit(C, u, t):
    ground(C); x = 400 + 150 * eo(u / 1.4); man(C, 'push', u, x, G, 0.44, flip=PUSH_FLIP)
    for j in range(3): coinstack(C, x - 170 - j * 95, G, 5 + (j * 3) % 4, 44)
    keys(C, 880, 900 + 10 * s_(u * 4), 0.9, 6 * s_(u * 3)); tag(C, u - 0.2, 'ЦЕНА', 880, 1080, 54, RED, WHITE, -6)
    slam(C, u, 'ТЕБЕ ПРИДЁТСЯ', 540, 390, 110); plate(C, t - T('выкупить'), 'ВЫКУПИТЬ', 540, 545, 120, RED, WHITE)
def s_napishi(C, u, t):
    ground(C); man(C, 'pointcam', u, 540, G, 0.44); speech(C, 540, 560, 820, 380, back(u / 0.22))
    if u > 0.12: txt(C, 'СКОЛЬКО У ТЕБЯ', 540, 480, 84); put(C, plate_img('ПОДПИСОК?', 110, YEL, INK, pad=20, r=14), 540, 620, back((u - 0.12) / 0.2))
    for j, (x, y) in enumerate([(170, 900), (900, 860), (190, 1120), (880, 1100)]): pop(C, u - 0.4 - j * 0.15, str([3, 7, 5, 9][j]), x, y + 8 * s_(u * 5 + j), 110, MID)
def s_sporim(C, u, t):
    ground(C); v = t - T('пяти'); man(C, 'hips', u, 540, G, 0.42)
    slam(C, u, 'СПОРИМ?', 540, 390, 140)
    if v > -0.35: burst(C, 540, 640, 140, u, n=16); put(C, text_img('5+', 170, INK), 540, 630, 1 + 1.5 * (1 - eo((v + 0.35) / 0.16)), -6)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 540, G + 40, 0.48)
    else: man(C, 'walkR', e, 540 - e * 620, G + 40, 0.48, flip=True)
    slam(C, u, 'ВСЁ.', 540, 380, 200)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 540, 570, 140, INK, YEL)
PUSH_FLIP = False

def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_otec30, 'none', 'thud'), SH(T('жил') - 0.05, s_treshka, 'zoomthru', 'bass', (540, 900)),
 SH(T('А', 0) - 0.05, s_ty30, 'whipL', 'whoosh'), SH(T('платишь') - 0.05, s_platish, 'push', 'bass'),
 SH(T('И', 0) - 0.05, s_dumaesh, 'drop', 'thud'), SH(T('Значит') - 0.05, s_netak, 'zoom', 'drop'),
 SH(T('Стоп') - 0.05, s_stop, 'shake', 'scratch'), SH(T('Тут') - 0.05, s_tupish, 'zoom', 'error'),
 SH(T('Он') - 0.05, s_nekupil, 'whipR', 'whoosh'), SH(T('Ему') - 0.05, s_dali, 'bodywipe', 'bass'),
 SH(T('Завод') - 0.05, s_zavod, 'zoom', 'boom'), SH(T('очередь') - 0.05, s_ochered, 'whipL', 'swipe'), SH(T('ордер') - 0.05, s_order, 'drop', 'thud'),
 SH(T('А', 1) - 0.05, s_potom, 'push', 'bass'), SH(T('бесплатно') - 0.05, s_besplatno, 'zoomthru', 'boom', (760, 900)),
 SH(T('Купить') - 0.05, s_nesmog, 'door', 'thud'),
 SH(T('Двухтысячный') - 0.05, s_2000, 'spin', 'zoomin'), SH(T('Зарплата') - 0.05, s_zp, 'zoomthru', 'bass', (540, 860)),
 SH(T('Метр') - 0.05, s_metr, 'whipU', 'whoosh'), SH(T('На', 0) - 0.05, s_15let, 'push', 'bass'), SH(T('не', 3) - 0.05, s_golod, 'shake', 'thud'),
 SH(T('А', 2) - 0.03, s_podvoh, 'glitch', 'scratch'),
 SH(T('Тебе', 0) - 0.05, s_nikto, 'zoom', 'bass'), SH(T('Ты') - 0.05, s_pokolenie, 'bodywipe', 'whoosh'), SH(T('покупает') - 0.05, s_snulya, 'whipL', 'swipe'),
 SH(T('И', 1) - 0.05, s_priuchili, 'drop', 'thud'),
 SH(T('Музыка') - 0.05, s_muzyka, 'zoomthru', 'zoomin', (540, 900)), SH(T('Кино') - 0.05, s_kino, 'whipR', 'whoosh'), SH(T('Даже') - 0.05, s_sidenie, 'push', 'bass'),
 SH(T('Аренда') - 0.05, s_arenda, 'door', 'thud'), SH(T('Самая') - 0.05, s_dorogaya, 'whipU', 'riser'), SH(T('И', 2) - 0.05, s_otmena, 'zoom', 'whoosh'),
 SH(T('Поэтому') - 0.05, s_esche, 'zoomthru', 'bass', (540, 820)), SH(T('На', 1) - 0.05, s_nasebya, 'shake', 'boom'),
 SH(T('Пришла') - 0.05, s_zarplata, 'drop', 'notif'), SH(T('автоплатёж') - 0.05, s_avto, 'whipL', 'whoosh'),
 SH(T('Сначала') - 0.05, s_snachala, 'push', 'bass'),
 SH(T('Отцу') - 0.05, s_vydali, 'door', 'thud'), SH(T('Тебе', 1) - 0.05, s_vykupit, 'whipR', 'whoosh'),
 SH(T('Напиши') - 0.05, s_napishi, 'bodywipe', 'bass'), SH(T('Спорим') - 0.05, s_sporim, 'zoom', 'whoosh'),
 SH(T('Всё') - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('тридцать'), 'pop'), (T('трёшке'), 'shine'), (T('тридцать', 1), 'pop'), (T('чужую'), 'error'), (T('однушку'), 'pop'),
       (T('он'), 'pop'), (T('я'), 'error'), (T('так'), 'boing'), (T('тупишь'), 'stamp'), (T('не', 1), 'swipe'), (T('дали'), 'ding'),
       (T('ордер') + 0.25, 'stamp'), (T('разрешили'), 'pop'), (T('собственность'), 'stamp'), (T('не', 2), 'error'),
       (T('две') - 0.25, 'tick2'), (T('тысячи'), 'kassa'), (T('три') - 0.3, 'pop'), (T('зарплаты'), 'pop'), (T('пятнадцать') - 0.2, 'tick'), (T('лет'), 'boom'),
       (T('подвох'), 'boom'), (T('никто'), 'clang'), (T('даст'), 'stamp'), (T('первое'), 'ding'), (T('жильё'), 'pop'),
       (T('не', 5), 'swipe'), (T('владеть') + 0.15, 'pop'), (T('подписке') - 0.1, 'click'), (T('подписке', 1) - 0.1, 'click'), (T('сидений'), 'pop'), (T('подписке', 2) - 0.08, 'clang'),
       (T('подписка'), 'kassa'), (T('дорогая'), 'boom'), (T('нельзя') - 0.2, 'click'), (T('нельзя') - 0.1, 'error'),
       (T('ещё'), 'ok'), (T('зарплата', 0) + 0.1, 'coins'), (T('вклад'), 'kassa'), (T('себе'), 'ding'), (T('потом', 1), 'pop'), (T('остальным'), 'pop'),
       (T('выдали'), 'shine'), (T('выкупить'), 'stamp'), (T('подписок'), 'msg'), (T('пяти') - 0.3, 'boing'), (T('тупи'), 'stamp')]

# ================= движок: глубина, переходы через действие, субтитры, кадр =================
ACTION = {'push', 'zoomthru', 'door', 'bodywipe', 'drop'}; PRE, POST = 0.10, 0.30
CARD_RGB = Image.new('RGB', (CW, CH), CARD)
def _pattern(layer_):
    W2 = CW * 2; im = Image.new('RGBA', (W2, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(7 + layer_)
    if layer_ == 0:
        for x in range(0, W2, 54):
            for y in range(0, CH, 54): d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(232, 230, 224))
    else:
        for j in range(30):
            x = rnd.randint(0, W2); y = rnd.randint(0, CH); r = rnd.randint(70, 190); d.ellipse([x - r, y - r, x + r, y + r], fill=(242, 240, 235))
            if x < 200: d.ellipse([x + W2 - r, y - r, x + W2 + r, y + r], fill=(242, 240, 235))
    return im
PAT = [_pattern(0), _pattern(1)]; SPEED = (18, 60)
def depth(C, u):
    """сцена на белом → фон с параллаксом + мягкая тень + лёгкий наезд переднего плана"""
    rgb = C.convert('RGB'); diff = ImageChops.difference(rgb, CARD_RGB).convert('L')
    small = diff.resize((CW // 8, CH // 8), Image.BILINEAR)
    if small.point(lambda v: 255 if v > 8 else 0).histogram()[255] > 0.8 * (CW // 8) * (CH // 8): return C      # сплошной цветной фон — без параллакса
    m = diff.point(lambda v: 0 if v < 2 else min(255, v * 60))
    out = Image.new('RGBA', (CW, CH), CARD + (255,))
    for l in (1, 0):
        off = int(u * SPEED[l]) % CW; out.alpha_composite(PAT[l].crop((off, 0, off + CW, CH)))
    z = 1 + 0.035 * clamp(u / 1.5)
    sh = m.resize((CW // 4, CH // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4)).resize((CW, CH), Image.BILINEAR)
    shadow = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.2)))
    fg = C.copy(); fg.putalpha(m)
    if z > 1.001:
        w, h = int(CW * z), int(CH * z); ox, oy = (w - CW) // 2, int((h - CH) * 0.45)
        fg = fg.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH)); shadow = shadow.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH))
    out.alpha_composite(shadow, (16, 20)); out.alpha_composite(fg); return out
def shot_at(t):
    i = max(j for j in range(len(SHOTS)) if SHOTS[j]['t'] <= t); return i, SHOTS[i]
def card_of(j, t):
    sh = SHOTS[j]; u = max(0.0, t - sh['t']); tt = max(t, sh['t'])
    C = Image.new('RGBA', (CW, CH), CARD + (255,)); sh['fn'](C, u, tt); return depth(C, u)
def tr_push(A, B, k, t):
    e = eio(k); v = s_(math.pi * k); out = Image.new('RGBA', (CW, CH), CARD + (255,)); x = int(CW * (1 - e))
    out.alpha_composite(hblur(A, 1 + 24 * v), (x - CW, 0)); out.alpha_composite(hblur(B, 1 + 24 * v), (x, 0))
    man(out, 'push', t * 1.4, x + 150, G, 0.7, flip=not PUSH_FLIP); return out
def tr_zoomthru(A, B, k, p):
    s = 1 + 11 * ei(clamp(k / 0.75)); cx, cy = lerp(p[0], CW / 2, eo(k)), lerp(p[1], CH / 2, eo(k))
    box = (p[0] - cx / s, p[1] - cy / s, p[0] + (CW - cx) / s, p[1] + (CH - cy) / s)
    a = A.crop(tuple(int(b) for b in box)).resize((CW, CH), Image.BILINEAR)
    if s > 1.5:
        s2 = s * 0.82; box2 = (p[0] - cx / s2, p[1] - cy / s2, p[0] + (CW - cx) / s2, p[1] + (CH - cy) / s2)
        a = Image.blend(a, A.crop(tuple(int(b) for b in box2)).resize((CW, CH), Image.BILINEAR), 0.45)
    zb = 0.7 + 0.3 * eo(k); w, h = int(CW * zb), int(CH * zb)
    out = Image.new('RGBA', (CW, CH), CARD + (255,)); out.alpha_composite(B.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2))
    al = 1 - clamp((k - 0.4) / 0.3)
    if al > 0: a = a.copy(); a.putalpha(int(255 * al)); out.alpha_composite(a)
    return out
def door_panel(w, left):
    im = Image.new('RGBA', (w + 30, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0 = 0 if left else 30
    d.rectangle([x0, 0, x0 + w, CH], fill=(196, 150, 100), outline=INK, width=14)
    for (ya, yb) in [(300, 820), (900, 1480)]: d.rounded_rectangle([x0 + 70, ya, x0 + w - 70, yb], radius=20, fill=(176, 130, 84), outline=INK, width=8)
    ex = x0 + w - 16 if left else x0 + 16; d.rectangle([ex - 16, 0, ex + 16, CH], fill=INK)
    hx = x0 + w - 90 if left else x0 + 90; d.ellipse([hx - 30, 830, hx + 30, 890], fill=YEL, outline=INK, width=7)
    sh = Image.new('RGBA', (30, CH), (0, 0, 0, 70)); im.alpha_composite(sh, (w if left else 0, 0)); return im
DP = (door_panel(CW // 2, True), door_panel(CW // 2, False))
def tr_door(A, B, k):
    c = eo(k / 0.42) if k < 0.5 else 1 - eio((k - 0.58) / 0.42) if k > 0.58 else 1
    out = (A if k < 0.5 else B).copy(); w = int(CW / 2 * c)
    if w > 0: out.alpha_composite(DP[0], (w - CW // 2, 0)); out.alpha_composite(DP[1], (CW - w - 30, 0))
    return out
def tr_bodywipe(A, B, k, t):
    x = int(lerp(-420, CW + 420, eio(k))); out = A.copy()
    if x > 0: out.paste(B.crop((0, 0, min(CW, x), CH)), (0, 0))
    man(out, 'walkR', 0, x, CH + 420, 2.0, frame=int(k * 5) * 3 % CLIPS['walkR']); return out
def tr_drop(A, B, k):
    y = int(-CH * (1 - back(k))); out = Image.new('RGBA', (CW, CH), CARD + (255,))
    z = 1 - 0.06 * k; w, h = int(CW * z), int(CH * z); a = A.resize((w, h), Image.BILINEAR)
    out.alpha_composite(a, ((CW - w) // 2, (CH - h) // 2)); out.alpha_composite(Image.new('RGBA', (CW, CH), (0, 0, 0, int(110 * k))))
    v = abs(s_(math.pi * min(1, k * 1.3))); b = vblur(B, 1 + 26 * v)
    out.alpha_composite(b, (0, min(0, y))); return out
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

# ---------- субтитры: 1–3 слова, текущее слово на жёлтой плашке ----------
def chunks():
    out, cur = [], []
    for w in W:
        cur.append(w); txtc = ' '.join(x[0] for x in cur)
        if w[0][-1] in '.!?…:»' or (w[0][-1] == ',' and len(txtc) > 7) or len(cur) == 3 or len(txtc) > 13: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CHK = chunks(); SUB_Y = 1432; REFH = text_img('Н', 88, INK, WHITE, 8).height
@lru_cache(400)
def sub_img(w, hl=False):
    f = font(88); wd = int(ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(w, font=f)) + 20
    im = Image.new('RGBA', (wd, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 8), w, font=f, fill=INK, stroke_width=8, stroke_fill=YEL if hl else WHITE); return im
def clean(w): return w.replace('«', '').replace('»', '').upper()
def subs(F, t):
    for ci, ch in enumerate(CHK):
        t1 = CHK[ci + 1][0][1] if ci + 1 < len(CHK) else ch[-1][2] + 0.6
        if ch[0][1] - 0.04 <= t < t1:
            ims = []
            for (w, a, b) in ch:
                nxt = [x for x in ch if x[1] > a]; cur = a - 0.03 <= t and (not nxt or t < nxt[0][1] - 0.03)
                ims.append((sub_img(clean(w), cur), cur, 1 + 0.14 * (1 - eo((t - a) / 0.12)) if cur else 1))
            tw = sum(im.width for im, _, _ in ims) + 40 * (len(ims) - 1)
            sc0 = min(1, 800 / tw); x = 540 - tw * sc0 / 2; k0 = back((t - ch[0][1] + 0.04) / 0.14); y = SUB_Y + (1 - k0) * 30
            pos = []
            for im, cur, sc in ims: pos.append((im, cur, sc, x + im.width * sc0 / 2)); x += (im.width + 40) * sc0
            for im, cur, sc, cx in pos:
                if cur:
                    w2, h2 = im.width * sc0 * sc / 2 + 12, 66 * sc0 * sc
                    ImageDraw.Draw(F).rounded_rectangle([cx - w2, y - h2, cx + w2, y + h2], radius=16, fill=YEL, outline=INK, width=5)
            for im, cur, sc, cx in pos: put(F, im, cx, y, sc * sc0)
            return
TITLE = None
def title(F, t):
    global TITLE
    if TITLE is None:
        a = text_img('ОТЕЦ С КВАРТИРОЙ,', 40, WHITE); b = text_img('А ТЫ НЕТ?', 40, YEL); w = a.width + b.width + 14 + 44; im = Image.new('RGBA', (w, 70), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, 69], radius=16, fill=INK); im.alpha_composite(a, (22, (70 - a.height) // 2)); im.alpha_composite(b, (22 + a.width + 14, (70 - b.height) // 2)); TITLE = im
    put(F, TITLE, 540, 292 - 60 * (1 - eo(t / 0.3)), 1, 0, clamp(t / 0.2))
GRAIN = []
for g in range(6):
    n = Image.effect_noise((WD // 2, HT // 2), 40).resize((WD, HT), Image.NEAREST); GRAIN.append(Image.merge('RGBA', (n, n, n, Image.new('L', (WD, HT), 12))))
def frame(t):
    C, i, sh, act = card_at(t); u = t - sh['t']
    if not act and i + 1 < len(SHOTS):
        r = SHOTS[i + 1]['t'] - t
        if r < 0.07 and SHOTS[i + 1]['tr'] not in {'cut', 'none'} | ACTION:
            z = 1 + 0.1 * (1 - r / 0.07); w, h = int(CW * z), int(CH * z); C2 = Image.new('RGBA', (CW, CH)); C2.paste(C.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2)); C = C2
    F = C.convert('RGBA')
    if not act and u < 0.07 and sh['tr'] not in ('none', 'cut'): F.alpha_composite(Image.new('RGBA', (CW, CH), (255, 255, 255, int(150 * (1 - u / 0.07)))))
    subs(F, t)
    F.alpha_composite(GRAIN[int(t * FPS) % 6])
    out = F.convert('RGB')
    if not act and u < 0.1 and sh['tr'] in ('shake', 'glitch', 'zoom'): out = rgbsplit(out, 10 * (1 - u / 0.1))
    return out

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        frac = float(a[1]) if len(a) > 1 else 0.6; ims = []
        for j, sh in enumerate(SHOTS):
            t1 = SHOTS[j + 1]['t'] if j + 1 < len(SHOTS) else DUR - 1.2; tt = sh['t'] + (t1 - sh['t']) * frac
            ims.append(frame(tt).resize((270, 480)))
        cols = 8; rows = (len(ims) + cols - 1) // cols
        for part in range(0, rows, 2):
            S = Image.new('RGB', (cols * 274, min(2, rows - part) * 484), (90, 90, 90))
            for j, im in enumerate(ims[part * cols:(part + 2) * cols]): S.paste(im, ((j % cols) * 274, (j // cols) * 484))
            S.save(f'sheet_{frac}_{part // 2}.png')
    elif a:
        for x in a: frame(float(x)).save(f'prev_{x}.png')
    else:
        ev = [(round(s['t'], 3), s['sfx']) for s in SHOTS if s['sfx']] + [(round(t, 3), n) for t, n in ACC]
        json.dump(dict(dur=DUR, ev=sorted(ev)), open('sfx.json', 'w'))
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p', os.environ.get('OUT', 'video_noaudio.mp4')], stdin=subprocess.PIPE)
        lo, hi = (int(os.environ.get('F0', 0)), int(os.environ.get('F1', N)))
        for i in range(lo, hi):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 150 == 0: print(i, N, flush=True)
        p.stdin.close(); p.wait(); print('done')
