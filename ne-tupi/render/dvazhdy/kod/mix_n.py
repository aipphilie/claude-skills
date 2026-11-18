"""Звук «Никогда не пропускай дважды»: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'
VZ = [23, 24, 25, 43]
ev = [(z(VZ[k % 4]), B[k] - 0.35, 0.35) for k in range(1, len(B))]
ev += [(z(43), T['vozvrashchayutsya'] - 0.5, 0.3)]
ev += [
    (z(22), 0.3, 0.25, 0.4), (z(13), 0.05, 0.25, 0.5),
    (z(4), T['tysyacham'], 0.3), (z(26), T['tysyacham'], 0.3),
    (z(13), B[2] + 0.1, 0.25, 0.5), (z(10), T['million'], 0.3), (z(13), B[3] + 0.1, 0.25, 0.4), (z(4), B[3] + 0.15, 0.3),
    (z(13), B[4] + 0.1, 0.25, 0.5), (z(4), B[4] + 0.15, 0.3),
    (z(4), B[5] + 0.05, 0.3), (z(4), B[5] + 0.17, 0.3), (z(4), B[5] + 0.29, 0.3), (z(16), T['brosali'] + 0.1, 0.25), (z(20), T['desyat'] - 0.05, 0.45),
    (z(22), B[6] + 0.1, 0.2, 0.3), (z(22), B[6] + 0.35, 0.2, 0.3), (z(22), B[6] + 0.6, 0.2, 0.3), (z(22), B[6] + 0.85, 0.2, 0.3), (z(13), B[6] + 0.1, 0.25, 1.2),
    (z(15), T['propustil'] + 0.2, 0.3), (z(7), T['normalno'], 0.3), (z(22), T['normalno'] + 0.1, 0.2, 0.3),
    (z(33), B[8], 0.3), (z(15), T['dva'] + 0.1, 0.25), (z(15), T['dva'] + 0.45, 0.25), (z(8), T['nelzya'] - 0.1, 0.35), (z(26), T['nelzya'], 0.35),
    (z(36), T['nikogda'] - 0.1, 0.4), (z(5), T['pochemu'] - 0.1, 0.3),
    (z(3), T['atomnye'] - 0.3, 0.3), (z(20), T['obyasnyaet'] + 0.1, 0.5),
    (z(33), B[12], 0.3), (z(8), T['norma'] - 0.2, 0.35),
    (z(26), T['razrushena'] - 0.05, 0.45), (z(16), T['razrushena'] + 0.2, 0.3),
    (z(29), B[15] + 0.05, 0.25, 1.0), (z(4), T['shest'] - 0.1, 0.3), (z(4), B[16], 0.3), (z(26), T['ni'] - 0.1, 0.4),
    (z(42), B[17] + 0.1, 0.3), (z(35), T['poluchilos'] - 0.1, 0.3),
    (z(22), T['vozvrashchayutsya'] + 0.3, 0.3, 0.4), (z(7), T['sleduyushchiy'], 0.35),
    (z(34), B[19] - 0.3, 0.4), (z(35), T['smog'] - 0.15, 0.35),
    (SNAP, T['netupi'] - 0.75, 0.8), (z(19), T['netupi'] - 0.75, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={max(0, e[3]-0.15)}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
