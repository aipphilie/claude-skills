# «Первый миллион тяжелее всех» v1 (2026-11-11)
- million-v1.mp4 — 1080x1920, 24 fps, 66 сек, голос hU3rD0Yk7DoiYULTX1pD (eleven_v3), сценарий ne-tupi-idei/million/scenariy-v1.md.
- Код на базе «Самозапрета»: kod/tts.py (озвучка, text.txt по строкам-сценам), words.py, tm.py (тайминги слов T), track_m.py (позы, включая новые tashit-v-goru / tashit-legko и шаг вправо), compose_m.py (гора, мешки, мешки на ножках, полоски «прокачки», копилка, плашки), mix_m.py (звуки из ne-tupi-zvuki/gotovye ×0.5).
- Пауза 0,5 сек перед «Всё. Не тупи» вставлена в zvuk/voice.wav (сырой файл voice-raw.mp3), align.json сдвинут.
- Мешок на спине рисуется по точке kadry/main/anchors.json (пишет 3d/frames.js).
- Порядок: tts.py → track_m.py → node 3d/frames.js track.json kadry flat 1080 1920 → compose_m.py → mix_m.py → склейка. Запуск из папки kod с PYTHONPATH=…/claude-skills/ne-tupi.
- Обложки: oblozhka/ (A «САМЫЙ ТЯЖЁЛЫЙ», B «ДЕСЯТЫЙ ЛЕГЧЕ»), код cover_m.py.
