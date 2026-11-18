"""Монтаж «Сварщик vs программист»: тематический фон (PIL) + графика + два человечка (RGBA) -> ffmpeg."""
import json, math, sys, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from words import W, B, END, DUR
from tm import T
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920; SS = 2; GH = 1000
BG = (247, 245, 240); YEL = (255, 214, 10); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (225, 222, 215); MID = (196, 192, 184)
L1 = (228, 224, 216); L2 = (205, 200, 191)   # заливка и линии фона
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
@lru_cache(None)
def font(sz): return ImageFont.truetype(FB, int(sz * SS))
@lru_cache(None)
def font1(sz): return ImageFont.truetype(FB, int(sz))
ONLY = sys.argv[1:]
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def S(v): return int(round(v * SS))
FEET = 1335; SUB_Y = 1410

# ---------- плашки (графика в верхних 1000 px, 2x) ----------
@lru_cache(None)
def plate_img(text, sz, bg, fg, pad=28, border=None):
    f = font(sz); lines = text.split('\n'); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    ws = [d0.textbbox((0, 0), l, font=f) for l in lines]
    lh = int(sz * 1.18 * SS); w = max(b[2] - b[0] for b in ws) + S(pad) * 2; h = lh * len(lines) + S(pad) * 1.4
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=S(18), fill=bg, outline=border, width=S(5) if border else 0)
    for i, (l, b) in enumerate(zip(lines, ws)):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], S(pad) * 0.7 + i * lh + (lh - sz * SS) / 2 - S(sz * 0.12)), l, font=f, fill=fg)
    return im
def paste(G, im, cx, cy, scale=1.0, rot=0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    G.alpha_composite(im, (int(S(cx) - im.width / 2), int(S(cy) - im.height / 2)))
def plate(G, t, t0, text, cx, cy, sz=64, bg=YEL, fg=INK, rot=0, t1=None, border=None):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28); a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    paste(G, plate_img(text, int(sz * 1.25), bg, fg, border=border), cx, cy, sc, rot, a)
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))

# ---------- фоны (1x, прямо на кадр) ----------
def ground(d, x0=0, x1=WD): d.line([x0, FEET + 8, x1, FEET + 8], fill=L2, width=5)
def bg_univ(img, cx=540, k=1.0):
    d = ImageDraw.Draw(img); w = 620 * k; top = FEET - 640 * k; x0 = cx - w / 2
    d.polygon([(x0 - 30 * k, top + 150 * k), (cx, top), (x0 + w + 30 * k, top + 150 * k)], fill=L1, outline=L2, width=5)
    d.rectangle([x0, top + 150 * k, x0 + w, top + 200 * k], fill=L1, outline=L2, width=5)
    f = font1(int(38 * k)); d.text((cx, top + 176 * k), 'УНИВЕРСИТЕТ', font=f, fill=L2, anchor='mm')
    for j in range(6):
        x = x0 + 30 * k + j * (w - 60 * k) / 5
        d.rectangle([x - 18 * k, top + 200 * k, x + 18 * k, FEET - 30 * k], fill=L1, outline=L2, width=4)
    d.rectangle([x0 - 30 * k, FEET - 30 * k, x0 + w + 30 * k, FEET + 8], fill=L1, outline=L2, width=5)
def bg_stroyka(img, cx=540, k=1.0):
    d = ImageDraw.Draw(img)
    tx = cx + 170 * k; top = FEET - 900 * k   # кран
    for x in (tx - 28 * k, tx + 28 * k): d.line([x, top, x, FEET], fill=L2, width=5)
    for j in range(16):
        y = top + j * 56 * k; d.line([tx - 28 * k, y, tx + 28 * k, y + 56 * k], fill=L2, width=3)
    d.line([cx - 330 * k, top, tx + 160 * k, top], fill=L2, width=6); d.line([cx - 330 * k, top + 40 * k, tx + 160 * k, top + 40 * k], fill=L2, width=4)
    for j in range(14):
        x = cx - 330 * k + j * 35 * k; d.line([x, top, x + 35 * k, top + 40 * k], fill=L2, width=3)
    d.line([tx, top - 70 * k, cx - 300 * k, top], fill=L2, width=3); d.line([tx, top - 70 * k, tx + 160 * k, top], fill=L2, width=3)
    d.rectangle([tx + 110 * k, top + 40 * k, tx + 160 * k, top + 110 * k], fill=L1, outline=L2, width=4)
    hx = cx - 220 * k; d.line([hx, top + 40 * k, hx, top + 330 * k], fill=L2, width=3)   # трос с балкой
    d.rectangle([hx - 90 * k, top + 330 * k, hx + 90 * k, top + 352 * k], fill=L1, outline=L2, width=4)
    bx0 = cx - 470 * k; bw = 330 * k   # каркас дома
    for r in range(5):
        y = FEET - r * 120 * k
        d.line([bx0, y, bx0 + bw, y], fill=L2, width=6)
    for c in range(4):
        x = bx0 + c * bw / 3; d.line([x, FEET, x, FEET - 480 * k], fill=L2, width=6)
    ground(d)
def bg_office(img):
    d = ImageDraw.Draw(img)
    for j in range(4):
        x = 90 + j * 240; d.rectangle([x, 470, x + 180, 760], fill=L1, outline=L2, width=5); d.line([x + 90, 470, x + 90, 760], fill=L2, width=4)
    d.rectangle([60, FEET - 230, 1020, FEET - 205], fill=L1, outline=L2, width=4)   # длинный стол
    for x in (120, 960): d.line([x, FEET - 205, x, FEET], fill=L2, width=6)
    ground(d)
def bg_corridor(img, door_x=800):
    d = ImageDraw.Draw(img)
    d.line([0, 430, WD, 430], fill=L2, width=5)
    d.rectangle([door_x - 110, FEET - 520, door_x + 110, FEET + 8], fill=WHITE, outline=L2, width=7)
    d.rounded_rectangle([door_x - 120, FEET - 600, door_x + 120, FEET - 535], radius=12, fill=YEL, outline=INK, width=4)
    d.text((door_x, FEET - 567), 'ВАКАНСИЯ', font=font1(40), fill=INK, anchor='mm')
    for x in (120, 380): d.rectangle([x, 520, x + 150, 700], fill=L1, outline=L2, width=4)
    ground(d)
def bg_city(img):
    d = ImageDraw.Draw(img)
    for x, w, h in ((-20, 170, 520), (170, 140, 700), (330, 200, 430), (550, 150, 820), (720, 190, 560), (930, 170, 660)):
        d.rectangle([x, FEET - h, x + w, FEET + 8], fill=L1, outline=L2, width=4)
        for r in range(int(h / 90) - 1):
            for c in range(int(w / 60)):
                d.rectangle([x + 22 + c * 55, FEET - h + 40 + r * 90, x + 46 + c * 55, FEET - h + 80 + r * 90], fill=BG)
    ground(d)
def bg_room(img):
    d = ImageDraw.Draw(img)
    d.rectangle([600, 430, 960, 820], fill=L1, outline=L2, width=6); d.line([780, 430, 780, 820], fill=L2, width=5); d.line([600, 625, 960, 625], fill=L2, width=5)
    d.line([80, 560, 400, 560], fill=L2, width=7)
    for j, (h, w) in enumerate(((110, 34), (90, 28), (120, 40), (80, 30))):
        x = 100 + j * 50; d.rectangle([x, 560 - h, x + w, 560], fill=L1, outline=L2, width=4)
    d.ellipse([280, 470, 360, 558], fill=L1, outline=L2, width=4)
    ground(d)

# ---------- серые фигурки и предметы ----------
def grey_person(img, cx, feet, h, col=MID, laptop=False, hat=False, sign=None, walk=0.0, t=0.0, alpha=255):
    d = ImageDraw.Draw(img); w = h * 0.24; hr = h * 0.13; bob = abs(math.sin(t * 9)) * h * 0.02 if walk else 0
    top = feet - h * 0.78 - bob
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, feet - bob * 0], radius=w / 2, fill=col)
    d.line([cx, feet - h * 0.38, cx, feet], fill=BG, width=max(2, int(h * 0.02)))
    d.ellipse([cx - hr, top - hr * 2.05, cx + hr, top - hr * 0.05], fill=col)
    if hat:
        d.chord([cx - hr * 1.1, top - hr * 2.25, cx + hr * 1.1, top - hr * 0.2], 180, 360, fill=YEL)
        d.rectangle([cx - hr * 1.35, top - hr * 1.25, cx + hr * 1.35, top - hr * 1.1], fill=YEL)
    if laptop:
        d.rounded_rectangle([cx - w * 0.3, top + h * 0.26, cx + w * 0.3, top + h * 0.34], radius=3, fill=(232, 230, 226))
    if sign is not None:
        sw = h * 0.36; sy = top - hr * 2.2 - sw * 0.55
        d.line([cx + w * 0.55, top + h * 0.15, cx + w * 0.55, sy + sw * 0.3], fill=col, width=max(3, int(h * 0.03)))
        d.rounded_rectangle([cx + w * 0.55 - sw / 2, sy - sw * 0.3, cx + w * 0.55 + sw / 2, sy + sw * 0.3], radius=8, fill=YEL, outline=INK, width=4)
        d.text((cx + w * 0.55, sy), sign, font=font1(int(sw * (0.36 if len(sign) < 3 else 0.27))), fill=INK, anchor='mm')
def money(img, cx, base, w, n, col=YEL):
    d = ImageDraw.Draw(img); hh = w * 0.16
    for j in range(n):
        y = base - j * hh * 0.85; d.rounded_rectangle([cx - w / 2, y - hh, cx + w / 2, y], radius=6, fill=col, outline=INK, width=4)
    d.text((cx, base - n * hh * 0.85 - hh * 0.9), '₽', font=font1(int(w * 0.4)), fill=INK, anchor='mm')
def books(img, cx, base, n, k=1.0, t=0, t0=0):
    d = ImageDraw.Draw(img); cols = [(255, 214, 10), (230, 230, 230), (190, 190, 190), (255, 230, 120)]
    for j in range(n):
        u = eo((t - t0 - j * 0.18) / 0.25)
        if u <= 0: continue
        y = base - j * 46 * k - 300 * (1 - u); w = (200 - (j % 2) * 24) * k
        d.rounded_rectangle([cx - w / 2 + (j % 2) * 10, y - 42 * k, cx + w / 2 + (j % 2) * 10, y], radius=6, fill=cols[j % 4], outline=INK, width=4)
        d.line([cx - w / 2 + 18 * k + (j % 2) * 10, y - 21 * k, cx + w / 2 - 18 * k + (j % 2) * 10, y - 21 * k], fill=INK, width=3)
    return base - n * 46 * k
def tag(img, cx, cy, w, col, txt=''):
    d = ImageDraw.Draw(img); h = w * 0.55
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2 - h / 2, cy - h / 2), (cx + w / 2, cy), (cx + w / 2 - h / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], fill=col, outline=INK, width=5)
    d.ellipse([cx + w / 2 - h * 0.62 - 9, cy - 9, cx + w / 2 - h * 0.62 + 9, cy + 9], fill=WHITE, outline=INK, width=3)
    if txt: d.text((cx - h * 0.25, cy), txt, font=font1(int(h * 0.5)), fill=INK, anchor='mm')
def sparks(img, x, y, t):
    d = ImageDraw.Draw(img)
    for j in range(9):
        a = j * 0.7 + t * 7; r = 30 + (t * 300 + j * 37) % 90
        d.line([x, y, x + math.cos(a) * r, y + math.sin(a) * r * 0.7 - 20], fill=YEL if j % 2 else (255, 160, 0), width=5)

# ---------- раскладка человечков: (cx, s) или None ----------
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)
L_, R_ = 300, 780
def lay(t):
    L = line_of(t)
    M = {0: ((L_, .42), (R_, .42)), 1: ((540, .48), None), 2: (None, (540, .48)), 3: ((L_, .42), (R_, .42)), 4: ((540, .46), None),
         5: ((540, .46), None), 6: ((420, .46), None), 7: ((540, .46), None), 8: ((590, .42), None), 9: (None, (260, .44)), 10: (None, (300, .44)),
         11: (None, (300, .44)), 12: ((540, .46), None), 13: ((L_, .42), (R_, .42)), 14: ((300, .44), None), 15: ((300, .44), None),
         16: ((470, .42), (820, .40)), 17: ((420, .42), (720, .42))}
    return M[L]
def zoom(t):
    for ta, tb, cy in ((T['mnogo'] - 0.1, B[7], 900), (T['trudno'], B[14], 900)):
        if ta <= t < tb: return 1 + 0.06 * eo((t - ta) / 0.25), cy
    return 1.0, 900

# ---------- сцены ----------
def under(img, t):
    L = line_of(t)
    if L in (0, 3, 13):
        bg_univ(img, 250, 0.62); bg_stroyka(img, 820, 0.62)
    if L == 0:
        k = back((t - T['svarshik']) / 0.3)
        if k > 0.1: money(img, R_, FEET - 740, 200 * k, 7)
        k = back((t - T['programmist']) / 0.3)
        if k > 0.1: money(img, L_, FEET - 740, 200 * k, 2, (230, 230, 230))
    elif L == 1:
        bg_univ(img)
        books(img, 830, 1000, 4, 1.25, t, T['chetyre'] - 0.1)
    elif L == 2:
        bg_stroyka(img)
        books(img, 250, 1000, 2, 1.25, t, T['dva'] - 0.1)
        if t >= T['kolledzha']: sparks(img, 700, FEET - 260, t)
    elif L == 3:
        if t >= T['menshe'] - 0.3:
            u = eo((t - T['menshe'] + 0.3) / 0.3)
            tag(img, L_ + 60, 560 - 300 * (1 - u), 150, (230, 230, 230), '₽')
            tag(img, R_ + 30, 520 - 300 * (1 - u), 280, YEL, '₽₽₽')
    elif L in (4, 5, 6):
        bg_office(img)
        if L == 6:
            n = 3 if t < T['mnogo'] - 0.1 else 11
            for j in range(n):
                x = 130 + (j * 83) % 860; f = FEET - 10 - (j % 3) * 18
                if abs(x - 420) < 110: x += 230
                k = back((t - B[6] - 0.08 * j) / 0.3) if j < 3 else back((t - T['mnogo'] + 0.1 - 0.05 * j) / 0.3)
                if k > 0.1: grey_person(img, x, f, 380 * k * (0.9 + 0.1 * (j % 2)), laptop=True)
    elif L in (7, 12):
        bg_city(img)
    elif L == 8:
        bg_corridor(img)
        for j in range(7):
            x = 470 - j * 105
            k = back((t - B[8] - 0.07 * j) / 0.3)
            if k > 0.1: grey_person(img, x, FEET, 400 * k)
        if t >= T['vybiray'] - 0.2:   # работодатель в двери
            grey_person(img, 800, FEET, 420, col=(170, 166, 158))
    elif L in (9, 10, 11):
        bg_stroyka(img, 600, 0.9)
        if L == 9:
            for j in range(4):
                tk = T['ochered'] + j * 0.25; k = back((t - tk) / 0.3)
                if k <= 0.1: continue
                lvl = clamp((t - T['perebivayut']) / 1.2) * 3
                sg = '₽' * min(3, 1 + int(lvl + j * 0.6)) if t >= T['perebivayut'] else '₽'
                grey_person(img, 470 + j * 125, FEET, 360 * k, col=(170, 166, 158), sign=sg[:3])
        elif L == 10:
            for j in range(4): grey_person(img, 470 + j * 125, FEET, 360, col=(170, 166, 158), sign='₽₽₽')
        else:
            go = clamp((t - T['razvernetsya'] + 0.4) / 1.0)
            for j in range(4):
                if go < 1: grey_person(img, 470 + j * 125 + go * 600, FEET, 360, col=(170, 166, 158), sign='₽', walk=go > 0, t=t)
            for j in range(5):
                tk = T['poydut'] + 0.3 + j * 0.25; u = eo((t - tk) / 0.6)
                if u <= 0: continue
                grey_person(img, -150 + (170 - j * 80 + 150) * u, FEET, 340, hat=True, walk=u < 1, t=t)
    elif L in (14, 15):
        bg_room(img)
    elif L in (16, 17):
        bg_city(img)
        if L == 16:
            for j in range(4):
                k = back((t - B[16] - 0.1 * j) / 0.3)
                if k > 0.1: grey_person(img, 300 - j * 85, FEET, 300 * k, col=(170, 166, 158), sign='₽₽')

def sc(G, t):
    L = line_of(t)
    if L == 0:
        plate(G, t, T['svarshik'] - 0.1, 'СВАРЩИК', 780, 120, 72, YEL, INK, rot=3)
        plate(G, t, T['programmist'] - 0.1, 'ПРОГРАММИСТ', 300, 120, 64, INK, WHITE, rot=-3)
    elif L == 1: plate(G, t, T['chetyre'] - 0.1, '4 ГОДА', 820, 120, 90, INK, WHITE, rot=-3)
    elif L == 2: plate(G, t, T['dva'] - 0.1, '2 ГОДА', 250, 120, 90, YEL, INK, rot=3)
    elif L == 3: plate(G, t, T['prostite'] - 0.05, 'ПРОСТИТЕ,\nА ЗА ЧТО?', 540, 150, 76, INK, WHITE, rot=-2)
    elif L == 4: plate(G, t, T['dumaesh'] + 0.1, 'ПРОГРАММИСТЫ\nНЕ НУЖНЫ?', 540, 220, 70, LG, GREY, rot=-3)
    elif L == 5:
        plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 200, 84, YEL, INK, rot=-3)
        paste(G, plate_img('НЕ НУЖНЫ?', 64, LG, GREY, pad=22), 540, 520, 1.0, 3)
        cross(G, 300, 470, 780, 580, clamp((t - T['stop'] - 0.4) / 0.3))
    elif L == 6:
        plate(G, t, T['nuzhny2'] - 0.05, 'НУЖНЫ', 300, 110, 70, INK, WHITE, rot=-3)
        plate(G, t, T['mnogo'] - 0.15, 'ИХ МНОГО', 700, 230, 92, YEL, INK, rot=3)
    elif L == 7:
        if t < T['zarplata'] - 0.1: plate(G, t, T['nas'], 'НАС ЭТОМУ\nНЕ УЧИЛИ', 540, 200, 80, INK, WHITE, rot=-3)
        else:
            plate(G, t, T['nagrada'] - 0.1, 'НЕ НАГРАДА', 540, 120, 70, LG, GREY, rot=-2)
            cross(G, 300, 70, 780, 170, clamp((t - T['cena'] + 0.6) / 0.3))
            plate(G, t, T['cena'] - 0.1, 'ЗАРПЛАТА = ЦЕНА', 540, 300, 76, YEL, INK, rot=2)
    elif L == 8:
        plate(G, t, T['tolpa'] - 0.1, 'ТОЛПА ДИМ', 400, 110, 72, INK, WHITE, rot=-3)
        plate(G, t, T['vybiray'] - 0.05, 'ВЫБИРАЙ ЛЮБОГО', 540, 260, 66, LG, INK, rot=2)
    elif L == 9:
        plate(G, t, T['ochered'] - 0.1, 'ОЧЕРЕДЬ К НЕМУ', 540, 110, 80, YEL, INK, rot=-3)
    elif L == 10: plate(G, t, T['podvoh'] - 0.4, 'А ВОТ И ПОДВОХ', 540, 160, 92, YEL, INK, rot=-3)
    elif L == 11: plate(G, t, T['poydut'], 'ВСЕ В СВАРЩИКИ?', 540, 120, 76, INK, WHITE, rot=-2)
    elif L == 12: plate(G, t, B[12] + 0.05, 'ЗА ЧТО\nПЛАТЯТ?', 540, 200, 92, YEL, INK, rot=-3)
    elif L == 13:
        if t < T['trudno'] - 0.2:
            plate(G, t, T['tyazhelo'] - 0.2, 'КАК ТЯЖЕЛО\nУЧИЛСЯ', 300, 180, 64, LG, GREY, rot=-3)
            cross(G, 120, 110, 480, 260, clamp((t - T['tyazhelo'] - 0.6) / 0.3))
        else:
            plate(G, t, T['trudno'] - 0.2, 'КАК ТРУДНО\nЗАМЕНИТЬ', 700, 180, 76, YEL, INK, rot=3)
    elif L == 14:
        if t < T['prestizh'] - 0.2: plate(G, t, T['delat'] - 0.6, 'И ЧТО С ЭТИМ\nДЕЛАТЬ?', 540, 200, 84, YEL, INK, rot=-3); return
        plate(G, t, T['prestizh'] - 0.1, 'ПРЕСТИЖ', 260, 90, 64, LG, GREY, rot=-3)
        cross(G, 100, 50, 420, 140, clamp((t - T['ochered2'] + 0.2) / 0.3))
        plate(G, t, T['ochered2'] - 0.1, 'ОЧЕРЕДЬ', 790, 90, 74, INK, WHITE, rot=3)
        d = ImageDraw.Draw(G)
        for j, (lab, key, ln, col) in enumerate((('ВАКАНСИИ', 'vakansiy', 180, YEL), ('РЕЗЮМЕ', 'rezume', 400, LG))):
            if t < T[key] - 0.1: continue
            u = eo((t - T[key] + 0.1) / 0.5); y = 300 + j * 130
            d.text((S(560), S(y)), lab, font=font(48), fill=INK)
            d.rounded_rectangle([S(560), S(y + 62), S(560 + ln * u), S(y + 110)], radius=S(20), fill=col, outline=INK, width=S(5))
    elif L == 15:
        k1 = back((t - T['soedini'] + 0.1) / 0.3); m = eo((t - T['navyka'] - 0.5) / 0.5)
        if m < 1:
            paste(G, plate_img('КОД', 64, WHITE, INK, border=INK), 560 + 80 * m, 250, k1, -4)
            paste(G, plate_img('МЕДИЦИНА', 64, WHITE, INK, border=INK), 860 - 80 * m, 400 - 150 * m, k1, 4)
        else:
            plate(G, t, T['navyka'] + 1.0, 'КОД + МЕДИЦИНА', 700, 250, 62, YEL, INK, rot=-2)
        plate(G, t, T['malo'] - 0.1, 'ТАКИХ МАЛО', 700, 420, 76, INK, WHITE, rot=3)
    elif L == 16: plate(G, t, T['k_tebe'] - 0.4, 'ОЧЕРЕДЬ К ТЕБЕ', 540, 160, 80, YEL, INK, rot=-3)
    elif L == 17: plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 280, 110, YEL, INK, rot=-4)
def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0)); sc(G, t)
    return G.resize((WD, GH), Image.LANCZOS)

# ---------- субтитры ----------
SUBF = ImageFont.truetype(FB, 56); SP = 14; MAXW = 780
_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
def wlen(w): return _d.textbbox((0, 0), w[0].upper().strip('«»'), font=SUBF)[2]
def wrap(ws):
    lines, cur, cw = [], [], 0
    for w in ws:
        l = wlen(w)
        if cur and cw + SP + l > MAXW: lines.append(cur); cur, cw = [], 0
        cw = l if not cur else cw + SP + l; cur.append(w)
    if cur: lines.append(cur)
    return lines
groups, cur = [], []
for w in W:
    if cur and (len(wrap(cur + [w])) > 2 or len(cur) >= 7): groups.append(cur); cur = []
    cur.append(w)
    if w[0].rstrip('»')[-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 3): groups.append(cur); cur = []
if cur: groups.append(cur)
def subs(img, t, y0=SUB_Y):
    g = next((g for i, g in enumerate(groups) if g[0][1] - 0.05 <= t < (groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else g[-1][2] + 0.4)), None)
    if not g: return
    d = ImageDraw.Draw(img); lines = wrap(g); y = y0 if len(lines) == 1 else y0 - 37
    for ln in lines:
        ws = [wlen(w) for w in ln]; x = (WD - (sum(ws) + SP * (len(ws) - 1))) / 2
        for w, wd in zip(ln, ws):
            if w[1] <= t < w[2] + 0.15:
                d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=YEL)
            else:
                d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=(255, 255, 255))
            d.text((x, y), w[0].upper().strip('«»'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

# ---------- человечки ----------
CH_CROP = (0, 60, 1080, 1660)
seg = json.load(open('seg.json'))
WALK0 = END + 0.75
def char(img, who, i, cx, s):
    t = i / FPS
    if seg[who][i] == 'walk': cx -= (i - int(round(WALK0 * FPS))) * 22.0
    cw, chh = int(1080 * s), int(1600 * s); x0 = int(cx - cw / 2); y0 = int(FEET + 70 * s - chh)
    ch = Image.open(f'kadry/{who}/{i:03d}.png').convert('RGBA').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    img.alpha_composite(ch, (x0, y0))

def frame(i):
    t = i / FPS; L = line_of(t)
    img = Image.new('RGBA', (WD, HT), BG + (255,))
    under(img, t)
    G = graphics(t); img.alpha_composite(G, (0, 190))
    a, b = lay(t)
    # плавный переезд между сценами
    if L > 0 and t - B[L] < 0.4:
        pa, pb = lay(B[L] - 0.01); e = eo((t - B[L]) / 0.4)
        if a and pa: a = (pa[0] + (a[0] - pa[0]) * e, pa[1] + (a[1] - pa[1]) * e)
        if b and pb: b = (pb[0] + (b[0] - pb[0]) * e, pb[1] + (b[1] - pb[1]) * e)
    if b: char(img, 'svar', i, *b)
    if a: char(img, 'main', i, *a)
    subs(img, t)
    img = img.convert('RGB')
    z, cy = zoom(t)
    if z != 1:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5), int((h - HT) * cy / HT); img = im2.crop((ox, oy, ox + WD, oy + HT))
    return img

if __name__ == '__main__':
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        for i in range(N):
            p.stdin.write(frame(i).tobytes())
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
