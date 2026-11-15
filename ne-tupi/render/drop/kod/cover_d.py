"""Обложки «Последний барабан»: A «ПОСЛЕДНИЙ БАРАБАН», B «5 000 ЗА СУДИМОСТЬ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_d import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
# A
C = base()
txt(C, 'ПОСЛЕДНИЙ', 470, 380, 150, INK)
put(C, plate_img('БАРАБАН', 150, YEL, INK, pad=30, r=20), 470, 560, 1, -3)
washer(C, 600, 1060, 1.45, 0.7, 'card', 1.0, lit=True)
man(C, 'pointcam', 0.3, 150, 1480, 0.40)
stains(C, 470, 1150, 260, 0.0)
C.convert('RGB').save('../oblozhka-A.png')
# B
C = base()
put(C, plate_img('5 000 ₽', 170, YEL, INK, pad=34, r=24, border=INK, bw=10), 470, 400, 1, -4)
txt(C, 'ЗА СУДИМОСТЬ', 470, 600, 120, RED)
L = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); man(L, 'sad', 0.2, 470, 1470, 0.62)
d = ImageDraw.Draw(L); d.rectangle([150, 690, 790, 730], fill=INK)
for x in range(170, 791, 100): d.rectangle([x, 690, x + 30, 1500], fill=INK)
C.alpha_composite(L); ImageDraw.Draw(C).line([60, 1500, 880, 1500], fill=LG, width=8)
C.convert('RGB').save('../oblozhka-B.png')
