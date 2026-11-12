from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(svarshik=wt('сварщик'), programmist=wt('программист'), diplom=wt('дипломом'), chetyre=wt('четыре'), uchilsya=wt('учился'),
         dva=wexact('два'), kolledzha=wt('колледжа'), menshe=wt('меньше'), prostite=wt('Простите'), dumaesh=wt('Думаешь'), nuzhny=wt('нужны?'),
         stop=wt('Стоп'), nuzhny2=wt('Нужны.'), mnogo=wt('много'), nas=wt('Нас'), zarplata=wt('зарплата'), nagrada=wt('награда'), cena=wt('цена'),
         tolpa=wt('толпа'), vybiray=wt('Выбирай'), kopeyki=wt('копейки'), ochered=wt('очередь'), rabotodateley=wt('работодателей'),
         perebivayut=wt('перебивают'), dengami=wt('деньгами'), podvoh=wt('подвох'), poydut=wt('Пойдут'), razvernetsya=wt('развернётся'),
         platyat=wt('платят?'), tyazhelo=wt('тяжело'), trudno=wt('трудно'), zamenit=wt('заменить'), delat=wt('делать'), prestizh=wt('престиж'),
         ochered2=wt('очередь:'), vakansiy=wt('вакансий'), rezume=wt('резюме'), soedini=wt('соедини'), navyka=wt('навыка'), malo=wt('мало'),
         vstan=wt('Встань'), k_tebe=wt('тебе'), netupi=wexact('тупи'))
if __name__ == '__main__': print({k: round(v, 2) for k, v in T.items()})
