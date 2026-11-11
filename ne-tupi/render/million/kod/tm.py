from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:…—') == word.lower()]
    return hits[k][1]
T = dict(tyazh=wt('тяжёлый'), dalshe=wt('дальше'), vtoroy=wt('второй'), tretiy=wt('третий'), pyatyy=wt('пятый'), legche=wt('легче'),
         pochemu=wt('Почему'), dumaesh=wt('Думаешь'), vezet=wt('везёт'), bogatym=wt('богатым'), stop=wt('Стоп'),
         gruz=wt('Груз'), silnee=wt('Сильнее'), nas=wt('Нас'), tri=wexact('три'), myshcy=wt('мышцы'),
         pervaya=wt('Первая'), zarab=wt('зарабатывать'), dorozhe=wt('дороже'), vtoraya=wt('Вторая'), uderzh=wt('удерживать'),
         utekat=wt('утекать'), erundu=wt('ерунду'), tretya=wt('Третья'), boyatsya=wt('бояться'), summa=wt('Сумма'), tryaslis=wt('тряслись'),
         cifroy=wt('цифрой'), podvoh=wt('подвох'), svalilsya=wt('свалился'), neba=wt('неба'), myshc=wt('мышц,'), uletaet=wt('улетает'),
         kazhdyy=wt('каждый'), odin=wt('один'), vtoroy2=wt('Второй', 1), vdvoem=wt('вдвоём'), vlozhen=wt('вложен'), prinosit=wt('приносит'),
         desyatyy=wt('десятый'), tashat=wt('тащат'), devyat=wt('девять'), delat=wt('делать'), gonis=wt('гонись'), dohod=wt('доход'),
         otkl=wt('откладывать'), vlozh=wt('вложения'), gora=wt('Гора'), drugoy=wt('другой'), vsyo=wexact('всё', -1), netupi=wexact('тупи'))
if __name__ == '__main__':
    print(len(B), DUR); print({k: round(v, 2) for k, v in T.items()})
