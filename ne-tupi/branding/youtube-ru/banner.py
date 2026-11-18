"""Шапка YouTube (2560x1440 + 2048x1152) для русского канала. Запуск: python3 banner.py
Лежит в branding/youtube-ru/, риг человечка берётся из branding/rig3.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import cairosvg, rig3
from PIL import Image, ImageFont

W, H = 2560, 1440
SX, SY, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423   # зона, видимая на всех устройствах
YEL, INK = "#FFD60A", "#111111"
NAME = "НЕ ТУПИ"
TAG1 = "Твой личный ассистент по жизни."
TAG2 = "Финансы. Привычки. Голова."
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"

def fig(x, y, h, **pose):
    s = h / 1102
    return f'<g transform="translate({x},{y}) scale({s}) translate(-540,-576)">{rig3.figure(**pose)}</g>'

def banner(out, guides=False):
    words = NAME.rsplit(" ", 1)
    fs = 165
    tx, ty = SX + 20, SY + 172
    f = ImageFont.truetype(FONT, fs)
    first_w = f.getlength(words[0] + " ") - 3 * (len(words[0]) + 1)
    last_w = f.getlength(words[1]) - 3 * len(words[1])
    parts = [
        f'<rect width="{W}" height="{H}" fill="#fff"/>',
        f'<circle cx="{SX-260}" cy="{SY+60}" r="34" fill="{YEL}"/>',
        f'<circle cx="{SX+SW+300}" cy="{SY+SH-40}" r="22" fill="{YEL}"/>',
        f'<circle cx="{SX+SW+180}" cy="{SY+20}" r="12" fill="{INK}"/>',
        f'<rect x="{tx+first_w-14}" y="{ty-fs*0.62}" width="{last_w+28}" height="{fs*0.78}" rx="10" fill="{YEL}"/>',
        f'<text x="{tx}" y="{ty}" font-family="Inter" font-weight="900" font-size="{fs}" fill="{INK}" letter-spacing="-3">{NAME}</text>',
        f'<text x="{tx+4}" y="{ty+122}" font-family="Inter" font-weight="800" font-size="58" fill="{INK}">{TAG1}</text>',
        f'<text x="{tx+4}" y="{ty+196}" font-family="Inter" font-weight="500" font-size="52" fill="#555">{TAG2}</text>',
        fig(SX + SW - 300, SY + 16, 395, mouth="smile", la=(98, -6), ra=(20, 2), head=6),
    ]
    if guides:
        parts.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="none" stroke="red" stroke-width="4" stroke-dasharray="20 12"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(parts)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=out)

big = os.path.join(HERE, "banner-2560x1440.png")
banner(big)
banner(os.path.join(HERE, "banner-guides.png"), guides=True)
im = Image.open(big).convert("RGB")
im.resize((2048, 1152), Image.LANCZOS).save(os.path.join(HERE, "banner-2048x1152.png"), optimize=True)
im.crop((SX, SY, SX + SW, SY + SH)).save(os.path.join(HERE, "preview-phone.png"))
