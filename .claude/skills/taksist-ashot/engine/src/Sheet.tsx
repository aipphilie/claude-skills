import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {Ashot, AshotState} from './characters/Ashot';
import {Passenger, PassengerState} from './characters/Passenger';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
const base: AshotState = {t: 0, turn: 1, browL: 0, browR: 0.15, blink: 0, wink: 0, mouth: 0, smirk: 1, look: [0.55, -0.1], arm: {from: 'rest', to: 'rest', k: 1}};
const A: [string, Partial<AshotState>][] = [
  ['смотрит в зеркало', {turn: 0, smirk: 0, look: [-0.6, -0.6], browL: 0.9}],
  ['ухмылка', {}],
  ['говорит', {mouth: 2, arm: {from: 'up', to: 'up', k: 1}}],
  ['подмигивает', {wink: 1, browR: 0.5, mouth: 1}],
  ['«с тебя 400»', {arm: {from: 'palm', to: 'palm', k: 1}, mouth: 3}],
];
const pb: PassengerState = {blink: 0, mouth: 0, shock: 0, worry: 0, look: [-0.5, 0], sweat: 0};
const PS: [string, Partial<PassengerState>][] = [
  ['спокоен', {mouth: 1, look: [0.3, 0]}],
  ['растерян', {worry: 1, sweat: 1}],
  ['шок «Чего?!»', {shock: 1, mouth: 3}],
];
const label = (x: number, y: number, s: string) => <text x={x} y={y} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={34} fill={P.ink}>{s}</text>;
export const Sheet: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={2400} height={960} viewBox="0 0 2400 960">
      <text x={60} y={90} fontFamily="Rubik" fontWeight={900} fontSize={64} fill={P.ink}>Таксист Ашот</text>
      {A.map(([n, o], i) => (
        <g key={i}>
          <rect x={30 + i * 470} y={130} width={440} height={720} rx={30} fill={P.beige} />
          <svg x={30 + i * 470} y={130} width={440} height={720} viewBox="-380 -480 760 1100"><Ashot s={{...base, ...o}} /></svg>
          {label(250 + i * 470, 900, n)}
        </g>
      ))}
      
      {[].map(([n, o], i) => (
        <g key={i}>
          <rect x={30 + i * 470} y={1040} width={440} height={380} rx={30} fill={P.beige} />
          <svg x={30 + i * 470} y={1040} width={440} height={380} viewBox="-230 -280 460 400"><Passenger s={{...pb, ...o}} /></svg>
          {label(250 + i * 470, 1465, n)}
        </g>
      ))}
    </svg>
  </AbsoluteFill>
);
