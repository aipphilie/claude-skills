# «Почему ты всем говоришь "да"» — рендер v1 (2026-11-08)
- da-ladno-neudobno-v1.mp4 — 1920x1080, 24 fps, 8:16, голос + звуки, без музыки.
- da-ladno-neudobno-v1-muzyka.mp4 — то же + тихая подложка (zvuk/muzyka-podlozhka.mp3, ElevenLabs Sound Effects, луп 22 с, приглушается под голосом). Генерация музыки через Music API у ключа недоступна.
- Холодный старт без сирены и полицейского фона (отзыв Ярослава по первому ролику).
- kod/ — конвейер первого ролика (ne-znayu-chego-hochu/render), изменены: tl.py (9 блоков, названия глав), scenes.py (51 сцена), gfx.py (+boxes, hourglass, meter), compose.py/mix.py/track.py (финал = блок 8, без сирены).
- Порядок: tts.py → voice.py → track.py → render_ch.sh (http.server 8777 в папке с 3d/, anim3d.py, anim.py, rig.py; нужен pip cairosvg) → mix.py → render_v.sh.
- Если Chromium падает (Target crashed), перезапустить frames2.js на недостающий диапазон: готовые кадры пропускаются.
