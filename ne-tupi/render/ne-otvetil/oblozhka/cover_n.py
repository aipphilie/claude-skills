import sys, math
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
RED = (226, 48, 48); DG = (150, 150, 150)
CL = [(-150, 30, 110), (-60, -50, 130), (70, -60, 140), (170, 20, 115), (60, 60, 120), (-50, 70, 115)]
def cloud(d, cx, cy, sc, tail=None):
    for dx, dy, r in CL: d.ellipse([cx + (dx - r) * sc, cy + (dy - r) * sc, cx + (dx + r) * sc, cy + (dy + r) * sc], fill=INK)
    if tail:
        for k, r in ((0.5, 34), (0.85, 20)):
            x = cx + (tail[0] - cx) * k; y = cy + 130 * sc + (tail[1] - cy - 130 * sc) * k; d.ellipse([x - r, y - r, x + r, y + r], fill=INK)
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20):
    f = F(sz); bb = d.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=12, fill=fill)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=f, fill=col)
def cover_a():   # сидит на стуле под огромной тучей мыслей
    fr = Image.open('ckadry/cv/000.png').convert('RGB')
    ch = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(ch); w = 16
    d.line([(735, 1300), (790, 860)], fill=INK, width=w + 6)
    d.rounded_rectangle([450, 1285, 790, 1320], radius=10, fill=WH, outline=INK, width=w)
    for x0, x1 in ((480, 470), (760, 780)): d.line([(x0, 1320), (x1, 1610)], fill=INK, width=w)
    fr = mul(ch, fr)
    bg = Image.new('RGB', (WD, HT), WH); bg = place(bg, fr, 0.6, 540 - 600 * 0.6 + 20, 1640 - 1610 * 0.6)
    d = ImageDraw.Draw(bg)
    cloud(d, 560, 800, 1.0)
    tag(d, 500, 730, 'ОБИДЕЛСЯ?', 44); tag(d, 620, 806, 'НЕ ТО НАПИСАЛ?', 40); tag(d, 520, 882, 'ЭТО КОНЕЦ?', 44, RED, WH)
    plates(d, 290, ['ОН ПРОСТО', 'ОБЕДАЛ'], 132)
    return bg
def cover_b():   # стоит у телефона «Прочитано», чешет голову
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    cx, cy, w, h = 760, 1180, 420, 720
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=54, fill=INK)
    d.rounded_rectangle([cx - w / 2 + 16, cy - h / 2 + 16, cx + w / 2 - 16, cy + h / 2 - 16], radius=40, fill=WH)
    tag(d, 800, 960, 'Ты как?', 54, YEL, INK, pad=26)
    f = F(40, FM); d.text((640, 1040), 'Прочитано', font=f, fill=DG); d.text((640, 1092), '10 мин назад', font=f, fill=RED)
    for j in range(3): d.ellipse([610 + j * 52, 1300, 644 + j * 52, 1334], fill=GREY)
    fr = Image.open('ckadry/cv/001.png').convert('RGB')
    bg = place(bg, fr, 0.66, 300 - 540 * 0.66, 1640 - 1595 * 0.66)
    d = ImageDraw.Draw(bg); plates(d, 290, ['ПРОЧИТАНО.', 'И ТИШИНА'], 124)
    return bg
for k, f in (('a-obedal', cover_a), ('b-prochitano', cover_b)): f().save(f'oblozhka-ne-otvetil-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-obedal', 'b-prochitano')): sh.paste(guide(Image.open(f'oblozhka-ne-otvetil-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
