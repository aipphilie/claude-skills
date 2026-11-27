"""Видеоряд «Вы даже не встречались» на движке «Автокредита»."""
from base_k import *
import argparse
import engine
from pathlib import Path

WORK = Path(__file__).resolve().parent
G = 1288
TAN, LEATHER, GOLD = (229,198,142), (161,110,64), (246,181,49)
PAPER, CREAM, SKY = (255,251,235), (246,232,195), (207,227,237)
SEA, DARKSEA, PINK = (113,172,189), (70,133,153), (239,143,159)
A = ImageDraw.Draw
SCHEDULE = {}


def word(key):
    return SCHEDULE[key]


def heading(C, u, text, color=INK, size=110, y=374):
    size = size * min(1, 820 / text_img(text, size).width)
    slam(C, u + .12, text, 540, y, size, color)


def banner(C, u, text, y=514, size=82, bg=YEL, fg=INK, rot=0):
    size = size * min(1, 760 / text_img(text, size).width)
    plate(C, u+.12, text, 540, y, size, bg, fg, rot, mode='pop')


@lru_cache(96)
def case_image(opening):
    im = Image.new('RGBA',(666,560))
    d=A(im)
    lift=round(225*opening/20)
    d.ellipse((49,479,637,536),fill=(125,108,80,65))
    d.rounded_rectangle((65,240-lift,602,473),35,fill=TAN,outline=INK,width=10)
    d.rounded_rectangle((83,254-lift,584,414-lift),26,fill=LEATHER,outline=INK,width=7)
    for j in range(9):
        x=111+j*51
        d.line((x,285-lift,x+21,304-lift),fill=(197,150,99),width=4)
    d.rounded_rectangle((62,376,610,497),26,fill=LEATHER,outline=INK,width=10)
    d.rounded_rectangle((74,387,598,472),20,fill=GOLD,outline=INK,width=5)
    for x in (151,485):
        d.rounded_rectangle((x,380,x+47,454),8,fill=TAN,outline=INK,width=5)
        d.rectangle((x+13,412,x+34,435),fill=INK)
    d.rounded_rectangle((267,475,403,522),18,fill=INK)
    d.rounded_rectangle((284,474,386,505),12,fill=LEATHER)
    put(im,plate_img('НАШИ ВОСПОМИНАНИЯ',30,CREAM,INK,pad=11,r=8,border=INK,bw=3),337,445)
    return im


def suitcase(C,x,y,k=1,s=1,rot=0):
    put(C,case_image(max(0,min(20,round(k*20)))),x,y,s,rot)


@lru_cache(1)
def key_image():
    im=Image.new('RGBA',(410,255))
    d=A(im)
    d.ellipse((15,27,185,197),fill=GOLD,outline=INK,width=10)
    d.ellipse((39,52,160,173),outline=YEL,width=8)
    d.polygon(((164,84),(378,84),(395,109),(361,151),(337,151),(337,174),(310,174),(310,151),(280,151),(280,170),(254,170),(254,152),(166,152)),fill=GOLD,outline=INK,width=8)
    d.line((180,104,377,104),fill=YEL,width=7)
    d.ellipse((64,77,132,145),fill=PAPER,outline=INK,width=8)
    d.arc((41,59,151,173),30,160,fill=(255,235,160),width=5)
    return im


@lru_cache(1)
def ticket_image():
    im=Image.new('RGBA',(465,230))
    d=A(im)
    d.rounded_rectangle((10,12,450,204),24,fill=SKY,outline=INK,width=8)
    for y in range(24,190,19): d.line((349,y,349,y+8),fill=INK,width=4)
    d.ellipse((41,45,151,155),fill=YEL,outline=INK,width=5)
    d.polygon(((55,132),(77,105),(102,133),(121,116),(143,139),(143,146),(55,146)),fill=SEA)
    d.line((208,135,305,135),fill=INK,width=5)
    d.line((208,148,280,148),fill=INK,width=3)
    txt(im,'К МОРЮ',250,81,56)
    txt(im,'02',402,106,46)
    return im


@lru_cache(5)
def photograph(back=False,empty=False):
    im=Image.new('RGBA',(370,414))
    d=A(im)
    d.rounded_rectangle((9,7,359,405),17,fill=PAPER,outline=INK,width=8)
    if back:
        for y in range(96,347,59): d.line((45,y,323,y),fill=(213,200,168),width=4)
        return im
    d.rounded_rectangle((33,31,335,319),13,fill=(211,225,237),outline=INK,width=5)
    for x,y,r in ((64,90,5),(291,68,7),(111,61,8),(304,187,4),(168,129,5),(60,209,6)):
        d.ellipse((x-r,y-r,x+r,y+r),fill=WHITE)
    d.polygon(((178,96),(107,231),(248,231)),fill=(98,145,125),outline=INK,width=4)
    for dx,dy in ((0,112),(-22,170),(26,172)):
        d.ellipse((175+dx-6,dy-6,175+dx+6,dy+6),fill=YEL)
    for x,color in ((120,INK),(238,(150,152,154) if empty else INK)):
        d.ellipse((x-36,149,x+36,221),fill=color)
        d.rounded_rectangle((x-25,227,x+25,316),19,fill=color)
    if empty:
        d.rounded_rectangle((198,138,281,320),25,outline=PAPER,width=5)
        d.line((206,298,269,163),fill=PAPER,width=5)
    txt(im,'31 ДЕКАБРЯ',185,362,40)
    return im


def memories(C,u,which='all'):
    suitcase(C,550,1166,eo(u/.45),.86)
    props=[(key_image(),293,824,-20),(ticket_image(),739,755,13),(photograph(),681,968,-13)]
    for j,(im,x,y,rot) in enumerate(props):
        if which!='all' and which!=j: continue
        k=eo((u-j*.075)/.5)
        put(C,im,lerp(550,x,k),lerp(1170,y,k)-95*math.sin(k*math.pi),.58+.20*k,rot*k)


def lock(C,u,large=False):
    d=A(C)
    x0,y0,x1,y1=(339,586,741,1281) if not large else (152,537,924,1350)
    d.rounded_rectangle((x0+24,y0+31,x1+24,y1+31),31,fill=(211,187,147))
    d.rounded_rectangle((x0,y0,x1,y1),31,fill=TAN,outline=INK,width=12)
    d.rounded_rectangle((x0+32,y0+43,x1-32,y1-49),22,outline=LEATHER,width=10)
    for y in range(y0+89,y1-67,54):
        d.arc((x0+52,y-25,x1-39,y+57),12,166,fill=(205,161,104),width=3)
    d.rounded_rectangle((432,762,648,1002),37,fill=GOLD,outline=INK,width=9)
    d.ellipse((505,802,575,872),fill=INK)
    d.polygon(((520,850),(560,850),(575,938),(505,938)),fill=INK)
    d.ellipse((446,775,464,793),fill=INK)
    d.ellipse((617,971,635,989),fill=INK)
    if not large:
        k=eo(u/.52)
        put(C,key_image(),lerp(230,470,k),lerp(944,851,k),.66,15-15*k)


def cup(C,x,y,s=1,steam=0):
    d=A(C)
    def xy(l,t,r,b): return (x+l*s,y+t*s,x+r*s,y+b*s)
    d.ellipse(xy(-92,35,102,77),fill=(176,148,98))
    d.ellipse(xy(23,-14,91,45),fill=CREAM,outline=INK,width=max(2,round(5*s)))
    d.ellipse(xy(42,-3,73,33),fill=TAN,outline=INK,width=max(2,round(4*s)))
    d.polygon([(x-65*s,y-22*s),(x+57*s,y-22*s),(x+43*s,y+52*s),(x-43*s,y+52*s)],fill=CREAM,outline=INK,width=max(2,round(5*s)))
    d.ellipse(xy(-66,-46,58,-5),fill=PAPER,outline=INK,width=max(2,round(5*s)))
    d.ellipse(xy(-52,-34,44,-15),fill=(109,62,38))
    if steam:
        for j in range(3):
            pts=[(x+(j-1)*24*s+10*math.sin(k*.25+steam*7+j),y-39*s-k*2*s) for k in range(12,41)]
            d.line(pts,fill=(243,229,196),width=max(2,round(6*s)))


def home_room(C,u,cloth=0):
    d=A(C)
    d.rounded_rectangle((114,639,970,1296),41,fill=(248,239,213),outline=(215,201,169),width=5)
    d.rounded_rectangle((368,689,712,924),14,fill=SKY,outline=INK,width=7)
    d.ellipse((596,723,664,792),fill=YEL)
    d.line((540,691,540,922),fill=INK,width=8)
    d.line((369,802,709,802),fill=INK,width=8)
    for x,y,h in ((105,973,128),(929,948,162)):
        d.rounded_rectangle((x-27,y+94,x+26,y+151),9,fill=LEATHER,outline=INK,width=4)
        d.line((x,y+99,x,y-h/3),fill=(89,126,76),width=6)
        for i in range(4):
            dy=i*23
            d.ellipse((x-49,y+dy-23,x+45,y+dy),fill=(142,171,110),outline=(96,125,77),width=3)
    man(C,'reach' if cloth else 'sit',u,306,1252,.46)
    man(C,'g_sit',u+.2,780,1252,.45)
    d.line((392,1123,365,1298),fill=INK,width=15)
    d.line((685,1123,719,1296),fill=INK,width=15)
    d.ellipse((238,1030,840,1185),fill=LEATHER,outline=INK,width=6)
    d.ellipse((238,1008,840,1159),fill=TAN,outline=INK,width=7)
    if cloth:
        x=round(283+405*eo(u/.48))
        pts=[(x,1046),(x+388,1026),(x+467,1130),(x+35,1199)]
        d.polygon(pts,fill=SKY,outline=INK,width=5)
        for j in range(5):
            d.line((x+22+j*67,1057,x+63+j*73,1172),fill=(171,203,220),width=3)
    cup(C,403,1047,.83,u+.2)
    cup(C,679,1036,.81,u+.4)


def lounger(C,x,y,s=1):
    d=A(C)
    pts=[(x+ax*s,y+ay*s) for ax,ay in ((-183,-120),(-110,-25),(184,-25),(135,40),(-112,39),(-216,-89))]
    d.polygon(pts,fill=YEL,outline=INK,width=max(2,round(7*s)))
    for i in range(3):
        d.line((x-87*s,(y-15*s)+i*14*s,x+150*s,(y-15*s)+i*14*s),fill=GOLD,width=max(2,round(5*s)))
    d.line((x-111*s,y+31*s,x-149*s,y+78*s),fill=INK,width=round(12*s))
    d.line((x+123*s,y+32*s,x+150*s,y+76*s),fill=INK,width=round(12*s))


def beach_room(C,u,zoom=0):
    d=A(C)
    d.rectangle((0,0,1080,1920),fill=SKY)
    d.ellipse((747,549,955,757),fill=YEL)
    for j in range(3):
        x=95+j*100+round(19*u)
        d.ellipse((x,662-j*34,x+170,709-j*34),fill=(234,245,245))
    d.rectangle((0,796,1080,1313),fill=SEA)
    d.polygon([(x,round(971+26*math.sin(x/109+u*4))) for x in range(0,1130,40)]+[(1080,1920),(0,1920)],fill=CREAM)
    for j in range(3):
        y=842+j*47
        d.line([(x,y+13*math.sin(x/116+u*3+j)) for x in range(0,1130,27)],fill=(236,247,239),width=8 if j==2 else 4)
    x=243
    d.line((x,971,x-17,1318),fill=LEATHER,width=14)
    d.pieslice((x-159,828,x+164,1020),182,360,fill=PINK,outline=INK,width=4)
    d.line((x-100,913,x+104,913),fill=INK,width=4)
    lounger(C,405,1178,.7)
    lounger(C,793,1233,.69)
    if zoom:
        man(C,'g_walk',u,lerp(780,510,eo(u/.82)),1114,.45)
    else:
        man(C,'walkR',u,lerp(527,737,eo(u/1.4)),1160,.52)


def screen(C,u,message=None,mini=False):
    d=A(C)
    x,y,w,h=269,568,542,762
    k=eo(u/.42)
    if mini:
        x,y=round(269+31*(1-k)),round(568+92*(1-k))
    d.rounded_rectangle((x+24,y+22,x+w+24,y+h+22),50,fill=(212,203,180))
    d.rounded_rectangle((x,y,x+w,y+h),50,fill=INK)
    d.rounded_rectangle((x+13,y+45,x+w-13,y+h-14),36,fill=(237,240,231))
    d.rounded_rectangle((x+205,y+16,x+339,y+27),7,fill=(105,104,98))
    txt(C,'ПЕРЕПИСКА',540,y+115,50)
    d.line((x+29,y+165,x+w-29,y+165),fill=(200,199,182),width=4)
    for j in range(3):
        cy=y+236+j*72
        d.rounded_rectangle((x+49+(j%2)*61,cy,x+424-(j%2)*40,cy+44),12,fill=(218,224,208))
    if message:
        bubble_y=y+455+round(63*(1-eo(u/.22)))
        d.rounded_rectangle((x+37,bubble_y,x+w-35,bubble_y+149),25,fill=YEL,outline=INK,width=7)
        txt(C,'Надо бы как-нибудь',540,bubble_y+47,46)
        txt(C,'увидеться',540,bubble_y+105,48)
    else:
        for j in range(3):
            r=10+round(3*math.sin(u*20+j))
            xx=500+j*44
            d.ellipse((xx-r,y+519-r,xx+r,y+519+r),fill=(172,177,156))


def objects(C,u,large):
    if large==0:
        put(C,key_image(),540,868,.80+eo(u/.3)*.55,-12+13*eo(u/.38))
    if large==1:
        put(C,ticket_image(),622,997,.90,17)
        put(C,ticket_image(),505,883,.97+eo(u/.31)*.26,-18+14*eo(u/.50))
    if large==2:
        put(C,photograph(),543,892,1.02+eo(u/.35)*.31,11-20*eo(u/.36))


def scattered(C,u):
    for j,im in enumerate((key_image(),ticket_image(),photograph())):
        k=eo((u-j*.06)/.34)
        put(C,im,216+j*324,886-85*math.sin(k*math.pi),(.67+.08*j)*k,(-17+17*j))
    suitcase(C,540,1190,1,.63)


def card(C,u,cue):
    # Каждая сцена получает собственное действие и позу, а переход ведёт к следующему предмету.
    if cue=='hook':
        heading(C,u,'ВЫ ДАЖЕ',size=150)
        banner(C,u-.05,'НЕ ВСТРЕЧАЛИСЬ',size=111,rot=-4)
        man(C,'reach',u,321,1263,.57)
        suitcase(C,637,1090,eo(u/.42),.87,3-3*eo(u/.4))
        if u>.48: memories(C,u-.48)
    elif cue=='pain':
        burst(C,550,891,278,u*.2,16,CREAM)
        man(C,'shock',u,540,1290,.74)
        banner(C,u,'ЧЁ ТАК БОЛЬНО?',416,110,rot=-4)
        heart(C,782,854,95,HRT,12,1)
    elif cue=='suitcase':
        memories(C,u)
        man(C,'reach',u,309,1273,.52)
        heading(C,u,'ПО ЧЕМУ СКУЧАЕШЬ?',size=106)
    elif cue in ('keys','tickets','photo'):
        props={'keys':(0,'КЛЮЧИ ОТ КВАРТИРЫ'),'tickets':(1,'БИЛЕТЫ НА МОРЕ'),'photo':(2,'ФОТКА С НОВОГО ГОДА')}
        index,text=props[cue]
        heading(C,u,text)
        objects(C,u,index)
    elif cue in ('stamp','none'):
        scattered(C,u+.3)
        stamp(C,u+.08,'НЕ БЫЛО',540,855,152,RED,-13)
        heading(C,u,'А ВОТ И ПОДВОХ' if cue=='stamp' else 'ЭТОГО НЕ БЫЛО',size=110)
    elif cue=='lock':
        lock(C,u,True)
        heading(C,u,'А В ГОЛОВЕ…',size=112)
    elif cue in ('breakfast','cloth'):
        home_room(C,u,cue=='cloth')
        if cue=='breakfast': heading(C,u,'УТРО. ВЫ ВДВОЁМ.',size=103)
        else:
            banner(C,u,'КТО УКРАЛ ОДЕЯЛО?',466,82,rot=-3)
    elif cue in ('beach','water'):
        beach_room(C,u,cue=='water')
        if cue=='beach': heading(C,u,'МОРЕ.',size=155)
        else: banner(C,u,'КРАСИВО, ДА?',404,97)
    elif cue in ('phone','message'):
        screen(C,u,cue=='message',cue=='phone')
        heading(C,u,'ОТКРОЙ ЧАТ' if cue=='phone' else 'ВОТ И ВЕСЬ ЧАТ',size=102)
    elif cue=='gap':
        screen(C,.8,True)
        banner(C,u,'ОДНА ФРАЗА',407,105,rot=-3)
        for j in range(3):
            strike(C,u-j*.08,226,881+j*36,165,872+j*40,LEATHER,5)
    elif cue=='home':
        home_room(C,u)
        heading(C,u,'ЦЕЛАЯ ЖИЗНЬ',size=123)
        for j,im in enumerate((key_image(),ticket_image(),photograph())):
            k=back((u-j*.08)/.35)
            put(C,im,[210,534,861][j],617,.39*k,(-15+15*j)*k)
    elif cue in ('fold','lost'):
        suitcase(C,549,1130,1-eo(u/.72) if cue=='fold' else 0,.91)
        man(C,'hold',u,329,1270,.59)
        if cue=='fold':
            for j,im in enumerate((key_image(),ticket_image(),photograph())):
                k=eo((u-j*.07)/.64)
                put(C,im,lerp(248+j*281,550,k),lerp(723+j*63,1072,k),.65*(1-k),(-13+17*j)*(1-k))
        else:
            heading(C,u,'И ЭТУ ЖИЗНЬ ТОЖЕ',size=101)
            put(C,photograph(False,True),747,759,.69,-7,.82)
    elif cue=='hurt':
        man(C,'hold',u,440,1320,.73)
        put(C,photograph(False,True),688,825,.87,-12)
        banner(C,u,'ПО НЕЙ ТОЖЕ БОЛЬНО',423,76)
    elif cue=='stop':
        man(C,'stop',u,540,1290,.74)
        banner(C,u,'СТОП.',392,160,rot=-4)
        heading(C,u-.1,'ТУТ ТЫ ТУПИШЬ.',size=100,y=557)
    elif cue in ('turn','ask','need'):
        man(C,'flip' if cue=='turn' else 'hold',u,282,1295,.53)
        if cue=='turn':
            k=eo(u/.65); scale=max(.03,abs(math.cos(k*math.pi)))
            im=photograph(k>=.5).resize((max(1,round(370*scale)),414))
            put(C,im,664,913,1.07,-10+20*k)
            heading(C,u,'ПЕРЕВЕРНИ ФОТКУ',size=106)
        else:
            put(C,photograph(True),653,910,1.13,-5)
            text='ЧЕГО НЕ ХВАТАЕТ?' if cue=='ask' else 'ХОЧУ, ЧТОБЫ МЕНЯ ЖДАЛИ'
            banner(C,u,text,409,85,rot=-4)
            if cue=='need':
                for j,v in enumerate(('Я ХОЧУ,','ЧТОБЫ МЕНЯ','ДОМА ЖДАЛИ.')):
                    if u>.06+j*.13: txt(C,v,654,806+j*72,42,INK,rot=-5)
    elif cue=='door':
        lock(C,u,False)
        man(C,'g_sit',u,783,1269,.53)
        banner(C,u,'ЧТОБЫ ЖДАЛИ ДОМА?',413,82)
    elif cue=='joke':
        screen(C,u,False,True)
        for j in range(3):
            k=back((u-j*.08)/.22)
            put(C,plate_img(('ХА','ХА','ХА!')[j],77,YEL,INK,pad=18,r=20,border=INK),426+j*120,1060-j*81,k,-13+j*11)
        heading(C,u,'КОМУ КИНУТЬ ШУТКУ?',size=103)
    elif cue=='step':
        stamp(C,u,'С ЭТИМ МОЖНО',540,842,107,INK,-6)
        banner(C,u-.1,'ЧТО-ТО СДЕЛАТЬ',1030,100)
        man(C,'point',u,325,1330,.47)
    elif cue=='mate':
        man(C,'call',u,428,1300,.76)
        for i in range(3):
            r=50+i*32+10*math.sin(u*9-i)
            A(C).arc((700-r,832-r,700+r,832+r),-49,48,fill=LEATHER,width=7)
        heading(C,u,'НАБЕРИ СВОЕГО',size=112)
        banner(C,u-.06,'КЕНТА',523,108,rot=-3)
    elif cue=='leave':
        k=eo(u/.55)
        suitcase(C,545,1090+170*k,0,.83,7*(1-k))
        man(C,'walkR',u,lerp(356,624,k),1304,.61)
    elif cue=='end':
        man(C,'walkR',u,lerp(311,831,eo(u/1.5)),1271,.56)
        suitcase(C,357,1227,0,.58)
        heading(C,u,'ВСЁ.',size=163)
        banner(C,u-.08,'НЕ ТУПИ.',544,141,rot=-4)
    else:
        raise KeyError(cue)


TRANSITIONS={
 'hook':('none',None,'hit'), 'pain':('shake',None,'boom'), 'suitcase':('drop',None,'fall'),
 'keys':('whipL',None,'key'), 'tickets':('whipR',None,'swipe'), 'photo':('zoom',None,'snapshot'),
 'stamp':('shake',None,'hit'), 'none':('cut',None,'pop'), 'lock':('whipL',None,'key'),
 'breakfast':('zoomthru',(540,855),'swish'), 'cloth':('cut',None,'swipe'), 'beach':('clothwipe',None,'swish'),
 'water':('cut',None,'wave'), 'phone':('screenfold',None,'reverse'), 'message':('cut',None,'message'),
 'gap':('zoom',None,'click'), 'home':('door',None,'swish'), 'fold':('drop',None,'fall'),
 'lost':('cut',None,'click'), 'hurt':('whipL',None,'pop'), 'stop':('shake',None,'hit'),
 'turn':('whipR',None,'swipe'), 'ask':('zoom',None,'pop'), 'door':('door',None,'swish'),
 'joke':('cut',None,'message'), 'need':('drop',None,'click'), 'step':('cut',None,'pop'),
 'mate':('whipL',None,'message'), 'leave':('cut',None,'fall'), 'end':('bodywipe',None,'final'),
}


def load_shots():
    source=json.loads((WORK/'align2.json').read_text())
    content=''.join(source['characters'])
    chars=source['character_start_times_seconds']
    rows=json.loads((WORK/'scenariy.json').read_text())
    result=[]
    cursor=0
    for i,(key,_,line) in enumerate(rows):
        pos=content.index(line,cursor)
        cursor=pos+len(line)
        t=max(0,chars[pos]-.035) if i else 0.0
        tr,p,sfx=TRANSITIONS[key]
        SCHEDULE[key]=t
        result.append({'t':t,'fn':(lambda C,u,tt,k=key:card(C,u,k)),'tr':tr,'p':p,'sfx':sfx,'name':key})
    return result


def covers(out):
    for name in ('a','b'):
        c=Image.new('RGBA',(CW,CH),CARD+(255,))
        if name=='a':
            title='ЭТОГО НЕ БЫЛО'
            put(c,photograph(False,True),644,884,1.42,-7)
            man(c,'hold',.08,270,1340,.70)
        else:
            title='ЧЁ ТАК БОЛЬНО?'
            scattered(c,.95)
            man(c,'reach',.15,335,1280,.52)
        heading(c,1,title,size=141,y=373)
        banner(c,1,'ВЫ ДАЖЕ НЕ ВСТРЕЧАЛИСЬ',597,73,rot=-3)
        c.convert('RGB').save(out/f'nebylo-oblozhka-{name}.png',optimize=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sheet',action='store_true')
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--end',type=int)
    parser.add_argument('--output',type=Path,default=WORK/'silent.mp4')
    args=parser.parse_args()
    engine.SHOTS=load_shots()
    duration=round((END+.7)*FPS)
    if args.sheet:
        columns=6
        result=Image.new('RGB',(180*columns,320*math.ceil(len(engine.SHOTS)/columns)),CARD)
        for i,shot in enumerate(engine.SHOTS):
            end=engine.SHOTS[i+1]['t'] if i+1<len(engine.SHOTS) else END+.7
            t=shot['t']+min(.59,(end-shot['t'])*.62)
            result.paste(engine.frame(t).resize((180,320)),((i%columns)*180,(i//columns)*320))
        result.save(WORK/'sheet.jpg',quality=91)
        target=Path(os.environ.get('NETUPI_OUTPUT',str(WORK))); target.mkdir(parents=True,exist_ok=True)
        covers(target)
        return
    args.output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','-',
         '-c:v','libx264','-threads','3','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',str(args.output)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        for i in range(args.start,args.end if args.end is not None else duration):
            process.stdin.write(engine.frame(i/FPS).tobytes())
            if i%180==0: print(args.output.name,i,flush=True)
        process.stdin.close()
        if process.wait(): raise SystemExit('Video encoding failed')


if __name__=='__main__':
    main()
