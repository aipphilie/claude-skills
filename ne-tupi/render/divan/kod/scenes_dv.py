"""Предметы рилса «Если бы деньги были не важны» (диван). Движок «Казино»/«Чаевых» (весь экран, белый фон, переходы через действие)."""
from scenes_kz import *
SOFA = YEL; SOFAD = (226, 178, 0); SOFAL = (255, 232, 120); CALC = (52, 56, 64); SCREEN = (196, 212, 184); GLOW = (255, 238, 150)

# ---------- диван по частям ----------
ALL = ('back', 'seat', 'cush', 'armL', 'armR', 'legL', 'legR')
def sofa_img(w, parts):
    w = int(w); h = int(w * 0.62); L = max(5, int(w * 0.014)); im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, x1, by = 10, w + 10, h + 10; lg = w * 0.08; aw = w * 0.13; st = by - lg - w * 0.2
    if 'back' in parts: d.rounded_rectangle([x0 + aw * 0.6, by - lg - w * 0.56, x1 - aw * 0.6, st + 10], radius=int(w * 0.06), fill=SOFAD, outline=INK, width=L)
    if 'seat' in parts: d.rounded_rectangle([x0 + w * 0.05, st, x1 - w * 0.05, by - lg], radius=int(w * 0.03), fill=SOFA, outline=INK, width=L)
    if 'cush' in parts:
        for q in (0, 1):
            a = x0 + aw * 0.9 + q * (w - aw * 1.8) / 2; b = a + (w - aw * 1.8) / 2
            d.rounded_rectangle([a + 4, st - w * 0.07, b - 4, st + w * 0.03], radius=int(w * 0.03), fill=SOFAL, outline=INK, width=L)
    for side, nm in ((0, 'armL'), (1, 'armR')):
        if nm in parts:
            a = x0 if side == 0 else x1 - aw
            d.rounded_rectangle([a, by - lg - w * 0.36, a + aw, by - lg], radius=int(aw * 0.45), fill=SOFA, outline=INK, width=L)
            d.line([a + aw * 0.3, by - lg - w * 0.3, a + aw * 0.3, by - lg - w * 0.06], fill=SOFAD, width=L)
    for side, nm in ((0, 'legL'), (1, 'legR')):
        if nm in parts:
            a = x0 + w * 0.1 if side == 0 else x1 - w * 0.1
            d.polygon([(a - w * 0.03, by - lg - 4), (a + w * 0.03, by - lg - 4), (a + w * 0.018, by), (a - w * 0.018, by)], fill=INK)
    return im
def sofa(C, cx, by, w, parts=ALL, scale=1.0, rot=0, alpha=1.0):
    im = sofa_img(w, tuple(parts)); im2 = im if scale == 1 else im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im2 = im2.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im2 = im2.copy(); im2.putalpha(im2.getchannel('A').point(lambda a: int(a * alpha)))
    C.alpha_composite(im2, (int(cx - im2.width / 2), int(by - im2.height + 10 * scale)))
def seat_y(by, w): return by - w * 0.08 - w * 0.2      # верх сиденья

def lie_on(C, u, cx, by, w, clip='lie', s=0.3):
    """человечек лежит на диване: голова слева, ноги справа"""
    feet_x = cx + w * 0.36; y = seat_y(by, w) - w * 0.04 - 95 * s
    man(C, clip, u, feet_x, y, s, rot=90)

def remote(C, cx, cy, s=1.0, rot=0):
    im = Image.new('RGBA', (int(60 * s) + 8, int(150 * s) + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 60 * s + 4, 150 * s + 4], radius=int(16 * s), fill=INK)
    d.ellipse([20 * s, 18 * s, 44 * s, 42 * s], fill=RED)
    for r_ in range(3):
        for c_ in range(2): d.ellipse([14 * s + c_ * 24 * s, 60 * s + r_ * 26 * s, 26 * s + c_ * 24 * s, 72 * s + r_ * 26 * s], fill=GREY)
    put(C, im, cx, cy, 1, rot)

def rays(C, cx, cy, r, u, n=16, col=GLOW, alpha=1.0):
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for j in range(n):
        a = j / n * 2 * math.pi + u * 0.5; wd = math.pi / n * 0.55
        d.polygon([(cx, cy), (cx + math.cos(a - wd) * r, cy + math.sin(a - wd) * r), (cx + math.cos(a + wd) * r, cy + math.sin(a + wd) * r)], fill=col + (int(255 * alpha),))
    C.alpha_composite(L)
def sparkle(C, cx, cy, r, u, col=YEL):
    k = 0.6 + 0.4 * abs(s_(u * 7 + cx)); r *= k; d = D(C)
    d.polygon([(cx, cy - r), (cx + r * 0.22, cy - r * 0.22), (cx + r, cy), (cx + r * 0.22, cy + r * 0.22), (cx, cy + r), (cx - r * 0.22, cy + r * 0.22), (cx - r, cy), (cx - r * 0.22, cy - r * 0.22)], fill=col, outline=INK, width=4)

def fluffy(C, cx, cy, w, h, k=1.0, tail=None, fill=WHITE):
    """облако мысли; tail=(x, y) — к чьей голове тянутся пузырьки"""
    if k <= 0.02: return
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    w *= k; h *= k; bl = []
    for j in range(11):
        a = j / 11 * 2 * math.pi; bl.append((cx + math.cos(a) * w * 0.4, cy + math.sin(a) * h * 0.36, min(w, h) * (0.26 + 0.05 * (j % 3))))
    bl.append((cx, cy, min(w, h) * 0.42))
    if tail:
        for q, rr in ((0.45, 0.07), (0.7, 0.05), (0.88, 0.035)):
            bl.append((lerp(cx, tail[0], q), lerp(cy + h * 0.4, tail[1], q), min(w, h) * rr))
    for (x, y, r) in bl: d.ellipse([x - r - 9, y - r - 9, x + r + 9, y + r + 9], fill=INK)
    for (x, y, r) in bl: d.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    C.alpha_composite(L)

def calc_img(w, screen):
    w = int(w); h = int(w * 1.45); im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); L = max(6, w // 50)
    d.rounded_rectangle([8, 8, w + 8, h + 8], radius=w // 10, fill=CALC, outline=INK, width=L)
    d.rounded_rectangle([8 + w * 0.08, 8 + w * 0.08, 8 + w * 0.92, 8 + w * 0.36], radius=w // 30, fill=SCREEN, outline=INK, width=L)
    if screen:
        t = text_img(screen, int(w * 0.17), INK); sc = min(1, w * 0.76 / t.width); t = t.resize((max(1, int(t.width * sc)), max(1, int(t.height * sc))), Image.BILINEAR)
        im.alpha_composite(t, (int(8 + w * 0.88 - t.width), int(8 + w * 0.22 - t.height / 2)))
    keys = ['C', '%', '÷', '×', '7', '8', '9', '−', '4', '5', '6', '+', '1', '2', '3', '=']
    bw_ = w * 0.84 / 4; bh = (h - w * 0.46) / 4.3
    for j, kk in enumerate(keys):
        r_, c_ = divmod(j, 4); x = 8 + w * 0.08 + c_ * bw_; y = 8 + w * 0.44 + r_ * bh * 1.06
        col = YEL if kk == '=' else (RED if kk == 'C' else (230, 228, 222))
        d.rounded_rectangle([x + 6, y + 6, x + bw_ - 6, y + bh - 6], radius=int(bw_ * 0.18), fill=col, outline=INK, width=L // 2 + 2)
        t = text_img(kk, int(bh * 0.5), INK if kk != 'C' else WHITE) if kk not in '÷×−' else text_img({'÷': '/', '×': 'x', '−': '-'}[kk], int(bh * 0.5), INK)
        im.alpha_composite(t, (int(x + bw_ / 2 - t.width / 2), int(y + bh / 2 - t.height / 2)))
    return im
@lru_cache(64)
def _calc(w, screen): return calc_img(w, screen)
def calc(C, cx, by, w, screen='', rise=1.0, rot=0):
    """калькулятор стоит на полу by; rise 0..1 — вылезает из-под пола"""
    im = _calc(int(w), screen)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    y = by - im.height * eo(clamp(rise)); vis = int(by - y)
    if vis <= 2: return
    C.alpha_composite(im.crop((0, 0, im.width, vis)), (int(cx - im.width / 2), int(y)))

def bignum(C, text, cx, cy, sz=150, scale=1.0, rot=0, bites=(), col=YEL):
    """большая жёлтая цифра с чёрной обводкой; bites — укусы [(dx, dy, r)] в долях ширины"""
    im = text_img(text, sz, col, INK, max(6, int(sz * 0.06))).copy()
    if bites:
        m = Image.new('L', im.size, 255); dm = ImageDraw.Draw(m)
        for (bx, by_, r) in bites:
            x = bx * im.width; y = by_ * im.height; R = r * im.height
            pts = [(x + math.cos(a / 18 * 2 * math.pi) * R * (1 if a % 2 else 0.8), y + math.sin(a / 18 * 2 * math.pi) * R * (1 if a % 2 else 0.8)) for a in range(18)]
            dm.polygon(pts, fill=0)
        im.putalpha(ImageChops.multiply(im.getchannel('A'), m))
    put(C, im, cx, cy, scale, rot)

def monster(C, cx, cy, r, u, chomp=True, label='ИНФЛЯЦИЯ', flip=False):
    """жёлтый монстрик-инфляция"""
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L); j = s_(u * 20) * r * 0.06; cy2 = cy + j
    pts = []
    for q in range(22):
        a = q / 22 * 2 * math.pi; rr = r * (1.18 if q % 2 == 0 else 0.95); pts.append((cx + math.cos(a) * rr, cy2 + math.sin(a) * rr))
    for sd in (-1, 1):
        d.line([cx + sd * r * 0.45, cy2 + r * 0.85, cx + sd * r * 0.55, cy2 + r * 1.45], fill=INK, width=max(6, int(r * 0.15)))
        d.line([cx + sd * r * 0.9, cy2 + r * 0.1, cx + sd * r * 1.5, cy2 - r * 0.3 + s_(u * 16 + sd) * r * 0.35], fill=INK, width=max(6, int(r * 0.15)))
    d.polygon(pts, fill=YEL, outline=INK, width=max(5, int(r * 0.08)))
    for sd in (-1, 1):
        d.ellipse([cx + sd * r * 0.35 - r * 0.2, cy2 - r * 0.5, cx + sd * r * 0.35 + r * 0.2, cy2 - r * 0.1], fill=WHITE, outline=INK, width=5)
        d.ellipse([cx + sd * r * 0.35 - r * 0.08 + r * 0.05, cy2 - r * 0.36, cx + sd * r * 0.35 + r * 0.08 + r * 0.05, cy2 - r * 0.2], fill=INK)
    mo = (0.1 + 0.32 * abs(s_(u * 14))) if chomp else 0.25
    d.chord([cx - r * 0.55, cy2 - r * 0.05 - mo * r * 0.4, cx + r * 0.55, cy2 + r * 0.2 + mo * r], 0, 180, fill=INK)
    for q in range(4): d.polygon([(cx - r * 0.42 + q * r * 0.28, cy2 + r * 0.07), (cx - r * 0.28 + q * r * 0.28, cy2 + r * 0.07), (cx - r * 0.35 + q * r * 0.28, cy2 + r * 0.24)], fill=WHITE)
    if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT); cx = CW - cx
    C.alpha_composite(L)
    if label: put(C, plate_img(label, max(22, int(r * 0.38)), INK, YEL, pad=10, r=8), cx, cy + r * 1.75)

def thumb(C, cx, cy, s=1.0, rot=0, scale=1.0):
    """значок «большой палец» (у человечка нет кистей, поэтому стикер)"""
    if scale <= 0.02: return
    im = Image.new('RGBA', (int(220 * s), int(220 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 110 * s
    d.ellipse([6, 6, 214 * s, 214 * s], fill=YEL, outline=INK, width=int(9 * s))
    d.rounded_rectangle([58 * s, 98 * s, 150 * s, 168 * s], radius=int(18 * s), fill=INK)
    d.rounded_rectangle([86 * s, 44 * s, 118 * s, 112 * s], radius=int(16 * s), fill=INK)
    d.rectangle([40 * s, 100 * s, 58 * s, 166 * s], fill=INK)
    put(C, im, cx, cy, scale, rot)

def plate_food(C, cx, cy, r, empty=True):
    dish(C, cx, cy, r)
    if not empty: D(C).ellipse([cx - r * 0.4, cy - r * 0.25, cx + r * 0.4, cy + r * 0.05], fill=(200, 140, 80), outline=INK, width=5)

def office(C, u, y0=640):
    room(C, y0, (232, 236, 240), (200, 204, 210))
