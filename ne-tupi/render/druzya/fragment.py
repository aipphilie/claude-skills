import bisect
import os
import json
import math
import re
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parents[2]
WORK = Path(os.environ['NETUPI_WORK'])
ASSETS = WORK/'poses'
OUT = Path(os.environ['NETUPI_OUTPUT'])
OUT.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1080, 1920, 30
PAPER, WHITE, INK, YELLOW = '#FBFAF5', '#FFFFFF', '#151513', '#FFD60A'
BLUE, STONE, LINE = '#E6EEF1', '#EFEBDF', '#D8D0BC'
WOOD, OCHRE, GREY = '#DFCA96', '#AA8751', '#6F6B5F'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
DISPLAY = PROJECT/'render/kvartira/kod/fonts/Oswald-Bold.ttf'

@lru_cache(maxsize=50)
def font(size, display=True):
    return ImageFont.truetype(str(DISPLAY if display else SANS), size)

def label(d, x, y, value, size, fill=INK, display=True, anchor='mm'):
    d.text((round(x),round(y)),value,fill=fill,font=font(size,display),anchor=anchor)

def box(d, x, y, w, h, fill=WHITE, r=22, border=None, width=4):
    d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=border,width=width)

def line(d, xy, fill=INK, width=5):
    d.line(xy,fill=fill,width=width,joint='curve')

def ease(x):
    return 1-(1-max(0,min(1,x)))**3

def pop(x):
    x=max(0,min(1,x))
    return 1+2.7*(x-1)**3+1.7*(x-1)**2

def shadow(d,x,y,w,h,fill='#DEDACD',r=24):
    box(d,x+13,y+15,w,h,fill,r)

def bubble(d,x,y,w,h,msg,active=False,sz=49):
    shadow(d,x,y,w,h)
    box(d,x,y,w,h,YELLOW if active else WHITE,26,INK)
    label(d,x+28,y+h/2,msg,sz,display=False,anchor='lm')

def person(d, im, name, seconds, x, base, height):
    frames = sorted((ASSETS/name).glob('*.png'))
    n=int(max(0,seconds)*25)%len(frames)
    sprite=scaled_sprite(frames[n],height)
    im.paste(sprite,(round(x-sprite.width/2),round(base-height)),sprite)

@lru_cache(maxsize=72)
def scaled_sprite(path,height):
    with Image.open(path) as image:
        sprite=image.convert('RGBA')
    b=sprite.getchannel('A').point(lambda a: 255 if a>=60 else 0).getbbox()
    l,t,r,e=b
    sprite=sprite.crop((l-3,t-3,r+3,e+3))
    assert sprite.height >= height
    return sprite.resize((round(height*sprite.width/sprite.height),height),Image.Resampling.LANCZOS)

a=json.loads((WORK/'fragment.json').read_text())
words=[(m.group(),a['character_start_times_seconds'][m.start()],a['character_end_times_seconds'][m.end()-1])
       for m in re.finditer(r'\S+',''.join(a['characters'])) if not m.group().startswith('[')]
marks=[w[1] for w in words]
cut=[0,1.25,2.39,3.71,4.91,5.85,6.89]
end=8.17

def captions(d,t):
    i=max(0,bisect.bisect_right(marks,t+.025)-1)
    ranges=((0,4),(4,6),(6,9),(9,13),(13,16),(16,len(words)))
    s,e=next((s,e) for s,e in ranges if s<=i<e)
    chunk=[word.upper() for word,_,_ in words[s:e]]
    fs=55
    while font(fs).getlength(' '.join(chunk))>820:
        fs-=1
    f=font(fs)
    x=(W-f.getlength(' '.join(chunk)))/2
    box(d,x-18,1432,f.getlength(' '.join(chunk))+36,93,PAPER,14)
    for j,w in enumerate(chunk):
        wid=f.getlength(w)
        if j==i-s:
            box(d,x-6,1441,wid+12,72,YELLOW,10)
        label(d,x,1478,w,fs,anchor='lm')
        x+=wid+f.getlength(' ')

def cafe(d,im,t,wide):
    d.ellipse((74,518,987,1400),fill='#F0EDDF')
    d.ellipse((139,1321,949,1402),fill='#E1DCCE')
    line(d,[(309,584),(309,686)],'#ADA68E',3)
    d.polygon(((257,738),(276,675),(342,675),(362,738)),fill='#E3CE88',outline='#B6A45E',width=3)
    d.ellipse((257,726,362,745),fill='#FFF0B5',outline='#B6A45E',width=2)
    off=round(75*(1-ease(t/.38))) if wide else 0
    x=767+off
    for dx,dy in ((-48,-4),(81,17),(43,39)):
        line(d,[(x+dx,1180),(x+dx+dy,1371)],INK,10)
    box(d,x-67,941,157,159,'#D6A718',34,INK,5)
    box(d,x-73,929,157,157,YELLOW,34,INK,5)
    line(d,[(x-43,950),(x+48,950)],'#FFF4A7',4)
    d.polygon(((x-84,1159),(x+41,1134),(x+109,1177),(x-34,1205)),fill='#E6B019',outline=INK,width=4)
    d.polygon(((x-84,1159),(x-34,1205),(x+109,1177),(x+106,1198),(x-34,1223),(x-84,1176)),fill='#BF8F1D',outline=INK,width=4)

    if wide:
        person(d,im,'cheshet-golovu',.39+t,304,1378,505)
    else:
        person(d,im,'pozhimaet-plechami',.58+t,250,1373,576)

    line(d,[(559,1117),(539,1344)],INK,18)
    line(d,[(508,1353),(632,1353)],INK,10)
    d.ellipse((326,1114,755,1211),fill=OCHRE,outline=INK,width=5)
    d.ellipse((326,1091,755,1188),fill=WOOD,outline=INK,width=5)
    d.arc((347,1103,731,1182),8,163,fill='#FFF0BC',width=3)
    for xx,yy,col in ((440,1101,'#FAF5DE'),(635,1095,YELLOW)):
        d.ellipse((xx-50,yy+34,xx+56,yy+56),fill='#BCA478')
        d.ellipse((xx+27,yy-1,xx+67,yy+37),fill=col,outline=INK,width=3)
        d.ellipse((xx+39,yy+8,xx+57,yy+27),fill=WOOD,outline=INK,width=3)
        d.polygon(((xx-38,yy-9),(xx+37,yy-9),(xx+28,yy+39),(xx-28,yy+39)),fill=col,outline=INK,width=3)
        d.ellipse((xx-38,yy-21,xx+37,yy+4),fill='#FFF9E6',outline=INK,width=4)
        d.ellipse((xx-26,yy-14,xx+26,yy-3),fill='#684629')

def draw(t):
    k=bisect.bisect_right(cut,t)-1
    u=t-cut[k]
    back=(BLUE,PAPER,YELLOW,STONE,PAPER,PAPER,PAPER)[k]
    im=Image.new('RGB',(W,H),back)
    d=ImageDraw.Draw(im)
    if k==0:
        d.ellipse((78,417,997,1318),fill='#D5E4E9')
        xx=315
        y=416+round(70*(1-ease(u/.32)))
        shadow(d,xx,y,450,733,'#BDCACE',44)
        box(d,xx,y,450,733,INK,44)
        box(d,xx+11,y+12,428,706,'#F7F8F3',34)
        box(d,xx+178,y+32,94,11,INK,5)
        label(d,540,y+128,'ЧАТ ДРУЗЕЙ',57)
        for i,c in enumerate(('#FFD60A','#F0EDDE','#BBCDD8')):
            x=422+i*118
            d.ellipse((x-39,y+221,x+39,y+299),fill=c,outline=INK,width=4)
            d.ellipse((x-12,y+236,x+12,y+260),fill=INK)
            box(d,x-21,y+262,42,21,INK,8)
        for i,e in enumerate((.13,.38,.64)):
            if u<e:
                continue
            x=420+i*119
            yy=y+381-round(25*(1-ease((u-e)/.19)))
            d.ellipse((x-23,yy-23,x+23,yy+23),fill=YELLOW,outline=INK,width=3)
            line(d,[(x-10,yy),(x-2,yy+8),(x+12,yy-9)],INK,4)
        box(d,xx+40,y+579,370,67,'#ECEDE6',16)
        label(d,540,y+611,'Сообщение…',31,GREY,False)
    elif k==1:
        d.ellipse((100,564,980,1046),fill='#F1EDDF')
        for j in range(3):
            x=135+j*52
            box(d,x,754+j*32,644,104,'#ECE7D7',26)
        x=159-round(160*(1-ease(u/.25)))
        bubble(d,x,666,745,137,'Надо увидеться',False,64)
        for j in range(3):
            cy=956+round(12*math.sin(7*u+j))
            d.ellipse((440+j*84,cy,466+j*84,cy+26),fill=INK)
    elif k==2:
        d.ellipse((74,438,1004,1368),fill='#F8E36B')
        for i in range(3):
            y=853+i*49
            box(d,240-i*40,y,638+i*15,112,'#F7DB53',27)
        yy=655+round(85*(1-ease(u/.24)))
        bubble(d,155,yy,770,158,'Да, на неделе!',True,67)
        x=738+round(60*(1-ease(u/.35)))
        line(d,[(x,yy+190),(x+19,yy+210),(x+65,yy+152)],INK,12)
        line(d,[(x+48,yy+191),(x+65,yy+209),(x+112,yy+152)],INK,12)
    elif k==3:
        d.ellipse((78,459,994,1364),fill='#E7E0CF')
        for i in range(5):
            shadow(d,238+14*i,575+13*i,537,481,'#D6CCB1',29)
        box(d,235,548,548,515,WHITE,34,INK)
        box(d,235,548,548,118,YELLOW,33,INK)
        for xx in (347,654):
            box(d,xx,500,25,96,INK,10)
        label(d,509,611,'ПРОШЛО',61)
        tick=min(6,max(1,int(u*8)+1))
        label(d,505,795,str(tick),196)
        label(d,505,949,'МЕСЯЦЕВ' if tick>=5 else ('МЕСЯЦ' if tick==1 else 'МЕСЯЦА'),56)
        page=Image.new('RGBA',(435,239))
        pd=ImageDraw.Draw(page)
        box(pd,2,2,430,229,'#FFFBE8',17,INK)
        for j in range(3):
            line(pd,[(55,64+36*j),(376,64+36*j)],LINE,6)
        angle=-14-u*39
        page=page.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        im.paste(page,(round(606+90*u),round(756+440*u)),page)
    elif k==4:
        d.ellipse((108,502,979,1369),fill='#F0ECDF')
        d.ellipse((149,621,885,1218),fill='#C5AF80')
        d.ellipse((149,603,885,1200),fill=WOOD,outline=INK,width=6)
        d.arc((181,627,854,1174),0,318,fill='#F3DFA8',width=5)
        for cx,cy,c in ((362,830,'#FFFBE8'),(697,996,YELLOW)):
            d.ellipse((cx-125,cy-112,cx+125,cy+112),fill='#C0A573')
            d.ellipse((cx-114,cy-109,cx+114,cy+105),fill='#FFF8DF',outline=INK,width=4)
            d.ellipse((cx+65,cy-29,cx+115,cy+29),fill=c,outline=INK,width=4)
            d.ellipse((cx-72,cy-71,cx+74,cy+72),fill=c,outline=INK,width=5)
            d.ellipse((cx-58,cy-57,cx+58,cy+57),fill='#694729',outline=INK,width=4)
        xx=round(980-166*ease(u/.34))
        box(d,xx,1145,138,133,YELLOW,28,INK,5)
        box(d,xx+6,1253,126,45,'#DBA514',18,INK,4)
    elif k==5:
        cafe(d,im,u,True)
        x=465+round(200*(1-ease(u/.38)))
        label(d,x,663,'ОДНА ДАТА?',101)
    else:
        cafe(d,im,u,False)
        y=650+round(49*(1-pop(u/.29)))
        shadow(d,141,y,795,156,'#DED4B3',28)
        box(d,141,y,795,156,YELLOW,24,INK,5)
        label(d,538,y+76,'КАК-НИБУДЬ',100)
    captions(d,t)
    return im

def pcm(path):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ar','44100','-ac','1','-'])
    return np.frombuffer(data,dtype='<f4')

def mix():
    samples=np.zeros(round(end*44100),np.float32)
    dry=pcm(WORK/'fragment.mp3')
    samples[:min(len(dry),len(samples))]=dry[:len(samples)]*.96
    cues=((.14,'04-pop.mp3',.09),(.39,'04-pop.mp3',.085),(.65,'04-pop.mp3',.09),
          (1.29,'12-soobshchenie.mp3',.11),(2.43,'11-uvedomlenie.mp3',.13),
          (3.73,'43-vzhuh-bas-skleyka.mp3',.12),(3.96,'28-tsik-bystro-a.mp3',.10),
          (4.92,'01-vzhuh-korotkiy.mp3',.10),(5.88,'05-klik.mp3',.10),
          (6.91,'19-udar-final.mp3',.14))
    for time,name,gain in cues:
        audio=pcm(PROJECT/'zvuki'/name)
        i=round(time*44100)
        n=min(len(audio),len(samples)-i)
        samples[i:i+n]+=audio[:n]*gain
    with wave.open(str(WORK/'fragment-mix.wav'),'wb') as sound:
        sound.setparams((1,2,44100,0,'NONE','not compressed'))
        sound.writeframes((np.clip(samples,-1,1)*32767).astype('<i2').tobytes())


if __name__ == '__main__':
    mix()
