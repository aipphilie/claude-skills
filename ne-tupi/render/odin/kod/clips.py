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
C = {
 'idle': std('dyhanie'), 'idle_smile': std('dyhanie', 'smile'), 'idle_sad': std('dyhanie', 'sad'),
 'shrug': std('pozhimaet-plechami'), 'net': std('net', 'sad'), 'scratch': std('cheshet-golovu'),
 'hips': std('ruki-v-boki'), 'explain': std('obyasnyaet', 'smile'), 'point': std('ukazyvaet-vbok'),
 'wave': std('mashet', 'smile'), 'jump': std('pryzhok', 'wow'), 'walk': std('shag-profil'),
 'walkR': [dict(f, yaw=90) for f in std('shag-profil')], 'turn': std('povorot'),
 'push': std('tashit-v-goru'), 'nod': std('kivok', 'smile'),
 'sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad'),
 'scared': cus(lambda u: dict(la=[125 + 6 * s(u * 30), -35], ra=[125 - 6 * s(u * 30), -35], laF=0.5, raF=0.5, lean=-7 + 1.5 * s(u * 40), head=3 * s(u * 37), yaw=0, sink=0.15), mouth='wow'),
 'stop': cus(lambda u: dict(la=[88, 6], ra=[88, 6], laF=1.2, raF=1.2, lean=2 * s(u * 25), yaw=0), mouth='A'),
 'armsup': cus(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), mouth='smile'),
 'jumpjoy': cus(lambda u: dict(la=[160, 10], ra=[160, 10], dy=1.0 * abs(s(u * 7)), sink=0.25 * (1 - abs(s(u * 7))) ** 4, yaw=-10), mouth='smile'),
 'dig': cus(lambda u: dict(la=[55 + 25 * s(u * 9), -15], ra=[35 + 25 * s(u * 9), 20], laF=0.6, raF=0.6, lean=-8 - 8 * s(u * 9), head=-6, yaw=20, sink=0.2 + 0.15 * s(u * 9))),
 'climb': cus(lambda u: dict(la=[165 + 12 * s(u * 8), 8], ra=[165 - 12 * s(u * 8), 8], lean=4 * s(u * 8), yaw=0, head=-4), mouth='E'),
 'carry': cus(lambda u: dict(la=[70, -30], ra=[70, -30], laF=0.9, raF=0.9, lean=-4 + 2 * s(u * 8), sink=0.1 + 0.08 * s(u * 8), yaw=0)),
 'pointcam': cus(lambda u: dict(ra=[86 + 3 * s(u * 8), -4], raF=1.6, la=[22, 6], lean=3, head=4, yaw=0), mouth='smile'),
 'hugL': cus(lambda u: dict(la=[82, -10], ra=[70, -20], laF=0.2, raF=0.6, lean=6, head=8 + 2 * s(u * 4), yaw=-25), mouth='smile'),
 'cross': cus(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=1.5 * s(u * 3), yaw=0)),
 'eat': cus(lambda u: dict(la=[30, 110 + 20 * s(u * 5)], ra=[24, 10], laF=0.8, head=-6, yaw=0)),
 'shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), mouth='wow'),
 'g_idle': std('dyhanie', **G), 'g_wave': std('mashet', 'smile', **G), 'g_shrug': std('pozhimaet-plechami', **G),
 'g_sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad', **G),
 'g_walk': std('shag-profil', **G), 'g_joy': cus(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), mouth='smile', **G),
 'g_hugR': cus(lambda u: dict(la=[70, -20], ra=[82, -10], laF=0.6, raF=0.2, lean=-6, head=-8 + 2 * s(u * 4), yaw=25), mouth='smile', **G),
}
json.dump(C, open('clips.json', 'w')); print({k: len(v) for k, v in C.items()}, sum(len(v) for v in C.values()))
