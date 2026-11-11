# Threads

Карусели «Не тупи» для Threads. Что за площадка и правила карусели: [THREADS.md](THREADS.md).

| Карусель | Основа | Файлы |
|---|---|---|
| Самозапрет на кредиты (9 слайдов, 4:5) | рилс `idei/samozapret/` | [samozapret/](samozapret/): `slides/`, текст поста `post.md` |
| Почему ты не уходишь с работы (9 слайдов, 4:5) | рилс `idei/rabota/` | [rabota/](rabota/): `slides/`, текст поста `post.md` |

## Как пересобрать слайды
Из папки `ne-tupi/`:
```
python3 -m http.server 8777 &
node 3d/frames.js threads/samozapret/poses.json /tmp/kadry flat 1080 1920
python3 threads/samozapret/slides.py /tmp/kadry/p threads/samozapret/slides
```
Для «Работы» то же с `threads/rabota/poses.json` и `threads/rabota/slides.py` (он берёт общие функции из `samozapret/slides.py`; добавлены позы 10 сидит на стуле, 11 плетётся, 12 стоит и лежит при повороте на 90°).

Позы человечка в `poses.json` (по номеру кадра: 0 шок, 1 руки в боки, 2 рука у лица, 3 пожимает плечами, 4 указывает вверх, 5 указывает вправо, 6 влево, 7 объясняет, 8 машет, 9 удивлённо пожимает).
