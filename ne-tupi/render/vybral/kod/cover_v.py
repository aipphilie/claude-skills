"""Обложки «Он выбрал тебя» в стиле «Десятый легче»: белый фон, жёлтые плашки, человечки + 3D-предмет."""
import math, random
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
MIDG = (200, 197, 190)
def ch(bg, idx, s, cx, feet):
    fr = Image.open(f'ckadry/cv/{idx:03d}.png').convert('RGBA'); w, h = int(WD * s), int(HT * s)
    fr = fr.resize((w, h), Image.LANCZOS); bg.alpha_composite(fr, (int(cx - w / 2), int(feet + 40 * s - h * (1660 / 1920))))
def prop(bg, idx, cx, cy, s):
    im = Image.open(f'ckadry/c/{idx:03d}.png').convert('RGBA').resize((s, s), Image.LANCZOS); bg.alpha_composite(im, (int(cx - s / 2), int(cy - s / 2)))
def grey(d, cx, feet, h, dress):
    w = h * .24; hr = h * .13; top = feet - h * .78
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, feet], radius=w / 2, fill=MIDG); d.line([cx, feet - h * .38, cx, feet], fill=WH, width=5)
    d.ellipse([cx - hr, top - hr * 2.05, cx + hr, top - hr * .05], fill=MIDG)
    if dress:
        d.chord([cx - hr * 1.15, top - hr * 2.2, cx + hr * 1.15, top], 180, 360, fill=MIDG)
        d.rectangle([cx - hr * 1.15, top - hr * 1.15, cx - hr * .75, top + hr * .3], fill=MIDG); d.rectangle([cx + hr * .75, top - hr * 1.15, cx + hr * 1.15, top + hr * .3], fill=MIDG)
def cover_a():   # толпа, он показывает на неё, луч и сердце
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640; d = ImageDraw.Draw(bg); rnd = random.Random(5)
    for row, (fy, h, n) in enumerate(((g - 200, 230, 9), (g - 100, 290, 7))):
        for j in range(n):
            x = (j + .5) * WD / n
            if row == 1 and (abs(x - 260) < 120 or abs(x - 800) < 140): continue
            grey(d, x, fy, h, rnd.random() < .5)
    ov = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
    do.polygon([(750, 760), (850, 760), (990, g + 20), (610, g + 20)], fill=YEL + (90,)); do.ellipse([620, g - 30, 980, g + 40], fill=YEL + (190,))
    bg.alpha_composite(ov)
    ch(bg, 0, 0.58, 270, g); ch(bg, 1, 0.56, 800, g)
    prop(bg, 0, 820, 700, 250)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 300, ['ОН ВЫБРАЛ', 'ТЕБЯ'], 130)
    return bg.convert('RGB')
def cover_b():   # она грустит над вянущим цветком
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640; d = ImageDraw.Draw(bg)
    prop(bg, 1, 660, g - 300, 700)
    ch(bg, 2, 0.6, 290, g)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 300, ['ЛЮБОВЬ', 'ВЯНЕТ'], 130)
    return bg.convert('RGB')
O = '/mnt/project-files/ne-tupi-render/vybral/oblozhka/'
for k, f in (('a-vybral', cover_a), ('b-vyanet', cover_b)): f().save(f'{O}oblozhka-vybral-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-vybral', 'b-vyanet')): sh.paste(guide(Image.open(f'{O}oblozhka-vybral-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save(f'{O}obl-obzor.png')
