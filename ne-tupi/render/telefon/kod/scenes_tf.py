"""СДВГ-монтаж «Что знает о тебе телефон». Движок «Пряника»/«Автокредита» (engine_part.py), герои из zveri.py.
python3 compose_tf.py 1.5 12.3 -> prev_*.png;  python3 compose_tf.py sheet [доля];  без аргументов -> video_noaudio.mp4 + sfx.json"""
from zveri import *
from zveri import _e, _thick, _curve
G = FEET
OB = lambda C, u, seed=1: (C.paste(ORNG, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(250, 160, 70), seed=seed))
YB = lambda C, u, seed=1: (C.paste(YEL, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(246, 200, 0), seed=seed))
RB = lambda C, u, seed=1: (C.paste(RUST, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(160, 56, 28), seed=seed))
def tw(t, w, k=0): return t - T(w, k)
_slam0, _plate0 = slam, plate
def _fit(text, sz, lim=780):
    w = text_img(text, sz).width
    return sz * min(1.0, lim / w) if w else sz
def slam(C, u, text, cx, cy, sz=90, *a, **k): _slam0(C, u, text, cx, cy, _fit(text, sz), *a, **k)
def plate(C, u, text, cx, cy, sz=70, *a, **k): _plate0(C, u, text, cx, cy, _fit(text, sz, 740), *a, **k)
SY, PY = 440, 600
def ttl(C, u, t, a, b=None, wb=None, rot=3, bcol=YEL, fcol=INK, sza=120, szb=96, k=0):
    slam(C, u, a, 540, SY, sza)
    if b:
        tb = tw(t, wb, k) if wb else u - 0.15
        if tb > -0.1: plate(C, tb + (0.1 if wb else 0), b, 540, PY, szb, bcol, fcol, rot)
def at(t, w, k=0, d=0.0): return tw(t, w, k) > d

# ================= ПРЕДМЕТЫ =================
def eye_glyph(d, cx, cy, w, col=RED, pup=INK, open_=1.0):
    """миндалевидный глаз «следит»"""
    h = w * 0.36 * open_; pts = []
    for j in range(25):
        a = math.pi * j / 24; pts.append((cx - w / 2 + w * j / 24, cy - h * math.sin(a)))
    for j in range(25):
        a = math.pi * j / 24; pts.append((cx + w / 2 - w * j / 24, cy + h * math.sin(a)))
    d.polygon(pts, fill=WHITE, outline=col, width=max(3, int(w * 0.07)))
    if open_ > 0.3: _e(d, cx, cy, h * 0.8, h * 0.8, fill=col); _e(d, cx, cy, h * 0.38, h * 0.38, fill=pup)
def phone_frame(C, cx, cy, w, rot=0, screen=(30, 30, 36), notch=True):
    """большой телефон; возвращает рамку экрана (x0, y0, x1, y1)"""
    h = w * 2.0; d = ImageDraw.Draw(C)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(w * 0.16), fill=INK)
    x0, y0, x1, y1 = cx - w / 2 + w * 0.06, cy - h / 2 + w * 0.08, cx + w / 2 - w * 0.06, cy + h / 2 - w * 0.08
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(w * 0.1), fill=screen)
    if notch: d.rounded_rectangle([cx - w * 0.14, y0 + w * 0.03, cx + w * 0.14, y0 + w * 0.08], radius=int(w * 0.03), fill=INK)
    return x0, y0, x1, y1
APPS = [(ORNG, 'ФОНАРИК'), (TEAL, 'ПОГОДА'), (OLIVE, 'ИГРА'), (RUST, 'ЕДА'), (OCHRE, 'ФОТО'), ((120, 96, 160), 'КАРТЫ'), ((90, 120, 190), 'ЧАТ'), ((200, 90, 120), 'МУЗЫКА'), ((110, 110, 110), 'НАСТР.')]
def app_icon(C, cx, cy, sz, col, glyph=None, watch=0.0, pulse=0.0, label=None):
    d = ImageDraw.Draw(C); r = sz / 2 * (1 + 0.08 * pulse)
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=int(r * 0.45), fill=col, outline=INK if watch else None, width=6 if watch else 0)
    if glyph == 'torch':
        d.polygon([(cx - r * 0.22, cy - r * 0.15), (cx + r * 0.22, cy - r * 0.15), (cx + r * 0.14, cy + r * 0.55), (cx - r * 0.14, cy + r * 0.55)], fill=WHITE)
        d.polygon([(cx - r * 0.42, cy - r * 0.6), (cx + r * 0.42, cy - r * 0.6), (cx + r * 0.22, cy - r * 0.15), (cx - r * 0.22, cy - r * 0.15)], fill=YEL)
    elif glyph == 'sun': _e(d, cx, cy, r * 0.35, r * 0.35, fill=YEL)
    elif glyph == 'game': d.rounded_rectangle([cx - r * 0.5, cy - r * 0.25, cx + r * 0.5, cy + r * 0.3], radius=int(r * 0.2), fill=WHITE)
    elif glyph == 'food': _e(d, cx, cy + r * 0.05, r * 0.45, r * 0.3, fill=WHITE); d.chord([cx - r * 0.45, cy - r * 0.4, cx + r * 0.45, cy + r * 0.35], 180, 360, fill=OCHRE)
    if watch > 0: eye_glyph(d, cx, cy, r * 1.3 * min(1, watch * 1.5), RED, INK, min(1, watch * 2))
    if label: put(C, text_img(label, max(18, int(sz * 0.2)), WHITE), cx, cy + r + sz * 0.18)
def bed(C, cx, by, w=640):
    d = ImageDraw.Draw(C)
    d.rounded_rectangle([cx - w / 2, by - 300, cx - w / 2 + 40, by], radius=14, fill=DOGD)        # спинка
    d.rounded_rectangle([cx - w / 2, by - 170, cx + w / 2, by - 60], radius=20, fill=WHITE, outline=INK, width=6)
    d.rounded_rectangle([cx - w / 2 + 50, by - 230, cx - w / 2 + 210, by - 160], radius=30, fill=WHITE, outline=INK, width=6)    # подушка
    d.rounded_rectangle([cx - w / 2 + 180, by - 210, cx + w / 2 - 10, by - 110], radius=40, fill=OCHRE, outline=INK, width=6)  # одеяло (спящий)
    d.rectangle([cx - w / 2 + 10, by - 60, cx - w / 2 + 40, by], fill=DOGD); d.rectangle([cx + w / 2 - 40, by - 60, cx + w / 2 - 10, by], fill=DOGD)
def zzz(C, x, y, u, col=INK):
    for j in range(3):
        k = (u * 0.8 + j * 0.33) % 1; put(C, text_img('Z', int(40 + j * 16), col), x + j * 40 + 10 * s_(u * 3 + j), y - j * 60 - k * 30, 1, 0, 1 - k * 0.6)
def nightstand(C, cx, by):
    d = ImageDraw.Draw(C); d.rounded_rectangle([cx - 110, by - 190, cx + 110, by], radius=10, fill=DOG, outline=INK, width=6); d.line([cx - 110, by - 95, cx + 110, by - 95], fill=INK, width=5)
    _e(d, cx, by - 140, 14, 8, fill=INK)
ROUTE = [(250, 1130), (310, 900), (560, 860), (800, 760), (820, 1010), (560, 1080), (250, 1130)]
def mapcard(C, u, x0=150, y0=700, x1=930, y1=1240, dot=1.0):
    d = ImageDraw.Draw(C)
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(238, 226, 200), outline=INK, width=8)
    d.polygon([(x0 + 8, y0 + 360), (x0 + 260, y0 + 300), (x0 + 360, y1 - 8), (x0 + 8, y1 - 8)], fill=(206, 214, 160))       # парк
    d.line([(x1 - 200, y0 + 8), (x1 - 120, y0 + 220), (x1 - 8, y0 + 300)], fill=(150, 196, 210), width=40)                # река
    for yy in (y0 + 140, y0 + 300, y0 + 440):
        d.line([(x0 + 8, yy), (x1 - 8, yy - 40)], fill=WHITE, width=22)
    for xx in (x0 + 180, x0 + 420, x0 + 640): d.line([(xx, y0 + 8), (xx + 30, y1 - 8)], fill=WHITE, width=22)
    # точки маршрута
    pts = ROUTE; L = [0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    tot = L[-1]; pos = clamp(dot) * tot; trail = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= pos: trail.append(pts[i])
        else:
            k = (pos - L[i - 1]) / (L[i] - L[i - 1]); trail.append((lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k))); break
    for a, b in zip(trail, trail[1:]):
        n = int(math.dist(a, b) // 26)
        for j in range(n):
            p = (lerp(a[0], b[0], (j + 0.2) / max(1, n)), lerp(a[1], b[1], (j + 0.2) / max(1, n))); _e(d, p[0], p[1], 7, 7, fill=RED)
    for (px, py), nm in [((250, 1130), 'ДОМ'), ((560, 860), 'РАБОТА'), ((820, 1010), 'МАГАЗИН')]:
        pin(C, px, py, 50, INK); put(C, plate_img(nm, 32, WHITE, INK, pad=10, r=8, border=INK, bw=4), px, py + 48)
    p = trail[-1]; r = 26 + 4 * s_(u * 10); _e(d, p[0], p[1], r + 14, r + 14, fill=(232, 44, 52, 0), outline=RED, width=5); _e(d, p[0], p[1], r * 0.8, r * 0.8, fill=RED, outline=WHITE, width=6)
def pin(C, x, y, s=60, col=RED):
    d = ImageDraw.Draw(C); _e(d, x, y - s * 1.1, s * 0.55, s * 0.55, fill=col); d.polygon([(x - s * 0.45, y - s * 0.85), (x + s * 0.45, y - s * 0.85), (x, y)], fill=col); _e(d, x, y - s * 1.1, s * 0.2, s * 0.2, fill=WHITE)
def torch(C, cx, cy, s=1.0, rot=0, beam=0.0, eye=0.0):
    im = Image.new('RGBA', (int(900 * s), int(420 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ox, oy = 60 * s, 210 * s
    if beam > 0:
        bl = 560 * s * eo(beam)
        d.polygon([(ox + 300 * s, oy - 60 * s), (ox + 300 * s + bl, oy - 190 * s), (ox + 300 * s + bl, oy + 190 * s), (ox + 300 * s, oy + 60 * s)], fill=(255, 236, 140, 200))
        if eye > 0: eye_glyph(d, ox + 300 * s + bl * 0.62, oy, 200 * s * eo(eye), RUST, INK)
    d.rounded_rectangle([ox, oy - 45 * s, ox + 220 * s, oy + 45 * s], radius=int(20 * s), fill=OCHRE, outline=INK, width=int(8 * s))
    d.polygon([(ox + 220 * s, oy - 45 * s), (ox + 300 * s, oy - 75 * s), (ox + 300 * s, oy + 75 * s), (ox + 220 * s, oy + 45 * s)], fill=INK)
    d.rounded_rectangle([ox + 70 * s, oy - 18 * s, ox + 110 * s, oy + 18 * s], radius=6, fill=RED)
    put(C, im, cx + im.width / 2 - ox - 150 * s, cy, 1, rot)
PH_COL = [(238, 196, 140), (206, 214, 160), (150, 196, 210), (240, 170, 120), (220, 200, 230), (250, 220, 150)]
def thumb(C, x, y, w, h, kind, seed=0):
    d = ImageDraw.Draw(C); d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PH_COL[seed % 6])
    if kind == 'mount':
        d.polygon([(x + 10, y + h - 8), (x + w * 0.4, y + h * 0.35), (x + w * 0.7, y + h - 8)], fill=OLIVE); _e(d, x + w * 0.75, y + h * 0.3, w * 0.12, w * 0.12, fill=YEL)
    elif kind == 'sun': d.rectangle([x, y + h * 0.65, x + w, y + h], fill=(150, 196, 210)); _e(d, x + w / 2, y + h * 0.62, w * 0.2, w * 0.2, fill=ORNG)
    elif kind == 'food': _e(d, x + w / 2, y + h / 2, w * 0.32, w * 0.32, fill=WHITE); _e(d, x + w / 2, y + h / 2, w * 0.2, w * 0.2, fill=RUST)
    elif kind == 'leaf': leaf(d, x + w / 2, y + h / 2, w * 0.3, ORNG, 30)
def leaf(d, cx, cy, r, col, rot=0):
    pts = []
    for j in range(30):
        a = 2 * math.pi * j / 30; rr = r * (0.55 + 0.45 * abs(math.cos(a))) * (0.9 + 0.1 * math.cos(5 * a))
        x, y = rr * math.cos(a) * 0.6, rr * math.sin(a); ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(pts, fill=col)
def gallery(C, u, x0, y0, x1, y1, scroll=0):
    d = ImageDraw.Draw(C); cols = 3; gap = 14; w = (x1 - x0 - gap * (cols + 1)) / cols; kinds = ['mount', 'sun', 'food', 'leaf', 'mount', 'food', 'sun', 'leaf', 'food', 'mount', 'sun', 'leaf', 'food', 'mount', 'leaf']
    for i in range(18):
        r, c = divmod(i, cols); y = y0 + gap + r * (w + gap) - scroll
        if y + w < y0 or y > y1: continue
        thumb(C, x0 + gap + c * (w + gap), y, w, w, kinds[i % len(kinds)], i)
def polaroid(C, cx, cy, w, draw_fn, rot=0, caption=None):
    h = w * 1.15; im = Image.new('RGBA', (int(w) + 20, int(h) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=10, fill=WHITE, outline=INK, width=6)
    inner = Image.new('RGBA', (int(w * 0.86), int(w * 0.86)), PH_COL[1] + (255,)); draw_fn(inner); im.alpha_composite(inner, (int(10 + w * 0.07), int(10 + w * 0.07)))
    if caption: t_ = text_img(caption, int(w * 0.09)); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(10 + h - w * 0.15)))
    put(C, im, cx, cy, 1, rot)
def cafe_bg(C):
    d = ImageDraw.Draw(C)
    d.rectangle([0, 680, CW, G + 6], fill=(244, 232, 212))
    for x in range(0, CW, 90): d.line([x, 680, x, G], fill=(236, 220, 196), width=40)
    d.rounded_rectangle([90, 700, 990, 820], radius=16, fill=RUST, outline=INK, width=6)   # навес
    for j in range(9): d.chord([90 + j * 100, 790, 190 + j * 100, 850], 0, 180, fill=RUST if j % 2 else WHITE, outline=INK, width=4)
    put(C, text_img('КАФЕ', 60, WHITE), 540, 758)
def table(C, cx, by, w=420):
    d = ImageDraw.Draw(C); d.rounded_rectangle([cx - w / 2, by - 210, cx + w / 2, by - 180], radius=10, fill=DOGD, outline=INK, width=5)
    d.rectangle([cx - 12, by - 180, cx + 12, by], fill=INK); d.rectangle([cx - 80, by - 10, cx + 80, by], fill=INK)
def cup(C, cx, by, s=1.0):
    d = ImageDraw.Draw(C); d.polygon([(cx - 34 * s, by - 80 * s), (cx + 34 * s, by - 80 * s), (cx + 26 * s, by), (cx - 26 * s, by)], fill=WHITE, outline=INK, width=5)
    d.rectangle([cx - 31 * s, by - 56 * s, cx + 30 * s, by - 34 * s], fill=DOGD); d.rounded_rectangle([cx - 38 * s, by - 96 * s, cx + 38 * s, by - 78 * s], radius=6, fill=INK)
def lap_back(C, cx, by, w=300, glow=None):
    """ноутбук, повёрнутый к зверю (видим крышку сзади)"""
    d = ImageDraw.Draw(C); h = w * 0.66
    d.rounded_rectangle([cx - w / 2, by - h, cx + w / 2, by], radius=14, fill=(180, 176, 170), outline=INK, width=6)
    _e(d, cx, by - h / 2, w * 0.07, w * 0.07, fill=WHITE)
    d.rounded_rectangle([cx - w * 0.56, by - 4, cx + w * 0.56, by + 12], radius=6, fill=(140, 136, 130), outline=INK, width=4)
def wifi(C, cx, cy, s=1.0, k=1.0, col=INK, label=None, bad=False):
    d = ImageDraw.Draw(C)
    for j in range(3):
        if k > j / 3:
            r = (40 + j * 40) * s; d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=col, width=int(16 * s))
    _e(d, cx, cy - 4 * s, 12 * s, 12 * s, fill=col)
    if label: put(C, plate_img(label, int(40 * s), WHITE, INK, pad=12, r=10, border=INK, bw=5), cx, cy + 60 * s)
def sneak(C, t, cx, by, s=1.0, look=0):
    """сосед по сети: серый в капюшоне и тёмных очках"""
    d = ImageDraw.Draw(C); gx = (118, 116, 120); gd = (84, 82, 88)
    d.rounded_rectangle([cx - 120 * s, by - 300 * s, cx + 120 * s, by], radius=int(70 * s), fill=gx)
    _e(d, cx, by - 380 * s, 105 * s, 110 * s, fill=gx)
    _e(d, cx + look * 8 * s, by - 365 * s, 70 * s, 75 * s, fill=(70, 66, 70))
    d.rounded_rectangle([cx - 66 * s + look * 10 * s, by - 395 * s, cx + 66 * s + look * 10 * s, by - 360 * s], radius=int(14 * s), fill=INK)
    d.arc([cx - 30 * s + look * 10 * s, by - 350 * s, cx + 30 * s + look * 10 * s, by - 320 * s], 20, 160, fill=(220, 220, 220), width=int(6 * s))
def envelope_(C, cx, cy, w=110, locked=0.0, col=WHITE):
    d = ImageDraw.Draw(C); h = w * 0.66
    if locked >= 1:
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=10, fill=INK)
        d.arc([cx - w * 0.18, cy - h * 0.62, cx + w * 0.18, cy - h * 0.0], 180, 360, fill=YEL, width=max(4, int(w * 0.07)))
        d.rounded_rectangle([cx - w * 0.24, cy - h * 0.25, cx + w * 0.24, cy + h * 0.3], radius=6, fill=YEL); return
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=col, outline=INK, width=5)
    d.line([(cx - w / 2, cy - h / 2), (cx, cy + h * 0.1), (cx + w / 2, cy - h / 2)], fill=INK, width=5)
def lock(C, cx, cy, s=1.0, k=1.0):
    if k <= 0: return
    im = Image.new('RGBA', (int(220 * s), int(260 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc([40 * s, 10 * s, 180 * s, 150 * s], 180, 360, fill=INK, width=int(26 * s)); d.line([53 * s, 80 * s, 53 * s, 120 * s], fill=INK, width=int(26 * s)); d.line([167 * s, 80 * s, 167 * s, 120 * s], fill=INK, width=int(26 * s))
    d.rounded_rectangle([10 * s, 110 * s, 210 * s, 250 * s], radius=int(24 * s), fill=YEL, outline=INK, width=int(10 * s)); _e(d, 110 * s, 170 * s, 18 * s, 18 * s, fill=INK); d.rectangle([102 * s, 170 * s, 118 * s, 215 * s], fill=INK)
    put(C, im, cx, cy, back(k / 0.25) if k < 0.4 else 1)
def comment(C, cx, cy, w, text, k=1.0, rot=0, av=ORNG, sz=44, hl=False):
    if k <= 0: return
    tt = text_img(text, sz); h = max(110, tt.height + 50); im = Image.new('RGBA', (int(w) + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=26, fill=YEL if hl else WHITE, outline=INK, width=6)
    _e(d, 10 + 58, 10 + h / 2, 34, 34, fill=av, outline=INK, width=4)
    im.alpha_composite(tt, (10 + 112, int(10 + h / 2 - tt.height / 2)))
    put(C, im, cx, cy, back(k / 0.22) if k < 0.35 else 1, rot)
def searchbar(C, cx, cy, w, text, k=1.0, cursor_t=0):
    d = ImageDraw.Draw(C); h = 110
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=55, fill=WHITE, outline=INK, width=7)
    _e(d, cx - w / 2 + 62, cy - 8, 22, 22, outline=INK, width=7); d.line([cx - w / 2 + 78, cy + 8, cx - w / 2 + 96, cy + 28], fill=INK, width=8)
    s_txt = text[:int(len(text) * clamp(k))]
    if s_txt: t_ = text_img(s_txt, 50, GREY); C.alpha_composite(t_, (int(cx - w / 2 + 120), int(cy - t_.height / 2)))
    if int(cursor_t * 2.5) % 2 == 0:
        xx = cx - w / 2 + 124 + (text_img(s_txt, 50, GREY).width if s_txt else 0); d.rectangle([xx, cy - 30, xx + 6, cy + 30], fill=INK)
def scales(C, cx, cy, u, left, right, tilt=0.0):
    d = ImageDraw.Draw(C); a = math.radians(tilt * 12)
    d.rectangle([cx - 10, cy, cx + 10, cy + 330], fill=INK); d.rounded_rectangle([cx - 110, cy + 320, cx + 110, cy + 350], radius=10, fill=INK)
    L = 330; xl, yl = cx - L * math.cos(a), cy - L * math.sin(a) * -1; xr, yr = cx + L * math.cos(a), cy - L * math.sin(a)
    yl = cy + L * math.sin(a); yr = cy - L * math.sin(a)
    d.line([xl, yl, xr, yr], fill=INK, width=14); _e(d, cx, cy, 22, 22, fill=YEL, outline=INK, width=6)
    for (x, y, lab, col) in ((xl, yl, left, WHITE), (xr, yr, right, YEL)):
        d.line([x, y, x - 80, y + 150], fill=INK, width=5); d.line([x, y, x + 80, y + 150], fill=INK, width=5)
        d.chord([x - 120, y + 110, x + 120, y + 200], 0, 180, fill=col, outline=INK, width=6)
        put(C, plate_img(lab, 34, col, INK, pad=10, r=8, border=INK, bw=4), x, y + 90)
def bubble_say(C, cx, cy, text, k=1.0, col=WHITE, tail_dx=-60, sz=56):
    if k <= 0: return
    t_ = text_img(text, sz); w, h = t_.width + 70, t_.height + 50; im = Image.new('RGBA', (w + 20, h + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tx = w / 2 + 10 + tail_dx; d.polygon([(tx - 26, 10 + h - 4), (tx + 26, 10 + h - 4), (tx - tail_dx * 0.4, 10 + h + 55)], fill=col, outline=INK)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=40, fill=col, outline=INK, width=6); d.polygon([(tx - 20, 10 + h - 8), (tx + 20, 10 + h - 8), (tx - tail_dx * 0.4, 10 + h + 48)], fill=col)
    im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(10 + h / 2 - t_.height / 2)))
    put(C, im, cx, cy, back(k / 0.22) if k < 0.35 else 1)
def dossier(C, cx, cy, w, k=1.0, rot=-4, lines=('СПИТ ДО 11', 'ГУГЛИТ НОЧЬЮ', 'ЕСТ В 2:00')):
    if k <= 0: return
    h = w * 1.25; im = Image.new('RGBA', (int(w) + 20, int(h) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10 + w * 0.42, 10 + h * 0.1], radius=12, fill=(214, 166, 90), outline=INK, width=6)
    d.rounded_rectangle([10, 10 + h * 0.06, 10 + w, 10 + h], radius=16, fill=(232, 190, 110), outline=INK, width=7)
    t_ = text_img('ДОСЬЕ', int(w * 0.14)); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(10 + h * 0.13)))
    y = h * 0.38
    for ln in lines:
        tl = text_img(ln, int(w * 0.075)); im.alpha_composite(tl, (int(10 + w * 0.12), int(10 + y))); y += h * 0.15
    put(C, im, cx, cy, back(k / 0.22) if k < 0.35 else 1, rot)
def sign_sale(C, cx, by, text='ПРОДАМ ДАННЫЕ', s=1.0):
    d = ImageDraw.Draw(C); d.rectangle([cx - 8 * s, by - 300 * s, cx + 8 * s, by], fill=DOGD)
    put(C, plate_img(text, int(36 * s), WHITE, INK, pad=16, r=8, border=INK, bw=5), cx, by - 300 * s, 1, -5)

# ================= СЦЕНЫ =================
def s_hook(C, u, t):    # Твой телефон знает о тебе больше, чем твоя мама.
    ground(C); phone_frame(C, 540, 1000, 300, screen=(40, 44, 56), notch=False)
    kot(C, t, 540, 1180, 440, pose='loaf', look=(0, 0.2), shadow=False)
    slam(C, u, 'ЧТО ЗНАЕТ ТЕЛЕФОН?', 540, SY, 110)
    if at(t, 'больше'): plate(C, tw(t, 'больше') + 0.05, 'БОЛЬШЕ, ЧЕМ МАМА', 540, PY, 96, YEL, INK, -3)
def s_bkot(C, u, t):    # И даже больше, чем твой кот.
    OB(C, u, 2); z = 1 + 0.25 * eo(u / 1.2)
    kot(C, t, 540, G + 120 + 160 * (z - 1), int(470 * z), look=(0, 0), shadow=False)
    slam(C, u, 'И ДАЖЕ БОЛЬШЕ,', 540, SY, 110, WHITE)
    if at(t, 'кот', 0, -0.2): plate(C, tw(t, 'кот') + 0.15, 'ЧЕМ ТВОЙ КОТ', 540, PY, 104, INK, YEL, 3)
def s_vse(C, u, t):    # А кот, между прочим, знает про тебя ВСЁ.
    ground(C); kot(C, t, 300, G, 400, pose='sit', look=(0.6, 0))
    dossier(C, 760, 960, 360, u / 0.3, 5)
    slam(C, u, 'А КОТ ЗНАЕТ', 540, SY, 120)
    if at(t, 'ВСЁ', 0, -0.05): stamp(C, tw(t, 'ВСЁ'), 'ВСЁ', 540, PY + 10, 140, RED, -8)
def s_pes(C, u, t):    # Пёс у нас по безопасности.
    ground(C); x = lerp(-200, 470, eo(u / 0.5))
    dog(C, t, x, G, 440)
    slam(C, u, 'ПЁС', 540, SY, 150)
    if at(t, 'безопасности'): plate(C, tw(t, 'безопасности') + 0.05, 'ПО БЕЗОПАСНОСТИ', 540, PY, 100, INK, YEL, -3)
def s_nyuh(C, u, t):    # Нюхнул телефон и сразу доложил:
    ground(C); dl = at(t, 'доложил', 0, -0.1)
    d = ImageDraw.Draw(C); x0, y0, x1, y1 = 700, 1150, 920, 1270
    phone_frame(C, 850, 1200, 130, rot=0, screen=(40, 44, 56))
    dog(C, t, 420, G, 400, 'point' if dl else 'sniff', eyes='shock' if dl else 'n', mouth='o' if dl else 'flat')
    slam(C, u, 'НЮХНУЛ ТЕЛЕФОН', 540, SY, 110)
    if dl: plate(C, tw(t, 'доложил') + 0.05, 'И ДОЛОЖИЛ', 540, PY, 100, YEL, INK, 3)
def s_tri(C, u, t):    # тут три приложения следят за тобой,
    x0, y0, x1, y1 = phone_frame(C, 540, 1000, 330, screen=(44, 48, 60))
    gl = ['torch', 'sun', 'game', 'food', None, None, None, None, None]; watch = {0: 'три', 1: 'приложения', 3: 'следят'}
    for i in range(9):
        r_, c_ = divmod(i, 3); cx = x0 + (x1 - x0) * (0.2 + 0.3 * c_); cy = y0 + 140 + r_ * 150
        wk = clamp(tw(t, watch[i]) / 0.25) if i in watch and at(t, watch[i]) else 0
        app_icon(C, cx, cy, 96, APPS[i][0], gl[i], wk, abs(s_(t * 8)) if wk else 0)
    slam(C, u, 'ТУТ ТРИ ПРИЛОЖЕНИЯ', 540, SY, 104)
    if at(t, 'следят'): plate(C, tw(t, 'следят') + 0.05, 'СЛЕДЯТ ЗА ТОБОЙ', 540, PY, 100, RED, WHITE, -3)
def s_spish(C, u, t):    # пока ты спишь.
    ground(C); bed(C, 600, G, 620); nightstand(C, 170, G); zzz(C, 640, 980, u)
    phone_frame(C, 170, G - 230, 70, screen=(255, 236, 140))
    d = ImageDraw.Draw(C)
    for j, (dx, dy) in enumerate([(-120, -330), (0, -380), (120, -330)]):
        if u > 0.1 + j * 0.15: eye_glyph(d, 170 + dx, G - 230 + dy, 100, RED, INK, min(1, (u - 0.1 - j * 0.15) * 5))
    slam(C, u, 'ПОКА ТЫ СПИШЬ', 540, SY, 120)
def s_karta(C, u, t):    # Вот твоя карта за неделю.
    mapcard(C, t, dot=u / 1.3)
    slam(C, u, 'ТВОЯ КАРТА', 540, SY, 130)
    if at(t, 'неделю'): plate(C, tw(t, 'неделю') + 0.05, 'ЗА НЕДЕЛЮ', 540, PY, 100, YEL, INK, 3)
def s_app(C, u, t):    # Приложение для фонарика знает, где ты ночуешь.
    mapcard(C, t, dot=1.0); d = ImageDraw.Draw(C)
    app_icon(C, 780, 840, 170, ORNG, 'torch', clamp(tw(t, 'знает', 2) / 0.3) if at(t, 'знает', 2) else 0)
    if at(t, 'ночуешь', 0, -0.1): pin(C, 250, 1130, 110 * back(tw(t, 'ночуешь') / 0.25 + 0.4), RED)
    slam(C, u, 'ФОНАРИК ЗНАЕТ', 540, SY, 120)
    if at(t, 'ночуешь'): plate(C, tw(t, 'ночуешь') + 0.05, 'ГДЕ ТЫ НОЧУЕШЬ', 540, PY, 100, RED, WHITE, -3)
def s_karl(C, u, t):    # Фонарик, Карл!
    RB(C, u, 3); burst(C, 540, 960, 330 + 14 * s_(u * 9), u, 16, YEL, INK)
    torch(C, 540, 960, 1.15, 12 + 4 * s_(u * 10))
    slam(C, u, 'ФОНАРИК,', 540, SY, 140, WHITE)
    if at(t, 'Карл', 0, -0.05): stamp(C, tw(t, 'Карл'), 'КАРЛ!', 540, PY + 10, 130, WHITE, -8)
def s_vidit(C, u, t):    # Ему чего светить, он и так всё видит.
    ground(C); torch(C, 380, 900, 0.9, 0, clamp(u / 0.5), clamp(tw(t, 'видит') / 0.3) if at(t, 'видит', 0, -0.2) else 0)
    dog(C, t, 760, G, 340, 'stand', eyes='shock', mouth='o', flip=True)
    slam(C, u, 'ЕМУ ЧЕГО СВЕТИТЬ?', 540, SY, 104)
    if at(t, 'видит', 0, -0.1): plate(C, tw(t, 'видит') + 0.1, 'ОН И ТАК ВСЁ ВИДИТ', 540, PY, 92, YEL, INK, 3)
def s_fotki(C, u, t):    # Дальше фотки.
    x0, y0, x1, y1 = phone_frame(C, 540, 1000, 330, screen=(250, 250, 250))
    C2 = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); gallery(C2, u, x0, y0, x1, y1, scroll=420 * eo(u / 1.0))
    mask = Image.new('L', (CW, CH), 0); ImageDraw.Draw(mask).rounded_rectangle([x0, y0, x1, y1], radius=30, fill=255)
    C.paste(C2, (0, 0), ImageChops.multiply(mask, C2.getchannel('A')))
    slam(C, u, 'ДАЛЬШЕ ФОТКИ', 540, SY, 130)
def _photo_mount(im):
    d = ImageDraw.Draw(im); w, h = im.size
    d.rectangle([0, 0, w, h], fill=(250, 214, 160)); _e(d, w * 0.72, h * 0.3, w * 0.12, w * 0.12, fill=ORNG)
    d.polygon([(0, h), (w * 0.35, h * 0.4), (w * 0.7, h)], fill=OLIVE); d.polygon([(w * 0.4, h), (w * 0.75, h * 0.5), (w * 1.05, h)], fill=(100, 110, 56))
    for j in range(5): leaf(d, w * (0.1 + j * 0.2), h * 0.15 + 20 * (j % 2), w * 0.04, RUST, j * 40)
def s_exif(C, u, t):    # В каждой спрятаны время, место и модель телефона.
    polaroid(C, 400, 960, 440, _photo_mount, -4)
    for j, (w, txt_, y) in enumerate([('время', 'ВРЕМЯ: 23:47', 800), ('место', 'ГЕО: 55.7°, 37.6°', 940), ('модель', 'МОДЕЛЬ ТЕЛЕФОНА', 1080)]):
        if at(t, w, 0, -0.05): tag(C, tw(t, w) + 0.05, txt_, 690, y, 44, YEL if j != 1 else WHITE, INK, (-1) ** j * 3)
    slam(C, u, 'В КАЖДОЙ ФОТКЕ', 540, SY, 120)
    if at(t, 'спрятаны'): plate(C, tw(t, 'спрятаны') + 0.05, 'СПРЯТАНЫ ДАННЫЕ', 540, PY, 96, INK, YEL, 3)
def _ph_animal(kind):
    def f(im):
        d = ImageDraw.Draw(im); w, h = im.size; d.rectangle([0, 0, w, h], fill={'cat': (206, 214, 160), 'dog': (150, 196, 210), 'kot': (240, 200, 150)}[kind])
        for j in range(4): leaf(d, w * (0.15 + j * 0.25), h * 0.12, w * 0.05, (ORNG, RUST, OCHRE, RUST)[j], j * 50)
        if kind == 'dog': dog(im, 0.3, w * 0.5, h * 0.98, int(h * 0.75), shadow=False)
        elif kind == 'cat': cat(im, 0.3, w * 0.5, h * 0.98, int(h * 0.82), shadow=False, eyes='happy')
        else: kot(im, 0.3, w * 0.5, h * 1.02, int(h * 0.82), shadow=False, look=(0.5, 0))
    return f
def s_phcat(C, u, t):    # Вот кошка,
    polaroid(C, 540, 960, 560, _ph_animal('cat'), -4 + 2 * eo(u / 0.3), 'КОШКА'); slam(C, u, 'ВОТ КОШКА', 540, SY, 130)
def s_phdog(C, u, t):    # вот собака,
    polaroid(C, 540, 960, 560, _ph_animal('dog'), 4, 'СОБАКА'); slam(C, u, 'ВОТ СОБАКА', 540, SY, 130)
def s_phkot(C, u, t):    # вот кот, которому вообще пофиг.
    polaroid(C, 540, 960, 560, _ph_animal('kot'), -3, 'КОТ'); slam(C, u, 'ВОТ КОТ', 540, SY, 130)
    if at(t, 'пофиг', 0, -0.05): stamp(C, tw(t, 'пофиг'), 'ЕМУ ПОФИГ', 540, PY + 10, 110, RED, -8)
def s_troe(C, u, t):    # Кстати, да, у меня их трое,
    ground(C); dog(C, t, 240, G, 330); cat(C, t, 580, G, 320, look=(0.3, 0)); kot(C, t, 840, G, 300, look=(-0.4, 0))
    slam(C, u, 'КСТАТИ, ДА', 540, SY, 130)
    if at(t, 'трое', 0, -0.1): plate(C, tw(t, 'трое') + 0.05, 'У МЕНЯ ИХ ТРОЕ', 540, PY, 100, YEL, INK, -3)
def s_paroli(C, u, t):    # и они в курсе всех моих паролей.
    ground(C); dog(C, t, 220, G, 300, eyes='happy'); kot(C, t, 830, G, 290)
    d = ImageDraw.Draw(C); w = 520; x0 = 540 - w / 2
    d.rounded_rectangle([x0, 820, x0 + w, 960], radius=24, fill=WHITE, outline=INK, width=8)
    n = int(clamp(u / 0.9) * 8); put(C, text_img('•' * n if n else ' ', 90, INK) if n else text_img('ПАРОЛЬ', 50, GREY), 540, 890)
    lock(C, 540, 1110, 0.7, u / 0.3)
    slam(C, u, 'В КУРСЕ ВСЕХ', 540, SY, 130)
    if at(t, 'паролей', 0, -0.1): plate(C, tw(t, 'паролей') + 0.05, 'МОИХ ПАРОЛЕЙ', 540, PY, 100, INK, YEL, 3)
def s_pochti(C, u, t):    # Ну, почти.
    YB(C, u, 4); kot(C, t, 540, G, 440, pose='shrug', eyes='half', mouth='smug')
    slam(C, u, 'НУ...', 540, SY, 150)
    if at(t, 'почти', 0, -0.05): stamp(C, tw(t, 'почти'), 'ПОЧТИ', 540, PY + 10, 120, INK, -6)
def s_kafe(C, u, t):    # А это кошка в кафе на бесплатном вайфае.
    cafe_bg(C); ground(C, col=(214, 196, 170))
    cat(C, t, 400, G - 175, 280, shadow=False, eyes='happy' if at(t, 'вайфае', 0, -0.1) else 'n')
    table(C, 500, G, 520); lap_back(C, 600, G - 212, 200); cup(C, 730, G - 212, 1.0)
    wifi(C, 840, 1000, 0.9, clamp(u / 0.6) * 1.1, INK, 'Free_WiFi' if at(t, 'бесплатном', 0, -0.1) else None)
    slam(C, u, 'КОШКА В КАФЕ', 540, SY, 120)
    if at(t, 'бесплатном'): plate(C, tw(t, 'бесплатном') + 0.05, 'БЕСПЛАТНЫЙ ВАЙФАЙ', 540, PY, 96, YEL, INK, -3)
def s_vidos(C, u, t):    # Ей кажется, что она просто смотрит видосики.
    ground(C); cat(C, t, 270, G, 380, eyes='happy')
    x0, y0, x1, y1 = phone_frame(C, 740, 1000, 240, screen=(44, 48, 60))
    d = ImageDraw.Draw(C); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.rounded_rectangle([x0 + 16, cy - 120, x1 - 16, cy + 60], radius=16, fill=(206, 214, 160)); d.polygon([(cx - 30, cy - 70), (cx - 30, cy + 10), (cx + 40, cy - 30)], fill=WHITE)
    d.rounded_rectangle([x0 + 20, cy + 90, x0 + 20 + (x1 - x0 - 40) * clamp(u / 2.4), cy + 104], radius=6, fill=RED)
    for j in range(3):
        k = (u * 0.7 + j * 0.33) % 1; put(C, text_img('♥' if False else '+1', 40, RUST), 560 - 30 * j, 820 - k * 140, 1, 0, 1 - k)
    slam(C, u, 'ЕЙ КАЖЕТСЯ', 540, SY, 130)
    if at(t, 'видосики', 0, -0.1): plate(C, tw(t, 'видосики') + 0.05, 'ПРОСТО ВИДОСИКИ', 540, PY, 96, YEL, INK, 3)
def _cafe2(C, t, u, look=0, links=0.0, lines_=None, lockk=0.0):
    ground(C); cat(C, t, 220, G, 300, eyes='happy'); lap_back(C, 390, G, 160)
    sneak(C, t, 800, G, 0.75, look)
    d = ImageDraw.Draw(C); lap_back(C, 680, G, 160)
    if links > 0:   # пакеты от кошки к роутеру и «подслушка»
        wifi(C, 540, 840, 0.7, 1.0, INK)
        for j in range(4):
            k = (u * 0.9 + j * 0.25) % 1; x = lerp(400, 540, k); y = lerp(1120, 880, k)
            envelope_(C, x, y, 70, lockk)
        for j in range(0, 12):
            if j / 12 < links: d.line([lerp(560, 760, j / 12), lerp(880, 960, j / 12), lerp(560, 760, (j + 0.5) / 12), lerp(880, 960, (j + 0.5) / 12)], fill=RED, width=8)
    if lines_:
        y = 700
        for ln in lines_: put(C, plate_img(ln, 34, WHITE, INK, pad=10, r=8, border=INK, bw=4), 820, y); y += 66
def s_sosed(C, u, t):    # А на деле любой сосед по сети может
    _cafe2(C, t, u, -1, clamp(u / 1.0))
    slam(C, u, 'А НА ДЕЛЕ', 540, SY, 130)
    if at(t, 'сосед'): plate(C, tw(t, 'сосед') + 0.05, 'СОСЕД ПО СЕТИ', 540, PY, 100, RED, WHITE, -3)
def s_podsm(C, u, t):    # подсмотреть, куда она ходит.
    sh = ['САЙТ ВИДОСИКОВ', 'ПОИСК: «КОРМ»', 'БАНК']
    _cafe2(C, t, u, -1, 1.0, sh[:1 + int(clamp(u / 1.2) * 2)] if at(t, 'куда', 0, -0.1) else None)
    eye_glyph(ImageDraw.Draw(C), 800, 760 - 120, 130, RED, INK, clamp(u / 0.3)) if not at(t, 'куда', 0, -0.1) else None
    slam(C, u, 'ПОДСМОТРЕТЬ,', 540, SY, 120)
    if at(t, 'ходит', 0, -0.1): plate(C, tw(t, 'ходит') + 0.05, 'КУДА ОНА ХОДИТ', 540, PY, 100, YEL, INK, 3)
def s_shifr(C, u, t):    # Поэтому данные в таких сетях шифруют.
    sh_ = at(t, 'шифруют', 0, -0.05); lk = 1.0 if sh_ else 0.0
    ground(C); d = ImageDraw.Draw(C)
    for j in range(5):
        k = (u * 0.5 + j * 0.2) % 1; envelope_(C, lerp(150, 930, k), 980 + 40 * s_(k * 6 + j), 120, lk)
    if sh_: lock(C, 540, 1150, 0.8, tw(t, 'шифруют') / 0.3)
    slam(C, u, 'ПОЭТОМУ ДАННЫЕ', 540, SY, 116)
    if sh_: plate(C, tw(t, 'шифруют') + 0.05, 'ШИФРУЮТ', 540, PY, 120, INK, YEL, -3)
def tunnel(C, x0, x1, y, h=150, k=1.0):
    d = ImageDraw.Draw(C); xe = lerp(x0, x1, eo(k))
    d.rounded_rectangle([x0, y - h / 2, xe, y + h / 2], radius=int(h / 2), fill=INK)
    d.rounded_rectangle([x0 + 10, y - h / 2 + 10, max(x0 + 20, xe - 10), y - h / 2 + 26], radius=8, fill=(70, 70, 70))
def s_vpn(C, u, t):    # Это, например, делает VPN: он закрывает твой трафик,
    ground(C); cat(C, t, 170, G, 270, eyes='happy'); sneak(C, t, 860, G, 0.7, -1)
    tk = clamp(tw(t, 'ви-пи-эн') / 0.6) if at(t, 'ви-пи-эн', 0, -0.1) else 0
    tunnel(C, 260, 760, 960, 160, tk)
    if tk > 0.3: put(C, text_img('VPN', 70, YEL), 510, 960)
    if tk < 0.3:
        for j in range(3):
            k = (u * 0.8 + j * 0.33) % 1; envelope_(C, lerp(280, 740, k), 960, 90)
    if at(t, 'закрывает', 0, -0.1): tag(C, tw(t, 'закрывает'), 'ТРАФИК ЗАШИФРОВАН', 510, 1110, 42, YEL, INK, -2)
    slam(C, u, 'ЭТО, НАПРИМЕР,', 540, SY, 110)
    if at(t, 'ви-пи-эн', 0, -0.1): plate(C, tw(t, 'ви-пи-эн') + 0.05, 'ДЕЛАЕТ VPN', 540, PY, 104, INK, YEL, 3)
def s_chitali(C, u, t):    # чтобы чужие не читали.
    ground(C); sneak(C, t, 640, G, 0.9, 0)
    for j, q in enumerate('???'): pop(C, u - 0.1 - j * 0.12, q, 420 + j * 110, 820 - 30 * (j % 2), 130, RED, (-1) ** j * 10)
    tunnel(C, 0, 1080, 1180, 90, 1.0); put(C, text_img('VPN', 44, YEL), 300, 1180)
    slam(C, u, 'ЧТОБЫ ЧУЖИЕ', 540, SY, 130)
    if at(t, 'читали', 0, -0.1): plate(C, tw(t, 'читали') + 0.05, 'НЕ ЧИТАЛИ', 540, PY, 104, RED, WHITE, -3)
def s_odin(C, u, t):    # Но это только один из способов,
    ground(C); dog(C, t, 290, G, 380, 'stand')
    tunnel(C, 560, 900, 1040, 110, 1.0); put(C, text_img('VPN', 50, YEL), 730, 1040); put(C, text_img('1', 80, INK), 730, 920)
    slam(C, u, 'НО ЭТО ЛИШЬ', 540, SY, 120)
    if at(t, 'способов', 0, -0.1): plate(C, tw(t, 'способов') + 0.05, 'ОДИН ИЗ СПОСОБОВ', 540, PY, 96, YEL, INK, 3)
def s_esche(C, u, t):    # ещё есть обновления, разрешения приложений и вообще мозги.
    ground(C); dog(C, t, 230, G, 300, 'point' if at(t, 'мозги', 0, -0.1) else 'stand', eyes='happy' if at(t, 'мозги', 0, -0.1) else 'n')
    tk = tuple(i for i, w in enumerate(['обновления', 'разрешения', 'мозги']) if at(t, w))
    sheet(C, 680, 990, 420, 'ЕЩЁ ЗАЩИТА', ['ОБНОВЛЕНИЯ', 'РАЗРЕШЕНИЯ', 'МОЗГИ'], tk, u / 0.3, 3)
    slam(C, u, 'ЕЩЁ ЕСТЬ', 540, SY, 140)
    if at(t, 'мозги', 0, -0.05): stamp(C, tw(t, 'мозги'), 'И МОЗГИ', 540, PY + 10, 110, RED, -6)
def s_nuzhen(C, u, t):    # (кот) Да кому я нужен... пусть смотрят.
    ground(C); lie = at(t, 'смотрят', 0, -0.1)
    kot(C, t, 540, G, 460, pose='loaf' if lie else 'stretch', eyes='closed' if not lie else 'half', mouth='smug')
    if not lie: bubble_say(C, 540, 640, 'ДА КОМУ Я НУЖЕН...', u / 0.3, (240, 238, 234), -40, 76)
    else: bubble_say(C, 540, 640, 'ПУСТЬ СМОТРЯТ', tw(t, 'смотрят') / 0.3 + 0.35, (240, 238, 234), -40, 80)
    if lie: zzz(C, 720, 900, u, KOTD)
    slam(C, u, 'КОТ:', 540, SY, 120, KOTD)
def s_geroy(C, u, t):    # Ну ладно, герой.
    YB(C, u, 5); kot(C, t, 540, G, 440, pose='cape', look=(0, 0))
    slam(C, u, 'НУ ЛАДНО,', 540, SY, 140)
    if at(t, 'герой', 0, -0.05): plate(C, tw(t, 'герой') + 0.05, 'ГЕРОЙ', 540, PY, 130, INK, YEL, -4)
def s_gugl(C, u, t):    # Тогда пиши в комментах, что ты гуглил последним.
    ground(C); dog(C, t, 230, G, 300); cat(C, t, 830, G, 290, look=(-0.6, 0))
    searchbar(C, 540, 860, 820, 'что я гуглил последним...', u / 1.4, t)
    comment(C, 540, 1040, 640, 'ПИШИ В КОММЕНТЫ', clamp(tw(t, 'комментах') / 0.3) if at(t, 'комментах') else 0, -2, ORNG)
    slam(C, u, 'ЧТО ТЫ ГУГЛИЛ', 540, SY, 120)
    if at(t, 'последним'): plate(C, tw(t, 'последним') + 0.05, 'ПОСЛЕДНИМ?', 540, PY, 110, YEL, INK, 3)
def s_nevidim(C, u, t):    # Если не страшно, мы же всё равно не видим.
    ground(C); cv = at(t, 'мы', 0, -0.1)
    dog(C, t, 300, G, 380, 'cover' if cv else 'stand'); cat(C, t, 780, G, 360, pose='cover' if cv else 'sit')
    slam(C, u, 'ЕСЛИ НЕ СТРАШНО', 540, SY, 110)
    if at(t, 'видим', 0, -0.1): plate(C, tw(t, 'видим') + 0.05, 'МЫ НЕ ВИДИМ', 540, PY, 104, INK, YEL, -3)
def s_takzhe(C, u, t):    # А те, кому есть что скрывать, пишите «у меня так же»,
    d = ImageDraw.Draw(C)
    for j in range(6):
        k = clamp(tw(t, 'пишите') / 0.25 - j * 0.6) if at(t, 'пишите', 0, -0.1) else 0
        comment(C, 540 + (-1) ** j * 40, 760 + j * 105, 600, 'У МЕНЯ ТАК ЖЕ', k, (-1) ** j * 2, [ORNG, TEAL, OLIVE, RUST, OCHRE, KOT][j], 44, j == 0)
    slam(C, u, 'ЕСТЬ ЧТО СКРЫВАТЬ?', 540, SY, 106)
def s_kogo(C, u, t):    # посмотрим, кого больше.
    ground(C); scales(C, 540, 760, u, 'ГУГЛИЛ', 'ТАК ЖЕ', 0.6 * s_(u * 4) * math.exp(-u))
    slam(C, u, 'ПОСМОТРИМ,', 540, SY, 130)
    if at(t, 'больше', 2, -0.1): plate(C, tw(t, 'больше', 2) + 0.05, 'КОГО БОЛЬШЕ', 540, PY, 104, YEL, INK, 3)
def s_podpis(C, u, t):    # Подписывайся, пока кот не продал твои данные.
    ground(C); sign_sale(C, 830, G - 10, 'ПРОДАМ ДАННЫЕ', 0.9); kot(C, t, 830, G, 260, look=(-0.6, 0))
    z = 1 + 0.12 * eo(u / 2.5); dog(C, t, 380, G, int(400 * z), 'stand', eyes='n')
    slam(C, u, 'ПОДПИСЫВАЙСЯ', 540, SY, 130)
    if at(t, 'кот', 3, -0.1): plate(C, tw(t, 'кот', 3) + 0.05, 'ПОКА КОТ НЕ ПРОДАЛ', 540, PY, 92, INK, YEL, -3)
    if at(t, 'данные', 1, -0.1): tag(C, tw(t, 'данные', 1), 'ТВОИ ДАННЫЕ', 540, 740, 56, YEL, INK, 3)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'zoomin'), SH(T('И', 0) - 0.05, s_bkot, 'zoomthru', 'bass', (540, 1000)), SH(T('А', 0) - 0.05, s_vse, 'whipL', 'whoosh'),
 SH(T('Пёс') - 0.05, s_pes, 'door', 'bass'), SH(T('Нюхнул') - 0.05, s_nyuh, 'whipR', 'whoosh'), SH(T('тут') - 0.05, s_tri, 'zoomthru', 'bass', (850, 1200)),
 SH(T('пока', 0) - 0.05, s_spish, 'whipL', 'whoosh'), SH(T('Вот', 0) - 0.05, s_karta, 'drop', 'bass'), SH(T('Приложение') - 0.05, s_app, 'zoom', 'pop'),
 SH(T('Фонарик') - 0.05, s_karl, 'shake', 'boom'), SH(T('Ему') - 0.05, s_vidit, 'whipR', 'whoosh'),
 SH(T('Дальше') - 0.05, s_fotki, 'door', 'bass'), SH(T('В', 0) - 0.05, s_exif, 'zoomthru', 'bass', (540, 900)),
 SH(T('Вот', 1) - 0.05, s_phcat, 'whipL', 'swipe'), SH(T('вот', 0) - 0.05, s_phdog, 'whipL', 'swipe'), SH(T('вот', 1) - 0.05, s_phkot, 'whipL', 'swipe'),
 SH(T('Кстати') - 0.05, s_troe, 'drop', 'bass'), SH(T('они') - 0.15, s_paroli, 'whipR', 'whoosh'), SH(T('Ну', 0) - 0.05, s_pochti, 'shake', 'boing'),
 SH(T('А', 1) - 0.05, s_kafe, 'door', 'bass'), SH(T('Ей') - 0.05, s_vidos, 'whipL', 'whoosh'), SH(T('А', 2) - 0.05, s_sosed, 'shake', 'alarm'),
 SH(T('подсмотреть') - 0.05, s_podsm, 'zoom', 'zoomin'), SH(T('Поэтому') - 0.05, s_shifr, 'drop', 'bass'), SH(T('Это') - 0.05, s_vpn, 'whipR', 'whoosh'),
 SH(T('чтобы') - 0.05, s_chitali, 'zoom', 'error'), SH(T('Но') - 0.05, s_odin, 'door', 'bass'), SH(T('ещё') - 0.05, s_esche, 'whipL', 'whoosh'),
 SH(T('Да') - 0.1, s_nuzhen, 'zoomthru', 'drop', (540, 1000)), SH(T('Ну', 1) - 0.05, s_geroy, 'shake', 'boom'), SH(T('Тогда') - 0.05, s_gugl, 'whipR', 'whoosh'),
 SH(T('Если') - 0.05, s_nevidim, 'whipL', 'whoosh'), SH(T('А', 3) - 0.05, s_takzhe, 'drop', 'bass'), SH(T('посмотрим') - 0.05, s_kogo, 'whipR', 'whoosh'),
 SH(T('Подписывайся') - 0.05, s_podpis, 'zoomthru', 'final', (540, 900)),
]
ACC = [(T('больше', 0), 'pop'), (T('ВСЁ'), 'stamp'), (T('безопасности'), 'pop'), (T('доложил'), 'ding'), (T('три'), 'alarm'), (T('следят'), 'error'),
       (T('неделю'), 'pop'), (T('ночуешь'), 'drop'), (T('Карл'), 'stamp'), (T('видит'), 'shine'), (T('время'), 'pop'), (T('место'), 'pop'), (T('модель'), 'pop'),
       (T('пофиг'), 'stamp'), (T('трое'), 'pop'), (T('паролей'), 'click'), (T('почти'), 'scratch'), (T('бесплатном'), 'notif'), (T('видосики'), 'pop'),
       (T('ходит'), 'click'), (T('шифруют'), 'ok'), (T('ви-пи-эн'), 'zoomin'), (T('читали'), 'error'), (T('обновления'), 'ok'), (T('разрешения'), 'ok'),
       (T('мозги'), 'stamp'), (T('герой'), 'pop'), (T('последним'), 'msg'), (T('видим'), 'pop'), (T('пишите'), 'msg'), (T('больше', 2), 'ding'),
       (T('продал'), 'kassa')]
def qcounter(F, t): return
