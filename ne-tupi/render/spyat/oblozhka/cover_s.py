"""Обложки рилса «Они спят» (единый стиль: белый фон, чёрное + жёлтые плашки)."""
import math
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
LG = (232, 230, 225); MID = (205, 201, 193); DG = (150, 150, 150)
def bagimg(w, text):
    k = 3; W_ = int(w * k); H_ = int(w * 1.1 * k); pad = int(w * 0.1 * k)
    im = Image.new('RGBA', (W_ + 2 * pad, H_ + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ox = oy = pad; lw = int(w * 0.04 * k)
    d.rounded_rectangle((ox + W_ * .30, oy + H_ * .04, ox + W_ * .70, oy + H_ * .26), radius=int(W_ * .08), fill=YEL, outline=INK, width=lw)
    d.rounded_rectangle((ox + W_ * .03, oy + H_ * .22, ox + W_ * .97, oy + H_), radius=int(W_ * .36), fill=YEL, outline=INK, width=lw)
    d.line((ox + W_ * .33, oy + H_ * .22, ox + W_ * .67, oy + H_ * .22), fill=INK, width=lw * 2)
    if text:
        sz = int(W_ * .34); f = F(sz)
        while d.textlength(text, font=f) > W_ * .8: sz -= 3; f = F(sz)
        d.text((ox + W_ / 2, oy + H_ * .63), text, font=f, fill=INK, anchor='mm')
    return im.resize((im.width // k, im.height // k), Image.LANCZOS)
def put(bg, im, cx, cy, rot=0):
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    bg.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)
def sofa(d, cx, g, w=560):
    x0, x1 = cx - w / 2, cx + w / 2
    d.rounded_rectangle([x0 + 30, g - 320, x1 - 30, g - 125], radius=40, fill=MID, outline=INK, width=10)
    d.rounded_rectangle([x0 + 30, g - 170, x1 - 30, g - 55], radius=24, fill=LG, outline=INK, width=10)
    for sx in (x0, x1 - 85): d.rounded_rectangle([sx, g - 225, sx + 85, g - 40], radius=34, fill=MID, outline=INK, width=10)
    for lx in (x0 + 55, x1 - 72): d.rectangle([lx, g - 45, lx + 17, g], fill=INK)
    return g - 170
def zz(d, x, y, k=1.0):
    for j, (dx, dy, sz) in enumerate(((0, 0, 44), (40, -60, 58), (90, -135, 74))):
        d.text((x + dx * k, y + dy * k), 'Z', font=F(int(sz * k)), fill=DG)
def cover_a():   # мешки спят на диване «КАРТА», человечек в шоке
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg); g = 1620
    seat = sofa(d, 700, g)
    for j, (x, r) in enumerate(((560, -12), (700, 8), (840, -6))):
        put(bg, bagimg(140, '₽'), x, seat - 72, r)
    d = ImageDraw.Draw(bg)
    for j, x in enumerate((570, 715, 850)): zz(d, x, seat - 230 - j * 10, 0.9)
    lab = 'КАРТА'; f = F(54); bb = d.textbbox((0, 0), lab, font=f); w = bb[2] - bb[0]
    d.rounded_rectangle([700 - w / 2 - 22, g - 140, 700 + w / 2 + 22, g - 70], radius=12, fill=WH, outline=INK, width=6)
    d.text((700 - w / 2 - bb[0], g - 136 - bb[1] + 8), lab, font=f, fill=INK)
    fr = Image.open('ck/cv/000.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 220 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['ОНИ', 'СПЯТ'], 150)
    return bg
def cover_b():   # загадка «60К → ?»
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg); g = 1620
    f = F(96); txt = '60 000 ₽'; bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]
    cx, cy = 720, 900
    d.rounded_rectangle([cx - w / 2 - 36, cy - 80, cx + w / 2 + 36, cy + 80], radius=26, fill=WH, outline=INK, width=9)
    d.text((cx - w / 2 - bb[0], cy - (bb[3] + bb[1]) / 2), txt, font=f, fill=INK)
    d.line([(cx, cy + 100), (cx, cy + 260)], fill=INK, width=14); d.polygon([(cx - 36, cy + 250), (cx + 36, cy + 250), (cx, cy + 300)], fill=INK)
    put(bg, bagimg(230, '?'), cx, cy + 450)
    fr = Image.open('ck/cv/001.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 250 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['60К → ?'], 160)
    return bg
for k, f in (('a-spyat', cover_a), ('b-60k', cover_b)): f().save(f'oblozhka-spyat-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-spyat', 'b-60k')): sh.paste(guide(Image.open(f'oblozhka-spyat-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
