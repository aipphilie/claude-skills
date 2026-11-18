"""Монтаж «Первый миллион»: фон + графика (PIL, 2x) + персонаж (multiply) + мешки -> ffmpeg."""
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

# ---------- гора ----------
SL0 = (-60, 1400); SUM = (640, 900)
def slope_y(x): return SL0[1] + (x - SL0[0]) * (SUM[1] - SL0[1]) / (SUM[0] - SL0[0])
def mountain(img, pan=0.0, plateau=True):
    d = ImageDraw.Draw(img)
    pts = [(SL0[0] - pan, SL0[1]), (SUM[0] - pan, SUM[1])]
    if plateau: pts.append((WD + 3000, SUM[1]))
    poly = pts + [(pts[-1][0], HT), (pts[0][0], HT)]
    d.polygon(poly, fill=LG); d.line(pts, fill=INK, width=8, joint='curve')

# ---------- сцены (графика G в верхних 1000 px) ----------
def sc_intro(G, t):
    if t >= B[1]:
        plate(G, t, T['legche'], 'ВСЁ ЛЕГЧЕ', 540, 110, 80, YEL, INK, rot=-3, t1=T['pochemu'] - 0.1)
        plate(G, t, T['pochemu'] - 0.05, 'ПОЧЕМУ?', 540, 110, 96, INK, WHITE, rot=2)
def sc_luck(G, t):
    plate(G, t, T['dumaesh'] + 0.1, 'ВЕЗЕНИЕ?', 290, 230, 72, LG, GREY, rot=-4)
    plate(G, t, T['bogatym'], 'БОГАТЫМ\nВСЁ ДАЮТ?', 790, 420, 64, LG, GREY, rot=4)
def sc_stop(G, t):
    plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 260, 84, YEL, INK, rot=-3)
    paste(G, plate_img('ВЕЗЕНИЕ?', 64, LG, GREY, pad=22), 290, 620, 1.0, -4)
    paste(G, plate_img('БОГАТЫМ ДАЮТ?', 64, LG, GREY, pad=22), 760, 680, 1.0, 4)
    cross(G, 90, 570, 1000, 740, clamp((t - T['stop'] - 0.4) / 0.3))
def sc_strong(G, t):
    plate(G, t, B[4] + 0.05, 'ГРУЗ ТОТ ЖЕ', 540, 90, 70, INK, WHITE, rot=-2)
    if t >= T['silnee'] - 0.1:
        plate(G, t, T['silnee'] - 0.1, 'СИЛЬНЕЕ ТЫ', 540, 250, 92, YEL, INK, rot=3)
BARS = (('ЗАРАБАТЫВАТЬ', 'zarab'), ('УДЕРЖИВАТЬ', 'uderzh'), ('НЕ БОЯТЬСЯ', 'boyatsya'))
def bars(G, t, y0=80):
    d = ImageDraw.Draw(G)
    for j, (lab, key) in enumerate(BARS):
        k = back((t - T['tri'] - j * 0.15) / 0.3)
        if k <= 0.1: continue
        y = y0 + j * 118
        im = Image.new('RGBA', (S(1000), S(100)), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        hl = t >= T[key] and (j == 2 or t < T[BARS[j + 1][1]])
        dd.text((S(0), S(8)), lab, font=font(60), fill=INK if t >= T[key] else GREY)
        dd.rounded_rectangle([S(560), S(14), S(990), S(80)], radius=S(33), fill=WHITE, outline=INK, width=S(7))
        u = eo((t - T[key]) / 0.9) if t >= T[key] else 0
        if u > 0.02: dd.rounded_rectangle([S(569), S(23), S(569 + 412 * u), S(71)], radius=S(26), fill=YEL)
        if hl: dd.rounded_rectangle([S(0), S(88), S(540), S(96)], radius=S(3), fill=INK)
        paste(G, im, 540, y, k)
def sc_muscles(G, t):
    if t < T['tri'] - 0.1:
        plate(G, t, T['nas'], 'НАС ЭТОМУ\nНЕ УЧИЛИ', 560, 200, 80, INK, WHITE, rot=-3)
        return
    bars(G, t)
    if B[6] <= t < B[7]:   # зарабатывать: работа дорожает
        d = ImageDraw.Draw(G); k = back((t - T['zarab'] - 0.3) / 0.3)
        if k > 0.1:
            paste(G, plate_img('ТВОЯ РАБОТА', 62, WHITE, INK, pad=22, border=INK), 760, 490, k, -3)
            u = eo((t - T['dorozhe'] + 0.6) / 0.5)
            if u > 0:
                x = 760; yb = 860; yt = 860 - 260 * u
                d.line([S(x), S(yb), S(x), S(yt + 50)], fill=YEL, width=S(44))
                d.polygon([(S(x - 80), S(yt + 70)), (S(x), S(yt - 20)), (S(x + 80), S(yt + 70))], fill=YEL, outline=INK, width=S(6))
            plate(G, t, T['dorozhe'] + 0.1, 'ДОРОЖЕ', 760, 900, 80, INK, WHITE, rot=3)
    elif B[7] <= t < B[8]:  # удерживать: утечки
        plate(G, t, T['utekat'] - 0.2, 'ЕРУНДА', 760, 905, 60, LG, GREY, rot=-2, t1=T['erundu'] + 0.35)
        if t >= T['erundu'] + 0.4: plate(G, t, T['erundu'] + 0.4, 'НЕ УТЕКАЕТ', 760, 760, 64, INK, WHITE, rot=3)
    elif B[8] <= t < B[9]:  # не бояться: цифра перестаёт пугать
        u = clamp((t - T['summa']) / max(0.5, T['cifroy'] - T['summa']))
        if t >= T['summa'] - 0.2:
            sh = 16 * (1 - u) * math.sin(t * 60); sz = 130 - 60 * eo(u)
            big_text(G, '1 000 000 ₽', 590 + sh, 520 + 60 * eo(u) + sh * 0.5, sz, INK if u < 1 else GREY)
        plate(G, t, T['cifroy'], 'ПРОСТО ЦИФРА', 710, 800, 76, YEL, INK, rot=-3)
def sc_twist(G, t):
    plate(G, t, T['podvoh'] - 0.4, 'А ВОТ И ПОДВОХ', 540, 180, 92, YEL, INK, rot=-3)
def sc_sky(G, t):
    plate(G, t, B[10] + 0.05, 'С НЕБА', 300, 80, 62, INK, WHITE, rot=-3)
    plate(G, t, T['myshc'] - 0.2, 'БЕЗ МЫШЦ', 760, 80, 62, LG, GREY, rot=3)
def sc_why(G, t):
    plate(G, t, B[11] + 0.05, 'ПОЧЕМУ ДАЛЬШЕ\nБЫСТРЕЕ?', 540, 220, 78, YEL, INK, rot=-3)
def sc_two(G, t):
    plate(G, t, T['odin'] - 0.3, 'ОДИН', 540, 90, 76, INK, WHITE, rot=-3, t1=T['vtoroy2'] - 0.05)
    plate(G, t, T['vdvoem'] - 0.1, 'ВДВОЁМ', 540, 90, 86, YEL, INK, rot=3)
def sc_invest(G, t):
    plate(G, t, T['vlozhen'] - 0.2, 'ВЛОЖЕН', 400, 90, 70, INK, WHITE, rot=-3)
    plate(G, t, T['prinosit'], 'ПРИНОСИТ ДЕНЬГИ', 600, 250, 62, YEL, INK, rot=2)
def sc_ten(G, t):
    plate(G, t, T['desyatyy'] - 0.1, 'ДЕСЯТЫЙ', 330, 80, 70, INK, WHITE, rot=-3)
    plate(G, t, T['tashat'] - 0.1, 'ТАЩАТ ДЕВЯТЬ', 650, 230, 70, YEL, INK, rot=3)
def sc_do(G, t):
    if t < T['gonis'] - 0.15:
        plate(G, t, T['delat'] - 0.6, 'И ЧТО С ЭТИМ\nДЕЛАТЬ?', 540, 220, 84, YEL, INK, rot=-3); return
    big_text(G, '1 000 000 ₽', 540, 10, 80, GREY)
    cross(G, 250, 20, 830, 120, clamp((t - T['gonis'] - 0.1) / 0.3))
    plate(G, t, T['gonis'] - 0.1, 'НЕ ГОНИСЬ ЗА ЦИФРОЙ', 540, 235, 60, INK, WHITE, rot=-2)
    for j, (lab, key) in enumerate((('ДОХОД', 'dohod'), ('ОТКЛАДЫВАТЬ', 'otkl'), ('ВЛОЖЕНИЯ', 'vlozh'))):
        plate(G, t, T[key] - 0.05, lab, (290, 760, 520)[j], (400, 470, 610)[j], 70, YEL, INK, rot=(-4, 4, -2)[j])
def sc_ring(G, t):
    plate(G, t, T['gora'] - 0.1, 'ГОРА ТА ЖЕ', 540, 90, 76, INK, WHITE, rot=-3)
    plate(G, t, T['drugoy'] - 0.1, 'ТЫ ДРУГОЙ', 540, 250, 96, YEL, INK, rot=3)
def sc_final(G, t):
    plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 300, 110, YEL, INK, rot=-4)

SCENES = [sc_intro, sc_intro, sc_luck, sc_stop, sc_strong, sc_muscles, sc_muscles, sc_muscles, sc_muscles, sc_twist, sc_sky, sc_why,
          sc_two, sc_invest, sc_ten, sc_do, sc_ring, sc_final]
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)
def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    SCENES[line_of(t)](G, t)
    return G.resize((WD, GH), Image.LANCZOS)
# субтитры: до двух строк, каждая не шире MAXW; группа рвётся на конце фразы
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
def subs(img, t, y0=905):
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


CH_CROP = (0, 60, 1080, 1660)
SUB_Y = 1410; FEET = 1335
DEF = (540, FEET, 0.45, 190, 0.72); LEFT = (270, FEET, 0.5, 190, 0.72); RIGHT = (850, FEET, 0.42, 190, 0.72)
LAY = [(B[2], *DEF), (B[4], *LEFT), (B[9], *DEF), (B[10], *LEFT), (B[11], *DEF), (B[12], 290, FEET, 0.47, 190, 0.72),
       (B[14], 220, FEET, 0.42, 190, 0.72), (B[15], *DEF), (B[17], *DEF)]
T_DROP = T['dalshe'] - 0.25; T_WALK = T['vtoroy'] - 0.1; PAN_V = 260
def pan(t): return max(0.0, t - T_WALK) * PAN_V
def layout(t):
    L = line_of(t)
    if L <= 1:   # подъём в гору, потом плато
        cx = 210 + 430 * (t / T_DROP) ** 0.9 if t < T_DROP else SUM[0]
        return (cx, slope_y(cx) if cx < SUM[0] else SUM[1], 0.36, 190, 0.72)
    if L == 16:
        u = clamp((t - B[16]) / (B[17] - B[16] - 0.2)); cx = 120 + 470 * u
        return (cx, slope_y(cx), 0.36, 190, 0.72)
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    out = tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]
    if L == 4:   # «сильнее становишься ты» — человечек растёт
        g = 1 + 0.18 * back((t - T['silnee']) / 0.4) if t >= T['silnee'] else 1
        out = (out[0], out[1], out[2] * g) + out[3:]
    return out
def zoom(t):
    for ta, tb in ((T['silnee'], B[5]), (T['desyatyy'], B[15])):
        if ta <= t < tb: return 1 + 0.06 * eo((t - ta) / 0.25)
    return 1.0

def char_box(i, cx, feet, s):
    bot = feet + 70 * s; cw, chh = int(1080 * s), int(1600 * s)
    return int(cx - cw / 2 + xoff[i]), int(bot - chh), cw, chh
def back_pt(i, cx, feet, s):
    x0, y0, cw, chh = char_box(i, cx, feet, s); a = anchors()[i]
    return x0 + a['back'][0] * s, y0 + (a['back'][1] - 60) * s, x0 + a['top'][0] * s, y0 + (a['top'][1] - 60) * s

def under(img, i, t, cx, feet, s):
    """всё, что под персонажем (фон кадра): гора, мешки, мешки на ножках."""
    L = line_of(t)
    if L <= 1:
        p = pan(t); mountain(img, p)
        if t >= T_DROP:   # сброшенный первый мешок лежит на склоне
            u = eo((t - T_DROP) / 0.3); x = 480 - p; y = slope_y(480) - 110
            bag(img, x, y - 60 * (1 - u), 270, '1 000 000 ₽', rot=14 * u)
        for j, (key, lab, w) in enumerate((('vtoroy', '2 МЛН', 160), ('tretiy', '3 МЛН', 140), (None, '4 МЛН', 122), ('pyatyy', '5 МЛН', 106))):
            tk = T[key] if key else (T['tretiy'] + T['pyatyy']) / 2
            if t < tk - 0.15: continue
            u = eo((t - tk + 0.15) / 0.25); wx = SUM[0] + pan(tk) + 250 + j * 75
            bag(img, wx - p, SUM[1] - w * 0.48 - 500 * (1 - u), w, lab)
    elif L == 16:
        mountain(img, 0, plateau=True)
    elif L == 4:
        k = back((t - B[4]) / 0.3)
        if k > 0.1: bag(img, 760, FEET - 140, 280, '1 000 000 ₽', scale=k)
    elif L == 7:   # удерживать: из мешка утекают монетки
        k = back((t - T['uderzh'] + 0.1) / 0.3)
        if k > 0.1: bag(img, 700, 560, 190, '', scale=k)
        if T['uderzh'] <= t < T['erundu'] + 0.4:
            d = ImageDraw.Draw(img)
            for j in range(5):
                u = ((t - T['uderzh']) * 1.5 + j / 5) % 1
                d.ellipse([688 - 22, 660 + 160 * u - 22, 688 + 22, 660 + 160 * u + 22], fill=YEL, outline=INK, width=5)
    elif L == 10:   # миллион с неба у серого человечка без мышц
        d = ImageDraw.Draw(img); gx = 800
        d.rounded_rectangle([gx - 55, FEET - 330, gx + 55, FEET], radius=55, fill=MID)
        d.ellipse([gx - 62, FEET - 450, gx + 62, FEET - 326], fill=MID)
        for j in range(3):
            d.rounded_rectangle([gx - 70, FEET - 560 + j * 34, gx + 70, FEET - 538 + j * 34], radius=11, fill=WHITE, outline=GREY, width=4)
        u = eo((t - T['svalilsya'] + 0.2) / 0.5)
        if t >= T['svalilsya'] - 0.2:
            if t < T['uletaet'] - 0.3:
                bag(img, 620, -150 + (FEET - 110 + 150) * u, 200, '1 000 000 ₽')
            else:
                f = clamp((t - T['uletaet'] + 0.3) / 1.4); fl = 0.5 + 0.5 * math.sin(t * 30)
                bag(img, 620 + 380 * f * f, FEET - 110 - 1000 * f * f, 200, '1 000 000 ₽', rot=-10 * f, wings=fl)
    elif L == 12:
        if t >= T['vtoroy2'] - 0.1:
            k = back((t - T['vtoroy2'] + 0.1) / 0.3)
            if k > 0.1: walker(img, 730, FEET, 210 * k, '1 МЛН', t)
    elif L == 13:
        walker(img, 640, FEET, 200, '1 МЛН', t)
        d = ImageDraw.Draw(img); jx = 860; grow = clamp((t - T['vlozhen']) / (B[14] - T['vlozhen']))
        jw = 110 + 50 * grow; jh = 150 + 90 * grow
        d.rounded_rectangle([jx - jw / 2, FEET - jh, jx + jw / 2, FEET], radius=24, fill=WHITE, outline=INK, width=7)
        lvl = jh * (0.15 + 0.6 * grow)
        d.rounded_rectangle([jx - jw / 2 + 8, FEET - lvl, jx + jw / 2 - 8, FEET - 8], radius=16, fill=YEL)
        if t >= T['vlozhen']:
            for j in range(3):
                u = ((t - T['vlozhen']) * 1.4 + j / 3) % 1
                x = 690 + (jx - 690) * u; y = FEET - 300 - 160 * math.sin(math.pi * u) + (300 - jh + 40) * u
                d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=YEL, outline=INK, width=5)
    elif L == 14:
        k = back((t - B[14]) / 0.35)
        if k > 0.1:
            for j in range(9):
                walker(img, 400 + j * 62, FEET, 58 * k, '', t + j * 0.4, speed=9)
            if k > 0.6: bag(img, 648, FEET - 58 * 1.6 - 170, 340 * min(1, k), '10 МЛН')

def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    cx, feet, s, gy, gs = layout(t); L = line_of(t)
    under(bg, i, t, cx, feet, s)
    G = graphics(t)
    if gs != 1: G = G.resize((int(WD * gs), int(GH * gs)), Image.LANCZOS)
    bg.paste(G, (int((WD - G.width) / 2), int(gy)), G)
    # мешок на спине (под персонажем, руки поверх)
    lab = None
    if L == 0 or (L == 1 and t < T_DROP): lab, bw = '1 000 000 ₽', 760 * s
    elif L == 12: lab, bw = ('1 МЛН' if t < T['vtoroy2'] - 0.05 else '2 МЛН'), 400 * s
    elif L == 16: lab, bw = '10 МЛН', 760 * s
    if lab:
        bx, by, hx, hy = back_pt(i, cx, feet, s)
        bag(bg, bx - bw * 0.62, by - bw * 0.02, bw, lab, rot=8 if L == 0 else 0)
    subs(bg, t, 1440 if L in (0, 1, 16) else SUB_Y)
    x0, y0, cw, chh = char_box(i, cx, feet, s)
    ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (x0, y0))
    img = (np.asarray(bg, np.float32) * np.asarray(layer, np.float32) / 255)
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if L == 0:   # капли пота
        bx, by, hx, hy = back_pt(i, cx, feet, s); d = ImageDraw.Draw(img)
        for j in range(2):
            u = ((t * 1.3) + j * 0.5) % 1
            x = hx + 30 + 50 * u; y = hy + 10 - 40 * math.sin(math.pi * u) + 60 * u
            d.ellipse([x - 7, y - 10, x + 7, y + 10], fill=(120, 170, 230))
    z = zoom(t)
    if z != 1:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5), int((h - HT) * 900 / HT); img = im2.crop((ox, oy, ox + WD, oy + HT))
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
