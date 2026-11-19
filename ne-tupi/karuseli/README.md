# Карусели

Общие правила: [PRAVILA-KARUSELEY.md](PRAVILA-KARUSELEY.md). Карусели для Threads лежат в `../threads/`.

| Карусель | Слайды | Файлы |
|---|---|---|
| 6 тем, чтобы не тупить (10 слайдов, 4:5) | `6-tem/slides/`, обзор `obzor.png` | план Ярослава `plan.md`, подпись `post.md`, код `slides.py`, позы `poses.json` |

## Как пересобрать
Из папки `ne-tupi/`:
```
node 3d/frames.js karuseli/6-tem/poses.json /tmp/kadry flat 1080 1920 file
python3 karuseli/6-tem/slides.py /tmp/kadry/p karuseli/6-tem/slides
```
