"""Превью 1280x720 для «Почему денег нет, даже когда зарплата растёт». По шаблону ne-umeesh-skazat-net/prevyu/prevyu.py."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "ne-znayu-chego-hochu", "prevyu", "prevyu.py")
sys.argv = [sys.argv[0]]
src = open(BASE).read().split("# A. «НЕ ИЩИ СЕБЯ»")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {HERE!r}")
src = src.replace('os.path.join(HERE, "..", "..", "..", "ne-tupi-branding")', "'/mnt/project-files/ne-tupi-branding'")
g = {}; exec(src, g)
fig, plate, render, W, H, YEL, INK = g['fig'], g['plate'], g['render'], g['W'], g['H'], g['YEL'], g['INK']
feed_src = open(BASE).read().split("# Как это выглядит в ленте телефона")[1].split("feed([(A")[0]
exec("from PIL import Image, ImageDraw, ImageFont\nimport os\n#" + feed_src, g)
RED = "#E23030"; WATER = "#78AAEB"

def phone(x, y, w=230, h=400, rot=-8, text="0 ₽"):
    return (f'<g transform="rotate({rot},{x+w/2},{y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#fff" stroke="#111" stroke-width="12"/>'
            f'<rect x="{x+w/2-34}" y="{y+18}" width="68" height="12" rx="6" fill="#111"/>'
            f'<text x="{x+w/2}" y="{y+120}" font-family="Inter" font-weight="900" font-size="30" text-anchor="middle" fill="#999">БАЛАНС</text>'
            f'<text x="{x+w/2}" y="{y+235}" font-family="Inter" font-weight="900" font-size="104" text-anchor="middle" fill="{RED}">{text}</text></g>')

def stairs(x0, y0, n=3, sw=150, sh=95):
    out = ""
    for i in range(n):
        x = x0 + i * sw; y = y0 - (i + 1) * sh
        out += f'<rect x="{x}" y="{y}" width="{sw}" height="{(i+1)*sh}" fill="#E6E3DC"/>'
        out += f'<text x="{x+sw/2}" y="{y+62}" font-family="Inter" font-weight="900" font-size="54" text-anchor="middle" fill="#B5B1A8">+</text>'
    return out

def bucket(cx, cy, s=1.0):
    tw, bw, h = 300 * s, 220 * s, 250 * s; top, bot = cy - h / 2, cy + h / 2
    out = (f'<polygon points="{cx-tw/2},{top} {cx+tw/2},{top} {cx+bw/2},{bot} {cx-bw/2},{bot}" fill="#fff" stroke="#111" stroke-width="12" stroke-linejoin="round"/>'
           f'<polygon points="{cx-bw/2-6},{bot-34*s} {cx+bw/2+6},{bot-34*s} {cx+bw/2},{bot-6} {cx-bw/2},{bot-6}" fill="{WATER}"/>'
           f'<path d="M{cx-tw/2+10},{top} Q{cx},{top-190*s} {cx+tw/2-10},{top}" fill="none" stroke="#111" stroke-width="9"/>')
    for side, fy in ((-1, 0.35), (1, 0.55), (-1, 0.8), (1, 0.85)):
        half = tw / 2 + (bw / 2 - tw / 2) * fy; hx = cx + side * (half - 4); hy = top + h * fy
        out += f'<circle cx="{hx}" cy="{hy}" r="{17*s}" fill="#111"/>'
        for j in range(3):
            q = (j + 1) / 3.2
            out += f'<circle cx="{hx + side*(25+70*q)*s}" cy="{hy + (30*q + 150*q*q)*s}" r="{11*s}" fill="{WATER}"/>'
    # кран
    fx = cx - 40 * s; fy0 = top - 230 * s
    out += (f'<rect x="{fx-110*s}" y="{fy0-20*s}" width="{130*s}" height="{40*s}" rx="10" fill="#111"/>'
            f'<rect x="{fx-20*s}" y="{fy0}" width="{40*s}" height="{55*s}" rx="8" fill="#111"/>'
            f'<rect x="{fx-10*s}" y="{fy0+55*s}" width="{20*s}" height="{top+200*s-fy0-55*s}" fill="{WATER}"/>')
    return out

# A. белый фон, «ГДЕ ДЕНЬГИ?», человечек в шоке смотрит в телефон с «0 ₽», за ним лестница повышений
A = render("A-gde-dengi",
           fig(790, 900, 0.74, mouth="A", head=-8, head_dy=6, ra=(95, 15), la=(25, 8), lean=4)
           + phone(1000, 230, rot=8)
           + plate(40, 230, ["ГДЕ", "ДЕНЬГИ?"], 120))
# B. жёлтый фон, чёрная плашка «ОПЯТЬ НОЛЬ», дырявое ведро под краном, человечек разводит руками
B = render("B-opyat-nol",
           bucket(1090, 500, 0.95)
           + fig(770, 900, 0.74, mouth="wow", head=10, head_dy=6, ra=(80, 10), la=(25, 8), lean=-3)
           + plate(40, 220, ["ОПЯТЬ", "НОЛЬ"], 130, fill=INK, color=YEL), bg=YEL)
g['feed']([(A, "Почему денег нет, даже когда зарплата растёт"), (B, "Почему денег нет, даже когда зарплата растёт"),
           ("/mnt/project-files/ne-tupi-youtube/ne-umeesh-skazat-net/prevyu/A-da-ladno-neudobno.png", "Почему ты всем говоришь «да»")],
          os.path.join(HERE, "v-lente.png"))
print(A, B)
