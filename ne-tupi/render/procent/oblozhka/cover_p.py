"""Обложки A/B: белый фон, чёрное + жёлтые плашки (стиль обложек канала), сюжет — гора и монеты."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import compose_p as C
YEL = (255, 214, 10); INK = C.INK; OR = C.OR; RED = C.RED
W, H = 1080, 1920
def F(sz): return ImageFont.truetype(C.FB, sz)
def ch(i, s):  # кадр персонажа (белый фон) -> слой для multiply
    im = Image.open(f'kadry/main/{i:03d}.png').convert('RGB').crop(C.CH_CROP); return im.resize((int(1080 * s), int(1600 * s)), Image.LANCZOS)
def mult(img, chim, cx, feet, s):
    layer = Image.new('RGB', (W, H), 'white'); layer.paste(chim, (int(cx - chim.width / 2), int(feet + 70 * s - chim.height)))
    return Image.fromarray((np.asarray(img, np.float32) * np.asarray(layer, np.float32) / 255).astype(np.uint8))
def ptext(d, cx, y, s, sz, bg=None, fg=INK, rot=0, img=None):
    f = F(sz); w = d.textlength(s, font=f)
    if bg:
        p = Image.new('RGBA', (int(w + 60), int(sz * 1.35)), (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.rounded_rectangle([0, 0, p.width - 1, p.height - 1], radius=18, fill=bg); pd.text((30, p.height / 2), s, font=f, fill=fg, anchor='lm')
        p = p.rotate(rot, Image.BICUBIC, expand=True); img.paste(p, (int(cx - p.width / 2), int(y)), p)
    else: d.text((cx, y), s, font=f, fill=fg, anchor='ma')
def mountain(img, top=1350, gnd=1700, sx=430):
    d = ImageDraw.Draw(img); pts = [(-10, gnd), (sx, top), (W + 10, gnd + 60)]
    d.polygon(pts + [(W + 10, H), (-10, H)], fill=(232, 229, 223)); d.line(pts, fill=INK, width=10, joint='curve')
    return lambda x: gnd - (gnd - top) * x / sx if x <= sx else top + (gnd + 60 - top) * (x - sx) / (W - sx)
def coinp(img, cx, cy, r, lab, rot=0):
    im = C.coin_img(r, lab, rot); img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def cover_a():
    img = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(img)
    ptext(d, W / 2, 360, 'ДЕСЯТЫЙ', 170)
    ptext(d, W / 2, 560, 'ЗА 8 МЕСЯЦЕВ', 118, YEL, INK, -2, img)
    ptext(d, W / 2, 760, 'а первый — почти 3 года', 52, fg=(140, 140, 140))
    sl = mountain(img)
    # слева тащит 1 млн
    x = 230; img = mult(img, ch(36, 0.32), x, sl(x) + 4, 0.32); d = ImageDraw.Draw(img)
    coinp(img, x - 85, sl(x) - 290, 85, '1 МЛН', 10)
    ptext(d, 200, 900, '34 МЕС', 70, fg=RED)
    # справа: монета 10 млн катится, человечек сверху
    cx = 800; r = 150; cy = sl(cx) - r - 10
    for j in range(3): d.line([cx - r - 40 - j * 30, cy - 60 + j * 70, cx - r - 150 - j * 30, cy - 120 + j * 70], fill=(160, 160, 160), width=9)
    coinp(img, cx, cy, r, '10 МЛН', -18)
    img = mult(img, ch(96, 0.26), cx, cy - r + 6, 0.26); d = ImageDraw.Draw(img)
    ptext(d, 800, 830, '8 МЕС', 70, fg=OR)
    img.save('oblozhka-a-desyatyy-8-mes.png')

def cover_b():
    img = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(img)
    ptext(d, W / 2, 330, '25 000 В МЕСЯЦ', 96)
    ptext(d, W / 2, 470, '→ 10 МЛН', 150, YEL, INK, -2, img)
    ptext(d, W / 2, 700, 'за сколько лет?', 60, fg=(140, 140, 140))
    # график-кривая
    x0, x1, y0, y1 = 120, 900, 1060, 1560; M = C.MARK[10]
    pts = [(x0 + (x1 - x0) * m / M, y1 - (y1 - y0) * C.bal[m] / C.bal[M]) for m in range(M + 1)]
    mid = [(x0 + (x1 - x0) * m / M, y1 - (y1 - y0) * C.own[m] / C.bal[M]) for m in range(M + 1)]
    d.polygon(pts + mid[::-1], fill=OR); d.polygon(mid + [(x1, y1), (x0, y1)], fill=C.OWN)
    d.line(pts, fill=INK, width=10, joint='curve'); d.line([x0, y1, x1 + 20, y1], fill=INK, width=8)
    for j in range(1, 11):
        m = C.MARK[j]; x, y = pts[m]; d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=RED if j == 1 else (OR if j == 10 else INK), outline='white', width=5)
    ptext(d, 300, 1600, 'свои 4 млн', 46); ptext(d, 700, 1600, 'проценты 6 млн', 46, fg=OR)
    img = mult(img, ch(36, 0.22), x1 - 20, y0 + 6, 0.22)
    coinp(img, x1 - 75, y0 - 200, 58, '₽', 10)
    img.save('oblozhka-b-25k-10mln.png')
cover_a(); cover_b()
