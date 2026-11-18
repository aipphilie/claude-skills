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
def raw(word, k=0): return [w for w in W if w[0] == word][k][1]
T = dict(proch=wt('Read'), desyat=wt('Ten'), tish=wt('nothing'), tochno=wt('exactly'), stop=wt('Stop'), podvoh=wt('catch', 0),
         nezn=wt("don't", 0), obid=wt('mad'), neto=wt('wrong'), konec=wt('over'), nu=wexact('okay', 0), dramu=wt('drama'), odinch=wexact('one', 0),
         ty=raw('You.'), zachem=wt('Why', 1), tri=wexact('three', 0), tretem=wt('third'), ruku=wt('red-handed'), r1=wexact('one', 2), fakt=wt('fact'),
         otveta=wexact('no', 0), ostal=wt('Everything', 0), neon=wt("didn't"), r2=wexact('two'), pyt=wt('try'), nevyd=wt("Won't"),
         prid=wt('Come'), rul=wt('driving'), sov=wt('meeting'), usnul=wt('asleep'), r3=wexact('three', 2), spr=wt('Just', 0), propal=wt('quiet'),
         mozhno=wt('allowed'), mozhno2=raw('is.', 0), nakonec=wt('finally'), mozg=wt('brain', 1), pust=wt('blank'), doris=wt('fills'),
         strash=wt('scariest'), kstati=wexact('way'), kto=wexact('who'), pred=wt('pictured'), vot=wt('works'), aon=wexact('he', 2), obedal=wt('lunch'),
         vsyo=wt("That's", 4), netupi=wexact('dumb', 1))

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
def sc_read(G, t):
    d = phone_frame(G, 720, 500, 480, 780)
    big_text(G, 'today', 720, 160, 28, GREY, black=False)
    paste(G, plate_img('Hey!\nHow are you?', 34, YEL, INK, pad=24), 790, 320, back((t - 0.02) / 0.25))
    if t >= T['proch'] + 0.3: big_text(G, 'Read', 800, 420, 30, GREY, black=False)
    if t >= T['desyat']: big_text(G, '10 min ago', 786, 462, 30, RED if t >= T['desyat'] + 0.3 else GREY, black=False)
    if t >= T['tish']:
        for j in range(3):
            on = int((t - T['tish']) * 3) % 4 > j
            d.ellipse([S(560 + j * 44), S(600), S(588 + j * 44), S(628)], fill=GREY if on else LG)
    plate(G, t, T['tish'], 'NOTHING', 720, 780, 60, INK, WHITE, rot=-4, t1=T['tochno'] - 0.15)
    plate(G, t, T['tochno'], '"I KNOW\nEXACTLY WHY"', 720, 780, 44, YEL, INK, rot=3)
def sc_storm(G, t):
    keys = ['obid', 'neto', 'konec']
    n = sum(1 for k in keys if t >= T[k]); last = max([T[k] for k in keys if t >= T[k]] or [B[2]])
    sc = 0.6 + 0.3 * max(0, n - 1 + back((t - last) / 0.3)) if n else 0.6 * back((t - B[2]) / 0.3)
    sag = 14 * n
    cloud(G, 540, 330 + sag, sc, tail=(540, 760), wob=t)
    if t < T['obid'] - 0.1:
        plate(G, t, T['podvoh'] - 0.05, 'THE CATCH!', 540, 330, 84, RED, WHITE, rot=5, t1=T['nezn'] - 0.15)
        plate(G, t, T['nezn'] - 0.1, "YOU DON'T KNOW", 540, 330, 64, YEL, INK, rot=-3)
    for j, (k, txt) in enumerate(zip(keys, ("HE'S MAD", 'I SAID IT WRONG', "IT'S OVER"))):
        if t < T['nu']: plate(G, t, T[k], txt, 540 + (-70, 60, -30)[j], 220 + j * 110 + sag, (44, 42, 54)[j], WHITE if j < 2 else RED, INK if j < 2 else WHITE, rot=(-4, 3, -3)[j])
    plate(G, t, T['nu'], "OKAY, THAT'S\nTOO MUCH", 540, 330 + sag, 62, RED, WHITE, rot=-4)
def sc_author(G, t):
    cloud(G, 700, 420, 1.2, wob=t)
    for j, txt in enumerate(("HE'S MAD", 'I SAID IT WRONG', "IT'S OVER")):
        paste(G, plate_img(txt, 46, WHITE if j < 2 else RED, INK if j < 2 else WHITE), 680 + (-40, 50, -20)[j], 330 + j * 100, 1, (-4, 3, -3)[j])
        if t >= T['odinch'] + j * 0.12: paste(G, plate_img('you', 36, YEL, INK, pad=14), 990, 300 + j * 100, back((t - T['odinch'] - j * 0.12) / 0.2), 6)
    plate(G, t, T['dramu'] - 0.2, 'WHO WROTE THIS?', 640, 90, 50, INK, WHITE, rot=-2)
    plate(G, t, T['ty'] - 0.05, 'YOU', 700, 800, 150, YEL, INK, rot=-4)
def sc_what(G, t):
    plate(G, t, T['zachem'] - 0.1, 'WHY DOES YOUR\nBRAIN DO THIS?', 540, 220, 72, YEL, INK, rot=-3)
    for j in range(4):
        t0 = T['tri'] + j * 0.12
        if t < t0: continue
        hot = j == 2 and t >= T['tretem']
        lab = str(j + 1) if j < 3 else '?'
        paste(G, plate_img(lab, 110, YEL if hot else (INK if j < 3 else LG), INK if hot else (WHITE if j < 3 else GREY), pad=30), 210 + j * 220, 560, back((t - t0) / 0.25) * (1.15 if hot else 1))
def sc_rule1(G, t):
    plate(G, t, B[5], '1', 540, 70, 60, YEL, INK)
    if t >= T['fakt'] - 0.1:
        d = card(G, 760, 290, 540, 230, YEL, k=back((t - T['fakt'] + 0.1) / 0.28))
        if t >= T['fakt'] + 0.2:
            d.text((S(520), S(200)), 'FACT', font=font(44), fill=INK)
            if t >= T['otveta']: d.text((S(520), S(282)), '•  no reply yet', font=font(40), fill=INK)
    if t >= T['ostal'] - 0.1:
        d = card(G, 760, 660, 540, 400, k=back((t - T['ostal'] + 0.1) / 0.28))
        if t >= T['ostal'] + 0.2:
            d.text((S(520), S(480)), 'MADE UP', font=font(44), fill=INK)
            for j, l in enumerate(("he's mad", 'I said something wrong', "I'm boring", "it's over")):
                d.text((S(520), S(560 + j * 68)), '•  ' + l, font=font(36, False), fill=GREY)
        cross(G, 520, 500, 1000, 830, clamp((t - T['neon']) / 0.3))
        plate(G, t, T['neon'], 'NOT HIM', 860, 900, 56, RED, WHITE, rot=-5)
def sc_rule2(G, t):
    plate(G, t, B[6], '2', 540, 70, 60, YEL, INK)
    if t < T['prid'] - 0.15:
        plate(G, t, T['pyt'], "\"DON'T THINK\"", 600, 360, 80, WHITE, INK, border=INK, rot=-3)
        cross(G, 300, 270, 900, 450, clamp((t - T['nevyd'] + 0.15) / 0.25))
        plate(G, t, T['nevyd'], "WON'T WORK", 640, 600, 60, RED, WHITE, rot=4)
        cloud(G, 800, 820, 0.8, wob=t); return
    plate(G, t, T['prid'], '3 BORING REASONS', 540, 190, 46, INK, WHITE, rot=-2)
    n = 0
    for j, (k, lab, ic) in enumerate((('rul', 'driving', wheel), ('sov', 'in a meeting', chart), ('usnul', 'asleep', sleeper))):
        if t < T[k] - 0.15: continue
        n += 1; x = 200 + j * 340; s = back((t - T[k] + 0.15) / 0.28)
        card(G, x, 430, 310, 330, k=s)
        if s > 0.9:
            if ic is wheel: wheel(G, x, 400, 78)
            else: ic(G, x, 400)
            big_text(G, lab, x, 520, 34, INK)
    last = max([T[k] for k in ('rul', 'sov', 'usnul') if t >= T[k]] or [0])
    sc = 0.8 - 0.22 * (n - 1 + eo((t - last) / 0.35)) if n else 0.8
    cloud(G, 800, 820, max(sc, 0.12), wob=t)
def sc_rule3(G, t):
    plate(G, t, B[7], '3', 540, 70, 60, YEL, INK)
    phone_frame(G, 720, 500, 480, 720)
    plate(G, t, T['spr'], 'JUST ASK', 720, 250, 38, INK, WHITE, rot=-2)
    if t >= T['propal'] - 0.1:
        paste(G, plate_img('You went quiet,\neverything okay?', 34, YEL, INK, pad=24), 740, 450, back((t - T['propal'] + 0.1) / 0.25))
    plate(G, t, T['mozhno'] - 0.6, "WAIT, THAT'S\nALLOWED?", 720, 660, 40, WHITE, INK, border=INK, rot=-2)
    plate(G, t, T['mozhno2'], 'IT IS', 720, 900, 76, YEL, INK, rot=4)
def sc_void(G, t, cx=440):
    plate(G, t, B[8], '?', 540, 70, 60, YEL, INK)
    plate(G, t, T['nakonec'] + 0.6, 'WHY', 300, 70, 44, INK, WHITE, rot=-3, t1=T['mozg'] - 0.1)
    plate(G, t, T['mozg'], 'YOUR BRAIN\nHATES A BLANK', cx, 190, 46, INK, WHITE, rot=-2)
    k = back((t - T['pust'] + 0.3) / 0.3)
    if k > 0.01:
        d = card(G, cx, 520, 620, 400, k=k)
        if k > 0.9:
            d.text((S(cx - 270), S(350)), 'REPLY:', font=font(44), fill=GREY)
            if t < T['doris']:
                for j in range(5): d.rounded_rectangle([S(cx - 260 + j * 100), S(530), S(cx - 200 + j * 100), S(544)], radius=S(6), fill=LG)
    g = clamp((t - T['doris']) / 1.0)
    if g > 0:
        cloud(G, cx, 545, 0.25 + 0.55 * eo(g), wob=t)
        bolt(G, cx + 10, 560, back((t - T['doris'] - 0.7) / 0.25) * 0.9)
    plate(G, t, T['strash'] - 0.3, 'THE SCARIEST ONE', cx - 20, 820, 44, RED, WHITE, rot=-3)
def sc_meta(G, t):
    d = card(G, 700, 400, 440, 520, k=back((t - B[9]) / 0.28))
    if t >= B[9] + 0.25:
        d.ellipse([S(610), S(210), S(790), S(390)], fill=LG)
        d.rounded_rectangle([S(560), S(410), S(840), S(640)], radius=S(90), fill=LG)
        d.rectangle([S(550), S(600), S(850), S(650)], fill=WHITE)
        big_text(G, '?', 700, 232, 120, GREY)
    plate(G, t, T['kto'], 'WHO IS "HE"?', 700, 90, 46, INK, WHITE, rot=-2)
    plate(G, t, T['pred'] - 0.5, 'YOU ALREADY\nPICTURED\nSOMEONE', 700, 600, 52, YEL, INK, rot=-4)
    if t >= T['vot']:
        plate(G, t, T['vot'], "THAT'S HOW\nIT WORKS", 700, 860, 50, INK, WHITE, rot=2)
def sc_final(G, t):
    if t < T['vsyo'] - 0.1:
        if t < T['obedal']:
            cloud(G, 540, 280, 0.95 * back((t - B[10]) / 0.25), wob=t, tail=(540, 700))
            if t >= T['aon'] + 0.05: paste(G, plate_img('sorry, was at lunch', 64, WHITE, INK, pad=30, border=INK), 540, 580, back((t - T['aon'] - 0.05) / 0.25))
        else:
            d = ImageDraw.Draw(G); k = (t - T['obedal']) / 0.35
            if k < 1:
                for a in range(0, 360, 30):
                    r0, r1 = 120 + 220 * k, 170 + 260 * k; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                    d.line([S(540 + ca * r0), S(280 + sa * r0 * 0.7), S(540 + ca * r1), S(280 + sa * r1 * 0.7)], fill=INK, width=S(14 * (1 - k) + 2))
            paste(G, plate_img('sorry, was at lunch', 64, WHITE, INK, pad=30, border=INK), 540, 580)
            plate(G, t, T['obedal'], 'HE WAS JUST AT LUNCH', 540, 300, 64, YEL, INK, rot=-3)
    else:
        plate(G, t, T['netupi'] - 0.15, "DON'T\nBE DUMB", 540, 470, 100, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_read(G, t)
    elif t < B[2]: plate(G, t, T['stop'] - 0.05, "STOP.\nYOU'RE BEING DUMB", 540, 420, 64, YEL, INK, rot=-3)
    elif t < B[3]: sc_storm(G, t)
    elif t < B[4]: sc_author(G, t)
    elif t < B[5]: sc_what(G, t)
    elif t < B[6]: sc_rule1(G, t)
    elif t < B[7]: sc_rule2(G, t)
    elif t < B[8]: sc_rule3(G, t)
    elif t < B[9]: sc_void(G, t)
    elif t < B[10]: sc_meta(G, t)
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
            d.text((x, y), w[0].upper().strip('«»"'), font=SUBF, fill=INK)
            x += wd + SP
        y += 78


CH_CROP = (0, 60, 1080, 1660)
SUB_Y = 1410; FEET = 1335
DEF = (540, FEET, 0.45, 190, 0.72); LEFT = (270, FEET, 0.5, 190, 0.72); RIGHT = (790, FEET, 0.5, 190, 0.72)
PH = (240, FEET, 0.52, 270, 1.0)
LAY = [(0, *PH), (B[1], *DEF), (B[2], *DEF), (B[3], *LEFT), (B[4], *DEF), (B[5], *PH), (B[6], *LEFT),
       (B[7], *PH), (B[8], *RIGHT), (B[9], *LEFT), (B[10], *DEF)]
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
