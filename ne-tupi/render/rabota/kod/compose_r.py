"""Монтаж: фон + графика (PIL, 2x суперсэмплинг) + персонаж (multiply) -> ffmpeg."""
import json, math, sys, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageChops
from words import W, wt, B, DUR
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
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:') == word.lower()]
    return hits[k][1]
T = dict(rabotu=wt('работу'), zavtra=wt('завтра'), dumaesh=wt('Думаешь'), slabak=wt('слабак'), stop=wt('Стоп'),
         dver=wexact('дверь', 0), uchenye=wexact('учёные', 0), priznali=wt('признали'), naoborot=wt('наоборот'),
         god=wt('Шестьдесят'), selig=wt('Селигман'), sobaki=wt('Собаки'), tokom=wt('током'), barer=wt('барьер'), pereprygni=wt('перепрыгни'),
         svoboden=wt('свободен'), lozhilis=wt('ложились'), nazvali=wt('назвали'), uznal=wt('Узнал'), rezyume=wexact('резюме', 0), tishina=wt('тишина'),
         nichego=wt('ничего'), dumali=wt('думали'), pravda=wt('правда'), cherez=wt('Через'), terpet=wexact('терпеть'), zavod=wt('заводская'),
         drugoe=wt('другое'), vliyaesh=wexact('влияешь', 0), delat=wt('делать'), smelost=wt('Смелость'), nuzhen=wt('Нужен'), nedelyu=wt('неделю'),
         rez2=wexact('резюме', 1), sozvon=wt('Созвон'), sobes=wt('Собеседование'), kazhdy=wt('Каждый'), vliyaesh2=wexact('влияешь', 1),
         tolko=wt('Только'), kuda=wt('куда'), dver2=wexact('дверь', 1), otkryta2=wexact('открыта', 1), vsyo=wexact('всё', 3), netupi=wexact('тупи'))
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

def sc_intro(G, t):
    d = ImageDraw.Draw(G)
    k = back(t / 0.3); cx, cy = 230, 400
    if k > 0.1:
        sh = 8 * math.sin(t * 60) if t < 1.6 else 0
        for ex in (-1, 1):
            d.ellipse([S(cx + ex * 120 - 45 + sh), S(cy - 185), S(cx + ex * 120 + 45 + sh), S(cy - 105)], fill=INK)
        d.ellipse([S(cx - 150 + sh), S(cy - 150), S(cx + 150 + sh), S(cy + 150)], fill=WHITE, outline=INK, width=S(14))
        big_text(G, '07:00', cx + sh, cy - 48, 80, RED)
    x0, x1, top, bot = 700, 960, 150, 960
    d.rectangle([S(x0 - 20), S(top - 20), S(x1 + 20), S(bot)], fill=LG)
    d.rectangle([S(x0), S(top), S(x1), S(bot)], fill=WHITE, outline=INK, width=S(10))
    d.ellipse([S(x0 + 26), S(560), S(x0 + 62), S(596)], fill=YEL, outline=INK, width=S(5))
    paste(G, plate_img('ОФИС', 60, INK, WHITE, pad=20), (x0 + x1) / 2, 260)
    if t >= T['zavtra']:
        for j in range(3):
            tj = T['zavtra'] + j * 0.45
            if t >= tj: paste(G, plate_img('ПН', 80, WHITE, INK, pad=28, border=INK), 420 + j * 95, 640 + j * 22, back((t - tj) / 0.25), -6 + j * 5)
    if t >= T['dumaesh']:
        paste(G, plate_img('СЛАБАК?', 90, LG, GREY, pad=26), 560, 880, back((t - T['dumaesh']) / 0.3), -3)
def sc_stop(G, t):
    plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 300, 84, YEL, INK, rot=-3)
    paste(G, plate_img('СЛАБАК', 80, LG, GREY, pad=24), 300, 620, 1.0, 2)
    cross(G, 110, 570, 490, 670, clamp((t - T['stop'] - 0.4) / 0.3))
def sc_door(G, t):
    plate(G, t, T['dver'] - 0.05, 'ДВЕРЬ ОТКРЫТА', 540, 100, 84, YEL, INK, rot=-3)
    if t >= T['uchenye']:
        d = ImageDraw.Draw(G); k = eo((t - T['uchenye']) / 0.6)
        d.line([S(200), S(260), S(200 + 680 * k), S(260)], fill=INK, width=S(10))
        paste(G, plate_img('1967', 54, INK, WHITE, pad=20), 200, 260, back((t - T['uchenye']) / 0.25))
        if k >= 1: paste(G, plate_img('2016', 54, INK, WHITE, pad=20), 880, 260, back((t - T['uchenye'] - 0.6) / 0.25))
    plate(G, t, T['naoborot'] - 0.1, '↺ НАОБОРОТ', 700, 400, 68, YEL, INK, rot=4)

def dog(G, cx, cy, lying=0.0, sc=1.0):
    """силуэт собаки-пиктограммы; lying 0..1 — ложится"""
    d = ImageDraw.Draw(G); s = sc
    leg = 70 * (1 - lying) * s; by = cy - leg
    d.rounded_rectangle([S(cx - 110 * s), S(by - 55 * s), S(cx + 90 * s), S(by + 10 * s)], radius=S(30 * s), fill=INK)
    hy = by - 40 * s + 30 * lying * s
    d.ellipse([S(cx + 60 * s), S(hy - 50 * s), S(cx + 150 * s), S(hy + 35 * s)], fill=INK)
    d.polygon([(S(cx + 140 * s), S(hy - 10 * s)), (S(cx + 185 * s), S(hy + 5 * s)), (S(cx + 140 * s), S(hy + 25 * s))], fill=INK)
    d.ellipse([S(cx + 62 * s), S(hy - 40 * s), S(cx + 92 * s), S(hy + 30 * s)], fill=INK)
    ta = 35 - 75 * lying
    d.line([S(cx - 105 * s), S(by - 40 * s), S(cx - 105 * s - 60 * s * math.cos(math.radians(ta))), S(by - 40 * s - 60 * s * math.sin(math.radians(ta)))], fill=INK, width=S(14 * s))
    if leg > 4:
        for lx in (-85, -55, 45, 70):
            d.rounded_rectangle([S(cx + lx * s), S(by), S(cx + (lx + 20) * s), S(cy)], radius=S(8), fill=INK)
def sc_dogs(G, t):
    plate(G, t, T['god'], '1967 · Селигман и Майер', 520, 90, 60, INK, WHITE, rot=-2)
    if t < T['sobaki'] - 0.1: return
    d = ImageDraw.Draw(G); k = eo((t - T['sobaki'] + 0.1) / 0.35)
    x0, x1, top, bot = 30, 1050, 190, 830
    d.rectangle([S(x0), S(top), S(x0 + (x1 - x0) * k), S(bot)], fill=WHITE, outline=INK, width=S(8))
    if k < 1: return
    lying = clamp((t - T['lozhilis']) / 0.6)
    dog(G, 280, bot - 20, lying, 1.5)
    if T['tokom'] - 0.4 <= t < T['barer']:   # серая молния, мигает
        if int(t * 8) % 2 == 0:
            d.polygon([(S(x*1.4-60), S(y*1.1)) for x, y in ((250, 240), (200, 400), (250, 400), (205, 540), (330, 360), (275, 360), (320, 240))], fill=GREY)
    if t >= T['barer']:
        h = 110 * back((t - T['barer']) / 0.3)
        d.rectangle([S(600), S(bot - h * 1.4), S(640), S(bot)], fill=YEL, outline=INK, width=S(5))
        d.line([S(640), S(bot), S(1050), S(bot)], fill=INK, width=S(6))
    if t >= T['pereprygni']:
        a = clamp((t - T['pereprygni']) / 0.5); d = ImageDraw.Draw(G)
        pts = [(S(470 + 360 * u), S(bot - 230 - 250 * math.sin(math.pi * u))) for u in [i / 20 * a for i in range(21)]]
        d.line(pts, fill=YEL, width=S(14))
        if a >= 1: paste(G, plate_img('ПЕРЕПРЫГНИ', 60, YEL, INK, pad=20), 760, 300, 1.0, 3)
    if t >= T['svoboden']: paste(G, plate_img('СВОБОДА', 56, WHITE, INK, pad=18, border=INK), 880, 760, back((t - T['svoboden']) / 0.25))
    if t >= T['lozhilis'] + 0.3: paste(G, plate_img('…И ТЕРПЕЛИ', 70, INK, WHITE, pad=22), 330, 560, back((t - T['lozhilis'] - 0.3) / 0.3), -2)
def sc_help(G, t):
    plate(G, t, T['nazvali'], 'ВЫУЧЕННАЯ\nБЕСПОМОЩНОСТЬ', 540, 150, 70, INK, WHITE, rot=-2, t1=T['uznal'] - 0.1)
    if t >= T['rezyume']:
        for j in range(3):
            u = clamp((t - T['rezyume'] - j * 0.25) / 0.9)
            if 0 < u < 1:
                d = ImageDraw.Draw(G); x = 300 + 500 * u; y = 520 - 380 * u
                paste(G, plate_img('РЕЗЮМЕ', 70, WHITE, INK, pad=18, border=INK), x, y, 1 - 0.4 * u, -20 * u)
    if t >= T['tishina']: paste(G, plate_img('…', 80, WHITE, GREY, pad=22, border=LG), 800, 160, back((t - T['tishina']) / 0.25))
    plate(G, t, T['nichego'] - 0.2, '«Я НИЧЕГО\nНЕ УМЕЮ»', 290, 330, 64, LG, INK, rot=-3)
def gear(G, cx, cy, r, ang):
    d = ImageDraw.Draw(G)
    for k in range(10):
        a = ang + k * math.pi / 5
        pts = [(S(cx + (r + 26) * math.cos(a + o)), S(cy + (r + 26) * math.sin(a + o))) for o in (-0.15, 0.15)] + \
              [(S(cx + (r - 4) * math.cos(a + o)), S(cy + (r - 4) * math.sin(a + o))) for o in (0.22, -0.22)]
        d.polygon(pts, fill=INK)
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=INK)
    d.ellipse([S(cx - r * .35), S(cy - r * .35), S(cx + r * .35), S(cy + r * .35)], fill=BG)
def sc_twist(G, t):
    if t < T['cherez'] - 0.1:
        paste(G, plate_img('ВЫУЧЕННАЯ\nБЕСПОМОЩНОСТЬ', 60, INK, WHITE, pad=28), 540, 160, 1.0, -2)
        if t >= T['dumali']:
            d = ImageDraw.Draw(G); k = clamp((t - T['dumali']) / 0.4)
            pts = [(260, 90), (420, 200), (520, 110), (650, 230), (820, 120)]
            n = 1 + int(k * (len(pts) - 1))
            d.line([(S(x), S(y)) for x, y in pts[:n + 1]], fill=RED, width=S(12))
        plate(G, t, T['pravda'], 'ЭТО ПРАВДА?', 540, 420, 70, YEL, INK, rot=3)
        return
    plate(G, t, T['cherez'] - 0.1, '2016 · те же учёные', 540, 70, 56, INK, WHITE, rot=-2)
    if T['terpet'] <= t < T['zavod'] - 0.1:
        paste(G, plate_img('ТЕРПЕТЬ\nНЕ УЧАТСЯ', 76, WHITE, INK, pad=26, border=INK), 540, 280, back((t - T['terpet']) / 0.25))
    if T['zavod'] - 0.1 <= t < T['drugoe'] - 0.3:
        s_ = back((t - T['zavod'] + 0.1) / 0.3)
        if s_ > 0.1: gear(G, 190, 290, 95 * s_, t * 0.8)
        paste(G, plate_img('ЗАВОДСКАЯ\nНАСТРОЙКА', 70, LG, INK, pad=24), 610, 290, s_)
    if t >= T['drugoe'] - 0.3:
        d = ImageDraw.Draw(G); k = eo((t - T['drugoe'] + 0.3) / 0.4)
        d.line([S(170), S(430), S(170), S(430 - 200 * k)], fill=YEL, width=S(34))
        if k >= 1: d.polygon([(S(110), S(240)), (S(230), S(240)), (S(170), S(160))], fill=YEL)
        plate(G, t, T['drugoe'] - 0.3, 'УЧИТСЯ:\nЯ ВЛИЯЮ', 600, 300, 84, YEL, INK, rot=-2)
def sc_fix(G, t):
    if t < T['nuzhen'] - 0.05:
        plate(G, t, T['delat'] - 0.5, 'ЧТО ДЕЛАТЬ?', 540, 150, 84, YEL, INK, rot=-3)
        if t >= T['smelost']:
            paste(G, plate_img('СМЕЛОСТЬ', 80, WHITE, INK, pad=26, border=INK), 540, 340, back((t - T['smelost']) / 0.25))
            cross(G, 300, 270, 780, 410, clamp((t - T['smelost'] - 0.35) / 0.3))
        return
    plate(G, t, T['nuzhen'] - 0.05, '1 ШАГ В НЕДЕЛЮ', 540, 75, 66, YEL, INK, rot=-2, t1=T['tolko'] - 0.15)
    labs = [('резюме', T['rez2']), ('созвон', T['sozvon']), ('собес', T['sobes'])]
    n = 0
    for j, (lab, tj) in enumerate(labs):
        x = 230 + j * 310
        card(G, x, 255, 270, 190)
        ImageDraw.Draw(G).text((S(x - 110), S(172)), f'неделя {j + 1}', font=font(30, False), fill=GREY)
        if t >= tj:
            n += 1; d = ImageDraw.Draw(G); k = clamp((t - tj) / 0.25)
            d.line([(S(x - 60), S(245)), (S(x - 20), S(285))][:2], fill=INK, width=S(16)) if k > 0.3 else None
            if k > 0.6: d.line([(S(x - 20), S(285)), (S(x + 60), S(200))], fill=INK, width=S(16))
            big_text(G, lab, x, 295, 40, INK)
    # шкала «Я ВЛИЯЮ»
    lvl = clamp(n / 3 * 0.75 + (0.25 * clamp((t - T['vliyaesh2']) / 0.4)))
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(150), S(385), S(930), S(445)], radius=S(30), fill=WHITE, outline=INK, width=S(6))
    if lvl > 0.02: d.rounded_rectangle([S(156), S(391), S(156 + 768 * lvl), S(439)], radius=S(26), fill=YEL)
    big_text(G, 'Я ВЛИЯЮ', 540, 389, 38, INK)
    if t >= T['tolko']: paste(G, plate_img('СНАЧАЛА НАШЁЛ,\nПОТОМ УШЁЛ', 52, INK, WHITE, pad=20), 540, 80, back((t - T['tolko']) / 0.25), -2)
def sc_final(G, t):
    if t < T['vsyo'] - 0.1:
        plate(G, t, T['dver2'], 'ДВЕРЬ БЫЛА ОТКРЫТА', 540, 150, 62, YEL, INK, rot=-3)
    else:
        plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 300, 110, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_intro(G, t)
    elif t < B[2]: sc_stop(G, t)
    elif t < B[3]: sc_door(G, t)
    elif t < B[4]: sc_dogs(G, t)
    elif t < B[5]: sc_help(G, t)
    elif t < B[6]: sc_twist(G, t)
    elif t < B[7]: sc_fix(G, t)
    else: sc_final(G, t)
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
OUT = (790, FEET, 0.45, 190, 0.72)
LAY = [(0, *LEFT), (B[1], *DEF), (B[2], *DEF), (B[3], *RIGHT), (B[4], *DEF), (B[5], *DEF), (B[6], *DEF), (T['dver2'], *OUT)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; dur = 1.6 if k == len(LAY) - 1 else 0.45; e = eo((t - cur[0]) / dur)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]

def cage_on(t):
    if B[2] <= t < B[3]: return eo((t - T['dver'] + 0.1) / 0.35) if t >= T['dver'] - 0.1 else 0
    if B[4] <= t < B[6]: return eo((t - T['uznal'] + 0.1) / 0.35) if t >= T['uznal'] - 0.1 else 0
    if t >= B[6]: return 1
    return 0
def cage(img, t, k):
    """клетка вокруг человечка в центре, дверца справа распахнута; k — проявление"""
    d = ImageDraw.Draw(img); cx, top, bot, hw = 540, 600, 1360, 235
    col = tuple(int(255 - (255 - c) * k) for c in INK)
    d.rectangle([cx - hw - 10, bot - 6, cx + hw + 10, bot + 10], fill=col)
    d.rectangle([cx - hw - 10, top - 10, cx + hw + 10, top + 6], fill=col)
    d.pieslice([cx - 120, top - 70, cx + 120, top + 70], 180, 360, fill=None, outline=col, width=10)
    gap0 = cx + hw - 150   # проём двери справа
    x = cx - hw
    while x <= cx + hw + 1:
        if not (gap0 < x < cx + hw): d.line([x, top, x, bot], fill=col, width=10)
        x += 58
    # дверца: распахнута наружу (параллелограмм справа)
    hx = cx + hw; w = 125
    d.polygon([(hx, top + 10), (hx + w, top + 50), (hx + w, bot - 40), (hx, bot)], outline=col, width=9)
    for j in (1, 2):
        xx = hx + w * j / 3
        d.line([xx, top + 10 + 40 * j / 3, xx, bot - 40 * j / 3], fill=col, width=8)
    if k > 0.9 and B[6] <= t: pass
def door2(img, t):
    if t < T['tolko']: return
    k = back((t - T['tolko']) / 0.3); d = ImageDraw.Draw(img)
    x0, x1, top, bot = 830, 935, 1060, 1360
    h = (bot - top) * k
    d.rectangle([x0, bot - h, x1, bot], fill=WHITE, outline=INK, width=7)
    if k > 0.9:
        d.ellipse([x0 + 12, bot - 160, x0 + 30, bot - 142], fill=YEL, outline=INK, width=3)
        f = ImageFont.truetype(FB, 22); d.text((x0 + 8, top - 10 + 0), '', font=f, fill=INK)
def key(img, t, cx, cy):
    if t < T['kazhdy'] or t >= B[7] + 0.0 and False: return
    k = back((t - T['kazhdy']) / 0.3); d = ImageDraw.Draw(img); s = 1.0 * k
    if s < 0.1: return
    d.ellipse([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s], fill=YEL, outline=INK, width=6)
    d.ellipse([cx - 12 * s, cy - 12 * s, cx + 12 * s, cy + 12 * s], fill=BG, outline=INK, width=4)
    d.rectangle([cx + 30 * s, cy - 9 * s, cx + 120 * s, cy + 9 * s], fill=YEL, outline=INK, width=5)
    d.rectangle([cx + 90 * s, cy + 6 * s, cx + 104 * s, cy + 30 * s], fill=YEL, outline=INK, width=4)
def hud(img, t):
    vis = t < B[1] or (B[7] <= t < T['vsyo'])
    if not vis: return
    im = plate_img('ТЕРПИШЬ: 5 ЛЕТ', 34, INK, WHITE, pad=16).resize((0, 0)) if False else plate_img('ТЕРПИШЬ: 5 ЛЕТ', 34, INK, WHITE, pad=16)
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    img.paste(im, (60, 262), im)
    if t >= B[7]:
        k = clamp((t - T['otkryta2']) / 0.3); d = ImageDraw.Draw(img)
        if k > 0: d.line([60, 262 + im.height / 2, 60 + im.width * k, 262 + im.height / 2], fill=RED, width=8)

def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    cx, feet, s, gy, gs = layout(t)
    G = graphics(t)
    if gs != 1: G = G.resize((int(WD * gs), int(GH * gs)), Image.LANCZOS)
    bg.paste(G, (int((WD - G.width) / 2), int(gy)), G)
    k = cage_on(t)
    if k > 0: cage(bg, t, k)
    if B[6] <= t: door2(bg, t)
    if B[6] <= t < B[7]: key(bg, t, cx + 150, 1010)
    hud(bg, t)
    subs(bg, t, SUB_Y)
    bot = feet + 70 * s; cw, chh = int(1080 * s), int(1600 * s)
    ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (int(cx - cw / 2 + xoff[i]), int(bot - chh)))
    img = (np.asarray(bg, np.float32) * np.asarray(layer, np.float32) / 255)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

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
