import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from '../palette';
import * as S from './Shots';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
// [время, ракурс, что происходит, кадр]
export const BOARDS: [string, string, string, React.ReactNode][] = [
  ['0.0–0.8', 'Снаружи, сбоку', 'Такси влетает, щёлк поворотника, камера ныряет в окно', <S.ShotExterior t={0.3} />],
  ['0.8–1.8', 'С переднего сиденья назад', 'Пацан суёт телефон: «ИПОТЕКА ОДОБРЕНА», конфетти', <S.ShotPhone />],
  ['1.8–2.6', 'С заднего: зеркало', 'Голова Ашота наполовину на зеркале, в зеркале глаза, бровь ползёт вверх', <S.ShotMirror />],
  ['2.6–3.4', 'Сбоку, пассажирское', 'Ашот резко поворачивается, ухмылка, вжух', <S.ShotSide turn={0.55} text="Пять взял?" keys={['Пять']} whoosh />],
  ['3.4–5.0', 'Таксометр крупно', 'Цифры крутятся до 12 000 000, дым, касса', <S.ShotMeter mode="crazy" />],
  ['5.0–5.8', 'Спереди, через лобовое', '«Чего?!» — шок, машина подпрыгивает на кочке, шашки мигают', <S.ShotCarFront text="Чего?!" />],
  ['5.8–7.0', 'Сбоку, пассажирское', 'Ашот спокойно, палец вверх', <S.ShotSide turn={1} arm="up" text="Банк тебе не квартиру продал" keys={[]} />],
  ['7.0–9.5', 'Заднее сиденье', 'Пацан стареет: 3 склейки, за окном сезоны, календарь 2026→2046', <S.ShotAging />],
  ['9.5–10.5', 'Торпеда', 'Телефон в держателе, рука Ашота тянется к навигатору', <S.ShotDash />],
  ['10.5–12.5', 'Экран навигатора', 'Карточки маршрутов: «платёж» 20 лет в пробках, «срок» быстрее. Тык — зелёный', <S.ShotNav />],
  ['12.5–13.5', 'Сверху', 'Слева пробка на 20 лет, такси проскакивает развилку по короткой', <S.ShotTopDown />],
  ['13.5–14.3', 'Таксометр крупно', 'Цифры отматываются назад, монеты летят обратно', <S.ShotMeter mode="rewind" />],
  ['14.3–15.0', 'С заднего: зеркало', 'В зеркале Ашот подмигивает', <S.ShotMirror wink={1} brow={0.3} />],
  ['15.0–16.5', 'Глазами пассажира', 'Ладонь на камеру, таксометр щёлкает 400 ₽', <S.ShotPOV />],
  ['16.5–17.0', 'Салон: стоп-кадр', 'Ашот с протянутой рукой, пацан в шоке, штамп 400 ₽, вспышка, затвор', <S.ShotFreeze />],
];
const CW = 430, CH = 764, GAP = 30, CAP = 180;
export const Storyboard: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={2420} height={3050} viewBox="0 0 2420 3050">
      <text x={40} y={90} fontFamily="Rubik" fontWeight={900} fontSize={64} fill={P.ink}>Таксист Ашот · «Ипотека» · раскадровка</text>
      {BOARDS.map(([tm, ang, what, node], i) => {
        const x = 40 + (i % 5) * (CW + GAP), y = 140 + Math.floor(i / 5) * (CH + CAP + 30);
        return (
          <g key={i}>
            <clipPath id={`c${i}`}><rect x={x} y={y} width={CW} height={CH} rx={22} /></clipPath>
            <g clipPath={`url(#c${i})`}><svg x={x} y={y} width={CW} height={CH} viewBox="0 0 1080 1920">{(node as any).type((node as any).props).props.children}</svg></g>
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
