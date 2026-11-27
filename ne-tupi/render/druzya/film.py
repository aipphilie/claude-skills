"""Сборка полного рилса из пословных таймингов и исходных 3D-кадров."""
import bisect
import json
import math
import re
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import fragment

WORK = fragment.WORK
W, H, FPS = fragment.W, fragment.H, fragment.FPS
PAPER, WHITE, INK, YELLOW = fragment.PAPER, fragment.WHITE, fragment.INK, fragment.YELLOW
BLUE, STONE, LINE = fragment.BLUE, fragment.STONE, fragment.LINE
WOOD, GREY = fragment.WOOD, fragment.GREY
box, line, label, shadow = fragment.box, fragment.line, fragment.label, fragment.shadow
bubble, person, ease, pop = fragment.bubble, fragment.person, fragment.ease, fragment.pop
PROJECT = fragment.PROJECT
OUT = fragment.OUT
OUT.mkdir(parents=True,exist_ok=True)
FRAGMENT_FRAMES = round(fragment.end*FPS)

INTRO = [
    ('cover',None), ('when','А когда'), ('memes','Мемы'), ('empty','А встретиться')]
TAIL = [
    ('guess',None), ('question','не хотят'), ('office','Один после'), ('tired','выжатый'),
    ('family','Второй'), ('waiting','Третий'), ('clock','предложит время'),
    ('four','И вот'), ('stare','ждёте'), ('blank','сама появится'),
    ('stop','Стоп'), ('compare','Сравни'), ('vague','«Когда'), ('silence','И тишина'),
    ('switch','А теперь'), ('day','четверг'), ('place','кофе'), ('send','Кто со'),
    ('accept','Могут'), ('coffee','Идите'), ('next','Кто свободен'), ('next_cup','следующий раз'),
    ('copy','Скопируй'), ('check','День'), ('outro','Всё')]

def timeline(section, plan):
    a=json.loads((WORK/f'{section}.json').read_text())
    s=''.join(a['characters'])
    starts,ends=a['character_start_times_seconds'],a['character_end_times_seconds']
    marks=[]
    cursor=0
    for name, anchor in plan:
        if anchor is None:
            marks.append((name,0.0))
            continue
        match=s.index(anchor,cursor)
        marks.append((name,round(starts[match]*FPS)/FPS))
        cursor=match+len(anchor)
    words=[(m.group(),starts[m.start()],ends[m.end()-1])
           for m in re.finditer(r'\S+',s) if not m.group().startswith('[')]
    groups=[]
    word_group=[]
    for word in words:
        word_group.append(word)
        if len(word_group)==4 or word[0].rstrip('»').endswith(('.', '!', '?', ':')):
            groups.append(word_group)
            word_group=[]
    if word_group:
        groups.append(word_group)
    return marks,groups,math.ceil((ends[-1]+(.53 if section=='tail' else .03))*FPS)

def title(d, value, y=358, size=88, bg=None):
    if bg is not None:
        width=fragment.font(size).getlength(value)+75
        box(d,(W-width)/2,y-size*.68,width,size*1.37,bg,18)
    label(d,540,y,value,size)

def phone(d,x=300,y=420,w=480,h=819):
    shadow(d,x,y,w,h,'#D2D4CA',42)
    box(d,x,y,w,h,INK,44)
    box(d,x+12,y+12,w-24,h-24,'#F9F9F3',35)
    box(d,x+w/2-63,y+31,126,13,INK,6)
    label(d,x+w/2,y+111,'ЧАТ ДРУЗЕЙ',48)

def avatars(d,x,y,active=0,n=4,step=169):
    for i in range(n):
        cx=x+i*step
        fill=YELLOW if i<active else '#E0E7E7'
        d.ellipse((cx-56,y-56,cx+56,y+56),fill=fill,outline=INK,width=4)
        d.ellipse((cx-18,y-25,cx+18,y+11),fill=INK)
        box(d,cx-31,y+15,62,25,INK,10)

def cup(d,x,y,color=YELLOW,scale=1.0):
    s=scale
    d.ellipse((x-89*s,y+51*s,x+98*s,y+82*s),fill='#C9B27E')
    d.ellipse((x+43*s,y-6*s,x+108*s,y+55*s),fill=color,outline=INK,width=5)
    d.ellipse((x+59*s,y+7*s,x+89*s,y+41*s),fill=WOOD,outline=INK,width=4)
    d.polygon(((x-66*s,y-11*s),(x+61*s,y-11*s),(x+46*s,y+63*s),(x-48*s,y+63*s)),fill=color,outline=INK,width=5)
    d.ellipse((x-67*s,y-34*s,x+62*s,y+6*s),fill='#FFF9E8',outline=INK,width=5)
    d.ellipse((x-48*s,y-23*s,x+43*s,y-7*s),fill='#694629')

def calendar(d,x,y,w,h,marked=False):
    shadow(d,x,y,w,h,'#D7CEB5',27)
    box(d,x,y,w,h,WHITE,34,INK)
    box(d,x,y,w,111,YELLOW,31,INK)
    for dx in (83,w-110):
        box(d,x+dx,y-38,26,78,INK,9)
    label(d,x+w/2,y+59,'КАЛЕНДАРЬ',51)
    for row in range(3):
        for col in range(4):
            xx=x+44+col*(w-64)/4
            yy=y+159+row*91
            box(d,xx,yy,83,66,YELLOW if marked and (row,col)==(1,2) else '#F2F0E6',12)
            if marked and (row,col)==(1,2):
                label(d,xx+41,yy+32,'ЧТ',32)

def paint(key,t,clock):
    colors={'memes':BLUE,'guess':BLUE,'family':'#F6EDCF','stare':BLUE,
            'vague':STONE,'switch':YELLOW,'day':'#FFF0A1','place':BLUE,'outro':YELLOW}
    im=Image.new('RGB',(W,H),colors.get(key,PAPER))
    d=ImageDraw.Draw(im)
    if key in ('cover','empty','when'):
        fragment.cafe(d,im,t,key!='when')
        if key=='cover':
            title(d,'ДРУЗЬЯ ЕСТЬ.',340,108)
            title(d,'ВСТРЕЧ НЕТ.',477,112,YELLOW)
        elif key=='empty':
            title(d,'А ВСТРЕЧА?',388,111,YELLOW)
        else:
            title(d,'КОГДА ВИДЕЛИСЬ?',400,88)
    elif key=='memes':
        phone(d,292,414,496,811)
        for i,(msg,at) in enumerate((('Это ты!',0.0),('Смотри до конца',.22),('Ахахах',.44))):
            if t>=at:
                x=326+round(95*(1-ease((t-at)/.23)))+(i%2)*30
                bubble(d,x,602+i*149,393-(i%2)*25,101,msg,i%2==0,30)
    elif key in ('guess','question'):
        d.ellipse((130,565,950,1364),fill='#E9E6D9')
        person(d,im,'cheshet-golovu' if key=='guess' else 'pozhimaet-plechami',clock,540,1333,666)
        title(d,'ОНИ НЕ ХОТЯТ?',402,92,YELLOW if key=='question' else None)
        if key=='question':
            label(d,822,739,'?',round(158*max(.2,pop(t/.24))),GREY)
    elif key in ('office','tired'):
        d.ellipse((92,574,988,1337),fill='#E7EBE5')
        d.polygon(((154,1116),(924,1116),(991,1195),(100,1195)),fill=WOOD,outline=INK,width=5)
        if key=='office':
            person(d,im,'dyhanie',clock,317,1113,460)
            shadow(d,564,797,271,176)
            box(d,564,797,271,176,INK,16)
            box(d,580,811,239,144,BLUE,9)
            d.polygon(((527,977),(866,977),(896,1010),(492,1010)),fill='#7E8384',outline=INK,width=4)
            label(d,699,888,'19:42',58)
            title(d,'ПОСЛЕ РАБОТЫ',411,88)
        else:
            person(d,im,'pozhimaet-plechami',clock,540,1111,540)
            box(d,318,1170,444,88,WHITE,22,INK)
            for i in range(3):
                box(d,342+i*127,1192,102,43,'#E2DED1',9)
            box(d,342,1192,73*(1-ease(t/.75)),43,'#D3A933',9)
            title(d,'ВЫЖАТЫЙ',413,108,YELLOW)
    elif key=='family':
        d.ellipse((110,616,970,1330),fill='#F2E6BC')
        person(d,im,'dyhanie',clock,478,1300,588)
        person(d,im,'pozhimaet-plechami',clock+.3,703,1296,287)
        for i in range(3):
            x=241+i*51
            box(d,x,1220-i*35,80,73,YELLOW if i%2 else '#C1D0D6',10,INK)
        title(d,'ДЕТИ',383,112)
    elif key in ('waiting','clock'):
        if key=='waiting':
            phone(d,298,475,484,778)
            avatars(d,414,750,0,3,124)
            for i in range(3):
                yy=878+round(14*math.sin(10*t+i*.8))
                d.ellipse((460+i*64,yy,479+i*64,yy+19),fill=GREY)
            title(d,'КТО ПРЕДЛОЖИТ?',361,76)
        else:
            d.ellipse((260,544,820,1104),fill=WHITE,outline=INK,width=11)
            d.ellipse((292,576,788,1072),outline=LINE,width=4)
            for q in range(12):
                ang=q*math.tau/12
                line(d,[(540+219*math.sin(ang),824-219*math.cos(ang)),(540+240*math.sin(ang),824-240*math.cos(ang))],INK,6)
            ang=1.5+6*t
            line(d,[(540,824),(540+209*math.sin(ang),824-209*math.cos(ang))],INK,9)
            line(d,[(540,824),(603,760)],INK,13)
            d.ellipse((521,805,559,843),fill=YELLOW,outline=INK,width=3)
    elif key in ('four','stare','blank'):
        if key=='four':
            title(d,'ЧЕТВЕРО ДРУЗЕЙ',411,87)
            count=min(4,int(t*5)+1)
            avatars(d,285,795,count)
            for i in range(count):
                label(d,285+i*169,943,'…',61,GREY)
        elif key=='stare':
            for i in range(4):
                x=174+(i%2)*377
                y=550+(i//2)*300
                box(d,x,y,329,267,'#F3F4F0',28,INK)
                avatars(d,x+165,y+99,0,1)
                label(d,x+165,y+209,'ЖДУ…',50,GREY)
        else:
            calendar(d,261,578,559,464)
            title(d,'ВСТРЕЧИ НЕТ',409,98)
    elif key=='stop':
        d.ellipse((165,610,915,1395),fill='#EFEBD9')
        person(d,im,'pozhimaet-plechami',clock,540,1378,560)
        title(d,'СТОП.',390,133,YELLOW)
        title(d,'ТУТ ТЫ ТУПИШЬ',532,79)
    elif key=='compare':
        title(d,'ДВА СООБЩЕНИЯ',391,84)
        for i in range(2):
            x=126+408*i
            box(d,x,583+round(55*(1-ease((t-i*.1)/.26))),378,591,WHITE if i==0 else YELLOW,30,INK)
            label(d,x+189,801,str(i+1),149)
            for q in range(3):
                line(d,[(x+86,938+q*44),(x+292-q*35,938+q*44)],GREY,6)
    elif key in ('vague','silence'):
        phone(d,269,481,540,769)
        bubble(d,296,741,487,99,'Когда вам удобно?',False,31)
        if key=='silence':
            for i in range(3):
                cy=932+round(10*math.sin(13*t+i))
                d.ellipse((471+i*58,cy,491+i*58,cy+20),fill=LINE)
            title(d,'ТИШИНА',388,100)
        else:
            title(d,'«КОГДА УДОБНО?»',394,80)
    elif key=='switch':
        for i in range(3):
            rr=120+i*137
            d.ellipse((540-rr,846-rr,540+rr,846+rr),outline='#F5C800',width=5)
        title(d,'А ТЕПЕРЬ ТАК',817,110)
    elif key=='day':
        calendar(d,268,560,543,452,True)
        title(d,'ЧЕТВЕРГ',401,115)
        title(d,'19:00',1137,113,YELLOW)
    elif key=='place':
        box(d,189,535,701,656,'#F4F3E6',44,INK)
        for i in range(5):
            x=251+i*130
            line(d,[(x,568),(x+38,1156)],'#DDDCCF',9)
            line(d,[(212,633+i*120),(863,601+i*122)],'#DDDCCF',9)
        r=ease(t/.43)
        d.ellipse((296,822,405,931),fill=BLUE,outline=INK,width=4)
        label(d,350,878,'М',63)
        line(d,[(405,874),(405+round(169*r),874),(405+round(261*r),857)],'#95907C',8)
        cup(d,680,842,YELLOW,.8)
        title(d,'КОФЕ У МЕТРО',391,95)
    elif key in ('send','accept','copy'):
        phone(d,252,462,576,833)
        box(d,285,689,510,288,YELLOW,24,INK)
        for i,msg in enumerate(('В четверг в семь,','кофе у метро.','Кто со мной?')):
            label(d,318,745+i*69,msg,37,display=False,anchor='lm')
        if key=='accept':
            bubble(d,325,1033-45*(1-ease(t/.29)),377,91,'Я могу!',False,40)
        elif key=='copy':
            title(d,'КИНЬ В ЧАТ',378,107)
            box(d,362,1071,352,86,INK,19)
            label(d,538,1114,'СКОПИРОВАТЬ',44,WHITE)
        else:
            title(d,'КТО СО МНОЙ?',387,95)
            rad=24+44*ease(t/.27)
            d.ellipse((752-rad,1037-rad,752+rad,1037+rad),outline='#E3C126',width=5)
            d.polygon(((733,1021),(774,1038),(732,1055),(744,1038)),fill=INK)
    elif key in ('coffee','next','next_cup'):
        d.ellipse((92,498,987,1417),fill='#EFEBDB')
        d.ellipse((183,951,897,1383),fill='#D0BE95')
        if key!='next_cup':
            person(d,im,'dyhanie',clock,316,1265,527)
            person(d,im,'dyhanie',clock+.59,756,1265,481)
        d.ellipse((219,1020,863,1228),fill=WOOD,outline=INK,width=7)
        cup(d,384,1071,'#FCF5E0',.85)
        cup(d,691,1065,YELLOW,.85)
        if key=='next_cup':
            cup(d,541,1151-70*(1-ease(t/.3)),'#D8E3E5',.76)
            title(d,'В СЛЕДУЮЩИЙ РАЗ',391,82)
        elif key=='next':
            bubble(d,357,610,380,94,'Я в другой раз',False,33)
        else:
            title(d,'ИДИТЕ ВДВОЁМ',395,93)
    elif key=='check':
        count=1+(t>.43)+(t>.97)
        for i,word in enumerate(('ДЕНЬ','ВРЕМЯ','МЕСТО')):
            y=572+i*196
            shadow(d,219,y,651,131)
            box(d,219,y,651,131,YELLOW if i<count else WHITE,25,INK)
            label(d,361,y+63,'✓' if i<count else '·',62,display=False)
            label(d,582,y+63,word,73)
    elif key=='outro':
        person(d,im,'dyhanie',clock,540,1343,561)
        title(d,'ВСЁ.',396,151)
        title(d,'НЕ ТУПИ.',553,128)
    else:
        raise ValueError(key)
    return im

def captions(im,groups,t):
    matches=[g for g in groups if g[0][1]<=t+.025]
    if not matches:
        return
    group=matches[-1]
    if t>group[-1][2]+.36:
        return
    d=ImageDraw.Draw(im)
    words=[row[0].upper() for row in group]
    fs=56
    while fragment.font(fs).getlength(' '.join(words))>819:
        fs-=1
    f=fragment.font(fs)
    wi=f.getlength(' '.join(words))
    x=(W-wi)/2
    box(d,x-22,1432,wi+44,92,PAPER,15)
    active=bisect.bisect_right([row[1] for row in group],t+.035)-1
    for i, word in enumerate(words):
        w=f.getlength(word)
        if i==active:
            box(d,x-5,1443,w+10,69,YELLOW,11)
        label(d,x,1478,word,fs,anchor='lm')
        x+=w+f.getlength(' ')

def section_frame(marks,groups,t):
    i=max(0,bisect.bisect_right([entry[1] for entry in marks],t)-1)
    key,start=marks[i]
    im=paint(key,t-start,t)
    captions(im,groups,t)
    return im

SOUNDS={'cover':('19-udar-final.mp3',.10),'memes':('04-pop.mp3',.10),'empty':('03-perehod-swipe.mp3',.09),
        'office':('43-vzhuh-bas-skleyka.mp3',.09),'family':('04-pop.mp3',.08),'clock':('28-tsik-bystro-a.mp3',.09),
        'four':('11-uvedomlenie.mp3',.055),'blank':('16-proval.mp3',.08),'stop':('05-klik.mp3',.11),
        'compare':('03-perehod-swipe.mp3',.09),'switch':('43-vzhuh-bas-skleyka.mp3',.09),
        'day':('04-pop.mp3',.081),'place':('04-pop.mp3',.075),'accept':('07-pravilno.mp3',.10),
        'coffee':('06-dzyn-insayt.mp3',.10),'check':('05-klik.mp3',.10),'outro':('19-udar-final.mp3',.11)}

def section_audio(section,marks,count):
    duration=count/FPS
    audio=np.zeros(round(duration*44100),np.float32)
    dry=fragment.pcm(WORK/f'{section}.mp3')
    audio[:min(len(dry),len(audio))]=dry[:len(audio)]*.96
    for key,time in marks:
        if key not in SOUNDS:
            continue
        name,gain=SOUNDS[key]
        s=fragment.pcm(PROJECT/'zvuki'/name)
        pos=round(time*44100)
        n=min(len(audio)-pos,len(s))
        audio[pos:pos+n]+=s[:n]*gain
    return audio

def main():
    intro,cap_intro,intro_count=timeline('intro',INTRO)
    tail,cap_tail,tail_count=timeline('tail',TAIL)
    fragment.mix()
    frag_audio=fragment.pcm(fragment.WORK/'fragment-mix.wav')[:round(FRAGMENT_FRAMES/FPS*44100)]
    all_audio=np.concatenate((section_audio('intro',intro,intro_count),frag_audio,section_audio('tail',tail,tail_count)))
    with wave.open(str(WORK/'full.wav'),'wb') as f:
        f.setparams((1,2,44100,0,'NONE','not compressed'))
        f.writeframes((np.clip(all_audio,-1,1)*32767).astype('<i2').tobytes())
    target=OUT/'druzya-est-vstrech-net.mp4'
    seq=[(intro,cap_intro,intro_count),(None,None,FRAGMENT_FRAMES),(tail,cap_tail,tail_count)]
    shots=[section_frame(intro,cap_intro,t+.24) for _,t in intro]
    shots.extend(fragment.draw(t+.24) for t in fragment.cut)
    shots.extend(section_frame(tail,cap_tail,t+.24) for _,t in tail)
    grid=Image.new('RGB',(180*7,320*math.ceil(len(shots)/7)),PAPER)
    for i,fr in enumerate(shots):
        grid.paste(fr.resize((180,320),Image.Resampling.LANCZOS),((i%7)*180,(i//7)*320))
    grid.save(WORK/'full-sheet.jpg',quality=92)
    paint('cover',.12,.28).save(OUT/'druzya-oblozhka-a.png',optimize=True)
    alt=paint('empty',.37,.69)
    d=ImageDraw.Draw(alt)
    d.rectangle((0,250,W,516),fill=PAPER)
    title(d,'НАДО УВИДЕТЬСЯ',354,77,YELLOW)
    alt.save(OUT/'druzya-oblozhka-b.png',optimize=True)
    command=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1080x1920',
             '-framerate',str(FPS),'-i','pipe:0','-i',str(WORK/'full.wav'),'-c:v','libx264','-threads','5',
             '-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',
             '-movflags','+faststart',str(target)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as f:
        for marks,captions_list,count in seq:
            for i in range(count):
                t=i/FPS
                im=fragment.draw(t) if marks is None else section_frame(marks,captions_list,t)
                f.stdin.write(im.tobytes())
        f.stdin.close()
        if f.wait():
            raise SystemExit('Video export failed')
    print(target, len(shots),'shots', (intro_count+FRAGMENT_FRAMES+tail_count)/FPS,'s')


if __name__=='__main__':
    main()
