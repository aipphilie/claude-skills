"""СДВГ-монтаж «Чаевые — это налог» (сценарий Ярослава). Движок «Привычек богатых» (compose_bg.py).
python3 compose_ch.py 1.5 12.3 -> prev_*.png;  python3 compose_ch.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_ch import *
YB = lambda C, u, seed=1: (C.paste(YEL, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(246, 200, 0), seed=seed))
RB = lambda C, u, seed=1: (C.paste(RED, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(206, 30, 40), seed=seed))
BB = lambda C, u, seed=1: (C.paste(BLK, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(34, 34, 34), seed=seed))
def tw(t, w, k=0): return t - T(w, k)
FOOT = None    # сноска внизу кадра (над субтитрами)

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_hook(C, u, t):   # Два доллара тринадцать центов в час!
    YB(C, u); burst(C, 380, 860, 300, u, 16, WHITE, INK)
    check(C, 380, 860, 400, [('ОФИЦИАНТ', '1 ЧАС')], '$2.13', -6, back(u / 0.22))
    waiter(C, 'jaw', u, 820, 0.42, G + 40, flip=True)
    slam(C, u, 'ЧАЕВЫЕ —', 540, 360, 120); plate(C, u - 0.15, 'ЭТО НАЛОГ', 540, 520, 100, INK, YEL, -3)
def s_usa(C, u, t):   # Столько в Америке может получать официант
    ground(C); usflag(C, 300, 820, 380, u); D(C).rectangle([104, 700, 116, G], fill=INK)
    waiter(C, 'tray', u, 720, 0.5); tray(C, 820, G - 0.5 * 1000 - 30, 170)
    slam(C, u, 'В АМЕРИКЕ', 540, 400, 140)
    if tw(t, 'официант.') > -0.1: plate(C, tw(t, 'официант.') + 0.1, 'ОФИЦИАНТ', 540, 560, 90, INK, YEL, 3)
def s_legal(C, u, t):   # Законно.
    ground(C); a = -40 + 55 * eo(u / 0.25); gavel(C, 640, 760, 1.4, a); D(C).rectangle([300, G - 60, 780, G], fill=WOODD, outline=INK, width=7)
    if u > 0.25: stamp(C, u - 0.25, 'ЗАКОННО', 540, 1080, 120, RED, -8)
    check(C, 250, 900, 260, [], '$2.13', 8, tsz=80)
def s_you(C, u, t):   # А доплачиваешь ему ты.
    ground(C); man(C, 'pay', u, 280, G, 0.44); waiter(C, 'idle', u, 820, 0.44, flip=True); dflow(C, u, 400, 860, 720, 860, 4, 30, 180)
    slam(C, u, 'ДОПЛАЧИВАЕШЬ', 540, 400, 120)
    if tw(t, 'ты.') > -0.1: plate(C, tw(t, 'ты.') + 0.1, 'ТЫ', 540, 570, 130, RED, WHITE, -4)
def s_where(C, u, t):   # Откуда это пошло?
    ground(C); man(C, 'think', u, 540, G, 0.5); qmark(C, 260, 760, 260, u); qmark(C, 830, 700, 200, u + 1)
    slam(C, u, 'ОТКУДА', 540, 400, 170); plate(C, u - 0.2, 'ЭТО ПОШЛО?', 540, 570, 90, INK, YEL, 3)
def s_notus(C, u, t):   # Чаевые придумали не американцы.
    ground(C); usflag(C, 540, 880, 560, u); xcross(C, tw(t, 'не', 0) - 0.1, 540, 880, 300, RED, 26)
    slam(C, u, 'ПРИДУМАЛИ', 540, 400, 140); plate(C, tw(t, 'американцы.'), 'НЕ АМЕРИКАНЦЫ', 540, 570, 90, INK, YEL, -3)
def s_noble(C, u, t):   # Европейская знать кидала монетку слугам
    ground(C); aristo(C, 'throw', u, 280, 0.5); waiter(C, 'bow', u, 830, 0.36, flip=True)
    q = (u * 0.9) % 1; dcoin(C, lerp(420, 800, q), lerp(760, 1000, q) - 260 * s_(math.pi * q), 34, q * 720)
    slam(C, u, 'ЕВРОПЕЙСКАЯ', 540, 400, 130)
    if tw(t, 'знать') > -0.1: plate(C, tw(t, 'знать') + 0.1, 'ЗНАТЬ', 540, 560, 100, INK, YEL, 3)
def s_barin(C, u, t):   # показать, кто тут барин.
    YB(C, u, 3); aristo(C, 'laugh', u, 540, 0.56, G + 40)
    for j in range(6): dcoin(C, 140 + j * 160, 700 + 40 * s_(u * 5 + j), 36, u * 200 + j * 40)
    slam(C, u, 'КТО ТУТ', 540, 380, 150); plate(C, tw(t, 'барин.'), 'БАРИН', 540, 545, 120, INK, YEL, -3)
def s_ship(C, u, t):   # Богатые американцы привезли эту моду из Европы
    water(C, G - 40, u); steamer(C, lerp(380, 600, eo(u / 2.0)), G - 60, 0.95, u); aristo(C, 'wave', u, lerp(330, 550, eo(u / 2.0)), 0.2, G - 60 - 0.95 * 240)
    slam(C, u, 'МОДУ ИЗ ЕВРОПЫ', 540, 400, 110); plate(C, u - 0.2, 'ЕВРОПА → США', 540, 545, 70, INK, YEL, 3)
def s_aristo(C, u, t):   # чтобы выглядеть по-аристократски.
    ground(C); aristo(C, 'boss', u, 380, 0.52); man(C, 'idle_smile', u, 820, 0.4, flip=True)
    for j, (x, y) in enumerate([(200, 640), (560, 700), (300, 1000)]):
        burst(C, x, y, 30 + 10 * s_(u * 8 + j), u, 4, YEL, INK, j)
    slam(C, u, 'ПО-АРИСТОКРАТСКИ', 540, 400, 100)
def s_hard(C, u, t):   # А дальше жёстко.
    BB(C, u); tape(C, u, 'ДАЛЬШЕ ЖЁСТКО', 880, 150, -5); tape(C, u - 0.15, 'ДАЛЬШЕ ЖЁСТКО', 1090, 110, 4)
def s_war(C, u, t):   # После Гражданской войны
    ground(C); calendar(C, 540, 880, 0.9, '1865', 'КОНЕЦ ВОЙНЫ', back(u / 0.22), -3)
    slam(C, u, 'ПОСЛЕ', 540, 380, 130); plate(C, tw(t, 'Гражданской'), 'ГРАЖДАНСКОЙ ВОЙНЫ', 540, 540, 76, INK, YEL, 3)
def s_hire(C, u, t):   # освобождённых рабов брали официантами
    ground(C); table(C, 330, G - 150, 420, 150); dish(C, 330, G - 200, 90); waiter(C, 'tray', u, 760, 0.5); tray(C, 860, G - 530, 170)
    slam(C, u, 'БРАЛИ', 540, 400, 150); plate(C, tw(t, 'официантами'), 'ОФИЦИАНТАМИ', 540, 560, 90, INK, YEL, -3)
def s_train(C, u, t):   # и проводниками в поезда.
    railcar(C, lerp(700, 540, eo(u / 0.8)), G + 40, 920, u, ''); waiter(C, 'bow', u, lerp(860, 700, eo(u / 0.8)), 0.3, G + 40)
    slam(C, u, 'И ПРОВОДНИКАМИ', 540, 400, 110); plate(C, tw(t, 'поезда.'), 'В ПОЕЗДА', 540, 560, 90, INK, YEL, 3)
def s_nopay(C, u, t):   # И почти не платили.
    ground(C); kassa(C, 560, G - 120, 1.2, u - 0.3, '$0'); D(C).rectangle([380, G - 120, 740, G], fill=WOODD, outline=INK, width=7)
    rich(C, 'boss', u, 220, 0.42); waiter(C, 'sad', u, 900, 0.4, flip=True)
    slam(C, u, 'ПОЧТИ', 540, 380, 140); plate(C, tw(t, 'не', 0), 'НЕ ПЛАТИЛИ', 540, 540, 100, RED, WHITE, -3)
def s_live(C, u, t):   # «Живи на чаевые».
    ground(C); rich(C, 'point', u, 280, 0.44); waiter(C, 'hat', u, 800, 0.44, flip=True); bowler(C, 800, G - 0.44 * 560, 170)
    if u > 0.3: dcoin(C, 800, lerp(500, G - 0.44 * 560 - 10, eo(((u - 0.3) * 1.4) % 1)), 26)
    speech(C, 360, 430, 600, 210, back(u / 0.2)); put(C, text_img('ЖИВИ\nНА ЧАЕВЫЕ', 70, INK), 366, 470, back(u / 0.2))
def s_profit(C, u, t):   # Бизнесу выгодно
    YB(C, u, 5); rich(C, 'laugh', u, 380, 0.5, G + 40); moneybag(C, 820, G + 40, max(0.15, 1.1 * back(u / 0.25)), 6 * s_(u * 6))
    slam(C, u, 'БИЗНЕСУ', 540, 380, 150); plate(C, tw(t, 'выгодно:'), 'ВЫГОДНО', 540, 545, 110, INK, WHITE, 3)
def s_scheme(C, u, t):   # работник есть, а платит за него клиент.
    ground(C); desk(C, 540, G, 340, 260); rich(C, 'boss', u, 540, 0.34, G - 260); tag(C, u - 0.1, 'ПЛАТИТ $0', 540, G - 150, 44, WHITE, INK)
    waiter(C, 'idle', u, 210, 0.36); man(C, 'pay', u, 880, 0.36, flip=True); dflow(C, u, 790, 1000, 290, 1000, 5, 26, 150)
    slam(C, u, 'РАБОТНИК ЕСТЬ', 540, 380, 110)
    if tw(t, 'платит', 0) > -0.1: plate(C, tw(t, 'платит', 0) + 0.1, 'ПЛАТИТ КЛИЕНТ', 540, 540, 86, RED, WHITE, -3)
def s_angry(C, u, t):   # Людей это бесило.
    RB(C, u, 7)
    for j, x in enumerate((200, 540, 880)): man(C, 'angry', u + j * 0.3, x, G + 40, 0.36 + 0.06 * (j == 1), flip=j == 2)
    slam(C, u, 'ЛЮДЕЙ', 540, 380, 150, WHITE); plate(C, tw(t, 'бесило.'), 'БЕСИЛО', 540, 545, 120, INK, YEL, 3)
STATES = ['ВАШИНГТОН', 'МИССИСИПИ', 'АРКАНЗАС', 'АЙОВА', 'ЮЖНАЯ КАРОЛИНА', 'ТЕННЕССИ']
def s_states(C, u, t):   # В начале двадцатого века шесть штатов
    for j, n in enumerate(STATES):
        x = 300 if j % 2 == 0 else 780; y = 760 + (j // 2) * 160
        tag(C, u - 0.12 * j, n, x, y, 62, WHITE if j % 2 else YEL, INK, (-3, 3)[j % 2])
    slam(C, u, '6 ШТАТОВ', 540, 380, 160); plate(C, u - 0.2, '1909–1915', 540, 545, 80, INK, YEL, -3)
def s_ban(C, u, t):   # запретили чаевые законом.
    ground(C); man(C, 'sign', u, 540, G, 0.44); placard(C, 540, G - 0.44 * 1250, 400, 'NO TIPS', 4 * s_(u * 8))
    if tw(t, 'законом.') > 0: stamp(C, tw(t, 'законом.'), 'ЗАПРЕЩЕНО', 540, 1120, 90, RED, -10)
    slam(C, u, 'ЗАПРЕТИЛИ', 540, 380, 140)
def s_rip(C, u, t):   # Но запреты не прижились
    ground(C); man(C, 'shrug', u, 540, G, 0.44); placard(C, 540, G - 0.44 * 1250, 400, 'NO TIPS', 0, clamp((u - 0.2) / 1.6), u)
    slam(C, u, 'НЕ ПРИЖИЛИСЬ', 540, 380, 130)
def s_1926(C, u, t):   # и к середине двадцатых их все отменили.
    ground(C); calendar(C, 540, 880, 0.9, '1926', 'К ЭТОМУ ГОДУ', back(u / 0.22), 3)
    if tw(t, 'отменили.') > 0: stamp(C, tw(t, 'отменили.'), 'ВСЁ ОТМЕНИЛИ', 540, 1110, 90, RED, -8)
    slam(C, u, 'К СЕРЕДИНЕ 20-Х', 540, 380, 110)
def s_gov(C, u, t):   # А потом государство
    ground(C); capitol(C, 540, G, max(0.1, back(u / 0.25)), u)
    slam(C, u, 'ГОСУДАРСТВО', 540, 380, 130)
def s_law(C, u, t):   # схему узаконило.
    ground(C); doc(C, 540, 900, 460, 560, 'ЗАКОН', -3, back(u / 0.2), 'О МИНИМАЛКЕ', True)
    if tw(t, 'узаконило.') > 0.1: stamp(C, tw(t, 'узаконило.') - 0.1, 'УЗАКОНЕНО', 540, 1060, 90, RED, -10)
    slam(C, u, 'СХЕМУ', 540, 380, 150)
def s_minw(C, u, t):   # Для официантов отдельная минималка.
    ground(C); pricetag(C, 540, 790, 1.9, 'ВСЕМ', '$7.25', -4, WHITE, back(u / 0.2)); pricetag(C, 540, 1110, 1.9, 'ОФИЦИАНТУ', '$2.13', 3, YEL, back((u - 0.25) / 0.2))
    slam(C, u, 'ОТДЕЛЬНАЯ', 540, 380, 140); plate(C, tw(t, 'минималка.'), 'МИНИМАЛКА', 540, 545, 100, INK, YEL, -3)
def s_now(C, u, t):   # Сейчас это два доллара тринадцать центов.
    YB(C, u, 9); check(C, 540, 900, 520, [('СТАВКА', 'В ЧАС')], '$2.13', -3, back(u / 0.22), 190); waiter(C, 'sad', u, 900, 0.3, G + 40, flip=True)
    slam(C, u, 'СЕЙЧАС', 540, 380, 150)
    put(C, plate_img('* если чаевых не хватит, хозяин обязан доплатить до $7.25', 28, WHITE, INK, pad=12, r=8, border=INK, bw=3), 540, 1322)
def s_rest(C, u, t):   # Остальное, мол, доберёт чаевыми.
    ground(C); check(C, 420, 1000, 380, [], '$2.13', -4, tsz=120)
    k = eo(u / 0.4); bighand(C, 1250, 300, lerp(1200, 760, k), lerp(380, 640, k), 150)
    if u > 0.3:
        for j in range(5):
            q = ((u - 0.3) * 1.3 + j / 5) % 1; dcoin(C, 700 - j * 40 + 30 * s_(j), lerp(700, 1080, q), 34, q * 400)
    dstack(C, 650, 1180, int(clamp(u / 1.2) * 6), 50)
    slam(C, u, 'ДОБЕРЁТ', 540, 380, 150); plate(C, tw(t, 'чаевыми.'), 'ЧАЕВЫМИ', 540, 545, 110, INK, YEL, 3)
def s_twice(C, u, t):   # Получается, за ужин ты платишь дважды.
    YB(C, u, 4); man(C, 'pay', u, 330, G + 40, 0.48); txt(C, '×2', 790, 900, 300 * back(clamp(tw(t, 'дважды.') / 0.25)) if tw(t, 'дважды.') > 0 else 1, RED, 1, -8, 1 if tw(t, 'дважды.') > 0 else 0, INK, 10)
    slam(C, u, 'ПЛАТИШЬ', 540, 380, 150); plate(C, tw(t, 'дважды.'), 'ДВАЖДЫ', 540, 545, 120, INK, WHITE, -3)
def s_owner(C, u, t):   # Владельцу за еду.
    ground(C); man(C, 'pay', u, 230, G, 0.4); rich(C, 'idle', u, 850, 0.4, flip=True); table(C, 540, G - 120, 300, 120); dish(C, 540, G - 165, 80)
    dflow(C, u, 330, 900, 750, 900, 3, 28, 150)
    slam(C, u, 'ВЛАДЕЛЬЦУ', 540, 380, 140); plate(C, tw(t, 'еду.'), 'ЗА ЕДУ', 540, 545, 110, INK, YEL, 3)
def s_wtr(C, u, t):   # А официанту за то, что владелец ему не платит.
    ground(C); man(C, 'pay', u, 230, G, 0.4); waiter(C, 'idle', u, 850, 0.4, flip=True); dflow(C, u, 330, 900, 750, 900, 3, 28, 150)
    slam(C, u, 'ОФИЦИАНТУ', 540, 380, 140)
    if tw(t, 'владелец') > -0.1: plate(C, tw(t, 'владелец') + 0.1, 'ЗА ТО, ЧТО ЕМУ НЕ ПЛАТЯТ', 540, 545, 64, RED, WHITE, -3)
def s_thanks(C, u, t):   # Чаевые — это не благодарность.
    ground(C); heart(C, 540, 880, 230, HRT, 6 * s_(u * 5), clamp((tw(t, 'благодарность.')) / 0.4))
    slam(C, u, 'ЧАЕВЫЕ —', 540, 380, 140); plate(C, tw(t, 'благодарность.') - 0.25, 'НЕ БЛАГОДАРНОСТЬ', 540, 545, 90, INK, YEL, 3)
def s_tax(C, u, t):   # Это налог,
    RB(C, u, 2); check(C, 540, 920, 600, [('ЕДА', '$40'), ('ЗП ОФИЦИАНТА', '$8')], None, -3, back(u / 0.22), hl=1)
    stamp(C, u - 0.25, 'НАЛОГ', 540, 1150, 130, INK, -10)
    slam(C, u, 'ЭТО НАЛОГ', 540, 380, 150, WHITE)
def s_shift(C, u, t):   # который бизнес переложил на тебя.
    ground(C); rich(C, 'give', u, 230, 0.4); man(C, 'shock', u, 870, 0.4, flip=True)
    k = eo(clamp(tw(t, 'переложил') / 0.5)); box(C, lerp(400, 720, k), lerp(G - 330, G - 300, k) - 120 * s_(math.pi * k), 260, 170, 'ЗАРПЛАТА', 6 * s_(u * 6), sz=34)
    slam(C, u, 'ПЕРЕЛОЖИЛ', 540, 380, 140)
    if tw(t, 'тебя.') > -0.1: plate(C, tw(t, 'тебя.') + 0.1, 'НА ТЕБЯ', 540, 545, 120, RED, WHITE, 3)
def s_vse(C, u, t):   # Всё.
    ground(C); man(C, 'turn', u, 540, G, 0.54); check(C, 540, G - 0.54 * 560, 200, [('ЕДА', '$40'), ('ЗП', '$8')], None, 0, hl=1)
    slam(C, u, 'ВСЁ.', 540, 400, 180)
def s_netupi(C, u, t):   # Не тупи.
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    man(C, 'pointcam', u, 540, G + 40, 0.56)
    slam(C, u, 'НЕ ТУПИ', 540, 420, 190)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'boom'), SH(T('Столько') - 0.05, s_usa, 'whipL', 'whoosh'), SH(T('Законно.') - 0.05, s_legal, 'shake', 'boom'),
 SH(T('А', 0) - 0.05, s_you, 'whipR', 'whoosh'), SH(T('Откуда') - 0.05, s_where, 'push', 'bass'), SH(T('Чаевые', 0) - 0.05, s_notus, 'zoom', 'whoosh'),
 SH(T('Европейская') - 0.05, s_noble, 'door', 'thud'), SH(T('показать,') - 0.05, s_barin, 'zoom', 'boom'),
 SH(T('Богатые') - 0.05, s_ship, 'whipL', 'whoosh'), SH(T('чтобы') - 0.05, s_aristo, 'whipR', 'whoosh'),
 SH(T('А', 1) - 0.05, s_hard, 'glitch', 'riser'), SH(T('После') - 0.05, s_war, 'drop', 'thud'), SH(T('освобождённых') - 0.05, s_hire, 'whipL', 'whoosh'),
 SH(T('проводниками') - 0.05, s_train, 'whipR', 'whoosh'), SH(T('И', 0) - 0.05, s_nopay, 'shake', 'boom'), SH(T('Живи') - 0.05, s_live, 'zoom', 'whoosh'),
 SH(T('Бизнесу') - 0.05, s_profit, 'push', 'bass'), SH(T('работник') - 0.05, s_scheme, 'whipL', 'whoosh'),
 SH(T('Людей') - 0.05, s_angry, 'shake', 'boom'), SH(T('В', 0) - 0.05, s_states, 'zoomthru', 'whoosh', (540, 880)), SH(T('запретили') - 0.05, s_ban, 'whipR', 'whoosh'),
 SH(T('Но') - 0.05, s_rip, 'door', 'thud'), SH(T('середине') - 0.05, s_1926, 'zoom', 'bass'),
 SH(T('А', 2) - 0.05, s_gov, 'drop', 'thud'), SH(T('схему') - 0.05, s_law, 'whipL', 'whoosh'), SH(T('Для') - 0.05, s_minw, 'whipR', 'whoosh'),
 SH(T('Сейчас') - 0.05, s_now, 'zoom', 'boom'), SH(T('Остальное,') - 0.05, s_rest, 'bodywipe', 'bass'),
 SH(T('Получается,') - 0.05, s_twice, 'push', 'bass'), SH(T('Владельцу') - 0.05, s_owner, 'whipL', 'whoosh'), SH(T('А', 3) - 0.05, s_wtr, 'whipR', 'whoosh'),
 SH(T('Чаевые', 1) - 0.05, s_thanks, 'zoom', 'bass'), SH(T('Это') - 0.05, s_tax, 'shake', 'boom'), SH(T('который') - 0.05, s_shift, 'whipL', 'whoosh'),
 SH(T('Всё.') - 0.05, s_vse, 'door', 'thud'), SH(T('Не', 0) - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('доллара', 0), 'kassa'), (T('час!'), 'pop'), (T('официант.') + 0.1, 'pop'), (T('Законно.') + 0.25, 'stamp'), (T('ты.'), 'pop'),
       (T('пошло?'), 'pop'), (T('американцы.'), 'error'), (T('знать'), 'pop'), (T('монетку'), 'coins'), (T('барин.'), 'shine'),
       (T('Европы,'), 'pop'), (T('по-аристократски.'), 'shine'), (T('Гражданской'), 'pop'), (T('официантами'), 'pop'), (T('поезда.'), 'pop'),
       (T('И', 0) + 0.25, 'click'), (T('не', 0), 'error'), (T('чаевые»'), 'coins'), (T('выгодно:'), 'kassa'), (T('клиент.'), 'coins'),
       (T('бесило.'), 'pop'), (T('шесть'), 'pop'), (T('законом.'), 'stamp'), (T('прижились,'), 'scratch'), (T('отменили.'), 'stamp'),
       (T('узаконило.'), 'stamp'), (T('минималка.'), 'pop'), (T('доллара', 1), 'kassa'), (T('Остальное,') + 0.35, 'coins'), (T('чаевыми.'), 'pop'),
       (T('дважды.'), 'boom'), (T('еду.'), 'kassa'), (T('платит.'), 'error'), (T('благодарность.'), 'crack'), (T('Это') + 0.25, 'stamp'),
       (T('переложил'), 'swipe'), (T('тебя.'), 'pop'), (T('тупи.'), 'stamp')]
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
