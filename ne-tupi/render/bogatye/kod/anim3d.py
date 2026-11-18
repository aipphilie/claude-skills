"""Анимации человечка: 3D-модель с плоским рендером (выглядит как 2D, но может поворачиваться).
Стиль: flat (по умолчанию, чистый силуэт) или toon (лёгкая тень), переменная STYLE.
Позы берутся из anim.py (те же ключевые кадры), плюс 3D-анимации с поворотом.
Запуск (из папки с 3d/index.html, при запущенном http.server 8777):
  python3 anim3d.py <out> [имя ...]"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anim

anim.BASE.update(yaw=0, laF=0, raF=0, lsw=0, rsw=0, pitch=0)
YAW = -10   # лёгкий поворот на 3/4, чтобы был виден объём


def a_povorot():
    n = 72
    keys = [(0, dict(yaw=0)), (16, dict(yaw=-90)), (40, dict(yaw=-90)), (56, dict(yaw=0)), (71, dict(yaw=0))]
    mouths = ["rest"] * 16 + anim.talk_track(24, seed=4) + ["rest"] * 32
    return anim.timeline(keys, n), mouths


def a_shag_profil():
    n = 32
    A, B = dict(lsw=25, rsw=-25, laF=-0.7, raF=0.7, la=(8, 4), ra=(8, 4), sink=0), dict(lsw=-25, rsw=25, laF=0.7, raF=-0.7, la=(8, 4), ra=(8, 4), sink=0)
    mid = dict(lsw=0, rsw=0, laF=0, raF=0, sink=-6)
    keys = [(0, dict(A, yaw=-90)), (8, mid), (16, B), (24, mid), (31, A)]
    return anim.timeline(keys, n), anim.mouths_const(n)


def a_tashit_v_goru():
    """Тащит тяжёлый груз в гору: профиль вправо, корпус наклонён вперёд, руки за спиной держат мешок,
    короткий медленный шаг с проседанием. Мешок рисуется в монтаже по точке anchors.json["back"]."""
    n = 40
    arms = dict(la=(28, 125), ra=(22, 130), laF=-1.6, raF=-1.6)
    A = dict(arms, yaw=90, pitch=28, lsw=-18, rsw=14, sink=10)
    mid = dict(lsw=-2, rsw=-2, sink=2)
    B = dict(lsw=14, rsw=-18, sink=10)
    keys = [(0, A), (10, mid), (20, B), (30, mid), (39, A)]
    return anim.timeline(keys, n), anim.mouths_const(n)


def a_tashit_legko():
    """Тот же груз, но легко: корпус почти прямой, быстрый шаг с подскоком."""
    n = 24
    arms = dict(la=(25, 120), ra=(20, 125), laF=-1.4, raF=-1.4)
    A = dict(arms, yaw=90, pitch=6, lsw=-24, rsw=22, sink=4, dy=0)
    mid = dict(lsw=0, rsw=0, sink=-2, dy=18)
    B = dict(lsw=22, rsw=-24, sink=4, dy=0)
    keys = [(0, A), (6, mid), (12, B), (18, mid), (23, A)]
    return anim.timeline(keys, n), anim.mouths_const(n, "smile")


ANIMS = {k: v for k, v in anim.ANIMS.items()}
ANIMS["tashit-v-goru"] = ("Тащит груз в гору", a_tashit_v_goru)
ANIMS["tashit-legko"] = ("Несёт груз легко", a_tashit_legko)
ANIMS["povorot"] = ("Поворот в профиль", a_povorot)
ANIMS["shag-profil"] = ("Шаг в профиль", a_shag_profil)
OWN_YAW = {"povorot", "shag-profil", "tashit-v-goru", "tashit-legko"}


def to3d(p, m, name):
    q = dict(la=list(p["la"]), ra=list(p["ra"]), head=p["head"], head_dy=p["head_dy"] / 100, lean=p["lean"],
             dy=-p["dy"] / 100, sink=p["sink"] / 100, llift=p["llift"] / 100, rlift=p["rlift"] / 100,
             yaw=p["yaw"] + (0 if name in OWN_YAW else YAW), laF=p["laF"], raF=p["raF"], lsw=p["lsw"], rsw=p["rsw"], pitch=p.get("pitch", 0), mouth=m)
    return q


if __name__ == "__main__":
    out = sys.argv[1]
    names = sys.argv[2:] or list(ANIMS)
    jobs = {}
    for n in names:
        poses, mouths = ANIMS[n][1]()
        jobs[n] = [to3d(p, m, n) for p, m in zip(poses, mouths)]
    os.makedirs(out, exist_ok=True)
    json.dump(jobs, open(f"{out}/frames.json", "w"))
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["node", f"{here}/3d/frames.js", f"{out}/frames.json", f"{out}/kadry", os.environ.get("STYLE", "flat")], check=True)
    os.makedirs(f"{out}/gif", exist_ok=True); os.makedirs(f"{out}/mp4", exist_ok=True)
    for n in names:
        d = f"{out}/kadry/{n}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", f"{d}/%03d.png",
                        "-vf", "scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=32[p];[b][p]paletteuse",
                        "-loop", "0", f"{out}/gif/{n}.gif"], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-stream_loop", "2", "-i", f"{d}/%03d.png",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", f"{out}/mp4/{n}.mp4"], check=True)
