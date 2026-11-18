"""Монтаж «Он выбрал тебя»: фон + 2D-графика (PIL) + 3D-предметы (RGBA) + муж и жена (RGBA) -> ffmpeg.
python3 compose_v.py [сек ...] — превью кадров; без аргументов — video_noaudio.mp4"""
import json, math, sys, subprocess, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from words import W, B, END, DUR, wt
from props_plan import T as PT
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920; SS = 2
BG = (247, 245, 240); YEL = (255, 214, 10); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (225, 222, 215); MID = (196, 192, 184); PINK = (255, 79, 139); HRT = (232, 52, 74)
L1 = (228, 224, 216); L2 = (205, 200, 191)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
@lru_cache(None)
def font(sz): return ImageFont.truetype(FB, int(sz * SS))
@lru_cache(None)
def font1(sz): return ImageFont.truetype(FB, int(sz))
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return t * t * (3 - 2 * t)
def S(v): return int(round(v * SS))
FEET = 1335; SUB_Y = 1410
def w_(s, k=0): return wt(s, k)
TT = dict(vybral=w_('выбрал'), sam=w_('сам.'), roditeli=w_('Родители'), vybirali=w_('выбирали'), rebenok=w_('ребёнок'), bratya=w_('Братья'),
          krov=w_('кровь'), detyam=w_('Детям'), dala=w_('дала'), dolzhen=w_('должен'), nichego=w_('ничего'), naznachal=w_('назначал'), mog=w_('мог'),
          uyti=w_('уйти'), vosmi=w_('восьми'), milliardov=w_('миллиардов'), pokazal=w_('показал'), tebya3=w_('тебя', 2), skazal=w_('сказал'),
          stroyu=w_('строю'), stop=w_('Стоп'), tupish=w_('тупишь'), navsegda=w_('навсегда'), shkaf=w_('шкаф'), podvoh=w_('подвох'),
          lyubov=w_('Любовь'), cvetok=w_('цветок'), polivaesh=w_('поливаешь'), vyanet=w_('вянет'), vybrali=w_('выбрали'), kazhdy=w_('Каждый'),
          otprav=w_('Отправь'), znaet=w_('знает'), netupi=w_('тупи.'))
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)

# ---------- плашки (2x слой на весь кадр) ----------
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
def paste(G, im, cx, cy, scale=1.0, rot=0, alpha=1.0, ss=SS):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    G.alpha_composite(im, (int(cx * ss - im.width / 2), int(cy * ss - im.height / 2)))
def plate(G, t, t0, text, cx, cy, sz=64, bg=YEL, fg=INK, rot=0, t1=None, border=None):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28); a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    paste(G, plate_img(text, int(sz * 1.25), bg, fg, border=border), cx, cy, sc, rot, a)
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))
def heart2d(d, cx, cy, r, col=HRT, ss=1):
    pts = []
    for j in range(60):
        a = j / 60 * 2 * math.pi; x = 16 * math.sin(a) ** 3; y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append(((cx + x * r / 16) * ss, (cy - y * r / 16) * ss))
    d.polygon(pts, fill=col)

# ---------- фон и серые фигурки (1x) ----------
def ground(d, x0=0, x1=WD): d.line([x0, FEET + 8, x1, FEET + 8], fill=L2, width=5)
def grey_person(d, cx, feet, h, col=MID, dress=False, walk=0.0, t=0.0):
    w = h * 0.24; hr = h * 0.13; bob = abs(math.sin(t * 9 + cx)) * h * 0.03 if walk else 0
    top = feet - h * 0.78 - bob
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, feet - bob], radius=w / 2, fill=col)
    d.line([cx, feet - h * 0.38 - bob, cx, feet - bob], fill=BG, width=max(2, int(h * 0.02)))
    d.ellipse([cx - hr, top - hr * 2.05, cx + hr, top - hr * 0.05], fill=col)
    if dress:
        d.chord([cx - hr * 1.15, top - hr * 2.2, cx + hr * 1.15, top - hr * 0.0], 180, 360, fill=col)
        d.rectangle([cx - hr * 1.15, top - hr * 1.15, cx - hr * 0.75, top + hr * 0.3], fill=col); d.rectangle([cx + hr * 0.75, top - hr * 1.15, cx + hr * 1.15, top + hr * 0.3], fill=col)
def door(d, cx, k, open_=0.3):
    if k <= 0.1: return
    h = 560 * k; top = FEET + 8 - h
    d.rectangle([cx - 120, top, cx + 120, FEET + 8], fill=(255, 250, 225), outline=L2, width=7)
    ow = 240 * (1 - open_)
    d.polygon([(cx - 120, top), (cx - 120 + ow, top + 30 * k), (cx - 120 + ow, FEET + 8 - 10), (cx - 120, FEET + 8)], fill=L1, outline=L2)
    d.ellipse([cx - 120 + ow - 34, top + h * 0.5, cx - 120 + ow - 16, top + h * 0.5 + 18], fill=L2)
def wardrobe(d, cx, k, t):
    if k <= 0.1: return
    w, h = 300 * k, 560 * k; x0 = cx - w / 2; top = FEET + 8 - h
    d.rectangle([x0, top, x0 + w, FEET + 8], fill=L1, outline=L2, width=6)
    d.line([cx, top + 20, cx, FEET - 20], fill=L2, width=5)
    for x in (cx - 26, cx + 14): d.rounded_rectangle([x, top + h * 0.45, x + 12, top + h * 0.45 + 60 * k], radius=5, fill=L2)
    d.line([x0, top, x0 + 60 * k, top + 60 * k], fill=L2, width=2); d.line([x0 + 30 * k, top, x0 + 30 * k, top + 45 * k], fill=L2, width=2)   # паутина
    d.arc([x0 - 20 * k, top - 20 * k, x0 + 70 * k, top + 70 * k], 0, 90, fill=L2, width=2)
    rnd = random.Random(7)
    for j in range(14):   # пыль
        y = top - 130 + ((t * 25 + j * 37) % 160); x = cx - 110 + rnd.random() * 220
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=MID)
def watering_can(d, cx, cy, k):
    if k <= 0.25: return
    s = 110 * k
    d.rounded_rectangle([cx - s, cy - s * 0.7, cx + s * 0.6, cy + s * 0.7], radius=20, fill=L1, outline=INK, width=5)
    d.polygon([(cx + s * 0.6, cy + s * 0.2), (cx + s * 1.5, cy - s * 0.9), (cx + s * 1.6, cy - s * 0.75), (cx + s * 0.6, cy + s * 0.5)], fill=L1, outline=INK)
    d.arc([cx - s * 1.1, cy - s * 1.3, cx + s * 0.2, cy + s * 0.1], 180, 320, fill=INK, width=8)
def phone(d, cx, cy, k, t, t0):
    if k <= 0.25: return
    w, h = 230 * k, 420 * k
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=34 * k, fill=INK)
    d.rounded_rectangle([cx - w / 2 + 14, cy - h / 2 + 30, cx + w / 2 - 14, cy + h / 2 - 30], radius=16 * k, fill=WHITE)
    u = eo((t - t0 - 0.25) / 0.3)
    if u > 0:
        d.rounded_rectangle([cx - w / 2 + 34, cy - 40, cx - w / 2 + 34 + (w - 68) * u, cy + 30], radius=18, fill=YEL)
        if u > 0.9: heart2d(d, cx, cy - 5, 22)
    f = clamp((t - t0 - 0.7) / 0.9)   # бумажный самолётик
    if f > 0:
        px = cx + 80 + f * 380; py = cy - 120 - f * 260 + math.sin(f * 6) * 30
        d.polygon([(px + 60, py), (px - 50, py - 34), (px - 20, py), (px - 50, py + 30)], fill=WHITE, outline=INK, width=5)
        d.line([px - 20, py, px + 60, py], fill=INK, width=4)

# ---------- раскладка человечков ----------
def keyx(keys, t):   # [(t, x)] с плавной интерполяцией
    if t <= keys[0][0]: return keys[0][1]
    for (a, x0), (b, x1) in zip(keys, keys[1:]):
        if a <= t < b: return x0 + (x1 - x0) * clamp((t - a) / (b - a))
    return keys[-1][1]
def lay(who, t):
    L = line_of(t)
    if who == 'muzh':
        M = {0: (keyx([(0, 1250), (1.55, 760)], t), .42), 1: None, 2: (keyx([(w_('просто', 1), 540), (16.95, 730)], t), .48), 3: (250, .40), 4: None, 5: None,
             6: (790, .42), 7: (680, .42), 8: (680, .42)}
    else:
        M = {0: (300, .40), 1: (540, .46), 2: None, 3: (820, .40), 4: (330, .46), 5: (210, .40), 6: (keyx([(B[6], 120), (33.35, 590)], t), .42),
             7: (420, .42), 8: (420, .42)}
    return M[L]
def pos(who, t):
    L = line_of(t); a = lay(who, t); sc = 1.0
    if L > 0 and t - B[L] < 0.4:
        pa = lay(who, B[L] - 0.01)
        if a and pa and L not in (6,):
            e = eo((t - B[L]) / 0.4); a = (pa[0] + (a[0] - pa[0]) * e, pa[1] + (a[1] - pa[1]) * e)
        elif a and not pa: sc = back((t - B[L]) / 0.35)
    return a, sc
CH_CROP = (0, 60, 1080, 1660)
seg = json.load(open('seg.json'))
WALK0 = END + 0.75
def char(img, who, i, cx, s, sc=1.0):
    if seg[who][i] == 'walkL' and i / FPS > END: cx -= (i - int(round(WALK0 * FPS))) * 22.0
    s *= sc
    if s < 0.02: return
    cw, chh = int(1080 * s), int(1600 * s); x0 = int(cx - cw / 2); y0 = int(FEET + 70 * s - chh)
    import os
    if not os.path.exists(f'kadry/{who}/{i:03d}.png'): return
    ch = Image.open(f'kadry/{who}/{i:03d}.png').convert('RGBA').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    img.alpha_composite(ch, (x0, y0))
def head_y(s): return FEET + 70 * s - 1600 * s + (380 - 60) * s   # примерно верх головы

# ---------- 3D-предметы ----------
PPLAN = json.load(open('props_plan.json'))
@lru_cache(64)
def prop_img(idx): return Image.open(f'kadry_props/p/{idx:03d}.png').convert('RGBA')
def props(img, i, front):
    for idx, x, y, s in PPLAN[i]:
        im = prop_img(idx)
        kind = PROPK[idx]
        if (kind in ('house',)) == front: continue    # дом позади людей, остальное спереди
        im = im.resize((max(1, int(s)), max(1, int(s))), Image.LANCZOS)
        img.alpha_composite(im, (int(x - s / 2), int(y - s / 2)))
PROPK = [p['kind'] for p in json.load(open('props.json'))['p']]

# ---------- сцены: фон (1x, под людьми) ----------
def under(img, t):
    d = ImageDraw.Draw(img); L = line_of(t)
    ground(d)
    if L == 1:   # пузыри «родные»: родители, братья и сёстры, дети
        hx, hy = 540, head_y(.46) + 40
        for j, (cx, cy, key, lab) in enumerate(((200, 660, 'roditeli', 'РОДИТЕЛИ'), (540, 560, 'bratya', 'БРАТЬЯ И СЁСТРЫ'), (880, 660, 'detyam', 'ДЕТИ'))):
            k = back((t - TT[key] + 0.1) / 0.35)
            if k <= 0.02: continue
            r = 150 * k; k *= 1.25
            d.line([cx, cy + r, hx + (cx - 540) * 0.08, hy], fill=L2, width=4)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=5)
            if j == 0: grey_person(d, cx - 30 * k, cy + 80 * k, 150 * k); grey_person(d, cx + 32 * k, cy + 80 * k, 140 * k, dress=True)
            if j == 1: grey_person(d, cx - 34 * k, cy + 80 * k, 125 * k); grey_person(d, cx + 34 * k, cy + 80 * k, 120 * k, dress=True); d.ellipse([cx - 14 * k, cy - 95 * k, cx + 14 * k, cy - 60 * k], fill=HRT)
            if j == 2: grey_person(d, cx - 26 * k, cy + 80 * k, 85 * k); grey_person(d, cx + 26 * k, cy + 80 * k, 75 * k, dress=True)
            d.text((cx, cy + r + 34), lab, font=font1(34), fill=INK, anchor='mm')
    if L == 2:
        door(d, 900, back((t - TT['mog'] + 0.2) / 0.4), open_=0.2 + 0.4 * clamp((t - TT['uyti']) / 0.6))
    if L == 3:   # толпа: 8 миллиардов
        layer = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
        fade = 1 - clamp((t - TT['tebya3'] - 0.4) / 0.5)
        rnd = random.Random(3)
        rows = [(FEET - 230, 150, 15), (FEET - 140, 220, 11), (FEET - 30, 300, 8)]
        n = 0
        for ri, (fy, h, cnt) in enumerate(rows):
            for j in range(cnt):
                x = (j + 0.5) * WD / cnt + rnd.uniform(-20, 20)
                if ri == 2 and (abs(x - 250) < 120 or abs(x - 820) < 120): continue
                k = back((t - TT['vosmi'] - 0.03 * n) / 0.3); n += 1
                if k > 0.05: grey_person(dl, x, fy, h * k * rnd.uniform(0.9, 1.05), col=(208 - ri * 10,) * 3, dress=rnd.random() < 0.5)
        if fade < 1: layer.putalpha(layer.getchannel('A').point(lambda a: int(a * fade)))
        img.alpha_composite(layer)
        if t >= TT['pokazal'] + 0.6:   # луч прожектора на неё
            u = eo((t - TT['pokazal'] - 0.6) / 0.3)
            ov = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
            do.polygon([(780, 300), (860, 300), (980, FEET + 20), (660, FEET + 20)], fill=YEL + (int(70 * u),))
            do.ellipse([660, FEET - 20, 980, FEET + 40], fill=YEL + (int(160 * u),))
            img.alpha_composite(ov)
    if L == 4:
        wardrobe(d, 800, back((t - TT['shkaf'] + 0.1) / 0.35), t)
    if L == 5:
        k = back((t - TT['polivaesh'] + 0.15) / 0.3)
        watering_can(d, 880, 560, k)
    if L == 6:
        for j in range(10):   # всплывающие сердечки
            t0 = 33.4 + j * 0.22
            if t < t0: continue
            u = (t - t0) / 1.6
            if u > 1: continue
            x = 690 + math.sin(j * 1.7 + u * 5) * 90; y = 950 - u * 420
            heart2d(d, x, y, 18 + 10 * (j % 3), col=HRT if j % 2 else PINK)
    if L == 7:
        phone(d, 840, 560, back((t - TT['otprav'] + 0.1) / 0.3), t, TT['otprav'])

# ---------- плашки сверху ----------
def sc(G, t):
    L = line_of(t)
    if L == 0:
        plate(G, t, 0.05, 'ТВОЙ МУЖ', 540, 330, 92, INK, WHITE, rot=-3)
        plate(G, t, TT['vybral'] - 0.1, 'ВЫБРАЛ ТЕБЯ САМ', 540, 470, 72, YEL, INK, rot=2)
    elif L == 1:
        plate(G, t, TT['vybirali'] - 0.15, 'НЕ ВЫБИРАЛИ', 220, 320, 46, LG, INK, rot=-4, t1=TT['bratya'] - 0.2)
        plate(G, t, TT['krov'] - 0.15, 'КРОВЬ', 540, 330, 54, LG, INK, rot=3, t1=TT['detyam'] - 0.2)
        plate(G, t, TT['dala'] - 0.15, 'ТЫ ДАЛА ЖИЗНЬ', 790, 320, 46, LG, INK, rot=-3)
    elif L == 2:
        if t < TT['mog'] - 0.2:
            plate(G, t, TT['nichego'] - 0.1, 'НИЧЕГО НЕ ДОЛЖЕН', 540, 320, 66, INK, WHITE, rot=-3)
            if t >= TT['naznachal'] - 0.7:   # листок «назначение» и красный штамп
                u = eo((t - TT['naznachal'] + 0.7) / 0.35)
                card = card_img(); paste(G, card, 540, 560 - 320 * (1 - u), 1.0, -4 + 4 * u)
                if t >= TT['naznachal'] + 0.25:
                    k = back((t - TT['naznachal'] - 0.25) / 0.25)
                    paste(G, plate_img('НЕ БЫЛО', 70, (0, 0, 0, 0), RED, border=RED), 560, 590, 2.2 - 1.2 * k, 12)
        else:
            plate(G, t, TT['mog'] - 0.15, 'МОГ ПРОСТО УЙТИ', 470, 380, 70, YEL, INK, rot=-3)
    elif L == 3:
        if t < TT['pokazal'] + 0.4:
            if t >= TT['vosmi'] - 0.1:
                u = eo((t - TT['vosmi'] + 0.1) / 0.9); v = int(8_000_000_000 * u)
                paste(G, plate_img(f'{v:,}'.replace(',', ' '), 70, INK, WHITE), 540, 330, back((t - TT['vosmi'] + 0.1) / 0.25), -2)
                plate(G, t, TT['milliardov'] + 0.2, 'ЛЮДЕЙ', 540, 470, 56, LG, INK, rot=3)
        else:
            plate(G, t, TT['pokazal'] + 0.4, 'А ОН ВЫБРАЛ ТЕБЯ', 540, 330, 72, YEL, INK, rot=-3, t1=TT['stroyu'] - 0.6)
    elif L == 4:
        plate(G, t, TT['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 400, 84, YEL, INK, rot=-3, t1=TT['navsegda'] - 0.3)
        plate(G, t, TT['navsegda'] - 0.1, 'НАВСЕГДА?', 400, 360, 76, INK, WHITE, rot=-3)
        plate(G, t, TT['shkaf'] - 0.1, 'КАК ШКАФ', 400, 500, 60, LG, INK, rot=3)
    elif L == 5:
        plate(G, t, TT['podvoh'] - 0.4, 'А ВОТ И ПОДВОХ', 540, 330, 80, YEL, INK, rot=-3, t1=TT['lyubov'] - 0.1)
        plate(G, t, TT['lyubov'] - 0.05, 'ЛЮБОВЬ = ЦВЕТОК', 540, 330, 72, INK, WHITE, rot=-2)
        if t >= TT['polivaesh'] + 0.2: cross(G, 790, 470, 990, 650, clamp((t - TT['polivaesh'] - 0.2) / 0.25))
        plate(G, t, TT['vyanet'] - 0.1, 'ВЯНЕТ', 300, 500, 70, LG, GREY, rot=4)
    elif L == 6:
        plate(G, t, TT['vybrali'] - 0.15, 'ВЫБРАЛИ ЕГО', 540, 330, 80, YEL, INK, rot=-3)
        plate(G, t, TT['kazhdy'] - 0.1, 'КАЖДЫЙ ДЕНЬ', 540, 460, 60, INK, WHITE, rot=2)
    elif L == 7:
        plate(G, t, B[7] + 0.02, 'ОТПРАВЬ ЕМУ', 430, 330, 84, YEL, INK, rot=-3)
        plate(G, t, TT['znaet'] - 0.2, 'ПУСТЬ ЗНАЕТ', 400, 470, 56, INK, WHITE, rot=3)
    elif L == 8:
        plate(G, t, TT['netupi'] - 0.4, 'ВСЁ.\nНЕ ТУПИ', 540, 420, 110, YEL, INK, rot=-4)
@lru_cache(None)
def card_img():
    w, h = S(440), S(300); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=S(16), fill=WHITE, outline=INK, width=S(5))
    d.text((w / 2, S(52)), 'НАЗНАЧЕНИЕ', font=font(44), fill=INK, anchor='mm')
    d.text((S(36), S(118)), 'МУЖ:', font=font(32), fill=GREY)
    for j in range(3): d.line([S(36), S(190 + j * 34), w - S(36), S(190 + j * 34)], fill=LG, width=S(6))
    return im
def graphics(t):
    G = Image.new('RGBA', (WD * SS // 2, HT * SS // 2), (0, 0, 0, 0))
    return G
# плашки рисуем в 2x-слое верхних 1000 px
GH = 1000
def top_layer(t):
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
            d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=YEL if w[1] <= t < w[2] + 0.15 else WHITE)
            d.text((x, y), w[0].upper().strip('«»'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

def zoom(t):
    if TT['stop'] - 0.05 <= t < TT['stop'] + 0.7: return 1 + 0.07 * (1 - eo((t - TT['stop'] + 0.05) / 0.75)), 900
    if TT['pokazal'] + 0.6 <= t < B[4]: return 1 + 0.05 * eo((t - TT['pokazal'] - 0.6) / 0.5), 1000
    return 1.0, 900
def shake(t):
    if TT['stop'] - 0.05 <= t < TT['stop'] + 0.3: return int(10 * math.sin(t * 90)), int(6 * math.cos(t * 70))
    return 0, 0

def frame(i):
    t = i / FPS
    img = Image.new('RGBA', (WD, HT), BG + (255,))
    under(img, t)
    props(img, i, front=False)
    for who in ('muzh', 'zhena'):
        a, s = pos(who, t)
        if a: char(img, who, i, a[0], a[1], s)
    props(img, i, front=True)
    img.alpha_composite(top_layer(t), (0, 0))
    subs(img, t)
    img = img.convert('RGB')
    z, cy = zoom(t)
    if z != 1:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5), int((h - HT) * cy / HT); img = im2.crop((ox, oy, ox + WD, oy + HT))
    dx, dy = shake(t)
    if dx or dy: img = img.transform(img.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), fillcolor=BG)
    return img

if __name__ == '__main__':
    ONLY = sys.argv[1:]
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        for i in range(N):
            p.stdin.write(frame(i).tobytes())
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
