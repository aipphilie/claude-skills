"""СДВГ-монтаж «Если бы деньги были не важны». Движок «Чаевых» (compose_ch.py).
python3 compose_ch.py 1.5 12.3 -> prev_*.png;  python3 compose_ch.py sheet [доля] -> лист сцен;  без аргументов -> video_noaudio.mp4 + sfx.json"""
from scenes_dv import *
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
SW = 520     # ширина дивана в мечте
def dream_cloud(C, u, cx=540, cy=900, w=820, h=560, k=1.0, tail=(330, 1000), lie=True, glow=True):
    if glow and k > 0.5: rays(C, cx, cy, 620, u, 18, GLOW, 0.8 * clamp((k - 0.5) * 2))
    fluffy(C, cx, cy, w, h, k, tail)
    if k > 0.6 and lie:
        sc = clamp((k - 0.6) / 0.4); sw = SW * 0.95 * sc; by = cy + h * 0.24 * sc
        if sw > 40:
            sofa(C, cx, by, sw)
            lie_on(C, u, cx, by, sw, 'lie', 0.27 * sc)
            remote(C, cx - sw * 0.05, seat_y(by, sw) - sw * 0.26, 0.55 * sc, 70)
            for j, (dx, dy) in enumerate([(-0.55, -0.2), (0.5, -0.32), (0.58, 0.1), (-0.48, 0.12)]): sparkle(C, cx + dx * w * 0.8, cy + dy * h, 26 * sc, u + j)

def s_hook(C, u, t):   # Чем бы ты занимался,
    ground(C); man(C, 'dream', u, 250, G, 0.42)
    fluffy(C, 700, 780, 520, 380, back(clamp((u - 0.15) / 0.35)), (380, 860))
    if u > 0.4: qmark(C, 700, 780, 200, u, INK)
    slam(C, u, 'ЧЕМ БЫ ТЫ', 540, 360, 140); plate(C, u - 0.2, 'ЗАНИМАЛСЯ?', 540, 520, 100, INK, YEL, -3)
def s_hook2(C, u, t):   # если бы деньги были не важны?
    ground(C); man(C, 'dream', u + 1, 250, G, 0.42)
    fluffy(C, 700, 780, 520, 380, 1, (380, 860))
    for j in range(5): bill(C, 700 + (j - 2) * 70, 780 + 20 * s_(u * 4 + j), 120, (j - 2) * 14 + 6 * s_(u * 3 + j))
    xcross(C, u - 0.5, 700, 780, 190, RED, 18)
    slam(C, u, 'ЕСЛИ БЫ ДЕНЬГИ', 540, 360, 116); plate(C, tw(t, 'были') if tw(t, 'были') > -0.1 else -1, 'БЫЛИ НЕ ВАЖНЫ…', 540, 520, 96, INK, YEL, 3)
def s_hero(C, u, t):   # Наш герой отвечает честно:
    ground(C); man(C, 'scratch', u, 540, G, 0.46)
    tag(C, u - 0.1, 'НАШ ГЕРОЙ', 780, 760, 60, YEL, INK, 6); strike(C, u - 0.25, 760, 810, 640, 900, INK, 10)
    slam(C, u, 'ОТВЕЧАЕТ', 540, 360, 140)
    if tw(t, 'честно:') > -0.1: plate(C, tw(t, 'честно:') + 0.1, 'ЧЕСТНО', 540, 520, 110, INK, YEL, -3)
def s_sofa(C, u, t):   # лежал бы на диване.
    dream_cloud(C, u, k=back(clamp(u / 0.35)))
    slam(C, u, 'ЛЕЖАЛ БЫ', 540, 340, 140)
    if tw(t, 'диване.') > -0.1: plate(C, tw(t, 'диване.') + 0.1, 'НА ДИВАНЕ', 540, 500, 110, INK, YEL, 3)
def s_life(C, u, t):   # Всю жизнь.
    dream_cloud(C, u)
    yr = int(lerp(2026, 2076, eo(clamp(u / 0.9)))); calendar(C, 870, 1150, 0.36, str(yr), 'ГОД', back(u / 0.2), -8)
    slam(C, u, 'ВСЮ ЖИЗНЬ', 540, 360, 150)
def s_pretty(C, u, t):   # Красиво.
    YB(C, u, 2); rays(C, 540, 900, 900, u, 20, (255, 236, 120), 1)
    sw = 760; by = 1180; sofa(C, 540, by, sw); lie_on(C, u, 540, by, sw, 'lie_remote', 0.4)
    remote(C, 552, 735 + 4 * s_(u * 5), 0.6, 20)
    for j, (x, y) in enumerate([(160, 700), (920, 680), (200, 1180), (900, 1150), (540, 640)]): sparkle(C, x, y, 44, u + j, WHITE)
    stamp(C, u - 0.1, 'КРАСИВО', 540, 420, 130, INK, -6)
def s_ok(C, u, t):   # Окей, мечта принята.
    ground(C); man(C, 'dream', u, 230, G, 0.42); dream_cloud(C, u, 680, 780, 600, 420, 1, (360, 860))
    slam(C, u, 'ОКЕЙ,', 540, 340, 140)
    if tw(t, 'принята.') > -0.05: stamp(C, tw(t, 'принята.') + 0.05, 'МЕЧТА ПРИНЯТА', 680, 780, 80, RED, -8)
def s_pop(C, u, t):   # Давай посчитаем,
    ground(C)
    if u < 0.12: fluffy(C, 680, 780, 600 * (1 + u * 3), 420 * (1 + u * 3), 1, (360, 860))
    elif u < 0.4:
        burst(C, 680, 780, 300 * (1 + (u - 0.12) * 2), u, 14, WHITE, INK)
        for j in range(10): a = j / 10 * 6.28; r = 300 + (u - 0.12) * 1600; D(C).ellipse([680 + math.cos(a) * r - 22, 780 + math.sin(a) * r - 22, 680 + math.cos(a) * r + 22, 780 + math.sin(a) * r + 22], fill=WHITE, outline=INK, width=5)
    k = eo(clamp((u - 0.1) / 0.35)); man(C, 'fall', u, 230, G, 0.42, rot=lerp(0, -82, k))
    if u > 0.45: txt(C, 'БАЦ!', 760, 1150, 90, RED, back((u - 0.45) / 0.2), -10)
    slam(C, u, 'ДАВАЙ', 540, 340, 140); plate(C, u - 0.15, 'ПОСЧИТАЕМ', 540, 500, 110, INK, YEL, -3)
def s_cost(C, u, t):   # сколько стоит лежать.
    ground(C); man(C, 'shock', u, 260, G, 0.36, rot=lerp(-82, 0, eo(clamp(u / 0.35))))
    calc(C, 700, G + 6, 400, '0', clamp((u - 0.1) / 0.5))
    slam(C, u, 'СКОЛЬКО СТОИТ', 540, 340, 116); plate(C, tw(t, 'лежать.') if tw(t, 'лежать.') > -0.1 else -1, 'ЛЕЖАТЬ?', 540, 500, 120, INK, YEL, 3)
def s_month(C, u, t):   # Чтобы жить на шестьдесят тысяч в месяц
    ground(C); man(C, 'explain', u, 230, G, 0.34)
    on = tw(t, 'шестьдесят') > -0.1; scr = num(roll(tw(t, 'шестьдесят'), 0, 60000, 0.4)) if on else '0'
    calc(C, 660, G + 6, 420, scr)
    slam(C, u, 'ЧТОБЫ ЖИТЬ', 540, 330, 130)
    if on: plate(C, tw(t, 'шестьдесят') + 0.1, '60 000 ₽', 540, 490, 110, INK, YEL, -3)
    if tw(t, 'месяц') > -0.1: tag(C, tw(t, 'месяц') + 0.1, 'В МЕСЯЦ', 660, 620, 54, WHITE, INK, 5)
def s_nowork(C, u, t):   # и не работать,
    ground(C); sw = 560; by = G; sofa(C, 640, by, sw); lie_on(C, u, 640, by, sw, 'lie', 0.32)
    briefcase(C, 220, G - 110, 0.7, -10); xcross(C, u - 0.15, 220, G - 110, 120, RED, 16)
    slam(C, u, 'И НЕ РАБОТАТЬ', 540, 380, 130)
def s_year(C, u, t):   # нужно семьсот двадцать тысяч в год.
    YB(C, u, 4)
    for j in range(12):
        x = 170 + (j % 4) * 247; y = 700 + (j // 4) * 150; k = back((u - j * 0.04) / 0.2)
        put(C, plate_img('60 000', 42, WHITE, INK, pad=10, r=10, border=INK, bw=4), x, y, k, (j % 3 - 1) * 4)
    tag(C, u - 0.3, '× 12 МЕСЯЦЕВ', 540, 1150, 56, INK, YEL, -3)
    slam(C, u, 'НУЖНО', 540, 330, 120)
    if tw(t, 'семьсот') > -0.1: plate(C, tw(t, 'семьсот') + 0.1, '720 000 ₽ В ГОД', 540, 500, 100, INK, WHITE, 3)
def s_bank(C, u, t):   # Банк сейчас даёт около четырнадцати процентов годовых,
    ground(C); bank(C, 360, G, 0.62, label='БАНК'); man(C, 'explain', u, 800, G, 0.36, flip=True)
    slam(C, u, 'БАНК ДАЁТ', 540, 330, 130)
    if tw(t, 'четырнадцати') > -0.1: bignum(C, '≈14%', 760, 760, 170, back(tw(t, 'четырнадцати') / 0.22), -6)
    if tw(t, 'годовых,') > -0.1: tag(C, tw(t, 'годовых,') + 0.1, 'ГОДОВЫХ', 760, 900, 50, WHITE, INK, 4)
def s_tax(C, u, t):   # но минус налог с процентов,
    ground(C); man(C, 'sad', u, 260, G, 0.36)
    k = eo(clamp((u - 0.25) / 0.4)); bignum(C, '14%', 600, 820, 230, 1, -4, bites=((0.9, 0.3, 0.5 * k),) if k > 0.05 else ())
    if k > 0.05: hx = lerp(1150, 920, k) if u < 0.9 else lerp(920, 1200, eo((u - 0.9) / 0.4)); bighand(C, 1300, 900, hx, 760, 110)
    slam(C, u, 'НО МИНУС', 540, 330, 130)
    if tw(t, 'налог') > -0.1: plate(C, tw(t, 'налог') + 0.1, 'НАЛОГ С ПРОЦЕНТОВ', 540, 490, 86, RED, WHITE, -3)
def s_twelve(C, u, t):   # и выходит примерно двенадцать.
    ground(C); man(C, 'shrug', u, 260, G, 0.36)
    if tw(t, 'двенадцать.') > -0.1: bignum(C, '≈12%', 650, 830, 230, back(tw(t, 'двенадцать.') / 0.22), 4)
    else: bignum(C, '14%', 650, 830, 200, 1 - 0.3 * clamp(u / 0.6), 0, ((0.9, 0.3, 0.5),))
    slam(C, u, 'ВЫХОДИТ', 540, 330, 130); plate(C, u - 0.2, 'ПРИМЕРНО', 540, 490, 96, INK, YEL, 3)
def s_need(C, u, t):   # Значит, на вкладе должно лежать…
    ground(C); safe(C, 300, G, 0.95, 'ВКЛАД'); man(C, 'scratch', u, 820, G, 0.34, flip=True)
    rnd = random.Random(int(u * 14)); scr = ''.join(str(rnd.randint(0, 9)) for _ in range(7))
    calc(C, 620, G - 330, 240, scr, 1, 6)
    slam(C, u, 'НА ВКЛАДЕ', 540, 330, 130); plate(C, u - 0.25, 'ДОЛЖНО ЛЕЖАТЬ…', 540, 490, 96, INK, YEL, -3)
def s_six(C, u, t):   # шесть миллионов.
    ground(C); k = clamp(u / 0.3); y = lerp(-200, G - 285, ei(k))
    sq = 1 if k < 1 else 0.45 + 0.55 * math.exp(-(u - 0.3) * 0)   # прижат
    if k < 1: man(C, 'shock', u, 540, G, 0.42)
    else: man(C, 'pressed', u, 540, G, 0.42, sx=1.35, sy=0.42)
    shake = 14 * math.exp(-(u - 0.3) * 6) * s_(u * 70) if k >= 1 else 0
    bignum(C, '6 000 000 ₽', 540 + shake, y, 170, 1, 0)
    if k >= 1: txt(C, 'ХРЯСЬ!', 540, 820, 100, RED, back((u - 0.3) / 0.2), 8)
    src(C, 'Расчёт упрощённый: 720 000 ₽ ÷ 12% = 6 000 000 ₽', 1318)
def s_infl(C, u, t):   # А ещё инфляция каждый год съедает кусок,
    ground(C); man(C, 'pressed', u, 540, G, 0.42, sx=1.35, sy=0.42)
    mx = lerp(1300, 870, eo(clamp(u / 0.5))); monster(C, mx, 720, 85, u)
    nb = int(clamp((u - 0.6) / 1.6) * 4 + (0.99 if u > 0.6 else 0)); bites = [(0.98 - q * 0.12, 0.35 + (q % 2) * 0.2, 0.42) for q in range(nb)]
    bignum(C, '6 000 000 ₽', 540, G - 285, 170, 1, 0, tuple(bites))
    slam(C, u, 'А ЕЩЁ ИНФЛЯЦИЯ', 540, 330, 110)
    if tw(t, 'съедает') > -0.1: plate(C, tw(t, 'съедает') + 0.1, 'СЪЕДАЕТ КУСОК', 540, 490, 96, RED, WHITE, -3)
def s_more(C, u, t):   # так что честно — ещё больше.
    YB(C, u, 5); man(C, 'shrug', u, 540, G + 40, 0.42)
    bignum(C, '6 000 000 ₽ +', 540, 760, 140, 1 + 0.18 * eo(clamp((u - 0.4) / 1.0)), -3, col=WHITE)
    for j in range(2):
        x = 150 + j * 780; y = 1010 - 30 * s_(u * 6 + j); D(C).polygon([(x, y - 50), (x + 45, y + 30), (x - 45, y + 30)], fill=INK)
    slam(C, u, 'ЧЕСТНО —', 540, 330, 130); plate(C, tw(t, 'больше.') if tw(t, 'больше.') > -0.1 else -1, 'ЕЩЁ БОЛЬШЕ', 540, 490, 110, INK, WHITE, 3)
def s_trick(C, u, t):   # Но фишка в другом.
    ground(C); man(C, 'pressed', 0, 540, G, 0.42, sx=lerp(1.35, 1, eo(clamp(u / 0.3))), sy=lerp(0.42, 1, eo(clamp(u / 0.3)))) if u < 0.3 else man(C, 'pointcam', u, 540, G, 0.46)
    bignum(C, '6 000 000 ₽', lerp(540, 1500, ei(clamp(u / 0.4))), G - 285, 170, 1, -20 * clamp(u / 0.4))
    slam(C, u, 'НО ФИШКА', 540, 330, 140); plate(C, u - 0.2, 'В ДРУГОМ', 540, 490, 110, INK, YEL, -3)
def s_notdream(C, u, t):   # Диван не мечта.
    ground(C); sofa(C, 540, G, 640); xcross(C, u - 0.3, 540, G - 200, 280, RED, 22)
    slam(C, u, 'ДИВАН', 540, 340, 150); plate(C, u - 0.2, 'НЕ МЕЧТА', 540, 510, 110, RED, WHITE, 3)
def s_want(C, u, t):   # Мечта — это когда работаешь, потому что хочешь,
    office(C, u); desk(C, 640, G, 480, 210); laptop(C, 640, G - 210, 300, u); man(C, 'work', u, 300, G, 0.4)
    for j in range(3): heart(C, 180 + j * 110, 760 - 40 * ((u * 0.8 + j * 0.33) % 1) * 3, 30, HRT)
    slam(C, u, 'МЕЧТА — ЭТО', 540, 330, 120)
    if tw(t, 'работаешь,') > -0.1: plate(C, tw(t, 'работаешь,') + 0.1, 'РАБОТАЕШЬ, ПОТОМУ ЧТО ХОЧЕШЬ', 540, 490, 70, INK, YEL, -3)
def s_food(C, u, t):   # а не потому что жрать надо.
    office(C, u); desk(C, 640, G, 480, 210); laptop(C, 640, G - 210, 300, u); man(C, 'tired', u, 300, G, 0.4)
    plate_food(C, 860, G - 228, 70, True); txt(C, '...', 860, G - 290, 60, GREY)
    slam(C, u, 'А НЕ ПОТОМУ', 540, 330, 120)
    if tw(t, 'жрать') > -0.1: plate(C, tw(t, 'жрать') + 0.1, 'ЧТО ЖРАТЬ НАДО', 540, 490, 96, RED, WHITE, 3)
PIG = (560, G)
def coin_drop(C, u, t0, x0=420):
    """монетка летит из руки в копилку за 0.45 сек"""
    q = clamp((u - t0) / 0.45)
    if 0 < q < 1: coin(C, lerp(x0, PIG[0] + 10, q), lerp(G - 330, G - 300, q) - 160 * s_(math.pi * q), 34, q * 360)
def s_rub(C, u, t):   # И каждый отложенный рубль
    ground(C); man(C, 'give', u, 280, G, 0.4); piggy(C, PIG[0], G, 0.75, u)
    coin_drop(C, u, 0.15, 400)
    leg = clamp((u - 0.7) / 0.3); sofa(C, 860, G, 300, ('legL',), back(leg) if leg > 0 else 0)
    slam(C, u, 'КАЖДЫЙ', 540, 330, 140)
    if tw(t, 'отложенный') > -0.1: plate(C, tw(t, 'отложенный') + 0.1, 'ОТЛОЖЕННЫЙ РУБЛЬ', 540, 490, 90, INK, YEL, -3)
def s_piece(C, u, t):   # это кусочек дивана,
    ground(C); man(C, 'give', u + 1, 280, G, 0.4); piggy(C, PIG[0], G, 0.75, u)
    coin_drop(C, u, 0.05, 400)
    arm = clamp((u - 0.45) / 0.25); sofa(C, 860, G, 300, ('legL', 'armL') if arm > 0 else ('legL',))
    if 0 < arm < 1: sparkle(C, 790, G - 110, 50 * (1 - arm) + 20, u)
    slam(C, u, 'ЭТО КУСОЧЕК', 540, 330, 120)
    if tw(t, 'дивана,') > -0.1: plate(C, tw(t, 'дивана,') + 0.1, 'ДИВАНА', 540, 490, 120, INK, YEL, 3)
def s_yours(C, u, t):   # который уже твой.
    ground(C); man(C, 'nod', u, 230, G, 0.36); piggy(C, 470, G, 0.6, u)
    n = 2 + int(clamp(u / 0.9) * 3); parts = ('legL', 'armL', 'legR', 'seat', 'armR')[:n]; sofa(C, 820, G, 360, parts)
    slam(C, u, 'КОТОРЫЙ', 540, 330, 130)
    if tw(t, 'твой.') > -0.05: stamp(C, tw(t, 'твой.') + 0.05, 'УЖЕ ТВОЙ', 540, 520, 100, RED, -6)
def s_dontdream(C, u, t):   # Так что не мечтай о диване.
    ground(C); man(C, 'net', u, 330, G, 0.42)
    fluffy(C, 680, 820, 520, 380, 1 - 0.15 * clamp(u / 1), (440, 900)); sofa(C, 680, 900, 300)
    xcross(C, u - 0.5, 680, 820, 180, RED, 18)
    slam(C, u, 'НЕ МЕЧТАЙ', 540, 330, 140)
    if tw(t, 'диване.', 1) > -0.1: plate(C, tw(t, 'диване.', 1) + 0.1, 'О ДИВАНЕ', 540, 490, 110, INK, YEL, -3)
def sit_scene(C, u, cx=540, w=560, s=0.46, clip='sit_thumb'):
    L = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); parts = ('legL', 'armL', 'seat', 'back', 'cush')
    sofa(L, cx, G, w, parts); man(L, clip, u, cx - w * 0.05, seat_y(G, w) - w * 0.02, s)
    ang = 7 * s_(u * 3.5) - 4      # кренится на сторону без ножки
    px, py = cx - w * 0.4, G
    big = L.rotate(ang, Image.BICUBIC, center=(px, py)); C.alpha_composite(big)
    return ang
def s_build(C, u, t):   # Собирай его.
    ground(C); sit_scene(C, u)
    thumb(C, 860, 760, 0.8, -10, back((u - 0.25) / 0.25))
    slam(C, u, 'СОБИРАЙ', 540, 330, 150); plate(C, tw(t, 'его.') if tw(t, 'его.') > -0.1 else -1, 'ЕГО', 540, 500, 130, INK, YEL, 3)
def s_netupi(C, u, t):   # НЕ ТУПИ (текст на экране)
    C.paste(YEL, [0, 0, CW, CH]); speedlines(C, 540, 900, u, r0=520, col=(246, 200, 0))
    sit_scene(C, u + 2)
    thumb(C, 860, 760, 0.8, -10)
    slam(C, u, 'НЕ ТУПИ', 540, 420, 190)

PUSH_FLIP = False
def SH(t0, fn, tr='zoom', sfx='whoosh', p=None): return dict(t=t0, fn=fn, tr=tr, sfx=sfx, p=p)
SHOTS = [
 SH(0.0, s_hook, 'none', 'pop'), SH(T('если') - 0.05, s_hook2, 'whipL', 'whoosh'), SH(T('Наш') - 0.05, s_hero, 'whipR', 'whoosh'),
 SH(T('лежал') - 0.05, s_sofa, 'zoomthru', 'bass', (330, 700)), SH(T('Всю') - 0.05, s_life, 'zoom', 'whoosh'), SH(T('Красиво.') - 0.05, s_pretty, 'zoomthru', 'shine', (540, 900)),
 SH(T('Окей,') - 0.05, s_ok, 'whipL', 'whoosh'), SH(T('Давай') - 0.05, s_pop, 'shake', 'pop'), SH(T('сколько') - 0.05, s_cost, 'whipR', 'bass'),
 SH(T('Чтобы') - 0.05, s_month, 'push', 'whoosh'), SH(T('и', 0) - 0.05, s_nowork, 'whipL', 'whoosh'), SH(T('нужно') - 0.05, s_year, 'zoom', 'bass'),
 SH(T('Банк') - 0.05, s_bank, 'door', 'thud'), SH(T('но', 0) - 0.05, s_tax, 'whipR', 'whoosh'), SH(T('выходит') - 0.05, s_twelve, 'whipL', 'whoosh'),
 SH(T('Значит,') - 0.05, s_need, 'zoom', 'riser'), SH(T('шесть') - 0.05, s_six, 'cut', 'boom'), SH(T('А') - 0.05, s_infl, 'whipL', 'whoosh'),
 SH(T('так') - 0.05, s_more, 'zoom', 'bass'), SH(T('Но') - 0.05, s_trick, 'shake', 'scratch'), SH(T('Диван') - 0.05, s_notdream, 'whipR', 'whoosh'),
 SH(T('Мечта') - 0.05, s_want, 'door', 'thud'), SH(T('а', 0) - 0.05, s_food, 'whipL', 'whoosh'), SH(T('И') - 0.05, s_rub, 'bodywipe', 'bass'),
 SH(T('это', 1) - 0.05, s_piece, 'zoom', 'whoosh'), SH(T('который') - 0.05, s_yours, 'whipR', 'whoosh'), SH(T('Так') - 0.05, s_dontdream, 'push', 'bass'),
 SH(T('Собирай') - 0.05, s_build, 'zoomthru', 'whoosh', (680, 900)), SH(END + 0.25, s_netupi, 'zoomthru', 'final', (540, 800)),
]
ACC = [(T('занимался,') + 0.3, 'pop'), (T('важны?') - 0.2, 'error'), (T('честно:'), 'pop'), (T('диване.', 0), 'angel'), (T('Всю') + 0.2, 'tick'),
       (T('принята.') + 0.05, 'stamp'), (T('посчитаем,') + 0.1, 'thud'), (T('лежать.', 0) + 0.1, 'kassa'), (T('шестьдесят'), 'click'), (T('месяц'), 'pop'),
       (T('работать,') + 0.1, 'error'), (T('семьсот'), 'kassa'), (T('четырнадцати'), 'pop'), (T('налог'), 'scratch'), (T('двенадцать.'), 'pop'),
       (T('шесть') + 0.3, 'thud'), (T('инфляция') + 0.2, 'boing'), (T('съедает'), 'crunch'), (T('кусок,'), 'crunch'), (T('больше.'), 'pop'),
       (T('мечта', 1) - 0.1, 'error'), (T('работаешь,'), 'heart'), (T('жрать'), 'error'), (T('рубль'), 'coins'), (T('кусочек'), 'coins'),
       (T('дивана,'), 'shine'), (T('твой.') + 0.05, 'stamp'), (T('диване.', 1), 'error'), (T('его.'), 'ding')]
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
