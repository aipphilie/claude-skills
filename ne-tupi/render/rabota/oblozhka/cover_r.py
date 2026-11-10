from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
RED = (226, 48, 48); DG = (150, 150, 150); LG = (225, 222, 215)
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20, outline=None):
    f = F(sz); bb = d.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=12, fill=fill, outline=outline, width=5 if outline else 0)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=f, fill=col)
def cage(d, cx, top, bot, hw, lw=14):
    d.rectangle([cx - hw - 14, bot - 8, cx + hw + 14, bot + 14], fill=INK)
    d.rectangle([cx - hw - 14, top - 14, cx + hw + 14, top + 8], fill=INK)
    d.arc([cx - 170, top - 100, cx + 170, top + 100], 180, 360, fill=INK, width=lw)
    gap0 = cx + hw - 210; x = cx - hw
    while x <= cx + hw + 1:
        if not (gap0 < x < cx + hw): d.line([x, top, x, bot], fill=INK, width=lw)
        x += 80
    hx = cx + hw; w = 175
    d.polygon([(hx, top + 14), (hx + w, top + 70), (hx + w, bot - 56), (hx, bot)], outline=INK, width=lw)
    for j in (1, 2): xx = hx + w * j / 3; d.line([xx, top + 14 + 56 * j / 3, xx, bot - 56 * j / 3], fill=INK, width=lw - 2)
def chair(d, ox, oy, s):   # стул как в «Зарплате», в координатах кадра персонажа
    w = 16
    for (a, b) in (((735, 1300), (790, 860)),): d.line([a, b], fill=INK, width=w + 6)
    d.rounded_rectangle([450, 1285, 790, 1320], radius=10, fill=WH, outline=INK, width=w)
    for x0, x1 in ((480, 470), (760, 780)): d.line([(x0, 1320), (x1, 1610)], fill=INK, width=w)
def cover_a():   # сидит на стуле в клетке, дверца открыта
    fr = Image.open('ckadry/cv/000.png').convert('RGB')
    ch = Image.new('RGB', (WD, HT), WH); chair(ImageDraw.Draw(ch), 0, 0, 1); fr = mul(ch, fr)
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    cage(d, 470, 830, 1575, 330)
    s = 0.58; bg = place(bg, fr, s, 470 - 600 * s + 50, 1640 - 1610 * s - 70)
    d = ImageDraw.Draw(bg)
    tag(d, 900, 800, 'ВЫХОД', 44, INK, WH, pad=18)
    d.line([(900, 835), (900, 900)], fill=INK, width=10); d.polygon([(880, 895), (920, 895), (900, 925)], fill=INK)
    tag(d, 300, 720, 'ТЕРПИШЬ: 5 ЛЕТ', 46, WH, DG, pad=18, outline=LG)
    plates(d, 290, ['ДВЕРЬ', 'ОТКРЫТА'], 124)
    return bg
def cover_b():   # плетётся в офис в 7 утра
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    x0, x1, top, bot = 690, 960, 820, 1640
    d.rectangle([x0 - 22, top - 22, x1 + 22, bot], fill=GREY)
    d.rectangle([x0, top, x1, bot], fill=WH, outline=INK, width=12)
    d.ellipse([x0 + 24, 1220, x0 + 64, 1260], fill=YEL, outline=INK, width=6)
    tag(d, (x0 + x1) / 2, 920, 'ОФИС', 54, INK, WH, pad=20)
    cx, cy = 230, 820
    for ex in (-1, 1): d.ellipse([cx + ex * 95 - 38, cy - 150, cx + ex * 95 + 38, cy - 84], fill=INK)
    d.ellipse([cx - 125, cy - 125, cx + 125, cy + 125], fill=WH, outline=INK, width=14)
    w = d.textbbox((0, 0), '07:00', font=F(70))[2]; d.text((cx - w / 2, cy - 45), '07:00', font=F(70), fill=RED)
    fr = Image.open('ckadry/cv/001.png').convert('RGB')
    s = 0.62; bg = place(bg, fr, s, 400 - 540 * s, 1640 - 1600 * s)
    d = ImageDraw.Draw(bg)
    d.line([(60, 1640), (1020, 1640)], fill=GREY, width=6)
    plates(d, 290, ['НЕНАВИЖУ,', 'НО ИДУ'], 124)
    return bg
for k, f in (('a-dver', cover_a), ('b-nenavizhu', cover_b)): f().save(f'oblozhka-rabota-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-dver', 'b-nenavizhu')): sh.paste(guide(Image.open(f'oblozhka-rabota-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
