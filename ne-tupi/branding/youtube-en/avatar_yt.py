"""Аватарка для YouTube: человечек №5 (указывает вверх) вписан в круг. Запуск: python3 avatar_yt.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import cairosvg, rig3
S = 800
x, y, size = 62, 380, 960   # кадр в координатах рига: голова, рука и корпус по центру круга
body = rig3.figure(mouth="O", ra=(155, 10), head=-5)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="{x} {y} {size} {size}">'
       f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="#fff"/>{body}</svg>')
cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(HERE, "avatarka-yt-800.png"))
