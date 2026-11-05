import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from '../palette';
import * as S from './Shots';
import * as W from './World04';
import {SceneTeaser} from './World02';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
// Серия 4 «До зарплаты не хватает», сценарий v3. [время, ракурс, что происходит, кадр]
export const BOARDS04: [string, string, string, React.ReactNode][] = [
  ['0.0–1.0', 'С заднего: зеркало', 'ЩЁЛК счётчика + оранжевая вспышка, хлопок двери, глаза Ашота в зеркале', <S.ShotMirror brow={0.6} sub={null} />],
  ['1.0–2.0', 'Заднее сиденье', 'Кристина падает на сиденье, телефон в камеру: «312 ₽ · до зарплаты 9 дней»', <W.ShotKristina e={{worry: 1, sweat: 1}} phone />],
  ['2.0–4.0', 'Сбоку, пассажирское', 'Ашот хитро: «Джан, я знаю, куда у тебя деваются десять тысяч»', <S.ShotSide turn={0.55} text="Знаю, куда деваются десять тысяч" keys={['десять', 'тысяч']} />],
  ['4.0–5.0', 'Заднее сиденье', '«Ашот, гони в МФО!» Плашка «КУДА ИСЧЕЗАЮТ 10 000?» в угол', <W.ShotKristina e={{mouth: 3, shock: 0.6}} lean={0.6} />],
  ['5.0–9.0', 'Улица, вывеска', '«ВСЕГО 0,8%» мигает неоном, трескается — вываливается «292% ГОДОВЫХ»', <W.SceneLoanSign lt={2.4} dur={3} />],
  ['9.0–13.0', 'Календарь', '«И ты ведь не раз берёшь. Каждый месяц»: 12 листов по −2 400, монеты в трубу МФО', <W.SceneLoanCalendar lt={2.6} dur={3.5} />],
  ['13.0–15.5', 'Кофейня', '«Ну давай, скажи — не пей кофе!» Стаканчик 300 ₽ перечёркивается: НЕ КОФЕ', <W.SceneNotCoffee lt={0.9} dur={3} />],
  ['15.5–17.0', 'Пакет доставки', 'Без слов: НЕ ДОСТАВКА (1 сек)', <W.SceneNotCoffee lt={2.6} dur={3} />],
  ['17.0–19.5', 'Заднее сиденье', 'Кристина подаётся вперёд: «Ты меня сейчас обвиняешь?!»', <W.ShotKristina e={{mouth: 2, worry: 1, smile: 0}} lean={1} />],
  ['19.5–22.0', 'Сбоку, пассажирское', 'Ашот мягко, стучит по таксометру: «Нет, джан. Я тебя считаю»', <S.ShotSide turn={1} arm="up" text="Нет, джан. Я тебя считаю" keys={['считаю']} />],
  ['22.0–27.0', 'Таксометр крупно', 'СЮРПРИЗЫ ГОДА: праздники + школа → 55 000. Вставки: ёлка, линейка', <W.SceneSurprises lt={2.5} dur={15} />],
  ['27.0–30.0', 'Заднее сиденье', '«Ну Новый год же не отменишь!» … «Да он за лето вырос!»', <W.ShotKristina e={{mouth: 2, smile: 0.2}} lean={0.3} />],
  ['30.0–33.0', 'Таксометр крупно', 'Врачи + куртка сыну → 95 000. Вставки: кресло стоматолога, куртка', <W.SceneSurprises lt={8} dur={15} />],
  ['33.0–37.0', 'Таксометр: стоп-кадр', 'Телефон + к маме → 120 000. Зум, затемнение по краям. «Ну это же всё внезапно…»', <W.SceneSurprises lt={14.5} dur={15} />],
  ['37.0–41.0', 'Двор зимой', '«Внезапно — это когда метеорит. А Новый год каждый год 31-го»', <W.SceneMeteor lt={2.6} dur={4} />],
  ['41.0–47.0', 'Цифры крупно', '120 000 ÷ 12 = 10 000. «…Десять. Ровно десять». Плашка переворачивается', <W.SceneDivide lt={4.5} dur={5} />],
  ['47.0–58.0', 'Конверт и счёт', '«Начни с 2 400 — то, что МФО отдала бы». Конверт «СЮРПРИЗЫ», счёт с процентами', <W.SceneEnvelope lt={4} dur={5} />],
  ['58.0–62.0', 'Навигатор', '«Разворачивай!» — «Я давно развернул». Маршрут к «Дом», МФО зачёркнута', <W.SceneNavHome lt={3} dur={4} />],
  ['62.0–70.0', 'Глазами пассажира → шпаргалка', '«С тебя триста рублей… Я и есть сюрприз». Шпаргалка 5 сек', <W.SceneCheat lt={2} dur={5} />],
  ['70.0–75.0', 'Салон: тизер', 'Таксометр на 0, дверь, тётя Люда: «Ашот, я кредит на шубу взяла!»', <SceneTeaser lt={1.5} dur={4} />],
];
const CW = 430, CH = 764, GAP = 30, CAP = 180;
export const Storyboard04: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={2420} height={4040} viewBox="0 0 2420 4040">
      <text x={40} y={90} fontFamily="Rubik" fontWeight={900} fontSize={64} fill={P.ink}>Таксист Ашот · «До зарплаты не хватает» · раскадровка</text>
      {BOARDS04.map(([tm, ang, what, node], i) => {
        const x = 40 + (i % 5) * (CW + GAP), y = 140 + Math.floor(i / 5) * (CH + CAP + 30);
        return (
          <g key={i}>
            <clipPath id={`d${i}`}><rect x={x} y={y} width={CW} height={CH} rx={22} /></clipPath>
            <g clipPath={`url(#d${i})`}><svg x={x} y={y} width={CW} height={CH} viewBox="0 0 1080 1920">{(node as any).type((node as any).props).props.children}</svg></g>
            <rect x={x} y={y} width={CW} height={CH} rx={22} fill="none" stroke={P.ink} strokeWidth={5} />
            <circle cx={x + 40} cy={y + 40} r={30} fill={P.mustard} stroke={P.ink} strokeWidth={4} />
            <text x={x + 40} y={y + 51} textAnchor="middle" fontFamily="Rubik" fontWeight={900} fontSize={32} fill={P.ink}>{i + 1}</text>
            <text x={x} y={y + CH + 38} fontFamily="Rubik" fontWeight={900} fontSize={28} fill={P.terracotta}>{tm} сек</text>
            <text x={x} y={y + CH + 72} fontFamily="Rubik" fontWeight={900} fontSize={26} fill={P.ink}>{ang}</text>
            <foreignObject x={x} y={y + CH + 84} width={CW} height={CAP - 40}>
              <div style={{fontFamily: 'Rubik', fontWeight: 600, fontSize: 24, lineHeight: 1.25, color: P.ink}}>{what}</div>
            </foreignObject>
          </g>
        );
      })}
    </svg>
  </AbsoluteFill>
);
