"""СДВГ-монтаж «Почему в казино нет часов и окон». Движок «Чаевых» (compose_ch.py).
python3 compose_ch.py 1.5 12.3 -> prev_*.png;  python3 compose_ch.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_kz import *
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

# ================= СЦЕНЫ =================  fn(C, u, t)
def s_hook(C, u, t):   # Сколько сейчас времени?
    YB(C, u); wallclock(C, 540, 760, 175, u, 3.0, scale=back(u / 0.25), rot=8 * s_(u * 9))
    man(C, 'wrist', u, 540, G + 60, 0.4)
    slam(C, u, 'СКОЛЬКО', 540, 360, 150); plate(C, u - 0.15, 'СЕЙЧАС ВРЕМЕНИ?', 540, 530, 86, INK, YEL, -3)
def s_dontlook(C, u, t):   # Не смотри!
    RB(C, u, 2); man(C, 'net', u, 540, G + 60, 0.56)
    slam(C, u, 'НЕ СМОТРИ!', 540, 420, 170, WHITE, -4, INK, 10)
def s_dunno(C, u, t):   # Не знаешь?
    ground(C); man(C, 'shrug', u, 540, G, 0.5); qmark(C, 300, 780, 240, u); qmark(C, 800, 720, 190, u + 1)
    slam(C, u, 'НЕ ЗНАЕШЬ?', 540, 400, 150)
def s_casino(C, u, t):   # Поздравляю, ты в казино.
    casino(C, u); slotm(C, 330, G, 0.95, u, True, lever=0.5 + 0.5 * s_(u * 6)); man(C, 'slot', u, 720, G, 0.46, flip=True)
    for j in range(8): burst(C, 120 + j * 130, 700 + 40 * s_(u * 4 + j), 18, u, 4, YEL, INK, j)
    slam(C, u, 'ПОЗДРАВЛЯЮ,', 540, 340, 110)
    if tw(t, 'казино.') > -0.1: plate(C, tw(t, 'казино.') + 0.1, 'ТЫ В КАЗИНО', 540, 500, 110, INK, YEL, 3)
def s_noclock(C, u, t):   # Нет, ну вы это видели? В казино нет ни часов,
    casino(C, u); emptyclock(C, 540, 880, 190); man(C, 'scratch', u, 820, G, 0.36, flip=True)
    slam(C, u, 'ВЫ ЭТО ВИДЕЛИ?', 540, 380, 116)
    if tw(t, 'часов,') > -0.1: plate(C, tw(t, 'часов,') + 0.1, 'НИ ЧАСОВ', 540, 545, 110, RED, WHITE, -3)
def s_nowin(C, u, t):   # ни окон.
    casino(C, u); brickwin(C, 540, 900, 420, 400, clamp(u / 0.35)); man(C, 'shock', u, 860, G, 0.34, flip=True)
    slam(C, u, 'НИ ОКОН', 540, 420, 160)
def s_puppet(C, u, t):   # Думаешь, это чтобы тебя обмануть и ты играл до утра?
    casino(C, u); slotm(C, 330, G, 0.9, u, True, lever=0.5 + 0.5 * s_(u * 6)); man(C, 'slot', u, 720, G, 0.44, flip=True)
    hy = 640 + 10 * s_(u * 3); bighand(C, 1200, 300, 780, hy, 130)
    strings(C, 780, hy + 40, [(640, 860), (700, 760), (760, 760), (820, 860)])
    slam(C, u, 'ДУМАЕШЬ,', 540, 360, 130)
    if tw(t, 'обмануть') > -0.1: plate(C, tw(t, 'обмануть') + 0.1, 'ЧТОБЫ ОБМАНУТЬ?', 540, 520, 90, LG, INK, 3)
def s_catch(C, u, t):   # А вот и подвох.
    casino(C, u); slotm(C, 330, G, 0.9, u, False, ('7', '$', '7')); man(C, 'shock', u, 720, G, 0.44, flip=True)
    k = clamp(u / 0.3); bighand(C, 1200, 300, lerp(780, 1100, k), lerp(640, 420, k), 130); strings(C, 780, 680, [(640, 860), (700, 760), (760, 760), (820, 860)], k + 0.01)
    tape(C, u, 'А ВОТ И ПОДВОХ', 420, 150, -5)
def s_friedman(C, u, t):   # Билл Фридман, который проектировал казино в Вегасе, говорил:
    ground(C); grey_man(C, 'explain', u, 360, 0.46); blueprint(C, 760, 900, 360, 280, -6, back(u / 0.25))
    slam(C, u, 'БИЛЛ ФРИДМАН', 540, 360, 130)
    if tw(t, 'проектировал') > -0.1: plate(C, tw(t, 'проектировал') + 0.1, 'ПРОЕКТИРОВАЛ КАЗИНО', 540, 520, 76, INK, YEL, -3)
    if tw(t, 'Вегасе,') > -0.1: tag(C, tw(t, 'Вегасе,') + 0.1, 'ЛАС-ВЕГАС', 760, 1110, 54, WHITE, INK, 4)
def s_removed(C, u, t):   # часы убрали,
    casino(C, u); emptyclock(C, 540, 760, 120); stretcher(C, u, lerp(420, 700, eo(u / 0.9)), G, 0.28)
    slam(C, u, 'ЧАСЫ УБРАЛИ', 540, 380, 140)
def s_demand(C, u, t):   # потому что этого потребовали сами игроки.
    casino(C, u, lights=False)
    for j, x in enumerate((200, 540, 880)):
        sc = 0.32 + 0.04 * (j == 1); man(C, 'sign', u + j * 0.25, x, G, sc, flip=j == 2); L = Image.new('RGBA', (CW, CH)); placard(L, x, G - sc * 1250 - 70, 240, 'УБЕРИТЕ\nЧАСЫ!', 5 * s_(u * 8 + j)); C.alpha_composite(L.crop((0, 0, CW, int(G - sc * 1060))), (0, 0))
    slam(C, u, 'ПОТРЕБОВАЛИ', 540, 360, 130)
    if tw(t, 'игроки.') > -0.05: stamp(C, tw(t, 'игроки.') + 0.05, 'САМИ ИГРОКИ', 540, 540, 100, RED, -6)
def s_threat(C, u, t):   # Иначе грозились не вернуться.
    RB(C, u, 5)
    for j, x in enumerate((220, 540, 860)): man(C, 'angry', u + j * 0.3, x, G + 40, 0.36 + 0.05 * (j == 1), flip=j == 2)
    slam(C, u, 'ИНАЧЕ', 540, 360, 150, WHITE)
    if tw(t, 'не', 0) > -0.1: plate(C, tw(t, 'не', 0) + 0.1, 'НЕ ВЕРНЁМСЯ!', 540, 530, 100, INK, YEL, 3)
def s_notime(C, u, t):   # Они не хотели знать, сколько времени.
    casino(C, u); man(C, 'slot', u, 540, G, 0.44)
    for j, (x, y) in enumerate([(200, 760), (880, 760), (190, 1060), (890, 1060)]):
        wallclock(C, x, y, 80, u, 1.0, LG, GREY, back((u - j * 0.1) / 0.2)); xcross(C, u - 0.3 - j * 0.12, x, y, 80, RED, 12)
    slam(C, u, 'НЕ ХОТЕЛИ', 540, 360, 140); plate(C, tw(t, 'знать,') if tw(t, 'знать,') > -0.1 else -1, 'ЗНАТЬ ВРЕМЯ', 540, 520, 100, INK, YEL, -3)
def s_escape(C, u, t):   # Они пришли сбежать.
    ground(C); bubble_escape(C, 540, 940, 430, 330, u, back(u / 0.3)); man(C, 'idle_smile', u, 540, G, 0.4)
    for j, (x, y) in enumerate([(120, 700), (960, 720), (110, 1180), (970, 1180)]): wallclock(C, x, y, 56, u, 1.5, LG, GREY)
    slam(C, u, 'ПРИШЛИ', 540, 360, 150)
    if tw(t, 'сбежать.') > -0.1: plate(C, tw(t, 'сбежать.') + 0.1, 'СБЕЖАТЬ', 540, 525, 110, INK, YEL, 3)
def s_notsimple(C, u, t):   # А это оказалось не так просто.
    YB(C, u, 7); man(C, 'think', u, 540, G + 40, 0.52)
    slam(C, u, 'А ЭТО ОКАЗАЛОСЬ', 540, 360, 110); plate(C, u - 0.25, 'НЕ ТАК ПРОСТО', 540, 520, 100, INK, WHITE, -3)
def s_pocket(C, u, t):   # Сегодня часы есть у каждого в кармане.
    ground(C); man(C, 'idle', u, 330, G, 0.46)
    k = eo(clamp(u / 0.4)); bigphone(C, lerp(380, 740, k), lerp(1130, 900, k), 260, 470, u, 'time', '03:47', max(0.2, k), rot=lerp(30, -4, k))
    slam(C, u, 'ЧАСЫ ЕСТЬ', 540, 360, 140)
    if tw(t, 'кармане.') > -0.1: plate(C, tw(t, 'кармане.') + 0.1, 'У КАЖДОГО В КАРМАНЕ', 540, 520, 74, INK, YEL, 3)
def s_nolook(C, u, t):   # Только кто на них смотрит?
    casino(C, u); slotm(C, 640, G, 0.9, u, True, lever=0.5 + 0.5 * s_(u * 6)); man(C, 'slot', u, 300, G, 0.44)
    bigphone(C, 170, 1180, 120, 216, u, 'time', '03:47', 1, rot=-70)
    slam(C, u, 'КТО НА НИХ', 540, 360, 140); plate(C, u - 0.2, 'СМОТРИТ?', 540, 520, 110, INK, YEL, -3)
def s_stop(C, u, t):   # Стоп. Тут ты тупишь.
    YB(C, u, 3); man(C, 'pointcam', u, 540, G + 60, 0.56)
    plate(C, u, 'СТОП.', 540, 360, 150, INK, YEL, -3)
    if tw(t, 'Тут') > -0.1: plate(C, tw(t, 'Тут') + 0.1, 'ТУТ ТЫ ТУПИШЬ', 540, 540, 100, WHITE, INK, 3, border=INK)
def s_youare(C, u, t):   # Ты прямо сейчас сидишь в таком же казино.
    casino(C, u); k = eo(clamp((u - 0.3) / 0.6))
    if k < 0.5: slotm(C, 540, G, 0.95 * (1 - k * 0.8), u, True)
    else: bigphone(C, 540, G - 360, 300, 540, u, 'feed', k=lerp(0.4, 1, (k - 0.5) * 2), scroll=u * 1.5)
    man(C, 'phone_scr', u, 860, G, 0.38, flip=True)
    slam(C, u, 'ТЫ ПРЯМО СЕЙЧАС', 540, 340, 110)
    if tw(t, 'таком') > -0.1: plate(C, tw(t, 'таком') + 0.1, 'В ТАКОМ ЖЕ КАЗИНО', 540, 500, 86, RED, WHITE, -3)
def s_feed(C, u, t):   # Лента без дна.
    ground(C); bigphone(C, 540, 880, 380, 700, u, 'feed', scroll=u * 2.5, k=back(u / 0.2))
    man(C, 'phone_scr', u, 880, G, 0.3, flip=True)
    slam(C, u, 'ЛЕНТА', 540, 330, 140)
    if tw(t, 'дна.') > -0.1: plate(C, tw(t, 'дна.') + 0.1, 'БЕЗ ДНА', 540, 480, 100, INK, YEL, 3)
def s_auto(C, u, t):   # Следующее видео включается само.
    ground(C); bigphone(C, 540, 880, 380, 700, u, 'play', scroll=u * 1.2); man(C, 'idle', u, 200, G, 0.3)
    slam(C, u, 'СЛЕДУЮЩЕЕ', 540, 330, 130)
    if tw(t, 'само.') > -0.1: plate(C, tw(t, 'само.') + 0.1, 'ВКЛЮЧАЕТСЯ САМО', 540, 480, 80, INK, YEL, -3)
def s_nobtn(C, u, t):   # Нигде нет точки «хватит».
    ground(C); nobutton(C, 540, 840, 560, 180, u); man(C, 'scratch', u, 540, G, 0.3)
    slam(C, u, 'НИГДЕ НЕТ', 540, 360, 140)
    if tw(t, 'хватит».') > -0.1: plate(C, tw(t, 'хватит».') + 0.1, 'ТОЧКИ «ХВАТИТ»', 540, 520, 90, RED, WHITE, 3)
def s_inventor(C, u, t):   # Человек, который придумал бесконечную ленту,
    ground(C); desk(C, 560, G, 460, 200); laptop(C, 560, G - 200, 330, u, clamp(u / 1.4)); grey_man(C, 'idle_smile', u, 220, 0.42)
    slam(C, u, 'ПРИДУМАЛ', 540, 360, 140)
    if tw(t, 'бесконечную') > -0.1: plate(C, tw(t, 'бесконечную') + 0.1, 'БЕСКОНЕЧНУЮ ЛЕНТУ', 540, 520, 82, INK, YEL, -3)
def s_regret(C, u, t):   # потом сам признался, что жалеет.
    ground(C); desk(C, 560, G, 460, 200); laptop(C, 560, G - 200, 330, u, 1.0); grey_man(C, 'sad', u, 220, 0.42)
    slam(C, u, 'ПОТОМ ПРИЗНАЛСЯ:', 540, 360, 110)
    if tw(t, 'жалеет.') > -0.05: stamp(C, tw(t, 'жалеет.') + 0.05, 'ЖАЛЕЮ', 540, 640, 110, RED, -8)
def s_what(C, u, t):   # И что с этим делать?
    YB(C, u, 9); man(C, 'shrug', u, 540, G + 40, 0.54)
    slam(C, u, 'И ЧТО', 540, 360, 160); plate(C, u - 0.2, 'С ЭТИМ ДЕЛАТЬ?', 540, 530, 96, INK, WHITE, 3)
def s_hang(C, u, t):   # Повесь часы сам.
    casino(C, u); emptyclock(C, 540, 820, 150); wallclock(C, 400, 820, 130, u, 0.2, YEL, INK)
    man(C, 'hammer', u, 700, G, 0.44, flip=True)
    slam(C, u, 'ПОВЕСЬ ЧАСЫ', 540, 360, 130)
    if tw(t, 'сам.') > -0.1: plate(C, tw(t, 'сам.') + 0.1, 'САМ', 540, 520, 130, INK, YEL, -3)
def s_decide(C, u, t):   # До того как открыть ленту, реши: двадцать минут.
    ground(C); man(C, 'think', u, 260, G, 0.42)
    show = tw(t, 'двадцать') > -0.1
    bigphone(C, 740, 880, 300, 540, u, 'timer' if show else 'feed', '20:00', back(u / 0.2), 0.0 if show else u * 0.3)
    slam(C, u, 'ДО ТОГО КАК ОТКРЫТЬ', 540, 340, 96)
    if tw(t, 'реши:') > -0.1: plate(C, tw(t, 'реши:') + 0.1, 'РЕШИ ЗАРАНЕЕ', 540, 490, 90, INK, YEL, 3)
    if show: tag(C, tw(t, 'двадцать') + 0.1, '20 МИНУТ', 740, 1220, 70, YEL, INK, -4)
def s_timer(C, u, t):   # Поставь таймер.
    YB(C, u, 4); q = clamp(u / 0.95); sec = int(20 * 60 * (1 - q)); bigphone(C, 540, 900, 360, 640, u, 'timer', f'{sec // 60:02d}:{sec % 60:02d}', 1, q)
    slam(C, u, 'ПОСТАВЬ ТАЙМЕР', 540, 360, 116)
def s_out(C, u, t):   # Прозвенел — встал и вышел.
    ground(C); alarm(C, 300, 840, 0.6, u, True, '00:00'); bigphone(C, 300, G - 20, 120, 216, u, 'time', '', 1, rot=90)
    x = lerp(620, 1000, clamp((u - 0.5) / 1.2)); man(C, 'walkR', u, x, G, 0.42)
    slam(C, u, 'ПРОЗВЕНЕЛ', 540, 360, 140)
    if tw(t, 'встал') > -0.1: plate(C, tw(t, 'встал') + 0.1, 'ВСТАЛ И ВЫШЕЛ', 540, 520, 96, INK, YEL, -3)
def s_ring(C, u, t):   # В казино часов нет.
    casino(C, u); brickwin(C, 270, 860, 300, 360, 1, u, clamp((u - 0.2) / 0.9), clamp((u - 0.5) / 0.4))
    wallclock(C, 760, 820, 140, u, 0.25, YEL, INK); man(C, 'idle_smile', u, 540, G, 0.36)
    slam(C, u, 'В КАЗИНО', 540, 360, 140)
    if tw(t, 'часов', 1) > -0.1: plate(C, tw(t, 'часов', 1) + 0.1, 'ЧАСОВ НЕТ', 540, 520, 110, LG, INK, 3)
def s_own(C, u, t):   # Поэтому носи свои.
    YB(C, u, 6); wallclock(C, 540, 735, 145, u, 0.25, WHITE, INK, back(u / 0.25)); man(C, 'nod', u, 540, G + 40, 0.36)
    slam(C, u, 'ПОЭТОМУ', 540, 340, 130)
    if tw(t, 'носи') > -0.1: plate(C, tw(t, 'носи') + 0.1, 'НОСИ СВОИ', 540, 500, 120, INK, YEL, -3)
def s_vse(C, u, t):   # Всё.
    casino(C, u); wallclock(C, 540, 800, 130, u, 0.25, YEL, INK); man(C, 'walkR', u, lerp(540, 760, clamp(u / 0.6)), G, 0.42)
    slam(C, u, 'ВСЁ.', 540, 400, 180)
def s_netupi(C, u, t):   # Не тупи.
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    man(C, 'pointcam', u, 540, G + 40, 0.56)
    slam(C, u, 'НЕ ТУПИ', 540, 420, 190)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'tick'), SH(T('Не', 0) - 0.05, s_dontlook, 'shake', 'boom'), SH(T('Не', 1) - 0.05, s_dunno, 'whipL', 'whoosh'),
 SH(T('Поздравляю,') - 0.05, s_casino, 'zoomthru', 'bass', (540, 900)), SH(T('Нет,') - 0.05, s_noclock, 'whipR', 'whoosh'),
 SH(T('ни', 1) - 0.05, s_nowin, 'whipL', 'thud'), SH(T('Думаешь,') - 0.05, s_puppet, 'door', 'thud'), SH(T('А', 0) - 0.05, s_catch, 'shake', 'scratch'),
 SH(T('Билл') - 0.05, s_friedman, 'push', 'bass'), SH(T('часы', 0) - 0.05, s_removed, 'whipL', 'whoosh'), SH(T('потому') - 0.05, s_demand, 'whipR', 'whoosh'),
 SH(T('Иначе') - 0.05, s_threat, 'shake', 'boom'), SH(T('Они', 0) - 0.05, s_notime, 'drop', 'thud'), SH(T('Они', 1) - 0.05, s_escape, 'zoomthru', 'whoosh', (540, 900)),
 SH(T('А', 1) - 0.05, s_notsimple, 'glitch', 'riser'), SH(T('Сегодня') - 0.05, s_pocket, 'whipL', 'whoosh'), SH(T('Только') - 0.05, s_nolook, 'whipR', 'whoosh'),
 SH(T('Стоп.') - 0.05, s_stop, 'shake', 'scratch'), SH(T('Ты') - 0.05, s_youare, 'zoom', 'bass'), SH(T('Лента') - 0.05, s_feed, 'zoomthru', 'whoosh', (540, 1000)),
 SH(T('Следующее') - 0.05, s_auto, 'whipU', 'swipe'), SH(T('Нигде') - 0.05, s_nobtn, 'whipL', 'whoosh'),
 SH(T('Человек,') - 0.05, s_inventor, 'bodywipe', 'bass'), SH(T('потом') - 0.05, s_regret, 'zoom', 'whoosh'),
 SH(T('И', 0) - 0.05, s_what, 'push', 'bass'), SH(T('Повесь') - 0.05, s_hang, 'door', 'thud'), SH(T('До') - 0.05, s_decide, 'whipL', 'whoosh'),
 SH(T('Поставь') - 0.05, s_timer, 'zoom', 'tick'), SH(T('Прозвенел') - 0.05, s_out, 'shake', 'alarm'),
 SH(T('В', 1) - 0.05, s_ring, 'drop', 'thud'), SH(T('Поэтому') - 0.05, s_own, 'zoomthru', 'bass', (760, 820)),
 SH(T('Всё.') - 0.05, s_vse, 'door', 'thud'), SH(T('Не', 2) - 0.05, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('времени?', 0), 'pop'), (T('казино.', 0), 'kassa'), (T('часов,'), 'error'), (T('окон.') + 0.1, 'thud'), (T('обмануть'), 'pop'),
       (T('Вегасе,'), 'pop'), (T('игроки.') + 0.05, 'stamp'), (T('вернуться.'), 'pop'), (T('знать,'), 'error'), (T('сбежать.'), 'shine'),
       (T('кармане.'), 'notif'), (T('смотрит?'), 'pop'), (T('Тут') + 0.1, 'click'), (T('таком'), 'boom'), (T('дна.'), 'drop'),
       (T('само.'), 'pop'), (T('хватит».'), 'error'), (T('бесконечную'), 'pop'), (T('жалеет.') + 0.05, 'stamp'), (T('сам.', 1), 'clang'),
       (T('двадцать'), 'pop'), (T('вышел.'), 'whoosh'), (T('часов', 1), 'pop'), (T('свои.'), 'ding'), (T('тупи.'), 'stamp')]
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
