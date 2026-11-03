import React from 'react';
import {P} from '../palette';
import {lerp, clamp} from '../lib';

// Ашот: начало координат — основание шеи. Голова ~290×330, центр головы (0,-215).
// Слои: дальнее ухо, шея, торс (рубашка, ворот, цепочка, ремень), левая рука на руле,
// голова (волосы, кепка-восьмиклинка, лицо), правая рука (поза rest/up/palm).

const O = 9; // толщина контура
export type ArmPose = 'rest' | 'up' | 'palm';
export type AshotState = {
  t: number;
  turn: number;      // 0 — смотрит вперёд-влево в зеркало, 1 — повернулся к пассажиру/камере
  browL: number;     // подъём левой брови 0..1
  browR: number;
  blink: number;     // 0..1
  wink: number;      // 0..1 подмигивание (правый глаз)
  mouth: number;     // 0..3
  smirk: number;     // 0..1 ухмылка
  look: [number, number]; // направление зрачков -1..1
  arm: {from: ArmPose; to: ArmPose; k: number};
  poke?: number;     // 0..1 тычок пальцем вперёд
  noRightArm?: boolean; // правую руку рисует сцена сама (например, тянется в камеру)
};

const ARM: Record<ArmPose, {e: [number, number]; h: [number, number]; hand: 'fist' | 'finger' | 'palm'}> = {
  rest: {e: [300, 330], h: [250, 500], hand: 'fist'},
  up: {e: [330, 250], h: [345, 20], hand: 'finger'},
  palm: {e: [360, 170], h: [520, 90], hand: 'palm'},
};

const limb = (pts: [number, number][], w: number, fill: string) => {
  const d = 'M' + pts.map((p) => p.join(',')).join(' L');
  return (
    <>
      <path d={d} stroke={P.ink} strokeWidth={w + O * 2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={d} stroke={fill} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </>
  );
};

const Hand: React.FC<{x: number; y: number; kind: 'fist' | 'finger' | 'palm'; rot?: number}> = ({x, y, kind, rot = 0}) => (
  <g transform={`translate(${x},${y}) rotate(${rot})`} stroke={P.ink} strokeWidth={O} strokeLinejoin="round">
    {kind === 'palm' ? (
      <>
        <path d="M-58,-6 Q-60,34 -10,40 Q48,42 62,6 L70,-14 Q74,-26 62,-26 L50,-12 Q30,-30 -10,-28 Q-50,-26 -58,-6Z" fill={P.skin} />
        {[-34, -12, 10, 32].map((fx, i) => (
          <path key={i} d={`M${fx},-24 q-4,-26 8,-28 q12,2 8,28`} fill={P.skin} />
        ))}
        <path d="M-30,10 Q0,22 34,8" fill="none" stroke={P.skinShade} strokeWidth={5} />
      </>
    ) : (
      <>
        {kind === 'finger' && <rect x={-46} y={-120} width={32} height={104} rx={16} fill={P.skin} />}
        <rect x={-46} y={-40} width={92} height={80} rx={34} fill={P.skin} />
        <path d="M-40,-6 Q-10,6 30,-8" fill="none" stroke={P.skinShade} strokeWidth={5} />
        <path d="M-48,8 Q-78,-6 -66,-34 Q-46,-38 -36,-10" fill={P.skinLight} />
      </>
    )}
  </g>
);

export const AshotEyes: React.FC<{s: AshotState; dx: number}> = ({s, dx}) => {
  const eye = (cx: number, b: number, browUp: number, browSide: 1 | -1) => {
    const open = clamp(1 - b);
    const ry = 21 * open + 1.5;
    const px = s.look[0] * 9, py = s.look[1] * 6;
    return (
      <g>
        <ellipse cx={cx} cy={-240} rx={25} ry={ry} fill="#FFF8EC" stroke={P.ink} strokeWidth={6} />
        {open > 0.25 && <circle cx={cx + px} cy={-238 + py} r={10.5} fill={P.ink} />}
        {open > 0.25 && <circle cx={cx + px + 3.5} cy={-242 + py} r={3.2} fill="#fff" />}
        {/* хитрое верхнее веко */}
        <path d={`M${cx - 29},${-246 - 6 * open} Q${cx},${-262 - 4 * open + (1 - open) * 18} ${cx + 29},${-246 - 6 * open} L${cx + 29},${-268} L${cx - 29},${-268}Z`} fill={P.skin} />
        <path d={`M${cx - 28},${-246 - 4 * open} Q${cx},${-258 - 2 * open + (1 - open) * 16} ${cx + 28},${-246 - 4 * open}`} fill="none" stroke={P.ink} strokeWidth={6} strokeLinecap="round" />
        {/* бровь */}
        <path
          d={`M${cx - 34 * browSide},${-278 - browUp * 30 + 6} Q${cx},${-298 - browUp * 34} ${cx + 34 * browSide},${-282 - browUp * 22 - 2}`}
          fill="none" stroke={P.brow} strokeWidth={17} strokeLinecap="round"
        />
      </g>
    );
  };
  return (
    <g transform={`translate(${dx},22)`}>
      {eye(-52, s.blink, s.browL, 1)}
      {eye(48, Math.max(s.blink, s.wink), s.browR, -1)}
    </g>
  );
};

export const Ashot: React.FC<{s: AshotState}> = ({s}) => {
  const dx = lerp(-38, 22, s.turn);
  const sq = 1 - Math.sin(s.turn * Math.PI) * 0.05; // лёгкое сжатие головы в середине поворота
  const a0 = ARM[s.arm.from], a1 = ARM[s.arm.to];
  const k = s.arm.k;
  const eR: [number, number] = [lerp(a0.e[0], a1.e[0], k), lerp(a0.e[1], a1.e[1], k) - Math.sin(k * Math.PI) * 40];
  let hR: [number, number] = [lerp(a0.h[0], a1.h[0], k), lerp(a0.h[1], a1.h[1], k)];
  const poke = s.poke || 0;
  hR = [hR[0] + poke * 22, hR[1] - poke * 14];
  const handKind = k < 0.5 ? a0.hand : a1.hand;
  const mouthY = -138;
  const sm = s.smirk;

  const mouth = () => {
    if (s.mouth === 0) {
      return <path d={`M${-34},${mouthY + 2} Q${0},${mouthY + 12 - sm * 4} ${36},${mouthY - 4 - sm * 12}`} fill="none" stroke={P.ink} strokeWidth={8} strokeLinecap="round" />;
    }
    const W = [0, 24, 32, 26][s.mouth], H = [0, 10, 22, 30][s.mouth];
    return (
      <g>
        <ellipse cx={2 + sm * 4} cy={mouthY + H * 0.45} rx={W} ry={H} fill="#5A1F1A" stroke={P.ink} strokeWidth={7} />
        <ellipse cx={4 + sm * 4} cy={mouthY + H * 0.9} rx={W * 0.55} ry={H * 0.4} fill="#C9665A" />
      </g>
    );
  };

  return (
    <g>
      {/* уши (за головой, одно выглядывает в зависимости от поворота) */}
      {[-1, 1].map((side) => (
        <g key={side} transform={`translate(${side * 132 - dx * 1.05},-222)`}>
          <ellipse rx={30} ry={42} fill={P.skin} stroke={P.ink} strokeWidth={O} />
          <path d={`M${side * 6},-18 q${side * 12},18 0,34`} fill="none" stroke={P.skinShade} strokeWidth={6} />
        </g>
      ))}
      {/* шея */}
      <path d="M-88,-100 L-92,30 L92,30 L88,-100Z" fill={P.skinShade} stroke={P.ink} strokeWidth={O} />

      {/* торс */}
      <path d="M-250,70 Q-250,10 -120,0 L120,0 Q250,10 262,80 L300,900 L-300,900Z" fill={P.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      <path d="M150,60 Q230,90 250,300 L270,900 L200,900Z" fill={P.shirtShade} />
      {/* расстёгнутый ворот: кожа */}
      <path d="M-70,0 L70,0 L18,170 L-18,170Z" fill={P.skin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      <path d="M-24,60 q8,-10 14,0 q8,-10 14,0 q8,-10 14,0 M-16,96 q8,-10 14,0 q8,-10 14,0" fill="none" stroke={P.mustache} strokeWidth={5} strokeLinecap="round" />
      {/* золотая цепочка */}
      <path d="M-62,6 Q-40,120 0,128 Q40,120 62,6" fill="none" stroke={P.goldDark} strokeWidth={11} strokeLinecap="round" />
      <path d="M-62,6 Q-40,120 0,128 Q40,120 62,6" fill="none" stroke={P.gold} strokeWidth={6} strokeLinecap="round" strokeDasharray="7 5" />
      <rect x={-9} y={126} width={18} height={24} rx={4} fill={P.gold} stroke={P.ink} strokeWidth={5} />
      {/* воротник */}
      <path d="M-76,-6 L-140,40 L-96,120 L-24,150Z" fill={P.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      <path d="M76,-6 L140,40 L96,120 L24,150Z" fill={P.shirt} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {/* пуговицы */}
      {[200, 300, 400].map((y) => <circle key={y} cx={4} cy={y} r={8} fill={P.beige} stroke={P.ink} strokeWidth={4} />)}
      {/* ремень безопасности */}
      <path d="M-150,40 L170,820" stroke={P.ink} strokeWidth={66} strokeLinecap="butt" />
      <path d="M-150,40 L170,820" stroke="#6B6560" strokeWidth={50} strokeLinecap="butt" />

      {/* левая рука на руле */}
      {limb([[-215, 70], [-300, 250]], 92, P.shirt)}
      <ellipse cx={-300} cy={250} rx={56} ry={34} fill={P.shirtShade} stroke={P.ink} strokeWidth={O} transform="rotate(-20,-300,250)" />
      {limb([[-300, 260], [-185, 288]], 62, P.skin)}

      {/* голова */}
      <g transform={`translate(0,-215) scale(${sq},1) translate(0,215)`}>
        {/* волосы сзади-по бокам (седые) */}
        <path d={`M${-150 - dx * 0.3},-290 Q${-168 - dx * 0.3},-200 ${-118 - dx * 0.2},-150 L${118 - dx * 0.2},-150 Q${168 - dx * 0.3},-200 ${150 - dx * 0.3},-290Z`} fill={P.hairGray} stroke={P.ink} strokeWidth={O} />
        {/* голова */}
        <path d="M-140,-270 Q-146,-384 0,-388 Q146,-384 140,-270 L142,-150 Q140,-86 92,-78 L-92,-78 Q-140,-86 -142,-150Z" fill={P.skin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
        {/* тень со стороны, куда он не смотрит */}
        <path d={`M${dx < 0 ? 80 : -80},-300 Q${dx < 0 ? 150 : -150},-210 ${dx < 0 ? 60 : -60},-92 Q${dx < 0 ? 130 : -130},-150 ${dx < 0 ? 136 : -136},-260Z`} fill={P.skinShade} opacity={0.55} />
        <path d="M-126,-180 Q-112,-92 0,-86 Q112,-92 126,-180 Q90,-140 0,-132 Q-90,-140 -126,-180Z" fill="#5E4A3E" opacity={0.3} />
        {/* виски — седые с тёмными прядями */}
        {[-1, 1].map((side) => (
          <path key={side} d={`M${side * 138 - dx * 0.25},-300 Q${side * 150 - dx * 0.25},-240 ${side * 124 - dx * 0.25},-198 L${side * 108 - dx * 0.25},-228 Q${side * 112 - dx * 0.25},-270 ${side * 106 - dx * 0.25},-300Z`} fill={P.hairGray} stroke={P.ink} strokeWidth={6} />
        ))}
        <path d={`M${-130 - dx * 0.25},-282 l10,40 M${132 - dx * 0.25},-282 l-10,40`} stroke={P.hairDark} strokeWidth={5} />

        {/* лицо */}
        <g>
          {/* морщинки-ухмылка */}
          <path d={`M${dx - 82},-190 q-12,30 2,56`} fill="none" stroke={P.skinShade} strokeWidth={6} strokeLinecap="round" opacity={0.4 + sm * 0.6} />
          <path d={`M${dx + 86},-196 q16,28 -2,60`} fill="none" stroke={P.skinShade} strokeWidth={6} strokeLinecap="round" opacity={0.4 + sm * 0.6} />
          <AshotEyes s={s} dx={dx} />
          <g transform={`translate(${dx},0)`}>
            {mouth()}
            {/* нос */}
            <path d="M-4,-250 Q-2,-224 -24,-192 Q-34,-170 -6,-166 Q12,-162 26,-172 Q34,-184 22,-196 Q12,-214 14,-250" fill={P.skinShade} stroke={P.ink} strokeWidth={7} strokeLinejoin="round" />
            <ellipse cx={-4} cy={-182} rx={9} ry={6} fill={P.skinLight} opacity={0.7} />
            {/* густые усы */}
            <path
              d={`M-6,-170 Q-40,-180 -70,-160 Q-92,-146 -84,${-118 + sm * 2} Q-66,-134 -40,-138 Q-16,-140 2,-150 Q22,-140 44,-140 Q70,${-138 - sm * 6} 88,${-124 - sm * 8} Q96,-150 74,-164 Q44,-182 8,-170Z`}
              fill={P.mustache} stroke={P.ink} strokeWidth={6} strokeLinejoin="round"
            />
            <path d="M-50,-158 l-10,10 M-28,-162 l-6,12 M30,-162 l6,12 M54,-156 l10,10" stroke="#4A3A30" strokeWidth={4} strokeLinecap="round" />
          </g>
        </g>

        {/* кепка-восьмиклинка */}
        <g>
          <path d={`M-160,-300 Q-178,-420 ${-20 + dx * 0.4},-440 Q${150 + dx * 0.3},-438 168,-322 Q170,-292 140,-286 L-140,-286 Q-166,-288 -160,-300Z`} fill={P.cap} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
          {[-110, -50, 20, 80].map((x, i) => (
            <path key={i} d={`M${x + dx * 0.3},-292 Q${(x + dx * 0.3) * 0.55},-370 ${-8 + dx * 0.4},-432`} fill="none" stroke={P.capDark} strokeWidth={5} />
          ))}
          <path d={`M-150,-330 Q-120,-410 -20,-428`} fill="none" stroke={P.capLight} strokeWidth={10} strokeLinecap="round" opacity={0.6} />
          <circle cx={-8 + dx * 0.4} cy={-436} r={11} fill={P.capDark} stroke={P.ink} strokeWidth={5} />
          <g transform={`translate(${dx * 0.9},-352)`}>
            <rect x={-96} y={-24} width={82} height={50} rx={18} fill="#2E2A2E" stroke={P.ink} strokeWidth={6} />
            <rect x={14} y={-24} width={82} height={50} rx={18} fill="#2E2A2E" stroke={P.ink} strokeWidth={6} />
            <path d="M-14,-4 Q0,-14 14,-4" fill="none" stroke={P.ink} strokeWidth={6} />
            <path d="M-80,-12 l20,0 M30,-12 l20,0" stroke="#fff" strokeWidth={5} opacity={0.5} strokeLinecap="round" />
          </g>
          {/* козырёк */}
          <path d={`M${-150 + dx * 1.4},-298 Q${dx * 1.6},-272 ${150 + dx * 1.4},-300 Q${dx * 1.6},-250 ${-150 + dx * 1.4},-298Z`} fill={P.capDark} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
        </g>
      </g>

      {/* правая рука */}
      {!s.noRightArm && <>
      {limb([[215, 70], eR], 92, P.shirt)}
      <ellipse cx={eR[0]} cy={eR[1]} rx={54} ry={34} fill={P.shirtShade} stroke={P.ink} strokeWidth={O} />
      {limb([eR, hR], 62, P.skin)}
      <Hand x={hR[0]} y={hR[1]} kind={handKind} rot={handKind === 'finger' ? 8 - poke * 30 : handKind === 'palm' ? -8 : 0} />
      </>}
    </g>
  );
};
