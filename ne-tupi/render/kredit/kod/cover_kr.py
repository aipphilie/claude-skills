"""Обложки «Если все перестанут платить кредит»: A «МЫ БОЛЬШЕ НЕ ПЛАТИМ!», B «ДОЛГ НЕ СГОРИТ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_kr import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
C = base()
txt(C, 'МЫ БОЛЬШЕ', 540, 360, 150, INK)
stamp(C, 1.0, 'НЕ ПЛАТИМ!', 540, 570, 130, RED, -6)
bank(C, 540, 1200, 0.8, 1.0, 0, 4)
pickets(C, 0.3, 540, 1470, 6, 0.24, ['НЕ ПЛАТИМ', 'ХВАТИТ', 'НЕТ КРЕДИТАМ'], 960)
ImageDraw.Draw(C).line([60, 1476, 1020, 1476], fill=LG, width=8)
C.convert('RGB').save('../oblozhka-v2-A.png')
C = base()
txt(C, 'ДОЛГ', 540, 370, 200, INK)
put(C, plate_img('НЕ СГОРИТ', 150, RED, WHITE, pad=30, r=20), 540, 585, 1, -3)
doc(C, 640, 1010, 440, 560, 'ДОЛГ', 5, 1, '+ ПРОЦЕНТЫ\n+ ПЕНИ', False, 140)
flames(C, 640, 1300, 520, 200, 0.4)
ImageDraw.Draw(C).line([60, 1476, 1020, 1476], fill=LG, width=8)
man(C, 'shock', 0.2, 240, 1470, 0.44)
C.convert('RGB').save('../oblozhka-v2-B.png')
