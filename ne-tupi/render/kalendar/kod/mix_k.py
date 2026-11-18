"""Звук «Листок на 66 тысяч»: голос + эффекты из ne-tupi-zvuki/gotovye, громкость эффектов ×0.5."""
import subprocess, glob
from tm import T, B, END, DUR
Z = '/mnt/project-files/ne-tupi-zvuki/gotovye/'
def z(n): return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
SNAP = '/mnt/project-files/ne-tupi-render/zvuk/sfx/snap.mp3'
VZ = [23, 24, 25, 43]
ev = []
for k in range(1, len(B)):   # вжух с басом на каждую смену сцены (кроме тишины перед «подвохом»)
    if k in (13,): continue
    ev.append((z(VZ[k % 4]), B[k] - 0.35, 0.35))
for tt in (T['brosish'] - 0.5, T['kalendar'] - 0.4, T['sto'] - 0.45, T['odna'] - 0.45, T['pervyy'] + 0.1):   # внутренние склейки
    ev.append((z(43), tt, 0.3))
ev += [
    (z(22), T['listok'] - 0.1, 0.25, 0.4), (z(22), T['shest'] - 0.05, 0.25, 0.4), (z(22), T['tysyach'] - 0.05, 0.25, 0.4),   # «шурх» закраски
    (z(13), T['shest'] - 0.1, 0.25, 0.6), (z(26), T['shest'], 0.35),
    (z(22), B[1] + 0.15, 0.25, 0.4), (z(22), B[1] + 0.5, 0.25, 0.4), (z(22), B[1] + 0.85, 0.25, 0.4),
    (z(13), B[2] + 0.1, 0.25, 0.4), (z(4), B[2] + 0.1, 0.3), (z(13), B[3] + 0.1, 0.25, 0.5), (z(4), B[3] + 0.1, 0.3),
    (z(13), B[4] + 0.1, 0.25, 0.5), (z(14), B[4] + 0.2, 0.3),
    (z(4), T['kopit'] + 0.25, 0.3), (z(10), T['kopit'] + 0.4, 0.3), (z(4), T['pyatnice'] - 0.25, 0.3), (z(20), T['vsyo1'] - 0.05, 0.45), (z(16), T['vsyo1'] + 0.1, 0.25),
    (SNAP, T['stop'] - 0.05, 0.8),
    (z(33), T['desyat'] - 0.15, 0.3), (z(14), T['desyat'] + 0.35, 0.5), (z(42), T['desyat'] + 0.4, 0.3), (z(8), T['mozg'], 0.3),
    (z(13), B[8] + 0.05, 0.25, 0.5), (z(4), T['priyom'] - 0.1, 0.3), (z(13), T['kalendar'] - 0.05, 0.25, 0.8),
    (z(40), B[9], 0.3), (z(35), T['kazhdom'], 0.3),
    (z(13), T['lyuboy'] - 0.1, 0.25, 0.5), (z(22), T['lyuboy'] - 0.05, 0.3, 0.4), (z(10), T['otkladyvaesh'] + 0.4, 0.4), (z(4), T['rubley'] - 0.1, 0.3),
    (z(13), T['deneg'] - 0.05, 0.25, 0.5), (z(22), T['zakras1'] + 0.15, 0.3, 0.4), (z(16), T['byvaet'] - 0.05, 0.25),
    (z(34), B[12] - 0.3, 0.45), (z(26), T['trista2'] - 0.05, 0.5), (z(9), T['trista2'] + 0.2, 0.35),
    (z(36), T['podvoh'] - 0.5, 0.4),
    (z(29), B[14] + 0.1, 0.25, 1.5), (z(8), T['dekabre'] - 0.1, 0.3), (z(26), T['brosish'] - 0.15, 0.4), (z(16), T['brosish'] + 0.1, 0.3), (z(10), T['brosish'] + 0.2, 0.3),
    (z(13), B[15] + 0.05, 0.25, 0.6), (z(4), T['samyy'] - 0.3, 0.35), (z(35), T['samyy'], 0.3),
    (z(13), T['slozhi'] - 0.1, 0.25, 1.3), (z(28), T['summa'], 0.25, 2.1), (z(20), T['pyat'] + 0.2, 0.5), (z(9), T['pyat'] + 0.3, 0.35),
    (z(13), B[18] + 0.05, 0.25, 0.6), (z(4), T['sto'] - 0.1, 0.3), (z(4), T['den'] - 0.1, 0.3), (z(14), T['odna'] - 0.05, 0.3),
    (z(4), T['raspechatay'] - 0.05, 0.3), (z(14), T['raspechatay'] + 0.55, 0.3), (z(5), T['holodilnik'] - 0.1, 0.35),
    (z(22), T['pervyy'] - 0.1, 0.3, 0.4), (z(7), T['pervyy'] + 0.2, 0.35), (z(13), T['pervyy'] + 0.45, 0.25, 0.5), (z(35), T['pervyy'] + 0.6, 0.35),
    (SNAP, T['netupi'] - 0.75, 0.8), (z(19), T['netupi'] - 0.75, 0.35), (z(2), END + 0.75, 0.4)]
inp = ['-i', 'voice.wav']; fl = []; lab = ['[0:a]']
for k, e in enumerate(ev):
    f, t, v = e[:3]; inp += ['-i', f]; ms = int(max(0, t) * 1000)
    tr = f'atrim=0:{e[3]},afade=t=out:st={max(0, e[3]-0.15)}:d=0.15,' if len(e) > 3 else ''
    fl.append(f'[{k+1}:a]{tr}volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('ok', DUR, len(ev))
