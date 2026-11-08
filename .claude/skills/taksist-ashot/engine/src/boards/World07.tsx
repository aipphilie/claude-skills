// Серия 7 «Подработка в прачечной»: сцены-объяснялки. Пассажир — Влад (VLAD[1]).
// Слово «обнал» нигде не пишем: только «прачечная», «стирать деньги», «барабан».
// Все надписи — через T (maxW) или Plate: текст никогда не вылезает за свою рамку (правило автора).
import React from 'react';
import {P} from '../palette';
import {RiderFigure, VLAD, ZINA, Emotion, Rider} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';
import {Cam, Note} from './World';
import {CabinBack} from '../scene/Cabin';
import {Plate, T, Phone, em, F} from './World06';

export const VLD = VLAD[1];
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);

// мини-аватар в кружке (Влад или Альбина Григорьевна)
const Mini: React.FC<{r?: Rider; x: number; y: number; s?: number; e?: Partial<Emotion>; id: string}> = ({r = VLD, x, y, s = 0.75, e = {}, id}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <circle r={130} fill={P.cream} stroke={P.ink} strokeWidth={8} />
    <clipPath id={id}><circle r={126} /></clipPath>
    <g clipPath={`url(#${id})`}><g transform="translate(0,175) scale(0.82)"><RiderFigure r={r} e={em(e)} /></g></g>
  </g>
);

// бейдж «ЧЕК · ПУНКТ n/3» в углу
const CHK = ['#C8553D', '#EDB447', '#8E6FB8'];
export const ChekBadge: React.FC<{n: number}> = ({n}) => (
  <g transform="translate(790,300)">
    <rect x={-150} y={-56} width={300} height={112} rx={30} fill={P.ink} opacity={0.9} stroke={CHK[n - 1]} strokeWidth={7} />
    <T maxW={260} y={-10} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={28} fill={P.cream}>ПУНКТ ЧЕКА</T>
    <T maxW={260} y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={CHK[n - 1]}>{`${n}/3`}</T>
  </g>
);

// грязная купюра: обычная Note + бурые пятна
const Dirty: React.FC<{x: number; y: number; s?: number; rot?: number; o?: number}> = ({x, y, s = 1, rot = 0, o = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`} opacity={o}>
    <Note x={0} y={0} />
    {[[-70, -20, 22], [30, 25, 16], [80, -30, 12]].map(([a, b, r], i) => <ellipse key={i} cx={a} cy={b} rx={r} ry={r * 0.7} fill="#5B3A22" opacity={0.75} />)}
  </g>
);

// банковская карта с лицом владельца
const Card: React.FC<{x: number; y: number; s?: number; rot?: number; r?: Rider; name: string; c?: string; stain?: number; id: string}> = ({x, y, s = 1, rot = 0, r = VLD, name, c = '#5E7FA0', stain = 0, id}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-130} y={-82} width={260} height={164} rx={20} fill={c} stroke={P.ink} strokeWidth={7} />
    <rect x={-108} y={-50} width={50} height={38} rx={7} fill={P.gold} stroke={P.ink} strokeWidth={4} />
    <circle cx={60} cy={-10} r={46} fill={P.cream} stroke={P.ink} strokeWidth={5} />
    <clipPath id={id}><circle cx={60} cy={-10} r={43} /></clipPath>
    <g clipPath={`url(#${id})`}><g transform="translate(60,52) scale(0.3)"><RiderFigure r={r} e={em({})} /></g></g>
    <T maxW={220} x={0} y={62} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.cream}>{name}</T>
    {stain > 0 && [[-60, 10, 26], [10, -40, 18], [95, 40, 20], [-20, 50, 14]].map(([a, b, rr], i) => <ellipse key={i} cx={a} cy={b} rx={rr * stain} ry={rr * 0.7 * stain} fill="#5B3A22" opacity={0.85} />)}
  </g>
);

// ---------- ТАКСИ: Влад на заднем сиденье, телефон в руке ----------
export const ShotVlad: React.FC<{lt?: number; e?: Partial<Emotion>; lean?: number; phone?: 'chat' | 'money' | 'deleted' | 'none'}> = ({lt = 1, e = {}, lean = 0, phone = 'none'}) => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={lt} /></g>
    <g transform={`translate(${540 + lean * 120},${1300 - Math.abs(lean) * 60}) scale(1.9) rotate(${lean * 6})`}><RiderFigure r={VLD} e={em(e)} /></g>
    {phone !== 'none' && (
      <Phone x={820} y={520} s={0.52} rot={8}>
        {phone === 'chat' && (
          <g>
            <rect x={-184} y={-344} width={368} height={100} rx={38} fill="#2F6E5A" />
            <T maxW={320} y={-280} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.cream}>Подработка</T>
            {[['Нужна твоя карта', -150], ['30 000 ₽ за неделю', -20], ['Делать ничего не надо', 110]].map(([t, y], i) => (
              <g key={i} opacity={after(lt, 0.15 + i * 0.25, 0.2)}>
                <rect x={-160} y={(y as number) - 50} width={320} height={90} rx={26} fill={i === 1 ? P.mustard : '#E6E0D6'} stroke={P.ink} strokeWidth={4} />
                <T maxW={290} y={(y as number) + 8} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink}>{t as string}</T>
              </g>
            ))}
          </g>
        )}
        {phone === 'money' && (
          <g>
            <circle cy={-170} r={80} fill={P.sage} stroke={P.ink} strokeWidth={6} />
            <T maxW={130} y={-145} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={80} fill={P.cream}>₽</T>
            <T maxW={330} y={10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.sageDark}>+120 000 ₽</T>
            <T maxW={330} y={100} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={P.ink}>Перекинь дальше</T>
            <T maxW={330} y={160} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.terracotta}>твои 30 000</T>
          </g>
        )}
        {phone === 'deleted' && (
          <g>
            <g transform={`translate(0,-120) scale(${1 + Math.sin(clamp(lt / 0.5) * Math.PI) * 0.15})`}>
              <rect x={-70} y={-60} width={140} height={150} rx={14} fill="#8A7A70" stroke={P.ink} strokeWidth={6} />
              <rect x={-90} y={-90} width={180} height={34} rx={10} fill="#8A7A70" stroke={P.ink} strokeWidth={6} />
            </g>
            <T maxW={330} y={110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.ink}>Чат удалён</T>
          </g>
        )}
      </Phone>
    )}
  </svg>
);

// ---------- ДИСКЛЕЙМЕР (по просьбе автора) ----------
export const SceneDisclaimer: React.FC<{lt: number; dur: number}> = ({lt}) => {
  const k = easeOut(after(lt, 0, 0.35));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#1E1A22" />
      <g opacity={k} transform={`translate(0,${lerp(30, 0, k)})`}>
        <rect x={110} y={520} width={860} height={600} rx={44} fill="#2C2533" stroke={P.mustard} strokeWidth={6} />
        <circle cx={540} cy={620} r={56} fill={P.mustard} stroke={P.ink} strokeWidth={6} />
        <T maxW={80} x={540} y={645} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={72} fill={P.ink}>!</T>
        <T maxW={780} x={540} y={760} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.cream}>ВСЕ ПЕРСОНАЖИ ВЫМЫШЛЕНЫ</T>
        <T maxW={780} x={540} y={830} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={46} fill={P.cream}>Любые совпадения случайны</T>
        <rect x={190} y={872} width={700} height={4} fill={P.mustard} opacity={0.6} />
        <T maxW={780} x={540} y={950} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={42} fill="#C9BFB4">Ролик предупреждает об опасности</T>
        <T maxW={780} x={540} y={1000} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={42} fill="#C9BFB4">и не объясняет, как устроены схемы</T>
        <T maxW={780} x={540} y={1060} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={42} fill="#C9BFB4">Не является инструкцией</T>
      </g>
    </svg>
  );
};

// ---------- стиральная машина посреди города: грязные деньги → стирка ----------
export const SceneWasher: React.FC<{lt: number; dur: number; washAt: number}> = ({lt, dur, washAt}) => {
  const wash = lt >= washAt, spin = wash ? (lt - washAt) * 9 : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2B3A55" />
      <path d="M0,1180 L0,980 L90,980 L90,880 L190,880 L190,1010 L300,1010 L300,860 L380,860 L380,1180 L700,1180 L700,900 L800,900 L800,820 L900,820 L900,960 L1080,960 L1080,1180Z" fill="#1F2A40" />
      <rect y={1180} width={1080} height={740} fill="#1A2236" />
      <Cam k={clamp(lt / dur)} z1={1.08} cy={820}>
        {/* машина */}
        <g transform={`translate(540,${830 + (wash ? Math.sin(lt * 40) * 4 : 0)})`}>
          <rect x={-280} y={-330} width={560} height={640} rx={40} fill="#F3EDE4" stroke={P.ink} strokeWidth={10} />
          <rect x={-280} y={-330} width={560} height={110} rx={40} fill="#DCD4C8" stroke={P.ink} strokeWidth={10} />
          {[-200, -140].map((x) => <circle key={x} cx={x} cy={-275} r={20} fill={P.terracotta} stroke={P.ink} strokeWidth={5} />)}
          <rect x={60} y={-300} width={170} height={52} rx={10} fill="#2A2630" stroke={P.ink} strokeWidth={5} />
          <circle cy={40} r={200} fill="#B9C0C8" stroke={P.ink} strokeWidth={10} />
          <circle cy={40} r={160} fill="#3E5A78" stroke={P.ink} strokeWidth={8} />
          <clipPath id="hatch7"><circle cy={40} r={156} /></clipPath>
          <g clipPath="url(#hatch7)">
            {wash && <rect x={-160} y={60} width={320} height={140} fill="#7FB6D6" opacity={0.6} />}
            <g transform={`translate(0,40) rotate(${spin * 57})`}>
              {[0, 1, 2, 3].map((i) => <Dirty key={i} x={Math.cos(i * 1.57) * 80} y={Math.sin(i * 1.57) * 80} s={0.45} rot={i * 50} o={wash ? 1 - clamp((lt - washAt) / 2.5) * 0.6 : clamp((lt - 0.4 - i * 0.25) / 0.2)} />)}
            </g>
          </g>
          <circle cy={40} r={160} fill="none" stroke="#FFFFFF" strokeWidth={6} opacity={0.35} />
        </g>
        {/* купюры падают в люк */}
        {!wash && [0, 1, 2, 3].map((i) => {
          const k = clamp((lt - i * 0.25) / 0.6);
          return k > 0 && k < 1 ? <Dirty key={i} x={lerp(300 + i * 160, 540, easeInOut(k))} y={lerp(260, 870, easeInOut(k))} s={lerp(0.9, 0.4, k)} rot={i * 40 + k * 120} /> : null;
        })}
      </Cam>
      <Plate x={540} y={330} text={wash ? 'СТИРКА' : 'ГРЯЗНЫЕ ДЕНЬГИ'} s={pop(after(lt, wash ? washAt : 0.1, 0.4))} rot={-3} fill={wash ? P.sage : '#5B3A22'} size={66} />
      {!wash && <T maxW={700} x={540} y={440} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={P.cream} opacity={after(lt, 0.6, 0.3)}>украденные у людей</T>}
    </svg>
  );
};

// ---------- барабан изнутри: карты людей крутятся, барабан = ты ----------
export const SceneDrum: React.FC<{lt: number; dur: number; stainAt: number; talk?: number}> = ({lt, dur, stainAt, talk = 0}) => {
  const a = lt * 40, st = easeOut(after(lt, stainAt, 0.8));
  const ppl: {r: Rider; n: string; c: string}[] = [
    {r: {...VLAD[0], name: 'курьер'}, n: 'КУРЬЕР', c: '#7FAF6B'},
    {r: {...VLAD[2], name: 'студентка', hair: 'ponytail', hairColor: '#3B2A22', lashes: true, lips: true, headphones: false}, n: 'СТУДЕНТКА', c: '#8E6FB8'},
    {r: VLD, n: 'ВЛАД', c: '#5E7FA0'},
  ];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#D9DCE0" />
      <g transform="translate(540,760)">
        <circle r={400} fill="#9AA3AD" stroke={P.ink} strokeWidth={12} />
        <circle r={360} fill="#C3C9D0" stroke={P.ink} strokeWidth={6} />
        {Array.from({length: 24}, (_, i) => <circle key={i} cx={Math.cos(i * 0.2618 + a / 57) * 330} cy={Math.sin(i * 0.2618 + a / 57) * 330} r={10} fill="#7D858F" />)}
        {ppl.map((p, i) => {
          const ang = (a + i * 120) / 57.3;
          return <Card key={i} id={`drc${i}`} x={Math.cos(ang) * 200} y={Math.sin(ang) * 200} s={0.9} rot={Math.sin(ang) * 10} r={p.r} name={p.n} c={p.c} stain={i === 2 ? st : 0} />;
        })}
        {[0, 1, 2, 3, 4].map((i) => { const ang = (-a * 1.5 + i * 72) / 57.3; return <Note key={i} x={Math.cos(ang) * 90} y={Math.sin(ang) * 90} s={0.35} rot={i * 60 + a} />; })}
      </g>
      <Plate x={540} y={1240} text="БАРАБАН — ЭТО ТЫ" s={pop(after(lt, 0.3, 0.4))} rot={-3} fill={P.terracotta} size={62} />
      <Mini id="mdrum" x={180} y={330} e={{worry: st, mouth: talk > 0.1 ? 2 : 0}} />
    </svg>
  );
};

// ---------- глава чека: «что не пишут в чеке», пункт n/3 ----------
const CHEK_NAMES = ['КАРТА — В СТОП', 'ЭТО ЧЬИ-ТО ДЕНЬГИ', 'ТЮРЬМА'];
export const SceneChek: React.FC<{lt: number; dur: number; n: number}> = ({lt, n}) => {
  const up = easeOut(after(lt, 0, 0.45));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <circle cx={540} cy={760} r={1400 * easeOut(after(lt, 0.05, 0.3))} fill={CHK[n - 1]} />
      <g transform={`translate(540,${lerp(1500, 760, up)})`}>
        <path d="M-300,-420 L300,-420 L300,420 L270,440 L240,420 L210,440 L180,420 L150,440 L120,420 L90,440 L60,420 L30,440 L0,420 L-30,440 L-60,420 L-90,440 L-120,420 L-150,440 L-180,420 L-210,440 L-240,420 L-270,440 L-300,420Z" fill="#FFFBF2" stroke={P.ink} strokeWidth={8} />
        <T maxW={540} y={-330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.ink}>ЧТО НЕ ПИШУТ В ЧЕКЕ</T>
        {[-280, 120].map((y) => <path key={y} d={`M-260,${y} H260`} stroke={P.ink} strokeWidth={4} strokeDasharray="14 10" />)}
        <T maxW={540} y={-170} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.ink}>ПУНКТ</T>
        <T maxW={540} y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={200} fill={CHK[n - 1]} stroke={P.ink} strokeWidth={8}>{`${n}/3`}</T>
        <T maxW={520} y={240} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink} opacity={after(lt, 0.35, 0.25)}>{CHEK_NAMES[n - 1]}</T>
      </g>
    </svg>
  );
};

// ---------- пункт 1: карта в стоп + база ЦБ во всех банках ----------
export const SceneBlock: React.FC<{lt: number; dur: number; dbAt: number; allAt: number}> = ({lt, dur, dbAt, allAt}) => {
  const lock = easeOut(after(lt, 0.25, 0.3)), db = easeOut(after(lt, dbAt, 0.5)), all = after(lt, allAt, 0.3);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#F0D3C6" />
      <Cam k={clamp(lt / dur)} z1={1.05}>
        <Card id="blk" x={430} y={560} s={1.5} rot={-6} name="ВЛАД" c="#5E7FA0" />
        <g transform={`translate(480,${lerp(150, 560, lock)})`}>
          <rect x={-70} y={-20} width={140} height={110} rx={16} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
          <path d="M-42,-20 V-60 Q-42,-110 0,-110 Q42,-110 42,-60 V-20" fill="none" stroke={P.ink} strokeWidth={16} />
        </g>
        {lock >= 1 && <Plate x={480} y={790} text="БЛОКИРОВКА" s={pop(after(lt, 0.55, 0.35))} rot={-6} size={56} />}
        {/* папка «БАЗА ЦБ» */}
        <g transform={`translate(${lerp(1300, 540, db)},1050)`}>
          <rect x={-250} y={-120} width={500} height={240} rx={18} fill="#E3B04B" stroke={P.ink} strokeWidth={8} />
          <rect x={-250} y={-150} width={180} height={50} rx={12} fill="#E3B04B" stroke={P.ink} strokeWidth={8} />
          <T maxW={440} y={-40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={52} fill={P.ink}>БАЗА ЦБ</T>
          <rect x={-200} y={0} width={400} height={90} rx={10} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
          <T maxW={370} y={58} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.terracotta}>ВЛАД, 19</T>
        </g>
      </Cam>
      {all > 0 && [0, 1, 2, 3].map((i) => (
        <g key={i} transform={`translate(${210 + i * 220},${1240}) scale(${pop(after(lt, allAt + i * 0.1, 0.3))})`}>
          <path d="M-70,-30 L0,-70 L70,-30Z" fill="#B9C0C8" stroke={P.ink} strokeWidth={5} />
          <rect x={-70} y={-30} width={140} height={80} fill="#DCE3E8" stroke={P.ink} strokeWidth={5} />
          <T maxW={120} y={22} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.ink}>БАНК</T>
          <path d="M-50,-60 L50,40 M50,-60 L-50,40" stroke={P.terracotta} strokeWidth={12} strokeLinecap="round" />
        </g>
      ))}
      <ChekBadge n={1} />
    </svg>
  );
};

// ---------- пункт 2: деньги бабушки, след ведёт к последней карте ----------
export const SceneTrail: React.FC<{lt: number; dur: number; lensAt: number; talk?: number}> = ({lt, dur, lensAt, talk = 0}) => {
  const pts = [[300, 640], [520, 760], [380, 900], [640, 1000]];
  const lens = easeOut(after(lt, lensAt, 0.5));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#E9E1D3" />
      {/* Альбина Григорьевна у пустого сейфа */}
      <g transform="translate(250,560) scale(0.62)"><RiderFigure r={ZINA[0]} e={em({worry: 1, shock: 0.5})} /></g>
      <g transform="translate(540,480)">
        <rect x={-90} y={-90} width={180} height={180} rx={14} fill="#7D858F" stroke={P.ink} strokeWidth={7} />
        <rect x={-70} y={-70} width={140} height={140} rx={8} fill="#2A2630" />
        <T maxW={130} y={10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={36} fill="#8A7A70">ПУСТО</T>
      </g>
      {/* след из карт */}
      {pts.map(([x, y], i) => {
        const k = after(lt, 0.3 + i * 0.35, 0.3);
        const [px, py] = i ? pts[i - 1] : [540, 580];
        return (
          <g key={i} opacity={k}>
            <path d={`M${px},${py} L${x},${y}`} stroke={P.terracotta} strokeWidth={8} strokeDasharray="18 14" />
            {i < 3 ? <Card id={`tr${i}`} x={x} y={y} s={0.55} rot={i % 2 ? 6 : -6} r={{...VLAD[i % 3 === 1 ? 2 : 0]}} name="???" c="#8A7A70" /> : null}
          </g>
        );
      })}
      <Card id="trv" x={720} y={1080} s={1.05} rot={-4} name="ВЛАД" c="#5E7FA0" stain={0.8} />
      {lens > 0 && (
        <g transform={`translate(${lerp(980, 760, lens)},${lerp(1300, 1060, lens)})`}>
          <circle r={110} fill="#BFE0F2" opacity={0.35} stroke={P.ink} strokeWidth={12} />
          <rect x={70} y={70} width={40} height={140} rx={16} fill={P.ink} transform="rotate(-45 90 140)" />
        </g>
      )}
      {lens > 0 && <Plate x={540} y={300} text="ИЩУТ ПО ПОСЛЕДНЕЙ КАРТЕ" s={pop(after(lt, lensAt + 0.2, 0.4))} rot={-3} fill={P.ink} size={46} />}
      <Mini id="mtrail" x={180} y={1200} e={{worry: 1, mouth: talk > 0.1 ? 2 : 0}} />
      {lens === 0 && <ChekBadge n={2} />}
    </svg>
  );
};

// ---------- пункт 3: дверца барабана → решётка, до 6 лет, 312 недель ----------
export const SceneJail: React.FC<{lt: number; dur: number; countAt: number}> = ({lt, countAt}) => {
  const open = easeInOut(after(lt, 0.3, 0.6)), cnt = clamp((lt - countAt) / 1.4), two = lt >= countAt;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2A2034" />
      <g transform="translate(540,640)">
        <circle r={290} fill="#B9C0C8" stroke={P.ink} strokeWidth={12} />
        <circle r={240} fill="#1A1420" stroke={P.ink} strokeWidth={8} />
        {[-160, -80, 0, 80, 160].map((x) => <rect key={x} x={x - 12} y={-230} width={24} height={460} fill="#8A8F96" stroke={P.ink} strokeWidth={4} opacity={open} />)}
        <g transform={`translate(-240,0) scale(${1 - open * 0.9},1) translate(240,0)`}>
          <circle r={240} fill="#3E5A78" stroke={P.ink} strokeWidth={8} opacity={0.95} />
          <circle r={240} fill="none" stroke="#FFFFFF" strokeWidth={6} opacity={0.3} />
        </g>
      </g>
      <Plate x={540} y={300} text="ЗАКОН 2025: ДРОПОВ САЖАЮТ" s={pop(after(lt, 0.2, 0.4))} rot={-3} fill={P.terracotta} size={50} />
      {!two && <T maxW={860} x={540} y={1110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={150} fill={P.mustard} stroke={P.ink} strokeWidth={8} opacity={after(lt, 0.9, 0.3)}>ДО 6 ЛЕТ</T>}
      {!two && <T maxW={860} x={540} y={1200} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={P.cream} opacity={0.8 * after(lt, 1.1, 0.3)}>за то, что дал карту за деньги · 176-ФЗ, ст. 187 УК</T>}
      {two && (
        <g>
          <g transform={`translate(540,1020) scale(${pop(after(lt, countAt, 0.4))})`}>
            <rect x={-400} y={-70} width={800} height={130} rx={36} fill={P.sage} stroke={P.ink} strokeWidth={8} />
            <T maxW={740} y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.ink}>30 000 ₽ = 1 НЕДЕЛЯ</T>
          </g>
          <g transform={`translate(540,1190) scale(${pop(after(lt, countAt + 0.5, 0.4))})`}>
            <rect x={-400} y={-70} width={800} height={130} rx={36} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
            <T maxW={740} y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.cream}>{`6 ЛЕТ = ${Math.round(312 * easeOut(cnt))} НЕДЕЛЬ`}</T>
          </g>
        </g>
      )}

    </svg>
  );
};

// ---------- островок в ТЦ: никого, а по бумагам — очередь и миллионы ----------
const fmt = (n: number) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
export const SceneIsland: React.FC<{lt: number; dur: number; paperAt: number; talk?: number; vladUntil?: number}> = ({lt, dur, paperAt, talk = 0, vladUntil = 0}) => {
  const pap = after(lt, paperAt, 0.4), rev = 4000000 * easeOut(clamp((lt - paperAt - 0.3) / 2.2));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#EDE6DA" />
      {/* коридор ТЦ */}
      <path d="M0,1250 L1080,1250 L1080,1920 L0,1920Z" fill="#CFC6B8" />
      {[0, 1, 2, 3].map((i) => <rect key={i} x={20 + i * 270} y={720} width={240} height={330} fill={['#B9C9D6', '#E3D2B4', '#C9D6B9', '#D6C1C9'][i]} stroke={P.ink} strokeWidth={5} opacity={0.7} />)}
      {/* прохожие идут мимо */}
      {[0, 1, 2].map((i) => {
        const x = ((lt * 130 + i * 380) % 1300) - 110;
        return <g key={i} transform={`translate(${i % 2 ? 1080 - x : x},1180)`}><circle cy={-150} r={34} fill="#6B5A52" /><rect x={-36} y={-115} width={72} height={150} rx={30} fill="#6B5A52" /></g>;
      })}
      <Cam k={clamp(lt / dur)} z1={1.06} cy={1050}>
        <g transform="translate(540,1060)">
          <g transform="translate(0,-40) scale(0.55)"><RiderFigure r={{...ZINA[1], name: 'продавщица', wrinkles: false, glasses: false, hairColor: '#7A4A2A'}} e={em({mouth: Math.sin(lt * 2) > 0.6 ? 3 : 0})} /></g>
          <rect x={-230} y={-20} width={460} height={190} rx={18} fill="#F3EDE4" stroke={P.ink} strokeWidth={8} />
          <rect x={-250} y={-260} width={500} height={70} rx={14} fill={P.terracotta} stroke={P.ink} strokeWidth={7} />
          <T maxW={460} y={-210} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>ЧЕХЛЫ · БРЕЛОКИ</T>
          {[-150, -50, 50, 150].map((x, i) => <rect key={x} x={x - 32} y={20} width={64} height={110} rx={12} fill={['#7FB6D6', '#E3B04B', '#B5677A', '#7FAF6B'][i]} stroke={P.ink} strokeWidth={5} />)}
        </g>
      </Cam>
      {/* по бумагам */}
      {pap > 0 && (
        <g transform={`translate(540,520) scale(${pop(pap)})`}>
          <rect x={-380} y={-200} width={760} height={380} rx={26} fill="#FFFBF2" stroke={P.ink} strokeWidth={8} />
          <T maxW={700} y={-130} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.terracotta}>ПО БУМАГАМ</T>
          <T maxW={700} y={-60} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={P.ink}>выручка за месяц</T>
          <T maxW={700} y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.sageDark}>{`${fmt(rev)} ₽`}</T>
          {Array.from({length: 9}, (_, i) => <g key={i} transform={`translate(${-300 + i * 75},130)`} opacity={after(lt, paperAt + 0.4 + i * 0.08, 0.2)}><circle cy={-22} r={13} fill="none" stroke={P.ink} strokeWidth={4} /><path d="M-14,20 Q0,-8 14,20" fill="none" stroke={P.ink} strokeWidth={4} /></g>)}
        </g>
      )}
      {lt < vladUntil && <Mini id="misl" x={180} y={1200} e={{smile: 0.6, mouth: talk > 0.1 ? 2 : 0}} />}
    </svg>
  );
};

// ---------- магазин одежды без покупателей, выручка как у ТЦ ----------
export const SceneBoutique: React.FC<{lt: number; dur: number; plateAt: number}> = ({lt, dur, plateAt}) => {
  const ch = easeOut(clamp((lt - 0.5) / 2));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#3A3140" />
      <Cam k={clamp(lt / dur)} z1={1.06}>
        <rect x={90} y={340} width={900} height={880} rx={20} fill="#5B4E63" stroke={P.ink} strokeWidth={10} />
        <rect x={250} y={250} width={580} height={110} rx={18} fill={P.mustard} stroke={P.ink} strokeWidth={8} />
        <T maxW={520} x={540} y={325} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.ink}>МОДНЫЙ БУТИК</T>
        <rect x={130} y={400} width={820} height={780} fill="#E9E1EE" stroke={P.ink} strokeWidth={6} />
        {/* манекены в пыли */}
        {[290, 540, 790].map((x, i) => (
          <g key={x} transform={`translate(${x},860)`}>
            <circle cy={-200} r={44} fill="#D6CEC4" stroke={P.ink} strokeWidth={6} />
            <path d="M-70,-140 L70,-140 L90,120 L-90,120Z" fill={['#B5677A', '#5E7FA0', '#7FAF6B'][i]} stroke={P.ink} strokeWidth={6} />
            <rect x={-6} y={120} width={12} height={160} fill={P.ink} />
            {[[-30, -100], [20, -40], [-40, 30], [35, 80]].map(([a, b], j) => <circle key={j} cx={a} cy={b} r={5} fill="#FFFFFF" opacity={0.6} />)}
          </g>
        ))}
        {/* паутина в углу */}
        <path d="M130,400 L230,400 M130,400 L130,500 M130,400 L215,485 M150,400 Q160,430 130,440 M185,400 Q190,465 130,470" stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.7} />
        {/* график выручки в углу витрины */}
        <g transform="translate(770,470)">
          <rect x={-150} y={-50} width={300} height={200} rx={12} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
          <path d={`M-120,120 L${-120 + 80 * ch},${120 - 40 * ch} L${-120 + 160 * ch},${120 - 70 * ch} L${-120 + 240 * ch},${120 - 140 * ch}`} stroke={P.sageDark} strokeWidth={9} fill="none" strokeLinecap="round" />
          <T maxW={260} y={-12} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.ink}>ВЫРУЧКА ↑</T>
        </g>
        <g transform="translate(300,470)">
          <rect x={-150} y={-50} width={300} height={100} rx={12} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
          <T maxW={270} y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.terracotta}>ПОКУПАТЕЛЕЙ: 0</T>
        </g>
      </Cam>
      {lt >= plateAt && <Plate x={540} y={1260} text="ПРАЧЕЧНАЯ С ВЫВЕСКОЙ" s={pop(after(lt, plateAt, 0.4))} rot={-3} fill={P.terracotta} size={58} />}
    </svg>
  );
};

// ---------- табличка «Директор: Влад, 19» падает в папку «ДЕЛО» ----------
export const SceneDirector: React.FC<{lt: number; dur: number; fallAt: number; lawAt: number}> = ({lt, fallAt, lawAt}) => {
  const fall = easeInOut(after(lt, fallAt, 0.7));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#D6E2F0" />
      <g transform="translate(540,720)">
        <rect x={-230} y={-420} width={460} height={840} rx={14} fill="#8C6A4E" stroke={P.ink} strokeWidth={10} />
        <rect x={-190} y={-380} width={380} height={340} rx={10} fill="#7A5A40" stroke={P.ink} strokeWidth={5} />
        <circle cx={170} cy={60} r={22} fill={P.gold} stroke={P.ink} strokeWidth={6} />
      </g>
      {/* папка «ДЕЛО» */}
      <g transform="translate(540,1180)" opacity={after(lt, fallAt - 0.3, 0.3)}>
        <rect x={-260} y={-90} width={520} height={190} rx={16} fill="#E9D4B4" stroke={P.ink} strokeWidth={8} />
        <T maxW={460} y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.ink}>ДЕЛО</T>
      </g>
      {/* табличка */}
      <g transform={`translate(540,${lerp(500, 1130, fall)}) rotate(${fall * 14})`} opacity={1 - after(lt, fallAt + 0.7, 0.2)}>
        <rect x={-200} y={-80} width={400} height={160} rx={14} fill={P.gold} stroke={P.ink} strokeWidth={7} />
        <T maxW={360} y={-12} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.ink}>ДИРЕКТОР:</T>
        <T maxW={360} y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.ink}>ВЛАД, 19 ЛЕТ</T>
      </g>
      {lt >= lawAt && <Plate x={540} y={300} text="ФИРМА НА ТВОЁ ИМЯ — ТОЖЕ СТАТЬЯ" s={pop(after(lt, lawAt, 0.4))} rot={-3} fill={P.terracotta} size={48} />}
    </svg>
  );
};
