import React from 'react';
import {P} from '../palette';

// Варианты внешности Ашота (анфас, по пояс). Начало координат — основание шеи.
export type Look = {
  name: string;
  face: 'round' | 'long' | 'square' | 'oval';
  build: number;            // ширина плеч, 1 = обычный
  neck: number;             // ширина шеи
  skin: string; shade: string;
  nose: 'bulb' | 'hook' | 'big';
  stache: 'walrus' | 'handlebar' | 'bushy' | 'chevron';
  stacheColor: string;
  brows: 'thick' | 'uni' | 'arched';
  eyes: 'sly' | 'round' | 'smile';
  stubble?: boolean;
  cheeks?: boolean;
  cap: string; capDark: string; capCheck?: boolean;
  shirt: string; shirtShade: string; stripes?: string;
  vest?: string;
  glassesOnCap?: boolean;
  chestHair?: boolean;
  belly?: boolean;
};

const O = 9;
const faces = {
  round: 'M-150,-260 Q-156,-390 0,-392 Q156,-390 150,-260 L150,-180 Q140,-70 0,-62 Q-140,-70 -150,-180Z',
  long: 'M-120,-280 Q-126,-400 0,-404 Q126,-400 120,-280 L118,-170 Q104,-50 0,-40 Q-104,-50 -118,-170Z',
  square: 'M-140,-280 Q-144,-394 0,-396 Q144,-394 140,-280 L142,-150 Q140,-74 90,-64 L-90,-64 Q-140,-74 -142,-150Z',
  oval: 'M-132,-270 Q-138,-392 0,-394 Q138,-392 132,-270 L128,-180 Q112,-66 0,-58 Q-112,-66 -128,-180Z',
};
const W = {round: 150, long: 120, square: 140, oval: 132};

export const AshotVariant: React.FC<{l: Look}> = ({l}) => {
  const hw = W[l.face];
  const sw = 250 * l.build;
  const nw = 62 * l.neck;
  const chinY = l.face === 'long' ? -40 : -62;
  const eyeY = -228;
  const eye = (cx: number, side: number) => {
    if (l.eyes === 'smile') return <path d={`M${cx - 22},${eyeY + 4} Q${cx},${eyeY - 16} ${cx + 22},${eyeY + 4}`} fill="none" stroke={P.ink} strokeWidth={8} strokeLinecap="round" />;
    const ry = l.eyes === 'sly' ? 13 : 20;
    return (
      <g>
        <ellipse cx={cx} cy={eyeY} rx={23} ry={ry} fill="#FFF8EC" stroke={P.ink} strokeWidth={6} />
        <circle cx={cx + 5} cy={eyeY + 1} r={10} fill={P.ink} />
        <circle cx={cx + 8} cy={eyeY - 3} r={3} fill="#fff" />
        {l.eyes === 'sly' && <path d={`M${cx - 27},${eyeY - 4} Q${cx},${eyeY - 18} ${cx + 27},${eyeY - 4 + side * 3}`} fill="none" stroke={P.ink} strokeWidth={7} strokeLinecap="round" />}
      </g>
    );
  };
  const brows = () => {
    if (l.brows === 'uni') return <path d="M-82,-262 Q-40,-284 0,-266 Q40,-284 82,-262" fill="none" stroke={P.brow} strokeWidth={22} strokeLinecap="round" />;
    if (l.brows === 'arched') return <>{[-1, 1].map((s) => <path key={s} d={`M${s * 82},-254 Q${s * 52},-292 ${s * 20},-266`} fill="none" stroke={P.brow} strokeWidth={14} strokeLinecap="round" />)}</>;
    return <>{[-1, 1].map((s) => <path key={s} d={`M${s * 86},-260 Q${s * 52},-280 ${s * 18},-264`} fill="none" stroke={P.brow} strokeWidth={20} strokeLinecap="round" />)}</>;
  };
  const nose = () => {
    if (l.nose === 'hook') return <path d="M-4,-262 Q-6,-226 -24,-196 Q-30,-176 -4,-174 Q16,-172 24,-186 Q12,-200 14,-262" fill={l.shade} stroke={P.ink} strokeWidth={7} strokeLinejoin="round" />;
    if (l.nose === 'big') return <path d="M-10,-262 Q-20,-220 -40,-200 Q-50,-168 -10,-162 Q10,-156 34,-164 Q58,-180 36,-206 Q20,-222 14,-262" fill={l.shade} stroke={P.ink} strokeWidth={7} strokeLinejoin="round" />;
    return <><path d="M-6,-250 Q-14,-216 -26,-202 Q-34,-176 -4,-170 Q10,-166 24,-172 Q44,-184 30,-206 Q18,-218 10,-250" fill={l.shade} stroke={P.ink} strokeWidth={7} strokeLinejoin="round" /><ellipse cx={-4} cy={-186} rx={9} ry={6} fill="#fff" opacity={0.2} /></>;
  };
  const stache = () => {
    const c = l.stacheColor;
    const st = {fill: c, stroke: P.ink, strokeWidth: 6, strokeLinejoin: 'round' as const};
    if (l.stache === 'walrus') return <path d="M0,-172 Q-50,-186 -86,-160 Q-104,-130 -92,-92 Q-70,-120 -40,-124 Q-14,-126 0,-136 Q14,-126 40,-124 Q70,-120 92,-92 Q104,-130 86,-160 Q50,-186 0,-172Z" {...st} />;
    if (l.stache === 'handlebar') return <path d="M0,-168 Q-40,-178 -70,-158 Q-90,-146 -96,-170 Q-104,-150 -84,-132 Q-56,-128 -30,-140 Q-10,-146 0,-148 Q10,-146 30,-140 Q56,-128 84,-132 Q104,-150 96,-170 Q90,-146 70,-158 Q40,-178 0,-168Z" {...st} />;
    if (l.stache === 'chevron') return <path d="M0,-170 Q-44,-180 -72,-156 L-66,-128 Q-34,-144 0,-142 Q34,-144 66,-128 L72,-156 Q44,-180 0,-170Z" {...st} />;
    return <path d="M0,-174 Q-50,-190 -84,-166 Q-102,-146 -90,-114 Q-74,-132 -44,-134 Q-18,-136 0,-148 Q18,-136 44,-134 Q74,-132 90,-114 Q102,-146 84,-166 Q50,-190 0,-174Z" {...st} />;
  };
  const mouthY = l.stache === 'walrus' ? -100 : -118;
  return (
    <g>
      {/* уши */}
      {[-1, 1].map((s) => <ellipse key={s} cx={s * (hw - 4)} cy={-226} rx={28} ry={40} fill={l.skin} stroke={P.ink} strokeWidth={O} />)}
      {/* шея */}
      <path d={`M${-nw},${chinY - 40} L${-nw - 4},30 L${nw + 4},30 L${nw},${chinY - 40}Z`} fill={l.shade} stroke={P.ink} strokeWidth={O} />
      {/* торс */}
      <path d={`M${-sw},90 Q${-sw},10 -110,0 L110,0 Q${sw},10 ${sw},90 L${sw + 30 + (l.belly ? 50 : 0)},${l.belly ? 600 : 700} Q${sw + 40},760 ${sw + 20},760 L${-sw - 20},760 Q${-sw - 40},760 ${-sw - 30 - (l.belly ? 50 : 0)},${l.belly ? 600 : 700}Z`} fill={l.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.stripes && [-3, -2, -1, 0, 1, 2, 3].map((i) => <path key={i} d={`M${i * 64},30 L${i * 74},760`} stroke={l.stripes} strokeWidth={10} opacity={0.6} />)}
      <path d={`M${sw * 0.6},60 Q${sw * 0.95},90 ${sw + 10},300 L${sw + 30},760 L${sw * 0.75},760Z`} fill={l.shirtShade} opacity={0.6} />
      {/* ворот */}
      <path d="M-70,0 L70,0 L20,170 L-20,170Z" fill={l.skin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.chestHair && <path d="M-24,70 q8,-10 14,0 q8,-10 14,0 q8,-10 14,0 M-16,110 q8,-10 14,0 q8,-10 14,0" fill="none" stroke={P.mustache} strokeWidth={5} strokeLinecap="round" />}
      <path d="M-62,6 Q-40,120 0,128 Q40,120 62,6" fill="none" stroke={P.goldDark} strokeWidth={12} strokeLinecap="round" />
      <path d="M-62,6 Q-40,120 0,128 Q40,120 62,6" fill="none" stroke={P.gold} strokeWidth={6} strokeDasharray="7 5" strokeLinecap="round" />
      <rect x={-9} y={124} width={18} height={26} rx={4} fill={P.gold} stroke={P.ink} strokeWidth={5} />
      <path d="M-76,-6 L-140,40 L-96,120 L-24,150Z" fill={l.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      <path d="M76,-6 L140,40 L96,120 L24,150Z" fill={l.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.vest && <>
        <path d={`M${-sw + 30},70 L-60,40 L-30,420 L${-sw - 4},640Z`} fill={l.vest} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
        <path d={`M${sw - 30},70 L60,40 L30,420 L${sw + 4},640Z`} fill={l.vest} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
        {[-1, 1].map((s) => [140, 220, 300, 380, 460].map((y) => <path key={s + '' + y} d={`M${s * 50},${y} l${s * 30},16 l${s * 30},-16 l${s * 30},16`} fill="none" stroke={P.ink} strokeWidth={3} opacity={0.35} />))}
      </>}
      {/* голова */}
      <path d={faces[l.face]} fill={l.skin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.stubble && <path d={`M${-hw + 14},-180 Q${-hw + 30},${chinY + 30} 0,${chinY + 8} Q${hw - 30},${chinY + 30} ${hw - 14},-180 Q${hw - 50},-140 0,-130 Q${-hw + 50},-140 ${-hw + 14},-180Z`} fill="#6E5A4E" opacity={0.28} />}
      {l.cheeks && <>{[-1, 1].map((s) => <ellipse key={s} cx={s * (hw - 52)} cy={-178} rx={26} ry={14} fill={P.terracotta} opacity={0.3} />)}</>}
      {/* седые виски */}
      {[-1, 1].map((s) => <path key={s} d={`M${s * (hw - 2)},-310 Q${s * (hw + 10)},-250 ${s * (hw - 16)},-206 L${s * (hw - 34)},-236 Q${s * (hw - 30)},-280 ${s * (hw - 36)},-310Z`} fill={P.hairGray} stroke={P.ink} strokeWidth={6} />)}
      {/* морщины-ухмылка */}
      {[-1, 1].map((s) => <path key={s} d={`M${s * 84},-196 q${s * 14},30 ${-s * 2},60`} fill="none" stroke={l.shade} strokeWidth={6} strokeLinecap="round" />)}
      {eye(-50, -1)}{eye(50, 1)}
      {brows()}
      <path d={`M-30,${mouthY} Q0,${mouthY + 12} 36,${mouthY - 10}`} fill="none" stroke={P.ink} strokeWidth={8} strokeLinecap="round" />
      {nose()}
      {stache()}
      {/* кепка */}
      <path d={`M-${hw + 18},-306 Q-${hw + 34},-430 -10,-448 Q${hw + 30},-446 ${hw + 26},-326 Q${hw + 26},-296 ${hw - 6},-292 L-${hw - 6},-292 Q-${hw + 24},-294 -${hw + 18},-306Z`} fill={l.cap} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.capCheck ? (
        [-120, -80, -40, 0, 40, 80, 120].map((x) => <path key={x} d={`M${x},-300 L${x * 0.5},-440`} stroke={l.capDark} strokeWidth={4} opacity={0.6} />)
          .concat([-410, -370, -330].map((y) => <path key={y} d={`M-${hw + 10},${y + 40} Q0,${y - 10} ${hw + 10},${y + 40}`} fill="none" stroke={l.capDark} strokeWidth={4} opacity={0.6} />))
      ) : (
        [-110, -50, 20, 80].map((x) => <path key={x} d={`M${x},-296 Q${x * 0.55},-374 -8,-440`} fill="none" stroke={l.capDark} strokeWidth={5} />)
      )}
      <circle cx={-8} cy={-444} r={11} fill={l.capDark} stroke={P.ink} strokeWidth={5} />
      <path d={`M-${hw + 10},-302 Q0,-270 ${hw + 10},-302 Q0,-244 -${hw + 10},-302Z`} fill={l.capDark} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {l.glassesOnCap && <g transform="translate(0,-360)">
        <rect x={-96} y={-26} width={82} height={52} rx={18} fill="#2E2A2E" stroke={P.ink} strokeWidth={6} />
        <rect x={14} y={-26} width={82} height={52} rx={18} fill="#2E2A2E" stroke={P.ink} strokeWidth={6} />
        <path d="M-14,-4 Q0,-14 14,-4" fill="none" stroke={P.ink} strokeWidth={6} />
        <path d="M-80,-14 l20,0 M30,-14 l20,0" stroke="#fff" strokeWidth={5} opacity={0.5} strokeLinecap="round" />
      </g>}
    </g>
  );
};

export const LOOKS: Look[] = [
  {name: 'А. Дядя Ашот', face: 'round', build: 1.25, neck: 1.45, skin: '#D9A07A', shade: '#BF8460', nose: 'bulb', stache: 'walrus', stacheColor: '#2E2019', brows: 'thick', eyes: 'sly', cheeks: true, cap: '#6B5A4A', capDark: '#54463A', shirt: '#E8DCC4', shirtShade: '#CDBFA4', belly: true},
  {name: 'Б. Хитрый лис', face: 'long', build: 0.95, neck: 1.0, skin: '#CF9670', shade: '#B27B58', nose: 'hook', stache: 'handlebar', stacheColor: '#2A1D17', brows: 'arched', eyes: 'sly', cap: '#5E6670', capDark: '#474E57', shirt: '#B8C6CF', shirtShade: '#97A8B3', stripes: '#7F95A5'},
  {name: 'В. Таксист со стажем', face: 'square', build: 1.35, neck: 1.6, skin: '#C98F68', shade: '#AC7553', nose: 'big', stache: 'bushy', stacheColor: '#3A2E28', brows: 'uni', eyes: 'round', stubble: true, cap: '#3F3A36', capDark: '#2C2825', shirt: '#9A4A3C', shirtShade: '#7E3A2F', glassesOnCap: true, chestHair: true},
  {name: 'Г. Добряк в жилетке', face: 'oval', build: 1.15, neck: 1.3, skin: '#DDA884', shade: '#C38D69', nose: 'bulb', stache: 'chevron', stacheColor: '#4A3A30', brows: 'thick', eyes: 'smile', cheeks: true, cap: '#8A6A4A', capDark: '#6C5238', capCheck: true, shirt: '#F1E6D0', shirtShade: '#D8CBB0', vest: '#7E8A5E'},
  {name: 'Д. Ашот-бизнесмен', face: 'square', build: 1.2, neck: 1.4, skin: '#D39B74', shade: '#B78059', nose: 'hook', stache: 'walrus', stacheColor: '#262019', brows: 'thick', eyes: 'sly', stubble: true, cap: '#2F3B4A', capDark: '#222B36', shirt: '#2E2B33', shirtShade: '#1F1D23', chestHair: true, glassesOnCap: true},
];
