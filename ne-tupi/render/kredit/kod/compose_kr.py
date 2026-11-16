"""СДВГ-монтаж «Если все перестанут платить кредит». Движок «Квартиры» (compose_k.py): кадр на весь экран 1080x1920, белый фон, без чёрных полос.
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

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_50mln(C, u, t):
    ground(C); crowd(C, u, 540, G, 11, 0.16, 'idle', 940, 1); crowd(C, u + 0.5, 540, G - 150, 9, 0.12, 'idle', 820, 2)
    v = u; put(C, plate_img(num(roll(v, 0, 50_000_000, 0.9)), 150, YEL, INK, pad=26, r=20, border=INK, bw=8), 540, 450, 1 + 0.15 * (1 - eo(v / 0.2)), -2)
    src(C, 'ЗАЁМЩИКИ БАНКОВ И МФО · ДАННЫЕ ЦБ, 2025', 1318)
def s_skreditami(C, u, t):
    slam(C, u, 'С КРЕДИТАМИ', 540, TY, 150)
    for j in range(7): card(C, 540 + (j - 3) * 34, 860 - j * 26 + 40 * (1 - eo(clamp((u - j * 0.06) / 0.2))) * 6, 520, (j - 3) * 6, 0, 1 if u > j * 0.06 else 0)
    tag(C, u - 0.4, 'ПОЧТИ КАЖДЫЙ ВТОРОЙ ВЗРОСЛЫЙ', 540, 1180, 46, INK, YEL, -2)
def s_predstav(C, u, t):
    ground(C); man(C, 'think', u, 300, G, 0.46); v = t - T('завтра')
    slam(C, u, 'ПРЕДСТАВЬ', 540, TY, 150)
    if v > -0.1:
        k = back((v + 0.1) / 0.2); L = layer(); calendar(L, 770, 900, 0.8, ' ', '', 1, 6); txt(L, 'ЗАВТРА', 772, 940, 92, INK, 1, 6); put(C, L.crop((520, 620, 1020, 1180)), 770, 900, k)
def s_razom(C, u, t):
    sky(C); bank(C, 820, G + 6, 0.62); v = t - T('Ни')
    for j in range(4):
        x = 110 + j * 130; clip = ['idle', 'g_idle', 'd_idle', 'v_idle'][j] if v < 0 else ['hips', 'g_idle', 'd_hips', 'v_idle'][j]
        man(C, clip, u + j * 0.3, x, G + 6, 0.2)
    coinflow(C, u, 300, 980, 700, 1000, 6, 28, 200, None if v < 0 else u)
    if v > 0: xcross(C, v, 500, 860, 90); plate(C, v, 'НИ РУБЛЯ', 540, 560, 110, RED, WHITE, -3)
    slam(C, u, 'РАЗОМ', 540, 400, 160)
def s_razor(C, u, t):
    sky(C); k = clamp((u - 0.25) / 0.9); bank(C, 540, G + 6, 1.15, clamp(u / 0.3), 260 * ei(k), 6 * k)
    for j in range(6):
        q = (u * 1.5 + j * 0.17) % 1; d = D(C); x = 300 + j * 95; d.ellipse([x - 40 - 60 * q, G - 30 - 140 * q, x + 40 + 60 * q, G + 10 - 100 * q], fill=(200 + int(40 * q),) * 3) if u > 0.3 else None
    slam(C, u, 'БАНКИ', 540, 380, 150); plate(C, t - T('разорились'), 'РАЗОРИЛИСЬ', 540, 530, 100, RED, WHITE)
def s_sgorayut(C, u, t):
    k = clamp(u / 1.0); doc(C, 540, 880 + 60 * k, 520, 640 * (1 - 0.55 * k), 'ДОЛГ', -4, 1, '2 400 000 ₽', False, 150)
    flames(C, 540, 880 + 60 * k + 320 * (1 - 0.55 * k), 640, 420 + 120 * k, u)
    slam(C, u, 'ДОЛГИ', 540, 380, 150); plate(C, t - T('сгорели'), 'СГОРЕЛИ', 540, 530, 100)
def s_svobodny(C, u, t):
    ground(C); crowd(C, u, 540, G, 7, 0.24, 'cheer', 920, 3)
    for j in range(26):
        rnd = random.Random(j); x = rnd.uniform(60, 1020); y = (rnd.uniform(0, 900) + u * (300 + 200 * rnd.random())) % 900 + 450
        D(C).rectangle([x, y, x + 18, y + 30], fill=[YEL, RED, PINK, GREEN, BLUE][j % 5])
    slam(C, u, 'ВСЕ', 540, 360, 130); plate(C, t - T('свободны'), 'СВОБОДНЫ!', 540, 520, 120)
def s_krasota(C, u, t):
    ground(C); burst(C, 540, 960, 280, u, n=16); man(C, 'armsup', u, 540, G, 0.46)
    slam(C, u, 'ОХ*ЕННО', 540, 390, 180); plate(C, t - T('же'), 'ЖЕ?', 540, 560, 110)
    for j, (x, y) in enumerate([(170, 760), (900, 700), (210, 1110), (880, 1080)]): pop(C, u - 0.2 - j * 0.1, '✦', x, y, 120, YEL, j * 20, stroke=INK, sw=6)
def pickets(C, u, cx, by, n, s, labels, spread=900, seed=5):
    rnd = random.Random(seed)
    for j in range(n):
        x = cx - spread / 2 + spread * (j + 0.5) / n; k = ['', 'g_', 'd_', 'v_'][j % 4]; clip = 'cheer' if k == '' else k + 'cheer'
        man(C, clip, u + j * 0.27, x, by + (j % 2) * 12, s, flip=j % 2 == 1)
        if j % 2 == 0:
            yy = by - 1040 * s - 90 + 14 * s_(u * 14 + j); D(C).line([x, yy, x, yy + 170], fill=INK, width=10)
            put(C, plate_img(labels[(j // 2) % len(labels)], 40, WHITE, INK, pad=12, r=6, border=INK, bw=5), x, yy, 1, 8 * s_(u * 9 + j))
def s_hook1(C, u, t):
    sky(C, col=(240, 214, 210)); sh = 10 * s_(u * 60) if u > 0.3 else 0
    bank(C, 540 + sh, 1150, 0.75, clamp((u - 0.4) / 0.6))
    for j in range(4):
        q = (u * 0.9 + j / 4) % 1; doc(C, [110, 970, 160, 920][j], 1150 - 500 * q, 110, 140, 'КРЕДИТ', q * 500 + j * 50, 1, None, False, 28)
    pickets(C, u, 540, G + 6, 6, 0.22, ['НЕ ПЛАТИМ', 'ХВАТИТ', 'НЕТ КРЕДИТАМ'])
    slam(C, u, 'БАНКИ,', 540, 380, 170)
    v = t - T('идите')
    if v > 0: plate(C, v, 'ИДИТЕ НА Х*Й!', 540 + (6 * s_(v * 70) if v > 0.2 else 0), 560, 104, RED, WHITE, -4)
def s_hook2(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); man(C, 'stop', u, 540, G + 40, 0.5)
    slam(C, u, 'МЫ БОЛЬШЕ', 540, 360, 140)
    for j, (x, y, r) in enumerate([(170, 900, -20), (910, 860, 18)]):
        k = clamp(u / 0.4); doc(C, x - 50 * k, y, 160 * (1 - 0.5 * k) + 10, 200, 'КРЕДИТ', r - 30 * k, 1, None, False, 34); doc(C, x + 50 * k, y + 30 * k, 80 * k + 10, 200, ' ', r + 30 * k, 1, None, False, 34) if k > 0.05 else None
    stamp(C, t - T('платим'), 'НЕ ПЛАТИМ!', 540, 570, 110, RED, -8)
def s_bolno(C, u, t):
    C.paste((150, 18, 24), [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=600, col=(130, 12, 18), seed=4)
    man(C, 'idle_sad', u, 540, G + 40, 0.56)
    slam(C, u, 'И СЕЙЧАС', 540, 390, 140, WHITE); plate(C, t - T('больно'), 'БУДЕТ БОЛЬНО', 540, 560, 110, YEL, INK, -3)
def s_pizdec(C, u, t):
    C.paste(RED, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(200, 30, 38), seed=6)
    for j, x in enumerate((200, 540, 880)): man(C, ['g_shock', 'shock', 'd_shock'][j], u + j * 0.2, x, G + 40, 0.34 if j != 1 else 0.42)
    slam(C, u, 'П*ЗДЕЦ.', 540 + 8 * s_(u * 80) * math.exp(-u * 3), 450, 230, WHITE, -4, INK, 12)
def s_stop(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=620, col=(246, 200, 0)); man(C, 'stop', u, 540, G + 40, 0.6); slam(C, u, 'СТОП.', 540, 440, 280)
def s_tupish(C, u, t):
    ground(C); man(C, 'idle_sad', u, 540, G, 0.56); plate(C, u, 'ТУТ ТЫ ТУПИШЬ', 540, 470, 124, YEL)
def s_vydaet(C, u, t):
    sky(C); bank(C, 700, G + 6, 0.8); man(C, 'walkR', u, 120 + 160 * eo(u / 0.9), G + 6, 0.3)
    for j in range(3): wad(C, 700 + (j - 1) * 170, 760 + 20 * s_(u * 4 + j), 150, 2, back((u - 0.2 - j * 0.08) / 0.2))
    slam(C, u, 'БАНК ВЫДАЁТ', 540, 380, 130); plate(C, t - T('кредиты'), 'КРЕДИТЫ', 540, 530, 100)
def s_karman(C, u, t):
    pocket(C, 540, 920, 1.25, u); v = t - T('не', 1)
    slam(C, u, 'НЕ ИЗ СВОЕГО', 540, 380, 120); plate(C, t - T('кармана'), 'КАРМАНА', 540, 530, 100, INK, YEL)
    tag(C, t - T('кармана') - 0.1, 'ПУСТО', 540, 1180, 60, RED, WHITE, -5)
def s_vklady(C, u, t):
    ground(C); safe(C, 300, G, 1.25, 'ВКЛАДЫ'); d = D(C)
    arrow(C, 470, 950, 640, 950, INK, 14, eo(u / 0.4)); coinflow(C, u, 360, 980, 800, 1000, 5, 30, 180)
    man(C, 'give', u + 1, 840, G, 0.36, flip=True); tag(C, u - 0.3, 'КРЕДИТ', 840, 760, 52, YEL)
    slam(C, u, 'А ИЗ ВКЛАДОВ', 540, TY, 140)
def s_tvoih(C, u, t):
    ground(C); safe(C, 540, 800, 0.95, 'ВКЛАДЫ В БАНКЕ')
    for j, (w, x, cl, lab) in enumerate([('Твоих', 200, 'idle_smile', 'ТВОИ'), ('мамы', 540, 'g_idle', 'МАМЫ'), ('соседа', 880, 'd_idle', 'СОСЕДА')]):
        v = t - T(w)
        if v > -0.05:
            man(C, cl, u, x, G, 0.3, flip=j == 2)
            put(C, plate_img(lab, 62, YEL if j == 0 else INK, INK if j == 0 else WHITE, pad=14, r=12, border=INK, bw=5), x, 860, back(v / 0.2), (-4, 3, -2)[j])
            q = clamp(v / 0.5)
            if q < 1: coin(C, lerp(x, 540, eo(q)), lerp(880, 640, eo(q)) - 140 * s_(math.pi * q), 34)
def s_netplat(C, u, t):
    ground(C); bank(C, 540, G, 0.95); xcross(C, u - 0.1, 540, 760, 260, RED, 28)
    slam(C, u, 'НЕТ ПЛАТЕЖЕЙ', 540, TY, 130)
    for j in range(5): coin(C, 200 + j * 170, 1180 + 30 * eo(clamp(u / 0.4)), 40, 90)
def s_nechem(C, u, t):
    ground(C); safe(C, 540, G, 1.3, 'СЕЙФ БАНКА'); d = D(C)
    d.rounded_rectangle([384, 866, 696, 1196], radius=14, fill=(40, 42, 50))
    put(C, text_img('0 ₽', 130, RED, WHITE, 8), 540, 1030, back((u - 0.2) / 0.2))
    slam(C, u, 'НЕЧЕМ ОТДАВАТЬ', 540, 380, 110); plate(C, t - T('вклады'), 'ВКЛАДЫ', 540, 520, 100, RED, WHITE)
def s_utrom(C, u, t):
    sky(C); d = D(C); d.ellipse([820, 640, 960, 780], fill=YEL, outline=INK, width=7)
    atm(C, 880, G + 6, 0.95)
    for j in range(6):
        x = 700 - j * 115 + 10 * max(0, s_(u * 7 - j)); cl = ['idle', 'g_idle', 'd_shock', 'v_idle', 'shock', 'g_shock'][j]
        man(C, cl, u + j * 0.3, x, G + 6 + (j % 2) * 8, 0.24)
    slam(C, u, 'УТРОМ', 540, 380, 150); plate(C, t - T('очередь'), 'ОЧЕРЕДЬ', 540, 530, 100)
def s_dnem(C, u, t):
    sky(C, col=(196, 206, 214)); atm(C, 540, G + 6, 1.35, 'НЕТ\nНАЛИЧНЫХ', RED); man(C, 'idle_sad', u, 230, G + 6, 0.34); man(C, 'g_sad', u, 860, G + 6, 0.3, flip=True)
    slam(C, u, 'ДНЁМ', 540, 380, 150); plate(C, t - T('пустой'), 'ПУСТОЙ', 540, 530, 100, RED, WHITE)
def s_gos(C, u, t):
    ground(C); d = D(C); k = back(u / 0.25)
    L = layer(); dl = D(L); dl.pieslice([240, 620, 840, 1100], 180, 360, fill=YEL, outline=INK, width=10)
    for x in (340, 440, 540, 640, 740): dl.arc([x - 50, 820, x + 50, 900], 0, 180, fill=INK, width=8)
    dl.line([540, 860, 540, 1150], fill=INK, width=14); dl.arc([540, 1110, 620, 1190], 0, 180, fill=INK, width=14)
    put(C, L.crop((220, 600, 860, 1200)), 540, 900, k)
    safe(C, 540, G, 0.75, 'ВКЛАД'); slam(C, u, 'ГОСУДАРСТВО ВЕРНЁТ', 540, 380, 100)
    v = t - T('до');
    if v > -0.1: put(C, plate_img('ДО 1,4 МЛН ₽', 120, INK, YEL, pad=24, r=18), 540, 530, 1 + 0.4 * (1 - eo((v + 0.1) / 0.18)), -3)
    src(C, 'НА ЧЕЛОВЕКА В ОДНОМ БАНКЕ · СИСТЕМА СТРАХОВАНИЯ ВКЛАДОВ', 1318)
def s_novymi(C, u, t):
    ground(C); press(C, 540, G, 1.2, u)
    for j in range(8):
        q = ((u * 1.3 + j / 8) % 1) if u > 0.15 else 0; bill(C, lerp(540, 140 + (j * 113) % 800, eo(q)), lerp(1010, 700 - (j % 3) * 60, eo(q)) + 500 * q * q, 140, q * 400 + j * 30) if q > 0 else None
    slam(C, u, 'СПАСАТЬ БАНКИ', 540, 380, 120); plate(C, t - T('новыми'), 'НОВЫМИ ДЕНЬГАМИ', 540, 530, 88)
def s_ceny(C, u, t):
    ground(C); v = t - T('цены')
    for j, (name, a, b, x, y, r) in enumerate([('ХЛЕБ', 60, 120, 290, 820, -8), ('МОЛОКО', 110, 230, 790, 780, 6), ('БЕНЗИН', 70, 140, 300, 1110, 5), ('АРЕНДА', 40, 80, 780, 1090, -5)]):
        k = clamp(v / 0.6) if v > 0 else 0; p = lerp(a, b, eo(k)); unit = ' 000 ₽' if name == 'АРЕНДА' else ' ₽'
        pricetag(C, x, y + (6 * s_(v * 40 + j) if 0 < k < 1 else 0), 1.15, name, f'{int(p)}{unit}', r, RED if k > 0.5 else YEL, back((u - j * 0.06) / 0.2))
    slam(C, u, 'НОВЫЕ ДЕНЬГИ', 540, 380, 120)
    if v > -0.1: plate(C, v + 0.1, 'ЦЕНЫ ВВЕРХ', 540, 530, 100, RED, WHITE); arrow(C, 120, 1250, 960, 640, RED, 18, eo(clamp(v / 0.5)))
    src(C, 'ЦЕНЫ УСЛОВНЫЕ', 1318)
def s_nekreditu(C, u, t):
    sky(C); v = t - T('никто'); kiosk(C, 540, G + 6, 640, 520, eo(clamp(v / 0.25)) if v > 0 else 0, 'КРЕДИТЫ', u)
    man(C, 'reach' if v < 0.2 else 'idle_sad', u, 130, G + 6, 0.34)
    slam(C, u, 'КРЕДИТЫ', 540, 370, 130)
    if v > 0.05: plate(C, v - 0.05, 'НИКТО НЕ ДАЁТ', 540, 510, 90, RED, WHITE)
    w = t - T('даёт')
    if w > 0: stamp(C, w, 'ОТКАЗАНО', 540, 960, 90, RED, -8)
def s_biznes(C, u, t):
    sky(C); factory(C, 540, G + 6, 0.95, u * 0.2); v = t - T('платить')
    slam(C, u, 'БИЗНЕСУ', 540, 380, 140); plate(C, t - T('нечем', 1), 'НЕЧЕМ ПЛАТИТЬ', 540, 520, 90, INK, YEL)
    if v > -0.1: tag(C, v + 0.1, 'ЗАРПЛАТЫ: 0 ₽', 540, 1180, 60, RED, WHITE, -4)
def s_uvol(C, u, t):
    sky(C); block(C, 860, G + 6, 260, 520, 3, 6, lit=0.2, door=True); man(C, 'box', u, 520 - 120 * eo(u / 0.9), G + 6, 0.4)
    d = D(C); bx = 520 - 120 * eo(u / 0.9); box(C, bx, 1060, 210, 140, 'ВЕЩИ')
    slam(C, u, 'ТЕБЯ', 540, 370, 130); stamp(C, t - T('увольняют'), 'УВОЛЕН', 540, 540, 140, RED, -8)
def s_podvoh(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); slam(C, u, 'А ВОТ И', 540, 720, 130, WHITE); slam(C, t - T('подвох'), 'ПОДВОХ', 540, 930, 260, YEL)
def s_dolg(C, u, t):
    ground(C); v = t - T('никуда'); man(C, 'shock', u, 230, G, 0.36)
    yy = 880 - 40 * abs(s_(u * 6)) * math.exp(-u * 1.5)
    doc(C, 690, yy, 420, 540, 'ДОЛГ', 4, back(u / 0.25), '+ ПРОЦЕНТЫ\n+ ПЕНИ', False, 140)
    slam(C, u, 'ДОЛГ', 540, 380, 150)
    if v > 0: plate(C, v, 'НИКУДА НЕ ДЕЛСЯ', 540, 530, 90, RED, WHITE)
def s_sud(C, u, t):
    ground(C); v = t - T('приставы'); d = D(C)
    hit = abs(s_(min(u, 0.35) / 0.35 * math.pi / 2)); ang = 50 * (1 - hit) - 6
    d.rounded_rectangle([380, 1090, 700, 1150], radius=16, fill=WOODD, outline=INK, width=8); gavel(C, 640, 900, 1.25, ang)
    if u > 0.33: speedlines(C, 540, 1120, u, n=18, r0=120, col=INK, seed=2) if u < 0.45 else None
    slam(C, u, 'СУД', 540, 400, 190)
    if v > 0: plate(C, v, 'ПРИСТАВЫ', 540, 590, 100, RED, WHITE, -3)
def s_polovina(C, u, t):
    ground(C); v = t - T('половины'); k = eo(clamp((v - 0.15) / 0.4)) if v > 0.15 else 0
    L = layer(); wad(L, 540, 920, 520, 3); left = L.crop((0, 0, 540, CH)); right = L.crop((540, 0, CW, CH))
    C.alpha_composite(left, (int(-60 * k), 0)); C.alpha_composite(right.rotate(-14 * k, Image.BICUBIC, center=(0, 920)), (540 + int(120 * k), int(90 * k)))
    scissors(C, 540 + 20 * (1 - k), 920, 0.9, abs(s_(u * 10)) if k < 1 else 0)
    slam(C, u, 'ДО ПОЛОВИНЫ', 540, 380, 140); plate(C, t - T('зарплаты', 1), 'ЗАРПЛАТЫ', 540, 530, 100, INK, YEL)
    if k > 0.5: tag(C, k, '−50%', 820, 1180, 80, RED, WHITE, 8)
    src(C, '229-ФЗ «ОБ ИСПОЛНИТЕЛЬНОМ ПРОИЗВОДСТВЕ», СТ. 99', 1318)
def s_bylo(C, u, t):
    ground(C); d = D(C); r = 260; a = -u * 600
    d.ellipse([540 - r, 870 - r, 540 + r, 870 + r], fill=WHITE, outline=INK, width=12)
    for j in range(12): aa = math.radians(j * 30); d.line([540 + math.cos(aa) * r * 0.82, 870 + math.sin(aa) * r * 0.82, 540 + math.cos(aa) * r * 0.94, 870 + math.sin(aa) * r * 0.94], fill=INK, width=8)
    d.line([540, 870, 540 + math.cos(math.radians(a - 90)) * r * 0.7, 870 + math.sin(math.radians(a - 90)) * r * 0.7], fill=INK, width=14)
    d.line([540, 870, 540 + math.cos(math.radians(a / 12 - 90)) * r * 0.45, 870 + math.sin(math.radians(a / 12 - 90)) * r * 0.45], fill=RED, width=18)
    d.arc([540 - r - 60, 870 - r - 60, 540 + r + 60, 870 + r + 60], 200, 320, fill=YEL, width=26); d.polygon([(540 - r - 40, 870 - 130), (540 - r - 100, 870 - 200), (540 - r + 10, 870 - 220)], fill=YEL, outline=INK)
    slam(C, u, 'И ЭТО', 540, 380, 140); plate(C, t - T('уже'), 'УЖЕ БЫЛО', 540, 530, 100)
def s_2008(C, u, t):
    calendar(C, 540, 760, 1.0, '2008', 'ГОД', 1 + 0.5 * (1 - eo(u / 0.18)), -3); v = t - T('Америка')
    if v > -0.1: usflag(C, 540, 1150, 440 * back((v + 0.1) / 0.2), u); plate(C, v, 'США', 820, 1270, 70, INK, WHITE, 6)
def s_ipoteka(C, u, t):
    sky(C); v = t - T('ипотеку')
    for j in range(3):
        x = 200 + j * 340; house(C, x, G + 6, 1.0, [WALL, (230, 214, 190), (214, 226, 236), WALL][j], [BRICK, BLUE, BRICK, GREEN][j], 'НЕ ПЛАЧУ' if v > 0.1 * j else None, u)
    slam(C, u, 'ПЕРЕСТАЛИ ПЛАТИТЬ', 540, 380, 104)
    if v > -0.1: plate(C, v + 0.1, 'ИПОТЕКУ', 540, 530, 100, INK, YEL)
def s_ruhnul(C, u, t):
    sky(C); k = clamp((u - 0.2) / 0.9); d = D(C)
    L = layer(); dl = D(L); x0, x1, top = 380, 700, 520
    dl.rectangle([x0, top, x1, G + 6], fill=(170, 186, 204), outline=INK, width=10)
    for r in range(9):
        for c in range(4): dl.rectangle([x0 + 30 + c * 72, top + 30 + r * 78, x0 + 78 + c * 72, top + 80 + r * 78], fill=WIN, outline=INK, width=4)
    dl.rectangle([x0 + 40, top - 70, x1 - 40, top], fill=INK); put(L, text_img('БАНК', 46, YEL), 540, top - 36)
    L = L.rotate(-78 * ei(k), Image.BICUBIC, center=(x1, G + 6)); C.alpha_composite(L)
    if k > 0.85:
        for j in range(10): rr = 40 + 30 * j % 90; q = (u - 0.95) * 2; d.ellipse([700 + j * 30 - rr, G - 40 - 120 * q - rr * 0.6, 700 + j * 30 + rr, G - 40 - 120 * q + rr * 0.6], fill=(214, 210, 200))
    block(C, 160, G + 6, 200, 360, 2, 4, door=False); block(C, 930, G + 6, 180, 300, 2, 3, door=False, seed=4)
    slam(C, u, 'РУХНУЛ БАНК', 540, 380, 130); tag(C, u - 0.3, 'ОДИН ИЗ КРУПНЕЙШИХ', 540, 520, 56, INK, YEL, -3)
def s_mir(C, u, t):
    globe_(C, 540, 900, 330, u, clamp((t - T('накрыл')) / 0.6) if t > T('накрыл') else 0)
    slam(C, u, 'КРИЗИС', 540, 380, 170); plate(C, t - T('весь'), 'НА ВЕСЬ МИР', 540, 530, 100, RED, WHITE)
def s_nebanku(C, u, t):
    ground(C); bank(C, 540, G, 0.9); v = t - T('не', 4)
    if v > 0: xcross(C, v, 540, 1000, 300, RED, 30)
    slam(C, u, 'КРЕДИТ —', 540, 380, 150); plate(C, t - T('долг'), 'НЕ ДОЛГ БАНКУ', 540, 530, 96)
def s_sosedu(C, u, t):
    room(C); d = D(C); d.rectangle([700, 660, 980, G + 6], fill=WOOD, outline=INK, width=10); d.rectangle([730, 690, 950, 1200], outline=WOODD, width=6); d.ellipse([920, 950, 950, 980], fill=YEL, outline=INK, width=4)
    put(C, plate_img('КВ. 47', 40, WHITE, INK, pad=10, r=6, border=INK, bw=4), 840, 740)
    man(C, 'd_idle', u, 560, G, 0.44, flip=True); man(C, 'idle', u, 220, G, 0.4)
    v = t - T('положил'); slam(C, u, 'ДОЛГ', 540, 380, 150); plate(C, t - T('соседу'), 'СОСЕДУ', 540, 530, 110, INK, YEL)
    if v > -0.1: safe(C, 380, 1220, 0.45, 'ЕГО ВКЛАД'); coinflow(C, u, 560, 900, 380, 1050, 3, 26, 80)
def s_napishi(C, u, t):
    ground(C); man(C, 'pointcam', u, 540, G, 0.44); speech(C, 540, 560, 820, 380, back(u / 0.22))
    if u > 0.12: txt(C, 'ЧЕСТНО: ЕСТЬ', 540, 480, 84); put(C, plate_img('КРЕДИТ?', 120, YEL, INK, pad=20, r=14), 540, 620, back((u - 0.12) / 0.2))
    for j, (x, y, lab, bg) in enumerate([(200, 980, 'ДА', YEL), (880, 980, 'НЕТ', WHITE)]): put(C, plate_img(lab, 80, bg, INK, pad=22, r=16, border=INK, bw=6), x, y + 8 * s_(u * 5 + j), back((u - 0.4 - j * 0.12) / 0.2))
def s_chestno(C, u, t):
    ground(C); man(C, 'hips', u, 540, G, 0.44)
    slam(C, u, 'ТОЛЬКО', 540, 390, 140); plate(C, t - T('честно'), 'ЧЕСТНО', 540, 540, 130, INK, YEL, -3)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 540, G + 40, 0.48)
    else: man(C, 'walkR', e, 540 - e * 620, G + 40, 0.48, flip=True)
    slam(C, u, 'ВСЁ.', 540, 380, 200)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 540, 570, 140, INK, YEL)
PUSH_FLIP = False

def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook1, 'none', 'boom'), SH(T('Мы') - 0.05, s_hook2, 'shake', 'scratch'),
 SH(T('Пятьдесят') - 0.05, s_50mln, 'zoom', 'bass'), SH(T('Разом') - 0.05, s_razom, 'whipL', 'whoosh'),
 SH(T('Банки', 1) - 0.05, s_razor, 'drop', 'thud'), SH(T('долги') - 0.05, s_sgorayut, 'whipR', 'whoosh'), SH(T('все') - 0.05, s_svobodny, 'zoomthru', 'bass', (540, 900)),
 SH(T('Охуенно') - 0.05, s_krasota, 'zoom', 'shine'),
 SH(T('Стоп') - 0.05, s_stop, 'shake', 'scratch'), SH(T('Тут') - 0.05, s_tupish, 'zoom', 'error'), SH(T('И', 0) - 0.05, s_bolno, 'glitch', 'drop'),
 SH(T('Банк') - 0.05, s_vydaet, 'whipL', 'whoosh'), SH(T('не', 1) - 0.05, s_karman, 'zoomthru', 'bass', (700, 760)),
 SH(T('А', 0) - 0.05, s_vklady, 'push', 'bass'), SH(T('Твоих') - 0.05, s_tvoih, 'door', 'thud'),
 SH(T('Нет') - 0.05, s_netplat, 'drop', 'thud'), SH(T('нечем') - 0.05, s_nechem, 'zoom', 'drop'),
 SH(T('Утром') - 0.05, s_utrom, 'whipR', 'whoosh'), SH(T('Днём') - 0.05, s_dnem, 'zoomthru', 'bass', (880, 900)), SH(T('Пиздец') - 0.05, s_pizdec, 'shake', 'boom'),
 SH(T('Государство') - 0.05, s_gos, 'whipU', 'riser'), SH(T('Но') - 0.05, s_novymi, 'push', 'bass'),
 SH(T('А', 1) - 0.05, s_ceny, 'zoom', 'whoosh'),
 SH(T('Кредиты') - 0.05, s_nekreditu, 'door', 'thud'), SH(T('Бизнесу') - 0.05, s_biznes, 'whipL', 'whoosh'), SH(T('Тебя') - 0.05, s_uvol, 'drop', 'thud'),
 SH(T('А', 2) - 0.03, s_podvoh, 'glitch', 'scratch'),
 SH(T('Долг') - 0.05, s_dolg, 'shake', 'bass'), SH(T('Суд') - 0.05, s_sud, 'shake', 'boom'), SH(T('до', 1) - 0.05, s_polovina, 'whipR', 'whoosh'),
 SH(T('И', 1) - 0.05, s_bylo, 'spin', 'zoomin'), SH(T('Две') - 0.05, s_2008, 'zoomthru', 'bass', (540, 870)),
 SH(T('Люди') - 0.05, s_ipoteka, 'push', 'bass'), SH(T('рухнул') - 0.05, s_ruhnul, 'zoom', 'whoosh'), SH(T('и', 2) - 0.03, s_mir, 'shake', 'boom'),
 SH(T('Так') - 0.05, s_nebanku, 'bodywipe', 'whoosh'), SH(T('Это') - 0.05, s_sosedu, 'door', 'thud'),
 SH(T('Напиши') - 0.05, s_napishi, 'bodywipe', 'bass'),
 SH(T('Всё') - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('идите'), 'alarm'), (T('хуй'), 'boom'), (T('платим'), 'stamp'), (T('Пятьдесят') + 0.1, 'tick2'), (T('человек'), 'kassa'), (T('Ни'), 'error'),
       (T('разорились') + 0.3, 'crack'), (T('сгорели'), 'whoosh'), (T('свободны'), 'ok'), (T('же'), 'boing'), (T('тупишь'), 'stamp'), (T('больно'), 'drop'),
       (T('кредиты'), 'coins'), (T('кармана'), 'boing'),
       (T('вкладов'), 'kassa'), (T('Твоих'), 'pop'), (T('мамы'), 'pop'), (T('соседа'), 'pop'), (T('платежей'), 'error'), (T('вклады'), 'drop'),
       (T('очередь'), 'tick'), (T('пустой'), 'error'), (T('до') - 0.1, 'ding'), (T('новыми'), 'kassa'), (T('цены'), 'riser'), (T('никто'), 'clang'), (T('даёт'), 'stamp'),
       (T('платить'), 'error'), (T('увольняют'), 'stamp'), (T('подвох'), 'boom'), (T('никуда'), 'alarm'), (T('Суд') + 0.3, 'thud'), (T('приставы'), 'clang'),
       (T('половины') + 0.15, 'scratch'), (T('уже'), 'pop'), (T('Америка'), 'pop'), (T('ипотеку'), 'error'), (T('рухнул') + 0.6, 'boom'), (T('накрыл'), 'crack'),
       (T('не', 4), 'error'), (T('соседу'), 'pop'), (T('кредит', 1), 'msg'), (T('тупи'), 'stamp')]

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
CENS = {'ХУЙ': 'Х*Й', 'ОХУЕННО': 'ОХ*ЕННО', 'ПИЗДЕЦ': 'П*ЗДЕЦ', 'СУКА': 'С*КА'}
def clean(w):
    w = w.replace('«', '').replace('»', '').upper()
    for a, b in CENS.items(): w = w.replace(a, b)
    return w
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
        a = text_img('ЕСЛИ ВСЕ ПЕРЕСТАНУТ', 40, WHITE); b = text_img('ПЛАТИТЬ КРЕДИТ?', 40, YEL); w = a.width + b.width + 14 + 44; im = Image.new('RGBA', (w, 70), (0, 0, 0, 0))
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
