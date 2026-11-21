"""Герои рилса «Что знает о тебе телефон»: пёс (охрана), кошка (с розовым бантом), кот (толстый ленивый скептик).
Плоские 2D-фигуры в тёплой осенней палитре, рисуются кодом (PIL, суперсэмплинг ×2).
Анкер у всех — середина пятна под лапами (feet)."""
from scenes_pr import *

# тёплая осенняя палитра
CARD = (251, 246, 237)                                   # кремовый фон вместо холодного белого
import base_k as _bk; _bk.CARD = CARD
DOG = (201, 132, 68); DOGD = (128, 76, 38); DOGL = (244, 220, 180)
CAT = (233, 138, 58); CATD = (176, 88, 30); CATL = (250, 214, 162)
KOT = (92, 86, 84); KOTD = (58, 54, 53); KOTL = (156, 148, 142)
PINKN = (240, 128, 140); BOW = (255, 79, 139)
ORNG = (236, 128, 44); RUST = (186, 74, 38); OCHRE = (222, 170, 60); OLIVE = (128, 138, 70); TEAL = (70, 130, 140)
EYEW = (255, 255, 255); PUPC = (24, 18, 14)
SS = 2

def _e(d, cx, cy, rx, ry, **k): d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], **k)
def _thick(d, pts, w, col):
    d.line(pts, fill=col, width=int(w), joint='curve')
    for (x, y) in (pts[0], pts[-1]): _e(d, x, y, w / 2, w / 2, fill=col)
def _curve(p0, p1, p2, n=14): return [((1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0], (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1]) for k in [j / n for j in range(n + 1)]]

def _eyes(d, xs, y, r, eyes, look=(0, 0), lid=0.0, slit=False):
    """eyes: n / shock / happy / closed / half / side; look — сдвиг зрачков (-1..1)"""
    for x in xs:
        if eyes == 'happy':
            d.arc([x - r, y - r * 0.5, x + r, y + r * 1.3], 200, 340, fill=PUPC, width=max(3, int(r * 0.35))); continue
        if eyes == 'closed':
            d.arc([x - r, y - r * 1.2, x + r, y + r * 0.6], 20, 160, fill=PUPC, width=max(3, int(r * 0.35))); continue
        rr = r * (1.3 if eyes == 'shock' else 1.0)
        _e(d, x, y, rr, rr * 1.1, fill=EYEW, outline=PUPC, width=max(2, int(r * 0.18)))
        pr = rr * (0.42 if eyes == 'shock' else 0.55); px, py = x + look[0] * rr * 0.4, y + look[1] * rr * 0.4
        if slit and eyes != 'shock': _e(d, px, py, pr * 0.45, pr * 1.2, fill=PUPC)
        else: _e(d, px, py, pr, pr, fill=PUPC)
        _e(d, px - pr * 0.35, py - pr * 0.4, pr * 0.28, pr * 0.28, fill=EYEW)
        lid_ = 0.55 if eyes == 'half' else lid
        if lid_ > 0:   # веко сверху
            d.chord([x - rr * 1.15, y - rr * 1.25, x + rr * 1.15, y - rr * 1.25 + rr * 2.5 * lid_ * 1.6], 180, 360, fill=d._lidcol)
            d.line([x - rr * 1.05, y - rr * 1.1 + rr * 2.2 * lid_, x + rr * 1.05, y - rr * 1.1 + rr * 2.2 * lid_], fill=PUPC, width=max(2, int(r * 0.25)))

def _mouth(d, cx, cy, w, mo, kind='smile', col=PUPC):
    lw = max(3, int(w * 0.14))
    if mo > 0:
        ry = w * (0.12 + 0.07 * mo); rx = w * (0.32 + 0.02 * mo)
        _e(d, cx, cy + ry * 0.5, rx, ry, fill=(90, 30, 30), outline=col, width=lw)
        _e(d, cx, cy + ry * 1.05, rx * 0.5, ry * 0.4, fill=(232, 110, 120)); return
    if kind == 'smile':
        d.arc([cx - w * 0.5, cy - w * 0.35, cx, cy + w * 0.15], 10, 170, fill=col, width=lw); d.arc([cx, cy - w * 0.35, cx + w * 0.5, cy + w * 0.15], 10, 170, fill=col, width=lw)
    elif kind == 'flat': d.line([cx - w * 0.3, cy, cx + w * 0.3, cy], fill=col, width=lw)
    elif kind == 'smug': d.arc([cx - w * 0.45, cy - w * 0.4, cx + w * 0.45, cy + w * 0.1], 20, 120, fill=col, width=lw)
    elif kind == 'o': _e(d, cx, cy + w * 0.1, w * 0.16, w * 0.22, fill=(90, 30, 30), outline=col, width=lw)
    elif kind == 'sad': d.arc([cx - w * 0.35, cy, cx + w * 0.35, cy + w * 0.5], 200, 340, fill=col, width=lw)

def _shadow(C, cx, feet, w):
    d = ImageDraw.Draw(C); _e(d, cx, feet, w, w * 0.12, fill=(228, 218, 202))

# ================= ПЁС =================
@lru_cache(600)
def dog_img(s, pose, eyes, mo, wag, cap, mouth):
    """s — высота до макушки, px. pose: stand / sniff / point / cover. Смотрит вправо, голова анфас."""
    U = s / 200 * SS; Wd, Hd = int(340 * U), int(300 * U); ox, oy = Wd * 0.5, Hd * 0.93
    im = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d._lidcol = DOG
    P = lambda x, y: (ox + x * U, oy + y * U)
    # хвост
    tw = (wag - 3.5) / 3.5
    if pose == 'point': tail = [P(-78, -95), P(-110, -99), P(-138, -102)]
    else: tail = [P(-78, -95), P(-110 + tw * 8, -120), P(-112 + tw * 28, -160)]
    _thick(d, _curve(*tail), 18 * U, DOG)
    # дальние лапы
    for x in (-48, 42):
        if pose == 'point' and x == 42: continue
        d.rounded_rectangle([*P(x - 9, -70), *P(x + 9, 0)], radius=int(9 * U), fill=DOGD)
    # тело
    _e(d, *P(0, -92), 84 * U, 40 * U, fill=DOG)
    _e(d, *P(10, -76), 50 * U, 18 * U, fill=DOGL)
    # ближние лапы
    for x in (-62, 58):
        if pose == 'point' and x == 58:
            _thick(d, [P(58, -80), P(80, -70), P(88, -44)], 20 * U, DOG); continue
        d.rounded_rectangle([*P(x - 11, -72), *P(x + 11, 0)], radius=int(11 * U), fill=DOG)
        _e(d, *P(x + 4, -4), 15 * U, 8 * U, fill=DOGL)
    # голова
    if pose == 'sniff': hx, hy, tilt = 98, -88, 0
    elif pose == 'point': hx, hy, tilt = 92, -150, 0
    else: hx, hy, tilt = 76, -156, 0
    H = Image.new('RGBA', (int(140 * U), int(150 * U)), (0, 0, 0, 0)); h = ImageDraw.Draw(H); h._lidcol = DOG
    Q = lambda x, y: (70 * U + x * U, 80 * U + y * U)
    for sd in (-1, 1): h.polygon([Q(sd * 30, -28), Q(sd * 58, -18), Q(sd * 56, 26), Q(sd * 40, 32), Q(sd * 28, -4)], fill=DOGD)   # уши
    _e(h, *Q(0, 0), 44 * U, 42 * U, fill=DOG)
    _e(h, *Q(0, 20), 26 * U, 19 * U, fill=DOGL)
    _eyes(h, [Q(-16, -10)[0], Q(16, -10)[0]], Q(0, -10)[1], 8 * U, eyes, (0.6, 0) if pose == 'point' else (0, 0.6) if pose == 'sniff' else (0, 0))
    _e(h, *Q(0, 9), 9 * U, 6.5 * U, fill=PUPC)
    _mouth(h, *Q(0, 23), 22 * U, mo, mouth)
    if pose == 'sniff':
        for j in range(3): h.arc([*Q(44 + j * 10, -6 - j * 3), *Q(58 + j * 12, 16 + j * 3)], 300, 60, fill=PUPC, width=max(2, int(3 * U)))
    if cap:   # фуражка охраны: чёрная + жёлтая кокарда
        h.chord([*Q(-40, -60), *Q(40, -2)], 180, 360, fill=INK); h.rounded_rectangle([*Q(-48, -34), *Q(48, -24)], radius=int(5 * U), fill=INK)
        _e(h, *Q(0, -44), 9 * U, 8 * U, fill=YEL)
    if pose == 'cover':   # лапы закрывают глаза
        for sd in (-1, 1): _e(h, *Q(sd * 18, -10), 20 * U, 15 * U, fill=DOG, outline=DOGD, width=max(2, int(3 * U)))
    im.alpha_composite(H, (int(P(hx, hy)[0] - 70 * U), int(P(hx, hy)[1] - 80 * U)))
    return im.resize((Wd // SS, Hd // SS), Image.LANCZOS), ox / SS, oy / SS

def blink(t, seed=0):
    p = (t + seed * 1.37) % 3.3; return p < 0.12
def dog(C, t, cx, feet=FEET, s=300, pose='stand', eyes='n', mo=0, cap=True, flip=False, mouth='smile', sway=1.0, shadow=True):
    e = 'closed' if (eyes == 'n' and blink(t, 1)) else eyes
    wag = int((s_(t * 14) * 0.5 + 0.5) * 7) if pose != 'point' else 0
    im, ox, oy = dog_img(int(s), pose, e, mo, wag, cap, mouth)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT); ox = im.width - ox
    b = abs(s_(t * 3.0)) * s * 0.012 * sway
    if shadow: _shadow(C, cx, feet, s * 0.48)
    C.alpha_composite(im, (int(cx - ox), int(feet - oy - b)))

# ================= КОШКА / КОТ (анфас, сидят) =================
@lru_cache(600)
def cat_img(s, kind, pose, eyes, mo, tailp, mouth, look):
    """kind: cat (кошка, рыжая, бант) / kot (толстый серый). pose: sit / loaf / stretch / cape / cover / shrug"""
    fat = 1.38 if kind == 'kot' else 1.0
    B, BD, BL = (CAT, CATD, CATL) if kind == 'cat' else (KOT, KOTD, KOTL)
    U = s / 200 * SS; Wd, Hd = int(360 * U), int(280 * U); ox, oy = Wd / 2, Hd * 0.95
    im = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d._lidcol = B
    P = lambda x, y: (ox + x * U, oy + y * U)
    tp = (tailp - 3.5) / 3.5
    if pose == 'cape':   # плащ героя
        d.polygon([P(-40 * fat, -118), P(40 * fat, -118), P(70 * fat + tp * 6, -4), P(-70 * fat - tp * 6, -4)], fill=RED)
    if pose == 'loaf':
        _thick(d, _curve(P(70 * fat, -18), P(112 * fat, -10), P(118 * fat + tp * 10, -46)), 16 * U, B)
        _e(d, *P(0, -40), 86 * fat * U, 42 * U, fill=B)
        _e(d, *P(0, -22), 50 * fat * U, 18 * U, fill=BL)
        for sd in (-1, 1): _e(d, *P(sd * 26, -6), 18 * U, 9 * U, fill=BL)
        hx, hy = 0, -96
    else:
        _thick(d, _curve(P(30 * fat, -12), P(90 * fat, -14), P(84 * fat + tp * 14, -76 - tp * 6)), 15 * U, B)
        _e(d, *P(0, -46), 52 * fat * U, 48 * U, fill=B)
        _e(d, *P(0, -84), 38 * fat * U, 40 * U, fill=B)
        _e(d, *P(0, -52), 26 * fat * U, 36 * U, fill=BL)
        if pose == 'stretch':
            for sd in (-1, 1): _thick(d, [P(sd * 30 * fat, -100), P(sd * 50 * fat, -150), P(sd * 56 * fat, -196)], 18 * U, B); _e(d, *P(sd * 56 * fat, -198), 13 * U, 11 * U, fill=BL)
        elif pose == 'shrug':
            for sd in (-1, 1): _thick(d, [P(sd * 34 * fat, -96), P(sd * 70 * fat, -88), P(sd * 82 * fat, -116)], 16 * U, B); _e(d, *P(sd * 84 * fat, -120), 12 * U, 10 * U, fill=BL)
        elif pose == 'cover': pass
        else:
            for sd in (-1, 1): _e(d, *P(sd * 18 * fat, -8), 15 * U, 9 * U, fill=BL)
        hx, hy = 0, -142
    # голова
    hw = 50 * (1.18 if kind == 'kot' else 1.0)
    H = Image.new('RGBA', (int(170 * U), int(160 * U)), (0, 0, 0, 0)); h = ImageDraw.Draw(H); h._lidcol = B
    Q = lambda x, y: (85 * U + x * U, 92 * U + y * U)
    for sd in (-1, 1):
        h.polygon([Q(sd * hw * 0.32, -34), Q(sd * hw * 0.95, -62), Q(sd * hw * 0.86, -8)], fill=B)
        h.polygon([Q(sd * hw * 0.48, -32), Q(sd * hw * 0.86, -50), Q(sd * hw * 0.8, -18)], fill=PINKN if kind == 'cat' else BD)
    _e(h, *Q(0, 0), hw * U, 40 * U, fill=B)
    _e(h, *Q(0, 16), hw * 0.5 * U, 18 * U, fill=BL)
    if kind == 'kot':   # полоски на лбу
        for x in (-10, 0, 10): h.line([Q(x, -38), Q(x * 0.7, -24)], fill=BD, width=max(2, int(4 * U)))
    _eyes(h, [Q(-hw * 0.38, -6)[0], Q(hw * 0.38, -6)[0]], Q(0, -6)[1], 9 * U, eyes, look, 0, slit=True)
    h.polygon([Q(-6, 8), Q(6, 8), Q(0, 14)], fill=PINKN)
    _mouth(h, *Q(0, 17), 20 * U, mo, mouth)
    for sd in (-1, 1):
        for j in (-1, 0, 1): h.line([Q(sd * hw * 0.35, 14 + j * 5), Q(sd * hw * 1.05, 10 + j * 9)], fill=BD, width=max(1, int(2 * U)))
    if kind == 'cat':   # розовый бант
        bx, by = Q(hw * 0.55, -36)
        h.polygon([(bx, by), (bx - 22 * U, by - 14 * U), (bx - 22 * U, by + 14 * U)], fill=BOW); h.polygon([(bx, by), (bx + 22 * U, by - 14 * U), (bx + 22 * U, by + 14 * U)], fill=BOW)
        _e(h, bx, by, 7 * U, 7 * U, fill=(220, 50, 110))
    if pose == 'cover':
        for sd in (-1, 1): _e(h, *Q(sd * hw * 0.38, -4), 18 * U, 14 * U, fill=B, outline=BD, width=max(2, int(3 * U)))
    im.alpha_composite(H, (int(P(hx, hy)[0] - 85 * U), int(P(hx, hy)[1] - 92 * U)))
    return im.resize((Wd // SS, Hd // SS), Image.LANCZOS), ox / SS, oy / SS

CAT_SPAN = json.load(open(os.path.join(HERE, 'cat_span.json')))['cat']
def kot_loud(t): return loud(t) if CAT_SPAN[0] - 0.05 <= t <= CAT_SPAN[1] + 0.05 else 0
def feline(C, t, kind, cx, feet=FEET, s=300, pose='sit', eyes='n', mo=None, mouth='smile', look=(0, 0), sway=1.0, shadow=True, rot=0):
    seed = 2 if kind == 'cat' else 3
    e = 'closed' if (eyes in ('n',) and blink(t, seed)) else eyes
    if mo is None: mo = int(round(kot_loud(t) * 5)) if (kind == 'kot' and kot_loud(t) > 0.12) else 0
    tp = int((s_(t * (5 if kind == 'cat' else 2.2)) * 0.5 + 0.5) * 7)
    im, ox, oy = cat_img(int(s), kind, pose, e, mo, tp, mouth, look)
    br = 1 + 0.015 * s_(t * (3.2 if kind == 'cat' else 1.6)) * sway
    if br != 1: im = im.resize((im.width, max(1, int(im.height * br))), Image.BILINEAR); oy *= br
    if rot: im = im.rotate(rot, Image.BICUBIC, center=(ox, oy))
    if shadow: _shadow(C, cx, feet, s * (0.55 if pose == 'loaf' else 0.36) * (1.35 if kind == 'kot' else 1))
    C.alpha_composite(im, (int(cx - ox), int(feet - oy)))
def cat(C, t, cx, feet=FEET, s=300, **k): feline(C, t, 'cat', cx, feet, s, **k)
def kot(C, t, cx, feet=FEET, s=300, **k): k.setdefault('eyes', 'half'); k.setdefault('mouth', 'smug'); feline(C, t, 'kot', cx, feet, s, **k)

if __name__ == '__main__':
    C = Image.new('RGBA', (1080, 1920), CARD + (255,))
    dog(C, 0.5, 260, 600, 320); dog(C, 0.5, 760, 600, 320, 'sniff', mouth='flat')
    dog(C, 0.5, 260, 1000, 320, 'point', eyes='shock', mouth='o'); dog(C, 0.5, 760, 1000, 320, 'cover')
    cat(C, 0.5, 200, 1400, 300); cat(C, 0.5, 540, 1400, 300, eyes='happy'); kot(C, 0.5, 860, 1400, 300)
    kot(C, 0.5, 250, 1850, 300, pose='loaf'); kot(C, 0.5, 600, 1850, 280, pose='stretch', eyes='closed', mo=4); kot(C, 0.5, 880, 1850, 260, pose='cape')
    C.convert('RGB').save('zveri_test.png'); print('ok')
