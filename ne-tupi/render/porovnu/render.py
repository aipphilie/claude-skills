"""Вертикальный рилс из сцен, таймингов ElevenLabs и анимаций проекта."""
import argparse
import bisect
import json
import math
import re
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps, ImageSequence

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
WIDTH, HEIGHT, FPS = 720, 1280, 30
WHITE, INK, YELLOW = '#FFFFFF', '#131313', '#FFD60A'
GREY, PALE, LINE = '#6C6B65', '#F4F3EF', '#DEDDD6'
FONT = PROJECT / 'render/kvartira/kod/fonts/Oswald-Bold.ttf'
SYMBOL_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


@lru_cache(maxsize=64)
def font(size, symbols=False):
    return ImageFont.truetype(SYMBOL_FONT if symbols else FONT, size)


def label(draw, text, x, y, size, fill=INK):
    draw.text((int(x), int(y)), text, font=font(size, '₽' in text), anchor='mm', fill=fill)


def pill(draw, text, x, y, size=29, bg=YELLOW, fg=INK):
    f = font(size, '₽' in text)
    w = f.getlength(text) / 2 + 14
    draw.rounded_rectangle((x-w, y-size*.76, x+w, y+size*.77), radius=8, fill=bg)
    label(draw, text, x, y, size, fg)


def ease(value):
    return 1 - (1 - min(1, max(0, value))) ** 3


@lru_cache(maxsize=18)
def poses(name, height):
    path = PROJECT / 'animacii-3d/gif' / (name + '.gif')
    with Image.open(path) as source:
        frames = [f.convert('RGB') for f in ImageSequence.Iterator(source)]
    boxes = [ImageOps.invert(frame.convert('L')).point(lambda v: 255 if v > 14 else 0).getbbox()
             for frame in frames]
    top = max(0, min(b[1] for b in boxes)-2)
    bottom = min(frames[0].height, max(b[3] for b in boxes)+2)
    left = max(0, min(b[0] for b in boxes)-2)
    right = min(frames[0].width, max(b[2] for b in boxes)+2)
    width = round((right-left) * height / (bottom-top))
    return tuple(frame.crop((left, top, right, bottom)).resize(
        (width, height), Image.Resampling.LANCZOS) for frame in frames)


def person(canvas, x, bottom, height, pose, clock, reverse=False):
    height = round(height*.86)
    frames = poses(pose, height)
    frame = frames[int(max(0, clock) * 25) % len(frames)]
    if reverse:
        frame = ImageOps.mirror(frame)
    left = round(x-frame.width/2)
    top = round(bottom-height)
    region = canvas.crop((left, top, left+frame.width, bottom))
    canvas.paste(ImageChops.multiply(region, frame), (left, top))


def ground(draw, y=806):
    draw.line((80, y, 640, y), fill=LINE, width=2)


def bag(d, x, y, scale=1):
    s = scale
    d.arc((x-17*s, y-55*s, x+17*s, y-12*s), 180, 360, fill=INK, width=max(2, int(4*s)))
    d.polygon(((x-29*s,y-28*s),(x+29*s,y-28*s),(x+37*s,y+40*s),(x-37*s,y+40*s)), fill=YELLOW)
    d.line(((x-29*s,y-28*s),(x+29*s,y-28*s),(x+37*s,y+40*s),(x-37*s,y+40*s),(x-29*s,y-28*s)), fill=INK, width=max(2,int(3*s)))
    d.line((x-13*s,y+8*s,x+13*s,y+8*s), fill=INK, width=max(2,int(4*s)))


def receipt(d, x, y, top, total, yellow=True):
    outline = YELLOW if yellow else LINE
    d.rounded_rectangle((x-107,y-119,x+107,y+119), radius=14, fill=PALE, outline=outline, width=4)
    pill(d, top, x, y-74, 23, bg=outline)
    d.line((x-73,y+13,x+73,y+13), fill=LINE, width=3)
    d.line((x-73,y+30,x+62,y+30), fill=LINE, width=3)
    label(d, total, x, y+73, 29)


def phone(d, x, y, lines):
    d.rounded_rectangle((x-158,y-170,x+158,y+170), radius=31, fill=INK)
    d.rounded_rectangle((x-150,y-149,x+150,y+148), radius=22, fill=PALE)
    d.rounded_rectangle((x-21,y-161,x+21,y-156), radius=2, fill=LINE)
    for j, text in enumerate(lines):
        pill(d, text, x, y-81+72*j, 24, bg=YELLOW if j == 0 else WHITE)


def table(d):
    d.rounded_rectangle((126,697,594,733), radius=14, fill=INK)
    d.rounded_rectangle((157,728,171,804), radius=5, fill=INK)
    d.rounded_rectangle((549,728,563,804), radius=5, fill=INK)
    for x in (260,360,460):
        d.ellipse((x-28,687,x+28,708), fill=WHITE, outline=INK, width=3)


def trio(canvas, d, values, u, carry=True):
    ground(d)
    for i, x in enumerate((185,360,535)):
        role = 'pozhimaet-plechami' if i == 2 and carry else 'dyhanie'
        person(canvas, x, 804, 241 if i == 2 else 215, role, u+.27*i)
        if values:
            value = values[i]
            drop = 54 * (1-ease((u-.12*i)/.38)) if u >= 0 else 0
            pill(d, value, x, 497-drop, 24, bg=YELLOW if i == 2 else PALE)
    table(d)
    if carry:
        bag(d, 500, 713, .72)
        bag(d, 565, 717, .82)


def taxi(d, x, y):
    d.rounded_rectangle((x-153,y-33,x+153,y+41), radius=29, fill=YELLOW, outline=INK, width=5)
    d.polygon(((x-103,y-31),(x-64,y-83),(x+50,y-83),(x+111,y-31)), fill=YELLOW)
    d.line(((x-103,y-31),(x-64,y-83),(x+50,y-83),(x+111,y-31)), fill=INK, width=5)
    d.polygon(((x-84,y-36),(x-57,y-73),(x+43,y-73),(x+88,y-36)), fill=WHITE)
    d.line((x-5,y-72,x-5,y-37), fill=INK, width=4)
    for hub in (x-93,x+96):
        d.ellipse((hub-24,y+20,hub+24,y+68), fill=INK)
        d.ellipse((hub-10,y+34,hub+10,y+54), fill=WHITE)
    for i in range(5):
        d.rectangle((x-50+i*17,y-11+(i%2)*11,x-38+i*17,y-1+(i%2)*11), fill=INK)


def sofa(d, x, y):
    d.rounded_rectangle((x-174,y-91,x+174,y+56), radius=26, fill=PALE, outline=INK, width=4)
    d.rounded_rectangle((x-146,y-3,x+146,y+51), radius=13, fill=YELLOW, outline=INK, width=3)
    for shift in (-155,155):
        d.rounded_rectangle((x+shift-26,y-25,x+shift+26,y+61), radius=16, fill=PALE, outline=INK, width=4)


def title(d, lines, sizes=(72, 78)):
    for idx, line in enumerate(lines):
        label(d, line, 360, 260+86*idx, sizes[idx])


HEADERS = {
    'friends': ('УЖИН НА ТРОИХ',), 'bill': ('ЧЕК НА ТРОИХ',), 'chat': ('ВСЁ, РАССЧИТАЛИСЬ',),
    'twist': ('А ВОТ И ПОДВОХ',), 'taxi': ('ТАКСИ',), 'movie': ('КТО ЕДЕТ ЗА ЕДОЙ?',),
    'total': ('СКОЛЬКО ВЫШЛО?',), 'receipt': ('В ОБЩИЙ СЧЁТ', 'НЕ ПОПАЛО'),
    'ask': ('ТАКСИ ДЕЛИМ?',), 'equal': ('ТЕПЕРЬ ПОРОВНУ',),
    'choice': ('КТО ЗАБИРАЕТ?',), 'return': ('ДВА ВОПРОСА',)
}


def illustration(canvas, d, key, u, fraction):
    if key == 'open':
        title(d, ('СКИНУЛИСЬ', 'ПОРОВНУ?'), (77,90))
        trio(canvas,d,('900 ₽','900 ₽','1 200 ₽'),u)
    elif key in ('friends','total','equal'):
        title(d, HEADERS[key], (63,63))
        values = {'friends': None, 'total': ('900 ₽','900 ₽','1 200 ₽'), 'equal': ('1 000 ₽',)*3}
        trio(canvas,d,values[key],u,carry=key != 'equal')
        if key == 'friends':
            pill(d,'ЕДА · 2 700 ₽',360,513,31)
    elif key == 'bill':
        title(d, HEADERS[key], (66,66))
        receipt(d,360,541,'ЕДА','2 700 ₽')
        for i, x in enumerate((181,360,539)):
            if u > 1.1 + .24*i:
                y = 708-42*(1-ease((u-1.1-.24*i)/.32))
                pill(d,'900 ₽',x,y,27,bg=PALE if i == 1 else YELLOW)
        ground(d)
    elif key in ('chat','ask','return'):
        title(d, HEADERS[key],(59,59))
        lines = {'chat': ['+900 ₽', '+900 ₽', 'Всё, рассчитались.'],
                 'ask': ['Я заберу.', 'Такси делим?'],
                 'return': ['Кто забирает?', 'Кто платит?']}[key]
        phone(d,360,610,lines[:min(len(lines),1+int(fraction*len(lines)))])
    elif key == 'twist':
        title(d, HEADERS[key], (63,63))
        points = [(130,722),(203,636),(290,675),(390,538),(500,560),(593,493)]
        count = max(2, int(1+ease(u/1.6)*(len(points)-1)))
        d.line(points[:count],fill=YELLOW,width=12,joint='curve')
        for x,y in (points[0],points[count-1]):
            d.ellipse((x-12,y-12,x+12,y+12),fill=INK)
        bag(d,592,457,.64)
        person(canvas,236+215*ease(u/2.8),807,218,'shag-profil',u)
    elif key == 'taxi':
        title(d, HEADERS[key],(78,78))
        ground(d)
        taxi(d,360+360*(1-ease(u/.65)),671)
        if u>.25:
            pill(d,'300 ₽',360,490,54)
    elif key == 'movie':
        title(d, HEADERS[key],(63,63))
        if fraction < .44:
            sofa(d,360,740)
            person(canvas,286,755,218,'dyhanie',u)
            person(canvas,425,755,218,'razgovor',u)
            d.rounded_rectangle((267,480,453,579),radius=10,fill=INK)
            d.polygon(((348,508),(348,553),(386,531)),fill=YELLOW)
        else:
            ground(d)
            x = 278+80*ease((fraction-.44)/.3)
            person(canvas,x,807,314,'tashit-legko',u)
            for i in range(3):
                bag(d,x+41+39*i,697+12*math.sin(11*u-i),.63)
            d.rounded_rectangle((x+25,567,x+57,584),radius=4,fill=YELLOW,outline=INK,width=2)
    elif key == 'receipt':
        title(d, HEADERS[key],(63,63))
        receipt(d,225,623,'ЕДА','900 ₽',False)
        receipt(d,495,623-82*(1-ease(u/.52)),'ТАКСИ','+300 ₽')
    elif key == 'stop':
        ground(d)
        person(canvas,360,817,303,'ukazyvaet-vverh',u)
        pill(d,'СТОП.',360,344,99)
        label(d,'ТУТ ТЫ ТУПИШЬ',360,443,59)
    elif key == 'choice':
        title(d,HEADERS[key],(68,68))
        person(canvas,221,791,270,'shag-profil',u)
        bag(d,267,715,.65)
        taxi(d,501,691)
        pill(d,'САМИ',222,490,30)
        pill(d,'ДОСТАВКА',511,490,30,bg=PALE)
    elif key == 'end':
        ground(d)
        sofa(d,334,745)
        person(canvas,330+90*ease(u/1.4),804,285,'shag-profil',u)
        pill(d,'ВСЁ. НЕ ТУПИ.',360,381,68)


def align(script, alignment):
    source = ''.join(alignment['characters'])
    starts = alignment['character_start_times_seconds']
    ends = alignment['character_end_times_seconds']
    scenes = []
    cursor = 0
    for name, _, line in script:
        index = source.index(line, cursor)
        words = [(m.group(), starts[index+m.start()], ends[index+m.end()-1])
                 for m in re.finditer(r'\S+',line)]
        groups = []
        group = []
        for word in words:
            group.append(word)
            if len(group) == 4 or (len(group) > 1 and word[0].rstrip('»').endswith(('.', '?', '!'))):
                groups.append(group)
                group = []
        if group:
            groups.append(group)
        scenes.append((name,words[0][1],groups))
        cursor = index + len(line)
    return scenes, ends[-1]


def question_counter(draw, key):
    progress = {
        'twist': 0, 'taxi': 1, 'movie': 1, 'total': 2,
        'receipt': 2, 'stop': 2, 'ask': 2, 'equal': 3, 'choice': 3,
    }.get(key)
    if progress is None:
        return
    for number in range(1, 4):
        x = 360 + (number - 2) * 41
        draw.ellipse((x-13, 174, x+13, 200), fill=YELLOW if number <= progress else WHITE,
                     outline=INK if number == progress+1 else LINE, width=2)
        label(draw, str(number), x, 187, 14)


def shot_framing(canvas, key, elapsed, duration):
    # Чередуем общий и крупный планы внутри длинных реплик, оставляя плашки в кадре.
    shots = max(1, math.ceil(duration/1.5))
    shot_length = duration/shots
    shot = min(shots-1, int(elapsed/shot_length))
    local = elapsed-shot*shot_length
    center_x = {'total': 407, 'movie': 395, 'receipt': 390, 'choice': 380}.get(key, 360)
    crop = 52 if shot % 2 else 0
    overshoot = 18*(1-ease(local/.28)) if shot == 0 and key in ('bill','twist','total','stop','equal') else 0
    crop += round(overshoot)
    if not crop:
        return canvas
    x = WIDTH/2 + (center_x-WIDTH/2) * min(1, crop/52)
    y = HEIGHT/2 - crop*.36
    return canvas.crop((round(x-WIDTH/2+crop), round(y-HEIGHT/2+crop),
                        round(x+WIDTH/2-crop), round(y+HEIGHT/2-crop))).resize(
                            (WIDTH, HEIGHT), Image.Resampling.BILINEAR)


def subtitles(draw, groups, t):
    available = [group for group in groups if group[0][1] <= t+.045]
    if not available:
        return
    group = available[-1]
    if t > group[-1][2]+.32:
        return
    words = [word.upper() for word, _, _ in group]
    size = 42
    while font(size).getlength(' '.join(words)) > 530:
        size -= 1
    f = font(size)
    x = 360 - f.getlength(' '.join(words))/2
    active = bisect.bisect_right([start for _, start, _ in group], t+.035)-1
    for i, word in enumerate(words):
        w = f.getlength(word)
        if i == active:
            draw.rounded_rectangle((x-5,893,x+w+5,944),radius=6,fill=YELLOW)
        draw.text((x,919),word,font=f,anchor='lm',fill=INK)
        x += w + f.getlength(' ')


def covers(out):
    for variant in ('a','b'):
        img = Image.new('RGB',(WIDTH,HEIGHT),WHITE)
        d = ImageDraw.Draw(img)
        if variant == 'a':
            title(d,('СКИНУЛИСЬ','ПОРОВНУ'),(83,100))
            trio(img,d,None,0,carry=True)
            receipt(d,529,856,'ТАКСИ','+300 ₽')
        else:
            label(d,'900 / 900',360,259,83)
            pill(d,'1 200 ₽',360,365,63)
            trio(img,d,None,1.0)
        label(d,'netupi.tv',360,995,30,GREY)
        img.resize((1080,1920),Image.Resampling.LANCZOS).save(out/f'porovnu-oblozhka-{variant}.png')


EFFECTS = {
    'open': ('19-udar-final.mp3',0.06), 'bill': ('09-kassa.mp3',0.10),
    'chat': ('11-uvedomlenie.mp3',0.11), 'twist': ('03-perehod-swipe.mp3',0.065),
    'taxi': ('10-monetki.mp3',0.095), 'total': ('14-plyuh.mp3',0.09),
    'stop': ('05-klik.mp3',0.13), 'equal': ('06-dzyn-insayt.mp3',0.105),
    'end': ('05-klik.mp3',0.10)
}


def pcm(path):
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ar','44100','-ac','1','-'])
    return np.frombuffer(raw,dtype='<f4')


def mix(voice, scenes, seconds, output):
    track = np.zeros(round(seconds*44100),dtype=np.float32)
    dry = pcm(voice)
    track[:min(len(dry),len(track))] = dry[:len(track)]*.94
    for key, start, _ in scenes:
        if key not in EFFECTS:
            continue
        name, gain = EFFECTS[key]
        sound = pcm(PROJECT/'zvuki'/name)
        at = round(start*44100)
        n = min(len(track)-at,len(sound))
        track[at:at+n] += sound[:n]*gain
    with wave.open(str(output),'wb') as f:
        f.setparams((1,2,44100,0,'NONE','not compressed'))
        f.writeframes((np.clip(track,-1,1)*32767).astype('<i2').tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('voice',type=Path)
    parser.add_argument('alignment',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--preview',type=Path)
    args = parser.parse_args()
    script = json.loads((HERE/'scenariy.json').read_text())
    scenes, end = align(script,json.loads(args.alignment.read_text()))
    marks = [row[1] for row in scenes]+[end+.8]
    args.output.mkdir(parents=True,exist_ok=True)

    def frame(t):
        scene = max(0,bisect.bisect_right(marks,t)-1)
        scene = min(scene,len(scenes)-1)
        key,start,groups = scenes[scene]
        u = max(0,t-start)
        duration = max(.1,marks[scene+1]-start)
        canvas = Image.new('RGB',(WIDTH,HEIGHT),WHITE)
        draw = ImageDraw.Draw(canvas)
        illustration(canvas,draw,key,u,u/duration)
        canvas = shot_framing(canvas,key,u,duration)
        draw = ImageDraw.Draw(canvas)
        question_counter(draw,key)
        subtitles(draw,groups,t)
        return canvas

    covers(args.output)
    if args.preview:
        sheet = Image.new('RGB',(180*5,320*3),WHITE)
        for i, mark in enumerate(marks[:-1]):
            sheet.paste(frame(mark+(marks[i+1]-mark)*.65).resize((180,320)),(i%5*180,i//5*320))
        sheet.save(args.preview)
        return

    mix_path = args.voice.parent/'mix-porovnu.wav'
    frames = math.ceil((end+.8)*FPS)
    mix(args.voice,scenes,frames/FPS,mix_path)
    target = args.output/'tebe-zaplatili-tvoimi-zhe-dengami.mp4'
    command = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24',
               '-video_size',f'{WIDTH}x{HEIGHT}','-framerate',str(FPS),'-i','pipe:0','-i',str(mix_path),
               '-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-threads','4','-preset','veryfast',
               '-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(target)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as encode:
        for i in range(frames):
            encode.stdin.write(frame(i/FPS).tobytes())
        encode.stdin.close()
        if encode.wait():
            raise SystemExit('Не удалось закодировать ролик')
    print(target)


if __name__ == '__main__':
    main()
