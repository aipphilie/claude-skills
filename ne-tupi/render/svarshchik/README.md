# «Почему сварщик получает больше программиста» v1 (2026-11-12)
- svarshchik-v1.mp4 — 1080x1920, 24 fps, 60 сек. Голос hU3rD0Yk7DoiYULTX1pD, **eleven_v4**. Сценарий: ne-tupi-idei/svarshchik/scenariy-v1.md.
- Впервые два человечка: Дима (обычный) и сварщик (шире ×1.22, ниже, жёлтая каска с тёмными очками). Каска и пропорции добавлены в kod/3d/index.html (параметры позы bw, th, lh, helmet), рендер с прозрачным фоном (omitBackground), чтобы под человечками были видны фоны.
- Впервые тематические фоны (просьба Ярослава): университет, стройка с краном, офис, коридор с дверью «ВАКАНСИЯ», город, комната. Светло-серые линии, функции bg_* в compose_s.py.
- Порядок: из kod/ при запущенном `python3 -m http.server 8777` → track_s.py → `node 3d/frames.js track.json kadry flat 1080 1920` → compose_s.py → mix_s.py → склейка ffmpeg. anim3d/anim берутся из claude-skills/ne-tupi (нужен pip cairosvg).
- zvuk/voice.mp3 — сырая озвучка, voice.wav — с паузой 0,5 сек перед «Всё. Не тупи», align2.json сдвинут.
- Обложки: oblozhka/ (A «ОЧЕРЕДЬ К НЕМУ», B «ДИПЛОМ НЕ ПЛАТИТ»), код cover_s.py.
