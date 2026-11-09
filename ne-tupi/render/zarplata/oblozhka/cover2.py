"""Сюжетные чёрно-белые обложки «Зарплата». Главное в центре 1080x1440."""
import math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont
WD, HT = 1080, 1920; INK = (17, 17, 17); WH = (255, 255, 255); YEL = (255, 214, 10); GREY = (217, 217, 217)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FM = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
def F(sz, f=FB): return ImageFont.truetype(f, sz)
def mul(a, b): return Image.fromarray((np.asarray(a, np.uint16) * np.asarray(b, np.uint16) // 255).astype(np.uint8))
def place(bg, fr, s, dx, dy):   # кадр 1080x1920 -> масштаб s, сдвиг
    im = fr.resize((int(WD * s), int(HT * s)), Image.LANCZOS); lay = Image.new('RGB', (WD, HT), WH); lay.paste(im, (int(dx), int(dy)))
    return mul(bg, lay)
def ctext(d, y, txt, f, fill=INK):
    w = d.textbbox((0, 0), txt, font=f)[2]; d.text(((WD - w) / 2, y), txt, font=f, fill=fill)
def plates(d, y, lines, sz, fill=YEL, color=INK, gap=14, pad=24):
    f = F(sz)
    for l in lines:
        bb = d.textbbox((0, 0), l, font=f); w, h = bb[2] - bb[0], sz * 0.78
        x = (WD - w) / 2; d.rounded_rectangle([x - pad, y - pad * 0.7, x + w + pad, y + h + pad * 0.7], radius=12, fill=fill)
        d.text((x - bb[0], y - bb[1] + (h - (bb[3] - bb[1])) / 2), l, font=f, fill=color); y += h + pad * 1.4 + gap
    return y
def guide(img):
    g = img.copy(); d = ImageDraw.Draw(g, 'RGBA'); d.rectangle([0, 0, WD, 240], fill=(0, 0, 0, 110)); d.rectangle([0, 1680, WD, HT], fill=(0, 0, 0, 110)); return g

# A: сидит на стуле, «до зарплаты 27 дней»
def cover_a():
    fr = Image.open('ckadry/c3/002.png').convert('RGB')
    ch = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(ch); w = 16
    d.line([(735, 1300), (790, 860)], fill=INK, width=w + 6)                       # спинка
    d.rounded_rectangle([450, 1285, 790, 1320], radius=10, fill=WH, outline=INK, width=w)  # сиденье
    for x0, x1 in ((480, 470), (760, 780)): d.line([(x0, 1320), (x1, 1610)], fill=INK, width=w)  # ножки
    d.line([(735, 1300), (790, 860)], fill=INK, width=w + 6)
    fr = mul(ch, fr)
    bg = Image.new('RGB', (WD, HT), WH); bg = place(bg, fr, 0.78, 540 - 600 * 0.78 + 60, 1640 - 1610 * 0.78)
    d = ImageDraw.Draw(bg)
    ctext(d, 290, 'до зарплаты', F(64, FM))
    plates(d, 400, ['27 ДНЕЙ'], 170)
    return bg

# B: машет улетающей зарплате
def banknote(img, cx, cy, ang, sc, flap):
    w, h = int(260 * sc), int(140 * sc); n = Image.new('RGBA', (w + 160, h + 160), (0, 0, 0, 0)); d = ImageDraw.Draw(n)
    ox, oy = 80, 80; lw = max(4, int(9 * sc))
    for side in (-1, 1):   # крылышки
        bx = ox + w / 2; by = oy + 10
        tip = (bx + side * w * 0.55, by - h * (0.55 + 0.35 * flap))
        d.polygon([(bx - side * 10, by + 4), tip, (bx + side * w * 0.25, by + 6)], fill=WH, outline=INK, width=lw)
    d.rounded_rectangle([ox, oy, ox + w, oy + h], radius=int(12 * sc), fill=YEL, outline=INK, width=lw)
    d.ellipse([ox + w / 2 - h * 0.3, oy + h * 0.2, ox + w / 2 + h * 0.3, oy + h * 0.8], outline=INK, width=lw)
    f = F(int(54 * sc)); tb = d.textbbox((0, 0), '₽', font=f); d.text((ox + w / 2 - (tb[2] - tb[0]) / 2 - tb[0], oy + h / 2 - (tb[3] - tb[1]) / 2 - tb[1]), '₽', font=f, fill=INK)
    n = n.rotate(ang, Image.BICUBIC, expand=True); img.alpha_composite(n, (int(cx - n.width / 2), int(cy - n.height / 2)))
def cover_b():
    bg = Image.new('RGB', (WD, HT), WH)
    fr = Image.open('ckadry/c2/002.png').convert('RGB')
    bg = place(bg, fr, 0.72, 540 - 540 * 0.72 - 160, 1640 - 1595 * 0.72)
    o = bg.convert('RGBA'); d = ImageDraw.Draw(o)
    pts = [(560, 1080, -8, 0.75, 0.2), (720, 930, 6, 0.85, 0.9), (880, 780, -12, 0.95, 0.4), (620, 790, 10, 0.6, 0.7), (920, 1110, 14, 0.55, 0.1)]
    for x, y, a, s, fl in pts:
        for k in range(3): d.line([(x - 120 * s - k * 35, y + 60 * s + k * 28), (x - 170 * s - k * 35, y + 90 * s + k * 28)], fill=GREY, width=8)
        banknote(o, x, y, a, s, fl)
    bg = o.convert('RGB'); d = ImageDraw.Draw(bg)
    plates(d, 300, ['ПОКА,', 'ЗАРПЛАТА'], 140)
    return bg

# C: пустой кошелёк, из него вылетает моль
def moth(d, cx, cy, s):
    for side in (-1, 1):
        d.ellipse([cx + side * 10 * s - (60 * s if side < 0 else 0), cy - 45 * s, cx + side * 10 * s + (60 * s if side > 0 else 0), cy + 10 * s], fill=INK)
        d.ellipse([cx + side * 8 * s - (40 * s if side < 0 else 0), cy - 5 * s, cx + side * 8 * s + (40 * s if side > 0 else 0), cy + 35 * s], fill=INK)
    d.rounded_rectangle([cx - 8 * s, cy - 40 * s, cx + 8 * s, cy + 40 * s], radius=int(8 * s), fill=INK)
    d.line([(cx - 4 * s, cy - 40 * s), (cx - 25 * s, cy - 75 * s)], fill=INK, width=max(3, int(5 * s))); d.line([(cx + 4 * s, cy - 40 * s), (cx + 25 * s, cy - 75 * s)], fill=INK, width=max(3, int(5 * s)))
def cover_c():
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    # кошелёк раскрыт, справа
    wx, wy = 760, 1250; lw = 16
    d.rounded_rectangle([wx - 210, wy - 60, wx + 210, wy + 230], radius=30, fill=WH, outline=INK, width=lw)
    d.polygon([(wx - 210, wy - 40), (wx - 180, wy - 230), (wx + 180, wy - 230), (wx + 210, wy - 40)], fill=WH, outline=INK, width=lw)
    d.line([(wx - 150, wy - 150), (wx + 150, wy - 150)], fill=GREY, width=8)
    d.rounded_rectangle([wx + 110, wy + 50, wx + 230, wy + 130], radius=20, fill=YEL, outline=INK, width=lw)
    moth(d, wx - 40, wy - 420, 1.4); moth(d, wx + 120, wy - 600, 0.9)
    for k in range(5): d.ellipse([wx - 20 + k * 30 - 6, wy - 280 - k * 60 - 6, wx - 20 + k * 30 + 6, wy - 280 - k * 60 + 6], fill=INK)
    fr = Image.open('ckadry/c2/004.png').convert('RGB')
    bg = place(bg, fr, 0.62, 300 - 540 * 0.62, 1640 - 1595 * 0.62)
    d = ImageDraw.Draw(bg); plates(d, 300, ['ОПЯТЬ', 'ПУСТО'], 150)
    return bg

def cover_kofe():
    import sys; sys.path.insert(0, '..')
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    rnd = random.Random(3)
    for x, y, a in ((150, 820, 20), (930, 760, -15), (110, 1180, -25), (950, 1450, 8)):   # серые купюры улетают
        n = Image.new('RGBA', (230, 140), (0, 0, 0, 0)); nd = ImageDraw.Draw(n)
        nd.rounded_rectangle([10, 10, 220, 130], radius=12, fill=GREY); nd.text((90, 30), '₽', font=F(70), fill=WH)
        n = n.rotate(a, Image.BICUBIC, expand=True); o = bg.convert('RGBA'); o.alpha_composite(n, (x - n.width // 2, y - n.height // 2)); bg = o.convert('RGB')
    fr = Image.open('../ckadry/cover/002.png').convert('RGB')
    bg = place(bg, fr, 0.62, 540 - 540 * 0.62, 1640 - 1595 * 0.62)
    # стакан в поднятой руке (справа)
    cup = Image.new('RGBA', (300, 420), (0, 0, 0, 0)); cd = ImageDraw.Draw(cup)
    cd.polygon([(60, 90), (240, 90), (215, 400), (85, 400)], fill=INK); cd.rounded_rectangle([45, 50, 255, 100], radius=14, fill=INK)
    cd.polygon([(70, 190), (230, 190), (222, 290), (78, 290)], fill=YEL)
    cup = cup.resize((150, 210), Image.LANCZOS).rotate(-12, Image.BICUBIC, expand=True)
    o = bg.convert('RGBA'); o.alpha_composite(cup, (745, 1010)); bg = o.convert('RGB')
    d = ImageDraw.Draw(bg); plates(d, 300, ['КОФЕ ТЕБЯ', 'НЕ РАЗОРЯЕТ'], 120)
    return bg

if __name__ == '__main__':
    out = {'a-stul': cover_a(), 'b-poka': cover_b(), 'c-pusto': cover_c()}
    cover_kofe().save('oblozhka-kofe-zheltaya.png')
    sh = Image.new('RGB', (3 * 370 + 10, 640), (40, 40, 40))
    for i, (k, im) in enumerate(out.items()):
        im.save(f'oblozhka-zarplata-{k}.png'); sh.paste(guide(im).resize((360, 640)), (10 + i * 370, 0))
    sh.save('obl2-obzor.png')
