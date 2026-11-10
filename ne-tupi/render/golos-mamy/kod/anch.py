"""Якоря по словам озвучки (общие для track, compose, mix)."""
from words import W, wt, B, END, DUR
def wexact(word, k=0):
    hits = [w for w in W if w[0].lower().strip('«».,!?:') == word.lower()]
    return hits[k][1]
T = dict(eto=wt('Это'), golos1=wexact('голос', 0), otkr=wt('открываешь'), bank=wt('банк'), stop=wt('Стоп'),
         golos2=wexact('голос', 1), zapisala=wt('записала'), nemama=wexact('мама', 0), sluh=wt('слух'), otlich=wt('отличишь'),
         no=wexact('но', 0), slovo1=wexact('слово', 0), mozhet=wt('может'),
         smotri=wt('Смотри'), vzlomal=wt('взломал'), tam=wexact('там'), starye=wt('старые'), neiro=wt('Нейросети'),
         obrazca=wt('образца'), skazat=wt('сказать'), ugodno=wt('угодно'),
         glavnoe=wt('главное'), rodnoy=wt('Родной'), plus=wt('плюс'), srochno=wt('срочно'), perest=wt('перестаёшь'),
         nedum=wt('думаешь', 0), spas=wt('спасаешь'),
         dumaesh=wt('думаешь', 1), uslyshal=wt('услышал'), poddelku=wt('подделку'), zapomni=wt('Запомни'),
         delat=wt('делать'), perezvoni=wt('Перезвони'), pridum=wt('придумайте'), kodovoe=wt('кодовое'), egonet=wexact('его', 1),
         perepiske=wt('переписке'), ukrast=wt('украсть'), netslova=wexact('нет', 1), perevoda=wt('перевода'),
         teper=wt('теперь'), golos3=wexact('голос', 3), minutu=wt('минуту'), sdelala=wt('сделала'), neiroset=wt('нейросеть'),
         zametil=wt('Заметил'), vot=wt('Вот'), pereshli=wt('Перешли'), vsyo=wexact('всё'), netupi=wexact('тупи'))
if __name__ == '__main__':
    for k, v in T.items(): print(k, v)
    print(B, END, DUR)
