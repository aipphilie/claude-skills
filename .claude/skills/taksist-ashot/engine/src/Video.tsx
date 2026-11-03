import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {FPS, after, ampAt, blink, clamp, cue, easeInOut, easeOut, lerp, mouthShape, noise, story, freezeT, timeline} from './lib';
import {Ashot, AshotState, ArmPose} from './characters/Ashot';
import {RiderFigure, RIDERS, Emotion} from './characters/Rider';
import {CabinBack, CabinFront, DriverSeat} from './scene/Cabin';
import {Buttons, HouseRibbon, MoneyCard, Stamp400} from './overlays/Graphics';
import {Subtitles} from './overlays/Subtitles';
import * as SH from './boards/Shots';

// врезки-ракурсы поверх салона (story.json → inserts)
const inserts = (story.inserts || []).map((x: any) => ({...x, a: cue(x.from), b: cue(x.to)}));
const renderInsert = (name: string, t: number, lt: number, dur: number) => {
  const k = clamp(lt / dur);
  switch (name) {
    case 'exterior': return <SH.ShotExterior t={t} />;
    case 'phone': return <SH.ShotPhone />;
    case 'meterCrazy': { const kk = easeInOut(clamp((t - cue('cross')) / (cue('n12') - cue('cross')))); return <SH.ShotMeter mode="crazy" value={lerp(287, 12000000, kk)} />; }
    case 'meterRewind': return <SH.ShotMeter mode="rewind" value={lerp(12000000, 9000000, easeOut(k))} />;
    case 'meterFare': return <SH.ShotMeter mode="fare" value={400} />;
    case 'aging': { const st = Math.min(2, Math.floor(k * 3)); return <SH.ShotAging stage={st} year={Math.round(lerp(2026, 2046, easeOut(k)))} />; }
    case 'nav': return <SH.ShotNav pick={t >= cue('poke')} hand={easeOut(clamp((t - cue('navIn')) / (cue('poke') - cue('navIn'))))} />;
    case 'topdown': return <SH.ShotTopDown k={easeInOut(k)} />;
  }
  return null;
};

// шрифт
const fontHandle = typeof window !== 'undefined' ? delayRender('fonts') : 0;
if (typeof window !== 'undefined') {
  const faces = [600, 800, 900].flatMap((w) => ['cyrillic', 'latin'].map((sub) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${sub}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(fontHandle));
}

const shots = story.shots.map((s: any) => ({...s, t: cue(s.at)}));
const camera = (t: number) => {
  let i = 0; while (i + 1 < shots.length && t >= shots[i + 1].t) i++;
  const s = shots[i], p = shots[i - 1];
  let [x, y, z] = s.cam;
  if (p && s.move) { const k = easeInOut((t - s.t) / (s.move / FPS)); x = lerp(p.cam[0], x, k); y = lerp(p.cam[1], y, k); z = lerp(p.cam[2], z, k); }
  const dur = (shots[i + 1]?.t ?? timeline.total) - s.t;
  z *= 1 + (s.drift || 0.015) * clamp((t - s.t) / dur);
  let sh = 0; for (const q of shots) if (q.shake && t >= q.t) sh = Math.max(sh, q.shake * Math.exp(-(t - q.t) * 6));
  return {x, y, z, sh, i};
};

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const real = frame / FPS;
  const tf = freezeT();
  const t = Math.min(real, tf);          // после стоп-кадра время замирает
  const cam = camera(t);
  const vib = Math.sin(t * 31) * 1.6 + Math.sin(t * 13.3) * 1.2; // тряска салона
  const shx = noise(t, 1) * cam.sh, shy = noise(t + 9, 1.3) * cam.sh;

  // ---- Ашот
  const turn = easeOut(after(t, cue('turn'), 0.28));
  const brow = easeOut(after(t, cue('brow'), 0.45)) * (1 - turn * 0.5);
  const armSeq: [number, ArmPose][] = [[0, 'rest'], [cue('explain'), 'up'], [cue('pay'), 'palm']];
  let ai = 0; while (ai + 1 < armSeq.length && t >= armSeq[ai + 1][0]) ai++;
  const arm = {from: armSeq[Math.max(0, ai - 1)][1], to: armSeq[ai][1], k: ai === 0 ? 1 : easeOut(after(t, armSeq[ai][0], 0.3))};
  const aAmp = ampAt('ashot', t);
  const winkK = Math.sin(clamp(after(t, cue('remember') + 0.55, 0.45)) * Math.PI);
  const ashot: AshotState = {
    t, turn, browL: brow, browR: brow * 0.25 + turn * 0.15 + winkK * 0.3, blink: blink(t, 1), wink: winkK,
    mouth: mouthShape(aAmp), smirk: turn, look: turn < 0.5 ? [-0.6, -0.6] : [0.55, -0.1],
    arm, poke: 0,
  };
  // ---- пассажир
  const pAmp = ampAt('passenger', t);
  const shockK = Math.max(
    easeOut(after(t, cue('shock'), 0.12)) * (1 - easeOut(after(t, cue('explain') + 0.6, 0.5))),
    easeOut(after(t, cue('n400'), 0.15)),
  );
  const worry = clamp(easeOut(after(t, cue('n12'), 0.3)) * 0.7 + (t > cue('explain') ? 0.3 : 0));
  const pass: Emotion = {smile: 0,
    blink: blink(t, 4), mouth: mouthShape(pAmp), shock: shockK, worry,
    look: t < cue('turn') ? [0.4, 0] : [-0.7, 0.1], sweat: easeOut(after(t, cue('years'), 0.4)) * (t < cue('pay') ? 1 : 0),
  };
  const fare = t < cue('n400') ? 287 + t * 4 : 400;
  const fl = Math.max(...shots.filter((s: any) => s.whoosh).map((s: any) => 1 - clamp(Math.abs(t - s.t) * 8)), ...inserts.map((x: any) => 1 - clamp(Math.abs(t - x.a) * 10)), 0);
  const ins = inserts.find((x: any) => t >= x.a && t < x.b);
  const insShake = ins && ins.shot === 'meterCrazy' && t > cue('n12') ? 14 * Math.exp(-(t - cue('n12')) * 5) : 0;
  const freezeFlash = real >= tf ? 1 - clamp((real - tf) * 3) : 0;

  return (
    <AbsoluteFill style={{background: P.cabin}}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute'}}>
        <g transform={`translate(${540 + shx},${960 + shy}) scale(${cam.z}) translate(${-cam.x},${-cam.y + vib})`}>
          <CabinBack t={t} />
          <g transform={`translate(720,1000) rotate(${noise(t * 0.3, 0.2) * 1.2})`}><RiderFigure r={RIDERS[0]} e={pass} /></g>
          <DriverSeat />
          <g transform={`translate(330,1090) rotate(${lerp(-3, 2, turn)})`}><Ashot s={ashot} /></g>
          <CabinFront t={t} ashot={ashot} mirrorOn={1 - turn} fare={fare} shake={cam.sh / 20} />
        </g>
        {/* виньетка */}
        <defs>
          <radialGradient id="vig" cx="0.5" cy="0.5" r="0.75">
            <stop offset="0.6" stopColor="#000" stopOpacity={0} />
            <stop offset="1" stopColor="#1A0E08" stopOpacity={0.55} />
          </radialGradient>
        </defs>
        <rect width={1080} height={1920} fill="url(#vig)" />
        <Stamp400 t={t} />
      </svg>
      {ins && (
        <AbsoluteFill style={{background: '#1D1A1F', overflow: 'hidden'}}>
          <div style={{position: 'absolute', inset: 0, transform: `translate(${noise(t, 1) * insShake}px,${noise(t + 5, 1.2) * insShake}px) scale(${1.02 + 0.06 * clamp((t - ins.a) / (ins.b - ins.a))})`}}>
            <SH.SubCtx.Provider value={false}>
              <style>{'.ins > svg{width:1080px;height:1920px;display:block}'}</style>
              <div className="ins">{renderInsert(ins.shot, t, t - ins.a, ins.b - ins.a)}</div>
            </SH.SubCtx.Provider>
          </div>
        </AbsoluteFill>
      )}
      <Subtitles t={t} />
      <AbsoluteFill style={{background: '#FFF6E6', opacity: fl * 0.35 + freezeFlash * 0.8}} />
      {real >= tf && <AbsoluteFill style={{boxShadow: `inset 0 0 0 ${18 * (1 - freezeFlash * 0.5)}px ${P.cream}`}} />}
      <Audio src={staticFile('mix.wav')} />
    </AbsoluteFill>
  );
};
