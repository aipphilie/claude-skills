"""Предметы рилса «Автокредит: как отдать банку на миллион меньше»: машина, кредитный договор, заявление, табличка ставки, столбики платежа."""
from scenes_sv import *
CARB = (214, 222, 232); CARD2 = (176, 188, 204); GLASSC = (190, 214, 236); GRN = (52, 168, 92); GRND = (30, 120, 64)

def layer(): return Image.new('RGBA', (CW, CH), (0, 0, 0, 0))

@lru_cache(16)
def car_img(s, col=CARB, ghost=False):
    w, h = int(620 * s), int(270 * s); im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0 = 20, 20; L = max(5, int(10 * s)); body_y = y0 + h * 0.42; base = y0 + h * 0.82
    fill = (0, 0, 0, 0) if ghost else col; ol = (150, 150, 150) if ghost else INK
    # кузов
    body = [(x0, base), (x0, body_y + h * 0.08), (x0 + w * 0.06, body_y), (x0 + w * 0.24, body_y - h * 0.02), (x0 + w * 0.36, y0 + h * 0.06),
            (x0 + w * 0.68, y0 + h * 0.06), (x0 + w * 0.82, body_y - h * 0.02), (x0 + w * 0.97, body_y + h * 0.06), (x0 + w, base - h * 0.06), (x0 + w, base)]
    d.polygon(body, fill=fill); d.line(body + [body[0]], fill=ol, width=L, joint='curve')
    if not ghost:
        d.polygon([(x0 + w * 0.39, y0 + h * 0.13), (x0 + w * 0.51, y0 + h * 0.13), (x0 + w * 0.51, body_y - h * 0.04), (x0 + w * 0.29, body_y - h * 0.04)], fill=GLASSC, outline=INK)
        d.polygon([(x0 + w * 0.54, y0 + h * 0.13), (x0 + w * 0.66, y0 + h * 0.13), (x0 + w * 0.77, body_y - h * 0.04), (x0 + w * 0.54, body_y - h * 0.04)], fill=GLASSC, outline=INK)
        d.line([x0 + w * 0.52, y0 + h * 0.1, x0 + w * 0.52, base - h * 0.04], fill=INK, width=max(3, L // 2))
        d.line([x0 + w * 0.03, body_y + h * 0.2, x0 + w * 0.97, body_y + h * 0.2], fill=CARD2, width=max(4, int(L * 0.8)))
        d.rounded_rectangle([x0 + w * 0.9, body_y + h * 0.06, x0 + w * 0.99, body_y + h * 0.15], radius=4, fill=YEL, outline=INK, width=max(2, L // 3))
        d.rounded_rectangle([x0 + w * 0.0, body_y + h * 0.08, x0 + w * 0.05, body_y + h * 0.17], radius=4, fill=RED, outline=INK, width=max(2, L // 3))
    else:
        for j in range(0, w, int(40 * s)): d.line([x0 + j, base + 4, x0 + j + 20 * s, base + 4], fill=ol, width=L)
    for xx in (0.21, 0.79):
        r = h * 0.2; cx = x0 + w * xx; cy = base
        if ghost: d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ol, width=L)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK); d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=MID, outline=INK, width=max(2, L // 2))
    return im
def car(C, cx, by, s=1.0, rot=0, alpha=1.0, ghost=False, bump=0.0, scale=1.0):
    im = car_img(round(s, 2), CARB, ghost); put(C, im, cx, by - im.height / 2 + 20 + 30 * s * 0.27 - bump, scale, rot, alpha)

def doc(C, cx, cy, w=520, rows=(), hl=(), title='КРЕДИТНЫЙ\nДОГОВОР', k=1.0, rot=-3, strike_=(), sk=1.0):
    """лист договора: rows — строки текста (или '' — серая линия), hl — подсвеченные индексы (красная рамка)"""
    if k <= 0: return
    h = int(w * 1.32); im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([8, 8, w + 8, h + 8], fill=WHITE, outline=INK, width=8)
    t = text_img(title, int(w * 0.075), INK); im.alpha_composite(t, ((w + 16 - t.width) // 2, int(w * 0.07)))
    y = int(w * 0.07) + t.height + int(w * 0.06); lh = int(w * 0.11)
    for j in range(7):
        r = rows[j] if j < len(rows) else ''
        if r:
            if j in hl: d.rounded_rectangle([w * 0.06, y - 6, w * 0.96, y + lh - 14], radius=8, fill=(255, 236, 236), outline=RED, width=6)
            tt = text_img(r, int(w * 0.055), RED if j in hl else INK); im.alpha_composite(tt, (int(w * 0.1), y + (lh - 20 - tt.height) // 2))
            if j in strike_: d.line([w * 0.08, y + lh / 2 - 10, w * 0.08 + (w * 0.86) * clamp(sk), y + lh / 2 - 10], fill=INK, width=8)
        else:
            d.line([w * 0.1, y + lh / 2 - 10, w * 0.9, y + lh / 2 - 10], fill=LG, width=8)
        y += lh
    d.line([w * 0.55, h - w * 0.08, w * 0.9, h - w * 0.08], fill=INK, width=4)
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1, rot)

def calc(C, cx, cy, rows, total=None, k=1.0, rot=2, w=640):
    """карточка-расчёт: строки (имя, значение), итог красным"""
    if k <= 0: return
    h = 120 + 92 * len(rows) + (130 if total else 0); im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, w + 8, h + 8], radius=26, fill=WHITE, outline=INK, width=8)
    d.rounded_rectangle([8, 8, w + 8, 100], radius=26, fill=INK); d.rectangle([8, 60, w + 8, 100], fill=INK)
    t = text_img('АВТОКРЕДИТ', 52, YEL); im.alpha_composite(t, ((w + 16 - t.width) // 2, 28))
    y = 124
    for a, b in rows:
        ta = text_img(a, 44, GREY); im.alpha_composite(ta, (40, y + 10)); tb = text_img(b, 56, INK); im.alpha_composite(tb, (w - 24 - tb.width, y + 2)); y += 92
    if total:
        d.line([30, y + 6, w - 14, y + 6], fill=INK, width=5); tt = plate_img(total, 64, RED, WHITE, pad=14, r=10); im.alpha_composite(tt, ((w + 16 - tt.width) // 2, y + 22))
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1, rot)

def form(C, cx, cy, ticks=(False, False), k=1.0, tk=(1.0, 1.0), rot=-2, w=600):
    """заявление на досрочное погашение: два квадрата-галочки"""
    if k <= 0: return
    h = 560; im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([8, 8, w + 8, h + 8], fill=WHITE, outline=INK, width=8)
    t = text_img('ЗАЯВЛЕНИЕ', 60, INK); im.alpha_composite(t, ((w + 16 - t.width) // 2, 34))
    t = text_img('на досрочное погашение', 34, GREY); im.alpha_composite(t, ((w + 16 - t.width) // 2, 110))
    for j, lab in enumerate(('УМЕНЬШИТЬ СРОК', 'УМЕНЬШИТЬ ПЛАТЁЖ')):
        y = 200 + j * 130; d.rounded_rectangle([44, y, 124, y + 80], radius=10, fill=WHITE, outline=INK, width=8)
        if ticks[j] and tk[j] > 0:
            pts = [(58, y + 40), (80, y + 64), (118, y + 14)]; q = clamp(tk[j])
            seg = pts[:2] if q < 0.5 else pts
            if q < 0.5: seg = [pts[0], (lerp(pts[0][0], pts[1][0], q * 2), lerp(pts[0][1], pts[1][1], q * 2))]
            else: seg = [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], (q - 0.5) * 2), lerp(pts[1][1], pts[2][1], (q - 0.5) * 2))]
            d.line(seg, fill=GRN, width=16, joint='curve')
        tt = text_img(lab, 50, INK if j == 0 or not ticks[0] else GREY); im.alpha_composite(tt, (150, y + 8))
    d.line([w * 0.5, h - 50, w * 0.9, h - 50], fill=INK, width=4)
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1, rot)

def ratesign(C, cx, cy, val, col=RED, k=1.0, rot=0, arrow_=0):
    """табличка ставки с колышком; arrow_: +1 вверх красная, -1 вниз зелёная"""
    if k <= 0: return
    im = plate_img(val, 120, col, WHITE, pad=30, r=20, border=INK, bw=8); put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1, rot)
    if arrow_:
        x = cx + im.width / 2 + 70; a = 1 if arrow_ > 0 else -1; d = D(C); c = RED if a > 0 else GRN
        d.line([x, cy + 80 * a, x, cy - 80 * a], fill=c, width=26); d.polygon([(x - 50, cy - 50 * a), (x + 50, cy - 50 * a), (x, cy - 120 * a)], fill=c)

def stackbar(C, cx, by, h, parts, w=200, k=1.0):
    """столбик платежа снизу вверх: parts = [(доля, цвет, подпись, бок), ...]"""
    d = D(C); y = by
    d.rounded_rectangle([cx - w / 2, by - h, cx + w / 2, by], radius=12, fill=WHITE, outline=INK, width=8)
    for frac, col, lab, side in parts:
        hh = h * frac * clamp(k)
        if hh < 2: continue
        d.rectangle([cx - w / 2 + 6, y - hh, cx + w / 2 - 6, y - 6 if y == by else y], fill=col);
        if lab: put(C, text_img(lab, 44, WHITE), cx, y - hh / 2)
        y -= hh
    d.rounded_rectangle([cx - w / 2, by - h, cx + w / 2, by], radius=12, outline=INK, width=8)

def debtplate(C, cx, cy, val, k=1.0, rot=4, top='ДОЛГ'):
    if k <= 0: return
    t1 = text_img(top, 40, WHITE); t2 = text_img(val, 84, WHITE); w = max(t1.width, t2.width) + 60; h = t1.height + t2.height + 50
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill=RED, outline=INK, width=6)
    im.alpha_composite(t1, ((w - t1.width) // 2, 16)); im.alpha_composite(t2, ((w - t2.width) // 2, 26 + t1.height))
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1, rot)

def ptag(C, cx, cy, name, price, rot=0, col=YEL, scale=1.0, fg=INK):
    """ценник с автошириной"""
    if scale <= 0.02: return
    t1 = text_img(name, 40, fg); t2 = text_img(price, 84, fg); h = t1.height + t2.height + 46; w = max(t1.width, t2.width) + 60 + int(h * 0.45)
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); n = h * 0.45
    d.polygon([(5, 5 + h / 2), (5 + n, 5), (w + 5, 5), (w + 5, h + 5), (5 + n, h + 5)], fill=col, outline=INK, width=7)
    d.ellipse([n * 0.55 - 12, h / 2 - 7, n * 0.55 + 12, h / 2 + 17], fill=CARD, outline=INK, width=5)
    im.alpha_composite(t1, (int(n + 20), 16)); im.alpha_composite(t2, (int(n + 20), 22 + t1.height))
    put(C, im, cx, cy, scale, rot)
