"""Предметы рилса «Сколько стоит твоя свобода»: витрина, мешки на ножках, шезлонг, растяжка Black Friday, корзина трат, листок-расчёт, кружки-вопросы."""
from scenes_dv import *
GLASS = (226, 236, 244); GLASS2 = (206, 222, 234); SAND2 = (232, 214, 170); BAGY = YEL

def vitrina(C, cx, by, w=440, h=540, price='?', psz=None, stick=None, star=False, u=0, label='СВОБОДА', pcol=YEL):
    """витрина магазина «СВОБОДА»: вывеска, стекло, табличка на подставке, ценник на верёвочке"""
    d = D(C); x0, x1, y0 = cx - w / 2, cx + w / 2, by - h
    d.rectangle([x0 - 24, y0 - 96, x1 + 24, y0], fill=BLK, outline=INK, width=6)
    put(C, text_img(label, 60, YEL), cx, y0 - 48)
    d.rounded_rectangle([x0, y0, x1, by], radius=16, fill=GLASS, outline=INK, width=12)
    for k in range(3): d.line([(x0 + 50 + k * 46, y0 + 40), (x0 + 16 + k * 46, y0 + 150)], fill=WHITE, width=10)
    # подставка + светящаяся табличка
    d.rectangle([cx - 110, by - 150, cx + 110, by - 12], fill=MID, outline=INK, width=8)
    rays(C, cx, by - 220, 170, u, 12, (255, 236, 140), 0.7)
    put(C, plate_img('СВОБОДА', 40, YEL, INK, pad=14, r=10, border=INK, bw=6), cx, by - 200, 1, 0)
    # ценник
    ty = y0 + 170; d.line([(cx, y0 + 20), (cx, ty - 70)], fill=INK, width=5)
    tw_, th_ = w * 0.86, 150
    d.rounded_rectangle([cx - tw_ / 2, ty - 75, cx + tw_ / 2, ty + 75], radius=18, fill=WHITE, outline=INK, width=8)
    if isinstance(price, tuple):     # (старая зачёркнутая, новая)
        put(C, text_img(price[0], 50, GREY), cx, ty - 34); d.line([(cx - tw_ * 0.4, ty - 26), (cx + tw_ * 0.4, ty - 44)], fill=RED, width=9)
        put(C, plate_img(price[1], 54, pcol, INK, pad=8, r=10), cx, ty + 34)
    elif price == '?': qmark(C, cx, ty, psz or 120, u, INK)
    else:
        im = text_img(price, psz or 66, INK); sc = min(1, tw_ * 0.9 / im.width); put(C, im, cx, ty, sc)
    if star: put(C, text_img('*ориентир', 34, GREY), cx, ty + 105)
    if stick: put(C, stick, x1 - 40, by - 260, 1, -12)

def sticker(text, r=120, col=YEL):
    im = Image.new('RGBA', (2 * r + 16, 2 * r + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([8, 8, 2 * r + 8, 2 * r + 8], fill=col, outline=INK, width=9)
    t = text_img(text, int(r * 0.5), INK); sc = min(1, 1.6 * r / t.width); im.alpha_composite(t.resize((int(t.width * sc), int(t.height * sc))), (int(r + 8 - t.width * sc / 2), int(r + 8 - t.height * sc / 2)))
    return im

def bagleg(C, cx, by, s=1.0, u=0, text='', walk=True, rot=0, env=None, helmet=False):
    """жёлтый мешок на ножках (как в «Десятом легче»)"""
    w = 200 * s; h = 210 * s; ph = 1.4 * u * 6.28 if walk else 0
    d = D(C); lw = max(4, int(10 * s))
    for j, sgn in enumerate((-1, 1)):
        a = 0.35 * s_(ph + j * 3.14) if walk else 0
        hx = cx + sgn * w * 0.18; hy = by - 70 * s
        fx = hx + math.sin(a) * 70 * s; fy = hy + math.cos(a) * 70 * s
        d.line([(hx, hy), (fx, fy)], fill=INK, width=lw); d.ellipse([fx - 18 * s, fy - 8 * s, fx + 22 * s, fy + 8 * s], fill=INK)
    bob = 6 * s * abs(s_(ph)) if walk else 0
    im = Image.new('RGBA', (int(w) + 20, int(h) + 20), (0, 0, 0, 0)); q = ImageDraw.Draw(im); ox = oy = 10
    q.rounded_rectangle((ox + w * .30, oy, ox + w * .70, oy + h * .24), radius=int(w * .08), fill=BAGY, outline=INK, width=lw)
    q.rounded_rectangle((ox + w * .03, oy + h * .18, ox + w * .97, oy + h), radius=int(w * .36), fill=BAGY, outline=INK, width=lw)
    q.line((ox + w * .33, oy + h * .19, ox + w * .67, oy + h * .19), fill=INK, width=lw * 2)
    if text:
        t = text_img(text, int(w * 0.24), INK); sc = min(1, w * 0.8 / t.width); im.alpha_composite(t.resize((max(1, int(t.width * sc)), max(1, int(t.height * sc)))), (int(ox + w / 2 - t.width * sc / 2), int(oy + h * 0.6 - t.height * sc / 2)))
    put(C, im, cx, by - 60 * s - h / 2 - bob, 1, rot)
    if env: envelope(C, cx + w * 0.45, by - 60 * s - h * 0.55 - bob, 120 * s, -8, env)
    if helmet: d.pieslice([cx - 60 * s, by - 60 * s - h - 50 * s - bob, cx + 60 * s, by - 60 * s - h + 40 * s - bob], 180, 360, fill=YEL, outline=INK)

def deckchair(C, cx, by, s=1.0):
    d = D(C); lw = int(10 * s)
    d.line([(cx - 200 * s, by), (cx + 120 * s, by - 230 * s)], fill=WOODD, width=int(18 * s))
    d.line([(cx + 180 * s, by), (cx - 80 * s, by - 120 * s)], fill=WOODD, width=int(18 * s))
    d.polygon([(cx - 210 * s, by - 110 * s), (cx + 60 * s, by - 120 * s), (cx + 170 * s, by - 290 * s), (cx + 120 * s, by - 300 * s), (cx + 20 * s, by - 160 * s), (cx - 220 * s, by - 150 * s)], fill=(250, 120, 110), outline=INK)
    for k in range(3): d.line([(cx - 180 * s + k * 80 * s, by - 112 * s), (cx - 186 * s + k * 80 * s, by - 150 * s)], fill=WHITE, width=lw)

def lie_chair(C, u, cx, by, s=0.36, clip='lie'):
    deckchair(C, cx, by, 1.0)
    man(C, clip, u, cx - 40, by - 135, s, rot=-62)

def bfbanner(C, cy, u, text='BLACK FRIDAY', sub='−70%'):
    d = D(C); d.rectangle([0, cy - 90, CW, cy + 90], fill=BLK)
    put(C, text_img(text, 96, YEL), 540 - 110, cy, 1, -2)
    put(C, sticker(sub, 70, RED), 900, cy + 6, 1, 10 + 4 * s_(u * 8))

def sneakers(C, cx, by, s=1.0):
    d = D(C)
    d.rectangle([cx - 230 * s, by - 20 * s, cx + 230 * s, by], fill=WOODD, outline=INK, width=6)
    for k, x in enumerate((cx - 120 * s, cx + 120 * s)):
        y = by - 20 * s
        d.rounded_rectangle([x - 90 * s, y - 70 * s, x + 90 * s, y], radius=int(30 * s), fill=WHITE if k else (90, 160, 230), outline=INK, width=7)
        d.rectangle([x - 90 * s, y - 18 * s, x + 90 * s, y], fill=INK)
    pricetag(C, cx, by - 150 * s, 0.6 * s, 'КРОССЫ', '−70%', 8, RED)

def basket(C, cx, by, s=1.0, n=5, out=0.0, u=0):
    """корзина «ТРАТЫ» с кирпичами; out — кирпич «−10 000» вылетает вверх"""
    d = D(C); w, h = 360 * s, 200 * s; x0 = cx - w / 2
    for j in range(n):
        bx = x0 + 30 * s + (j % 3) * 105 * s; byy = by - h - 10 * s - (j // 3) * 60 * s
        d.rounded_rectangle([bx, byy - 55 * s, bx + 96 * s, byy], radius=8, fill=(214, 120, 90), outline=INK, width=6)
    if out > 0:
        k = eo(out); bx, byy = cx + 30 * s * k, by - h - 70 * s - 330 * s * k
        put(C, plate_img('−10 000 / МЕС', int(46 * s), (214, 120, 90), WHITE, pad=14, r=10, border=INK, bw=6), bx, byy, 1, -8 * k)
    d.polygon([(x0, by - h), (x0 + w, by - h), (x0 + w - 30 * s, by), (x0 + 30 * s, by)], fill=WOODD, outline=INK)
    for k in range(1, 4): d.line([(x0 + k * w / 4, by - h), (x0 + 30 * s + k * (w - 60 * s) / 4, by)], fill=INK, width=5)
    put(C, plate_img('ТРАТЫ', int(44 * s), WHITE, INK, pad=10, r=8, border=INK, bw=5), cx, by - h * 0.45)

def bar(C, cx, by, hgt, label, col=YEL, w=150, top=None):
    d = D(C); d.rounded_rectangle([cx - w / 2, by - hgt, cx + w / 2, by], radius=14, fill=col, outline=INK, width=8)
    if top: put(C, plate_img(top, 36, WHITE, INK, pad=10, r=8, border=INK, bw=5), cx, by - hgt - 50)
    put(C, text_img(label, 34, INK), cx, by + 40)

def sheet(C, cx, cy, a='', b='', k=1.0, rot=-3):
    w, h = 720, 330; im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, w + 8, h + 8], radius=18, fill=WHITE, outline=INK, width=8)
    for y in range(90, h, 70): d.line([(40, y), (w - 24, y)], fill=(200, 220, 240), width=3)
    im.alpha_composite(text_img('МОИ РАСХОДЫ', 50, INK), (40, 34))
    line2 = f"{a or '_____'}  × 300  =" ; im.alpha_composite(text_img(line2, 64, INK), (40, 120))
    t = plate_img(b or '?', 70, YEL, INK, pad=12, r=10); im.alpha_composite(t, ((w + 16 - t.width) // 2, 210))
    put(C, im, cx, cy, k, rot)

def progressbar(C, cx, cy, w, frac, label='ДО СВОБОДЫ'):
    d = D(C); d.rounded_rectangle([cx - w / 2, cy - 22, cx + w / 2, cy + 22], radius=20, fill=WHITE, outline=INK, width=6)
    if frac > 0: d.rounded_rectangle([cx - w / 2 + 6, cy - 16, cx - w / 2 + 6 + (w - 12) * frac, cy + 16], radius=14, fill=YEL)
    put(C, text_img(label, 30, INK), cx, cy - 50)

def circles(F, t, act, done, y=292, alpha=1.0):
    """счётчик вопросов 1-2-3: done — множество отвеченных, act — текущий"""
    d = ImageDraw.Draw(F)
    for j in range(3):
        cx = 540 + (j - 1) * 110; r = 34 * (1.18 if act == j + 1 else 1)
        if j + 1 in done:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=YEL, outline=INK, width=6)
            d.line([(cx - r * 0.45, y), (cx - r * 0.1, y + r * 0.38), (cx + r * 0.5, y - r * 0.4)], fill=INK, width=9)
        else:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=INK if act == j + 1 else WHITE, outline=INK, width=6)
            put(F, text_img(str(j + 1), int(r * 1.2), YEL if act == j + 1 else INK), cx, y + 2)
