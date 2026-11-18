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

# ---------- сцены ----------
T = {k: wt(*v) if isinstance(v, tuple) else wt(v) for k, v in dict(
    stop='Stop', no=('But', 0), vse='Everybody', razb='rich', dvesti='Six', eto='over', strashno='Scary', tak='So,',
    podozhdi='Wait', taksi='Uber', dost='Takeout', tel=('credit', 0), nu='which', kofe2=('pocket', 0), kop='pocket',
    tri=('three', 1), kak='How', otkroi='Open', posm='look', perv=('three', 2), nast='real', rezh='Cut',
    melk='keep', otn=('Take', 1), kup='buy', kofe_pei='drink', tel2=('credit', 1), vsyo=("That's", 1), netupi=('dumb.', 2)).items()}

def scales(G, t, zoom=1.0):
    appear = back((t - T['podozhdi']) / 0.35)
    if appear <= 0.01: return
    cx, cy = 495, 400; zoom *= 1.25
    def Z(x, y): return cx + (x - cx) * zoom * appear, cy + (y - cy) * zoom * appear
    drops = [(T['taksi'], 'UBER\n$2,600', 6), (T['dost'] + 0.1, 'TAKEOUT\n$5,000+', -16), (T['tel'], 'CREDIT CARD\nINTEREST', -24)]
    target, prev, tt = 12, 12, None   # угол: + левая чаша вниз
    for t0, _, ang in drops:
        if t >= t0 + 0.3: prev, target, tt = target, ang, t0 + 0.3
    ang = target if tt is None else target + (prev - target) * math.exp(-(t - tt) * 7) * math.cos((t - tt) * 18)
    a = math.radians(ang); L = 250
    d = ImageDraw.Draw(G)
    # стойка
    x0, y0 = Z(cx, cy); x1, y1 = Z(cx, cy + 380)
    d.line([S(x0), S(y0), S(x1), S(y1)], fill=INK, width=S(14 * zoom))
    bx0, by0 = Z(cx - 110, cy + 380); bx1, by1 = Z(cx + 110, cy + 400)
    d.rounded_rectangle([S(bx0), S(by0), S(bx1), S(by1)], radius=S(8), fill=INK)
    lx, ly = cx - L * math.cos(a), cy + L * math.sin(a); rx, ry = cx + L * math.cos(a), cy - L * math.sin(a)
    p, q = Z(lx, ly), Z(rx, ry)
    d.line([S(p[0]), S(p[1]), S(q[0]), S(q[1])], fill=INK, width=S(12 * zoom))
    d.ellipse([S(x0 - 16 * zoom), S(y0 - 16 * zoom), S(x0 + 16 * zoom), S(y0 + 16 * zoom)], fill=YEL, outline=INK, width=S(5))
    for (px, py) in ((lx, ly), (rx, ry)):   # подвесы и чаши
        pa, pb, pc = Z(px, py), Z(px - 90, py + 170), Z(px + 90, py + 170)
        d.line([S(pa[0]), S(pa[1]), S(pb[0]), S(pb[1])], fill=INK, width=S(4)); d.line([S(pa[0]), S(pa[1]), S(pc[0]), S(pc[1])], fill=INK, width=S(4))
        e0, e1 = Z(px - 120, py + 160), Z(px + 120, py + 195)
        d.chord([S(e0[0]), S(e0[1] - 20), S(e1[0]), S(e1[1])], 0, 180, fill=INK)
    # кофе на левой чаше (после «копейки» сжимается)
    shrink = 1 - 0.55 * eo((t - T['kop']) / 0.4)
    c = Z(lx, ly + 160 - 75 * shrink)
    cup(G, c[0], c[1], 130, zoom * appear * shrink)
    plate(G, t, T['kop'], 'POCKET CHANGE', c[0], c[1] - 150, 52, YEL, INK, rot=6)
    # грузы на правой чаше
    hi = t >= T['tri']
    stack_y = ry + 160
    for i, (t0, txt, _) in enumerate(drops):
        if t < t0: continue
        im = plate_img(txt, 26 if i == 2 else 34, INK, WHITE, pad=18, border=YEL if hi else None)
        hgt = im.height / SS
        fall = eo((t - t0) / 0.3); y_end = stack_y - hgt / 2; stack_y -= hgt + 4
        y = -150 + (y_end + 150) * fall
        pz = Z(rx, y); paste(G, im, pz[0], pz[1], zoom * appear)

def phone(G, t):
    t0 = T['kak']
    if t < t0: return
    sl = eo((t - t0) / 0.4); cx, cy = 680, 450 + (1 - sl) * 900
    d = ImageDraw.Draw(G); w, h = 520, 820
    d.rounded_rectangle([S(cx - w / 2), S(cy - h / 2), S(cx + w / 2), S(cy + h / 2)], radius=S(60), fill=INK)
    d.rounded_rectangle([S(cx - w / 2 + 18), S(cy - h / 2 + 18), S(cx + w / 2 - 18), S(cy + h / 2 - 18)], radius=S(44), fill=WHITE)
    d.text((S(cx - w / 2 + 50), S(cy - h / 2 + 60)), 'Last month', font=font(42), fill=INK)
    rows = [('Takeout', '$460'), ('Uber', '$220'), ('Card interest', '$140'), ('Coffee shops', '$90'), ('Subscriptions', '$60')]
    for i, (a, b) in enumerate(rows):
        ta = T['posm'] + i * 0.3
        if t < ta: continue
        y = cy - h / 2 + 160 + i * 115; al = int(255 * clamp((t - ta) / 0.2))
        col = INK + (al,)
        d.text((S(cx - w / 2 + 50), S(y)), a, font=font(33, False), fill=col)
        bb = d.textbbox((0, 0), b, font=font(33))
        d.text((S(cx + w / 2 - 50) - (bb[2] - bb[0]), S(y)), b, font=font(33), fill=col)
        d.line([S(cx - w / 2 + 50), S(y + 70), S(cx + w / 2 - 50), S(y + 70)], fill=(225, 225, 225, al), width=S(2))
        if i < 3 and t >= T['perv'] + i * 0.25:
            d.rounded_rectangle([S(cx - w / 2 + 34), S(y - 18), S(cx + w / 2 - 34), S(y + 58)], radius=S(14), outline=YEL, width=S(7))
    plate(G, t, T['nast'], 'YOUR REAL "COFFEE"', cx - 80, cy + 470, 40, YEL, INK, rot=-5)

def cuts(G, t):
    items = [('UBER  $2,600', 230), ('TAKEOUT  $5,000+', 380), ('CARD INTEREST', 530)]
    t_in = B[11]
    for i, (txt, y) in enumerate(items):
        tc = T['rezh'] + 0.15 + i * 0.32
        im = plate_img(txt, 44, INK, WHITE, pad=24)
        if t < tc:
            paste(G, im, 540, y, back((t - t_in - i * 0.08) / 0.25)); continue
        k = (t - tc) / 0.6
        if k > 1: continue
        hw = im.width // 2; L = im.crop((0, 0, hw, im.height)); R = im.crop((hw, 0, im.width, im.height))
        dx = 30 + 120 * k; dy = 400 * k * k
        paste(G, L, 540 - im.width / SS / 4 - dx, y + dy, 1, 12 * k, 1 - k); paste(G, R, 540 + im.width / SS / 4 + dx, y + dy, 1, -12 * k, 1 - k)
        if k < 0.25:   # линия разреза
            d = ImageDraw.Draw(G); d.line([S(540), S(y - 60), S(540), S(y + 60)], fill=YEL, width=S(8))
    if t >= T['melk']:
        cup(G, 540, 470, 170, back((t - T['melk']) / 0.3))
        plate(G, t, T['melk'] + 0.3, 'KEEP IT', 540, 700, 46, YEL, INK, rot=-3, t1=T['otn'] - 0.1)
    plate(G, t, T['otn'], "CUT EVERYTHING =\nYOU'LL SNAP", 540, 700, 46, INK, WHITE, rot=3)
    plate(G, t, T['kup'], 'AND BUY BIGGER', 540, 210, 44, RED, WHITE, rot=-4)

def final(G, t):
    if t < T['vsyo']:
        cup(G, 360, 420, 170, back((t - T['kofe_pei'] + 0.5) / 0.3))
        plate(G, t, T['kofe_pei'], 'COFFEE ✓', 360, 640, 44, YEL, INK, rot=-3)
        if t >= T['tel2']:
            sc = back((t - T['tel2']) / 0.28)
            paste(G, plate_img('CARD\nINTEREST', 44, INK, WHITE), 760, 470, sc, 4)
            if t >= T['tel2'] + 0.6:
                k = eo((t - T['tel2'] - 0.6) / 0.25); d = ImageDraw.Draw(G)
                d.line([S(620), S(370), S(620 + 280 * k), S(370 + 200 * k)], fill=RED, width=S(16))
                d.line([S(900), S(370), S(900 - 280 * k), S(370 + 200 * k)], fill=RED, width=S(16))
    else:
        plate(G, t, T['netupi'] - 0.15, "DON'T\nBE DUMB", 540, 470, 100, YEL, INK, rot=-4)

def graphics(t):
    G = Image.new('RGBA', (WD * SS, GH * SS), (0, 0, 0, 0))
    if t < B[1]:
        pass
    elif t < B[2]:
        plate(G, t, T['stop'] - 0.05, "STOP.\nYOU'RE BEING DUMB", 540, 420, 64, YEL, INK, rot=-3)
        plate(G, t, T['no'], 'but not where you think', 540, 680, 42, INK, WHITE, rot=2)
    elif t < B[3]:
        cup(G, 540, 300, 150, back((t - B[2] - 0.03) / 0.3))
        plate(G, t, T['vse'], '"SKIP THE LATTE', 540, 540, 54, WHITE, INK, border=INK)
        plate(G, t, T['razb'], '= GET RICH"', 540, 680, 54, WHITE, INK, border=INK, rot=-2)
    elif t < B[4]:
        plate(G, t, T['dvesti'], '$6 × 365 days', 540, 330, 60, WHITE, INK, border=INK)
        if t >= T['eto']:
            k = eo((t - T['eto']) / 0.9); val = int(2190 * k / 10) * 10
            txt = f'${val:,}'
            f = font(150); d = ImageDraw.Draw(G); bb = d.textbbox((0, 0), txt, font=f)
            sh = math.sin(t * 60) * 6 if t > T['strashno'] else 0
            col = RED if k >= 1 else INK
            d.text((S(540 + sh) - (bb[2] - bb[0]) / 2, S(480)), txt, font=f, fill=col)
            d.text((S(540) - d.textbbox((0, 0), 'a year', font=font(44, False))[2] / 2, S(650)), 'a year', font=font(44, False), fill=INK)
        plate(G, t, T['strashno'], 'SCARY?', 820, 200, 44, RED, WHITE, rot=8)
    elif t < B[10]:
        if t < T['podozhdi']:
            cup(G, 540, 420, 200, 1 - 0.3 * eo((t - T['tak'] - 0.6) / 0.3), rot=-20 * eo((t - T['tak'] - 0.6) / 0.3))
            plate(G, t, T['tak'] + 0.2, 'QUIT COFFEE?', 540, 680, 60, WHITE, INK, border=INK)
        else:
            z = 1 + 0.06 * eo((t - T['nu']) / 0.5) if t >= T['nu'] else 1
            scales(G, t, z)
    elif t < B[11]:
        phone(G, t)
    elif t < B[12]:
        cuts(G, t)
    else:
        final(G, t)
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
from words import END
# раскладки: (начало, cx персонажа, y ног, масштаб, сдвиг графики gy, масштаб графики gs)
# безопасная зона Reels: всё между ~250 и ~1530 по высоте, справа внизу не ближе ~140 px к краю
SUB_Y = 1410; FEET = 1335
DEF = (540, FEET, 0.45, 190, 0.72)
LAY = [(0, 540, FEET, 0.75, 0, 1.0), (B[1], *DEF), (B[2], 270, FEET, 0.5, 190, 0.72), (B[3], 790, FEET, 0.5, 190, 0.72),
       (B[4], *DEF), (T['podozhdi'] - 0.2, 540, 660, 0.35, 470, 1.0), (B[10], 240, FEET, 0.52, 270, 1.0),
       (B[11], *DEF), (B[12], *DEF)]
def layout(t):
    k = max(j for j, l in enumerate(LAY) if l[0] <= t); cur = LAY[k]
    if k == 0: return cur[1:]
    prev = LAY[k - 1]; e = eo((t - cur[0]) / 0.45)
    ch = tuple(p + (q - p) * e for p, q in zip(prev[1:4], cur[1:4]))
    return ch + cur[4:]
I_S = LAY[0][3]; PXCM_FEET = FEET
PXCM = 1241 * I_S / 180   # рост фигуры в пикселях (1241 при масштабе 1) = 180 см
def board(bg, t):
    d = ImageDraw.Draw(bg); f = ImageFont.truetype(FB, 40); fs = ImageFont.truetype(FX, 30)
    for cm in range(0, 241, 10):
        y = PXCM_FEET - cm * PXCM
        if y < 0: continue
        main = cm == 180
        d.line([0, y, WD, y], fill=INK if main else (150, 150, 160), width=7 if main else 3)
        if cm % 20 == 0 or main:
            for x in (24, WD - 24 - d.textbbox((0, 0), str(cm), font=f if main else fs)[2]):
                d.text((x, y - (50 if main else 38)), str(cm), font=f if main else fs, fill=INK if main else (110, 110, 120))
def frame(i):
    t = i / FPS
    bg = Image.new('RGB', (WD, HT), BG)
    if t < B[1]:   # мигалка + ростовая доска
        on = int(t * 6) % 2
        ov = Image.new('RGB', (WD, HT), BG); d = ImageDraw.Draw(ov)
        d.rectangle([0, 0, WD // 2, HT], fill=(255, 150, 150) if on else (165, 185, 255))
        d.rectangle([WD // 2, 0, WD, HT], fill=(165, 185, 255) if on else (255, 150, 150))
        bg = Image.blend(bg, ov, 0.4); board(bg, t)
    cx, feet, s, gy, gs = layout(t)
    G = graphics(t)
    if gs != 1: G = G.resize((int(WD * gs), int(GH * gs)), Image.LANCZOS)
    bg.paste(G, (int((WD - G.width) / 2), int(gy)), G)
    subs(bg, t, SUB_Y)
    bot = feet + 70 * s
    cw, chh = int(1080 * s), int(1600 * s)
    ch = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(CH_CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), WHITE); layer.paste(ch, (int(cx - cw / 2 + xoff[i]), int(bot - chh)))
    out = Image.fromarray((np.asarray(bg, np.uint16) * np.asarray(layer, np.uint16) // 255).astype(np.uint8)).convert('RGBA')
    if t < B[1]:   # табличка на груди и стакан в руке — поверх персонажа
        F = Image.new('RGBA', (WD * SS, HT * SS), (0, 0, 0, 0))
        plate(F, t, 0.15, 'SUSPECT', 540, FEET - 0.54 * 1241 * I_S, 54, RED, WHITE, rot=-3)
        cup(F, 540 + 330 * I_S / 0.9, FEET - 0.45 * 1241 * I_S, 95, back((t - 0.4) / 0.3), rot=-10)
        F = F.resize((WD, HT), Image.LANCZOS); out.alpha_composite(F)
    return out.convert('RGB')

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
