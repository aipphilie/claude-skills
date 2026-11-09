"""Обложки 1080x1920 для «Кофе тебя не разоряет». Главное в центре 1080x1440 (сетка профиля режет до 3:4)."""
import numpy as np
from PIL import Image, ImageDraw
import compose as c
WD, HT, SS = 1080, 1920, c.SS
def char(bg, idx, cx, feet, s):
    cw, chh = int(1080 * s), int(1360 * s)
    ch = Image.open(f'ckadry/cover/{idx:03d}.png').convert('RGB').crop(c.CH_CROP).resize((cw, chh), Image.LANCZOS)
    layer = Image.new('RGB', (WD, HT), (255, 255, 255)); layer.paste(ch, (int(cx - cw / 2), int(feet + 70 * s - chh)))
    return Image.fromarray((np.asarray(bg, np.uint16) * np.asarray(layer, np.uint16) // 255).astype(np.uint8))
def overlay(img, fn):
    F = Image.new('RGBA', (WD * SS, HT * SS), (0, 0, 0, 0)); fn(F)
    out = img.convert('RGBA'); out.alpha_composite(F.resize((WD, HT), Image.LANCZOS)); return out.convert('RGB')
def grid_guide(img):   # превью: как обрежется в сетке
    g = img.copy(); d = ImageDraw.Draw(g, 'RGBA'); d.rectangle([0, 0, WD, 240], fill=(0, 0, 0, 120)); d.rectangle([0, 1680, WD, HT], fill=(0, 0, 0, 120)); return g

# A: преступник у ростовой доски
def cover_a():
    bg = Image.new('RGB', (WD, HT), c.BG); ov = Image.new('RGB', (WD, HT), c.BG); d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, WD // 2, HT], fill=(255, 150, 150)); d.rectangle([WD // 2, 0, WD, HT], fill=(165, 185, 255))
    bg = Image.blend(bg, ov, 0.35)
    s, feet = 0.82, 1640
    c.PXCM_FEET, c.PXCM = feet, 1241 * s / 180; c.board(bg, 99)
    bg = char(bg, 0, 540, feet, s)
    def fg(F):
        c.plate(F, 9, 0, 'ПРЕСТУПНИК', 540, feet - 0.54 * 1241 * s, 58, c.RED, c.WHITE, rot=-3)
        c.cup(F, 540 + 330 * s / 0.9, feet - 0.45 * 1241 * s, 105, rot=-10)
        c.plate(F, 9, 0, 'ТЫ БЕДНЫЙ\nИЗ-ЗА КОФЕ?', 540, 400, 92, c.YEL, c.INK, rot=-2)
    return overlay(bg, fg)

# B: весы
def cover_b():
    bg = Image.new('RGB', (WD, HT), c.BG)
    G = Image.new('RGBA', (WD * SS, c.GH * SS), (0, 0, 0, 0)); c.scales(G, c.T['nu'] + 0.6, 1.1)
    G = G.resize((WD, c.GH), Image.LANCZOS); bg.paste(G, (0, 330), G)
    bg = char(bg, 1, 250, 1650, 0.42)
    return overlay(bg, lambda F: c.plate(F, 9, 0, 'КОФЕ НЕ ВИНОВАТ', 540, 330, 80, c.YEL, c.INK, rot=-2))

# C: жёлтый фон, крупный заголовок
def cover_c():
    bg = Image.new('RGB', (WD, HT), c.YEL)
    d = ImageDraw.Draw(bg); f = c.ImageFont.truetype(c.FB, 150)
    for i, l in enumerate(['КОФЕ', 'ТЕБЯ НЕ', 'РАЗОРЯЕТ']):
        w = d.textbbox((0, 0), l, font=f)[2]; d.text(((WD - w) / 2, 300 + i * 170), l, font=f, fill=c.INK)
    bg = char(bg, 2, 540, 1640, 0.55)
    return bg

if __name__ == '__main__':
    outs = {'a-prestupnik': cover_a(), 'b-vesy': cover_b(), 'c-zagolovok': cover_c()}
    sheet = Image.new('RGB', (3 * 360 + 40, 640), (40, 40, 40))
    for i, (k, im) in enumerate(outs.items()):
        im.save(f'oblozhka-{k}.png'); sheet.paste(grid_guide(im).resize((360, 640)), (10 + i * 370, 0))
    sheet.save('oblozhki-obzor.png')

def cover_c_white():
    bg = Image.new('RGB', (WD, HT), (255, 255, 255))
    d = ImageDraw.Draw(bg); f = c.ImageFont.truetype(c.FB, 150)
    for i, l in enumerate(['КОФЕ', 'ТЕБЯ НЕ', 'РАЗОРЯЕТ']):
        w = d.textbbox((0, 0), l, font=f)[2]; d.text(((WD - w) / 2, 300 + i * 170), l, font=f, fill=c.INK)
    return char(bg, 2, 540, 1640, 0.55)
