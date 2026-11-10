"""Звук: голос (мама + диктор) + эффекты (громкость ×0.5 от прежней нормы)."""
import subprocess
from anch import T, B, END, DUR
ev = [('ding', 0.2, 0.7), ('pop', T['eto'] - 0.05, 0.4), ('pop', T['golos1'], 0.4), ('whoosh', T['otkr'] - 0.15, 0.45),
      ('snap', T['stop'] - 0.05, 0.8), ('scissors', T['stop'] + 0.35, 0.4),
      ('whoosh', T['zapisala'], 0.5), ('thud', T['nemama'] - 0.05, 0.7), ('pop', T['sluh'] - 0.3, 0.4), ('pop', T['sluh'], 0.4),
      ('ding', T['no'] - 0.05, 0.6), ('pop', T['mozhet'] - 0.6, 0.4),
      ('whoosh', B[3], 0.4), ('thud', T['vzlomal'] + 0.25, 0.6), ('pop', T['tam'] - 0.1, 0.4), ('pop', T['tam'] + 0.18, 0.4), ('pop', T['tam'] + 0.46, 0.4),
      ('whoosh', T['neiro'], 0.45), ('pop', T['obrazca'] - 0.6, 0.4), ('ding', T['skazat'], 0.5),
      ('whoosh', B[4], 0.4), ('pop', T['glavnoe'], 0.4), ('pop', T['rodnoy'] - 0.05, 0.4), ('thud', T['srochno'] - 0.1, 0.6), ('snap', T['perest'] + 0.15, 0.6),
      ('pop', T['spas'] - 0.1, 0.45),
      ('whoosh', B[5], 0.45), ('pop', T['uslyshal'], 0.4), ('pop', T['uslyshal'] + 0.15, 0.4), ('ding', T['zapomni'], 0.55),
      ('whoosh', B[6], 0.4), ('pop', T['perezvoni'], 0.45), ('pop', T['pridum'] - 0.1, 0.45), ('ding', T['kodovoe'], 0.5),
      ('whoosh', T['egonet'], 0.35), ('thud', T['ukrast'] - 0.3, 0.55), ('pop', T['netslova'] - 0.1, 0.45), ('thud', T['perevoda'] - 0.45, 0.6), ('scissors', T['perevoda'], 0.4),
      ('whoosh', B[7], 0.4), ('pop', T['teper'] + 0.2, 0.4), ('whoosh', T['golos3'] - 0.05, 0.4), ('thud', T['sdelala'] - 0.1, 0.8), ('pop', T['zametil'], 0.45),
      ('whoosh', B[8], 0.4), ('ding', T['pereshli'] - 0.1, 0.5), ('snap', T['netupi'] - 0.3, 0.8), ('whoosh', END + 0.75, 0.5)]
inp = ['-i', 'voice.mp3']; fl = []; lab = ['[0:a]']
for k, (n, t, v) in enumerate(ev):
    inp += ['-i', f'sfx/{n}.mp3']; ms = int(max(0, t) * 1000)
    fl.append(f'[{k+1}:a]volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR)
