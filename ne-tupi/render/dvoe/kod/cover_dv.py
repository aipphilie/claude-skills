"""Обложки «Одна зарплата — две судьбы»: A «ЦЕПЬ ИЛИ КОПИЛКА?» (реком.), B «ОДНА ЗАРПЛАТА / ДВЕ СУДЬБЫ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_dv import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
def scene(C):
    ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
    for j in range(5): doc(C, 150 + (j % 3) * 90, FL - 60 - (j // 3) * 120, 150, 190, 'КРЕДИТ', (-18, 12, -6, 20, -10)[j], 1, None, False, 28)
    leha(C, 'idle_sad', 0.3, 290, 0.4, FL)
    for j, x in enumerate((690, 800, 910)): stack_col(C, x, FL, (220, 300, 240)[j], 50)
    misha(C, 'cheer', 0.3, 800, 0.34, FL - 292)
    vs(C, 1.0, 540, 1080)
C = base(); txt(C, 'ЦЕПЬ ИЛИ', 540, 380, 170, INK); put(C, plate_img('КОПИЛКА?', 150, YEL, INK, pad=30, r=20, border=INK, bw=8), 540, 600, 1, -3)
scene(C); C.convert('RGB').save('../oblozhka/oblozhka-A.png')
C = base(); txt(C, 'ОДНА ЗАРПЛАТА', 540, 380, 130, INK); put(C, plate_img('ДВЕ СУДЬБЫ', 140, YEL, INK, pad=30, r=20, border=INK, bw=8), 540, 590, 1, 3)
scene(C); C.convert('RGB').save('../oblozhka/oblozhka-B.png')
