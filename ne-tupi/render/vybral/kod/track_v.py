"""Трек двух человечков рилса «Он выбрал тебя»: muzh (обычный) и zhena (девушка: каре, розовый бант, чуть тоньше и ниже).
Губы не синхроним (говорит закадровый голос), рот — эмоция по сценам."""
import json, sys, math
sys.path.insert(0, '/home/user/claude-skills/ne-tupi')
import anim3d
from words import B, END, DUR, wt
FPS = 24; N = int(DUR * FPS)
BASE = anim3d.to3d(anim3d.ANIMS['dyhanie'][1]()[0][0], 'rest', 'dyhanie')
def custom(name, n):
    out = []
    for j in range(n):
        u = j / FPS; p = dict(BASE)
        if name == 'jumpjoy':      # прыжки с руками вверх
            b = abs(math.sin(u * 7)); p.update(la=[160, 10], ra=[160, 10], dy=1.0 * b, sink=0.25 * (1 - b) ** 4, yaw=-10)
        elif name == 'armsup':     # руки вверх, покачивание
            b = math.sin(u * 6); p.update(la=[150 + 8 * b, 12], ra=[150 - 8 * b, 12], lean=3 * b)
        elif name == 'hug_r':      # тянется/обнимает вправо (девушка слева)
            b = math.sin(u * 4); p.update(la=[70, -20], ra=[82, -10], laF=0.6, raF=0.2, lean=-6, head=-8 + 2 * b, yaw=25)
        elif name == 'hug_l':      # обнимает влево (муж справа)
            b = math.sin(u * 4); p.update(la=[82, -10], ra=[70, -20], laF=0.2, raF=0.6, lean=6, head=8 + 2 * b, yaw=-25)
        elif name == 'point_r':    # уверенно показывает вправо
            p.update(ra=[92, -4], la=[22, 4], lean=-3, head=6, yaw=10)
        elif name == 'prof_r':     # стоит в профиль вправо (к двери)
            p.update(yaw=90)
        elif name == 'prof_l':
            p.update(yaw=-90)
        elif name == 'sad':        # голова вниз, руки висят
            p.update(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0)
        out.append(p)
    return out
CUSTOM = {'jumpjoy', 'armsup', 'hug_r', 'hug_l', 'point_r', 'prof_r', 'prof_l', 'sad'}
def frames_of(name, L):
    if name in CUSTOM: return custom(name, L)
    if name in ('walkL', 'walkR'):
        p, m = anim3d.ANIMS['shag-profil'][1](); fr = [anim3d.to3d(q, 'rest', 'shag-profil') for q in p]
        if name == 'walkR': fr = [dict(f, yaw=90) for f in fr]
        return (fr * (L // len(fr) + 1))[:L]
    if name in ('turnR', 'turnL'):   # поворот в профиль за 0.6 сек
        p, m = anim3d.ANIMS['povorot'][1](); fr = [anim3d.to3d(q, 'rest', 'povorot') for q in p[:16]]
        if name == 'turnR': fr = [dict(f, yaw=-f['yaw']) for f in fr]
        return (fr + [fr[-1]] * L)[:L]
    p, m = anim3d.ANIMS[name][1](); fr = [anim3d.to3d(q, mm, name) for q, mm in zip(p, m)]
    return (fr * (L // len(fr) + 1))[:L]
t = wt
SEG = {
 'muzh': [(0, 'walkL'), (1.55, 'jumpjoy'), (3.0, 'dyhanie'), (B[2], 'ruki-v-boki'), (t('ничего'), 'net'), (t('назначал'), 'pozhimaet-plechami'),
          (t('мог') - 0.15, 'turnR'), (t('просто', 1) + 0.0, 'walkR'), (16.95, 'prof_r'), (B[3], 'turnL'), (B[3] + 0.35, 'dyhanie'), (t('показал') - 0.25, 'point_r'),
          (t('сказал'), 'mashet'), (B[6], 'dyhanie'), (t('чувствовать'), 'hug_l'), (B[7], 'mashet'), (B[8], 'armsup'), (END + 0.1, 'turnL'), (END + 0.75, 'walkL')],
 'zhena': [(0, 'dyhanie'), (t('выбрал') - 0.1, 'kivok'), (B[1], 'dyhanie'), (t('выбирали'), 'pozhimaet-plechami'), (t('Братья'), 'razgovor-zhesty'),
           (t('Детям'), 'ukazyvaet-vverh'), (B[2], 'dyhanie'), (t('показал'), 'cheshet-golovu'), (t('тебя', 2) - 0.1, 'jumpjoy'), (t('сказал') + 0.3, 'armsup'),
           (B[4], 'ruki-v-boki'), (t('навсегда'), 'pozhimaet-plechami'), (t('шкаф'), 'obyasnyaet'), (B[5], 'cheshet-golovu'), (t('поливаешь'), 'sad'),
           (B[6], 'walkR'), (33.35, 'hug_r'), (B[7], 'mashet'), (B[8], 'armsup'), (END + 0.1, 'turnL'), (END + 0.75, 'walkL')]}
MOUTH = {
 'muzh': [(0, 'smile'), (B[2], 'rest'), (B[3] + 0.4, 'rest'), (t('показал'), 'smile'), (B[4], 'rest'), (B[6], 'smile')],
 'zhena': [(0, 'rest'), (t('выбрал'), 'smile'), (B[1], 'rest'), (t('показал'), 'wow'), (t('тебя', 2) + 0.4, 'smile'), (B[4], 'rest'), (t('подвох'), 'wow'),
           (t('поливаешь'), 'sad'), (B[6], 'rest'), (33.3, 'smile')]}
BUILD = {'muzh': {}, 'zhena': dict(girl=1, bw=0.9, th=0.9, lh=0.9)}
def at(lst, tt): return [v for a, v in lst if a <= tt][-1]
jobs, segs = {}, {}
for who, seg in SEG.items():
    out, so = [], []
    for si, (t0, nm) in enumerate(seg):
        t1 = seg[si + 1][0] if si + 1 < len(seg) else DUR
        L = int(round(t1 * FPS)) - len(out)
        if L <= 0: continue
        out += frames_of(nm, L); so += [nm] * L
    out = out[:N]; so = so[:N]
    jobs[who] = [dict(f, mouth=at(MOUTH[who], i / FPS) if f.get('mouth', 'rest') not in ('wow',) or True else f['mouth'], **BUILD[who]) for i, f in enumerate(out)]
    segs[who] = so
json.dump(jobs, open('track.json', 'w')); json.dump(segs, open('seg.json', 'w'))
print({k: len(v) for k, v in jobs.items()}, N)
