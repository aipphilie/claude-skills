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
LABELS = ['DOCTOR', 'IT', 'INFLUENCER', 'OWN BUSINESS', 'DESIGN', 'MOVE AWAY', 'MUSIC', 'FREELANCE', 'CHEF', 'SPORTS', 'SCHOOL', 'OFFICE']
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
       'plate card dark red txt emoji strike crossline check arrow counter bars cloud battery tabs flash cross'.split()}
