"""Обложки «Листок на 66 тысяч» в стиле «Десятый легче»: белый фон, жёлтые плашки, человечек с крупным предметом."""
import sys
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
import compose_k as ck
def ch(bg, idx, s, cx, feet):
    fr = Image.open(f'ckadry/cv/{idx:03d}.png').convert('RGBA'); w, h = int(WD * s), int(HT * s)
    fr = fr.resize((w, h), Image.LANCZOS); bg.alpha_composite(fr, (int(cx - w / 2), int(feet + 40 * s - h * (1660 / 1920))))
def sheet(bg, cx, cy, w, frac, rot=0):
    ck.mini_sheet(bg, cx, cy, w, frac, 0, rot)
def cover_a():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640
    ch(bg, 0, 0.55, 540, g)
    sheet(bg, 540, 770, 340, 0.55, -4)
    d = ImageDraw.Draw(bg); d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 290, ['ЛИСТОК', 'НА 66К'], 130)
    return bg.convert('RGB')
def cover_b():
    bg = Image.new('RGBA', (WD, HT), WH + (255,)); g = 1640; d = ImageDraw.Draw(bg)
    cx, cy, r = 330, 1080, 230
    bg.alpha_composite(ck.chalk(int(2 * r)), (cx - r, cy - r))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=12)
    d.text((cx, cy), '300', font=F(180), fill=INK, anchor='mm')
    ch(bg, 1, 0.6, 760, g)
    d.line([(60, g), (1020, g)], fill=(150, 150, 150), width=6)
    plates(d, 290, ['ЗАКРАСЬ', 'КРУЖОК'], 130)
    return bg.convert('RGB')
O = 'obl/'
for k, f in (('a-listok', cover_a), ('b-zakras', cover_b)): f().save(f'{O}oblozhka-kalendar-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-listok', 'b-zakras')): sh.paste(guide(Image.open(f'{O}oblozhka-kalendar-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save(f'{O}obl-obzor.png')
