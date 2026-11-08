import React from 'react';
import {AbsoluteFill, staticFile, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {measure} from './lib';
import {RiderFigure, KRISTINA, SVETA, ZINA, VLAD, EMO, Rider} from './characters/Rider';
const h = typeof window !== 'undefined' ? delayRender('f') : 0;
if (typeof window !== 'undefined') {
  const fs = [800, 900].flatMap((w) => ['cyrillic', 'latin'].map((s) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${s}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(fs.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(h));
}
const colsF: [string, string][] = [['calm', 'спокойна'], ['talk', 'говорит'], ['worry', 'растеряна'], ['shock', 'шок']];
const colsM: [string, string][] = [['calm', 'спокоен'], ['talk', 'говорит'], ['worry', 'растерян'], ['shock', 'шок']];
// подпись строки не длиннее карточки (380 px): иначе уменьшаем шрифт
const fitSize = (t: string, size: number, maxW: number) => Math.min(size, size * maxW / measure(t, size));
const Sheet: React.FC<{title: string; set: Rider[]; male?: boolean}> = ({title, set, male}) => { const cols = male ? colsM : colsF; return (
  <AbsoluteFill style={{background: P.cream}}>
    <svg width={1760} height={1400} viewBox="0 0 1760 1400">
      <text x={40} y={70} fontFamily="Rubik" fontWeight={900} fontSize={fitSize(title, 52, 1680)} fill={P.ink}>{title}</text>
      {cols.map(([, n], j) => <text key={n} x={330 + j * 400} y={140} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={30} fill={P.ink}>{n}</text>)}
      {set.map((r, i) => (
        <g key={i}>
          <text x={30} y={170 + i * 410 + 200} fontFamily="Rubik" fontWeight={900} fontSize={fitSize(r.name, 30, 360)} fill={P.ink} transform={`rotate(-90 30 ${370 + i * 410})`} textAnchor="middle">{r.name}</text>
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
); };

export const KristinaSheet: React.FC = () => <Sheet title="Кристина, 32 · кассир, мама первоклассника" set={KRISTINA} />;
export const SvetaSheet: React.FC = () => <Sheet title="Света, 22 · студентка, «кредитка на Турцию»" set={SVETA} />;
export const VladSheet: React.FC = () => <Sheet title="Влад, 19 · студент, «подработка в прачечной»" set={VLAD} male />;
export const ZinaSheet: React.FC = () => <Sheet title="Баба Зина, 68 · бывшая учительница, «безопасный счёт»" set={ZINA} />;
