"""Обложки «Чаевые — это налог»: A «ЧАЕВЫЕ — ЭТО НАЛОГ» (реком.), B «$2.13 В ЧАС». Белый фон, чёрное + жёлтое, безопасные зоны Reels."""
from scenes_ch import *
def base():
    C = Image.new('RGBA', (1080, 1920), (250, 249, 246, 255)); d = ImageDraw.Draw(C)
    for x in range(0, 1080, 46):
        for y in range(0, 1920, 46): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(234, 232, 226))
    return C
FL = 1440
# A: клиент в шоке над чеком, где строка «зарплата официанта»; рядом официант протягивает шляпу
C = base(); txt(C, 'ЧАЕВЫЕ —', 540, 380, 175, INK)
put(C, plate_img('ЭТО НАЛОГ', 130, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 570, 1, -3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
man(C, 'read_shock', 0.1, 310, FL, 0.56)
check(C, 330, 1150, 340, [('ЕДА', '$40'), ('ЗП ОФИЦИАНТА', '$8')], None, -6, hl=1)
waiter(C, 'hat', 0.2, 800, 0.44, FL, flip=True); bowler(C, 800, FL - 0.44 * 560, 170)
for j, (x, y) in enumerate([(760, 860), (840, 800), (900, 900)]): dcoin(C, x, y, 30, j * 40)
C.convert('RGB').save('../oblozhka/oblozhka-A.png')
# B: официант с отвисшей челюстью и огромный чек $2.13
C = base(); txt(C, '$2.13', 540, 400, 230, RED, stroke=INK, sw=6)
put(C, plate_img('В ЧАС', 130, YEL, INK, pad=28, r=18, border=INK, bw=8), 540, 610, 1, 3)
ImageDraw.Draw(C).line([60, FL + 6, 1020, FL + 6], fill=LG, width=8)
burst(C, 330, 1050, 250, 0, 16, YEL, INK)
check(C, 330, 1050, 380, [('ОФИЦИАНТ', '1 ЧАС')], '$2.13', -6)
waiter(C, 'jaw', 0.1, 790, 0.52, FL, flip=True)
C.convert('RGB').save('../oblozhka/oblozhka-B.png')
