from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(pravilo=wt('правило'), tysyacham=wt('тысячам'), million=wt('миллион'), dvadcat=wt('двадцать'), angl=wt('английский'),
         brosali=wt('бросали'), desyat=wt('десять'), nikogda_t=wt('Никогда'), dvazhdy_t=wt('дважды»'), propustil=wt('Пропустил'),
         normalno=wt('Нормально'), byvaet=wt('Бывает'), dva=wexact('два'), nelzya=wt('нельзя'), nikogda=wt('Никогда.'), pochemu=wt('Почему'),
         atomnye=wt('Атомные'), klir=wt('Клир'), obyasnyaet=wt('объясняет'), sluchaynost=wt('случайность'), dvazhdy=wexact('дважды', 1),
         norma=wexact('норма'), razrushena=wt('разрушена'), mesyac=wt('месяц'), shest=wt('шесть'), dva2=wexact('два', 1), ni=wexact('ни'),
         dobivayutsya=wt('добиваются'), poluchilos=wt('получилось'), idealnye=wt('идеальные'), vozvrashchayutsya=wt('возвращаются'),
         sleduyushchiy=wt('следующий'), smog=wt('смог'), netupi=wexact('тупи'))
if __name__ == '__main__': print({k: round(v, 2) for k, v in T.items()})
