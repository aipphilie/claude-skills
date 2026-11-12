"""Монтаж «Они спят»: фон + графика (PIL, 2x) + персонаж (multiply) + мешки -> ffmpeg."""
import json, math, sys, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageChops
from words import W, wt, B, DUR
from tm import T
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920
GH = 1000; SS = 2   # графика в верхних 1000 px, рисуем в 2x
BG = (247, 245, 240); YEL = (255, 212, 0); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
@lru_cache(None)
def font(sz, black=True): return ImageFont.truetype(FB if black else FX, int(sz * SS))
xoff = json.load(open('xoff.json'))
ONLY = sys.argv[1:]  # для превью: список секунд

def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):  # easeOutBack
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def S(v): return int(round(v * SS))

@lru_cache(None)
def plate_img(text, sz, bg, fg, pad=28, border=None):
    f = font(sz); lines = text.split('\n')
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
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

def plate(G, t, t0, text, cx, cy, sz=64, bg=YEL, fg=INK, rot=0, t1=None, border=None, k=1.0):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28) * k
    a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    paste(G, plate_img(text, int(sz * 1.25), bg, fg, border=border), cx, cy, sc, rot, a)


import random
GREY = (150, 150, 150); LG = (225, 222, 215)
def big_text(G, txt, cx, y, sz, col=INK, black=True):
    d = ImageDraw.Draw(G); f = font(sz, black); bb = d.textbbox((0, 0), txt, font=f)
    d.text((S(cx) - (bb[2] - bb[0]) / 2, S(y)), txt, font=f, fill=col)
def card(G, cx, cy, w, h, fill=WHITE, k=1.0):
    d = ImageDraw.Draw(G); w *= k; h *= k
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(26), fill=fill, outline=INK, width=S(7))
    return d
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))


GREY = (150, 150, 150); LG = (225, 222, 215); MID = (200, 196, 188)
seg_of = json.load(open('seg.json'))
ANCH = None
def anchors():
    global ANCH
    if ANCH is None: ANCH = json.load(open('kadry/main/anchors.json'))
    return ANCH
def big_text(G, txt, cx, y, sz, col=INK, black=True):
    d = ImageDraw.Draw(G); f = font(sz, black); bb = d.textbbox((0, 0), txt, font=f)
    d.text((S(cx) - (bb[2] - bb[0]) / 2, S(y)), txt, font=f, fill=col)
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(16))

# ---------- мешок (рисуется в координатах кадра, 1x, через суперсэмплинг) ----------
@lru_cache(None)
def bag_img(w, text, wings=0):
    """w — ширина мешка в px кадра. Возвращает RGBA (центр мешка = центр картинки)."""
    k = 3; W_ = int(w * k); H_ = int(w * 1.1 * k); pad = int(w * 0.7 * k)
    im = Image.new('RGBA', (W_ + 2 * pad, H_ + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, oy = pad, pad; lw = max(3, int(w * 0.04 * k))
    if wings:
        for sgn in (-1, 1):
            cx = ox + W_ / 2 + sgn * W_ * 0.62; cy = oy + H_ * 0.35 - wings * W_ * 0.12
            d.ellipse([cx - W_ * .32, cy - W_ * .16, cx + W_ * .32, cy + W_ * .16], fill=WHITE, outline=INK, width=lw)
    d.rounded_rectangle((ox + W_ * .30, oy + H_ * .04, ox + W_ * .70, oy + H_ * .26), radius=int(W_ * .08), fill=YEL, outline=INK, width=lw)
    d.rounded_rectangle((ox + W_ * .03, oy + H_ * .22, ox + W_ * .97, oy + H_), radius=int(W_ * .36), fill=YEL, outline=INK, width=lw)
    d.line((ox + W_ * .33, oy + H_ * .22, ox + W_ * .67, oy + H_ * .22), fill=INK, width=lw * 2)
    if text:
        lines = text.split('\n'); sz = int(W_ * 0.3)
        f = ImageFont.truetype(FB, sz)
        while max(d.textlength(t, font=f) for t in lines) > W_ * .78: sz -= 2; f = ImageFont.truetype(FB, sz)
        d.multiline_text((ox + W_ / 2, oy + H_ * .63), text, font=f, fill=INK, anchor='mm', align='center', spacing=int(sz * .1))
    return im.resize((im.width // k, im.height // k), Image.LANCZOS)
def put(img, im, cx, cy, rot=0, scale=1.0):
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)
def bag(img, cx, cy, w, text, rot=0, wings=0, scale=1.0):
    put(img, bag_img(int(w), text, wings), cx, cy, rot, scale)
def walker(img, cx, ground, w, text, t, speed=6.0, carry=None, cw=None):
    """мешок на ножках: шагает на месте. carry — надпись мешка, который он несёт на себе."""
    d = ImageDraw.Draw(img); ph = math.sin(t * speed); lw = max(4, int(w * 0.07)); leg = w * 0.42
    by = ground - leg - w * 0.55 + abs(ph) * w * 0.04
    for sgn, p in ((-1, ph), (1, -ph)):
        x0 = cx + sgn * w * 0.18; d.line([x0, by + w * 0.45, x0 + p * w * 0.16, ground], fill=INK, width=lw)
        d.ellipse([x0 + p * w * 0.16 - lw, ground - lw * 0.8, x0 + p * w * 0.16 + lw * 1.6, ground + lw * 0.6], fill=INK)
    bag(img, cx, by, w, text)
    if carry: bag(img, cx, by - w * 0.95, cw or w * 1.1, carry)

# ---------- новое для «Они спят» ----------
def helmet(img, cx, top, w):
    d = ImageDraw.Draw(img)
    d.chord([cx - w * .36, top - w * .26, cx + w * .36, top + w * .2], 180, 360, fill=WHITE, outline=INK, width=max(3, int(w * .04)))
    d.line([cx - w * .44, top - w * .03, cx + w * .44, top - w * .03], fill=INK, width=max(3, int(w * .05)))
def worker(img, cx, ground, w, text, t, speed=6.0, hat=True):
    walker(img, cx, ground, w, text, t, speed)
    if hat:
        ph = math.sin(t * speed); by = ground - w * 0.42 - w * 0.55 + abs(ph) * w * 0.04
        helmet(img, cx, by - w * 0.5, w)
ZF = ImageFont.truetype(FB, 44)
def zzz(img, x, y, t, k=1.0, seed=0):
    d = ImageDraw.Draw(img)
    for j in range(3):
        u = ((t * 0.6) + j / 3 + seed * 0.17) % 1
        f = ImageFont.truetype(FB, int((26 + 26 * u) * k))
        a = int(255 * (1 - abs(u - 0.5) * 1.6))
        d.text((x + 50 * u * k + 10 * math.sin(u * 6), y - 110 * u * k), 'Z', font=f, fill=(GREY[0], GREY[1], GREY[2]))
SOFA_X = 720
def sofa(img, cx=SOFA_X, ground=None, label='КАРТА'):
    ground = ground or FEET; d = ImageDraw.Draw(img); w = 400
    x0, x1 = cx - w / 2, cx + w / 2
    d.rounded_rectangle([x0 + 20, ground - 230, x1 - 20, ground - 90], radius=30, fill=MID, outline=INK, width=7)   # спинка
    d.rounded_rectangle([x0 + 20, ground - 120, x1 - 20, ground - 40], radius=18, fill=LG, outline=INK, width=7)    # сиденье
    for sx in (x0, x1 - 60):
        d.rounded_rectangle([sx, ground - 160, sx + 60, ground - 30], radius=24, fill=MID, outline=INK, width=7)  # подлокотники
    for lx in (x0 + 40, x1 - 50):
        d.rectangle([lx, ground - 32, lx + 12, ground], fill=INK)
    if label:
        im = plate_img(label, 40, WHITE, INK, pad=16, border=INK)
        put(img, im.resize((im.width // SS, im.height // SS), Image.LANCZOS), cx, ground - 72)
    return ground - 120   # верх сиденья
def sleeping_bags(img, t, n=3, k=1.0, shrink=1.0, cx=SOFA_X):
    seat = FEET - 120
    xs = [cx - 110, cx + 5, cx + 115][:n] if n > 1 else [cx]
    for j, x in enumerate(xs):
        br = math.sin(t * 2.2 + j) * 0.03
        w = 105 * k * (shrink if j == 0 or n == 1 else 1)
        bag(img, x, seat - w * 0.5, w * (1 + br), '₽', rot=(-12, 8, -6)[j])
        zzz(img, x + 20, seat - w * 1.1, t, 0.9, j)
def card60(img, cx, cy, text, k=1.0):
    if k <= 0.05: return
    im = plate_img(text, 64, WHITE, INK, pad=26, border=INK)
    put(img, im.resize((max(1, int(im.width / SS * k)), max(1, int(im.height / SS * k))), Image.LANCZOS), cx, cy)
def house(img, cx, base, w, k=1.0):
    if k <= 0.05: return
    d = ImageDraw.Draw(img); w *= k
    d.rectangle([cx - w / 2, base - w * .7, cx + w / 2, base], fill=WHITE, outline=INK, width=7)
    d.polygon([(cx - w * .62, base - w * .66), (cx, base - w * 1.15), (cx + w * .62, base - w * .66)], fill=INK)
    d.rectangle([cx - w * .12, base - w * .36, cx + w * .12, base], fill=YEL, outline=INK, width=5)
def jar(img, jx, ground, fill):
    d = ImageDraw.Draw(img); jw, jh = 150, 210
    d.rounded_rectangle([jx - jw / 2, ground - jh, jx + jw / 2, ground], radius=24, fill=WHITE, outline=INK, width=7)
    lvl = jh * (0.08 + 0.75 * fill)
    d.rounded_rectangle([jx - jw / 2 + 9, ground - lvl, jx + jw / 2 - 9, ground - 9], radius=16, fill=YEL)
    d.rounded_rectangle([jx - jw / 2 - 10, ground - jh - 22, jx + jw / 2 + 10, ground - jh + 4], radius=8, fill=INK)
def clock(img, cx, cy, r, t, ring=True):
    d = ImageDraw.Draw(img); sh = 7 * math.sin(t * 70) if ring else 0
    cx += sh
    for sgn in (-1, 1):
        d.ellipse([cx + sgn * r * .75 - r * .32, cy - r * 1.05 - r * .32, cx + sgn * r * .75 + r * .32, cy - r * 1.05 + r * .32], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=9)
    d.line([cx, cy, cx, cy - r * .62], fill=INK, width=8); d.line([cx, cy, cx + r * .45, cy], fill=RED, width=8)
    for sgn in (-1, 1):
        d.line([cx + sgn * r * 1.15, cy - r * .9, cx + sgn * r * 1.45, cy - r * 1.2], fill=INK, width=6)
def lying(img, cx, seat, t):
    """человечек спит на диване (плоский силуэт)."""
    d = ImageDraw.Draw(img); br = 3 * math.sin(t * 2.0)
    d.rounded_rectangle([cx - 150, seat - 78 - br, cx + 175, seat + 4], radius=40, fill=INK)
    d.ellipse([cx - 245, seat - 128 - br, cx - 120, seat - 3 - br], fill=INK)
    d.arc([cx - 215, seat - 85 - br, cx - 160, seat - 45 - br], 20, 160, fill=WHITE, width=6)
    zzz(img, cx - 170, seat - 150, t, 1.2)

# ---------- сцены в графике G (верхние 1000 px, 2x) ----------
def sc_riddle(G, t):
    plate(G, t, 0.05, 'ЗАГАДКА', 540, 90, 84, YEL, INK, rot=-3)
def sc_q(G, t):
    plate(G, t, B[1] + 0.05, 'КАК ЗАСТАВИТЬ\nИХ РАБОТАТЬ?', 540, 120, 74, INK, WHITE, rot=-2)
    plate(G, t, T['otvet'] - 0.05, 'ОТВЕТ В КОНЦЕ', 540, 860, 60, YEL, INK, rot=3)
def sc_false(G, t):
    plate(G, t, T['dumaesh'], 'С ТАКОЙ ЗП\nНЕ НАКОПИШЬ?', 540, 320, 84, LG, GREY, rot=-3)
def sc_stop(G, t):
    plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 220, 84, YEL, INK, rot=-3)
    paste(G, plate_img('НЕ НАКОПИШЬ?', 64, LG, GREY, pad=22), 540, 450, 1.0, -3)
    cross(G, 230, 390, 850, 510, clamp((t - T['stop'] - 0.4) / 0.3))
    plate(G, t, T['dengi'] - 0.05, 'ДЕНЬГИ ЕСТЬ', 540, 640, 70, INK, WHITE, rot=2)
def sc_sleep(G, t):
    plate(G, t, B[4] + 0.05, 'ОНИ СПЯТ', 540, 110, 100, YEL, INK, rot=-3)
    plate(G, t, T['karte'] - 0.05, 'НА КАРТЕ: +0 ₽', 620, 330, 64, INK, WHITE, rot=2)
def sc_step1(G, t):
    plate(G, t, B[5] + 0.05, '1. СЕБЕ ПЕРВОМУ', 540, 80, 76, YEL, INK, rot=-2)
    plate(G, t, T['avto'] - 0.05, 'АВТОПЕРЕВОД', 320, 300, 62, INK, WHITE, rot=-3, t1=T['do'] - 0.1)
    plate(G, t, T['do'] - 0.05, 'ДО ТРАТ', 300, 300, 80, YEL, INK, rot=3)
    plate(G, t, T['ostanetsya'] - 0.1, 'А НЕ ОСТАТКИ', 300, 470, 56, LG, GREY, rot=-2)
def sc_step2(G, t):
    plate(G, t, B[6] + 0.05, '2. РАЗБУДИ', 540, 80, 86, YEL, INK, rot=-2)
DOORS = (('НАКОПИТЕЛЬНЫЙ\nСЧЁТ', 'подушка', 'nakop'), ('ОБЛИГАЦИИ\nИ ФОНДЫ', 'надолго', 'oblig'), ('ИИС', '+13% от государства', 'iis'))
def sc_where(G, t):
    plate(G, t, B[7] - 0.2, '2. РАЗБУДИ', 540, 30, 60, YEL, INK, rot=-2, k=0.8)
    for j, (lab, sub, key) in enumerate(DOORS):
        k = back((t - T[key] + 0.1) / 0.3)
        if k <= 0.05: continue
        y = 245 + j * 285
        paste(G, plate_img(lab, 70, WHITE, INK, pad=24, border=INK), 640, y - 20, k, (-2, 2, -1)[j])
        paste(G, plate_img(sub, 50, YEL if j == 2 else LG, INK, pad=16), 640, y + (112 if j < 2 else 72), k, (2, -2, 1)[j])
def sc_step3(G, t):
    plate(G, t, B[8] + 0.05, '3. НЕ ТРОГАЙ', 540, 80, 86, YEL, INK, rot=-2)
    plate(G, t, T['pust'] - 0.05, 'ПУСТЬ ТАСКАЮТ', 540, 260, 70, INK, WHITE, rot=3)
def sc_twist(G, t):
    plate(G, t, T['podvoh'] - 0.4, 'А ВОТ И ПОДВОХ', 540, 220, 92, YEL, INK, rot=-3)
def sc_infl(G, t):
    plate(G, t, T['ceny'] - 0.05, 'ЦЕНЫ РАСТУТ', 380, 90, 70, INK, WHITE, rot=-3)
    plate(G, t, T['hudeyut'] - 0.1, 'МЕШКИ ХУДЕЮТ', 620, 260, 76, YEL, INK, rot=3)
def counter(G, t, lab, val, t0, t1, cy, col=WHITE):
    u = eo((t - t0) / max(0.3, t1 - t0)); v = int(round(val * u / 1000)) * 1000
    paste(G, plate_img(f'{lab}\n{v:,} ₽'.replace(',', ' '), 60, col, INK, pad=24, border=INK), 640, cy, back((t - t0 + 0.2) / 0.3))
def sc_answer(G, t):
    plate(G, t, B[11] + 0.05, 'ОТВЕТ', 540, 70, 96, YEL, INK, rot=-3)
    if t >= T['otlozhish'] - 0.3: counter(G, t, 'ТЫ ОТЛОЖИЛ ЗА 5 ЛЕТ', 360000, T['otlozhish'] - 0.1, T['trista'] + 0.9, 300)
    if t >= B[12]: counter(G, t, 'ПРИТАЩИЛИ МЕШКИ', 130000, T['pritashat'], T['sta'] + 0.6, 540, YEL)
    if t >= B[13]: counter(G, t, 'ВЕРНЁТ ГОСУДАРСТВО', 47000, T['pyatdesyat'] - 0.2, T['gosudarstvo2'] + 0.4, 780, YEL)
def sc_thirty(G, t):
    plate(G, t, T['tridcat'] - 0.1, '≈ 30 МЕШКОВ', 540, 120, 100, YEL, INK, rot=-3)
    plate(G, t, T['nes'] - 0.5, 'КОТОРЫЕ ТЫ НЕ НЁС', 540, 320, 64, INK, WHITE, rot=2)
def sc_ring(G, t):
    plate(G, t, T['spish'] - 0.2, 'ТЕПЕРЬ СПИШЬ ТЫ', 540, 90, 80, INK, WHITE, rot=-3)
    plate(G, t, T['rabotayut'] - 0.2, 'ОНИ РАБОТАЮТ', 540, 280, 92, YEL, INK, rot=3)
def sc_final(G, t):
    plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 300, 110, YEL, INK, rot=-4)
SCENES = [sc_riddle, sc_q, sc_false, sc_stop, sc_sleep, sc_step1, sc_step2, sc_where, sc_step3, sc_twist, sc_infl,
          sc_answer, sc_answer, sc_answer, sc_thirty, sc_ring, sc_final]
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)
def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    SCENES[line_of(t)](G, t)
    return G.resize((WD, GH), Image.LANCZOS)

# субтитры (как в «Миллионе»), И-И-С показываем как ИИС
SUBF = ImageFont.truetype(FB, 56); SP = 14; MAXW = 780
W = [(w[0].replace('И-И-С', 'ИИС'), w[1], w[2]) for w in W]
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
def subs(img, t, y0):
    g = next((g for i, g in enumerate(groups) if g[0][1] - 0.05 <= t < (groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else g[-1][2] + 0.4)), None)
    if not g: return
    d = ImageDraw.Draw(img); lines = wrap(g)
    y = y0 if len(lines) == 1 else y0 - 37
    for ln in lines:
        ws = [wlen(w) for w in ln]; x = (WD - (sum(ws) + SP * (len(ws) - 1))) / 2
        for w, wd in zip(ln, ws):
            if w[1] <= t < w[2] + 0.15: d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=YEL)
            d.text((x, y), w[0].upper().strip('«»'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

# плашка «не рекомендация»
DF = ImageFont.truetype(FX, 25)
def disclaimer(img, t):
    L = line_of(t)
    lines = []; a = 1.0
    if t < 5.3: lines = ['Не является индивидуальной инвестиционной рекомендацией']; a = 1 - clamp((t - 5.0) / 0.3)   # первые 5 сек, потом гаснет
    if 11 <= L <= 14: lines = ['Расчёт условный: 12% годовых. Доходность не гарантирована.']
    if not lines or a <= 0: return
    ov = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    y = 1528 - 32 * len(lines)
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=DF); w = bb[2] - bb[0]
        d.rounded_rectangle([(WD - w) / 2 - 12, y - 3, (WD + w) / 2 + 12, y + 29], radius=8, fill=(255, 255, 255, int(190 * a)))
        d.text(((WD - w) / 2, y), ln, font=DF, fill=(110, 110, 110, int(255 * a))); y += 32
    img.paste(ov, (0, 0), ov)

CH_CROP = (0, 60, 1080, 1660)
SUB_Y = 1365; FEET = 1290
DEF = (540, FEET, 0.45, 190, 0.72); LEFT = (250, FEET, 0.45, 190, 0.72); RIGHT = (850, FEET, 0.42, 190, 0.72)
LAY = [(B[0], *LEFT), (B[2], *DEF), (B[4], *LEFT), (B[5], *RIGHT), (B[6], *LEFT), (B[8], *DEF), (B[10], *LEFT), (B[11], 230, FEET, 0.42, 190, 0.72),
       (B[14], 820, FEET, 0.42, 190, 0.72), (B[15], *LEFT), (B[16], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]
def zoom(t):
    for ta, tb in ((T['spyat'] - 0.6, T['karte'] - 0.1), (T['tridcat'], B[15])):
        if ta <= t < tb: return 1 + 0.06 * eo((t - ta) / 0.25)
    return 1.0
def gx(x): return 151 + x * 0.72
def gy_(y): return 190 + y * 0.72
def char_box(i, cx, feet, s):
    bot = feet + 70 * s; cw, chh = int(1080 * s), int(1600 * s)
    return int(cx - cw / 2 + xoff[i]), int(bot - chh), cw, chh

def under(img, i, t):
    L = line_of(t); d = ImageDraw.Draw(img)
    if L == 0:
        k = back((t - T['zarplata'] + 0.1) / 0.35)
        card60(img, 700, 860, '60 000 ₽', k)
        if t >= T['dvadcat'] - 0.15:
            kh = back((t - T['dvadcat'] + 0.15) / 0.35); house(img, 700, FEET - 40, 230, kh)
            plate_k = back((t - T['kvart']) / 0.3)
            if plate_k > 0.05: card60(img, 700, 1040, '−20 000 ₽', plate_k * 0.8)
    elif L == 1:
        card60(img, 690, 860, '60 000 ₽', 0.7); card60(img, 690, 960, '−20 000 ₽', 0.6)
        u = back((t - B[1]) / 0.35); card60(img, 690, 1120, '= 40 000 ₽', 1.1 * u)
    elif L in (4,):
        sofa(img); sleeping_bags(img, t, k=back((t - B[4]) / 0.35))
    elif L == 5:
        card60(img, 260, 760, '60 000 ₽', back((t - B[5]) / 0.35))
        f = clamp((t - T['zaplati']) / 1.0) * 0.3 + clamp((t - T['storonu']) / 0.8) * 0.5
        jar(img, 300, FEET, f)
        if T['shest6'] - 0.1 <= t:
            u = eo((t - T['shest6'] + 0.1) / 0.9)
            if u < 1: bag(img, 260 + 40 * u, 820 + (FEET - 200 - 820) * u - 140 * math.sin(math.pi * u), 120, '6 000')
            elif t < B[6]: bag(img, 300, FEET - 280, 90, '6 000')
    elif L == 6:
        sofa(img)
        rise = clamp((t - T['razbudi'] + 0.1) / 0.5)
        if rise <= 0: sleeping_bags(img, t)
        else:
            for j, x in enumerate((SOFA_X - 110, SOFA_X + 5, SOFA_X + 115)):
                walker(img, x, FEET - 120 - 120 * math.sin(math.pi * min(1, rise)) * 0.6, 100, '₽', t * (1 + j * 0.1), speed=12)
        clock(img, 760, 620, 80, t, ring=t >= B[6] + 0.1)
    elif L == 7:
        for j, (lab, sub, key) in enumerate(DOORS):
            if t < T[key] - 0.1: continue
            y = gy_(245 + j * 285) + 30; u = clamp((t - T[key] + 0.1) / 0.6)
            worker(img, 1010 - 130 * u, y + 40, 70, '', t + j, speed=10, hat=False)
    elif L == 8:
        for j in range(3):
            x = 660 + j * 130 + max(0, t - T['trogay']) * 260
            if x < 1000: worker(img, x, FEET, 100, '₽', t + j * 0.5, speed=10)
    elif L == 10:
        sofa(img)
        sh = 1 - 0.45 * clamp((t - T['ceny']) / max(0.5, T['hudeyut'] + 0.6 - T['ceny']))
        sleeping_bags(img, t, n=1, k=1.5, shrink=sh)
        for j, (x, y) in enumerate(((560, 760), (760, 700), (880, 860))):
            tk = T['ceny'] + j * 0.35
            if t >= tk:
                u = eo((t - tk) / 0.6)
                card60(img, x, y - 60 * u, '₽ ↑', 0.7 * back((t - tk) / 0.3))
    elif L == 11:
        for j in range(min(10, int(max(0, t - T['otlozhish'] + 0.2) * 7))):
            bag(img, 470, FEET - 40 - j * 34, 80, '6 000')
    elif L == 12:
        for j in range(10): bag(img, 470, FEET - 40 - j * 34, 80, '6 000')
        u = eo((t - B[12]) / 1.2)
        for j in range(3): worker(img, 1100 - 560 * u + j * 110, FEET, 90, '₽', t + j * 0.4, speed=10)
    elif L == 13:
        for j in range(10): bag(img, 470, FEET - 40 - j * 34, 80, '6 000')
        for j in range(3): worker(img, 540 + j * 110, FEET, 90, '₽', t + j * 0.4, speed=6)
        if t >= T['pyatdesyat'] - 0.4:
            u = eo((t - T['pyatdesyat'] + 0.4) / 0.6)
            bag(img, 720, -120 + (FEET - 330 + 120) * u, 150, 'ВЫЧЕТ')
    elif L == 14:
        k = back((t - B[14]) / 0.35)
        for r in range(3):
            for j in range(10):
                if r * 10 + j >= 29: break
                x = 60 + j * 62 + r * 22; g = FEET - 150 + r * 75
                if k > 0.1: walker(img, x, g, 52 * min(1, k), '', t + j * 0.37 + r, speed=9)
    elif L == 15:
        seat = sofa(img, cx=SOFA_X - 140); lying(img, SOFA_X - 140, seat, t)
        for j in range(3):
            x = 720 + ((t - B[15]) * 160 + j * 120) % 420
            worker(img, x, FEET + 20, 70, '₽', t + j * 0.5, speed=10)

def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    cx, feet, s, gy, gs = layout(t); L = line_of(t)
    under(bg, i, t)
    G = graphics(t)
    if gs != 1: G = G.resize((int(WD * gs), int(GH * gs)), Image.LANCZOS)
    bg.paste(G, (int((WD - G.width) / 2), int(gy)), G)
    subs(bg, t, SUB_Y)
    if L != 15:
        x0, y0, cw, chh = char_box(i, cx, feet, s)
        ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
        layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (x0, y0))
        img = (np.asarray(bg, np.float32) * np.asarray(layer, np.float32) / 255)
        img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    else: img = bg
    z = zoom(t)
    if z != 1:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5), int((h - HT) * 900 / HT); img = im2.crop((ox, oy, ox + WD, oy + HT))
    disclaimer(img, t)
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
