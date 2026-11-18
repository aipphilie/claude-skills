import sys, json, re
sys.path.insert(0, '.'); from extract import literals
v = sys.argv[1]; sys.path.insert(0, v); from tr_en import TR
A = set(json.load(open(f'{v}/anchors.json'))); miss = set()
for f in ['scenes', 'gfx', 'compose', 'tl', 'mix', 'track']:
    p = f'{v}/kod/{f}.py'; src = open(p).read(); lines = src.split('\n')
    lits = literals(p)
    for (sr, sc), (er, ec), lit in sorted(lits, reverse=True):
        val = eval(lit)
        if val in A and not (f == 'tl' and 'TITLES' in lines[sr - 1]): continue
        if val not in TR: miss.add(val); continue
        new = repr(TR[val])
        if sr == er: lines[sr - 1] = lines[sr - 1][:sc] + new + lines[sr - 1][ec:]
    src = '\n'.join(lines).replace('₽', '$')
    open(p, 'w').write(src)
print('missing:', miss)
