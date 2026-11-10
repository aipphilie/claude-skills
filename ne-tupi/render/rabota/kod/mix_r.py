import subprocess, re
src = open('compose_r.py').read()
# берём тайминги из compose_r без рендера
ns = {}
exec(src.split('def big_text')[0].split('xoff = json.load')[0], ns)   # шапка (импорты, words)
exec('import random\n' + src.split('import random', 1)[1].split('def big_text')[0], ns)
T, B, DUR = ns['T'], ns['B'], ns['DUR']
from words import END
ev = [('pop', 0.15, 0.35), ('pop', T['zavtra'], 0.4), ('pop', T['dumaesh'], 0.4), ('snap', T['stop'] - 0.05, 0.8),
      ('whoosh', T['dver'] - 0.15, 0.5), ('pop', T['uchenye'], 0.4), ('thud', T['naoborot'] - 0.1, 0.7),
      ('whoosh', B[3], 0.4), ('pop', T['god'], 0.4), ('pop', T['sobaki'], 0.35), ('pop', T['barer'], 0.45), ('whoosh', T['pereprygni'], 0.4),
      ('thud', T['lozhilis'] + 0.3, 0.6), ('pop', T['nazvali'], 0.45), ('whoosh', T['uznal'] - 0.1, 0.4), ('whoosh', T['rezyume'], 0.3),
      ('pop', T['nichego'] - 0.2, 0.4), ('scissors', T['dumali'], 0.5), ('pop', T['pravda'], 0.45), ('whoosh', T['cherez'] - 0.1, 0.4),
      ('pop', T['terpet'], 0.4), ('thud', T['zavod'] - 0.1, 0.6), ('ding', T['drugoe'] - 0.3, 0.6),
      ('pop', T['delat'] - 0.5, 0.45), ('scissors', T['smelost'] + 0.35, 0.45), ('pop', T['nuzhen'] - 0.05, 0.45),
      ('pop', T['rez2'], 0.45), ('pop', T['sozvon'], 0.45), ('pop', T['sobes'], 0.45), ('ding', T['kazhdy'], 0.5),
      ('pop', T['tolko'], 0.45), ('whoosh', T['dver2'], 0.5), ('scissors', T['otkryta2'], 0.4), ('snap', T['netupi'] - 0.3, 0.8), ('whoosh', END + 0.75, 0.5)]
inp = ['-i', 'voice.mp3']; fl = []; lab = ['[0:a]']
for k, (n, t, v) in enumerate(ev):
    inp += ['-i', f'sfx/{n}.mp3']; ms = int(max(0, t) * 1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR)
