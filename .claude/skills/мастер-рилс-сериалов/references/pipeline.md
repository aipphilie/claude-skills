# Технический конвейер

## Что нужно в окружении
Node + Playwright (Chromium), ffmpeg, Python 3 + numpy (+ scipy для скорости).
Шрифты: `scripts/fonts/` (Montserrat Black для субтитров, Caveat для рукописного), JetBrains Mono для HUD
(или любой моноширинный).

## Рабочая папка серии
```
work/
  fonts/            ← из scripts/fonts
  lib.js            ← scripts/lib.js (утилиты, слои, оверлеи, общие сцены)
  character.js      ← scripts/character.js (персонаж)
  render.js         ← scripts/render.js
  episode.html      ← assets/example_episode/episode.html (подключает character, timeline, lib, episode)
  episode.js        ← шоты серии (пример: assets/example_episode/episode.js)
  vo/01.mp3 …       ← куски голоса от автора
  voice_config.json ← фразы по кускам (пример в assets)
  sound.json        ← фоны и эффекты (пример в assets)
```

## Команды
```bash
python3 timeline.py voice_config.json .        # → voice.wav, timeline.json, timeline.js
PAGE=episode.html node render.js stills 2,8,12.6,18     # кадры для проверки → still_<t>.png
ffmpeg -i still_2.png -i still_8.png ... -filter_complex "xstack=inputs=N:layout=...,scale=1800:-1" grid.jpg
PAGE=episode.html node render.js video ep_noaudio.mp4 <TOTAL>   # фоном: ~15 мин на 2 мин видео
python3 mix_audio.py sound.json .              # → mix.wav (−14 LUFS)
ffmpeg -i ep_noaudio.mp4 -i mix.wav -c:v libx264 -preset fast -crf 21 -pix_fmt yuv420p \
       -c:a aac -b:a 192k -shortest -movflags +faststart episode.mp4
```

## Устройство страницы
- `renderFrame(t)` рисует кадр в момент `t`, детерминированно (свой `rng(seed)`, никакого `Math.random`).
- `SHOTS = [{s, e, cap, f(g,t), hud(t)}]`: каждый шот привязан к фразам через `ps('04.3')`
  (начало фразы), `pe(...)` (конец) и `wt('03.8', k)` (время k-го слова). Перезаписал голос →
  перезапустил `timeline.py` → всё сдвинулось само.
- `cap` = высота субтитров для шота (портрет ~1600–1640, радио ~1520, пейзаж ~1290), чтобы не закрывать лицо.
- Субтитры собираются из `PH` автоматически: группы по ≤3 слова/≤17 букв, тире приклеивается к
  предыдущему слову; словари RED/YEL/BLU задают цвета.
- Стикер меняет текст по таймлайну (`STK`), при смене заново падает.
- Списки событий (гудки, удары) держи в одном месте и переиспользуй и для картинки, и для звука.

## Параллельный рендер (4 ядра → ~4× быстрее)
`render.js video out.mp4 DUR F0 F1` рендерит только кадры F0..F1. Запусти 4 процесса фоном на четверти кадров,
склей и наложи звук:
```bash
N=$((DUR*30)); for k in 0 1 2 3; do nohup node render.js video parts/p$k.mp4 $DUR $((k*N/4)) $(((k+1)*N/4)) > parts/log$k.txt 2>&1 & done
printf "file 'p0.mp4'\nfile 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > parts/list.txt
ffmpeg -f concat -safe 0 -i parts/list.txt -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart ep.mp4
```
Серия 2 мин (3564 кадра, детализированный стиль) так рендерится примерно за 8 мин. Перед склейкой проверь число кадров в кусках (`ffprobe -count_frames`).

## Огибающая голоса для анимации
```python
# env.js: громкость голоса 30 раз в секунду, 0..1 → const ENV=[...]
a=np.frombuffer(ffmpeg('-i voice.wav -ac 1 -ar 24000 -f s16le -'),np.int16)/32768
env=[sqrt(mean(a[i*800:(i+1)*800]**2)) for i in range(len(a)//800)]; env=[min(1,e/max(env)*1.6) for e in env]
```
В странице `envAt(t)=ENV[floor(t*30)]` отвечает за рот говорящего, осциллограмму динамика и дрожь от голоса.

## Проверка безопасной зоны
Добавь в страницу режим наложения рамки и включай его только для кадров-проверок:
```js
function safeOverlay(){ctx.save();ctx.fillStyle='rgba(255,60,60,.28)';
  ctx.fillRect(0,0,W,250);ctx.fillRect(0,1600,W,320);ctx.fillRect(922,250,W-922,1350);
  ctx.fillRect(0,250,56,1350);ctx.strokeStyle='#3ddc84';ctx.setLineDash([12,8]);ctx.lineWidth=3;ctx.strokeRect(56,250,866,1350);ctx.restore()}
// в конце renderFrame: if(window.SAFE) safeOverlay();   → в render.js: page.evaluate(()=>window.SAFE=true)
```
Пример серии в `assets/` сделан ДО этого правила: его стикер/термометр/субтитры частично
в красных полях. Для новых серий используй координаты из SKILL.md.

## Грабли, на которые уже наступили
- **Шторка**: клип нового кадра `rect(cx,0,W*4,H)`, а не `W`, иначе новая сцена видна полосой.
- Отрицательный остаток в JS: `((x%1)+1)%1`, иначе `arc` с отрицательным радиусом роняет рендер.
- `pgrep -f "render.js"` в цикле ожидания находит **сам себя** (строка команды содержит шаблон),
  поэтому цикл не заканчивается. Проверяй по выходному файлу или по `node`-процессу точнее; `pkill -f`
  с таким шаблоном убьёт собственную оболочку.
- Кадры, где камера наезжает на объект у края, «зажимаются» `cam()` (края слоя не показываются):
  проверь, что объект реально в кадре, а не уехал под субтитры.
- Метки, привязанные к объекту при движущейся камере, считай через `g.getTransform().transformPoint()`.
- Логика состояний объектов (шнур, шкала, тумблер) зависит от сцены, проверяй её на кадрах.
- Длинные рендеры запускай в фоне и сообщай автору, сколько ждать (~3700 кадров ≈ 17 мин).
- Не перерендеривай готовое видео без запроса: автор может уже публиковать.
- **Утечка состояния канваса**: `textAlign='center'`, оставленный одной сценой, сдвигает текст в другой (имена-плашки
  и ники в чате уезжают за край). В начале `renderFrame` сбрасывай `textAlign`, `textBaseline`, `globalAlpha`,
  `globalCompositeOperation`, `filter`, камеру.
- Длинный субтитр ужимай по ширине (`measureText` → scale до 900 px), а не обрезай. Но лучше делить вручную (`SUBTXT`: «А ЖЕНЩИНА|В ФОРМЕ|МЕТРОПОЛИТЕНА…»).
- Цифры в субтитрах пиши цифрами («ноль сорок семь» → «00:47», «восемьсот двадцать пять вольт» → «825 ВОЛЬТ»).
- Склейки ставь за 0,15 с до начала фразы; тайминги всех событий (удары трости, нажатие, штамп) считай от `ps()`.
  Тогда звук (`times.json`) и картинка берут одни и те же числа.
- Локальное время сцены, написанной под тест (`lt=t-6`): при повторном использовании передавай `u+6`, а не переписывай сцену.

## Персонаж и аватарки
Варианты персонажа и аватарок рендерятся той же связкой: страница с `renderFrame()`, рисующая
на offscreen-канвасы, затем `toDataURL` → PNG. Всегда показывай аватарку и в реальном размере
(110 px и 48 px): так её видят в профиле и комментариях.
