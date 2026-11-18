"""Звук «Где деньги?»: голос + редкие эффекты (не чаще одного на ~4 сек) + тихая лоу-фай подложка с приглушением под голос
и секундой тишины на трёх откровениях."""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tl import wt, DUR, GAPS
from scenes import SHOTS, SILENCE, HOLE_T
SF = '/mnt/project-files/ne-tupi-render/zvuk/sfx'
fixed = [('snap', wt(0, 'Стоп') - 0.05, 0.8), ('snap', wt(8, 'тупи') - 0.2, 0.7), ('ding', wt(4, 'Пикнуло') - 0.05, 0.3)]
for g0, g1 in GAPS: fixed += [('whoosh', g0, 0.4), ('ding', g0 + 0.35, 0.25)]
cand = [('pop', h, 0.3) for h in HOLE_T if h]
for sh in SHOTS:
    for kind, ta, te, kw in sh['els']:
        if kind == 'plate' and kw.get('sz', 0) >= 60: cand.append(('whoosh', ta, 0.18))
        if kind == 'source': cand.append(('pop', ta, 0.2))
        if kind == 'bucket' and kw.get('mine'): cand.append(('pop', kw['mine'], 0.3))
ev = list(fixed)
for e in sorted(cand, key=lambda e: e[1]):
    if all(abs(e[1] - f[1]) >= 4.0 for f in ev): ev.append(e)
ev.sort(key=lambda e: e[1])
inp = ['-i', 'zvuk/voice.wav', '-i', 'zvuk/muzyka-podlozhka.mp3']; fl = []; lab = []
fl.append('[0:a]asplit=2[v][vsc]')
sil = '+'.join(f'between(t,{s:.2f},{s + 1.0:.2f})' for s in SILENCE)
fl.append(f"[1:a]aloop=loop=-1:size=2000000000,atrim=0:{DUR},asetpts=N/SR/TB,volume=0.3,volume=0:enable='{sil}',"
          f"afade=t=in:d=1.5:st={wt(0, 'где') - 0.3:.2f},afade=t=out:d=3:st={DUR - 3:.2f}[m0]")
fl.append('[m0][vsc]sidechaincompress=threshold=0.04:ratio=3:attack=30:release=500[m]')
lab = ['[v]', '[m]']
# музыка вступает на «Так где деньги?» (до этого — тишина под голосом)
for k, (n, t, v) in enumerate(ev):
    inp += ['-i', f'{SF}/{n}.mp3']; ms = max(0, int(t * 1000))
    fl.append(f'[{k + 2}:a]volume={v*0.5:.3f},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
open('mixfilter.txt', 'w').write(';'.join(fl))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex_script', 'mixfilter.txt', '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print(len(ev), 'effects')
