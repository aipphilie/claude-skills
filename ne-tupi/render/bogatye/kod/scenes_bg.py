"""Предметы рилса «Реальные привычки богатых» (по чужому рилсу, наш поворот: стань богатой семьёй сам). Движок «Конца света» (весь экран, белый фон)."""
from scenes_ap import *
GOLD = (244, 190, 30); GOLDD = (186, 132, 10); SMOO = (110, 190, 80); SEA = (90, 170, 220); SAND = (240, 214, 150); LEAF = (60, 160, 80)
BOTTLE = (60, 150, 80); LIVER = (170, 70, 60); BLUE = (40, 90, 200); PURP = (230, 220, 245)

# ---------- персонажи ----------
def chain_on(C, cx, feet, s, u=0):
    d = D(C); y0 = feet - 945 * s; w = 100 * s; sag = 120 * s; r = max(3, 13 * s)
    for j in range(15):
        q = j / 14; x = cx - w + 2 * w * q; y = y0 + sag * (1 - (2 * q - 1) ** 2)
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=GOLD, outline=GOLDD, width=max(1, int(3 * s)))
    my = y0 + sag + 34 * s; mr = 34 * s; sw = 4 * s_(u * 5)
    d.ellipse([cx + sw - mr, my - mr, cx + sw + mr, my + mr], fill=GOLD, outline=GOLDD, width=max(2, int(5 * s)))
    d.text((cx + sw, my), '$', font=font2(max(8, mr * 1.2)), fill=GOLDD, anchor='mm')
def rich(C, clip, u, cx, s=0.4, feet=None, flip=False, chain=True, rot=0):
    """богач: корона + сигара (3D) + золотая цепь"""
    feet = feet or G; man(C, 'r_' + clip, u, cx, feet, s, flip=flip, rot=rot)
    if chain and not rot and clip not in ('walkR',): chain_on(C, cx, feet, s, u)
def dad(C, clip, u, cx, s=0.4, feet=None, flip=False): man(C, 'd_' + clip, u, cx, feet or G, s, flip=flip)
def label(C, text, cx, cy, sz=44, bg=YEL, fg=INK, rot=0): put(C, plate_img(text, sz, bg, fg, pad=12, r=10, border=INK, bw=4), cx, cy, 1, rot)

# ---------- заголовок пункта и номер ----------
def badge(C, n, u=1.0, cx=540, cy=300, r=44):
    if u < 0: return
    k = back(u / 0.2); d = D(C); rr = r * k
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=RED, outline=INK, width=6)
    put(C, text_img(str(n), int(r * 1.15), WHITE), cx, cy + 2, k)
def head(C, u, a, b=None, tb=None, n=None, sza=110, szb=96, col=INK, bcol=YEL):
    if n: badge(C, n, u)
    slam(C, u, a, 540, 420, sza, col)
    if b: plate(C, tb if tb is not None else u - 0.12, b, 540, 570, szb, bcol, INK, -3 if (n or 0) % 2 else 3)
def bigno(C, u, n, word):
    """весь экран: огромная цифра пункта"""
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 880, u, r0=430, col=(246, 200, 0), seed=n)
    k = back(u / 0.2); d = D(C); r = 300 * k
    d.ellipse([540 - r, 880 - r, 540 + r, 880 + r], fill=INK)
    put(C, text_img(str(n), 420, YEL), 540, 885, k, -6 + 3 * s_(u * 9))
    slam(C, u - 0.05, word, 540, 420, 130)

# ---------- предметы ----------
def alarm(C, cx, cy, s=1.0, u=0, ring=True, text='5:00'):
    d = D(C); j = (8 * s_(u * 70) if ring else 0); cx2 = cx + j * s
    for sd in (-1, 1):
        bx = cx2 + sd * 150 * s; by = cy - 190 * s; d.ellipse([bx - 70 * s, by - 60 * s, bx + 70 * s, by + 60 * s], fill=RED, outline=INK, width=int(9 * s))
        d.line([cx2 + sd * 120 * s, cy + 170 * s, cx2 + sd * 170 * s, cy + 260 * s], fill=INK, width=int(18 * s))
    r = 230 * s; d.ellipse([cx2 - r, cy - r, cx2 + r, cy + r], fill=RED, outline=INK, width=int(12 * s))
    r2 = 185 * s; d.ellipse([cx2 - r2, cy - r2, cx2 + r2, cy + r2], fill=WHITE, outline=INK, width=int(7 * s))
    put(C, text_img(text, int(120 * s), INK), cx2, cy)
    if ring:
        for sd in (-1, 1):
            for q in range(3):
                rr = (270 + q * 50 + 30 * ((u * 5) % 1)) * s; d.arc([cx2 - rr, cy - rr, cx2 + rr, cy + rr], (-40 if sd > 0 else 140) - 90 + 90, (40 if sd > 0 else 220) - 90 + 90, fill=INK, width=int(10 * s))
def smoothie(C, cx, by, s=1.0, rot=0):
    w0, w1, h = 120 * s, 170 * s, 380 * s; im = Image.new('RGBA', (int(w1 * 2 + 40), int(h + 200 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = im.width / 2; top = 180 * s
    d.line([c + 20 * s, top + 40 * s, c + 110 * s, 10 * s], fill=RED, width=int(22 * s))
    d.polygon([(c - w1, top), (c + w1, top), (c + w0, top + h), (c - w0, top + h)], fill=SMOO, outline=INK)
    d.line([(c - w1, top), (c + w1, top), (c + w0, top + h), (c - w0, top + h), (c - w1, top)], fill=INK, width=int(10 * s))
    d.ellipse([c - w1 - 10 * s, top - 40 * s, c + w1 + 10 * s, top + 30 * s], fill=(140, 214, 110), outline=INK, width=int(8 * s))
    for (x, y) in [(-50, 130), (40, 210), (-10, 290), (60, 100)]: d.ellipse([c + x * s - 14 * s, top + y * s - 14 * s, c + x * s + 14 * s, top + y * s + 14 * s], fill=(80, 150, 60))
    put(C, im, cx, by - im.height / 2, 1, rot)
def ribbon(C, x, y0, y1, broke=0.0):
    d = D(C); d.rectangle([x - 14, y0, x + 14, y1], fill=STEEL2, outline=INK, width=4)
def envelope(C, cx, cy, w=260, rot=0, text='', open_=0, cash=0):
    h = w * 0.62; im = Image.new('RGBA', (int(w) + 12, int(h * 1.6) + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im); oy = int(h * 0.6)
    if cash:
        for j in range(cash): t = bill_img(int(w * 0.8)); im.alpha_composite(t, (int(w * 0.1 + j * 6), int(oy - h * 0.45 - j * 10)))
    d.rectangle([6, oy, w + 6, oy + h], fill=PAPER, outline=INK, width=7)
    d.line([6, oy, w / 2 + 6, oy + h * 0.55, w + 6, oy], fill=INK, width=6)
    if text:
        t = text_img(text, int(w * 0.13), INK); im.alpha_composite(t, (int(6 + w / 2 - t.width / 2), int(oy + h * 0.68)))
    put(C, im, cx, cy, 1, rot)
def taxbox(C, cx, by, s=1.0, val='0 ₽'):
    d = D(C); w, h = 360 * s, 460 * s; x0 = cx - w / 2
    d.rectangle([x0, by - h, x0 + w, by], fill=WHITE, outline=INK, width=int(9 * s))
    d.rounded_rectangle([cx - 110 * s, by - h + 150 * s, cx + 110 * s, by - h + 172 * s], radius=8, fill=INK)
    put(C, text_img('НАЛОГИ', int(70 * s), INK), cx, by - h + 80 * s)
    put(C, text_img(val, int(90 * s), RED), cx, by - h + 290 * s)
def wash(C, cx, by, s=1.0, u=0, bills=True, foam=0.0):
    d = D(C); w, h = 440 * s, 540 * s; x0 = cx - w / 2; y0 = by - h
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=int(30 * s), fill=WHITE, outline=INK, width=int(10 * s))
    d.line([x0, y0 + 100 * s, x0 + w, y0 + 100 * s], fill=INK, width=int(7 * s))
    d.ellipse([x0 + w - 90 * s, y0 + 30 * s, x0 + w - 40 * s, y0 + 80 * s], fill=LG, outline=INK, width=5); d.rounded_rectangle([x0 + 30 * s, y0 + 38 * s, x0 + 170 * s, y0 + 68 * s], radius=8, fill=LG, outline=INK, width=4)
    cy = y0 + 330 * s; r = 160 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=STEEL, outline=INK, width=int(12 * s)); r2 = 125 * s
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(200, 226, 245), outline=INK, width=int(6 * s))
    if bills:
        for j in range(5):
            a = u * 9 + j * 2 * math.pi / 5; bill(C, cx + math.cos(a) * 62 * s, cy + math.sin(a) * 62 * s, 110 * s, math.degrees(-a) + 90)
    if foam > 0:
        rnd = random.Random(4)
        for j in range(int(18 * clamp(foam))):
            x = cx + rnd.uniform(-1.3, 1.3) * w / 2; y = y0 - rnd.uniform(0, 260) * s * foam + 40 * s_(u * 3 + j); rr = rnd.uniform(18, 50) * s
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(230, 244, 255), outline=(120, 170, 210), width=4)
def shop(C, cx, by, w, h, sign, u=0, col=(196, 220, 240)):
    d = D(C); x0 = cx - w / 2
    d.rectangle([x0, by - h, x0 + w, by], fill=WALL, outline=INK, width=8)
    d.rectangle([x0 - 20, by - h - 110, x0 + w + 20, by - h + 10], fill=RED, outline=INK, width=8)
    put(C, text_img(sign, 70, WHITE), cx, by - h - 50)
    for j in range(6):
        x = x0 - 20 + j * (w + 40) / 6; d.polygon([(x, by - h + 10), (x + (w + 40) / 6, by - h + 10), (x + (w + 40) / 12, by - h + 70)], fill=WHITE if j % 2 else RED, outline=INK)
    d.rectangle([x0 + 40, by - h + 120, x0 + w * 0.55, by - 40], fill=col, outline=INK, width=7)
    d.rectangle([x0 + w * 0.65, by - h + 140, x0 + w - 40, by], fill=WOODD, outline=INK, width=7)
def bottle(C, cx, by, s=1.0, rot=0, col=BOTTLE):
    im = Image.new('RGBA', (int(110 * s) + 10, int(330 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = im.width / 2
    d.rounded_rectangle([c - 50 * s, 120 * s, c + 50 * s, 325 * s], radius=int(22 * s), fill=col, outline=INK, width=max(3, int(7 * s)))
    d.rectangle([c - 18 * s, 20 * s, c + 18 * s, 130 * s], fill=col, outline=INK, width=max(3, int(6 * s))); d.rectangle([c - 20 * s, 8 * s, c + 20 * s, 34 * s], fill=GOLD, outline=INK, width=max(2, int(4 * s)))
    d.rectangle([c - 44 * s, 190 * s, c + 44 * s, 260 * s], fill=PAPER, outline=INK, width=max(2, int(4 * s)))
    put(C, im, cx, by - im.height / 2, 1, rot)
def flipchart(C, cx, by, s=1.0, text='ПЛАН'):
    d = D(C); w, h = 300 * s, 360 * s
    for sd in (-1, 1): d.line([cx, by - h - 40 * s, cx + sd * w * 0.55, by], fill=INK, width=int(12 * s))
    d.rectangle([cx - w / 2, by - h - 60 * s, cx + w / 2, by - 120 * s], fill=WHITE, outline=INK, width=int(8 * s))
    put(C, text_img(text, int(46 * s), INK), cx, by - h + 10 * s)
    d.line([cx - w * 0.35, by - 160 * s, cx - w * 0.1, by - 220 * s, cx + 0.05 * w, by - 190 * s, cx + w * 0.35, by - 290 * s], fill=RED, width=int(10 * s))
def yacht(C, cx, by, s=1.0, u=0, name='ЯХТА'):
    d = D(C); bob = 8 * s_(u * 4) * s; by = by + bob
    d.polygon([(cx - 420 * s, by - 140 * s), (cx + 440 * s, by - 140 * s), (cx + 320 * s, by), (cx - 340 * s, by)], fill=WHITE, outline=INK)
    d.line([(cx - 420 * s, by - 140 * s), (cx + 440 * s, by - 140 * s), (cx + 320 * s, by), (cx - 340 * s, by), (cx - 420 * s, by - 140 * s)], fill=INK, width=int(10 * s))
    d.rectangle([cx - 400 * s, by - 100 * s, cx + 400 * s, by - 76 * s], fill=BLUE)
    d.polygon([(cx - 260 * s, by - 140 * s), (cx - 200 * s, by - 250 * s), (cx + 200 * s, by - 250 * s), (cx + 280 * s, by - 140 * s)], fill=WHITE, outline=INK)
    d.line([(cx - 260 * s, by - 140 * s), (cx - 200 * s, by - 250 * s), (cx + 200 * s, by - 250 * s), (cx + 280 * s, by - 140 * s)], fill=INK, width=int(9 * s))
    for j in range(4): d.rounded_rectangle([cx - 170 * s + j * 90 * s, by - 225 * s, cx - 110 * s + j * 90 * s, by - 170 * s], radius=8, fill=SKY, outline=INK, width=5)
    d.polygon([(cx - 130 * s, by - 250 * s), (cx - 80 * s, by - 330 * s), (cx + 120 * s, by - 330 * s), (cx + 150 * s, by - 250 * s)], fill=WHITE, outline=INK)
    d.line([(cx - 130 * s, by - 250 * s), (cx - 80 * s, by - 330 * s), (cx + 120 * s, by - 330 * s), (cx + 150 * s, by - 250 * s)], fill=INK, width=int(8 * s))
    put(C, text_img(name, int(40 * s), INK), cx + 160 * s, by - 112 * s)
def water(C, y, u=0, col=SEA):
    d = D(C); d.rectangle([0, y, CW, CH], fill=col)
    for j in range(14):
        x = (j * 90 + u * 60) % (CW + 90) - 45; d.arc([x - 40, y - 14, x + 40, y + 26], 200, 340, fill=WHITE, width=6)
def briefcase(C, cx, cy, s=1.0, rot=0, open_=0.0):
    im = Image.new('RGBA', (int(300 * s) + 10, int(240 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([100 * s, 5, 200 * s, 70 * s], radius=int(20 * s), outline=INK, width=int(14 * s))
    d.rounded_rectangle([5, 50 * s, 300 * s, 235 * s], radius=int(20 * s), fill=(110, 70, 40), outline=INK, width=int(9 * s))
    d.rectangle([5, 120 * s, 300 * s, 132 * s], fill=INK); d.rectangle([130 * s, 108 * s, 175 * s, 145 * s], fill=GOLD, outline=INK, width=4)
    put(C, im, cx, cy, 1, rot)
    if open_ > 0:
        for j in range(4): bill(C, cx + (j - 1.5) * 60 * s, cy - 80 * s - 120 * s * eo(open_) - j * 15, 140 * s, (j - 1.5) * 18)
def desk(C, cx, by, w=520, h=260):
    d = D(C); d.rectangle([cx - w / 2, by - h, cx + w / 2, by - h + 34], fill=WOOD, outline=INK, width=7)
    d.rectangle([cx - w / 2 + 20, by - h + 34, cx - w / 2 + 180, by], fill=WOODD, outline=INK, width=7); d.rectangle([cx + w / 2 - 180, by - h + 34, cx + w / 2 - 20, by], fill=WOODD, outline=INK, width=7)
    d.line([cx - w / 2 + 50, by - h + 120, cx - w / 2 + 150, by - h + 120], fill=INK, width=6)
def plane(C, cx, cy, s=1.0, rot=0, bag=True):
    im = Image.new('RGBA', (int(560 * s), int(300 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(220 * s, 150 * s), (330 * s, 150 * s), (210 * s, 280 * s), (160 * s, 280 * s)], fill=LG, outline=INK)
    d.rounded_rectangle([30 * s, 110 * s, 520 * s, 175 * s], radius=int(32 * s), fill=WHITE, outline=INK, width=int(8 * s))
    d.polygon([(40 * s, 120 * s), (20 * s, 30 * s), (90 * s, 30 * s), (130 * s, 115 * s)], fill=RED, outline=INK)
    for j in range(6): d.ellipse([200 * s + j * 46 * s, 128 * s, 222 * s + j * 46 * s, 150 * s], fill=SKY, outline=INK, width=3)
    d.polygon([(250 * s, 145 * s), (330 * s, 145 * s), (220 * s, 20 * s), (190 * s, 20 * s)], fill=LG, outline=INK)
    if bag:
        d.line([290 * s, 175 * s, 290 * s, 215 * s], fill=INK, width=int(5 * s)); d.ellipse([240 * s, 205 * s, 340 * s, 295 * s], fill=BOXC, outline=INK, width=int(6 * s))
        d.text((290 * s, 252 * s), '$', font=font2(int(50 * s)), fill=INK, anchor='mm')
    put(C, im, cx, cy, 1, rot)
def moneybag(C, cx, by, s=1.0, rot=0, sign='$'):
    im = Image.new('RGBA', (int(260 * s) + 10, int(300 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = im.width / 2
    d.ellipse([10, 80 * s, 260 * s, 300 * s], fill=BOXC, outline=INK, width=int(8 * s)); d.polygon([(c - 50 * s, 95 * s), (c - 70 * s, 20 * s), (c + 70 * s, 20 * s), (c + 50 * s, 95 * s)], fill=BOXC, outline=INK)
    d.line([c - 60 * s, 90 * s, c + 60 * s, 90 * s], fill=INK, width=int(10 * s))
    d.text((c, 200 * s), sign, font=font2(int(110 * s)), fill=INK, anchor='mm'); put(C, im, cx, by - im.height / 2, 1, rot)
def island(C, cx, by, s=1.0, u=0, sign='ОФШОР'):
    d = D(C); d.pieslice([cx - 360 * s, by - 120 * s, cx + 360 * s, by + 120 * s], 180, 360, fill=SAND, outline=INK, width=int(8 * s))
    tx = cx + 40 * s; d.line([tx, by - 60 * s, tx - 40 * s, by - 380 * s], fill=WOODD, width=int(30 * s))
    for a in (-160, -120, -60, -20, -90):
        r = 190 * s; aa = math.radians(a + 6 * s_(u * 3)); x2 = tx - 40 * s + math.cos(aa) * r; y2 = by - 380 * s + math.sin(aa) * r * 0.5 + 60 * s
        d.polygon([(tx - 40 * s, by - 380 * s), (x2, y2), (tx - 40 * s + math.cos(aa) * r * 0.5, by - 380 * s + math.sin(aa) * r * 0.25 + 50 * s)], fill=LEAF, outline=INK)
    if sign: d.line([cx - 200 * s, by - 50 * s, cx - 200 * s, by - 200 * s], fill=INK, width=int(10 * s)); label(C, sign, cx - 200 * s, by - 220 * s, int(46 * s), WHITE)
def firm(C, cx, by, s, name, u=0, bankrupt=0.0):
    block(C, cx, by, 330 * s, 460 * s, 3, 4, PANEL, 0, 2)
    label(C, name, cx, by - 500 * s, int(40 * s), WHITE)
    if bankrupt > 0: stamp(C, bankrupt, 'БАНКРОТ', cx, by - 260 * s, int(60 * s), RED, -12)
def crown(C, cx, cy, w=160, rot=0):
    h = w * 0.7; im = Image.new('RGBA', (int(w) + 12, int(h) + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(6, 6 + h), (6, 6 + h * 0.25), (6 + w * 0.25, 6 + h * 0.55), (6 + w * 0.5, 6), (6 + w * 0.75, 6 + h * 0.55), (6 + w, 6 + h * 0.25), (6 + w, 6 + h)]
    d.polygon(pts, fill=GOLD, outline=INK); d.line(pts + [pts[0]], fill=INK, width=max(3, int(w * 0.05)))
    d.ellipse([6 + w * 0.42, 6 + h * 0.6, 6 + w * 0.58, 6 + h * 0.84], fill=RED, outline=INK, width=3)
    put(C, im, cx, cy, 1, rot)
def crib(C, cx, by, s=1.0, u=0, baby=True):
    d = D(C); w, h = 560 * s, 300 * s; x0 = cx - w / 2
    for j in range(9): x = x0 + 40 * s + j * (w - 80 * s) / 8; d.rounded_rectangle([x - 12 * s, by - h, x + 12 * s, by - 40 * s], radius=6, fill=GOLD, outline=INK, width=4)
    d.rounded_rectangle([x0, by - h - 30 * s, x0 + w, by - h + 10 * s], radius=14, fill=GOLD, outline=INK, width=7)
    d.rounded_rectangle([x0, by - 120 * s, x0 + w, by - 40 * s], radius=14, fill=GOLD, outline=INK, width=7)
    for sd in (-1, 1): d.rounded_rectangle([cx + sd * w / 2 - 24 * s, by - h - 80 * s, cx + sd * w / 2 + 24 * s, by], radius=12, fill=GOLDD, outline=INK, width=7)
    if baby:
        man(C, 'cheer', u, cx, by - 110 * s, 0.24 * s); crown(C, cx + 4 * s, by - 110 * s - HEAD(0.24 * s) * 1.05 - 85 * s, 100 * s, -10)
def bars(C, k=1.0, x0=200, x1=880, y0=600, y1=FEET + 6):
    if k <= 0: return
    d = D(C); dy = (1 - eo(k)) * -900
    d.rectangle([x0 - 20, y0 + dy - 30, x1 + 20, y0 + dy], fill=STEEL2, outline=INK, width=6)
    for j in range(7): x = x0 + j * (x1 - x0) / 6; d.rectangle([x - 12, y0 + dy, x + 12, y1 + dy], fill=STEEL, outline=INK, width=5)
def liver(C, cx, cy, s=1.0, crack=0.0, u=0):
    d = D(C); j = 4 * s_(u * 20) * crack
    pts = [(cx - 230 * s + j, cy - 40 * s), (cx - 120 * s, cy - 150 * s), (cx + 120 * s, cy - 140 * s), (cx + 240 * s, cy - 100 * s), (cx + 160 * s, cy + 20 * s), (cx - 40 * s, cy + 130 * s), (cx - 200 * s, cy + 70 * s)]
    d.polygon(pts, fill=LIVER, outline=INK); d.line(pts + [pts[0]], fill=INK, width=int(10 * s), joint='curve')
    if crack > 0: d.line([(cx - 20 * s, cy - 140 * s), (cx + 10 * s, cy - 60 * s), (cx - 30 * s, cy), (cx + 20 * s, cy + 80 * s)][:max(2, int(4 * clamp(crack)))], fill=CARD, width=int(12 * s))
def listcard(C, cx, cy, w, items, hl=None, st=(), stw=1.0, stamp_=(), k=1.0):
    """список пунктов: hl — индекс подсветки, st — зачёркнутые, stamp_ — помеченные «СТАТЬЯ»"""
    if k <= 0: return
    lh = 74; h = lh * len(items) + 60; im = Image.new('RGBA', (int(w) + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([5, 5, w + 5, h + 5], radius=26, fill=WHITE, outline=INK, width=8)
    for j, it in enumerate(items):
        y = 35 + j * lh
        if hl == j: d.rounded_rectangle([20, y - 4, w - 10, y + lh - 10], radius=12, fill=YEL)
        t = text_img(f'{j + 1}. {it}', 48, INK if hl in (None, j) else GREY); im.alpha_composite(t, (34, y + (lh - 10 - t.height) // 2))
        if j in st: d.line([28, y + lh / 2 - 4, 28 + (t.width + 14) * clamp(stw), y + lh / 2 - 4], fill=RED, width=8)
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1)
    for j in stamp_: pass
def pie10(C, cx, cy, r, k=1.0, u=0):
    d = D(C); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LG, outline=INK, width=10)
    a = 36 * clamp(k); off = 30 * eo(clamp(k)); ax = math.radians(-90 + a / 2)
    if a > 1: d.pieslice([cx - r + off * math.cos(ax), cy - r + off * math.sin(ax), cx + r + off * math.cos(ax), cy + r + off * math.sin(ax)], -90, -90 + a, fill=YEL, outline=INK, width=10)
    put(C, text_img('90%', int(r * 0.42), GREY), cx - r * 0.1, cy + r * 0.25)
def piggy(C, cx, by, s=1.0, u=0, coins=0):
    d = D(C); w, h = 380 * s, 270 * s; cy = by - 60 * s - h / 2
    for sd in (-1, 1): d.rounded_rectangle([cx + sd * 100 * s - 26 * s, cy + h * 0.3, cx + sd * 100 * s + 26 * s, by], radius=10, fill=PINK, outline=INK, width=6)
    d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=PINK, outline=INK, width=9)
    d.ellipse([cx + w / 2 - 50 * s, cy - 40 * s, cx + w / 2 + 40 * s, cy + 40 * s], fill=(255, 140, 180), outline=INK, width=7)
    for q in (-14, 14): d.ellipse([cx + w / 2 - 5 * s + q * s - 7 * s, cy - 7 * s, cx + w / 2 - 5 * s + q * s + 7 * s, cy + 7 * s], fill=INK)
    d.polygon([(cx + 60 * s, cy - h / 2 + 10 * s), (cx + 110 * s, cy - h / 2 - 60 * s), (cx + 130 * s, cy - h / 2 + 30 * s)], fill=PINK, outline=INK)
    d.rounded_rectangle([cx - 50 * s, cy - h / 2 + 4 * s, cx + 50 * s, cy - h / 2 + 22 * s], radius=6, fill=INK)
    d.ellipse([cx + 60 * s, cy - 50 * s, cx + 80 * s, cy - 30 * s], fill=INK)
def child(C, clip, u, cx, s=0.2, feet=None, flip=False): man(C, clip, u, cx, feet or G, s, flip=flip)
