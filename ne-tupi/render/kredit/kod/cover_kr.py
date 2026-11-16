"""Обложки «Если все перестанут платить кредит»: A «НИКТО НЕ ПЛАТИТ», B «ДОЛГ НЕ СГОРИТ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_kr import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
C = base()
txt(C, 'НИКТО', 540, 370, 180, INK)
put(C, plate_img('НЕ ПЛАТИТ', 150, YEL, INK, pad=30, r=20), 540, 575, 1, -3)
bank(C, 540, 1300, 1.0, 1.0, 0, 4)
ImageDraw.Draw(C).line([60, 1306, 1020, 1306], fill=LG, width=8)
crowd(C, 0.3, 540, 1470, 6, 0.24, 'cheer', 980, 3)
ImageDraw.Draw(C).line([60, 1476, 1020, 1476], fill=LG, width=8)
C.convert('RGB').save('../oblozhka-A.png')
C = base()
txt(C, 'ДОЛГ', 540, 370, 200, INK)
put(C, plate_img('НЕ СГОРИТ', 150, RED, WHITE, pad=30, r=20), 540, 585, 1, -3)
doc(C, 640, 1010, 440, 560, 'ДОЛГ', 5, 1, '+ ПРОЦЕНТЫ\n+ ПЕНИ', False, 140)
flames(C, 640, 1300, 520, 200, 0.4)
ImageDraw.Draw(C).line([60, 1476, 1020, 1476], fill=LG, width=8)
man(C, 'shock', 0.2, 240, 1470, 0.44)
C.convert('RGB').save('../oblozhka-B.png')
