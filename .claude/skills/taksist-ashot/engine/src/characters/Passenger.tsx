import React from 'react';
import {P} from '../palette';
import {clamp, lerp} from '../lib';

// Пассажир: молодой парень в худи на заднем сиденье. Начало координат — основание шеи.
export type PassengerState = {
  blink: number; mouth: number; shock: number; worry: number; look: [number, number]; sweat: number;
};
const O = 7;

export const Passenger: React.FC<{s: PassengerState}> = ({s}) => {
  const sh = s.shock;
  const eye = (cx: number) => {
    const open = clamp(1 - s.blink * (1 - sh));
    const rx = 17 + sh * 7, ry = (17 + sh * 9) * open + 1.5;
    const pr = lerp(8, 5, sh);
    return (
      <g>
        <ellipse cx={cx} cy={-122} rx={rx} ry={ry} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
        {open > 0.3 && <circle cx={cx + s.look[0] * 6} cy={-121 + s.look[1] * 5} r={pr} fill={P.ink} />}
        {open > 0.3 && <circle cx={cx + s.look[0] * 6 + 2.5} cy={-124 + s.look[1] * 5} r={2.2} fill="#fff" />}
      </g>
    );
  };
  const by = -158 - sh * 22 - s.worry * 8;
  const mouth = () => {
    if (sh > 0.5 && s.mouth === 0) return <ellipse cx={0} cy={-62} rx={14} ry={18} fill="#5A1F1A" stroke={P.ink} strokeWidth={5} />;
    if (s.mouth === 0) return <path d={`M-18,-64 Q0,${-58 - s.worry * -6} 18,-64`} fill="none" stroke={P.ink} strokeWidth={6} strokeLinecap="round" />;
    const W = [0, 15, 20, 18][s.mouth] + sh * 4, H = [0, 7, 14, 20][s.mouth] + sh * 8;
    return (
      <g>
        <ellipse cx={0} cy={-64 + H * 0.4} rx={W} ry={H} fill="#5A1F1A" stroke={P.ink} strokeWidth={5} />
        <ellipse cx={1} cy={-64 + H * 0.85} rx={W * 0.5} ry={H * 0.35} fill="#C9665A" />
      </g>
    );
  };
  return (
    <g>
      {/* капюшон за шеей */}
      <path d="M-120,-10 Q-130,-70 -60,-60 L60,-60 Q130,-70 120,-10 Q60,30 0,26 Q-60,30 -120,-10Z" fill={P.hoodieShade} stroke={P.ink} strokeWidth={O} />
      {/* шея */}
      <rect x={-36} y={-60} width={72} height={70} fill={P.pSkinShade} stroke={P.ink} strokeWidth={O} />
      {/* торс */}
      <path d="M-190,60 Q-180,0 -70,-4 L70,-4 Q180,0 190,60 L215,420 L-215,420Z" fill={P.hoodie} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      <path d="M-60,-2 Q0,40 60,-2" fill="none" stroke={P.ink} strokeWidth={O} />
      <path d="M-26,24 l-6,90 M26,24 l6,90" stroke={P.cream} strokeWidth={6} strokeLinecap="round" />
      <path d="M-120,250 L120,250 L110,330 L-110,330Z" fill={P.hoodieShade} stroke={P.ink} strokeWidth={5} />
      {/* уши */}
      <ellipse cx={-94} cy={-112} rx={18} ry={26} fill={P.pSkin} stroke={P.ink} strokeWidth={O} />
      <ellipse cx={94} cy={-112} rx={18} ry={26} fill={P.pSkin} stroke={P.ink} strokeWidth={O} />
      {/* голова */}
      <path d="M-92,-150 Q-96,-230 0,-232 Q96,-230 92,-150 L88,-96 Q74,-30 0,-26 Q-74,-30 -88,-96Z" fill={P.pSkin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {/* щёки при шоке бледнеют, при волнении румянец */}
      <ellipse cx={-52} cy={-82} rx={16} ry={9} fill={P.terracotta} opacity={0.25 + s.worry * 0.2} />
      <ellipse cx={52} cy={-82} rx={16} ry={9} fill={P.terracotta} opacity={0.25 + s.worry * 0.2} />
      {/* волосы: небрежная чёлка */}
      <path d="M-98,-150 Q-112,-250 -10,-252 Q100,-262 104,-160 Q90,-196 60,-200 Q50,-176 20,-188 Q0,-170 -28,-190 Q-52,-170 -70,-196 Q-90,-180 -98,-150Z" fill={P.pHair} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
      {eye(-36)}
      {eye(36)}
      <path d={`M-58,${by + 8 + s.worry * 6} Q-36,${by - 6} -16,${by + 4 - s.worry * 6}`} fill="none" stroke={P.pHair} strokeWidth={8} strokeLinecap="round" />
      <path d={`M16,${by + 4 - s.worry * 6} Q36,${by - 6} 58,${by + 8 + s.worry * 6}`} fill="none" stroke={P.pHair} strokeWidth={8} strokeLinecap="round" />
      <path d="M-4,-112 Q-12,-90 -2,-84 Q6,-82 10,-88" fill="none" stroke={P.pSkinShade} strokeWidth={5} strokeLinecap="round" />
      {mouth()}
      {/* капля пота */}
      {s.sweat > 0.01 && (
        <path transform={`translate(86,${-190 + s.sweat * 40}) scale(${s.sweat})`} d="M0,-18 Q12,0 8,8 Q0,16 -8,8 Q-12,0 0,-18Z" fill="#BFE0F2" stroke={P.ink} strokeWidth={4} />
      )}
    </g>
  );
};
