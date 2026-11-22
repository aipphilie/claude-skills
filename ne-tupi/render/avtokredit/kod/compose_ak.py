"""СДВГ-монтаж «Автокредит». Движок «Дивана»/«Чаевых».
python3 compose_ak.py 1.5 12.3 -> prev_*.png;  python3 compose_ak.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_ak import *
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

# ================= СЦЕНЫ «Автокредит» =================  fn(C, u, t)
SY, PY = 410, 570
def ttl(C, u, t, a, b=None, wb=None, rot=3, bcol=YEL, fcol=INK, sza=120, szb=96):
    slam(C, u, a, 540, SY, sza)
    if b:
        tb = tw(t, wb) if wb else u - 0.15
        if tb > -0.1: plate(C, tb + (0.1 if wb else 0), b, 540, PY, szb, bcol, fcol, rot)
def s_hook(C, u, t):    # Машина за три миллиона
    ground(C); k = eo(clamp(u / 0.5)); car(C, lerp(1300, 640, k), G, 0.95, bump=6 * abs(s_(u * 30)) * (1 - k))
    man(C, 'pointup', u, 190, G, 0.36)
    ptag(C, 640, 820, 'ЦЕНА', '3 000 000 ₽', -6, YEL, back((u - 0.3) / 0.22))
    slam(C, u, 'МАШИНА ЗА 3 МЛН', 540, SY, 116)
def s_credit(C, u, t):   # в кредит
    ground(C); car(C, 640, G, 0.95); man(C, 'idle_smile', u, 190, G, 0.36)
    ptag(C, 640, 820, 'ЦЕНА', '3 000 000 ₽', -6)
    slam(C, u, 'МАШИНА ЗА 3 МЛН', 540, SY, 116); stamp(C, u - 0.05, 'В КРЕДИТ', 540, PY + 10, 96, RED, -8)
def s_pay53(C, u, t):    # а отдашь пять триста
    ground(C); car(C, 640, G, 0.95); man(C, 'shock', u, 190, G, 0.36)
    on = tw(t, 'пять') > -0.05; v = roll(tw(t, 'пять'), 3000000, 5300000, 0.7) if on else 3000000
    ptag(C, 640, 820, 'ОТДАШЬ', num(v) + ' ₽', -6 + 3 * s_(u * 30) * (1 - clamp(u / 0.6)), RED if on else YEL, 1, WHITE if on else INK)
    slam(C, u, 'А ОТДАШЬ', 540, SY, 120)
    if on: plate(C, tw(t, 'пять') + 0.1, '5 300 000 ₽', 540, PY, 100, RED, WHITE, -3)
def s_how(C, u, t):    # Как отдать банку на миллион меньше?
    ground(C); bank(C, 700, G, 0.75); rich(C, 'boss', u, 700, 0.3)
    man(C, 'think', u, 210, G, 0.36); qmark(C, 300, 760, 120, u)
    slam(C, u, 'КАК ОТДАТЬ БАНКУ', 540, SY, 110)
    if tw(t, 'миллион') > -0.1: plate(C, tw(t, 'миллион') + 0.05, 'НА МИЛЛИОН МЕНЬШЕ?', 540, PY, 90, YEL, INK, 3)
def s_end(C, u, t):    # Ответ в конце.
    YB(C, u, 2); man(C, 'pointcam', u, 540, G, 0.44)
    slam(C, u, 'ОТВЕТ', 540, SY, 150); plate(C, tw(t, 'конце.') + 0.05, 'В КОНЦЕ', 540, PY + 10, 120, INK, YEL, -3)
def s_count(C, u, t):    # Считаем.
    ground(C); man(C, 'scratch', u, 200, G, 0.36); calc(C, 650, 880, [('СУММА', ''), ('СРОК', ''), ('СТАВКА', '')], None, u, 2, 560)
    slam(C, u, 'СЧИТАЕМ', 540, SY, 140)
def s_terms(C, u, t):   # Пять лет под двадцать пять процентов
    ground(C); man(C, 'explain', u, 200, G, 0.36)
    rows = [('СУММА', '3 000 000 ₽'), ('СРОК', '5 ЛЕТ' if tw(t, 'лет') > -0.05 else ''), ('СТАВКА', '25 %' if tw(t, 'процентов') > -0.15 else '')]
    calc(C, 650, 880, rows, None, 1, 2, 560)
    slam(C, u, '5 ЛЕТ · 25 %', 540, SY, 130)
def s_88(C, u, t):    # платёж восемьдесят восемь тысяч.
    YB(C, u, 3); burst(C, 540, 880, 360 + 16 * s_(u * 8), u, 16, WHITE, INK)
    v = roll(tw(t, 'восемьдесят') + 0.1, 0, 88000, 0.7)
    put(C, text_img(num(v) + ' ₽', 118, INK), 540, 855, back(u / 0.2), -3); put(C, text_img('В МЕСЯЦ', 70, INK), 540, 990, clamp(u / 0.3))
    slam(C, u, 'ПЛАТЁЖ', 540, SY, 140)
def s_bank62(C, u, t):    # И в первый год шестьдесят две из них — проценты банку.
    ground(C); k = clamp(tw(t, 'шестьдесят') / 0.6) if tw(t, 'шестьдесят') > 0 else 0
    stackbar(C, 300, G - 40, 560, [(0.71, RED, '62 500' if k > 0.6 else '', 0)], 210, k)
    tag(C, tw(t, 'шестьдесят') + 0.3, 'БАНКУ', 300, G - 660, 44, RED, WHITE, -4)
    rich(C, 'laugh' if tw(t, 'проценты') > 0 else 'boss', u, 780, 0.38)
    if tw(t, 'проценты') > 0: coinflow(C, tw(t, 'проценты'), 400, 900, 720, 900, 4, 34, 180)
    slam(C, u, 'ПЕРВЫЙ ГОД', 540, SY, 120)
    if tw(t, 'проценты') > -0.1: plate(C, tw(t, 'проценты') + 0.05, '62 500 — ПРОЦЕНТЫ', 540, PY, 86, RED, WHITE, -3)
def s_car25(C, u, t):   # На саму машину — двадцать пять.
    ground(C); k = clamp(tw(t, 'двадцать', 1) / 0.5) if tw(t, 'двадцать', 1) > 0 else 0
    stackbar(C, 300, G - 40, 560, [(0.71, RED, '62 500', 0), (0.29, GRN, '25 500' if k > 0.6 else '', 0)], 210, 1)
    tag(C, 0.3, 'БАНКУ', 690, 1000, 40, RED, WHITE, -4); tag(C, tw(t, 'двадцать', 1) + 0.2, 'МАШИНЕ', 690, 790, 40, GRN, WHITE, 4)
    car(C, 760, G, 0.45); man(C, 'sad', u, 900, G, 0.3, flip=True)
    slam(C, u, 'НА МАШИНУ —', 540, SY, 120)
    if tw(t, 'двадцать', 1) > -0.1: plate(C, tw(t, 'двадцать', 1) + 0.05, 'ВСЕГО 25 500', 540, PY, 96, GRN, WHITE, 3)
def s_year(C, u, t):    # А годовалый «китаец»
    ground(C); car(C, 600, G, 0.9); calendar(C, 230, 760, 0.42, '1', 'ГОД', back(u / 0.2), -6)
    slam(C, u, 'ГОДОВАЛЫЙ «КИТАЕЦ»', 540, SY, 104)
def s_third(C, u, t):    # может потерять до трети цены.
    ground(C); car(C, 600, G, 0.9)
    v = roll(tw(t, 'трети') + 0.1, 3000000, 2000000, 0.8) if tw(t, 'трети') > -0.1 else 3000000
    ptag(C, 600, 820, 'СТОИТ', num(v) + ' ₽', 6 - 10 * clamp((u - 0.4) / 1.0), YEL)
    if tw(t, 'трети') > 0:
        y = 760 + 20 * s_(u * 8); d = D(C); d.line([930, y - 90, 930, y + 40], fill=RED, width=26); d.polygon([(880, y + 30), (980, y + 30), (930, y + 100)], fill=RED)
    slam(C, u, 'ТЕРЯЕТ ДО ТРЕТИ', 540, SY, 120)
    if tw(t, 'цены.') > -0.1: plate(C, tw(t, 'цены.') + 0.05, 'ЦЕНЫ', 540, PY, 100, RED, WHITE, -3)
    src(C, 'Оценки экспертов рынка, 2025. Зависит от модели', 1340)
def s_sell(C, u, t):    # Продашь за два миллиона
    ground(C); car(C, 640, G, 0.9); man(C, 'give', u, 200, G, 0.36)
    keys(C, 330, 870, 0.5, 20 * s_(u * 6))
    placard(C, 640, 820, 360, 'ПРОДАМ\n2 000 000', 4, 0, u) if 'placard' in globals() else None
    slam(C, u, 'ПРОДАШЬ ЗА 2 МЛН', 540, SY, 112)
def s_owe(C, u, t):    # и ещё больше шестисот тысяч должен.
    ground(C); man(C, 'shock', u, 300, G, 0.4)
    debtplate(C, 720, 840, '656 000 ₽', back(u / 0.2) if u < 0.3 else 1, 4 + 2 * s_(u * 20) * (1 - clamp(u / 0.5)))
    slam(C, u, 'И ЕЩЁ ДОЛЖЕН', 540, SY, 120)
    if tw(t, 'должен.') > -0.1: stamp(C, tw(t, 'должен.'), 'МАШИНЫ НЕТ', 540, PY + 10, 84, RED, -8)
def s_ghost(C, u, t):    # Платишь за машину, которой уже нет.
    ground(C); a = 1 - clamp((u - 0.4) / 1.0)
    car(C, 640, G, 0.9, alpha=a); car(C, 640, G, 0.9, ghost=True, alpha=1 - a)
    man(C, 'pay', u, 200, G, 0.36)
    for j in range(4):
        q = (u * 0.9 + j / 4) % 1; bill(C, lerp(320, 900, q), 900 - 160 * s_(math.pi * q), 110, q * 300, alpha=1 - q * 0.7)
    slam(C, u, 'МАШИНЫ НЕТ —', 540, SY, 116)
    if tw(t, 'которой') > -0.1: plate(C, tw(t, 'которой') + 0.05, 'А ПЛАТЁЖ ЕСТЬ', 540, PY, 96, RED, WHITE, 3)
def s_three(C, u, t):    # Так что три вопроса.
    C.paste(INK, [0, 0, CW, CH]); speedlines(C, 540, 880, u, r0=430, col=(34, 34, 34), seed=5)
    for j in range(3):
        k = back((u - 0.15 - j * 0.12) / 0.2); r = 110 * k; cx = 540 + (j - 1) * 270; d = D(C)
        if k > 0: d.ellipse([cx - r, 880 - r, cx + r, 880 + r], fill=YEL, outline=WHITE, width=8); put(C, text_img(str(j + 1), 130, INK), cx, 884, k)
    slam(C, u, 'ТРИ ВОПРОСА', 540, SY, 130, WHITE)
def s_q1(C, u, t):    # Первый: что тебе подсунули в договор?
    ground(C); man(C, 'read', u, 220, G, 0.38)
    doc(C, 690, 950, 440, ['', '', '', '', ''], k=back(u / 0.2) if u < 0.3 else 1, rot=-4); magnifier(C, 760 + 40 * s_(u * 3), 960 + 30 * s_(u * 4), 0.7, 0)
    ttl(C, u, t, 'ВОПРОС 1', 'ЧТО ПОДСУНУЛИ В ДОГОВОР?', 'подсунули', -3, szb=80)
def s_q2(C, u, t):    # Второй: как гасить досрочно?
    ground(C); man(C, 'carryR', u, lerp(150, 430, clamp(u / 2)), G, 0.38); bill(C, lerp(150, 430, clamp(u / 2)) + 60, G - 230, 120, 10)
    bank(C, 800, G, 0.55)
    ttl(C, u, t, 'ВОПРОС 2', 'КАК ГАСИТЬ ДОСРОЧНО?', 'досрочно?', 3, szb=86)
def s_q3(C, u, t):    # И третий: можно ли сбежать от банка?
    ground(C); bank(C, 820, G, 0.55); x = lerp(560, 120, clamp(u / 1.8))
    man(C, 'run', u * 1.6, x, G, 0.36, flip=True); rich(C, 'shock', u, 640, 0.28)
    ttl(C, u, t, 'ВОПРОС 3', 'СБЕЖАТЬ ОТ БАНКА?', 'сбежать', -3, szb=90)
def s_a1(C, u, t):    # Ответ первый. Страховки и «карты помощи».
    ground(C); man(C, 'read_shock', u, 210, G, 0.38)
    hl = []; rows = ['', 'СТРАХОВКА ЖИЗНИ', '', 'КАРТА ПОМОЩИ', '']
    if tw(t, 'Страховки') > 0: hl.append(1)
    if tw(t, 'карты') > 0: hl.append(3)
    doc(C, 690, 960, 440, rows, tuple(hl), k=1, rot=-3)
    ttl(C, u, t, 'ОТВЕТ 1', 'ДОПЫ В ДОГОВОРЕ', 'Страховки', 3, RED, WHITE)
def s_refuse(C, u, t):    # От добровольной страховки можно отказаться
    ground(C); man(C, 'net', u, 210, G, 0.38)
    doc(C, 690, 960, 440, ['', 'СТРАХОВКА ЖИЗНИ', '', 'КАРТА ПОМОЩИ', ''], (1,), k=1, rot=-3, strike_=(1,), sk=clamp(tw(t, 'отказаться') / 0.4) if tw(t, 'отказаться') > 0 else 0)
    slam(C, u, 'ДОБРОВОЛЬНАЯ?', 540, SY, 120)
    if tw(t, 'отказаться') > -0.1: plate(C, tw(t, 'отказаться') + 0.05, 'МОЖНО ОТКАЗАТЬСЯ', 540, PY, 92, YEL, INK, -3)
def s_14(C, u, t):    # за четырнадцать дней и вернуть деньги.
    ground(C); calendar(C, 300, 860, 0.5, '14', 'ДНЕЙ', back(u / 0.2), -6)
    man(C, 'cheer' if tw(t, 'вернуть') > 0 else 'idle_smile', u, 780, G, 0.38)
    if tw(t, 'вернуть') > 0: coinflow(C, tw(t, 'вернуть'), 330, 1100, 760, 900, 4, 32, 200)
    slam(C, u, 'ЗА 14 ДНЕЙ', 540, SY, 130)
    if tw(t, 'вернуть') > -0.1: plate(C, tw(t, 'вернуть') + 0.05, 'ВЕРНИ ДЕНЬГИ', 540, PY, 100, GRN, WHITE, 3)
    src(C, 'Период охлаждения: Указание Банка России № 3854-У', 1340)
def s_check(C, u, t):    # Но проверь договор: банк может поднять ставку.
    ground(C); doc(C, 330, 960, 400, ['', 'СТАВКА БЕЗ СТРАХОВКИ', '', '', ''], (1,) if tw(t, 'банк', 0) > 0 else (), k=1, rot=-4)
    magnifier(C, 400, 940, 0.6)
    on = tw(t, 'поднять') > -0.05
    ratesign(C, 780, 860, '25 %' if not on else '28 %?', RED, back(u / 0.2), 4, 1 if on else 0) if True else None
    slam(C, u, 'ПРОВЕРЬ ДОГОВОР', 540, SY, 116)
    if on: plate(C, tw(t, 'поднять') + 0.05, 'СТАВКУ МОГУТ ПОДНЯТЬ', 540, PY, 80, RED, WHITE, -3)
def s_a2(C, u, t):    # Ответ второй.
    YB(C, u, 6); form(C, 540, 960, (False, False), back(u / 0.2) if u < 0.3 else 1, rot=-3)
    slam(C, u, 'ОТВЕТ 2', 540, SY, 150)
def s_over(C, u, t):    # Плати сверху и в заявлении выбирай
    ground(C); man(C, 'explain', u, 190, G, 0.34)
    form(C, 640, 970, (False, False), 1, rot=-3)
    slam(C, u, 'ПЛАТИ СВЕРХУ', 540, SY, 124)
    if tw(t, 'заявлении') > -0.1: plate(C, tw(t, 'заявлении') + 0.05, 'В ЗАЯВЛЕНИИ', 540, PY, 96, YEL, INK, 3)
def s_srok(C, u, t):    # «уменьшить срок», а не платёж.
    ground(C); man(C, 'nod', u, 190, G, 0.34)
    q = tw(t, 'срок»,'); form(C, 640, 970, (q > 0, False), 1, (clamp(q / 0.3), 0), rot=-3)
    if tw(t, 'платёж', 1) > 0: xcross(C, tw(t, 'платёж', 1), 640, 1105, 260, RED, 12)
    slam(C, u, 'УМЕНЬШИТЬ СРОК', 540, SY, 116)
    if tw(t, 'не', 0) > -0.1: plate(C, tw(t, 'не', 0) + 0.05, 'А НЕ ПЛАТЁЖ', 540, PY, 100, RED, WHITE, -3)
def s_plus10(C, u, t):    # Плюс десять тысяч в месяц
    ground(C); bank(C, 820, G, 0.5); x = lerp(150, 520, clamp(u / 1.4))
    man(C, 'carryR', u, x, G, 0.38); bill(C, x + 60, G - 230, 130, 8); bill(C, x + 70, G - 250, 130, -6)
    slam(C, u, '+10 000', 540, SY, 150); plate(C, tw(t, 'месяц') + 0.05, 'КАЖДЫЙ МЕСЯЦ', 540, PY, 96, YEL, INK, 3)
def s_year_early(C, u, t):   # и кредит закроешь почти на год раньше.
    ground(C); d = D(C)
    v = int(round(roll(tw(t, 'закроешь'), 60, 50, 0.9))) if tw(t, 'закроешь') > 0 else 60
    calendar(C, 300, 860, 0.5, str(v), 'МЕСЯЦЕВ', 1, -5)
    man(C, 'cheer' if tw(t, 'раньше.') > 0 else 'idle_smile', u, 790, G, 0.38)
    slam(C, u, 'ЗАКРОЕШЬ', 540, SY, 130)
    if tw(t, 'год', 1) > -0.1: plate(C, tw(t, 'год', 1) + 0.05, 'ПОЧТИ НА ГОД РАНЬШЕ', 540, PY, 86, GRN, WHITE, -3)
def s_a3(C, u, t):    # Ответ третий.
    YB(C, u, 8); bank(C, 540, G - 40, 0.7)
    slam(C, u, 'ОТВЕТ 3', 540, SY, 150)
def s_rates(C, u, t):    # Ставки упали — рефинансируйся.
    ground(C); on = tw(t, 'упали') > 0
    ratesign(C, 520, 820, '18 %' if on else '25 %', GRN if on else RED, 1, -3 if on else 3, -1 if on else 0)
    man(C, 'cheer' if tw(t, 'рефинансируйся.') > 0 else 'idle', u, 920, G, 0.32)
    slam(C, u, 'СТАВКИ УПАЛИ?', 540, SY, 120)
    if tw(t, 'рефинансируйся.') > -0.1: plate(C, tw(t, 'рефинансируйся.') + 0.05, 'РЕФИНАНСИРУЙСЯ', 540, PY, 96, YEL, INK, 3)
def s_bank2(C, u, t):    # Другой банк выкупит остаток дешевле.
    ground(C); bank(C, 250, G, 0.42, label='БАНК 1'); bank(C, 830, G, 0.42, label='БАНК 2')
    rich(C, 'shock' if tw(t, 'выкупит') > 0 else 'boss', u, 250, 0.22)
    q = clamp(tw(t, 'выкупит') / 1.2) if tw(t, 'выкупит') > 0 else 0
    debtplate(C, lerp(250, 830, eo(q)), 760 - 140 * s_(math.pi * q), 'ОСТАТОК', 1, 4, top='18 %' if q > 0.5 else '25 %')
    slam(C, u, 'ДРУГОЙ БАНК', 540, SY, 124)
    if tw(t, 'дешевле.') > -0.1: plate(C, tw(t, 'дешевле.') + 0.05, 'ВЫКУПИТ ДЕШЕВЛЕ', 540, PY, 92, GRN, WHITE, -3)
def s_main(C, u, t):    # А теперь главный ответ.
    ground(C); z = 1 + 0.1 * eo(clamp(u / 1.5)); man(C, 'pointcam', u, 540, G, 0.4 * z)
    slam(C, u, 'А ТЕПЕРЬ', 540, SY, 130)
    if tw(t, 'главный') > -0.1: plate(C, tw(t, 'главный') + 0.05, 'ГЛАВНЫЙ ОТВЕТ', 540, PY, 110, YEL, INK, 3)
def s_combo(C, u, t):    # Плюс десять тысяч и рефинанс под восемнадцать
    YB(C, u, 9); burst(C, 540, 880, 380 + 16 * s_(u * 8), u, 16, WHITE, INK)
    put(C, text_img('+10 000', 120, INK), 540, 800, back(u / 0.2), -3)
    if tw(t, 'рефинанс') > -0.1: put(C, text_img('+ РЕФИНАНС', 84, INK), 540, 920, back(tw(t, 'рефинанс') / 0.2), 2)
    if tw(t, 'восемнадцать') > -0.1: put(C, plate_img('18 %', 80, GRN, WHITE, pad=14, r=10, border=INK, bw=6), 540, 1040, back(tw(t, 'восемнадцать') / 0.2), -4)
    slam(C, u, 'ГЛАВНЫЙ ОТВЕТ', 540, SY, 116)
def s_million(C, u, t):    # и переплата меньше почти на миллион.
    ground(C); k = clamp(u / 0.6)
    bar(C, 330, G - 50, 430 * k, 'БЫЛО', RED, 190, '2 280 000' if k >= 1 else None)
    k2 = clamp((tw(t, 'меньше', 1) - 0.0) / 0.6) if tw(t, 'меньше', 1) > 0 else 0
    if k2 > 0: bar(C, 750, G - 50, 430 * 0.61 * k2, 'СТАЛО', GRN, 190, '1 390 000' if k2 >= 1 else None)
    if tw(t, 'миллион.') > 0: stamp(C, tw(t, 'миллион.'), '−890 000 ₽', 760, 760, 70, GRN, -8)
    slam(C, u, 'ПЕРЕПЛАТА', 540, SY, 130)
    if tw(t, 'почти', 1) > -0.1: plate(C, tw(t, 'почти', 1) + 0.05, 'МЕНЬШЕ ПОЧТИ НА МИЛЛИОН', 540, PY, 80, GRN, WHITE, -3)
    src(C, 'Пример: 3 млн, 5 лет, 25 %; +10 000/мес, через год рефинанс под 18 %', 1340)
def s_share(C, u, t):    # Перешли тому, кто собрался за машиной.
    ground(C); man(C, 'phone', u, 230, G, 0.38); car(C, 760, G, 0.55)
    sms(C, 690, 760, 520, 'ПРОЧТИ ДО ДИЛЕРА!', clamp(u / 0.3) if u < 0.4 else 1, INK)
    slam(C, u, 'ПЕРЕШЛИ ТОМУ,', 540, SY, 116)
    if tw(t, 'собрался') > -0.1: plate(C, tw(t, 'собрался') + 0.05, 'КТО ЗА МАШИНОЙ', 540, PY, 96, YEL, INK, -3)
def s_netupi(C, u, t):   # Всё. Не тупи.
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    man(C, 'pointcam', u, 540, G, 0.46)
    slam(C, u, 'ВСЁ.', 540, SY, 150)
    if tw(t, 'Не') > -0.1: plate(C, tw(t, 'Не') + 0.05, 'НЕ ТУПИ', 540, PY + 20, 150, INK, YEL, -3)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'zoomin'), SH(T('в') - 0.05, s_credit, 'cut', 'stamp'), SH(T('а') - 0.05, s_pay53, 'shake', 'kassa'),
 SH(T('Как') - 0.05, s_how, 'whipL', 'whoosh'), SH(T('Ответ') - 0.05, s_end, 'zoomthru', 'bass', (300, 760)),
 SH(T('Считаем.') - 0.05, s_count, 'door', 'whoosh'), SH(T('Пять') - 0.05, s_terms, 'zoom', 'pop'), SH(T('платёж') - 0.05, s_88, 'zoomthru', 'boom', (650, 880)),
 SH(T('И') - 0.05, s_bank62, 'whipR', 'whoosh'), SH(T('На') - 0.05, s_car25, 'whipL', 'swipe'),
 SH(T('А') - 0.05, s_year, 'bodywipe', 'bass'), SH(T('может') - 0.05, s_third, 'zoom', 'whoosh'), SH(T('Продашь') - 0.05, s_sell, 'whipR', 'whoosh'),
 SH(T('и', 0) - 0.05, s_owe, 'shake', 'boom'), SH(T('Платишь') - 0.05, s_ghost, 'whipL', 'whoosh'),
 SH(T('Так') - 0.05, s_three, 'drop', 'bass'), SH(T('Первый:') - 0.05, s_q1, 'zoom', 'pop'), SH(T('Второй:') - 0.05, s_q2, 'whipL', 'pop'),
 SH(T('И', 1) - 0.05, s_q3, 'door', 'pop'), SH(T('Ответ', 1) - 0.05, s_a1, 'zoomthru', 'bass', (540, 880)), SH(T('От') - 0.05, s_refuse, 'whipR', 'whoosh'),
 SH(T('за', 3) - 0.05, s_14, 'zoom', 'whoosh'), SH(T('Но') - 0.05, s_check, 'shake', 'alarm'),
 SH(T('Ответ', 2) - 0.05, s_a2, 'zoomthru', 'bass', (780, 860)), SH(T('Плати') - 0.05, s_over, 'whipL', 'whoosh'), SH(T('уменьшить') - 0.05, s_srok, 'zoom', 'click'),
 SH(T('Плюс') - 0.05, s_plus10, 'whipR', 'coins'), SH(T('и', 4) - 0.05, s_year_early, 'whipL', 'whoosh'),
 SH(T('Ответ', 3) - 0.05, s_a3, 'door', 'bass'), SH(T('Ставки') - 0.05, s_rates, 'zoom', 'whoosh'), SH(T('Другой') - 0.05, s_bank2, 'whipR', 'whoosh'),
 SH(T('А', 1) - 0.05, s_main, 'cut', 'riser'), SH(T('Плюс', 1) - 0.05, s_combo, 'zoomthru', 'boom', (540, 800)), SH(T('и', 6) - 0.05, s_million, 'whipL', 'whoosh'),
 SH(T('Перешли') - 0.05, s_share, 'bodywipe', 'bass'), SH(T('Всё.') - 0.05, s_netupi, 'zoomthru', 'final', (690, 760)),
]
ACC = [(T('миллиона', 0), 'pop'), (T('триста.'), 'error'), (T('меньше?'), 'pop'), (T('Пять'), 'click'), (T('процентов'), 'click'),
       (T('восемьдесят'), 'tick2'), (T('шестьдесят'), 'pop'), (T('проценты'), 'coins'), (T('двадцать', 1), 'pop'), (T('трети'), 'drop'),
       (T('должен.'), 'stamp'), (T('которой'), 'error'), (T('подсунули'), 'pop'), (T('сбежать'), 'swipe'), (T('Страховки'), 'pop'), (T('карты'), 'pop'),
       (T('отказаться'), 'scratch'), (T('вернуть'), 'coins'), (T('поднять'), 'error'), (T('срок»,'), 'ok'), (T('платёж', 1), 'error'),
       (T('раньше.'), 'ding'), (T('упали'), 'drop'), (T('рефинансируйся.'), 'ok'), (T('выкупит'), 'whoosh'), (T('дешевле.'), 'ding'),
       (T('главный') - 0.2, 'riser'), (T('рефинанс'), 'pop'), (T('восемнадцать'), 'pop'), (T('меньше', 1), 'kassa'), (T('миллион.'), 'stamp'), (T('машиной.'), 'msg')]
Q_ON = T('вопроса.'); Q_OFF = T('А', 1) - 0.1
Q_ACT = [(1, T('Первый:'), T('Второй:')), (2, T('Второй:'), T('И', 1)), (3, T('И', 1), T('Ответ', 1)),
         (1, T('Ответ', 1), T('Ответ', 2)), (2, T('Ответ', 2), T('Ответ', 3)), (3, T('Ответ', 3), T('А', 1))]
Q_DONE = {1: T('ставку.') + 0.5, 2: T('раньше.') + 0.5, 3: T('дешевле.') + 0.4}
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
