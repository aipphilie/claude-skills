"""Превью 1280x720 для «Почему ты всем говоришь "да"». По шаблону ne-znayu-chego-hochu/prevyu/prevyu.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ne-znayu-chego-hochu", "prevyu"))
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location("pv", '/mnt/project-files/ne-tupi-youtube/ne-znayu-chego-hochu/prevyu/prevyu.py')
# берём только функции, не перерисовывая старые превью
src = open(spec.origin).read().split("# A. «НЕ ИЩИ СЕБЯ»")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {HERE!r}")
src = src.replace('os.path.join(HERE, "..", "..", "..", "ne-tupi-branding")', "'/mnt/project-files/ne-tupi-branding'")
g = {}; src = src.replace("\"Не тупи\\nмакет ленты\"", "\"Ne Tupi\\nfeed mockup\"")
exec(src, g)
fig, plate, render, W, H, YEL, INK = g['fig'], g['plate'], g['render'], g['W'], g['H'], g['YEL'], g['INK']
feed_src = open(spec.origin).read().split("# Как это выглядит в ленте телефона")[1].split("feed([(A")[0]
feed_src = feed_src.replace("Не тупи\\nмакет ленты", "Ne Tupi\\nfeed mockup")
exec("from PIL import Image, ImageDraw, ImageFont\nimport os\n#" + feed_src, g)

def box(x, y, w, h, label, rot=0, fill="#fff", size=40):
    return (f'<g transform="rotate({rot},{x+w/2},{y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="10"/>'
            f'<rect x="{x+w/2-16}" y="{y+5}" width="32" height="{h-10}" fill="#E2DED5"/>'
            f'<text x="{x+w/2}" y="{y+h/2+size*0.36}" font-family="Inter" font-weight="900" font-size="{size}" text-anchor="middle" fill="#111">{label}</text></g>')

def tower(x0, y0, labels, w=300, h=104, size=42):
    out = ""; y = y0
    for i, l in enumerate(labels):
        dx = (-1) ** i * (8 + 6 * i); out += box(x0 + dx, y - h, w, h, l, rot=(-1) ** i * (2 + i * 0.8), size=size); y -= h - 2
    return out

LAB = ["LOAN", "SATURDAY", "MOVING", "BIRTHDAY", "\"1 HOUR\"", "COVER ME"]
# A. белый фон, «ДА ЛАДНО, НЕУДОБНО», человечек с натужной улыбкой держит гору чужих коробок
A = render("cover-ne-umeesh-a-eh-its-fine",
           tower(935, 760, LAB, w=275, h=112, size=38)
           + fig(790, 900, 0.74, mouth="smile", head=-12, lean=5, ra=(95, 15), la=(25, 8))
           + plate(40, 230, ["EH,", "IT'S FINE"], 120))
# B. жёлтый фон, чёрная плашка «ОПЯТЬ "ДА"?», коробки до потолка, рот «А»
B = render("cover-ne-umeesh-b-yes-again",
           tower(935, 760, LAB, w=275, h=112, size=36)
           + fig(770, 900, 0.74, mouth="A", head=8, head_dy=6, ra=(70, 5), la=(160, 40), lean=-4)
           + plate(40, 220, ["YES", "AGAIN?"], 130, fill=INK, color=YEL), bg=YEL)
g['feed']([(A, "Why You Say Yes to Everyone"), (B, "Why You Say Yes to Everyone"),
           ("/mnt/project-files/ne-tupi-usa/ne-znayu-chego-hochu/oblozhka/cover-ne-znayu-a-stop-looking.png", "You're 30 and Don't Know What You Want")],
          os.path.join(HERE, "cover-ne-umeesh-v-lente.png"))
print(A, B)
