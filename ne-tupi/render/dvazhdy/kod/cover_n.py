"""Обложки «Никогда не пропускай дважды» в стиле «Десятый легче»."""
import os, sys
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
import compose_n as cn
def ch(bg, idx, s, cx, feet):
    fr = Image.open(f'ckadry/cv/{idx:03d}.png').convert('RGBA'); w, h = int(WD * s), int(HT * s)
    fr = fr.resize((w, h), Image.LANCZOS); bg.alpha_composite(fr, (int(cx - w / 2), int(feet + 40 * s - h * (1660 / 1920))))
def cover_a():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640
    stt = cn.st(base_f={1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14}, base_x={5, 8, 9})
    cn.draw_month(bg, 92, (11, 420, 1080), stt, 0, pulse=lambda d, t: d in (8, 9))
    ch(bg, 1, 0.58, 800, g)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 290, ['НИКОГДА', 'ДВАЖДЫ'], 130)
    return bg.convert('RGB')
def cover_b():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640
    ch(bg, 0, 0.48, 540, g)
    cn.trophy(bg, 540, 1040, 0.9)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 290, ['ПРАВИЛО', 'УСПЕХА'], 130)
    return bg.convert('RGB')
for k, f in (('a-nikogda', cover_a), ('b-pravilo', cover_b)): f().save(f'obl/oblozhka-dvazhdy-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-nikogda', 'b-pravilo')): sh.paste(guide(Image.open(f'obl/oblozhka-dvazhdy-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl/obl-obzor.png')
