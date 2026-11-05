# Голоса сериала «Таксист Ашот» (ElevenLabs Voice Design)

**Статус на 2026-11-03.** Тариф **Starter**: 40 000 символов в месяц, до 10 своих голосов. Ключ лежит в настройках облачного окружения (`ELEVENLABS_API_KEY`) и проверен по API. Голоса Ашота и Тимура сохранены и утверждены автором по пробам.

| Герой | Имя в ElevenLabs | Voice ID |
|---|---|---|
| Ашот (все серии) | `Ashot` | `aiETsjwAyUVKjNepebct` |
| Тимур (серия «Ипотека») | `Тимур` | `Inof0Um2Sd8Y9OYSblWu` |
| Кристина (серия «До зарплаты», 2026-11-05, проба А) | `Кристина` | `DPHZNjJnpZWDX0Noo7vV` |

Модель `eleven_v3`, similarity 0.75. Ашот: stability **0.0** (Creative) + тег `[strong Armenian accent]` перед каждой репликой (ставит `tts.py`), пассажиры: stability 0.5. Скорость: Ашот 1.1, пассажир 1.05. Полная серия «Ипотека» (30 реплик) — ~1 600 символов.

## Как сохранять

Voice Design → Generate → лучший вариант → **Save voice**. Имя как в таблице ниже. После сохранения id голоса прописывается сюда и в `engine/tools/tts.py`.

Настройки Voice Design:
- выключить «Generate Preview Text» и вставить свой пробный текст;
- Guidance Scale 80–90%;
- Loudness оставить по умолчанию.

## Ашот — постоянный голос сериала (`Ашот`)

**Армянский акцент (решение автора 2026-11-05).** С написанием «тэбе, дэньги, нэ» через «э» Ашот звучал «по-хохляцки»: модель читает такое «э» как украинское твёрдое «е». Сравнили 6 проб (`taksist-ashot/proba-golosov/armyanskij/` в папке проекта): старый голос, он же с тегом, библиотечный «Gogi Kavkaz» (грузинский акцент), три новых голоса Voice Design. Выбрана **проба №2**: тот же голос `aiETsjwAyUVKjNepebct`, реплики **обычной орфографией** (как в `sub`), в начале тег `[strong Armenian accent]`, stability 0.0. Эмоциональные теги (`[sly]`, `[pause]` и т.п.) оставлять. Акцент через «э», «слюшай», «дарагой» в тексте реплик больше не писать. Зато словечки «дорогой», «ара», «вах/вай», «джан» в сценарии нужны (см. SKILL.md), они пишутся обычной орфографией.
Тег меняется переменной `EL_ACCENT_ASHOT`. У ключа API нет права `voices_write`: сохранять новые голоса Voice Design и добавлять голоса из библиотеки — только в интерфейсе ElevenLabs.

**Решения автора:**
- акцент кавказский, **жёсткий**, «прямо в голосе»;
- говор **быстрее**, не медленно;
- пробный текст с написанием «как слышится» даёт нужный эффект.

Prompt (меньше 500 символов):
```
Thick Caucasian (Armenian) accent in Russian, the key feature. Man, 55. Deep, low, raspy smoker's voice. Hard rolled R, stretched vowels, soft consonants ("слюшай", "дарагой"), sing-song rising-falling intonation, odd word stress. Fast, brisk, energetic pace, no long pauses. Sly, warm, funny old Caucasian taxi driver giving life advice. Heavy accent in every word.
```
Пробный текст:
```
Слюшай, дарагой, я тэбе адну вэщь скажу, толко нэ обижайся, да? Банк тэбе нэ квартиру продал, а дваццать лэт твоей жизни, панимаишь? Гаси досрочно, срок уменьшай, а нэ платёж. Запомнил, брат? С тэбя чэтырэста рублей.
```
При генерации реплик: Speed 1.1–1.15. Реплики пишутся обычной орфографией (см. выше про армянский акцент), **цифры без искажений**. Если всё равно медленно, ускорю на монтаже на 5–15% без смены тона.

## Пассажиры — новый голос под каждый типаж

На Starter до 10 своих голосов: хватит на Ашота и всех пассажиров из таблицы.

| Типаж (Rider.tsx) | Имя голоса | Prompt | Пробный текст |
|---|---|---|---|
| Молодой пацан — **Тимур** (серия «Ипотека») | `Тимур` | `Young Russian guy, 20-25, no accent. Fast casual street-style speech, a bit naive and excited, easily impressed. Light, slightly nasal voice. His voice cracks up high when shocked. Natural, modern, not a cartoon.` | `Ашот, брат, я ипотеку взял! Пять лямов, прикинь? Чего?! Двенадцать? Да ну, гонишь… А где я лишние десять тысяч возьму?` |
| Тётя Люда, 60 | `Люда` | `Russian woman, 60, no accent. Warm, loud, chatty, slightly theatrical, a typical talkative auntie. Fast emotional speech, sighs and exclamations, sometimes a little shrill when outraged.` | `Ашот, я кредит на шубу взяла! Ну а что, все берут! Как это переплачу? Ой, мамочки… Да ты что!` |
| Школьник, 10 | `Школьник` | `Russian boy, 10 years old, no accent. High clear child voice, curious, fast, a little cheeky, asks lots of questions, giggles.` | `Дядя Ашот, а зачем копить, если можно сразу купить? А если я сто рублей в копилку положу, они вырастут?` |
| Студентка, 20 | `Студентка` | `Russian girl, 20, no accent. Bright, quick, slightly ironic, modern student slang, expressive, laughs easily.` | `Ашот, ну я же не транжира, я просто кофе каждый день беру! Сколько-сколько за год? Серьёзно?!` |
| Дед Михалыч, 70 | `Михалыч` | `Russian old man, 70, no accent. Slow-ish, gravelly, grumpy but kind, old-school, a bit hard of hearing, says "в наше время".` | `Ашот, в наше время сберкнижку завели — и спокойно! Чего? Инфляция? А ну-ка объясни старику.` |
| Офисный клерк, 30 | `Клерк` | `Russian man, 30, no accent. Neat, polite, slightly nervous, fast office-speak, sighs when stressed.` | `Ашот, у меня три кредитки, но я всё контролирую. Ну… почти. Минимальный платёж же плачу!` |

## Связь с движком

- `tools/tts.py`: если задан `ELEVENLABS_API_KEY`, озвучивает через ElevenLabs. Id голосов по умолчанию Ашот и Тимур (см. таблицу), для другого пассажира задать `EL_PASS=<id>`. Без ключа работает edge-tts как временная заглушка.
- Готовые mp3 в `public/voice/` не перегенерируются, чтобы не тратить символы. Перегенерировать реплику: удалить её mp3 и запустить снова.
- В `lines.json` у реплики `text` — для голоса (обычная орфография + эмоциональные теги), `sub` — то же без тегов, для субтитров.
- Ключ API хранить в настройках окружения (`ELEVENLABS_API_KEY`), **не в чате и не в репозитории**.
