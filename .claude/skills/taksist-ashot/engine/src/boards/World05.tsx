import React from 'react';
import {P} from '../palette';
import {RiderFigure, SVETA, EMO, Emotion} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';
import {Cam, Coin, Note, fmt} from './World';
import {CabinBack} from '../scene/Cabin';

// Сцены серии 5 «Кредитка 100 дней». Формат (решение автора 2026-11-06): объясняющие картинки главные, такси врезками.
// Правила как в World.tsx: 1080×1920, lt — сек от начала врезки, dur — длина врезки, важное в зоне x 56..922, y 250..1300.
// Света — SVETA[2] (вариант В: каре, жакет; утверждён автором 2026-11-06). Мини-аватар Светы реагирует в углу сцен.

const F = 'Rubik';
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);
export const SVE = SVETA[2];
const em = (e: Partial<Emotion>): Emotion => ({...EMO.calm, ...e});
export const CH_COLORS = ['#C8553D', '#EDB447', '#7FAF6B'];
const CH_BG = ['#F0D3C6', '#F6E3B8', '#DCEBD3'];

// ширина текста Rubik 900: заглавные и цифры шире строчных; длинное ужимаем textLength, чтобы не вылезало за плашку
export const textW = (t: string, size: number) => [...t].reduce((a, ch) => a + size * (ch === ' ' ? 0.3 : /[А-ЯЁA-Z0-9₽%]/.test(ch) ? 0.74 : /[—–]/.test(ch) ? 0.8 : 0.6), 0);
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

// счётчик ловушек в углу
export const TrapBadge: React.FC<{n: number; lit?: number}> = ({n, lit = 0}) => (
  <g transform={`translate(780,300) scale(${1 + Math.sin(clamp(lit) * Math.PI) * 0.25})`}>
    <rect x={-150} y={-56} width={300} height={112} rx={30} fill={P.ink} opacity={0.9} stroke={n ? CH_COLORS[n - 1] : P.cream} strokeWidth={7} />
    <text y={-10} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={28} fill={P.cream}>ЛОВУШКА</text>
    <text y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={n ? CH_COLORS[n - 1] : P.cream}>{n}/3</text>
  </g>
);

// мини-аватар Светы в кружке (реакция внутри объясняющих сцен)
export const MiniSveta: React.FC<{x?: number; y?: number; s?: number; e?: Partial<Emotion>; old?: boolean; o?: number}> = ({x = 190, y = 1120, s = 1, e = {}, old, o = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`} opacity={o}>
    <circle r={130} fill={P.cream} stroke={P.ink} strokeWidth={8} />
    <clipPath id="miniSv"><circle r={126} /></clipPath>
    <g clipPath="url(#miniSv)"><g transform="translate(0,175) scale(0.82)"><RiderFigure r={old ? {...SVE, wrinkles: true} : SVE} e={em(e)} /></g></g>
  </g>
);

// гора долга
const DebtHill: React.FC<{x: number; y: number; v: string; wob?: number}> = ({x, y, v, wob = 0}) => (
  <g transform={`translate(${x},${y + wob})`}>
    <path d="M-260,120 Q-200,-60 -80,-130 Q0,-180 80,-130 Q200,-60 260,120Z" fill="#8C6D5B" stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
    <path d="M-120,-80 Q-60,-120 0,-140" fill="none" stroke="#A98A76" strokeWidth={10} strokeLinecap="round" />
    <rect x={-180} y={-30} width={360} height={110} rx={22} fill={P.cream} stroke={P.ink} strokeWidth={6} />
    <text y={18} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={30} fill="#8A7A70">ДОЛГ</text>
    <text y={66} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.terracotta}>{v}</text>
  </g>
);

// здание банка
const Bank: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M-170,-120 L0,-210 L170,-120Z" fill={P.beige} stroke={P.ink} strokeWidth={8} strokeLinejoin="round" />
    <rect x={-160} y={-120} width={320} height={40} fill={P.beige} stroke={P.ink} strokeWidth={8} />
    {[-110, -37, 37, 110].map((cx) => <rect key={cx} x={cx - 18} y={-80} width={36} height={170} fill="#FFFBF2" stroke={P.ink} strokeWidth={6} />)}
    <rect x={-180} y={90} width={360} height={36} fill={P.beige} stroke={P.ink} strokeWidth={8} />
    <text y={-140} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink}>БАНК</text>
  </g>
);

// 1. Купюра под ножницами: 1 570 → 1 527 уходит в банк, 43 ₽ падает на гору долга, гора не шевелится.
// labels — подписи «ПРОЦЕНТЫ» (в главе 2), в хуке без них.
export const SceneCutBill: React.FC<{lt: number; dur: number; cutAt: number; coinAt: number; labels?: boolean; badge?: number}> = ({lt, dur, cutAt, coinAt, labels, badge}) => {
  const cut = after(lt, cutAt, 0.35), fly = easeInOut(after(lt, cutAt + 0.35, 0.7));
  const fall = after(lt, coinAt - 0.45, 0.45), land = after(lt, coinAt, 0.25);
  const wob = land > 0 && land < 1 ? Math.sin(land * Math.PI * 4) * 3 : 0;
  const shock = land > 0 ? 1 : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={labels ? CH_BG[1] : '#F3E2C6'} />
      <Cam k={clamp(lt / dur)} z1={1.08}>
        <Bank x={800} y={540} s={0.9} />
        <DebtHill x={430} y={1010} v="52 340 ₽" wob={wob} />
        {/* купюра: большой кусок + малый кусок */}
        <g transform={`translate(${lerp(470, 800, fly)},${lerp(620, 540, fly)}) scale(${lerp(1, 0.35, fly)}) rotate(${lerp(-4, 8, fly)})`} opacity={1 - after(lt, cutAt + 0.95, 0.15)}>
          <rect x={-300} y={-120} width={560} height={240} rx={18} fill="#9FC48A" stroke={P.ink} strokeWidth={8} />
          <rect x={-276} y={-96} width={512} height={192} rx={12} fill="none" stroke="#5E8F4E" strokeWidth={5} />
          <text x={-10} y={28} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={labels && cut > 0.5 ? 78 : 96} fill="#2F5A2A">{labels && cut > 0.5 ? '1 527' : '1 570 ₽'}</text>
        </g>
        {cut < 0.5 && <g transform="translate(470,620) rotate(-4)"><rect x={260} y={-120} width={40} height={240} fill="#9FC48A" stroke={P.ink} strokeWidth={8} /></g>}
        {/* ножницы проезжают сверху вниз по линии разреза */}
        {cut > 0 && cut < 1 && (
          <g transform={`translate(745,${lerp(460, 780, cut)}) rotate(90)`}>
            <path d="M0,0 L-120,-24 M0,0 L-120,24" stroke={P.ink} strokeWidth={14} strokeLinecap="round" />
            <circle cx={36} cy={-24} r={22} fill="none" stroke={P.terracotta} strokeWidth={12} />
            <circle cx={36} cy={24} r={22} fill="none" stroke={P.terracotta} strokeWidth={12} />
          </g>
        )}
        {cut >= 0.5 && (
          <g transform={`translate(${lerp(760, 470, easeOut(fall))},${lerp(620, 900, fall * fall)}) rotate(${fall * 200})`}>
            <Coin x={0} y={0} r={46} />
          </g>
        )}
        {fall > 0.2 && <Plate x={lerp(760, 560, easeOut(fall))} y={lerp(540, 820, fall)} text="43 ₽" s={pop(after(lt, coinAt - 0.3, 0.4))} rot={4} fill={P.cream} color={P.terracotta} size={70} />}
        {labels && cut > 0.6 && <Plate x={760} y={640} text="ПРОЦЕНТЫ" s={pop(after(lt, cutAt + 0.4, 0.4)) * (1 - after(lt, cutAt + 1.2, 0.3))} rot={-4} size={56} />}
      </Cam>
      {land > 0 && <Plate x={480} y={1220} text="ДОЛГ НЕ СДВИНУЛСЯ" s={pop(after(lt, coinAt + 0.3, 0.4))} rot={-3} fill={P.ink} size={50} />}
      <MiniSveta x={170} y={420} s={0.8} e={{shock, worry: 0.4, mouth: shock ? 2 : 0}} />
      {badge !== undefined && <TrapBadge n={badge} />}
    </svg>
  );
};

// 2. Заставка главы: «ЛОВУШКА 1/3» щелчком заливает фон цветом главы; phoneAt — дальше телефон с минималкой
export const SceneChapter: React.FC<{lt: number; dur: number; n: number; title: string; phoneAt?: number}> = ({lt, dur, n, title, phoneAt}) => {
  const fill = easeOut(after(lt, 0.05, 0.3));
  const ph = phoneAt !== undefined ? easeOut(after(lt, phoneAt, 0.4)) : 0;
  const c = CH_COLORS[n - 1];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <circle cx={540} cy={760} r={1400 * fill} fill={c} />
      <g transform={`translate(${lerp(540, 780, ph)},${lerp(760, 300, ph)}) scale(${lerp(pop(after(lt, 0, 0.45)), 0.3, ph)})`} opacity={1 - ph}>
        <text y={-150} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.ink}>ЛОВУШКА</text>
        <text y={160} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={330} fill={P.cream} stroke={P.ink} strokeWidth={12}>{n}/3</text>
      </g>
      <g opacity={1 - ph}><Plate x={540} y={1140} text={title} s={pop(after(lt, 0.35, 0.4))} rot={-3} fill={P.ink} size={80} /></g>
      {ph > 0 && <TrapBadge n={n} />}
      {ph > 0 && (
        <g transform={`translate(540,${lerp(1500, 780, ph)}) rotate(-4)`}>
          <rect x={-250} y={-430} width={500} height={860} rx={60} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
          <rect x={-222} y={-394} width={444} height={788} rx={40} fill={P.cream} />
          <rect x={-200} y={-300} width={400} height={300} rx={30} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
          <text y={-236} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={30} fill="#8A7A70">Минимальный</text>
          <text y={-200} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={30} fill="#8A7A70">платёж</text>
          <text y={-110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.ink}>1 570 ₽</text>
          <text y={-42} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={28} fill="#8A7A70">Удобно! Всего 3%</text>
          <g transform={`translate(0,170) scale(${1 + Math.sin(lt * 6) * 0.03})`}>
            <rect x={-170} y={-60} width={340} height={120} rx={60} fill={P.sage} stroke={P.ink} strokeWidth={7} />
            <text x={34} y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>Оплатить</text>
            <circle cx={-120} cy={0} r={34} fill={P.cream} stroke={P.ink} strokeWidth={5} />
            <path d="M-136,-6 l0,0 M-104,-6 l0,0" stroke={P.ink} strokeWidth={9} strokeLinecap="round" />
            <path d="M-136,8 Q-120,22 -104,8" fill="none" stroke={P.ink} strokeWidth={5} strokeLinecap="round" />
          </g>
        </g>
      )}
    </svg>
  );
};

// 3. Банкомат с зубами: выдаёт 50 000, откусывает 2 340, табличка долга 50 000 → 52 340
export const SceneAtm: React.FC<{lt: number; dur: number; biteAt: number; debtAt: number}> = ({lt, dur, biteAt, debtAt}) => {
  const cash = easeOut(after(lt, 0.4, 0.5));
  const chomp = lt > biteAt - 0.15 && lt < biteAt + 0.6 ? Math.abs(Math.sin((lt - biteAt + 0.15) * 14)) : 0;
  const bit = after(lt, biteAt, 0.3), d = after(lt, debtAt, 0.4);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={CH_BG[0]} />
      <Cam k={clamp(lt / dur)}>
        <rect x={230} y={380} width={520} height={860} rx={40} fill="#5E6B78" stroke={P.ink} strokeWidth={10} />
        <rect x={290} y={440} width={400} height={240} rx={20} fill="#BFE0F2" stroke={P.ink} strokeWidth={7} />
        {/* глаза-экран */}
        {[-80, 80].map((dx) => <g key={dx}><ellipse cx={490 + dx} cy={555} rx={44} ry={bit > 0 ? 30 : 44} fill="#FFFBF2" stroke={P.ink} strokeWidth={6} /><circle cx={490 + dx + 8} cy={565} r={18} fill={P.ink} /></g>)}
        <path d={`M410,${bit > 0 ? 490 : 500} L460,${bit > 0 ? 515 : 500} M570,${bit > 0 ? 490 : 500} L520,${bit > 0 ? 515 : 500}`} stroke={P.ink} strokeWidth={10} strokeLinecap="round" />
        {/* рот-щель с зубами */}
        <g transform={`translate(490,${820})`}>
          <rect x={-200} y={-50 - chomp * 40} width={400} height={100 + chomp * 80} rx={30} fill="#3A1414" stroke={P.ink} strokeWidth={8} />
          {Array.from({length: 7}, (_, i) => <path key={'u' + i} d={`M${-180 + i * 55},${-50 - chomp * 40} l27,${46} l27,${-46}Z`} fill="#FFFBF2" stroke={P.ink} strokeWidth={4} />)}
          {Array.from({length: 7}, (_, i) => <path key={'d' + i} d={`M${-180 + i * 55},${50 + chomp * 40} l27,${-46} l27,${46}Z`} fill="#FFFBF2" stroke={P.ink} strokeWidth={4} />)}
        </g>
        <rect x={330} y={980} width={320} height={50} rx={12} fill="#2B3540" stroke={P.ink} strokeWidth={6} />
        {/* пачка 50 000 выезжает из щели */}
        <g transform={`translate(${lerp(490, 300, cash)},${lerp(1000, 1080, cash)}) rotate(${-cash * 10})`} opacity={cash}>
          {[0, 1].map((i) => <g key={i} transform={`translate(${i * 10},${-i * 14})`}><rect x={-150} y={-70} width={300} height={140} rx={14} fill="#E9A06B" stroke={P.ink} strokeWidth={7} /><rect x={-132} y={-52} width={264} height={104} rx={9} fill="none" stroke="#B56E40" strokeWidth={4} /><text y={18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={52} fill="#7A3E1E">50 000</text></g>)}
        </g>
        {bit > 0 && <Plate x={700} y={760} text="−2 340 ₽" s={pop(bit)} rot={6} size={74} />}
      </Cam>
      {/* табличка долга */}
      <g transform={`translate(760,1130) scale(${pop(after(lt, 0.3, 0.4))})`}>
        <rect x={-190} y={-90} width={380} height={180} rx={30} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={-34} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill="#8A7A70">ДОЛГ</text>
        <text y={46} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={d > 0.5 ? P.terracotta : P.ink} transform={`scale(${1 + Math.sin(d * Math.PI) * 0.2})`}>{d > 0.5 ? '52 340' : '50 000'}</text>
      </g>
      <TrapBadge n={1} />
    </svg>
  );
};

// 4. Календарь «100 ДНЕЙ БЕЗ %» разлетается листками, под ним счётчик процентов с «ДЕНЬ 1»; grabAt — Света хватается за голову
export const SceneCalFly: React.FC<{lt: number; dur: number; tearAt?: number; grabAt?: number}> = ({lt, dur, tearAt = 0.9, grabAt}) => {
  const tear = after(lt, tearAt, 1.2);
  const days = Math.max(1, Math.floor(clamp((lt - tearAt - 0.6) / Math.max(1, dur - tearAt - 0.6)) * 30) + 1);
  const grab = grabAt !== undefined && lt >= grabAt;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={CH_BG[0]} />
      {/* счётчик процентов под календарём */}
      <g transform="translate(540,760)" opacity={clamp(tear * 2)}>
        <rect x={-380} y={-200} width={760} height={400} rx={50} fill="#1E1816" stroke={P.ink} strokeWidth={12} />
        <text y={-100} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={46} fill="#8A7A70">ПРОЦЕНТЫ КАПАЮТ</text>
        <text y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={130} fill="#FF9A4A">+{fmt(days * 50.2)} ₽</text>
        <text y={140} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.mustard}>ДЕНЬ {days}</text>
      </g>
      {/* листки календаря */}
      {Array.from({length: 8}, (_, i) => {
        const k = clamp(tear * 1.3 - i * 0.04);
        const dx = (i % 2 ? 1 : -1) * (200 + i * 60) * k, dy = -k * (200 + i * 70) + k * k * 900, r = (i % 2 ? 1 : -1) * k * (90 + i * 30);
        return (
          <g key={i} transform={`translate(${540 + dx},${760 + dy}) rotate(${r})`} opacity={1 - clamp(k * 1.4 - 0.4)}>
            <rect x={-300} y={-260} width={600} height={520} rx={30} fill="#FFFBF2" stroke={P.ink} strokeWidth={9} />
            <rect x={-300} y={-260} width={600} height={120} rx={28} fill={P.sage} stroke={P.ink} strokeWidth={9} />
            <text y={-178} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.cream}>БЕЗ %</text>
            <text y={90} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={190} fill={P.ink}>100</text>
            <text y={190} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={54} fill="#8A7A70">ДНЕЙ</text>
          </g>
        );
      })}
      {tear > 0.4 && <Plate x={540} y={1150} text="НА НАЛИЧНЫЕ НЕ ДЕЙСТВУЕТ" s={pop(after(lt, tearAt + 0.5, 0.4))} rot={-3} size={46} />}
      <MiniSveta x={180} y={grab ? 470 : 420} s={grab ? 1 : 0.8} e={grab ? {shock: 1, worry: 1, mouth: 3, sweat: 1} : {worry: 0.5}} />
      <TrapBadge n={1} />
    </svg>
  );
};

// 5. Пляж: Света стареет 22 → 32, счётчик растёт до ≈196 000 ₽; angryAt — она возмущается
export const SceneBeachAge: React.FC<{lt: number; dur: number; endAt: number; angryAt?: number}> = ({lt, dur, endAt, angryAt}) => {
  const k = easeInOut(clamp((lt - 0.3) / Math.max(0.5, endAt - 0.3)));
  const age = Math.round(lerp(22, 32, k)), year = Math.round(lerp(2026, 2036, k));
  const angry = angryAt !== undefined && lt >= angryAt;
  const stomp = angry ? Math.abs(Math.sin((lt - angryAt!) * 9)) * 18 : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <defs><linearGradient id="beachSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#8FC9E8" /><stop offset="1" stopColor="#F4E2B8" /></linearGradient></defs>
      <rect width={1080} height={1920} fill="url(#beachSky)" />
      <circle cx={860} cy={520} r={110} fill="#FFD36B" opacity={0.95} />
      <rect y={860} width={1080} height={220} fill="#4F9CC4" />
      <path d="M0,880 Q135,850 270,880 T540,880 T810,880 T1080,880" fill="none" stroke="#FFFBF2" strokeWidth={8} opacity={0.6} />
      <rect y={1060} width={1080} height={860} fill="#EBCB8B" />
      {/* зонтик */}
      <path d="M760,1060 L790,700" stroke={P.ink} strokeWidth={10} />
      <path d="M600,760 Q790,560 980,760Z" fill={P.terracotta} stroke={P.ink} strokeWidth={8} strokeLinejoin="round" />
      <g transform={`translate(400,${1290 - stomp}) scale(1.1)`}>
        <RiderFigure r={k > 0.7 ? {...SVE, wrinkles: true, hairColor: '#4A3A32'} : SVE} e={em(angry ? {shock: 0.7, worry: 1, mouth: 3} : {worry: k, sweat: k > 0.5 ? 0.6 : 0})} />
      </g>
      <g transform="translate(540,470)">
        <rect x={-300} y={-80} width={600} height={160} rx={40} fill={P.ink} opacity={0.88} />
        <text x={-150} y={28} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.cream}>{age}</text>
        <text x={-60} y={26} fontFamily={F} fontWeight={800} fontSize={40} fill={P.cream} opacity={0.8}>года</text>
        <text x={190} y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.mustard}>{year}</text>
      </g>
      <g transform="translate(540,680)">
        <rect x={-330} y={-90} width={660} height={180} rx={40} fill="#1E1816" stroke={P.ink} strokeWidth={10} />
        <text y={34} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={104} fill="#FF9A4A">≈{fmt(lerp(52340, 196000, k))} ₽</text>
      </g>
      <Plate x={540} y={850} text="если платить по 1 570 ₽ в месяц" s={pop(after(lt, 0.6, 0.4))} rot={0} fill={P.cream} color={P.ink} size={36} />
      <TrapBadge n={2} />
    </svg>
  );
};

// 6. Песочные часы: камера пролетает внутрь, последнее зерно «1 ₽» застревает, переворот, счёт и штамп
export const SceneHourglass: React.FC<{lt: number; dur: number; flipAt: number; stampAt: number}> = ({lt, dur, flipAt, stampAt}) => {
  const fly = easeOut(after(lt, 0, 0.7));
  const flip = easeInOut(after(lt, flipAt, 0.45)), bill = easeOut(after(lt, flipAt + 0.35, 0.4)), st = after(lt, stampAt, 0.2);
  const sand = clamp(lt / Math.max(0.5, flipAt));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={CH_BG[2]} />
      <g transform={`translate(540,820) scale(${lerp(3.2, 0.85, fly)}) rotate(${flip * 180})`}>
        <path d="M-230,-380 L230,-380 L230,-350 Q230,-120 30,0 Q230,120 230,350 L230,380 L-230,380 L-230,350 Q-230,120 -30,0 Q-230,-120 -230,-350Z" fill="#FFFBF2" fillOpacity={0.55} stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
        <path d={`M${-170 * (1 - sand)},${-350 + 300 * sand} L${170 * (1 - sand)},${-350 + 300 * sand} L20,-20 L-20,-20Z`} fill={P.mustard} opacity={sand < 0.98 ? 1 : 0} />
        <path d={`M-200,350 L200,350 Q${120},${350 - 260 * sand} 0,${350 - 300 * sand} Q-120,${350 - 260 * sand} -200,350Z`} fill={P.mustard} stroke={P.ink} strokeWidth={5} />
        <rect x={-260} y={-420} width={520} height={50} rx={14} fill="#8C6D5B" stroke={P.ink} strokeWidth={8} />
        <rect x={-260} y={370} width={520} height={50} rx={14} fill="#8C6D5B" stroke={P.ink} strokeWidth={8} />
        {flip < 0.3 && <text y={-440} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.ink}>100 ДНЕЙ</text>}
        {/* застрявшее зерно-монета */}
        {flip < 0.5 && <Coin x={0} y={-30 + Math.sin(lt * 20) * 3} r={30} />}
      </g>
      {flip < 0.5 && lt > 0.8 && <Plate x={760} y={700} text="1 ₽" s={pop(after(lt, 0.8, 0.4))} rot={6} fill={P.cream} color={P.terracotta} size={60} />}
      {bill > 0 && (
        <g transform={`translate(540,${lerp(-200, 980, bill)}) rotate(${lerp(-12, -3, bill)})`}>
          <rect x={-400} y={-110} width={800} height={220} rx={24} fill={P.cream} stroke={P.ink} strokeWidth={9} />
          <text y={-24} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.ink}>ПРОЦЕНТЫ</text>
          <text y={60} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.terracotta} textLength={680} lengthAdjust="spacingAndGlyphs">ЗА ВСЕ 100 ДНЕЙ</text>
        </g>
      )}
      {st > 0 && (
        <g transform={`translate(540,1270) scale(${lerp(2.2, 1, easeOut(st))}) rotate(-6)`} opacity={clamp(st * 3)}>
          <rect x={-380} y={-70} width={760} height={140} rx={20} fill="none" stroke={P.terracotta} strokeWidth={14} />
          <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.terracotta} textLength={660} lengthAdjust="spacingAndGlyphs">НЕ СЧИТАЕТСЯ</text>
        </g>
      )}
      <TrapBadge n={3} lit={after(lt, 0.6, 0.6)} />
    </svg>
  );
};

// 7. Поворот: три правила щёлкают по очереди, денежная стрелка разворачивается (кэшбэк), «ДЕНЬ 99 — ПОГАШЕНО»
export const SceneRules: React.FC<{lt: number; dur: number; steps: number[]; flipAt: number}> = ({lt, dur, steps, flipAt}) => {
  const R = [['ТОЛЬКО КАРТОЙ', P.sage], ['АВТОПЛАТЁЖ НА ВСЮ СУММУ', P.mustard], ['0 % + КЭШБЭК', P.terracotta]] as const;
  const flip = easeInOut(after(lt, flipAt, 0.5));
  const done = after(lt, flipAt + 0.6, 0.4);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={P.cream} />
      {R.map(([txt, c], i) => {
        const k = after(lt, steps[i] ?? 0, 0.3), press = lt > (steps[i] ?? 0) && lt < (steps[i] ?? 0) + 0.15 ? 10 : 0;
        return (
          <g key={i} transform={`translate(540,${330 + i * 150}) scale(${pop(k)})`}>
            <rect x={-420} y={-56 + 12} width={840} height={112} rx={56} fill={P.ink} opacity={0.4} />
            <rect x={-420} y={-56 + press} width={840} height={112} rx={56} fill={c} stroke={P.ink} strokeWidth={8} />
            <text y={18 + press} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={txt.length > 16 ? 46 : 56} fill={i === 1 ? P.ink : P.cream}>{txt}</text>
          </g>
        );
      })}
      {/* банк ⇄ кошелёк */}
      <Bank x={250} y={950} s={0.8} />
      <g transform="translate(820,960)">
        <rect x={-120} y={-80} width={240} height={160} rx={30} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
        <rect x={40} y={-30} width={90} height={60} rx={20} fill="#A8432F" stroke={P.ink} strokeWidth={6} />
        <text y={130} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={36} fill={P.ink}>СВЕТА</text>
      </g>
      <g transform={`translate(540,930) scale(${lerp(-1, 1, flip)},1)`}>
        <path d="M-160,0 L130,0 M90,-40 L140,0 L90,40" fill="none" stroke={flip > 0.5 ? P.sage : P.terracotta} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" />
      </g>
      {Array.from({length: 4}, (_, i) => {
        const k = ((lt * 1.2 + i / 4) % 1), dir = flip > 0.5 ? 1 : -1;
        return <Coin key={i} x={540 + dir * lerp(-220, 220, k)} y={880 - Math.sin(k * Math.PI) * 90} r={28} rot={k * 360} o={0.9} />;
      })}
      {flip > 0.5 && <Plate x={540} y={800} text="КЭШБЭК" s={pop(after(lt, flipAt + 0.3, 0.4))} rot={-3} fill={P.sage} size={56} />}
      {done > 0 && (
        <g transform={`translate(540,1180) scale(${pop(done)}) rotate(-2)`}>
          <rect x={-330} y={-80} width={660} height={160} rx={30} fill="#FFFBF2" stroke={P.ink} strokeWidth={8} />
          <text x={-185} y={18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={48} fill={P.ink}>ДЕНЬ 99</text>
          <text x={135} y={18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.sageDark}>ПОГАШЕНО ✓</text>
        </g>
      )}
    </svg>
  );
};

// Света крупно в такси: phone — «ОДОБРЕНО 100 ДНЕЙ БЕЗ %», scissors — достаёт ножницы
export const ShotSveta: React.FC<{lt?: number; e?: Partial<Emotion>; lean?: number; phone?: boolean; scissors?: boolean}> = ({lt = 1, e = {}, lean = 0, phone, scissors}) => {
  const hop = phone ? Math.abs(Math.sin(lt * 7)) * 24 * (1 - clamp(lt / 2)) : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={lt} /></g>
      <g transform={`translate(540,${1300 - lean * 110 - hop}) scale(${1.9 + lean * 0.4}) rotate(${lean * -4})`}><RiderFigure r={SVE} e={em(e)} /></g>
      {phone && (
        <g transform={`translate(820,1180) rotate(8) scale(${0.56 * pop(after(lt, 0, 0.35))})`}>
          <rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
          <rect x={-184} y={-344} width={368} height={688} rx={38} fill={P.cream} />
          <circle cy={-190} r={80} fill={P.sage} stroke={P.ink} strokeWidth={6} />
          <path d="M-36,-192 L-8,-162 L40,-222" fill="none" stroke={P.cream} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" />
          <text y={-50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.sageDark}>ОДОБРЕНО</text>
          <text y={20} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill="#8A7A70">кредитная карта</text>
          <rect x={-160} y={70} width={320} height={170} rx={24} fill={P.mustard} stroke={P.ink} strokeWidth={5} />
          <text y={150} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink}>100 ДНЕЙ</text>
          <text y={214} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.ink}>БЕЗ %</text>
        </g>
      )}
      {scissors && (
        <g transform={`translate(800,${lerp(1500, 1200, easeOut(after(lt, 0.1, 0.4)))}) rotate(-30) scale(1.5)`}>
          <path d="M0,0 L-120,-24 M0,0 L-120,24" stroke="#B9C0C8" strokeWidth={14} strokeLinecap="round" />
          <path d="M0,0 L-120,-24 M0,0 L-120,24" stroke={P.ink} strokeWidth={3} strokeLinecap="round" />
          <circle cx={36} cy={-24} r={22} fill="none" stroke={P.terracotta} strokeWidth={12} />
          <circle cx={36} cy={24} r={22} fill="none" stroke={P.terracotta} strokeWidth={12} />
        </g>
      )}
    </svg>
  );
};
