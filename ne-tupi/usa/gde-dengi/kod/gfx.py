"""Графические элементы для 16:9. Рисуем в 2x (SS) на полном кадре, координаты в пикселях 1920x1080."""
import math, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
WD, HT = 1920, 1080; SS = 2
BG = (247, 245, 240); YEL = (255, 212, 0); RED = (226, 48, 48); INK = (17, 17, 17); WHITE = (255, 255, 255)
GRAY = (190, 190, 190); GREEN = (40, 170, 90); BLUE = (60, 110, 230)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
FE = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
@lru_cache(None)
def font(sz, black=True): return ImageFont.truetype(FB if black else FX, int(sz * SS))
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(t):
    t = clamp(t); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def S(v): return int(round(v * SS))
def vis(t, ta, te):
    """масштаб появления и альфа исчезновения; None если не видно"""
    if t < ta or (te is not None and t > te + 0.2): return None
    sc = back((t - ta) / 0.28)
    al = 1.0 if te is None or t < te else 1 - (t - te) / 0.2
    return sc, al

@lru_cache(None)
def plate_img(text, sz, bg, fg, pad=26, border=None, black=True):
    f = font(sz, black); lines = text.split('\n')
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    ws = [d0.textbbox((0, 0), l, font=f) for l in lines]
    lh = int(sz * 1.18 * SS); w = max(b[2] - b[0] for b in ws) + S(pad) * 2; h = lh * len(lines) + S(pad) * 1.4
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if bg is not None:
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=S(16), fill=bg, outline=border, width=S(5) if border else 0)
    for i, (l, b) in enumerate(zip(lines, ws)):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], S(pad) * 0.7 + i * lh + (lh - sz * SS) / 2 - S(sz * 0.12)), l, font=f, fill=fg)
    return im

def paste(G, im, cx, cy, scale=1.0, rot=0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    G.alpha_composite(im, (int(S(cx) - im.width / 2), int(S(cy) - im.height / 2)))

# ---------------- элементы: f(G, t, ta, te, **kw) ----------------
def plate(G, t, ta, te, text, x, y, sz=56, bg=YEL, fg=INK, rot=0, border=None, black=True):
    v = vis(t, ta, te)
    if v: paste(G, plate_img(text, int(sz * 1.25 / 1.25), bg, fg, border=border, black=black), x, y, v[0], rot, v[1])
def card(G, t, ta, te, text, x, y, sz=44, rot=0):          # белая карточка с рамкой
    plate(G, t, ta, te, text, x, y, sz, WHITE, INK, rot, INK)
def dark(G, t, ta, te, text, x, y, sz=44, rot=0):
    plate(G, t, ta, te, text, x, y, sz, INK, WHITE, rot)
def red(G, t, ta, te, text, x, y, sz=48, rot=0):
    plate(G, t, ta, te, text, x, y, sz, RED, WHITE, rot)
def txt(G, t, ta, te, text, x, y, sz=60, col=INK, rot=0):
    plate(G, t, ta, te, text, x, y, sz, None, col, rot)

@lru_cache(None)
def emoji_img(ch):
    f = ImageFont.truetype(FE, 109); im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True); return im.crop(im.getbbox())
def emoji(G, t, ta, te, ch, x, y, size=150, rot=0, bob=0, gray=None):
    v = vis(t, ta, te)
    if not v: return
    im = emoji_img(ch); k = S(size) / max(im.size)
    if gray is not None and t >= gray:   # обесцветить
        g = im.convert('LA').convert('RGBA'); g.putalpha(im.getchannel('A').point(lambda a: a // 2)); im = g
    yy = y + (math.sin(t * 3 + x) * bob if bob else 0)
    paste(G, im, x, yy, k * v[0], rot, v[1])

def strike(G, t, ta, te, x, y, w=220, h=220, col=RED):      # красный крест
    if t < ta or (te and t > te): return
    k = eo((t - ta) / 0.25); d = ImageDraw.Draw(G)
    d.line([S(x - w / 2), S(y - h / 2), S(x - w / 2 + w * k), S(y - h / 2 + h * k)], fill=col, width=S(16))
    if k >= 1:
        k2 = eo((t - ta - 0.25) / 0.2)
        d.line([S(x + w / 2), S(y - h / 2), S(x + w / 2 - w * k2), S(y - h / 2 + h * k2)], fill=col, width=S(16))
def crossline(G, t, ta, te, x, y, w=400, col=RED):            # зачёркивание линией
    if t < ta or (te and t > te): return
    k = eo((t - ta) / 0.25); ImageDraw.Draw(G).line([S(x - w / 2), S(y + 10), S(x - w / 2 + w * k), S(y - 10)], fill=col, width=S(12))
def check(G, t, ta, te, x, y, s=60, col=GREEN):
    if t < ta or (te and t > te): return
    k = eo((t - ta) / 0.25); d = ImageDraw.Draw(G)
    p = [(x - s * .5, y), (x - s * .1, y + s * .4), (x + s * .6, y - s * .5)]
    if k < .4: d.line([S(p[0][0]), S(p[0][1]), S(p[0][0] + (p[1][0] - p[0][0]) * k / .4), S(p[0][1] + (p[1][1] - p[0][1]) * k / .4)], fill=col, width=S(14))
    else:
        q = (k - .4) / .6
        d.line([S(p[0][0]), S(p[0][1]), S(p[1][0]), S(p[1][1])], fill=col, width=S(14))
        d.line([S(p[1][0]), S(p[1][1]), S(p[1][0] + (p[2][0] - p[1][0]) * q), S(p[1][1] + (p[2][1] - p[1][1]) * q)], fill=col, width=S(14))

def arrow(G, t, ta, te, x0, y0, x1, y1, col=INK, w=10):
    if t < ta or (te and t > te + 0.2): return
    k = eo((t - ta) / 0.35); x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    d = ImageDraw.Draw(G); d.line([S(x0), S(y0), S(x), S(y)], fill=col, width=S(w))
    a = math.atan2(y - y0, x - x0); L = 28
    d.polygon([(S(x), S(y)), (S(x - L * math.cos(a - .5)), S(y - L * math.sin(a - .5))), (S(x - L * math.cos(a + .5)), S(y - L * math.sin(a + .5)))], fill=col)

def counter(G, t, ta, te, v0, v1, x, y, sz=140, dur=1.0, fmt='{}', col=INK, endcol=None):
    if t < ta or (te and t > te): return
    k = eo((t - ta) / dur); v = int(round(v0 + (v1 - v0) * k))
    s = fmt.format(f'{v:,}'.replace(',', ' '))
    c = endcol if endcol and k >= 1 else col
    paste(G, plate_img(s, sz, None, c), x, y, 1.0)

def bars(G, t, ta, te, x, y, items, maxh=300, bw=120, gap=90):
    """items: (подпись, значение 0..1, цвет, время_появления)"""
    if t < ta or (te and t > te): return
    d = ImageDraw.Draw(G); n = len(items); x0 = x - (n * bw + (n - 1) * gap) / 2
    d.line([S(x0 - 30), S(y), S(x0 + n * bw + (n - 1) * gap + 30), S(y)], fill=INK, width=S(6))
    for i, (lab, val, col, t0) in enumerate(items):
        if t < t0: continue
        h = maxh * val * eo((t - t0) / 0.5); bx = x0 + i * (bw + gap)
        d.rounded_rectangle([S(bx), S(y - h), S(bx + bw), S(y)], radius=S(10), fill=col)
        paste(G, plate_img(lab, 28, None, INK, pad=6), bx + bw / 2, y + 55)

def cloud(G, t, ta, te, text, x, y, w=420, sz=40, fg=INK, bubbles=True):
    v = vis(t, ta, te)
    if not v: return
    im = cloud_img(text, w, sz, fg, bubbles); paste(G, im, x, y, v[0], 0, v[1])
@lru_cache(None)
def cloud_img(text, w, sz, fg, bubbles):
    p = plate_img(text, sz, None, fg); W2 = max(S(w), p.width + S(80)); H2 = p.height + S(120)
    im = Image.new('RGBA', (W2 + S(200), H2 + S(200)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rnd = random.Random(len(text)); cx, cy = im.width / 2, H2 / 2 + S(70)
    blobs = [(cx + (W2 / 2 - S(50)) * math.cos(a), cy + (H2 / 2 - S(40)) * math.sin(a), S(55 + rnd.random() * 25)) for a in [i * math.pi / 5 for i in range(10)]]
    for bx, by, r in blobs: d.ellipse([bx - r - S(5), by - r - S(5), bx + r + S(5), by + r + S(5)], fill=INK)
    d.ellipse([cx - W2 / 2 - S(5), cy - H2 / 2 - S(5), cx + W2 / 2 + S(5), cy + H2 / 2 + S(5)], fill=INK)
    for bx, by, r in blobs: d.ellipse([bx - r, by - r, bx + r, by + r], fill=WHITE)
    d.ellipse([cx - W2 / 2, cy - H2 / 2, cx + W2 / 2, cy + H2 / 2], fill=WHITE)
    if bubbles:
        for k, r in enumerate((S(18), S(11))):
            bx, by = cx - W2 * 0.3 - k * S(30), cy + H2 / 2 + S(25) + k * S(28)
            d.ellipse([bx - r - S(4), by - r - S(4), bx + r + S(4), by + r + S(4)], fill=INK); d.ellipse([bx - r, by - r, bx + r, by + r], fill=WHITE)
    im.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2))); return im

def battery(G, t, ta, te, x, y, l0=1.0, l1=0.03, dur=1.5, charge_at=None):
    v = vis(t, ta, te)
    if not v: return
    lv = l0 + (l1 - l0) * eo((t - ta - 0.3) / dur)
    if charge_at and t > charge_at: lv = l1 + (1 - l1) * eo((t - charge_at) / 1.5)
    d = ImageDraw.Draw(G); w, h = 300 * v[0], 140 * v[0]
    if h < 40: return
    d.rounded_rectangle([S(x - w / 2), S(y - h / 2), S(x + w / 2), S(y + h / 2)], radius=S(18), outline=INK, width=S(10))
    d.rounded_rectangle([S(x + w / 2 + 4), S(y - h / 5), S(x + w / 2 + 22), S(y + h / 5)], radius=S(5), fill=INK)
    col = RED if lv < 0.2 else (YEL if lv < 0.5 else GREEN)
    if lv > 0.005 and h > 40: d.rounded_rectangle([S(x - w / 2 + 16), S(y - h / 2 + 16), S(x - w / 2 + 16 + (w - 32) * lv), S(y + h / 2 - 16)], radius=S(8), fill=col)
    paste(G, plate_img(f'{int(lv * 100)}%', 40, None, INK), x, y + h / 2 + 45)

def tabs(G, t, ta, te, x, y, n=12, t_close=None):
    if t < ta or (te and t > te): return
    for i in range(n):
        t0 = ta + i * 0.12
        if t < t0: continue
        sc = back((t - t0) / 0.2)
        if t_close and t > t_close + i * 0.05: sc = 1 - eo((t - t_close - i * 0.05) / 0.15)
        if sc <= 0.01: continue
        im = plate_img('COURSE', 26, WHITE, INK, pad=14, border=INK)
        paste(G, im, x - 330 + (i % 4) * 220, y - 110 + (i // 4) * 110 + (i % 2) * 10, sc, (i * 7) % 11 - 5)

def flash(G, t, ta, te, x, y, text):        # мигающая на 1 сек размытая плашка «спойлер»
    if t < ta or t > ta + 1.2: return
    k = 1 - abs((t - ta - 0.6) / 0.6)
    im = plate_img(text, 60, YEL, INK)
    from PIL import ImageFilter
    im = im.filter(ImageFilter.GaussianBlur(S(6)))
    paste(G, im, x, y, 0.9 + 0.1 * k, -3, clamp(k * 1.5))

# ---------------- перекрёсток ----------------
LABELS = ['DOCTOR', 'IT', 'INFLUENCER', 'OWN BUSINESS', 'DESIGN', 'MOVE', 'MUSIC', 'FREELANCE', 'CHEF', 'SPORTS', 'COLLEGE', 'OFFICE']
def cross(G, t, ta, te, x, y, r=330, alive=1.0, hi=None, labels=True, alive_to=None, alive_t=None, n=24, sz=26):
    """дороги-лучи из центра; alive — доля «живых» (чёрных) дорог, остальные серые и короче; hi — индекс жёлтой"""
    v = vis(t, ta, te)
    if not v: return
    sc = v[0]
    if alive_to is not None and alive_t is not None: alive = alive + (alive_to - alive) * eo((t - alive_t) / 2.0)
    d = ImageDraw.Draw(G); rnd = random.Random(7); order = list(range(n)); rnd.shuffle(order)
    rank = {k: j for j, k in enumerate(order)}
    for k in range(n):
        a = -math.pi / 2 + k * 2 * math.pi / n
        live = rank[k] < alive * n or k == hi
        L = r * sc * (1.0 if live else 0.55); col = YEL if k == hi else (INK if live else (215, 213, 208))
        x1, y1 = x + L * math.cos(a), y + L * math.sin(a) * 0.62
        d.line([S(x), S(y), S(x1), S(y1)], fill=col, width=S(10 if k == hi else 6))
        if labels and live and k % 2 == 0 and sc > 0.9:
            lab = LABELS[(k // 2) % len(LABELS)]
            paste(G, plate_img(lab, sz, YEL if k == hi else WHITE, INK, pad=10, border=None if k == hi else INK), x1 + 30 * math.cos(a), y1 + 22 * math.sin(a), 1.0)
    d.ellipse([S(x - 26 * sc), S(y - 16 * sc), S(x + 26 * sc), S(y + 16 * sc)], fill=YEL, outline=INK, width=S(5))


# ---------------- башня коробок (сквозной образ ролика «нет») ----------------
def boxes(G, t, ta, te, x, y, labels, gone=(), w=250, h=84, mine=None, sz=30):
    """коробки снизу вверх; gone[i] — время, когда i-я коробка улетает; mine — время появления своей жёлтой «МОЁ»"""
    v = vis(t, ta, te)
    if not v: return
    d = ImageDraw.Draw(G); k = 0
    for i, lab in enumerate(labels):
        t0 = ta + i * 0.12
        if t < t0: continue
        sc = back((t - t0) / 0.25); dx = dy = 0; al = 1.0
        if i < len(gone) and gone[i] is not None and t > gone[i]:
            q = eo((t - gone[i]) / 0.5); dx = 500 * q * (1 if i % 2 else -1); dy = -260 * q; al = 1 - q
            if al <= 0.02: continue
        else:
            k += 1
        yy = y - (k - 0.5) * (h + 6) if not (i < len(gone) and gone[i] is not None and t > gone[i]) else y - (i + 0.5) * (h + 6)
        im = box_img(lab, w, h, sz, False)
        paste(G, im, x + dx + ((i * 37) % 23 - 11), yy + dy, sc, ((i * 13) % 7 - 3), al)
    if mine is not None and t >= mine:
        paste(G, box_img('MINE', w, h, sz, True), x, y - 0.5 * (h + 6), back((t - mine) / 0.3))
@lru_cache(None)
def box_img(lab, w, h, sz, yel):
    im = Image.new('RGBA', (S(w), S(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S(w) - 1, S(h) - 1], fill=YEL if yel else WHITE, outline=INK, width=S(5))
    d.rectangle([S(w / 2 - 14), 0, S(w / 2 + 14), S(h) - 1], fill=(225, 222, 214) if not yel else (240, 190, 0))
    p = plate_img(lab, sz, None, INK, pad=4); im.alpha_composite(p, (int((im.width - p.width) / 2), int((im.height - p.height) / 2))); return im

def hourglass(G, t, ta, te, x, y, size=200, dur=4.0):
    v = vis(t, ta, te)
    if not v: return
    s = size * v[0]; d = ImageDraw.Draw(G); k = clamp((t - ta) / dur)
    w2, h2 = s * 0.45, s * 0.5
    d.line([S(x - w2), S(y - h2), S(x + w2), S(y - h2)], fill=INK, width=S(10)); d.line([S(x - w2), S(y + h2), S(x + w2), S(y + h2)], fill=INK, width=S(10))
    top = [(S(x - w2 * .8), S(y - h2 + 8)), (S(x + w2 * .8), S(y - h2 + 8)), (S(x), S(y))]
    bot = [(S(x), S(y)), (S(x + w2 * .8), S(y + h2 - 8)), (S(x - w2 * .8), S(y + h2 - 8))]
    d.polygon(top, outline=INK, width=S(6)); d.polygon(bot, outline=INK, width=S(6))
    lt = (1 - k); yt = y - h2 * lt * 0.9
    if lt > 0.02: d.polygon([(S(x - w2 * .8 * lt), S(yt)), (S(x + w2 * .8 * lt), S(yt)), (S(x), S(y - 4))], fill=YEL)
    if k > 0.02:
        yb = y + h2 - 8 - h2 * k * 0.8
        d.polygon([(S(x - w2 * .8), S(y + h2 - 8)), (S(x + w2 * .8), S(y + h2 - 8)), (S(x + w2 * .8 * (1 - k * .8)), S(yb)), (S(x - w2 * .8 * (1 - k * .8)), S(yb))], fill=YEL)
    if 0.02 < k < 0.98: d.line([S(x), S(y), S(x), S(y + h2 - 8)], fill=YEL, width=S(4))

def meter(G, t, ta, te, x, y, label, v0=0.0, v1=1.0, dur=2.0, w=520, col=RED):   # шкала, которая наполняется
    v = vis(t, ta, te)
    if not v: return
    k = v0 + (v1 - v0) * eo((t - ta - 0.2) / dur); d = ImageDraw.Draw(G); ww = w * v[0]
    d.rounded_rectangle([S(x - ww / 2), S(y - 30), S(x + ww / 2), S(y + 30)], radius=S(14), outline=INK, width=S(6))
    if k > 0.01: d.rounded_rectangle([S(x - ww / 2 + 10), S(y - 20), S(x - ww / 2 + 10 + (ww - 20) * k), S(y + 20)], radius=S(8), fill=col)
    paste(G, plate_img(label, 30, None, INK, pad=4), x, y - 62)


# ---------------- «Где деньги?»: ведро, телефон, источник, HUD ----------------
WATER = (120, 170, 235)
HOLES = [(-1, -30), (1, 20), (-1, 85), (1, 115)]
def _bucket_shape(d, x, y, sc, label=None, fill=0.0, col=INK):
    tw, bw, h = 380 * sc, 280 * sc, 320 * sc
    top, bot = y - h / 2, y + h / 2
    d.polygon([(S(x - tw / 2), S(top)), (S(x + tw / 2), S(top)), (S(x + bw / 2), S(bot)), (S(x - bw / 2), S(bot))], fill=WHITE)
    if fill > 0.01:
        fy = bot - (h - 24 * sc) * fill; k = (fy - top) / h; wl = tw / 2 + (bw / 2 - tw / 2) * k
        d.polygon([(S(x - wl + 6), S(fy)), (S(x + wl - 6), S(fy)), (S(x + bw / 2 - 6), S(bot - 4)), (S(x - bw / 2 + 6), S(bot - 4))], fill=WATER)
    for fr in (0.18, 0.82):   # обручи
        yy = top + h * fr; hw = tw / 2 + (bw / 2 - tw / 2) * fr
        d.line([S(x - hw), S(yy), S(x + hw), S(yy)], fill=(200, 200, 200), width=S(6))
    d.polygon([(S(x - tw / 2), S(top)), (S(x + tw / 2), S(top)), (S(x + bw / 2), S(bot)), (S(x - bw / 2), S(bot))], outline=col, width=S(12))
    d.arc([S(x - tw / 2 + 10 * sc), S(top - 150 * sc), S(x + tw / 2 - 10 * sc), S(top + 120 * sc)], 200, 340, fill=col, width=S(8))
    return tw, bw, h, top, bot
def _stream(d, t, x, y0, y1, sc):
    if y1 <= y0: return
    d.rectangle([S(x - 11 * sc), S(y0), S(x + 11 * sc), S(y1)], fill=WATER)
    off = (t * 500) % 50; yy = y0 - 50 + off
    while yy < y1:
        a, b2 = max(y0, yy), min(y1, yy + 18)
        if b2 > a: d.rectangle([S(x - 4 * sc), S(a), S(x + 2 * sc), S(b2)], fill=(200, 225, 250))
        yy += 50
def bucket(G, t, ta, te, x, y, tags=(), labels=('HABIT', 'THE NEIGHBORS', 'NO PAIN', 'I DESERVE IT'), glow=None, mine=None, sc=1.0, big=None):
    """ведро-кошелёк под краном ЗАРПЛАТА; tags — времена появления бирок у дыр; glow — время, с которого 4-я дыра светится;
    mine — время, когда струя делится и рядом наполняется второе ведро «МОЁ»"""
    v = vis(t, ta, te)
    if not v: return
    sc = sc * v[0]; d = ImageDraw.Draw(G)
    split = mine is not None and t >= mine
    bx = x - (200 if split else 0) * eo((t - mine) / 0.6) if mine is not None else x
    # кран
    fx = bx - 70 * sc; fy = y - 400 * sc
    d.rounded_rectangle([S(fx - 260 * sc), S(fy - 22 * sc), S(fx + 22 * sc), S(fy + 22 * sc)], radius=S(10), fill=INK)
    d.rounded_rectangle([S(fx - 22 * sc), S(fy), S(fx + 22 * sc), S(fy + 60 * sc)], radius=S(8), fill=INK)
    paste(G, plate_img('PAYCHECK', 30, YEL, INK, pad=10), fx - 140 * sc, fy - 62 * sc, sc)
    tw, bw, h, top, bot = 380 * sc, 280 * sc, 320 * sc, y - 160 * sc, y + 160 * sc
    _bucket_shape(d, bx, y, sc, fill=0.14)
    _stream(d, t, fx, fy + 60 * sc, bot - 50 * sc, sc)
    # дыры и капли
    for k, (side, hy) in enumerate(HOLES):
        frac = (hy * sc + h / 2) / h; half = tw / 2 + (bw / 2 - tw / 2) * frac
        hx = bx + side * (half - 4); cy = y + hy * sc
        r = (20 if k < 3 else 27) * sc
        if glow is not None and k == 3 and t >= glow:
            rr = r + 10 * sc + 6 * math.sin(t * 8)
            d.ellipse([S(hx - rr), S(cy - rr), S(hx + rr), S(cy + rr)], fill=YEL)
        d.ellipse([S(hx - r), S(cy - r), S(hx + r), S(cy + r)], fill=INK)
        for j in range(3):   # капли
            q = ((t * 1.6 + j / 3 + k * 0.17) % 1.0)
            dx = side * (20 + 110 * q) * sc; dy = (60 * q + 260 * q * q) * sc
            rd = 12 * sc
            d.ellipse([S(hx + dx - rd), S(cy + dy - rd), S(hx + dx + rd), S(cy + dy + rd)], fill=WATER)
        if k < len(tags) and tags[k] is not None and t >= tags[k]:
            ts = back((t - tags[k]) / 0.3)
            paste(G, plate_img(labels[k], 28, YEL, INK, pad=10), hx + side * 150 * sc, cy - 6 * sc, ts * sc, -side * 3)
    if split:
        k = eo((t - mine) / 0.6); mx = bx + 520 * sc * k
        # вторая струя: отвод от трубы
        d.line([S(fx - 150 * sc), S(fy), S(mx), S(fy)], fill=INK, width=S(30 * sc))
        d.line([S(mx), S(fy), S(mx), S(fy + 50 * sc)], fill=INK, width=S(36 * sc))
        lv = 0.08 + 0.8 * eo((t - mine - 0.6) / 4.0)
        _bucket_shape(d, mx, y, sc * 0.95, fill=lv)
        _stream(d, t, mx, fy + 60 * sc, bot - 30 * sc - 300 * sc * lv, sc)
        paste(G, plate_img('MINE', 40, YEL, INK, pad=12), mx, bot + 50 * sc, back((t - mine - 0.3) / 0.3) * sc)
        paste(G, plate_img('LIFE', 34, WHITE, INK, pad=10, border=INK), bx, bot + 50 * sc, back((t - mine - 0.3) / 0.3) * sc)

def phone(G, t, ta, te, x, y, text, t2=None, text2=None, col2=GREEN, sz=96):
    v = vis(t, ta, te)
    if not v: return
    s = v[0]; d = ImageDraw.Draw(G); w, h = 300 * s, 520 * s
    if h < 60: return
    d.rounded_rectangle([S(x - w / 2), S(y - h / 2), S(x + w / 2), S(y + h / 2)], radius=S(40 * s), fill=WHITE, outline=INK, width=S(10))
    d.rounded_rectangle([S(x - 40 * s), S(y - h / 2 + 18 * s), S(x + 40 * s), S(y - h / 2 + 30 * s)], radius=S(6), fill=INK)
    paste(G, plate_img('BANK', 30, INK, WHITE, pad=10), x, y - 160 * s, s)
    paste(G, plate_img('BALANCE', 26, None, (130, 130, 130), pad=4), x, y - 70 * s, s)
    if t2 is not None and t >= t2: paste(G, plate_img(text2, int(sz * 0.55), None, col2), x, y + 20 * s, back((t - t2) / 0.3) * s)
    else: paste(G, plate_img(text, sz, None, RED), x, y + 20 * s, s)

def source(G, t, ta, te, year, name, x, y, ch=None):
    v = vis(t, ta, te)
    if not v: return
    a = plate_img(year, 32, INK, WHITE, pad=12); b = plate_img(name, 32, YEL, INK, pad=12)
    tw = (a.width + b.width) / SS + 12
    paste(G, a, x - tw / 2 + a.width / SS / 2, y, v[0], 0, v[1]); paste(G, b, x + tw / 2 - b.width / SS / 2, y, v[0], 0, v[1])
    if ch: emoji(G, t, ta, te, ch, x - tw / 2 - 60, y, size=80)

def hud(G, rest_ok=False):
    a = plate_img('PAYCHECK ↑', 24, WHITE, INK, pad=10, border=INK)
    b = plate_img('LEFT  > $0' if rest_ok else 'LEFT  $0', 24, GREEN if rest_ok else RED, WHITE, pad=10)
    x = S(WD - 36) - b.width; G.alpha_composite(b, (x, S(30))); G.alpha_composite(a, (x - S(10) - a.width, S(30)))

def holes_counter(G, n):
    d = ImageDraw.Draw(G)
    for k in range(4):
        cx, cy = 56 + k * 44, 112
        d.ellipse([S(cx - 15), S(cy - 15), S(cx + 15), S(cy + 15)], fill=YEL if k < n else WHITE, outline=INK, width=S(4))
    paste(G, plate_img('HOLES', 22, None, INK, pad=4), 56 + 4 * 44 + 30, 112)

# ---------------- служебное ----------------
def badge(G, ch, title):
    im = plate_img(f'{ch}  ·  {title.upper()}', 26, INK, WHITE, pad=14)
    G.alpha_composite(im, (S(36), S(30)))
def chapter_card(G, t, t0, t1, ch, title):
    k_in = eo((t - t0) / 0.3); k_out = 1 - eo((t - t1 + 0.25) / 0.25)
    a = clamp(min(k_in, k_out))
    if a <= 0: return
    d = ImageDraw.Draw(G)
    w = WD * a
    d.rectangle([S(WD / 2 - w / 2), S(380), S(WD / 2 + w / 2), S(700)], fill=YEL)
    if a > 0.7:
        paste(G, plate_img(f'CHAPTER {ch}', 44, None, INK), WD / 2, 450)
        paste(G, plate_img(title.upper(), 90, None, INK), WD / 2, 590)

ELS = {k: v for k, v in globals().items() if callable(v) and k in
       'plate card dark red txt emoji strike crossline check arrow counter bars cloud battery tabs flash cross boxes hourglass meter bucket phone source'.split()}
