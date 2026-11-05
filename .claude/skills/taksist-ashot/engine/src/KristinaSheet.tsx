import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {RiderFigure, KRISTINA, EMO} from './characters/Rider';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
const cols: [string, string][] = [['calm', 'спокойна'], ['talk', 'говорит'], ['worry', 'растеряна'], ['shock', 'шок']];
export const KristinaSheet: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={1760} height={1400} viewBox="0 0 1760 1400">
      <text x={40} y={70} fontFamily="Rubik" fontWeight={900} fontSize={52} fill={P.ink}>Кристина, 32 · кассир, мама первоклассника</text>
      {cols.map(([, n], j) => <text key={n} x={330 + j * 400} y={140} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={30} fill={P.ink}>{n}</text>)}
      {KRISTINA.map((r, i) => (
        <g key={i}>
          <text x={30} y={170 + i * 410 + 200} fontFamily="Rubik" fontWeight={900} fontSize={30} fill={P.ink} transform={`rotate(-90 30 ${370 + i * 410})`} textAnchor="middle">{r.name}</text>
          {cols.map(([k], j) => (
            <g key={k}>
              <rect x={140 + j * 400} y={170 + i * 410} width={380} height={380} rx={28} fill={P.beige} />
              <svg x={140 + j * 400} y={170 + i * 410} width={380} height={380} viewBox="-250 -330 500 500"><RiderFigure r={r} e={EMO[k]} /></svg>
            </g>
          ))}
        </g>
      ))}
    </svg>
  </AbsoluteFill>
);
