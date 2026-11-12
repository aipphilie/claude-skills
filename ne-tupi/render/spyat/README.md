# «Они спят» v1 (2026-11-12)
- spyat-v1.mp4 — 1080x1920, 24 fps, 63 сек, голос hU3rD0Yk7DoiYULTX1pD (eleven_v3), сценарий ne-tupi-idei/spyat/scenariy-v1.md, описание opisanie.md.
- Код на базе «Первого миллиона»: kod/tts.py (озвучка по строкам text.txt), words.py, tm.py (тайминги T), track_s.py (позы), compose_s.py (диван «КАРТА», спящие мешки, мешки на ножках в касках, три шага, счётчики ответа, плашка «Не является индивидуальной инвестиционной рекомендацией»), mix_s.py (звуки из ne-tupi-zvuki/gotovye ×0.5).
- В text.txt «И-И-С» через дефисы, чтобы голос читал по буквам; в субтитрах показывается «ИИС».
- Пауза 0,5 сек перед «Всё. Не тупи» вставлена в zvuk/voice.wav (сырой voice-raw.mp3), align.json сдвинут.
- Порядок: tts.py → track_s.py → node 3d/frames.js track.json kadry flat 1080 1920 → compose_s.py → mix_s.py → склейка. PYTHONPATH=…/claude-skills/ne-tupi (нужна версия anim3d из PR #37).
- Обложки: oblozhka/ (A «ОНИ СПЯТ», B «60К → ?»), код cover_s.py.
