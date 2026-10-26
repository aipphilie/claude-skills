import json,subprocess,re
CH={'01':["Через семь минут","Соня будет стоять вот здесь.","Над чёрным тоннелем.","А пока — ноль сорок семь.","Поезд встал. Свет погас. Пахнет дымом.","Что Соня сделает дальше…","— решаете вы."],
'02':["Это Соня.","Девятнадцать лет.","Последний поезд после смены в кофейне.","До любой станции — под километр темноты.","Заряд телефона — двадцать три процента.","Это её единственный фонарь."],
'03':["Михалыч стучит тростью в пол:","«Сейчас поедем».","Парень в капюшоне уже в эфире:","«Нас тут замуровали».","А женщина в форме метрополитена…","молча прячет рацию в карман.","Машинист молчит.","Ни объявления.","Ничего."],
'04':["Соня делает правильно.","Кнопка «Связь с машинистом» у дверей.","Нажать.","Назвать номер вагона.","Сказать, что случилось.","И двери самим не открывать: внизу контактный рельс.","Восемьсот двадцать пять вольт."],
'05':["В динамике — тишина.","А дым всё гуще.","Видимость — тридцать метров… двадцать.","Парень читает чат — и замолкает.","Кто-то пишет:","«кабина пустая».","Он разжимает двери руками.","«Я тут сдыхать не собираюсь».","Створки поддаются.","И тогда динамик оживает.","Голос.","Спокойный."],
'06':["Соня.","Не выходи.","Пусть решат они."],'07':["Своё имя она никому не называла."],
'08':["Парень спрыгивает вниз и уходит в темноту.","Соня стоит над проёмом.","А — остаться в вагоне и ждать.","Б — выйти за ним в тоннель.","Пишите А или Б в комментариях.","Следующая серия — по вашему выбору."]}
PRE=.35;GAP={'01':.9,'02':.45,'03':.45,'04':.45,'05':.5,'06':.35,'07':.5,'08':0}
t=PRE;out=[];files=[]
for c in ['01','02','03','04','05','06','07','08']:
    f=f'vo/{c}.mp3';d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    log=subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=n=-38dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
    ss=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',log)];se=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',log)]
    segs=[];a=0
    for s0,e0 in zip(ss,se):segs.append((a,s0));a=e0
    segs.append((a,d))
    ph=CH[c];assert len(segs)==len(ph),(c,len(segs),len(ph))
    for i,(p,(a,b)) in enumerate(zip(ph,segs)):out.append({'id':f'{c}.{i+1}','txt':p,'s':round(t+a,3),'e':round(t+b,3)})
    files.append((f,t));t+=d+GAP[c]
END=t+3.2
json.dump({'phr':out,'end':END,'files':files},open('timeline.json','w'),ensure_ascii=False,indent=0)
open('timeline.js','w').write('const TL='+json.dumps({'phr':out,'end':END},ensure_ascii=False)+';')
print('END',END)
# voice track
inp=[];flt=[]
for i,(f,st) in enumerate(files):
    inp+=['-i',f];ms=int(st*1000)
    ch=f'[{i}:a]aresample=48000,aformat=channel_layouts=mono'
    if '06' in f: ch+=',highpass=f=280,lowpass=f=3200,aecho=0.8:0.6:60:0.25,volume=1.25'
    flt.append(f'{ch},adelay={ms}|{ms}[a{i}]')
flt.append(''.join(f'[a{i}]' for i in range(len(files)))+f'amix=inputs={len(files)}:normalize=0,apad=whole_dur={END}[v]')
subprocess.run(['ffmpeg','-y','-v','error']+inp+['-filter_complex',';'.join(flt),'-map','[v]','-t',str(END),'voice.wav'],check=True)
