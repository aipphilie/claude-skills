"""СДВГ-монтаж «Реальные привычки богатых» (по присланному рилсу; поворот: стань богатой семьёй сам). Движок «Конца света» (compose_ap.py).
python3 compose_bg.py 1.5 12.3 -> prev_*.png;  python3 compose_bg.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_bg import *
YB = lambda C, u, seed=1: (C.paste(YEL, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(246, 200, 0), seed=seed))
RB = lambda C, u, seed=1: (C.paste(RED, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(206, 30, 40), seed=seed))
BB = lambda C, u, seed=1: (C.paste(BLK, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(34, 34, 34), seed=seed))

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_h5(C, u, t):   # Подъём в пять утра
    YB(C, u); alarm(C, 540, 860, 1.05, u); man(C, 'scream', u, 200, G + 60, 0.3); man(C, 'shock', u + .2, 880, G + 60, 0.3, flip=True)
    slam(C, u, 'ПОДЪЁМ В 5:00', 540, 400, 130)
def s_smoo(C, u, t):   # смузи
    ground(C); smoothie(C, 540, G - 20, 1.2 * back(u / 0.2), 6 * s_(u * 8)); man(C, 'think', u, 870, G, 0.32)
    slam(C, u, 'СМУЗИ', 540, 400, 170)
def s_run(C, u, t):   # полумарафон
    speedlines(C, 540, 900, u, r0=420, col=LG); ground(C)
    d = D(C); x = 940; d.rectangle([x - 12, 760, x + 12, G], fill=STEEL2); d.rectangle([x - 40, 700, x + 140, 770], fill=RED, outline=INK, width=5); put(C, text_img('21 КМ', 40, WHITE), x + 50, 735)
    man(C, 'run', u * 1.8, lerp(160, 560, eo(u / 1.0)), G, 0.42, flip=False)
    slam(C, u, 'ПОЛУМАРАФОН', 540, 400, 130)
def s_hn(C, u, t):   # Хуйня это всё!
    RB(C, u)
    for j, w in enumerate(['ПОДЪЁМ В 5:00', 'СМУЗИ', 'ПОЛУМАРАФОН']):
        y = 680 + j * 130; txt(C, w, 540, y, 100, WHITE); tw = text_img(w, 100, WHITE).width
        strike(C, u - 0.08 * j, 540 - tw / 2 - 20, y + 4, 540 + tw / 2 + 20, y + 4, INK, 18)
    stamp(C, u - 0.25, 'Х*ЙНЯ', 540, 1120, 150, YEL, -9)
    slam(C, u, 'ЭТО ВСЁ', 540, 420, 130, WHITE)
def s_real(C, u, t):   # Вот реальные привычки
    ground(C); rich(C, 'walkR', u, lerp(-100, 540, eo(u / 0.6)), 0.48)
    slam(C, u, 'РЕАЛЬНЫЕ', 540, 400, 150); plate(C, t - T('привычки'), 'ПРИВЫЧКИ', 540, 560, 110, INK, YEL, -3)
def s_bog(C, u, t):   # богатых
    YB(C, u, 3); burst(C, 540, 860, 380, u, 16, WHITE, INK)
    for j in range(8):
        q = (u * 1.3 + j / 8) % 1; coin(C, 90 + j * 128, 620 + 700 * q, 46, j * 40 + u * 300)
    rich(C, 'armsup', u, 540, 0.56, G + 40)
    slam(C, u, 'БОГАТЫХ', 540, 400, 190)
def s_n1(C, u, t): bigno(C, u, 1, 'ПЕРВОЕ')
def s_1a(C, u, t):   # Наёбывать
    ground(C); rich(C, 'laugh', u, 300, 0.42); envelope(C, 760, 860, 300, -8, 'ЗАРПЛАТА', cash=0)
    v = t - T('Наёбывать')
    if v > 0.3: stamp(C, v - 0.3, 'ПУСТО', 760, 1010, 70, RED, 10)
    head(C, u, 'НАЁ*ЫВАТЬ', None, n=1, sza=150)
def s_1b(C, u, t):   # своих сотрудников
    ground(C); rich(C, 'boss', u, 220, 0.38)
    man(C, 'idle_sad', u, 500, G, 0.3); welder(C, 'sad', u + .3, 700, 0.3); girl(C, 'sad', u + .6, 900, 0.3)
    head(C, u, 'СВОИХ', 'СОТРУДНИКОВ', T('сотрудников') - t + u, n=1)
def s_1c(C, u, t):   # «Мы же семья!»
    YB(C, u, 5); rich(C, 'hug', u, 540, 0.5, G + 40)
    man(C, 'idle_sad', u, 170, G + 40, 0.28); welder(C, 'sad', u, 910, 0.28, G + 40)
    speech(C, 540, 640, 700, 230, back(u / 0.2)); txt(C, 'МЫ ЖЕ СЕМЬЯ!', 540, 630, 96, INK, back(u / 0.2))
    badge(C, 1, 1)
def s_n2(C, u, t): bigno(C, u, 2, 'ВТОРОЕ')
def s_2(C, u, t):   # Не платить налоги
    ground(C); taxbox(C, 720, G, 1.05, '')
    rich(C, 'shh', u, 280, 0.42)
    head(C, u, 'НЕ ПЛАТИТЬ', 'НАЛОГИ', t - T('налоги'), n=2)
    if t > T('налоги'): stamp(C, t - T('налоги') - 0.1, '0 ₽', 720, 1060, 110, RED, -8)
def s_n3(C, u, t): bigno(C, u, 3, 'ТРЕТЬЕ')
def s_3a(C, u, t):   # Брать
    ground(C); table(C, 540, 1020, 760); rich(C, 'idle', u, 230, 0.4); dad(C, 'reach', u, 860, 0.4, flip=True)
    envelope(C, lerp(800, 330, eo(u / 0.5)), 1110, 170, 0, '', cash=2)
    head(C, u, 'БРАТЬ', None, n=3, sza=170)
def s_3b(C, u, t):   # откаты
    RB(C, u, 3); envelope(C, 540, 900, 560 * back(u / 0.2), -6 + 3 * s_(u * 6), 'ОТКАТ', cash=4)
    slam(C, u, 'ОТКАТЫ', 540, 420, 180, WHITE); badge(C, 3, 1)
def s_n4(C, u, t): bigno(C, u, 4, 'ЧЕТВЁРТОЕ')
def s_4a(C, u, t):   # Стирать деньги
    ground(C); wash(C, 540, G, 1.25, u, True, clamp(u / 0.8))
    head(C, u, 'СТИРАТЬ', 'ДЕНЬГИ', t - T('деньги'), n=4)
def s_4b(C, u, t):   # через прачечную
    ground(C); shop(C, 600, G, 640, 520, 'ПРАЧЕЧНАЯ', u); rich(C, 'wave', u, 190, 0.38)
    for j in range(4): bill(C, 600 + (j - 1.5) * 90, 860 - 80 * s_(u * 4 + j), 110, 12 * s_(u * 3 + j))
    head(C, u, 'ЧЕРЕЗ', 'ПРАЧЕЧНУЮ', t - T('прачечную'), n=4)
def s_n5(C, u, t): bigno(C, u, 5, 'ПЯТОЕ')
def s_5a(C, u, t):   # Бухать неделями
    ground(C); table(C, 540, 1080, 860, 190)
    for j, x in enumerate((240, 420, 640, 820)): bottle(C, x, 1050, 0.5, (j - 1.5) * 4)
    rich(C, 'drink', u, 540, 0.36, 1050); man(C, 'cheer', u + .3, 200, 1050, 0.3); dad(C, 'cheer', u + .5, 880, 0.3, 1050)
    head(C, u, 'БУХАТЬ', 'НЕДЕЛЯМИ', t - T('неделями'), n=5)
def s_5b(C, u, t):   # с партнёрами
    YB(C, u, 7)
    for j, dd in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']):
        q = clamp((u - j * 0.06) / 0.5); calendar(C, 140 + j * 133, 700 + 420 * eo(q) - 60 * (j % 2), 0.38, dd, 'ПЬЁМ', 1, (j - 3) * 9)
    rich(C, 'drink', u, 540, 0.42, G + 40); bottle(C, 790, G + 40, 0.7, 12)
    head(C, u, 'С ПАРТНЁРАМИ', None, n=5, sza=120)
def s_5c(C, u, t):   # Это называется «стратегическая сессия»
    ground(C); flipchart(C, 800, G, 1.0, 'ПЛАН: ЕЩЁ'); table(C, 380, 1100, 520, 170)
    for j, x in enumerate((220, 330, 450, 540)): bottle(C, x, 1070, 0.42, (j - 1.5) * 25 * clamp(u / 0.4))
    rich(C, 'drink', u, 380, 0.34, 1070)
    slam(C, u, 'ЭТО НАЗЫВАЕТСЯ', 540, 400, 100)
    v = t - T('стратегическая')
    if v > -0.05: put(C, plate_img('СТРАТЕГИЧЕСКАЯ\nСЕССИЯ', 90, YEL, INK, pad=26, r=16, border=INK, bw=7), 540, 610, 1 + 0.5 * (1 - eo((v + 0.05) / 0.18)), -4)
    badge(C, 5, 1)
def s_n6(C, u, t): bigno(C, u, 6, 'ШЕСТОЕ')
def s_6a(C, u, t):   # Записывать яхту
    sky(C, 600); water(C, 1150, u); yacht(C, 520 + 30 * s_(u), 1180, 1.0, u, 'МЕЧТА')
    rich(C, 'pointcam', u, 830, 0.24, 930)
    head(C, u, 'ЗАПИСЫВАТЬ', 'ЯХТУ', t - T('яхту'), n=6)
def s_6b(C, u, t):   # на тёщу
    ground(C); girl(C, 'shock', u, 300, 0.42); label(C, 'ТЁЩА', 300, G - HEAD(0.42) - 70, 52, PINK, WHITE, -5)
    doc(C, 760, 880, 400, 500, 'ЯХТА', 6, back(u / 0.2), 'СОБСТВЕННИК:\nТЁЩА', True, 70)
    rich(C, 'shh', u, 930, 0.26, G)
    head(C, u, 'НА ТЁЩУ', None, n=6, sza=160)
def s_n7(C, u, t): bigno(C, u, 7, 'СЕДЬМОЕ')
def s_7a(C, u, t):   # Заносить
    ground(C); desk(C, 820, G, 420, 300); dad(C, 'idle', u, 860, 0.3, G - 120)
    x = lerp(120, 480, eo(u / 0.55)); rich(C, 'walkR', u, x, 0.4, chain=False); briefcase(C, x + 70, G - 300, 0.6)
    head(C, u, 'ЗАНОСИТЬ', None, n=7, sza=160)
def s_7b(C, u, t):   # чиновникам
    YB(C, u, 9); desk(C, 540, G + 40, 640, 300); dad(C, 'reach', u, 540, 0.42, G - 80)
    briefcase(C, 540, 1010, 1.0, 0, clamp(u / 0.5))
    head(C, u, 'ЧИНОВНИКАМ', None, n=7, sza=140)
    stamp(C, u - 0.4, 'ОДОБРЕНО', 540, 640, 90, GREEN, -8)
def s_n8(C, u, t): bigno(C, u, 8, 'ВОСЬМОЕ')
def s_8a(C, u, t):   # Выводить бабки
    sky(C, 0)
    for j in range(5): cloud(C, (j * 260 + u * -300) % 1400 - 160, 700 + (j % 3) * 170, 220, 90)
    plane(C, lerp(-200, 620, eo(u / 0.9)), 920 - 40 * s_(u * 3), 1.3, 4)
    head(C, u, 'ВЫВОДИТЬ', 'БАБКИ', t - T('бабки'), n=8)
def s_8b(C, u, t):   # на острова
    sky(C, 0); water(C, 1150, u); island(C, 540, 1160, 1.1, u)
    moneybag(C, 400, lerp(500, 1120, back(clamp(u / 0.5))), 0.8, -8)
    head(C, u, 'НА ОСТРОВА', None, n=8, sza=150)
def s_n9(C, u, t): bigno(C, u, 9, 'ДЕВЯТОЕ')
def s_9a(C, u, t):   # Обанкротить фирму
    ground(C); firm(C, 540, G, 1.3, 'ООО «РОМАШКА»', u, t - T('фирму'))
    head(C, u, 'ОБАНКРОТИТЬ', 'ФИРМУ', t - T('фирму'), n=9, sza=120)
def s_9b(C, u, t):   # и открыть такую же
    ground(C); firm(C, 290, G, 0.9, 'ООО «РОМАШКА»', 9, 1)
    k = back(clamp(u / 0.25)); 
    if k > 0.05: firm(C, 790, G, 0.9 * k, 'ООО «РОМАШКА-2»', u)
    rich(C, 'wave', u, 540, 0.3)
    head(C, u, 'И ОТКРЫТЬ', 'ТАКУЮ ЖЕ', t - T('такую'), n=9, sza=120)
def s_main(C, u, t):   # И самое главное
    BB(C, u); tape(C, u, 'САМОЕ ГЛАВНОЕ', 880, 150, -5); tape(C, u - 0.15, 'САМОЕ ГЛАВНОЕ', 1080, 110, 4)
    slam(C, u, 'ПУНКТ 10', 540, 420, 170, YEL)
def s_born(C, u, t):   # Родиться в богатой семье
    YB(C, u, 11); burst(C, 540, 980, 420, u, 18, WHITE, INK); crib(C, 540, G + 20, 1.25, u)
    for j in range(9):
        q = (u * 1.1 + j / 9) % 1; coin(C, 80 + j * 115, 560 + 760 * q, 42, j * 30 + u * 360)
    slam(C, u, 'РОДИТЬСЯ', 540, 400, 150); plate(C, t - T('богатой', 0), 'В БОГАТОЙ СЕМЬЕ', 540, 560, 80, INK, YEL, -3)
def s_smesh(C, u, t):   # Смешно?
    ground(C); man(C, 'laugh', u, 540, G, 0.56)
    slam(C, u, 'СМЕШНО?', 540, 420, 180)
LIST = ['НАЁ*ЫВАТЬ СВОИХ', 'НЕ ПЛАТИТЬ НАЛОГИ', 'БРАТЬ ОТКАТЫ', 'СТИРАТЬ ДЕНЬГИ', 'БУХАТЬ НЕДЕЛЯМИ', 'ЯХТА НА ТЁЩУ', 'ЗАНОСИТЬ', 'ВЫВОДИТЬ БАБКИ', 'БАНКРОТИТЬ', 'РОДИТЬСЯ БОГАТЫМ']
CRIME = [0, 1, 2, 3, 6, 7, 8]
def s_ugol(C, u, t):   # Половина списка — уголовка
    ground(C); rich(C, 'sad', u, 540, 0.5); bars(C, clamp((t - T('уголовка')) / 0.3), 220, 860, 720)
    slam(C, u, 'ПОЛОВИНА СПИСКА', 540, 400, 110)
    if t > T('уголовка'): plate(C, t - T('уголовка'), 'УГОЛОВКА', 540, 560, 110, RED, WHITE, -3)
def s_cirroz(C, u, t):   # Вторая половина — цирроз
    ground(C); liver(C, 640, 860, 1.2, clamp((t - T('цирроз')) / 0.3), u); label(C, 'ПЕЧЕНЬ', 640, 700, 56, WHITE, INK, -4); rich(C, 'sad', u, 260, 0.3, chain=False)
    for j in range(3): bottle(C, 420 + j * 60, G, 0.6, -10 + j * 20 - 60 * (j == 2))
    slam(C, u, 'ВТОРАЯ ПОЛОВИНА', 540, 400, 110)
    if t > T('цирроз'): stamp(C, t - T('цирроз'), 'ЦИРРОЗ', 640, 1120, 100, RED, -8)
def s_last(C, u, t):   # Работает только последний пункт
    listcard(C, 540, 960, 820, LIST, 9 if t > T('последний') else None, [j for j in range(9)], clamp(u / 0.6), (), back(u / 0.2))
    slam(C, u, 'РАБОТАЕТ ТОЛЬКО', 540, 360, 100); 
def s_nerod(C, u, t):   # Не родился в богатой семье?
    ground(C); man(C, 'shrug', u, 540, G, 0.5); crib(C, 860, G, 0.45, u, False); xcross(C, u - 0.2, 860, G - 90, 110, RED, 16)
    slam(C, u, 'НЕ РОДИЛСЯ', 540, 400, 150); plate(C, t - T('богатой', 1), 'В БОГАТОЙ?', 540, 560, 110, INK, YEL, 3)
def s_stan(C, u, t):   # Стань ею для своих детей
    YB(C, u, 13); man(C, 'pointcam', u, 380, G + 40, 0.5)
    v = t - T('детей'); child(C, 'cheer' if v > 0 else 'idle_smile', u, 800, 0.24, G + 40)
    if v > -0.2: crown(C, 806, lerp(300, G + 40 - HEAD(0.24) - 40, back(clamp((v + 0.2) / 0.35))), 120, -8)
    slam(C, u, 'СТАНЬ ЕЮ', 540, 400, 170); plate(C, t - T('своих', 1), 'ДЛЯ СВОИХ ДЕТЕЙ', 540, 560, 90, INK, YEL, -3)
def s_zp(C, u, t):   # Каждую зарплату
    ground(C); man(C, 'cheer', u, 300, G, 0.42); card(C, 760, 860, 420, -8, scale=back(u / 0.22)); put(C, plate_img('+ ЗАРПЛАТА', 60, GREEN, WHITE, pad=14, r=10, border=INK, bw=5), 760, 1060, back((u - 0.1) / 0.2), 4)
    slam(C, u, 'КАЖДУЮ', 540, 400, 170); plate(C, t - T('зарплату'), 'ЗАРПЛАТУ', 540, 560, 110, INK, YEL, 3)
def s_10(C, u, t):   # десять процентов себе
    ground(C); pie10(C, 380, 880, 250, clamp(u / 0.5), u); piggy(C, 820, G, 0.9, u)
    k = clamp((t - T('себе')) / 0.5)
    if k > 0: coin(C, lerp(440, 820, eo(k)), lerp(700, 980, ei(k)) - 180 * s_(math.pi * k), 50, k * 360)
    slam(C, u, '10%', 540, 420, 200); plate(C, t - T('себе'), 'СЕБЕ', 540, 590, 100, INK, YEL, -3)
def s_first(C, u, t):   # Первым делом, до всех трат
    items = ['СЕБЕ 10%', 'АРЕНДА', 'ЕДА', 'ДОСТАВКА', 'ХОТЕЛКИ']
    listcard(C, 540, 940, 720, items, 0, [], 0, (), back(u / 0.2))
    slam(C, u, 'ПЕРВЫМ ДЕЛОМ', 540, 400, 130)
    if t > T('до'): plate(C, t - T('до'), 'ДО ВСЕХ ТРАТ', 540, 560, 90, RED, WHITE, 3)
def s_nesm(C, u, t):   # Не смузи
    ground(C); smoothie(C, 540, G - 20, 1.1, 0); xcross(C, u - 0.05, 540, 880, 260, RED, 30)
    slam(C, u, 'НЕ СМУЗИ', 540, 400, 160)
def s_ne5(C, u, t):   # Не подъём в пять
    ground(C); alarm(C, 540, 880, 0.85, u, False); xcross(C, u - 0.05, 540, 880, 280, RED, 30)
    slam(C, u, 'НЕ ПОДЪЁМ В 5', 540, 400, 130)
def s_10b(C, u, t):   # Десять процентов
    YB(C, u, 15); burst(C, 540, 900, 400, u, 16, WHITE, INK)
    put(C, text_img('10%', 330, INK, WHITE, 14), 540, 900, back(u / 0.22), -5 + 2 * s_(u * 7))
    for j in range(8):
        q = (u * 1.2 + j / 8) % 1; coin(C, 90 + j * 128, 1300 - 760 * q, 40, j * 45)
    slam(C, u, 'ДЕСЯТЬ ПРОЦЕНТОВ', 540, 400, 110)
def s_skin(C, u, t):   # Скинь другу, который встаёт в пять
    ground(C); man(C, 'phone', u, 280, G, 0.42); alarm(C, 780, 820, 0.55, u)
    sms(C, 700, 1100, 520, 'ЧИТАЙ, ЖАВОРОНОК', clamp(u / 0.3))
    slam(C, u, 'СКИНЬ ДРУГУ', 540, 400, 140)
    if t > T('который'): plate(C, t - T('который'), 'КОТОРЫЙ ВСТАЁТ В 5', 540, 560, 80, INK, YEL, -3)
def s_netupi(C, u, t):   # И не тупи
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    man(C, 'pointcam', u, 540, G + 40, 0.56)
    slam(C, u, 'И НЕ ТУПИ', 540, 420, 180)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_h5, 'none', 'boom'), SH(T('смузи', 0) - 0.05, s_smoo, 'whipL', 'whoosh'), SH(T('полумарафон') - 0.05, s_run, 'whipR', 'whoosh'),
 SH(T('Хуйня') - 0.05, s_hn, 'shake', 'boom'), SH(T('Вот') - 0.05, s_real, 'push', 'bass'), SH(T('богатых') - 0.05, s_bog, 'zoom', 'boom'),
 SH(T('Первое') - 0.05, s_n1, 'zoom', 'bass'), SH(T('Наёбывать') - 0.05, s_1a, 'whipL', 'whoosh'), SH(T('своих', 0) - 0.05, s_1b, 'whipR', 'whoosh'),
 SH(T('Мы') - 0.05, s_1c, 'shake', 'boom'),
 SH(T('Второе') - 0.05, s_n2, 'spin', 'bass'), SH(T('Не', 0) - 0.05, s_2, 'zoomthru', 'whoosh', (540, 880)),
 SH(T('Третье') - 0.05, s_n3, 'zoom', 'bass'), SH(T('Брать') - 0.05, s_3a, 'whipL', 'whoosh'), SH(T('откаты') - 0.05, s_3b, 'shake', 'boom'),
 SH(T('Четвёртое') - 0.05, s_n4, 'glitch', 'bass'), SH(T('Стирать') - 0.05, s_4a, 'zoomthru', 'whoosh', (540, 880)), SH(T('через') - 0.05, s_4b, 'whipR', 'whoosh'),
 SH(T('Пятое') - 0.05, s_n5, 'spin', 'bass'), SH(T('Бухать') - 0.05, s_5a, 'door', 'thud'), SH(T('с', 0) - 0.05, s_5b, 'whipL', 'whoosh'),
 SH(T('Это') - 0.05, s_5c, 'zoom', 'whoosh'),
 SH(T('Шестое') - 0.05, s_n6, 'whipU', 'bass'), SH(T('Записывать') - 0.05, s_6a, 'drop', 'thud'), SH(T('на', 0) - 0.05, s_6b, 'whipR', 'whoosh'),
 SH(T('Седьмое') - 0.05, s_n7, 'zoom', 'bass'), SH(T('Заносить') - 0.05, s_7a, 'push', 'bass'), SH(T('чиновникам') - 0.05, s_7b, 'shake', 'boom'),
 SH(T('Восьмое') - 0.05, s_n8, 'glitch', 'bass'), SH(T('Выводить') - 0.05, s_8a, 'whipU', 'whoosh'), SH(T('на', 1) - 0.05, s_8b, 'zoomthru', 'whoosh', (620, 920)),
 SH(T('Девятое') - 0.05, s_n9, 'spin', 'bass'), SH(T('Обанкротить') - 0.05, s_9a, 'door', 'thud'), SH(T('и', 0) - 0.05, s_9b, 'whipL', 'whoosh'),
 SH(T('И', 0) - 0.05, s_main, 'glitch', 'riser'), SH(T('Родиться') - 0.05, s_born, 'zoom', 'boom'),
 SH(T('Смешно') - 0.05, s_smesh, 'drop', 'thud'), SH(T('Половина') - 0.05, s_ugol, 'whipL', 'whoosh'), SH(T('Вторая') - 0.05, s_cirroz, 'whipR', 'whoosh'),
 SH(T('Работает') - 0.05, s_last, 'zoom', 'whoosh'),
 SH(T('Не', 1) - 0.05, s_nerod, 'push', 'bass'), SH(T('Стань') - 0.05, s_stan, 'zoom', 'boom'),
 SH(T('Каждую') - 0.05, s_zp, 'bodywipe', 'bass'), SH(T('десять') - 0.05, s_10, 'whipL', 'whoosh'), SH(T('Первым') - 0.05, s_first, 'whipR', 'whoosh'),
 SH(T('Не', 2) - 0.05, s_nesm, 'shake', 'error'), SH(T('Не', 3) - 0.05, s_ne5, 'shake', 'error'), SH(T('Десять') - 0.05, s_10b, 'zoom', 'boom'),
 SH(T('Скинь') - 0.05, s_skin, 'door', 'thud'), SH(T('И', 1) - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('пять', 0), 'alarm'), (T('утра'), 'pop'), (T('Хуйня') + 0.25, 'stamp'), (T('привычки'), 'pop'), (T('Наёбывать') + 0.3, 'stamp'), (T('сотрудников'), 'pop'),
       (T('семья'), 'heart'), (T('налоги'), 'stamp'), (T('Брать') + 0.1, 'swipe'), (T('откаты'), 'kassa'), (T('деньги', 0), 'pop'), (T('прачечную'), 'ding'),
       (T('неделями'), 'pop'), (T('партнёрами'), 'pop'), (T('стратегическая'), 'stamp'), (T('яхту'), 'shine'), (T('тёщу'), 'boing'),
       (T('чиновникам') + 0.4, 'stamp'), (T('бабки'), 'coins'), (T('острова'), 'drop'), (T('фирму'), 'stamp'), (T('такую'), 'pop'),
       (T('самое'), 'pop'), (T('семье', 0), 'kassa'), (T('Смешно') + 0.2, 'scratch'), (T('уголовка'), 'clang'), (T('цирроз'), 'stamp'),
       (T('последний'), 'ding'), (T('богатой', 1), 'pop'), (T('детей'), 'shine'), (T('зарплату'), 'kassa'), (T('себе'), 'coins'),
       (T('до'), 'pop'), (T('трат'), 'pop'), (T('Десять') + 0.1, 'kassa'), (T('который'), 'msg'), (T('тупи'), 'stamp')]
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
CENS = {'БЛЯТЬ': 'БЛ*ТЬ', 'ХУЙНЯ': 'Х*ЙНЯ', 'НАЁБЫВАТЬ': 'НАЁ*ЫВАТЬ', 'СУКА': 'С*КА'}
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
    if t < 5.3: put(F, plate_img('Сатира. Все персонажи вымышлены. Не является инструкцией', 26, WHITE, GREY, pad=12, r=8, border=GREY, bw=3), 540, 1322, 1, 0, 1 - clamp((t - 5.0) / 0.3))
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
