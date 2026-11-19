"""Обложки «Почему в казино нет часов и окон»: A «ИГРОКИ САМИ ПОПРОСИЛИ» (реком.), B «ГДЕ ЧАСЫ?». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from scenes_kz import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
def floor(C): ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
# A: человечек с плакатом «УБЕРИТЕ ЧАСЫ!», рот открыт; рядом пустой круг от часов и автомат
C = base(); txt(C, 'ИГРОКИ', 540, 330, 170, INK)
put(C, plate_img('САМИ ПОПРОСИЛИ', 104, YEL, INK, pad=26, r=18, border=INK, bw=8), 540, 510, 1, -3)
floor(C); emptyclock(C, 300, 880, 130)
slotm(C, 300, FL, 0.62, 0, False, ('7', '$', '7'))
man(C, 'sign', 0.1, 720, FL, 0.46, flip=True); L = layer(); placard(L, 720, 750, 300, 'УБЕРИТЕ\nЧАСЫ!', 4); L = L.crop((0, 0, CW, 880)); C.alpha_composite(L)
C.convert('RGB').save('../oblozhka/oblozhka-A.png')
# B: человечек чешет голову у стены, где вместо часов пустой круг, рядом окно в кирпичах
C = base(); txt(C, 'ГДЕ', 540, 360, 190, INK)
put(C, plate_img('ЧАСЫ?', 150, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 570, 1, 3)
floor(C); emptyclock(C, 300, 900, 150); qmark(C, 300, 900, 200, 0, RED)
brickwin(C, 300, 1230, 260, 230, 1)
man(C, 'shock', 0.05, 750, FL, 0.5, flip=True)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
