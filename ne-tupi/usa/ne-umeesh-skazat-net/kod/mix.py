import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tl import wt, DUR, GAPS
from scenes import SHOTS
SF = '/mnt/project-files/ne-tupi-render/zvuk/sfx'
ev = [('snap', wt(0, 'Стоп') - 0.05, 0.8), ('snap', wt(8, 'тупи') - 0.2, 0.8)]
for sh in SHOTS[1:]: ev.append(('whoosh', sh['t'], 0.22))
for g0, g1 in GAPS: ev.append(('whoosh', g0, 0.5)); ev.append(('ding', g0 + 0.35, 0.35))
for sh in SHOTS:
    for kind, ta, te, kw in sh['els']:
        if kind == 'plate': ev.append(('pop', ta, 0.3))
        if kind == 'check': ev.append(('ding', ta, 0.25))
        if kind == 'strike': ev.append(('pop', ta, 0.25))
ev.sort(key=lambda e: e[1])
inp = ['-i', 'zvuk/voice.wav']; fl = []; lab = ['[0:a]']
for k, (n, t, v) in enumerate(ev):
    inp += ['-i', f'{SF}/{n}.mp3']; ms = max(0, int(t * 1000))
    fl.append(f'[{k + 1}:a]volume={v*0.5:.3f},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
open('mixfilter.txt', 'w').write(';'.join(fl))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex_script', 'mixfilter.txt', '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print(len(ev))
