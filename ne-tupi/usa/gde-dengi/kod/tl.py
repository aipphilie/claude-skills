"""Общая шкала времени: главы склеены с паузами GAP, слова и теги с глобальными временами."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__)); ZV = os.path.join(HERE, '..', 'zvuk')
NCH = 9; GAP = 1.6; TAIL = 4.0; FPS = 24
TITLES = ['', "It's not prices", 'You get used to it', 'The neighbors', "Paying doesn't hurt", '"I deserve it"', 'Where the money went', 'The half rule', 'Outro']
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


# ---------- EN-версия: якоря ищутся в русском тексте (zvuk_ru) и переносятся на английскую озвучку ----------
import bisect as _bs
_ZR = os.path.join(HERE, '..', 'zvuk_ru')
_RU = [json.load(open(f'{_ZR}/ch{i:02d}.json')) for i in range(NCH)]
def _plain(a):
    C = a['characters']; out = []; idx = []; intag = False
    for k, ch in enumerate(C):
        if ch == '[': intag = True; continue
        if ch == ']': intag = False; continue
        if intag: continue
        out.append(ch); idx.append(k)
    return ''.join(out), idx
def _sents(p):
    res = []; st = 0
    for m in re.finditer(r'[.!?…]+["»”]?(?=\s|$)', p):
        e = m.end()
        if re.search(r'\w', p[st:e]): res.append((st, e))
        st = e
    if re.search(r'\w', p[st:]): res.append((st, len(p)))
    return res
_RP = [_plain(a) for a in _RU]; _EP = [_plain(a) for a in CH]
_RS = [_sents(p[0]) for p in _RP]; _ES = [_sents(p[0]) for p in _EP]
def _map(ch, pos):
    rs, es = _RS[ch], _ES[ch]
    si = max(0, _bs.bisect_right([s for s, e in rs], pos) - 1)
    s0, e0 = rs[si]; f = (pos - s0) / max(1, e0 - s0)
    if len(rs) == len(es): ti = si
    else: ti = min(len(es) - 1, int(round(si * (len(es) - 1) / max(1, len(rs) - 1))))
    s1, e1 = es[ti]; p = int(s1 + f * (e1 - s1))
    txt = _EP[ch][0]
    while p > s1 and txt[p - 1].isalnum(): p -= 1        # к началу слова
    while p < len(txt) - 1 and not txt[p].isalnum(): p += 1
    return p
def wt(ch, sub, k=0, end=False):
    """время k-го слова главы ch, содержащего sub (русский якорь) -> время в английской озвучке"""
    p, idx = _RP[ch]
    hits = [m for m in re.finditer(r'\S+', p) if re.search(r'\w', m.group()) and sub.lower() in m.group().lower()]
    if len(hits) <= k: raise KeyError(f'гл.{ch}: нет «{sub}» #{k}')
    m = hits[k]; ep = _map(ch, m.start()); a = CH[ch]; eidx = _EP[ch][1]
    if end:
        txt = _EP[ch][0]; q = ep
        while q < len(txt) - 1 and txt[q + 1].isalnum(): q += 1
        return O[ch] + a['character_end_times_seconds'][eidx[q]]
    return O[ch] + a['character_start_times_seconds'][eidx[ep]]

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for w in WC[int(sys.argv[1])]: print(f'{w[1]:7.2f} {w[0]}')
    print('END', END, 'DUR', DUR, 'O', [round(o, 1) for o in O])
