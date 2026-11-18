"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'   # фирменный щелчок «Стоп»
T_DROP = T['dalshe'] - 0.25
# (файл, время, громкость[, обрезать до сек])
ev = [(z(18), 0.0, 0.3, 2.4), (z(14), T_DROP + 0.25, 0.4),
      (z(4), T['vtoroy'] - 0.1, 0.3), (z(4), T['tretiy'] - 0.1, 0.32), (z(4), (T['tretiy'] + T['pyatyy']) / 2 - 0.1, 0.34), (z(4), T['pyatyy'] - 0.1, 0.36),
      (z(3), T['legche'], 0.35), (z(4), T['pochemu'] - 0.05, 0.35),
      (z(23), B[2] - 0.4, 0.45), (z(21), T['dumaesh'] + 0.1, 0.25), (z(4), T['bogatym'], 0.3),
      (SNAP, T['stop'] - 0.05, 0.8), (z(8), T['stop'] + 0.4, 0.3),
      (z(1), B[4], 0.4), (z(33), T['silnee'] - 0.1, 0.45),
      (z(24), B[5] - 0.3, 0.4), (z(6), T['tri'], 0.3),
      (z(1), T['zarab'] - 0.1, 0.35), (z(10), T['dorozhe'] - 0.3, 0.35),
      (z(1), T['uderzh'] - 0.1, 0.35), (z(10), T['utekat'] - 0.3, 0.3), (z(7), T['erundu'] + 0.4, 0.35),
      (z(1), T['boyatsya'] - 0.1, 0.35), (z(41), T['summa'], 0.35, 1.6), (z(35), T['cifroy'], 0.3),
      (z(36), T['podvoh'] - 0.5, 0.4),
      (z(2), T['svalilsya'] - 0.2, 0.35), (z(14), T['svalilsya'] + 0.35, 0.4), (z(42), T['uletaet'] - 0.3, 0.35),
      (z(23), B[11] - 0.4, 0.4), (z(4), B[11] + 0.05, 0.3),
      (z(3), B[12] - 0.1, 0.35), (z(4), T['odin'] - 0.3, 0.3), (z(4), T['vtoroy2'] - 0.1, 0.35), (z(4), T['vdvoem'] - 0.1, 0.3),
      (z(10), T['vlozhen'], 0.35), (z(9), T['prinosit'] + 0.2, 0.35),
      (z(26), T['desyatyy'] - 0.05, 0.5), (z(4), T['tashat'] - 0.1, 0.3),
      (z(25), B[15] - 0.4, 0.4), (z(8), T['gonis'] + 0.1, 0.3),
      (z(4), T['dohod'] - 0.05, 0.35), (z(4), T['otkl'] - 0.05, 0.35), (z(4), T['vlozh'] - 0.05, 0.35),
      (z(23), B[16] - 0.4, 0.4), (z(35), T['drugoy'], 0.3),
      (SNAP, T['netupi'] - 0.3, 0.8), (z(19), T['netupi'] - 0.3, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={e[3]-0.15}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
