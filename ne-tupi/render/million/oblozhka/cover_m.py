"""Обложки рилса «Первый миллион тяжелее всех» (единый стиль: белый фон, чёрное + жёлтые плашки)."""
import json, math
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/zarplata/oblozhka/cover2.py').read().split("# A: сидит")[0])
LG = (232, 230, 225); DG = (150, 150, 150)
A = json.load(open('ckadry/cv/anchors.json'))
def bagimg(w, text):
    k = 3; W_ = int(w * k); H_ = int(w * 1.1 * k); pad = int(w * 0.1 * k)
    im = Image.new('RGBA', (W_ + 2 * pad, H_ + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ox = oy = pad; lw = int(w * 0.04 * k)
    d.rounded_rectangle((ox + W_ * .30, oy + H_ * .04, ox + W_ * .70, oy + H_ * .26), radius=int(W_ * .08), fill=YEL, outline=INK, width=lw)
    d.rounded_rectangle((ox + W_ * .03, oy + H_ * .22, ox + W_ * .97, oy + H_), radius=int(W_ * .36), fill=YEL, outline=INK, width=lw)
    d.line((ox + W_ * .33, oy + H_ * .22, ox + W_ * .67, oy + H_ * .22), fill=INK, width=lw * 2)
    if text:
        lines = text.split('\n'); sz = int(W_ * .3); f = F(sz)
        while max(d.textlength(t, font=f) for t in lines) > W_ * .8: sz -= 3; f = F(sz)
        d.multiline_text((ox + W_ / 2, oy + H_ * .63), text, font=f, fill=INK, anchor='mm', align='center', spacing=int(sz * .1))
    return im.resize((im.width // k, im.height // k), Image.LANCZOS)
def put(bg, im, cx, cy, rot=0):
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    bg.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)
def walker(bg, cx, ground, w, text):
    d = ImageDraw.Draw(bg); lw = max(5, int(w * .07)); by = ground - w * .42 - w * .55
    for sgn, p in ((-1, .6), (1, -.6)):
        x0 = cx + sgn * w * .18; d.line([x0, by + w * .45, x0 + p * w * .16, ground], fill=INK, width=lw)
    put(bg, bagimg(w, text), cx, by)
def cover_a(idx=0):   # тащит огромный мешок в гору
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg)
    x0, y0, x1, y1 = -60, 1700, 1140, 1080
    d.polygon([(x0, y0), (x1, y1), (x1, HT), (x0, HT)], fill=LG); d.line([(x0, y0), (x1, y1)], fill=INK, width=10)
    s = 0.62; cx = 600; feet = y0 + (cx - x0) * (y1 - y0) / (x1 - x0)
    dx, dy = cx - 540 * s, feet + 40 * s - 1600 * s - 60 * s
    a = A[idx]['back']; bx, by = dx + a[0] * s, dy + a[1] * s; bw = 470
    put(bg, bagimg(bw, '1 000 000 ₽'), bx - bw * .66, by - bw * .02, rot=10)
    fr = Image.open(f'ckadry/cv/{idx:03d}.png').convert('RGB')
    bg = place(bg, fr, s, dx, dy); d = ImageDraw.Draw(bg)
    t = A[idx]['top']; hx, hy = dx + t[0] * s, dy + t[1] * s
    for j, (ox, oy) in enumerate(((60, 40), (100, 0), (90, 90))):
        d.ellipse([hx + ox - 12, hy + oy - 18, hx + ox + 12, hy + oy + 18], fill=(120, 170, 230))
    plates(d, 300, ['САМЫЙ', 'ТЯЖЁЛЫЙ'], 130)
    return bg
def cover_b():   # мешки на ножках тащат десятый, он налегке
    bg = Image.new('RGB', (WD, HT), WH); d = ImageDraw.Draw(bg); g = 1640
    w = 104
    for j in range(4): walker(bg, 590 + j * 112, g, w, '')
    put(bg, bagimg(400, '10 МЛН'), 758, g - w * 1.5 - 205)
    fr = Image.open('ckadry/cv/002.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 250 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['ДЕСЯТЫЙ', 'ЛЕГЧЕ'], 130)
    return bg
for k, f in (('a-tyazhely', cover_a), ('b-desyatyy', cover_b)): f().save(f'oblozhka-million-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-tyazhely', 'b-desyatyy')): sh.paste(guide(Image.open(f'oblozhka-million-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
