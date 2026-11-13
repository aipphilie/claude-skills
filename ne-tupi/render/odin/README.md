# «Почему он не пускает тебя близко» v1 (2026-11-14)
- odin-v1.mp4 — 1080x1920, 30 fps, 62,6 сек. Голос hU3rD0Yk7DoiYULTX1pD, eleven_v4. Звуки из ne-tupi-zvuki/gotovye, ×0.5 (76 событий).
- По присланному Ярославом рилсу «Почему он не пускает в отношения» (СДВГ-монтаж): чёрный кадр, заголовок, белая карточка-сцена 1080x720, субтитр 1–3 слова под ней. 44 сцены, склейка в среднем раз в 1,4 сек.
- НОВЫЙ ДВИЖОК СДВГ-МОНТАЖА: kod/compose_o.py. Сцена = функция fn(C, u, t), список SHOTS (время по слову озвучки, переход, звук), ACC — звуковые акценты внутри сцен. Переходы: zoom, whipL/R/U, shake, spin, glitch, cut + вспышка и RGB-сдвиг. Хелперы: slam (текст влетает ударом), stamp, plate, tape, strike/xcross, speedlines, burst, heart, box, gremlin, brain, armor, wall, cards.
- Человечек: клипы (kod/clips.py → clips.json → kadry/<клип>/NNN.png, 24 fps), монтаж берёт кадр по локальному времени сцены. Новые позы: scared, stop, dig, climb, carry, pointcam, cross, shock.
- Шрифт карточек и субтитров: Oswald Bold (kod/fonts/), обложки — Inter Black, как раньше.
- Порядок: python3 -m http.server 8791 (из kod/) → tts.py → clips.py → node 3d/frames.js clips.json kadry flat 1080 1920 8791 → compose_o.py (sheet 0.6 — лист всех сцен; числа — превью кадров; без аргументов — видео и sfx.json) → mix_o.py → ffmpeg склейка → cover_o.py.
- Обложки: oblozhka/ (A «ОН НЕ ХОЛОДНЫЙ» — рекомендую, B «СВОБОДА = БРОНЯ»). Описание: ne-tupi-idei/odin/opisanie.md.
