from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(listok=wt('листок'), shest=wt('шестьдесят'), tysyach=wt('тысяч.'), zametish=wt('заметишь'), more=wt('море'), telefon=wt('телефон'),
         podushku=wt('подушку'), spat=wt('спать'), ponedelnik=wt('понедельник'), pyatnice=wt('пятнице'), vsyo1=wexact('всё'), kopit=wt('копить'),
         stop=wt('Стоп'), desyat=wt('десять'), mozg=wt('Мозг'), tyanet=wt('тянет'), nas=wt('Нас'), priyom=wt('приём'), kalendar=wt('Календарь'),
         trista=wt('Триста'), kazhdom=wt('каждом'), lyuboy=wt('любой'), otkladyvaesh=wt('откладываешь'), rubley=wt('рублей'),
         deneg=wt('Денег'), zakras1=wt('Закрась'), edinichku=wt('единичку'), byvaet=wt('Бывает'), zarplata=wt('зарплата?'), trista2=wt('триста!'),
         podvoh=wt('подвох'), malenkie=wt('маленькие'), dekabre=wt('декабре'), tryohsotki=wt('трёхсотки'), brosish=wt('бросишь'),
         pravilo=wt('правило'), samyy=wt('самый'), slozhi=wt('сложи'), chisla=wt('числа'), summa=wt('Шестьдесят', 2), pyat=wt('пять.'),
         cena=wt('цена'), sto=wexact('сто'), den=wt('день.'), odna=wt('Одна'), kofe=wt('кофе'), raspechatay=wt('Распечатай'),
         holodilnik=wt('холодильник'), zakras_perv=wt('Закрась', 2), pervyy=wt('первый'), netupi=wexact('тупи'))
if __name__ == '__main__': print({k: round(v, 2) for k, v in T.items()})
