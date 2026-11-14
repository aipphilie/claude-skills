"""Анимации человечка «Не тупи»: ключевые кадры -> PNG-кадры 1080x1920, GIF и MP4.
Запуск: python3 anim.py <папка_вывода> [имя_анимации ...]"""
import sys, os, io, math, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg
import rig

FPS = 24
SCALE = 1.15
BASE = dict(rig.POSE)
BASE.pop("mouth")


def ease(t):
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    if isinstance(a, tuple):
        return tuple(lerp(x, y, t) for x, y in zip(a, b))
    return a + (b - a) * t


def timeline(keys, n):
    """keys: [(кадр, {поза})]. Поза наследует базовую и предыдущий ключ."""
    full, cur = [], dict(BASE)
    for f, k in keys:
        cur = dict(cur, **k)
        full.append((f, dict(cur)))
    out = []
    for i in range(n):
        for j in range(len(full) - 1):
            f0, p0 = full[j]
            f1, p1 = full[j + 1]
            if f0 <= i <= f1:
                t = ease((i - f0) / max(1, f1 - f0))
                out.append({k: lerp(p0[k], p1[k], t) for k in p0})
                break
        else:
            out.append(dict(full[-1][1]))
    return out


def talk_track(n, seed=1, hold=3, pause_every=None):
    """Рот под «речь»: случайная смена форм, каждые hold кадров. Для монтажа под озвучку
    формы потом будут браться из таймингов фонем."""
    rnd = random.Random(seed)
    seq, last = [], "M"
    pool = ["A", "E", "O", "A", "U", "M", "E", "A", "rest"]
    i = 0
    while len(seq) < n:
        if pause_every and i and i % pause_every == 0:
            seq += ["rest"] * (hold * 3)
        m = rnd.choice([x for x in pool if x != last])
        seq += [m] * hold
        last = m
        i += 1
    seq = seq[:n]
    seq[-hold:] = ["rest"] * hold
    return seq


def mouths_const(n, m="rest"):
    return [m] * n


# ---------------- анимации ----------------
def a_razgovor():
    """Говорит, руки спокойно, лёгкое покачивание головой."""
    n = 72
    poses = timeline([(0, dict(head=0, head_dy=0)), (18, dict(head=-3, head_dy=3)),
                      (36, dict(head=2, head_dy=0)), (54, dict(head=-2, head_dy=3)), (71, dict(head=0, head_dy=0))], n)
    return poses, talk_track(n, seed=3)


def a_razgovor_zhesty():
    """Говорит и объясняет руками."""
    n = 96
    poses = timeline([
        (0, dict(la=(20, 2), ra=(20, 2), head=0)),
        (12, dict(la=(55, 45), ra=(55, 45), head=-3)),
        (30, dict(la=(70, 30), ra=(40, 60), head=3)),
        (48, dict(la=(30, 50), ra=(80, 25), head=-4)),
        (66, dict(la=(60, 40), ra=(60, 40), head=2)),
        (84, dict(la=(20, 2), ra=(20, 2), head=0)),
        (95, dict()),
    ], n)
    return poses, talk_track(n, seed=7, pause_every=9)


def a_mashet():
    n = 48
    up = dict(ra=(110, 35), head=-6)
    keys = [(0, dict(ra=(20, 2), head=0)), (10, up)]
    f = 10
    for _ in range(3):
        keys += [(f + 5, dict(ra=(110, 70))), (f + 10, dict(ra=(110, 30)))]
        f += 10
    keys += [(47, dict(ra=(20, 2), head=0))]
    return timeline(keys, n), ["rest"] * 6 + ["smile"] * 36 + ["rest"] * 6


def a_obyasnyaet():
    n = 48
    keys = [(0, dict()), (12, dict(la=(75, 35), ra=(75, 35), head=-4)), (24, dict(la=(60, 50), ra=(60, 50), head=0)),
            (36, dict(la=(75, 35), ra=(75, 35), head=3)), (47, dict(la=(20, 2), ra=(20, 2), head=0))]
    return timeline(keys, n), talk_track(n, seed=11)


def a_ukazyvaet_vverh():
    n = 48
    keys = [(0, dict()), (10, dict(ra=(155, 10), head=-5)), (18, dict(ra=(150, 14))), (24, dict(ra=(158, 6))),
            (30, dict(ra=(150, 14))), (38, dict(ra=(155, 10))), (47, dict(ra=(20, 2), head=0))]
    return timeline(keys, n), ["rest"] * 8 + ["O"] * 10 + talk_track(30, seed=5)[:22] + ["rest"] * 8


def a_ukazyvaet_vbok():
    """Показывает рукой в сторону (туда можно ставить текст/картинку)."""
    n = 48
    keys = [(0, dict()), (10, dict(ra=(92, -4), head=6, lean=-2)), (20, dict(ra=(96, -8))),
            (30, dict(ra=(92, -4))), (38, dict(ra=(92, -4))), (47, dict(ra=(20, 2), head=0, lean=0))]
    return timeline(keys, n), ["rest"] * 8 + talk_track(32, seed=9) + ["rest"] * 8


def a_pozhimaet():
    n = 40
    keys = [(0, dict()), (10, dict(la=(45, 95), ra=(45, 95), head=10, head_dy=6)),
            (28, dict(la=(45, 95), ra=(45, 95), head=10, head_dy=6)), (39, dict(la=(20, 2), ra=(20, 2), head=0, head_dy=0))]
    return timeline(keys, n), ["rest"] * 8 + ["sad"] * 24 + ["rest"] * 8


def a_facepalm():
    n = 48
    keys = [(0, dict()), (10, dict(ra=(118, 100), head=8, head_dy=8, lean=2)),
            (36, dict(ra=(122, 104), head=10, head_dy=10, lean=2)), (47, dict(ra=(20, 2), head=0, head_dy=0, lean=0))]
    return timeline(keys, n), ["rest"] * 8 + ["sad"] * 32 + ["rest"] * 8


def a_ruki_v_boki():
    n = 36
    keys = [(0, dict()), (10, dict(la=(55, -100), ra=(55, -100), head=-3)), (26, dict(la=(55, -100), ra=(55, -100), head=-3)),
            (35, dict(la=(20, 2), ra=(20, 2), head=0))]
    return timeline(keys, n), ["rest"] * 8 + ["M"] * 20 + ["rest"] * 8


def a_dyhanie():
    n = 48
    keys = [(0, dict(sink=0, la=(20, 2), ra=(20, 2))), (24, dict(sink=8, la=(22, 4), ra=(22, 4))), (47, dict(sink=0, la=(20, 2), ra=(20, 2)))]
    return timeline(keys, n), mouths_const(n)


def a_kivok():
    n = 32
    keys = [(0, dict()), (7, dict(head_dy=18, head=0)), (13, dict(head_dy=0)), (20, dict(head_dy=18)), (31, dict(head_dy=0))]
    return timeline(keys, n), ["rest"] * 4 + ["smile"] * 24 + ["rest"] * 4


def a_net():
    n = 36
    keys = [(0, dict()), (6, dict(head=-12)), (12, dict(head=12)), (18, dict(head=-12)), (24, dict(head=10)), (35, dict(head=0))]
    return timeline(keys, n), ["M"] * n


def a_pokachivanie():
    n = 48
    keys = [(0, dict(lean=0)), (12, dict(lean=-4, head=3)), (36, dict(lean=4, head=-3)), (47, dict(lean=0, head=0))]
    return timeline(keys, n), mouths_const(n)


def a_shag():
    """Шаг на месте (вид спереди)."""
    n = 32
    keys = [(0, dict(llift=0, rlift=0, sink=0, la=(20, 2), ra=(20, 2))),
            (8, dict(llift=60, rlift=0, sink=6, la=(14, 2), ra=(28, 6))),
            (16, dict(llift=0, rlift=0, sink=0, la=(20, 2), ra=(20, 2))),
            (24, dict(llift=0, rlift=60, sink=6, la=(28, 6), ra=(14, 2))),
            (31, dict(llift=0, rlift=0, sink=0, la=(20, 2), ra=(20, 2)))]
    return timeline(keys, n), mouths_const(n)


def a_pryzhok():
    n = 36
    keys = [(0, dict()), (6, dict(sink=40, la=(30, 10), ra=(30, 10))),
            (14, dict(sink=0, dy=-220, la=(140, -25), ra=(140, -25))),
            (20, dict(dy=-220)),
            (27, dict(dy=0, sink=35, la=(40, 10), ra=(40, 10))),
            (35, dict(sink=0, la=(20, 2), ra=(20, 2)))]
    return timeline(keys, n), ["rest"] * 8 + ["wow"] * 18 + ["smile"] * 10


ANIMS = {
    "razgovor": ("Разговор", a_razgovor),
    "razgovor-zhesty": ("Разговор с жестами", a_razgovor_zhesty),
    "mashet": ("Машет", a_mashet),
    "obyasnyaet": ("Объясняет", a_obyasnyaet),
    "ukazyvaet-vverh": ("Указывает вверх", a_ukazyvaet_vverh),
    "ukazyvaet-vbok": ("В сторону", a_ukazyvaet_vbok),
    "pozhimaet-plechami": ("Пожимает плечами", a_pozhimaet),
    "cheshet-golovu": ("Чешет голову", a_facepalm),
    "ruki-v-boki": ("Руки в боки", a_ruki_v_boki),
    "dyhanie": ("Дыхание (стоит)", a_dyhanie),
    "kivok": ("Кивает «да»", a_kivok),
    "net": ("Мотает «нет»", a_net),
    "pokachivanie": ("Покачивается", a_pokachivanie),
    "shag": ("Шаг на месте", a_shag),
    "pryzhok": ("Прыжок", a_pryzhok),
}


def render(name, out, size=1080):
    poses, mouths = ANIMS[name][1]()
    d = os.path.join(out, "kadry", name)
    os.makedirs(d, exist_ok=True)
    for i, (p, m) in enumerate(zip(poses, mouths)):
        svg = rig.svg(scale=SCALE, mouth=m, **p)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f"{d}/{i:03d}.png",
                         output_width=size, output_height=int(size * 16 / 9))
    os.makedirs(f"{out}/gif", exist_ok=True)
    os.makedirs(f"{out}/mp4", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{d}/%03d.png",
                    "-vf", "scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse",
                    "-loop", "0", f"{out}/gif/{name}.gif"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-stream_loop", "2", "-i", f"{d}/%03d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", f"{out}/mp4/{name}.mp4"], check=True)
    return len(poses)


if __name__ == "__main__":
    out = sys.argv[1]
    names = sys.argv[2:] or list(ANIMS)
    for n in names:
        print(n, render(n, out))
