"""Обложки «Зарплаты в автобусе»: белый фон, жёлтые плашки, сюжетная сцена (стиль обложек канала)."""
from PIL import Image, ImageDraw, ImageFont
import compose_a as c
WD, HT = 1080, 1920; WH = (255, 255, 255); G = 1640
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
def plates(d, y, lines, sz, fill=c.YEL, color=c.INK, gap=14, pad=24):
    f = ImageFont.truetype(FB, sz)
    for l in lines:
        bb = d.textbbox((0, 0), l, font=f); w, h = bb[2] - bb[0], sz * 0.78; x = (WD - w) / 2
        d.rounded_rectangle([x - pad, y - pad * 0.7, x + w + pad, y + h + pad * 0.7], radius=12, fill=fill)
        d.text((x - bb[0], y - bb[1] + (h - (bb[3] - bb[1])) / 2), l, font=f, fill=color); y += h + pad * 1.4 + gap
def base(): return Image.new('RGBA', (WD, HT), WH + (255,))
def card(fn, u, t):   # сцена из ролика, увеличенная
    C = Image.new('RGBA', (c.CW, c.CH), WH + (255,)); fn(C, u, t); return C
def cover_a():   # миллионер в цилиндре заходит в автобус, у всех «средняя» выросла
    bg = base(); C = Image.new('RGBA', (c.CW, c.CH), WH + (255,))
    c.bus(C, 0.3, pax=30, door=1.0, tags=1.0)
    c.rich(C, 'boss', 0.3, c.DOOR[0] + c.DOOR[2] / 2, c.BY + c.BH + 50, 0.25)
    C = C.resize((int(c.CW * 1.04), int(c.CH * 1.04)), Image.LANCZOS); bg.alpha_composite(C, (-30, 860))
    d = ImageDraw.Draw(bg); d.line([(60, G), (1020, G)], fill=(150, 150, 150), width=6)
    plates(d, 300, ['СРЕДНЯЯ', 'ВРЁТ'], 150)
    f = ImageFont.truetype(FB, 64); d.text((540, 760), '70 000 → 100 000 ₽', font=f, fill=c.RED, anchor='mm')
    return bg.convert('RGB')
def cover_b():   # человечек у линейки «средняя», не дотягивает
    bg = base(); d = ImageDraw.Draw(bg); d.line([(60, G), (1020, G)], fill=(150, 150, 150), width=6)
    c.man(bg, 'idle_sad', 0, 360, G, 0.62)
    top = G - 1000; d.rectangle([600, top, 760, G], fill=c.YEL, outline=c.INK, width=8)
    for j in range(24): d.line([600, G - j * 42, 650 if j % 2 else 690, G - j * 42], fill=c.INK, width=6)
    f = ImageFont.truetype(FB, 54); d.rounded_rectangle([560, top - 100, 900, top - 20], radius=12, fill=c.INK); d.text((730, top - 60), '103 000 ₽', font=f, fill=c.YEL, anchor='mm')
    plates(d, 230, ['2 ИЗ 3', 'НЕ ДОТЯНУТ'], 130)
    return bg.convert('RGB')
O = '../oblozhka/'
A, B = cover_a(), cover_b(); A.save(O + 'oblozhka-avtobus-a-srednyaya-vryot.png'); B.save(O + 'oblozhka-avtobus-b-ne-dotyanut.png')
sh = Image.new('RGB', (750, 640), (40, 40, 40))
for i, im in enumerate((A, B)):
    g = im.copy(); d = ImageDraw.Draw(g, 'RGBA'); d.rectangle([0, 0, WD, 240], fill=(0, 0, 0, 110)); d.rectangle([0, 1680, WD, HT], fill=(0, 0, 0, 110)); sh.paste(g.resize((360, 640)), (10 + i * 370, 0))
sh.save(O + 'obl-obzor.png')
