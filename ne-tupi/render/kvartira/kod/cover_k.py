"""Обложки «Отцу квартиру дали»: A «ОН ЕЁ НЕ КУПИЛ», B «АРЕНДА = ПОДПИСКА». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_k import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
# A
C = base()
txt(C, 'ОН ЕЁ', 540, 370, 170, INK)
put(C, plate_img('НЕ КУПИЛ', 160, YEL, INK, pad=30, r=20), 540, 570, 1, -3)
flat(C, 660, 1010, 620, 440, 3, 1, 3)
ImageDraw.Draw(C).line([90, 1476, 990, 1476], fill=LG, width=8)
man(C, 'd_keys', 0.3, 300, 1470, 0.62)
burst(C, 560, 830, 120, 0.2, fill=YEL); keys(C, 560, 830, 0.9, 8)
C.convert('RGB').save('../oblozhka-A.png')
# B
C = base()
txt(C, 'АРЕНДА', 540, 360, 190, INK)
put(C, plate_img('= ПОДПИСКА', 130, YEL, INK, pad=30, r=20), 540, 570, 1, -3)
flat(C, 540, 1010, 640, 450, 1, 1, -2); lock(C, 540, 1000, 1.5)
put(C, plate_img('ОТМЕНИТЬ НЕЛЬЗЯ', 64, RED, WHITE, pad=18, r=12), 540, 1300, 1, -4)
ImageDraw.Draw(C).line([90, 1476, 990, 1476], fill=LG, width=8)
man(C, 'sad', 0.2, 190, 1470, 0.4)
C.convert('RGB').save('../oblozhka-B.png')
