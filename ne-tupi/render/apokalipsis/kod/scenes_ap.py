"""Предметы и сцены рилса «Конец света 17 ноября» (по Shorts Mutabor). Движок «Двух судеб» (compose_dv.py): весь экран, белый фон."""
from props_dv import *
GOLD = (244, 190, 30); GOLDD = (186, 132, 10); SCREEN = (40, 46, 60); BTC = (247, 147, 26); BRG = (0, 156, 59); BRY = (255, 223, 0); BRB = (0, 39, 118)
GRECH = (176, 120, 70)
# ---------- персонажи ----------
def girl(C, clip, u, cx, s=0.4, feet=None, flip=False): man(C, 'g_' + clip, u, cx, feet or G, s, flip=flip)
def welder(C, clip, u, cx, s=0.4, feet=None, flip=False): man(C, 'v_' + clip, u, cx, feet or G, s, flip=flip)
def crowd2(C, u, cx, by, n=7, s=0.2, mode='shock', spread=900, seed=1):
    rnd = random.Random(seed); kinds = ['', 'g_', 'v_']
    for j in range(n):
        k = kinds[(j + seed) % 3]
        clip = {'shock': {'': 'scream', 'g_': 'g_scream', 'v_': 'v_shock'}, 'cheer': {'': 'cheer', 'g_': 'g_cheer', 'v_': 'v_cheer'}, 'idle': {'': 'idle', 'g_': 'g_idle', 'v_': 'v_idle'}}[mode][k]
        x = cx - spread / 2 + spread * (j + 0.5) / n + rnd.uniform(-14, 14)
        man(C, clip, u + j * 0.31, x, by + (j % 2) * 14, s * rnd.uniform(0.92, 1.08), flip=j % 3 == 0)
# ---------- предметы ----------
def wifi(C, cx, cy, s=1.0, col=INK, cross=0.0, ok=0.0):
    d = D(C)
    for j, r in enumerate((260, 180, 100)):
        r *= s; d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=col, width=int(44 * s))
    r = 34 * s; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    if cross > 0: xcross(C, cross, cx, cy - 120 * s, 230 * s, RED, int(34 * s))
    if ok > 0:
        k = back(ok / 0.25); r = 90 * s * k; x, y = cx + 200 * s, cy - 40 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=GREEN, outline=INK, width=8)
        if k > 0.5: d.line([x - r * 0.45, y, x - r * 0.1, y + r * 0.38, x + r * 0.5, y - r * 0.35], fill=WHITE, width=int(20 * s))
def browser(C, cx, cy, w, h, label='', inf=0.0, u=0, logo=None):
    d = D(C); x0, y0 = cx - w / 2, cy - h / 2; bar = max(30, h * 0.16)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(min(w, h) * 0.08), fill=WHITE, outline=INK, width=8)
    d.rectangle([x0 + 4, y0 + bar, x0 + w - 4, y0 + bar + 4], fill=INK)
    for j, c in enumerate((RED, YEL, GREEN)): rr = bar * 0.18; d.ellipse([x0 + bar * 0.5 + j * bar * 0.5 - rr, y0 + bar / 2 - rr, x0 + bar * 0.5 + j * bar * 0.5 + rr, y0 + bar / 2 + rr], fill=c, outline=INK, width=2)
    d.rounded_rectangle([x0 + bar * 1.9, y0 + bar * 0.25, x0 + w - bar * 0.4, y0 + bar * 0.75], radius=int(bar * 0.25), fill=LG)
    for j in range(3): d.rounded_rectangle([x0 + w * 0.1, y0 + bar + h * (0.2 + j * 0.16), x0 + w * (0.9 - 0.2 * (j % 2)), y0 + bar + h * (0.27 + j * 0.16)], radius=6, fill=LG)
    if label: put(C, text_img(label, int(h * 0.16), INK), cx, y0 + bar + h * 0.13)
    if inf > 0:
        k = clamp(inf); ov = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(min(w, h) * 0.08), fill=(228, 44, 52, int(120 * k)))
        C.alpha_composite(ov, (int(x0), int(y0)))
        if k > 0.5: put(C, plate_img('ЗАРАЖЁН', int(h * 0.12), RED, WHITE, pad=10, r=6, border=INK, bw=4), cx, cy + h * 0.22, 1, -6)
def brflag(C, cx, cy, w, u=0):
    h = w * 0.66; im = Image.new('RGBA', (int(w) + 10, int(h) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([5, 5, w + 5, h + 5], fill=BRG); d.polygon([(5 + w * 0.08, 5 + h / 2), (5 + w / 2, 5 + h * 0.1), (5 + w * 0.92, 5 + h / 2), (5 + w / 2, 5 + h * 0.9)], fill=BRY)
    d.ellipse([5 + w / 2 - h * 0.25, 5 + h * 0.25, 5 + w / 2 + h * 0.25, 5 + h * 0.75], fill=BRB); d.rectangle([5, 5, w + 5, h + 5], outline=INK, width=7)
    put(C, im, cx, cy, 1, 3 * s_(u * 4))
def post(C, cx, cy, w, k=1.0, text='', views=None):
    if k <= 0: return
    h = w * 0.62; im = Image.new('RGBA', (int(w) + 10, int(h) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([5, 5, w + 5, h + 5], radius=30, fill=WHITE, outline=INK, width=8)
    d.ellipse([35, 35, 125, 125], fill=INK); d.rounded_rectangle([145, 50, 145 + w * 0.36, 78], radius=10, fill=INK); d.rounded_rectangle([145, 92, 145 + w * 0.24, 112], radius=8, fill=MID)
    t = text_img(text, int(w * 0.075), INK); im.alpha_composite(t, (40, 150))
    if views: tv_ = plate_img(views, int(w * 0.06), LG, INK, pad=10, r=8); im.alpha_composite(tv_, (40, int(h - tv_.height - 20)))
    put(C, im, cx, cy, back(k / 0.22) if k < 0.4 else 1, -3)
def eye(C, cx, cy, s=1.0, u=0):
    d = D(C); w, h = 300 * s, 170 * s; blink = abs(s_(u * 2.2)) > 0.97
    top = [(cx - w + 2 * w * q / 40, cy - h * math.sin(math.pi * q / 40)) for q in range(41)]
    bot = [(cx + w - 2 * w * q / 40, cy + h * math.sin(math.pi * q / 40)) for q in range(41)]
    d.polygon(top + bot, fill=WHITE); 
    if not blink:
        r = h * 0.62; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK); r2 = r * 0.28; d.ellipse([cx - r * 0.45 - r2, cy - r * 0.45 - r2, cx - r * 0.45 + r2, cy - r * 0.45 + r2], fill=WHITE)
    d.line(top, fill=INK, width=int(14 * s), joint='curve'); d.line(bot + [bot[-1]], fill=INK, width=int(14 * s), joint='curve')
def magnifier(C, cx, cy, s=1.0, rot=0):
    im = Image.new('RGBA', (int(460 * s), int(460 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 170 * s; r = 130 * s
    d.line([c + r * 0.7, c + r * 0.7, 440 * s, 440 * s], fill=INK, width=int(46 * s)); d.ellipse([c - r, c - r, c + r, c + r], fill=(220, 236, 250, 200), outline=INK, width=int(26 * s))
    d.arc([c - r * 0.7, c - r * 0.7, c + r * 0.7, c + r * 0.7], 200, 250, fill=WHITE, width=int(14 * s))
    put(C, im, cx, cy, 1, rot)
def siren(C, cx, by, s=1.0, u=0, on=True):
    d = D(C); d.rectangle([cx - 14 * s, by - 620 * s, cx + 14 * s, by], fill=STEEL2, outline=INK, width=5)
    for sd in (-1, 1):
        x = cx + sd * 30 * s; y = by - 560 * s
        d.polygon([(x, y - 30 * s), (x + sd * 220 * s, y - 110 * s), (x + sd * 220 * s, y + 110 * s), (x, y + 30 * s)], fill=(200, 204, 210), outline=INK, width=7)
        d.ellipse([x + sd * 220 * s - 22 * s, y - 110 * s, x + sd * 220 * s + 22 * s, y + 110 * s], fill=STEEL2, outline=INK, width=6)
        if on:
            for j in range(3):
                rr = (60 + j * 50 + 20 * ((u * 4) % 1)) * s; xx = x + sd * 250 * s
                d.arc([xx - rr, y - rr, xx + rr, y + rr], (-45 if sd > 0 else 135), (45 if sd > 0 else 225), fill=INK, width=int(10 * s))
def tvset(C, cx, cy, w, h, screen='TEST', u=0):
    d = D(C); d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=30, fill=INK)
    sw, sh = w - 60, h - 60; x0, y0 = cx - sw / 2, cy - sh / 2; cols = [(255, 255, 255), (255, 214, 10), (0, 200, 220), (40, 190, 80), (220, 60, 200), (228, 44, 52), (40, 70, 200)]
    for j, c in enumerate(cols): d.rectangle([x0 + sw * j / 7, y0, x0 + sw * (j + 1) / 7, y0 + sh], fill=c)
    put(C, plate_img(screen, int(h * 0.16), INK, WHITE, pad=14, r=8), cx, cy)
    d.line([cx - 60, cy + h / 2, cx - 120, cy + h / 2 + 80], fill=INK, width=12); d.line([cx + 60, cy + h / 2, cx + 120, cy + h / 2 + 80], fill=INK, width=12)
def server(C, cx, by, s=1.0, label='', u=0, inf=0.0):
    d = D(C); w, h = 360 * s, 560 * s; x0 = cx - w / 2; y0 = by - h
    d.rounded_rectangle([x0, y0, x0 + w, by], radius=int(20 * s), fill=(64, 70, 82), outline=INK, width=9)
    for j in range(5):
        y = y0 + 40 * s + j * 100 * s; d.rounded_rectangle([x0 + 26 * s, y, x0 + w - 26 * s, y + 70 * s], radius=10, fill=(90, 98, 112), outline=INK, width=5)
        for q in range(3):
            on = (int(u * 8) + j + q) % 3 == 0; c = (RED if inf > 0.5 else GREEN) if on else (50, 54, 62)
            d.ellipse([x0 + (52 + q * 34) * s, y + 26 * s, x0 + (72 + q * 34) * s, y + 46 * s], fill=c)
    if label: put(C, plate_img(label, int(44 * s), YEL, INK, pad=12, r=8, border=INK, bw=5), cx, y0 - 50 * s, 1, -3)
def addr_field(C, cx, cy, w, text, col=INK, bg=WHITE, hl=None, k=1.0, cursor_=False, u=0):
    """поле ввода с адресом кошелька; hl=(n_первых, n_последних) подсветка жёлтым"""
    if k <= 0: return
    h = 140; im = Image.new('RGBA', (int(w) + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([5, 5, w + 5, h + 5], radius=24, fill=bg, outline=INK, width=8)
    f = font(66); tw = d.textlength(text, font=f); x = (w + 10 - tw) / 2; y = 5 + h / 2
    if hl:
        a, b = hl; wa = d.textlength(text[:a], font=f); wb = d.textlength(text[len(text) - b:], font=f)
        d.rounded_rectangle([x - 8, y - 46, x + wa + 8, y + 46], radius=10, fill=YEL); d.rounded_rectangle([x + tw - wb - 8, y - 46, x + tw + 8, y + 46], radius=10, fill=YEL)
    d.text((x, y), text, font=f, fill=col, anchor='lm')
    if cursor_ and int(u * 3) % 2 == 0: d.rectangle([x + tw + 10, y - 40, x + tw + 18, y + 40], fill=INK)
    put(C, im, cx, cy, back(k / 0.2) if k < 0.3 else 1)
def btc(C, cx, cy, r=40, rot=0):
    d = D(C); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BTC, outline=INK, width=max(3, int(r * 0.12)))
    d.line([cx - r * 0.12, cy - r * 0.72, cx - r * 0.12, cy + r * 0.72], fill=WHITE, width=max(2, int(r * 0.1))); d.line([cx + r * 0.12, cy - r * 0.72, cx + r * 0.12, cy + r * 0.72], fill=WHITE, width=max(2, int(r * 0.1)))
    put(C, text_img('B', int(r * 1.15), WHITE), cx + r * 0.04, cy, 1, rot)
def grechka(C, cx, by, s=1.0, rot=0):
    im = Image.new('RGBA', (int(240 * s) + 10, int(320 * s) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = 240 * s, 320 * s
    d.polygon([(5, 5 + h * 0.12), (5 + w * 0.15, 5), (5 + w * 0.85, 5), (5 + w, 5 + h * 0.12), (5 + w, 5 + h), (5, 5 + h)], fill=(246, 236, 212), outline=INK)
    d.line([(5, 5 + h * 0.12), (5 + w * 0.15, 5), (5 + w * 0.85, 5), (5 + w, 5 + h * 0.12), (5 + w, 5 + h), (5, 5 + h), (5, 5 + h * 0.12)], fill=INK, width=max(3, int(8 * s)))
    d.rectangle([5 + w * 0.08, 5 + h * 0.3, 5 + w * 0.92, 5 + h * 0.62], fill=(200, 60, 40))
    t = text_img('ГРЕЧКА', int(46 * s), WHITE); im.alpha_composite(t, (int(5 + w / 2 - t.width / 2), int(5 + h * 0.46 - t.height / 2)))
    for j in range(9): x = 5 + w * (0.15 + (j % 3) * 0.3); y = 5 + h * (0.72 + (j // 3) * 0.08); d.ellipse([x - 6 * s, y - 5 * s, x + 6 * s, y + 5 * s], fill=GRECH)
    put(C, im, cx, by - h / 2, 1, rot)
def grech_pile(C, cx, by, n, s=0.6):
    for j in range(n):
        row = 0; m = j; per = 4
        while m >= per: m -= per; row += 1; per -= 1
        grechka(C, cx + (m - (per - 1) / 2) * 150 * s / 0.6, by - row * 196 * s / 0.6, s, (j * 7 % 11) - 5)
def sms(C, cx, cy, w, text, k=1.0, col=INK):
    if k <= 0: return
    t = text_img(text, 62, WHITE); h = t.height + 70; im = Image.new('RGBA', (int(w) + 10, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([5, 5, w + 5, h + 5], radius=40, fill=col); d.polygon([(40, h - 10), (20, h + 45), (110, h - 5)], fill=col)
    im.alpha_composite(t, (int(5 + w / 2 - t.width / 2), int(5 + h / 2 - t.height / 2))); put(C, im, cx, cy, back(k / 0.22) if k < 0.4 else 1, -2)
def ninja(C, cx, cy, r, u, label=None, seed=0, tip=False):
    """гремлин-код крадётся на цыпочках"""
    gremlin(C, cx, cy - (abs(s_(u * 9)) * r * 0.25 if tip else 0), r, u, label, seed)
def man_o(C, clip, u, cx, feet, s, flip=False, w=9):
    """человечек с белой «стикерной» обводкой — для тёмного фона"""
    L = layer(); man(L, clip, u, cx, feet, s, flip=flip); a = L.getchannel('A').filter(ImageFilter.MaxFilter(w * 2 + 1))
    O = Image.new('RGBA', (CW, CH), WHITE + (0,)); O.putalpha(a); C.alpha_composite(O); C.alpha_composite(L)
