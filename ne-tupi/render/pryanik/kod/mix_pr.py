"""Звук: голос + эффекты из ne-tupi-zvuki/gotovye по списку склеек и акцентов (sfx.json из compose_k.py). Эффекты ×0.5."""
import subprocess, glob, json, os
Z = os.environ.get('ZVUKI', '/mnt/project-files/ne-tupi-zvuki/gotovye/')
def z(n):
    if n == 'A': return Z + '44-angely-hor.mp3'
    if n == 'B': return Z + '45-ukus-hrum.mp3'
    return glob.glob(f'{Z}{n:02d}-*.mp3')[0]
# имя: ([варианты файлов], громкость, обрезка сек, опережение сек)
M = {'whoosh': ([1, 3], .40, .7, .12), 'bass': ([23, 25, 43], .40, .75, .15), 'boom': ([26], .50, 1.0, .03), 'thud': ([14], .40, .6, .0),
     'tick': ([28], .30, 1.4, .0), 'tick2': ([29], .30, 1.1, .0), 'boing': ([42], .35, .8, .0), 'heart': ([41], .45, 1.2, .0), 'stamp': ([20], .50, .6, .02),
     'alarm': ([21], .35, .7, .0), 'riser': ([18], .30, 1.5, .0), 'drop': ([27], .40, 1.2, .0), 'pop': ([4], .30, .5, .0), 'swipe': ([3], .30, .6, .05),
     'ok': ([7], .30, 1.0, .0), 'click': ([5], .35, .5, .0), 'crack': ([32], .40, .7, .0), 'ding': ([6], .30, 1.0, .0), 'error': ([8], .28, .8, .0),
     'clang': ([19], .40, 1.2, .0), 'kassa': ([9], .35, 1.3, .0), 'msg': ([12], .35, .6, .0), 'zoomin': ([33], .40, .8, .1), 'final': ([19], .40, 1.5, .0),
     'scratch': ([15], .40, .8, .0), 'coins': ([10], .35, 1.2, .0), 'shine': ([35], .35, 1.0, .0), 'notif': ([11], .35, 1.0, .0), 'angel': (['A'], .45, 2.6, .0), 'crunch': (['B'], .45, .7, .0)}
J = json.load(open('sfx.json')); DUR = J['dur']; cnt = {}
inp = ['-i', '../zvuk/voice.mp3']; fl = []; lab = ['[0:a]']
for k, (t, name) in enumerate(J['ev']):
    files, v, cut, lead = M[name]; i = cnt.get(name, 0); cnt[name] = i + 1
    inp += ['-i', z(files[i % len(files)])]; ms = int(max(0, t - lead) * 1000)
    fl.append(f'[{k+1}:a]atrim=0:{cut},afade=t=out:st={cut-0.15}:d=0.15,volume={v*0.5},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab) + f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[out]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', '../mix-v1.m4a'], check=True)
print('ok', DUR, len(J['ev']))
