"""Макеты превью 1280x720 для ролика «Тебе 30, и ты не знаешь, чего хочешь».
Риг человечка берётся из ne-tupi-branding/rig3.py. Запуск: python3 prevyu.py"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "ne-tupi-branding"))
import cairosvg, rig3
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
YEL, INK, GREY = "#FFD60A", "#111111", "#D9D9D9"


def fig(x, y, s, **pose):
    """Человечек ступнями в точке (x, y), масштаб s."""
    return (f'<g transform="translate({x},{y}) scale({s}) translate({-rig3.CX},{-rig3.GROUND})">'
            f'{rig3.figure(**pose)}</g>')


def plate(x, y, lines, size, fill=YEL, color=INK, pad=22, gap=14):
    """Текст на плашке, по строке на плашку (как в стиле канала)."""
    out, cy = "", y
    for t in lines:
        w = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Black.otf", size).getlength(t) + pad * 2
        h = size * 1.12
        out += (f'<rect x="{x}" y="{cy}" width="{w:.0f}" height="{h:.0f}" rx="10" fill="{fill}"/>'
                f'<text x="{x+pad}" y="{cy+h*0.8:.0f}" font-family="Inter" font-weight="900" '
                f'font-size="{size}" fill="{color}">{t}</text>')
        cy += h + gap
    return out


def arrow(x1, y1, x2, y2, color, w=26):
    a = math.atan2(y2 - y1, x2 - x1)
    hl = w * 1.9
    bx, by = x2 - math.cos(a) * hl * 0.8, y2 - math.sin(a) * hl * 0.8
    p1 = (x2 - math.cos(a) * hl + math.sin(a) * hl * 0.75, y2 - math.sin(a) * hl - math.cos(a) * hl * 0.75)
    p2 = (x2 - math.cos(a) * hl - math.sin(a) * hl * 0.75, y2 - math.sin(a) * hl + math.cos(a) * hl * 0.75)
    return (f'<path d="M{x1},{y1} L{bx:.0f},{by:.0f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x2},{y2} L{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f} Z" fill="{color}" '
            f'stroke="{color}" stroke-width="6" stroke-linejoin="round"/>')


def render(name, body, bg="#fff"):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')
    path = os.path.join(HERE, name + ".png")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path)
    return path


# A. «НЕ ИЩИ СЕБЯ»: перекрёсток, все стрелки серые, одна жёлтая
cx, cy = 900, 660
roads = ""
for ang in (200, 225, 250, 290, 315, 340, 160):
    a = math.radians(ang)
    roads += arrow(cx + math.cos(a) * 230, cy - 60 + math.sin(a) * 120,
                   cx + math.cos(a) * 420, cy - 60 + math.sin(a) * 300, GREY, 22)
a = math.radians(270)
roads += arrow(cx + 230, cy - 380, cx + 320, cy - 600, YEL, 34)
A = render("A-ne-ishchi-sebya",
           roads + fig(cx, cy + 150, 0.74, mouth="smile", head=-8, la=(25, 5), ra=(150, 0))
           + plate(60, 210, ["НЕ ИЩИ", "СЕБЯ"], 120))

# B. «ЗРЯ»: ищет с огромной лупой
lupa = ('<circle cx="1050" cy="250" r="95" fill="#fff" stroke="#111" stroke-width="26"/>'
        '<circle cx="1050" cy="250" r="70" fill="#F4F4F4"/>'
        '<path d="M985,320 L905,410" stroke="#111" stroke-width="34" stroke-linecap="round"/>'
        '<text x="1050" y="290" font-family="Inter" font-weight="900" font-size="110" text-anchor="middle" '
        'fill="#BBBBBB">?</text>')
B = render("B-zrya",
           fig(820, 860, 0.76, mouth="wow", head=6, lean=-4, ra=(130, 20), la=(20, 2)) + lupa
           + plate(70, 250, ["ЗРЯ"], 210))

# C. Жёлтый фон, «УЖЕ ПОЗДНО?» и зачёркнутое 30
C = render("C-uzhe-pozdno",
           '<text x="1150" y="300" font-family="Inter" font-weight="900" font-size="300" text-anchor="middle" '
           'fill="#111" opacity="0.12">30</text>'
           + fig(980, 860, 0.76, mouth="A", head=10, head_dy=6, ra=(160, 60), la=(25, 5), lean=3)
           + plate(50, 220, ["УЖЕ", "ПОЗДНО?"], 116, fill=INK, color=YEL),
           bg=YEL)


# Как это выглядит в ленте телефона: превью + название под ним, 2 размера
def feed(items, out):
    font = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
    tw, th = 360, 203
    sheet = Image.new("RGB", (40 + len(items) * (tw + 40), 420), "#0F0F0F")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(font, 19)
    small = ImageFont.truetype(font, 15)
    for i, (p, title) in enumerate(items):
        x = 40 + i * (tw + 40)
        im = Image.open(p).convert("RGB")
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, 30))
        # мелкий размер, как в «рекомендуемых» справа
        sheet.paste(im.resize((168, 94), Image.LANCZOS), (x, 300))
        d.rectangle([x + tw - 54, 30 + th - 26, x + tw - 6, 30 + th - 6], fill="#000")
        d.text((x + tw - 50, 30 + th - 25), "11:02", font=small, fill="#fff")
        words, line, lines = title.split(), "", []
        for w_ in words:
            t = (line + " " + w_).strip()
            if d.textlength(t, font=f) > tw:
                lines.append(line); line = w_
            else:
                line = t
        lines.append(line)
        for j, l in enumerate(lines[:2]):
            d.text((x, 245 + j * 24), l, font=f, fill="#F1F1F1")
        d.text((x + 180, 310), "Не тупи\nмакет ленты", font=small, fill="#AAAAAA")
    sheet.save(out)


feed([(A, "Тебе 30, и ты не знаешь, чего хочешь"),
      (B, "Не знаешь, чего хочешь в 30? Перестань искать"),
      (C, "Почему в 30 ты не знаешь, чего хочешь")],
     os.path.join(HERE, "v-lente.png"))
print("ok")
