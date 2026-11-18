import io, tokenize, re, json, sys
CYR = re.compile('[А-Яа-яЁё]')
def literals(path):
    src = open(path).read(); toks = list(tokenize.generate_tokens(io.StringIO(src).readline)); out = []
    for i, t in enumerate(toks):
        if t.type != tokenize.STRING or not CYR.search(t.string): continue
        if t.string.startswith(('"""', "'''")): continue
        # предыдущие значимые токены
        prev = [x for x in toks[max(0, i - 6):i] if x.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)]
        ps = ' '.join(x.string for x in prev[-4:])
        if re.search(r'(^|\s)(c|wt|cw|w)\s\($', ps) or re.search(r'wt \( \d+ ,$', ps) or re.search(r'(c|wt) \( \w+ ,$', ps): continue
        out.append((t.start, t.end, t.string))
    return out
if __name__ == '__main__':
    allst = {}
    for v in sys.argv[1:]:
        for f in ['scenes', 'gfx', 'compose', 'tl', 'mix', 'track']:
            for s, e, lit in literals(f'{v}/kod/{f}.py'):
                allst.setdefault(lit, []).append(f'{v}/{f}')
    json.dump({k: '' for k in allst}, open('strings.json', 'w'), ensure_ascii=False, indent=0)
    print(len(allst))
