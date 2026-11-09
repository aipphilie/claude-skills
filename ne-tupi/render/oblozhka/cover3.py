"""Сюжетные обложки «Кофе» в стиле «Пока, зарплата»: белый фон, чёрное, жёлтые плашки, серые второстепенные элементы."""
import math
from PIL import Image, ImageDraw
from cover2 import WD, HT, INK, WH, YEL, GREY, F, FM, mul, place, plates, guide, ctext

def cup(w, sleeve=YEL, lid=True):
    h = int(w * 1.3); im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = 10
    top, bot = w * 0.86, w * 0.66; cx = o + w / 2
    d.polygon([(cx - top / 2, o + h * 0.14), (cx + top / 2, o + h * 0.14), (cx + bot / 2, o + h), (cx - bot / 2, o + h)], fill=INK)
    if lid: d.rounded_rectangle([cx - w / 2, o, cx + w / 2, o + h * 0.16], radius=int(w * 0.05), fill=INK)
    def xat(y): return top / 2 + (bot / 2 - top / 2) * (y - o - h * 0.14) / (h * 0.86)
    y0, y1 = o + h * 0.42, o + h * 0.68
    d.polygon([(cx - xat(y0), y0), (cx + xat(y0), y0), (cx + xat(y1), y1), (cx - xat(y1), y1)], fill=sleeve)
    return im
def paste(bg, im, cx, cy, rot=0):
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    o = bg.convert('RGBA'); o.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))); return o.convert('RGB')

# A: «ОН НЕ ВИНОВАТ» — стакан на фото из полиции, человечек показывает на него
def cover_a():
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    x0, x1, yb = 560, 1010, 1500
    for k in range(9):
        y = yb - k * 75; d.line([(x0, y), (x1, y)], fill=GREY, width=5)
        if k % 2 == 0: d.text((x1 - 60, y - 40), str(k * 20 + 40), font=F(28, FM), fill=(170, 170, 170))
    bg = paste(bg, cup(300), 770, yb - 230)
    d = ImageDraw.Draw(bg); d.rounded_rectangle([630, yb - 70, 910, yb + 20], radius=10, fill=INK)
    ctext_x = lambda t, cx, y, f, col: d.text((cx - d.textbbox((0, 0), t, font=f)[2] / 2, y), t, font=f, fill=col)
    ctext_x('№ 250 ₽', 770, yb - 60, F(48), WH)
    fr = Image.open('ckadry/c4/000.png').convert('RGB')
    bg = place(bg, fr, 0.66, 260 - 540 * 0.66, 1600 - 1595 * 0.66)
    d = ImageDraw.Draw(bg); plates(d, 300, ['ОН НЕ', 'ВИНОВАТ'], 150)
    return bg

# B: «КОФЕ — КОПЕЙКИ» — весы: стакан взлетел, крупные траты перевесили
def cover_b():
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    cx, cy, L, ang = 610, 900, 270, math.radians(-20)
    lx, ly = cx - L * math.cos(ang), cy + L * math.sin(ang); rx, ry = cx + L * math.cos(ang), cy - L * math.sin(ang)
    d.line([(cx, cy), (cx, 1560)], fill=INK, width=16); d.rounded_rectangle([cx - 130, 1550, cx + 130, 1580], radius=10, fill=INK)
    d.line([(lx, ly), (rx, ry)], fill=INK, width=14); d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=YEL, outline=INK, width=6)
    for px, py in ((lx, ly), (rx, ry)):
        d.line([(px, py), (px - 110, py + 190)], fill=INK, width=5); d.line([(px, py), (px + 110, py + 190)], fill=INK, width=5)
        d.chord([px - 150, py + 160, px + 150, py + 230], 0, 180, fill=INK)
    bg = paste(bg, cup(90), lx, ly + 125)
    d = ImageDraw.Draw(bg); y = ry + 190
    for txt, w in (('ТАКСИ', 220), ('ДОСТАВКА', 270), ('КРЕДИТ', 240)):
        h = 90; d.rounded_rectangle([rx - w / 2, y - h, rx + w / 2, y], radius=12, fill=GREY)
        f = F(40); tw = d.textbbox((0, 0), txt, font=f)[2]; d.text((rx - tw / 2, y - h + 20), txt, font=f, fill=INK); y -= h + 8
    fr = Image.open('ckadry/c4/000.png').convert('RGB')
    bg = place(bg, fr, 0.5, 150 - 540 * 0.5, 1600 - 1595 * 0.5)
    d = ImageDraw.Draw(bg); plates(d, 300, ['КОФЕ —', 'КОПЕЙКИ'], 150)
    return bg

# C: «ПЕЙ СПОКОЙНО» — сидит на стуле и пьёт кофе
def cover_c():
    fr = Image.open('ckadry/c4/001.png').convert('RGB')
    ch = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(ch); w = 16
    d.rounded_rectangle([470, 1290, 800, 1325], radius=10, fill=WH, outline=INK, width=w)
    for x0, x1 in ((500, 490), (770, 790)): d.line([(x0, 1325), (x1, 1610)], fill=INK, width=w)
    d.line([(760, 1300), (820, 860)], fill=INK, width=w + 6)
    fr = mul(ch, fr)
    bg = Image.new('RGB', (WD, HT), WH)
    s = 0.8; dx, dy = 560 - 640 * s, 1640 - 1610 * s
    bg = place(bg, fr, s, dx, dy)
    hx, hy = dx + 300 * s, dy + 930 * s            # ладонь поднятой руки
    bg = paste(bg, cup(120), hx + 10, hy - 40, rot=-15)
    d = ImageDraw.Draw(bg)
    for k in range(3):  # пар
        x = hx + 10 + (k - 1) * 30
        for j in range(3): d.arc([x - 14, hy - 190 - j * 34, x + 14, hy - 160 - j * 34], 90 if j % 2 else 270, 270 if j % 2 else 90, fill=GREY, width=7)
    plates(d, 300, ['ПЕЙ', 'СПОКОЙНО'], 150)
    return bg

if __name__ == '__main__':
    out = {'a-ne-vinovat': cover_a(), 'b-kopeyki': cover_b(), 'c-pey-spokoyno': cover_c()}
    sh = Image.new('RGB', (3 * 370 + 10, 640), (40, 40, 40))
    for i, (k, im) in enumerate(out.items()):
        im.save(f'oblozhka-kofe-{k}.png'); sh.paste(guide(im).resize((360, 640)), (10 + i * 370, 0))
    sh.save('kofe-obzor.png')
