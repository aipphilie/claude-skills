"""Карусель Threads «Самозапрет на кредиты»: 9 слайдов 1080x1350 (4:5).
Запуск: python3 slides.py <папка с кадрами человечка kadry/p/NNN.png> <выходная папка>
Кадры позы рендерятся из poses.json через ../../3d/frames.js (см. README.md)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
KD, OUT = sys.argv[1], sys.argv[2]
W, H = 1080, 1350; INK = (17, 17, 17); WH = (255, 255, 255); YEL = (255, 214, 10); GREY = (217, 217, 217)
DG = (130, 130, 130); LG = (232, 229, 222); RED = (226, 48, 48); GRN = (40, 160, 80)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FM = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
if not os.path.exists(FX): FX = FB
N = 9
def F(sz, f=FB): return ImageFont.truetype(f, sz)
def mul(a, b): return Image.fromarray((np.asarray(a, np.uint16) * np.asarray(b, np.uint16) // 255).astype(np.uint8))
def man(bg, pose, cx, floor, s):          # человечек: кадр 1080x1920, ноги ~y1600, центр x540
    fr = Image.open(f'{KD}/{pose:03d}.png').convert('RGB')
    im = fr.resize((int(1080 * s), int(1920 * s)), Image.LANCZOS)
    lay = Image.new('RGB', (W, H), WH); lay.paste(im, (int(cx - 540 * s), int(floor - 1600 * s)))
    return mul(bg, lay)
def tw(d, t, f): b = d.textbbox((0, 0), t, font=f); return b[2] - b[0]
def plates(d, y, lines, sz, fill=YEL, color=INK, pad=22, x=None):
    f = F(sz)
    for l in lines:
        bb = d.textbbox((0, 0), l, font=f); w, h = bb[2] - bb[0], sz * 0.78
        xx = (W - w) / 2 if x is None else x + pad
        d.rounded_rectangle([xx - pad, y - pad * .7, xx + w + pad, y + h + pad * .7], radius=12, fill=fill)
        d.text((xx - bb[0], y - bb[1] + (h - (bb[3] - bb[1])) / 2), l, font=f, fill=color); y += h + pad * 1.4 + 12
    return y
def para(d, y, lines, sz=40, f=FM, col=INK, x=None):
    fo = F(sz, f)
    for l in lines:
        xx = (W - tw(d, l, fo)) / 2 if x is None else x
        d.text((xx, y), l, font=fo, fill=col); y += sz * 1.3
    return y
def tag(d, cx, cy, txt, sz, fill=WH, col=INK, pad=20, outline=INK, f=FB):
    fo = F(sz, f); bb = d.textbbox((0, 0), txt, font=fo); w, h = bb[2] - bb[0], sz * 0.78
    d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * .7, cx + w / 2 + pad, cy + h / 2 + pad * .7], radius=14, fill=fill, outline=outline, width=5 if outline else 0)
    d.text((cx - w / 2 - bb[0], cy - h / 2 - bb[1] + (h - (bb[3] - bb[1])) / 2), txt, font=fo, fill=col)
    return cx - w / 2 - pad, cx + w / 2 + pad
def floor_line(d, y, x0=60, x1=1020): d.line([(x0, y), (x1, y)], fill=GREY, width=6)
def lock(d, cx, cy, s, opened=0.0):
    w, h = 120 * s, 100 * s; r = 38 * s; lift = 34 * s * opened; top = cy - h / 2; lw = int(16 * s)
    d.arc([cx - r, top - r * 1.25 - lift, cx + r, top + r * 0.9 - lift], 180, 360, fill=INK, width=lw)
    d.line([cx - r + 7 * s, top - r * 0.2 - lift, cx - r + 7 * s, top + 6 * s], fill=INK, width=lw)
    if opened < 0.5: d.line([cx + r - 7 * s, top - r * 0.2, cx + r - 7 * s, top + 6 * s], fill=INK, width=lw)
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, top + h], radius=int(18 * s), fill=YEL, outline=INK, width=int(8 * s))
    d.ellipse([cx - 13 * s, cy - 20 * s, cx + 13 * s, cy + 6 * s], fill=INK); d.rectangle([cx - 5 * s, cy, cx + 5 * s, cy + 26 * s], fill=INK)
def phone(d, x0, top, x1, bot):
    d.rounded_rectangle([x0, top, x1, bot], radius=52, fill=WH, outline=INK, width=13)
    cx = (x0 + x1) / 2; d.rounded_rectangle([cx - 56, top + 26, cx + 56, top + 44], radius=9, fill=INK)
def notif(d, x0, y0, x1, who, title, line, col, dot=RED):
    d.rounded_rectangle([x0, y0, x1, y0 + 200], radius=26, fill=LG, outline=INK, width=6)
    d.ellipse([x0 + 18, y0 + 18, x0 + 62, y0 + 62], fill=dot, outline=INK, width=4)
    d.text((x0 + 76, y0 + 22), who, font=F(28), fill=DG)
    d.text((x0 + 20, y0 + 82), title, font=F(30), fill=INK); d.text((x0 + 20, y0 + 126), line, font=F(48), fill=col)
def hood(d, cx, bot, s):
    c = (130, 130, 130)
    d.rounded_rectangle([cx - 70 * s, bot - 250 * s, cx + 70 * s, bot], radius=int(60 * s), fill=c)
    d.polygon([(cx - 86 * s, bot - 190 * s), (cx, bot - 345 * s), (cx + 86 * s, bot - 190 * s)], fill=c)
    d.ellipse([cx - 44 * s, bot - 262 * s, cx + 44 * s, bot - 178 * s], fill=(60, 60, 60))
def stamp(bg, txt, x, y, ang=12, sz=110, col=RED):
    f = F(sz); tmp = ImageDraw.Draw(bg); bb = tmp.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0] + 70, sz + 60
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([6, 6, w - 7, h - 7], radius=16, outline=col, width=11)
    dd.text(((w - bb[2] + bb[0]) / 2 - bb[0], (h - bb[3] + bb[1]) / 2 - bb[1]), txt, font=f, fill=col)
    im = im.rotate(ang, Image.BICUBIC, expand=True); bg.paste(im, (int(x - im.width / 2), int(y - im.height / 2)), im)
def footer(d, i, swipe=True):           # точки прогресса + «листай»
    r, g = 9, 30; x = 70
    for k in range(N):
        d.ellipse([x + k * g - r, 1290 - r, x + k * g + r, 1290 + r], fill=YEL if k == i else GREY, outline=INK if k == i else None, width=3)
    if swipe:
        f = F(34); t = 'листай →'; d.text((1010 - tw(d, t, f), 1268), t, font=f, fill=INK)
def check(d, cx, cy, s, col=INK):
    d.line([(cx - 30 * s, cy), (cx - 8 * s, cy + 24 * s), (cx + 34 * s, cy - 26 * s)], fill=col, width=int(12 * s), joint='curve')

def s1():   # хук
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['Я ЕГО', 'НЕ БРАЛ'], 118)
    phone(d, 70, 470, 500, 1230); notif(d, 92, 560, 478, 'БАНК', 'Вам одобрен кредит', '500 000 ₽', RED)
    bg = man(bg, 0, 790, 1210, 0.5); d = ImageDraw.Draw(bg); floor_line(d, 1210, 540, 1020)
    tag(d, 790, 520, '???', 76)
    footer(d, 0); return bg
def s2():   # ложный ответ + стоп
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 90, ['Думаешь, с тобой', 'такого не будет?'], 64, FB)
    bg = man(bg, 1, 330, 1080, 0.46); d = ImageDraw.Draw(bg); floor_line(d, 1080, 80, 600)
    x0, x1 = tag(d, 740, 520, 'Я ЖЕ', 64, outline=DG, col=DG); tag(d, 740, 620, 'ОСТОРОЖНЫЙ', 64, outline=DG, col=DG)
    d.line([(560, 650), (930, 480)], fill=RED, width=14)
    plates(d, 1130, ['СТОП. ТУТ ТЫ ТУПИШЬ'], 72)
    footer(d, 1); return bg
def box(d, cx, cy):
    d.rectangle([cx - 60, cy - 40, cx + 60, cy + 50], fill=WH, outline=INK, width=8); d.line([(cx - 60, cy - 40), (cx - 40, cy - 70), (cx + 80, cy - 70), (cx + 60, cy - 40)], fill=INK, width=8)
    d.line([(cx + 80, cy - 70), (cx + 80, cy + 20), (cx + 60, cy + 50)], fill=INK, width=8); d.line([(cx - 10, cy - 40), (cx - 10, cy + 50)], fill=YEL, width=14)
def cross(d, cx, cy):
    d.rounded_rectangle([cx - 22, cy - 66, cx + 22, cy + 66], radius=8, fill=INK); d.rounded_rectangle([cx - 66, cy - 22, cx + 66, cy + 22], radius=8, fill=INK)
def card(d, cx, cy):
    d.rounded_rectangle([cx - 80, cy - 52, cx + 80, cy + 52], radius=14, fill=YEL, outline=INK, width=8); d.text((cx - 62, cy - 34), '-5%', font=F(52), fill=INK)
def drip(d, cx, y):
    for k, dx in enumerate((-30, 10, 40)):
        yy = y + k * 18; d.ellipse([cx + dx - 11, yy, cx + dx + 11, yy + 26], fill=INK); d.polygon([(cx + dx - 10, yy + 10), (cx + dx, yy - 12), (cx + dx + 10, yy + 10)], fill=INK)
def s3():   # слил не ты
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['СЛИЛ НЕ ТЫ'], 112)
    para(d, 270, ['Твои данные, скорее всего, уже утекли'], 42)
    bg = man(bg, 3, 280, 1180, 0.46); d = ImageDraw.Draw(bg); floor_line(d, 1180, 70, 500)
    for (fn, lab), y in zip(((box, 'доставка'), (cross, 'аптека'), (card, 'скидочная\nкарта')), (470, 720, 970)):
        fn(d, 640, y); drip(d, 640, y + 85); d.multiline_text((760, y - 26 - (26 if chr(10) in lab else 0)), lab, font=F(44, FM), fill=INK, spacing=6)
    footer(d, 2); return bg
def s4():   # защита есть
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 90, ['Нас этому не учили, но'], 52, FM, DG)
    plates(d, 190, ['ЗАЩИТА ЕСТЬ'], 112)
    bg = man(bg, 5, 300, 1180, 0.5); d = ImageDraw.Draw(bg); floor_line(d, 1180, 70, 1010)
    for t, y in (('1 ГАЛОЧКА', 560), ('0 ₽', 760), ('2 МИНУТЫ', 960)): tag(d, 780, y, t, 78, fill=YEL, outline=INK, pad=26)
    footer(d, 3); return bg
def s5():   # как поставить
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['КАК ПОСТАВИТЬ'], 100)
    phone(d, 70, 300, 480, 1220)
    d.rounded_rectangle([96, 400, 454, 470], radius=35, fill=LG, outline=INK, width=5)
    d.ellipse([116, 418, 146, 448], outline=INK, width=5); d.line([(142, 444), (156, 458)], fill=INK, width=6)
    d.text((166, 416), 'самозапрет на', font=F(28, FM), fill=INK)
    d.text((110, 500), 'Самозапрет', font=F(40), fill=INK); d.text((110, 550), 'на кредиты', font=F(40), fill=INK)
    for k, (t, on) in enumerate((('Банки', 1), ('МФО', 1), ('Онлайн', 1))):
        y = 640 + k * 90; d.text((110, y), t, font=F(34, FM), fill=INK)
        d.rounded_rectangle([340, y - 4, 430, y + 44], radius=24, fill=YEL if on else GREY, outline=INK, width=4); d.ellipse([388, y + 2, 426, y + 38], fill=INK)
    d.rounded_rectangle([110, 960, 440, 1050], radius=20, fill=INK); d.text((150, 982), 'Установить', font=F(38), fill=WH)
    for k, (n, a, b) in enumerate((('1', 'Госуслуги', ''), ('2', 'В поиске:', '«самозапрет на кредиты»'), ('3', 'Установить', ''))):
        y = 360 + k * 230; d.ellipse([530, y, 610, y + 80], fill=YEL, outline=INK, width=5); d.text((556, y + 6), n, font=F(56), fill=INK)
        d.text((635, y + 6), a, font=F(52), fill=INK)
        if b: para(d, y + 76, ['«самозапрет', 'на кредиты»'], 40, FM, INK, x=635)
    d.text((530, 1050), 'Нет Госуслуг?', font=F(36), fill=INK); d.text((530, 1098), 'МФЦ с паспортом.', font=F(36, FM), fill=INK)
    d.text((530, 1146), 'Бесплатно.', font=F(36, FM), fill=INK)
    footer(d, 4); return bg
def s6():   # банк откажет
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['БАНК ОТКАЖЕТ'], 104)
    para(d, 260, ['любому, кто придёт за кредитом', 'на твоё имя'], 42)
    hood(d, 800, 1170, 1.45)
    bg = man(bg, 1, 300, 1170, 0.47); d = ImageDraw.Draw(bg); floor_line(d, 1170)
    lock(d, 300, 900, 1.6)
    tag(d, 800, 1000, 'КРЕДИТ', 44, pad=16)
    stamp(bg, 'ОТКАЗ', 790, 520, 10, 100); d = ImageDraw.Draw(bg)
    footer(d, 5, swipe=False); f = F(34); t = 'но есть подвох →'; x = 1010 - tw(d, t, f)
    d.rounded_rectangle([x - 16, 1258, 1026, 1322], radius=12, fill=YEL); d.text((x, 1268), t, font=f, fill=INK)
    return bg
def bubble(d, x0, y0, txt, right=False):
    f = F(36, FM); w = tw(d, txt, f) + 52
    if right: x0 -= w
    d.rounded_rectangle([x0, y0, x0 + w, y0 + 74], radius=30, fill=WH, outline=INK, width=5); d.text((x0 + 26, y0 + 14), txt, font=f, fill=INK)
def s7():   # подвох
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['А ВОТ И ПОДВОХ'], 100)
    para(d, 250, ['Запрет можно снять. И мошенники это знают'], 38)
    phone(d, 70, 360, 470, 1210)
    d.ellipse([200, 470, 340, 610], fill=GREY); d.text((235, 488), '?', font=F(90), fill=WH)
    d.text((145, 640), 'Неизвестный', font=F(40), fill=INK); d.text((190, 690), 'номер', font=F(40), fill=INK)
    d.ellipse([110, 1030, 210, 1130], fill=RED); d.ellipse([330, 1030, 430, 1130], fill=GRN)
    bubble(d, 500, 370, '«Снимите запрет'); bubble(d, 500, 450, 'для проверки»')
    bubble(d, 500, 570, '«Это для защиты'); bubble(d, 500, 650, 'вашего счёта»')
    bg = man(bg, 2, 800, 1210, 0.3); d = ImageDraw.Draw(bg); floor_line(d, 1210, 560, 1020)
    lock(d, 800, 1040, 1.0, opened=1)
    footer(d, 6); return bg
def s8():   # правило
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['ПРОСЯТ СНЯТЬ', '= МОШЕННИК'], 104)
    para(d, 410, ['Всегда. Кто бы ни звонил:', '«банк», «Госуслуги», «полиция»'], 42)
    bg = man(bg, 4, 280, 1170, 0.42); d = ImageDraw.Draw(bg); floor_line(d, 1170, 70, 470)
    d.rounded_rectangle([520, 600, 1020, 1170], radius=28, fill=LG)
    para(d, 630, ['Нужен кредит', 'самому?'], 46, FB, INK, x=555)
    lock(d, 600, 900, 0.75, 1); d.text((660, 870), '→', font=F(60), fill=INK)
    d.rounded_rectangle([735, 860, 850, 925], radius=10, fill=YEL, outline=INK, width=5); d.text((774, 866), '₽', font=F(44), fill=INK)
    d.text((865, 870), '→', font=F(60), fill=INK); lock(d, 965, 900, 0.75)
    para(d, 1000, ['Снял, взял,', 'поставил обратно'], 40, FM, INK, x=555)
    footer(d, 7); return bg
def s9():   # кольцо
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['ПОСТАВЬ СЕГОДНЯ'], 96)
    para(d, 240, ['и перешли родителям'], 48, FM)
    phone(d, 70, 400, 500, 1180); notif(d, 92, 490, 478, 'БАНК', 'В кредите', 'ОТКАЗАНО', INK, dot=GRN)
    bg = man(bg, 1, 790, 1180, 0.47); d = ImageDraw.Draw(bg); floor_line(d, 1180, 540, 1020)
    lock(d, 790, 900, 1.5)
    tag(d, 790, 1240, 'ВСЁ. НЕ ТУПИ.', 52, fill=YEL, outline=None, pad=18)
    return bg
os.makedirs(OUT, exist_ok=True)
for i, f in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9), 1): f().save(f'{OUT}/slide-{i:02d}.png')
sh = Image.new('RGB', (5 * 330 + 60, 2 * 412 + 30), (40, 40, 40))
for i in range(9):
    im = Image.open(f'{OUT}/slide-{i + 1:02d}.png').resize((324, 405)); sh.paste(im, (10 + (i % 5) * 340, 10 + (i // 5) * 420))
sh.save(f'{OUT}/obzor.png')
