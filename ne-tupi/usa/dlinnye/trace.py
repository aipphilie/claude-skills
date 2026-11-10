import sys, os, json, importlib
v = sys.argv[1]; sys.path.insert(0, f'{v}/kod'); sys.path.insert(0, v)
import tl
USED = set(); _wt = tl.wt
def wt(ch, sub, k=0, end=False):
    USED.add(sub); return _wt(ch, sub, k, end)
tl.wt = wt
import scenes
for m in ('mix', 'track', 'compose'):
    src = open(f'{v}/kod/{m}.py').read()
    # только строки вызовов wt(...) — выполнять модули целиком не нужно
    import re
    for mm in re.finditer(r"wt\(\s*\d+\s*,\s*'([^']+)'", src): USED.add(mm.group(1))
json.dump(sorted(USED), open(f'{v}/anchors.json', 'w'), ensure_ascii=False)
print(len(USED))
