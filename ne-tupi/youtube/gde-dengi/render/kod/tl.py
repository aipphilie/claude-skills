"""Общая шкала времени: главы склеены с паузами GAP, слова и теги с глобальными временами."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__)); ZV = os.path.join(HERE, '..', 'zvuk')
NCH = 9; GAP = 1.6; TAIL = 4.0; FPS = 24
TITLES = ['', 'Это не цены', 'Ты привыкаешь', 'Соседи', 'Платить не больно', '«Я заслужил»', 'Где деньги', 'Правило половины', 'Финал']
CH = []; O = []; t = 0.0
for i in range(NCH):
    a = json.load(open(f'{ZV}/ch{i:02d}.json'))
    CH.append(a); O.append(t)
    t += a['character_end_times_seconds'][-1] + 0.15
    if i < NCH - 1: t += GAP
END = t; DUR = round(END + TAIL, 2); N = int(DUR * FPS)
# старт главы (начало первой фразы после паузы); пауза-заставка перед ней
CH_START = O[:]; GAPS = [(O[i] - GAP, O[i]) for i in range(1, NCH)]

def _words(i):
    a = CH[i]; C, S, E = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
    out = []; intag = False; cur = None
    for k, ch in enumerate(C):
        if ch == '[': intag = True; cur = None; continue
        if ch == ']': intag = False; continue
        if intag: continue
        if ch.isalnum() or (ch in '-«»' and cur):
            if cur is None: cur = [k, k]; out.append(cur)
            else: cur[1] = k
        elif ch in ' \n': cur = None
        else:
            if cur: cur[1] = k
            elif ch in '«': cur = [k, k]; out.append(cur)
    return [(''.join(C[s:e + 1]).strip(), O[i] + S[s], O[i] + E[e], i) for s, e in out]
W = [w for i in range(NCH) for w in _words(i)]
WC = [[w for w in W if w[3] == i] for i in range(NCH)]

def wt(ch, sub, k=0, end=False):
    """время k-го слова главы ch, содержащего sub (без регистра)"""
    hits = [w for w in WC[ch] if sub.lower() in w[0].lower()]
    if len(hits) <= k: raise KeyError(f'гл.{ch}: нет «{sub}» #{k}')
    return hits[k][2] if end else hits[k][1]

def spans():
    """(start, end, буква) для рта + теги"""
    out = []; tg = []
    for i, a in enumerate(CH):
        C, S, E = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
        intag = False; txt = ''.join(C)
        for k, ch in enumerate(C):
            if ch == '[': intag = True; continue
            if ch == ']': intag = False; continue
            if intag or not ch.isalpha(): continue
            out.append((O[i] + S[k], O[i] + E[k], ch.lower()))
        for m in re.finditer(r'\[([^\]]*)\]', txt):
            tg.append((m.group(1), O[i] + S[m.start()], O[i] + E[m.end() - 1]))
    return out, tg

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for w in WC[int(sys.argv[1])]: print(f'{w[1]:7.2f} {w[0]}')
    print('END', END, 'DUR', DUR, 'O', [round(o, 1) for o in O])
