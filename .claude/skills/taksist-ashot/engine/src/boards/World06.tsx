import React from 'react';
import {P} from '../palette';
import {RiderFigure, ZINA, EMO, Emotion} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';
import {Cam, Note} from './World';
import {textW} from './World05';
import {CabinBack} from '../scene/Cabin';

// Сцены серии 6 «Звонок из службы безопасности».
// Структура (решение автора 2026-11-07): хук-разговор в такси → объясняющие картинки → один раз такси посередине → картинки → финал в такси.
// Реплики Зины в объясняющей части звучат поверх картинок через мини-аватар в углу.
// Правила как в World.tsx: 1080×1920, lt — сек от начала врезки, dur — длина, важное в зоне x 56..922, y 250..1300.

const F = 'Rubik';
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);
export const ZIN = ZINA[0];
const em = (e: Partial<Emotion>): Emotion => ({...EMO.calm, ...e});
export const BTN_COLORS = ['#C8553D', '#EDB447', '#8E6FB8'];
const BTN_NAMES = ['СТРАХ', 'СПЕШКА', 'СЕКРЕТ'];

const Plate: React.FC<{x: number; y: number; text: string; s?: number; rot?: number; fill?: string; color?: string; size?: number; maxW?: number}> = ({x, y, text, s = 1, rot = 0, fill = P.terracotta, color = P.cream, size = 64, maxW = 860}) => {
  const tw = textW(text, size), pad = size * 0.9;
  const w = Math.min(maxW, tw + pad * 2), fit = tw > w - pad * 2;
  return (
    <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
      <rect x={-w / 2} y={-size * 0.95} width={w} height={size * 1.9} rx={size * 0.5} fill={fill} stroke={P.ink} strokeWidth={8} />
      <text y={size * 0.36} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={size} fill={color} {...(fit ? {textLength: w - pad * 2, lengthAdjust: 'spacingAndGlyphs' as const} : {})}>{text}</text>
    </g>
  );
};
const Caption: React.FC<{text: string; y?: number; o?: number}> = ({text, y = 1260, o = 1}) => (
  <text x={540} y={y} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={30} fill={P.ink} opacity={0.7 * o}>{text}</text>
);

// счётчик кнопок в углу
export const BtnBadge: React.FC<{n: number}> = ({n}) => (
  <g transform="translate(790,300)">
    <rect x={-150} y={-56} width={300} height={112} rx={30} fill={P.ink} opacity={0.9} stroke={n ? BTN_COLORS[n - 1] : P.cream} strokeWidth={7} />
    <text y={-10} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={28} fill={P.cream}>КНОПКА</text>
    <text y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={n ? BTN_COLORS[n - 1] : P.cream}>{n}/3</text>
  </g>
);

// мини-аватар Зины в кружке
export const MiniZina: React.FC<{x?: number; y?: number; s?: number; e?: Partial<Emotion>; tape?: boolean}> = ({x = 190, y = 1120, s = 1, e = {}, tape}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <circle r={130} fill={P.cream} stroke={P.ink} strokeWidth={8} />
    <clipPath id="miniZn"><circle r={126} /></clipPath>
    <g clipPath="url(#miniZn)"><g transform="translate(0,175) scale(0.82)"><RiderFigure r={ZIN} e={em(e)} /></g></g>
    {tape && <g transform="translate(0,58) rotate(-6)"><rect x={-62} y={-20} width={124} height={40} rx={6} fill="#E9DCC0" stroke={P.ink} strokeWidth={5} /><text y={12} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={26} fill={P.terracotta}>ТСС</text></g>}
  </g>
);

// телефон: корпус + экран (children рисуются в координатах экрана, центр 0,0, экран 368×688)
const Phone: React.FC<{x: number; y: number; s?: number; rot?: number; children?: React.ReactNode; dark?: boolean}> = ({x, y, s = 1, rot = 0, children, dark}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
    <rect x={-184} y={-344} width={368} height={688} rx={38} fill={dark ? '#2A2630' : P.cream} />
    {children}
  </g>
);
// экран входящего звонка «БАНК · Служба безопасности»
const CallScreen: React.FC<{secs: number; label?: string; hang?: number}> = ({secs, label = 'БАНК', hang = 0}) => {
  const mm = Math.floor(secs / 60), ss = Math.floor(secs % 60);
  return (
    <g>
      <circle cy={-200} r={84} fill={hang ? '#8A7A70' : P.sage} stroke={P.cream} strokeWidth={6} />
      <text y={-176} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>{label === 'БАНК' ? 'Б' : '?'}</text>
      <text y={-50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={label === 'БАНК' ? 66 : 90} fill={P.cream}>{label}</text>
      <text y={0} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={32} fill="#C9BFB4">Служба безопасности</text>
      <text y={110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={hang ? 44 : 76} fill={hang ? P.terracotta : P.mustard}>{hang ? 'ЗВОНОК ЗАВЕРШЁН' : `${mm}:${String(ss).padStart(2, '0')}`}</text>
      <g transform="translate(0,250)"><circle r={56} fill={P.terracotta} stroke={P.cream} strokeWidth={5} /><path d="M-26,6 Q0,-16 26,6" stroke={P.cream} strokeWidth={12} fill="none" strokeLinecap="round" /></g>
    </g>
  );
};

// ---------- ТАКСИ: Зина на заднем сиденье крупно ----------
export const ShotZina: React.FC<{lt?: number; e?: Partial<Emotion>; lean?: number; phone?: 'ear' | 'forward' | 'none'; door?: boolean}> = ({lt = 1, e = {}, lean = 0, phone = 'none', door}) => {
  const tug = door ? Math.sin(lt * 18) * 10 * clamp(lt / 0.3) : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={lt} /></g>
      {door && (
        <g transform={`translate(${960 + tug},1180)`}>
          <rect x={-40} y={-300} width={140} height={600} rx={20} fill={P.seatDark} stroke={P.ink} strokeWidth={8} />
          <rect x={-30} y={-30} width={70} height={36} rx={14} fill="#B9C0C8" stroke={P.ink} strokeWidth={6} />
        </g>
      )}
      <g transform={`translate(${540 + lean * 120},${1300 - Math.abs(lean) * 60}) scale(1.9) rotate(${lean * 6})`}><RiderFigure r={ZIN} e={em(e)} /></g>
      {phone === 'ear' && <g transform="translate(700,1010) rotate(14) scale(0.32)"><rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={14} /></g>}
      {phone === 'ear' && <path d="M560,1120 Q620,1080 690,1060" stroke={ZIN.skin} strokeWidth={70} strokeLinecap="round" fill="none" />}
      {phone === 'forward' && <Phone x={720} y={1080} s={0.5} rot={-10}><CallScreen secs={47 * 60 + 12 + lt} /></Phone>}
      {door && <Plate x={540} y={460} text="ВЫЙДУ ТУТ!" s={pop(after(lt, 0.2, 0.4))} rot={-4} size={70} />}
    </svg>
  );
};

// ---------- ХУК: телефон крупно, 47:12 тикает ----------
export const SceneCall: React.FC<{lt: number; dur: number}> = ({lt, dur}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#2A2034" />
    <Cam k={clamp(lt / dur)} z0={1.15} z1={1.3} cy={820}>
      <Phone x={540} y={820} s={1.15} rot={-3} dark><CallScreen secs={47 * 60 + 12 + lt} /></Phone>
      <path d={`M${lerp(1180, 900, easeOut(after(lt, 0.2, 0.5)))},620 q-140,40 -180,180 q-20,80 40,120`} fill={ZIN.skin} stroke={P.ink} strokeWidth={8} opacity={0.95} />
    </Cam>
    <Plate x={540} y={1250} text="47 МИНУТ С «БАНКОМ»" s={pop(after(lt, 0.35, 0.4))} rot={-3} fill={P.mustard} color={P.ink} size={60} />
  </svg>
);

// ---------- заставка кнопки: «КНОПКА n/3» + название ----------
export const SceneBtnChapter: React.FC<{lt: number; dur: number; n: number}> = ({lt, n}) => {
  const fill = easeOut(after(lt, 0.05, 0.3)), c = BTN_COLORS[n - 1];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <circle cx={540} cy={760} r={1400 * fill} fill={c} />
      <g transform={`translate(540,700) scale(${pop(after(lt, 0, 0.45))})`}>
        <text y={-150} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.ink}>КНОПКА</text>
        <text y={160} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={330} fill={P.cream} stroke={P.ink} strokeWidth={12}>{n}/3</text>
      </g>
      {/* большая кнопка, которую давят */}
      <g transform={`translate(540,${1140 + Math.sin(clamp(after(lt, 0.5, 0.25)) * Math.PI) * 26})`}>
        <ellipse cy={40} rx={260} ry={70} fill={P.ink} />
        <rect x={-250} y={-60} width={500} height={110} rx={50} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={76} fill={c}>{BTN_NAMES[n - 1]}</text>
      </g>
      <g transform={`translate(${lerp(1100, 700, easeOut(after(lt, 0.25, 0.3)))},${lerp(1300, 1060, easeOut(after(lt, 0.25, 0.3)))}) rotate(-30)`}>
        <rect x={-30} y={-140} width={60} height={160} rx={30} fill={P.pSkin} stroke={P.ink} strokeWidth={7} />
      </g>
    </svg>
  );
};

// ---------- 1/3 страх: телефон-рупор «НА ВАС КРЕДИТ!», лампочка ДУМАТЬ гаснет ----------
export const SceneFear: React.FC<{lt: number; dur: number; lampAt: number}> = ({lt, dur, lampAt}) => {
  const off = after(lt, lampAt, 0.2);
  const wav = (lt * 2) % 1;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#F0D3C6" />
      <Cam k={clamp(lt / dur)} z1={1.06}>
        <g transform={`translate(330,640) rotate(-12) scale(${1 + Math.sin(lt * 20) * 0.02})`}>
          <path d="M-120,-80 L120,-160 L120,160 L-120,80Z" fill={P.terracotta} stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
          <rect x={-200} y={-80} width={90} height={160} rx={16} fill="#1D1A1F" stroke={P.ink} strokeWidth={9} />
          {[0, 1, 2].map((i) => <path key={i} d={`M${160 + ((wav + i / 3) % 1) * 140},-140 q60,140 0,280`} fill="none" stroke={P.terracotta} strokeWidth={10} opacity={1 - ((wav + i / 3) % 1)} />)}
        </g>
        <Plate x={470} y={470} text="НА ВАС КРЕДИТ!" s={pop(after(lt, 0.2, 0.4))} rot={6} size={74} />
        {/* Зина и лампочки */}
        <g transform="translate(700,1000)">
          <g transform="translate(0,-330)">
            <circle r={70} fill={off > 0.5 ? '#8A7A70' : '#FFE38A'} stroke={P.ink} strokeWidth={7} />
            <rect x={-28} y={64} width={56} height={40} fill="#B9C0C8" stroke={P.ink} strokeWidth={6} />
            <Plate x={0} y={-120} text={off > 0.5 ? 'СЛУШАТЬСЯ' : 'ДУМАТЬ'} s={off > 0.5 ? pop(after(lt, lampAt, 0.4)) : 1} fill={off > 0.5 ? P.terracotta : P.sage} size={44} />
          </g>
          <g transform="scale(1.15)"><RiderFigure r={ZIN} e={em({shock: 0.8, worry: 1, mouth: 2, sweat: off})} /></g>
        </g>
      </Cam>
      <BtnBadge n={1} />
    </svg>
  );
};

// ---------- шашки на чужую машину: «БАНК» → «???» ----------
export const SceneShashki: React.FC<{lt: number; dur: number; capAt: number; swapAt: number; talk?: number}> = ({lt, dur, capAt, swapAt, talk = 0}) => {
  const drop = easeOut(after(lt, capAt, 0.35)), sw = after(lt, swapAt, 0.25);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#F6E3B8" />
      <rect y={1150} width={1080} height={770} fill="#8C8178" />
      <Cam k={clamp(lt / dur)} z1={1.08} cy={1000}>
        {/* ржавая машина */}
        <g transform="translate(560,1060)">
          <path d="M-330,40 L-300,-60 L-170,-80 L-110,-170 L130,-170 L200,-80 L320,-60 L340,40 Z" fill="#9A6A4A" stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
          <path d="M-90,-150 L110,-150 L160,-84 L-140,-84Z" fill="#9EC2D6" stroke={P.ink} strokeWidth={7} />
          {[[-120, 0], [80, -30], [-240, 10]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={14} fill="#6E3E25" opacity={0.7} />)}
          {[-210, 210].map((x) => <g key={x}><circle cx={x} cy={44} r={62} fill="#2A2421" stroke={P.ink} strokeWidth={8} /><circle cx={x} cy={44} r={24} fill="#8A8A8A" /></g>)}
          {/* шашки падают на крышу */}
          <g transform={`translate(10,${lerp(-560, -200, drop)})`}>
            <rect x={-110} y={-40} width={220} height={60} rx={10} fill={P.cream} stroke={P.ink} strokeWidth={7} />
            {Array.from({length: 8}, (_, i) => <rect key={i} x={-110 + i * 27.5} y={(i % 2) * 30 - 40} width={27.5} height={30} fill={P.ink} />)}
          </g>
        </g>
        <Phone x={820} y={660} s={0.55} rot={8} dark><CallScreen secs={47 * 60 + 30 + lt} label={sw > 0.5 ? '???' : 'БАНК'} /></Phone>
      </Cam>
      {drop >= 1 && <Plate x={360} y={720} text="ЛЮБОЙ МОЖЕТ" s={pop(after(lt, capAt + 0.3, 0.4))} rot={-5} fill={P.ink} size={64} />}
      <MiniZina x={190} y={360} s={0.85} e={{worry: 1 - sw, shock: sw, mouth: talk > 0.1 ? 2 : 0}} />
      <BtnBadge n={1} />
    </svg>
  );
};

// ---------- 2/3 спешка: таймер 10:00, склейки в такт тиканью, контакт «Сынок» ----------
export const SceneTimer: React.FC<{lt: number; dur: number; sonAt: number}> = ({lt, dur, sonAt}) => {
  const left = Math.max(0, 600 - lt * 9), tick = lt % 1, beat = Math.floor(lt);
  const bgs = ['#F6E3B8', '#EDB447', '#F3D58A', '#E8A93A'];
  const son = after(lt, sonAt, 0.35);
  const push = son > 0 ? Math.sin(clamp((lt - sonAt - 0.4) / 0.6) * Math.PI) : 0;
  const z = 1 + (1 - tick) * 0.06;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={bgs[beat % 4]} />
      <g transform={`translate(540,640) scale(${z}) rotate(${(beat % 2 ? 1 : -1) * 3})`}>
        <circle r={300} fill={P.cream} stroke={P.ink} strokeWidth={12} />
        <path d={`M0,0 L${Math.sin(lt * 6.28) * 230},${-Math.cos(lt * 6.28) * 230}`} stroke={P.terracotta} strokeWidth={14} strokeLinecap="round" />
        <text y={120} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={130} fill={P.ink}>{`${Math.floor(left / 60)}:${String(Math.floor(left % 60)).padStart(2, '0')}`}</text>
        <circle r={20} fill={P.ink} />
      </g>
      {son > 0 && (
        <g>
          <Phone x={540} y={1150} s={0.45} rot={-4}>
            <circle cy={-160} r={90} fill={P.sage} stroke={P.ink} strokeWidth={6} />
            <text y={-130} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={80} fill={P.cream}>С</text>
            <text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.ink}>Сынок</text>
            <rect x={-140} y={110} width={280} height={110} rx={55} fill={P.sage} stroke={P.ink} strokeWidth={6} />
            <text y={182} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.cream}>Позвонить</text>
          </Phone>
          <g transform={`translate(${lerp(980, 660, easeOut(son)) + push * 200},${1500 - push * 40}) rotate(-35)`}>
            <rect x={-30} y={-150} width={60} height={170} rx={30} fill={ZIN.skin} stroke={P.ink} strokeWidth={7} />
          </g>
          <Plate x={830} y={1020} text="1 МИНУТА" s={pop(after(lt, sonAt + 0.3, 0.4))} rot={-4} fill={P.sage} size={64} />
        </g>
      )}
      <MiniZina x={180} y={360} s={0.75} e={{worry: 1, sweat: 1}} />
      <BtnBadge n={2} />
    </svg>
  );
};

// ---------- 3/3 секрет: темнота, пластырь «ТСС», стена между Зиной и сыном ----------
export const SceneSecret: React.FC<{lt: number; dur: number; crackAt: number}> = ({lt, dur, crackAt}) => {
  const lit = easeOut(after(lt, 0.15, 0.5)), crack = after(lt, crackAt, 0.5);
  const fx = 540 + Math.sin(lt * 1.3) * 160;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#17121C" />
      <defs>
        <radialGradient id="torch" cx={fx / 1080} cy={0.47} r={0.42}>
          <stop offset="0" stopColor="#FFF3C4" stopOpacity={0.55 * lit} />
          <stop offset="1" stopColor="#FFF3C4" stopOpacity={0} />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill="#3A2D55" opacity={0.35 + crack * 0.5} />
      <rect width={1080} height={1920} fill="url(#torch)" />
      <g transform={`translate(260,1000) scale(${0.95})`}><RiderFigure r={ZIN} e={em({worry: 1})} /></g>
      <g transform="translate(260,860) rotate(-6)"><rect x={-70} y={-22} width={140} height={44} rx={6} fill="#E9DCC0" stroke={P.ink} strokeWidth={5} /><text y={13} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.terracotta}>ТСС</text></g>
      {/* стена */}
      <g opacity={1 - crack * 0.85}>
        <rect x={470} y={420} width={140} height={1000} fill="#6B5A52" stroke={P.ink} strokeWidth={8} />
        {Array.from({length: 10}, (_, i) => <path key={i} d={`M470,${470 + i * 100} h140 M${i % 2 ? 540 : 505},${420 + i * 100} v50`} stroke={P.ink} strokeWidth={4} opacity={0.5} />)}
        {crack > 0 && <path d="M540,420 l-30,180 l50,140 l-40,200 l30,220 l-20,260" stroke="#FFF3C4" strokeWidth={10} fill="none" />}
      </g>
      <g transform={`translate(830,1000) scale(0.95)`} opacity={0.35 + crack * 0.65}>
        <RiderFigure r={{name: 'сын', skin: '#E7B996', shade: '#CC9A78', headScale: 1, bodyScale: 1, jaw: 'soft', hair: 'sidepart', hairColor: '#5A3B28', clothes: 'jacket', c1: '#5E7FA0', c2: '#46627F'}} e={em({smile: 1})} />
      </g>
      {crack > 0 && <Plate x={830} y={560} text="МАМ, ТЫ ЧЕГО?" s={pop(after(lt, crackAt + 0.2, 0.4))} rot={4} fill={P.sage} size={50} />}
      <BtnBadge n={3} />
    </svg>
  );
};

// ---------- ответ: три кнопки разом + секундомер 0:10 ----------
export const SceneButtons: React.FC<{lt: number; dur: number}> = ({lt}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#2A2034" />
    {BTN_NAMES.map((n, i) => {
      const on = after(lt, 0.15 + i * 0.22, 0.2);
      return (
        <g key={n} transform={`translate(540,${520 + i * 230}) scale(${0.9 + pop(on) * 0.1})`}>
          <rect x={-300} y={-80} width={600} height={160} rx={70} fill={on > 0.5 ? BTN_COLORS[i] : '#4A4054'} stroke={P.ink} strokeWidth={9} />
          <text y={28} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.cream}>{n}</text>
        </g>
      );
    })}
    <g transform="translate(540,1250)">
      <circle r={110} fill={P.cream} stroke={P.ink} strokeWidth={9} />
      <rect x={-20} y={-150} width={40} height={40} fill={P.ink} />
      <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.ink}>0:10</text>
    </g>
    <Plate x={540} y={300} text="= МОШЕННИК" s={pop(after(lt, 0.9, 0.4))} rot={-3} fill={P.terracotta} size={80} />
  </svg>
);

// ---------- откуда номер: карточка Зины разлетается на кусочки ----------
const PIECES = [
  {x: 230, y: 820, t: 'КАРТА МАГАЗИНА', s: '☑ передавать партнёрам'},
  {x: 830, y: 820, t: 'ДОСТАВКА', s: 'Альбина Г., +7 9…'},
  {x: 230, y: 1180, t: 'ЗАПИСЬ К ВРАЧУ', s: 'телефон, возраст'},
  {x: 830, y: 1180, t: 'ОБЪЯВЛЕНИЕ', s: '«продам дачу»'},
];
export const ScenePuzzle: React.FC<{lt: number; dur: number}> = ({lt}) => {
  const br = easeInOut(after(lt, 0.5, 0.8));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#D6E2F0" />
      <g transform="translate(540,460)" opacity={1 - br * 0.3}>
        <rect x={-330} y={-110} width={660} height={220} rx={24} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={-20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink}>Альбина Григорьевна</text>
        <text y={56} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={48} fill="#5E7FA0">+7 9•• •••-••-••</text>
      </g>
      {PIECES.map((p, i) => {
        const k = easeOut(after(lt, 0.55 + i * 0.12, 0.6));
        return (
          <g key={i} transform={`translate(${lerp(540, p.x, k)},${lerp(460, p.y, k)}) scale(${0.4 + k * 0.6}) rotate(${(1 - k) * (i % 2 ? 20 : -20)})`} opacity={clamp(k * 3)}>
            <rect x={-200} y={-120} width={400} height={240} rx={22} fill={['#F6E3B8', '#E9D4B4', '#FFFBF2', '#DCEBD3'][i]} stroke={P.ink} strokeWidth={7} />
            <path d="M-40,-120 q40,-40 80,0" fill={['#F6E3B8', '#E9D4B4', '#FFFBF2', '#DCEBD3'][i]} stroke={P.ink} strokeWidth={7} />
            <text y={-20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.ink}>{p.t}</text>
            <text y={44} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={30} fill={P.terracotta}>{p.s}</text>
          </g>
        );
      })}
      <MiniZina x={540} y={1000} s={0.7} e={{shock: br, mouth: br > 0.5 ? 2 : 0}} />
    </svg>
  );
};

// ---------- трубы из компаний в ларёк «БАЗА», сотрудник выносит папку ----------
export const ScenePipes: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const B = [{x: 200, t: 'МАГАЗИН', c: '#E3B04B'}, {x: 540, t: 'ДОСТАВКА', c: '#C8553D'}, {x: 880, t: 'КЛИНИКА', c: '#7FAF6B'}];
  const emp = easeInOut(after(lt, dur * 0.5, 1.2));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#E8E1EE" />
      <Cam k={clamp(lt / dur)} z1={1.06}>
        {B.map((b) => (
          <g key={b.t}>
            <rect x={b.x - 140} y={330} width={280} height={260} fill={b.c} stroke={P.ink} strokeWidth={8} />
            <rect x={b.x - 150} y={290} width={300} height={60} fill={P.cream} stroke={P.ink} strokeWidth={8} />
            <text x={b.x} y={334} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink}>{b.t}</text>
            {[0, 1].map((r) => [0, 1, 2].map((c) => <rect key={r + '' + c} x={b.x - 110 + c * 80} y={380 + r * 90} width={50} height={60} fill="#FFFBF2" stroke={P.ink} strokeWidth={4} />))}
            <path d={`M${b.x},590 L${b.x},760 Q${b.x},860 ${lerp(b.x, 540, 0.6)},900 L540,1000`} fill="none" stroke="#6B5A52" strokeWidth={40} />
            <path d={`M${b.x},590 L${b.x},760 Q${b.x},860 ${lerp(b.x, 540, 0.6)},900 L540,1000`} fill="none" stroke={P.ink} strokeWidth={4} strokeDasharray="12 30" strokeDashoffset={-lt * 120} />
          </g>
        ))}
        {/* ларёк БАЗА */}
        <g transform="translate(540,1180)">
          <rect x={-260} y={-180} width={520} height={330} fill="#3A2D45" stroke={P.ink} strokeWidth={9} />
          <path d="M-290,-180 L290,-180 L250,-250 L-250,-250Z" fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
          <text y={-198} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.cream}>БАЗА</text>
          <rect x={-210} y={-120} width={420} height={170} rx={14} fill={P.cream} stroke={P.ink} strokeWidth={6} opacity={clamp(lt / 1.5)} />
          <text y={-60} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink} opacity={clamp(lt / 1.5)}>Альбина Григорьевна · 68</text>
          <text y={0} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={32} fill={P.terracotta} opacity={clamp((lt - 1) / 1)}>вклад · пенсия</text>
        </g>
        {/* сотрудник выносит папку из двери */}
        <g transform={`translate(${lerp(880, 780, emp)},${lerp(640, 1100, emp)}) scale(0.55)`} opacity={after(lt, dur * 0.5, 0.2)}>
          <RiderFigure r={{name: 'сотрудник', skin: '#E4B592', shade: '#C99673', headScale: 1, bodyScale: 1, jaw: 'narrow', hair: 'sidepart', hairColor: '#2E2420', clothes: 'shirtTie', c1: '#DCE3E8', c2: '#3E5A78'}} e={em({look: [0.8, 0]})} />
          <rect x={120} y={60} width={140} height={110} rx={8} fill={P.mustard} stroke={P.ink} strokeWidth={7} />
        </g>
      </Cam>
      <Plate x={540} y={720} text="ВЗЛОМАЛИ ИЛИ СЛИЛИ" s={pop(after(lt, 0.6, 0.4))} rot={-3} fill={P.ink} size={62} />
    </svg>
  );
};

// ---------- 710 млн записей, по 5 на каждого ----------
export const SceneLeak: React.FC<{lt: number; dur: number}> = ({lt}) => {
  const n = Math.round(710 * easeOut(clamp(lt / 1.2)));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#F0D3C6" />
      <text x={540} y={560} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={230} fill={P.terracotta} stroke={P.ink} strokeWidth={10}>{n}</text>
      <Plate x={540} y={700} text="МЛН ЗАПИСЕЙ УТЕКЛО" s={pop(after(lt, 0.4, 0.4))} rot={-3} fill={P.ink} size={56} />
      <Caption text="2024 · Роскомнадзор" y={800} />
      {[0, 1, 2, 3, 4].map((i) => {
        const k = after(lt, 1.2 + i * 0.12, 0.3);
        return (
          <g key={i} transform={`translate(${150 + i * 195},1280) scale(0.42)`} opacity={clamp(k * 2)}>
            <RiderFigure r={i === 2 ? ZIN : {...ZIN, hair: (['messy', 'ponytail', 'bob', 'sidepart', 'bald'] as const)[i], hairColor: ['#5A3B28', '#3B2A22', '#C9C3BD', '#2E2420', '#E8E2DA'][i], glasses: false, beads: false, wrinkles: i === 4, clothes: (['hoodie', 'sweater', 'cardigan', 'jacket', 'jacket'] as const)[i], c1: ['#8FA57E', '#E3B04B', '#7E6BA0', '#5E7FA0', '#6B6A55'][i]}} e={em({shock: k})} />
            {[0, 1, 2, 3, 4].map((j) => <rect key={j} x={-110 + j * 44} y={-480 - (j % 2) * 30 - easeOut(k) * 40} width={60} height={80} rx={8} fill={P.cream} stroke={P.ink} strokeWidth={8} />)}
          </g>
        );
      })}
      <Plate x={540} y={940} text="≈ ПО 5 НА КАЖДОГО" s={pop(after(lt, 1.9, 0.4))} rot={3} fill={P.mustard} color={P.ink} size={60} />
    </svg>
  );
};

// ---------- робот-молчун: проверка «живой номер» ----------
export const SceneRobot: React.FC<{lt: number; dur: number; stampAt: number}> = ({lt, stampAt}) => {
  const st = after(lt, stampAt, 0.2), price = Math.round(lerp(5, 50, easeOut(after(lt, stampAt + 0.2, 0.6))));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#DCE6E0" />
      {/* робот */}
      <g transform="translate(300,700)">
        <rect x={-130} y={-120} width={260} height={220} rx={40} fill="#B9C0C8" stroke={P.ink} strokeWidth={9} />
        {[-55, 55].map((x) => <circle key={x} cx={x} cy={-20} r={30} fill={Math.floor(lt * 3) % 2 ? '#7FD6FF' : '#4A90B8'} stroke={P.ink} strokeWidth={6} />)}
        <rect x={-50} y={40} width={100} height={20} rx={8} fill={P.ink} />
        <path d="M-150,-40 Q-160,-170 0,-170 Q160,-170 150,-40" fill="none" stroke={P.ink} strokeWidth={14} />
        <rect x={-120} y={110} width={240} height={200} rx={30} fill="#9AA3AD" stroke={P.ink} strokeWidth={9} />
        <text x={0} y={-200} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink}>ОБЗВОН 24/7</text>
      </g>
      {/* телефон Зины: тишина */}
      <Phone x={780} y={760} s={0.55} rot={6}>
        <text y={-120} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.ink}>Неизвестный</text>
        <text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={110} fill="#8A7A70">• • •</text>
        <text y={140} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={44} fill="#8A7A70">тишина…</text>
      </Phone>
      {/* карточка в базе + штамп */}
      <g transform="translate(540,1260)">
        <rect x={-300} y={-110} width={600} height={220} rx={22} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={-30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.ink}>Альбина Григорьевна</text>
        <text y={40} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill="#5E7FA0">+7 9•• •••-••-••</text>
        {st > 0 && <g transform={`rotate(-12) scale(${lerp(2.2, 1, st)})`} opacity={st}><rect x={-170} y={-60} width={340} height={120} rx={14} fill="none" stroke={P.sageDark} strokeWidth={12} /><text y={28} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={80} fill={P.sageDark}>ЖИВОЙ</text></g>}
        <g transform={`translate(260,-150) rotate(10) scale(${1 + Math.sin(after(lt, stampAt + 0.2, 0.6) * Math.PI) * 0.2})`}>
          <path d="M-70,-40 L60,-40 L100,0 L60,40 L-70,40Z" fill={P.mustard} stroke={P.ink} strokeWidth={6} />
          <text x={10} y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.ink}>{st > 0 ? `×${Math.round(price / 5)}` : '×1'}</text>
        </g>
      </g>
      <MiniZina x={180} y={380} s={0.75} e={{shock: st, mouth: st ? 2 : 0}} />
    </svg>
  );
};

// ---------- «безопасный счёт»: сейф, задняя стенка — карман мошенника ----------
export const SceneSafe: React.FC<{lt: number; dur: number; openAt: number}> = ({lt, dur, openAt}) => {
  const inn = easeInOut(after(lt, 0.2, 0.6)), op = easeInOut(after(lt, openAt, 0.6)), gone = easeInOut(after(lt, openAt + 0.5, 0.6));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#D9DCE0" />
      <Cam k={clamp(lt / dur)} z1={1.08}>
        {/* куртка мошенника за сейфом */}
        <g transform={`translate(${lerp(540, 720, op)},820)`} opacity={op}>
          <path d="M-260,-300 L260,-300 L300,320 L-300,320Z" fill="#2E2B33" stroke={P.ink} strokeWidth={9} />
          <path d="M-160,40 L160,40 L150,240 L-150,240Z" fill="#46424D" stroke={P.ink} strokeWidth={7} />
          <text y={-200} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>КАРМАН</text>
          <text y={-150} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>МОШЕННИКА</text>
        </g>
        <g transform={`translate(${lerp(540, 300, op)},820)`}>
          <rect x={-260} y={-300} width={520} height={600} rx={30} fill="#7D858F" stroke={P.ink} strokeWidth={10} />
          <rect x={-220} y={-260} width={440} height={520} rx={20} fill="#5E6670" stroke={P.ink} strokeWidth={7} />
          <circle cx={150} cy={0} r={50} fill="#B9C0C8" stroke={P.ink} strokeWidth={7} />
          <Plate x={0} y={-370} text="БЕЗОПАСНЫЙ СЧЁТ" size={48} fill={P.sage} />
        </g>
        <g transform={`translate(${lerp(540, 900, gone)},${lerp(1400, 900, inn) + gone * 40})`} opacity={1 - gone * 0.9}>
          <Note x={0} y={0} s={1.3} v="800 000" />
        </g>
      </Cam>
      <MiniZina x={900} y={1180} s={0.75} e={{shock: gone, worry: 1 - gone, mouth: gone > 0.5 ? 3 : 0}} />
    </svg>
  );
};

// ---------- статистика: каждые 16 секунд → Москва 33 млрд ----------
export const SceneStats: React.FC<{lt: number; dur: number; splitAt: number}> = ({lt, dur, splitAt}) => {
  const two = lt >= splitAt, l2 = lt - splitAt;
  if (!two) {
    const s = (lt * 1.6) % 16;
    return (
      <svg viewBox="0 0 1080 1920">
        <rect width={1080} height={1920} fill="#E9D4B4" />
        <g transform="translate(540,700)">
          <circle r={290} fill={P.cream} stroke={P.ink} strokeWidth={12} />
          <path d={`M0,0 L0,-290 A290,290 0 ${s > 8 ? 1 : 0},1 ${Math.sin(s / 16 * 6.283) * 290},${-Math.cos(s / 16 * 6.283) * 290}Z`} fill={P.terracotta} opacity={0.8} />
          <circle r={24} fill={P.ink} />
        </g>
        <Plate x={540} y={1150} text="КАЖДЫЕ 16 СЕКУНД" s={pop(after(lt, 0.2, 0.4))} rot={-3} size={70} />
        <Caption text="ЦБ · все хищения без согласия клиентов · 1 п/г 2026" y={1270} />
      </svg>
    );
  }
  const k = easeOut(clamp(l2 / 1.0));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2C2342" />
      {/* силуэт Москвы */}
      <path d="M0,1250 L0,1100 L80,1100 L80,1000 L140,1000 L140,1120 L230,1120 L240,880 L260,820 L280,880 L290,1120 L380,1120 L380,960 L460,960 L460,1120 L520,1120 L540,760 L560,1120 L640,1120 L640,1010 L720,1010 L730,900 L760,860 L790,900 L800,1120 L900,1120 L900,1040 L1080,1040 L1080,1250Z" fill="#1E1730" stroke={P.ink} strokeWidth={6} />
      <rect y={1250} width={1080} height={670} fill="#1E1730" />
      {Array.from({length: 18}, (_, i) => <Note key={i} x={200 + (i % 6) * 136} y={lerp(-200, 1060 - Math.floor(i / 6) * 70, easeOut(clamp(l2 / 0.9 - i * 0.03)))} s={0.7} rot={(i * 37) % 30 - 15} />)}
      <text x={540} y={560} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={140} fill={P.mustard} stroke={P.ink} strokeWidth={8} opacity={k}>{Math.round(33 * k)} МЛРД ₽</text>
      <text x={540} y={660} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={30} fill={P.cream} opacity={0.75 * k}>Москва · 9 месяцев 2026 · МВД</text>
      <MiniZina x={880} y={330} s={0.7} e={{shock: k, mouth: 3}} />
    </svg>
  );
};

// ---------- трубка брошена ----------
export const SceneHangup: React.FC<{lt: number; dur: number}> = ({lt}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#2A2034" />
    <Phone x={540} y={780} s={1.0} rot={3} dark><CallScreen secs={0} label="???" hang={1} /></Phone>
    <Plate x={540} y={1250} text="ТУ-ТУ-ТУ…" s={pop(after(lt, 0.15, 0.4))} rot={-4} fill={P.mustard} color={P.ink} size={70} />
  </svg>
);

// ---------- карта: номер на обороте, «деньги на месте» ----------
export const SceneCard: React.FC<{lt: number; dur: number; flipAt: number; bubbleAt: number}> = ({lt, dur, flipAt, bubbleAt}) => {
  const f = easeInOut(after(lt, flipAt, 0.5)), back = f > 0.5, sx = Math.abs(Math.cos(f * Math.PI));
  const b = after(lt, bubbleAt, 0.3);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#DCEBD3" />
      <Cam k={clamp(lt / dur)} z1={1.05}>
        <g transform={`translate(540,640) scale(${sx},1) rotate(-4)`}>
          <rect x={-330} y={-200} width={660} height={400} rx={36} fill={back ? '#F3EDE4' : '#5E7FA0'} stroke={P.ink} strokeWidth={10} />
          {!back && <g><rect x={-260} y={-90} width={110} height={80} rx={12} fill={P.gold} stroke={P.ink} strokeWidth={6} /><text x={-260} y={120} fontFamily={F} fontWeight={800} fontSize={44} fill={P.cream}>•••• 1234</text><text x={260} y={-120} textAnchor="end" fontFamily={F} fontWeight={900} fontSize={50} fill={P.cream}>БАНК</text></g>}
          {back && <g><rect x={-330} y={-150} width={660} height={80} fill={P.ink} /><text y={40} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill="#8A7A70">телефон банка</text><text y={120} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={64} fill={P.ink}>8 800 •••-••-••</text><rect x={-300} y={70} width={600} height={80} rx={20} fill="none" stroke={P.sage} strokeWidth={8} opacity={0.5 + Math.sin(lt * 8) * 0.5} /></g>}
        </g>
        {b > 0 && (
          <g transform={`translate(640,1010) scale(${pop(b)*0.95})`}>
            <path d="M-330,-110 L330,-110 Q370,-110 370,-70 L370,70 Q370,110 330,110 L-200,110 L-260,170 L-250,110 L-330,110 Q-370,110 -370,70 L-370,-70 Q-370,-110 -330,-110Z" fill={P.cream} stroke={P.ink} strokeWidth={8} />
            <text y={-10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.sageDark}>Ваши деньги на месте ✓</text>
            <text y={56} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={32} fill="#8A7A70">безопасных счетов не бывает</text>
          </g>
        )}
      </Cam>
      <MiniZina x={160} y={1190} s={0.8} e={{smile: b, worry: 1 - b}} />
      <Plate x={540} y={330} text="ПОЛОЖИЛ — ПОЗВОНИЛ САМ" s={pop(after(lt, 0.2, 0.4))} rot={-3} fill={P.sage} size={54} />
    </svg>
  );
};
