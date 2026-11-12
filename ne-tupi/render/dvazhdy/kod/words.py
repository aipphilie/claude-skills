import json, re
a = json.load(open('align2.json'))
C = a['characters']; S = a['character_start_times_seconds']; E = a['character_end_times_seconds']
txt = ''.join(C)
def words():
    out = []; intag = False; cur = None
    for i, ch in enumerate(C):
        if ch == '[': intag = True; cur = None; continue
        if ch == ']': intag = False; continue
        if intag: continue
        if ch.isalnum() or (ch in "-«»" and cur):
            if cur is None: cur = [i, i]; out.append(cur)
            else: cur[1] = i
        elif ch in ' \n': cur = None
        else:
            if cur: cur[1] = i
    return [(''.join(C[s:e + 1]).strip(), S[s], E[e]) for s, e in out]
def tags():
    return [(m.group(1), S[m.start()], E[m.end() - 1]) for m in re.finditer(r'\[([^\]]*)\]', txt)]
W = words()
def wt(sub, k=0):
    hits = [w for w in W if sub.lower() in w[0].lower()]
    return hits[k][1]
STARTS = ['Это простое', 'помогло тысячам', 'заработать', 'сбросить', 'выучить', 'Хотя раньше', 'Называется', 'Пропустил один', 'Бывает',
          'Но два дня', 'Никогда.', 'Автор книги', 'для мозга', 'Но дважды', 'И привычка', 'Смотри', 'Но два подряд', 'Именно так',
          'Они не идеальные', 'Правило, которое', 'Всё. Не тупи']
_ix = [txt.index(s) for s in STARTS]
def _prev_end(i):
    j = i - 1
    while j > 0 and not C[j].isalnum(): j -= 1
    return E[j]
B = [0.0] + [(_prev_end(i) + S[i]) / 2 for i in _ix[1:]]
END = E[len(txt.rstrip()) - 1]
DUR = round(END + 2.6, 2)
if __name__ == '__main__':
    for w in W: print(f"{w[1]:6.2f} {w[2]:6.2f} {w[0]}")
    print([round(b, 2) for b in B], END, DUR)
