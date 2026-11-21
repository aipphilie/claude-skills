"""Обложки «Что знает о тебе телефон»: A «ТЕЛЕФОН ЗНАЕТ ВСЁ» (реком.), B «ФОНАРИК, КАРЛ!». Кремовый фон, чёрное + жёлтое, безопасные зоны Reels."""
from scenes_tf import *
def base():
    C = Image.new('RGBA', (1080, 1920), CARD + (255,)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(238, 226, 206))
    rnd = random.Random(4)
    for j in range(14): leaf(d, rnd.randint(40, 1040), rnd.randint(700, 1500), rnd.randint(22, 36), rnd.choice([(240, 200, 160), (236, 210, 150)]), rnd.randint(0, 360))
    return C
FL = 1440
# A: кот развалился на телефоне с досье, вокруг красные «глаза»-слежка
C = base(); txt(C, 'ТЕЛЕФОН', 540, 380, 180, INK)
put(C, plate_img('ЗНАЕТ ВСЁ', 130, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 580, 1, -3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
phone_frame(C, 460, 1180, 300, screen=(40, 44, 56), notch=False)
kot(C, 0.0, 460, 1370, 520, pose='loaf', eyes='half', look=(0.4, 0), shadow=False)
dossier(C, 820, 1040, 260, 1, 8)
d = ImageDraw.Draw(C)
for (x, y, w) in [(170, 820, 120), (330, 760, 90), (690, 780, 110)]: eye_glyph(d, x, y, w, RED, INK)
C.convert('RGB').save('../oblozhka/oblozhka-A.png')
# B: пёс-охранник в шоке, фонарик с глазом в луче
C = base(); txt(C, 'ФОНАРИК,', 540, 380, 175, INK)
put(C, plate_img('КАРЛ!', 140, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 590, 1, 3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
torch(C, 300, 790, 0.9, -6, 1.0, 1.0)
dog(C, 0.0, 600, FL, 420, 'stand', eyes='shock', mouth='o', flip=True)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
print('ok')
