"""СДВГ-монтаж «Конец света 17 ноября» (по Shorts Mutabor). Движок «Двух судеб» (compose_dv.py), кадр на весь экран, белый фон.
python3 compose_ap.py 1.5 12.3 -> prev_*.png;  python3 compose_ap.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_ap import *
ADDR = 'bc1q 7Fa2 … 9kD4'; ADDR2 = 'bc1q 7Fa2 … X0m1'

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_h1(C, u, t):   # Семнадцатое ноября!
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 860, u, r0=560, col=(246, 200, 0))
    calendar(C, 540, 820, 1.0, '17', 'НОЯБРЯ', back(u / 0.25), -6 + 3 * s_(u * 30) * clamp(1 - u))
    girl(C, 'scream', u, 900, 0.3, G + 40); man(C, 'scream', u + 0.3, 180, G + 40, 0.3)
    slam(C, u, 'КОНЕЦ СВЕТА', 540, 380, 140, INK)
def s_inet(C, u, t):   # Интернет вырубят на три месяца
    wifi(C, 540, 1000, 1.25, INK, t - T('вырубят'))
    slam(C, u, 'ИНТЕРНЕТ ВЫРУБЯТ', 540, 380, 110)
    v = t - T('три')
    if v > -0.05: put(C, plate_img('НА 3 МЕСЯЦА', 110, RED, WHITE, pad=24, r=16, border=INK, bw=7), 540, 540, 1 + 0.4 * (1 - eo((v + 0.05) / 0.18)), -3)
def s_card0(C, u, t):   # бабки на картах обнулят
    card(C, 540, 880, 560, -8 + 4 * s_(u * 5), scale=back(u / 0.22))
    v = t - T('обнулят')
    if v > 0: put(C, text_img('0 ₽', 220, RED, WHITE, 12), 540, 880, back(v / 0.2), 6)
    slam(C, u, 'БАБКИ НА КАРТАХ', 540, 380, 110)
    if v > 0: stamp(C, v, 'ОБНУЛЯТ', 540, 1150, 100, RED, -8)
def s_grechka(C, u, t):   # Скупай гречку, блять!
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0))
    grech_pile(C, 780, G + 40, min(9, 1 + int(u * 9)), 0.55)
    girl(C, 'box', u, 330, 0.44, G + 40); grechka(C, 330, G + 40 - 330, 0.6, 4 * s_(u * 8))
    slam(C, u, 'СКУПАЙ ГРЕЧКУ', 540, 380, 130)
    v = t - T('блять')
    if v > 0: stamp(C, v, 'БЛ*ТЬ!', 540, 560, 120, RED, -10)
def s_oral(C, u, t):   # Так орал весь интернет
    ground(C); crowd2(C, u, 540, G, 7, 0.22, 'shock')
    for j in range(6):
        q = (u * 1.1 + j / 6) % 1; x = 120 + j * 168; phone(C, x, 820 - 160 * q, 0.55, (j - 3) * 8)
    slam(C, u, 'ТАК ОРАЛ', 540, 380, 140); plate(C, t - T('весь'), 'ВЕСЬ ИНТЕРНЕТ', 540, 540, 100, INK, YEL, 3)
def s_segodnya(C, u, t):   # Сегодня семнадцатое
    ground(C); calendar(C, 540, 860, 1.1, '17', 'НОЯБРЯ', back(u / 0.22), 3); man(C, 'shrug', u, 870, G, 0.3)
    slam(C, u, 'СЕГОДНЯ', 540, 380, 160)
def s_namest(C, u, t):   # Интернет на месте
    ground(C); man(C, 'phone', u, 330, G, 0.44); wifi(C, 770, 900, 0.8, INK, 0, t - T('месте'))
    slam(C, u, 'ИНТЕРНЕТ', 540, 380, 150); plate(C, t - T('месте'), 'НА МЕСТЕ', 540, 540, 110, GREEN, WHITE, -3)
def s_dengi(C, u, t):   # Деньги тоже
    ground(C); atm(C, 330, G, 1.15, '100 000 ₽'); welder(C, 'cheer', u, 780, 0.4)
    for j in range(3): bill(C, 330 + (j - 1) * 60, 880 - 160 * eo(clamp((u - 0.1 * j) / 0.4)), 150, (j - 1) * 14)
    slam(C, u, 'ДЕНЬГИ', 540, 380, 160); plate(C, t - T('тоже'), 'ТОЖЕ', 540, 540, 110, GREEN, WHITE, 3)
def s_otkuda(C, u, t):   # Откуда паника?
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); man(C, 'scratch', u, 540, G + 40, 0.5)
    slam(C, u, 'ОТКУДА', 540, 380, 180); plate(C, t - T('паника'), 'ПАНИКА?', 540, 570, 130, INK, YEL, -3)
def s_brazil(C, u, t):   # Один чел из Бразилии написал: мне шепнул источник в даркнете
    ground(C); man(C, 'phone', u, 230, G, 0.36); brflag(C, 230, 640, 200, u)
    v = t - T('написал')
    post(C, 640, 890, 640, v + 0.1, 'МНЕ ШЕПНУЛ\nИСТОЧНИК\nВ ДАРКНЕТЕ…')
    if t > T('даркнете'): put(C, plate_img('ДАРКНЕТ', 56, INK, WHITE, pad=12, r=8), 800, 1130, back((t - T('даркнете')) / 0.2), 6)
    slam(C, u, 'ОДИН ЧЕЛ', 540, 380, 140); plate(C, t - T('Бразилии'), 'ИЗ БРАЗИЛИИ', 540, 530, 90, BRG, WHITE, 3)
def s_nol(C, u, t):   # Ноль доказательств
    doc(C, 540, 880, 460, 580, 'ДОКАЗАТЕЛЬСТВА', -4, back(u / 0.2), None, False, 44)
    magnifier(C, 540 + 150 * s_(u * 3), 900 + 60 * s_(u * 4), 1.0, -10)
    slam(C, u, 'НОЛЬ', 540, 380, 170); stamp(C, t - T('доказательств') - 0.2, 'ПУСТО', 540, 1180, 100, RED, -8)
def s_views(C, u, t):   # Четыре миллиона просмотров
    eye(C, 540, 820, 1.0, u); v = t - T('Четыре')
    put(C, plate_img(num(roll(max(0, v), 0, 4000000, 0.9)), 130, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 1110, 1, -2)
    slam(C, u, 'ПРОСМОТРОВ', 540, 380, 150)
def s_data(C, u, t):   # А дата?
    ground(C); calendar(C, 420, 880, 0.95, '17', 'НОЯБРЯ', back(u / 0.2), -4)
    pop(C, u - 0.15, '?', 820, 760, 300, RED, 10); slam(C, u, 'А ДАТА?', 540, 380, 170)
def s_usa(C, u, t):   # В США сегодня просто проверяют систему оповещения
    ground(C); usflag(C, 250, 600, 260, u); siren(C, 250, G, 0.9, u); tvset(C, 740, 860, 480, 340, 'ТЕСТ', u)
    slam(C, u, 'В США', 540, 380, 150); plate(C, t - T('проверяют'), 'ПРОВЕРКА СИРЕН', 540, 530, 96, INK, YEL, -3)
    src(C, '17 НОЯБРЯ — ПЛАНОВЫЙ ТЕСТ ОПОВЕЩЕНИЯ EAS (FEMA И FCC)', 1318)
def s_podvoh(C, u, t):   # А вот и подвох
    C.paste(INK, [0, 0, CW, CH]); man_o(C, 'whisper', u, 540, G + 20, 0.5)
    slam(C, u, 'А ВОТ И', 540, 380, 140, WHITE); plate(C, u - 0.25, 'ПОДВОХ', 540, 550, 140, YEL, INK, -3)
def s_ataka(C, u, t):   # Атака реально была
    C.paste(INK, [0, 0, CW, CH]); speedlines(C, 540, 880, u, r0=520, col=(34, 34, 34), seed=8)
    for j in range(4): browser(C, 300 + (j % 2) * 480, 760 + (j // 2) * 360, 420, 300, '', clamp((u - 0.2 - j * 0.15) / 0.2))
    slam(C, u, 'АТАКА', 540, 380, 170, WHITE); plate(C, t - T('реально'), 'РЕАЛЬНО БЫЛА', 540, 540, 96, RED, WHITE, 3)
def s_tihaya(C, u, t):   # Только тихая
    ground(C); x = lerp(150, 760, clamp(u / 1.0)); ninja(C, x, G - 200, 90, u, 'КОД', 1, tip=True)
    man(C, 'idle', u, 300, G, 0.36, flip=True)
    slam(C, u, 'ТОЛЬКО', 540, 380, 140); plate(C, u - 0.2, 'ТИХАЯ', 540, 540, 120, INK, WHITE, -3)
    pop(C, u - 0.35, 'ТСС…', 820, 820, 80, GREY, 8)
def s_servis(C, u, t):   # Хакеры влезли в один сервис для сайтов
    ground(C); server(C, 640, G, 1.1, 'СЕРВИС ДЛЯ САЙТОВ', u, clamp((u - 0.8) / 0.2))
    q = clamp(u / 1.0); ninja(C, lerp(160, 560, eo(q)), lerp(G - 120, 760, eo(q)) - 140 * s_(math.pi * q), 80, u, None, 2)
    slam(C, u, 'ХАКЕРЫ ВЛЕЗЛИ', 540, 380, 120)
def s_178(C, u, t):   # И через него сразу на 178 сайтов
    C.paste(INK, [0, 0, CW, CH]); d = D(C); v = t - T('сто'); n = int(clamp(v / 1.2) * 178) if v > 0 else 0
    cx, cy = 540, 880; k = clamp((u - 0.2) / 1.6)
    for j in range(24):
        a = j / 24 * 2 * math.pi; r = 330 + 30 * (j % 2); x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.95
        if j / 24 < k:
            d.line([cx, cy, x, y], fill=RED, width=5); browser(C, x, y, 110, 80, '', 1.0 if j / 24 < k - 0.1 else 0)
    server(C, cx, cy + 180, 0.55, '', u, 1)
    put(C, plate_img(f'{n} САЙТОВ', 110, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 1330 - 60, 1, -2) if v > 0 else None
    slam(C, u, 'СРАЗУ НА', 540, 380, 150, WHITE)
def s_bmn(C, u, t):   # Банки, магазины, новости
    ground(C)
    for j, (w_, lab) in enumerate([('Банки', 'БАНК'), ('магазины', 'МАГАЗИН'), ('новости', 'НОВОСТИ')]):
        v = t - T(w_)
        if v > -0.05: browser(C, 540, 640 + j * 230, max(260, 760 * back((v + 0.05) / 0.2)) if v < 0.2 else 760, 200, lab, clamp((v - 0.25) / 0.2))
    src(C, 'СРЕДИ НИХ HSBC, LEDGER, BBC, CNN, IKEA, ZOOM — ПО ДАННЫМ REUTERS', 1318)
def s_melochi(C, u, t):   # Код делал мелочь
    ground(C); ninja(C, 540, G - 330, 130, u, 'КОД', 3); magnifier(C, 820, 720, 0.7, -20)
    slam(C, u, 'КОД ДЕЛАЛ', 540, 380, 140); plate(C, t - T('мелочь'), 'ОДНУ МЕЛОЧЬ', 540, 540, 100, INK, YEL, -3)
def s_copy(C, u, t):   # копируешь номер кошелька
    ground(C); man(C, 'phone', u, 220, G, 0.34)
    addr_field(C, 610, 760, 760, ADDR, INK, WHITE, None, u)
    put(C, plate_img('КОПИРОВАТЬ', 54, INK, WHITE, pad=14, r=10), 610, 920, back((u - 0.25) / 0.2)); cursor(C, 650 + 30 * eo(clamp((u - 0.2) / 0.3)), 940, 1.2)
    slam(C, u, 'КОПИРУЕШЬ', 540, 380, 150); plate(C, t - T('кошелька'), 'НОМЕР КОШЕЛЬКА', 540, 540, 90, YEL, INK, 3)
def s_chuzhoy(C, u, t):   # а вставляется чужой
    ground(C); v = t - T('чужой'); sw = clamp(v / 0.25) if v > 0 else 0
    addr_field(C, 540, 760, 860, ADDR if sw < 0.5 else ADDR2, INK if sw < 0.5 else RED, WHITE if sw < 0.5 else (255, 228, 230))
    ninja(C, lerp(1180, 860, eo(clamp(u / 0.4))), 940 + 20 * s_(u * 8), 70, u, None, 4)
    if sw > 0.5: put(C, plate_img('ЧУЖОЙ', 80, RED, WHITE, pad=16, r=10, border=INK, bw=5), 540, 960, back((v - 0.12) / 0.2), -5)
    man(C, 'idle_smile' if sw < 0.5 else 'shock', u, 300, G, 0.32)
    slam(C, u, 'ВСТАВЛЯЕТСЯ', 540, 380, 130)
def s_9h(C, u, t):   # За девять часов около семи тысяч долларов
    ground(C); calendar(C, 260, 760, 0.6, '9', 'ЧАСОВ', back(u / 0.2), -6)
    ninja(C, 760, G - 260, 110, u, 'ХАКЕР', 5)
    for j in range(6):
        q = (u * 1.3 + j / 6) % 1; btc(C, lerp(260, 760, q), lerp(900, 920, q) - 220 * s_(math.pi * q), 40, q * 300)
    v = t - T('около')
    if v > -0.05: put(C, plate_img('≈ $' + num(roll(max(0, v), 0, 7000, 0.7)), 120, YEL, INK, pad=24, r=16, border=INK, bw=7), 540, 540, 1 + 0.4 * (1 - eo((v + 0.05) / 0.18)), -3)
    slam(C, u, 'ЗА 9 ЧАСОВ', 540, 380, 140)
def s_580(C, u, t):   # Это примерно 580 тысяч рублей
    ground(C); k = eo(clamp(u / 0.8))
    for j in range(5): wad(C, 540 + (j - 2) * 170, G - 70 - 40 * (j % 2), 180, 1 + int(k * 4))
    v = t - T('пятьсот')
    put(C, plate_img('≈ ' + num(roll(max(0, v), 0, 580000, 0.9)) + ' ₽', 130, YEL, INK, pad=24, r=16, border=INK, bw=8), 540, 760, 1, -2)
    slam(C, u, 'ЭТО ПРИМЕРНО', 540, 380, 120)
    src(C, '$7 040 ПО ДАННЫМ REPORT URI, ПО КУРСУ ≈82,5 ₽ ЗА $', 1318)
def s_prikol(C, u, t):   # Понял прикол?
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=560, col=(246, 200, 0)); man(C, 'pointcam', u, 540, G + 40, 0.5)
    slam(C, u, 'ПОНЯЛ ПРИКОЛ?', 540, 400, 140)
def s_sirena(C, u, t):   # Конец света не придёт с сиреной
    ground(C); siren(C, 540, G, 1.0, u); xcross(C, t - T('сиреной'), 540, 760, 330, RED, 34)
    slam(C, u, 'КОНЕЦ СВЕТА', 540, 380, 140); plate(C, t - T('придёт', 0), 'НЕ С СИРЕНОЙ', 540, 540, 100, RED, WHITE, -3)
def s_tiho(C, u, t):   # Он придёт тихо
    ground(C); x = lerp(-100, 540, eo(clamp(u / 0.8))); ninja(C, x, G - 140, 110, u, None, 6, tip=True)
    slam(C, u, 'ОН ПРИДЁТ', 540, 380, 140); plate(C, t - T('тихо'), 'ТИХО', 540, 540, 130, INK, WHITE, 3)
def s_stroka(C, u, t):   # подменой одной строчки
    d = D(C); d.rounded_rectangle([120, 640, 960, 1240], radius=30, fill=WHITE, outline=INK, width=8); v = t - T('одной')
    for j in range(6):
        y = 700 + j * 88; bad = j == 3 and v > 0
        d.rounded_rectangle([170, y, 170 + (640 if j % 2 else 560), y + 50], radius=10, fill=(255, 205, 210) if bad else LG)
        if bad: d.rounded_rectangle([160, y - 10, 920, y + 60], radius=14, outline=RED, width=8)
    if v > 0: put(C, plate_img('ПОДМЕНА', 70, RED, WHITE, pad=14, r=10, border=INK, bw=5), 780, 1000, back(v / 0.2), -8)
    slam(C, u, 'ОДНОЙ СТРОЧКИ', 540, 400, 130)
def s_rekv(C, u, t):   # Вставил реквизиты
    ground(C); man(C, 'explain', u, 220, G, 0.34); addr_field(C, 620, 800, 760, ADDR, INK, WHITE, None, u, True, u)
    slam(C, u, 'ВСТАВИЛ', 540, 380, 150); plate(C, t - T('реквизиты'), 'РЕКВИЗИТЫ?', 540, 540, 110, YEL, INK, -3)
def s_sver(C, u, t):   # сверь первые и последние символы
    ground(C); v1 = t - T('первые'); v2 = t - T('последние')
    addr_field(C, 540, 800, 900, ADDR, INK, WHITE, (4 if v1 > 0 else 0, 4 if v2 > 0 else 0))
    if v1 > 0: arrow(C, 210, 1040, 250, 890, INK, 12, clamp(v1 / 0.2)); tag(C, v1, 'ПЕРВЫЕ', 210, 1080, 50, YEL, INK, -4)
    if v2 > 0: arrow(C, 870, 1040, 830, 890, INK, 12, clamp(v2 / 0.2)); tag(C, v2, 'ПОСЛЕДНИЕ', 870, 1080, 50, YEL, INK, 4)
    slam(C, u, 'СВЕРЬ', 540, 380, 170)
def s_srochno(C, u, t):   # Пишут «срочно снимай деньги»
    phone(C, 300, 900, 2.2, -6, ring=u if u < 0.6 else 0, screen=SCREEN)
    sms(C, 640, 760, 620, 'СРОЧНО СНИМАЙ\nДЕНЬГИ!!!', t - T('срочно') + 0.1, RED)
    slam(C, u, 'ПИШУТ', 540, 380, 160)
def s_moshenniki(C, u, t):   # это не апокалипсис, это мошенники
    ground(C); globe_(C, 540, 840, 250, u); v = t - T('мошенники')
    if v < 0: put(C, plate_img('АПОКАЛИПСИС', 80, RED, WHITE, pad=16, r=10, border=INK, bw=5), 540, 1150, back(u / 0.2), -4); xcross(C, u - 0.5, 540, 1150, 260, INK, 22)
    else: ninja(C, 540, 1080, 100, u, 'МОШЕННИК', 7)
    slam(C, u, 'ЭТО НЕ', 540, 380, 160)
    if v > 0: stamp(C, v, 'ЭТО МОШЕННИКИ', 540, 560, 96, RED, -6)
def s_skin(C, u, t):   # Скинь тому, кто купил гречку
    ground(C); grech_pile(C, 760, G, 9, 0.36); girl(C, 'sad', u, 760, 0.22, G - 345)
    man(C, 'pointcam', u, 250, G, 0.4)
    slam(C, u, 'СКИНЬ ТОМУ,', 540, 380, 130); plate(C, t - T('купил'), 'КТО КУПИЛ ГРЕЧКУ', 540, 540, 90, YEL, INK, -3)
def s_netupi(C, u, t):
    C.paste(YEL, [0, 0, CW, CH]); v = t - T('тупи'); e = t - END - 0.25
    if e < 0: man(C, 'armsup' if v > 0 else 'idle_smile', u, 540, G + 40, 0.48)
    else: man(C, 'walkR', e, 540 - e * 620, G + 40, 0.48, flip=True)
    slam(C, u, 'И', 540, 380, 200)
    if v > -0.12: plate(C, v + 0.12, 'НЕ ТУПИ.', 540, 570, 140, INK, YEL)
PUSH_FLIP = False

def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_h1, 'none', 'boom'), SH(T('Интернет', 0) - 0.05, s_inet, 'whipL', 'whoosh'), SH(T('бабки') - 0.05, s_card0, 'shake', 'bass'),
 SH(T('Скупай') - 0.05, s_grechka, 'zoom', 'boom'),
 SH(T('Так') - 0.05, s_oral, 'push', 'bass'), SH(T('Сегодня') - 0.05, s_segodnya, 'door', 'thud'),
 SH(T('Интернет', 1) - 0.05, s_namest, 'whipR', 'whoosh'), SH(T('Деньги') - 0.05, s_dengi, 'whipL', 'whoosh'),
 SH(T('Откуда') - 0.05, s_otkuda, 'shake', 'scratch'), SH(T('Один') - 0.05, s_brazil, 'zoomthru', 'bass', (540, 900)),
 SH(T('Ноль') - 0.05, s_nol, 'glitch', 'error'), SH(T('Четыре') - 0.05, s_views, 'zoom', 'tick2'),
 SH(T('А', 0) - 0.05, s_data, 'whipU', 'whoosh'), SH(T('В', 0) - 0.05, s_usa, 'whipL', 'whoosh'),
 SH(T('А', 1) - 0.05, s_podvoh, 'drop', 'thud'), SH(T('Атака') - 0.05, s_ataka, 'glitch', 'riser'), SH(T('Только') - 0.05, s_tihaya, 'zoom', 'whoosh'),
 SH(T('Хакеры') - 0.05, s_servis, 'push', 'bass'), SH(T('И', 0) - 0.05, s_178, 'zoomthru', 'bass', (640, 900)),
 SH(T('Банки') - 0.05, s_bmn, 'whipR', 'whoosh'), SH(T('Код') - 0.05, s_melochi, 'door', 'thud'),
 SH(T('копируешь') - 0.05, s_copy, 'zoom', 'click'), SH(T('а', 0) - 0.05, s_chuzhoy, 'whipL', 'whoosh'),
 SH(T('За') - 0.05, s_9h, 'zoomthru', 'bass', (540, 900)), SH(T('Это') - 0.05, s_580, 'whipR', 'whoosh'),
 SH(T('Понял') - 0.05, s_prikol, 'shake', 'boom'), SH(T('Конец') - 0.05, s_sirena, 'whipL', 'whoosh'),
 SH(T('Он') - 0.05, s_tiho, 'zoom', 'whoosh'), SH(T('подменой') - 0.05, s_stroka, 'glitch', 'error'),
 SH(T('Вставил') - 0.05, s_rekv, 'push', 'bass'), SH(T('сверь') - 0.05, s_sver, 'zoom', 'whoosh'),
 SH(T('Пишут') - 0.05, s_srochno, 'whipR', 'notif'), SH(T('это', 0) - 0.05, s_moshenniki, 'shake', 'boom'),
 SH(T('Скинь') - 0.05, s_skin, 'bodywipe', 'bass'), SH(T('И', 1) - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('ноября'), 'alarm'), (T('вырубят') + 0.1, 'error'), (T('три'), 'pop'), (T('обнулят'), 'stamp'), (T('блять'), 'stamp'), (T('весь'), 'pop'),
       (T('месте'), 'ok'), (T('тоже'), 'kassa'), (T('Бразилии'), 'pop'), (T('написал'), 'msg'), (T('даркнете'), 'pop'), (T('доказательств') + 0.2, 'stamp'),
       (T('дата'), 'boing'), (T('проверяют'), 'alarm'), (T('подвох'), 'drop'), (T('реально'), 'pop'), (T('тихая'), 'swipe'),
       (T('сервис') + 0.5, 'error'), (T('сто'), 'tick'), (T('сайтов', 1), 'alarm'), (T('Банки'), 'pop'), (T('магазины'), 'pop'), (T('новости'), 'pop'),
       (T('мелочь'), 'ding'), (T('номер'), 'click'), (T('чужой'), 'error'), (T('около'), 'coins'), (T('долларов'), 'kassa'), (T('пятьсот'), 'tick2'), (T('рублей'), 'kassa'),
       (T('придёт', 0), 'pop'), (T('сиреной'), 'error'), (T('тихо'), 'swipe'), (T('одной'), 'alarm'), (T('реквизиты'), 'pop'), (T('первые'), 'ding'), (T('последние'), 'ding'),
       (T('срочно'), 'msg'), (T('мошенники'), 'stamp'), (T('гречку', 1), 'pop'), (T('тупи'), 'stamp')]

# ================= движок: глубина, переходы через действие, субтитры, кадр =================
ACTION = {'push', 'zoomthru', 'door', 'bodywipe', 'drop'}; PRE, POST = 0.10, 0.30
CARD_RGB = Image.new('RGB', (CW, CH), CARD)
def _pattern(layer_):
    W2 = CW * 2; im = Image.new('RGBA', (W2, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(7 + layer_)
    if layer_ == 0:
        for x in range(0, W2, 54):
            for y in range(0, CH, 54): d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(232, 230, 224))
    else:
        for j in range(30):
            x = rnd.randint(0, W2); y = rnd.randint(0, CH); r = rnd.randint(70, 190); d.ellipse([x - r, y - r, x + r, y + r], fill=(242, 240, 235))
            if x < 200: d.ellipse([x + W2 - r, y - r, x + W2 + r, y + r], fill=(242, 240, 235))
    return im
PAT = [_pattern(0), _pattern(1)]; SPEED = (18, 60)
def depth(C, u):
    """сцена на белом → фон с параллаксом + мягкая тень + лёгкий наезд переднего плана"""
    rgb = C.convert('RGB'); diff = ImageChops.difference(rgb, CARD_RGB).convert('L')
    small = diff.resize((CW // 8, CH // 8), Image.BILINEAR)
    if small.point(lambda v: 255 if v > 8 else 0).histogram()[255] > 0.8 * (CW // 8) * (CH // 8): return C      # сплошной цветной фон — без параллакса
    m = diff.point(lambda v: 0 if v < 2 else min(255, v * 60))
    out = Image.new('RGBA', (CW, CH), CARD + (255,))
    for l in (1, 0):
        off = int(u * SPEED[l]) % CW; out.alpha_composite(PAT[l].crop((off, 0, off + CW, CH)))
    z = 1 + 0.035 * clamp(u / 1.5)
    sh = m.resize((CW // 4, CH // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4)).resize((CW, CH), Image.BILINEAR)
    shadow = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.2)))
    fg = C.copy(); fg.putalpha(m)
    if z > 1.001:
        w, h = int(CW * z), int(CH * z); ox, oy = (w - CW) // 2, int((h - CH) * 0.45)
        fg = fg.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH)); shadow = shadow.resize((w, h), Image.BILINEAR).crop((ox, oy, ox + CW, oy + CH))
    out.alpha_composite(shadow, (16, 20)); out.alpha_composite(fg); return out
def shot_at(t):
    i = max(j for j in range(len(SHOTS)) if SHOTS[j]['t'] <= t); return i, SHOTS[i]
def card_of(j, t):
    sh = SHOTS[j]; u = max(0.0, t - sh['t']); tt = max(t, sh['t'])
    C = Image.new('RGBA', (CW, CH), CARD + (255,)); sh['fn'](C, u, tt); return depth(C, u)
def tr_push(A, B, k, t):
    e = eio(k); v = s_(math.pi * k); out = Image.new('RGBA', (CW, CH), CARD + (255,)); x = int(CW * (1 - e))
    out.alpha_composite(hblur(A, 1 + 24 * v), (x - CW, 0)); out.alpha_composite(hblur(B, 1 + 24 * v), (x, 0))
    man(out, 'push', t * 1.4, x + 150, G, 0.7, flip=not PUSH_FLIP); return out
def tr_zoomthru(A, B, k, p):
    s = 1 + 11 * ei(clamp(k / 0.75)); cx, cy = lerp(p[0], CW / 2, eo(k)), lerp(p[1], CH / 2, eo(k))
    box = (p[0] - cx / s, p[1] - cy / s, p[0] + (CW - cx) / s, p[1] + (CH - cy) / s)
    a = A.crop(tuple(int(b) for b in box)).resize((CW, CH), Image.BILINEAR)
    if s > 1.5:
        s2 = s * 0.82; box2 = (p[0] - cx / s2, p[1] - cy / s2, p[0] + (CW - cx) / s2, p[1] + (CH - cy) / s2)
        a = Image.blend(a, A.crop(tuple(int(b) for b in box2)).resize((CW, CH), Image.BILINEAR), 0.45)
    zb = 0.7 + 0.3 * eo(k); w, h = int(CW * zb), int(CH * zb)
    out = Image.new('RGBA', (CW, CH), CARD + (255,)); out.alpha_composite(B.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2))
    al = 1 - clamp((k - 0.4) / 0.3)
    if al > 0: a = a.copy(); a.putalpha(int(255 * al)); out.alpha_composite(a)
    return out
def door_panel(w, left):
    im = Image.new('RGBA', (w + 30, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0 = 0 if left else 30
    d.rectangle([x0, 0, x0 + w, CH], fill=(196, 150, 100), outline=INK, width=14)
    for (ya, yb) in [(300, 820), (900, 1480)]: d.rounded_rectangle([x0 + 70, ya, x0 + w - 70, yb], radius=20, fill=(176, 130, 84), outline=INK, width=8)
    ex = x0 + w - 16 if left else x0 + 16; d.rectangle([ex - 16, 0, ex + 16, CH], fill=INK)
    hx = x0 + w - 90 if left else x0 + 90; d.ellipse([hx - 30, 830, hx + 30, 890], fill=YEL, outline=INK, width=7)
    sh = Image.new('RGBA', (30, CH), (0, 0, 0, 70)); im.alpha_composite(sh, (w if left else 0, 0)); return im
DP = (door_panel(CW // 2, True), door_panel(CW // 2, False))
def tr_door(A, B, k):
    c = eo(k / 0.42) if k < 0.5 else 1 - eio((k - 0.58) / 0.42) if k > 0.58 else 1
    out = (A if k < 0.5 else B).copy(); w = int(CW / 2 * c)
    if w > 0: out.alpha_composite(DP[0], (w - CW // 2, 0)); out.alpha_composite(DP[1], (CW - w - 30, 0))
    return out
def tr_bodywipe(A, B, k, t):
    x = int(lerp(-420, CW + 420, eio(k))); out = A.copy()
    if x > 0: out.paste(B.crop((0, 0, min(CW, x), CH)), (0, 0))
    man(out, 'walkR', 0, x, CH + 420, 2.0, frame=int(k * 5) * 3 % CLIPS['walkR']); return out
def tr_drop(A, B, k):
    y = int(-CH * (1 - back(k))); out = Image.new('RGBA', (CW, CH), CARD + (255,))
    z = 1 - 0.06 * k; w, h = int(CW * z), int(CH * z); a = A.resize((w, h), Image.BILINEAR)
    out.alpha_composite(a, ((CW - w) // 2, (CH - h) // 2)); out.alpha_composite(Image.new('RGBA', (CW, CH), (0, 0, 0, int(110 * k))))
    v = abs(s_(math.pi * min(1, k * 1.3))); b = vblur(B, 1 + 26 * v)
    out.alpha_composite(b, (0, min(0, y))); return out
def card_at(t):
    i, sh = shot_at(t); j = None
    W_ = lambda q: {'door': (0.18, 0.42)}.get(SHOTS[q]['tr'], (PRE, POST))
    if i + 1 < len(SHOTS) and SHOTS[i + 1]['tr'] in ACTION and SHOTS[i + 1]['t'] - t < W_(i + 1)[0]: j = i + 1
    elif sh['tr'] in ACTION and t - sh['t'] < W_(i)[1] and i > 0: j = i
    if j is not None:
        pr, po = W_(j); k = clamp((t - (SHOTS[j]['t'] - pr)) / (pr + po)); A, B = card_of(j - 1, t), card_of(j, t); tr = SHOTS[j]['tr']
        if tr == 'push': C = tr_push(A, B, k, t)
        elif tr == 'zoomthru': C = tr_zoomthru(A, B, k, SHOTS[j]['p'])
        elif tr == 'door': C = tr_door(A, B, k)
        elif tr == 'bodywipe': C = tr_bodywipe(A, B, k, t)
        else: C = tr_drop(A, B, k)
        return C, i, sh, True
    C = card_of(i, t); C = transform(C, t - sh['t'], sh['tr'], i); return C, i, sh, False

# ---------- субтитры: 1–3 слова, текущее слово на жёлтой плашке ----------
def chunks():
    out, cur = [], []
    for w in W:
        cur.append(w); txtc = ' '.join(x[0] for x in cur)
        if w[0][-1] in '.!?…:»' or (w[0][-1] == ',' and len(txtc) > 7) or len(cur) == 3 or len(txtc) > 13: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CHK = chunks(); SUB_Y = 1432; REFH = text_img('Н', 88, INK, WHITE, 8).height
@lru_cache(400)
def sub_img(w, hl=False):
    f = font(88); wd = int(ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(w, font=f)) + 20
    im = Image.new('RGBA', (wd, 150), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 8), w, font=f, fill=INK, stroke_width=8, stroke_fill=YEL if hl else WHITE); return im
CENS = {'БЛЯТЬ': 'БЛ*ТЬ', 'БЛЯ': 'БЛ*', 'СУКА': 'С*КА'}
def clean(w):
    w = w.replace('«', '').replace('»', '').upper()
    for a, b in CENS.items(): w = w.replace(a, b)
    return w
def subs(F, t):
    for ci, ch in enumerate(CHK):
        t1 = CHK[ci + 1][0][1] if ci + 1 < len(CHK) else ch[-1][2] + 0.6
        if ch[0][1] - 0.04 <= t < t1:
            ims = []
            for (w, a, b) in ch:
                nxt = [x for x in ch if x[1] > a]; cur = a - 0.03 <= t and (not nxt or t < nxt[0][1] - 0.03)
                ims.append((sub_img(clean(w), cur), cur, 1 + 0.14 * (1 - eo((t - a) / 0.12)) if cur else 1))
            tw = sum(im.width for im, _, _ in ims) + 40 * (len(ims) - 1)
            sc0 = min(1, 800 / tw); x = 540 - tw * sc0 / 2; k0 = back((t - ch[0][1] + 0.04) / 0.14); y = SUB_Y + (1 - k0) * 30
            pos = []
            for im, cur, sc in ims: pos.append((im, cur, sc, x + im.width * sc0 / 2)); x += (im.width + 40) * sc0
            for im, cur, sc, cx in pos:
                if cur:
                    w2, h2 = im.width * sc0 * sc / 2 + 12, 66 * sc0 * sc
                    ImageDraw.Draw(F).rounded_rectangle([cx - w2, y - h2, cx + w2, y + h2], radius=16, fill=YEL, outline=INK, width=5)
            for im, cur, sc, cx in pos: put(F, im, cx, y, sc * sc0)
            return
TITLE = None
def title(F, t):
    global TITLE
    if TITLE is None:
        a = text_img('ЕСЛИ ВСЕ ПЕРЕСТАНУТ', 40, WHITE); b = text_img('ПЛАТИТЬ КРЕДИТ?', 40, YEL); w = a.width + b.width + 14 + 44; im = Image.new('RGBA', (w, 70), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, 69], radius=16, fill=INK); im.alpha_composite(a, (22, (70 - a.height) // 2)); im.alpha_composite(b, (22 + a.width + 14, (70 - b.height) // 2)); TITLE = im
    put(F, TITLE, 540, 292 - 60 * (1 - eo(t / 0.3)), 1, 0, clamp(t / 0.2))
GRAIN = []
for g in range(6):
    n = Image.effect_noise((WD // 2, HT // 2), 40).resize((WD, HT), Image.NEAREST); GRAIN.append(Image.merge('RGBA', (n, n, n, Image.new('L', (WD, HT), 12))))
def frame(t):
    C, i, sh, act = card_at(t); u = t - sh['t']
    if not act and i + 1 < len(SHOTS):
        r = SHOTS[i + 1]['t'] - t
        if r < 0.07 and SHOTS[i + 1]['tr'] not in {'cut', 'none'} | ACTION:
            z = 1 + 0.1 * (1 - r / 0.07); w, h = int(CW * z), int(CH * z); C2 = Image.new('RGBA', (CW, CH)); C2.paste(C.resize((w, h), Image.BILINEAR), ((CW - w) // 2, (CH - h) // 2)); C = C2
    F = C.convert('RGBA')
    if not act and u < 0.07 and sh['tr'] not in ('none', 'cut'): F.alpha_composite(Image.new('RGBA', (CW, CH), (255, 255, 255, int(150 * (1 - u / 0.07)))))
    subs(F, t)
    if t < 5.3: put(F, plate_img('По открытым источникам · ссылки в описании', 26, WHITE, GREY, pad=12, r=8, border=GREY, bw=3), 540, 1322, 1, 0, 1 - clamp((t - 5.0) / 0.3))
    F.alpha_composite(GRAIN[int(t * FPS) % 6])
    out = F.convert('RGB')
    if not act and u < 0.1 and sh['tr'] in ('shake', 'glitch', 'zoom'): out = rgbsplit(out, 10 * (1 - u / 0.1))
    return out

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        frac = float(a[1]) if len(a) > 1 else 0.6; ims = []
        for j, sh in enumerate(SHOTS):
            t1 = SHOTS[j + 1]['t'] if j + 1 < len(SHOTS) else DUR - 1.2; tt = sh['t'] + (t1 - sh['t']) * frac
            ims.append(frame(tt).resize((270, 480)))
        cols = 8; rows = (len(ims) + cols - 1) // cols
        for part in range(0, rows, 2):
            S = Image.new('RGB', (cols * 274, min(2, rows - part) * 484), (90, 90, 90))
            for j, im in enumerate(ims[part * cols:(part + 2) * cols]): S.paste(im, ((j % cols) * 274, (j // cols) * 484))
            S.save(f'sheet_{frac}_{part // 2}.png')
    elif a:
        for x in a: frame(float(x)).save(f'prev_{x}.png')
    else:
        ev = [(round(s['t'], 3), s['sfx']) for s in SHOTS if s['sfx']] + [(round(t, 3), n) for t, n in ACC]
        json.dump(dict(dur=DUR, ev=sorted(ev)), open('sfx.json', 'w'))
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p', os.environ.get('OUT', 'video_noaudio.mp4')], stdin=subprocess.PIPE)
        lo, hi = (int(os.environ.get('F0', 0)), int(os.environ.get('F1', N)))
        for i in range(lo, hi):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 150 == 0: print(i, N, flush=True)
        p.stdin.close(); p.wait(); print('done')
