"""Риг человечка «Не тупи», v3.
Тело — один столбик одной ширины от плеч до пят, ноги отделены только щелью между ними.
Руки начинаются от плеч, но плечи не выступают (рука вписана в скругление верха).
Руки и ноги заканчиваются полукругом. Из деталей только рот."""
import math

W, H = 1080, 1920
INK = "#111111"
CX, GROUND = 540, 1660

BODY_W = 190          # ширина столбика
GAP = 22              # щель между ногами
LEG_W = (BODY_W - GAP) / 2
LEG_L = 400           # от промежности до пола
TORSO_H = 400         # от промежности до макушки корпуса
ARM_W = 56
UPPER, FORE = 175, 165
HEAD_R = 130

POSE = dict(dx=0, dy=0, lean=0, head=0, head_dy=0, head_gap=-18,
            la=(20, 2), ra=(20, 2), ll=(0, 0), rl=(0, 0), mouth="rest")


def pt(o, ang, length, side):
    a = math.radians(ang)
    return (o[0] + side * math.sin(a) * length, o[1] + math.cos(a) * length)


def stroke(pts, w):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def mouth_svg(m, k=1.0):
    def line(d):
        return f'<path d="{d}" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>'

    def ell(rx, ry):
        t = (f'<ellipse cx="0" cy="{ry*0.6:.1f}" rx="{rx*0.6:.1f}" ry="{ry*0.33:.1f}" fill="#cfcfcf" '
             f'clip-path="url(#mc)"/>') if ry > 20 else ""
        return f'<clipPath id="mc"><ellipse rx="{rx}" ry="{ry}"/></clipPath><ellipse rx="{rx}" ry="{ry}" fill="#fff"/>{t}'

    def opn(w, h):
        top = -h * 0.25
        d = (f"M{-w},{top:.1f} Q0,{top-6:.1f} {w},{top:.1f} Q{w*0.95:.1f},{top+h*1.3:.1f} 0,{top+h*1.25:.1f} "
             f"Q{-w*0.95:.1f},{top+h*1.3:.1f} {-w},{top:.1f} Z")
        t = (f'<ellipse cx="0" cy="{top+h*1.15:.1f}" rx="{w*0.55:.1f}" ry="{h*0.4:.1f}" fill="#cfcfcf" '
             f'clip-path="url(#mc)"/>') if h > 25 else ""
        return f'<clipPath id="mc"><path d="{d}"/></clipPath><path d="{d}" fill="#fff"/>{t}'

    shapes = {
        "rest": lambda: line("M-34,0 Q0,18 34,0"),
        "M": lambda: line("M-30,4 L30,4"),
        "A": lambda: opn(44, 44),
        "E": lambda: opn(50, 18),
        "O": lambda: ell(25, 31),
        "U": lambda: ell(14, 16),
        "smile": lambda: opn(54, 36),
        "sad": lambda: line("M-32,14 Q0,-6 32,14"),
        "wow": lambda: ell(22, 36),
    }
    return f'<g transform="scale({k:.3f})">{shapes[m]()}</g>'


def torso_path():
    """Корпус: скруглённый верх, прямые бока, снизу — полукруглая арка промежности.
    Координаты от промежности (0,0) вверх."""
    r = BODY_W / 2
    g = GAP / 2
    top = -TORSO_H
    return (f'<path d="M{-r},{top + r} A{r},{r} 0 0 1 {r},{top + r} L{r},{LEG_W/2} '
            f'L{g},{LEG_W/2} L{g},0 A{g},{g} 0 0 0 {-g},0 L{-g},{LEG_W/2} L{-r},{LEG_W/2} Z" fill="{INK}"/>')


def shoulder(side):
    """Плечо внутри скругления верха: круг руки касается края изнутри, поэтому плеча не видно."""
    r = BODY_W / 2
    c = (0, -TORSO_H + r)
    d = r - ARM_W / 2
    a = math.radians(62)          # угол от вертикали
    return (c[0] + side * d * math.sin(a), c[1] - d * math.cos(a) + 18)


def figure(**kw):
    p = dict(POSE, **kw)
    crotch = (CX + p["dx"], GROUND - LEG_L - LEG_W / 2 + p["dy"])

    legs = ""
    for side, (a1, a2) in ((-1, p["ll"]), (1, p["rl"])):
        o = (crotch[0] + side * (GAP / 2 + LEG_W / 2), crotch[1])
        half = (LEG_L) / 2
        k = pt(o, a1, half, side)
        e = pt(k, a1 - a2, half, side)
        legs += stroke([o, k, e], LEG_W + 1.5)

    arms = ""
    for side, (a1, a2) in ((-1, p["la"]), (1, p["ra"])):
        o = shoulder(side)
        k = pt(o, a1, UPPER, side)
        e = pt(k, a1 + a2, FORE, side)
        arms += stroke([o, k, e], ARM_W)

    neck_y = -TORSO_H
    hc_y = neck_y - HEAD_R - p["head_gap"] + p["head_dy"]
    head = (f'<g transform="rotate({p["head"]} 0 {neck_y})">'
            f'<circle cy="{hc_y:.1f}" r="{HEAD_R}" fill="{INK}"/>'
            f'<g transform="translate(0,{hc_y + HEAD_R*0.36:.1f})">{mouth_svg(p["mouth"], HEAD_R/135)}</g></g>')

    upper = (f'<g transform="translate({crotch[0]:.1f},{crotch[1]:.1f}) rotate({p["lean"]})">'
             f'{torso_path()}{head}{arms}</g>')
    shadow = f'<ellipse cx="{CX+p["dx"]}" cy="{GROUND+12}" rx="190" ry="18" fill="#000" opacity="0.07"/>'
    return shadow + legs + upper


def svg(scale=1.0, **kw):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="100%" height="100%" fill="#fff"/>'
            f'<g transform="translate({CX},{GROUND}) scale({scale}) translate({-CX},{-GROUND})">'
            f'{figure(**kw)}</g></svg>')
