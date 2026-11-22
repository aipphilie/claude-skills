"""СДВГ-монтаж «Сколько стоит твоя свобода». Движок «Дивана»/«Чаевых».
python3 compose_ch.py 1.5 12.3 -> prev_*.png;  python3 compose_ch.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_sv import *
YB = lambda C, u, seed=1: (C.paste(YEL, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(246, 200, 0), seed=seed))
RB = lambda C, u, seed=1: (C.paste(RED, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(206, 30, 40), seed=seed))
BB = lambda C, u, seed=1: (C.paste(BLK, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(34, 34, 34), seed=seed))
def tw(t, w, k=0): return t - T(w, k)
import base_k as _b
_slam0, _plate0 = slam, plate
def _fit(text, sz, lim=780):
    w = text_img(text, sz).width
    return sz * min(1.0, lim / w) if w else sz
def slam(C, u, text, cx, cy, sz=90, *a, **k): _slam0(C, u, text, cx, cy, _fit(text, sz), *a, **k)
def plate(C, u, text, cx, cy, sz=70, *a, **k): _plate0(C, u, text, cx, cy, _fit(text, sz, 740), *a, **k)
FOOT = None    # сноска внизу кадра (над субтитрами)

# ================= СЦЕНЫ «Сколько стоит твоя свобода» =================  fn(C, u, t)
VX = 690      # витрина справа, человечек слева
SY, PY = 410, 570     # заголовок и плашка (ниже кружков-счётчика)
def ttl(C, u, t, a, b=None, wb=None, rot=3, bcol=YEL, fcol=INK, sza=120, szb=96):
    slam(C, u, a, 540, SY, sza)
    if b:
        tb = tw(t, wb) if wb else u - 0.15
        if tb > -0.1: plate(C, tb + (0.1 if wb else 0), b, 540, PY, szb, bcol, fcol, rot)
def s_q(C, u, t):    # Сколько денег нужно, чтобы больше никогда не работать? Ответ в конце.
    ground(C); man(C, 'pointup', u, 250, G, 0.4); vitrina(C, VX, G, u=u)
    slam(C, u, 'СКОЛЬКО НУЖНО,', 540, SY, 116)
    if tw(t, 'чтобы') > -0.1: plate(C, tw(t, 'чтобы') + 0.1, 'ЧТОБЫ НЕ РАБОТАТЬ?', 540, PY, 92, YEL, INK, -3)
    if tw(t, 'Ответ') > -0.1: tag(C, tw(t, 'Ответ') + 0.1, 'ОТВЕТ В КОНЦЕ', 250, 760, 46, INK, YEL, -6)
def s_billion(C, u, t):   # Миллиард? Лотерея?
    ground(C); man(C, 'shrug', u, 250, G, 0.4)
    lot = tw(t, 'Лотерея?') > -0.05
    vitrina(C, VX, G, price='1 000 000 000?' if not lot else 'ЛОТЕРЕЯ?', psz=58, u=u)
    if lot:
        im = plate_img('БИЛЕТ  № 777', 40, (255, 240, 200), INK, pad=18, r=6, border=INK, bw=5); put(C, im, 250, 740 + 10 * s_(u * 6), back(tw(t, 'Лотерея?') / 0.2), 8)
    slam(C, u, 'МИЛЛИАРД?', 540, SY, 130, GREY)
    if lot: plate(C, tw(t, 'Лотерея?') + 0.05, 'ЛОТЕРЕЯ?', 540, PY, 96, LG, INK, 3)
def s_stop(C, u, t):   # Стоп. Тут ты тупишь.
    RB(C, u, 3); man(C, 'stop', u, 540, G, 0.46)
    slam(C, u, 'СТОП.', 540, SY, 170, WHITE)
    if tw(t, 'Тут') > -0.1: plate(C, tw(t, 'Тут') + 0.1, 'ТУТ ТЫ ТУПИШЬ', 540, PY, 100, YEL, INK, -3)
def s_three(C, u, t):   # Формула есть. Но сначала три вопроса.
    ground(C); man(C, 'explain', u, 250, G, 0.4)
    put(C, plate_img('? × ??? = ?', 70, WHITE, INK, pad=24, r=14, border=INK, bw=7), VX, 800, back(u / 0.2), -4)
    lock(C, VX + 200, 720, 0.55, back((u - 0.2) / 0.2), 10)
    slam(C, u, 'ФОРМУЛА ЕСТЬ.', 540, SY, 120)
    if tw(t, 'сначала') > -0.1: plate(C, tw(t, 'сначала') + 0.1, 'НО СНАЧАЛА 3 ВОПРОСА', 540, PY, 84, YEL, INK, 3)
    if tw(t, 'три') > -0.1: put(C, sticker('3', 110, YEL), VX, 1060, back(tw(t, 'три') / 0.2), -8)
def s_q1(C, u, t):   # Первый: почему эта цифра не зависит от зарплаты?
    ground(C); man(C, 'scratch', u, 260, G, 0.4)
    put(C, plate_img('ЗАРПЛАТА', 70, WHITE, INK, pad=22, r=12, border=INK, bw=7), VX, 820, back(u / 0.2), -3)
    if tw(t, 'зависит') > -0.1: strike(C, tw(t, 'зависит') + 0.05, VX - 200, 840, VX + 200, 800, RED, 16)
    qmark(C, VX, 1060, 150, u, INK)
    ttl(C, u, t, 'ВОПРОС 1', 'ПОЧЕМУ НЕ ОТ ЗАРПЛАТЫ?', 'зависит', -3, szb=80)
def s_q2(C, u, t):   # Второй: кто платит тебе зарплату, если ты не работаешь?
    ground(C); lie_chair(C, u, 420, G)
    k = clamp(u / 1.6); ex = lerp(1160, 640, eo(k)); envelope(C, ex, 760 - 60 * s_(k * 3.14), 200, -10 + 20 * k, 'ЗАРПЛАТА')
    if tw(t, 'работаешь?') > -0.1: tag(C, tw(t, 'работаешь?'), 'ОТ КОГО?', 860, 640, 50, INK, YEL, 6)
    ttl(C, u, t, 'ВОПРОС 2', 'КТО ПЛАТИТ ЗАРПЛАТУ?', 'платит', 3, szb=86)
def s_q3(C, u, t):   # И третий: где на чёрной пятнице главная скидка твоей жизни?
    ground(C); bfbanner(C, 760, u)
    sneakers(C, 830, G, 0.8)
    for j, cl in enumerate(('walkR', 'g_walkR', 'd_walkR', 'v_walkR')):
        man(C, cl, u * 1.6 + j * 0.3, (lerp(-140, 520, clamp(u / 2.4)) + j * 120 - 360) % 760, G + (j % 2) * 8, 0.26)
    ttl(C, u, t, 'ВОПРОС 3', 'ГДЕ ГЛАВНАЯ СКИДКА?', 'главная', -3, szb=86)
def s_a1(C, u, t):   # Ответ первый. Свобода считается от расходов.
    YB(C, u, 4); man(C, 'explain', u, 270, G, 0.4); basket(C, VX + 20, G, 0.9, 5, 0, u)
    ttl(C, u, t, 'ОТВЕТ 1', 'ОТ РАСХОДОВ', 'расходов.', 3, INK, WHITE)
def s_a1b(C, u, t):   # Кто получает триста тысяч и всё тратит, дальше от неё, чем тот, кто живёт на пятьдесят.
    ground(C)
    man(C, 'shrug', u, 300, G, 0.34); man(C, 'idle_smile', u, 780, G, 0.34)
    tag(C, u, '300 000', 300, 820, 54, WHITE, INK, -4)
    if tw(t, 'тратит,') > -0.1:
        q = tw(t, 'тратит,')
        for j in range(4):
            k = clamp((q - j * 0.18) / 0.6)
            if 0 < k < 1: bill(C, lerp(300, -60, k), 820 - 200 * s_(k * 3.14), 100, k * 200)
    if tw(t, 'дальше') > -0.1:
        k = eo(clamp(tw(t, 'дальше') / 0.5))
        put(C, plate_img('ДО СВОБОДЫ: ДАЛЕКО', 34, RED, WHITE, pad=12, r=8), 300, 700, k, -4)
    if tw(t, 'живёт') > -0.1:
        k = eo(clamp(tw(t, 'живёт') / 0.4)); tag(C, k, '50 000', 780, 820, 54, YEL, INK, 4)
        put(C, plate_img('ДО СВОБОДЫ: БЛИЖЕ', 34, YEL, INK, pad=12, r=8, border=INK, bw=4), 780, 700, k, 4)
    slam(C, u, 'КТО ТРАТИТ ВСЁ —', 540, SY, 104)
    if tw(t, 'дальше') > -0.1: plate(C, tw(t, 'дальше') + 0.1, 'ДАЛЬШЕ ОТ СВОБОДЫ', 540, PY, 84, INK, YEL, -3)
def s_a2(C, u, t):   # Ответ второй. Твои же деньги.
    ground(C); man(C, 'shock', u, 270, G, 0.4)
    k = clamp(u / 1.0); bagleg(C, lerp(1200, VX + 20, eo(k)), G, 1.25, u, 'ТВОИ', walk=k < 1)
    ttl(C, u, t, 'ОТВЕТ 2', 'ТВОИ ЖЕ ДЕНЬГИ', 'деньги.', -3)
def s_a2b(C, u, t):   # Бери из них около четырёх процентов в год — по американскому исследованию, их хватает десятилетиями.
    ground(C); lie_chair(C, u, 330, G)
    bagleg(C, 860, G, 1.35, 0, 'КАПИТАЛ', walk=False)
    if tw(t, 'четырёх') > -0.1: tag(C, tw(t, 'четырёх') + 0.05, '4% В ГОД', 860, 640, 56, INK, YEL, -4)
    per = 1.3; q = (u % per) / per; nb = int(u / per)
    if u > 0.3: bagleg(C, lerp(780, 470, eo(q)), G, 0.5, u, '', env='4%')
    if tw(t, 'десятилетиями.') > -0.3 or u > 2:
        yr = 2026 + min(30, int(clamp((u - 1.5) / 3.5) * 30)); calendar(C, 200, 760, 0.3, str(yr), 'ГОД', back((u - 1.5) / 0.2), -6)
    slam(C, u, 'БЕРИ ~4% В ГОД', 540, SY, 112)
    if tw(t, 'хватает') > -0.1: plate(C, tw(t, 'хватает') + 0.1, 'ХВАТАЕТ ДЕСЯТИЛЕТИЯМИ', 540, PY, 76, YEL, INK, 3)
    src(C, 'Ориентир: «правило 4%», Trinity University, США, 1998. Доход не гарантирован', 1340)
def s_a3(C, u, t):   # Ответ третий. Скидка на свободу.
    ground(C); bfbanner(C, 700, u)
    k = clamp((u - 0.2) / 0.8); man(C, 'walkR' if k < 1 else 'pointcam', u, lerp(200, 540, eo(k)), G, 0.4)
    ttl(C, u, t, 'ОТВЕТ 3', 'СКИДКА НА СВОБОДУ', 'свободу.', 3)
def s_a3b(C, u, t):   # Минус десять тысяч трат в месяц — и она дешевле на три миллиона.
    ground(C); basket(C, 260, G, 0.75, 5, clamp(u / 0.7), u)
    st = sticker('−3 млн', 110, YEL) if tw(t, 'дешевле') > -0.05 else None
    vitrina(C, VX + 20, G, w=420, stick=None, u=u)
    if st: put(C, st, VX + 120, 900, back(tw(t, 'дешевле') / 0.18), -12)
    slam(C, u, '−10 000 ТРАТ', 540, SY, 120)
    if tw(t, 'дешевле') > -0.1: plate(C, tw(t, 'дешевле') + 0.05, 'ДЕШЕВЛЕ НА 3 МЛН', 540, PY, 92, RED, WHITE, -3)
def s_why(C, u, t):   # Почему на три? Вот и главный ответ.
    ground(C); z = 1 + 0.22 * eo(clamp(u / 1.8))
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); vitrina(L, 540, G, w=460, u=u, psz=150)
    w, h = int(CW * z), int(CH * z); L = L.resize((w, h), Image.BILINEAR); C.alpha_composite(L.crop(((w - CW) // 2, int((h - CH) * 0.66), (w - CW) // 2 + CW, int((h - CH) * 0.66) + CH)))
    slam(C, u, 'ПОЧЕМУ НА ТРИ?', 540, SY, 116)
    if tw(t, 'главный') > -0.1: plate(C, tw(t, 'главный') + 0.05, 'ГЛАВНЫЙ ОТВЕТ', 540, PY, 100, YEL, INK, 3)
def s_formula(C, u, t):   # Расходы за месяц умножь на триста.
    YB(C, u, 7); burst(C, 540, 900, 380 + 20 * s_(u * 8), u, 16, WHITE, INK)
    put(C, text_img('РАСХОДЫ', 110, INK), 540, 840, back(u / 0.2))
    if tw(t, 'умножь') > -0.1: put(C, text_img('× 300', 170, INK), 540, 990, back(tw(t, 'умножь') / 0.22), -4)
    slam(C, u, 'ГЛАВНЫЙ ОТВЕТ', 540, SY, 110)
def s_15(C, u, t):   # Тратишь пятьдесят тысяч — нужно пятнадцать миллионов.
    ground(C); man(C, 'point', u, 250, G, 0.4)
    on = tw(t, 'пятнадцать') > -0.1
    vitrina(C, VX, G, price=num(roll(tw(t, 'пятнадцать'), 0, 15000000, 0.6)) if on else '?', psz=60, u=u)
    put(C, plate_img('50 000 × 300', 54, WHITE, INK, pad=16, r=10, border=INK, bw=6), 270, 760, back(u / 0.2), -5)
    if on and tw(t, 'пятнадцать') > 0.9: put(C, text_img('10 000 × 300 = 3 млн', 40, GREY), 540, 1330, clamp((tw(t, 'пятнадцать') - 0.9) / 0.2))
    slam(C, u, 'ТРАТИШЬ 50 000', 540, SY, 112)
    if on: plate(C, tw(t, 'пятнадцать') + 0.1, 'НУЖНО 15 000 000', 540, PY, 92, YEL, INK, -3)
def s_zapas(C, u, t):   # Это ориентир, держи запас.
    ground(C); man(C, 'nod', u, 250, G, 0.4); vitrina(C, VX, G, price='15 000 000', psz=60, star=True, u=u)
    ttl(C, u, t, 'ОРИЕНТИР,', 'ДЕРЖИ ЗАПАС', 'держи', 3)
def s_calc(C, u, t):   # Посчитай свою цифру.
    ground(C); man(C, 'explain', u, 230, G, 0.36)
    a = '' if u < 0.3 else ('4' if u < 0.4 else '40' if u < 0.5 else '40 0' if u < 0.6 else '40 000'); b = '' if u < 0.8 else '12 000 000'
    sheet(C, 650, 900, a, b, back(u / 0.2), -3)
    slam(C, u, 'ПОСЧИТАЙ', 540, SY, 130); plate(C, u - 0.15, 'СВОЮ ЦИФРУ', 540, PY, 100, YEL, INK, -3)
def s_monday(C, u, t):   # А в понедельник иди на работу. Но уже зная, сколько осталось.
    ground(C); calendar(C, 820, 790, 0.4, 'ПН', 'ПОНЕДЕЛЬНИК', back(u / 0.2), 6)
    k = clamp((u - 0.3) / 3.2); x = lerp(150, 760, k)
    man(C, 'carryR', u, x, G, 0.4); briefcase(C, x + 55, G - 215, 0.42, 0)
    if tw(t, 'зная,') > -0.1: progressbar(C, 360, 790, 400, 0.18 + 0.5 * eo(clamp(tw(t, 'зная,') / 1.2)))
    slam(C, u, 'В ПОНЕДЕЛЬНИК', 540, SY, 110)
    if tw(t, 'зная,') > -0.1: plate(C, tw(t, 'зная,') + 0.05, 'ЗНАЯ, СКОЛЬКО ОСТАЛОСЬ', 540, PY, 76, YEL, INK, 3)
    elif tw(t, 'работу.') > -0.1: plate(C, tw(t, 'работу.') + 0.05, 'ИДИ НА РАБОТУ', 540, PY, 96, WHITE, INK, 3)
def s_netupi(C, u, t):   # Всё. Не тупи.
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    man(C, 'pointcam', u, 540, G, 0.46)
    slam(C, u, 'ВСЁ.', 540, SY, 150)
    if tw(t, 'Не') > -0.1: plate(C, tw(t, 'Не') + 0.05, 'НЕ ТУПИ', 540, PY + 20, 150, INK, YEL, -3)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_q, 'none', 'zoomin'), SH(T('Миллиард?') - 0.05, s_billion, 'whipL', 'whoosh'), SH(T('Стоп.') - 0.05, s_stop, 'shake', 'scratch'),
 SH(T('Формула') - 0.05, s_three, 'whipR', 'whoosh'), SH(T('Первый:') - 0.05, s_q1, 'zoom', 'pop'), SH(T('Второй:') - 0.05, s_q2, 'whipL', 'pop'),
 SH(T('И') - 0.05, s_q3, 'door', 'pop'), SH(T('Ответ', 1) - 0.05, s_a1, 'zoomthru', 'bass', (540, 900)), SH(T('Кто') - 0.05, s_a1b, 'whipR', 'whoosh'),
 SH(T('Ответ', 2) - 0.05, s_a2, 'whipL', 'bass'), SH(T('Бери') - 0.05, s_a2b, 'zoom', 'whoosh'), SH(T('Ответ', 3) - 0.05, s_a3, 'door', 'bass'),
 SH(T('Минус') - 0.05, s_a3b, 'whipR', 'whoosh'), SH(T('Почему') - 0.05, s_why, 'cut', 'riser'), SH(T('Расходы') - 0.05, s_formula, 'zoomthru', 'boom', (540, 800)),
 SH(T('Тратишь') - 0.05, s_15, 'whipL', 'whoosh'), SH(T('Это') - 0.05, s_zapas, 'whipR', 'whoosh'), SH(T('Посчитай') - 0.05, s_calc, 'zoom', 'whoosh'),
 SH(T('А') - 0.05, s_monday, 'bodywipe', 'bass'), SH(T('Всё.') - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('работать?') + 0.1, 'pop'), (T('Ответ') + 0.05, 'pop'), (T('Миллиард?'), 'error'), (T('Лотерея?'), 'error'),
       (T('сначала'), 'tick2'), (T('три'), 'stamp'), (T('зависит'), 'error'), (T('работаешь?'), 'pop'), (T('чёрной'), 'whoosh'),
       (T('расходов.'), 'ok'), (T('тратит,'), 'kassa'), (T('пятьдесят', 0), 'ok'), (T('деньги.'), 'boom'), (T('четырёх'), 'pop'),
       (T('десятилетиями.'), 'ok'), (T('свободу.'), 'shine'), (T('Минус'), 'thud'), (T('дешевле'), 'stamp'), (T('миллиона.'), 'ok'),
       (T('главный') - 0.2, 'riser'), (T('умножь'), 'ding'), (T('пятнадцать'), 'kassa'), (T('держи'), 'pop'), (T('Посчитай') + 0.2, 'click'),
       (T('Посчитай') + 0.5, 'click'), (T('цифру.'), 'ding'), (T('зная,'), 'shine')]
# вопросы: (номер, начало, конец активности); ответы: когда кружок закрашивается
Q_ON = T('сначала'); Q_OFF = T('Расходы') - 0.1
Q_ACT = [(1, T('Первый:'), T('Второй:')), (2, T('Второй:'), T('И')), (3, T('И'), T('Ответ', 1)),
         (1, T('Ответ', 1), T('Ответ', 2)), (2, T('Ответ', 2), T('Ответ', 3)), (3, T('Ответ', 3), T('Почему'))]
Q_DONE = {1: T('пятьдесят', 0) + 0.6, 2: T('десятилетиями.') + 0.6, 3: T('миллиона.') + 0.4}
def qcounter(F, t):
    if not (Q_ON <= t < Q_OFF): return
    act = next((n for n, a, b in Q_ACT if a <= t < b), None); done = {n for n, tt in Q_DONE.items() if t >= tt}
    if act in done: act = None
    circles(F, t, act, done)
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
def disclaimer(F, t):
    if t >= 5.3: return
    a = 1 - clamp((t - 5.0) / 0.3); im = plate_img('Не является индивидуальной инвестиционной рекомендацией', 26, WHITE, GREY, pad=12, r=8, border=LG, bw=3)
    put(F, im, 540, 1340, 1, 0, a)
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
    qcounter(F, t)
    disclaimer(F, t)
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
