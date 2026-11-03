# Голоса сериала «Таксист Ашот» (ElevenLabs Voice Design)

**Статус на 2026-11-03.** Голос Ашота подбирается в Voice Design. В библиотеке ElevenLabs пока нет ни одного сохранённого своего голоса (проверено по API). Тариф Free: можно сохранить до 3 своих голосов, через API голоса создавать нельзя, только вручную в интерфейсе. Озвучивать через API можно.

## Как сохранять

Voice Design → Generate → лучший вариант → **Save voice**. Имя строго как в таблице ниже, по нему я нахожу голос через API.

Настройки Voice Design:
- выключить «Generate Preview Text» и вставить свой пробный текст;
- Guidance Scale 80–90%;
- Loudness оставить по умолчанию.

## Ашот — постоянный голос сериала (`Ашот`)

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
При генерации реплик: Speed 1.1–1.15. Реплики пишутся с «э» после согласных, **цифры без искажений**. Если всё равно медленно, ускорю на монтаже на 5–15% без смены тона.

## Пассажиры — новый голос под каждый типаж

На Free тарифе свободных слотов два. Держим Ашота и 1–2 пассажиров текущих серий, старых удаляем.

| Типаж (Rider.tsx) | Имя голоса | Prompt | Пробный текст |
|---|---|---|---|
| Молодой пацан — **Тимур** (серия «Ипотека») | `Тимур` | `Young Russian guy, 20-25, no accent. Fast casual street-style speech, a bit naive and excited, easily impressed. Light, slightly nasal voice. His voice cracks up high when shocked. Natural, modern, not a cartoon.` | `Ашот, брат, я ипотеку взял! Пять лямов, прикинь? Чего?! Двенадцать? Да ну, гонишь… А где я лишние десять тысяч возьму?` |
| Тётя Люда, 60 | `Люда` | `Russian woman, 60, no accent. Warm, loud, chatty, slightly theatrical, a typical talkative auntie. Fast emotional speech, sighs and exclamations, sometimes a little shrill when outraged.` | `Ашот, я кредит на шубу взяла! Ну а что, все берут! Как это переплачу? Ой, мамочки… Да ты что!` |
| Школьник, 10 | `Школьник` | `Russian boy, 10 years old, no accent. High clear child voice, curious, fast, a little cheeky, asks lots of questions, giggles.` | `Дядя Ашот, а зачем копить, если можно сразу купить? А если я сто рублей в копилку положу, они вырастут?` |
| Студентка, 20 | `Студентка` | `Russian girl, 20, no accent. Bright, quick, slightly ironic, modern student slang, expressive, laughs easily.` | `Ашот, ну я же не транжира, я просто кофе каждый день беру! Сколько-сколько за год? Серьёзно?!` |
| Дед Михалыч, 70 | `Михалыч` | `Russian old man, 70, no accent. Slow-ish, gravelly, grumpy but kind, old-school, a bit hard of hearing, says "в наше время".` | `Ашот, в наше время сберкнижку завели — и спокойно! Чего? Инфляция? А ну-ка объясни старику.` |
| Офисный клерк, 30 | `Клерк` | `Russian man, 30, no accent. Neat, polite, slightly nervous, fast office-speak, sighs when stressed.` | `Ашот, у меня три кредитки, но я всё контролирую. Ну… почти. Минимальный платёж же плачу!` |

## Связь с движком

- `tools/tts.py`: если задан `ELEVENLABS_API_KEY`, берёт голоса из `EL_ASHOT` и `EL_PASS` (id голосов). Иначе работает edge-tts как временная заглушка.
- Id голосов ищу через API по имени (Voices: Read) и прописываю в окружение перед рендером.
- Ключ API хранить в настройках окружения (`ELEVENLABS_API_KEY`), **не в чате и не в репозитории**.
