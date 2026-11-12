from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(desyatyy=wt('десятый'), vosem=wt('восемь'), pochemu=wt('почему'), otkl=wt('Откладываем'), dvadcat=wt('двадцать'),
         dvenadcat=wt('двенадцать'), godovyh=wt('годовых'), bolsh=wt('Большинство'), pryamoy=wt('прямой'), znachit=wt('значит'),
         desyat=wexact('десять'), tridcat=wt('тридцать'), stop=wt('Стоп'), schitaem=wt('Считаем'), chestno=wt('честно'),
         pervyy2=wt('Первый', 2), desyat2=wexact('десять', 1), mesyacev2=wt('месяцев', 1), svoih=wt('своих'), vosemsot=wt('восемьсот'),
         dalshe=wt('дальше'), slozhnyy=wt('сложный'), kapayut=wt('капают'), tvoi=wt('твои'), proshlye=wt('прошлые'), kom=wexact('ком'),
         rastet=wt('растёт'), vtoroy=wt('Второй'), odinnadcat=wt('одиннадцать'), chetvertyy=wt('Четвёртый'), vosem_let=wt('восемь', 2),
         pyatyy=wt('Пятый'), nebolshim=wt('небольшим'), desyatyy2=wt('десятый', 1), vosem3=wt('восемь', 3), itogo=wt('Итого'),
         trinadcat=wt('тринадцать'), tolko=wt('только', 1), chetyre=wexact('четыре', 1), tvoi2=wt('твои.'), ostalnye=wt('Остальные'), shest=wt('шесть'),
         momentu=wt('моменту'), sto=wexact('сто'), mesyac3=wt('месяц.'), chetyre3=wexact('четыре', 2), raza=wt('раза'), dokl=wt('докладываешь'),
         podvoh=wt('подвох'), tyazh=wt('тяжёлый'), pervyy5=wt('первый', 3), sdayutsya=wt('сдаются'), skolko=wt('Сколько'), napishi=wt('Напиши'),
         kommentah=wt('комментах'), poschitayu=wt('посчитаю'), netupi=wexact('тупи'))
if __name__ == '__main__':
    print(len(B), [round(b, 2) for b in B], END, DUR); print({k: round(v, 2) for k, v in T.items()})
