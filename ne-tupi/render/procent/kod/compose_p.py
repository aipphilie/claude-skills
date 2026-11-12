"""Монтаж «Первый миллион и десятый» (сложный процент): шапка + карточка с графиками (PIL, 2x) + персонаж (multiply) -> ffmpeg.
Палитра: белый / оранжевый / чёрный / красный."""
import json, math, os, sys, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from words import W, B, END, DUR
from tm import T
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920; SS = 2
BG = (244, 242, 238); OR = (255, 122, 0); ORL = (255, 214, 170); RED = (226, 45, 45); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (232, 229, 223); OWN = (38, 38, 38)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
@lru_cache(None)
def font(sz, black=True, ss=SS): return ImageFont.truetype(FB if black else FX, int(sz * ss))
xoff = json.load(open('xoff.json'))
ONLY = sys.argv[1:]

def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t): t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return 3 * t * t - 2 * t * t * t
def S(v): return int(round(v * SS))
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)

# ---------------- честный расчёт: 25 000 ₽ в начале месяца, 12% годовых, капитализация ежемесячно ----------------
P, R = 25000, 0.12 / 12
bal, own = [0.0], [0.0]
while len(bal) < 200:
    o = own[-1] + P; b = (bal[-1] + P) * (1 + R); own.append(o); bal.append(b)
MARK = {}
for m in range(1, 200):
    k = int(bal[m] // 1e6)
    for j in range(1, k + 1): MARK.setdefault(j, m)
MARK = {j: MARK[j] for j in range(1, 11)}            # месяц, когда набран j-й миллион: 34, 59, 79, 96, 110, ...
PER = {j: MARK[j] - (MARK[j - 1] if j > 1 else 0) for j in MARK}   # месяцев на каждый миллион: 34, 25, 20, 17, 14, 13, 11, 10, 9, 8
M10 = MARK[10]
def at(arr, m):
    m = clamp(m, 0, len(arr) - 1); i = int(m); f = m - i
    return arr[i] if i + 1 >= len(arr) else arr[i] * (1 - f) + arr[i + 1] * f
def fmt(v): return f'{int(round(v)):,}'.replace(',', ' ')
def mln(v): return f'{v / 1e6:.1f}'.replace('.', ',') + ' МЛН'
def ym(m): m = int(round(m)); return f'{m // 12} г {m % 12} мес' if m % 12 else f'{m // 12} лет' if m // 12 >= 5 else f'{m // 12} г'
print('months:', MARK, PER, 'own10', own[M10], 'bal10', round(bal[M10]), 'int/мес', round(bal[M10] * R))

# месяц на графике по времени ролика (ключевые точки привязаны к словам озвучки)
MK = [(B[5] + 0.0, 0), (T['chestno'] + 0.5, 0), (T['mesyacev2'] + 0.4, MARK[1]), (B[7] - 0.01, MARK[1]),
      (T['odinnadcat'] + 0.6, MARK[2]), (T['vosem_let'] + 0.3, MARK[4]), (T['nebolshim'] + 0.3, MARK[5]),
      (T['vosem3'] + 0.5, MARK[10]), (99, MARK[10])]
def month(t):
    for (ta, ma), (tb, mb) in zip(MK, MK[1:]):
        if ta <= t < tb: return ma + (mb - ma) * eio((t - ta) / (tb - ta)) if mb != ma else ma
    return 0

# ---------------- примитивы ----------------
@lru_cache(None)
def plate_img(text, sz, bg, fg, pad=26, border=None, ss=SS):
    f = font(sz, True, ss); lines = text.split('\n'); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    ws = [d0.textbbox((0, 0), l, font=f) for l in lines]; P_ = int(pad * ss)
    lh = int(sz * 1.16 * ss); w = max(b[2] - b[0] for b in ws) + P_ * 2; h = lh * len(lines) + P_ * 1.2
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(16 * ss), fill=bg, outline=border, width=int(5 * ss) if border else 0)
    for i, (l, b) in enumerate(zip(lines, ws)):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], P_ * 0.6 + i * lh + (lh - sz * ss) / 2 - sz * ss * 0.1), l, font=f, fill=fg)
    return im
def paste(G, im, cx, cy, scale=1.0, rot=0, alpha=1.0, ss=SS):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    G.alpha_composite(im, (int(cx * ss - im.width / 2), int(cy * ss - im.height / 2)))
def plate(G, t, t0, text, cx, cy, sz=56, bg=OR, fg=INK, rot=0, t1=None, border=None, k=1.0, ss=SS):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28) * k; a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    paste(G, plate_img(text, sz, bg, fg, border=border, ss=ss), cx, cy, sc, rot, a, ss)
def text(d, xy, s, sz, col=INK, black=True, anchor='la'):
    d.text((S(xy[0]), S(xy[1])), s, font=font(sz, black), fill=col, anchor=anchor)
def coin_img(r, label, rot=0, col=OR):
    k = 3; R_ = int(r * k); im = Image.new('RGBA', (2 * R_ + 8, 2 * R_ + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = R_ + 4
    lw = max(3, int(r * 0.07 * k))
    d.ellipse([c - R_, c - R_, c + R_, c + R_], fill=col, outline=INK, width=lw)
    d.ellipse([c - R_ * .78, c - R_ * .78, c + R_ * .78, c + R_ * .78], outline=(255, 170, 80) if col == OR else GREY, width=max(2, lw // 2))
    if label:
        sz = int(R_ * 0.55); f = ImageFont.truetype(FB, sz)
        while d.textlength(label, font=f) > R_ * 1.35 and sz > 6: sz -= 2; f = ImageFont.truetype(FB, sz)
        d.text((c, c), label, font=f, fill=INK, anchor='mm')
    if rot: im = im.rotate(rot, Image.BICUBIC)
    return im.resize((im.width // k, im.height // k), Image.LANCZOS)
def coin(G, cx, cy, r, label, rot=0, ss=SS):
    im = coin_img(r * ss, label, rot); G.alpha_composite(im, (int(cx * ss - im.width / 2), int(cy * ss - im.height / 2)))
def cross(G, x0, y0, x1, y1, k, col=RED, w=14):
    if k <= 0: return
    d = ImageDraw.Draw(G); k1 = clamp(k * 2); k2 = clamp(k * 2 - 1)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k1), S(y0 + (y1 - y0) * k1)], fill=col, width=S(w))
    if k2 > 0: d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k2), S(y0 + (y1 - y0) * k2)], fill=col, width=S(w))
def dashed(d, p0, p1, k, col=RED, w=7, dash=22, gap=14):
    L = math.dist(p0, p1) * k; ux, uy = (p1[0] - p0[0]) / math.dist(p0, p1), (p1[1] - p0[1]) / math.dist(p0, p1); s = 0
    while s < L:
        e = min(L, s + dash); d.line([S(p0[0] + ux * s), S(p0[1] + uy * s), S(p0[0] + ux * e), S(p0[1] + uy * e)], fill=col, width=S(w)); s += dash + gap

# ---------------- раскладка кадра ----------------
CX0, CY0, CW, CH = 50, 452, 880, 712          # карточка (справа 150 px — зона кнопок Reels)
SUB_Y = 1236; NOTE_Y = 1462                   # субтитры, нижняя плашка-сноска (выше 390 px снизу)
# график внутри карточки (локальные координаты)
PX0, PX1, PY0, PY1 = 110, 846, 178, 500
BAR_Y = 682; BAR_H = 78

def chart_axes(m):
    yrs = m / 12; xmax = max(3.0, yrs * 1.1 + 0.4); ymax = max(1.25e6, at(bal, m) * 1.22)
    return xmax, ymax
def nice(v, n=4):
    raw = v / n; mag = 10 ** math.floor(math.log10(raw)); st = min((1, 2, 2.5, 5, 10), key=lambda q: abs(q * mag - raw)) * mag
    return st
def to_px(x_yrs, y, xmax, ymax): return PX0 + (PX1 - PX0) * x_yrs / xmax, PY1 - (PY1 - PY0) * y / ymax

def draw_grid(d, xmax, ymax, ylabel_mln=True, alpha=1.0):
    gc = tuple(int(255 - (255 - c) * alpha) for c in (225, 222, 216)); lc = tuple(int(255 - (255 - c) * alpha) for c in GREY)
    sy = nice(ymax); v = sy
    while v < ymax * 0.999:
        y = to_px(0, v, xmax, ymax)[1]; d.line([S(PX0), S(y), S(PX1), S(y)], fill=gc, width=S(2))
        lab = (f'{v / 1e6:g}'.replace('.', ',') + ' млн') if ylabel_mln else fmt(v)
        text(d, (PX0 - 10, y), lab, 17, lc, False, 'rm'); v += sy
    sx = nice(xmax, 5); sx = max(1, round(sx)); x = 0
    while x <= xmax:
        px = to_px(x, 0, xmax, ymax)[0]; text(d, (px, PY1 + 12), f'{x:g} л', 17, lc, False, 'ma'); x += sx
    d.line([S(PX0), S(PY1), S(PX1), S(PY1)], fill=INK, width=S(4))

def growth_chart(G, t, m, dots=True, labels=True):
    """кривая роста: свои (чёрное) + проценты (оранжевое), точки миллионов. Возвращает кончик кривой (локально)."""
    d = ImageDraw.Draw(G); xmax, ymax = chart_axes(m); draw_grid(d, xmax, ymax)
    if m > 0.05:
        ms = np.linspace(0, m, max(2, int(m * 3)))
        top = [to_px(q / 12, at(bal, q), xmax, ymax) for q in ms]; mid = [to_px(q / 12, at(own, q), xmax, ymax) for q in ms]
        base = [(top[-1][0], S(PY1) / SS), (top[0][0], PY1)]
        d.polygon([(S(x), S(y)) for x, y in top + mid[::-1]], fill=OR)
        d.polygon([(S(x), S(y)) for x, y in mid + base], fill=OWN)
        d.line([(S(x), S(y)) for x, y in top], fill=INK, width=S(6), joint='curve')
        if labels and m > 40:
            q = m * 0.72; x, y1 = to_px(q / 12, at(own, q), xmax, ymax); y2 = to_px(q / 12, at(bal, q), xmax, ymax)[1]
            text(d, (x, (y1 + PY1) / 2 + 4), 'свои', 19, WHITE, True, 'mm')
            if y1 - y2 > 26: text(d, (x - 4, (y1 + y2) / 2 + 2), 'проценты', 19, INK, True, 'mm')
        if dots:
            for j, mj in MARK.items():
                if mj <= m + 0.01:
                    x, y = to_px(mj / 12, at(bal, mj), xmax, ymax)
                    d.ellipse([S(x - 8), S(y - 8), S(x + 8), S(y + 8)], fill=RED if j == 1 else (OR if j == 10 else INK), outline=WHITE, width=S(3))
        return to_px(m / 12, at(bal, m), xmax, ymax)
    return (PX0, PY1)

def bars(G, t, m, hl10=False):
    d = ImageDraw.Draw(G); text(d, (PX0 - 40, BAR_Y - BAR_H - 46), 'месяцев на каждый миллион', 19, GREY, True)
    n = 10; w = (PX1 - PX0 + 40) / n
    for j in range(1, 11):
        x = PX0 - 40 + (j - 0.5) * w
        text(d, (x, BAR_Y + 6), f'{j}-й', 16, GREY, False, 'ma')
        if MARK[j] > m + 0.01:
            d.rounded_rectangle([S(x - w * 0.36), S(BAR_Y - 6), S(x + w * 0.36), S(BAR_Y)], radius=S(3), fill=LG); continue
        h = BAR_H * PER[j] / PER[1]
        col = RED if j == 1 else (OR if j == 10 else (90, 90, 90))
        d.rounded_rectangle([S(x - w * 0.36), S(BAR_Y - h), S(x + w * 0.36), S(BAR_Y)], radius=S(6), fill=col)
        big = (j == 10 and hl10)
        text(d, (x, BAR_Y - h - 4), str(PER[j]), 30 if big else 21, col if j in (1, 10) else INK, True, 'mb')

def chips(G, t, vals, t0=0):
    """плашки сверху карточки: [(текст, фон, цвет текста, время появления)]"""
    x = 22
    for txt, bg, fg, ta in vals:
        if t < ta: continue
        im = plate_img(txt, 24, bg, fg, pad=16, border=INK if bg == WHITE else None)
        k = back((t - ta) / 0.25); paste(G, im, x + im.width / SS / 2, 44, k); x += im.width / SS + 14

# ---------------- гора (хук и подвох) ----------------
SUMX, SUMY, GND = 440, 300, 640
def slope(x):  # высота склона в точке x (локально)
    return GND - (GND - SUMY) * (x / SUMX if x <= SUMX else (CW - x) / (CW - SUMX))
def mountain(G):
    d = ImageDraw.Draw(G); pts = [(-10, GND + 5), (SUMX, SUMY), (CW + 10, GND + 5)]
    d.polygon([(S(x), S(y)) for x, y in pts + [(CW + 10, CH + 10), (-10, CH + 10)]], fill=LG)
    d.line([(S(x), S(y)) for x, y in pts], fill=INK, width=S(6), joint='curve')

# ---------------- сцены карточки: рисуют в G (локально, 2x), возвращают позицию персонажа (x, ноги, масштаб) локально ----------------
CHS = 0.13
def sc_hook(G, t, i):
    mountain(G); d = ImageDraw.Draw(G)
    text(d, (30, 26), '1-Й МИЛЛИОН', 26, INK);
    k = back((t - 0.25) / 0.3)
    if k > 0.05: paste(G, plate_img('34 МЕС', 56, WHITE, RED, pad=0), 112, 92, k)
    td = T['desyatyy'] - 0.1
    if t < td:
        x = 150 + 150 * (t / td); return (x, slope(x) + 2, 0.24), 'coin1'
    text(d, (CW - 30, 26), '10-Й МИЛЛИОН', 26, INK, True, 'ra')
    k = back((t - td) / 0.3)
    if k > 0.05: paste(G, plate_img('8 МЕС', 56, WHITE, OR, pad=0), CW - 105, 92, k)
    # монета 10 МЛН катится вниз по правому склону, человечек едет сверху
    u = clamp((t - td) / (B[1] + 1.3 - td)); u = u * u * 0.85 + u * 0.15
    x = SUMX + 10 + (CW - 190 - SUMX) * u; r = 92 + 18 * u
    ang = (x - SUMX) / CW * (CW - SUMX)
    # центр монеты над склоном по нормали
    nx, ny = math.sin(math.atan2(GND - SUMY, CW - SUMX)), math.cos(math.atan2(GND - SUMY, CW - SUMX))
    cx, cy = x + nx * r * 0, slope(x) - r / ny
    for j in range(3):   # линии скорости
        if u > 0.02 and u < 0.98:
            yy = cy - r * 0.5 + j * r * 0.5; d.line([S(cx - r - 40 - j * 20), S(yy - 30), S(cx - r - 110 - j * 20), S(yy - 60)], fill=GREY, width=S(5))
    coin(G, cx, cy, r, '10 МЛН', rot=-ang * 1.4)
    return (cx, cy - r + 4, 0.17), None

def sc_why(G, t, i):
    st = sc_hook(G, t, i)
    plate(G, t, T['pochemu'] - 0.15, 'ПОЧЕМУ?', 440, 230, 70, INK, WHITE, rot=-3)
    return st

def line_axes(G, t, k_line, alpha=1.0):
    d = ImageDraw.Draw(G); xmax, ymax = 30, 11e6; draw_grid(d, xmax, ymax, alpha=alpha)
    p0 = to_px(0, 0, xmax, ymax); p1 = to_px(30, 10e6, xmax, ymax)
    if k_line > 0: dashed(d, p0, p1, k_line)
    return p0, p1
def sc_setup(G, t, i):
    chips(G, t, [('ВЗНОС 25 000 ₽', INK, WHITE, T['dvadcat']), ('СТАВКА 12% ГОДОВЫХ', OR, INK, T['dvenadcat'])])
    p0, p1 = line_axes(G, t, 0)
    return (p0[0] + 10, p0[1], CHS), 'coinR'
def sc_line(G, t, i):
    chips(G, t, [('ВЗНОС 25 000 ₽', INK, WHITE, 0), ('СТАВКА 12% ГОДОВЫХ', OR, INK, 0)])
    u = eio((t - T['pryamoy']) / (T['tridcat'] + 0.6 - T['pryamoy']))
    p0, p1 = line_axes(G, t, u)
    d = ImageDraw.Draw(G)
    if t >= T['pryamoy']:
        # 1 млн за 3 года — отметка
        q = to_px(3, 1e6, 30, 11e6)
        if u > 0.1:
            d.ellipse([S(q[0] - 8), S(q[1] - 8), S(q[0] + 8), S(q[1] + 8)], fill=RED, outline=WHITE, width=S(3))
            plate(G, t, T['pryamoy'] + 0.6, '1 МЛН ЗА 3 ГОДА', q[0] + 120, q[1] + 34, 22, WHITE, RED, border=RED)
    plate(G, t, T['tridcat'] - 0.1, '10 МЛН ЗА 30 ЛЕТ?', 470, 150, 30, RED, WHITE, rot=-2)
    x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u
    return (x + 6, y, CHS), 'coinR'
def sc_stop(G, t, i):
    chips(G, t, [('ВЗНОС 25 000 ₽', INK, WHITE, 0), ('СТАВКА 12% ГОДОВЫХ', OR, INK, 0)])
    p0, p1 = line_axes(G, t, 1, alpha=0.5)
    cross(G, p0[0] + 120, p1[1] - 10, p1[0] - 40, p0[1] - 60, clamp((t - T['stop'] - 0.3) / 0.35), INK, 16)
    return (p1[0] + 6, p1[1], CHS), None

def sc_count(G, t, i):
    m = month(t); d = ImageDraw.Draw(G)
    chips(G, t, [('ВЗНОС 25 000 ₽', INK, WHITE, 0), (f'ПРОЦЕНТЫ +{fmt(round(at(bal, m) * R, -2))} ₽/МЕС', OR, INK, 0)])
    text(d, (24, 86), mln(at(bal, m)), 50, INK)
    text(d, (24 + d.textlength(mln(at(bal, m)), font=font(50)) / SS + 16, 112), ym(m), 24, GREY, True)
    tip = growth_chart(G, t, m)
    bars(G, t, m)
    if line_of(t) == 5 and t >= T['svoih'] - 0.1:
        plate(G, t, T['svoih'] - 0.1, 'СВОИХ 850 000', 420, 300, 26, INK, WHITE, rot=-2)
        plate(G, t, T['svoih'] + 0.6, 'ПРОЦЕНТЫ 150 000', 470, 360, 26, OR, INK, rot=2)
    return (tip[0] - 2, tip[1], CHS), 'coin'

def sc_snow(G, t, i):
    d = ImageDraw.Draw(G); gy = 600; t0 = B[6]; tk = T['kom'] - 0.05
    d.line([S(0), S(gy), S(CW), S(gy)], fill=INK, width=S(6))
    sp = 180   # скорость земли (px/сек)
    roll = (min(t, tk) - t0) * sp + max(0, t - tk) * 0  # пока толкает — земля едет
    for j in range(14):
        x = (j * 90 - roll) % (CW + 90) - 45; d.line([S(x), S(gy + 16), S(x + 26), S(gy + 16)], fill=GREY, width=S(4))
    plate(G, t, B[6] + 0.1, 'СЛОЖНЫЙ ПРОЦЕНТ', 440, 70, 40, INK, WHITE, rot=-2)
    plate(G, t, T['tvoi'] - 0.1, '% НА ТВОИ ДЕНЬГИ', 300, 160, 26, WHITE, INK, border=INK, rot=-2, t1=T['rastet'] - 0.2)
    plate(G, t, T['proshlye'] - 0.1, '+ % НА ПРОЦЕНТЫ', 600, 205, 26, OR, INK, rot=2, t1=T['rastet'] - 0.2)
    u = clamp((t - t0) / (B[7] - t0)); r = 46 + 150 * u ** 1.6
    hx = 250; bx = hx + 70 + r + (eio((t - tk) / 1.2) * 220 if t > tk else 0)
    by = gy - r
    rot = -((t - t0) * sp + (eio((t - tk) / 1.2) * 220 if t > tk else 0)) / max(r, 1) * 57
    coin(G, bx, by, r, '', rot=rot)
    dd = ImageDraw.Draw(G)  # кольца «процентов на проценты»
    nr = 1 + int(u * 5)
    for j in range(1, nr):
        rr = r * (1 - j / (nr + 0.5)); dd.ellipse([S(bx - rr), S(by - rr), S(bx + rr), S(by + rr)], outline=(255, 170, 80) if j % 2 else INK, width=S(3))
    text(dd, (bx, by), fmt(round(at(bal, u * MARK[10]), -3)) + ' ₽', max(14, int(r * 0.26)), INK, True, 'mm')
    if t >= T['kapayut']:   # прилетающие монетки «%»
        for j in range(4):
            q = ((t - T['kapayut']) * 1.1 + j / 4) % 1
            x = bx + 40 + (1 - q) * 200 - q * 30; y = by - r - 160 * (1 - q) ** 1.5 + q * (r * 0.6)
            if q < 0.92: coin(G, x, y, 20, '%')
    plate(G, t, T['rastet'] - 0.1, 'КОМ РАСТЁТ САМ', 440, 270, 34, OR, INK, rot=-3)
    return (hx, gy, 0.26), None

def sc_pie(G, t, i):
    d = ImageDraw.Draw(G); o = own[M10]; b = bal[M10]
    text(d, (CW / 2, 26), '10 МЛН ЗА 13 Л 5 МЕС', 40, INK, True, 'ma')
    cx, cy, r = 560, 400, 210; k = eo((t - B[9]) / 0.5)
    if k > 0:
        rr = r * back((t - B[9]) / 0.4)
        d.ellipse([S(cx - rr), S(cy - rr), S(cx + rr), S(cy + rr)], fill=OR, outline=INK, width=S(6))
        u = eo((t - T['chetyre'] + 0.1) / 0.5)
        if u > 0:
            a = 360 * o / b * u
            d.pieslice([S(cx - rr), S(cy - rr), S(cx + rr), S(cy + rr)], -90, -90 + a, fill=OWN, outline=INK, width=S(6))
    plate(G, t, T['chetyre'] + 0.1, 'СВОИ\n4 МЛН', cx + 120, cy - 120, 30, INK, WHITE, rot=3)
    plate(G, t, T['ostalnye'], 'ПРОЦЕНТЫ\n6 МЛН', cx - 60, cy + 90, 34, WHITE, INK, border=INK, rot=-2)
    return (150, 640, 0.27), None

def sc_month(G, t, i):
    d = ImageDraw.Draw(G); gy = 640
    text(d, (CW / 2, 26), 'КАЖДЫЙ МЕСЯЦ', 40, INK, True, 'ma')
    d.line([S(40), S(gy), S(CW - 40), S(gy)], fill=INK, width=S(5))
    bw, bh = 170, 86
    ax, bxx = 400, 680
    k = back((t - B[10] - 0.1) / 0.3)
    if k > 0.05:
        d.rounded_rectangle([S(ax - bw / 2), S(gy - bh * k), S(ax + bw / 2), S(gy)], radius=S(10), fill=OWN)
        text(d, (ax, gy - bh - 70), 'ВЗНОС', 24, GREY, True, 'ma'); text(d, (ax, gy - bh - 42), '25 000 ₽', 30, INK, True, 'ma')
    for j in range(4):
        tj = T['sto'] + j * 0.22
        if t < tj: continue
        u = eo((t - tj) / 0.25); y0 = gy - (j + 1) * (bh + 6) - 200 * (1 - u)
        d.rounded_rectangle([S(bxx - bw / 2), S(y0), S(bxx + bw / 2), S(y0 + bh)], radius=S(10), fill=OR, outline=INK, width=S(4))
    if t >= T['sto']:
        text(d, (bxx, gy - 4 * (bh + 6) - 72), 'ПРОЦЕНТЫ', 24, GREY, True, 'ma'); text(d, (bxx, gy - 4 * (bh + 6) - 44), '100 000 ₽', 30, OR, True, 'ma')
    plate(G, t, T['chetyre3'] - 0.05, '×4', 540, 330, 64, RED, WHITE, rot=-8)
    return (170, gy, 0.27), None

def sc_twist(G, t, i):
    mountain(G); t0 = B[11]; ts = T['sdayutsya'] - 0.1
    if t < ts:
        x = 120 + 190 * clamp((t - t0) / (ts - t0)) ** 0.8
        return (x, slope(x) + 2, 0.24), 'coin1'
    # монета скатывается обратно, человечек остаётся
    x = 120 + 190
    u = clamp((t - ts) / 0.9); cxx = x + 60 - u * u * 260
    ang = math.atan2(GND - SUMY, SUMX)
    coin(G, cxx, slope(cxx) - 70 / math.cos(ang), 70, '1 МЛН', rot=u * 300)
    return (x, slope(x) + 2, 0.24), None

def sc_cta(G, t, i):
    m = MARK[10]; d = ImageDraw.Draw(G)
    chips(G, t, [('ВЗНОС 25 000 ₽', INK, WHITE, 0), ('ПРОЦЕНТЫ +100 000 ₽/МЕС', OR, INK, 0)])
    text(d, (24, 86), '10 МЛН', 50, INK); text(d, (24 + d.textlength('10 МЛН', font=font(50)) / SS + 16, 112), '13 г 5 мес', 24, GREY, True)
    tip = growth_chart(G, t, m); bars(G, t, m, hl10=True)
    k = back((t - T['skolko'] + 0.1) / 0.35)
    if k > 0.05:
        im = Image.new('RGBA', (S(820), S(110)), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, S(819), S(109)], radius=S(20), fill=WHITE, outline=OR, width=S(6))
        f = font(34); s1 = 'Сколько ты '; s2 = 'откладываешь'; s3 = ' в месяц?'
        w = sum(dd.textlength(s, font=f) for s in (s1, s2, s3)); x = (S(820) - w) / 2
        for s, c in ((s1, INK), (s2, OR), (s3, INK)): dd.text((x, S(55)), s, font=f, fill=c, anchor='lm'); x += dd.textlength(s, font=f)
        paste(G, im, CW / 2, CH - 70, k)
    return (tip[0] - 2, tip[1], CHS), None

def sc_final(G, t, i):
    plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 440, 150, 80, OR, INK, rot=-4)
    return (440, 660, 0.24), None

SCENES = [sc_hook, sc_why, sc_setup, sc_line, sc_stop, sc_count, sc_snow, sc_count, sc_count, sc_pie, sc_month, sc_twist, sc_cta, sc_final]
# смена карточки — короткий «вжух»: новая карточка въезжает справа
CARD_CHANGE = [B[2], B[5], B[6], B[7], B[9], B[10], B[11], B[12], B[13]]

# ---------------- шапка ----------------
def header(img, t):
    G = Image.new('RGBA', (WD * SS, 220 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(G)
    text(d, (WD / 2, 6), 'ПЕРВЫЙ МИЛЛИОН', 62, INK, True, 'ma')
    paste(G, plate_img('И ДЕСЯТЫЙ', 58, OR, INK, pad=16), WD / 2, 112)
    L = line_of(t)
    tag = None
    if L == 3 and t >= T['tridcat'] - 0.1: tag = ('ПО ПРЯМОЙ — 30 ЛЕТ', WHITE, RED, RED, T['tridcat'] - 0.1)
    elif L == 4: tag = ('ПО ПРЯМОЙ — 30 ЛЕТ', WHITE, RED, RED, -9)
    elif L == 5 and t >= T['svoih'] - 0.1: tag = ('СВОИХ — 850 000', INK, WHITE, None, T['svoih'] - 0.1)
    elif L == 6: tag = ('ПРОЦЕНТЫ НА ПРОЦЕНТЫ', OR, INK, None, B[6])
    elif L == 8 and t >= T['itogo'] - 0.1: tag = ('10 МЛН ЗА 13 ЛЕТ', OR, INK, None, T['itogo'] - 0.1)
    elif L == 9: tag = ('СВОИХ — 4 МЛН', INK, WHITE, None, T['chetyre'])
    elif L == 10: tag = ('В 4 РАЗА БОЛЬШЕ', RED, WHITE, None, T['chetyre3'])
    elif L == 11 and t >= T['tyazh'] - 0.1: tag = ('ПЕРВЫЙ — САМЫЙ ТЯЖЁЛЫЙ', WHITE, RED, RED, T['tyazh'] - 0.1)
    if tag and t >= tag[4]:
        plate(G, t, tag[4], tag[0], WD / 2, 182, 26, tag[1], tag[2], border=tag[3], rot=-1.5)
    elif t >= T['dvadcat']:
        text(d, (WD / 2, 168), '25 000 ₽ в месяц · 12% годовых', 24, GREY, True, 'ma')
    G = G.resize((WD, 220), Image.LANCZOS); img.paste(G, (0, 252), G)

# ---------------- нижние плашки ----------------
@lru_cache(None)
def note_img():
    im = Image.new('RGBA', (S(860), S(84)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S(859), S(83)], radius=S(14), fill=(232, 229, 223))
    d.text((S(430), S(26)), 'Расчёт: 25 000 ₽ в начале месяца, 12% годовых, капитализация ежемесячно', font=font(17, False), fill=(110, 110, 110), anchor='mm')
    d.text((S(430), S(58)), 'БЕЗ УЧЁТА ИНФЛЯЦИИ И НАЛОГА НА ДОХОДЫ', font=font(22), fill=INK, anchor='mm')
    return im.resize((860, 84), Image.LANCZOS)
@lru_cache(None)
def nir_img():
    im = plate_img('Не является индивидуальной инвестиционной рекомендацией', 23, WHITE, RED, pad=12, border=RED, ss=1)
    return im
def bottom(img, t):
    n = note_img(); img.paste(n, (int(490 - n.width / 2), NOTE_Y - n.height // 2), n)
    if t < 5.0:
        a = 1 if t < 4.7 else (5.0 - t) / 0.3; m = nir_img().copy()
        if a < 1: m.putalpha(m.getchannel('A').point(lambda v: int(v * a)))
        img.paste(m, (int(490 - m.width / 2), NOTE_Y - 42 - m.height), m)

# ---------------- субтитры ----------------
SUBF = ImageFont.truetype(FB, 54); SP = 13; MAXW = 800
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
    if cur and (len(wrap(cur + [w])) > 2 or len(cur) >= 6): groups.append(cur); cur = []
    cur.append(w)
    if w[0].rstrip('»')[-1] in '.!?:' or (w[0][-1] in ',—' and len(cur) >= 3): groups.append(cur); cur = []
if cur: groups.append(cur)
def subs(img, t, y0=SUB_Y):
    g = next((g for i, g in enumerate(groups) if g[0][1] - 0.05 <= t < (groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else g[-1][2] + 0.4)), None)
    if not g: return
    d = ImageDraw.Draw(img); lines = wrap(g); y = y0 if len(lines) == 1 else y0 - 36
    for ln in lines:
        ws = [wlen(w) for w in ln]; x = 490 - (sum(ws) + SP * (len(ws) - 1)) / 2
        for w, wd in zip(ln, ws):
            on = w[1] <= t < w[2] + 0.15
            if on: d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 66], radius=12, fill=OR)
            d.text((x, y), w[0].upper().strip('«»'), font=SUBF, fill=INK)
            x += wd + SP
        y += 74

# ---------------- персонаж ----------------
CH_CROP = (0, 60, 1080, 1660)
_anch = None
def anchors():
    global _anch
    if _anch is None: _anch = json.load(open('kadry/main/anchors.json'))
    return _anch
def char_box(i, cx, feet, s):
    bot = feet + 70 * s; cw, chh = int(1080 * s), int(1600 * s)
    return int(cx - cw / 2 + xoff[i]), int(bot - chh), cw, chh

def zoom(t):
    for ta, tb, z in ((T['stop'] - 0.05, B[5], 0.07), (T['desyatyy2'] - 0.05, T['itogo'] - 0.1, 0.05), (T['chetyre3'] - 0.05, B[11], 0.05), (T['netupi'] - 0.3, 99, 0.05)):
        if ta <= t < tb: return 1 + z * eo((t - ta) / 0.2)
    return 1.0

def frame(i):
    t = i / FPS; L = line_of(t)
    img = Image.new('RGB', (WD, HT), BG)
    header(img, t)
    # карточка
    G = Image.new('RGBA', (CW * SS, CH * SS), (255, 255, 255, 255))
    (lx, lf, ls), carry = SCENES[L](G, t, i)
    # въезд новой карточки
    dx = 0
    for tc in CARD_CHANGE:
        if tc <= t < tc + 0.28: dx = (1 - eo((t - tc) / 0.28)) * 260
    card = G.resize((CW, CH), Image.LANCZOS)
    mask = Image.new('L', (CW, CH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, CW - 1, CH - 1], radius=26, fill=255)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([CX0 + dx - 4, CY0 - 4 + 8, CX0 + dx + CW + 4, CY0 + CH + 4 + 8], radius=30, fill=(222, 219, 212))   # тень
    img.paste(card, (int(CX0 + dx), CY0), mask)
    d.rounded_rectangle([CX0 + dx, CY0, CX0 + dx + CW, CY0 + CH], radius=26, outline=INK, width=4)
    subs(img, t); bottom(img, t)
    # персонаж (multiply), только внутри карточки
    cx, feet, s = CX0 + dx + lx, CY0 + lf, ls
    x0, y0, cw, chh = char_box(i, cx, feet, s)
    ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (x0, y0))
    cl = Image.new('L', (WD, HT), 0); ImageDraw.Draw(cl).rounded_rectangle([CX0 + dx + 3, CY0 - 40, CX0 + dx + CW - 3, CY0 + CH - 3], radius=24, fill=255)
    layer = Image.composite(layer, Image.new('RGB', (WD, HT), WHITE), cl)
    arr = np.asarray(img, np.float32) * np.asarray(layer, np.float32) / 255
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if carry:   # монета на спине (поверх, у точки спины)
        a = anchors()[i]; bx = x0 + a['back'][0] * s; by = y0 + (a['back'][1] - 60) * s
        r = {'coin1': 300, 'coinR': 230, 'coin': 230}[carry] * s
        lab = {'coin1': '1 МЛН', 'coinR': '₽', 'coin': '₽'}[carry]
        im = coin_img(r, lab, rot=8); img.paste(im, (int(bx - r * 0.75 - im.width / 2), int(by - r * 0.15 - im.height / 2)), im)
    if L in (0, 11) and carry == 'coin1':   # капли пота
        a = anchors()[i]; hx = x0 + a['top'][0] * s; hy = y0 + (a['top'][1] - 60) * s; dd = ImageDraw.Draw(img)
        for j in range(2):
            u = ((t * 1.3) + j * 0.5) % 1; x = hx + 20 + 40 * u; y = hy + 10 - 30 * math.sin(math.pi * u) + 50 * u
            dd.ellipse([x - 6, y - 9, x + 6, y + 9], fill=(120, 170, 230))
    if L == 4:   # «Стоп» поверх всего
        G2 = Image.new('RGBA', (WD, HT), (0, 0, 0, 0))
        plate(G2, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 490, 780, 84, OR, INK, rot=-4, ss=1)
        img.paste(G2, (0, 0), G2)
    z = zoom(t)
    if z != 1:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        sh = 6 * math.sin(t * 70) if L == 4 and t < T['stop'] + 0.35 else 0
        ox, oy = int((w - WD) * 0.45 + sh), int((h - HT) * 800 / HT); img = im2.crop((ox, oy, ox + WD, oy + HT))
    return img

if __name__ == '__main__':
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        part, parts = int(os.environ.get('PART', 0)), int(os.environ.get('PARTS', 1))
        a, b = N * part // parts, N * (part + 1) // parts
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
        for i in range(a, b):
            p.stdin.write(frame(i).tobytes())
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
