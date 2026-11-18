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
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:') == word.lower()]
    return hits[k][1]
def raw(word, k=0): return [w for w in W if w[0] == word][k][1]
IZ = [wexact('sorry', k) for k in range(3)]
T = dict(stop=wt('Stop'), prost=wexact('sorry', 3), slomal=wt('break'), vopros=wt('question'), podvoh=wt('catch'), lishnee=wt('extra'),
         zvuchit=wt('sounds'), meshayu=wt('way', 0), desyat=wt('ten'), poveryat=wt('believe'), nas=wexact('we', 0), izvin=wt('apologizing'),
         vezhl=wexact('polite', 1), uvazh=wt('respect'), viny=wt('guilt', 0), delat=wexact('what', 1), tri=wexact('three', 0),
         r1=wexact('one', 0), nakos=wt('messed'), opozd=wt('late'), perep=wt('mixed'), nogu=wt('foot'),
         r2=wexact('two'), menyay=wt('swap'), spas1=wt('thank'), ne2=wexact('not', 1), zader=wt('wait', 0), spas2=wt('thanks'),
         mozhno=wt('allowed'), mozhno2=raw('is.', 0), r3=wexact('three', 1), soob=wt('message'), vych=wt('delete'), prich=wt('reason'),
         inache=wt('another'), vezhliv=wexact('polite', 2), zaranee=wt('pleading'), vinov=wt('guilty'), vsyo=wt("That's", 1), netupi=wexact('dumb', 1))
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
def card(G, cx, cy, w, h, fill=WHITE, k=1.0):
    d = ImageDraw.Draw(G); w *= k; h *= k
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(26), fill=fill, outline=INK, width=S(7))
    return d


def counter(G, t, n, cx, cy, sz=50, t0=0):
    """счётчик «ИЗВИНИТЕ ×n», подпрыгивает в момент смены"""
    k = 1 + 0.25 * max(0, 1 - (t - t0) / 0.2) if t0 else 1
    paste(G, plate_img(f'SORRY ×{n}', sz, INK if n else LG, WHITE if n else INK, pad=22), cx, cy, k)
def door(G, cx, top, bot, w=260, knock=0):
    d = ImageDraw.Draw(G)
    d.rectangle([S(cx - w / 2 - 18), S(top - 18), S(cx + w / 2 + 18), S(bot)], fill=LG)
    d.rectangle([S(cx - w / 2), S(top), S(cx + w / 2), S(bot)], fill=WHITE, outline=INK, width=S(8))
    for y0, y1 in ((top + 40, (top + bot) / 2 - 20), ((top + bot) / 2 + 20, bot - 40)):
        d.rectangle([S(cx - w / 2 + 34), S(y0), S(cx + w / 2 - 34), S(y1)], outline=INK, width=S(5))
    d.ellipse([S(cx - w / 2 + 22), S((top + bot) / 2 - 14), S(cx - w / 2 + 50), S((top + bot) / 2 + 14)], fill=YEL, outline=INK, width=S(4))
def bubble(G, text, cx, cy, sz=36, fill=WHITE, k=1.0, strike=0.0):
    im = plate_img(text, sz, fill, INK, pad=26, border=INK)
    paste(G, im, cx, cy, k)
    if strike > 0 and k > 0.9:
        d = ImageDraw.Draw(G); w = im.width / SS
        d.line([S(cx - w / 2 + 14), S(cy), S(cx - w / 2 + 14 + (w - 28) * clamp(strike)), S(cy)], fill=RED, width=S(12))
def n_iz(t):
    n = sum(1 for x in IZ[:3] if t >= x); last = max([x for x in IZ[:3] if t >= x] or [0]); return n, last

def sc_intro(G, t):
    door(G, 740, 160, 980)
    n, last = n_iz(t)
    if n: counter(G, t, n, 300, 130, 50, last)
    for j, (txt, x, y, r) in enumerate((('…to bother you', 690, 70, -3), ('…to ask', 560, 250, 3), ('…for even texting', 690, 430, -2))):
        if t >= IZ[j] + 0.2 and t < B[1]: paste(G, plate_img(txt, 46, WHITE, GREY, pad=20, border=LG), x, y, back((t - IZ[j] - 0.2) / 0.25), r)
def sc_zachto(G, t):
    plate(G, t, T['prost'], 'SORRY...\nFOR WHAT?', 600, 150, 72, YEL, INK, rot=-3)
    if t >= T['slomal'] - 0.3:
        k = back((t - T['slomal'] + 0.3) / 0.28); d = card(G, 600, 480, 720, 340, k=k)
        if k > 0.9:
            d.text((S(275), S(335)), 'To a coworker:', font=font(40, False), fill=GREY)
            bubble(G, "Where's the report?", 600, 500, 50, YEL)
    plate(G, t, T['vopros'], 'JUST A QUESTION', 600, 760, 54, INK, WHITE, rot=2)
def sc_podvoh(G, t):
    plate(G, t, T['podvoh'] - 0.05, 'THE CATCH!', 540, 140, 100, RED, WHITE, rot=4)
    if t >= T['lishnee']:
        k = back((t - T['lishnee']) / 0.28)
        bubble(G, '"Sorry"', 540, 420, 100, WHITE, k, strike=(t - T['zvuchit']) / 0.3 if t >= T['zvuchit'] else 0)
    if t >= T['meshayu'] - 0.6:
        plate(G, t, T['meshayu'] - 0.6, "\"I'M IN YOUR WAY\"", 540, 680, 70, INK, WHITE, rot=-3)
def sc_ten(G, t):
    n = 3 + int(7 * clamp((t - B[4] + 0.2) / (T['desyat'] + 0.3 - B[4] + 0.2)))
    counter(G, t, n, 540, 200, 80, 0)
    if n == 10: paste(G, plate_img(f'SORRY ×10', 80, RED, WHITE, pad=22), 540, 200, 1 + 0.15 * max(0, 1 - (t - T['desyat'] - 0.3) / 0.2))
    plate(G, t, T['poveryat'], 'AND THEY BELIEVE IT', 540, 470, 66, YEL, INK, rot=-3)
def sc_board(G, t):
    plate(G, t, T['nas'], 'WE WERE TAUGHT', 540, 90, 50, WHITE, INK, border=INK, rot=-2)
    d = ImageDraw.Draw(G); k = eo((t - T['nas']) / 0.3)
    if k > 0:
        d.rectangle([S(150), S(200), S(150 + 780 * k), S(640)], fill=(40, 52, 46), outline=(120, 90, 50), width=S(14))
    if k >= 1:
        if t >= T['izvin']: big_text(G, 'sorry = polite', 540, 240, 56, WHITE, black=False)
        cross(G, 230, 270, 850, 320, clamp((t - T['vezhl'] + 0.1) / 0.3) * 0)  # без зачёркивания, просто держим
        if t >= T['uvazh']: big_text(G, 'polite = respect', 540, 370, 56, WHITE)
        if t >= T['viny']: big_text(G, '≠ guilt', 540, 500, 68, YEL)
def sc_what(G, t):
    plate(G, t, T['delat'] - 0.5, 'WHAT TO DO?', 540, 260, 84, YEL, INK, rot=-3)
    for j in range(3):
        if t >= T['tri'] + j * 0.15:
            paste(G, plate_img(str(j + 1), 130, INK, WHITE, pad=34), 300 + j * 240, 600, back((t - T['tri'] - j * 0.15) / 0.25))
def clock(G, cx, cy, r=55):
    d = ImageDraw.Draw(G); d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], outline=INK, width=S(12))
    d.line([S(cx), S(cy), S(cx), S(cy - r * .7)], fill=INK, width=S(10)); d.line([S(cx), S(cy), S(cx + r * .5), S(cy + r * .2)], fill=RED, width=S(10))
def mixup(G, cx, cy):
    big_text(G, '?!', cx, cy - 70, 120, INK)
def foot(G, cx, cy):
    d = ImageDraw.Draw(G)
    d.ellipse([S(cx - 42), S(cy - 30), S(cx + 42), S(cy + 75)], fill=INK)
    for j, (dx, r) in enumerate(((-38, 16), (-12, 14), (12, 13), (34, 11), (52, 9))):
        d.ellipse([S(cx + dx - r), S(cy - 62 - r + abs(dx) * 0.3), S(cx + dx + r), S(cy - 62 + r + abs(dx) * 0.3)], fill=INK)
def sc_rule1(G, t):
    plate(G, t, B[7], '1', 340, 70, 60, YEL, INK)
    plate(G, t, T['nakos'] - 0.3, 'ONLY IF YOU\nMESSED UP', 340, 210, 58, INK, WHITE, rot=-2)
    for j, (k, lab, ic) in enumerate((('opozd', 'late', clock), ('perep', 'mixed up', mixup), ('nogu', 'stepped on\na foot', foot))):
        if t < T[k] - 0.15: continue
        y = 420 + j * 185; s = back((t - T[k] + 0.15) / 0.28)
        card(G, 320, y, 560, 175, k=s)
        if s > 0.9:
            ic(G, 150, y + (0 if ic is clock else 30), 55) if ic is clock else ic(G, 150, y + 20)
            ImageDraw.Draw(G).text((S(240), S(y - 32)), lab, font=font(62), fill=INK)
def sc_rule2(G, t):
    plate(G, t, B[8], '2', 540, 70, 60, YEL, INK)
    plate(G, t, T['menyay'], 'SORRY → THANK YOU', 540, 200, 52, INK, WHITE, rot=-2, t1=T['mozhno'] - 0.55)
    if t >= T['ne2'] and t < T['mozhno'] - 0.4:
        bubble(G, 'Sorry for the wait', 540, 340, 66, WHITE, back((t - T['ne2']) / 0.25), strike=(t - T['zader'] - 0.3) / 0.3 if t >= T['zader'] + 0.3 else 0)
    if t >= T['spas2'] and t < T['mozhno'] - 0.4:
        bubble(G, 'Thanks for waiting', 540, 510, 70, YEL, back((t - T['spas2']) / 0.25))
    plate(G, t, T['mozhno'] - 0.4, "WAIT, THAT'S\nALLOWED?", 540, 340, 64, WHITE, INK, border=INK, rot=-2)
    plate(G, t, T['mozhno2'], 'IT IS', 540, 560, 90, YEL, INK, rot=4)
MSG = [('Sorry,', ' to bother.'), ('Sorry,', ' question:'), ("Where's the file?", ''), ('Sorry.', '')]
def sc_rule3(G, t):
    plate(G, t, B[9], '3', 540, 70, 60, YEL, INK)
    d = phone_frame(G, 650, 520, 540, 760)
    big_text(G, 'before you hit send', 650, 170, 34, GREY, black=False)
    marks = [0, 1, 3]; step = (T['prich'] - T['vych']) / 3
    nleft = 3
    f = font(46, False); fb = font(46)
    for j, (a, b) in enumerate(MSG):
        y = 240 + j * 130
        if t < T['soob'] - 0.4 + j * 0.12: continue
        x0 = 410
        d.text((S(x0), S(y)), a, font=fb, fill=INK)
        wa = d.textbbox((0, 0), a, font=fb)[2] / SS
        d.text((S(x0 + wa), S(y)), b, font=f, fill=INK)
        if j in marks:
            ts = T['vych'] + marks.index(j) * step
            if t >= ts:
                k = clamp((t - ts) / 0.25); nleft -= 1 if k >= 1 else 0
                d.line([S(x0 - 6), S(y + 30), S(x0 - 6 + (wa + 6) * k), S(y + 30)], fill=RED, width=S(10))
    tlast = max([T['vych'] + i * step + 0.25 for i in range(3) if t >= T['vych'] + i * step + 0.25] or [0])
    counter(G, t, nleft, 650, 950, 50, tlast if tlast else 0)
def sc_final(G, t):
    if t < T['vsyo'] - 0.1:
        plate(G, t, B[10], 'WANT TO SEE IT\nANOTHER WAY?', 540, 160, 54, WHITE, INK, border=INK, rot=-2, t1=T['vezhliv'] - 0.5)
        if t >= T['vezhliv'] - 0.5:
            paste(G, plate_img("YOU'RE POLITE", 72, WHITE, INK, pad=28, border=INK), 540, 185, back((t - T['vezhliv'] + 0.5) / 0.28))
            cross(G, 300, 120, 780, 250, clamp((t - T['vezhliv']) / 0.3))
        plate(G, t, T['zaranee'], 'GUILTY IN\nADVANCE', 540, 420, 90, RED, WHITE, rot=-3)
    else:
        counter(G, t, 0, 540, 230, 50)
        plate(G, t, T['netupi'] - 0.15, "DON'T\nBE DUMB", 540, 470, 100, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]: sc_intro(G, t)
    elif t < B[2]: plate(G, t, T['stop'] - 0.05, "STOP.\nYOU'RE BEING DUMB", 540, 420, 64, YEL, INK, rot=-3)
    elif t < B[3]: sc_zachto(G, t)
    elif t < B[4]: sc_podvoh(G, t)
    elif t < B[5]: sc_ten(G, t)
    elif t < B[6]: sc_board(G, t)
    elif t < B[7]: sc_what(G, t)
    elif t < B[8]: sc_rule1(G, t)
    elif t < B[9]: sc_rule2(G, t)
    elif t < B[10]: sc_rule3(G, t)
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
SMALL_ = (540, FEET, 0.36, 190, 0.72)
LAY = [(0, *PH), (B[1], *DEF), (B[2], *LEFT), (B[3], *DEF), (B[4], *SMALL_), (B[5], *DEF), (B[6], *RIGHT),
       (B[7], *RIGHT), (B[8], *DEF), (B[9], *PH), (B[10], *DEF)]
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
