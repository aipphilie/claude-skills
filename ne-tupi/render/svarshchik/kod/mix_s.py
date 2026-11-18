"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'
ev = [(z(4), T['svarshik'] - 0.1, 0.35), (z(9), T['svarshik'] + 0.1, 0.3), (z(4), T['programmist'] - 0.1, 0.3),
      (z(23), B[1] - 0.4, 0.4), (z(4), T['chetyre'] - 0.1, 0.3), (z(4), T['chetyre'] + 0.1, 0.3), (z(4), T['chetyre'] + 0.3, 0.3), (z(4), T['chetyre'] + 0.5, 0.3),
      (z(24), B[2] - 0.4, 0.4), (z(4), T['dva'] - 0.1, 0.3), (z(4), T['dva'] + 0.1, 0.3), (z(22), T['kolledzha'], 0.3, 1.5),
      (z(25), B[3] - 0.4, 0.4), (z(14), T['menshe'] - 0.1, 0.4), (z(8), T['prostite'], 0.3),
      (z(21), T['dumaesh'] + 0.1, 0.25),
      (SNAP, T['stop'] - 0.05, 0.8), (z(8), T['stop'] + 0.4, 0.3),
      (z(4), B[6] + 0.05, 0.3), (z(33), T['mnogo'] - 0.15, 0.45),
      (z(23), B[7] - 0.4, 0.4), (z(6), T['cena'] - 0.1, 0.35),
      (z(24), B[8] - 0.4, 0.4), (z(16), T['kopeyki'], 0.3),
      (z(43), B[9] - 0.4, 0.4), (z(4), T['ochered'], 0.3), (z(4), T['ochered'] + 0.25, 0.3), (z(4), T['ochered'] + 0.5, 0.3), (z(9), T['perebivayut'], 0.35), (z(10), T['dengami'], 0.3),
      (z(36), T['podvoh'] - 0.5, 0.4),
      (z(2), T['poydut'] + 0.3, 0.35), (z(38), T['razvernetsya'] - 0.3, 0.35),
      (z(23), B[12] - 0.4, 0.4), (z(4), B[12] + 0.05, 0.3),
      (z(8), T['tyazhelo'] + 0.6, 0.3), (z(26), T['trudno'] - 0.05, 0.5),
      (z(25), B[14] - 0.4, 0.4), (z(8), T['ochered2'] - 0.2, 0.3), (z(4), T['vakansiy'] - 0.1, 0.3), (z(4), T['rezume'] - 0.1, 0.3),
      (z(5), T['navyka'] + 0.9, 0.4), (z(35), T['malo'], 0.3),
      (z(23), B[16] - 0.4, 0.4), (z(35), T['k_tebe'], 0.3),
      (SNAP, T['netupi'] - 0.3, 0.8), (z(19), T['netupi'] - 0.3, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={e[3]-0.15}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
