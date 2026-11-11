from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
RED = (226, 48, 48); DG = (150, 150, 150); LG = (225, 222, 215)
def lock(d, cx, cy, s, opened=0.0):
    w, h = 120 * s, 100 * s; r = 38 * s; lift = 34 * s * opened; top = cy - h / 2; lw = int(16 * s)
    d.arc([cx - r, top - r * 1.25 - lift, cx + r, top + r * 0.9 - lift], 180, 360, fill=INK, width=lw)
    d.line([cx - r + 7 * s, top - r * 0.2 - lift, cx - r + 7 * s, top + 6 * s], fill=INK, width=lw)
    if opened < 0.5: d.line([cx + r - 7 * s, top - r * 0.2, cx + r - 7 * s, top + 6 * s], fill=INK, width=lw)
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, top + h], radius=int(18 * s), fill=YEL, outline=INK, width=int(8 * s))
    d.ellipse([cx - 13 * s, cy - 20 * s, cx + 13 * s, cy + 6 * s], fill=INK); d.rectangle([cx - 5 * s, cy, cx + 5 * s, cy + 26 * s], fill=INK)
def phone(d, cx, top, bot, w, title, line, col):
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, bot], radius=56, fill=WH, outline=INK, width=14)
    d.rounded_rectangle([cx - 60, top + 28, cx + 60, top + 48], radius=10, fill=INK)
    x0, x1, y0 = cx - w / 2 + 26, cx + w / 2 - 26, top + 90
    d.rounded_rectangle([x0, y0, x1, y0 + 210], radius=28, fill=LG, outline=INK, width=6)
    d.ellipse([x0 + 20, y0 + 20, x0 + 68, y0 + 68], fill=col, outline=INK, width=4)
    d.text((x0 + 84, y0 + 26), 'БАНК', font=F(30), fill=DG)
    d.text((x0 + 22, y0 + 88), title, font=F(31), fill=INK); d.text((x0 + 22, y0 + 136), line, font=F(50), fill=RED if col == RED else INK)
def hood(d, cx, bot, s):
    c = (130, 130, 130)
    d.rounded_rectangle([cx - 70 * s, bot - 250 * s, cx + 70 * s, bot], radius=int(60 * s), fill=c)
    d.polygon([(cx - 86 * s, bot - 190 * s), (cx, bot - 345 * s), (cx + 86 * s, bot - 190 * s)], fill=c)
    d.ellipse([cx - 44 * s, bot - 262 * s, cx + 44 * s, bot - 178 * s], fill=(60, 60, 60))
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20, outline=None):
    f = F(sz); bb = d.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=12, fill=fill, outline=outline, width=5 if outline else 0)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=f, fill=col)
def cover_a():   # шок: в телефоне одобрен кредит, которого не брал
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    phone(d, 300, 760, 1640, 440, 'Вам одобрен кредит', '500 000 ₽', RED)
    fr = Image.open('ckadry/cv/002.png').convert('RGB')
    s = 0.6; bg = place(bg, fr, s, 780 - 540 * s, 1640 - 1600 * s)
    d = ImageDraw.Draw(bg); d.line([(60, 1640), (1020, 1640)], fill=GREY, width=6)
    tag(d, 790, 690, '???', 90, WH, INK, pad=24, outline=INK)
    plates(d, 290, ['Я ЕГО', 'НЕ БРАЛ'], 124)
    return bg
def cover_b():   # человечек с замком, мошенник получает отказ
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    hood(d, 830, 1640, 1.6)
    fr = Image.open('ckadry/cv/000.png').convert('RGB')
    s = 0.66; bg = place(bg, fr, s, 360 - 540 * s, 1640 - 1600 * s)
    d = ImageDraw.Draw(bg); d.line([(60, 1640), (1020, 1640)], fill=GREY, width=6)
    lock(d, 360, 1230, 1.9)
    tag(d, 760, 1400, 'КРЕДИТ', 50, WH, INK, pad=18, outline=INK)
    im = Image.new('RGBA', (460, 190), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([6, 6, 453, 183], radius=16, outline=RED, width=12); bb = dd.textbbox((0, 0), 'ОТКАЗ', font=F(120))
    dd.text(((460 - bb[2] + bb[0]) / 2 - bb[0], (190 - bb[3] + bb[1]) / 2 - bb[1]), 'ОТКАЗ', font=F(120), fill=RED)
    im = im.rotate(12, Image.BICUBIC, expand=True); bg.paste(im, (545, 840), im)
    plates(ImageDraw.Draw(bg), 290, ['КРЕДИТ', 'БЕЗ ТЕБЯ?'], 124)
    return bg
for k, f in (('a-ne-bral', cover_a), ('b-zamok', cover_b)): f().save(f'oblozhka-samozapret-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-ne-bral', 'b-zamok')): sh.paste(guide(Image.open(f'oblozhka-samozapret-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
