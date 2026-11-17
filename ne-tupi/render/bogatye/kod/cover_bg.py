"""Обложки «Реальные привычки богатых»: A «ПРИВЫЧКИ БОГАТЫХ / БЕЗ ЦЕНЗУРЫ» (реком.), B «СМУЗИ НЕ ПОМОЖЕТ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_bg import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
C = base(); txt(C, 'ПРИВЫЧКИ', 540, 360, 170, INK); txt(C, 'БОГАТЫХ', 540, 530, 170, INK)
put(C, plate_img('БЕЗ ЦЕНЗУРЫ', 110, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 700, 1, -3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
rich(C, 'laugh', 0.3, 470, 0.46, FL)
table(C, 540, FL - 170, 860, 170)
for j, x in enumerate((180, 290, 640, 900)): bottle(C, x, FL - 200, 0.55, (j - 1.5) * 6)
envelope(C, 800, FL - 330, 230, 10, '', cash=3)
C.convert('RGB').save('../oblozhka/oblozhka-A.png')
C = base(); txt(C, 'СМУЗИ', 540, 400, 200, INK); put(C, plate_img('НЕ ПОМОЖЕТ', 130, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 600, 1, 3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
smoothie(C, 260, FL, 0.8, -6); xcross(C, 1, 260, FL - 220, 170, RED, 24)
crib(C, 700, FL, 0.95, 0.4)
for j, (x, y) in enumerate([(560, 860), (700, 820), (840, 870), (620, 980), (790, 990)]): coin(C, x, y, 40, j * 30)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
