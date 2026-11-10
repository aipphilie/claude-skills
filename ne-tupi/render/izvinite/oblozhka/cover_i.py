from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
RED = (226, 48, 48); DG = (150, 150, 150); LG = (225, 222, 215)
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20, outline=None, rot=0, base=None):
    f = F(sz); bb = d.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=12, fill=fill, outline=outline, width=5 if outline else 0)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=f, fill=col)
def door(d, x0, x1, top, bot):
    d.rectangle([x0 - 22, top - 22, x1 + 22, bot], fill=GREY)
    d.rectangle([x0, top, x1, bot], fill=WH, outline=INK, width=12)
    m = (top + bot) / 2
    for a, b in ((top + 50, m - 25), (m + 25, bot - 50)): d.rectangle([x0 + 40, a, x1 - 40, b], outline=INK, width=7)
    d.ellipse([x0 + 22, m - 20, x0 + 62, m + 20], fill=YEL, outline=INK, width=6)
def cover_a():   # кланяется двери, над головой счётчик
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    door(d, 730, 960, 820, 1612)
    d.line([(60, 1612), (1020, 1612)], fill=GREY, width=6)
    fr = Image.open('ckadry/cv/000.png').convert('RGB')
    bg = place(bg, fr, 0.62, 360 - 540 * 0.62, 1612 - 1600 * 0.62)
    d = ImageDraw.Draw(bg)
    tag(d, 420, 830, 'ИЗВИНИТЕ ×10', 60, INK, WH, pad=24)
    plates(d, 330, ['ХВАТИТ', 'ИЗВИНЯТЬСЯ'], 124)
    return bg
def cover_b():   # разводит руками в облаке «извините»
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    for x, y, s in ((210, 820, 40), (850, 860, 36), (180, 1080, 34), (880, 1110, 40), (230, 1330, 36), (860, 1380, 34), (540, 760, 34)):
        tag(d, x, y, 'извините', s, WH, DG, pad=16, outline=LG)
    fr = Image.open('ckadry/cv/002.png').convert('RGB')
    bg = place(bg, fr, 0.62, 540 - 540 * 0.62, 1640 - 1600 * 0.62)
    d = ImageDraw.Draw(bg); plates(d, 330, ['А ЗА ЧТО?'], 140)
    tag(d, 540, 560, 'ты ничего не сломал', 48, INK, WH, pad=22)
    return bg
for k, f in (('a-hvatit', cover_a), ('b-za-chto', cover_b)): f().save(f'oblozhka-izvinite-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-hvatit', 'b-za-chto')): sh.paste(guide(Image.open(f'oblozhka-izvinite-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
