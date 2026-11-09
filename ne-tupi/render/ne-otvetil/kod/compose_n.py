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
T = dict(proch=wt('Прочитано'), desyat=wt('Десять'), tish=wt('тишина'), stop=wt('Стоп'), dum=wt('думаешь'), molchit=wt('молчит'),
         podvoh=wt('подвох'), nezn=wexact('знаешь', 1), prid=wt('придумываешь'), obid=wt('Обиделся'), neto=wt('что-то'), skuch=wt('скучно'),
         konec=wt('конец'), nu=wexact('ну'), mozg=wt('Мозг'), pust=wt('пустоты'), net=wexact('нет'), doris=wt('дорисует'), strash=wt('страшный'),
         poss=wt('поссорился'), pomir=wt('помирился'), obid2=wt('обиделся', 1), odin=wt('одиночку'), delat=wt('делать'), tri=wexact('три'),
         r1=wt('Первое'), razd=wt('раздели'), pridumal=wt('придумал'), odno=wt('одно'), poka=wt('пока'), r2=wt('Второе'), prich=wt('причины'),
         skuchn=wt('Скучные'), rul=wt('рулём'), sov=wt('совещании'), usnul=wt('Уснул'), r3=wt('Третье'), spr=wt('спроси'), propal=wt('пропал'),
         mozhno=wexact('можно', 0), mozhno2=wexact('можно', 1), perezh=wt('пережил'), dramu=wt('драму'), aon=wexact('он', 3), obedal=wt('обедал'),
         vsyo=wexact('всё', 3), netupi=wexact('тупи'))

def big_text(G, txt, cx, y, sz, col=INK, shake=0, black=True):
    d = ImageDraw.Draw(G); f = font(sz, black); bb = d.textbbox((0, 0), txt, font=f)
    d.text((S(cx + shake) - (bb[2] - bb[0]) / 2, S(y)), txt, font=f, fill=col)
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(18))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(18))
def phone_frame(G, cx, cy, w=440, h=760):
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(56), fill=INK)
    d.rounded_rectangle([S(cx - w / 2 + 16), S(cy - h / 2 + 16), S(cx + w / 2 - 16), S(cy + h / 2 - 16)], radius=S(42), fill=WHITE)
    return d
CL = [(-150, 30, 110), (-60, -50, 130), (70, -60, 140), (170, 20, 115), (60, 60, 120), (-50, 70, 115)]
def cloud(G, cx, cy, sc=1.0, col=INK, tail=None, wob=0.0):
    """облако мыслей; tail=(x,y) — пузырьки к голове"""
    if sc <= 0.02: return
    d = ImageDraw.Draw(G)
    for j, (dx, dy, r) in enumerate(CL):
        rr = r * sc * (1 + 0.04 * math.sin(wob * 5 + j)); x, y = cx + dx * sc, cy + dy * sc
        d.ellipse([S(x - rr), S(y - rr), S(x + rr), S(y + rr)], fill=col)
    if tail:
        for k, r in ((0.45, 26), (0.8, 15)):
            x = cx + (tail[0] - cx) * k; y = cy + 120 * sc + (tail[1] - cy - 120 * sc) * k
            d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=col)
def bolt(G, cx, cy, sc=1.0, col=YEL):
    if sc <= 0.02: return
    d = ImageDraw.Draw(G)
    pts = [(14, -90), (-50, 12), (-4, 12), (-20, 90), (52, -16), (4, -16)]
    d.polygon([(S(cx + x * sc), S(cy + y * sc)) for x, y in pts], fill=col)
def heart(G, cx, cy, sc=1.0, col=RED):
    if sc <= 0.02: return
    d = ImageDraw.Draw(G); r = 46 * sc
    d.ellipse([S(cx - 2 * r), S(cy - r * 1.3), S(cx), S(cy + r * 0.7)], fill=col); d.ellipse([S(cx), S(cy - r * 1.3), S(cx + 2 * r), S(cy + r * 0.7)], fill=col)
    d.polygon([(S(cx - 1.86 * r), S(cy + 0.1 * r)), (S(cx + 1.86 * r), S(cy + 0.1 * r)), (S(cx), S(cy + 2.0 * r))], fill=col)
def card(G, cx, cy, w, h, fill=WHITE, k=1.0):
    d = ImageDraw.Draw(G); w *= k; h *= k
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(26), fill=fill, outline=INK, width=S(7))
    return d

def sc_read(G, t):
    d = phone_frame(G, 720, 500, 480, 780)
    big_text(G, 'сегодня', 720, 160, 28, GREY, black=False)
    paste(G, plate_img('Привет!\nТы как?', 34, YEL, INK, pad=24), 790, 320, back((t - 0.02) / 0.25))
    if t >= T['proch'] + 0.3: big_text(G, 'Прочитано', 800, 420, 30, GREY, black=False)
    if t >= T['desyat']: big_text(G, '10 мин назад', 786, 462, 30, RED if t >= T['desyat'] + 0.3 else GREY, black=False)
    if t >= T['tish']:
        for j in range(3):   # точки «печатает…» появляются и пропадают
            on = int((t - T['tish']) * 3) % 4 > j
            d.ellipse([S(560 + j * 44), S(600), S(588 + j * 44), S(628)], fill=GREY if on else LG)
        plate(G, t, T['tish'], 'ТИШИНА', 720, 780, 60, INK, WHITE, rot=-4)
def sc_think(G, t):
    plate(G, t, T['dum'], 'ПОЧЕМУ ОН\nМОЛЧИТ?', 420, 200, 76, WHITE, INK, border=INK, rot=-2, t1=T['nezn'] - 0.1)
    if T['molchit'] <= t < T['nezn'] - 0.1: plate(G, t, T['molchit'], '«я знаю»', 560, 440, 56, INK, WHITE, rot=3)
    if t < T['nezn'] - 0.1: plate(G, t, T['podvoh'] - 0.05, 'ПОДВОХ!', 440, 640, 110, RED, WHITE, rot=5)
    plate(G, t, T['nezn'] - 0.1, 'ТЫ НЕ ЗНАЕШЬ', 440, 260, 84, INK, WHITE, rot=-3)
    plate(G, t, T['prid'], 'ТЫ\nПРИДУМЫВАЕШЬ', 440, 560, 76, YEL, INK, rot=3)
def sc_storm(G, t):
    keys = ['obid', 'neto', 'skuch', 'konec']
    n = sum(1 for k in keys if t >= T[k]); last = max([T[k] for k in keys if t >= T[k]] or [B[3]])
    sc = 0.55 + 0.25 * max(0, n - 1 + back((t - last) / 0.3)) if n else 0.55 * back((t - B[3]) / 0.3)
    sag = 14 * n
    cloud(G, 540, 330 + sag, sc, tail=(540, 760), wob=t)
    for j, (k, txt) in enumerate(zip(keys, ('ОБИДЕЛСЯ', 'НЕ ТО НАПИСАЛ', 'СО МНОЙ СКУЧНО', 'ЭТО КОНЕЦ'))):
        if t < T['nu']: plate(G, t, T[k], txt, 540 + (-70, 60, -50, 40)[j], 190 + j * 100 + sag, (40, 40, 40, 52)[j], WHITE if j < 3 else RED, INK if j < 3 else WHITE, rot=(-4, 3, -2, 4)[j])
    plate(G, t, T['nu'], 'НУ ЭТО УЖЕ\nСЛИШКОМ', 540, 330 + sag, 62, RED, WHITE, rot=-4)
def sc_void(G, t):
    plate(G, t, T['mozg'], 'МОЗГ НЕ ВЫНОСИТ ПУСТОТЫ', 540, 80, 44, INK, WHITE, rot=-2)
    k = back((t - T['pust'] + 0.3) / 0.3)
    if k > 0.01:
        d = card(G, 640, 420, 620, 420, k=k)
        if k > 0.9:
            d.text((S(370), S(240)), 'ОТВЕТ:', font=font(44), fill=GREY)
            if t < T['doris']:
                for j in range(5): d.rounded_rectangle([S(380 + j * 100), S(430), S(440 + j * 100), S(444)], radius=S(6), fill=LG)
    g = clamp((t - T['doris']) / 1.0)
    if g > 0:
        cloud(G, 640, 450, 0.25 + 0.6 * eo(g), wob=t)
        bolt(G, 650, 470, back((t - T['doris'] - 0.7) / 0.25) * 0.9)
    plate(G, t, T['strash'] - 0.3, 'САМЫЙ СТРАШНЫЙ', 640, 740, 54, RED, WHITE, rot=-3)
def sc_alone(G, t):
    for j, (k, lab) in enumerate((('poss', 'ссора'), ('pomir', 'мир'), ('obid2', 'обида'))):
        if t < T[k]: continue
        x = 200 + j * 340; s = back((t - T[k]) / 0.28)
        card(G, x, 280, 310, 340, k=s)
        if s > 0.9:
            (heart if j == 1 else bolt)(G, x, 240 if j == 1 else 245, 1.25, RED if j == 1 else INK)
            big_text(G, lab, x, 372, 44, GREY, black=False)
    plate(G, t, T['odin'] - 0.1, 'В ОДИНОЧКУ', 540, 580, 84, YEL, INK, rot=-3)
def sc_what(G, t):
    plate(G, t, T['delat'] - 0.5, 'ЧТО ДЕЛАТЬ?', 540, 260, 84, YEL, INK, rot=-3)
    for j in range(3):
        if t >= T['tri'] + j * 0.15:
            paste(G, plate_img(str(j + 1), 130, INK, WHITE, pad=34), 300 + j * 240, 600, back((t - T['tri'] - j * 0.15) / 0.25))
def sc_rule1(G, t):
    plate(G, t, B[7], '1', 540, 70, 60, YEL, INK)
    if t >= T['pridumal'] - 0.5:
        d = card(G, 760, 330, 540, 400, k=back((t - T['pridumal'] + 0.5) / 0.28))
        if t >= T['pridumal'] - 0.25:
            d.text((S(520), S(150)), 'ПРИДУМАЛ', font=font(44), fill=INK)
            for j, l in enumerate(('обиделся', 'не то написал', 'со мной скучно', 'это конец')):
                d.text((S(520), S(230 + j * 68)), '•  ' + l, font=font(36, False), fill=GREY)
        cross(G, 520, 170, 1000, 500, clamp((t - T['odno']) / 0.3))
    if t >= T['odno']:
        d = card(G, 760, 720, 540, 230, YEL, k=back((t - T['odno']) / 0.28))
        if t >= T['odno'] + 0.25:
            d.text((S(520), S(630)), 'ЗНАЮ', font=font(44), fill=INK)
            if t >= T['poka'] - 0.6: d.text((S(520), S(712)), '•  ответа пока нет', font=font(40), fill=INK)
def wheel(G, cx, cy, r):
    d = ImageDraw.Draw(G); d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], outline=INK, width=S(16))
    d.ellipse([S(cx - r * .28), S(cy - r * .28), S(cx + r * .28), S(cy + r * .28)], fill=INK)
    for a in (90, 210, 330):
        d.line([S(cx), S(cy), S(cx + math.cos(math.radians(a)) * r), S(cy + math.sin(math.radians(a)) * r)], fill=INK, width=S(14))
def chart(G, cx, cy):
    d = ImageDraw.Draw(G)
    for j, h in enumerate((50, 90, 70, 120)):
        d.rounded_rectangle([S(cx - 76 + j * 40), S(cy + 60 - h), S(cx - 48 + j * 40), S(cy + 60)], radius=S(5), fill=INK if j < 3 else YEL)
    d.line([S(cx - 90), S(cy + 66), S(cx + 90), S(cy + 66)], fill=INK, width=S(8))
def sleeper(G, cx, cy):
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(cx - 80), S(cy + 20), S(cx + 80), S(cy + 62)], radius=S(21), fill=INK)      # лежит
    d.rounded_rectangle([S(cx - 92), S(cy - 14), S(cx - 44), S(cy + 20)], radius=S(8), fill=YEL, outline=INK, width=S(5))  # телефон на лице
    for j in range(3): big_text(G, 'z', cx + 10 + j * 34, cy - 40 - j * 26, 30 + j * 8, GREY)
def sc_rule2(G, t):
    plate(G, t, B[8], '2', 540, 70, 60, YEL, INK)
    plate(G, t, T['prich'] - 0.5, '3 СКУЧНЫЕ ПРИЧИНЫ', 540, 190, 46, INK, WHITE, rot=-2)
    n = 0
    for j, (k, lab, ic) in enumerate((('rul', 'за рулём', wheel), ('sov', 'на совещании', chart), ('usnul', 'уснул', sleeper))):
        if t < T[k] - 0.15: continue
        n += 1; x = 200 + j * 340; s = back((t - T[k] + 0.15) / 0.28)
        card(G, x, 430, 310, 330, k=s)
        if s > 0.9:
            if ic is wheel: wheel(G, x, 400, 78)
            else: ic(G, x, 400)
            big_text(G, lab, x, 520, 34, INK)
    last = max([T[k] for k in ('rul', 'sov', 'usnul') if t >= T[k]] or [0])
    sc = 0.8 - 0.22 * (n - 1 + eo((t - last) / 0.35)) if n else 0.8
    cloud(G, 800, 800, max(sc, 0.12), wob=t)
def sc_rule3(G, t):
    plate(G, t, B[9], '3', 540, 70, 60, YEL, INK)
    phone_frame(G, 720, 500, 480, 720)
    plate(G, t, T['spr'], 'СПРОСИ ПРЯМО', 720, 250, 38, INK, WHITE, rot=-2)
    if t >= T['propal'] - 0.1:
        paste(G, plate_img('Ты пропал,\nвсё нормально?', 34, YEL, INK, pad=24), 740, 450, back((t - T['propal'] + 0.1) / 0.25))
    plate(G, t, T['mozhno'] - 0.4, 'А ТАК\nМОЖНО БЫЛО?', 720, 660, 40, WHITE, INK, border=INK, rot=-2)
    plate(G, t, T['mozhno2'], 'МОЖНО', 720, 900, 76, YEL, INK, rot=4)
def sc_final(G, t):
    if t < T['vsyo'] - 0.1:
        if t < T['obedal']:
            cloud(G, 540, 280, 0.95 * back((t - B[10]) / 0.3), wob=t, tail=(540, 700))
            plate(G, t, T['dramu'] - 0.2, 'ЦЕЛАЯ ДРАМА', 540, 280, 54, RED, WHITE, rot=-3)
            if t >= T['aon'] - 0.1: paste(G, plate_img('сорри, обедал', 64, WHITE, INK, pad=30, border=INK), 540, 580, back((t - T['aon'] + 0.1) / 0.25))
        else:
            d = ImageDraw.Draw(G); k = (t - T['obedal']) / 0.35
            if k < 1:   # облако лопается
                for a in range(0, 360, 30):
                    r0, r1 = 120 + 220 * k, 170 + 260 * k; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                    d.line([S(540 + ca * r0), S(280 + sa * r0 * 0.7), S(540 + ca * r1), S(280 + sa * r1 * 0.7)], fill=INK, width=S(14 * (1 - k) + 2))
            paste(G, plate_img('сорри, обедал', 64, WHITE, INK, pad=30, border=INK), 540, 580)
            plate(G, t, T['obedal'], 'ОН ПРОСТО ОБЕДАЛ', 540, 300, 64, YEL, INK, rot=-3)
    else:
        plate(G, t, T['netupi'] - 0.15, 'НЕ ТУПИ', 540, 470, 120, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_read(G, t)
    elif t < B[2]: plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 420, 84, YEL, INK, rot=-3)
    elif t < B[3]: sc_think(G, t)
    elif t < B[4]: sc_storm(G, t)
    elif t < B[5]: sc_void(G, t)
    elif t < B[6]: sc_alone(G, t)
    elif t < B[7]: sc_what(G, t)
    elif t < B[8]: sc_rule1(G, t)
    elif t < B[9]: sc_rule2(G, t)
    elif t < B[10]: sc_rule3(G, t)
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
DEF = (540, FEET, 0.45, 190, 0.72); LEFT = (270, FEET, 0.5, 190, 0.72); RIGHT = (790, FEET, 0.5, 190, 0.72)
PH = (240, FEET, 0.52, 270, 1.0)
LAY = [(0, *PH), (B[1], *DEF), (B[2], *RIGHT), (B[3], *DEF), (B[4], *LEFT), (B[5], *DEF), (B[6], *RIGHT),
       (B[7], *PH), (B[8], *LEFT), (B[9], *PH), (B[10], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]
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
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
