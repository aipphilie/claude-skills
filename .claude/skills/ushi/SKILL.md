---
name: ushi
description: Уши для Claude — живой звук для роликов и проверка того, что реально звучит. Openverse (где взять звук, CC0 без ключа), Real SFX / sound layer (библиотека живых записей, раскладка по таймлайну, микс -14 LUFS, QA), PANNs (нейросеть слушает дорожку и говорит словами, что и когда звучит). Включай, когда надо озвучить ролик звуками, найти звук, свести микс или проверить звук — для Ашота, Ярика, мистических сериалов и любого видео.
---

# Уши: Openverse + Real SFX + PANNs

Я не слышу звук. Поэтому: беру **живые записи** вместо синтеза, ставлю их **по таймлайну картинки**, а потом **слушаю ушами-нейросетью** и меряю, а не говорю «звук хороший». Финальная проверка — ухом автора.

| Инструмент | Что делает | Где |
|---|---|---|
| **Openverse** | где взять звук: поиск CC0-записей Freesound через api.openverse.org, без ключа | `scripts/sfx.py search` |
| **Real SFX** (opus-sound-layer, MIT) | куда его поставить: библиотека ~600–1100 CC0-звуков в 19 типах, выбор по картинке волны, микс по cue-листу, -14 LUFS, QA по кадрам | `scripts/sfx.py`, `scripts/mix.py`, `scripts/qa.py` |
| **PANNs** (Cnn14, AudioSet 527 классов) | уши: что звучит во всём файле, по секундам и в каждом cue | `scripts/hear.py` |

Пути ниже — от корня репозитория. `S=.claude/skills/ushi/scripts`.

## Установка (один раз за сессию, ~3–10 мин)

```bash
bash .claude/skills/ushi/scripts/setup.sh        # torch CPU + panns_inference + модели (~650 МБ) + библиотека звуков
```
Библиотека ложится в `~/.cache/ushi/kit` (в git не кладём — 160+ МБ), модели — в `~/panns_data`. Повторный запуск ничего не качает. Библиотеку запускать в фоне. Если часть Freesound отдала 403 — это лимит, перезапуск `setup.sh kit` докачает остальное (сначала удалить `~/.cache/ushi/kit/catalog.json`). Паки Kenney по старым ссылкам сейчас не качаются, поэтому типов `ui` и `zap` в библиотеке может не быть — искать их через Openverse.

**Проверено 2026-11-03 в облаке:** библиотека — 633 звука в 17 типах (hit 185, glitch 136, boom 46, tick 38, riser 37, pop 30, reverse 29, whoosh 24, swish 21, thump 18, key 17, chime 17, shimmer 15, paper 8, transition 8, click 2, tap 2). Freesound CDN после первой волны стал отвечать облачному IP `403`: поиск `sfx.py search` через Openverse работает, а скачивание найденного — нет. Тогда: взять звук из библиотеки, или автор скачивает файл со страницы Freesound (ссылку даёт search / Openverse) и кладёт в репо, дальше `sfx.py add`. Блокировку не обходить (не подделывать User-Agent и т.п.). На своём компьютере всё качается нормально.
Если `uv` ругается на сертификат: `export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt UV_SYSTEM_CERTS=1`.

## Порядок работы

1. **Cue-лист из картинки.** `audio/cues.json` строится из таймингов самого ролика (story.json / timeline.json / data-start), кадры руками не набирать. Формат: `uv run $S/mix.py --schema`. В поле `"kit"` пиши `"/root/.cache/ushi/kit"`. Звук только на настоящие действия, у каждого cue `visual`: `cut` (смена кадра) · `move` (пик скорости) · `land` (движение остановилось) · `appear`. Один «герой» на ~4 сек: `"hit+boom"` + `stop_before` + `build`, riser/reverse с пиком на нём.
2. **Выбрать каждый звук самому:**
   ```bash
   uv run $S/sfx.py browse --kit ~/.cache/ushi/kit --type whoosh --like "car fast air" --png audio/browse.png
   ```
   Смотреть `audio/browse.png` (волна + спектрограмма), id вписать в cue. Одна звуковая семья на ролик (у Ашота — машина, пластик салона, монеты; у Ярика — тело, мокрое, мягкое). Повторы разнообразить.
3. **Нет подходящего — Openverse:**
   ```bash
   uv run $S/sfx.py search "car turn signal" --type tick --n 6       # скачает, обрежет, оценит
   python3 $S/hear.py audio/candidates/tick/ov-xxxx.wav               # уши: правда ли это поворотник
   uv run $S/sfx.py add audio/candidates/tick/ov-xxxx.wav --type tick --kit ~/.cache/ushi/kit
   ```
   Кредит подтянется сам в `~/.cache/ushi/kit/CREDITS.md`. Не синтезировать удары, клики и вжухи, если есть живая запись; никаких мем-звуков.
4. **Микс:** картинку рендерить без звука, потом
   ```bash
   uv run $S/mix.py audio/cues.json                                   # audio/mix.wav, stems, mix-report.json
   ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
   uv run $S/qa.py out/final.mp4                                      # exit 1 = есть FAIL
   ```
5. **Послушать ушами:**
   ```bash
   python3 $S/hear.py out/final.mp4 --cues audio/cues.json --png audio/hear.png
   python3 $S/hear.py out/final.mp4 --timeline --win 0.5               # что звучит по полсекунды
   ```
   Для каждого cue печатается всплеск в dB и что PANNs там слышит (`Speech`, `Vehicle horn`, `Cash register`, `Whoosh, swoosh`, `Music`…). `??` — звука в этой точке не слышно (тонет под голосом/музыкой) или стоит не там. Если в точке поворотника PANNs слышит только `Speech` — звук не пробивается.
6. **Чинить** FAIL из qa.py и `??` из hear.py, меняя cue и звуки, максимум 2 круга. Пороги в скриптах не ослаблять, скрипты не переписывать.
7. **Сдать:** `final.mp4`, `CREDITS.md`, `LISTEN.md` — 5 таймкодов, которые автор проверит ухом. Писать, что показали проверки, а не «звук отличный».

## Что умеет hear.py

- `hear.py FILE` — топ-10 классов AudioSet по всему файлу.
- `--timeline [--win 0.5]` — по окнам: громкость и топ-3.
- `--at 1.2 3.5` — что слышно в эти секунды.
- `--cues audio/cues.json` — проверка каждого cue (понимает `frame`+`fps` и `t`).
- `--png` — волна + тепловая карта 12 самых сильных событий по времени (модель Cnn14_DecisionLevelMax), голубые линии — проверяемые точки. Открывать картинку и смотреть глазами.
- `--json out.json` — всё в файл.

Работает на CPU, 15 сек ролика ≈ 10–20 сек. PANNs ошибается на редких и смешанных звуках: это подсказка, а не приговор.

## Источники

- Openverse API: https://api.openverse.org/v1/ (CC0, `source=freesound`).
- Real SFX / sound layer: https://github.com/Bodila51/opus-sound-layer (MIT, `scripts/LICENSE-sound-layer`). Скрипты скопированы без изменений.
- PANNs: https://github.com/qiuqiangkong/panns_inference (Kong et al., 2020), модели с Zenodo 3987831.
