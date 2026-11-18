"""Карусель Threads «Почему ты не уходишь с работы»: 9 слайдов 1080x1350 (4:5).
Запуск: python3 slides.py <kadry/p> <выходная папка>. Общие функции берутся из ../samozapret/slides.py."""
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'samozapret', 'slides.py')).read()
exec(_src.split('def s1():')[0])
def cage(d, cx, top, bot, hw, lw=13, door=True):
    d.rectangle([cx - hw - 14, bot - 8, cx + hw + 14, bot + 12], fill=INK)
    d.rectangle([cx - hw - 14, top - 12, cx + hw + 14, top + 8], fill=INK)
    d.arc([cx - 150, top - 90, cx + 150, top + 90], 180, 360, fill=INK, width=lw)
    gap0 = cx + hw - 190; x = cx - hw
    while x <= cx + hw + 1:
        if not (gap0 < x < cx + hw): d.line([x, top, x, bot], fill=INK, width=lw)
        x += 72
    hx = cx + hw; w = 150
    d.polygon([(hx, top + 12), (hx + w, top + 60), (hx + w, bot - 48), (hx, bot)], outline=INK, width=lw)
    for j in (1, 2): xx = hx + w * j / 3; d.line([xx, top + 12 + 48 * j / 3, xx, bot - 48 * j / 3], fill=INK, width=lw - 2)
def sit(bg, cx, floor, s):          # сидит на стуле (поза 10 + стул в координатах кадра)
    fr = Image.open(f'{KD}/010.png').convert('RGB')
    ch = Image.new('RGB', (1080, 1920), WH); c = ImageDraw.Draw(ch); w = 16
    c.line([(735, 1300), (790, 860)], fill=INK, width=w + 6)
    c.rounded_rectangle([450, 1285, 790, 1320], radius=10, fill=WH, outline=INK, width=w)
    for x0, x1 in ((480, 470), (760, 780)): c.line([(x0, 1320), (x1, 1610)], fill=INK, width=w)
    fr = mul(ch, fr); im = fr.resize((int(1080 * s), int(1920 * s)), Image.LANCZOS)
    lay = Image.new('RGB', (W, H), WH); lay.paste(im, (int(cx - 600 * s + 50 * s / .58), int(floor - 1610 * s)))
    return mul(bg, lay)
def lie(bg, cx, floor, s):          # лежит (поза 12, повернута на 90°)
    fr = Image.open(f'{KD}/012.png').convert('RGB').rotate(90, expand=True)
    im = fr.resize((int(1920 * s), int(1080 * s)), Image.LANCZOS)
    lay = Image.new('RGB', (W, H), WH); lay.paste(im, (int(cx - 975 * s), int(floor - 650 * s)))
    return mul(bg, lay)
def door(d, x0, x1, top, bot, label, col=INK, fg=WH):
    d.rectangle([x0 - 18, top - 18, x1 + 18, bot], fill=GREY); d.rectangle([x0, top, x1, bot], fill=WH, outline=INK, width=11)
    d.ellipse([x0 + 20, (top + bot) / 2, x0 + 54, (top + bot) / 2 + 34], fill=YEL, outline=INK, width=5)
    tag(d, (x0 + x1) / 2, top + 80, label, 38, col, fg, pad=14, outline=None)
def clock(d, cx, cy, r=95):
    for ex in (-1, 1): d.ellipse([cx + ex * r * .76 - 30, cy - r * 1.2, cx + ex * r * .76 + 30, cy - r * .67], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WH, outline=INK, width=12)
    f = F(int(r * .56)); w = tw(d, '07:00', f); d.text((cx - w / 2, cy - r * .36), '07:00', font=f, fill=RED)
def arrow(d, x0, y, x1, lw=10):
    d.line([(x0, y), (x1 - 24, y)], fill=INK, width=lw); d.polygon([(x1, y), (x1 - 34, y - 22), (x1 - 34, y + 22)], fill=INK)

def r1():   # хук, как обложка A
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 90, ['ДВЕРЬ', 'ОТКРЫТА'], 118)
    cage(d, 440, 600, 1170, 270)
    bg = sit(bg, 440, 1120, 0.43); d = ImageDraw.Draw(bg)
    tag(d, 800, 540, 'ВЫХОД', 42, INK, WH, pad=16, outline=None); d.line([(800, 572), (800, 630)], fill=INK, width=9)
    d.polygon([(782, 626), (818, 626), (800, 654)], fill=INK)
    tag(d, 250, 440, 'ТЕРПИШЬ: 5 ЛЕТ', 40, WH, DG, pad=16, outline=LG)
    para(d, 1210, ['Почему ты не выходишь?'], 36, FM, DG)
    footer(d, 0); return bg
def r2():   # ненавижу, но иду + стоп
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['Ненавидишь работу.', 'И завтра опять пойдёшь.'], 56, FB)
    door(d, 700, 940, 420, 1040, 'ОФИС'); clock(d, 210, 470, 85)
    bg = man(bg, 11, 400, 1040, 0.4); d = ImageDraw.Draw(bg); floor_line(d, 1040)
    para(d, 1062, ['Думаешь, потому что слабак?'], 40, FM, DG)
    plates(d, 1140, ['СТОП. ТУТ ТЫ ТУПИШЬ'], 70)
    footer(d, 1); return bg
def r3():   # бомба: поняли наоборот
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['Почему ты не уходишь,', 'учёные объясняли полвека'], 52, FB)
    for x, yr in ((250, '1967'), (830, '2016')):
        tag(d, x, 380, yr, 80, WH, INK, pad=22, outline=INK)
    arrow(d, 420, 380, 660)
    para(d, 470, ['А потом признали:'], 44, FM)
    plates(d, 560, ['ПОНЯЛИ ВСЁ', 'НАОБОРОТ'], 96)
    bg = man(bg, 9, 540, 1220, 0.3); d = ImageDraw.Draw(bg); floor_line(d, 1220, 300, 780)
    footer(d, 2); return bg
def r4():   # опыт 1967
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 80, ['ОПЫТ 1967 ГОДА'], 90)
    para(d, 230, ['Селигман и Майер. Собак били током,', 'и уйти они не могли. Потом дали', 'низкий барьер: перепрыгни и свободен'], 40, FM)
    floor_line(d, 1000); bg = lie(bg, 420, 1000, 0.44); d = ImageDraw.Draw(bg)
    d.rounded_rectangle([760, 910, 790, 1000], radius=6, fill=YEL, outline=INK, width=5)
    tag(d, 900, 800, "СВОБОДА", 40, INK, WH, pad=14, outline=None); arrow(d, 820, 860, 1010)
    plates(d, 1080, ['А МНОГИЕ ЛОЖИЛИСЬ И ТЕРПЕЛИ'], 54, fill=WH)
    footer(d, 3); return bg
def sheet(d, x, y, ang=0):
    d.rectangle([x, y, x + 120, y + 160], fill=WH, outline=INK, width=6)
    for k in range(4): d.line([(x + 20, y + 30 + k * 30), (x + 100 - (k % 2) * 30, y + 30 + k * 30)], fill=GREY, width=8)
def r5():   # ложный ответ
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['Это назвали'], 46, FM, DG)
    plates(d, 160, ['ВЫУЧЕННАЯ', 'БЕСПОМОЩНОСТЬ'], 92)
    bg = man(bg, 2, 300, 1160, 0.44); d = ImageDraw.Draw(bg); floor_line(d, 1160, 70, 520)
    for k, (x, y) in enumerate(((600, 520), (760, 560), (650, 740))): sheet(d, x, y)
    tag(d, 840, 960, 'тишина...', 46, LG, DG, pad=18, outline=None)
    para(d, 1060, ['Узнал себя?'], 44, FB, INK, x=600)
    f = F(34); t = 'но это неправда →'; x = 1010 - tw(d, t, f)
    footer(d, 4, swipe=False); d.rounded_rectangle([x - 16, 1258, 1026, 1322], radius=12, fill=YEL); d.text((x, 1268), t, font=f, fill=INK)
    return bg
def r6():   # поворот
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    plates(d, 80, ['ВЫ ДУМАЛИ,', 'ЭТО ПРАВДА?'], 96)
    para(d, 350, ['2016: те же учёные написали,', 'что терпеть никто не учится.', 'Это заводская настройка мозга.'], 40, FM)
    bg = man(bg, 4, 260, 1210, 0.4); d = ImageDraw.Draw(bg); floor_line(d, 1210, 70, 460)
    para(d, 640, ['Учится другое:'], 46, FB, INK, x=520)
    tag(d, 760, 800, 'Я НА ЧТО-ТО', 60, YEL, INK, pad=22, outline=None); tag(d, 760, 900, 'ВЛИЯЮ', 60, YEL, INK, pad=22, outline=None)
    footer(d, 5); return bg
def r7():   # что делать
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['Смелость не нужна. Нужен'], 46, FM, DG)
    plates(d, 160, ['1 ШАГ В НЕДЕЛЮ'], 100)
    xs = [(360, 1150, 'резюме'), (560, 1010, 'созвон'), (760, 870, 'собес для тренировки')]
    for k, (x, y, lab) in enumerate(xs):
        d.rectangle([x, y, x + 200 if k < 2 else 1020, 1200], fill=YEL if k == 2 else WH, outline=INK, width=8)
    for (x, y, lab), dy in zip(xs, (0, 0, 0)):
        f = F(34, FM); ty = y - 52
        if lab.startswith('собес'): d.text((x + 6, y - 92), 'собеседование', font=f, fill=INK); d.text((x + 6, ty), 'для тренировки', font=f, fill=INK)
        else: d.text((x + 6, ty), lab, font=f, fill=INK)
    bg = man(bg, 8, 200, 1200, 0.38); d = ImageDraw.Draw(bg); floor_line(d, 1200, 60, 360)
    para(d, 400, ['Каждый шаг доказывает мозгу,', 'что ты влияешь'], 40, FM)
    footer(d, 6); return bg
def r8():   # правило
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['Только одно правило'], 46, FM, DG)
    plates(d, 160, ['УХОДИ, КОГДА', 'НАШЁЛ КУДА'], 100)
    door(d, 120, 340, 560, 1160, 'ОФИС', LG, DG)
    door(d, 760, 980, 560, 1160, 'НОВОЕ', INK, WH)
    bg = man(bg, 5, 540, 1160, 0.38); d = ImageDraw.Draw(bg); floor_line(d, 1160)
    para(d, 1190, ['Не в пустоту, а в новую дверь'], 38, FM)
    footer(d, 7); return bg
def r9():   # кольцо
    bg = Image.new('RGB', (W, H), WH); d = ImageDraw.Draw(bg)
    para(d, 80, ['А дверь всё это время'], 50, FM)
    plates(d, 170, ['БЫЛА ОТКРЫТА'], 104)
    cage(d, 330, 560, 1150, 230)
    bg = man(bg, 8, 860, 1150, 0.4); d = ImageDraw.Draw(bg); floor_line(d, 1150, 600, 1020)
    tag(d, 540, 1240, 'ВСЁ. НЕ ТУПИ.', 52, fill=YEL, outline=None, pad=18)
    return bg
os.makedirs(OUT, exist_ok=True)
for i, f in enumerate((r1, r2, r3, r4, r5, r6, r7, r8, r9), 1): f().save(f'{OUT}/slide-{i:02d}.png')
sh = Image.new('RGB', (5 * 330 + 60, 2 * 412 + 30), (40, 40, 40))
for i in range(9):
    im = Image.open(f'{OUT}/slide-{i + 1:02d}.png').resize((324, 405)); sh.paste(im, (10 + (i % 5) * 340, 10 + (i // 5) * 420))
sh.save(f'{OUT}/obzor.png')
