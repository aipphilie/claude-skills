from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:') == word.lower()]
    return hits[k][1]
T = dict(odobren=wt('одобрен'), pol=wt('Полмиллиона'), nebral=wt('брал'), dumaesh=wt('Думаешь'), nikomu=wt('никому'), stop=wt('Стоп'),
         tvoi=wt('Твои'), slil=wt('слил'), dostavka=wt('Доставка'), apteka=wt('аптека'), magazin=wt('магазин'), delat=wt('делать'),
         nas=wt('Нас'), odna=wt('Одна'), besplatno=wt('Бесплатно'), dve=wt('Две'), otkr=wt('Открываешь'), poiske=wt('поиске'),
         samozapret=wt('самозапрет'), stavish=wt('Ставишь'), bank=wexact('банк'), otkazat=wt('отказать'), podvoh=wt('подвох'),
         snyat=wexact('снять', 0), moshenniki=wt('мошенники'), zvonyat=wt('звонят'), proverki=wt('проверки'), zashity=wt('защиты'),
         zapomni=wt('Запомни'), moshennik=wexact('мошенник'), vsegda=wt('Всегда'), nuzhen=wt('нужен'), snyal=wt('Снял'), vzyal=wt('взял'),
         postavil=wt('поставил'), postav=wt('Поставь'), pereshli=wt('перешли'), pust=wt('Пусть'), otkazano=wt('отказано'),
         soob=wt('сообщение'), vsyo=wexact('всё', -1), netupi=wexact('тупи'))
if __name__ == '__main__':
    print(len(B), DUR); print({k: round(v, 2) for k, v in T.items()}); print([round(b, 2) for b in B])
