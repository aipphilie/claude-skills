"""«Голос мамы»: фон + графика (PIL, 2x суперсэмплинг, координаты кадра) + персонаж (multiply) -> ffmpeg."""
import json, math, sys, subprocess, random, numpy as np
from functools import lru_cache
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
from words import W, B, DUR
from anch import T
FPS = 24; N = int(DUR * FPS); WD, HT = 1080, 1920
GH = 1400; SS = 2   # графика в координатах кадра (верхние 1400 px), рисуем в 2x
BG = (247, 245, 240); YEL = (255, 212, 0); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
GREY = (150, 150, 150); LG = (225, 222, 215); DG = (95, 95, 95)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
@lru_cache(None)
def font(sz, black=True): return ImageFont.truetype(FB if black else FX, int(sz * SS))
xoff = json.load(open('xoff.json'))
MW = json.load(open('mama_words.json'))   # слова голосового «мамы»: [слово, start, end]
MEND = MW[-1][2]
ONLY = sys.argv[1:]

def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
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
def paste(G, im, cx, cy, scale=1.0, rot=0, alpha=1.0, sx=1.0):
    if scale <= 0.01 or alpha <= 0.01 or abs(sx) <= 0.02: return
    if scale != 1 or sx != 1: im = im.resize((max(1, int(im.width * scale * abs(sx))), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    G.alpha_composite(im, (int(S(cx) - im.width / 2), int(S(cy) - im.height / 2)))
def plate(G, t, t0, text, cx, cy, sz=64, bg=YEL, fg=INK, rot=0, t1=None, border=None, k=1.0):
    if t < t0 or (t1 and t > t1 + 0.15): return
    sc = back((t - t0) / 0.28) * k
    a = 1.0 if not t1 or t < t1 else 1 - (t - t1) / 0.15
    paste(G, plate_img(text, int(sz * 1.25), bg, fg, border=border), cx, cy, sc, rot, a)
def text(G, txt, cx, y, sz, col=INK, black=True, anchor='m'):
    d = ImageDraw.Draw(G); f = font(sz, black); bb = d.textbbox((0, 0), txt, font=f)
    x = S(cx) - (bb[2] - bb[0]) / 2 if anchor == 'm' else S(cx)
    d.text((x, S(y)), txt, font=f, fill=col)
def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, width=0):
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(r), fill=fill, outline=outline, width=S(width))
def cross(G, x0, y0, x1, y1, k, w=16):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(w))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(w))

# ---------- элементы ----------
@lru_cache(None)
def bars(seed, n):
    r = random.Random(seed); return [0.25 + 0.75 * r.random() * (0.55 + 0.45 * math.sin(i * 0.9 + seed)) ** 2 + 0.1 for i in range(n)]
def wave(d, x, cy, w, h, n=20, seed=1, prog=1.0, live=None, on=YEL, off=DG):
    """звуковая волна: n столбиков, первые prog доли закрашены; live=t — столбики дышат"""
    hs = bars(seed, n); step = w / n; bw = step * 0.56
    for i, a in enumerate(hs):
        if live is not None: a = clamp(a * (0.55 + 0.6 * abs(math.sin(live * 9 + i * 1.7))), 0.12, 1)
        bh = max(bw, h * min(1, a)); bx = x + i * step
        d.rounded_rectangle([S(bx), S(cy - bh / 2), S(bx + bw), S(cy + bh / 2)], radius=S(bw / 2), fill=on if (i + 0.5) / n <= prog else off)
def vbubble(G, cx, cy, w=380, h=110, seed=1, prog=1.0, live=None, k=1.0, label=None, tail=None, fill=INK, dur='0:04'):
    """пузырь голосового: тёмный, жёлтая кнопка и волна"""
    if k <= 0.05: return
    w *= k; h *= k; d = ImageDraw.Draw(G)
    rrect(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h * 0.42, fill=fill)
    if tail == 'l': d.polygon([(S(cx - w / 2 + 6), S(cy + h * 0.12)), (S(cx - w / 2 - 22 * k), S(cy + h / 2)), (S(cx - w / 2 + 40 * k), S(cy + h / 2 - 4))], fill=fill)
    r = h * 0.3; px = cx - w / 2 + h * 0.5
    d.ellipse([S(px - r), S(cy - r), S(px + r), S(cy + r)], fill=YEL)
    d.polygon([(S(px - r * .3), S(cy - r * .45)), (S(px - r * .3), S(cy + r * .45)), (S(px + r * .5), S(cy))], fill=INK)
    wave(d, px + r + 16 * k, cy, w - h - r - 30 * k, h * 0.52, n=18, seed=seed, prog=prog, live=live)
    if label: text(G, label, cx - w / 2 + 10, cy + h / 2 + 4, 24, GREY, False, 'l')
def avatar(G, cx, cy, r, kind='mama', sx=1.0):
    """аватарка: мама (жёлтый круг с «М») или мошенник (серый капюшон с «?»)"""
    if abs(sx) < 0.04: return
    im = Image.new('RGBA', (S(r * 2 + 12), S(r * 2 + 12)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = im.width / 2
    if kind == 'mama':
        d.ellipse([S(6), S(6), im.width - S(6), im.height - S(6)], fill=YEL, outline=INK, width=S(max(5, r * .09)))
        f = font(r * 1.0); bb = d.textbbox((0, 0), 'М', font=f); d.text((c - (bb[2] + bb[0]) / 2, c - (bb[3] + bb[1]) / 2), 'М', font=f, fill=INK)
    else:
        d.ellipse([S(6), S(6), im.width - S(6), im.height - S(6)], fill=(70, 70, 70), outline=INK, width=S(max(5, r * .09)))
        f = font(r * 1.15); bb = d.textbbox((0, 0), '?', font=f); d.text((c - (bb[2] + bb[0]) / 2, c - (bb[3] + bb[1]) / 2), '?', font=f, fill=WHITE)
    paste(G, im, cx, cy, 1.0, 0, 1.0, sx)
def lock(d, cx, cy, s, open_=False, fill=INK, body=YEL):
    w = 54 * s; h = 44 * s
    off = -26 * s if open_ else 0
    d.arc([S(cx - 19 * s + off), S(cy - 52 * s), S(cx + 19 * s + off), S(cy - 2 * s)], 180, 360, fill=fill, width=S(9 * s))
    d.line([S(cx + 19 * s + off - 4.5 * s), S(cy - 28 * s), S(cx + 19 * s + off - 4.5 * s), S(cy - 6 * s)], fill=fill, width=S(9 * s))
    if not open_: d.line([S(cx - 19 * s + 4.5 * s), S(cy - 28 * s), S(cx - 19 * s + 4.5 * s), S(cy - 6 * s)], fill=fill, width=S(9 * s))
    rrect(d, cx - w / 2, cy - 8 * s, cx + w / 2, cy - 8 * s + h, 9 * s, fill=body, outline=fill, width=5 * s)
    d.ellipse([S(cx - 6 * s), S(cy + 6 * s), S(cx + 6 * s), S(cy + 18 * s)], fill=fill)
def secret(G, cx, cy, k=1.0, open_=False, n=5, sz=1.0):
    """жёлтая плашка с закрытым словом ● ● ● ● ● и замком"""
    if k <= 0.05: return
    w = (150 + n * 62) * k * sz; h = 120 * k * sz; d = ImageDraw.Draw(G)
    rrect(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 22 * k, fill=YEL, outline=INK, width=6 * k)
    for i in range(n):
        x = cx - w / 2 + (50 + i * 62) * k * sz; r = 19 * k * sz
        d.ellipse([S(x - r), S(cy - r), S(x + r), S(cy + r)], fill=INK)
    lock(d, cx + w / 2 - 62 * k * sz, cy + 8 * k * sz, 1.0 * k * sz, open_, INK, WHITE)
def heart(d, cx, cy, s, fill=RED):
    d.ellipse([S(cx - 50 * s), S(cy - 48 * s), S(cx + 2 * s), S(cy + 4 * s)], fill=fill)
    d.ellipse([S(cx - 2 * s), S(cy - 48 * s), S(cx + 50 * s), S(cy + 4 * s)], fill=fill)
    d.polygon([(S(cx - 47 * s), S(cy - 8 * s)), (S(cx + 47 * s), S(cy - 8 * s)), (S(cx), S(cy + 52 * s))], fill=fill)
def handset(G, cx, cy, s):
    im = Image.new('RGBA', (S(170), S(170)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc([S(25), S(-20), S(205), S(160)], 100, 190, fill=INK, width=S(30))
    d.rounded_rectangle([S(18), S(38), S(66), S(84)], radius=S(16), fill=INK)
    d.rounded_rectangle([S(84), S(118), S(132), S(160)], radius=S(16), fill=INK)
    paste(G, im, cx, cy, s, 0)
def person(d, cx, by, s, col=INK):
    d.ellipse([S(cx - 20 * s), S(by - 100 * s), S(cx + 20 * s), S(by - 60 * s)], fill=col)
    rrect(d, cx - 23 * s, by - 56 * s, cx + 23 * s, by, 20 * s, fill=col)
def phone(G, x0, y0, x1, y1, title='Мама', k=1.0, kind='mama', sx=1.0):
    d = ImageDraw.Draw(G)
    rrect(d, x0 - 6, y0 - 6, x1 + 14, y1 + 14, 54, fill=LG)
    rrect(d, x0, y0, x1, y1, 48, fill=WHITE, outline=INK, width=10)
    rrect(d, x0 + 10, y0 + 10, x1 - 10, y0 + 132, 38, fill=LG)
    d.rectangle([S(x0 + 10), S(y0 + 80), S(x1 - 10), S(y0 + 132)], fill=LG)
    avatar(G, x0 + 76, y0 + 72, 42, kind, sx)
    text(G, title, x0 + 136, y0 + 34, 44, INK, True, 'l')
    text(G, 'в сети', x0 + 138, y0 + 88, 26, GREY, False, 'l')

# ---------- сцены ----------
PH = (470, 285, 925, 1215)   # телефон в интро (справа, в безопасной зоне)
def sc_intro(G, t):
    x0, y0, x1, y1 = PH; d = ImageDraw.Draw(G)
    k = eo(t / 0.35); dy = (1 - k) * 500
    phone(G, x0, y0 + dy, x1, y1 + dy)
    if k < 1: return
    for w_, yy in ((230, 175), (160, 232)):
        rrect(d, x0 + 34, y0 + yy, x0 + 34 + w_, y0 + yy + 40, 20, fill=LG)
    t0 = 0.25
    if t >= t0:
        kb = back((t - t0) / 0.3); prog = clamp((t - 0.45) / (MEND - 0.45))
        vbubble(G, x0 + 34 + 190, y0 + 440, 380, 112, seed=3, prog=prog, live=t if t < MEND + 0.2 else None, k=kb, tail='l')
        if kb > 0.9: text(G, 'сейчас', x0 + 44, y0 + 504, 26, GREY, False, 'l')
    if t >= T['eto'] - 0.05:
        paste(G, plate_img('МАМА ❤', 62, YEL, INK, pad=22), x0 + 265, y0 + 335, back((t - T['eto'] + 0.05) / 0.28), -5)
    if t >= T['golos1']:
        paste(G, plate_img('ГОЛОС ЕЁ', 62, INK, WHITE, pad=20), x0 + 250, y0 + 585, back((t - T['golos1']) / 0.28), 3)
    if t >= T['otkr'] - 0.15:
        kk = eo((t - T['otkr'] + 0.15) / 0.4); top = y1 - 285 * kk
        rrect(d, x0 + 10, top, x1 - 10, y1 - 10, 40, fill=INK)
        if kk > 0.97:
            text(G, 'ПЕРЕВОД · МАМЕ', (x0 + x1) / 2, top + 22, 28, GREY, False)
            text(G, '30 000 ₽', (x0 + x1) / 2, top + 58, 84, WHITE)
            pulse = 1 + 0.05 * math.sin(t * 12) if t >= T['bank'] else 1
            bw = 330 * pulse; bh = 96 * pulse; cx = (x0 + x1) / 2; cy = top + 212
            rrect(d, cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, 30, fill=YEL)
            text(G, 'ОТПРАВИТЬ', cx, cy - 30, 46, INK)
def sc_stop(G, t):
    plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 420, 86, YEL, INK, rot=-3)
    d = ImageDraw.Draw(G)
    # кнопка «отправить» гаснет и зачёркивается
    kk = clamp((t - T['stop'] - 0.35) / 0.3)
    rrect(d, 70, 760, 370, 860, 30, fill=LG if kk > 0.5 else YEL)
    text(G, 'ОТПРАВИТЬ', 220, 782, 42, GREY if kk > 0.5 else INK)
    cross(G, 90, 750, 350, 870, kk, 14)
    text(G, '30 000 ₽', 800, 780, 54, GREY)
def sc_reveal(G, t):
    d = ImageDraw.Draw(G)
    if t < T['sluh'] - 0.3:
        u = clamp((t - T['zapisala']) / 0.5)
        sx = math.cos(math.pi * u); kind = 'mama' if u < 0.5 else 'crook'
        k0 = back((t - B[2]) / 0.3)
        if k0 > 0.1: avatar(G, 540, 440, 150 * min(1, k0), kind, sx if u > 0 else 1.0)
        plate(G, t, T['golos2'], 'ГОЛОС ЕЁ', 225, 300, 54, INK, WHITE, rot=-5, t1=T['zapisala'] + 0.1)
        plate(G, t, T['nemama'] - 0.05, 'НЕ МАМА', 800, 560, 74, RED, WHITE, rot=5)
        return
    if t < T['no'] - 0.05:
        # две одинаковые волны
        for j, (lab, col) in enumerate((('МАМА', YEL), ('НЕ МАМА', RED))):
            tj = T['sluh'] - 0.3 + j * 0.3; kb = back((t - tj) / 0.28); yy = 340 + j * 200
            vbubble(G, 610, yy, 560, 140, seed=3, prog=1.0, live=t, k=kb)
            if kb > 0.5: paste(G, plate_img(lab, 44, col, INK if j == 0 else WHITE, pad=16), 190, yy, kb, -3)
        if t >= T['otlich']: paste(G, plate_img('=', 90, WHITE, INK, pad=14, border=INK), 610, 440, back((t - T['otlich']) / 0.25))
        return
    kk = back((t - T['no'] + 0.05) / 0.3)
    secret(G, 540, 410, kk, False, 5, 1.5)
    plate(G, t, T['slovo1'], 'СЛОВО', 215, 285, 64, INK, WHITE, rot=-5)
    plate(G, t, T['mozhet'] - 0.6, 'НЕ ПОДДЕЛАТЬ', 740, 560, 60, WHITE, INK, rot=3, border=INK)

def steps(G, t, cur, x0=120, y=325):
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y), S(x0 + 360), S(y)], fill=LG, width=S(10))
    for j in range(3):
        x = x0 + j * 180; on = j + 1 <= cur; r = 58 if j + 1 == cur else 46
        d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=YEL if on else WHITE, outline=INK, width=S(7))
        text(G, str(j + 1), x, y - 37, 60, INK if on else GREY)
def sc_how(G, t):
    d = ImageDraw.Draw(G)
    cur = 3 if t >= T['neiro'] - 0.1 else 2 if t >= T['tam'] - 0.1 else 1 if t >= T['vzlomal'] - 0.2 else 0
    k0 = eo((t - B[3]) / 0.3)
    if k0 > 0.2: steps(G, t, cur)
    if cur == 0:
        plate(G, t, T['smotri'], 'КАК ЭТО\nУСТРОЕНО', 330, 620, 70, INK, WHITE, rot=-3)
    elif cur == 1:
        kk = back((t - T['vzlomal'] + 0.2) / 0.3)
        if kk > 0.1:
            phone(G, 130, 430, 530, 1130, 'Мама')
            sh = 10 * math.sin(t * 50) * clamp(1 - (t - T['vzlomal']) / 0.5)
            lock(d, 330 + sh, 800, 3.0, t >= T['vzlomal'] + 0.3, INK, YEL)
            plate(G, t, T['vzlomal'] + 0.25, 'ВЗЛОМ', 330, 1010, 76, RED, WHITE, rot=-4)
    else:
        # старые голосовые -> нейросеть -> новое голосовое
        suck = clamp((t - T['neiro']) / 1.3) if cur == 3 else 0
        for j, lab in enumerate(('12 мая', '3 августа', 'вчера')):
            tj = T['tam'] - 0.1 + j * 0.28
            if t < tj: continue
            u = clamp((suck * 3 - j * 0.6)); kb = back((t - tj) / 0.28)
            x = 330; y = 490 + j * 150
            if u > 0: y = y + (960 - y) * eo(u); kb = 1 - 0.75 * eo(u)
            if u < 1: vbubble(G, x, y, 400, 104, seed=5 + j, prog=1.0, k=kb, label=lab if u == 0 else None, fill=DG)
        if cur == 3:
            kc = back((t - T['neiro'] + 0.1) / 0.3); cx, cy = 330, 960
            if kc > 0.1:
                w = 360 * kc; h = 150 * kc
                for j in range(5):
                    xx = cx - w / 2 + 40 + j * (w - 80) / 4
                    d.line([S(xx), S(cy - h / 2 - 22), S(xx), S(cy + h / 2 + 22)], fill=INK, width=S(8))
                rrect(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 24, fill=INK)
                text(G, 'НЕЙРОСЕТЬ', cx, cy - 34 * kc, 46 * kc, YEL)
                if suck > 0.2 and t < T['skazat']:
                    for j in range(3):
                        a = (t * 3 + j / 3) % 1
                        d.ellipse([S(cx - 130 + j * 130 - 8), S(cy + 52 - 8), S(cx - 130 + j * 130 + 8), S(cy + 52 + 8)], fill=YEL if a < 0.5 else DG)
            if t >= T['skazat']:
                u = eo((t - T['skazat']) / 0.45)
                vbubble(G, 330, 990 + 150 * u, 440, 116, seed=3, prog=1.0, live=t, k=0.4 + 0.6 * u)
                plate(G, t, T['ugodno'] - 0.5, '«СРОЧНО ПЕРЕВЕДИ»', 325, 1258, 38, YEL, INK, rot=-2)
            if T['obrazca'] - 0.6 <= t < T['skazat'] + 0.3: vbubble(G, 330, 640, 260, 96, seed=5, prog=1.0, k=back((t - T['obrazca'] + 0.6) / 0.28), fill=DG)
            plate(G, t, T['obrazca'] - 0.6, 'КОРОТКИЙ ОБРАЗЕЦ', 345, 520, 40, WHITE, INK, rot=-3, border=INK, t1=T['skazat'] + 0.3)
def toggle(G, cx, cy, on, k=1.0):
    d = ImageDraw.Draw(G); w = 190 * k; h = 96 * k
    col = tuple(int(a + (b - a) * on) for a, b in zip(LG, YEL))
    rrect(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=col, outline=INK, width=7)
    kx = cx - w / 2 + h / 2 + (w - h) * on; r = h / 2 - 12
    d.ellipse([S(kx - r), S(cy - r), S(kx + r), S(cy + r)], fill=WHITE, outline=INK, width=S(7))
def sc_main(G, t):
    d = ImageDraw.Draw(G)
    if t < T['rodnoy'] - 0.05:
        k0 = back((t - B[4]) / 0.3)
        if k0 > 0.1:
            r = 70 * k0 * (1 + 0.06 * math.sin(t * 10))
            d.ellipse([S(540 - r), S(380 - r), S(540 + r), S(380 + r)], fill=YEL, outline=INK, width=S(8))
            text(G, '3', 540, 380 - 50 * k0, 80 * k0, INK)
        plate(G, t, T['glavnoe'], 'ГЛАВНОЕ', 540, 540, 70, INK, WHITE, rot=-3)
        return
    if t < T['nedum'] - 0.25:
        plate(G, t, T['rodnoy'] - 0.05, 'РОДНОЙ ГОЛОС', 400, 320, 62, WHITE, INK, rot=-3, border=INK)
        plate(G, t, T['plus'], '+', 540, 432, 70, INK, WHITE)
        plate(G, t, T['srochno'] - 0.1, 'СРОЧНО!', 680, 545, 78, RED, WHITE, rot=3)
        if t >= T['perest'] - 0.3:
            kk = back((t - T['perest'] + 0.3) / 0.3); on = 1 - eo((t - T['perest'] - 0.15) / 0.25)
            if kk > 0.1:
                toggle(G, 205, 800, on, kk * 1.5)
                text(G, 'ПРОВЕРКА', 205, 890, 46, INK)
                text(G, 'ВКЛ' if on > 0.5 else 'ВЫКЛ', 205, 948, 60, INK if on > 0.5 else RED)
        return
    plate(G, t, T['nedum'] - 0.2, 'ТЫ НЕ ДУМАЕШЬ', 540, 310, 56, LG, DG, rot=-2)
    plate(G, t, T['spas'] - 0.1, 'ТЫ СПАСАЕШЬ\nМАМУ', 540, 500, 72, YEL, INK, rot=2)
    if t >= T['spas'] - 0.1:
        s = back((t - T['spas'] + 0.1) / 0.3) * (1 + 0.1 * abs(math.sin(t * 7)))
        heart(d, 850, 820, 1.25 * s); heart(d, 215, 880, 0.8 * s)
def yesno(G, t, t0, sel=None, y=930):
    for j, (lab, x) in enumerate((('ДА', 225), ('НЕТ', 825))):
        kb = back((t - t0 - j * 0.15) / 0.28)
        if kb <= 0.05: continue
        kb *= 1 + 0.05 * math.sin(t * 8 + j * 2)
        paste(G, plate_img(lab, 86, WHITE, INK, pad=34, border=INK), x, y, kb, -4 + j * 8)
def sc_quiz(G, t):
    plate(G, t, B[5] + 0.05, 'ТЫ БЫ\nОТЛИЧИЛ?', 540, 400, 84, INK, WHITE, rot=-3)
    yesno(G, t, T['uslyshal'])
    plate(G, t, T['zapomni'], 'ЗАПОМНИ ОТВЕТ', 540, 590, 48, YEL, INK, rot=3)
def sc_fix(G, t):
    d = ImageDraw.Draw(G); CX = 690
    plate(G, t, T['delat'] - 0.5, 'ЧТО ДЕЛАТЬ?', CX, 335, 58, YEL, INK, rot=-3, t1=T['netslova'] - 0.1)
    if t < T['netslova'] - 0.1:
        if t >= T['perezvoni']:
            kk = back((t - T['perezvoni']) / 0.28)
            if kk > 0.1:
                rrect(d, CX - 225 * kk, 520 - 85 * kk, CX + 225 * kk, 520 + 85 * kk, 26, fill=WHITE, outline=INK, width=7)
                d.ellipse([S(CX - 200), S(520 - 58), S(CX - 84), S(520 + 58)], fill=YEL)
                handset(G, CX - 142, 520, 0.5 * kk)
                text(G, 'ПЕРЕЗВОНИ', CX + 60, 462, 42 * kk, INK); text(G, 'САМ', CX + 60, 516, 42 * kk, INK)
        if t >= T['pridum'] - 0.1:
            kk = back((t - T['pridum'] + 0.1) / 0.28); cy = 790
            if kk > 0.1:
                rrect(d, CX - 225 * kk, cy - 150 * kk, CX + 225 * kk, cy + 150 * kk, 26, fill=WHITE, outline=INK, width=7)
                text(G, 'КОДОВОЕ СЛОВО', CX, cy - 130, 40 * kk, INK)
                if t >= T['kodovoe']: secret(G, CX, cy - 10, back((t - T['kodovoe']) / 0.28), True, 5, 0.82)
                for j in range(3):
                    if t >= T['pridum'] + j * 0.12: person(d, CX - 80 + j * 80, cy + 138, 0.62 + (0.12 if j == 1 else 0))
        if t >= T['egonet']:
            # лента переписки: слова там нет
            kk = eo((t - T['egonet']) / 0.3); y0, y1 = 975, 1270
            rrect(d, CX - 225, y0, CX + 225, y0 + (y1 - y0) * kk, 26, fill=WHITE, outline=INK, width=7)
            if kk >= 1:
                off = (t - T['egonet']) * 150
                for j in range(9):
                    yy = y0 + 30 + ((j * 52 - off) % 468) - 100
                    if y0 + 22 < yy < y1 - 50:
                        left = j % 3 != 0; wv = 150 + (j * 53) % 130
                        xa = CX - 200 if left else CX + 200 - wv
                        rrect(d, xa, yy, xa + wv, yy + 34, 17, fill=LG if left else (255, 236, 140))
                plate(G, t, T['ukrast'] - 0.3, 'НЕ УКРАСТЬ', CX, 1125, 54, INK, WHITE, rot=-4)
        return
    plate(G, t, T['netslova'] - 0.1, 'НЕТ СЛОВА', CX, 420, 76, YEL, INK, rot=-3)
    if t >= T['perevoda'] - 0.45:
        kk = back((t - T['perevoda'] + 0.45) / 0.28)
        text(G, '↓', CX, 505, 90, INK)
        paste(G, plate_img('НЕТ ПЕРЕВОДА', 78, INK, WHITE, pad=28), CX, 700, kk, 3)
        rrect(d, CX - 165, 860, CX + 165, 960, 30, fill=LG)
        text(G, 'ОТПРАВИТЬ', CX, 882, 42, GREY)
        cross(G, CX - 150, 850, CX + 150, 970, clamp((t - T['perevoda']) / 0.3), 14)
def sc_wow(G, t):
    d = ImageDraw.Draw(G)
    if t < T['golos3'] - 0.05:
        plate(G, t, T['teper'] - 0.1, 'ТВОЙ ОТВЕТ?', 540, 400, 84, INK, WHITE, rot=-3)
        yesno(G, t, T['teper'] + 0.2)
        return
    # волна у рта человечка: тот же пузырь, что был у «мамы»
    kb = back((t - T['golos3'] + 0.05) / 0.3)
    vbubble(G, 775, 735, 290, 104, seed=3, prog=1.0, live=t, k=kb, tail='l')
    plate(G, t, T['golos3'], 'ЭТОТ ГОЛОС', 540, 305, 60, WHITE, INK, rot=-3, border=INK)
    if t >= T['sdelala'] - 0.1:
        kk = back((t - T['sdelala'] + 0.1) / 0.3)
        paste(G, plate_img('СДЕЛАЛА\nНЕЙРОСЕТЬ', 100, YEL, INK, pad=30), 540, 515, kk * (1 + 0.02 * math.sin(t * 9)), 2)
    plate(G, t, T['zametil'], 'ЗАМЕТИЛ?', 235, 850, 58, INK, WHITE, rot=-4)
def sc_final(G, t):
    d = ImageDraw.Draw(G)
    if t < T['vsyo'] - 0.1:
        plate(G, t, T['vot'], 'МАМА ТОЖЕ\nНЕ ЗАМЕТИТ', 540, 380, 74, INK, WHITE, rot=-3)
        if t >= T['pereshli'] - 0.1:
            kk = back((t - T['pereshli'] + 0.1) / 0.3)
            paste(G, plate_img('ПЕРЕШЛИ ЕЙ  →', 66, YEL, INK, pad=26), 540, 585, kk, 3)
            avatar(G, 860, 830, 70 * min(1, kk), 'mama')
            vbubble(G, 215, 830, 290, 96, seed=3, prog=1.0, live=t, k=kk)
    else:
        plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 420, 112, YEL, INK, rot=-4)

SC = [sc_intro, sc_stop, sc_reveal, sc_how, sc_main, sc_quiz, sc_fix, sc_wow, sc_final]
def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    k = max(j for j in range(len(B)) if B[j] <= t)
    SC[k](G, t)
    return G.resize((WD, GH), Image.LANCZOS)

# ---------- субтитры: до двух строк, под человечком ----------
SUBF = ImageFont.truetype(FB, 56); SP = 14; MAXW = 780
_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
def clean(w): return w.upper().strip('«»')
def wlen(w): return _d.textbbox((0, 0), clean(w[0]), font=SUBF)[2]
def wrap(ws):
    lines, cur, cw = [], [], 0
    for w in ws:
        l = wlen(w)
        if cur and cw + SP + l > MAXW: lines.append(cur); cur, cw = [], 0
        cw = l if not cur else cw + SP + l; cur.append(w)
    if cur: lines.append(cur)
    return lines
def group(WL):
    groups, cur = [], []
    for w in WL:
        if cur and (len(wrap(cur + [w])) > 2 or len(cur) >= 7): groups.append(cur); cur = []
        cur.append(w)
        if w[0].rstrip('»')[-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 3): groups.append(cur); cur = []
    if cur: groups.append(cur)
    for i in range(1, len(groups)):   # не оставляем одно слово-сироту после разрыва посреди фразы
        p = groups[i - 1]
        if len(groups[i]) == 1 and len(p) > 2 and p[-1][0].rstrip('»')[-1] not in '.!?,:': groups[i].insert(0, p.pop())
    return groups
groups = group([tuple(w) for w in MW]) + group(W)
def subs(img, t, y0):
    g = next((g for i, g in enumerate(groups) if g[0][1] - 0.05 <= t < min(g[-1][2] + 0.5, groups[i + 1][0][1] - 0.05 if i + 1 < len(groups) else 1e9)), None)
    if not g: return
    d = ImageDraw.Draw(img); lines = wrap(g)
    y = y0 if len(lines) == 1 else y0 - 37
    for ln in lines:
        ws = [wlen(w) for w in ln]; x = (WD - (sum(ws) + SP * (len(ws) - 1))) / 2
        for w, wd in zip(ln, ws):
            if w[1] <= t < w[2] + 0.15: d.rounded_rectangle([x - 9, y - 6, x + wd + 9, y + 70], radius=12, fill=YEL)
            d.text((x, y), clean(w[0]), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

CH_CROP = (0, 60, 1080, 1660)
SUB_Y = 1410; FEET = 1335
DEF = (540, FEET, 0.45); LEFT = (255, FEET, 0.5); RIGHT = (830, FEET, 0.44)
LAY = [(0, *LEFT), (B[1], *DEF), (B[2], *DEF), (B[3], *RIGHT), (B[4], *DEF), (B[5], *DEF), (B[6], *LEFT), (B[7], *DEF), (B[8], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:], cur[1:]))

def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    cx, feet, s = layout(t)
    G = graphics(t)
    bg.paste(G, (0, 0), G)
    subs(bg, t, SUB_Y)
    bot = feet + 70 * s; cw, chh = int(1080 * s), int(1600 * s)
    try: ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    except FileNotFoundError: ch = Image.new('RGB', (cw, chh), WHITE)
    layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (int(cx - cw / 2 + xoff[i]), int(bot - chh)))
    img = (np.asarray(bg, np.float32) * np.asarray(layer, np.float32) / 255)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
def fbytes(i): return frame(i).tobytes()

if __name__ == '__main__':
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        with Pool(4) as pool:
            for i, b in enumerate(pool.imap(fbytes, range(N), chunksize=8)):
                p.stdin.write(b)
                if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
