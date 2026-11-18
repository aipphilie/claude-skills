"""Обложки «Сварщик vs программист» в стиле «Десятый легче»: белый фон, жёлтые плашки, крупный жёлтый предмет."""
import math
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
MIDG = (170, 166, 158)
def ch(bg, idx, s, cx, feet):
    fr = Image.open(f'ckadry/cv/{idx:03d}.png').convert('RGBA'); w, h = int(WD * s), int(HT * s)
    fr = fr.resize((w, h), Image.LANCZOS); bg.alpha_composite(fr, (int(cx - w / 2), int(feet + 40 * s - h * (1660 / 1920))))
def grey(bg, cx, feet, h, sign=None):
    d = ImageDraw.Draw(bg); w = h * .24; hr = h * .13; top = feet - h * .78
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, feet], radius=w / 2, fill=MIDG); d.line([cx, feet - h * .38, cx, feet], fill=WH, width=5)
    d.ellipse([cx - hr, top - hr * 2.05, cx + hr, top - hr * .05], fill=MIDG)
    if sign:
        sw = h * .58; sx = cx + w * .3; sy = top - hr * 2.2 - sw * .5
        d.line([sx, top + h * .15, sx, sy], fill=MIDG, width=8)
        d.rounded_rectangle([sx - sw / 2, sy - sw * .32, sx + sw / 2, sy + sw * .32], radius=12, fill=YEL, outline=INK, width=6)
        d.text((sx, sy), sign, font=F(int(sw * .27)), fill=INK, anchor='mm')
def money(bg, cx, base, w, n):
    d = ImageDraw.Draw(bg); hh = w * .17
    for j in range(n):
        y = base - j * hh * .85; d.rounded_rectangle([cx - w / 2, y - hh, cx + w / 2, y], radius=10, fill=YEL, outline=INK, width=7)
    d.text((cx, base - n * hh * .85 - hh * .2), '₽', font=F(int(w * .32)), fill=INK, anchor='mb')
def cover_a():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640; d = ImageDraw.Draw(bg)
    for j, sg in enumerate(('₽₽₽', '₽₽', '₽₽₽', '₽₽')): grey(bg, 540 + j * 125, g, 330 - j * 10, sg)
    ch(bg, 0, 0.62, 260, g)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 300, ['ОЧЕРЕДЬ', 'К НЕМУ'], 130)
    return bg.convert('RGB')
def cover_b():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640; d = ImageDraw.Draw(bg)
    money(bg, 820, g, 300, 9)
    ch(bg, 1, 0.5, 280, g); ch(bg, 2, 0.5, 600, g)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 300, ['ДИПЛОМ', 'НЕ ПЛАТИТ'], 130)
    return bg.convert('RGB')
O = '/mnt/project-files/ne-tupi-render/svarshchik/oblozhka/'
for k, f in (('a-ochered', cover_a), ('b-diplom', cover_b)): f().save(f'{O}oblozhka-svarshchik-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-ochered', 'b-diplom')): sh.paste(guide(Image.open(f'{O}oblozhka-svarshchik-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save(f'{O}obl-obzor.png')
