import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {Ashot, AshotState} from './characters/Ashot';
import {RiderFigure, RIDERS, EMO} from './characters/Rider';

// Аватарки профиля Instagram. Каждая — квадрат 1080×1080, Instagram обрежет в круг,
// поэтому всё важное держим внутри вписанного круга. Проверка: лист AvatarSheet
// показывает каждую в круге крупно и в размере ленты/комментариев.
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}

const base: AshotState = {t: 0, turn: 0.62, browL: 0, browR: 0.25, blink: 0, wink: 0, mouth: 0, smirk: 1, look: [0, 0], arm: {from: 'rest', to: 'rest', k: 1}, noRightArm: true};
const TIM = RIDERS[0];

// Шашечки такси по кругу
const CheckerRing: React.FC<{r: number; w: number; n: number; light?: string; dark?: string}> = ({r, w, n, light = '#FFF6E2', dark: dk = P.ink}) => (
  <g>
    {Array.from({length: n}, (_, i) => [0, 1].map((row) => {
      const a0 = (i / n) * Math.PI * 2, a1 = ((i + 1) / n) * Math.PI * 2;
      const r0 = r - w + row * (w / 2), r1 = r0 + w / 2;
      const p = (rr: number, a: number) => `${540 + rr * Math.cos(a)},${540 + rr * Math.sin(a)}`;
      const dark = (i + row) % 2 === 0;
      return <path key={i + '-' + row} d={`M${p(r0, a0)} L${p(r1, a0)} A${r1},${r1} 0 0 1 ${p(r1, a1)} L${p(r0, a1)} A${r0},${r0} 0 0 0 ${p(r0, a0)}Z`} fill={dark ? dk : light} />;
    }))}
  </g>
);

const Coin: React.FC<{x: number; y: number; r: number}> = ({x, y, r}) => (
  <g transform={`translate(${x},${y})`}>
    <circle r={r + 10} fill={P.ink} />
    <circle r={r} fill={P.gold} />
    <circle r={r * 0.78} fill="none" stroke={P.goldDark} strokeWidth={r * 0.08} />
    <text y={r * 0.36} textAnchor="middle" fontFamily="Rubik" fontWeight={900} fontSize={r * 1.05} fill={P.ink}>₽</text>
  </g>
);

export type AvatarId = 'A' | 'B' | 'C' | 'D' | 'E' | 'F';
export const AVATARS: {id: AvatarId; name: string; note: string}[] = [
  {id: 'A', name: 'Классика', note: 'Ашот с ухмылкой на горчичном'},
  {id: 'B', name: 'Шашечки', note: 'подмигивает, рамка-шашки такси'},
  {id: 'C', name: 'Ашот и рубль', note: 'зелёный фон, золотая монета'},
  {id: 'D', name: 'Дуэт', note: 'Ашот и Тимур, цвета героев'},
  {id: 'E', name: 'Крупно', note: 'только лицо: кепка, глаза, усы'},
];

export const AvatarArt: React.FC<{v: AvatarId}> = ({v}) => {
  switch (v) {
    case 'A': return (
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.mustard} />
        <circle cx={540} cy={470} r={400} fill="#F5C969" />
        <svg x={0} y={0} width={1080} height={1080} viewBox="-340 -520 680 680"><Ashot s={base} /></svg>
      </svg>
    );
    case 'B': return (
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.mustard} />
        <svg x={0} y={0} width={1080} height={1080} viewBox="-360 -540 720 720"><Ashot s={{...base, wink: 1, browR: 0.6, mouth: 1}} /></svg>
        <CheckerRing r={540} w={86} n={36} />
      </svg>
    );
    case 'C': return (
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.sage} />
        <circle cx={540} cy={470} r={400} fill="#93C07F" />
        <svg x={0} y={0} width={1080} height={1080} viewBox="-340 -520 680 680"><Ashot s={{...base, turn: 0.5, look: [0.5, 0.1]}} /></svg>
        <Coin x={790} y={760} r={120} />
      </svg>
    );
    case 'F': return ( // выбор автора: C + чёрно-белые шашечки по краю
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.sage} />
        <circle cx={540} cy={470} r={400} fill="#93C07F" />
        <svg x={0} y={0} width={1080} height={1080} viewBox="-360 -540 720 720"><Ashot s={{...base, turn: 0.5, look: [0.5, 0.1]}} /></svg>
        <Coin x={745} y={730} r={110} />
        <CheckerRing r={540} w={86} n={36} light="#FFFFFF" dark="#111111" />
      </svg>
    );
    case 'D': return (
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.sage} />
        <path d="M0,0 L700,0 L420,1080 L0,1080Z" fill={P.mustard} />
        <svg x={440} y={170} width={620} height={1020} viewBox="-230 -300 460 757"><RiderFigure r={TIM} e={{...EMO.calm, look: [-0.7, 0], smile: 0.9}} /></svg>
        <svg x={20} y={110} width={760} height={1000} viewBox="-300 -480 600 790"><Ashot s={{...base, turn: 0.95, look: [0.4, 0], browR: 0.5}} /></svg>
      </svg>
    );
    case 'E': return (
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <rect width={1080} height={1080} fill={P.mustard} />
        <svg x={0} y={0} width={1080} height={1080} viewBox="-235 -470 470 470"><Ashot s={{...base, turn: 0.62}} /></svg>
      </svg>
    );
  }
};

export const Avatar: React.FC<{v: AvatarId}> = ({v}) => (
  <AbsoluteFill style={{background: P.cream}}><AvatarArt v={v} /></AbsoluteFill>
);

// Лист проверки: каждая аватарка в круге — крупно, в шапке профиля и в комментариях.
export const AvatarSheet: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={1080} height={2300} viewBox="0 0 1080 2300">
      <text x={50} y={100} fontFamily="Rubik" fontWeight={900} fontSize={60} fill={P.ink}>Аватарка: 5 вариантов</text>
      <text x={50} y={160} fontFamily="Rubik" fontWeight={800} fontSize={30} fill={P.ink} opacity={0.6}>крупно · в шапке профиля · в комментариях</text>
      <defs>
        <clipPath id="c" clipPathUnits="objectBoundingBox"><circle cx={0.5} cy={0.5} r={0.5} /></clipPath>
      </defs>
      {AVATARS.map((a, i) => {
        const y = 210 + i * 415;
        const circ = (x: number, yy: number, s: number) => (
          <g>
            <foreignObject x={x} y={yy} width={s} height={s} style={{clipPath: 'circle(50%)'}}>
              <div style={{width: 1080, height: 1080, transform: `scale(${s / 1080})`, transformOrigin: '0 0'}}><AvatarArt v={a.id} /></div>
            </foreignObject>
          </g>
        );
        return (
          <g key={a.id}>
            <rect x={30} y={y} width={1020} height={390} rx={30} fill={P.beige} />
            {circ(55, y + 25, 340)}
            <text x={430} y={y + 85} fontFamily="Rubik" fontWeight={900} fontSize={50} fill={P.ink}>{a.id} · {a.name}</text>
            <text x={430} y={y + 130} fontFamily="Rubik" fontWeight={800} fontSize={27} fill={P.ink} opacity={0.65}>{a.note}</text>
            {circ(430, y + 180, 170)}
            {circ(640, y + 230, 70)}
            {circ(760, y + 248, 34)}
          </g>
        );
      })}
    </svg>
  </AbsoluteFill>
);
