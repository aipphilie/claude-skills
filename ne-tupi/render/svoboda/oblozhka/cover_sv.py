"""Обложки рилса «Сколько нужно, чтобы больше не работать» (белый фон, чёрное + жёлтые плашки)."""
from PIL import Image, ImageDraw
exec(open('/mnt/project-files/ne-tupi-render/spyat/oblozhka/cover_s.py').read().split("def cover_a")[0])
STONE = (214, 210, 202); WATER = (120, 170, 220)
def well(bg, cx, g, w=420):
    d = ImageDraw.Draw(bg); x0, x1 = cx - w / 2, cx + w / 2; top = g - 300
    # стойки и крыша
    for px in (x0 + 30, x1 - 54): d.rectangle([px, top - 330, px + 24, top], fill=INK)
    d.polygon([(x0 - 30, top - 320), (cx, top - 440), (x1 + 30, top - 320)], fill=MID, outline=INK, width=10)
    d.line([(x0 + 40, top - 250), (x1 - 40, top - 250)], fill=INK, width=14)
    d.line([(cx, top - 250), (cx, top - 120)], fill=INK, width=5)
    # сруб из камней
    d.rounded_rectangle([x0, top, x1, g], radius=18, fill=STONE, outline=INK, width=10)
    for r in range(3):
        y = top + 20 + r * 95; off = 0 if r % 2 == 0 else 70
        for k in range(-1, 4):
            bx = x0 + off + k * 140
            if bx + 40 > x1 or bx + 120 < x0: continue
            d.rounded_rectangle([max(x0 + 12, bx), y, min(x1 - 12, bx + 125), y + 75], radius=14, outline=INK, width=6)
    d.ellipse([x0 - 10, top - 40, x1 + 10, top + 40], fill=STONE, outline=INK, width=10)
    d.ellipse([x0 + 30, top - 22, x1 - 30, top + 22], fill=WATER, outline=INK, width=6)
    return top
def bucket(bg, cx, cy, w, text):
    d = ImageDraw.Draw(bg); h = w * 0.85
    d.arc([cx - w * 0.45, cy - h * 0.95, cx + w * 0.45, cy - h * 0.05], 180, 360, fill=INK, width=9)
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w * 0.38, cy + h / 2), (cx - w * 0.38, cy + h / 2)], fill=YEL, outline=INK, width=10)
    f = F(int(w * 0.2)); d.text((cx, cy + 4), text, font=f, fill=INK, anchor='mm')
def cover_a():   # колодец с ведром «×300», человечек в шоке
    bg = Image.new('RGB', (WD, HT), WH); g = 1620
    top = well(bg, 720, g)
    bucket(bg, 720, top - 70, 250, 'МЕСЯЦ')
    fr = Image.open('ck/cv/000.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 230 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['РАСХОДЫ', '×300'], 150)
    return bg
def cover_b():   # огромный мешок «?», «ЦЕНА СВОБОДЫ»
    bg = Image.new('RGB', (WD, HT), WH); g = 1620
    put(bg, bagimg(400, '?'), 730, g - 270)
    fr = Image.open('ck/cv/001.png').convert('RGB'); s = 0.62
    bg = place(bg, fr, s, 250 - 540 * s, g + 40 * s - 1660 * s); d = ImageDraw.Draw(bg)
    d.line([(60, g), (1020, g)], fill=DG, width=6)
    plates(d, 300, ['ЦЕНА', 'СВОБОДЫ'], 150)
    return bg
for k, f in (('a-rashody-300', cover_a), ('b-cena-svobody', cover_b)): f().save(f'oblozhka-svoboda-{k}.png')
sh = Image.new('RGB', (2 * 370 + 10, 640), (40, 40, 40))
for i, k in enumerate(('a-rashody-300', 'b-cena-svobody')): sh.paste(guide(Image.open(f'oblozhka-svoboda-{k}.png')).resize((360, 640)), (10 + i * 370, 0))
sh.save('obl-obzor.png')
