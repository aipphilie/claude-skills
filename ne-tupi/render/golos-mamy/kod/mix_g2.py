"""Звук v2: голос + новые эффекты из ne-tupi-zvuki/gotovye (вжух с басом на смены сцен, цик-цик на «срочно»).
Громкость эффектов ×0.5. У звуков с ударом (bass/bum/riser) удар подгоняется к акценту по пику."""
import subprocess, glob, numpy as np
from anch import T, B, END, DUR
F = {f.split('/')[-1][:2]: f for f in glob.glob('sfx2/*.mp3')}
def peak(n):
    pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', F[n], '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.abs(np.frombuffer(pcm, np.int16).astype(np.float32)); k = 400
    env = np.convolve(x, np.ones(k) / k, 'same'); return float(np.argmax(env)) / 8000
HIT = {n: peak(n) for n in ('23', '25', '43', '34', '26', '19')}
print({k: round(v, 2) for k, v in HIT.items()})
# (звук, время акцента, громкость, обрезка по длине или None); 'snap' — фирменный щелчок канала
ev = [('12', 0.2, 0.5, None), ('04', T['eto'] - 0.05, 0.35, None), ('04', T['golos1'], 0.35, None), ('03', T['otkr'] - 0.15, 0.4, None),
      ('23', T['stop'], 0.4, None), ('snap', T['stop'] - 0.05, 0.8, None),
      ('01', T['zapisala'], 0.4, None), ('26', T['nemama'], 0.45, None), ('04', T['sluh'] - 0.3, 0.35, None), ('04', T['sluh'], 0.35, None), ('05', T['otlich'], 0.5, None),
      ('35', T['no'] - 0.05, 0.4, None), ('04', T['mozhet'] - 0.6, 0.35, None),
      ('25', B[3] + 0.1, 0.4, None), ('21', T['vzlomal'] + 0.25, 0.4, None), ('04', T['tam'] - 0.1, 0.35, None), ('04', T['tam'] + 0.18, 0.35, None), ('04', T['tam'] + 0.46, 0.35, None),
      ('38', T['neiro'], 0.35, None), ('04', T['obrazca'] - 0.6, 0.3, None), ('11', T['skazat'], 0.35, None),
      ('43', B[4] + 0.1, 0.4, None), ('04', T['glavnoe'], 0.35, None),
      ('28', T['rodnoy'], 0.5, T['perest'] + 0.15 - T['rodnoy']), ('05', T['perest'] + 0.15, 0.6, None), ('41', T['spas'] - 0.1, 0.5, None),
      ('25', B[5] + 0.1, 0.4, None), ('04', T['uslyshal'], 0.35, None), ('04', T['uslyshal'] + 0.15, 0.35, None), ('32', T['zapomni'], 0.45, None),
      ('23', B[6] + 0.1, 0.38, None), ('04', T['perezvoni'], 0.38, None), ('04', T['pridum'] - 0.1, 0.38, None), ('07', T['kodovoe'], 0.4, None),
      ('13', T['egonet'], 0.4, None), ('08', T['ukrast'] - 0.3, 0.25, None), ('20', T['netslova'] - 0.1, 0.5, None), ('20', T['perevoda'] - 0.45, 0.5, None),
      ('30', T['teper'] - 0.1, 0.5, T['golos3'] - T['teper']), ('34', T['sdelala'] - 0.05, 0.45, None),
      ('01', B[8], 0.35, None), ('12', T['pereshli'] - 0.1, 0.45, None), ('19', T['netupi'] - 0.25, 0.35, None), ('snap', T['netupi'] - 0.3, 0.8, None), ('02', END + 0.75, 0.3, None)]
inp = ['-i', 'voice.mp3']; fl = []; lab = ['[0:a]']
for k, (n, t, v, cut) in enumerate(ev):
    inp += ['-i', 'sfx/snap.mp3' if n == 'snap' else F[n]]; ms = int(max(0, t - HIT.get(n, 0)) * 1000)
    tr = f'atrim=0:{cut:.2f},afade=t=out:st={max(0, cut - 0.25):.2f}:d=0.25,' if cut else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix2.m4a'], check=True)
print('ok', DUR)
