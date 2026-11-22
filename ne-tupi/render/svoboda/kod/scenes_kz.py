"""Предметы рилса «Почему в казино нет часов и окон». Движок «Чаевых» (весь экран, белый фон, переходы через действие)."""
from scenes_ch import *
from scenes_ap import post
SEA = (150, 200, 230); SAND = (240, 214, 150); PALM = (60, 150, 90); CARPET = (178, 40, 48); CARPET2 = (150, 28, 36)
WALLC = (236, 230, 218); BLUEP = (40, 90, 170); SUNC = (255, 214, 10)

def grey_man(C, clip, u, cx, s=0.4, feet=None, flip=False, col=(128, 128, 128)):
    """человечек серым силуэтом (не наш герой: Фридман, изобретатель ленты)"""
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); man(L, clip, u, cx, feet or G, s, flip=flip)
    g = Image.new('RGBA', (CW, CH), col + (255,)); g.putalpha(L.getchannel('A')); C.alpha_composite(g)

# ---------- зал казино ----------
def casino(C, u, y0=640, lights=True):
    """стена зала, гирлянда лампочек сверху, красный ковёр с жёлтыми ромбами"""
    d = D(C); d.rectangle([0, y0, CW, G + 6], fill=WALLC)
    for x in range(0, CW, 180): d.line([x, y0, x, G + 6], fill=(226, 219, 205), width=4)
    d.rectangle([0, G + 6, CW, G + 120], fill=CARPET); d.line([0, G + 6, CW, G + 6], fill=INK, width=6)
    for j, x in enumerate(range(-60, CW + 120, 120)):
        cy = G + 60; d.polygon([(x, cy - 28), (x + 28, cy), (x, cy + 28), (x - 28, cy)], fill=YEL if j % 2 else CARPET2)
    if lights:
        d.rectangle([0, y0 - 40, CW, y0], fill=INK)
        for j, x in enumerate(range(30, CW, 60)):
            on = (j + int(u * 8)) % 3 != 0; d.ellipse([x - 14, y0 - 34, x + 14, y0 - 6], fill=YEL if on else (90, 80, 40))

def wallclock(C, cx, cy, r, u=0, spin=0.0, col=WHITE, rim=INK, scale=1.0, rot=0, t0=(10, 10)):
    """настенные часы; spin — сколько оборотов в секунду у минутной стрелки"""
    if scale <= 0.02: return
    R = int(r); im = Image.new('RGBA', (R * 2 + 20, R * 2 + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = R + 10
    d.ellipse([c - R, c - R, c + R, c + R], fill=col, outline=rim, width=max(6, R // 9))
    for j in range(12):
        a = j / 12 * 2 * math.pi; r1 = R * (0.78 if j % 3 else 0.7)
        d.line([c + math.cos(a) * r1, c + math.sin(a) * r1, c + math.cos(a) * R * 0.86, c + math.sin(a) * R * 0.86], fill=INK, width=max(3, R // (14 if j % 3 else 9)))
    m = (t0[1] / 60 + u * spin) * 2 * math.pi; h = (t0[0] / 12 + u * spin / 12) * 2 * math.pi
    d.line([c, c, c + math.sin(h) * R * 0.45, c - math.cos(h) * R * 0.45], fill=INK, width=max(5, R // 9))
    d.line([c, c, c + math.sin(m) * R * 0.68, c - math.cos(m) * R * 0.68], fill=INK, width=max(4, R // 13))
    d.ellipse([c - R * 0.08, c - R * 0.08, c + R * 0.08, c + R * 0.08], fill=RED)
    put(C, im, cx, cy, scale, rot)

def emptyclock(C, cx, cy, r):
    """светлый след на стене, где висели часы, и гвоздь"""
    d = D(C); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(248, 245, 238), outline=(214, 206, 190), width=6)
    d.ellipse([cx - 9, cy - r * 0.9 - 9, cx + 9, cy - r * 0.9 + 9], fill=INK)

def brickwin(C, cx, cy, w, h, bricks=1.0, u=0, fall=0.0, sun=0.0):
    """окно: рама, небо; bricks — заложено кирпичом; fall — кирпичи вываливаются"""
    d = D(C); x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 230, 240))
    if sun > 0:
        r = 70 * sun; sx, sy = cx + w * 0.18, cy - h * 0.16; d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SUNC, outline=INK, width=5)
        for j in range(10):
            a = j / 10 * 2 * math.pi + u; d.line([sx + math.cos(a) * r * 1.25, sy + math.sin(a) * r * 1.25, sx + math.cos(a) * r * 1.6, sy + math.sin(a) * r * 1.6], fill=SUNC, width=8)
    bw_, bh_ = w / 4, h / 7
    if bricks > 0:
        rnd = random.Random(3)
        for row_ in range(7):
            for c in range(-1, 5):
                bx = x0 + c * bw_ + (bw_ / 2 if row_ % 2 else 0); by = y0 + row_ * bh_
                if (row_ * 5 + c) % 7 / 7 > bricks: continue
                dy = 0; rot = 0
                if fall > 0:
                    q = clamp(fall * 1.6 - rnd.random() * 0.6); dy = 900 * q * q; rot = 90 * q * (1 if c % 2 else -1)
                if by + dy > G - 10: continue
                a, b = max(x0, bx), min(x0 + w, bx + bw_)
                if b - a < 4: continue
                if rot:
                    im = Image.new('RGBA', (int(b - a) + 4, int(bh_) + 4), (0, 0, 0, 0)); ImageDraw.Draw(im).rectangle([2, 2, b - a, bh_], fill=BRICK, outline=BRICKD, width=4)
                    put(C, im, (a + b) / 2, by + bh_ / 2 + dy, 1, rot)
                else: d.rectangle([a, by + dy, b, by + bh_ + dy], fill=BRICK, outline=BRICKD, width=4)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=12); d.line([cx, y0, cx, y0 + h], fill=INK, width=8) if bricks <= 0 or fall > 0.6 else None
    d.rectangle([x0 - 24, y0 + h, x0 + w + 24, y0 + h + 26], fill=(214, 206, 190), outline=INK, width=6)

def slotm(C, cx, by, s=1.0, u=0, spin=True, reels=('7', '7', '7'), lever=0.0, screen=None):
    """игровой автомат без логотипов: серый корпус, три жёлтых барабана, рычаг справа"""
    d = D(C); w, h = 360 * s, 620 * s; x0 = cx - w / 2
    d.rounded_rectangle([x0, by - h, x0 + w, by], radius=int(30 * s), fill=STEEL, outline=INK, width=8)
    d.rounded_rectangle([x0 + 20 * s, by - h - 70 * s, x0 + w - 20 * s, by - h + 30 * s], radius=int(40 * s), fill=RED, outline=INK, width=7)
    for j in range(5):
        on = (j + int(u * 10)) % 2 == 0; lx = x0 + 60 * s + j * 60 * s; d.ellipse([lx - 12 * s, by - h - 32 * s, lx + 12 * s, by - h - 8 * s], fill=YEL if on else (120, 30, 30))
    sx0, sy0, sx1, sy1 = x0 + 30 * s, by - h + 70 * s, x0 + w - 30 * s, by - h + 280 * s
    if screen is not None: screen(C, sx0, sy0, sx1, sy1)
    else:
        d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(16 * s), fill=INK)
        rw = (sx1 - sx0 - 40 * s) / 3
        for j in range(3):
            rx = sx0 + 10 * s + j * (rw + 10 * s); d.rounded_rectangle([rx, sy0 + 12 * s, rx + rw, sy1 - 12 * s], radius=int(10 * s), fill=YEL, outline=INK, width=4)
            sym = random.Random(int(u * 14) + j * 7).choice('7$♦7') if spin else reels[j]
            put(C, text_img('$' if sym == '♦' else sym, int(110 * s), RED if sym == '7' else INK), rx + rw / 2, (sy0 + sy1) / 2 + (8 * s_(u * 40 + j) * s if spin else 0))
    d.rounded_rectangle([x0 + 50 * s, by - h + 330 * s, x0 + w - 50 * s, by - h + 400 * s], radius=int(12 * s), fill=STEEL2, outline=INK, width=5)
    d.rectangle([x0 + 40 * s, by - 150 * s, x0 + w - 40 * s, by - 80 * s], fill=INK)
    a = math.radians(-70 + 120 * lever); lx, ly = x0 + w + 20 * s, by - h + 260 * s
    d.rectangle([x0 + w - 4, ly - 20 * s, lx, ly + 20 * s], fill=STEEL2, outline=INK, width=4)
    ex, ey = lx + math.cos(a) * 190 * s * 0.25, ly + math.sin(a) * 190 * s
    d.line([lx, ly, ex, ey], fill=INK, width=int(14 * s)); d.ellipse([ex - 30 * s, ey - 30 * s, ex + 30 * s, ey + 30 * s], fill=RED, outline=INK, width=5)

def strings(C, x0, y0, pts, cut=0.0):
    d = D(C)
    for j, (x, y) in enumerate(pts):
        if cut <= 0: d.line([x0 + (j - 1.5) * 50, y0, x, y], fill=INK, width=4)
        else:
            k = eo(cut); mx, my = lerp(x0 + (j - 1.5) * 50, x, 0.5), lerp(y0, y, 0.5)
            d.line([x0 + (j - 1.5) * 50, y0, mx, my - 160 * k], fill=INK, width=4); d.line([x, y, mx + 40 * k * (1 if j % 2 else -1), my + 220 * k], fill=INK, width=4)

def blueprint(C, cx, cy, w, h, rot=0, scale=1.0):
    im = Image.new('RGBA', (int(w) + 10, int(h) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([5, 5, w + 5, h + 5], fill=BLUEP, outline=INK, width=7)
    for j in range(1, 8): d.line([5 + w * j / 8, 5, 5 + w * j / 8, h + 5], fill=(70, 120, 196), width=2)
    for j in range(1, 6): d.line([5, 5 + h * j / 6, w + 5, 5 + h * j / 6], fill=(70, 120, 196), width=2)
    # план-лабиринт
    pts = [(0.1, 0.15), (0.6, 0.15), (0.6, 0.35), (0.25, 0.35), (0.25, 0.6), (0.8, 0.6), (0.8, 0.85), (0.1, 0.85)]
    d.line([(5 + w * x, 5 + h * y) for x, y in pts], fill=WHITE, width=6)
    d.rectangle([5 + w * 0.68, 5 + h * 0.18, 5 + w * 0.9, 5 + h * 0.4], outline=WHITE, width=5)
    put(C, im, cx, cy, scale, rot)

def stretcher(C, u, cx, by, s=0.3):
    """двое уносят часы на носилках"""
    x1, x2 = cx - 210, cx + 210; man(C, 'walkR', u, x1, by, s); man(C, 'walkR', u + 0.2, x2, by, s)
    hy = by - 1460 * s * 0.42; D(C).line([x1 - 120, hy, x2 + 120, hy], fill=WOODD, width=18)
    wallclock(C, cx, hy - 120, 110, u, 0.4, rot=12 * s_(u * 6))

def bubble_escape(C, cx, cy, rx, ry, u, k=1.0):
    if k <= 0: return
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rx, ry = rx * k, ry * k
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=SEA)
    d.rectangle([cx - rx, cy + ry * 0.35, cx + rx, cy + ry], fill=SAND)
    sx, sy = cx - rx * 0.45, cy - ry * 0.45; d.ellipse([sx - 60, sy - 60, sx + 60, sy + 60], fill=SUNC)
    px = cx + rx * 0.55; d.line([px, cy + ry * 0.4, px - 30, cy - ry * 0.3], fill=WOODD, width=22)
    for a in (-160, -120, -60, -20, 200):
        r = math.radians(a + 6 * s_(u * 3)); d.line([px - 30, cy - ry * 0.3, px - 30 + math.cos(r) * 150, cy - ry * 0.3 + math.sin(r) * 90 + 40], fill=PALM, width=26)
    m = Image.new('L', (CW, CH), 0); ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    L.putalpha(ImageChops.multiply(L.getchannel('A'), m)); C.alpha_composite(L)
    D(C).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=INK, width=8)

def bigphone(C, cx, cy, w, h, u=0, mode='time', text='03:47', k=1.0, scroll=0.0, rot=0):
    """большой телефон: mode time / feed / play / timer"""
    if k <= 0.02: return
    W_, H_ = int(w), int(h); im = Image.new('RGBA', (W_ + 20, H_ + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, W_ + 10, H_ + 10], radius=int(w * 0.14), fill=INK)
    sx0, sy0, sx1, sy1 = 10 + w * 0.06, 10 + w * 0.12, 10 + w * 0.94, 10 + h - w * 0.12
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(w * 0.08), fill=WHITE)
    sc = Image.new('RGBA', (int(sx1 - sx0), int(sy1 - sy0)), WHITE + (255,)); ds = ImageDraw.Draw(sc); sw, sh = sc.size
    if mode == 'time':
        t = text_img(text, int(sw * 0.3), INK); sc.alpha_composite(t, ((sw - t.width) // 2, int(sh * 0.22)))
        t2 = text_img('ЧЕТВЕРГ', int(sw * 0.09), GREY); sc.alpha_composite(t2, ((sw - t2.width) // 2, int(sh * 0.14)))
    elif mode in ('feed', 'play'):
        ph = sh * 0.62; off = (scroll * ph) % ph
        for j in range(-1, 4):
            y = j * ph - off + sh * 0.04; col = [(255, 226, 120), (200, 220, 240), (240, 200, 200), (210, 236, 210)][(j + int(scroll)) % 4]
            ds.rounded_rectangle([sw * 0.06, y, sw * 0.94, y + ph * 0.9], radius=int(sw * 0.06), fill=col, outline=INK, width=5)
            ds.ellipse([sw * 0.12, y + ph * 0.06, sw * 0.24, y + ph * 0.06 + sw * 0.12], fill=INK)
            ds.rounded_rectangle([sw * 0.28, y + ph * 0.08, sw * 0.7, y + ph * 0.13], radius=6, fill=INK)
            cx_, cy_ = sw / 2, y + ph * 0.5; ds.polygon([(cx_ - sw * 0.08, cy_ - sw * 0.1), (cx_ - sw * 0.08, cy_ + sw * 0.1), (cx_ + sw * 0.11, cy_)], fill=WHITE, outline=INK)
        if mode == 'play':
            q = (scroll % 1); ds.rectangle([0, sh - 18, sw, sh], fill=LG); ds.rectangle([0, sh - 18, sw * q, sh], fill=RED)
    elif mode == 'timer':
        t = text_img(text, int(sw * 0.28), INK); sc.alpha_composite(t, ((sw - t.width) // 2, int(sh * 0.4 - t.height / 2)))
        ds.arc([sw * 0.12, sh * 0.4 - sw * 0.38, sw * 0.88, sh * 0.4 + sw * 0.38], -90, -90 + 360 * scroll, fill=YEL, width=int(sw * 0.05))
        b = plate_img('ТАЙМЕР', int(sw * 0.08), INK, YEL, pad=12, r=10); sc.alpha_composite(b, ((sw - b.width) // 2, int(sh * 0.75)))
    m = Image.new('L', sc.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, sw - 1, sh - 1], radius=int(w * 0.08), fill=255); sc.putalpha(m)
    im.alpha_composite(sc, (int(sx0), int(sy0)))
    d.rounded_rectangle([10 + w * 0.36, 10 + w * 0.04, 10 + w * 0.64, 10 + w * 0.08], radius=6, fill=(60, 60, 60))
    put(C, im, cx, cy, k, rot)

def nobutton(C, cx, cy, w, h, u):
    d = D(C)
    for j in range(0, int(2 * (w + h)), 40):
        p = j
        if p < w: x, y, x2, y2 = cx - w / 2 + p, cy - h / 2, cx - w / 2 + min(w, p + 22), cy - h / 2
        elif p < w + h: x, y, x2, y2 = cx + w / 2, cy - h / 2 + p - w, cx + w / 2, cy - h / 2 + min(h, p - w + 22)
        elif p < 2 * w + h: x, y, x2, y2 = cx + w / 2 - (p - w - h), cy + h / 2, cx + w / 2 - min(w, p - w - h + 22), cy + h / 2
        else: x, y, x2, y2 = cx - w / 2, cy + h / 2 - (p - 2 * w - h), cx - w / 2, cy + h / 2 - min(h, p - 2 * w - h + 22)
        d.line([x, y, x2, y2], fill=GREY, width=8)
    put(C, text_img('ХВАТИТ', int(h * 0.42), (200, 200, 200)), cx, cy - h * 0.05)
    qmark(C, cx + w / 2 + 60, cy - h * 0.6, 160, u, RED)

def laptop(C, cx, by, w=360, u=0, scrollpaper=0.0):
    d = D(C); h = w * 0.62
    d.rounded_rectangle([cx - w / 2, by - 30 - h, cx + w / 2, by - 30], radius=16, fill=INK); d.rectangle([cx - w / 2 + 18, by - 30 - h + 18, cx + w / 2 - 18, by - 48], fill=(220, 230, 240))
    d.polygon([(cx - w / 2 - 50, by), (cx + w / 2 + 50, by), (cx + w / 2, by - 30), (cx - w / 2, by - 30)], fill=STEEL, outline=INK)
    if scrollpaper > 0:   # бесконечный свиток из экрана вниз и на пол
        L = clamp(scrollpaper); x0, x1 = cx - w * 0.3, cx + w * 0.3; y0 = by - 30 - h * 0.5; y1 = lerp(y0, G + 80, L)
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=5)
        for yy in range(int(y0) + 30, int(y1), 46): d.rounded_rectangle([x0 + 24, yy, x1 - 24 - (yy % 3) * 30, yy + 18], radius=6, fill=LG)
        if L >= 1:
            for j in range(3): d.ellipse([x0 - 40 + j * 30, G + 40 - j * 26, x1 + 40 + j * 30, G + 100 - j * 26], outline=INK, width=5, fill=WHITE)
