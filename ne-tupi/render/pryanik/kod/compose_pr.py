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
CENS = {'БЛЯТЬ': 'БЛ*ТЬ', 'АХУЕ': 'АХ*Е', 'ХУЕВ': 'Х*ЕВ'}
DISP = {'КЛОД': 'CLAUDE', 'КОД.': 'CODE.', 'ГИТХАБА.': 'GITHUB.', 'СЛЭШ': '/INIT', 'ИНИТ,': '', 'КЛОД-ЭМ-ДИ.': 'CLAUDE.MD.', 'КЛОД-ЭМ-ДИ': 'CLAUDE.MD', 'КОНТИНЬЮ.': '--CONTINUE.', 'РЕМОУТ-КОНТРОЛ': 'REMOTE-CONTROL'}
def clean(w):
    w = w.replace('«', '').replace('»', '').upper()
    w = DISP.get(w, w)
    for a, b in CENS.items(): w = w.replace(a, b)
    return w
def subs(F, t):
    for ci, ch in enumerate(CHK):
        t1 = CHK[ci + 1][0][1] if ci + 1 < len(CHK) else ch[-1][2] + 0.6
        if ch[0][1] - 0.04 <= t < t1:
            ims = []
            for (w, a, b) in ch:
                if not clean(w): continue
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
