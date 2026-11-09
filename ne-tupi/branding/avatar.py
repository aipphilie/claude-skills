"""Аватарки «Не тупи» из рига человечка (rig3.py). Запуск: python3 avatar.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg, rig3

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avatarki")
S = 1080
YEL = "#FFD60A"

def avatar(name, box, bg="#fff", extra="", **pose):
    x, y, size = box
    body = rig3.figure(**pose)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="{x} {y} {size} {size}">'
           f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{bg}"/>{body}{extra}</svg>')
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name + ".png"))

def text_band(x, y, size, txt, fill, color):
    h = size * 0.2
    by = y + size * 0.66
    return (f'<rect x="{x}" y="{by}" width="{size}" height="{h}" fill="{fill}"/>'
            f'<text x="{x+size/2}" y="{by+h*0.73}" font-family="Inter" font-weight="900" font-size="{h*0.68}" '
            f'text-anchor="middle" fill="{color}" letter-spacing="2">{txt}</text>')

# 1. Крупно, ухмылка, белый
avatar("1-krupno-belyj", (220, 470, 640), mouth="smile", head=-6)
# 2. Крупно, жёлтый фон, «вау»
avatar("2-krupno-zheltyj", (220, 470, 640), bg=YEL, mouth="wow", head=5)
# 3. Фейспалм «ну ты чего», жёлтый
avatar("3-facepalm-zheltyj", (200, 450, 680), bg=YEL, mouth="sad", ra=(118, 100), head=8, head_dy=8, lean=2)
# 4. Руки в боки, в полный рост, белый
avatar("4-ruki-v-boki", (60, 520, 960), mouth="smile", la=(55, -100), ra=(55, -100), head=-3)
# 5. Указывает вверх «слушай сюда», жёлтый
avatar("5-ukazyvaet-vverh", (150, 390, 800), bg=YEL, mouth="O", ra=(155, 10), head=-5)
# 6. С надписью НЕ ТУПИ
b = (220, 450, 660)
avatar("6-s-nadpisyu", b, mouth="smile", head=-6, extra=text_band(*b, "НЕ ТУПИ", YEL, "#111"))
# 7. Белый человечек? нет — чёрный на жёлтом, плечи и надпись чёрным баннером
b = (220, 450, 660)
avatar("7-nadpis-chernaya", b, bg=YEL, mouth="smile", head=-6, extra=text_band(*b, "НЕ ТУПИ", "#111", YEL))
# 8. Крупно, ухмылка, жёлтый (рекомендую)
avatar("8-krupno-zheltyj-uhmylka", (220, 470, 640), bg=YEL, mouth="smile", head=-6)
# ФИНАЛ: вариант 5 на белом фоне
avatar("avatarka-final", (150, 390, 800), mouth="O", ra=(155, 10), head=-5)
