import json,re
a=json.load(open('align.json'))
C=a['characters']; S=a['character_start_times_seconds']; E=a['character_end_times_seconds']
txt=''.join(C)
def words():
    out=[]; intag=False; cur=None
    for i,ch in enumerate(C):
        if ch=='[': intag=True; cur=None; continue
        if ch==']': intag=False; continue
        if intag: continue
        if ch.isalnum() or ch in "-«»" and cur:
            if cur is None: cur=[i,i]; out.append(cur)
            else: cur[1]=i
        elif ch in ' \n': cur=None
        else:
            if cur: cur[1]=i  # punctuation attaches
    return [(''.join(C[s:e+1]).strip(), S[s], E[e]) for s,e in out]
def tags():
    return [(m.group(1), S[m.start()], E[m.end()-1]) for m in re.finditer(r'\[([^\]]*)\]', txt)]
W=words()
def wt(sub, k=0):
    hits=[w for w in W if sub.lower() in w[0].lower()]
    return hits[k][1]
if __name__=='__main__':
    for w in W: print(f"{w[1]:6.2f} {w[2]:6.2f} {w[0]}")
    print(tags())

# границы строк сценария: B[k] = середина паузы перед строкой k (B[0]=0), END = конец речи
def _lines():
    out, pos = [], 0
    for line in txt.split('\n'):
        m = re.match(r'(?:\[[^\]]*\]\s*)*', line); i = pos + m.end()
        out.append((S[i], E[pos + len(line) - 1])); pos += len(line) + 1
    return out
LINES = _lines()
B = [0.0] + [(LINES[k-1][1] + LINES[k][0]) / 2 for k in range(1, len(LINES))]
END = LINES[-1][1]
DUR = round(END + 3.5, 2)
