"""Лист вариантов: квадрат в круге (как в профиле) крупно и мелко."""
import os, glob
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(D, "avatarki", "*.png")))
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 30)
def circ(im, d):
    im = im.resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, d * 4, d * 4), fill=255)
    out = Image.new("RGBA", (d, d)); out.paste(im, (0, 0), m.resize((d, d), Image.LANCZOS)); return out
cols, cw, ch = 4, 420, 520
rows = (len(files) + cols - 1) // cols
sh = Image.new("RGB", (cols * cw, rows * ch), "#e9e9ec"); dr = ImageDraw.Draw(sh)
for i, f in enumerate(files):
    x, y = (i % cols) * cw, (i // cols) * ch
    im = Image.open(f).convert("RGB")
    sh.paste(circ(im, 340), (x + 40, y + 30), circ(im, 340))
    # мелко: светлая и тёмная тема
    dr.rectangle((x + 40, y + 390, x + 380, y + 470), fill="#fff")
    dr.rectangle((x + 210, y + 390, x + 380, y + 470), fill="#0f0f0f")
    for ox in (95, 265):
        c = circ(im, 56); sh.paste(c, (x + ox, y + 402), c)
    dr.text((x + 40, y + 478), os.path.basename(f)[:-4], font=F, fill="#222")
sh.save(os.path.join(D, "avatarki-obzor.png"))
