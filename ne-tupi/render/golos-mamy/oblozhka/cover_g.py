"""Обложки «Голос мамы»: белый фон, чёрное + жёлтые акценты. Главное в центре 1080x1440."""
import sys; sys.path.insert(0, '..')
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
FLIP = 1
RED = (226, 48, 48); DG = (95, 95, 95); LG = (225, 222, 215)
import random as _r
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20, outline=None):
    f = F(sz); bb = d.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=12, fill=fill, outline=outline, width=5 if outline else 0)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=f, fill=col)
def bubble(d, cx, cy, w, h, seed=3, fill=INK):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h * 0.42, fill=fill)
    d.polygon([(cx - w / 2 + 8, cy + h * 0.1), (cx - w / 2 - 34, cy + h / 2 + 6), (cx - w / 2 + 60, cy + h / 2 - 6)], fill=fill)
    r = h * 0.3; px = cx - w / 2 + h * 0.5
    d.ellipse([px - r, cy - r, px + r, cy + r], fill=YEL); d.polygon([(px - r * .3, cy - r * .45), (px - r * .3, cy + r * .45), (px + r * .5, cy)], fill=INK)
    rr = _r.Random(seed); x0 = px + r + 24; n = 16; step = (w - h - r - 44) / n
    for i in range(n):
        bh = h * 0.5 * (0.25 + 0.75 * rr.random()); bx = x0 + i * step
        d.rounded_rectangle([bx, cy - bh / 2, bx + step * .56, cy + bh / 2], radius=step * .28, fill=YEL)
def ava(d, cx, cy, r, crook=False):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 70) if crook else YEL, outline=INK, width=int(r * .1))
    ch = '?' if crook else 'М'; f = F(int(r * 1.15)); bb = d.textbbox((0, 0), ch, font=f)
    d.text((cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2), ch, font=f, fill=WH if crook else INK)
def cover_a():   # голосовое от «Мамы», из-за аватарки выглядывает «?»
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    fr = Image.open('ckadry/cv/000.png').convert('RGB')
    s = 0.72; bg = place(bg, fr, s, 300 - 540 * s, 1640 - 1610 * s)
    d = ImageDraw.Draw(bg)
    d.line([(60, 1640), (1020, 1640)], fill=GREY, width=6)
    ava(d, 905, 800, 105, True); ava(d, 800, 850, 105, False)
    tag(d, 800, 1000, 'Мама', 54, WH, INK, pad=16)
    bubble(d, 760, 1150, 470, 140)
    tag(d, 790, 1290, '«срочно переведи»', 44, WH, DG, pad=16, outline=LG)
    plates(d, 290, ['ЭТО', 'НЕ МАМА'], 150)
    return bg
def cover_b():   # кодовое слово
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    fr = Image.open('ckadry/cv/001.png').convert('RGB'); fr = fr if FLIP == 0 else fr.transpose(Image.FLIP_LEFT_RIGHT)
    s = 0.72; bg = place(bg, fr, s, 760 - 540 * s, 1640 - 1610 * s)
    d = ImageDraw.Draw(bg)
    d.line([(60, 1640), (1020, 1640)], fill=GREY, width=6)
    cx, cy, w, h = 330, 1000, 500, 170
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=30, fill=YEL, outline=INK, width=10)
    for i in range(5): d.ellipse([cx - 190 + i * 76 - 26, cy - 26, cx - 190 + i * 76 + 26, cy + 26], fill=INK)
    tag(d, 330, 850, 'семейное', 50, WH, DG, pad=16, outline=LG)
    ava(d, 220, 1250, 80, True); d.line([(160, 1190), (280, 1310)], fill=RED, width=18); d.line([(280, 1190), (160, 1310)], fill=RED, width=18)
    plates(d, 290, ['ОДНО СЛОВО', 'ОТ МОШЕННИКОВ'], 100)
    return bg
for k, f in (('a-ne-mama', cover_a), ('b-slovo', cover_b)): f().save(f'oblozhka-golos-mamy-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-ne-mama', 'b-slovo')): sh.paste(guide(Image.open(f'oblozhka-golos-mamy-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
