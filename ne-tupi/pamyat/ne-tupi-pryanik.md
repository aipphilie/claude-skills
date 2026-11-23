---
name: ne-tupi-pryanik
description: Шуточный рилс «Пряник и Claude Code» (2026-11-21): новый персонаж пряник, сценарий-инструкция по настройке Claude Code, статус
metadata:
  type: project
  modified: 2026-11-21T13:38:46.161Z
---
2026-11-21: Ярослав попросил шуточный рилс. Новый главный герой — круглый ПРЯНИК (не человечек), впервые открыл Claude Code «и в ахуе»; голос подкалывает и даёт базовую настройку, чтобы Claude не терял контекст. «Remotion Control» у Ярослава = Remote Control.
- Сценарий v1 (~134 слова): /mnt/project-files/ne-tupi-idei/pryanik/scenariy-v1.md. Шаги: репозиторий с GitHub, /init → CLAUDE.md, одна задача — один чат, claude --continue, claude remote-control (рули с телефона, код на своём компе). Факты сверены с code.claude.com/docs.
- Концепт пряника: koncept/varianty.png (A глазурь+только рот, B лицо из глазури с глазами — реком., C тёмный тульский с надкусом), кадры kadry-ABC.png, код pryanik.py (SVG → PNG через node shot.js). Пряник молчит, реакции пузырями.
- Ярослав одобрил сценарий и пряника B («охуенно»), попросил больше мата/подколов и НЕ заморачиваться с анимацией (одно движение): ролик для прикола над другом, не для профиля, обложки не нужны.
- Рендер v1 (60 сек, 22 сцены, мат 3 раза): /mnt/project-files/ne-tupi-render/pryanik/pryanik-v1.mp4, код kod/ (compose_pr.py = scenes_head.py + engine_part.py, пряник рисуется в scenes_pr.py, рот по громкости голоса). PR #62. Ждём отзыв.
