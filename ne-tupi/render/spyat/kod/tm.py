from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(zarplata=wt('Зарплата'), shest=wt('шестьдесят'), dvadcat=wt('Двадцать'), kvart=wt('квартиру'), kak=wexact('как'),
         rabotat=wt('работать'), otvet=wt('Ответ'), dumaesh=wt('Думаешь'), stop=wt('Стоп'), dengi=wt('Деньги', 1), est=wexact('есть'),
         spyat=wt('спят'), karte=wt('карте'), nichego=wt('ничего'),
         shag1=wt('Шаг'), zaplati=wt('заплати'), den=wexact('день'), shest6=wexact('шесть'), storonu=wt('сторону'), avto=wt('автопереводом'),
         do=wexact('до'), ostanetsya=wt('останется'),
         shag2=wt('Шаг', 1), razbudi=wt('разбуди'), nakop=wt('Накопительный'), podushki=wt('подушки'), oblig=wt('Облигации'),
         dolshe=wt('дольше'), iis=wt('И-И-С'), vernet=wt('вернёт'), trinad=wt('тринадцать'),
         shag3=wt('Шаг', 2), trogay=wt('трогай'), pust=wt('Пусть'),
         podvoh=wt('подвох'), karte2=wt('карте', 1), ceny=wt('Цены'), hudeyut=wt('худеют'),
         itak=wt('Итак'), otlozhish=wt('отложишь'), trista=wt('триста'), meshki=wt('Мешки', 1), pritashat=wt('притащат'), sta=wexact('ста'),
         pyatdesyat=wt('пятьдесят'), gosudarstvo2=wt('государство', 1), tridcat=wt('тридцать', 0), nes=wt('нёс'),
         teper=wt('Теперь'), spish=wt('спишь'), rabotayut=wt('работают'), vsyo=wexact('всё', -1), netupi=wexact('тупи'))
if __name__ == '__main__':
    print(len(B), DUR); print({k: round(v, 2) for k, v in T.items()})
