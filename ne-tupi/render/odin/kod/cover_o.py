"""Обложки «Почему он не пускает близко»: белый фон, жёлтые плашки, сюжетная сцена (стиль обложек канала)."""
from PIL import Image, ImageDraw, ImageFont
import compose_o as c
WD, HT = 1080, 1920; WH = (255, 255, 255); G = 1640
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
def plates(d, y, lines, sz, fill=c.YEL, color=c.INK, gap=14, pad=24):
    f = ImageFont.truetype(FB, sz)
    for l in lines:
        bb = d.textbbox((0, 0), l, font=f); w, h = bb[2] - bb[0], sz * 0.78; x = (WD - w) / 2
        d.rounded_rectangle([x - pad, y - pad * 0.7, x + w + pad, y + h + pad * 0.7], radius=12, fill=fill)
        d.text((x - bb[0], y - bb[1] + (h - (bb[3] - bb[1])) / 2), l, font=f, fill=color); y += h + pad * 1.4 + gap
def base(): return Image.new('RGBA', (WD, HT), WH + (255,))
def line(bg): ImageDraw.Draw(bg).line([(60, G), (1020, G)], fill=(150, 150, 150), width=6)
def cover_a():   # он за стеной из «своего покоя», она снаружи с сердцем
    bg = base(); line(bg)
    w = Image.new('RGBA', (600, 400), (0, 0, 0, 0)); c.wall(w, 300, 380, 11, 0); w = w.resize((810, 540), Image.LANCZOS)
    c.man(bg, 'idle_sad', 0, 640, G, 0.74)
    bg.alpha_composite(w, (640 - 405, G - 513))
    c.man(bg, 'g_wave', 0.5, 150, G, 0.56); c.heart(bg, 330, 900, 80)
    plates(ImageDraw.Draw(bg), 300, ['ОН НЕ', 'ХОЛОДНЫЙ'], 140); return bg.convert('RGB')
def cover_b():   # рыцарь: свобода как броня, сердца отскакивают
    bg = base(); line(bg); c.man(bg, 'hips', 0, 540, G, 0.78); c.armor(bg, 540, G, 0.78, 0, 1.0)
    for x, y, r, rot in ((190, 900, 80, 20), (900, 1010, 70, -25), (230, 1330, 56, -15), (880, 1420, 50, 30)):
        c.burst(bg, x + (70 if x < 540 else -70), y + 20, r * 0.9, 0, fill=c.YEL, n=9); c.heart(bg, x, y, r, rot=rot, crack=1)
    plates(ImageDraw.Draw(bg), 300, ['СВОБОДА', '= БРОНЯ'], 140); return bg.convert('RGB')
O = '../oblozhka/'
A, B = cover_a(), cover_b(); A.save(O + 'oblozhka-odin-a-ne-holodnyy.png'); B.save(O + 'oblozhka-odin-b-bronya.png')
sh = Image.new('RGB', (750, 640), (40, 40, 40))
for i, im in enumerate((A, B)):
    g = im.copy(); d = ImageDraw.Draw(g, 'RGBA'); d.rectangle([0, 0, WD, 240], fill=(0, 0, 0, 110)); d.rectangle([0, 1680, WD, HT], fill=(0, 0, 0, 110)); sh.paste(g.resize((360, 640)), (10 + i * 370, 0))
sh.save(O + 'obl-obzor.png')
