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
# ---------- сцены «Я выгорел» ----------
import random
GREY = (150, 150, 150)
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:') == word.lower()]
    return hits[k][1]
T = dict(stop=wt('Stop'), p71=wt('Tons'), nepr=wt('wrong'), otp=wt('vacation'), dve=wt('Two'), bat=wt('battery'),
         podvoh=wt('catch'), cherez=wexact('week', 0), nule=wt('empty', 1), uchili=wexact('taught'), nikto=wt('Nobody'), vykl=wexact('off'),
         chat=wexact('slack'), dodel=wt("I'll"), son=wexact('sleep', 0), nu=wexact('okay'), trat=wt('drain'), zar=wt('recharge'),
         delat=wexact('what', 0), tri=wexact('three', 0), r1=wexact('one', 0), semi=wexact('seven'), bezzv=wt('mute'), r2=wexact('two', 1),
         ned2=wexact('week', 1), pochtu=wt('email'), mozhno=wt('allowed'), mozhno2=[w for w in W if w[0] == 'is.'][0][1], r3=wexact('three', 1),
         kazhd3=wt('every', 1), radu=wt('happy'), len_=wt('laziness'), spec=wt('professional'), otp2=wt('vacation', 1),
         zaryadka=wt('charger'), pb=wt('power'), vsyo=wt("That's", 3), netupi=wexact('dumb', 1))

def big_text(G, txt, cx, y, sz, col=INK, shake=0, black=True):
    d = ImageDraw.Draw(G); f = font(sz, black); bb = d.textbbox((0, 0), txt, font=f)
    d.text((S(cx + shake) - (bb[2] - bb[0]) / 2, S(y)), txt, font=f, fill=col)
def counter(t, t0, a, b, dur=1.0): return a + (b - a) * eo((t - t0) / dur)

def battery(G, cx, cy, w, h, lvl, alpha=1.0, leak=0.0):
    """вертикальная батарейка, lvl 0..1; leak>0 — дырка снизу и капли"""
    d = ImageDraw.Draw(G); lvl = clamp(lvl)
    col = RED if lvl < 0.25 else (YEL if lvl < 0.99 else (255, 196, 0))
    if alpha < 1: col = tuple(int(c * alpha + 247 * (1 - alpha)) for c in col)
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([S(cx - w * 0.18), S(y0 - h * 0.07), S(cx + w * 0.18), S(y0 + 4)], radius=S(8), fill=INK)
    d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(w * 0.16), fill=WHITE, outline=INK, width=S(14))
    pad = 26; ih = (h - pad * 2) * lvl
    if ih > 2: d.rounded_rectangle([S(x0 + pad), S(y1 - pad - ih), S(x1 - pad), S(y1 - pad)], radius=S(10), fill=col)
    if leak > 0:
        d.ellipse([S(cx - 16), S(y1 - 14), S(cx + 16), S(y1 + 14)], fill=BG, outline=INK, width=S(6))
        for j in range(3):
            k = (leak * 1.3 + j / 3) % 1; yy = y1 + 20 + k * 220
            d.ellipse([S(cx - 12), S(yy - 16), S(cx + 12), S(yy + 16)], fill=YEL, outline=INK, width=S(3))
def pct(G, lvl, cx, y, sz=84):
    big_text(G, f'{int(round(lvl * 100))}%', cx, y, sz, RED if lvl < 0.25 else INK)

def palm(G, cx, cy, sc=1.0):
    if sc <= 0.01: return
    d = ImageDraw.Draw(G)
    d.ellipse([S(cx - 170 * sc), S(cy + 150 * sc), S(cx + 170 * sc), S(cy + 210 * sc)], fill=YEL)
    pts = [(cx + math.sin(k / 10 * 1.2) * 40 * sc, cy + 180 * sc - k * 26 * sc) for k in range(11)]
    d.line([(S(x), S(y)) for x, y in pts], fill=INK, width=S(26 * sc))
    tx, ty = pts[-1]
    for a in (-160, -120, -60, -20, 200):
        r = math.radians(a); ex, ey = tx + math.cos(r) * 150 * sc, ty + math.sin(r) * 60 * sc + 50 * sc
        d.line([S(tx), S(ty), S((tx + ex) / 2), S(min(ty, ey) - 30 * sc), S(ex), S(ey)], fill=INK, width=S(20 * sc), joint='curve')
def cross(G, x0, y0, x1, y1, k):
    if k <= 0: return
    d = ImageDraw.Draw(G)
    d.line([S(x0), S(y0), S(x0 + (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(18))
    d.line([S(x1), S(y0), S(x1 - (x1 - x0) * k), S(y0 + (y1 - y0) * k)], fill=RED, width=S(18))
def tick(G, x, y, ok, sc=1.0):
    d = ImageDraw.Draw(G)
    if ok: d.line([S(x - 26 * sc), S(y), S(x - 6 * sc), S(y + 22 * sc), S(x + 30 * sc), S(y - 26 * sc)], fill=YEL, width=S(12 * sc), joint='curve')
    else:
        d.line([S(x - 24 * sc), S(y - 24 * sc), S(x + 24 * sc), S(y + 24 * sc)], fill=RED, width=S(12 * sc))
        d.line([S(x + 24 * sc), S(y - 24 * sc), S(x - 24 * sc), S(y + 24 * sc)], fill=RED, width=S(12 * sc))
def phone_frame(G, cx, cy, w=440, h=760):
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(56), fill=INK)
    d.rounded_rectangle([S(cx - w / 2 + 16), S(cy - h / 2 + 16), S(cx + w / 2 - 16), S(cy + h / 2 - 16)], radius=S(42), fill=WHITE)
    return d
def moon(G, cx, cy, r, sc=1.0):
    if sc <= 0.01: return
    d = ImageDraw.Draw(G); r *= sc
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=INK)
    d.ellipse([S(cx - r * 0.45), S(cy - r * 1.05), S(cx + r * 1.4), S(cy + r * 0.75)], fill=BG)
    for j, (dx, dy) in enumerate(((1.3, -0.9), (1.6, 0.2), (0.9, 0.9))):
        big_text(G, 'z', cx + dx * r, cy + dy * r - 30, 44 + j * 8, GREY)
def powerbank(G, cx, cy, sc=1.0):
    if sc <= 0.01: return
    d = ImageDraw.Draw(G); w, h = 300 * sc, 170 * sc
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(30 * sc), fill=INK)
    d.polygon([(S(cx + 10 * sc), S(cy - 60 * sc)), (S(cx - 40 * sc), S(cy + 8 * sc)), (S(cx - 2 * sc), S(cy + 8 * sc)),
               (S(cx - 14 * sc), S(cy + 62 * sc)), (S(cx + 40 * sc), S(cy - 10 * sc)), (S(cx + 2 * sc), S(cy - 10 * sc))], fill=YEL)
    for j in range(4):
        d.ellipse([S(cx + w / 2 - 70 * sc + j * 14 * sc), S(cy + h / 2 - 30 * sc), S(cx + w / 2 - 62 * sc + j * 14 * sc), S(cy + h / 2 - 22 * sc)], fill=YEL if j < 1 else (90, 90, 90))

BX, BY, BW, BH = 720, 470, 230, 420   # батарейка в сценах «справа» (раскладка PH)
def sc_monday(G, t):
    plate(G, t, 0.05, 'MONDAY\n8:00 AM', 720, 120, 50, INK, WHITE, rot=-2)
    blink = 0.35 + 0.65 * (0.5 + 0.5 * math.cos(t * 7))
    battery(G, BX, BY + 60, BW, BH, 0.03, alpha=blink if t > 2.9 - 0.2 else 1.0)
    if t >= 2.2: pct(G, 0.03, BX, BY + 330, 90)
def sc_71(G, t):
    if t >= T['p71'] - 0.1:
        sc = back((t - T['p71'] + 0.1) / 0.3); paste(G, plate_img('BURNOUT', 130, WHITE, INK, pad=16), 540, 300, sc)
    plate(G, t, T['p71'] + 0.7, 'tons of working people', 540, 500, 40, INK, WHITE, rot=1)
    plate(G, t, T['nepr'], 'TREAT IT WRONG', 540, 760, 60, RED, WHITE, rot=-4)
def sc_otpusk(G, t):
    plate(G, t, T['otp'], 'VACATION?', 720, 70, 60, WHITE, INK, border=INK, rot=-3)
    palm(G, 560, 470, back((t - T['dve'] + 0.2) / 0.35) * 0.9)
    lvl = 0.03 if t < T['bat'] else counter(t, T['bat'], 0.03, 1.0, 1.3)
    battery(G, 840, 500, 180, 340, lvl); pct(G, lvl, 840, 700, 70)
    if t >= T['podvoh'] - 0.05:
        plate(G, t, T['podvoh'] - 0.05, 'THE CATCH!', 640, 930, 70, RED, WHITE, rot=5)
def sc_back(G, t):
    palm(G, 560, 470, 0.9); cross(G, 420, 300, 700, 700, clamp((t - T['cherez']) / 0.3))
    lvl = counter(t, T['cherez'] + 0.3, 1.0, 0.03, 0.9)
    battery(G, 840, 500, 180, 340, lvl); pct(G, lvl, 840, 700, 70)
    plate(G, t, T['cherez'] + 0.1, 'WORK SLACK  +99', 700, 90, 44, YEL, INK, rot=-3)
def sc_school(G, t):
    d = ImageDraw.Draw(G); k = back((t - B[5]) / 0.3)
    if k > 0.01:
        w, h = 820 * k, 520 * k
        d.rounded_rectangle([S(540 - w / 2), S(380 - h / 2), S(540 + w / 2), S(380 + h / 2)], radius=S(20), fill=(34, 60, 48), outline=INK, width=S(14))
    big_text(G, 'WHAT WE LEARNED', 540, 150, 40, (200, 210, 200)) if t >= B[5] + 0.3 else None
    if t >= T['uchili']: big_text(G, 'HOW TO WORK', 500, 260, 70, WHITE); tick(G, 790, 300, True, 1.3 if t < T['uchili'] + 0.2 else 1.0)
    if t >= T['nikto']: big_text(G, 'SWITCH OFF', 480, 420, 70, WHITE); tick(G, 870, 462, False, 1.2)
    plate(G, t, T['vykl'] + 0.2, 'NOBODY TAUGHT US', 540, 760, 56, YEL, INK, rot=-3)
def sc_leak(G, t):
    lvl = counter(t, T['chat'], 0.7, 0.06, T['nu'] - T['chat'])
    battery(G, 820, 380, 160, 320, lvl, leak=t); pct(G, lvl, 820, 760, 56)
    for k, (key, txt) in enumerate((('chat', 'Slack at 11 PM'), ('dodel', "I'll finish it\nthis weekend"), ('son', '5 hours of sleep'))):
        plate(G, t, T[key], txt, 540, 110 + k * 170, 38, INK, WHITE, rot=(-3, 2, -2)[k])
    plate(G, t, T['nu'], "OKAY, THAT'S\nTOO MUCH", 580, 640, 50, RED, WHITE, rot=-4)
def bar(G, t, t0, y, label, sub, n_on, col):
    if t < t0: return
    d = ImageDraw.Draw(G); a = clamp((t - t0) / 0.25)
    d.text((S(130), S(y - 110)), label, font=font(56), fill=INK); d.text((S(130), S(y - 46)), sub, font=font(40, False), fill=GREY)
    for j in range(12):
        x = 130 + j * 70; on = j < n_on and t >= t0 + 0.2 + j * 0.06
        d.rounded_rectangle([S(x), S(y + 10), S(x + 56), S(y + 110)], radius=S(10), fill=col if on else (225, 222, 215))
def sc_bars(G, t):
    bar(G, t, T['trat'] - 0.1, 250, 'DRAIN', 'every day', 12, RED)
    bar(G, t, T['zar'] - 0.1, 620, 'RECHARGE', 'once a year', 1, YEL)
def sc_what(G, t):
    plate(G, t, T['delat'] - 0.4, 'WHAT TO DO?', 540, 260, 84, YEL, INK, rot=-3)
    for j in range(3):
        if t >= T['tri'] + j * 0.15:
            paste(G, plate_img(str(j + 1), 130, INK, WHITE, pad=34), 300 + j * 240, 600, back((t - T['tri'] - j * 0.15) / 0.25))
def sc_rule1(G, t):
    plate(G, t, B[9], '1', 540, 70, 60, YEL, INK)
    d = phone_frame(G, 700, 520)
    big_text(G, '19:00', 700, 200, 100)
    d.text((S(520), S(400)), 'Work Slack', font=font(38), fill=INK); d.text((S(520), S(450)), '+99 messages', font=font(30, False), fill=GREY)
    on = eo((t - T['bezzv']) / 0.25)
    d.text((S(520), S(520)), 'Mute', font=font(38), fill=INK)
    tx = 760; col = tuple(int(210 + (c - 210) * on) for c in YEL)
    d.rounded_rectangle([S(tx), S(556), S(tx + 110), S(612)], radius=S(28), fill=col)
    kx = tx + 28 + 54 * on; d.ellipse([S(kx - 24), S(520), S(kx + 24), S(608)], fill=WHITE, outline=INK, width=S(3))
    plate(G, t, T['r1'] + 0.3, 'WORK HAS AN END', 620, 960, 40, INK, WHITE, rot=-2)
def sc_rule2(G, t):
    plate(G, t, B[10], '2', 540, 70, 60, YEL, INK)
    d = ImageDraw.Draw(G); days = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    for j, dn in enumerate(days):
        x = 90 + j * 130; hl = j == 6 and t >= T['ned2']
        d.rounded_rectangle([S(x), S(200), S(x + 116), S(330)], radius=S(16), fill=YEL if hl else WHITE, outline=INK, width=S(5))
        bb = d.textbbox((0, 0), dn, font=font(38)); d.text((S(x + 58) - (bb[2] - bb[0]) / 2, S(240)), dn, font=font(38), fill=INK)
    plate(G, t, T['ned2'], 'ZERO WORK', 760, 420, 46, YEL, INK, rot=-4)
    if t < T['mozhno'] - 0.3: plate(G, t, T['pochtu'] - 0.5, '"just checking email"', 460, 640, 40, WHITE, INK, border=INK, rot=2)
    if t >= T['pochtu'] + 0.2 and t < T['mozhno'] - 0.3: cross(G, 170, 590, 750, 700, clamp((t - T['pochtu'] - 0.2) / 0.3))
    plate(G, t, T['mozhno'] - 0.3, "WAIT, THAT'S ALLOWED?", 540, 640, 54, WHITE, INK, border=INK, rot=-2)
    plate(G, t, T['mozhno2'], 'IT IS', 540, 820, 80, YEL, INK, rot=4)
def sc_rule3(G, t):
    plate(G, t, B[11], '3', 540, 70, 60, YEL, INK)
    moon(G, 560, 300, 110, back((t - B[11] - 0.1) / 0.3))
    plate(G, t, T['r3'] + 0.4, 'SLEEP', 560, 540, 70, INK, WHITE, rot=-2)
    plate(G, t, T['kazhd3'], 'EVERY NIGHT', 560, 700, 46, YEL, INK, rot=3)
    lvl = counter(t, T['r3'], 0.15, 0.9, 3.5); battery(G, 850, 470, 170, 320, lvl); pct(G, lvl, 850, 660, 56)
def sc_spec(G, t):
    plate(G, t, T['radu'] - 0.2, 'NOTHING MAKES YOU\nHAPPY FOR MONTHS?', 540, 260, 50, WHITE, INK, border=INK)
    plate(G, t, T['len_'] - 0.1, "IT'S NOT LAZINESS", 540, 520, 76, RED, WHITE, rot=-3)
    plate(G, t, T['spec'] - 0.2, 'talk to a doctor or therapist', 540, 700, 40, INK, WHITE, rot=2)
def sc_final(G, t):
    if t < T['vsyo']:
        plate(G, t, T['otp2'], "A VACATION ISN'T A CHARGER", 540, 170, 50, WHITE, INK, border=INK, rot=-2)
        powerbank(G, 560, 440, back((t - T['pb'] + 0.1) / 0.3) * 1.3)
        plate(G, t, T['pb'], "IT'S A POWER BANK", 600, 700, 64, YEL, INK, rot=3)
    else:
        plate(G, t, T['netupi'] - 0.15, "DON'T\nBE DUMB", 540, 470, 100, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_monday(G, t)
    elif t < B[2]: plate(G, t, T['stop'] - 0.05, "STOP.\nYOU'RE BEING DUMB", 540, 420, 64, YEL, INK, rot=-3)
    elif t < B[3]: sc_71(G, t)
    elif t < B[4]: sc_otpusk(G, t)
    elif t < B[5]: sc_back(G, t)
    elif t < B[6]: sc_school(G, t)
    elif t < B[7]: sc_leak(G, t)
    elif t < B[8]: sc_bars(G, t)
    elif t < B[9]: sc_what(G, t)
    elif t < B[10]: sc_rule1(G, t)
    elif t < B[11]: sc_rule2(G, t)
    elif t < B[12]: sc_rule3(G, t)
    elif t < B[13]: sc_spec(G, t)
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
LAY = [(0, *PH), (B[1], *DEF), (B[2], *RIGHT), (B[3], *PH), (B[5], *LEFT), (B[6], *PH), (B[7], *DEF), (B[8], *RIGHT),
       (B[9], *PH), (B[10], *LEFT), (B[11], *PH), (B[12], *DEF), (B[13], *LEFT), (T['vsyo'], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    return tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4])) + cur[4:]

# ---------- Liquid Glass: линзы только на цифры и второстепенный текст (правило Ярослава) ----------
# стекло отключено
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
    # DEF/RIGHT: графика в масштабе 0.72 со сдвигом gy=190 -> экранные координаты
    def sx(x): return (WD - WD * 0.72) / 2 + x * 0.72
    def sy(y): return 190 + y * 0.72
    lens(img, 840, 270 + 700 + 50, 230, 120, t, T['bat'] + 0.2, B[5] - 0.05, zoom=1.25)  # % батарейки (отпуск -> ноль)
    lens(img, 700, 270 + 250, 360, 150, t, B[9] + 0.3, T['bezzv'] - 0.1, zoom=1.2)       # 19:00

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
    pass
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
