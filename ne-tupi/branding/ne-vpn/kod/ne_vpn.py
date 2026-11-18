"""Картинки для бота «NE VPN» в стиле «Не тупи». Запуск: python3 ne_vpn.py
Человечек из того же рига, что и аватарка канала (rig3.py)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cairosvg, rig3

OUT = os.path.dirname(HERE)
YEL, INK, WHITE = "#FFD60A", "#111111", "#FFFFFF"
FONT = 'font-family="Inter" font-weight="900"'


def hand(side, a1, a2, lean=0):
    """Где окажется конец руки (абсолютные координаты рига)."""
    crotch = (rig3.CX, rig3.GROUND - rig3.LEG_L - rig3.LEG_W / 2)
    o = rig3.shoulder(side)
    k = rig3.pt(o, a1, rig3.UPPER, side)
    e = rig3.pt(k, a1 + a2, rig3.FORE, side)
    return crotch[0] + e[0], crotch[1] + e[1]


def shield(cx, cy, s, fill, hole, stroke=None):
    d = (f"M0,{-s} C{s*0.45},{-s*0.72} {s*0.75},{-s*0.78} {s*0.9},{-s*0.8} L{s*0.9},{-s*0.05} "
         f"C{s*0.9},{s*0.6} {s*0.45},{s*0.95} 0,{s*1.12} C{-s*0.45},{s*0.95} {-s*0.9},{s*0.6} {-s*0.9},{-s*0.05} "
         f"L{-s*0.9},{-s*0.8} C{-s*0.75},{-s*0.78} {-s*0.45},{-s*0.72} 0,{-s} Z")
    st = f' stroke="{stroke}" stroke-width="{s*0.09:.1f}" stroke-linejoin="round"' if stroke else ""
    key = (f'<circle cy="{-s*0.12:.1f}" r="{s*0.2:.1f}" fill="{hole}"/>'
           f'<path d="M{-s*0.1:.1f},{-s*0.05:.1f} L{s*0.1:.1f},{-s*0.05:.1f} L{s*0.15:.1f},{s*0.48:.1f} '
           f'L{-s*0.15:.1f},{s*0.48:.1f} Z" fill="{hole}"/>')
    return f'<g transform="translate({cx:.1f},{cy:.1f})"><path d="{d}" fill="{fill}"{st}/>{key}</g>'


def png(svg, name, w, h):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name),
                     output_width=w, output_height=h)


def square(name, box, bg, body, extra=""):
    x, y, s = box
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="{x} {y} {s} {s}">'
           f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{bg}"/>{body}{extra}</svg>')
    png(svg, name, 640, 640)


def band(x, y, s, txt, fill, color, at=0.66):
    h = s * 0.2
    by = y + s * at
    return (f'<rect x="{x}" y="{by}" width="{s}" height="{h}" fill="{fill}"/>'
            f'<text x="{x+s/2}" y="{by+h*0.73}" {FONT} font-size="{h*0.66}" '
            f'text-anchor="middle" fill="{color}" letter-spacing="3">{txt}</text>')


# ---------- Фото бота (аватар 640×640) ----------
RA_UP = (150, 12)
hx, hy = hand(1, *RA_UP)

# A. Белый фон, человечек поднял жёлтый щит (реком.)
box = (195, 290, 840)
fig = rig3.figure(mouth="smile", ra=RA_UP, head=-6)
square("avatar-A-shchit.png", box, WHITE,
       shield(hx + 20, hy - 95, 120, YEL, INK, stroke=INK) + fig)

# B. Жёлтый фон, чёрная лента «NE VPN» (как вариант 7 у канала)
b = (220, 450, 660)
square("avatar-B-lenta.png", b, YEL, rig3.figure(mouth="smile", head=-6),
       band(*b, "NE VPN", INK, YEL))

# C. Жёлтый фон, человечек «О!» с белым щитом
square("avatar-C-zheltyj.png", box, YEL,
       shield(hx + 20, hy - 95, 120, WHITE, INK, stroke=INK) +
       rig3.figure(mouth="O", ra=RA_UP, head=-6))


# ---------- Стартовая картинка 1280×720 ----------
def start(name, mouth="smile"):
    W, H = 1280, 720
    k = 0.5                      # масштаб человечка
    fx, fy = 940, 700             # куда ставим ноги (центр, земля)
    fig = rig3.figure(mouth=mouth, ra=RA_UP, head=-6)
    sh = shield(hx + 20, hy - 95, 120, YEL, INK, stroke=INK)
    g = (f'<g transform="translate({fx},{fy}) scale({k}) translate({-rig3.CX},{-rig3.GROUND})">'
         f'{sh}{fig}</g>')
    txt = (f'<text x="90" y="300" {FONT} font-size="150" fill="{INK}" letter-spacing="-2">NE VPN</text>'
           f'<text x="94" y="380" font-family="Inter" font-weight="700" font-size="44" fill="{INK}">'
           f'Включил — и не тупи.</text>'
           f'<rect x="90" y="430" width="470" height="76" rx="38" fill="{YEL}"/>'
           f'<text x="325" y="481" font-family="Inter" font-weight="800" font-size="34" '
           f'text-anchor="middle" fill="{INK}">Подключение за минуту</text>'
           f'<text x="94" y="640" font-family="Inter" font-weight="600" font-size="28" fill="#8a8a8a">'
           f'от канала «Не тупи»</text>')
    deco = f'<circle cx="{fx}" cy="380" r="300" fill="{YEL}" opacity="0.22"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{WHITE}"/>{deco}{txt}{g}</svg>')
    png(svg, name, W, H)


start("start-kartinka.png")
print("ok", hx, hy)
