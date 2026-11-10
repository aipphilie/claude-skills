"""Монтаж: фон + графика (PIL, 2x суперсэмплинг) + персонаж (multiply) -> ffmpeg."""
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

# --- сцены «Самозапрет» ---
def lock(d, cx, cy, s, f=lambda v: v, opened=0.0, fill=None):
    """замок: cx,cy — центр корпуса, s — масштаб; opened 0..1 — дужка поднята"""
    fill = fill or YEL; w, h = 120 * s, 100 * s; r = 38 * s; lift = 34 * s * opened
    top = cy - h / 2
    d.arc([f(cx - r), f(top - r * 1.25 - lift), f(cx + r), f(top + r * 0.9 - lift)], 180, 360, fill=INK, width=max(2, int(f(16 * s))))
    d.line([f(cx - r + 7 * s), f(top - r * 0.2 - lift), f(cx - r + 7 * s), f(top + 6 * s)], fill=INK, width=max(2, int(f(16 * s))))
    if opened < 0.5: d.line([f(cx + r - 7 * s), f(top - r * 0.2), f(cx + r - 7 * s), f(top + 6 * s)], fill=INK, width=max(2, int(f(16 * s))))
    d.rounded_rectangle([f(cx - w / 2), f(top), f(cx + w / 2), f(top + h)], radius=int(f(18 * s)), fill=fill, outline=INK, width=max(2, int(f(8 * s))))
    d.ellipse([f(cx - 13 * s), f(cy - 20 * s), f(cx + 13 * s), f(cy + 6 * s)], fill=INK)
    d.rectangle([f(cx - 5 * s), f(cy), f(cx + 5 * s), f(cy + 26 * s)], fill=INK)
def phone(G, cx, top, bot, w=430):
    d = ImageDraw.Draw(G)
    d.rounded_rectangle([S(cx - w / 2), S(top), S(cx + w / 2), S(bot)], radius=S(54), fill=WHITE, outline=INK, width=S(14))
    d.rounded_rectangle([S(cx - 60), S(top + 26), S(cx + 60), S(top + 46)], radius=S(10), fill=INK)
    return d
def notif(G, cx, cy, k, title, line, ok=False, w=400):
    if k <= 0.05: return
    im = Image.new('RGBA', (S(w), S(190)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S(w) - 1, S(190) - 1], radius=S(28), fill=LG, outline=INK, width=S(6))
    d.ellipse([S(22), S(22), S(70), S(70)], fill=YEL if ok else RED, outline=INK, width=S(4))
    d.text((S(84), S(26)), 'БАНК', font=font(30), fill=GREY)
    d.text((S(24), S(86)), title, font=font(30), fill=INK)
    d.text((S(24), S(128)), line, font=font(40), fill=INK if ok else RED)
    paste(G, im, cx, cy, k)
def hood(G, cx, bot, s=1.0):
    d = ImageDraw.Draw(G); c = (120, 120, 120)
    d.rounded_rectangle([S(cx - 70 * s), S(bot - 250 * s), S(cx + 70 * s), S(bot)], radius=S(60 * s), fill=c)
    d.polygon([(S(cx - 86 * s), S(bot - 190 * s)), (S(cx), S(bot - 345 * s)), (S(cx + 86 * s), S(bot - 190 * s))], fill=c)
    d.ellipse([S(cx - 44 * s), S(bot - 262 * s), S(cx + 44 * s), S(bot - 178 * s)], fill=(60, 60, 60))
def icon_card(G, cx, cy, k, kind, label):
    if k <= 0.05: return
    im = Image.new('RGBA', (S(250), S(290)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S(250) - 1, S(290) - 1], radius=S(26), fill=WHITE, outline=INK, width=S(7))
    x, y = 125, 115
    if kind == 'box':
        d.rectangle([S(x - 62), S(y - 45), S(x + 62), S(y + 60)], fill=YEL, outline=INK, width=S(7))
        d.line([S(x), S(y - 45), S(x), S(y + 60)], fill=INK, width=S(7)); d.line([S(x - 62), S(y - 8), S(x + 62), S(y - 8)], fill=INK, width=S(7))
    elif kind == 'cross':
        d.rectangle([S(x - 22), S(y - 62), S(x + 22), S(y + 62)], fill=INK); d.rectangle([S(x - 62), S(y - 22), S(x + 62), S(y + 22)], fill=INK)
    else:
        d.rounded_rectangle([S(x - 78), S(y - 48), S(x + 78), S(y + 52)], radius=S(14), fill=YEL, outline=INK, width=S(7))
        bb = d.textbbox((0, 0), '−%', font=font(60)); d.text((S(x) - (bb[2] - bb[0]) / 2, S(y - 38)), '−%', font=font(60), fill=INK)
    bb = d.textbbox((0, 0), label, font=font(32)); d.text((S(125) - (bb[2] - bb[0]) / 2, S(212)), label, font=font(32), fill=INK)
    paste(G, im, cx, cy, k)
    # капля
    dd = ImageDraw.Draw(G); ph = (k * 3) % 1
def drop(G, cx, y0, t, t0):
    if t < t0: return
    u = ((t - t0) * 1.3) % 1.0; d = ImageDraw.Draw(G); y = y0 + 150 * u; a = int(255 * (1 - u))
    d.ellipse([S(cx - 12), S(y), S(cx + 12), S(y + 30)], fill=(150, 150, 150, a))

def sc_intro(G, t):
    phone(G, 300, 60, 900)
    notif(G, 300, 250, back((t - 0.15) / 0.3), 'Вам одобрен кредит', '500 000 ₽')
    if t >= T['nebral'] - 0.3: paste(G, plate_img('???', 110, WHITE, INK, pad=26, border=INK), 760, 250, back((t - T['nebral'] + 0.3) / 0.3), 6)
    plate(G, t, T['dumaesh'], '«СО МНОЙ\nТАКОГО\nНЕ БУДЕТ»', 800, 500, 44, LG, GREY, rot=-3, t1=T['nikomu'] - 0.15)
    plate(G, t, T['nikomu'], 'Я ЖЕ\nОСТОРОЖНЫЙ', 810, 500, 44, LG, GREY, rot=3)
def sc_stop(G, t):
    if t < T['tvoi'] - 0.1:
        plate(G, t, T['stop'] - 0.05, 'СТОП.\nТУТ ТЫ ТУПИШЬ', 540, 300, 84, YEL, INK, rot=-3)
        paste(G, plate_img('Я ЖЕ ОСТОРОЖНЫЙ', 60, LG, GREY, pad=24), 540, 640, 1.0, 2)
        cross(G, 190, 590, 890, 690, clamp((t - T['stop'] - 0.4) / 0.3))
        return
    if t < T['dostavka'] - 0.1:
        plate(G, t, T['tvoi'] - 0.1, 'ДАННЫЕ УТЕКЛИ', 540, 110, 80, INK, WHITE, rot=-2)
        for j, lab in enumerate(('ФИО', 'ПАСПОРТ', 'ТЕЛЕФОН')):
            u = clamp((t - T['tvoi'] - 0.25 - j * 0.3) / 2.2)
            if u <= 0: continue
            x = 300 + j * 240 + 180 * u * (j - 1) * 0.6; y = 620 - 330 * eo(u)
            paste(G, plate_img(lab, 60, WHITE, INK, pad=22, border=INK), x, y, back(u / 0.12), (-12, 5, 14)[j] * (0.4 + u))
        plate(G, t, T['slil'] - 0.3, 'И СЛИЛ ИХ НЕ ТЫ', 540, 720, 66, YEL, INK, rot=2)
        return
    paste(G, plate_img('ГДЕ ТЫ ИХ ОСТАВИЛ', 62, INK, WHITE, pad=24), 540, 100, back((t - T['dostavka'] + 0.1) / 0.25), -2)
    for j, (kind, lab, key) in enumerate((('box', 'ДОСТАВКА', 'dostavka'), ('cross', 'АПТЕКА', 'apteka'), ('card', 'СКИДКА', 'magazin'))):
        x = 215 + j * 325
        icon_card(G, x, 400, back((t - T[key]) / 0.28), kind, lab)
        drop(G, x, 560, t, T[key] + 0.3); drop(G, x, 560, t, T[key] + 0.7)
def sc_what(G, t):
    plate(G, t, T['delat'] - 0.6, 'ЧТО ДЕЛАТЬ?', 540, 120, 84, YEL, INK, rot=-3, t1=T['nas'] + 0.9)
    plate(G, t, T['nas'] + 1.0, 'ЗАЩИТА ЕСТЬ', 540, 120, 84, INK, WHITE, rot=-2)
    for j, (lab, key) in enumerate((('1 ГАЛОЧКА', 'odna'), ('0 ₽', 'besplatno'), ('2 МИНУТЫ', 'dve'))):
        plate(G, t, T[key], lab, (330, 760, 540)[j], (340, 400, 570)[j], 78, YEL, INK, rot=(-4, 5, -2)[j])
def sc_gos(G, t):
    if t < T['bank'] - 0.15:
        d = phone(G, 540, 40, 690, w=560)
        big_text(G, 'ГОСУСЛУГИ', 540, 110, 44, INK)
        d.rounded_rectangle([S(300), S(200), S(780), S(290)], radius=S(40), fill=LG, outline=INK, width=S(6))
        d.ellipse([S(322), S(222), S(358), S(258)], outline=INK, width=S(6)); d.line([S(352), S(254), S(370), S(272)], fill=INK, width=S(6))
        q = 'самозапрет на кредиты'; n = int(len(q) * clamp((t - T['poiske'] - 0.2) / max(0.6, T['stavish'] - T['poiske'] - 0.6)))
        if n: d.text((S(384), S(223)), q[:n] + ('|' if n < len(q) and int(t * 6) % 2 else ''), font=font(30, False), fill=INK)
        if t >= T['samozapret'] + 0.5:
            k = back((t - T['samozapret'] - 0.5) / 0.3)
            if k > 0.1:
                d.rounded_rectangle([S(300), S(340), S(780), S(600)], radius=S(26), fill=WHITE, outline=INK, width=S(6))
                big_text(G, 'Самозапрет', 540, 365, 44, INK); big_text(G, 'на кредиты', 540, 415, 44, INK)
                d.rounded_rectangle([S(495), S(490), S(585), S(580)], radius=S(16), fill=YEL if t >= T['stavish'] else WHITE, outline=INK, width=S(7))
                if t >= T['stavish']:
                    u = clamp((t - T['stavish']) / 0.25)
                    d.line([S(512), S(535), S(512 + 22 * min(1, u * 2)), S(535 + 22 * min(1, u * 2))], fill=INK, width=S(13))
                    if u > 0.5: d.line([S(534), S(557), S(534 + 38 * (u - 0.5) * 2), S(557 - 50 * (u - 0.5) * 2)], fill=INK, width=S(13))
        plate(G, t, T['stavish'] + 0.3, 'ЗАПРЕТ СТОИТ', 540, 640, 66, YEL, INK, rot=-3)
        return
    k = eo((t - T['bank'] + 0.15) / 0.5)
    hood(G, 1250 - 420 * k, 760, 1.5)
    paste(G, plate_img('КРЕДИТ', 44, WHITE, INK, pad=16, border=INK), 1250 - 420 * k - 150, 560, 1.0, -8)
    plate(G, t, T['bank'], 'БАНК', 260, 150, 80, INK, WHITE, rot=-2)
    if t >= T['otkazat']:
        u = clamp((t - T['otkazat']) / 0.18); sc = 2.2 - 1.2 * u
        im = plate_img('ОТКАЗ', 120, (255, 255, 255, 0), RED, pad=26, border=RED)
        paste(G, im, 420, 430, sc, -12, u)
def sc_twist(G, t):
    if t < T['zvonyat'] - 0.6:
        plate(G, t, T['podvoh'] - 0.5, 'А ВОТ И ПОДВОХ', 540, 120, 84, YEL, INK, rot=-3)
        if t >= T['snyat'] - 0.4:
            d = ImageDraw.Draw(G); k = back((t - T['snyat'] + 0.4) / 0.3); op = clamp((t - T['snyat']) / 0.35)
            if k > 0.2: lock(d, 540, 480, 2.3 * k, S, opened=op)
            plate(G, t, T['snyat'] + 0.2, 'МОЖНО СНЯТЬ', 540, 760, 70, INK, WHITE, rot=2)
        return
    # звонок
    d = ImageDraw.Draw(G); k = back((t - T['zvonyat'] + 0.6) / 0.3); sh = 10 * math.sin(t * 45) if t < T['proverki'] else 0
    if k > 0.1:
        d.rounded_rectangle([S(120 + sh), S(60), S(520 + sh), S(560)], radius=S(46), fill=INK)
        d.ellipse([S(250 + sh), S(130), S(390 + sh), S(270)], fill=GREY)
        big_text(G, 'Неизвестный', 320 + sh, 300, 38, WHITE); big_text(G, 'номер', 320 + sh, 345, 38, WHITE)
        d.ellipse([S(175 + sh), S(430), S(265 + sh), S(520)], fill=RED); d.ellipse([S(375 + sh), S(430), S(465 + sh), S(520)], fill=(60, 190, 90))
    plate(G, t, T['zvonyat'] + 0.3, 'СНИМИТЕ\nСАМИ', 800, 170, 62, WHITE, INK, rot=4, border=INK)
    plate(G, t, T['proverki'] - 0.3, '«для проверки»', 760, 420, 52, LG, INK, rot=-3)
    plate(G, t, T['zashity'] - 0.3, '«для защиты счёта»', 620, 690, 52, LG, INK, rot=2)
def sc_rule(G, t):
    plate(G, t, T['zapomni'], 'ЗАПОМНИ', 540, 90, 60, INK, WHITE, rot=-2)
    plate(G, t, T['zapomni'] + 0.7, 'ПРОСЯТ СНЯТЬ', 540, 290, 92, WHITE, INK, rot=-2, border=INK)
    plate(G, t, T['moshennik'] - 0.25, '= МОШЕННИК', 540, 500, 100, YEL, INK, rot=3)
    plate(G, t, T['vsegda'], 'ВСЕГДА', 540, 720, 80, RED, WHITE, rot=-3)
def sc_self(G, t):
    plate(G, t, T['nuzhen'] - 0.5, 'НУЖЕН КРЕДИТ ТЕБЕ?', 540, 100, 62, INK, WHITE, rot=-2)
    d = ImageDraw.Draw(G)
    for j, (lab, key) in enumerate((('СНЯЛ', 'snyal'), ('ВЗЯЛ', 'vzyal'), ('ПОСТАВИЛ', 'postavil'))):
        x = 200 + j * 340; k = back((t - T[key]) / 0.28)
        if k <= 0.1: continue
        card(G, x, 400, 280, 330, k=k); d = ImageDraw.Draw(G)
        if j == 1:
            d.rounded_rectangle([S(x - 85), S(320), S(x + 85), S(420)], radius=S(12), fill=YEL, outline=INK, width=S(7)); big_text(G, '₽', x, 328, 70, INK)
        else: lock(d, x, 385, 1.05, S, opened=1.0 if j == 0 else 0.0)
        big_text(G, lab, x, 490, 40, INK)
        if j: d.polygon([(S(x - 195), S(380)), (S(x - 150), S(400)), (S(x - 195), S(420))], fill=INK)
def sc_send(G, t):
    if t < T['pust'] - 0.15:
        plate(G, t, T['postav'], 'ПОСТАВЬ СЕГОДНЯ', 540, 110, 76, YEL, INK, rot=-3)
        if t >= T['pereshli'] - 0.2:
            d = ImageDraw.Draw(G); k = eo((t - T['pereshli'] + 0.2) / 0.5)
            d.line([S(160), S(470), S(160 + 330 * k), S(470)], fill=INK, width=S(16))
            if k >= 1: d.polygon([(S(490), S(430)), (S(560), S(470)), (S(490), S(510))], fill=INK)
            for j in range(2):
                kk = back((t - T['pereshli'] - 0.4 - j * 0.2) / 0.3); x = 690 + j * 190
                if kk <= 0.1: continue
                d.rounded_rectangle([S(x - 60 * kk), S(560 - 300 * kk), S(x + 60 * kk), S(560)], radius=S(58 * kk), fill=(90, 90, 90))
                if t >= T['pereshli'] + 1.1 + j * 0.2: lock(d, x, 440, 0.62 * back((t - T['pereshli'] - 1.1 - j * 0.2) / 0.25), S)
            plate(G, t, T['pereshli'] + 0.5, 'И ПЕРЕШЛИ РОДИТЕЛЯМ', 540, 730, 54, INK, WHITE, rot=2)
        return
    phone(G, 300, 60, 900)
    plate(G, t, T['pust'], 'В СЛЕДУЮЩИЙ\nРАЗ', 810, 300, 44, INK, WHITE, rot=3, t1=T['otkazano'] + 0.2)
    notif(G, 300, 250, back((t - T['soob']) / 0.3), 'Заявка на кредит', 'ОТКАЗАНО' if t >= T['otkazano'] - 0.1 else '…', ok=True)
    plate(G, t, T['otkazano'] + 0.3, 'ЗАМОК\nРАБОТАЕТ', 800, 300, 56, YEL, INK, rot=4)
def sc_final(G, t):
    plate(G, t, T['netupi'] - 0.3, 'ВСЁ.\nНЕ ТУПИ', 540, 300, 110, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[2]: sc_intro(G, t)
    elif t < B[3]: sc_stop(G, t)
    elif t < B[4]: sc_what(G, t)
    elif t < B[5]: sc_gos(G, t)
    elif t < B[6]: sc_twist(G, t)
    elif t < B[7]: sc_rule(G, t)
    elif t < B[8]: sc_self(G, t)
    elif t < B[9]: sc_send(G, t)
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
LAY = [(0, *RIGHT), (B[2], *DEF), (B[3], *LEFT), (B[4], *DEF), (T['bank'] - 0.15, *LEFT), (B[5], *DEF), (T['zvonyat'] - 0.6, *RIGHT), (B[6], *DEF),
       (B[7], *LEFT), (B[8], *DEF), (T['pust'] - 0.15, *RIGHT), (B[9], *DEF)]
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
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if t >= T['stavish'] + 0.15:   # жёлтый замок на человечке, поверх
        k = back((t - T['stavish'] - 0.15) / 0.3)
        if k > 0.1: lock(ImageDraw.Draw(img), cx + xoff[i], feet - 250 * s / 0.45, 0.62 * k * s / 0.45)
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
