"""Обложка v2 «СВОБОДА СО СКИДКОЙ»: витрина, зачёркнутый ценник, стикер −20%."""
from PIL import Image, ImageDraw
exec(open('cover_sv.py').read().split('def well')[0])
GLASS = (236, 242, 247); RED = (230, 57, 70)
def cover_s():
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg); g = 1620; cx = 680
    x0, x1, y0 = cx - 250, cx + 250, g - 720
    d.rounded_rectangle([x0, y0, x1, g], radius=20, fill=GLASS, outline=INK, width=12)
    d.rectangle([x0 - 15, y0 - 90, x1 + 5, y0], fill=INK)
    f = F(56); d.text((cx, y0 - 45), 'СВОБОДА', font=f, fill=YEL, anchor='mm')
    for k in range(3): d.line([(x0 + 60 + k * 50, y0 + 40), (x0 + 20 + k * 50, y0 + 140)], fill=WH, width=10)
    d.rounded_rectangle([cx - 90, g - 140, cx + 90, g - 20], radius=10, fill=MID, outline=INK, width=8)
    # ценник
    tx0, ty0, tx1, ty1 = cx - 200, y0 + 170, cx + 200, y0 + 470
    d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=22, fill=WH, outline=INK, width=9)
    f1 = F(64); d.text((cx, ty0 + 75), '15 000 000', font=f1, fill=DG, anchor='mm')
    d.line([(tx0 + 25, ty0 + 90), (tx1 - 25, ty0 + 60)], fill=RED, width=12)
    f2 = F(76); bb = d.textbbox((0, 0), '12 000 000', font=f2); w = bb[2] - bb[0]
    d.rounded_rectangle([cx - w / 2 - 16, ty0 + 150, cx + w / 2 + 16, ty0 + 260], radius=12, fill=YEL)
    d.text((cx, ty0 + 205), '12 000 000', font=f2, fill=INK, anchor='mm')
    # стикер −20%
    st = Image.new('RGBA', (260, 260), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 252, 252], fill=YEL, outline=INK, width=10)
    sd.text((148, 132), '20%', font=F(70), fill=INK, anchor='mm'); sd.rectangle([30, 124, 62, 138], fill=INK)
    put(bg, st, x1 - 130, ty1 + 95, -14)
    fr = Image.open('ck/cv/000.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 175 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['СВОБОДА', 'СО СКИДКОЙ'], 112)
    return bg
cover_s().save('oblozhka-svoboda-v2-a-skidka.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('v2-a-skidka', 'a-rashody-300')): sh.paste(guide(Image.open(f'oblozhka-svoboda-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor-v2.png')
