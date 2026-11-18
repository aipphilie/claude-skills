"""Клипы человечка (24 fps) для СДВГ-монтажа: каждый клип рендерится один раз, монтаж берёт кадры по локальному времени сцены."""
import json, math
import anim3d
FPS = 24
BASE = anim3d.to3d(anim3d.ANIMS['dyhanie'][1]()[0][0], 'rest', 'dyhanie')
def std(name, mouth=None, n=None, **kw):
    p, m = anim3d.ANIMS[name][1]()
    fr = [dict(anim3d.to3d(q, mm, name), **kw) for q, mm in zip(p, m)]
    if mouth: fr = [dict(f, mouth=mouth) for f in fr]
    return fr[:n] if n else fr
def cus(fn, n=48, mouth='rest', **kw):
    out = []
    for j in range(n):
        p = dict(BASE, mouth=mouth); p.update(fn(j / FPS)); p.update(kw); out.append(p)
    return out
s = math.sin
G = dict(girl=1, bw=0.9, th=0.9, lh=0.9)
V = dict(bw=1.22, th=0.92, lh=0.85, helmet=1)
C = {
 'idle': std('dyhanie'), 'idle_smile': std('dyhanie', 'smile'), 'idle_sad': std('dyhanie', 'sad'),
 'shrug': std('pozhimaet-plechami'), 'net': std('net', 'sad'), 'scratch': std('cheshet-golovu'),
 'hips': std('ruki-v-boki'), 'explain': std('obyasnyaet', 'smile'), 'point': std('ukazyvaet-vbok'), 'pointup': std('ukazyvaet-vverh'),
 'wave': std('mashet', 'smile'), 'jump': std('pryzhok', 'wow'), 'walk': std('shag-profil'),
 'walkR': [dict(f, yaw=90) for f in std('shag-profil')], 'nod': std('kivok', 'smile'),
 'sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad'),
 'stop': cus(lambda u: dict(la=[88, 6], ra=[88, 6], laF=1.2, raF=1.2, lean=2 * s(u * 25), yaw=0), mouth='A'),
 'armsup': cus(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), mouth='smile'),
 'pointcam': cus(lambda u: dict(ra=[86 + 3 * s(u * 8), -4], raF=1.6, la=[22, 6], lean=3, head=4, yaw=0), mouth='smile'),
 'cross': cus(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=1.5 * s(u * 3), yaw=0)),
 'shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), mouth='wow'),
 'push': std('tashit-v-goru'),
 'boss': cus(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=-3, head=6, yaw=0), mouth='smile'),
 'g_idle': std('dyhanie', **G), 'g_shrug': std('pozhimaet-plechami', **G), 'g_smile': std('dyhanie', 'smile', **G),
 'g_sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad', **G),
 'g_shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0), mouth='wow', **G),
 'v_idle': std('dyhanie', **V), 'v_shrug': std('pozhimaet-plechami', **V),
 'v_shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0), mouth='wow', **V),
}
json.dump(C, open('clips.json', 'w')); print({k: len(v) for k, v in C.items()}, sum(len(v) for v in C.values()))
