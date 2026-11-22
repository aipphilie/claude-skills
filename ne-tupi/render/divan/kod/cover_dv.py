"""Обложки «Если бы деньги были не важны»: A «ДИВАН ЗА 6 МЛН» (реком.), B «СОБИРАЙ ДИВАН». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from scenes_dv import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
def floor(C): ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
# A: человечек лежит на диване, на диване ценник 6 000 000 ₽
C = base(); rays(C, 540, 1120, 700, 0.3, 18, GLOW, 0.8); txt(C, 'ДИВАН', 540, 340, 200, INK)
put(C, plate_img('ЗА 6 МЛН ₽', 120, YEL, INK, pad=26, r=18, border=INK, bw=8), 540, 560, 1, -3)
floor(C); sw = 800
sofa(C, 540, FL, sw); lie_on(C, 0.1, 540, FL, sw, 'lie_remote', 0.42); remote(C, 552, FL - 445, 0.6, 20)
put(C, plate_img('6 000 000 ₽', 64, WHITE, INK, pad=16, r=10, border=INK, bw=6), 830, FL - 470, 1, 12)
D(C).line([760, FL - 430, 700, FL - 330], fill=INK, width=6)
C.convert('RGB').save('../oblozhka/oblozhka-A.png')
# B: человечек на недостроенном диване, кренится, большой палец
C = base(); txt(C, 'СОБИРАЙ', 540, 340, 180, INK)
put(C, plate_img('ДИВАН', 140, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 570, 1, 3)
floor(C); piggy(C, 200, FL, 0.62); coin(C, 210, FL - 300, 38, 20)
L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); w = 580; cx = 700
sofa(L, cx, FL, w, ('legL', 'armL', 'seat', 'back', 'cush')); man(L, 'sit_thumb', 0.3, cx - w * 0.05, seat_y(FL, w) - w * 0.02, 0.5)
C.alpha_composite(L.rotate(-6, Image.BICUBIC, center=(cx - w * 0.4, FL)))
thumb(C, 560, 900, 0.9, -10)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
