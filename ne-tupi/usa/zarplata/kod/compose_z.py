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

@lru_cache(None)
def cup_img(h):
    w = int(h * 0.8); im = Image.new('RGBA', (S(w + 40), S(h + 120)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, oy = S(20), S(100); H = S(h); Wt = S(w)
    top, bot = Wt * 0.86, Wt * 0.66; cx = ox + Wt / 2
    d.polygon([(cx - top / 2, oy + H * 0.14), (cx + top / 2, oy + H * 0.14), (cx + bot / 2, oy + H), (cx - bot / 2, oy + H)], fill=INK)
    d.rounded_rectangle([cx - Wt / 2, oy, cx + Wt / 2, oy + H * 0.16], radius=S(10), fill=INK)
    sy0, sy1 = oy + H * 0.42, oy + H * 0.68
    def xat(y): return top / 2 + (bot / 2 - top / 2) * (y - oy - H * 0.14) / (H * 0.86)
    d.polygon([(cx - xat(sy0), sy0), (cx + xat(sy0), sy0), (cx + xat(sy1), sy1), (cx - xat(sy1), sy1)], fill=YEL)
    for k in (-1, 0, 1):   # пар
        x = cx + k * Wt * 0.22
        for j in range(3):
            d.arc([x - S(14), oy - S(90) + j * S(28), x + S(14), oy - S(62) + j * S(28)], 90 if j % 2 else 270, 270 if j % 2 else 90, fill=(170, 170, 170), width=S(5))
    return im
def cup(G, cx, cy, h, scale=1.0, rot=0, alpha=1.0):
    paste(G, cup_img(h), cx, cy - 20 * scale, scale, rot, alpha)

# ---------- сцены «Зарплата» ----------
import random
T = {k: wt(*v) if isinstance(v, tuple) else wt(v) for k, v in dict(
    zp=('Payday', 0), gde=('Where', 0), stop='Stop', kuda=('Where', 1), perv='first', d1='one:', d2='two:', d3='three:',
    dumaesh='Think', net='Nope', dva='Double', budet='same', dorozhe='expensive', kopish='save', togo=("whatever's", 0), ost=('left', 0),
    nol1=('zero', 0), naob='Flip', desyat='ten', postav='Better', avto='automatic', shest=('four', 1),
    sem='Forty-eight', bez=('zero', 1), snach=('pay', 4), potom='Everybody', ost2=("whatever's", 1), nol2=('zero', 2), vsegda=('always', 1),
    vsyo=("That's", 1), netupi=('dumb.', 1)).items()}
def rub(v): return f'${int(round(v / 10) * 10):,}'
def big_text(G, txt, cx, y, sz, col=INK, shake=0):
    d = ImageDraw.Draw(G); f = font(sz); bb = d.textbbox((0, 0), txt, font=f)
    d.text((S(cx + shake) - (bb[2] - bb[0]) / 2, S(y)), txt, font=f, fill=col)
def counter(t, t0, a, b, dur=1.0): return a + (b - a) * eo((t - t0) / dur)
def phone_frame(G, cx, cy, w=520, h=820):
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(60), fill=INK)
    d.rounded_rectangle([S(cx - w / 2 + 18), S(cy - h / 2 + 18), S(cx + w / 2 - 18), S(cy + h / 2 - 18)], radius=S(44), fill=WHITE)
    return d
def confetti(G, t, t0):
    if t < t0: return
    d = ImageDraw.Draw(G); rnd = random.Random(5); k = t - t0
    for j in range(70):
        x = rnd.uniform(60, 1020) + math.sin(k * 3 + j) * 20; y = -40 + rnd.uniform(0, 300) + k * rnd.uniform(250, 420)
        if y > 980: continue
        c = rnd.choice([YEL, INK, RED]); r = rnd.uniform(8, 14)
        d.rectangle([S(x - r), S(y - r / 2), S(x + r), S(y + r / 2)], fill=c)
def bags(G, cx, cy, sc=1.0):
    if sc <= 0.01: return
    d = ImageDraw.Draw(G)
    for dx, w, h, col in ((-70, 170, 200, INK), (70, 150, 170, INK)):
        x, y = cx + dx * sc, cy + (200 - h) / 2 * sc
        d.arc([S(x - 40 * sc), S(y - h / 2 * sc - 50 * sc), S(x + 40 * sc), S(y - h / 2 * sc + 30 * sc)], 180, 360, fill=INK, width=S(10 * sc))
        d.rounded_rectangle([S(x - w / 2 * sc), S(y - h / 2 * sc), S(x + w / 2 * sc), S(y + h / 2 * sc)], radius=S(14 * sc), fill=col, outline=WHITE, width=S(4))
        d.rectangle([S(x - w / 2 * sc), S(y - 10 * sc), S(x + w / 2 * sc), S(y + 20 * sc)], fill=YEL)
def balloon(G, cx, cy, k):   # k: 0 надут -> 1 сдулся
    d = ImageDraw.Draw(G); r = 120 * (1 - 0.8 * k); wob = math.sin(k * 40) * 25 * k
    x = cx + wob; y = cy + 120 * k
    d.ellipse([S(x - r), S(y - r * 1.15), S(x + r), S(y + r * 1.15)], fill=RED)
    d.polygon([(S(x), S(y + r * 1.1)), (S(x - 14), S(y + r * 1.1 + 22)), (S(x + 14), S(y + r * 1.1 + 22))], fill=RED)
    d.line([S(x), S(y + r * 1.1 + 22), S(x - 20), S(y + r * 1.1 + 140)], fill=INK, width=S(4))
def piggy(G, cx, cy, sc=1.0, label=None):
    if sc <= 0.01: return
    d = ImageDraw.Draw(G); w, h = 300 * sc, 220 * sc
    d.ellipse([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], fill=INK)
    d.polygon([(S(cx - 40 * sc), S(cy - h / 2 + 10 * sc)), (S(cx - 10 * sc), S(cy - h / 2 - 50 * sc)), (S(cx + 20 * sc), S(cy - h / 2 + 15 * sc))], fill=INK)
    d.ellipse([S(cx + w / 2 - 30 * sc), S(cy - 30 * sc), S(cx + w / 2 + 40 * sc), S(cy + 30 * sc)], fill=INK, outline=WHITE, width=S(4))
    for lx in (-80, 50):
        d.rounded_rectangle([S(cx + lx * sc), S(cy + h / 2 - 30 * sc), S(cx + (lx + 40) * sc), S(cy + h / 2 + 40 * sc)], radius=S(8), fill=INK)
    d.rounded_rectangle([S(cx - 50 * sc), S(cy - h / 2 + 30 * sc), S(cx + 50 * sc), S(cy - h / 2 + 44 * sc)], radius=S(6), fill=WHITE)
def coin(G, cx, y, sc=1.0):
    d = ImageDraw.Draw(G); r = 34 * sc
    d.ellipse([S(cx - r), S(y - r), S(cx + r), S(y + r)], fill=YEL, outline=INK, width=S(5))
    big_text(G, '$', cx, y - 26 * sc, 40 * sc)
def arrow(G, x0, y0, x1, y1, k=1.0, col=INK):
    if k <= 0: return
    d = ImageDraw.Draw(G); x1, y1 = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    d.line([S(x0), S(y0), S(x1), S(y1)], fill=col, width=S(8)); a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(S(x1), S(y1)), (S(x1 - 26 * math.cos(a - 0.5)), S(y1 - 26 * math.sin(a - 0.5))), (S(x1 - 26 * math.cos(a + 0.5)), S(y1 - 26 * math.sin(a + 0.5)))], fill=col)

def sc_phone_zp(G, t):
    cx, cy = 680, 450; d = phone_frame(G, cx, cy)
    d.text((S(cx - 210), S(cy - 340)), 'Balance', font=font(36), fill=INK)
    v = 0 if t < T['zp'] else (4000 if t < T['gde'] - 0.5 else counter(t, T['gde'] - 0.5, 4000, 0, 1.0))
    col = INK if v > 0 or t < T['gde'] else RED
    big_text(G, rub(v), cx, cy - 220, 64, col)
    if t >= T['zp'] - 0.1:   # уведомление
        k = eo((t - T['zp'] + 0.1) / 0.3); y = cy - 120 + (1 - k) * -200
        d.rounded_rectangle([S(cx - 220), S(y), S(cx + 220), S(y + 130)], radius=S(24), fill=YEL)
        d.text((S(cx - 190), S(y + 18)), 'Bank · now', font=font(24, False), fill=INK)
        d.text((S(cx - 190), S(y + 56)), 'Deposit +$4,000', font=font(32), fill=INK)
    if t >= T['gde'] - 0.4:
        for j, (dx, dy) in enumerate(((-120, 120), (60, 200), (150, 90))):
            k = (t - T['gde'] + 0.4 - j * 0.15) / 0.8
            if 0 < k < 1: big_text(G, 'WHOOSH', cx + dx, cy + dy + 60 - 80 * k, 40, (180, 180, 180))
def sc_day(G, t, n, t0, a, b, icon):
    plate(G, t, t0 - 0.05, f'DAY {n}', 540, 160, 70, YEL, INK, rot=-3)
    v = counter(t, t0 + 0.4, a, b, 1.2); big_text(G, rub(v), 540, 280, 120, RED if b < 1000 and v <= b + 1 else INK)
    if icon == 'confetti': confetti(G, t, t0)
    if icon == 'bags': bags(G, 540, 620, back((t - t0 - 0.2) / 0.3))
    if icon == 'balloon': balloon(G, 540, 600, clamp((t - t0 - 0.4) / 1.6))

def sc_schema(G, t):
    rev = t >= T['naob']
    k = eo((t - T['naob']) / 0.6) if rev else 0
    pos_old = {'PAYCHECK': 190, 'SPENDING': 540, 'SAVINGS': 890}
    pos_new = {'PAYCHECK': 190, 'SAVINGS': 540, 'SPENDING': 890}
    shown = {'PAYCHECK': T['kopish'], 'SPENDING': T['togo'], 'SAVINGS': T['ost']}
    y = 430
    for name in ('PAYCHECK', 'SPENDING', 'SAVINGS'):
        if t < shown[name] - 0.1: continue
        x = pos_old[name] + (pos_new[name] - pos_old[name]) * k
        yy = y + (math.sin(k * math.pi) * (-90 if name == 'SAVINGS' else 90))
        bgc = YEL if (name == 'SAVINGS' and rev) else INK; fgc = INK if bgc == YEL else WHITE
        paste(G, plate_img(name, 40, bgc, fgc, pad=20), x, yy, back((t - shown[name] + 0.1) / 0.25) * (1.15 if bgc == YEL else 1))
    if t >= T['togo'] and k in (0, 1):
        arrow(G, 315, y, 410, y, clamp((t - T['togo']) / 0.3)) if t >= T['togo'] else None
    if t >= T['ost'] and k in (0, 1):
        arrow(G, 665, y, 760, y, clamp((t - T['ost']) / 0.3))
    if not rev and t >= T['nol1'] - 0.1:
        fall = eo((t - T['nol1'] + 0.1) / 0.35); big_text(G, '$0', 860, -100 + 640 * fall, 100, RED)
    if rev and t >= T['desyat']:
        plate(G, t, T['desyat'], '10%', 540, 300, 64, RED, WHITE, rot=-6)
        plate(G, t, T['desyat'] + 0.6, 'right away, on payday', 540, 600, 40, INK, WHITE, rot=2)
def sc_avto(G, t):
    cx, cy = 680, 450; d = phone_frame(G, cx, cy)
    d.text((S(cx - 210), S(cy - 340)), 'Auto transfer', font=font(40), fill=INK)
    rows = [('When', 'On payday'), ('Amount', '10%'), ('To', 'Savings')]
    for j, (a, b) in enumerate(rows):
        y = cy - 230 + j * 120
        d.text((S(cx - 210), S(y)), a, font=font(28, False), fill=(120, 120, 120)); d.text((S(cx - 210), S(y + 38)), b, font=font(34), fill=INK)
        d.line([S(cx - 210), S(y + 96), S(cx + 210), S(y + 96)], fill=(225, 225, 225), width=S(2))
    on = eo((t - T['avto'] - 0.2) / 0.25); y = cy + 170
    d.text((S(cx - 210), S(y)), 'Turn on', font=font(34), fill=INK)
    tx = cx + 110; col = tuple(int(200 + (c - 200) * on) for c in YEL)
    d.rounded_rectangle([S(tx), S(y - 4), S(tx + 110), S(y + 56)], radius=S(30), fill=col)
    kx = tx + 30 + 50 * on; d.ellipse([S(kx - 24), S(y + 2), S(kx + 24), S(y + 50)], fill=WHITE, outline=INK, width=S(3))
def sc_piggy(G, t):
    piggy(G, 540, 560, back((t - B[10]) / 0.3))
    if t >= T['shest'] - 0.2:
        for j in range(3):
            k = (t - T['shest'] + 0.2 - j * 0.25) / 0.45
            if 0 < k < 1: coin(G, 540, 200 + 230 * k * k)
    if t < T['sem']:
        if t >= T['shest']: big_text(G, '$400 / mo', 540, 180, 80)
    else:
        v = counter(t, T['sem'], 400, 4800, 1.0); big_text(G, rub(v), 540, 140, 110, INK)
        plate(G, t, T['sem'] + 1.0, 'A YEAR', 540, 330, 50, YEL, INK, rot=-3)
def sc_spend(G, t):
    bags(G, 540, 520, back((t - B[11]) / 0.3))
    plate(G, t, T['bez'], 'ZERO GUILT', 540, 220, 56, YEL, INK, rot=-3)
def sc_first(G, t):
    plate(G, t, T['snach'], 'PAY YOURSELF\nFIRST', 540, 380, 78, YEL, INK, rot=-3)
    plate(G, t, T['potom'], 'everybody else second', 540, 600, 44, INK, WHITE, rot=2)
def sc_final(G, t):
    if t < T['vsyo']:
        piggy(G, 600, 660, back((t - B[13]) / 0.3))
        plate(G, t, B[13] + 0.2, '"WHATEVER\'S LEFT"', 540, 200, 50, WHITE, INK, border=INK)
        if t >= T['nol2']: big_text(G, '$0', 540, 290, 120, RED, shake=math.sin(t * 50) * 5 if t < T['nol2'] + 0.4 else 0)
        plate(G, t, T['vsegda'], 'ALWAYS', 820, 330, 44, RED, WHITE, rot=8)
    else:
        plate(G, t, T['netupi'] - 0.15, "DON'T\nBE DUMB", 540, 470, 100, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_phone_zp(G, t)
    elif t < B[2]:
        plate(G, t, T['stop'] - 0.05, "STOP.\nYOU'RE BEING DUMB", 540, 420, 64, YEL, INK, rot=-3)
    elif t < B[3]:
        big_text(G, '$4,000', 540, 300, 130)
        for j, (x, y, r) in enumerate(((200, 200, -12), (880, 230, 10), (760, 560, -6))):
            plate(G, t, T['kuda'] + j * 0.2, '?', x, y, 70, YEL, INK, rot=r)
        plate(G, t, T['perv'], 'FIRST 3 DAYS', 360, 560, 50, INK, WHITE, rot=3)
    elif t < B[4]: sc_day(G, t, 1, T['d1'], 4000, 2700, 'confetti')
    elif t < B[5]: sc_day(G, t, 2, T['d2'], 2700, 1500, 'bags')
    elif t < B[6]: sc_day(G, t, 3, T['d3'], 1500, 300, 'balloon')
    elif t < B[7]:
        plate(G, t, T['dumaesh'] + 0.6, 'UNDERPAID?', 540, 400, 72, WHITE, INK, border=INK)
        if t >= T['net'] - 0.1:
            k = eo((t - T['net'] + 0.1) / 0.25); d = ImageDraw.Draw(G)
            d.line([S(200), S(300), S(200 + 680 * k), S(300 + 200 * k)], fill=RED, width=S(18))
            d.line([S(880), S(300), S(880 - 680 * k), S(300 + 200 * k)], fill=RED, width=S(18))
            plate(G, t, T['net'], 'NOPE', 540, 650, 70, RED, WHITE, rot=-4)
    elif t < B[8]:
        v = counter(t, T['budet'], 8000, 0, 1.6) if t >= T['budet'] else 8000
        big_text(G, rub(v), 540, 320, 120, RED if v < 1 else INK)
        plate(G, t, T['dva'], '× 2', 860, 220, 60, YEL, INK, rot=8)
        if t >= T['budet']: bags(G, 540, 640, 1.3 * back((t - T['budet'] - 0.3) / 0.3))
        plate(G, t, T['dorozhe'], 'JUST PRICIER', 540, 160, 50, RED, WHITE, rot=-4)
    elif t < T['avto'] - 0.3: sc_schema(G, t)
    elif t < B[10]: sc_avto(G, t)
    elif t < B[11]: sc_piggy(G, t)
    elif t < B[12]: sc_spend(G, t)
    elif t < B[13]: sc_first(G, t)
    else: sc_final(G, t)
    return G.resize((WD, GH), Image.LANCZOS)

# субтитры: до двух строк, каждая не шире MAXW; группа рвётся на конце фразы
SUBF = ImageFont.truetype(FB, 56); SP = 14; MAXW = 780
_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
def wlen(w): return _d.textbbox((0, 0), w[0].upper().strip('«»"'), font=SUBF)[2]
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
    if w[0][-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 3): groups.append(cur); cur = []
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
            d.text((x, y), w[0].upper().strip('«»"'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78

CH_CROP = (0, 60, 1080, 1660)   # сверху запас под прыжок и поднятые руки
SUB_Y = 1410; FEET = 1335
DEF = (540, FEET, 0.45, 190, 0.72); LEFT = (270, FEET, 0.5, 190, 0.72); RIGHT = (790, FEET, 0.5, 190, 0.72)
PH = (240, FEET, 0.52, 270, 1.0); TOP = (540, 660, 0.35, 470, 1.0)
LAY = [(0, *PH), (B[1], *DEF), (B[2], *DEF), (B[3], *LEFT), (B[4], *RIGHT), (B[5], *LEFT), (B[6], *DEF), (B[7], *RIGHT),
       (B[8], *TOP), (T['avto'] - 0.3, *PH), (B[10], *DEF), (B[11], *LEFT), (B[12], *DEF), (B[13], 250, FEET, 0.5, 190, 0.72), (T['vsyo'], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]

# ---------- Liquid Glass: линзы только на цифры и второстепенный текст (правило Ярослава) ----------
# стекло отключено (Liquid Glass больше не используем)
def pop(t, t0):
    a = t - t0; return (1 - spring(a, 6, 12)), 0.10 * np.exp(-5 * max(a, 0)) * np.sin(16 * a)
def lens(img, cx, cy, w, h, t, t0, t1=None, zoom=1.2):
    if t < t0 or (t1 and t > t1): return
    sc, sq = pop(t, t0)
    if t1 and t > t1 - 0.2: sc *= max(0, (t1 - t) / 0.2)
    glass(img, cx, cy, w * sc * (1 + sq), h * sc * (1 - sq), zoom=zoom, refr=40, bevel=40, tint=0.05, shadow=0.13, chroma=0.18)
def lens_move(img, keys, w, h, t, t1, zoom=1.18):
    """keys: [(время, x, y)] — линза перетекает между точками и тянется в движении"""
    if t < keys[0][0] or t > t1: return
    def pos(tt):
        k = max(i for i, kk in enumerate(keys) if kk[0] <= tt) if tt >= keys[0][0] else 0
        ts, x, y = keys[k]; px, py = (keys[k - 1][1], keys[k - 1][2]) if k else (x, y); s = spring(tt - ts, 8, 11)
        return x + (px - x) * s, y + (py - y) * s
    x, y = pos(t); vy = (pos(t + 1 / FPS)[1] - pos(t - 1 / FPS)[1]) * FPS / 2; st = min(abs(vy) / 2500, 0.45)
    sc, _ = pop(t, keys[0][0])
    if t > t1 - 0.2: sc *= max(0, (t1 - t) / 0.2)
    glass(img, x, y, w * sc * (1 - 0.12 * st), h * sc * (1 + 0.9 * st), zoom=zoom, refr=32, bevel=32, tint=0.04, shadow=0.12, chroma=0.18)
def lenses(img, t):
    lens(img, 680, 662, 490, 175, t, T['zp'] + 0.25, T['gde'] - 0.5)                    # «Зачислено 60 000 ₽»
    lens(img, 540, 438, 520, 150, t, T['d1'] + 0.3, B[6] - 0.05)                         # баланс по дням
    lens(img, 540, 467, 600, 160, t, B[7] + 0.1, B[8] - 0.05)                            # 120 000 тает
    lens_move(img, [(T['avto'] + 0.1, 680, 935), (T['avto'] + 1.3, 680, 652)], 470, 112, t, B[10] - 0.05)   # тумблер -> «10%»
    lens(img, 540, 338, 560, 150, t, T['sem'] + 0.1, B[11] - 0.05, zoom=1.22)            # 72 000 за год
    lens(img, 540, 442, 300, 150, t, T['nol2'] + 0.05, T['vsyo'] - 0.05, zoom=1.3)        # «0 ₽»

def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    cx, feet, s, gy, gs = layout(t)
    G = graphics(t)
    if gs != 1: G = G.resize((int(WD * gs), int(GH * gs)), Image.LANCZOS)
    bg.paste(G, (int((WD - G.width) / 2), int(gy)), G)
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
            if i % 120 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
