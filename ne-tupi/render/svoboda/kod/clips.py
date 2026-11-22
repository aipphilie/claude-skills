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
D = dict(dad=1, bw=1.12, th=0.98, lh=0.95)
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
 'phone': cus(lambda u: dict(ra=[62, 48], raF=1.5, la=[10, 4], head=-10, head_dy=0.05, lean=1.5 * s(u * 3), yaw=0), mouth='smile'),
 'reach': cus(lambda u: dict(ra=[78 + 4 * s(u * 5), -6], raF=0.6, la=[12, 4], lean=5, yaw=0)),
 'd_idle': std('dyhanie', 'smile', **D), 'd_hips': std('ruki-v-boki', **D), 'd_shrug': std('pozhimaet-plechami', **D), 'd_wave': std('mashet', 'smile', **D),
 'd_armsup': cus(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), mouth='smile', **D),
 'd_reach': cus(lambda u: dict(ra=[120 + 4 * s(u * 5), -6], raF=0.4, la=[12, 4], lean=2, yaw=0), mouth='smile', **D),
 'd_keys': cus(lambda u: dict(ra=[110 + 6 * s(u * 7), 20], raF=0.5, la=[30, 80], laF=0.6, lean=2 * s(u * 3), yaw=0), mouth='smile', **D),
 'self': cus(lambda u: dict(ra=[30, 120], raF=0.9, la=[30, 120], laF=0.9, lean=2 * s(u * 4), yaw=0), mouth='smile'),
 'think': cus(lambda u: dict(ra=[40, 125], raF=1.0, la=[30, 80], laF=0.7, head=-8 + 2 * s(u * 3), lean=-2, yaw=0)),
 'give': cus(lambda u: dict(ra=[80 + 4 * s(u * 6), 0], raF=1.0, la=[12, 4], lean=4, head=-4, yaw=0), mouth='sad'),
 'g_idle': std('dyhanie', 'smile', **G), 'g_sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad', **G),
 'g_shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), mouth='wow', **G),
 'v_idle': std('dyhanie', **V), 'v_sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad', **V),
 'd_shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), mouth='wow', **D),
 'd_sad': cus(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), mouth='sad', **D),
 'g_walkR': [dict(f, yaw=90, **G) for f in std('shag-profil')], 'd_walkR': [dict(f, yaw=90, **D) for f in std('shag-profil')], 'v_walkR': [dict(f, yaw=90, **V) for f in std('shag-profil')],
 'cheer': cus(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), mouth='smile'),
 'g_cheer': cus(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), mouth='smile', **G),
 'd_cheer': cus(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), mouth='smile', **D),
 'v_cheer': cus(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), mouth='smile', **V),
 'box': cus(lambda u: dict(la=[55, 70], ra=[55, 70], laF=0.5, raF=0.5, head=-10, lean=1.5 * s(u * 3), yaw=0), mouth='sad'),
 'v_smile': std('dyhanie', 'smile', **V), 'v_shock': cus(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), mouth='wow', **V),
 'v_hips': std('ruki-v-boki', **V), 'v_nod': std('kivok', 'smile', **V), 'v_explain': std('obyasnyaet', 'smile', **V), 'v_point': std('ukazyvaet-vbok', **V),
 'v_think': cus(lambda u: dict(ra=[40, 125], raF=1.0, la=[30, 80], laF=0.7, head=-8 + 2 * s(u * 3), lean=-2, yaw=0), **V),
 'v_read': cus(lambda u: dict(la=[52, 62], ra=[52, 62], laF=0.55, raF=0.55, head=-16 + 2 * s(u * 2), head_dy=0.05, lean=1 * s(u * 3), yaw=0), mouth='smile', **V),
 'v_box': cus(lambda u: dict(la=[55, 70], ra=[55, 70], laF=0.5, raF=0.5, head=-4, lean=1.5 * s(u * 3), yaw=0), mouth='smile', **V),
 'v_boss': cus(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=-3, head=6, yaw=0), mouth='smile', **V),
 'v_pointcam': cus(lambda u: dict(ra=[86 + 3 * s(u * 8), -4], raF=1.6, la=[22, 6], lean=3, head=4, yaw=0), mouth='smile', **V),
 'v_shrug': std('pozhimaet-plechami', **V), 'v_armsup': cus(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), mouth='smile', **V),
 'laugh': cus(lambda u: dict(la=[30, 110], ra=[30, 110], laF=0.8, raF=0.8, lean=-6 + 5 * s(u * 22), head=8 + 4 * s(u * 22), yaw=0, dy=0.06 * abs(s(u * 22))), mouth='A'),
}
C['g_box'] = cus(lambda u: dict(la=[55, 70], ra=[55, 70], laF=0.5, raF=0.5, head=-4, lean=1.5 * s(u * 6), yaw=0, dy=0.05 * abs(s(u * 10))), mouth='wow', **G)
C['g_phone'] = cus(lambda u: dict(ra=[62, 48], raF=1.5, la=[10, 4], head=-10, head_dy=0.05, lean=1.5 * s(u * 3), yaw=0), mouth='wow', **G)
C['g_scream'] = cus(lambda u: dict(la=[150 + 10 * s(u * 18), 12], ra=[150 - 10 * s(u * 18), 12], lean=2 * s(u * 18), yaw=0, dy=0.12 * abs(s(u * 9))), mouth='wow', **G)
C['scream'] = cus(lambda u: dict(la=[150 + 10 * s(u * 18), 12], ra=[150 - 10 * s(u * 18), 12], lean=2 * s(u * 18), yaw=0, dy=0.12 * abs(s(u * 9))), mouth='A')
C['v_box'] = cus(lambda u: dict(la=[55, 70], ra=[55, 70], laF=0.5, raF=0.5, head=-4, lean=1.5 * s(u * 6), yaw=0), mouth='wow', **V)
C['whisper'] = cus(lambda u: dict(ra=[70, 120], raF=0.7, la=[12, 4], head=6, lean=6 + 1.5 * s(u * 3), yaw=0), mouth='rest')
R = dict(rich=1, bw=1.15)
def rr(name, mouth=None): return std(name, mouth, **R)
def rc(fn, mouth='rest'): return cus(fn, mouth=mouth, **R)
C['r_idle'] = rr('dyhanie', 'smile'); C['r_hips'] = rr('ruki-v-boki', 'smile'); C['r_shrug'] = rr('pozhimaet-plechami'); C['r_wave'] = rr('mashet', 'smile')
C['r_point'] = rr('ukazyvaet-vbok', 'smile'); C['r_walkR'] = [dict(f, yaw=90, **R) for f in std('shag-profil')]
C['r_laugh'] = rc(lambda u: dict(la=[30, 110], ra=[30, 110], laF=0.8, raF=0.8, lean=-6 + 5 * s(u * 22), head=8 + 4 * s(u * 22), yaw=0, dy=0.06 * abs(s(u * 22))), 'A')
C['r_boss'] = rc(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=-3, head=6, yaw=0), 'smile')
C['r_armsup'] = rc(lambda u: dict(la=[150 + 8 * s(u * 6), 12], ra=[150 - 8 * s(u * 6), 12], lean=3 * s(u * 6), yaw=0), 'smile')
C['r_hug'] = rc(lambda u: dict(la=[95 + 6 * s(u * 5), 25], ra=[95 - 6 * s(u * 5), 25], laF=0.4, raF=0.4, lean=2 * s(u * 5), head=5, yaw=0), 'A')
C['r_give'] = rc(lambda u: dict(ra=[80 + 4 * s(u * 6), 0], raF=1.0, la=[12, 4], lean=4, head=4, yaw=0), 'smile')
C['r_box'] = rc(lambda u: dict(la=[55, 70], ra=[55, 70], laF=0.5, raF=0.5, head=4, lean=1.5 * s(u * 3), yaw=0), 'smile')
C['r_shock'] = rc(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), 'wow')
C['r_sad'] = rc(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), 'sad')
C['r_cheer'] = rc(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), 'smile')
C['r_drink'] = rc(lambda u: dict(ra=[120 + 10 * s(u * 4), 60], raF=0.6, la=[150 - 10 * s(u * 7), 12], lean=-4 + 4 * s(u * 7), head=6 + 4 * s(u * 7), yaw=0), 'A')
C['r_pointcam'] = rc(lambda u: dict(ra=[86 + 3 * s(u * 8), -4], raF=1.6, la=[22, 6], lean=3, head=4, yaw=0), 'smile')
C['r_phone'] = rc(lambda u: dict(ra=[62, 48], raF=1.5, la=[10, 4], head=-10, head_dy=0.05, lean=1.5 * s(u * 3), yaw=0), 'smile')
C['r_shh'] = rc(lambda u: dict(ra=[70, 120], raF=0.7, la=[12, 4], head=6, lean=6 + 1.5 * s(u * 3), yaw=0), 'smile')
C['laugh'] = cus(lambda u: dict(la=[30, 110], ra=[30, 110], laF=0.8, raF=0.8, lean=-6 + 5 * s(u * 22), head=8 + 4 * s(u * 22), yaw=0, dy=0.06 * abs(s(u * 22))), mouth='A')
C['think'] = cus(lambda u: dict(ra=[40, 125], raF=1.0, la=[30, 80], laF=0.7, head=-8 + 2 * s(u * 3), lean=-2, yaw=0))
C['run'] = [dict(f, yaw=90, lean=8) for f in std('shag-profil')]

W_ = dict(waiter=1); H_ = dict(tophat=1, bw=1.05)
def wr(name, mouth=None): return std(name, mouth, **W_)
def wc(fn, mouth='rest'): return cus(fn, mouth=mouth, **W_)
def hc(fn, mouth='rest'): return cus(fn, mouth=mouth, **H_)
C['w_idle'] = wr('dyhanie', 'smile'); C['w_sad'] = wc(lambda u: dict(head=-14, head_dy=0.15, la=[8, 0], ra=[8, 0], lean=0, yaw=0), 'sad')
C['w_shock'] = wc(lambda u: dict(la=[60, -20], ra=[60, -20], lean=-5, head=2 * s(u * 40), yaw=0, dy=0.15 * abs(s(u * 20))), 'wow')
C['w_jaw'] = wc(lambda u: dict(ra=[70, 40], raF=1.3, la=[60, -20], lean=-4, head=3 * s(u * 30), yaw=0), 'A')      # держит чек, челюсть отвисла
C['w_tray'] = wc(lambda u: dict(ra=[95, -95], raF=0.4, la=[12, 4], lean=1.5 * s(u * 3), head=4, yaw=0), 'smile')    # поднос на ладони
C['w_hat'] = wc(lambda u: dict(ra=[62, 48], raF=1.0, la=[62, 48], laF=1.0, head=-8, lean=1.5 * s(u * 3), yaw=0), 'sad')    # протягивает шляпу
C['w_shrug'] = wr('pozhimaet-plechami'); C['w_walkR'] = [dict(f, yaw=90, **W_) for f in std('shag-profil')]
C['w_bow'] = wc(lambda u: dict(la=[20, 4], ra=[70, 60], raF=0.8, pitch=0, lean=0, head=-18 + 4 * s(u * 4), head_dy=0.1, yaw=0), 'smile')
C['w_cheer'] = wc(lambda u: dict(la=[150 + 20 * s(u * 14), 12], ra=[150 - 20 * s(u * 14), 12], lean=0, yaw=0, dy=0.25 * abs(s(u * 7))), 'smile')
C['w_rip'] = wc(lambda u: dict(la=[110 + 25 * s(u * 10), 40], ra=[110 - 25 * s(u * 10), 40], laF=0.8, raF=0.8, lean=3 * s(u * 10), yaw=0), 'A')
C['h_boss'] = hc(lambda u: dict(la=[38, 95], ra=[38, 95], laF=0.9, raF=0.9, lean=-4, head=10, yaw=0), 'smile')
C['h_throw'] = hc(lambda u: dict(ra=[60 + 50 * (0.5 + 0.5 * s(u * 5)), -20], raF=0.8, la=[30, 100], laF=0.8, lean=-3, head=10, yaw=0), 'smile')
C['h_laugh'] = hc(lambda u: dict(la=[30, 110], ra=[30, 110], laF=0.8, raF=0.8, lean=-6 + 5 * s(u * 22), head=8 + 4 * s(u * 22), yaw=0, dy=0.06 * abs(s(u * 22))), 'A')
C['h_walkR'] = [dict(f, yaw=90, **H_) for f in std('shag-profil')]
C['h_wave'] = std('mashet', 'smile', **H_)
C['pay'] = cus(lambda u: dict(ra=[80 + 4 * s(u * 6), 0], raF=1.0, la=[12, 4], lean=4, head=-4, yaw=0), mouth='sad')
C['read'] = cus(lambda u: dict(la=[52, 62], ra=[52, 62], laF=0.55, raF=0.55, head=-16 + 2 * s(u * 2), head_dy=0.05, lean=1 * s(u * 3), yaw=0), mouth='rest')
C['read_shock'] = cus(lambda u: dict(la=[52, 62], ra=[52, 62], laF=0.55, raF=0.55, head=-6 + 2 * s(u * 30), lean=-3, yaw=0), mouth='wow')
C['turn'] = cus(lambda u: dict(la=[52, 62], ra=[52, 62], laF=0.55, raF=0.55, head=-6, lean=0, yaw=max(0, 70 - u * 50)), mouth='M', n=60)
C['angry'] = cus(lambda u: dict(la=[40, 100], ra=[40, 100], laF=0.5, raF=0.5, lean=4 * s(u * 18), head=-6, yaw=0, dy=0.08 * abs(s(u * 9))), mouth='A')
C['sign'] = cus(lambda u: dict(la=[160, 0], ra=[160, 0], lean=2 * s(u * 8), yaw=0, dy=0.1 * abs(s(u * 8))), mouth='A')
C['slot'] = cus(lambda u: dict(ra=[125 - 55 * (0.5 + 0.5 * s(u * 6)), -8], raF=0.9, la=[14, 4], lean=3, head=-4, yaw=0), mouth='smile')
C['hammer'] = cus(lambda u: dict(ra=[150 - 75 * abs(s(u * 6)), 8], raF=0.9, la=[95, 30], laF=0.7, lean=2, head=6, yaw=0), mouth='smile')
C['wrist'] = cus(lambda u: dict(la=[72, 75], laF=0.6, ra=[14, 4], head=-12 + 2 * s(u * 20), head_dy=0.05, lean=2, yaw=0), mouth='wow')
C['phone_scr'] = cus(lambda u: dict(ra=[62 + 6 * abs(s(u * 9)), 48], raF=1.5, la=[10, 4], head=-12, head_dy=0.05, lean=1.5 * s(u * 3), yaw=0), mouth='rest')
C['explain'] = std('obyasnyaet', 'smile'); C['scratch'] = std('cheshet-golovu'); C['pointup'] = std('ukazyvaet-vverh'); C['nod'] = std('kivok', 'smile'); C['phone'] = C['phone']
# --- «Если бы деньги были не важны» (диван) ---
SIT = dict(lsw=85, rsw=85, dy=-3.4, yaw=30)
C['dream'] = cus(lambda u: dict(ra=[40, 125], raF=1.0, la=[30, 80], laF=0.7, head=8 + 3 * s(u * 2), lean=-3 + 1.5 * s(u * 2), yaw=0), mouth='smile')
C['lie'] = cus(lambda u: dict(la=[6, 0], ra=[6, 0], head=4 * s(u * 2), lean=0, yaw=0, lsw=4 * s(u * 3)), mouth='smile')
C['lie_remote'] = cus(lambda u: dict(la=[6, 0], ra=[40 + 6 * s(u * 5), 30], raF=0.3, head=3 * s(u * 2), lean=0, yaw=0), mouth='smile')
C['fall'] = cus(lambda u: dict(la=[150 + 20 * s(u * 20), 30], ra=[150 - 20 * s(u * 20), 30], lsw=20 * s(u * 18), rsw=-20 * s(u * 18), lean=0, yaw=0), mouth='wow')
C['give'] = cus(lambda u: dict(ra=[75 + 10 * s(u * 6), 10], raF=1.0, la=[12, 4], lean=4, head=-6, yaw=0), mouth='smile')
C['sit'] = cus(lambda u: dict(SIT, la=[20, 2], ra=[20, 2], lean=1.5 * s(u * 3)), mouth='smile')
C['sit_thumb'] = cus(lambda u: dict(SIT, la=[70 + 15 * s(u * 7), -20], ra=[150 + 6 * s(u * 5), 10], lean=6 * s(u * 3.5)), mouth='smile')
C['work'] = cus(lambda u: dict(la=[60 + 8 * s(u * 14), 50], ra=[60 - 8 * s(u * 14), 50], laF=0.6, raF=0.6, head=-6 + 2 * s(u * 3), lean=2, yaw=0), mouth='smile')
C['tired'] = cus(lambda u: dict(la=[60 + 4 * s(u * 6), 50], ra=[60 - 4 * s(u * 6), 50], laF=0.6, raF=0.6, head=-16, head_dy=0.12, lean=4, yaw=0), mouth='sad')
C['pressed'] = cus(lambda u: dict(la=[165, 5], ra=[165, 5], head=-8, lean=2 * s(u * 18), yaw=0, sink=0.6), mouth='A')
C['carry'] = cus(lambda u: dict(ra=[20, 4], raF=0.9, la=[12, 4], lean=2 * s(u * 3), yaw=0), mouth='smile')
C['carryR'] = [dict(f, yaw=90, ra=[22, 6]) for f in std('shag-profil', 'smile')]
KEEP = ['idle', 'idle_smile', 'shock', 'shrug', 'think', 'pointcam', 'walkR', 'net', 'cheer', 'hips', 'explain', 'scratch',
        'pointup', 'nod', 'stop', 'lie', 'give', 'point', 'sad', 'g_walkR', 'd_walkR', 'v_walkR', 'carryR', 'run', 'g_idle', 'v_idle', 'd_idle']
C = {k: C[k] for k in KEEP}
json.dump(C, open('clips.json', 'w')); print({k: len(v) for k, v in C.items()}, sum(len(v) for v in C.values()))
