"""Рилс «Пряник и Claude Code» (шуточный). Пряник B: имбирный круг, лицо из белой глазури.
Одно движение: покачивание + рот под громкость голоса."""
from scenes_ak import *
import subprocess as _sp, array as _ar
D = ImageDraw.Draw
BR = (184, 105, 46); BRD = (122, 63, 23); ICE = (255, 255, 255); PUP = (42, 18, 6)
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
@lru_cache(None)
def mono(sz): return ImageFont.truetype(MONO, int(sz))

# ---------- громкость голоса по кадрам (для рта) ----------
def _env():
    raw = _sp.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(HERE, '../zvuk/voice.mp3'), '-ac', '1', '-ar', '6000', '-f', 's16le', '-'], capture_output=True).stdout
    a = _ar.array('h'); a.frombytes(raw); step = 6000 // FPS; out = []
    for i in range(0, len(a), step):
        seg = a[i:i + step]; out.append((sum(x * x for x in seg) / max(1, len(seg))) ** 0.5)
    m = sorted(out)[int(len(out) * 0.97)] or 1
    return [min(1.0, v / m) for v in out]
ENV = _env()
def loud(t):
    i = int(t * FPS); return ENV[i] if 0 <= i < len(ENV) else 0

# ---------- пряник ----------
def _limb(d, pts, w, col):
    for a, b in zip(pts, pts[1:]): d.line([a, b], fill=col, width=int(w))
    for (x, y) in (pts[0], pts[-1]): d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)
def _qb(p0, p1, p2, n=12):
    return [((1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0], (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1]) for k in [j / n for j in range(n + 1)]]
@lru_cache(512)
def pr_img(r, pose, mo, eyes):
    """r — радиус, pose: up/down/hips/phone, mo — раскрытие рта 0..6, eyes: n/shock/happy/angry"""
    S = int(r * 3.4); im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = D(im); cx, cy = S / 2, S * 0.40; w = r * 0.26
    # руки
    if pose == 'up':
        for sd in (-1, 1): _limb(d, _qb((cx + sd * r * 0.9, cy), (cx + sd * r * 1.35, cy - r * 0.4), (cx + sd * r * 1.15, cy - r * 0.95)), w, BRD)
    elif pose == 'hips':
        for sd in (-1, 1): _limb(d, _qb((cx + sd * r * 0.9, cy + r * 0.1), (cx + sd * r * 1.45, cy + r * 0.35), (cx + sd * r * 0.95, cy + r * 0.62)), w, BRD)
    elif pose == 'phone':
        _limb(d, _qb((cx - r * 0.95, cy + r * 0.1), (cx - r * 1.3, cy + r * 0.5), (cx - r * 1.35, cy + r * 0.75)), w, BRD)
        _limb(d, _qb((cx + r * 0.9, cy + r * 0.1), (cx + r * 1.4, cy + r * 0.1), (cx + r * 1.25, cy - r * 0.35)), w, BRD)
    else:
        for sd in (-1, 1): _limb(d, [(cx + sd * r * 0.95, cy + r * 0.1), (cx + sd * r * 1.35, cy + r * 0.6)], w, BRD)
    for sd in (-1, 1): _limb(d, [(cx + sd * r * 0.35, cy + r * 0.85), (cx + sd * r * 0.4, cy + r * 1.42)], w, BRD)
    # тело + волна глазури
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BR)
    pts = []
    for i in range(29):
        a = 2 * math.pi * i / 28; rr = r * 0.84 + (r * 0.035 if i % 2 else -r * 0.035); pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(pts, fill=ICE, width=int(r * 0.06), joint='curve')
    # глаза
    ex, ey, er = r * 0.3, cy - r * 0.15, r * 0.13
    for sd in (-1, 1):
        x = cx + sd * ex
        if eyes == 'happy': d.arc([x - er, ey - er * 0.6, x + er, ey + er * 1.2], 200, 340, fill=ICE, width=int(r * 0.06)); continue
        rr = er * (1.25 if eyes == 'shock' else 1); d.ellipse([x - rr, ey - rr, x + rr, ey + rr], fill=ICE)
        pr = r * (0.035 if eyes == 'shock' else 0.05); d.ellipse([x - pr, ey + r * 0.02 - pr, x + pr, ey + r * 0.02 + pr], fill=PUP)
        if eyes == 'angry': d.line([x - sd * er * 1.3, ey - er * 1.6, x + sd * er * 1.1, ey - er * 0.7], fill=ICE, width=int(r * 0.06))
    # рот
    my = cy + r * 0.33; lw = int(r * 0.06)
    if mo == 0 and eyes == 'happy': d.arc([cx - r * 0.25, my - r * 0.2, cx + r * 0.25, my + r * 0.12], 20, 160, fill=ICE, width=lw)
    elif mo == 0: d.line([cx - r * 0.13, my, cx + r * 0.13, my], fill=ICE, width=lw)
    else:
        ry = r * (0.05 + 0.032 * mo); rx = r * (0.13 + 0.008 * mo); d.ellipse([cx - rx, my - ry, cx + rx, my + ry], outline=ICE, width=lw)
    return im
def pryanik(C, t, cx, feet=FEET, r=150, pose='down', eyes='n', mouth=None, rot=None, scale=1.0, sway=1.0):
    """одно движение: покачивание с подпрыгиванием, рот по громкости голоса"""
    r = int(r * scale)
    mo = mouth if mouth is not None else (int(round(loud(t) * 6)) if loud(t) > 0.12 else 0)
    im = pr_img(r, pose, mo, eyes); S = im.width
    a = (4 * s_(t * 4.2) if rot is None else rot) * sway; b = abs(s_(t * 4.2)) * r * 0.06 * sway
    D(C).ellipse([cx - r * 0.85, feet - r * 0.11, cx + r * 0.85, feet + r * 0.11], fill=(0, 0, 0, 30) if False else (226, 223, 216))
    if a: im = im.rotate(a, Image.BICUBIC, center=(S / 2, S * 0.40 + r * 1.42))
    C.alpha_composite(im, (int(cx - S / 2), int(feet - (S * 0.40 + r * 1.42) - b)))

# ---------- предметы ----------
def laptop(C, cx, cy, w, lines, k=1.0, cursor=True, t=0):
    """ноутбук с терминалом Claude Code; lines: [(текст, цвет)]"""
    if k <= 0: return
    h = w * 0.62; im = Image.new('RGBA', (int(w * 1.2) + 20, int(h + w * 0.1) + 20), (0, 0, 0, 0)); d = D(im); ox = w * 0.1 + 10
    d.rounded_rectangle([ox, 10, ox + w, 10 + h], radius=int(w * 0.03), fill=(30, 30, 30), outline=INK, width=6)
    d.rounded_rectangle([ox + w * 0.035, 10 + w * 0.035, ox + w * 0.965, 10 + h - w * 0.035], radius=8, fill=(14, 14, 14))
    d.polygon([(ox - w * 0.08, 10 + h + w * 0.07), (ox + w * 1.08, 10 + h + w * 0.07), (ox + w, 10 + h), (ox, 10 + h)], fill=(52, 52, 52), outline=INK)
    sz = w * 0.068; y = 10 + w * 0.07; f = mono(sz)
    d.text((ox + w * 0.07, y), '✻ Claude Code', font=mono(sz * 1.05), fill=(217, 119, 87)); y += sz * 1.9
    for (s, col) in lines:
        d.text((ox + w * 0.07, y), s, font=f, fill=col); y += sz * 1.5
    if cursor and int(t * 2.5) % 2 == 0: d.rectangle([ox + w * 0.07, y + 4, ox + w * 0.07 + sz * 0.55, y + sz * 1.1], fill=(220, 220, 220))
    put(C, im, cx, cy, back(k / 0.22) if k < 0.3 else 1)
GRY = (200, 200, 200); GRNT = (110, 210, 120); ORG = (217, 119, 87)
def folder(C, cx, cy, s=1.0, label='МОЙ ПРОЕКТ', rot=0, k=1.0):
    if k <= 0: return
    w, h = int(300 * s), int(220 * s); im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = D(im)
    d.rounded_rectangle([10, 10, 10 + w * 0.45, 10 + h * 0.25], radius=int(14 * s), fill=(240, 180, 40), outline=INK, width=6)
    d.rounded_rectangle([10, 10 + h * 0.15, 10 + w, 10 + h], radius=int(16 * s), fill=YEL, outline=INK, width=6)
    t_ = text_img(label, int(34 * s)); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(10 + h * 0.58 - t_.height / 2)))
    put(C, im, cx, cy, back(k / 0.22) if k < 0.3 else 1, rot)
def sheet(C, cx, cy, w, title, rows, ticks=(), k=1.0, rot=-3):
    if k <= 0: return
    h = int(w * 1.2); im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = D(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=14, fill=WHITE, outline=INK, width=7)
    d.polygon([(10 + w - 70, 10), (10 + w, 80), (10 + w - 70, 80)], fill=LG, outline=INK)
    t_ = text_img(title, int(w * 0.11)); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), 40))
    y = 60 + t_.height + 30
    for i, row in enumerate(rows):
        bx = 50; d.rounded_rectangle([bx, y, bx + 54, y + 54], radius=8, outline=INK, width=6, fill=WHITE)
        if i in ticks: d.line([(bx + 10, y + 28), (bx + 24, y + 44), (bx + 48, y + 8)], fill=GRN, width=10)
        tt = text_img(row, int(w * 0.085)); im.alpha_composite(tt, (bx + 80, int(y + 27 - tt.height / 2))); y += 92
    put(C, im, cx, cy, back(k / 0.22) if k < 0.3 else 1, rot)
def chatwin(C, cx, cy, w, h, n_msgs, title='ЧАТ', rot=0, messy=False, seed=1, empty_text=None):
    im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = D(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=20, fill=WHITE, outline=INK, width=7)
    d.rounded_rectangle([10, 10, 10 + w, 80], radius=20, fill=INK); d.rectangle([10, 60, 10 + w, 80], fill=INK)
    t_ = text_img(title, 40, WHITE); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(45 - t_.height / 2)))
    rnd = random.Random(seed); y = 100
    for j in range(n_msgs):
        if y > h - 30: break
        bw = rnd.randint(int(w * 0.35), int(w * 0.75)); right = j % 2 == 1; x0 = 10 + w - 25 - bw if right else 35
        d.rounded_rectangle([x0, y, x0 + bw, y + 44], radius=18, fill=YEL if right else LG); y += 58 if not messy else rnd.randint(30, 50)
    if empty_text:
        t2 = text_img(empty_text, 46, GREY); im.alpha_composite(t2, (int(10 + w / 2 - t2.width / 2), int(10 + h / 2 - t2.height / 2)))
    put(C, im, cx, cy, 1, rot)
def qr(C, cx, cy, s=200, k=1.0):
    if k <= 0: return
    n = 21; c = s / n; im = Image.new('RGBA', (s + 40, s + 40), WHITE + (255,)); d = D(im); rnd = random.Random(5)
    d.rectangle([0, 0, s + 39, s + 39], outline=INK, width=6)
    for i in range(n):
        for j in range(n):
            fin = any(i0 <= i < i0 + 7 and j0 <= j < j0 + 7 for i0, j0 in ((0, 0), (0, n - 7), (n - 7, 0)))
            if fin:
                ii, jj = min(i % 7, (6 - i % 7)) if False else i, j
                on = any((i0 <= i < i0 + 7 and j0 <= j < j0 + 7) and (i in (i0, i0 + 6) or j in (j0, j0 + 6) or (i0 + 2 <= i <= i0 + 4 and j0 + 2 <= j <= j0 + 4)) for i0, j0 in ((0, 0), (0, n - 7), (n - 7, 0)))
            else: on = rnd.random() < 0.45
            if on: d.rectangle([20 + j * c, 20 + i * c, 20 + (j + 1) * c, 20 + (i + 1) * c], fill=INK)
    put(C, im, cx, cy, back(k / 0.22) if k < 0.3 else 1)
def bigphone(C, cx, cy, s=1.0, rot=0, label='CLAUDE'):
    w, h = int(200 * s), int(380 * s); im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = D(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=int(34 * s), fill=INK)
    d.rounded_rectangle([10 + 14 * s, 10 + 34 * s, 10 + w - 14 * s, 10 + h - 34 * s], radius=int(16 * s), fill=(14, 14, 14))
    t_ = text_img('*', int(110 * s), ORG); im.alpha_composite(t_, (int(10 + w / 2 - t_.width / 2), int(10 + h * 0.36)))
    t2 = text_img(label, int(34 * s), WHITE); im.alpha_composite(t2, (int(10 + w / 2 - t2.width / 2), int(10 + h * 0.6)))
    put(C, im, cx, cy, 1, rot)
def house(C, cx, by, w=420):
    d = D(C); h = w * 0.7
    d.rectangle([cx - w / 2, by - h, cx + w / 2, by], fill=WHITE, outline=INK, width=8)
    d.polygon([(cx - w / 2 - 40, by - h + 4), (cx, by - h - w * 0.45), (cx + w / 2 + 40, by - h + 4)], fill=RED, outline=INK)
def toilet(C, cx, by, s=1.0):
    d = D(C)
    d.rounded_rectangle([cx + 60 * s, by - 420 * s, cx + 200 * s, by - 170 * s], radius=int(16 * s), fill=WHITE, outline=INK, width=8)   # бачок
    d.rounded_rectangle([cx - 190 * s, by - 200 * s, cx + 170 * s, by - 150 * s], radius=int(20 * s), fill=WHITE, outline=INK, width=8)  # сиденье
    d.polygon([(cx - 150 * s, by - 150 * s), (cx + 130 * s, by - 150 * s), (cx + 60 * s, by - 40 * s), (cx + 80 * s, by), (cx - 60 * s, by), (cx - 40 * s, by - 40 * s)], fill=WHITE, outline=INK)
    d.line([(cx - 150 * s, by - 150 * s), (cx - 40 * s, by - 40 * s), (cx - 60 * s, by), (cx + 80 * s, by), (cx + 60 * s, by - 40 * s), (cx + 130 * s, by - 150 * s)], fill=INK, width=8)
def crumbs(C, t0, cx, cy, n=7):
    if t0 < 0: return
    d = D(C); rnd = random.Random(2)
    for j in range(n):
        vx = rnd.uniform(-160, 160); y = cy + 900 * t0 * t0 + rnd.uniform(-20, 20); x = cx + vx * t0; r = rnd.uniform(8, 16)
        d.ellipse([x - r, y - r, x + r, y + r], fill=BR, outline=BRD, width=3)
def arrow(C, x0, y, x1, k=1.0, col=INK):
    if k <= 0: return
    d = D(C); x = lerp(x0, x1, eo(k)); d.line([x0, y, x - 30, y], fill=col, width=20); d.polygon([(x - 50, y - 40), (x + 10, y), (x - 50, y + 40)], fill=col)
