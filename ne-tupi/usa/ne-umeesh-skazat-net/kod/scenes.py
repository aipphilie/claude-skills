"""Сцены ролика «Почему ты всем говоришь "да"». Координаты элементов — относительно центра графики шота."""
from tl import wt, O, GAP, END, NCH
from gfx import YEL, RED, INK, WHITE, GRAY, GREEN
SHOTS = []
def E(kind, ta, te=None, **kw): return (kind, ta, te, kw)
def shot(t, side, els, anim=(), s=0.72, bg=None):
    SHOTS.append(dict(t=t, side=side, s=s, anim=list(anim), els=els, bg=bg))
TOWER = ['"JUST AN HOUR"', 'HELP ME MOVE', "SOMEONE'S BIRTHDAY", 'SATURDAY SHIFT', 'LOAN'][::-1]

# ---------- 0. холодный старт ----------
c = lambda s, k=0: wt(0, s, k)
shot(0, 'L', [E('boxes', 0.0, x=-440, y=400, labels=tuple(TOWER), w=290, h=88, sz=30),
              E('card', c('неделю'), x=180, y=-320, text='IN ONE WEEK', sz=52),
              E('emoji', c('одолжил'), x=-30, y=-120, ch='💸', size=160),
              E('emoji', c('выходной'), x=200, y=-120, ch='🏢', size=160),
              E('emoji', c('рождения'), x=430, y=-120, ch='🎂', size=160),
              E('dark', c('хотел'), x=200, y=60, text="DIDN'T EVEN WANT TO GO", sz=44)],
     anim=['pozhimaet-plechami', 'razgovor'])
shot(c('каждый') - 0.2, 'R', [E('emoji', c('голове'), x=0, y=-280, ch='🧠', size=150),
                              E('cloud', c('ладно'), x=0, y=40, text="EH, IT'S FINE,\nDON'T BE RUDE…", w=520, sz=58)],
     anim=['dyhanie', 'cheshet-golovu'])
shot(c('Стоп') - 0.2, 'L', [E('plate', c('Стоп') - 0.05, x=0, y=-250, text="STOP.\nYOU'RE BEING DUMB", sz=84, rot=-3),
                            E('card', c('кредит') - 0.4, c('ладно', 1) - 0.1, x=0, y=60, text='"I\'LL PUT IT ON THE CARD"', sz=54),
                            E('crossline', c('Это', 1) - 0.1, c('ладно', 1) - 0.1, x=0, y=60, w=600),
                            E('red', c('Самая'), x=0, y=300, text='THE MOST EXPENSIVE PHRASE', sz=46, rot=2),
                            E('plate', c('ладно', 1), x=0, y=70, text="EH,\nIT'S FINE", sz=96, rot=2)],
     anim=['ukazyvaet-vverh', 'net'], s=0.76)
shot(c('десять') - 0.2, 'R', [E('card', c('стоит'), x=0, y=-300, text='WHAT IT COSTS', sz=50),
                              E('dark', c('страшно'), x=0, y=-170, text='WHY NO IS SCARY', sz=44),
                              E('flash', c('три') - 0.1, x=0, y=60, text='3 PHRASES TO SAY NO'),
                              E('plate', c('оправданий') - 0.3, x=0, y=220, text='"NO" WITHOUT EXCUSES', sz=60, rot=-2)],
     anim=['obyasnyaet', 'mashet'])

# ---------- 1. почему «нет» страшно ----------
c = lambda s, k=0: wt(1, s, k)
shot(None, 'L', [E('emoji', c('просят'), x=-280, y=-260, ch='🙏', size=160),
                 E('card', c('отказать'), x=150, y=-260, text='YOU WANT TO SAY NO', sz=50),
                 E('emoji', c('Сердце'), x=-280, y=-40, ch='❤️', size=150, bob=12),
                 E('card', c('горле'), x=150, y=-40, text='LUMP IN YOUR THROAT', sz=50),
                 E('cloud', c('конечно') - 0.3, x=0, y=220, text='"YEAH, OF COURSE"', w=480, sz=50)],
     anim=['razgovor', 'cheshet-golovu'])
shot(c('слабый') - 0.2, 'R', [E('card', c('слабый'), x=0, y=-180, text='WEAK PERSONALITY', sz=60),
                              E('crossline', c('старая') - 0.2, x=0, y=-180, w=620),
                              E('plate', c('программа'), x=0, y=60, text='OLD SOFTWARE', sz=80, rot=-2)],
     anim=['net', 'obyasnyaet'])
shot(c('Тысячи') - 0.2, 'C', [E('emoji', c('Тысячи'), x=-560, y=-190, ch='🔥', size=150),
                              E('card', c('группе'), x=-560, y=-20, text='SURVIVAL = THE GROUP', sz=36),
                              E('red', c('Выгнали'), x=560, y=-190, text='KICKED OUT OF THE TRIBE', sz=44, rot=3),
                              E('emoji', c('лесу'), x=560, y=-20, ch='🌲', size=160),
                              E('plate', c('недовольство'), x=0, y=-340, text='DISAPPROVAL = DANGER', sz=56)],
     anim=['obyasnyaet', 'razgovor-zhesty'], s=0.76)
shot(c('известном') - 0.2, 'L', [E('dark', c('известном'), x=0, y=-330, text='A WELL-KNOWN EXPERIMENT', sz=42),
                                 E('emoji', c('мяч'), x=-250, y=-160, ch='⚽', size=150),
                                 E('card', c('выключали'), x=150, y=-160, text='LEFT OUT OF THE GAME', sz=44),
                                 E('txt', c('Пустяк'), x=0, y=-20, text='a tiny thing, cartoon players', sz=40),
                                 E('emoji', c('мозг', 1), x=-200, y=150, ch='🧠', size=160),
                                 E('red', c('боль') - 0.2, x=140, y=150, text='LIKE PAIN', sz=60, rot=-3)],
     anim=['ukazyvaet-vbok', 'razgovor'])
shot(c('отказываешь') - 0.2, 'R', [E('card', c('субботу'), x=0, y=-300, text='"COVER MY SATURDAY?"', sz=48),
                                   E('plate', c('орёт'), x=-200, y=-150, text='AAAH!', sz=70, rot=-6),
                                   E('emoji', c('пещеры'), x=-180, y=100, ch='🪨', size=170),
                                   E('emoji', c('тигру') - 0.2, x=180, y=100, ch='🐅', size=200)],
     anim=['pryzhok', 'net'])
shot(c('пещеры', 1) - 0.2, 'L', [E('emoji', c('пещеры', 1), x=-250, y=-280, ch='🐅', size=140),
                                 E('strike', c('давно'), x=-250, y=-280, w=150, h=150),
                                 E('card', c('съест'), x=150, y=-280, text="YOUR COWORKER WON'T EAT YOU", sz=44),
                                 E('meter', c('Опасность'), x=0, y=-40, label='DANGER IN YOUR HEAD', v1=0.97, dur=0.8),
                                 E('meter', c('жизни'), x=0, y=140, label='DANGER IN REAL LIFE', v1=0.08, dur=0.6, col=GREEN)],
     anim=['pozhimaet-plechami', 'obyasnyaet'])
shot(c('Зато') - 0.2, 'R', [E('card', c('бесплатным') - 0.3, x=0, y=-250, text='"YES" = FREE?', sz=60),
                            E('txt', c('помог'), x=0, y=-110, text='you just helped someone out…', sz=44),
                            E('plate', c('стоило') - 0.3, x=0, y=80, text='WHAT DID THAT\n"YES" COST?', sz=72)],
     anim=['razgovor', 'cheshet-golovu'])

# ---------- 2. сколько стоит «неудобно» ----------
c = lambda s, k=0: wt(2, s, k)
shot(None, 'L', [E('plate', c('Первое'), x=0, y=-340, text='1.  MONEY', sz=64),
                 E('emoji', c('Одолжил'), x=-260, y=-150, ch='💸', size=170),
                 E('card', c('полгода'), x=150, y=-150, text='PAID BACK 6 MONTHS LATER', sz=40),
                 E('dark', c('напомнить'), x=0, y=40, text='AWKWARD TO REMIND THEM', sz=46, rot=-2)],
     anim=['obyasnyaet', 'pozhimaet-plechami'])
shot(c('Скинулся') - 0.2, 'R', [E('emoji', c('подарок'), x=-230, y=-230, ch='🎁', size=170),
                                E('card', c('видел'), x=-230, y=-60, text='MET TWICE', sz=40),
                                E('emoji', c('косметику'), x=230, y=-230, ch='💄', size=170),
                                E('card', c('начинает') - 0.3, x=230, y=-60, text='"SHE\'S JUST\nGETTING STARTED"', sz=40)],
     anim=['razgovor-zhesty'])
shot(c('Второе') - 0.2, 'L', [E('plate', c('Второе'), x=0, y=-340, text='2.  TIME', sz=64),
                              E('emoji', c('Час'), x=-300, y=-160, ch='⏰', size=140),
                              E('card', c('быстрый'), x=120, y=-160, text='"QUICK QUESTION" = 1 HOUR', sz=40),
                              E('emoji', c('переезд'), x=-300, y=10, ch='📦', size=140),
                              E('card', c('переезд'), x=120, y=10, text='AN EVENING HELPING MOVE', sz=40),
                              E('red', c('свободен') - 0.3, x=40, y=190, text='"WELL, YOU\'RE FREE ANYWAY"', sz=40, rot=-2)],
     anim=['razgovor', 'ukazyvaet-vbok'])
shot(c('Третье') - 0.2, 'R', [E('plate', c('Третье'), x=0, y=-340, text='3.  ENERGY', sz=64),
                              E('battery', c('Третье'), x=0, y=-120, l0=0.9, l1=0.04, dur=2.5),
                              E('red', c('себя') - 0.2, x=0, y=170, text='ANGRY AT YOURSELF', sz=56, rot=3)],
     anim=['dyhanie', 'pozhimaet-plechami'])
shot(c('коварное') - 0.2, 'L', [E('plate', c('коварное') - 0.2, x=0, y=-340, text='ONE "YES" PULLS THE NEXT', sz=46),
                                E('dark', c('шестидесятых'), x=0, y=-235, text='A 1960s EXPERIMENT', sz=36),
                                E('card', c('наклейку') - 0.3, x=-230, y=-110, text='TINY\nSTICKER', sz=40),
                                E('arrow', c('недель'), x0=-60, y0=-110, x1=60, y1=-110),
                                E('card', c('плакат') - 0.3, x=230, y=-110, text='HUGE\nSIGN', sz=40),
                                E('bars', c('согласился') - 0.2, x=0, y=250, maxh=170, bw=150, gap=140, items=(
                                    ('no tiny ask', 0.25, GRAY, c('согласился')), ('after the tiny ask', 0.95, RED, c('чаще'))))],
     anim=['obyasnyaet', 'ukazyvaet-vverh'])
shot(c('выручит') - 0.6, 'R', [E('plate', c('выручит') - 0.4, x=0, y=-320, text='"ALWAYS HELPS OUT"', sz=60, rot=-2),
                               E('txt', c('родился'), x=0, y=-190, text='not born that way', sz=44),
                               E('boxes', c('натренировали'), x=0, y=330, labels=('"YES"',) * 5, w=200, h=70, sz=30)],
     anim=['razgovor-zhesty', 'kivok'])
shot(c('деньги', 1) - 0.2, 'L', [E('card', c('деньги', 1), x=0, y=-200, text='MONEY AND TIME COME BACK', sz=44),
                                 E('plate', c('цена'), x=0, y=40, text="THE PRICE\nYOU DON'T SEE", sz=76, rot=-2)],
     anim=['ukazyvaet-vverh', 'cheshet-golovu'])

# ---------- 3. твоё «да» = «нет» себе ----------
c = lambda s, k=0: wt(3, s, k)
shot(None, 'R', [E('emoji', c('сутках'), x=0, y=-260, ch='🕐', size=170),
                 E('card', c('всех'), x=0, y=-90, text='24 HOURS, LIKE EVERYONE', sz=50),
                 E('plate', c('автоматически') - 0.3, x=0, y=120, text='"YES" TO SOMEONE =\n"NO" TO SOMETHING', sz=68, rot=-2)],
     anim=['obyasnyaet', 'razgovor'])
ROWS = [('начальнику', 'спортзалу', 'YES TO THE BOSS', 'NO TO THE GYM'), ('встрече', 'сну', 'YES TO HANGOUT #3', 'NO TO SLEEP'),
        ('подруге', 'проекту', 'YES TO A FRIEND', 'NO TO YOUR PROJECT')]
els = []
for k, (a, b, ta_, tb_) in enumerate(ROWS):
    y = -250 + k * 170
    els += [E('card', c(a) - 0.2, x=-330, y=y, text=ta_, sz=40), E('arrow', c(b) - 0.5, x0=-115, y0=y, x1=-5, y1=y),
            E('red', c(b) - 0.1, x=280, y=y, text=tb_, sz=40)]
shot(c('Сказал') - 0.2, 'L', els, anim=['razgovor-zhesty', 'net', 'razgovor-zhesty'])
shot(c('парадокс') - 0.3, 'R', [E('card', c('помогаешь'), x=0, y=-340, text='YOU HELP EVERYONE', sz=40),
                                E('red', c('времени'), x=0, y=-245, text='NO TIME FOR YOU', sz=36),
                                E('emoji', c('банкомат'), x=0, y=-60, ch='🏧', size=220),
                                E('plate', c('пин'), x=0, y=150, text='NO PIN', sz=70, rot=-3),
                                E('txt', c('снимай'), x=0, y=280, text='take as much as you want', sz=40)],
     anim=['ruki-v-boki', 'pozhimaet-plechami'])
shot(c('цена') - 0.2, 'L', [E('card', c('Снаружи'), x=0, y=-320, text='OUTSIDE: NICE AND EASY', sz=42),
                            E('meter', c('копится') - 0.3, x=0, y=-140, label='INSIDE: RESENTMENT', v0=0.1, v1=1.0, dur=2.5),
                            E('emoji', c('чашки') - 0.3, x=-160, y=70, ch='☕', size=150),
                            E('emoji', c('срываешься'), x=150, y=70, ch='💥', size=170),
                            E('dark', c('чашке') - 0.5, x=0, y=250, text='NOT ABOUT THE MUG', sz=50)],
     anim=['obyasnyaet', 'net'])
shot(c('Ладно') - 0.2, 'R', [E('cloud', c('откажу'), x=0, y=-220, text='WHAT IF THEY\nGET OFFENDED?', w=460, sz=54),
                             E('plate', c('проверим'), x=0, y=40, text="LET'S CHECK", sz=76, rot=-3),
                             E('dark', c('фразы'), x=0, y=210, text='3 PHRASES: COMING UP', sz=44)],
     anim=['cheshet-golovu', 'kivok'])

# ---------- 4. обижаются меньше ----------
c = lambda s, k=0: wt(4, s, k)
shot(None, 'L', [E('dark', c('серию'), x=0, y=-330, text='A SERIES OF EXPERIMENTS', sz=40),
                 E('emoji', c('отказываются'), x=-230, y=-160, ch='🙅', size=150),
                 E('card', c('отказываются'), x=-230, y=0, text='YOU SAY NO', sz=40),
                 E('emoji', c('отказали'), x=230, y=-160, ch='🤷', size=150),
                 E('card', c('отказали'), x=230, y=0, text='YOU GET A NO', sz=40)],
     anim=['obyasnyaet', 'razgovor'])
shot(c('уверены') - 0.3, 'R', [E('emoji', c('обидятся'), x=-300, y=-300, ch='😢', size=110),
                               E('emoji', c('разозлятся'), x=-140, y=-300, ch='😠', size=110),
                               E('emoji', c('позовут'), x=20, y=-300, ch='🚪', size=110),
                               E('bars', c('уверены'), x=0, y=160, maxh=280, bw=170, gap=150, items=(
                                   ('expected\nhurt', 0.95, RED, c('обидятся')), ('actually\nhurt', 0.25, GREEN, c('спокойнее') - 0.3))),
                               E('txt', c('бывает'), x=0, y=320, text='"couldn\'t make it, it happens"', sz=38)],
     anim=['razgovor', 'kivok'])
shot(c('Твоё') - 0.2, 'L', [E('emoji', c('чужой'), x=-240, y=-200, ch='⏱️', size=150),
                            E('card', c('минуту'), x=-240, y=-30, text='THEM: A MINUTE', sz=46),
                            E('emoji', c('неделю') - 0.4, x=240, y=-200, ch='⏳', size=150),
                            E('red', c('неделю'), x=240, y=-30, text='YOU: A WEEK', sz=46, rot=3)],
     anim=['net', 'razgovor-zhesty'])
shot(c('ловушка') - 0.2, 'C', [E('emoji', c('прожектора') - 0.4, x=-560, y=-290, ch='🔦', size=140),
                               E('plate', c('прожектора'), x=-560, y=-130, text='THE SPOTLIGHT\nEFFECT', sz=50),
                               E('cloud', c('смотрят'), x=560, y=-260, text="EVERYONE'S\nWATCHING ME", w=400, sz=42),
                               E('dark', c('заняты'), x=560, y=-20, text='PEOPLE ARE BUSY WITH THEMSELVES', sz=40),
                               E('emoji', c('сном'), x=-560, y=60, ch='😴', size=130)],
     anim=['ukazyvaet-vverh', 'obyasnyaet'], s=0.76)
shot(c('неприятная') - 0.2, 'R', [E('dark', c('неприятная'), x=0, y=-330, text='THE UNCOMFORTABLE TRUTH', sz=42),
                                  E('card', c('обижается'), x=0, y=-190, text='WHO GETS THE MOST UPSET?', sz=42),
                                  E('red', c('удобно') - 0.2, x=0, y=-40, text='THOSE WHO LIKED YOUR "YES"', sz=50, rot=-2),
                                  E('plate', c('фильтр') - 0.1, x=0, y=150, text="IT'S A FILTER", sz=84, rot=2)],
     anim=['razgovor-zhesty', 'ukazyvaet-vverh'])
shot(c('Если') - 0.2, 'L', [E('emoji', c('держатся'), x=0, y=-250, ch='🤝', size=170),
                            E('card', c('дружба') - 0.4, x=0, y=-50, text='FRIENDSHIP', sz=70),
                            E('strike', c('дружба'), x=0, y=-50, w=380, h=110),
                            E('red', c('обслуживание') - 0.2, x=0, y=150, text='CUSTOMER SERVICE', sz=80, rot=-3)],
     anim=['net', 'ruki-v-boki'])
shot(c('Хорошо') - 0.2, 'R', [E('plate', c('грубо') - 0.5, x=0, y=-160, text='HOW TO SAY NO\nWITHOUT BEING RUDE?', sz=76),
                              E('dark', c('ошибку') - 0.3, x=0, y=100, text='ALMOST EVERYONE MAKES ONE MISTAKE', sz=38)],
     anim=['cheshet-golovu'])

# ---------- 5. отказ без оправданий ----------
c = lambda s, k=0: wt(5, s, k)
shot(None, 'L', [E('red', c('оправдываться') - 0.3, x=0, y=-330, text='MISTAKE: MAKING EXCUSES', sz=46),
                 E('emoji', c('бабушка'), x=-280, y=-130, ch='👵', size=150),
                 E('emoji', c('кот'), x=0, y=-130, ch='🐈', size=150),
                 E('emoji', c('тяжёлая') - 0.4, x=280, y=-130, ch='😩', size=150),
                 E('txt', c('радостью'), x=0, y=60, text='"I\'d love to, but…"', sz=46),
                 E('dark', c('тяжёлая'), x=0, y=200, text='…AND A ROUGH WEEK', sz=44)],
     anim=['pozhimaet-plechami', 'razgovor-zhesty'])
shot(c('длиннее') - 0.2, 'R', [E('card', c('дырок') - 0.3, x=0, y=-330, text='LONG EXCUSE = HOLES', sz=42),
                               E('emoji', c('бабушку'), x=-230, y=-150, ch='👵', size=130),
                               E('plate', c('воскресенье'), x=-230, y=0, text='"GO ON SUNDAY!"', sz=36),
                               E('emoji', c('кота'), x=230, y=-150, ch='🐈', size=130),
                               E('plate', c('собой') - 0.2, x=230, y=0, text='"BRING THE CAT!"', sz=36),
                               E('red', c('снова') - 0.2, x=0, y=190, text='AND YOU SAID "YES" AGAIN', sz=50, rot=-2)],
     anim=['net', 'pozhimaet-plechami'])
shot(c('Короткий') - 0.2, 'L', [E('card', c('увереннее') - 0.3, x=0, y=-300, text='SHORT = MORE CONFIDENT', sz=48),
                                E('dark', c('вежливее') - 0.3, x=0, y=-180, text='AND MORE POLITE', sz=44),
                                E('plate', c('тепло') - 0.1, x=0, y=10, text='WARMTH + "NO"', sz=96, rot=-2),
                                E('txt', c('объяснений') - 0.3, x=0, y=180, text='no explanations', sz=50)],
     anim=['obyasnyaet', 'kivok'])
shot(c('Фраза') - 0.2, 'R', [E('plate', c('Фраза'), x=0, y=-320, text='PHRASE #1', sz=60),
                             E('card', c('Спасибо') - 0.1, x=0, y=-110, text='"THANKS FOR INVITING ME,\nBUT I CAN\'T MAKE IT"', sz=56),
                             E('dark', c('Точка'), x=0, y=110, text='PERIOD.', sz=60, rot=3),
                             E('txt', c('Доклад'), x=0, y=240, text='no report needed', sz=44)],
     anim=['ukazyvaet-vverh', 'kivok'])
shot(c('тонкость') - 0.2, 'L', [E('dark', c('исследовании'), x=0, y=-340, text='STUDY, 2012', sz=38),
                                E('card', c('могу', 1) - 0.2, x=-30, y=-210, text='"I CAN\'T EAT SWEETS"', sz=42),
                                E('txt', c('запретили'), x=-30, y=-110, text='banned → up for debate', sz=38, col=RED),
                                E('plate', c('сладкое', 1) - 0.4, x=-30, y=30, text='"I DON\'T EAT SWEETS"', sz=56),
                                E('txt', c('решение'), x=-30, y=130, text='= your decision', sz=42),
                                E('check', c('лучше') - 0.3, x=0, y=250, s=80),
                                E('dark', c('держались'), x=-30, y=330, text='"I DON\'T" STUCK BETTER', sz=36)],
     anim=['razgovor', 'obyasnyaet'])
shot(c('фраза', 1) - 0.2, 'R', [E('plate', c('фраза', 1), x=0, y=-340, text='PHRASE #2', sz=60),
                                E('card', c('подработки') - 0.3, x=0, y=-200, text='"I DON\'T WORK\nWEEKENDS"', sz=42),
                                E('card', c('долг') - 0.3, x=0, y=-50, text='"I DON\'T LEND MONEY"', sz=46),
                                E('card', c('могу', 2) - 0.1, x=-200, y=90, text="I CAN'T", sz=46),
                                E('crossline', c('делаю') - 0.3, x=-200, y=90, w=260),
                                E('plate', c('делаю') - 0.1, x=200, y=90, text="I DON'T", sz=52),
                                E('dark', c('правилом') - 0.2, x=0, y=230, text='NOBODY ARGUES WITH A RULE', sz=46)],
     anim=['obyasnyaet', 'ukazyvaet-vbok'])
shot(c('Отлично') - 0.2, 'L', [E('cloud', c('врасплох') - 0.3, x=0, y=-230, text='SO,\nWILL YOU HELP?', w=460, sz=52),
                               E('emoji', c('смотрит'), x=-180, y=60, ch='👀', size=150),
                               E('red', c('сейчас') - 0.3, x=120, y=200, text='ANSWER NEEDED NOW', sz=50, rot=-2)],
     anim=['dyhanie', 'cheshet-golovu'])

# ---------- 6. «я подумаю и отвечу» ----------
c = lambda s, k=0: wt(6, s, k)
shot(None, 'R', [E('plate', c('вылетает') - 0.2, x=-120, y=-260, text='"YES!"', sz=100, rot=-8),
                 E('card', c('подумать') - 0.3, x=60, y=-60, text='BEFORE YOU THINK', sz=50),
                 E('dark', c('неловкой') - 0.3, x=0, y=100, text='PAUSE = AWKWARD', sz=50),
                 E('txt', c('согласием'), x=0, y=230, text='you fill it with a yes', sz=42)],
     anim=['razgovor', 'net'])
shot(c('фраза') - 0.3, 'L', [E('plate', c('фраза'), x=0, y=-330, text='PHRASE #3', sz=60),
                             E('card', c('подумаю') - 0.2, x=0, y=-150, text='"LET ME THINK ABOUT IT\nAND GET BACK TO YOU TONIGHT"', sz=62),
                             E('hourglass', c('пауза', 1) - 0.2, x=-220, y=120, size=200, dur=6.0),
                             E('dark', c('пауза', 1) - 0.2, x=140, y=80, text='NOT A NO.\nA PAUSE.', sz=50),
                             E('txt', c('давления'), x=140, y=230, text='get out from under the pressure', sz=38)],
     anim=['obyasnyaet', 'ukazyvaet-vverh'])
shot(c('помогают') - 0.4, 'R', [E('plate', c('Первый') - 0.2, x=0, y=-330, text='QUESTION 1', sz=56),
                                E('emoji', c('месяц'), x=-230, y=-150, ch='🗓️', size=150),
                                E('card', c('завтра') - 0.1, x=130, y=-150, text='WHAT IF IT WERE TOMORROW?', sz=52),
                                E('txt', c('месяц', 1), x=0, y=20, text="next month we're all free and generous", sz=38),
                                E('plate', c('честный') - 0.2, x=0, y=170, text='THE HONEST ANSWER', sz=64, rot=-2)],
     anim=['cheshet-golovu', 'razgovor'])
shot(c('Второй') - 0.2, 'L', [E('plate', c('Второй'), x=0, y=-340, text='QUESTION 2', sz=56),
                              E('dark', c('Сиверс') - 0.3, x=0, y=-235, text='DEREK SIVERS', sz=40),
                              E('plate', c('чёрт') - 0.1, x=-180, y=-90, text='"HELL YEAH!"', sz=56, rot=-3),
                              E('check', c('конечно'), x=150, y=-90, s=70),
                              E('red', c('значит') - 0.1, x=-180, y=50, text='OTHERWISE: "NO"', sz=52, rot=2),
                              E('card', c('посередине') - 0.2, x=0, y=210, text='EVERYTHING IN BETWEEN =\n"EH, IT\'S FINE"', sz=42)],
     anim=['razgovor-zhesty', 'ukazyvaet-vverh'])
shot(c('страх') - 0.4, 'R', [E('cloud', c('эгоиста') - 0.4, x=0, y=-220, text='WILL I BECOME\nA SELFISH JERK?', w=480, sz=52),
                             E('plate', c('поворот') - 0.3, x=0, y=80, text='THE BIGGEST TWIST', sz=80, rot=-2)],
     anim=['cheshet-golovu', 'mashet'])

# ---------- 7. чтобы «да» чего-то стоило ----------
c = lambda s, k=0: wt(7, s, k)
shot(None, 'C', [E('card', c('Цель'), x=-560, y=-250, text='GOAL: SAY NO\nTO EVERYONE', sz=46),
                 E('strike', c('Цель', 1) - 0.1, x=-560, y=-250, w=320, h=160),
                 E('plate', c('значило') - 0.4, x=560, y=-250, text='GOAL: MAKE "YES"\nMEAN SOMETHING', sz=46, rot=2)],
     anim=['ruki-v-boki', 'obyasnyaet'], s=0.76)
shot(c('Смотри') - 0.2, 'L', [E('card', c('подряд') - 0.3, x=0, y=-320, text='"YES" TO EVERYTHING', sz=50),
                              E('emoji', c('обесценивается') - 0.3, x=-230, y=-130, ch='🪙', size=150, gray=c('обесценивается') + 0.5),
                              E('red', c('обесценивается'), x=150, y=-130, text='LOSES ITS VALUE', sz=46),
                              E('dark', c('фактом') - 0.3, x=0, y=40, text='"DON\'T EVEN ASK,\nJUST TELL HIM"', sz=40),
                              E('emoji', c('автомате') - 0.4, x=-150, y=230, ch='😒', size=130),
                              E('txt', c('автомате') - 0.2, x=150, y=230, text='out of obligation', sz=44)],
     anim=['obyasnyaet', 'net'])
shot(c('умеешь') - 0.2, 'R', [E('plate', c('выбором') - 0.3, x=0, y=-320, text='EVERY "YES" = A CHOICE', sz=56, rot=-2),
                              E('emoji', c('переездом'), x=-230, y=-120, ch='📦', size=150),
                              E('card', c('захотел') - 0.2, x=130, y=-120, text='YOU WANTED TO', sz=50),
                              E('emoji', c('души') - 0.2, x=-230, y=100, ch='😊', size=150),
                              E('card', c('души'), x=130, y=60, text='WITH YOUR WHOLE HEART', sz=50),
                              E('dark', c('кислым') - 0.1, x=130, y=170, text='NOT WITH A SOUR FACE', sz=34)],
     anim=['kivok', 'razgovor-zhesty'])
shot(c('поворот') - 0.3, 'C', [E('dark', c('поворот') - 0.2, x=0, y=-390, text='THE TWIST', sz=40),
                               E('card', c('меньше') - 0.3, x=-560, y=-230, text='HELP\nLESS', sz=56),
                               E('strike', c('настоящему') - 0.5, x=-560, y=-230, w=330, h=170),
                               E('plate', c('настоящему') - 0.3, x=560, y=-230, text='HELP\nFOR REAL', sz=56, rot=-2)],
     anim=['pryzhok', 'ukazyvaet-vverh'], s=0.76)
shot(c('Хорошие') - 0.2, 'L', [E('card', c('уходят') - 0.2, x=150, y=-320, text='GOOD PEOPLE STAY', sz=44),
                               E('plate', c('уважать') - 0.2, x=150, y=-200, text='AND RESPECT YOU MORE', sz=52, rot=-2),
                               E('txt', c('правда'), x=150, y=-80, text='said yes = really means it', sz=38),
                               E('boxes', c('уходит') - 0.3, x=-150, y=330, labels=('FAVOR',) * 4, w=220, h=72, sz=28,
                                 gone=tuple(c('просьбами') - 0.6 + 0.15 * i for i in range(4)))],
     anim=['razgovor', 'mashet'])
shot(c('Осталось') - 0.2, 'R', [E('plate', c('сегодня') - 0.4, x=0, y=-100, text='WHERE TO START\nTODAY?', sz=76)],
     anim=['cheshet-golovu'])

# ---------- 8. финал ----------
c = lambda s, k=0: wt(8, s, k)
IT = [('пещере', 'YOUR BRAIN LIVES IN A CAVE'), ('денег', '"IT\'S FINE" COSTS MONEY AND ENERGY'), ('себе', '"YES" TO THEM = "NO" TO YOU'),
      ('обижаются', 'PEOPLE GET LESS UPSET THAN YOU THINK'), ('коротко', 'SAY NO: SHORT, NO EXCUSES')]
els = [E('plate', c('Итак'), x=0, y=-360, text='RECAP', sz=50)]
for k, (w, tx) in enumerate(IT):
    y = -240 + k * 105; ta = c(w) - 0.4
    els += [E('check', ta + 0.2, x=-420, y=y, s=46), E('card', ta, x=30, y=y, text=tx, sz=36)]
shot(None, 'R', els, anim=['razgovor', 'kivok', 'razgovor'])
shot(c('План') - 0.2, 'L', [E('plate', c('План'), x=0, y=-340, text='YOUR PLAN FOR TODAY', sz=70),
                            E('card', c('Вспомни') - 0.1, x=0, y=-200, text='1.  RECALL ONE AWKWARD "YES"', sz=36),
                            E('card', c('следующую') - 0.2, x=0, y=-90, text='2.  NEXT TIME SOMEONE ASKS:', sz=40),
                            E('plate', c('подумаю') - 0.3, x=0, y=40, text='"LET ME THINK ABOUT IT"', sz=62, rot=-2),
                            E('emoji', c('комментариях'), x=-250, y=230, ch='💬', size=130),
                            E('card', c('комментариях'), x=110, y=230, text='WHAT DID YOU AGREE TO?', sz=40)],
     anim=['ukazyvaet-vverh', 'obyasnyaet', 'mashet'])
TFIN = c('плохой') - 0.6
shot(TFIN, 'C', [E('txt', c('плохой') - 0.3, c('тупи') - 0.4, x=-560, y=-260, text="you're not a bad person", sz=50),
                 E('dark', c('жизнь') - 0.5, c('тупи') - 0.4, x=560, y=-260, text='YOU HAVE A LIFE\nOF YOUR OWN', sz=50),
                 E('boxes', c('жизнь') - 0.5, c('тупи') + 0.2, x=230, y=405, labels=(), w=300, h=100, sz=40, mine=c('жизнь') - 0.4),
                 E('plate', c('тупи') - 0.15, x=0, y=-370, text="THAT'S IT. DON'T BE DUMB.", sz=90, rot=-3)],
     anim=['dyhanie', 'kivok'], s=0.78)

# первый шот каждой главы начинается в паузе перед ней
_ch = 0
for sh in SHOTS:
    if sh['t'] is None:
        _ch += 1; sh['t'] = O[_ch] - GAP
for a, b in zip(SHOTS, SHOTS[1:]): assert a['t'] < b['t'], (a['t'], b['t'], b['els'][0])
