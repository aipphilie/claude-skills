"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'
ev = [(z(18), 0.0, 0.3, 2.6), (z(4), 0.25, 0.3),
      (z(2), T['desyatyy'] - 0.1, 0.4), (z(4), T['desyatyy'] + 0.1, 0.3), (z(42), B[1] + 0.9, 0.3),
      (z(4), T['pochemu'] - 0.15, 0.35),
      (z(23), B[2] - 0.3, 0.45), (z(4), T['dvadcat'], 0.3), (z(4), T['dvenadcat'], 0.32),
      (z(30), T['pryamoy'], 0.3, 3.5), (z(4), T['tridcat'] - 0.1, 0.35),
      (SNAP, T['stop'] - 0.05, 0.8), (z(8), T['stop'] + 0.3, 0.3),
      (z(24), B[5] - 0.3, 0.45), (z(28), T['chestno'] + 0.5, 0.3, 3.0), (z(9), T['mesyacev2'] + 0.4, 0.35), (z(4), T['svoih'] - 0.1, 0.3), (z(4), T['svoih'] + 0.6, 0.3),
      (z(25), B[6] - 0.3, 0.45), (z(10), T['kapayut'], 0.3), (z(10), T['proshlye'], 0.3), (z(33), T['rastet'] - 0.1, 0.4),
      (z(23), B[7] - 0.3, 0.45), (z(28), B[7] + 0.4, 0.28, 7.0),
      (z(9), T['odinnadcat'] + 0.6, 0.3), (z(9), T['vosem_let'] + 0.3, 0.3), (z(9), T['nebolshim'] + 0.3, 0.3),
      (z(34), T['desyatyy2'] - 1.0, 0.4), (z(26), T['vosem3'] + 0.5, 0.5), (z(35), T['itogo'], 0.3), (z(42), T['itogo'] - 0.05, 0.3),
      (z(1), B[9], 0.4), (z(4), T['chetyre'] + 0.1, 0.35), (z(4), T['ostalnye'], 0.35),
      (z(1), B[10], 0.4), (z(10), T['sto'], 0.35), (z(26), T['chetyre3'] - 0.05, 0.45),
      (z(36), T['podvoh'] - 0.5, 0.4), (z(16), T['sdayutsya'] - 0.1, 0.35),
      (z(23), B[12] - 0.3, 0.4), (z(12), T['skolko'], 0.35), (z(13), T['napishi'], 0.3, 1.2),
      (SNAP, T['netupi'] - 0.3, 0.8), (z(19), T['netupi'] - 0.3, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={e[3]-0.15}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
