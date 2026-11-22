"""Обложки «Автокредит»: белый фон, чёрное + жёлтые плашки, сюжетная сцена. A — ВЗЯЛ 3 МЛН / ОТДАЛ 5,3 (реком.), B — МАШИНЫ НЕТ / ДОЛГ ЕСТЬ."""
import os, sys
os.environ.setdefault('F0', '0')
from scenes_ak import *
GG = 1500
def base():
    C = Image.new('RGBA', (CW, CH), WHITE + (255,)); ImageDraw.Draw(C).line([60, GG + 6, 1020, GG + 6], fill=LG, width=8); return C
def cover_a():
    C = base()
    put(C, plate_img('ВЗЯЛ 3 МЛН', 150, WHITE, INK, pad=24, r=18, border=INK, bw=8), 540, 420, 1, -3)
    put(C, plate_img('ОТДАЛ 5,3', 170, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 640, 1, 3)
    car(C, 660, GG, 1.0); man(C, 'shock', 0.3, 245, GG, 0.48)
    ptag(C, 690, 1050, 'ПЕРЕПЛАТА', '2 280 000 ₽', -7, RED, 1.15, WHITE)
    return C
def cover_b():
    C = base()
    put(C, plate_img('МАШИНЫ НЕТ', 150, WHITE, INK, pad=24, r=18, border=INK, bw=8), 540, 420, 1, -3)
    put(C, plate_img('ДОЛГ ЕСТЬ', 170, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 640, 1, 3)
    car(C, 660, GG, 1.0, ghost=True); man(C, 'pay', 0.5, 230, GG, 0.48)
    debtplate(C, 690, 1060, '656 000 ₽', 1, 5)
    return C
os.makedirs('../oblozhka', exist_ok=True)
for k, f in (('A-vzyal-otdal', cover_a), ('B-mashiny-net', cover_b)): f().convert('RGB').save(f'../oblozhka/oblozhka-avtokredit-{k}.png')
S = Image.new('RGB', (2 * 370 + 10, 660), (40, 40, 40))
for i, k in enumerate(('A-vzyal-otdal', 'B-mashiny-net')):
    im = Image.open(f'../oblozhka/oblozhka-avtokredit-{k}.png').copy(); d = ImageDraw.Draw(im); d.rectangle([0, 240, 1079, 1680], outline=(0, 160, 255), width=6)
    S.paste(im.resize((360, 640)), (10 + i * 370, 10))
S.save('../oblozhka/obzor.png')
