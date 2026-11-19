"""Карусель «6 тем, чтобы не тупить»: 10 слайдов 1080x1350 (4:5) по правилам ne-tupi/karuseli/PRAVILA-KARUSELEY.md.
Запуск (из папки ne-tupi/):
  node 3d/frames.js karuseli/6-tem/poses.json /tmp/kadry flat 1080 1920 file
  python3 karuseli/6-tem/slides.py /tmp/kadry/p karuseli/6-tem/slides
Позы в poses.json по номеру кадра: 0 руки вверх (обложка), 1 руки в стороны, 2 держит кошелёк, 3 марионетка,
4 телефон у лица, 5 сидит, 6 болтает, 7 спокойно говорит, 8 в профиль с телескопом, 9 рука вверх (таймер), 10 показывает вперёд."""
import sys, os, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

KD, OUT = sys.argv[1], sys.argv[2]
W, H = 1080, 1350
INK = (17, 17, 17); WH = (255, 255, 255); YEL = (255, 214, 10); GREY = (205, 205, 205)
DG = (88, 88, 88); MG = (150, 150, 150); LG = (236, 234, 228)
FD = '/usr/share/fonts/opentype/inter/'
FB, FX, FS, FM = FD + 'Inter-Black.otf', FD + 'Inter-ExtraBold.otf', FD + 'Inter-SemiBold.otf', FD + 'Inter-Medium.otf'
M = 64                      # боковое поле (правило: не меньше 35 px)
HR = 135                    # радиус головы в пикселях кадра 1080x1920
ANCH = json.load(open(f'{KD}/anchors.json'))
def F(sz, f=FB): return ImageFont.truetype(f, sz)
def tw(d, t, f): b = d.textbbox((0, 0), t, font=f); return b[2] - b[0]

# ---------- текст: крупно → средне → мелко ----------
def title(d, y, lines, sz, x=M, center=False):
    """Крупно. Возвращает низ блока и рамки строк [(x0, y0, x1, y1)]."""
    f = F(sz)
    wmax = max(tw(d, l, f) for l in lines)
    if wmax > W - 2 * M: sz = int(sz * (W - 2 * M) / wmax); f = F(sz)
    boxes = []
    for l in lines:
        b = d.textbbox((0, 0), l, font=f); w = b[2] - b[0]
        xx = (W - w) / 2 if center else x
        d.text((xx - b[0], y - b[1]), l, font=f, fill=INK)
        boxes.append((xx, y, xx + w, y + (b[3] - b[1]))); y += sz * 1.02
    return y, boxes
def mid(d, y, lines, sz=42, x=M, col=INK, center=False):
    f = F(sz, FS)
    for l in lines:
        xx = (W - tw(d, l, f)) / 2 if center else x
        d.text((xx, y), l, font=f, fill=col); y += sz * 1.28
    return y
def small(d, y, items, sz=33, x=M, wrap=None):
    """Мелко: до 3 пунктов, маркер — жёлтый квадрат с чёрной обводкой."""
    f = F(sz, FM)
    for it in items:
        rows = it if isinstance(it, list) else [it]
        d.rounded_rectangle([x, y + sz * .28, x + sz * .5, y + sz * .78], radius=4, fill=YEL, outline=INK, width=3)
        for r in rows: d.text((x + sz * .95, y), r, font=f, fill=DG); y += sz * 1.3
        y += sz * .35
    return y
def plate(d, cx, cy, txt, sz, fill=YEL, col=INK, pad=22, f=FB, outline=None):
    fo = F(sz, f); b = d.textbbox((0, 0), txt, font=fo); w, h = b[2] - b[0], b[3] - b[1]
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .75, cx + w / 2 + pad, cy + h / 2 + pad * .75], radius=16, fill=fill,
                        outline=outline, width=6 if outline else 0)
    d.text((cx - w / 2 - b[0], cy - h / 2 - b[1]), txt, font=fo, fill=col)
def emoji(bg, ch, x, y, sz):
    f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(im).text((4, 4), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox()).resize((sz, sz), Image.LANCZOS); bg.paste(im, (int(x), int(y)), im)
def footer(d, arrow=True):
    f = F(26, FS); t = 'netupi.tv'; d.text(((W - tw(d, t, f)) / 2, 1292), t, font=f, fill=MG)
    if arrow:
        y = 1306; d.line([(W - M - 64, y), (W - M - 14, y)], fill=INK, width=9)
        d.polygon([(W - M, y), (W - M - 26, y - 20), (W - M - 26, y + 20)], fill=INK)

# ---------- человечек: без фона, белая обводка-стикер, мягкая тень ----------
_cache = {}
def cut(i):
    if i in _cache: return _cache[i]
    fr = Image.open(f'{KD}/{i:03d}.png').convert('RGB'); g = fr.convert('L')
    body = g.point(lambda v: 255 if v < 110 else 0)
    inv = ImageChops.invert(body); ImageDraw.floodfill(inv, (0, 0), 128)
    holes = inv.point(lambda v: 255 if v == 255 else 0)           # рот внутри силуэта
    mask = ImageChops.lighter(body, holes); bb = mask.getbbox()
    _cache[i] = (fr, mask, bb); return _cache[i]
def man(bg, i, cx, feet, h, outline=9, shadow=True, flip=False):
    """Ставит позу i: x=540 кадра -> cx, низ силуэта -> feet, высота силуэта h. Возвращает функцию кадр->слайд."""
    fr, mask, bb = cut(i); s = h / (bb[3] - bb[1])
    fw, fh = int(1080 * s), int(1920 * s)
    im = fr.resize((fw, fh), Image.LANCZOS); mk = mask.resize((fw, fh), Image.LANCZOS)
    if flip: im, mk = im.transpose(Image.FLIP_LEFT_RIGHT), mk.transpose(Image.FLIP_LEFT_RIGHT)
    ox, oy = int(cx - 540 * s), int(feet - bb[3] * s)
    if shadow:
        sh = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(sh); sw = h * .36
        sd.ellipse([cx - sw, feet - h * .035, cx + sw, feet + h * .035], fill=70)
        sh = sh.filter(ImageFilter.GaussianBlur(h * .02)); bg.paste((120, 120, 120), (0, 0), sh)
    if outline:
        ring = mk.filter(ImageFilter.MaxFilter(outline * 2 + 1)); bg.paste(WH, (ox, oy), ring)
    bg.paste(im, (ox, oy), mk)
    def P(x, y):
        if flip: x = 1080 - x
        return (ox + x * s, oy + y * s)
    P.s = s; P.top = P(*ANCH[i]['top']); P.hands = [P(*hp) for hp in ANCH[i]['hands']]
    return P

# ---------- предметы ----------
def coin(d, cx, cy, r, wings=True):
    if wings:
        for sx in (-1, 1):
            pts = [(cx + sx * r * .7, cy - r * .1), (cx + sx * r * 2.0, cy - r * 1.0), (cx + sx * r * 1.9, cy - r * .45),
                   (cx + sx * r * 2.1, cy - r * .2), (cx + sx * r * 1.6, cy + r * .2), (cx + sx * r * .7, cy + r * .35)]
            d.polygon(pts, fill=WH, outline=INK, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YEL, outline=INK, width=6)
    f = F(int(r * 1.15)); t = '₽'; b = d.textbbox((0, 0), t, font=f)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), t, font=f, fill=INK)
def wallet(d, cx, cy, s=1):
    w, h = 150 * s, 104 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(18 * s), fill=WH, outline=INK, width=int(8 * s))
    d.rounded_rectangle([cx + w * .08, cy - h * .2, cx + w / 2 + 6 * s, cy + h * .2], radius=int(12 * s), fill=WH, outline=INK, width=int(7 * s))
    d.ellipse([cx + w * .22, cy - 9 * s, cx + w * .22 + 18 * s, cy + 9 * s], fill=YEL, outline=INK, width=3)
def dashed(d, a, b, dash=18, gap=14, w=5, col=INK):
    L = math.dist(a, b); n = int(L // (dash + gap)) + 1
    for k in range(n):
        t0, t1 = k * (dash + gap) / L, min(1, (k * (dash + gap) + dash) / L)
        d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=col, width=w)
def icon(d, kind, cx, cy, r=62):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WH, outline=INK, width=6)
    k = r / 62
    if kind == 'money': coin(d, cx, cy, 34 * k, wings=False)
    elif kind == 'psy':      # мозг: две доли с извилинами
        d.rounded_rectangle([cx - 36 * k, cy - 28 * k, cx + 36 * k, cy + 26 * k], radius=int(26 * k), fill=YEL, outline=INK, width=5)
        d.line([(cx, cy - 26 * k), (cx, cy + 24 * k)], fill=INK, width=4)
        for sx in (-1, 1):
            d.arc([cx + sx * 22 * k - 12 * k, cy - 18 * k, cx + sx * 22 * k + 12 * k, cy], 180, 360, fill=INK, width=4)
            d.arc([cx + sx * 16 * k - 12 * k, cy + 2 * k, cx + sx * 16 * k + 12 * k, cy + 20 * k], 0, 180, fill=INK, width=4)
    elif kind == 'hist':     # колонна
        d.polygon([(cx - 38 * k, cy - 22 * k), (cx, cy - 40 * k), (cx + 38 * k, cy - 22 * k)], fill=INK)
        for x in (-24, 0, 24): d.rectangle([cx + (x - 6) * k, cy - 16 * k, cx + (x + 6) * k, cy + 26 * k], fill=INK)
        d.rectangle([cx - 38 * k, cy + 28 * k, cx + 38 * k, cy + 36 * k], fill=INK)
    elif kind == 'phil':     # бюст мыслителя: голова + «?»
        f = F(int(70 * k)); t = '?'; b = d.textbbox((0, 0), t, font=f)
        d.rounded_rectangle([cx - 28 * k, cy - 34 * k, cx + 28 * k, cy + 34 * k], radius=int(14 * k), fill=YEL)
        d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), t, font=f, fill=INK)
    elif kind == 'talk':     # облачко речи
        d.rounded_rectangle([cx - 38 * k, cy - 30 * k, cx + 38 * k, cy + 18 * k], radius=int(18 * k), fill=INK)
        d.polygon([(cx - 18 * k, cy + 14 * k), (cx - 26 * k, cy + 36 * k), (cx + 2 * k, cy + 16 * k)], fill=INK)
        for x in (-18, 0, 18): d.ellipse([cx + (x - 5) * k, cy - 11 * k, cx + (x + 5) * k, cy - 1 * k], fill=WH)
    elif kind == 'sci':      # колба
        d.polygon([(cx - 10 * k, cy - 38 * k), (cx + 10 * k, cy - 38 * k), (cx + 10 * k, cy - 10 * k), (cx + 34 * k, cy + 32 * k),
                   (cx - 34 * k, cy + 32 * k), (cx - 10 * k, cy - 10 * k)], fill=WH, outline=INK, width=5)
        d.polygon([(cx - 22 * k, cy + 10 * k), (cx + 22 * k, cy + 10 * k), (cx + 32 * k, cy + 29 * k), (cx - 32 * k, cy + 29 * k)], fill=YEL)
        d.line([(cx - 16 * k, cy - 38 * k), (cx + 16 * k, cy - 38 * k)], fill=INK, width=6)
def cloud(d, x0, y0, x1, y1, fill=WH, w=7, tail=None):
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    bumps = [(cx + rx * .62 * math.cos(a), cy + ry * .55 * math.sin(a)) for a in [k * math.pi / 4 for k in range(8)]]
    br = min(rx, ry) * .55
    for (x, y) in bumps: d.ellipse([x - br, y - br, x + br, y + br], fill=INK)
    d.ellipse([cx - rx * .7, cy - ry * .62, cx + rx * .7, cy + ry * .62], fill=INK)
    if tail:
        for k, (tx, ty, tr) in enumerate(tail): d.ellipse([tx - tr - w, ty - tr - w, tx + tr + w, ty + tr + w], fill=INK)
    for (x, y) in bumps: d.ellipse([x - br + w, y - br + w, x + br - w, y + br - w], fill=fill)
    d.ellipse([cx - rx * .7 + w, cy - ry * .62 + w, cx + rx * .7 - w, cy + ry * .62 - w], fill=fill)
    if tail:
        for (tx, ty, tr) in tail: d.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], fill=fill)
def flame(d, cx, by, s=1):
    pts = [(cx, by - 70 * s), (cx + 18 * s, by - 40 * s), (cx + 30 * s, by - 12 * s), (cx + 22 * s, by), (cx - 22 * s, by),
           (cx - 30 * s, by - 14 * s), (cx - 14 * s, by - 34 * s), (cx - 4 * s, by - 26 * s)]
    d.polygon(pts, fill=YEL, outline=INK, width=5)
    d.polygon([(cx, by - 30 * s), (cx + 10 * s, by - 10 * s), (cx, by - 3 * s), (cx - 10 * s, by - 10 * s)], fill=WH)
def check(d, cx, cy, s=1, col=INK):
    d.line([(cx - 16 * s, cy), (cx - 4 * s, cy + 13 * s), (cx + 18 * s, cy - 14 * s)], fill=col, width=int(8 * s), joint='curve')

# ---------- слайды ----------
def new(): bg = Image.new('RGB', (W, H), WH); return bg, ImageDraw.Draw(bg)

def s1():   # обложка: человечек по пояс выходит из-за заголовка, голова на «ТУП», над головой «?»
    bg, d = new(); f = F(150); l1 = 'ТЫ ТУПИШЬ'
    w1 = tw(d, l1, f); x1 = (W - w1) / 2; y1 = 330
    _, bx = title(d, y1, [l1], 150, center=True)
    tup = x1 + tw(d, 'ТЫ ', f) + tw(d, 'ТУП', f) / 2       # центр «ТУП»
    fr, mk, bb = cut(0); s0 = 165 / (2 * HR)                # голова ~165 px
    hy0 = bx[0][3] + 48                                     # центр головы у нижнего края букв: «ТУП» читается
    feet = hy0 + (bb[3] - (ANCH[0]['top'][1] + HR)) * s0
    P = man(bg, 0, tup, feet, s0 * (bb[3] - bb[1]), shadow=False); d = ImageDraw.Draw(bg)
    # всё, что ниже пояса, закрыто блоком текста: человечек «из-за заголовка»
    top2 = int(hy0 + 200); d.rectangle([0, top2, W, H], fill=WH)
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse([tup - 170, top2 - 16, tup + 170, top2 + 16], fill=90)
    bg.paste((140, 140, 140), (0, 0), sh.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(bg)
    d.rectangle([0, top2 + 6, W, H], fill=WH)
    y, _ = title(d, top2 + 30, ['НЕ ПОТОМУ, ЧТО', 'ГЛУПЫЙ'], 112, center=True)
    y = mid(d, y + 50, ['а потому, что школа не научила', 'этим 6 вещам'], 46, center=True)
    hx, hy = P.top; plate(d, hx, y1 - 90, '?', 84, pad=28, outline=INK)
    f2 = F(36, FX); t = 'листай →'; d.text(((W - tw(d, t, f2)) / 2, y + 60), t, font=f2, fill=INK)
    footer(d); return bg

def s2():   # карта: 6 пунктиров от головы к 6 иконкам
    bg, d = new()
    y, _ = title(d, 80, ['6 ТЕМ =', 'НОВЫЙ МОЗГ'], 128)
    y = mid(d, y + 24, ['по 20 минут в день, 3 месяца'], 46)
    P = man(bg, 1, 540, 1150, 560); d = ImageDraw.Draw(bg)
    hx, hy = P.top[0], P.top[1] + 70
    kinds = ['money', 'psy', 'hist', 'phil', 'talk', 'sci']
    pos = [(170, 600), (150, 810), (190, 1020), (890, 1020), (930, 810), (910, 600)]
    for (x, yy) in pos:
        ang = math.atan2(yy - hy, x - hx); a = (hx + 95 * math.cos(ang), hy + 95 * math.sin(ang))
        b = (x - 70 * math.cos(ang), yy - 70 * math.sin(ang)); dashed(d, a, b)
    for k, (x, yy) in zip(kinds, pos): icon(d, k, x, yy)
    f = F(31, FS); t = 'деньги · психология · история · философия · общение · наука'
    d.text(((W - tw(d, t, f)) / 2, 1196), t, font=f, fill=DG)
    footer(d); return bg

def s3():   # деньги: кошелёк, монетки с крылышками улетают на заголовок
    bg, d = new()
    y, bx = title(d, 80, ['1. ЗАРПЛАТА', 'ИСЧЕЗАЕТ', 'НЕ САМА'], 124)
    y = mid(d, y + 30, ['зарабатывать умеют все,', 'понимать деньги — единицы'], 42)
    small(d, y + 46, ['почему растут цены', ['как банк зарабатывает', 'на тебе'], ['что такое', 'сложный процент']])
    P = man(bg, 2, 770, 1215, 620); d = ImageDraw.Draw(bg)
    wx, wy = P.hands[1]; wallet(d, wx + 20, wy - 10, 1.05)
    for (x, yy, r) in ((900, 640, 34), (820, 470, 40), (900, 330, 44), (730, 300, 38)):
        coin(d, x, yy, r)
    footer(d); return bg

def s4():   # психология: марионетка, нитки сквозь заголовок к руке с плашкой SALE
    bg, d = new()
    y, _ = title(d, 150, ['2. ТОБОЙ', 'УПРАВЛЯЮТ.', 'ТЫ НЕ', 'ЗАМЕЧАЕШЬ'], 112)
    yy = mid(d, y + 26, ['откладываешь дела и ведёшься', 'на «скидку 70%» —', 'это не случайность'], 40)
    small(d, yy + 40, ['ловушки мышления', 'как работают привычки', ['как тобой', 'манипулируют']])
    P = man(bg, 3, 820, 1215, 600); d = ImageDraw.Draw(bg)
    bx0, bx1, by = 680, 980, 120                     # вага (перекладина)
    pts = [P.hands[0], P.hands[1], P.top]
    for (x, yy2), sx in zip(pts, (bx0 + 20, bx1 - 20, (bx0 + bx1) / 2)):
        d.line([(sx, by + 6), (x, yy2)], fill=DG, width=4)
    d.rounded_rectangle([bx0, by - 10, bx1, by + 12], radius=10, fill=INK)
    d.rounded_rectangle([(bx0 + bx1) / 2 - 11, by - 70, (bx0 + bx1) / 2 + 11, by + 60], radius=10, fill=INK)
    d.line([((bx0 + bx1) / 2, by - 40), ((bx0 + bx1) / 2 + 60, -40)], fill=INK, width=34)   # рука кукловода сверху
    plate(d, bx1 - 30, by + 75, 'SALE', 44, outline=INK, pad=16)
    footer(d); return bg

def s5():   # история: римский шлем, телефон, гребень заходит на заголовок
    bg, d = new()
    y, _ = title(d, 80, ['3. ВСЁ ЭТО', 'УЖЕ БЫЛО'], 140)
    yy = mid(d, y + 40, ['история — инструкция,', 'как люди снова и снова', 'делают одни ошибки'], 42)
    small(d, yy + 46, ['почему пал Рим', ['откуда взялись', 'деньги и банки'], 'как поднимались с нуля'])
    P = man(bg, 4, 790, 1215, 800); d = ImageDraw.Draw(bg)
    hx, ht = P.top; hr = HR * P.s
    # шлем: купол поверх головы + назатыльник + нащёчник
    HG = (150, 150, 150)
    for sx in (-1, 1):                               # нащёчники
        d.polygon([(hx + sx * hr * 1.02, ht + hr * .8), (hx + sx * hr * .98, ht + hr * 1.55), (hx + sx * hr * .62, ht + hr * 1.7),
                   (hx + sx * hr * .7, ht + hr * .9)], fill=HG, outline=INK, width=6)
    d.chord([hx - hr * 1.06, ht - hr * .06, hx + hr * 1.06, ht + hr * 1.8], 180, 360, fill=HG, outline=INK, width=7)
    d.rounded_rectangle([hx - hr * 1.2, ht + hr * .8, hx + hr * 1.2, ht + hr * .98], radius=8, fill=HG, outline=INK, width=6)
    d.line([(hx, ht + hr * .05), (hx, ht + hr * .8)], fill=INK, width=6)
    # гребень (жёлтый веер) уходит вверх на заголовок
    cx0, cy0 = hx, ht + hr * .02; R1x, R1y = hr * 1.25, hr * 1.25
    d.pieslice([cx0 - R1x, cy0 - R1y, cx0 + R1x, cy0 + R1y], 180, 360, fill=YEL, outline=INK, width=7)
    for k in range(1, 9):
        a = math.pi + math.pi * k / 9
        d.line([(cx0 + hr * .3 * math.cos(a), cy0 + hr * .3 * math.sin(a)), (cx0 + R1x * .93 * math.cos(a), cy0 + R1y * .93 * math.sin(a))], fill=INK, width=4)
    d.rectangle([cx0 - hr * 1.3, cy0, cx0 + hr * 1.3, cy0 + 2], fill=INK)
    px, py = P.hands[1]; d.rounded_rectangle([px - 34, py - 64, px + 34, py + 54], radius=12, fill=WH, outline=INK, width=7)
    d.rectangle([px - 22, py - 46, px + 22, py + 34], fill=YEL)
    footer(d); return bg

def s6():   # философия: в тоге сидит на камне, вокруг огоньки, голова на заголовке
    bg, d = new()
    y, bx = title(d, 80, ['4. НЕ БЕСИСЬ', 'ИЗ-ЗА ТОГО, ЧТО', 'НЕ МОЖЕШЬ', 'ИЗМЕНИТЬ'], 106)
    yy = mid(d, y + 30, ['это написал', 'римский император', '2000 лет назад.', 'Работает до сих пор'], 38)
    small(d, yy + 40, ['стоицизм', ['Сократ: спрашивай,', 'а не доказывай'], 'факт или мнение?'], 32)
    hx_t = bx[-1][2] - 70                               # голова на конец «ИЗМЕНИТЬ»
    sx, sy = hx_t + 30, 1100                          # камень
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse([sx - 200, sy + 40, sx + 200, sy + 74], fill=80)
    bg.paste((120, 120, 120), (0, 0), sh.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(bg)
    d.rounded_rectangle([sx - 150, sy - 80, sx + 110, sy + 56], radius=40, fill=(175, 175, 175), outline=INK, width=7)
    h6 = (sy - 40 - (bx[-1][1] + 20)) / (1 - 70 / 1050)
    P = man(bg, 5, sx, sy - 40, h6, shadow=False, outline=9); d = ImageDraw.Draw(bg)
    hx, ht = P.top; hr = HR * P.s
    # тога: белая перевязь через плечо
    tx, ty = hx - hr * .1, ht + hr * 2.45
    d.polygon([(tx - hr * .6, ty - 4), (tx - hr * .05, ty - 8), (tx + hr * .7, ty + hr * 2.1), (tx + hr * .1, ty + hr * 2.3)], fill=WH, outline=INK, width=6)
    for k in range(3): d.line([(tx - hr * .42 + k * hr * .16, ty + 6), (tx + hr * .22 + k * hr * .16, ty + hr * 2.1)], fill=GREY, width=4)
    for (x, b, s) in ((sx - 230, 1160, 1.1), (sx + 200, 1150, 1.2), (sx - 210, 930, .9), (sx + 210, 900, 1.0), (sx + 230, 700, .8)): flame(d, min(x, W - M - 30), b, s)
    footer(d); return bg

def s7():   # общение: каша из слов против одного чистого облачка
    bg, d = new()
    y, _ = title(d, 80, ['5. УМНАЯ МЫСЛЬ', 'НИЧЕГО', 'НЕ СТОИТ'], 116)
    yy = mid(d, y + 26, ['если ты не можешь', 'её донести'], 42)
    small(d, yy + 40, ['как рассказывать истории', 'как спорить без наезда', ['как слушать, а не ждать', 'своей очереди']], 32)
    A = man(bg, 6, 230, 1215, 360); B = man(bg, 7, 820, 1215, 360); d = ImageDraw.Draw(bg)
    # каша: наложенные слова-обрывки у рта A
    ax, ay = A.top[0] + 110, A.top[1] + 230
    for k, (t, dx, dy, a) in enumerate((('бла', 0, 0, 12), ('короче', 40, -40, -15), ('типа', -60, -80, 25), ('ну', 90, -100, -30),
                                         ('вот', -10, -130, 8), ('как бы', 60, -170, -10), ('эээ', -70, -190, 20))):
        f = F(30, FX); b = d.textbbox((0, 0), t, font=f); im = Image.new('RGBA', (b[2] + 10, b[3] + 10), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((5 - b[0], 5 - b[1]), t, font=f, fill=(60, 60, 60, 255)); im = im.rotate(a, expand=True)
        bg.paste(im, (int(ax + dx), int(ay + dy - 60)), im)
    d = ImageDraw.Draw(bg)
    for k in range(5):
        cx, cy = ax + 40 + k * 7, ay - 150 + k * 9
        d.arc([cx - 90 + k * 8, cy - 60, cx + 70 - k * 6, cy + 70], 20 * k, 20 * k + 300, fill=MG, width=3)
    # чистое облачко B: заходит на заголовок
    bx, by = B.top
    cloud(d, 600, 330, 1020, 640, tail=[(bx - 20, by - 50, 14), (bx - 5, by - 95, 22)])
    plate(d, 810, 485, 'ПОНЯТНО', 52, pad=20)
    footer(d); return bg

def s8():   # наука: телескоп, труба перекрывает заголовок
    bg, d = new()
    y, bx = title(d, 80, ['6. «МНЕ БАБУШКА', 'СКАЗАЛА» —', 'НЕ ИСТОЧНИК'], 104)
    P = man(bg, 8, 280, 1215, 600); d = ImageDraw.Draw(bg)
    hx, ht = P.top; hr = HR * P.s
    e = (hx + hr * .95, ht + hr * .9)                  # окуляр у лица
    end = (1000, 330); ang = math.atan2(end[1] - e[1], end[0] - e[0]); nx, ny = -math.sin(ang), math.cos(ang)
    def seg(a, b, w0, w1, fill):
        pts = [(a[0] + nx * w0, a[1] + ny * w0), (b[0] + nx * w1, b[1] + ny * w1), (b[0] - nx * w1, b[1] - ny * w1), (a[0] - nx * w0, a[1] - ny * w0)]
        d.polygon(pts, fill=fill, outline=INK, width=7)
    L = math.dist(e, end); u = ((end[0] - e[0]) / L, (end[1] - e[1]) / L)
    p1 = (e[0] + u[0] * L * .18, e[1] + u[1] * L * .18); p2 = (e[0] + u[0] * L * .55, e[1] + u[1] * L * .55)
    mid_ = (e[0] + u[0] * L * .45, e[1] + u[1] * L * .45)
    mid_ = (e[0] + u[0] * L * .2, e[1] + u[1] * L * .2)
    for fx in (-90, 0, 90): d.line([mid_, (mid_[0] + fx, 1215)], fill=INK, width=10)   # тренога
    seg(e, p1, 16, 22, WH); seg(p1, p2, 30, 34, (175, 175, 175)); seg(p2, end, 46, 54, WH)
    seg((p2[0] + u[0] * 20, p2[1] + u[1] * 20), (p2[0] + u[0] * 60, p2[1] + u[1] * 60), 56, 56, YEL)
    yy = mid(d, 760, ['наука объясняет', 'мир лучше', 'любых догадок'], 40, x=620)
    small(d, yy + 36, [['как работает мозг', 'и почему', 'он ленится'], 'космос и масштабы', ['эволюция', 'на пальцах']], 31, x=620)
    footer(d); return bg

def s9():   # практика: таймер в руке заходит на заголовок, чек-лист с галочками
    bg, d = new()
    y, _ = title(d, 170, ['ОБЪЯСНИ ДРУГУ', 'ЗА МИНУТУ'], 116)
    yy = mid(d, y + 26, ['не можешь объяснить —', 'значит, не понял'], 44)
    # чек-лист (мелко)
    x0, y0, x1 = M, yy + 50, 600; rows = ['20 минут в день', 'одна тема — две недели', ['прочитал → пересказал', '→ галочка']]
    y1 = y0 + 40 + 3 * 96 + 40
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=LG, outline=INK, width=6)
    f = F(32, FM); ry = y0 + 40
    for r in rows:
        d.rounded_rectangle([x0 + 30, ry, x0 + 80, ry + 50], radius=10, fill=YEL, outline=INK, width=5); check(d, x0 + 55, ry + 26, 1.1)
        lines = r if isinstance(r, list) else [r]
        for k, l in enumerate(lines): d.text((x0 + 104, ry + 6 + k * 40), l, font=f, fill=DG)
        ry += 96
    P = man(bg, 9, 820, 1215, 640); d = ImageDraw.Draw(bg)
    tx, ty = P.hands[1]; ty -= 70; r = 82
    d.rectangle([tx - 14, ty - r - 34, tx + 14, ty - r + 4], fill=INK); d.rounded_rectangle([tx - 34, ty - r - 52, tx + 34, ty - r - 28], radius=8, fill=INK)
    d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=WH, outline=INK, width=10)
    d.pieslice([tx - r + 16, ty - r + 16, tx + r - 16, ty + r - 16], -90, 30, fill=YEL)
    d.line([(tx, ty), (tx, ty - r + 22)], fill=INK, width=8); d.ellipse([tx - 10, ty - 10, tx + 10, ty + 10], fill=INK)
    f2 = F(30, FX); t = '20:00'; d.text((tx - tw(d, t, f2) / 2, ty + 22), t, font=f2, fill=INK)
    footer(d); return bg

def s10():  # финал: «НЕ ТУПИ.» на жёлтой плашке, рука заходит на заголовок
    bg, d = new()
    f = F(200); t = 'НЕ ТУПИ.'; b = d.textbbox((0, 0), t, font=f); w, h = b[2] - b[0], b[3] - b[1]
    x, y = (W - w) / 2, 150
    d.rounded_rectangle([x - 34, y - 34, x + w + 34, y + h + 40], radius=24, fill=YEL); d.text((x - b[0], y - b[1]), t, font=f, fill=INK)
    P0 = ANCH[10]; fr, mk, bb = cut(10); hand_y = P0['hands'][1][1]
    h10 = (1215 - (y + h + 10)) / ((bb[3] - hand_y) / (bb[3] - bb[1]))   # кисть заходит на плашку
    P = man(bg, 10, 800, 1215, h10); d = ImageDraw.Draw(bg)
    yy = mid(d, 560, ['через 3 месяца', 'ты будешь умнее', '90% своего', 'окружения.', 'Или продолжишь', 'листать рилсы'], 42)
    f2 = F(32, FM); t1 = 'сохрани '; d.text((M, yy + 60), t1, font=f2, fill=DG); ex = M + tw(d, t1, f2)
    emoji(bg, '📌', ex, yy + 62, 32); d = ImageDraw.Draw(bg)
    d.text((ex + 42, yy + 60), 'и отправь другу,', font=f2, fill=DG); d.text((M, yy + 102), 'которому это надо', font=f2, fill=DG)
    footer(d, arrow=False); return bg

os.makedirs(OUT, exist_ok=True)
SL = (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)
for i, fn in enumerate(SL, 1): fn().save(f'{OUT}/slide-{i:02d}.png')
sh = Image.new('RGB', (5 * 340 + 10, 2 * 425 + 10), (40, 40, 40))
for i in range(len(SL)):
    im = Image.open(f'{OUT}/slide-{i + 1:02d}.png').resize((324, 405)); sh.paste(im, (10 + (i % 5) * 340, 10 + (i // 5) * 425))
sh.save(f'{OUT}/obzor.png')
