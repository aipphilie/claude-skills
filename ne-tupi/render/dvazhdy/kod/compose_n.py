"""Монтаж «Никогда не пропускай дважды» — один в один по присланному рилсу, но в стиле «Не тупи»:
календарь-трекер на месяц (жёлтая закраска, белые крестики), коллаж-карточки «мелко + КРУПНО», триптих, штамп, цепь, кубок.
Общие функции (текст, плашки, штамп, человечки, субтитры) берутся из compose_k.py (рилс «Листок на 66 тысяч»)."""
import sys, os, math, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.append(os.environ.get('KAL', '../kal'))
import compose_k as ck
from compose_k import (Image, ImageDraw, np, font, clamp, back, eo, eio, text_img, put, typed, title, plate, stamp, card_bg, bg_room,
                       chalk, shade, place, sprite, tips, WD, HT, FPS, FEET, BG, YEL, RED, INK, WHITE, GREY, LG, L1, L2, BOARD, MID)
from words import W, B, END, DUR
from tm import T
N = int(DUR * FPS)
ONLY = sys.argv[1:]
def line_of(t): return max(j for j in range(len(B)) if B[j] <= t)

# субтитры: числа цифрами
ck.NUMS = [(['двадцать', 'килограммов,'], '20 КГ,'), (['десять', 'раз.'], '10 РАЗ.'), (['два', 'дня'], '2 ДНЯ'), (['шесть', 'пропусков.'], '6 ПРОПУСКОВ.'),
           (['два', 'подряд'], '2 ПОДРЯД')]
ck.WS = ck.merge_nums(ck.W)
groups, cur = [], []
for w in ck.WS:
    if cur and (len(ck.wrap(cur + [w])) > 2 or len(cur) >= 6): groups.append(cur); cur = []
    cur.append(w)
    if w[0].rstrip('»')[-1] in '.!?' or (w[0][-1] in ',:—' and len(cur) >= 3): groups.append(cur); cur = []
if cur: groups.append(cur)
ck.groups = groups

# ---------- календарь на месяц (как в оригинале: ПН…ВС, 31 кружок) ----------
DAYS = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
def mgeom(cell, anchor):
    pad = cell * 0.5; head = cell * 0.95
    d, px, py = anchor; c = (d - 1) % 7; r = (d - 1) // 7
    return px - pad - (c + 0.5) * cell, py - head - (r + 0.5) * cell, pad, head
def mcenter(d, bx0, by0, pad, head, cell):
    return bx0 + pad + ((d - 1) % 7 + 0.5) * cell, by0 + head + ((d - 1) // 7 + 0.5) * cell
def chalk_x(d, x, y, r, k, col=WHITE, w=None):
    """Крестик мелом: два штриха по очереди."""
    w = w or max(3, int(r * 0.16))
    k1 = clamp(k * 2); k2 = clamp(k * 2 - 1); a = r * 0.55
    if k1 > 0: d.line([x - a, y - a, x - a + 2 * a * k1, y - a + 2 * a * k1], fill=col, width=w)
    if k2 > 0: d.line([x + a, y - a, x + a - 2 * a * k2, y - a + 2 * a * k2], fill=col, width=w)
def draw_month(img, cell, anchor, state, t, pulse=None):
    """state(d, t) -> (вид, прогресс): 'f' закраска, 'x' крестик."""
    d = ImageDraw.Draw(img)
    bx0, by0, pad, head = mgeom(cell, anchor)
    bw = 7 * cell + pad * 2; bh = 5 * cell + pad * 2 + head
    if cell < 180: d.rounded_rectangle([bx0 - cell * 0.25, by0 - cell * 0.25, bx0 + bw + cell * 0.25, by0 + bh + cell * 0.25], radius=cell * 0.3, fill=WHITE)   # белое поле листа
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=cell * 0.2, fill=BOARD)
    fh = font(int(cell * 0.3))
    for c, dn in enumerate(DAYS):
        d.text((bx0 + pad + (c + 0.5) * cell, by0 + head * 0.6), dn, font=fh, fill=WHITE, anchor='mm')
    r = cell * 0.36
    for day in range(1, 32):
        x, y = mcenter(day, bx0, by0, pad, head, cell)
        if x < -cell or x > WD + cell or y < -cell or y > HT + cell: continue
        kind, k = state(day, t)
        col = RED if pulse and pulse(day, t) else WHITE
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=max(2, int(cell * (0.035 if col == WHITE else 0.07))))
        if kind == 'f' and k > 0.02:
            s = int(2 * r * 0.98 * back(k))
            if s > 1: img.alpha_composite(chalk(s), (int(x - s / 2), int(y - s / 2)))
        elif kind == 'x' and k > 0: chalk_x(d, x, y, r, k)
    return bx0, by0, pad, head
def st(fills=(), xs=(), base_f=(), base_x=()):
    """fills/xs: {день: момент}; base_*: уже стоят."""
    fills = dict(fills); xs = dict(xs)
    def f(day, t):
        if day in base_f: return ('f', 1)
        if day in base_x: return ('x', 1)
        if day in fills: return ('f', clamp((t - fills[day]) / 0.25))
        if day in xs: return ('x', clamp((t - xs[day]) / 0.35))
        return ('', 0)
    return f
INTRO_X = {5, 11, 16, 22, 29}
MONTH_X = {3, 8, 13, 19, 24, 29}   # 6 пропусков, ни разу два подряд

def month_scene(img, i, t, cell, day, state, cx=790, s=0.5, pulse=None, dark=True, centered=False):
    """Календарь крупно, человечек справа «работает» кончиком левой руки у кружка day.
    centered: лист целиком по центру, человечек справа подходит рукой к кружку day."""
    if dark: img.paste(BOARD, [0, 0, WD, HT])
    if centered:
        img.paste(BG, [0, 0, WD, HT])
        g = draw_month(img, cell, (18, 540, 975), state, t, pulse)
        tx, ty = mcenter(day, *g, cell)
        left, _ = tips('main', int(round(B[line_of(t)] * FPS)) + 2, s, 0)
        cx = tx + cell * 0.15 - left[0]
        cx = max(cx, 560)
        place(img, 'main', i, cx, s, feet=FEET + (ty - left[1]) if False else FEET)
        return
    left, _ = tips('main', int(round(B[line_of(t)] * FPS)) + 2, s, cx)
    draw_month(img, cell, (day, left[0] - cell * 0.15, left[1]), state, t, pulse)
    place(img, 'main', i, cx, s)

# ---------- предметы ----------
def money_stack(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img)
    for j in range(7):
        y = by - j * 34 * k; w = 300 * k; off = (j % 2) * 14 * k - 7 * k
        d.rounded_rectangle([cx - w / 2 + off, y - 40 * k, cx + w / 2 + off, y], radius=8, fill=YEL, outline=INK, width=5)
    d.text((cx, by - 7 * 34 * k + 6 * k), '₽', font=font(int(70 * k)), fill=INK, anchor='mb')
def scales(img, cx, by, k=1.0, kg='57'):
    d = ImageDraw.Draw(img); w = 280 * k; h = 70 * k
    d.rounded_rectangle([cx - w / 2, by - h, cx + w / 2, by], radius=22 * k, fill=(60, 60, 64), outline=INK, width=5)
    d.ellipse([cx - 70 * k, by - h - 110 * k, cx + 70 * k, by - h + 30 * k], fill=WHITE, outline=INK, width=6)
    d.text((cx, by - h - 40 * k), kg + ' КГ', font=font(int(34 * k)), fill=INK, anchor='mm')
    d.line([cx, by - h - 40 * k, cx + 40 * k, by - h - 80 * k], fill=RED, width=5)
def bigben(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img); w = 110 * k
    d.rectangle([cx - w / 2, by - 420 * k, cx + w / 2, by], fill=(200, 196, 188), outline=INK, width=5)
    d.rectangle([cx - w / 2 - 12 * k, by - 520 * k, cx + w / 2 + 12 * k, by - 400 * k], fill=(200, 196, 188), outline=INK, width=5)
    d.ellipse([cx - 42 * k, by - 502 * k, cx + 42 * k, by - 418 * k], fill=WHITE, outline=INK, width=5)
    d.line([cx, by - 460 * k, cx, by - 490 * k], fill=INK, width=4); d.line([cx, by - 460 * k, cx + 22 * k, by - 460 * k], fill=INK, width=4)
    d.polygon([(cx - w / 2 - 12 * k, by - 520 * k), (cx, by - 700 * k), (cx + w / 2 + 12 * k, by - 520 * k)], fill=INK)
    for j in range(5): d.line([cx - w / 2 + 14 * k, by - 380 * k + j * 70 * k, cx + w / 2 - 14 * k, by - 380 * k + j * 70 * k], fill=INK, width=3)
def book(img, cx, cy, k=1.0, rot=0):
    w, h = int(330 * k), int(470 * k)
    im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([14, 14, w + 14, h + 14], fill=(190, 186, 178))
    d.rectangle([0, 0, w, h], fill=WHITE, outline=INK, width=6)
    d.rectangle([0, 0, int(26 * k), h], fill=YEL, outline=INK, width=4)
    d.text((w / 2 + 12 * k, h * 0.33), 'АТОМНЫЕ\nПРИВЫЧКИ', font=font(int(46 * k)), fill=INK, anchor='mm', align='center')
    d.text((w / 2 + 12 * k, h * 0.82), 'ДЖЕЙМС КЛИР', font=font(int(26 * k)), fill=GREY, anchor='mm')
    put(img, im, cx, cy, 'mm', 1.0, rot)
def chain(img, x0, x1, y, t, brk=0.0):
    """Цепь между руками; brk>0 — рвётся посередине, звенья разлетаются."""
    d = ImageDraw.Draw(img); n = 9; mid = (x0 + x1) / 2
    for j in range(n):
        u = j / (n - 1); x = x0 + (x1 - x0) * u; yy = y + 30 * math.sin(u * math.pi)
        if brk > 0:
            side = -1 if x < mid else 1; dist = 1 - abs(x - mid) / ((x1 - x0) / 2)
            x += side * brk * 220 * dist; yy += brk * brk * 500 * dist - 120 * brk * dist
            if j == n // 2: continue
        w, h = (46, 30) if j % 2 else (30, 46)
        d.ellipse([x - w, yy - h, x + w, yy + h], outline=WHITE, width=22); d.ellipse([x - w, yy - h, x + w, yy + h], outline=INK, width=12)
    if brk > 0:
        rr = random.Random(2)
        for q in range(10):
            a = rr.uniform(0, 6.28); r = brk * rr.uniform(80, 260)
            d.line([mid + math.cos(a) * r * 0.6, y + math.sin(a) * r * 0.6, mid + math.cos(a) * r, y + math.sin(a) * r], fill=INK, width=6)
def trophy(img, cx, by, k=1.0):
    d = ImageDraw.Draw(img)
    d.rectangle([cx - 110 * k, by - 50 * k, cx + 110 * k, by], fill=INK)
    d.rectangle([cx - 30 * k, by - 130 * k, cx + 30 * k, by - 50 * k], fill=YEL, outline=INK, width=5)
    for s in (-1, 1): d.arc([cx + s * 150 * k - 70 * k, by - 380 * k, cx + s * 150 * k + 70 * k, by - 240 * k], 0, 360, fill=INK, width=int(18 * k))
    d.chord([cx - 160 * k, by - 460 * k, cx + 160 * k, by - 120 * k], 0, 180, fill=YEL, outline=INK, width=6)
    d.rectangle([cx - 160 * k, by - 400 * k, cx + 160 * k, by - 290 * k], fill=YEL, outline=INK, width=6)
    d.rectangle([cx - 154 * k, by - 300 * k, cx + 154 * k, by - 285 * k], fill=YEL)
    d.polygon([(cx - 60 * k, by - 380 * k), (cx - 30 * k, by - 380 * k), (cx - 50 * k, by - 200 * k), (cx - 75 * k, by - 210 * k)], fill=(255, 240, 160))
def grey_person(img, cx, feet, h, col=MID):
    d = ImageDraw.Draw(img); w = h * 0.24; hr = h * 0.13; top = feet - h * 0.78
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, feet], radius=w / 2, fill=col)
    d.line([cx, feet - h * 0.38, cx, feet], fill=BG, width=max(2, int(h * 0.02)))
    d.ellipse([cx - hr, top - hr * 2.05, cx + hr, top - hr * 0.05], fill=col)
def bg_city(img, night=False):
    d = ImageDraw.Draw(img)
    for x, w, h in ((-20, 170, 520), (170, 140, 700), (330, 200, 430), (550, 150, 820), (720, 190, 560), (930, 170, 660)):
        d.rectangle([x, FEET - h, x + w, FEET + 8], fill=L1, outline=L2, width=4)
        for r in range(int(h / 90) - 1):
            for c in range(int(w / 60)):
                d.rectangle([x + 22 + c * 55, FEET - h + 40 + r * 90, x + 46 + c * 55, FEET - h + 80 + r * 90], fill=YEL if (r * 3 + c * 5 + x) % 7 == 0 else BG)
    d.line([0, FEET + 8, WD, FEET + 8], fill=L2, width=5)

# ---------- эффекты камеры ----------
def zoom_of(t):
    for ta, dur, amp in ((T['tysyacham'], 0.6, 0.06), (T['nelzya'], 0.7, 0.07), (T['nikogda'], 0.7, 0.06), (T['razrushena'], 0.8, 0.07), (T['ni'], 0.6, 0.06), (T['smog'], 0.7, 0.06)):
        if ta <= t < ta + dur: return 1 + amp * (1 - eo((t - ta) / dur))
    return 1.0
def shake(t):
    for ta in (T['obyasnyaet'] + 0.15, T['razrushena'], T['nelzya']):
        if ta <= t < ta + 0.25: u = (t - ta) / 0.25; return int(14 * (1 - u) * math.sin(t * 160)), int(10 * (1 - u) * math.cos(t * 140))
    return 0, 0

def frame(i):
    t = i / FPS; L = line_of(t)
    img = Image.new('RGBA', (WD, HT), BG + (255,))
    if L == 0:   # почти полный месяц с крестиками, как первый кадр оригинала
        month_scene(img, i, t, 150, 18, st(base_f=set(range(1, 32)) - INTRO_X - {18}, base_x=INTRO_X, fills={18: 0.3}))
        shade(img)
        title(img, t, 0.0, 'ПРОСТОЕ ПРАВИЛО', 'УСПЕХА', fg=WHITE, y=262)
    elif L == 1:   # «помогло ТЫСЯЧАМ людей»
        bg_city(img)
        for j in range(26):
            k = back((t - B[1] - 0.025 * j) / 0.3)
            if k > 0.1:
                rr = random.Random(j); x = rr.randint(60, 1020); f = FEET - rr.randint(0, 60)
                if abs(x - 540) > 90: grey_person(img, x, f, rr.randint(220, 330) * k)
        place(img, 'main', i, 540, 0.42)
        title(img, t, B[1], 'ПОМОГЛО', 'ТЫСЯЧАМ', typing=True)
    elif L in (2, 3, 4):
        img.alpha_composite(card_bg())
        _, top = tips('main', i, 0.46, 540); k = back((t - B[L]) / 0.3)
        if L == 2:
            title(img, t, B[2], 'ЗАРАБОТАТЬ ПЕРВЫЙ', 'МИЛЛИОН')
            place(img, 'main', i, 540, 0.46)
            if k > 0.05: money_stack(img, top[0], top[1] + 20, k)
        elif L == 3:
            title(img, t, B[3], 'СБРОСИТЬ', '20 КГ', bsz=230)
            place(img, 'main', i, 540, 0.46)
            if k > 0.05: scales(img, top[0], top[1] + 15, 1.1 * k)
        else:
            title(img, t, B[4], 'ВЫУЧИТЬ', 'АНГЛИЙСКИЙ', bsz=170)
            place(img, 'main', i, 540, 0.46)
            if k > 0.05: bigben(img, top[0], top[1] + 15, 0.45 * k)
    elif L == 5:   # триптих «бросали всё на полпути»
        img.paste(WHITE, [0, 0, WD, HT])
        bands = [(250, 625), (633, 1008), (1016, 1391)]
        starts = [B[5], B[5] + 0.12, B[5] + 0.24]
        for b, ((y0, y1), s0) in enumerate(zip(bands, starts)):
            u = eo((t - s0) / 0.25)
            if u <= 0: continue
            band = Image.new('RGBA', (WD, y1 - y0), BG + (255,)); d = ImageDraw.Draw(band); hb = y1 - y0; ft = hb - 30
            d.line([0, ft + 4, WD, ft + 4], fill=L2, width=4)
            cxs = 540
            if b == 0:
                d.rounded_rectangle([cxs - 110, ft - 30, cxs + 110, ft], radius=12, fill=(60, 60, 64))
                d.ellipse([cxs + 140, ft - 160, cxs + 260, ft - 40], fill=WHITE, outline=INK, width=5); d.text((cxs + 200, ft - 100), '+2', font=font(42), fill=RED, anchor='mm')
                fty = ft - 30
            elif b == 1:
                for q in range(12):
                    rr = random.Random(q); d.rectangle([rr.randint(60, 1000), rr.randint(20, 200), 0, 0] if False else [80 + q * 75, 40 + (q % 3) * 60, 140 + q * 75, 95 + (q % 3) * 60], fill=YEL, outline=INK, width=3)
                d.rectangle([140, ft - 150, 940, ft - 125], fill=L1, outline=L2, width=4)
                for x in (180, 900): d.line([x, ft - 125, x, ft], fill=L2, width=6)
                fty = ft
            else:
                d.rectangle([120, ft - 150, 960, ft - 125], fill=L1, outline=L2, width=4)
                for x in (160, 920): d.line([x, ft - 125, x, ft], fill=L2, width=6)
                d.polygon([(700, ft - 150), (790, ft - 175), (880, ft - 150)], fill=WHITE, outline=INK)
                fty = ft
            im = sprite(['t1', 't2', 't3'][b], i, 0.215)
            band.alpha_composite(im, (int(cxs - im.width / 2), int(fty + 70 * 0.215 - im.height)))
            img.alpha_composite(band, (int(-WD * (1 - u)) if b % 2 == 0 else int(WD * (1 - u)), y0))
        if t >= T['brosali']: plate(img, t, T['brosali'], 'БРОСАЛИ ВСЁ', 300, 470, 72, INK, WHITE, rot=-3)
        stamp(img, t, T['desyat'] - 0.05, '×10', 840, 820, rot=-12, sz=140)
    elif L == 6:   # название правила поверх календаря
        month_scene(img, i, t, 125, 4, st(fills={1: B[6] + 0.1, 2: B[6] + 0.35, 3: B[6] + 0.6, 4: B[6] + 0.85}), s=0.42, centered=True)
        title(img, t, B[6] + 0.1, 'НАЗЫВАЕТСЯ', '«НИКОГДА НЕ\nПРОПУСКАЙ ДВАЖДЫ»', y=262, bsz=88)
    elif L in (7, 9, 10):
        base_f = {1, 2, 3, 4}
        stt = st(base_f=base_f, xs={5: T['propustil'] + 0.2}, fills={6: T['normalno'] + 0.1, 7: T['normalno'] + 0.35}) if L == 7 else \
            st(base_f=base_f | {6, 7}, base_x={5}, xs={8: T['dva'] + 0.1, 9: T['dva'] + 0.45})
        pulse = (lambda d, tt: d in (8, 9) and tt >= T['nelzya'] - 0.1 and int(tt * 6) % 2 == 0) if L >= 9 else None
        month_scene(img, i, t, 125, 5 if L == 7 else 9, stt, pulse=pulse, s=0.42, centered=True)
        if L == 7:
            title(img, t, B[7], 'ПРОПУСТИЛ ОДИН ДЕНЬ?', 'НОРМАЛЬНО' if t >= T['normalno'] - 0.1 else '', y=262, bsz=170)
        elif L == 9:
            title(img, t, B[9], 'НО 2 ДНЯ ПОДРЯД', 'НЕЛЬЗЯ' if t >= T['nelzya'] - 0.1 else '', fg=RED, small_fg=INK, y=262, bsz=200)
        else:
            title(img, t, B[10], 'ПРОПУСКАТЬ 2 ДНЯ', 'НИКОГДА', fg=INK, y=262, bsz=200, typing=False)
            plate(img, t, T['pochemu'] - 0.1, 'ПОЧЕМУ?', 360, 760, 84, YEL, INK, rot=-4)
    elif L == 8:   # крестик крупно: «БЫВАЕТ»
        img.paste(BOARD, [0, 0, WD, HT])
        draw_month(img, 330, (5, 480, 900), st(base_f={1, 2, 3, 4, 6, 7}, base_x={5}), t)
        plate(img, t, B[8] + 0.05, 'БЫВАЕТ', 540, 1240, 100, WHITE, INK, rot=-3)
    elif L == 11:   # авторитет: книга + штамп
        img.alpha_composite(card_bg())
        title(img, t, B[11], 'АВТОР КНИГИ', 'ДЖЕЙМС КЛИР' if t >= T['klir'] - 0.1 else '', bsz=150)
        k = eo((t - T['atomnye'] + 0.3) / 0.35)
        if k > 0: book(img, 420 - 500 * (1 - k), 900, 1.0, -6 + 30 * (1 - k))
        place(img, 'main', i, 820, 0.36)
        stamp(img, t, T['obyasnyaet'] + 0.1, 'ОБЪЯСНИЛ', 440, 900, rot=18, sz=100)
    elif L in (12, 13):   # крестики крупно
        img.paste(BOARD, [0, 0, WD, HT])
        if L == 12:
            draw_month(img, 300, (5, 540, 860), st(base_f={1, 2, 3, 4, 6, 7}, base_x={5}), t)
            title(img, t, B[12], 'ДЛЯ МОЗГА ОДИН РАЗ —', 'СЛУЧАЙНОСТЬ' if t >= T['sluchaynost'] - 0.1 else '', fg=WHITE, y=262, bsz=150, typing=False)
        else:
            draw_month(img, 280, (8, 400, 1000), st(base_f={1, 2, 3, 4, 6, 7}, base_x={5, 8, 9}), t, pulse=lambda d, tt: d in (8, 9) and int(tt * 5) % 2 == 0)
            title(img, t, B[13], 'А ДВАЖДЫ —', 'НОВАЯ НОРМА' if t >= T['norma'] - 0.2 else '', fg=YEL, small_fg=WHITE, y=262, bsz=160, typing=False)
    elif L == 14:   # «ПРИВЫЧКА РАЗРУШЕНА» — цепь рвётся
        img.alpha_composite(card_bg())
        title(img, t, B[14], 'ПРИВЫЧКА', 'РАЗРУШЕНА' if t >= T['razrushena'] - 0.05 else '', typing=False)
        x0, y0, im = place(img, 'main', i, 540, 0.46)
        bb = im.getbbox(); yh = y0 + bb[1] + 30
        chain(img, x0 + bb[0] + 20, x0 + bb[2] - 20, yh, t, clamp((t - T['razrushena'] + 0.05) / 0.6))
    elif L in (15, 16):   # месяц целиком: 6 пропусков, ни разу два подряд
        img.paste(BG, [0, 0, WD, HT])
        fills = {d: B[15] + 0.05 + d * 0.03 for d in range(1, 32) if d not in MONTH_X}
        xs = {d: B[15] + 0.05 + d * 0.03 for d in MONTH_X}
        pulse = (lambda d, tt: d in MONTH_X and int(tt * 6) % 2 == 0) if L == 16 else None
        draw_month(img, 125, (18, 520, 900), st(fills=fills, xs=xs), t, pulse)
        if L == 15: plate(img, t, T['shest'] - 0.1, 'ЗА МЕСЯЦ — 6 ПРОПУСКОВ', 520, 330, 74, INK, WHITE, rot=-2)
        else:
            plate(img, t, B[16], '2 ПОДРЯД —', 380, 300, 74, INK, WHITE, rot=-2)
            plate(img, t, T['ni'] - 0.1, 'НИ РАЗУ', 680, 430, 96, YEL, INK, rot=3)
        place(img, 'main', i, 900, 0.3)
    elif L == 17:   # «так добиваются своего»
        bg_city(img)
        place(img, 'main', i, 540, 0.44)
        title(img, t, B[17], 'ИМЕННО ТАК', 'ДОБИВАЮТСЯ', bsz=170)
        plate(img, t, T['poluchilos'] - 0.1, 'ТЕ, У КОГО ПОЛУЧИЛОСЬ', 540, 690, 64, YEL, INK, rot=-2)
    elif L == 18:   # «возвращаются на следующий день»
        stt = st(base_f={15, 16, 17, 18}, base_x={19}, fills={20: T['vozvrashchayutsya'] + 0.3})
        month_scene(img, i, t, 190, 20, stt)
        shade(img)
        if t < T['vozvrashchayutsya'] - 0.2: title(img, t, B[18], 'ОНИ НЕ', 'ИДЕАЛЬНЫЕ', fg=WHITE, y=262, bsz=170)
        else: title(img, t, T['vozvrashchayutsya'] - 0.2, 'ОНИ ВОЗВРАЩАЮТСЯ', 'НА СЛЕДУЮЩИЙ ДЕНЬ', fg=YEL, small_fg=WHITE, y=262, bsz=96, typing=True)
    else:   # финальная карточка с кубком + «Всё. Не тупи.»
        img.alpha_composite(card_bg())
        d = ImageDraw.Draw(img)
        for q in range(16):
            a = q * math.pi / 8 + t * 0.6
            d.polygon([(540, 900), (540 + math.cos(a) * 1300, 900 + math.sin(a) * 1300), (540 + math.cos(a + 0.12) * 1300, 900 + math.sin(a + 0.12) * 1300)], fill=(232, 236, 241))
        title(img, t, B[19], 'ПРАВИЛО, КОТОРОЕ ЗНАЮТ ТЕ, КТО', 'СМОГ' if t >= T['smog'] - 0.15 else '', bsz=230, typing=False)
        _, top = tips('main', i, 0.42, 540)
        place(img, 'main', i, 540, 0.42)
        if t < END + 0.1: trophy(img, top[0], top[1] + 25, 0.8)
        if t >= T['netupi'] - 0.75: plate(img, t, T['netupi'] - 0.75, 'ВСЁ.\nНЕ ТУПИ', 540, 1150, 110, YEL, INK, rot=-4)
    ck.subs(img, t)
    img = img.convert('RGB')
    z = zoom_of(t); dx, dy = shake(t)
    if z != 1 or dx or dy:
        w, h = int(WD * z), int(HT * z); im2 = img.resize((w, h), Image.BILINEAR)
        ox, oy = int((w - WD) * 0.5) + dx, int((h - HT) * 0.47) + dy
        im3 = Image.new('RGB', (WD, HT), BG); im3.paste(im2, (-ox, -oy)); img = im3
    return img

if __name__ == '__main__':
    if ONLY:
        for s in ONLY: frame(int(float(s) * FPS)).save(f'prev_{s}.png')
    else:
        part, parts = int(os.environ.get('PART', 0)), int(os.environ.get('PARTS', 1))
        a, b = N * part // parts, N * (part + 1) // parts
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', f'part{part}.mp4' if parts > 1 else 'video_noaudio.mp4'], stdin=subprocess.PIPE)
        for i in range(a, b):
            p.stdin.write(frame(i).tobytes())
            if i % 240 == 0: print(i, flush=True)
        p.stdin.close(); p.wait()
