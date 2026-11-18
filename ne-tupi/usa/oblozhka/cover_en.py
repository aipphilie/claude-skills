"""Английские обложки Shorts «Кофе» и «Зарплата» (США), стиль как у русских: белый фон, чёрное, жёлтые плашки."""
from PIL import Image, ImageDraw
import cover2, cover3
from cover2 import plates, guide

def swap(fn, old, new):
    """перерисовать обложку, подменив только текст плашек"""
    orig = cover2.plates
    def p(d, y, lines, sz, *a, **k):
        if lines == old: lines, sz = new[0], new[1]
        return orig(d, y, lines, sz, *a, **k)
    cover2.plates = p; cover3.plates = p
    try: return fn()
    finally: cover2.plates = orig; cover3.plates = orig

out = {
    'kofe-a-not-guilty': swap(cover3.cover_a, ['ОН НЕ', 'ВИНОВАТ'], (['NOT', 'GUILTY'], 160)),
    'kofe-b-drink-up': swap(cover3.cover_c, ['ПЕЙ', 'СПОКОЙНО'], (['DRINK', 'UP'], 160)),
    'zarplata-a-bye-paycheck': swap(cover2.cover_b, ['ПОКА,', 'ЗАРПЛАТА'], (['BYE-BYE,', 'PAYCHECK'], 135)),
    'zarplata-b-broke-again': swap(cover2.cover_c, ['ОПЯТЬ', 'ПУСТО'], (['BROKE', 'AGAIN'], 160)),
}
sh = Image.new('RGB', (4 * 370 + 10, 640), (40, 40, 40))
for i, (k, im) in enumerate(out.items()):
    im.save(f'cover-{k}.png'); sh.paste(guide(im).resize((360, 640)), (10 + i * 370, 0))
sh.save('obzor-en.png')
