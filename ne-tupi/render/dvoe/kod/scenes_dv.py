"""СДВГ-монтаж «Одна зарплата — две судьбы» (Лёха и Миша). Движок «Кредита» (compose_kr.py), кадр на весь экран, белый фон.
python3 compose_dv.py 1.5 12.3 -> prev_*.png;  python3 compose_dv.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from props_dv import *
GOLD = (244, 190, 30); GOLDD = (186, 132, 10); GOLDL = (255, 230, 120); TAXI = (255, 200, 0); PIG = (255, 150, 170); PIGD = (220, 100, 130); SCREEN = (40, 46, 60)
CHAIN_FROM = None   # время, с которого Лёха в цепи (ставится ниже)

# ---------- персонажи ----------
def chain_on(C, cx, feet, s, u=0):
    """золотая цепь с медальоном ₽ на шее Лёхи"""
    d = D(C); y0 = feet - 945 * s; w = 92 * s; sag = 120 * s; r = max(3, 13 * s)
    for j in range(15):
        q = j / 14; x = cx - w + 2 * w * q; y = y0 + sag * (1 - (2 * q - 1) ** 2)
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=GOLD, outline=GOLDD, width=max(1, int(3 * s)))
    my = y0 + sag + 34 * s; mr = 34 * s; sw = 4 * s_(u * 5)
    d.ellipse([cx + sw - mr, my - mr, cx + sw + mr, my + mr], fill=GOLD, outline=GOLDD, width=max(2, int(5 * s)))
    d.text((cx + sw, my), '₽', font=font2(max(8, mr * 1.1)), fill=GOLDD, anchor='mm')
def leha(C, clip, u, cx, s=0.4, feet=None, flip=False, chain=True, rot=0):
    feet = feet or G; man(C, clip, u, cx, feet, s, flip=flip, rot=rot)
    if chain and not rot: chain_on(C, cx, feet, s, u)
def misha(C, clip, u, cx, s=0.4, feet=None, flip=False, rot=0):
    man(C, 'v_' + clip, u, cx, feet or G, s, flip=flip, rot=rot)
def name(C, u, text, cx, cy, bg=YEL, fg=INK, rot=-3, sz=70):
    if u < 0: return
    put(C, plate_img(text, sz, bg, fg, pad=16, r=12, border=INK, bw=6), cx, cy, back(u / 0.2), rot)

# ---------- предметы ----------
def watch(C, cx, cy, s=1.0, u=0, rot=0):
    im = Image.new('RGBA', (int(420 * s), int(620 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 210 * s; m = 310 * s
    d.rounded_rectangle([c - 80 * s, 10 * s, c + 80 * s, 610 * s], radius=int(30 * s), fill=GOLD, outline=INK, width=max(4, int(8 * s)))
    for j in range(9): y = 30 * s + j * 64 * s; d.line([c - 80 * s, y, c + 80 * s, y], fill=GOLDD, width=max(2, int(4 * s)))
    d.ellipse([c - 170 * s, m - 170 * s, c + 170 * s, m + 170 * s], fill=GOLD, outline=INK, width=max(5, int(10 * s)))
    d.ellipse([c - 136 * s, m - 136 * s, c + 136 * s, m + 136 * s], fill=WHITE, outline=GOLDD, width=max(3, int(8 * s)))
    for j in range(12):
        a = j / 12 * 2 * math.pi; d.line([c + math.cos(a) * 110 * s, m + math.sin(a) * 110 * s, c + math.cos(a) * 128 * s, m + math.sin(a) * 128 * s], fill=INK, width=max(2, int(7 * s)))
    a1 = u * 6 - math.pi / 2; a2 = u * 0.6 - 1
    d.line([c, m, c + math.cos(a2) * 70 * s, m + math.sin(a2) * 70 * s], fill=INK, width=max(3, int(12 * s))); d.line([c, m, c + math.cos(a1) * 105 * s, m + math.sin(a1) * 105 * s], fill=RED, width=max(2, int(6 * s)))
    d.ellipse([c - 14 * s, m - 14 * s, c + 14 * s, m + 14 * s], fill=INK)
    put(C, im, cx, cy, 1, rot)
def bigchain(C, cx, cy, s=1.0, u=0):
    d = D(C); w = 330 * s; sag = 380 * s; r = 30 * s
    for j in range(23):
        q = j / 22; x = cx - w + 2 * w * q; y = cy - sag / 2 + sag * (1 - (2 * q - 1) ** 2) + 8 * s_(u * 6 + q * 6)
        if j % 2: d.ellipse([x - r * 0.55, y - r, x + r * 0.55, y + r], outline=GOLDD, width=int(12 * s), fill=None); d.ellipse([x - r * 0.55, y - r, x + r * 0.55, y + r], outline=GOLD, width=int(7 * s))
        else: d.ellipse([x - r, y - r * 0.55, x + r, y + r * 0.55], outline=GOLDD, width=int(12 * s)); d.ellipse([x - r, y - r * 0.55, x + r, y + r * 0.55], outline=GOLD, width=int(7 * s))
    my = cy + sag / 2 + 110 * s; mr = 100 * s
    d.ellipse([cx - mr, my - mr, cx + mr, my + mr], fill=GOLD, outline=INK, width=int(10 * s)); d.text((cx, my), '₽', font=font2(mr * 1.2), fill=GOLDD, anchor='mm')
def sparkle(C, u, pts, col=WHITE):
    for j, (x, y) in enumerate(pts):
        k = abs(s_(u * 7 + j * 1.9)); r = 20 + 34 * k; d = D(C)
        d.polygon([(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r), (x - r * 0.22, y + r * 0.22), (x - r, y), (x - r * 0.22, y - r * 0.22)], fill=col, outline=INK)
def taxi(C, cx, by, s=1.0, u=0):
    d = D(C); w = 640 * s; x0 = cx - w / 2; b = by - 60 * s; bob = 4 * s_(u * 30)
    d.polygon([(x0 + w * 0.22, b - 250 * s + bob), (x0 + w * 0.72, b - 250 * s + bob), (x0 + w * 0.86, b - 140 * s + bob), (x0 + w * 0.12, b - 140 * s + bob)], fill=TAXI, outline=INK, width=8)
    d.polygon([(x0 + w * 0.27, b - 230 * s + bob), (x0 + w * 0.46, b - 230 * s + bob), (x0 + w * 0.46, b - 150 * s + bob), (x0 + w * 0.19, b - 150 * s + bob)], fill=WIN, outline=INK, width=6)
    d.polygon([(x0 + w * 0.5, b - 230 * s + bob), (x0 + w * 0.69, b - 230 * s + bob), (x0 + w * 0.8, b - 150 * s + bob), (x0 + w * 0.5, b - 150 * s + bob)], fill=WIN, outline=INK, width=6)
    d.rounded_rectangle([x0, b - 150 * s + bob, x0 + w, b + bob], radius=int(40 * s), fill=TAXI, outline=INK, width=8)
    for j in range(8): d.rectangle([x0 + w * (0.2 + j * 0.075), b - 100 * s + bob, x0 + w * (0.2 + j * 0.075) + w * 0.0375, b - 70 * s + bob], fill=INK if j % 2 else WHITE)
    d.rounded_rectangle([cx - 60 * s, b - 300 * s + bob, cx + 60 * s, b - 252 * s + bob], radius=8, fill=WHITE, outline=INK, width=5); put(C, text_img('ТАКСИ', int(30 * s), INK), cx, b - 276 * s + bob)
    for wx in (0.22, 0.78):
        x = x0 + w * wx; r = 62 * s; d.ellipse([x - r, b - r + 10 * s, x + r, b + r + 10 * s], fill=INK); d.ellipse([x - r * 0.45, b - r * 0.45 + 10 * s, x + r * 0.45, b + r * 0.45 + 10 * s], fill=GREY)
def bag(C, cx, by, s=1.0, rot=0):
    im = Image.new('RGBA', (int(380 * s), int(420 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10 * s, 60 * s, 370 * s, 410 * s], radius=int(24 * s), fill=(250, 120, 40), outline=INK, width=max(4, int(9 * s)))
    d.arc([110 * s, 0, 270 * s, 130 * s], 180, 360, fill=INK, width=max(4, int(16 * s)))
    t = text_img('ДОСТАВКА', int(46 * s), WHITE); im.alpha_composite(t, (int(190 * s - t.width / 2), int(150 * s)))
    d.ellipse([140 * s, 230 * s, 240 * s, 330 * s], fill=WHITE, outline=INK, width=max(3, int(6 * s))); d.line([170 * s, 280 * s, 190 * s, 300 * s, 215 * s, 255 * s], fill=INK, width=max(3, int(8 * s)))
    put(C, im, cx, by - 210 * s, 1, rot)
def wallet(C, cx, cy, s=1.0, open_=1.0, empty=True):
    d = D(C); w, h = 520 * s, 340 * s; x0 = cx - w / 2; y0 = cy - h / 2; LEA = (120, 74, 44); LEA2 = (90, 54, 32)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(30 * s), fill=LEA, outline=INK, width=9)
    d.rounded_rectangle([x0 + 24 * s, y0 - 70 * s * open_, x0 + w - 24 * s, y0 + 40 * s], radius=int(16 * s), fill=LEA2, outline=INK, width=7)
    d.line([x0 + 30 * s, y0 + h * 0.62, x0 + w - 30 * s, y0 + h * 0.62], fill=LEA2, width=5)
    d.rounded_rectangle([x0 + w * 0.72, y0 + h * 0.4, x0 + w + 16 * s, y0 + h * 0.66], radius=12, fill=LEA2, outline=INK, width=6)
def piggy(C, cx, by, s=1.0, u=0, fill=0.0, label=None):
    d = D(C); w, h = 460 * s, 330 * s; cy = by - 60 * s - h / 2; x0 = cx - w / 2
    for lx in (0.22, 0.38, 0.62, 0.78): d.rounded_rectangle([x0 + w * lx - 26 * s, cy + h * 0.3, x0 + w * lx + 26 * s, by], radius=int(14 * s), fill=PIGD, outline=INK, width=6)
    d.ellipse([x0, cy - h / 2, x0 + w, cy + h / 2], fill=PIG, outline=INK, width=9)
    d.polygon([(x0 + w * 0.3, cy - h * 0.38), (x0 + w * 0.36, cy - h * 0.72), (x0 + w * 0.46, cy - h * 0.46)], fill=PIGD, outline=INK, width=6)
    d.ellipse([x0 + w - 70 * s, cy - 50 * s, x0 + w + 40 * s, cy + 60 * s], fill=PIGD, outline=INK, width=7)
    for nx in (-18, 18): d.ellipse([x0 + w - 15 * s + nx * s - 9 * s, cy - 2 * s, x0 + w - 15 * s + nx * s + 9 * s, cy + 22 * s], fill=INK)
    d.ellipse([x0 + w * 0.7 - 14 * s, cy - h * 0.2, x0 + w * 0.7 + 14 * s, cy - h * 0.2 + 28 * s], fill=INK)
    d.rounded_rectangle([cx - 70 * s, cy - h / 2 + 18 * s, cx + 70 * s, cy - h / 2 + 38 * s], radius=8, fill=INK)
    d.arc([x0 - 70 * s, cy - 40 * s, x0 + 10 * s, cy + 40 * s], 90, 300, fill=INK, width=8)
    if fill > 0:
        k = clamp(fill); d.rectangle([cx - w * 0.3, cy + h * 0.38 - h * 0.6 * k, cx + w * 0.3, cy + h * 0.38], fill=GOLD)
        d.ellipse([x0, cy - h / 2, x0 + w, cy + h / 2], outline=INK, width=9)
    if label: put(C, plate_img(label, int(46 * s), YEL, INK, pad=12, r=8, border=INK, bw=5), cx, cy + h * 0.05)
def books(C, cx, by, s=1.0, n=4):
    d = D(C); cols = [(200, 60, 60), (60, 110, 190), (60, 160, 100), (230, 170, 30), (130, 80, 170)]
    y = by
    for j in range(n):
        w = (300 - (j % 3) * 30) * s; h = 62 * s; x = cx + (12 * s if j % 2 else -10 * s)
        d.rounded_rectangle([x - w / 2, y - h, x + w / 2, y], radius=8, fill=cols[j % 5], outline=INK, width=6); d.rectangle([x + w / 2 - 40 * s, y - h + 8, x + w / 2 - 12 * s, y - 8], fill=PAPER, outline=INK, width=3); y -= h
def laptop(C, cx, by, s=1.0, u=0, text=None):
    d = D(C); w, h = 560 * s, 340 * s; x0 = cx - w / 2
    d.rounded_rectangle([x0, by - h - 30 * s, x0 + w, by - 30 * s], radius=int(20 * s), fill=INK)
    d.rounded_rectangle([x0 + 22 * s, by - h - 8 * s, x0 + w - 22 * s, by - 52 * s], radius=int(8 * s), fill=SCREEN)
    d.polygon([(x0 - 60 * s, by), (x0 + w + 60 * s, by), (x0 + w, by - 34 * s), (x0, by - 34 * s)], fill=MID, outline=INK)
    d.line([(x0 - 60 * s, by), (x0 + w + 60 * s, by), (x0 + w, by - 34 * s), (x0, by - 34 * s), (x0 - 60 * s, by)], fill=INK, width=7)
    cy = by - h / 2 - 30 * s; r = 60 * s; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED); d.polygon([(cx - 20 * s, cy - 30 * s), (cx - 20 * s, cy + 30 * s), (cx + 32 * s, cy)], fill=WHITE)
    k = (u * 0.5) % 1; d.rectangle([x0 + 50 * s, by - 80 * s, x0 + w - 50 * s, by - 70 * s], fill=GREY); d.rectangle([x0 + 50 * s, by - 80 * s, x0 + 50 * s + (w - 100 * s) * k, by - 70 * s], fill=YEL)
    if text: put(C, plate_img(text, int(40 * s), YEL, INK, pad=10, r=6, border=INK, bw=4), cx, by - h - 70 * s)
def bulb(C, cx, cy, s=1.0, u=0):
    d = D(C); r = 120 * s; on = 0.6 + 0.4 * abs(s_(u * 8))
    for j in range(10):
        a = j / 10 * 2 * math.pi; d.line([cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3, cx + math.cos(a) * r * (1.5 + 0.3 * on), cy + math.sin(a) * r * (1.5 + 0.3 * on)], fill=YEL, width=int(14 * s))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 120), outline=INK, width=int(9 * s))
    d.rectangle([cx - r * 0.45, cy + r * 0.85, cx + r * 0.45, cy + r * 1.35], fill=GREY, outline=INK, width=int(7 * s))
    d.line([cx - r * 0.3, cy + r * 0.2, cx, cy - r * 0.2, cx + r * 0.3, cy + r * 0.2], fill=GOLDD, width=int(8 * s))
def pillow(C, cx, by, s=1.0, label='ПОДУШКА'):
    d = D(C); w, h = 620 * s, 200 * s; y0 = by - h
    d.rounded_rectangle([cx - w / 2, y0, cx + w / 2, by], radius=int(90 * s), fill=(220, 230, 250), outline=INK, width=9)
    for x in (-1, 1): d.ellipse([cx + x * w / 2 - 30 * s, y0 - 10 * s, cx + x * w / 2 + 30 * s, y0 + 50 * s], fill=(220, 230, 250), outline=INK, width=7); d.ellipse([cx + x * w / 2 - 30 * s, by - 50 * s, cx + x * w / 2 + 30 * s, by + 10 * s], fill=(220, 230, 250), outline=INK, width=7)
    put(C, text_img(label, int(64 * s), INK), cx, y0 + h / 2)
def clover(C, cx, cy, s=1.0, rot=0):
    im = Image.new('RGBA', (int(400 * s), int(460 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 200 * s
    d.line([c, c, c + 30 * s, 440 * s], fill=GREEN, width=int(22 * s))
    for a in (0, 90, 180, 270):
        x = c + math.cos(math.radians(a)) * 80 * s; y = c + math.sin(math.radians(a)) * 80 * s; r = 82 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=GREEN, outline=INK, width=int(8 * s))
    d.ellipse([c - 30 * s, c - 30 * s, c + 30 * s, c + 30 * s], fill=(30, 140, 70))
    put(C, im, cx, cy, 1, rot)
def hands(C, cx, cy, s=1.0, u=0):
    d = D(C); sh = 10 * s_(u * 20) * s
    d.rounded_rectangle([cx - 420 * s, cy - 50 * s + sh, cx - 60 * s, cy + 50 * s + sh], radius=int(30 * s), fill=INK); d.rounded_rectangle([cx + 60 * s, cy - 50 * s + sh, cx + 420 * s, cy + 50 * s + sh], radius=int(30 * s), fill=(60, 60, 64))
    d.ellipse([cx - 110 * s, cy - 80 * s + sh, cx + 30 * s, cy + 80 * s + sh], fill=INK); d.ellipse([cx - 30 * s, cy - 80 * s + sh, cx + 110 * s, cy + 80 * s + sh], fill=(60, 60, 64))
    for x in (-420, 360): d.rectangle([cx + x * s, cy - 60 * s + sh, cx + (x + 60) * s, cy + 60 * s + sh], fill=WHITE, outline=INK, width=6)
def coinman(C, cx, by, s, u, k=0):
    """монетка с ручками и ножками несёт коробку — «деньги работают»"""
    d = D(C); r = 70 * s; cy = by - 70 * s - r; ph = u * 12 + k
    for sd in (-1, 1): d.line([cx + sd * 20 * s, cy + r * 0.8, cx + sd * 20 * s + 26 * s * s_(ph + (sd > 0) * math.pi), by], fill=INK, width=int(12 * s))
    box(C, cx, cy - r * 0.9, 120 * s, 80 * s, None, 4 * s_(ph), False)
    coin(C, cx, cy + 4 * abs(s_(ph)) * s, r)
    for sd in (-1, 1): d.line([cx + sd * r * 0.8, cy - r * 0.2, cx + sd * 64 * s, cy - r * 1.1], fill=INK, width=int(11 * s))
def vs(C, u, cx, cy):
    burst(C, cx, cy, 120, u, 12, RED); put(C, text_img('VS', 100, WHITE, INK, 6), cx, cy, back(u / 0.2))
def stack_col(C, cx, by, h, r=58):
    n = max(1, int(h / (r * 0.34))); coinstack(C, cx, by, n, r)

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_h1(C, u, t):   # Одна зарплата
    ground(C); leha(C, 'idle', u, 300, 0.36, chain=False); misha(C, 'idle', u, 780, 0.36)
    k = back(u / 0.25); L = layer(); wad(L, 540, 860, 300, 3); put(C, L.crop((300, 700, 780, 1020)), 540, 860, k)
    put(C, plate_img('80 000 ₽', 110, YEL, INK, pad=22, r=16, border=INK, bw=7), 540, 1060, back((u - 0.15) / 0.2), -3)
    slam(C, u, 'ОДНА ЗАРПЛАТА', 540, 400, 130)
def s_h2(C, u, t):   # один завод
    sky(C); factory(C, 540, G + 6, 1.05, u); leha(C, 'v_idle' if False else 'idle', u, 250, 0.28, G + 6, chain=False); misha(C, 'idle', u, 830, 0.28, G + 6)
    slam(C, u, 'ОДИН ЗАВОД', 540, 400, 150)
def s_h3(C, u, t):   # Через десять лет
    k = clamp(u / 0.6); n = min(10, 1 + int(k * 10))
    calendar(C, 540, 880, 1.15, str(n), 'ЛЕТ' if n > 4 else 'ГОД', 1 + 0.08 * s_(u * 30) * (1 - k), 4 * s_(u * 40) * (1 - k))
    slam(C, u, 'ЧЕРЕЗ', 540, 380, 150)
def s_h4(C, u, t):   # один по уши в долгах
    ground(C); k = eo(clamp(u / 0.9))
    leha(C, 'idle_sad', u, 540, 0.42, chain=False)
    for j in range(14):
        rnd = random.Random(j); x = 540 + rnd.uniform(-330, 330); hh = 140 + 480 * k * rnd.uniform(0.7, 1.0); y = G - hh * (j % 4) / 4 - 60
        if y > G - 40 - 560 * k: doc(C, x, y, 170, 210, 'КРЕДИТ', rnd.uniform(-25, 25), 1, None, False, 32)
    slam(C, u, 'ОДИН', 540, 380, 150); plate(C, t - T('уши'), 'ПО УШИ В ДОЛГАХ', 540, 540, 96, RED, WHITE, -3)
def s_h5(C, u, t):   # а у второго, сука, почти два ляма
    ground(C); k = eo(clamp(u / 0.7))
    for j, x in enumerate((240, 360, 720, 840)): stack_col(C, x, G, 380 * k * (0.7 + 0.3 * (j % 2)), 56)
    for j in range(3): wad(C, 540 + (j - 1) * 200, 760 - 30 * (j % 2), 160, 2, back((u - 0.25 - j * 0.07) / 0.2))
    misha(C, 'cheer', u, 540, 0.4)
    slam(C, u, 'А У ВТОРОГО', 540, 380, 120)
    v = t - T('почти')
    if v > -0.05: put(C, plate_img('ПОЧТИ 2 ЛЯМА', 110, YEL, INK, pad=24, r=18, border=INK, bw=8), 540 + (5 * s_(v * 60) if v < 0.3 else 0), 540, 1 + 0.5 * (1 - eo((v + 0.05) / 0.18)), -3)
    elif t > T('сука') - 0.05: plate(C, t - T('сука'), 'С*КА', 540, 540, 120, RED, WHITE, 4)
    sparkle(C, u, [(140, 760), (950, 700), (180, 1100), (930, 1060)], YEL)
def s_pochemu(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); man(C, 'scratch', u, 540, G + 40, 0.5)
    slam(C, u, 'ПОЧЕМУ?', 540, 430, 230)
def s_smotri(C, u, t):
    ground(C); man(C, 'pointcam', u, 540, G, 0.5); slam(C, u, 'СМОТРИ', 540, 420, 190)
def s_leha(C, u, t):
    ground(C); leha(C, 'wave', u, 540, 0.5, chain=False); slam(C, u, 'ЭТО', 540, 380, 120); name(C, u - 0.15, 'ЛЁХА', 540, 540, YEL, INK, -4, 120)
def s_misha(C, u, t):
    ground(C); misha(C, 'nod', u, 540, 0.5); slam(C, u, 'А ЭТО', 540, 380, 120); name(C, u - 0.15, 'МИША', 540, 540, INK, YEL, 4, 120)
def s_oba(C, u, t):
    ground(C); leha(C, 'idle_smile', u, 290, 0.38, chain=False); misha(C, 'smile', u, 790, 0.38)
    for j, x in enumerate((290, 790)):
        q = clamp((u - 0.2 - j * 0.15) / 0.4); y = lerp(500, 860, eo(q)); wad(C, x, y, 170, 2) if q > 0 else None
        put(C, plate_img('80 000 ₽', 64, YEL, INK, pad=14, r=10, border=INK, bw=5), x, 1150, back((u - 0.5 - j * 0.15) / 0.2), (-4, 4)[j])
    slam(C, u, 'ОБА ПОЛУЧАЮТ', 540, 400, 120)
    if u > 0.6: put(C, text_img('=', 160, INK), 540, 900, back((u - 0.6) / 0.2))
def s_pashut(C, u, t):
    room(C, 600, (232, 226, 214), (190, 186, 178)); d = D(C)
    for j, x in enumerate((290, 790)):
        man(C, 'box' if j == 0 else 'v_box', u + j * 0.2, x, G, 0.38); box(C, x, G - 560 + 6 * s_(u * 6 + j), 230, 170, None)
        for q in range(3):   # капли пота
            p = (u * 1.4 + q / 3 + j * 0.2) % 1; sx = x + (q - 1) * 70; sy = G - 640 + p * 120
            d.ellipse([sx - 10, sy - 14, sx + 10, sy + 14], fill=(110, 170, 230), outline=INK, width=3)
    slam(C, u, 'ПАШУТ', 540, 380, 150); plate(C, t - T('одинаково'), 'ОДИНАКОВО', 540, 530, 100)
def s_yolo(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); leha(C, 'armsup', u, 540, 0.5, G + 40, chain=False)
    slam(C, u, 'ЖИВЁМ', 540, 360, 160); plate(C, t - T('один', 2), 'ОДИН РАЗ,', 540, 520, 110, INK, YEL, -3)
    v = t - T('бля')
    if v > 0: stamp(C, v, 'БЛ*!', 820, 760, 120, RED, 12)
def s_chasy(C, u, t):
    k = back(u / 0.25); L = layer(); watch(L, 540, 880, 1.25, u * 3); put(C, L.crop((270, 480, 810, 1280)), 540, 880, k, -6 + 6 * s_(u * 4))
    sparkle(C, u, [(250, 650), (850, 760), (280, 1150)])
    slam(C, u, 'ЧАСЫ', 540, 380, 170); pricetag(C, 800, 1180, 0.8, 'ЧАСЫ', '−40 000', -8, YEL, back((u - 0.3) / 0.2))
def s_cep(C, u, t):
    ground(C); leha(C, 'hips', u, 540, 0.48); bigchain(C, 540, 760, 0.7 * back(u / 0.25) if u < 0.25 else 0.7, u) if u < 0.35 else None
    sparkle(C, u, [(260, 700), (820, 640), (300, 1050), (800, 1000)], YEL)
    slam(C, u, 'ЦЕПЬ', 540, 400, 170)
def s_iphone(C, u, t):
    phone(C, 540, 880, 2.6 * back(u / 0.22) if u < 0.22 else 2.6, 6 * s_(u * 3), screen=(70, 70, 90))
    put(C, text_img('', 10), 540, 880); slam(C, u, 'АЙФОН', 540, 380, 160)
    stamp(C, t - T('кредит'), 'В КРЕДИТ', 540, 1150, 100, RED, -10)
def s_taxi(C, u, t):
    sky(C); x = lerp(1300, 540, eo(u / 0.35)); taxi(C, x, G + 6, 1.0, u)
    slam(C, u, 'ТАКСИ', 540, 400, 170); put(C, plate_img('−1 200 ₽', 70, RED, WHITE, pad=14, r=10), 820, 620, back((u - 0.25) / 0.2), 6)
def s_dostavka(C, u, t):
    ground(C); leha(C, 'phone', u, 300, 0.4)
    for j in range(3): bag(C, 680 + j * 120, G - j * 10, 0.55 + 0.05 * j * back((u - 0.15 * j) / 0.2), (j - 1) * 5) if u > 0.15 * j else None
    for j in range(6):
        q = (u * 1.3 + j / 6) % 1; coin(C, 300 + 80 * s_(j * 2), 700 - 400 * q, 30, q * 400) if u > 0.1 else None
    slam(C, u, 'ДОСТАВКА', 540, 400, 150)
def s_nol(C, u, t):
    wallet(C, 540, 900, 1.3, clamp(u / 0.3))
    v = t - T('ноль'); put(C, text_img('0 ₽', 200, RED, WHITE, 10), 540, 640, back(v / 0.2)) if v > 0 else None
    pocket_moth = (540 + 160 * s_(u * 3), 700 - 200 * ((u * 0.8) % 1)); d = D(C); mx, my = pocket_moth; f = abs(s_(u * 30))
    d.ellipse([mx - 10, my - 22, mx + 10, my + 22], fill=GREY); d.ellipse([mx - 50, my - 30 * f - 8, mx - 6, my + 10], fill=MID, outline=INK, width=3); d.ellipse([mx + 6, my - 30 * f - 8, mx + 50, my + 10], fill=MID, outline=INK, width=3)
    slam(C, u, 'К ЗАРПЛАТЕ', 540, 380, 140)
def s_nihrena(C, u, t):
    ground(C); leha(C, 'shrug', u, 540, 0.5)
    slam(C, u, 'НИ ХРЕНА', 540, 380, 170); plate(C, t - T('осталось'), 'НЕ ОСТАЛОСЬ', 540, 540, 100, RED, WHITE, -3)
def s_inache(C, u, t):
    ground(C); misha(C, 'hips', u, 540, 0.5); slam(C, u, 'А МИША', 540, 380, 150); plate(C, t - T('иначе'), 'ИНАЧЕ', 540, 540, 110, INK, YEL, 3)
def s_8k(C, u, t):
    ground(C); misha(C, 'point', u, 250, 0.38); piggy(C, 680, G, 1.1, u, clamp(u / 2.2) * 0.5)
    for j in range(4):
        q = clamp((u - 0.15 - j * 0.35) / 0.4)
        if 0 < q < 1: coin(C, lerp(360, 680, q), lerp(860, 720, q) - 160 * s_(math.pi * q), 34, q * 300)
    slam(C, u, 'КАЖДЫЙ МЕСЯЦ', 540, 380, 120)
    v = t - T('восемь')
    if v > -0.05: put(C, plate_img('8 000 ₽', 120, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 540, 1 + 0.4 * (1 - eo((v + 0.05) / 0.18)), -3)
    tag(C, v - 0.3, '10% ЗАРПЛАТЫ', 680, 1180, 48, INK, YEL, -2)
def s_golova(C, u, t):
    ground(C); misha(C, 'think', u, 540, 0.48); bulb(C, 540, 560 + 10 * s_(u * 4), 0.75 * back((u - 0.2) / 0.25) if u < 0.45 else 0.75, u)
    slam(C, u, 'В ГОЛОВУ', 540, 340, 140)
def s_knigi(C, u, t):
    ground(C); books(C, 250, G, 0.9, 1 + int(clamp(u / 0.5) * 5)); books(C, 830, G, 0.8, 1 + int(clamp((u - 0.1) / 0.5) * 4))
    misha(C, 'read', u, 540, 0.44); d = D(C)
    d.polygon([(470, 820), (540, 840), (540, 920), (470, 900)], fill=WHITE, outline=INK); d.polygon([(540, 840), (610, 820), (610, 900), (540, 920)], fill=WHITE, outline=INK)
    slam(C, u, 'КНИГИ', 540, 400, 170)
def s_kursy(C, u, t):
    ground(C); laptop(C, 540, G - 120, 1.25, u, 'КУРС'); table(C, 540, G - 110, 900, 116)
    slam(C, u, 'КУРСЫ', 540, 400, 170)
def s_navyk(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); misha(C, 'armsup', u, 540, 0.48, G + 40)
    slam(C, u, 'НОВЫЙ НАВЫК', 540, 380, 130); plate(C, u - 0.25, 'LEVEL UP +1', 540, 540, 100, INK, YEL, -3)
def s_rzhal(C, u, t):
    ground(C); leha(C, 'laugh', u, 300, 0.42); misha(C, 'read', u, 830, 0.34, flip=True)
    v = t - T('Ты', 0)
    slam(C, u, 'ЛЁХА РЖАЛ', 540, 380, 130)
    if v > -0.05:
        speech(C, 520, 600, 800, 260, back((v + 0.05) / 0.2))
        if v > 0.05: txt(C, 'ТЫ ЧЁ, БЛ*ТЬ,', 520, 560, 70); put(C, plate_img('ПЕНСИОНЕР?', 80, YEL, INK, pad=12, r=10), 520, 660, back((t - T('пенсионер')) / 0.2)) if t > T('пенсионер') else None
    for j in range(3): pop(C, u - 0.2 - j * 0.15, 'ХА', [150, 430, 200][j], [860, 820, 1000][j], 60, INK, (-14, 10, -6)[j])
def s_god1(C, u, t):
    ground(C); calendar(C, 300, 900, 0.75, '1', 'ГОД', back(u / 0.2), -5); piggy(C, 770, G, 0.75, u, 0.08)
    slam(C, u, 'ПЕРВЫЙ ГОД', 540, 380, 140); plate(C, t - T('копейки'), 'КОПЕЙКИ', 540, 530, 100, INK, YEL, 3)
def s_96(C, u, t):
    ground(C); v = t - T('Девяносто'); put(C, plate_img(num(roll(max(0, v), 0, 96000, 0.7)) + ' ₽', 130, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 470, 1, -2)
    tag(C, v - 0.2, '8 000 × 12', 540, 610, 50, INK, YEL, 2); piggy(C, 760, G, 0.7, u, 0.12); leha(C, 'laugh', u, 300, 0.36)
    w = t - T('Смешно')
    if w > 0: stamp(C, w, 'СМЕШНО', 540, 960, 100, RED, -8)
def s_god5(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); calendar(C, 540, 880, 1.05, '5', 'ЛЕТ', back(u / 0.2), 4); slam(C, u, 'ПЯТЫЙ ГОД', 540, 380, 150, YEL)
def s_podushka(C, u, t):
    ground(C); pillow(C, 400, G, 1.0); misha(C, 'boss', u, 400, 0.36, G - 150)
    k = eo(clamp((t - T('зарплата', 1)) / 0.5)) if t > T('зарплата', 1) else 0
    if k > 0:
        arrow(C, 850, 1180, 850, 1180 - 520 * k, GREEN, 30, 1); tag(C, t - T('зарплата', 1), 'ЗАРПЛАТА', 850, 1230, 46, GREEN, WHITE, 0)
    slam(C, u, 'У МИШИ', 540, 380, 150); plate(C, t - T('подушка'), 'ПОДУШКА', 540, 530, 100)
def s_kredit3(C, u, t):
    ground(C); leha(C, 'idle_sad', u, 300, 0.4)
    for j in range(3): doc(C, 720 + j * 70, 820 + j * 60, 260, 330, 'КРЕДИТ', -8 + j * 8, back((u - j * 0.15) / 0.2), f'№{j + 1}', False, 52)
    slam(C, u, 'У ЛЁХИ', 540, 380, 150); plate(C, t - T('третий'), 'ТРЕТИЙ КРЕДИТ', 540, 530, 100, RED, WHITE, -3)
def s_god10(C, u, t):
    C.paste(INK, [0, 0, CW, CH]); speedlines(C, 540, 880, u, r0=520, col=(34, 34, 34), seed=8)
    calendar(C, 540, 880, 1.15, '10', 'ЛЕТ', 0.7 + 0.45 * eo(clamp(u / 0.9)), 0)
    slam(C, u, 'А ДЕСЯТЫЙ…', 540, 380, 150, YEL)
def s_svoih(C, u, t):
    ground(C); k = eo(clamp(u / 0.8))
    for j in range(6): stack_col(C, 200 + j * 136, G, (200 + 60 * (j % 3)) * k, 52)
    misha(C, 'smile', u, 540, 0.3, G - 0)
    slam(C, u, 'СВОИХ', 540, 380, 150); v = t - T('девятьсот')
    if v > -0.05: put(C, plate_img('960 000 ₽', 120, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 540, 1 + 0.4 * (1 - eo((v + 0.05) / 0.18)), -2)
    tag(C, v - 0.3, '8 000 × 120 МЕС', 540, 680, 46, INK, YEL, 2)
def s_1840(C, u, t):
    ground(C); v = max(0, t - T('миллион')); k = eo(clamp(v / 0.9))
    for j in range(6): stack_col(C, 200 + j * 136, G, (240 + 60 * (j % 3)) * (1 + 1.1 * k), 52)
    put(C, plate_img(num(roll(v, 960000, 1840000, 0.9)) + ' ₽', 120, YEL, INK, pad=24, r=16, border=INK, bw=8), 540, 520, 1 + 0.06 * s_(v * 20) * (1 - k), -2)
    slam(C, u, 'ПОД 12%', 540, 370, 130)
    src(C, 'УСЛОВНО: 8 000 ₽ В МЕС, 12% ГОДОВЫХ, 10 ЛЕТ', 1318)
    if v > 0.9: sparkle(C, u, [(150, 700), (930, 660), (120, 1000), (960, 980)], YEL)
def s_rabotayut(C, u, t):
    ground(C); misha(C, 'boss', u, 860, 0.34, flip=True)
    for j in range(4): coinman(C, ((u * 260 + j * 230) % 920) - 60, G, 0.9, u, j)
    slam(C, u, 'ДЕНЬГИ РАБОТАЮТ', 540, 380, 110); plate(C, t - T('сами'), 'САМИ', 540, 530, 110, INK, YEL, -3)
def s_udacha(C, u, t):
    clover(C, 540, 880, 1.3, -8 + 4 * s_(u * 5)); xcross(C, u - 0.25, 540, 880, 300, RED, 30)
    slam(C, u, 'НЕ В УДАЧЕ', 540, 400, 140)
def s_svyazi(C, u, t):
    hands(C, 540, 880, 1.0, u); xcross(C, u - 0.2, 540, 880, 300, RED, 30); slam(C, u, 'НЕ В СВЯЗЯХ', 540, 400, 140)
def s_nezp(C, u, t):
    L = layer(); wad(L, 540, 880, 420, 3); put(C, L.crop((240, 640, 840, 1120)), 540, 880, back(u / 0.2)); xcross(C, u - 0.25, 540, 880, 300, RED, 30)
    slam(C, u, 'И ДАЖЕ', 540, 380, 140); plate(C, t - T('зарплате'), 'НЕ В ЗАРПЛАТЕ', 540, 530, 100, RED, WHITE, 3)
def s_delaesh(C, u, t):
    ground(C); d = D(C); d.line([540, 640, 540, G], fill=LG, width=8)
    leha(C, 'shrug', u, 270, 0.34); misha(C, 'smile', u, 810, 0.34, flip=True)
    for j in range(5):
        q = (u * 1.2 + j / 5) % 1; coin(C, 270 + (j - 2) * 60 + 200 * q * (1 if j % 2 else -0.4), 760 - 300 * q, 28, q * 500)
    piggy(C, 810, 820, 0.45, u, clamp(u / 2.5)); q = (u * 1.4) % 1; coin(C, 810, lerp(520, 700, q), 26)
    put(C, plate_img('ТРАТИТ', 52, RED, WHITE, pad=12, r=8), 270, 1180, back((u - 0.2) / 0.2), -3); put(C, plate_img('ВКЛАДЫВАЕТ', 52, GREEN, WHITE, pad=12, r=8), 810, 1180, back((u - 0.35) / 0.2), 3)
    slam(C, u, 'А В ТОМ, ЧТО ТЫ', 540, 360, 100); plate(C, t - T('делаешь'), 'ДЕЛАЕШЬ С ДЕНЬГАМИ', 540, 500, 84)
def s_kto(C, u, t):
    ground(C); leha(C, 'idle_smile', u, 270, 0.4); misha(C, 'smile', u, 810, 0.4, flip=True); vs(C, u, 540, 900)
    name(C, t - T('Лёха', 3), 'ЛЁХА?', 270, 1180, YEL, INK, -4, 64); name(C, t - T('Миша', 2), 'МИША?', 810, 1180, INK, YEL, 4, 64)
    slam(C, u, 'ТЫ КТО?', 540, 400, 170)
def s_napishi(C, u, t):
    ground(C); man(C, 'pointcam', u, 540, G, 0.44); speech(C, 540, 560, 820, 330, back(u / 0.22))
    if u > 0.12: txt(C, 'НАПИШИ ЧЕСТНО:', 540, 500, 70); put(C, plate_img('ЛЁХА ИЛИ МИША?', 84, YEL, INK, pad=18, r=12), 540, 620, back((u - 0.12) / 0.2))
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 540, G + 40, 0.48)
    else: man(C, 'walkR', e, 540 - e * 620, G + 40, 0.48, flip=True)
    slam(C, u, 'И', 540, 380, 200)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 540, 570, 140, INK, YEL)
PUSH_FLIP = False

def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_h1, 'none', 'boom'), SH(T('один', 0) - 0.05, s_h2, 'whipL', 'whoosh'), SH(T('Через') - 0.05, s_h3, 'spin', 'zoomin'),
 SH(T('один', 1) - 0.05, s_h4, 'drop', 'thud'), SH(T('а', 0) - 0.03, s_h5, 'zoomthru', 'bass', (540, 900)),
 SH(T('Почему') - 0.05, s_pochemu, 'shake', 'scratch'), SH(T('Смотри') - 0.05, s_smotri, 'zoom', 'whoosh'),
 SH(T('Это', 0) - 0.05, s_leha, 'whipR', 'whoosh'), SH(T('Это', 1) - 0.05, s_misha, 'whipL', 'whoosh'),
 SH(T('Оба', 0) - 0.05, s_oba, 'push', 'bass'), SH(T('Оба', 1) - 0.05, s_pashut, 'door', 'thud'),
 SH(T('Лёха', 1) - 0.05, s_yolo, 'shake', 'boom'), SH(T('Часы') - 0.05, s_chasy, 'zoom', 'shine'), SH(T('цепь') - 0.05, s_cep, 'whipL', 'coins'),
 SH(T('айфон') - 0.05, s_iphone, 'whipR', 'whoosh'), SH(T('такси') - 0.05, s_taxi, 'whipL', 'whoosh'), SH(T('доставка') - 0.05, s_dostavka, 'zoom', 'pop'),
 SH(T('К') - 0.05, s_nol, 'drop', 'thud'), SH(T('Ни') - 0.05, s_nihrena, 'glitch', 'error'),
 SH(T('А', 0) - 0.05, s_inache, 'bodywipe', 'bass'), SH(T('Каждый') - 0.05, s_8k, 'zoomthru', 'bass', (540, 900)),
 SH(T('И', 0) - 0.05, s_golova, 'whipU', 'riser'), SH(T('книги') - 0.05, s_knigi, 'whipL', 'whoosh'), SH(T('курсы') - 0.05, s_kursy, 'whipR', 'whoosh'),
 SH(T('новый') - 0.05, s_navyk, 'zoom', 'shine'),
 SH(T('Лёха', 2) - 0.05, s_rzhal, 'push', 'bass'),
 SH(T('Первый') - 0.05, s_god1, 'door', 'thud'), SH(T('Девяносто') - 0.05, s_96, 'zoom', 'tick2'),
 SH(T('Пятый') - 0.05, s_god5, 'spin', 'zoomin'), SH(T('У', 0) - 0.05, s_podushka, 'zoomthru', 'bass', (540, 880)), SH(T('У', 1) - 0.05, s_kredit3, 'drop', 'thud'),
 SH(T('А', 1) - 0.05, s_god10, 'glitch', 'riser'), SH(T('Своих') - 0.05, s_svoih, 'zoomthru', 'bass', (540, 880)),
 SH(T('А', 2) - 0.05, s_1840, 'shake', 'boom'), SH(T('Деньги') - 0.05, s_rabotayut, 'push', 'bass'),
 SH(T('Разница') - 0.05, s_udacha, 'whipL', 'whoosh'), SH(T('не', 2) - 0.05, s_svyazi, 'whipR', 'whoosh'), SH(T('и', 1) - 0.05, s_nezp, 'whipL', 'whoosh'),
 SH(T('А', 3) - 0.05, s_delaesh, 'door', 'thud'),
 SH(T('Ты', 1) - 0.05, s_kto, 'shake', 'boom'), SH(T('Напиши') - 0.05, s_napishi, 'bodywipe', 'bass'),
 SH(T('И', 1) - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('завод'), 'clang'), (T('долгах'), 'error'), (T('сука'), 'alarm'), (T('ляма'), 'kassa'), (T('Лёха', 0), 'pop'), (T('Миша', 0), 'pop'),
       (T('восемьдесят'), 'kassa'), (T('бля'), 'stamp'), (T('кредит'), 'stamp'), (T('такси') + 0.1, 'swipe'), (T('ноль'), 'error'), (T('осталось'), 'drop'),
       (T('иначе'), 'ding'), (T('восемь'), 'coins'), (T('голову') - 0.1, 'ding'), (T('навык'), 'ok'), (T('ржал'), 'boing'), (T('пенсионер'), 'pop'),
       (T('копейки'), 'pop'), (T('Смешно'), 'stamp'), (T('подушка'), 'pop'), (T('выше'), 'ok'), (T('третий'), 'error'),
       (T('девятьсот'), 'kassa'), (T('миллион'), 'coins'), (T('сорок'), 'shine'), (T('сами'), 'ding'), (T('удаче') + 0.2, 'error'), (T('связях') + 0.2, 'error'), (T('зарплате') + 0.2, 'error'),
       (T('деньгами'), 'kassa'), (T('Миша', 2), 'pop'), (T('честно'), 'msg'), (T('тупи'), 'stamp')]
