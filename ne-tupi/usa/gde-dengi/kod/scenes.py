"""Сцены ролика «Почему денег нет, даже когда зарплата растёт». Координаты элементов — относительно центра графики шота."""
from tl import wt, O, GAP, END, NCH
from gfx import YEL, RED, INK, WHITE, GRAY, GREEN
SHOTS = []
def E(kind, ta, te=None, **kw): return (kind, ta, te, kw)
def shot(t, side, els, anim=(), s=0.72):
    SHOTS.append(dict(t=t, side=side, s=s, anim=list(anim), els=els))
LIGHT = (205, 205, 205)

# ---------- 0. холодный старт ----------
c = lambda s, k=0: wt(0, s, k)
shot(0, 'L', [E('emoji', 0.0, x=-330, y=-250, ch='🌙', size=130),
              E('card', 0.4, x=60, y=-250, text='PAYDAY TOMORROW', sz=50),
              E('phone', c('банк') - 0.3, x=0, y=80, text='0 $', sz=110)],
     anim=['dyhanie', 'pozhimaet-plechami'])
STEP = [(-330, 230), (0, 90), (330, -50)]
els = []
for k, (w, kk) in enumerate([('поднимали', 0), ('один', 0), ('Теперь', 0)]):
    x, y = STEP[k]; ta = c(w, kk) - 0.1
    els += [E('card', ta, x=x, y=y, text='+ RAISE', sz=36)]
els += [E('red', c('нуле') - 0.1, x=-330, y=130, text='0 $', sz=44), E('red', c('нуле', 1) - 0.1, x=330, y=-150, text='0 $', sz=44),
        E('red', c('нуле', 1) + 0.2, x=0, y=-10, text='0 $', sz=44),
        E('plate', c('Простите') - 0.1, x=-250, y=-260, text='WHAT FOR?!', sz=64, rot=-4)]
shot(c('ведь') - 0.2, 'R', els, anim=['razgovor', 'cheshet-golovu', 'pozhimaet-plechami'])
shot(c('Стоп') - 0.2, 'L', [E('plate', c('Стоп') - 0.05, x=0, y=-250, text="STOP.\nYOU'RE BEING DUMB", sz=84, rot=-3),
                            E('card', c('Деньги'), x=0, y=40, text='"I JUST DON\'T MAKE ENOUGH"', sz=50),
                            E('crossline', c('мало') + 0.1, x=0, y=40, w=620),
                            E('dark', c('утекает') - 0.2, x=0, y=220, text='EVERY RAISE LEAKS OUT', sz=44)],
     anim=['ukazyvaet-vverh', 'net'], s=0.76)
shot(c('сегодня') - 0.2, 'R', [E('bucket', c('четыре') - 0.4, x=-40, y=80, sc=0.85),
                               E('flash', c('правило') - 0.1, x=0, y=310, text='THE HALF RULE'),
                               E('plate', c('где') - 0.1, x=0, y=310, text="WHERE'S THE MONEY?", sz=96, rot=-2)],
     anim=['obyasnyaet', 'ruki-v-boki'])
HOLE_T = [None] * 4

# ---------- 1. это не цены ----------
c = lambda s, k=0: wt(1, s, k)
shot(None, 'L', [E('emoji', c('подорожало') - 0.2, x=-300, y=-250, ch='🏷️', size=140),
                 E('arrow', c('цены') - 0.2, x0=-180, y0=-200, x1=-120, y1=-300, w=12),
                 E('card', c('цены'), x=150, y=-250, text='PRICES GO UP', sz=52),
                 E('txt', c('аренду') - 0.2, x=0, y=-100, text="can't cover the basics? that's a different video", sz=30, col=(140, 140, 140)),
                 E('dark', c('выросла') - 0.3, x=0, y=60, text='THE PAYCHECK GREW,\nTHE ZERO STAYED', sz=50)],
     anim=['razgovor', 'kivok'])
ICONS = [('Телефон', '📱'), ('Доставка', '🛵'), ('Такси', '🚕'), ('Подписок', '📺'), ('Кофе', '☕')]
els = [E('plate', c('поменялось') - 0.3, x=0, y=-320, text='WHAT CHANGED FOR YOU?', sz=56)]
for k, (w, ch) in enumerate(ICONS):
    els.append(E('emoji', c(w) - 0.1, x=-440 + k * 220, y=-130, ch=ch, size=140))
els += [E('card', c('одна') - 0.3, x=0, y=60, text='NONE COSTS THE WHOLE RAISE', sz=42),
        E('plate', c('копейки') - 0.4, x=0, y=220, text='TOGETHER: EVERY LAST CENT', sz=66, rot=-2)]
shot(c('честно') - 0.2, 'L', els, anim=['razgovor-zhesty', 'obyasnyaet'])
shot(c('странное') - 0.2, 'L', [E('emoji', c('странное'), x=-260, y=-230, ch='🪙', size=150, gray=c('растворилось')),
                                E('card', c('решал'), x=150, y=-230, text='"I\'LL SPEND IT ON UBERS"', sz=42),
                                E('crossline', c('растворилось'), x=150, y=-230, w=480),
                                E('plate', c('инфляция') - 0.2, x=0, y=10, text='LIFESTYLE\nINFLATION', sz=78, rot=-2),
                                E('txt', c('всех') - 0.2, x=0, y=200, text='prices go up for everyone', sz=40),
                                E('dark', c('уровень') - 0.2, x=0, y=280, text='YOUR LIFESTYLE = + YOUR RAISE', sz=40)],
     anim=['cheshet-golovu', 'obyasnyaet'])
shot(c('ноль', 1) - 0.3, 'L', [E('red', c('ноль', 1) - 0.2, x=-280, y=-160, text='0 $', sz=70),
                            E('emoji', c('переезжает') - 0.2, x=-280, y=-20, ch='🧳', size=120),
                            E('arrow', c('переезжает'), x0=-160, y0=-100, x1=140, y1=-100, w=12),
                            E('emoji', c('квартиру') - 0.2, x=290, y=-120, ch='🏡', size=200),
                            E('plate', c('зачем') - 0.2, x=0, y=200, text='WHY?', sz=88, rot=2)],
     anim=['pozhimaet-plechami', 'cheshet-golovu'])

# ---------- 2. дыра 1: ты привыкаешь ----------
c = lambda s, k=0: wt(2, s, k)
shot(None, 'R', [E('emoji', c('Кайф') - 0.2, x=-300, y=-250, ch='🎉', size=150, gray=c('месяц')),
                 E('card', c('Неделю') - 0.1, x=120, y=-250, text="WEEK 1: I'M RICH", sz=42),
                 E('card', c('месяц') - 0.1, x=120, y=-130, text='MONTH 1: NORMAL', sz=42),
                 E('red', c('три') - 0.1, x=120, y=-10, text='MONTH 3: NOT ENOUGH', sz=42),
                 E('meter', c('Неделю'), x=0, y=200, label='JOY FROM THE RAISE', v0=0.95, v1=0.08, dur=c('три') - c('Неделю') + 0.5, col=YEL)],
     anim=['pryzhok', 'dyhanie', 'pozhimaet-plechami'])
shot(c('жадный') - 0.3, 'R', [E('card', c('жадный') - 0.2, x=0, y=-300, text='GREEDY', sz=50),
                              E('crossline', c('психологии'), x=0, y=-300, w=300),
                              E('plate', c('беговой') - 0.3, x=0, y=-120, text='THE HEDONIC\nTREADMILL', sz=66, rot=-2),
                              E('source', c('Термин') - 0.1, x=40, y=60, year='1971', name='BRICKMAN & CAMPBELL', ch='🏃'),
                              E('dark', c('нормой') - 0.4, x=0, y=220, text='UPGRADE → NEW NORMAL', sz=48)],
     anim=['net', 'obyasnyaet', 'ukazyvaet-vbok'])
shot(c('Поэтому') - 0.2, 'R', [E('emoji', c('телефон') - 0.2, x=-260, y=-200, ch='📱', size=170),
                               E('emoji', c('радует'), x=-150, y=-290, ch='❤️', size=80, gray=c('потом')),
                               E('card', c('платёж') - 0.2, x=180, y=-200, text='MONTHLY PAYMENT', sz=38),
                               E('red', c('Радость') - 0.1, x=0, y=60, text='THE JOY IS GONE,\nTHE BILL STAYS', sz=54, rot=-2)],
     anim=['net', 'razgovor'])
shot(c('бежишь') - 0.2, 'R', [E('emoji', c('бежишь') - 0.1, x=-200, y=-200, ch='🏃', size=170, bob=10),
                              E('plate', c('ускоряется') - 0.3, x=150, y=-200, text='THE TREADMILL\nSPEEDS UP', sz=54, rot=2),
                              ],
     anim=['shag', 'ukazyvaet-vbok'])
HOLE_T[0] = c('разгоняют') - 0.1
shot(c('Только') - 0.2, 'R', [E('bucket', c('Только') - 0.2, x=-40, y=80, sc=0.85, tags=(HOLE_T[0],)),
                          E('emoji', c('острове') - 0.2, x=330, y=-260, ch='🏝️', size=110),
                          E('plate', c('люди') - 0.3, x=0, y=300, text='WHO SPEEDS IT UP?', sz=56)],
     anim=['ukazyvaet-vverh'])

# ---------- 3. дыра 2: соседи ----------
c = lambda s, k=0: wt(3, s, k)
shot(None, 'L', [E('emoji', c('ездят') - 0.1, x=-300, y=-240, ch='🚗', size=140),
                 E('emoji', c('отдыхают') - 0.1, x=0, y=-240, ch='🏖️', size=140),
                 E('emoji', c('сторис') - 0.1, x=300, y=-240, ch='📲', size=140),
                 E('card', c('нужно') - 0.3, x=0, y=-40, text='"WHAT I NEED"', sz=50),
                 E('crossline', c('вокруг') - 0.4, x=0, y=-40, w=520),
                 E('plate', c('вокруг') - 0.2, x=0, y=150, text='"WHAT EVERYONE HAS"', sz=66, rot=-2)],
     anim=['razgovor', 'ukazyvaet-vbok'])
HOUSES = [-400, -200, 0, 200, 400]
els = [E('dark', c('исследование') - 0.3, c('Экономисты') - 0.3, x=0, y=-320, text='STUDY', sz=44),
       E('source', c('Экономисты') - 0.1, x=0, y=-320, year='2020', name='AGARWAL, MIKHED, SCHOLNICK', ch='🎟️')]
for k, hx in enumerate(HOUSES): els.append(E('emoji', c('провинции') - 0.3 + k * 0.08, x=hx, y=-60, ch='🏠', size=130))
els += [E('emoji', c('выиграл') - 0.1, x=0, y=-190, ch='💰', size=100),
        E('plate', c('чаще') - 0.2, x=0, y=170, text='NEIGHBORS GO BANKRUPT MORE', sz=58, rot=-2)]
shot(c('исследование') - 0.3, 'L', els, anim=['obyasnyaet', 'razgovor-zhesty'])
els = [E('emoji', c('Соседу') - 0.3, x=hx, y=-60, ch='🏠', size=130) for hx in HOUSES]
els += [E('emoji', c('Соседу') - 0.3, x=0, y=-190, ch='💰', size=100)]
for k, hx in enumerate([-400, -200, 200, 400]):
    els += [E('emoji', c('машина') - 0.2 + k * 0.1, x=hx, y=60, ch='🚗' if k % 2 else '🛠️', size=90),
            E('red', c('долги') - 0.2 + k * 0.1, x=hx, y=-190, text='DEBT', sz=36)]
els += [E('txt', c('Сэкономили') - 0.1, x=0, y=220, text='great deal', sz=46)]
shot(c('Соседу') - 0.3, 'L', els, anim=['ruki-v-boki', 'pozhimaet-plechami'])
shot(c('делаешь') - 0.2, 'L', [E('dark', c('делаешь') - 0.1, x=0, y=230, text='SAME THING, JUST SMALLER', sz=42),
                               E('emoji', c('море') - 0.3, x=-240, y=-200, ch='🌊', size=160),
                               E('card', c('Коллега') - 0.1, x=-240, y=-50, text='COWORKER: HAWAII', sz=40),
                               E('emoji', c('даче') - 0.3, x=240, y=-200, ch='🏡', size=150, gray=c('провал') - 0.3),
                               E('card', c('даче') - 0.2, x=240, y=-50, text='YOU: STAYCATION', sz=40),
                               E('red', c('провал') - 0.1, x=240, y=80, text='FAILURE?', sz=50, rot=4)],
     anim=['razgovor', 'pozhimaet-plechami'])
HOLE_T[1] = c('способ') - 0.1
shot(c('если') - 0.2, 'L', [E('bucket', c('если') - 0.2, x=-40, y=80, sc=0.85, tags=(HOLE_T[0] - 1e4, HOLE_T[1])),
                            E('plate', c('хитрая') - 0.2, x=0, y=300, text='BUY WITHOUT MONEY?', sz=56)],
     anim=['obyasnyaet', 'ukazyvaet-vverh'])

# ---------- 4. дыра 3: платить не больно ----------
c = lambda s, k=0: wt(4, s, k)
shot(None, 'R', [E('emoji', c('наличными') - 0.2, x=-260, y=-230, ch='💵', size=150),
                 E('red', c('больно') - 0.2, x=140, y=-230, text='STINGS A LITTLE', sz=44),
                 E('emoji', c('телефон') - 0.2, x=-260, y=-30, ch='📱', size=150),
                 E('card', c('больно', 1) - 0.3, x=140, y=-30, text="DOESN'T HURT AT ALL", sz=44),
                 E('plate', c('Пикнуло') - 0.1, x=0, y=180, text='BEEP!', sz=80, rot=-5)],
     anim=['razgovor', 'kivok'])
shot(c('году') - 0.8, 'R', [E('source', c('году') - 0.5, x=30, y=-320, year='2001', name='PRELEC & SIMESTER, MIT', ch='🏀'),
                            E('card', c('наличными', 1) - 0.2, x=-270, y=-170, text='CASH ONLY', sz=36),
                            E('card', c('картой') - 0.2, x=270, y=-170, text='CARD ONLY', sz=36),
                            E('bars', c('предлагали') - 0.2, x=0, y=250, maxh=230, bw=150, gap=250, items=(
                                ('cash', 0.42, GRAY, c('предлагали')), ('card', 0.88, RED, c('больше') - 0.2))),
                            E('txt', c('пересказам') - 0.3, x=0, y=-80, text='by some accounts, almost double', sz=32, col=(120, 120, 120))],
     anim=['obyasnyaet', 'ukazyvaet-vbok'])
shot(c('одни', 1) - 0.4, 'R', [E('emoji', c('Билеты', 1) - 0.1, x=-150, y=-220, ch='🎟️', size=140),
                            E('emoji', c('Билеты', 1) + 0.1, x=150, y=-220, ch='🎟️', size=140),
                            E('txt', c('одни', 1), x=0, y=-90, text='same tickets', sz=40),
                            E('plate', c('боли') - 0.4, x=0, y=100, text='YOU\'RE BUYING\n"NO PAIN"', sz=70, rot=-2)],
     anim=['razgovor', 'net'])
els = [E('card', c('тысячи') - 0.3, x=0, y=-270, text='"JUST 4 EASY PAYMENTS"', sz=48),
       E('txt', c('ничего') - 0.1, x=0, y=-160, text='sounds like nothing', sz=40)]
for k in range(6):
    els.append(E('card', c('шесть') - 0.6 + k * 0.12, x=-320 + (k % 3) * 320, y=-20 + (k // 3) * 110, text='4 × $25', sz=34, rot=(k * 5) % 7 - 3))
shot(c('рассрочка') - 0.2, 'R', els, anim=['razgovor-zhesty', 'pozhimaet-plechami'])
shot(c('Кредит') - 0.2, 'R', [E('card', c('Кредит') - 0.1, x=-300, y=-240, text='ME NOW', sz=44),
                              E('arrow', c('будущим') - 0.3, x0=-160, y0=-240, x1=160, y1=-240, w=12),
                              E('dark', c('будущим') - 0.1, x=300, y=-240, text='FUTURE ME', sz=44),
                              E('emoji', c('заплатит', 1) - 0.2, x=0, y=-140, ch='🧾', size=100),
                              E('card', c('получает') - 0.2, x=300, y=-60, text='+ RAISE', sz=40),
                              E('arrow', c('банку') - 0.4, x0=300, y0=-10, x1=300, y1=110, w=12),
                              E('emoji', c('банку') - 0.2, x=300, y=180, ch='🏦', size=130),
                              E('plate', c('подвох') - 0.3, x=-230, y=140, text="HERE'S THE CATCH", sz=54, rot=-3)],
     anim=['net', 'cheshet-golovu', 'ruki-v-boki'])
HOLE_T[2] = c('Три') - 0.1
shot(c('Три') - 0.3, 'R', [E('bucket', c('Три') - 0.3, x=-40, y=80, sc=0.85, tags=(-1e4, -1e4, HOLE_T[2]), glow=c('четвёртая') - 0.1),
                           E('plate', c('интересное') - 0.2, x=0, y=300, text='THE BIG HOLE IS NEXT', sz=54)],
     anim=['ruki-v-boki', 'ukazyvaet-vbok'])

# ---------- 5. дыра 4: «я заслужил» ----------
c = lambda s, k=0: wt(5, s, k)
els = []
for k, (w, ch, tx) in enumerate([('еду', '🍔', 'ROUGH WEEK'), ('кроссовки', '👟', 'FINISHED A PROJECT'), ('отметить', '🥂', 'GOT A RAISE')]):
    y = -250 + k * 150
    els += [E('card', c(w) - 0.9, x=-200, y=y, text=tx, sz=38), E('emoji', c(w) - 0.2, x=120, y=y, ch=ch, size=110),
            E('plate', c(w), x=300, y=y, text='🏅 EARNED IT' if False else 'EARNED IT', sz=32, rot=-4)]
els += [E('txt', c('разумно') - 0.2, x=0, y=200, text='every purchase sounds reasonable', sz=40)]
shot(None, 'L', els, anim=['razgovor', 'kivok'])
shot(c('заметь') - 0.2, 'L', [E('meter', c('зарплатой') - 0.3, x=0, y=-240, label='PAYCHECK', v0=0.3, v1=0.75, dur=2.0, col=GREEN),
                              E('meter', c('поводов') - 0.3, x=0, y=-90, label='REASONS TO TREAT YOURSELF', v0=0.3, v1=0.85, dur=2.0, col=RED),
                              E('emoji', c('колесо') - 0.3, x=0, y=110, ch='🐹', size=130, bob=6),
                              E('card', c('покупать') - 0.3, x=-300, y=110, text='YOU WORK', sz=36),
                              E('arrow', c('покупать') - 0.1, x0=-160, y0=180, x1=160, y1=180),
                              E('card', c('Покупаешь') - 0.2, x=300, y=110, text='YOU BUY', sz=36),
                              E('arrow', c('терпеть') - 0.2, x0=160, y0=240, x1=-160, y1=240)],
     anim=['obyasnyaet', 'shag', 'razgovor-zhesty'])
shot(c('говорю') - 0.4, 'L', [E('card', c('говорю'), x=0, y=-250, text='"NEVER TREAT YOURSELF"', sz=50),
                              E('crossline', c('Радуй', 1) - 0.1, x=0, y=-250, w=480),
                              E('plate', c('Радуй', 1), x=0, y=-120, text='TREAT YOURSELF', sz=60, rot=2),
                              E('emoji', c('спроси') - 0.1, x=-200, y=80, ch='⏳', size=130),
                              E('txt', c('вспомнишь') - 0.3, x=120, y=80, text='what will you remember\nin a week?', sz=40)],
     anim=['razgovor', 'dyhanie'])
HOLE_T[3] = c('заслужил', 1) - 0.1
shot(c('Итак') - 0.2, 'L', [E('bucket', c('Итак') - 0.2, x=-40, y=80, sc=0.85, tags=(c('Привычка') - 0.05, c('Соседи') - 0.05, c('Оплата') - 0.05, HOLE_T[3]), glow=-1e4),
                            E('plate', c('общего') - 0.3, x=0, y=300, text='WHAT DO THEY HAVE IN COMMON?', sz=56)],
     anim=['ukazyvaet-vverh', 'cheshet-golovu'])
shot(c('одна') - 0.4, 'L', [E('card', c('одна') - 0.2, x=0, y=-260, text='NOT ABOUT "NEED"', sz=50),
                            E('crossline', c('нужно') + 0.1, x=0, y=-260, w=440),
                            E('dark', c('чувствуешь') - 0.3, x=0, y=-120, text='ABOUT HOW YOU FEEL', sz=44),
                            E('dark', c('видят') - 0.3, x=0, y=0, text='ABOUT HOW OTHERS SEE YOU', sz=44),
                            E('plate', c('главный') - 0.2, x=0, y=190, text='THE REAL ANSWER', sz=66, rot=-2)],
     anim=['net', 'obyasnyaet'])

# ---------- 6. где деньги (вау) ----------
c = lambda s, k=0: wt(6, s, k)
shot(None, 'R', [E('txt', c('пропали') - 0.3, x=0, y=-310, text="the money didn't disappear", sz=44),
                 E('plate', c('ощущение') - 0.2, x=0, y=-150, text='YOU BOUGHT THE FEELING\nOF HAVING MORE', sz=64, rot=-2),
                 E('card', c('жить') - 0.2, x=0, y=60, text="LIVE LIKE YOU'RE RICH", sz=48),
                 E('red', c('стать') - 0.3, x=0, y=180, text='INSTEAD OF GETTING RICHER', sz=48, rot=2)],
     anim=['obyasnyaet', 'dyhanie', 'razgovor'])
shot(c('Морган') - 0.2, 'R', [E('source', c('Морган') - 0.1, x=40, y=-320, year='2020', name='MORGAN HOUSEL, "THE PSYCHOLOGY OF MONEY"', ch='📕'),
                              E('plate', c('богатство') - 0.2, x=0, y=-160, text="WEALTH IS WHAT\nYOU DON'T SEE", sz=66, rot=-2),
                              E('emoji', c('Машина') - 0.1, x=-300, y=60, ch='🚗', size=130, gray=c('купил', 1) - 0.1),
                              E('txt', c('купил', 1), x=-300, y=160, text="didn't buy", sz=34),
                              E('emoji', c('Отпуск') - 0.1, x=0, y=60, ch='✈️', size=130, gray=c('полетел') - 0.1),
                              E('txt', c('полетел'), x=0, y=160, text="didn't fly", sz=34),
                              E('emoji', c('лежат') - 0.3, x=300, y=60, ch='💰', size=130),
                              E('txt', c('молчат') - 0.1, x=300, y=160, text='sits there quietly', sz=34)],
     anim=['ukazyvaet-vverh', 'razgovor'])
shot(c('девяностых') - 0.4, 'R', [E('source', c('девяностых') - 0.2, x=40, y=-320, year='1996', name='STANLEY & DANKO', ch='🏠'),
                                  E('emoji', c('скромно') - 0.2, x=-250, y=-120, ch='🏠', size=150),
                                  E('card', c('показухи') - 0.3, x=-250, y=40, text='SAVINGS ✓', sz=40),
                                  E('emoji', c('новыми') - 0.2, x=250, y=-120, ch='🏰', size=170),
                                  E('red', c('накоплений') - 0.2, x=250, y=40, text='NO SAVINGS', sz=40)],
     anim=['razgovor-zhesty', 'obyasnyaet'])
shot(c('стороны') - 0.3, 'R', [E('card', c('беднее') - 0.4, x=0, y=-260, text='THE RICH LOOK POORER', sz=44),
                               E('card', c('бедные') - 0.1, x=0, y=-150, text='THE POOR LOOK RICHER', sz=44),
                               E('dark', c('Видно', 1) - 0.1, x=0, y=0, text='YOU SEE WHAT WAS SPENT', sz=50),
                               E('txt', c('богатство', 1) + 0.1, x=0, y=130, text='wealth is invisible', sz=42)],
     anim=['ruki-v-boki', 'kivok'])
shot(c('поворот') - 0.4, 'R', [E('txt', c('поворот') - 0.3, x=0, y=-260, text="here's the twist", sz=44),
                               E('plate', c('перестать') - 0.4, x=0, y=-60, text='TO GET RICHER,\nSTOP LOOKING\nRICHER', sz=70, rot=-2)],
     anim=['kivok', 'ruki-v-boki'])
shot(c('работают') - 1.2, 'R', [E('emoji', c('Силой') - 0.2, x=-250, y=-220, ch='🏋️', size=150),
                                E('card', c('Силой') - 0.1, x=150, y=-220, text='WILLPOWER?', sz=48),
                                E('strike', c('Нет') - 0.1, x=-250, y=-220, w=170, h=170),
                                E('red', c('тяжёлая') - 0.3, x=0, y=-40, text='THE FIRST ROUGH WEEK', sz=46),
                                E('plate', c('съест') - 0.2, x=0, y=170, text='THEN HOW?', sz=80, rot=2)],
     anim=['net', 'pozhimaet-plechami'])

# ---------- 7. правило половины ----------
c = lambda s, k=0: wt(7, s, k)
shot(None, 'L', [E('card', c('исчезала') - 0.3, x=0, y=-270, text="THE RAISE DISAPPEARS BEFORE IT'S A HABIT", sz=42),
                 E('emoji', c('магазине') - 0.3, x=-220, y=-60, ch='🛒', size=150),
                 E('strike', c('магазине'), x=-220, y=-60, w=170, h=170),
                 E('emoji', c('счёте') - 0.3, x=220, y=-60, ch='🏦', size=150),
                 E('check', c('счёте'), x=320, y=40, s=60)],
     anim=['obyasnyaet', 'kivok'])
shot(c('Экономисты') - 0.2, 'L', [E('source', c('Экономисты') - 0.1, x=40, y=-320, year='2004', name='THALER & BENARTZI', ch='🏅'),
                                  E('plate', c('Сохраняй') - 0.3, x=0, y=-170, text='"SAVE MORE\nTOMORROW"', sz=64, rot=-2),
                                  E('red', c('больно') - 0.4, x=0, y=10, text='SAVING NOW HURTS', sz=40),
                                  E('crossline', c('больно') + 0.1, x=0, y=10, w=640),
                                  E('card', c('часть') - 0.3, x=0, y=140, text='NEXT RAISE: PART GOES TO SAVINGS', sz=40),
                                  E('check', c('накопления') - 0.2, x=-470, y=140, s=50)],
     anim=['obyasnyaet', 'ukazyvaet-vverh', 'razgovor'])
shot(c('Большинство') - 0.2, 'L', [E('card', c('Большинство') - 0.1, x=0, y=-310, text='MOST SAID YES', sz=44),
                                   E('bars', c('откладывали') - 0.3, x=0, y=230, maxh=320, bw=170, gap=230, items=(
                                       ('at the start', 0.22, GRAY, c('откладывали') - 0.3), ('≈ 3 years later', 0.88, YEL, c('четыре') - 0.2))),
                                   E('plate', c('раза') - 0.1, x=220, y=-150, text='ALMOST ×4', sz=60, rot=-4)],
     anim=['ukazyvaet-vverh', 'pryzhok'])
shot(c('Почему') - 0.2, 'L', [E('txt', c('Почему') - 0.1, x=0, y=-350, text='why does it work?', sz=40),
                              E('card', c('есть') - 0.3, x=0, y=-250, text='MONEY YOU ALREADY HAVE', sz=44),
                              E('crossline', c('есть') + 0.2, x=0, y=-250, w=640),
                              E('dark', c('привык', 1) - 0.4, x=0, y=-110, text="MONEY YOU'RE NOT USED TO", sz=44),
                              E('plate', c('жалко') - 0.2, x=0, y=60, text="DOESN'T HURT", sz=80, rot=-2)],
     anim=['razgovor', 'kivok'])
shot(c('правило') - 0.3, 'L', [E('bucket', c('правило') - 0.3, x=-120, y=90, sc=0.8, tags=(), mine=c('пополам') - 0.2),
                               E('plate', c('пополам') - 0.3, x=0, y=330, text='SPLIT IT IN HALF', sz=66, rot=-2)],
     anim=['razgovor-zhesty', 'obyasnyaet'])
shot(c('после') - 0.6, 'L', [E('card', c('после') - 0.2, x=-220, y=-200, text='AFTER', sz=50),
                             E('crossline', c('после') + 0.1, x=-220, y=-200, w=260),
                             E('card', c('останется') - 0.4, x=220, y=-200, text='"IF THERE\'S ANY LEFT"', sz=44),
                             E('crossline', c('останется'), x=220, y=-200, w=440),
                             E('plate', c('зарплаты', 1) - 0.4, x=0, y=20, text='ON PAYDAY', sz=84, rot=-2)],
     anim=['net', 'ukazyvaet-vverh'])
shot(c('вообще') - 0.6, 'L', [E('txt', c('вообще') - 0.4, x=0, y=-320, text="wait, that's allowed?", sz=40),
                              E('emoji', c('подушкой') - 0.3, x=-230, y=-170, ch='🛏️', size=150),
                              E('card', c('подушкой') - 0.2, x=170, y=-170, text='ACCOUNT = EMERGENCY FUND', sz=44),
                              E('red', c('страх') - 0.3, x=0, y=-20, text='NO FUND = WORKING OUT OF FEAR', sz=40),
                              E('plate', c('право') - 0.2, x=0, y=130, text='THE RIGHT TO SAY "NO"', sz=62, rot=-2),
                              E('txt', c('совет') - 0.3, x=0, y=280, text='not investment advice', sz=30, col=(140, 140, 140))],
     anim=['pryzhok', 'dyhanie', 'razgovor'])

# ---------- 8. финал ----------
c = lambda s, k=0: wt(8, s, k)
els = [E('plate', c('Итак') - 0.1, x=0, y=-330, text="WHERE'S THE MONEY", sz=50)]
for k, (w, tx) in enumerate([('привычка', 'HABIT'), ('соседи', 'THE NEIGHBORS'), ('боли', 'PAINLESS PAYMENTS'), ('заслужил', '"I DESERVE IT"')]):
    y = -220 + k * 95; ta = c(w) - 0.2
    els += [E('check', ta + 0.15, x=-300, y=y, s=44), E('card', ta, x=40, y=y, text=tx, sz=36)]
els += [E('dark', c('ощущение') - 0.3, x=0, y=180, text='= THE FEELING OF BEING RICHER', sz=42)]
shot(None, 'R', els, anim=['razgovor', 'kivok'])
shot(c('План') - 0.2, 'R', [E('plate', c('План') - 0.1, x=0, y=-330, text='YOUR PLAN FOR TODAY', sz=66),
                            E('card', c('автоперевод') - 0.3, x=0, y=-200, text='1.  AUTO TRANSFER ON PAYDAY', sz=38),
                            E('txt', c('пятьсот') - 0.2, x=0, y=-110, text='even $25', sz=40),
                            E('card', c('половину') - 0.3, x=0, y=-10, text='2.  NEXT RAISE → HALF GOES THERE', sz=38),
                            E('emoji', c('комментариях') - 0.2, x=-280, y=170, ch='💬', size=120),
                            E('card', c('комментариях'), x=90, y=170, text='WHICH HOLE IS YOUR BIGGEST?', sz=36)],
     anim=['ukazyvaet-vverh', 'obyasnyaet', 'mashet'])
TRING = c('следующий') - 0.3
shot(TRING, 'C', [E('phone', TRING, c('тупи') - 0.3, x=-540, y=40, text='0 $', t2=c('ноль') - 0.1, text2='NOT ZERO', sz=76),
                  E('plate', c('тупи') - 0.6, x=0, y=-360, text="THAT'S IT. DON'T BE DUMB.", sz=90, rot=-3)],
     anim=['kivok', 'dyhanie'], s=0.78)

# акцентные наезды (не чаще раза в минуту)
PUNCH = [wt(0, 'Ноль'), wt(1, 'копейки'), wt(2, 'нормой'), wt(3, 'чаще'), wt(4, 'вдвое'), wt(4, 'главная'),
         wt(6, 'ощущение'), wt(6, 'перестать'), wt(7, 'пополам'), wt(8, 'Всё', 1) if False else wt(8, 'тупи') - 0.6]
# тишина в музыке (секунда) на трёх откровениях
SILENCE = [wt(0, 'Ноль') - 0.1, wt(6, 'всё') - 0.2, wt(7, 'зарплаты', 1) - 0.3]
HUD_ON = wt(0, 'поднимали'); HUD_OK = wt(8, 'ноль')
HOLES_ON = wt(0, 'четыре')

_ch = 0
for sh in SHOTS:
    if sh['t'] is None:
        _ch += 1; sh['t'] = O[_ch] - GAP
bad = [(a['t'], b['t'], b['els'][0][:2]) for a, b in zip(SHOTS, SHOTS[1:]) if not a['t'] < b['t']]
assert not bad, bad
