"""YouTube banner (2560x1440) for the English channel. Run: python3 banner.py [name]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import cairosvg, rig3

W, H = 2560, 1440
SX, SY, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423   # safe area (all devices)
YEL, INK = "#FFD60A", "#111111"
NAME = "NE TUPI"
TAG1 = "Your personal life assistant."
TAG2 = "Money. Habits. Your head."

def fig(x, y, h, **pose):
    # figure spans y 576..1678 in rig coords (≈1102 px), centred on x=540
    s = h / 1102
    return f'<g transform="translate({x},{y}) scale({s}) translate(-540,-576)">{rig3.figure(**pose)}</g>'

def banner(out, guides=False):
    words = NAME.rsplit(" ", 1)
    fs = 170
    tx, ty = SX + 20, SY + 175
    # yellow marker behind the last word
    from PIL import ImageFont
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Black.otf", fs)
    sp = -3 * len(NAME)
    first_w = f.getlength(words[0] + " ") - 3 * (len(words[0]) + 1)
    last_w = f.getlength(words[1]) - 3 * len(words[1])
    parts = [
        f'<rect width="{W}" height="{H}" fill="#fff"/>',
        # desktop-only accents outside safe area
        f'<circle cx="{SX-260}" cy="{SY+60}" r="34" fill="{YEL}"/>',
        f'<circle cx="{SX+SW+300}" cy="{SY+SH-40}" r="22" fill="{YEL}"/>',
        f'<circle cx="{SX+SW+180}" cy="{SY+20}" r="12" fill="{INK}"/>',
        f'<rect x="{tx+first_w-14}" y="{ty-fs*0.62}" width="{last_w+28}" height="{fs*0.78}" rx="10" fill="{YEL}"/>',
        f'<text x="{tx}" y="{ty}" font-family="Inter" font-weight="900" font-size="{fs}" fill="{INK}" letter-spacing="-3">{NAME}</text>',
        f'<text x="{tx+4}" y="{ty+125}" font-family="Inter" font-weight="800" font-size="62" fill="{INK}">{TAG1}</text>',
        f'<text x="{tx+4}" y="{ty+200}" font-family="Inter" font-weight="500" font-size="54" fill="#555">{TAG2}</text>',
        fig(SX + SW - 330, SY + 16, 395, mouth="smile", la=(98, -6), ra=(20, 2), head=6),
    ]
    if guides:
        parts.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="none" stroke="red" stroke-width="4" stroke-dasharray="20 12"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(parts)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=out)

banner(os.path.join(HERE, "banner-v2-2560x1440.png"))
banner(os.path.join(HERE, "banner-guides.png"), guides=True)
