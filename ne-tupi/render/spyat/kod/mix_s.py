"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'   # фирменный щелчок «Стоп»
# (файл, время, громкость[, обрезать до сек])
ev = [(z(18), 0.0, 0.3, 2.4), (z(4), T['zarplata'] - 0.1, 0.35), (z(14), T['dvadcat'] - 0.1, 0.4), (z(5), T['kvart'], 0.35),
      (z(23), B[1] - 0.35, 0.4), (z(4), B[1], 0.35), (z(6), T['otvet'], 0.35),
      (z(21), T['dumaesh'], 0.25),
      (SNAP, T['stop'] - 0.05, 0.8), (z(8), T['stop'] + 0.4, 0.3), (z(4), T['dengi'] - 0.05, 0.3),
      (z(33), T['spyat'] - 0.7, 0.45), (z(4), T['karte'] - 0.05, 0.3),
      (z(23), B[5] - 0.35, 0.4), (z(10), T['shest6'], 0.35), (z(14), T['shest6'] + 0.8, 0.3), (z(5), T['avto'] - 0.05, 0.35), (z(7), T['do'] - 0.05, 0.35),
      (z(24), B[6] - 0.35, 0.4), (z(31), B[6] + 0.1, 0.3, 1.4), (z(42), T['razbudi'] - 0.1, 0.35),
      (z(4), T['nakop'] - 0.1, 0.35), (z(4), T['oblig'] - 0.1, 0.35), (z(4), T['iis'] - 0.1, 0.35), (z(9), T['trinad'], 0.35),
      (z(25), B[8] - 0.35, 0.4), (z(5), T['trogay'], 0.35), (z(1), T['pust'] - 0.1, 0.35),
      (z(36), T['podvoh'] - 0.5, 0.4),
      (z(4), T['ceny'], 0.3), (z(4), T['ceny'] + 0.35, 0.32), (z(4), T['ceny'] + 0.7, 0.34), (z(22), T['hudeyut'] - 0.2, 0.4),
      (z(23), B[11] - 0.35, 0.4), (z(10), T['otlozhish'], 0.3), (z(9), T['trista'] + 0.8, 0.35),
      (z(4), T['pritashat'], 0.35), (z(9), T['sta'] + 0.5, 0.35),
      (z(14), T['pyatdesyat'] + 0.2, 0.4), (z(35), T['gosudarstvo2'], 0.3),
      (z(33), T['tridcat'] - 0.15, 0.4), (z(26), T['tridcat'], 0.5),
      (z(24), B[15] - 0.35, 0.4), (z(35), T['rabotayut'], 0.3),
      (SNAP, T['netupi'] - 0.3, 0.8), (z(19), T['netupi'] - 0.3, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={e[3]-0.15}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
