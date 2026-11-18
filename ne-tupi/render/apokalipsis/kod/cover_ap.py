"""Обложки «Конец света 17 ноября»: A «ГРЕЧКА НЕ ПОМОГЛА» (реком.), B «КОНЕЦ СВЕТА / БЫЛ ТИХИМ». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from compose_ap import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
def scene(C):
    ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
    grech_pile(C, 320, FL, 9, 0.42); girl(C, 'scream', 0.3, 320, 0.26, FL - 400)
    ninja(C, 800, FL - 150, 120, 0.4, 'ХАКЕР', 5)
    for j, (x, y) in enumerate([(480, 980), (580, 900), (690, 880), (790, 960)]): btc(C, x, y, 46, j * 20)
C = base(); txt(C, 'ГРЕЧКА', 540, 400, 190, INK); put(C, plate_img('НЕ ПОМОГЛА', 140, YEL, INK, pad=30, r=20, border=INK, bw=8), 540, 610, 1, -3)
scene(C); C.convert('RGB').save('../oblozhka/oblozhka-A.png')
C = base(); txt(C, 'КОНЕЦ СВЕТА', 540, 390, 150, INK); put(C, plate_img('БЫЛ ТИХИМ', 140, YEL, INK, pad=30, r=20, border=INK, bw=8), 540, 600, 1, 3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
siren(C, 290, FL, 0.75, 0.3, False); xcross(C, 1, 290, FL - 420, 200, RED, 28)
addr_field(C, 540, 820, 820, ADDR2, RED, (255, 228, 230)); ninja(C, 780, FL - 160, 120, 0.4, 'КОД', 4)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
