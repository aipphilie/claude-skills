# «Если все перестанут платить кредит» v1 (2026-11-16)
- kredit-v1.mp4 — 1080x1920, 30 fps, 64,6 сек, 38 сцен. Голос hU3rD0Yk7DoiYULTX1pD, Eleven v4. Звуки из ne-tupi-zvuki/gotovye ×0.5 (78 событий). Музыки нет.
- Идея Ярослава, без чужого референса. Сценарий, хуки и источники: ne-tupi/idei/kredit/.
- Движок «Квартиры» (кадр на весь экран, белый фон, без чёрных полос): kod/base_k.py + kod/compose_kr.py.
- Новые нарисованные предметы: bank (банк с колоннами, трещина, уходит под землю), crowd (толпа из всех 4 персонажей), flames (огонь), atm (банкомат), gavel (молоток судьи), press (печатный станок ЦБ), pricetag (ценник), globe_ (глобус с трещинами), house (домик с табличкой), pocket (карман с молью), scissors, usflag, arrow, coinflow.
- Новые клипы: g_idle/g_sad/g_shock/g_cheer (девушка), v_idle/v_sad/v_cheer (сварщик), d_shock/d_sad/d_cheer (отец), *_walkR, cheer, box (несёт коробку).
- Порядок: из kod/ python3 -m http.server 8777 → tts.py → clips.py → node 3d/frames.js clips.json kadry flat → compose_kr.py sheet 0.6 → ./run_kr.sh → cover_kr.py.
- Обложки: oblozhka/ (A «НИКТО НЕ ПЛАТИТ» — рекомендую, B «ДОЛГ НЕ СГОРИТ»).

## v2 (2026-11-16)
- kredit-v2.mp4 — 67 сек, 39 сцен. Хук с криком и матом в первые 3,4 сек, мат в субтитрах через звёздочку (CENS в compose_kr.py), голос с тегами [shouting]/[excited]/[serious]. Новые сцены s_hook1, s_hook2, s_bolno, s_pizdec, pickets() — толпа с плакатами. Обложки oblozhka-v2-A «МЫ БОЛЬШЕ НЕ ПЛАТИМ!» (реком.) / B.
