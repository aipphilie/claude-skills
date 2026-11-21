"""СДВГ-монтаж «Пряник и Claude Code». Движок «Автокредита» (compose_ak.py) без 3D-человечка.
python3 compose_pr.py 1.5 12.3 -> prev_*.png;  python3 compose_pr.py sheet [доля];  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_pr import *
YB = lambda C, u, seed=1: (C.paste(YEL, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(246, 200, 0), seed=seed))
RB = lambda C, u, seed=1: (C.paste(RED, [0, 0, CW, CH]), speedlines(C, 540, 880, u, r0=520, col=(206, 30, 40), seed=seed))
def tw(t, w, k=0): return t - T(w, k)
_slam0, _plate0 = slam, plate
def _fit(text, sz, lim=780):
    w = text_img(text, sz).width
    return sz * min(1.0, lim / w) if w else sz
def slam(C, u, text, cx, cy, sz=90, *a, **k): _slam0(C, u, text, cx, cy, _fit(text, sz), *a, **k)
def plate(C, u, text, cx, cy, sz=70, *a, **k): _plate0(C, u, text, cx, cy, _fit(text, sz, 740), *a, **k)
SY, PY = 440, 600; PX = 250; LX, LY, LW = 640, 1000, 490
def ttl(C, u, t, a, b=None, wb=None, rot=3, bcol=YEL, fcol=INK, sza=120, szb=96):
    slam(C, u, a, 540, SY, sza)
    if b:
        tb = tw(t, wb) if wb else u - 0.15
        if tb > -0.1: plate(C, tb + (0.1 if wb else 0), b, 540, PY, szb, bcol, fcol, rot)

# ================= СЦЕНЫ =================
def s_hook(C, u, t):    # Нет, ну вы это видели?!
    YB(C, u, 1); pryanik(C, t, 540, G, 190, 'up', 'shock')
    slam(C, u, 'НЕТ, НУ ВЫ', 540, SY, 130); plate(C, u - 0.25, 'ЭТО ВИДЕЛИ?!', 540, PY, 110, INK, YEL, -3)
def s_open(C, u, t):    # Пряник впервые открыл Клод Код.
    ground(C); pryanik(C, t, PX, G, 140, 'down', 'n')
    laptop(C, LX, LY, LW, [('> привет', GRY)], u / 0.3, t=t)
    slam(C, u, 'ПРЯНИК ОТКРЫЛ', 540, SY, 116)
    if tw(t, 'Код.') > -0.1: plate(C, tw(t, 'Код.') + 0.05, 'CLAUDE CODE', 540, PY, 110, INK, ORG, 3)
def s_ahue(C, u, t):    # И он в ахуе.
    RB(C, u, 2); burst(C, 540, 1000, 330 + 14 * s_(u * 9), u, 16, YEL, INK)
    pryanik(C, t, 540, G, 200, 'up', 'shock', sway=2.2)
    slam(C, u, 'И ОН', 540, SY, 130, WHITE); stamp(C, tw(t, 'ахуе.') + 0.02, 'В АХ*Е', 540, PY + 10, 120, WHITE, -8)
def s_vchera(C, u, t):    # Вчера Клод сделал ему сайт.
    ground(C); pryanik(C, t, PX, G, 140, 'hips', 'happy')
    ln = [('> сделай мне сайт', GRY)] + ([('✓ сайт готов', GRNT)] if tw(t, 'сайт.') > 0 else [])
    laptop(C, LX, LY, LW, ln, 1, t=t)
    slam(C, u, 'ВЧЕРА', 540, SY, 140)
    if tw(t, 'сайт.') > -0.1: plate(C, tw(t, 'сайт.') + 0.05, 'СДЕЛАЛ САЙТ', 540, PY, 100, GRN, WHITE, -3)
def s_segodnya(C, u, t):    # Сегодня новый чат, а он: «А ты кто?»
    ground(C); q = tw(t, 'кто?»') > -0.3
    pryanik(C, t, PX, G, 140, 'up' if q else 'down', 'shock' if q else 'n')
    ln = [('> продолжи сайт', GRY)] + ([('а ты кто? :)', ORG)] if q else [])
    laptop(C, LX, LY, LW, ln, 1, t=t)
    slam(C, u, 'СЕГОДНЯ НОВЫЙ ЧАТ', 540, SY, 110)
    if q: plate(C, tw(t, 'кто?»') + 0.3, '«А ТЫ КТО?»', 540, PY, 110, RED, WHITE, 3)
def s_zachto(C, u, t):    # Простите, а за что, блять?!
    RB(C, u, 3); pryanik(C, t, 540, G, 200, 'up', 'angry', sway=2.5)
    slam(C, u, 'ПРОСТИТЕ,', 540, SY, 130, WHITE)
    if tw(t, 'за', 0) > -0.1: plate(C, tw(t, 'за', 0) + 0.05, 'А ЗА ЧТО, БЛ*ТЬ?!', 540, PY, 100, INK, YEL, -3)
def s_podvoh(C, u, t):    # А вот и подвох: каждый новый чат — с чистого листа.
    ground(C)
    chatwin(C, 300, 960, 360, 520, 12, 'ВЧЕРА', -5, seed=2)
    if tw(t, 'каждый') > -0.1: chatwin(C, 760, 960, 360, 520, 0, 'НОВЫЙ ЧАТ', 5, empty_text='ПУСТО')
    slam(C, u, 'А ВОТ И ПОДВОХ', 540, SY, 116)
    if tw(t, 'чистого') > -0.1: plate(C, tw(t, 'чистого') + 0.05, 'С ЧИСТОГО ЛИСТА', 540, PY, 100, RED, WHITE, 3)
def s_stop(C, u, t):    # Стоп. Тут ты тупишь, пряник.
    YB(C, u, 4); pryanik(C, t, 540, G, 190, 'down', 'shock')
    slam(C, u, 'СТОП.', 540, SY, 160)
    if tw(t, 'Тут') > -0.1: plate(C, tw(t, 'Тут') + 0.05, 'ТУТ ТЫ ТУПИШЬ', 540, PY + 10, 120, INK, YEL, -3)
def s_step1(C, u, t):    # Шаг первый. Подключи свой репозиторий с гитхаба.
    ground(C); pryanik(C, t, 540, G, 120, 'down', 'n')
    folder(C, 260, 860, 0.9, 'РЕПОЗИТОРИЙ', -4, u / 0.3)
    k = clamp(tw(t, 'репозиторий') / 0.5) if tw(t, 'репозиторий') > 0 else 0
    arrow(C, 420, 860, 600, k)
    if k > 0.5: laptop(C, 790, 860, 300, [('GitHub ✓', GRNT)], (k - 0.5) * 2, t=t)
    ttl(C, u, t, 'ШАГ 1', 'ПОДКЛЮЧИ GITHUB', 'Подключи', -3)
def s_vidit(C, u, t):    # Теперь Клод видит весь код, а не твои пересказы.
    ground(C); pryanik(C, t, PX, G, 140, 'hips', 'happy' if tw(t, 'пересказы.') < 0 else 'n')
    files = [('/ src', GRY), ('  index.html', GRNT), ('  app.js', GRNT), ('  style.css', GRNT)]
    laptop(C, LX, LY, LW, files[:1 + int(clamp(u / 0.8) * 3)], 1, t=t)
    slam(C, u, 'ВИДИТ ВЕСЬ КОД', 540, SY, 120)
    if tw(t, 'пересказы.') > -0.1:
        plate(C, tw(t, 'пересказы.') + 0.05, 'А НЕ ТВОИ ПЕРЕСКАЗЫ', 540, PY, 90, YEL, INK, 3); strike(C, tw(t, 'пересказы.') - 0.2, 190, PY + 40, 890, PY - 30, RED, 16, 0.2)
def s_step2(C, u, t):    # Шаг второй. Набери слэш инит, и Клод создаст файл клод-эм-ди.
    ground(C); pryanik(C, t, PX, G, 140, 'down', 'n')
    ln = [('> /init', WHITE)] + ([('✓ создан CLAUDE.md', GRNT)] if tw(t, 'создаст') > 0 else [])
    laptop(C, LX, LY, LW, ln, 1, t=t)
    ttl(C, u, t, 'ШАГ 2', '/INIT', 'слэш', -3, INK, YEL, szb=130)
    if tw(t, 'клод-эм-ди.') > -0.1: tag(C, tw(t, 'клод-эм-ди.'), 'CLAUDE.MD', LX, 760, 54, YEL, INK, 4)
def s_shpora(C, u, t):    # Это шпаргалка про проект, он читает её в каждой сессии. Правила, стиль, что не трогать — туда.
    ground(C); pryanik(C, t, 230, G, 120, 'hips', 'happy')
    tk = tuple(i for i, w in enumerate(['Правила,', 'стиль,', 'трогать']) if tw(t, w) > 0)
    sheet(C, 680, 990, 420, 'CLAUDE.MD', ['ПРАВИЛА', 'СТИЛЬ', 'НЕ ТРОГАТЬ'], tk, u / 0.3, 3)
    slam(C, u, 'ШПАРГАЛКА', 540, SY, 140)
    if tw(t, 'каждой') > -0.1: plate(C, tw(t, 'каждой') + 0.05, 'ЧИТАЕТ КАЖДЫЙ РАЗ', 540, PY, 96, YEL, INK, -3)
def s_step3(C, u, t):    # Шаг третий. Одна задача — один чат,
    ground(C); pryanik(C, t, 540, G, 120, 'down', 'n')
    for j, nm in enumerate(['САЙТ', 'БОТ', 'ДИЗАЙН']):
        if u > 0.15 + j * 0.25: chatwin(C, 220 + j * 320, 860, 260, 300, 4, nm, (j - 1) * 4, seed=j)
    ttl(C, u, t, 'ШАГ 3', 'ОДНА ЗАДАЧА — ОДИН ЧАТ', 'Одна', 3, szb=84)
def s_pomoyka(C, u, t):    # а не помойка на триста сообщений.
    ground(C)
    for j in range(7): chatwin(C, 300 + (j % 3) * 230 + 20 * s_(j), 1080 - j * 50, 300, 360, 14, 'ВСЁ ПОДРЯД', (j * 37) % 24 - 12, True, j)
    pryanik(C, t, 820, G, 110, 'up', 'shock')
    slam(C, u, 'А НЕ ПОМОЙКА', 540, SY, 130)
    if tw(t, 'триста') > -0.1: plate(C, tw(t, 'триста') + 0.05, 'НА 300 СООБЩЕНИЙ', 540, PY, 100, RED, WHITE, 3)
def s_continue(C, u, t):    # Вчерашний разговор продолжит клод континью.
    ground(C); pryanik(C, t, PX, G, 140, 'down', 'n')
    ln = [('$ claude --continue', WHITE)] + ([('✓ продолжаем', GRNT)] if tw(t, 'континью.') > 0.2 else [])
    laptop(C, LX, LY, LW, ln, 1, t=t)
    slam(C, u, 'ВЧЕРАШНИЙ РАЗГОВОР', 540, SY, 110)
    if tw(t, 'клод', 0) > -0.1: plate(C, tw(t, 'клод', 0) + 0.05, 'CLAUDE --CONTINUE', 540, PY, 96, INK, YEL, -3)
def s_komp(C, u, t):    # А проект на своём компе?
    ground(C); house(C, 640, G, 440); laptop(C, 640, 1060, 260, [], 1, False, t)
    pryanik(C, t, 230, G, 120, 'down', 'n'); qmark(C, 230, 780, 130, u)
    slam(C, u, 'ПРОЕКТ НА СВОЁМ КОМПЕ?', 540, SY, 100)
def s_rc(C, u, t):    # Запусти клод ремоут-контрол и рули с телефона.
    ground(C)
    ln = [('$ claude', WHITE), ('  remote-control', WHITE)]
    laptop(C, 640, 900, 470, ln, 1, t=t)
    if tw(t, 'ремоут-контрол') > 0.3: qr(C, 640, 1040, 130, tw(t, 'ремоут-контрол') - 0.3)
    pryanik(C, t, 220, G, 120, 'phone', 'happy' if tw(t, 'рули') > 0 else 'n')
    if tw(t, 'рули') > -0.1: bigphone(C, 385, 1000, 0.42, 8)
    slam(C, u, 'ЗАПУСТИ', 540, SY, 130)
    plate(C, u - 0.2, 'REMOTE-CONTROL', 540, PY, 104, INK, YEL, 3)
def s_tolchok(C, u, t):    # Хоть с толчка.
    YB(C, u, 5); toilet(C, 560, G + 30, 1.4)
    pryanik(C, t, 520, G - 150, 140, 'phone', 'happy', sway=0.6); bigphone(C, 705, 830, 0.42, 8)
    slam(C, u, 'ХОТЬ С ТОЛЧКА', 540, SY, 130)
    tag(C, u - 0.3, 'КОД НА КОМПЕ ДОМА', 540, PY, 52, INK, YEL, -3)
def s_mozhno(C, u, t):    # А так вообще можно было? Можно.
    YB(C, u, 6); pryanik(C, t, 540, G, 190, 'up', 'shock' if tw(t, 'Можно.') < 0 else 'happy', sway=1.8)
    slam(C, u, 'А ТАК МОЖНО БЫЛО?', 540, SY, 110)
    if tw(t, 'Можно.') > -0.05: stamp(C, tw(t, 'Можно.'), 'МОЖНО', 540, PY + 20, 120, GRN, -8)
def s_itogo(C, u, t):    # Итого: репозиторий, клод-эм-ди и порядок в чатах.
    ground(C); pryanik(C, t, 220, G, 120, 'hips', 'happy')
    tk = tuple(i for i, (w, k) in enumerate([('репозиторий,', 0), ('клод-эм-ди', 1), ('порядок', 0)]) if tw(t, w, k) > 0)
    sheet(C, 680, 1000, 420, 'ИТОГО', ['GITHUB', 'CLAUDE.MD', 'ЧАТЫ'], tk, u / 0.3, -3)
    slam(C, u, 'ИТОГО', 540, SY, 150)
def s_pomnit(C, u, t):    # И Клод помнит больше тебя, пряник ты хуев.
    ground(C); pryanik(C, t, 540, G, 170, 'down', 'shock' if tw(t, 'хуев.') > -0.4 else 'n')
    slam(C, u, 'CLAUDE ПОМНИТ', 540, SY, 120); plate(C, tw(t, 'больше') + 0.05, 'БОЛЬШЕ ТЕБЯ', 540, PY, 104, YEL, INK, 3)
    if tw(t, 'хуев.') > -0.05: stamp(C, tw(t, 'хуев.'), 'ПРЯНИК Х*ЕВ', 540, 760, 86, RED, -10)
def s_netupi(C, u, t):   # Всё. Не тупи. И не крошись.
    YB(C, u, 7); kr = tw(t, 'крошись.')
    pryanik(C, t, 540, G, 190, 'hips', 'happy'); crumbs(C, kr, 600, 1000)
    slam(C, u, 'ВСЁ.', 540, SY, 150)
    if tw(t, 'Не', 0) > -0.1: plate(C, tw(t, 'Не', 0) + 0.05, 'НЕ ТУПИ', 540, PY + 20, 150, INK, YEL, -3)
    if kr > -0.1: tag(C, kr + 0.05, 'И НЕ КРОШИСЬ', 540, 770, 60, WHITE, INK, 4)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'zoomin'), SH(T('Пряник', 0) - 0.05, s_open, 'whipL', 'whoosh'), SH(T('И', 0) - 0.05, s_ahue, 'shake', 'boom'),
 SH(T('Вчера') - 0.05, s_vchera, 'zoomthru', 'bass', (540, 900)), SH(T('Сегодня') - 0.05, s_segodnya, 'whipR', 'whoosh'),
 SH(T('Простите,') - 0.05, s_zachto, 'shake', 'scratch'), SH(T('вот') - 0.3, s_podvoh, 'door', 'bass'),
 SH(T('Стоп.') - 0.05, s_stop, 'cut', 'stamp'), SH(T('Шаг', 0) - 0.05, s_step1, 'drop', 'bass'), SH(T('Теперь') - 0.05, s_vidit, 'whipL', 'whoosh'),
 SH(T('Шаг', 1) - 0.05, s_step2, 'zoomthru', 'bass', (650, 980)), SH(T('Это', 0) - 0.05, s_shpora, 'whipR', 'whoosh'),
 SH(T('Шаг', 2) - 0.05, s_step3, 'door', 'bass'), SH(T('а', 3) - 0.05, s_pomoyka, 'shake', 'error'), SH(T('Вчерашний') - 0.05, s_continue, 'whipL', 'whoosh'),
 SH(T('А', 2) - 0.05, s_komp, 'zoom', 'pop'), SH(T('Запусти') - 0.05, s_rc, 'whipR', 'whoosh'), SH(T('Хоть') - 0.05, s_tolchok, 'drop', 'boing'),
 SH(T('А', 3) - 0.05, s_mozhno, 'zoomthru', 'bass', (540, 900)), SH(T('Итого:') - 0.05, s_itogo, 'door', 'bass'),
 SH(T('И', 1) - 0.05, s_pomnit, 'whipL', 'whoosh'), SH(T('Всё.') - 0.05, s_netupi, 'zoomthru', 'final', (540, 900)),
]
ACC = [(T('ахуе.'), 'stamp'), (T('сайт.'), 'ok'), (T('кто?»'), 'error'), (T('подвох:'), 'pop'), (T('чистого'), 'drop'), (T('Тут'), 'pop'),
       (T('репозиторий'), 'swipe'), (T('пересказы.'), 'scratch'), (T('слэш'), 'click'), (T('создаст'), 'ding'), (T('Правила,'), 'pop'), (T('стиль,'), 'pop'), (T('трогать'), 'pop'),
       (T('триста'), 'alarm'), (T('континью.'), 'ok'), (T('ремоут-контрол'), 'click'), (T('рули'), 'notif'), (T('Можно.'), 'stamp'),
       (T('репозиторий,'), 'ok'), (T('клод-эм-ди', 1), 'ok'), (T('порядок'), 'ok'), (T('хуев.'), 'stamp'), (T('крошись.'), 'crunch')]
Q_ON = T('Шаг', 0); Q_OFF = T('А', 3) - 0.1
Q_ACT = [(1, T('Шаг', 0), T('Шаг', 1)), (2, T('Шаг', 1), T('Шаг', 2)), (3, T('Шаг', 2), T('А', 3))]
Q_DONE = {1: T('пересказы.') + 0.4, 2: T('туда.') + 0.2, 3: T('толчка.') + 0.3}
def qcounter(F, t):
    if not (Q_ON <= t < Q_OFF): return
    act = next((n for n, a, b in Q_ACT if a <= t < b), None); done = {n for n, tt in Q_DONE.items() if t >= tt}
    if act in done: act = None
    circles(F, t, act, done)
