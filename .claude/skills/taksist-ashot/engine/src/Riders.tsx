import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {RiderFigure, RIDERS, EMO} from './characters/Rider';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
const rows: [string, string][] = [['calm', 'спокоен'], ['worry', 'растерян'], ['shock', 'шок']];
export const Riders: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={2460} height={1420} viewBox="0 0 2460 1420">
      <text x={40} y={80} fontFamily="Rubik" fontWeight={900} fontSize={58} fill={P.ink}>Пассажиры: новый в каждой серии</text>
      {RIDERS.map((r, i) => (
        <g key={i}>
          <text x={240 + i * 400} y={160} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={34} fill={P.ink}>{r.name}</text>
          {rows.map(([k], j) => (
            <g key={k}>
              <rect x={50 + i * 400} y={190 + j * 400} width={380} height={380} rx={28} fill={P.beige} />
              <svg x={50 + i * 400} y={190 + j * 400} width={380} height={380} viewBox="-190 -300 380 380"><RiderFigure r={r} e={EMO[k]} /></svg>
            </g>
          ))}
        </g>
      ))}
      {rows.map(([, n], j) => <text key={n} x={30} y={390 + j * 400} fontFamily="Rubik" fontWeight={800} fontSize={26} fill={P.ink} transform={`rotate(-90 30 ${390 + j * 400})`} textAnchor="middle">{n}</text>)}
    </svg>
  </AbsoluteFill>
);
