"""Сцены ролика: кадры (шоты) по главам. Координаты элементов — относительно центра графики шота."""
from tl import wt, O, GAP, END, NCH
from gfx import YEL, RED, INK, WHITE, GRAY
SHOTS = []
def E(kind, ta, te=None, **kw): return (kind, ta, te, kw)
def shot(t, side, els, anim=(), s=0.72, bg=None):
    SHOTS.append(dict(t=t, side=side, s=s, anim=list(anim), els=els, bg=bg))

# ---------- 0. холодный старт ----------
c = lambda s, k=0: wt(0, s, k)
shot(0, 'C', [E('emoji', 0.1, x=-560, y=-230, ch='🕙', size=200),
              E('card', c('Воскресенье'), x=-560, y=-20, text='SUNDAY, 10 PM', sz=48),
              E('emoji', c('работу'), x=560, y=-260, ch='💼', size=170),
              E('cloud', c('ноет'), x=560, y=0, text='IS THIS REALLY\nMY LIFE?', w=480, sz=42)],
     anim=['dyhanie', 'pozhimaet-plechami'], s=0.78, bg='evening')
shot(c('Тебе') - 0.2, 'C', [E('cross', c('Тебе') - 0.2, x=0, y=420, r=820, sz=30),
                            E('red', c('тридцать'), x=560, y=-260, text="YOU'RE 30", sz=60, rot=6),
                            E('cloud', c('знаешь'), x=-560, y=-250, text='WHAT DO I WANT?', w=420)],
     anim=['cheshet-golovu', 'ruki-v-boki'], s=0.78)
shot(c('гуглил') - 0.2, 'R', [E('card', c('гуглил'), x=0, y=-300, text='"how to find yourself"', sz=46),
                              E('dark', c('тесты'), x=0, y=-170, text='PERSONALITY TEST', sz=38),
                              E('tabs', c('двенадцать'), x=0, y=110, t_close=c('закрыл'))],
     anim=['razgovor-zhesty'])
shot(c('Стоп') - 0.2, 'L', [E('plate', c('Стоп') - 0.05, x=0, y=-230, text="STOP.\nYOU'RE BEING DUMB", sz=84, rot=-3),
                            E('card', c('Проблема'), c('ищешь') - 0.1, x=0, y=90, text="HAVEN'T FOUND YOUR PASSION", sz=50),
                            E('crossline', c('Проблема', 1) + 0.3, c('ищешь') - 0.1, x=0, y=90, w=640),
                            E('plate', c('ищешь'), x=0, y=110, text='STOP LOOKING FOR IT', sz=96, rot=2)],
     anim=['ukazyvaet-vverh', 'net'], s=0.76)
shot(c('десять', 1) - 0.2, 'R', [E('cross', c('десять', 1), x=0, y=60, r=380),
                              E('red', c('дорогая'), x=0, y=-330, text='THE MOST EXPENSIVE MISTAKE', sz=48),
                              E('flash', c('сегодня') - 0.2, x=0, y=370, text='3 THINGS → PICK 1')],
     anim=['obyasnyaet', 'mashet'])

# ---------- 1. миф ----------
c = lambda s, k=0: wt(1, s, k)
shot(None, 'L', [E('emoji', c('сказку'), x=-230, y=-150, ch='📖', size=230),
                 E('plate', c('Твоё'), x=170, y=-150, text='YOUR TRUE CALLING', sz=70, rot=-4),
                 E('txt', c('найти'), x=0, y=120, text='you just have to find it…', sz=50)],
     anim=['obyasnyaet'])
shot(c('бац') - 0.2, 'R', [E('emoji', c('бац'), x=-300, y=-230, ch='⚡', size=190),
                           E('emoji', c('музыка'), x=0, y=-230, ch='🎵', size=170),
                           E('emoji', c('просыпаешься'), x=300, y=-230, ch='🌅', size=170),
                           E('card', c('бесплатно'), x=0, y=10, text="I'D WORK FOR FREE", sz=44),
                           E('red', c('почти'), x=0, y=200, text='ALMOST NOBODY GETS THIS', sz=56, rot=-3)],
     anim=['pryzhok', 'razgovor-zhesty', 'net'])
shot(c('Психологи') - 0.2, 'L', [E('dark', c('Стэнфорда'), x=0, y=-320, text='STANFORD, 2018', sz=40),
                                 E('card', c('верят'), x=0, y=-160, text='"PASSION IS FOUND"', sz=50),
                                 E('arrow', c('теряют') - 0.3, x0=0, y0=-90, x1=0, y1=10),
                                 E('red', c('теряют'), x=0, y=110, text='LOSE INTEREST\nWHEN IT GETS HARD', sz=50)],
     anim=['razgovor', 'ukazyvaet-vbok'])
shot(c('Логика') - 0.2, 'R', [E('cloud', c('Логика'), x=0, y=-230, text="IF IT'S MY THING,\nIT'LL BE EASY", w=460),
                              E('card', c('Раз'), x=0, y=40, text='HARD = NOT MY THING?', sz=60),
                              E('red', c('Следующее'), x=40, y=220, text='NEXT!', sz=64, rot=6)],
     anim=['cheshet-golovu', 'mashet'])
shot(c('встречаться') - 0.2, 'L', [E('emoji', c('встречаться'), x=0, y=-200, ch='💘', size=200),
                                   E('card', c('втором'), x=0, y=60, text='2ND DATE = GOODBYE', sz=50),
                                   E('dark', c('взгляда'), x=0, y=210, text='NO LOVE AT FIRST SIGHT', sz=36)],
     anim=['razgovor-zhesty'])
shot(c('кругу') - 0.2, 'R', [E('emoji', c('гитара'), x=-330, y=-200, ch='🎸', size=170), E('strike', c('гитара') + 0.7, x=-330, y=-200, w=150, h=150),
                             E('emoji', c('программирование'), x=0, y=-200, ch='💻', size=170), E('strike', c('программирование') + 0.9, x=0, y=-200, w=150, h=150),
                             E('emoji', c('бизнес'), x=330, y=-200, ch='💼', size=170), E('strike', c('бизнес') + 0.7, x=330, y=-200, w=150, h=150),
                             E('card', c('везде'), x=0, y=60, text='IT WAS HARD EVERY TIME', sz=54),
                             E('plate', c('всегда'), x=0, y=210, text="IT'S ALWAYS HARD", sz=60, rot=-2)],
     anim=['net', 'pozhimaet-plechami'])
shot(c('монетка') - 0.2, 'L', [E('emoji', c('монетка'), x=-230, y=-150, ch='🛋️', size=220),
                               E('strike', c('вырастает') - 0.2, x=-230, y=-150, w=200, h=200),
                               E('emoji', c('вырастает'), x=230, y=-160, ch='🌱', size=230),
                               E('card', c('бросил'), x=0, y=160, text="FROM WHAT YOU DIDN'T QUIT", sz=54)],
     anim=['obyasnyaet', 'kivok'])
shot(c('Ладно') - 0.2, 'R', [E('plate', c('почему'), x=0, y=-110, text='WHY IS IT SO HARD\nTO JUST PICK?', sz=64),
                             E('dark', c('лень'), x=0, y=130, text="AND IT'S NOT LAZINESS", sz=50, rot=3)],
     anim=['cheshet-golovu'])

# ---------- 2. сто дорог ----------
c = lambda s, k=0: wt(2, s, k)
shot(None, 'L', [E('emoji', c('бабушки'), x=-300, y=-220, ch='👵', size=190),
                 E('card', c('бабушки'), x=-300, y=-50, text='3 ROADS', sz=44),
                 E('card', c('Тысяча'), x=200, y=-280, text='THOUSANDS OF CAREERS', sz=46),
                 E('card', c('Курсы'), x=200, y=-170, text='COURSES ON ANYTHING', sz=40),
                 E('emoji', c('переехать'), x=40, y=40, ch='✈️', size=130),
                 E('emoji', c('дома'), x=210, y=40, ch='🏠', size=130),
                 E('emoji', c('своё'), x=380, y=40, ch='🚀', size=130)],
     anim=['mashet', 'razgovor-zhesty'])
shot(c('Свобода') - 0.2, 'C', [E('cross', c('Свобода') - 0.2, x=0, y=420, r=820, sz=30),
                               E('plate', c('Свобода'), x=-560, y=-250, text='FREEDOM!', sz=80, rot=-6),
                               E('dark', c('стоишь'), x=560, y=-250, text="AND YOU'RE\nSTANDING STILL", sz=50, rot=4)],
     anim=['pryzhok', 'dyhanie'], s=0.78)
shot(c('джемом') - 0.2, 'R', [E('emoji', c('джемом'), x=-380, y=-300, ch='🍓', size=150),
                              E('card', c('двадцать'), x=-120, y=-300, text='24 FLAVORS', sz=44),
                              E('card', c('шесть'), x=200, y=-300, text='6 FLAVORS', sz=44),
                              E('bars', c('останавливались') - 0.6, x=0, y=170, maxh=280, items=[
                                  ('24\nstopped', 0.95, INK, c('останавливались')), ('6\nstopped', 0.6, GRAY, c('останавливались') + 0.2),
                                  ('24\nbought', 0.1, RED, c('покупали')), ('6\nbought', 0.75, YEL, c('покупали') + 0.2)]),
                              E('txt', c('крайней'), x=0, y=330, text='at least in that experiment', sz=30)],
     anim=['obyasnyaet', 'razgovor'])
shot(c('Слишком') - 0.2, 'L', [E('emoji', c('Слишком'), x=0, y=-200, ch='🤯', size=230),
                               E('card', c('зависает'), x=0, y=80, text='THE BRAIN FREEZES', sz=70)],
     anim=['cheshet-golovu'])
shot(c('жизнью') - 0.2, 'R', [E('cross', c('жизнью'), x=0, y=60, r=400, alive_to=0.04, alive_t=c('отказ'), hi=0),
                              E('plate', c('отказ'), x=0, y=-340, text='1 CHOICE = GIVING UP 99', sz=52),
                              E('red', c('ничего'), x=0, y=330, text='IT CHOOSES TO CHOOSE NOTHING', sz=40)],
     anim=['obyasnyaet', 'pozhimaet-plechami'])
shot(c('тоже') - 0.2, 'L', [E('card', c('тоже'), x=0, y=-280, text='"NOT CHOOSING" IS A CHOICE', sz=48),
                            E('red', c('плохой'), x=0, y=-150, text='THE WORST ONE', sz=50, rot=-3),
                            E('dark', c('временно'), x=-160, y=60, text='"JUST FOR NOW" JOB', sz=44),
                            E('arrow', c('карьерой') - 0.3, x0=40, y0=130, x1=160, y1=200),
                            E('red', c('карьерой'), x=230, y=250, text='10 YEARS', sz=80, rot=4)],
     anim=['razgovor-zhesty', 'net'])
shot(c('шестой') - 0.2, 'R', [E('dark', c('шестой'), x=0, y=-300, text='→ CHAPTER 6', sz=44),
                              E('cloud', c('голос'), x=0, y=-60, text='?!', w=360, sz=90, fg=RED),
                              E('emoji', c('точно'), x=0, y=230, ch='👂', size=160)],
     anim=['ukazyvaet-vverh', 'kivok'])
shot(c('сначала') - 0.2, 'L', [E('emoji', c('отмотаем'), x=0, y=-200, ch='⏪', size=200),
                               E('plate', c('выбирал'), x=0, y=90, text='HOW DID YOU CHOOSE AT 20?', sz=70)],
     anim=['pokachivanie'])

# ---------- 3. в двадцать ----------
c = lambda s, k=0: wt(3, s, k)
shot(None, 'R', [E('counter', c('двадцать') - 0.3, v0=30, v1=20, x=0, y=-230, sz=230, dur=0.8, endcol=RED),
                 E('emoji', c('вагон'), x=-220, y=60, ch='⏳', size=170),
                 E('card', c('вагон'), x=120, y=60, text='ALL THE TIME IN THE WORLD', sz=50),
                 E('txt', c('делаешь'), x=0, y=230, text='and what do you do with it?', sz=48)],
     anim=['pokachivanie', 'pozhimaet-plechami'])
shot(c('Поступаешь') - 0.2, 'L', [E('emoji', c('Поступаешь'), x=0, y=-320, ch='🎓', size=150),
                                  E('card', c('баллам'), x=-330, y=-160, text='GOT IN', sz=48),
                                  E('card', c('мама'), x=0, y=-160, text='PARENTS', sz=48),
                                  E('card', c('друзья'), x=330, y=-160, text='FRIENDS', sz=48),
                                  E('dark', c('учишься'), x=0, y=-20, text='STUDYING WHAT YOU NEVER CHOSE', sz=40),
                                  E('plate', c('временно'), x=-80, y=140, text='"IT\'S TEMPORARY,\nI\'LL FIGURE IT OUT"', sz=48, rot=-2),
                                  E('emoji', c('работу'), x=340, y=150, ch='💼', size=150)],
     anim=['razgovor-zhesty', 'pozhimaet-plechami'])
shot(c('главные') - 0.2, 'R', [E('plate', c('ошибки'), x=0, y=-340, text='MISTAKES AT 20', sz=60),
                               E('card', c('первая'), x=0, y=-200, text='1.  "WHERE I GOT IN"', sz=46),
                               E('card', c('вторая'), x=0, y=-80, text='2.  LIFE STARTS LATER', sz=46),
                               E('card', c('третья'), x=0, y=40, text='3.  "PLENTY OF TIME"', sz=46),
                               E('red', c('четвёртая'), x=0, y=170, text='4.  KNOW IT ALL AT 20', sz=48, rot=-2),
                               E('txt', c('так', 1), x=0, y=300, text="and if you don't, something's wrong with you", sz=34)],
     anim=['ukazyvaet-vverh', 'obyasnyaet', 'net'])
shot(c('Хорошая') - 0.2, 'L', [E('check', c('Хорошая') + 0.2, x=-330, y=-230),
                               E('card', c('Хорошая'), x=40, y=-230, text='ALMOST EVERYONE DID', sz=48),
                               E('red', c('Плохая'), x=40, y=-100, text='MANY STILL DO AT 30', sz=50),
                               E('counter', c('тридцать') - 0.3, v0=20, v1=30, x=0, y=80, sz=170, dur=0.6),
                               E('card', c('ставки'), x=0, y=250, text='SAME CHOICE, HIGHER STAKES', sz=46)],
     anim=['kivok', 'razgovor'])
shot(c('узнал') - 0.2, 'R', [E('emoji', c('видишь'), x=0, y=-230, ch='👀', size=190),
                             E('plate', c('тупил'), x=0, y=40, text="THAT'S STEP ONE", sz=70)],
     anim=['kivok'])
shot(c('допустим') - 0.2, 'L', [E('cloud', c('допустим'), x=0, y=-170, text='I WANT…', w=380, sz=60),
                                E('plate', c('твоё'), x=0, y=150, text='IS IT EVEN YOUR DREAM?', sz=60)],
     anim=['cheshet-golovu'])

# ---------- 4. чьё желание ----------
c = lambda s, k=0: wt(4, s, k)
shot(None, 'R', [E('emoji', c('машину'), x=-330, y=-220, ch='🚗', size=170),
                 E('emoji', c('бизнес'), x=0, y=-220, ch='💼', size=170),
                 E('emoji', c('моря'), x=330, y=-220, ch='🏖️', size=170),
                 E('plate', c('откуда'), x=0, y=80, text='WHERE DID IT COME FROM?', sz=80, rot=-3)],
     anim=['razgovor', 'cheshet-golovu'])
shot(c('папа') - 0.4, 'L', [E('emoji', c('папа') - 0.4, x=-330, y=-260, ch='🚗', size=150),
                            E('emoji', c('блогер') - 0.6, x=0, y=-260, ch='💼', size=150),
                            E('emoji', c('одноклассницы') - 1.0, x=330, y=-260, ch='🏖️', size=150),
                            E('emoji', c('папа'), x=-330, y=60, ch='👨', size=140), E('arrow', c('папа') + 0.2, x0=-330, y0=-20, x1=-330, y1=-170),
                            E('card', c('папа'), x=-330, y=180, text='DAD', sz=44),
                            E('emoji', c('блогер'), x=0, y=60, ch='🎥', size=140), E('arrow', c('блогер') + 0.2, x0=0, y0=-20, x1=0, y1=-170),
                            E('card', c('блогер'), x=0, y=180, text='INFLUENCER', sz=44),
                            E('emoji', c('одноклассницы'), x=330, y=60, ch='🤳', size=140), E('arrow', c('одноклассницы') + 0.2, x0=330, y0=-20, x1=330, y1=-170),
                            E('card', c('сторис'), x=330, y=180, text='INSTAGRAM', sz=44)],
     anim=['ukazyvaet-vbok', 'razgovor-zhesty'])
shot(c('Многое') - 0.2, 'R', [E('red', c('подкинули'), x=0, y=-280, text='A LOT WAS HANDED TO YOU', sz=54, rot=-2),
                              E('card', c('Родители'), x=-320, y=-120, text='PARENTS', sz=42),
                              E('card', c('школа'), x=0, y=-120, text='SCHOOL', sz=42),
                              E('card', c('соцсети'), x=310, y=-120, text='SOCIAL MEDIA', sz=42),
                              E('emoji', c('тихое'), x=0, y=90, ch='🤫', size=160),
                              E('txt', c('рекламе'), x=0, y=250, text='your own desire is quiet: nobody sells it in ads', sz=34)],
     anim=['obyasnyaet', 'dyhanie'])
shot(c('тест') - 0.2, 'L', [E('plate', c('тест'), x=0, y=-320, text='TEST: NOBODY WILL KNOW', sz=58),
                            E('emoji', c('лайков'), x=-300, y=-120, ch='❤️', size=140, gray=c('делал') - 0.5),
                            E('emoji', c('родителей'), x=0, y=-120, ch='👨‍👩‍👦', size=140, gray=c('делал') - 0.5),
                            E('emoji', c('одноклассников'), x=300, y=-120, ch='👥', size=140, gray=c('делал') - 0.5),
                            E('cloud', c('делал'), x=0, y=110, text='WHAT WOULD\nYOU DO?', w=500, sz=46),
                            E('dark', c('ближе'), x=0, y=360, text="THAT'S CLOSER TO YOURS", sz=40)],
     anim=['razgovor', 'kivok'])
shot(c('подсказка') - 0.2, 'R', [E('plate', c('подсказка'), x=0, y=-330, text='HINTS', sz=56),
                                 E('card', c('тратишь'), x=0, y=-190, text='WHAT YOU DO WHEN NOBODY MAKES YOU', sz=44),
                                 E('card', c('часами'), x=0, y=-70, text='WHAT YOU TALK ABOUT FOR HOURS', sz=44),
                                 E('card', c('вечер'), x=0, y=50, text='WHERE EVENINGS DISAPPEAR', sz=44),
                                 E('dark', c('направление'), x=0, y=200, text='NOT THE ANSWER, BUT A DIRECTION', sz=40)],
     anim=['ukazyvaet-vbok', 'obyasnyaet'])
shot(c('главный') - 0.2, 'L', [E('plate', c('главный'), x=0, y=-200, text='THE REAL ANSWER:\nCOMING UP', sz=64),
                               E('emoji', c('понравится'), x=-150, y=110, ch='😒', size=160),
                               E('emoji', c('понравится', 1), x=150, y=110, ch='😊', size=160)],
     anim=['ukazyvaet-vverh', 'kivok'])
shot(c('лежать') - 0.2, 'R', [E('emoji', c('лежать'), x=0, y=-140, ch='🛋️', size=240),
                              E('dark', c('следующая'), x=0, y=150, text='→ NEXT CHAPTER', sz=50)],
     anim=['pozhimaet-plechami'])

# ---------- 5. ничего не хочешь ----------
c = lambda s, k=0: wt(5, s, k)
shot(None, 'L', [E('cloud', c('спрашиваешь'), x=-60, y=-230, text='WHAT DO I WANT?', w=440, sz=46),
                 E('emoji', c('тишина'), x=300, y=-60, ch='🦗', size=150),
                 E('dark', c('машину'), x=0, y=90, text='NO CAR, NO OCEAN, NO BUSINESS', sz=40),
                 E('emoji', c('лечь'), x=0, y=250, ch='🛏️', size=170)],
     anim=['dyhanie', 'pozhimaet-plechami'])
shot(c('пустой') - 0.2, 'R', [E('card', c('пустой'), x=0, y=-180, text="YOU'RE NOT EMPTY", sz=64),
                              E('plate', c('причины'), x=0, y=40, text='3 REASONS', sz=90, rot=-3)],
     anim=['net', 'obyasnyaet'])
shot(c('Первая') - 0.2, 'L', [E('plate', c('Первая'), x=0, y=-340, text='1.  EXHAUSTION', sz=56),
                              E('emoji', c('спишь'), x=-330, y=-160, ch='😴', size=140),
                              E('battery', c('устал'), x=0, y=-170, l0=0.8, l1=0.05, dur=4.0),
                              E('emoji', c('лентой'), x=330, y=-160, ch='📱', size=140),
                              E('card', c('выживает'), x=0, y=90, text="THE BRAIN DOESN'T DREAM, IT SURVIVES", sz=42),
                              E('dark', c('пятницы'), x=0, y=230, text='JUST MAKE IT TO FRIDAY', sz=42)],
     anim=['dyhanie', 'razgovor'])
shot(c('дешёвый') - 0.2, 'R', [E('plate', c('дешёвый'), x=0, y=-340, text='2.  CHEAP FUN', sz=56),
                               E('emoji', c('Лента'), x=-330, y=-190, ch='📱', size=130),
                               E('emoji', c('сериалы'), x=-110, y=-190, ch='📺', size=130),
                               E('emoji', c('игры'), x=110, y=-190, ch='🎮', size=130),
                               E('emoji', c('доставка'), x=330, y=-190, ch='🍔', size=130),
                               E('card', c('секунду'), x=0, y=-40, text='IN ONE SECOND, ZERO EFFORT', sz=44),
                               E('emoji', c('книга'), x=-260, y=120, ch='📚', size=120, gray=c('книга') + 0.3),
                               E('emoji', c('спорт'), x=0, y=120, ch='🏃', size=120, gray=c('спорт') + 0.3),
                               E('emoji', c('хобби'), x=260, y=120, ch='🎨', size=120, gray=c('хобби') + 0.3),
                               E('dark', c('перебили'), x=0, y=290, text='YOUR DESIRES GOT DROWNED OUT', sz=42)],
     anim=['razgovor-zhesty', 'obyasnyaet'])
shot(c('третья') - 0.2, 'L', [E('plate', c('третья'), x=0, y=-340, text='3.  LET DOWN TOO OFTEN', sz=56),
                              E('cloud', c('Хотел', 1), c('получилось') - 0.05, x=-230, y=-140, text='I WANT IT!', w=320, sz=50),
                              E('red', c('получилось'), x=-230, y=-140, text="DIDN'T WORK OUT", sz=40, rot=-4),
                              E('cloud', c('Хотел', 2), c('высмеяли') - 0.05, x=230, y=-140, text='I WANT IT!', w=320, sz=50),
                              E('red', c('высмеяли'), x=230, y=-140, text='PEOPLE LAUGHED', sz=40, rot=4),
                              E('card', c('лучше'), x=0, y=100, text='"SAFER NOT TO WANT"', sz=46),
                              E('emoji', c('безопаснее'), x=0, y=260, ch='🐢', size=150)],
     anim=['dyhanie', 'net'])
shot(c('здесь') - 0.6, 'R', [E('emoji', c('выспись'), x=-250, y=-210, ch='🛏️', size=170),
                             E('emoji', c('телефоном'), x=250, y=-210, ch='📱', size=150),
                             E('strike', c('кровати'), x=250, y=-210, w=150, h=150),
                             E('card', c('кровати'), x=0, y=-20, text='PHONE AWAY FROM THE BED', sz=42),
                             E('battery', c('Желания'), x=0, y=170, l0=0.05, l1=0.05, charge_at=c('Желания') + 0.3)],
     anim=['razgovor', 'kivok'])
shot(c('Выспался') - 0.2, 'L', [E('check', c('появилось'), x=-320, y=-170),
                                E('card', c('появилось'), x=40, y=-170, text='A DESIRE SHOWED UP', sz=50),
                                E('cloud', c('голос'), x=0, y=110, text='?!', w=340, sz=90, fg=RED)],
     anim=['kivok', 'ukazyvaet-vverh'])

# ---------- 6. уже поздно ----------
c = lambda s, k=0: wt(6, s, k)
shot(None, 'R', [E('cloud', c('Мне'), x=0, y=-200, text="I'M ALREADY 30.\nTOO LATE.", w=520, sz=52, fg=RED),
                 E('card', c('нормальные'), x=0, y=110, text='"EVERYONE IS ALREADY SOMEONE"', sz=48)],
     anim=['pozhimaet-plechami', 'net'])
shot(c('Знаешь') - 0.2, 'L', [E('emoji', c('Кроку'), x=0, y=-280, ch='🍔', size=160),
                              E('counter', c('Пятьдесят') - 0.2, v0=0, v1=52, x=0, y=-60, sz=220, dur=0.7, col=RED),
                              E('card', c('Пятьдесят'), x=0, y=120, text="RAY KROC TOOK ON McDONALD'S", sz=40),
                              E('txt', c('миллиардером'), x=0, y=260, text='no billions promised', sz=36)],
     anim=['ukazyvaet-vverh', 'razgovor'])
shot(c('отговорка') - 0.6, 'R', [E('plate', c('отговорка'), x=0, y=-60, text='"TOO LATE" = EXCUSE', sz=76, rot=-3)],
     anim=['ruki-v-boki'])
shot(c('обратная') - 0.2, 'L', [E('emoji', c('боишься'), x=0, y=-320, ch='⏳', size=150),
                                E('card', c('любом'), x=0, y=-160, text='3 YEARS WILL PASS ANYWAY', sz=44),
                                E('card', c('пробу'), x=-240, y=10, text='TRYING', sz=50), E('check', c('пробу') + 0.4, x=-240, y=150),
                                E('dark', c('стояние'), x=240, y=10, text='STANDING STILL', sz=50), E('strike', c('стояние') + 0.6, x=240, y=150, w=110, h=110)],
     anim=['obyasnyaet', 'razgovor-zhesty'])
shot(c('Психологи') - 0.2, 'R', [E('plate', c('жалеют'), x=0, y=-330, text='WHAT PEOPLE REGRET', sz=56),
                                 E('card', c('вчерашний'), x=-250, y=-190, text='YESTERDAY', sz=44),
                                 E('dark', c('ошибках'), x=-250, y=-80, text='WHAT THEY DID', sz=40),
                                 E('card', c('всю'), x=250, y=-190, text='WHOLE LIFE', sz=44),
                                 E('red', c('попробовали'), x=250, y=-80, text='WHAT THEY NEVER TRIED', sz=40),
                                 E('emoji', c('восемьдесят'), x=-330, y=170, ch='👴', size=170),
                                 E('cloud', c('Надо'), x=90, y=170, text='I SHOULD HAVE\nTRIED', w=440, sz=42)],
     anim=['razgovor', 'dyhanie'])
shot(c('Неправильный') - 0.2, 'L', [E('card', c('Неправильный'), x=0, y=-140, text='WRONG STEP → FIXABLE', sz=46),
                                    E('red', c('нельзя'), x=0, y=20, text='NO STEP → NOT FIXABLE', sz=50)],
     anim=['ruki-v-boki'])
shot(c('Хорошо') - 0.2, 'R', [E('plate', c('понять'), x=0, y=-110, text='HOW DO YOU KNOW\nWHAT TO TRY?', sz=66),
                              E('dark', c('поворот'), x=0, y=140, text='THE BIGGEST TWIST', sz=46, rot=3)],
     anim=['cheshet-golovu'])

# ---------- 7. сначала делаешь ----------
c = lambda s, k=0: wt(7, s, k)
shot(None, 'C', [E('plate', c('главное'), x=0, y=-390, text='THE MAIN THING', sz=44),
                 E('card', c('понять'), x=-560, y=-110, text='FIGURE OUT WHAT I WANT', sz=44),
                 E('arrow', c('начать') - 0.3, x0=-560, y0=-50, x1=-560, y1=50),
                 E('card', c('начать'), x=-560, y=110, text='START', sz=44),
                 E('crossline', c('наоборот'), x=-560, y=0, w=380),
                 E('red', c('наоборот'), x=560, y=-260, text='THE OTHER WAY AROUND', sz=56, rot=4),
                 E('plate', c('делаешь'), x=560, y=-110, text='DO', sz=54),
                 E('arrow', c('хочешь', 1) - 0.3, x0=560, y0=-50, x1=560, y1=50),
                 E('plate', c('хочешь', 1), x=560, y=110, text='WANT', sz=54)],
     anim=['ukazyvaet-vverh', 'obyasnyaet'], s=0.74)
G = lambda k: [(0, -240), (300, 0), (0, 240), (-300, 0)][k]
shot(c('Интерес') - 0.2, 'L', [E('emoji', c('диване'), x=-380, y=-320, ch='🛋️', size=120), E('strike', c('диване') + 0.3, x=-380, y=-320, w=120, h=120),
                               E('card', c('Получается'), x=G(0)[0], y=G(0)[1], text='GET GOOD', sz=40),
                               E('arrow', c('хвалят') - 0.2, x0=130, y0=-200, x1=260, y1=-70),
                               E('card', c('хвалят'), x=G(1)[0], y=G(1)[1], text='PEOPLE NOTICE', sz=40),
                               E('arrow', c('больше') - 0.2, x0=260, y0=70, x1=130, y1=200),
                               E('card', c('больше'), x=G(2)[0], y=G(2)[1], text='DO MORE', sz=40),
                               E('arrow', c('лучше') - 0.2, x0=-130, y0=200, x1=-260, y1=70),
                               E('card', c('лучше'), x=G(3)[0], y=G(3)[1], text='GET EVEN BETTER', sz=40),
                               E('arrow', c('призвание') - 0.2, x0=-260, y0=-70, x1=-130, y1=-200),
                               E('plate', c('ком'), x=0, y=0, text='SNOW-\nBALL', sz=56, rot=-3),
                               E('emoji', c('молния'), x=380, y=-320, ch='⚡', size=120), E('strike', c('молния') + 0.3, x=380, y=-320, w=120, h=120)],
     anim=['obyasnyaet', 'pryzhok', 'razgovor-zhesty'])
shot(c('Покажи') - 0.2, 'R', [E('card', c('нашёл'), x=0, y=-250, text='"FOUND THEMSELVES"', sz=54),
                              E('arrow', c('долго') - 0.3, x0=0, y0=-185, x1=0, y1=-95),
                              E('dark', c('долго'), x=0, y=-30, text='DID BORING STUFF FOR A LONG TIME', sz=48),
                              E('arrow', c('хорош') - 0.3, x0=0, y0=35, x1=0, y1=125),
                              E('plate', c('хорош'), x=0, y=190, text='GOT GOOD AT IT', sz=56)],
     anim=['razgovor-zhesty', 'kivok'])
shot(c('повара') - 0.2, 'L', [E('emoji', c('повара'), x=-380, y=-290, ch='👨‍🍳', size=150),
                              E('emoji', c('лук'), x=-140, y=-290, ch='🧅', size=130),
                              E('red', c('Нет'), x=90, y=-290, text='NO', sz=50, rot=5),
                              E('emoji', c('деньги'), x=330, y=-290, ch='💰', size=130),
                              E('card', c('Резал'), x=-330, y=-60, text='ONIONS. BORING', sz=38),
                              E('card', c('быстрее'), x=0, y=-60, text='THE FASTEST', sz=38),
                              E('card', c('шеф'), x=330, y=-60, text='HEAD CHEF NOTICED', sz=38),
                              E('card', c('плиты'), x=-330, y=110, text='ON THE LINE', sz=38),
                              E('card', c('блюдо'), x=0, y=110, text='OWN DISH', sz=38),
                              E('emoji', c('загорелся'), x=330, y=100, ch='🔥', size=170),
                              E('plate', c('загорелся'), x=0, y=280, text='ONLY THEN THEY CAUGHT FIRE', sz=46)],
     anim=['razgovor', 'obyasnyaet', 'razgovor-zhesty'])
shot(c('Поэтому', 1) - 0.2, 'R', [E('card', c('хочу'), x=0, y=-200, text='"WHAT DO I WANT?"', sz=56),
                               E('crossline', c('плохой'), x=0, y=-200, w=520),
                               E('plate', c('Хороший'), x=0, y=60, text='"WHAT CAN I TRY\nTHIS WEEK?"', sz=60, rot=-2)],
     anim=['net', 'ukazyvaet-vverh'])
shot(c('пробовать', 2) - 0.3, 'L', [E('emoji', c('годы'), x=-150, y=-150, ch='⏳', size=160),
                                E('emoji', c('деньги', 1), x=150, y=-150, ch='💸', size=160),
                                E('plate', c('пробовать', 2), x=0, y=110, text='HOW TO TRY CHEAPLY?', sz=64)],
     anim=['cheshet-golovu'])

# ---------- 8. как пробовать ----------
c = lambda s, k=0: wt(8, s, k)
shot(None, 'R', [E('emoji', c('горы'), x=-170, y=-230, ch='🏔️', size=170),
                 E('emoji', c('лотерея'), x=170, y=-230, ch='🎟️', size=170),
                 E('card', c('лотерея'), x=0, y=-20, text='NOT COURAGE. THE LOTTERY', sz=42),
                 E('plate', c('дёшево'), x=0, y=170, text='TRY CHEAPLY', sz=80, rot=-3)],
     anim=['net', 'razgovor'])
shot(c('Первое') - 0.2, 'L', [E('plate', c('Первое'), x=0, y=-340, text='1.  ONE-MONTH EXPERIMENT', sz=52),
                              E('card', c('дизайнером'), x=-270, y=-180, text='"I\'LL BE A DESIGNER"', sz=36), E('crossline', c('логотипа'), x=-270, y=-180, w=380),
                              E('plate', c('логотипа'), x=270, y=-180, text='3 LOGOS FOR FRIENDS', sz=36),
                              E('card', c('кафе'), x=-270, y=-40, text='"I\'LL OPEN A CAFÉ"', sz=36), E('crossline', c('субботы'), x=-270, y=-40, w=320),
                              E('plate', c('субботы'), x=270, y=-40, text='2 SATURDAYS AT A COFFEE SHOP', sz=36),
                              E('emoji', c('Месяц'), x=-300, y=170, ch='📅', size=140),
                              E('dark', c('фантазия'), x=90, y=170, text='AN ANSWER, NOT A FANTASY', sz=44)],
     anim=['ukazyvaet-vverh', 'obyasnyaet'])
shot(c('Второе') - 0.2, 'R', [E('plate', c('Второе'), x=0, y=-340, text="2.  TALK TO SOMEONE WHO'S THERE", sz=44),
                              E('emoji', c('Поговори'), x=0, y=-200, ch='💬', size=130),
                              E('card', c('вторник'), x=0, y=-50, text='WHAT DOES THEIR TUESDAY LOOK LIKE?', sz=48),
                              E('emoji', c('отпуск'), x=-250, y=110, ch='🏝️', size=130), E('strike', c('картинка'), x=-250, y=110, w=130, h=130),
                              E('plate', c('вторник', 1), x=230, y=110, text='TUESDAY', sz=50),
                              E('dark', c('сэкономил'), x=0, y=270, text='YEARS SAVED', sz=48)],
     anim=['razgovor', 'razgovor-zhesty'])
shot(c('Третье') - 0.2, 'L', [E('plate', c('Третье'), x=0, y=-340, text='3.  THE 2-OUT-OF-3 RULE', sz=56),
                              E('card', c('интересно'), x=-60, y=-190, text='INTERESTING?', sz=42), E('check', c('интересно') + 0.4, x=280, y=-190),
                              E('card', c('получалось'), x=-60, y=-70, text='GETTING GOOD?', sz=42), E('check', c('получалось') + 0.4, x=280, y=-70),
                              E('card', c('платить'), x=-60, y=50, text='WOULD SOMEONE PAY?', sz=42), E('strike', c('платить') + 0.4, x=280, y=50, w=70, h=70),
                              E('plate', c('копай'), x=0, y=200, text='2 YESES → KEEP DIGGING', sz=50, rot=-2),
                              E('dark', c('следующий'), x=0, y=320, text='1 YES → NEXT EXPERIMENT', sz=36)],
     anim=['obyasnyaet', 'kivok'])
shot(c('четвёртое') - 0.2, 'R', [E('plate', c('четвёртое'), x=0, y=-340, text='4.  WRITE IT DOWN', sz=56),
                                 E('emoji', c('Записывай'), x=-260, y=-170, ch='📓', size=150),
                                 E('card', c('понравилось'), x=140, y=-210, text='WHAT YOU LIKED', sz=38),
                                 E('dark', c('бесило'), x=140, y=-110, text='WHAT DROVE YOU CRAZY', sz=38),
                                 E('emoji', c('карта'), x=0, y=90, ch='🗺️', size=170),
                                 E('red', c('горячо'), x=-280, y=90, text='WARM', sz=44, rot=-4),
                                 E('dark', c('холодно'), x=280, y=90, text='COLD', sz=44, rot=4)],
     anim=['razgovor', 'ukazyvaet-vbok'])
shot(c('большинство') - 0.2, 'C', [E('cross', c('большинство') - 0.2, x=0, y=420, r=820, sz=30, alive_to=0.3, alive_t=c('вычеркнутая')),
                                   E('dark', c('провалятся'), x=-560, y=-300, text='MOST WILL FAIL', sz=40),
                                   E('plate', c('вычеркнутая'), x=-560, y=-170, text='FAILURE = A ROAD\nCROSSED OFF', sz=44, rot=-3),
                                   E('counter', c('девяносто') - 0.1, c('девяносто', 1) - 0.1, v0=100, v1=99, x=560, y=-260, sz=180, dur=0.4),
                                   E('counter', c('девяносто', 1) - 0.1, v0=99, v1=98, x=560, y=-260, sz=180, dur=0.4),
                                   E('card', c('меньше'), x=560, y=-90, text='THE CROSSROADS SHRINKS', sz=40)],
     anim=['pozhimaet-plechami', 'razgovor'], s=0.78)

# ---------- 9. финал ----------
c = lambda s, k=0: wt(9, s, k)
IT = [('выращивают', 'PASSION IS GROWN'), ('одну', '100 ROADS → TRY ONE'), ('повторять', "DON'T REPEAT YOUR 20s"),
      ('чужие', "MANY DREAMS AREN'T YOURS"), ('отдохни', 'WANT NOTHING → REST'), ('отговорка', '"TOO LATE" IS AN EXCUSE'), ('после', 'INTEREST COMES AFTER YOU START')]
els = [E('plate', c('подведём'), x=0, y=-370, text='RECAP', sz=50)]
for k, (w, tx) in enumerate(IT):
    y = -270 + k * 88; ta = c(w) - 0.3
    els += [E('check', ta + 0.2, x=-380, y=y, s=44), E('card', ta, x=30, y=y, text=tx, sz=34)]
shot(None, 'R', els, anim=['razgovor', 'kivok', 'razgovor'])
shot(c('главное') - 0.2, 'L', [E('plate', c('обязан'), x=0, y=-200, text="YOU DON'T HAVE TO KNOW", sz=64),
                               E('card', c('Никто'), x=0, y=-50, text='NOBODY DOES', sz=50),
                               E('dark', c('раньше'), x=0, y=100, text='THE SURE ONES JUST STARTED SOONER', sz=40)],
     anim=['dyhanie', 'kivok'])
shot(c('План') - 0.2, 'R', [E('plate', c('План'), x=0, y=-330, text='YOUR PLAN FOR TODAY', sz=72),
                            E('card', c('Запиши'), x=0, y=-180, text='1.  WRITE DOWN 3 THINGS', sz=48),
                            E('card', c('выбери'), x=0, y=-60, text='2.  PICK ONE FOR A MONTH', sz=48),
                            E('dark', c('идеальное'), x=0, y=70, text='NOT THE PERFECT ONE. ANY ONE.', sz=46),
                            E('emoji', c('комментариях'), x=-260, y=240, ch='💬', size=130),
                            E('plate', c('комментариях'), x=80, y=240, text='WHAT DID YOU PICK?', sz=50)],
     anim=['ukazyvaet-vverh', 'obyasnyaet', 'mashet'])
TFIN = c('потерялся') - 0.3
shot(TFIN, 'C', [E('cross', TFIN, x=0, y=420, r=820, sz=30, alive=0.3, alive_to=0.0, alive_t=TFIN + 0.5, hi=18),
                 E('txt', c('потерялся'), c('тупи') - 0.4, x=-560, y=-280, text="you're not lost", sz=54),
                 E('dark', c('долго'), c('тупи') - 0.4, x=560, y=-280, text="YOU'VE BEEN STANDING\nSTILL TOO LONG", sz=44),
                 E('plate', c('тупи') - 0.15, x=0, y=-390, text="THAT'S IT. DON'T BE DUMB.", sz=90, rot=-3)],
     anim=['dyhanie'], s=0.78)

# первый шот каждой главы начинается в паузе перед ней
_ch = 0
for sh in SHOTS:
    if sh['t'] is None:
        _ch += 1; sh['t'] = O[_ch] - GAP
for a, b in zip(SHOTS, SHOTS[1:]): assert a['t'] < b['t'], (a['t'], b['t'], b['els'][0])
