# «Одна зарплата — две судьбы» (Лёха и Миша) v1 (2026-11-17)
- dvoe-v1.mp4: 1080x1920, 30 fps, 64,5 сек, 42 сцены. Голос hU3rD0Yk7DoiYULTX1pD, Eleven v4 (с тегами). Звуки из ne-tupi-zvuki/gotovye ×0.5 (76 событий). Музыки нет.
- По сценарию Ярослава про двух кротов, переделан: Лёха (чёрный человечек, с середины в золотой цепи) и Миша (сварщик в каске). Сценарий, озвучка, подпись: ne-tupi/idei/dvoe/.
- Движок «Кредита»/«Квартиры» (весь экран, белый фон): kod/compose_dv.py = предметы props_dv.py + scenes_dv.py + движок (переходы, глубина, субтитры). Плашка «не инвестрекомендация» первые 5 сек.
- Новые предметы: chain_on (цепь на Лёхе), watch, bigchain, taxi, bag (доставка), wallet, piggy (копилка), books, laptop, bulb, pillow (подушка), clover, coinman (монетка-работяга), vs.
- Новые клипы сварщика: v_smile, v_shock, v_hips, v_nod, v_explain, v_point, v_think, v_read, v_box, v_boss, v_pointcam, v_shrug, v_armsup; Лёхи: laugh.
- Порядок: из kod/ python3 -m http.server 8777 → tts.py → clips.py → node 3d/frames.js clips.json kadry flat → compose_dv.py sheet 0.6 → ./run_dv.sh → cover_dv.py.
- Обложки: oblozhka/ (A «ЦЕПЬ ИЛИ КОПИЛКА?» рекомендую, B «ОДНА ЗАРПЛАТА / ДВЕ СУДЬБЫ»).
