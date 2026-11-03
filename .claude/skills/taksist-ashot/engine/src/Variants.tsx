import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {AshotVariant, LOOKS} from './characters/AshotVariant';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
export const Variants: React.FC = () => (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={2500} height={1200} viewBox="0 0 2500 1200">
      <text x={50} y={86} fontFamily="Rubik" fontWeight={900} fontSize={62} fill={P.ink}>Варианты Ашота</text>
      {LOOKS.map((l, i) => (
        <g key={i}>
          <rect x={30 + i * 490} y={130} width={460} height={960} rx={30} fill={P.beige} />
          <svg x={30 + i * 490} y={130} width={460} height={960} preserveAspectRatio="xMidYMin slice" viewBox="-300 -470 600 1250"><AshotVariant l={l} /></svg>
          <text x={260 + i * 490} y={1150} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={36} fill={P.ink}>{l.name}</text>
        </g>
      ))}
    </svg>
  </AbsoluteFill>
);
