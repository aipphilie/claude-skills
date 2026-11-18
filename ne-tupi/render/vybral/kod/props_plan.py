"""План 3D-предметов по кадрам: props_at(t) -> [(params, cx, cy, size_px)]. Запуск: собирает уникальные кадры в props.json."""
import json, math
from words import B, END, DUR, wt
FPS = 24; N = int(DUR * FPS)
def clamp(v, a=0, b=1): return max(a, min(b, v))
def back(x):
    x = clamp(x); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def q(v, s=1): return round(v / s) * s
T = dict(vybral=wt('выбрал'), sam=wt('сам.'), pokazal=wt('показал'), skazal=wt('сказал'), stroyu=wt('строю'), zhizn=wt('жизнь', 1),
         navsegda=wt('навсегда'), shkaf=wt('шкаф'), polivaesh=wt('поливаешь'), vyanet=wt('вянет'), vybrali=wt('выбрали'), cvetok=wt('цветок'))
def props_at(t):
    out = []
    beat = 1 + 0.08 * max(0, math.sin(t * 9))   # «стук» сердца
    if B[0] <= t < B[1] and t >= T['vybral'] - 0.25:
        k = back((t - T['vybral'] + 0.25) / 0.35); f = eio((t - T['sam'] - 0.05) / 0.6)
        x = 760 + (300 - 760) * f; y = 700 - math.sin(f * math.pi) * 60
        out.append((dict(kind='heart', ry=q(math.sin(t * 3) * 30, 3), beat=q(beat, .02)), x, y, 220 * k))
    if B[3] <= t < B[4]:
        t0 = T['pokazal'] + 0.15
        if t >= t0 and t < T['skazal'] + 0.3:
            f = eio((t - t0) / 0.9); x = 300 + (820 - 300) * f; y = 760 - math.sin(f * math.pi) * 380
            k = back((t - t0) / 0.25)
            out.append((dict(kind='heart', ry=q(f * 360 + t * 40, 3), beat=q(beat, .02)), x, y, 260 * k))
        if t >= T['stroyu'] - 0.5:
            u = eio((t - T['stroyu'] + 0.5) / 0.6)
            out.append((dict(kind='house', ry=q(-25 + 10 * math.sin(t * 1.5), 1), rx=8, grow=q(max(0.02, u), .04)), 540, 1060, 560))
        if t >= T['zhizn'] - 0.2:
            k = back((t - T['zhizn'] + 0.2) / 0.35)
            out.append((dict(kind='rings', ry=q(t * 90 % 360, 3), rx=10), 540, 600, 330 * k))
    if B[4] <= t < B[5]:
        if t >= T['navsegda'] - 0.2:
            k = back((t - T['navsegda'] + 0.2) / 0.3)
            out.append((dict(kind='clock', tick=q(t * 2.0 % 12, 0.05), ry=-15, rz=q(math.sin(t * 40) * 4, 1)), 830, 520, 240 * k))
        if t >= T['shkaf'] - 0.1:
            k = back((t - T['shkaf'] + 0.1) / 0.3)
            out.append((dict(kind='heart', gray=1, ry=-20), 800, 795 - 0 * k, 170 * k))
    if B[5] <= t < B[6]:
        w = eio((t - T['polivaesh'] - 0.2) / (T['vyanet'] + 0.6 - T['polivaesh'] - 0.2))
        k = back((t - B[5]) / 0.35)
        out.append((dict(kind='flower', wilt=q(w, .02), ry=q(math.sin(t * 1.2) * 25, 1)), 640, 900, 760 * k))
    if B[6] <= t < B[8]:
        w = 1 - eio((t - B[6] - 0.3) / 1.6)
        out.append((dict(kind='flower', wilt=q(w, .02), ry=q(math.sin(t * 1.2) * 20, 1)), 150, 1140, 360))
        if T['vybrali'] - 0.2 <= t < B[7]:
            k = back((t - T['vybrali'] + 0.2) / 0.35)
            out.append((dict(kind='heart', ry=q(math.sin(t * 3) * 25, 3), beat=q(beat, .02)), 680, 640, 280 * k))
    return out
if __name__ == '__main__':
    uniq = {}; plan = []
    for i in range(N):
        row = []
        for p, x, y, s in props_at(i / FPS):
            if s < 5: continue
            key = json.dumps(p, sort_keys=True)
            if key not in uniq: uniq[key] = len(uniq)
            row.append((uniq[key], x, y, s))
        plan.append(row)
    json.dump({'p': [json.loads(k) for k in uniq]}, open('props.json', 'w')); json.dump(plan, open('props_plan.json', 'w'))
    print(len(uniq), 'уникальных кадров предметов')
