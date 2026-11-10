"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye (новая библиотека), громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = 'sfx/snap.mp3'   # фирменный щелчок «Стоп» из старого набора
# (файл, время, громкость[, обрезать до сек])
ev = [(z(11), 0.1, 0.5), (z(4), T['nebral'] - 0.3, 0.3), (z(4), T['dumaesh'], 0.3), (z(4), T['nikomu'], 0.3),
      (z(23), B[2] - 0.4, 0.45), (SNAP, T['stop'] - 0.05, 0.8),
      (z(1), T['tvoi'] - 0.15, 0.4), (z(4), T['slil'] - 0.3, 0.3),
      (z(14), T['dostavka'], 0.3), (z(14), T['apteka'], 0.3), (z(14), T['magazin'], 0.3),
      (z(4), T['delat'] - 0.6, 0.35), (z(24), T['nas'] + 0.6, 0.4), (z(4), T['odna'], 0.35), (z(9), T['besplatno'], 0.3),
      (z(28), T['dve'], 0.4, 1.3),
      (z(3), B[4] - 0.1, 0.4), (z(13), T['poiske'] + 0.2, 0.35), (z(5), T['stavish'], 0.45), (z(7), T['stavish'] + 0.3, 0.35),
      (z(25), T['bank'] - 0.45, 0.4), (z(20), T['otkazat'], 0.5),
      (z(36), T['podvoh'] - 0.5, 0.4), (z(5), T['snyat'], 0.45), (z(4), T['snyat'] + 0.2, 0.3),
      (z(1), T['zvonyat'] - 0.6, 0.4), (z(12), T['zvonyat'] + 0.3, 0.4), (z(4), T['proverki'] - 0.3, 0.3), (z(4), T['zashity'] - 0.3, 0.3),
      (z(43), B[6] - 0.5, 0.4), (z(4), T['zapomni'] + 0.7, 0.35), (z(26), T['moshennik'] - 0.3, 0.5), (z(4), T['vsegda'], 0.35),
      (z(3), B[7] - 0.1, 0.4), (z(5), T['snyal'], 0.4), (z(9), T['vzyal'], 0.3), (z(5), T['postavil'], 0.4),
      (z(23), B[8] - 0.4, 0.4), (z(1), T['pereshli'] - 0.2, 0.35), (z(35), T['pereshli'] + 1.1, 0.3),
      (z(3), T['pust'] - 0.2, 0.4), (z(11), T['soob'], 0.5), (z(20), T['otkazano'] - 0.05, 0.5),
      (SNAP, T['netupi'] - 0.3, 0.8), (z(19), T['netupi'] - 0.3, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.mp3']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={e[3]-0.15}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
