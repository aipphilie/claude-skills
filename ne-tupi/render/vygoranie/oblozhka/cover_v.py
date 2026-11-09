import sys, math
sys.argv = ['x']
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
RED = (226, 48, 48)
def batt(d, cx, cy, w, h, lvl, lw=18):
    d.rounded_rectangle([cx - w * .18, cy - h / 2 - h * .07, cx + w * .18, cy - h / 2 + 4], radius=8, fill=INK)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(w * .16), fill=WH, outline=INK, width=lw)
    pad = 30; ih = (h - 2 * pad) * lvl
    d.rounded_rectangle([cx - w / 2 + pad, cy + h / 2 - pad - ih, cx + w / 2 - pad, cy + h / 2 - pad], radius=8, fill=RED)
def cover_a():   # поникший человечек и пустая батарейка
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    batt(d, 830, 1200, 240, 450, 0.05)
    tb = d.textbbox((0, 0), '3%', font=F(110)); d.text((830 - (tb[2] - tb[0]) / 2, 1480), '3%', font=F(110), fill=RED)
    fr = Image.open('ckadry/c2/000.png').convert('RGB')
    bg = place(bg, fr, 0.66, 430 - 540 * 0.66, 1640 - 1595 * 0.66)
    d = ImageDraw.Draw(bg); plates(d, 300, ['ОТПУСК', 'НЕ ПОМОЖЕТ'], 130)
    return bg
def palm(d, cx, cy, s):
    d.ellipse([cx - 230 * s, cy + 190 * s, cx + 230 * s, cy + 260 * s], fill=YEL)
    pts = [(cx + math.sin(k / 10 * 1.2) * 50 * s, cy + 220 * s - k * 34 * s) for k in range(11)]
    d.line(pts, fill=INK, width=int(30 * s), joint='curve'); tx, ty = pts[-1]
    for a in (-160, -120, -60, -20, 200):
        r = math.radians(a); ex, ey = tx + math.cos(r) * 190 * s, ty + math.sin(r) * 70 * s + 60 * s
        d.line([(tx, ty), ((tx + ex) / 2, min(ty, ey) - 40 * s), (ex, ey)], fill=INK, width=int(24 * s), joint='curve')
def cover_b():   # стоит у пальмы в отпуске, а над головой батарейка на нуле
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    palm(d, 790, 1230, 1.25)
    fr = Image.open('ckadry/c2/003.png').convert('RGB')
    bg = place(bg, fr, 0.66, 360 - 540 * 0.66, 1640 - 1595 * 0.66)
    d = ImageDraw.Draw(bg); batt(d, 360, 720, 120, 210, 0.06, lw=12)
    plates(d, 300, ['СИЛ НОЛЬ'], 150)
    return bg
for k, f in (('a-otpusk', cover_a), ('b-palma', cover_b)): f().save(f'oblozhka-vygoranie-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-otpusk', 'b-palma')): sh.paste(guide(Image.open(f'oblozhka-vygoranie-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
