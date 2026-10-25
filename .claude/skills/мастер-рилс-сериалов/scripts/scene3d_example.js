// 3D test: «Ночью минус пятьдесят два. Генератор встал.» — low-poly, flat-shaded, The Long Dark mood.
// Three.js draws the world; the existing 2D layer (paint texture, grain, HUD, captions) goes on top.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const T0 = 78.7;                                   // excerpt start on the episode-2 timeline
const T_OFF = PH['05.4'].s + 0.15;                 // «Генератор встал» — the lights die here
const gl = document.createElement('canvas'); gl.width = 1080; gl.height = 1920;
const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false);
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x1a3440, 0.006);
const camera = new THREE.PerspectiveCamera(48, 1080 / 1920, 0.5, 3000);

let seed = 11;
const R = () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const lam = (c, o = {}) => new THREE.MeshLambertMaterial(Object.assign({ color: c, flatShading: true }, o));

// ---- sky, stars, moon, aurora ----
scene.add(new THREE.Mesh(new THREE.SphereGeometry(2000, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: 'varying vec3 v; void main(){ v = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
  fragmentShader: `varying vec3 v; void main(){ float h = clamp(v.y,0.,1.);
    vec3 c = mix(vec3(.17,.31,.35), vec3(.05,.12,.15), smoothstep(0.,.16,h)); c = mix(c, vec3(.015,.035,.055), smoothstep(.16,.75,h));
    gl_FragColor = vec4(c,1.); }`
})));
{ const p = []; for (let i = 0; i < 1600; i++) { const a = R() * Math.PI * 2, y = .12 + R() * .88, r = Math.sqrt(1 - y * y); p.push(Math.cos(a) * r * 1900, y * 1900, Math.sin(a) * r * 1900); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xdfe9ec, size: 2, sizeAttenuation: false, fog: false }))); }
{ const m = new THREE.Mesh(new THREE.CircleGeometry(38, 24), new THREE.MeshBasicMaterial({ color: 0xdfe6e3, fog: false }));
  m.position.set(-500, 700, -1500); m.lookAt(0, 0, 0); scene.add(m); }
const aurora = [];
for (let k = 0; k < 3; k++) {
  const geo = new THREE.PlaneGeometry(1800, 420, 90, 1), pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), a = x / 1800 * 1.6 - .8 + k * .3;
    pos.setXYZ(i, Math.sin(a) * 1500, pos.getY(i) + 330 + k * 70 + Math.sin(x * .004 + k) * 50, -Math.cos(a) * 1500 + 200); }
  const mat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, fog: false,
    uniforms: { t: { value: 0 }, k: { value: k } },
    vertexShader: 'varying vec2 u; void main(){ u = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
    fragmentShader: `uniform float t; uniform float k; varying vec2 u;
      void main(){ float curtain = .55 + .45 * sin(u.x * 60. + t * .7 + k * 2.) * sin(u.x * 17. - t * .4);
        float a = smoothstep(0.,.15,u.y) * (1. - smoothstep(.15,1.,u.y)) * curtain * (.16 - k * .03);
        gl_FragColor = vec4(vec3(.37,.75,.56) * a, a); }` });
  const m = new THREE.Mesh(geo, mat); scene.add(m); aurora.push(mat);
}

// ---- light ----
scene.add(new THREE.HemisphereLight(0x6f97a6, 0x0b1418, 1.4));
const moon = new THREE.DirectionalLight(0xa9c6d4, 1.6); moon.position.set(-300, 420, -500); scene.add(moon);

// ---- ground: low-poly snow, flattened around the station ----
{ const g = new THREE.PlaneGeometry(2400, 2400, 140, 140); g.rotateX(-Math.PI / 2); const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), d = Math.hypot(x, z);
    let y = Math.sin(x * .011) * 3 + Math.cos(z * .013) * 3 + Math.sin((x + z) * .03) * 1.2 + (R() - .5) * 1.4;
    y *= THREE.MathUtils.smoothstep(d, 30, 110); p.setY(i, y); }
  g.computeVertexNormals(); scene.add(new THREE.Mesh(g, lam(0xaec2c9))); }

// ---- mountains: faceted, snow on the upper faces ----
for (let i = 0; i < 22; i++) {
  const a = -Math.PI * .95 + R() * Math.PI * 1.25, d = 650 + R() * 600, h = 160 + R() * 260, r = 140 + R() * 160;
  let g = new THREE.ConeGeometry(r, h, 5 + (R() * 3 | 0), 3).toNonIndexed(); const p = g.attributes.position, col = [];
  for (let v = 0; v < p.count; v++) { if (p.getY(v) < h / 2 - 1) { p.setX(v, p.getX(v) + (R() - .5) * r * .35); p.setZ(v, p.getZ(v) + (R() - .5) * r * .35); } }
  for (let f = 0; f < p.count; f += 3) { const yy = (p.getY(f) + p.getY(f + 1) + p.getY(f + 2)) / 3 / h + .5, c = new THREE.Color(yy > .62 ? 0xd3dfe2 : yy > .5 ? 0x7e98a0 : 0x2a464f); for (let k = 0; k < 3; k++) col.push(c.r, c.g, c.b); }
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, lam(0xffffff, { vertexColors: true })); m.position.set(Math.sin(a) * d, h / 2 - 8, -Math.cos(a) * d); scene.add(m);
}

// ---- pines: instanced, snow on top tiers ----
{ const tiers = [], snow = [];
  for (let k = 0; k < 4; k++) { const c = new THREE.ConeGeometry(2.6 - k * .55, 3.4, 6); c.translate(0, 2.6 + k * 2.1, 0); tiers.push(c);
    const s = new THREE.ConeGeometry(1.3 - k * .25, 1.2, 6); s.translate(-.3, 3.9 + k * 2.1, .2); snow.push(s); }
  const trunk = new THREE.CylinderGeometry(.25, .3, 2, 5); trunk.translate(0, 1, 0); tiers.push(trunk);
  const gT = mergeGeometries(tiers), gS = mergeGeometries(snow), N = 2600;
  const mT = new THREE.InstancedMesh(gT, lam(0x18312f), N), mS = new THREE.InstancedMesh(gS, lam(0xc9d8dc), N), o = new THREE.Object3D(); let n = 0;
  while (n < N) { const a = R() * Math.PI * 2, d = 70 + Math.pow(R(), .6) * 600, x = Math.cos(a) * d, z = Math.sin(a) * d;
    if (z > 0 && Math.abs(x) < 120 && z < 260) continue;           // keep the camera's approach clear
    const s = .7 + R() * 1.4; o.position.set(x, 0, z); o.rotation.y = R() * 6; o.scale.set(s, s * (.8 + R() * .5), s); o.updateMatrix(); mT.setMatrixAt(n, o.matrix); mS.setMatrixAt(n, o.matrix); n++; }
  scene.add(mT, mS); }

// ---- the station ----
const st = new THREE.Group(); scene.add(st);
const box = (w, h, d, c, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), lam(c)); m.position.set(x, y, z); st.add(m); return m; };
box(14, 6, 9, 0x22343b, 0, 3, 0);
{ // gable roof: a triangle extruded along the building, snow on top
  const sh = new THREE.Shape(); sh.moveTo(-5.4, 0); sh.lineTo(5.4, 0); sh.lineTo(0, 3.2); sh.closePath();
  const g = new THREE.ExtrudeGeometry(sh, { depth: 15, bevelEnabled: false }); g.translate(0, 0, -7.5); g.rotateY(Math.PI / 2);
  const roof = new THREE.Mesh(g, lam(0xd5e0e2)); roof.position.set(0, 6, 0); st.add(roof); }
box(1.6, 3.6, .3, 0x0c1418, 4.5, 1.8, 4.6);
box(1, 3, 1, 0x101a1e, 3.5, 8.6, -1);
const winMat = new THREE.MeshBasicMaterial({ color: 0xffb04a, fog: false }), wins = [];
for (const x of [-4, -.8]) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.3), winMat); w.position.set(x, 3.6, 4.52); st.add(w); wins.push(w); }
const shed = box(5, 3.6, 4.5, 0x1d2c31, 11.5, 1.8, -2); box(5.8, .5, 5.2, 0xd5e0e2, 11.5, 3.8, -2);
const shedWinMat = new THREE.MeshBasicMaterial({ color: 0xffc070, fog: false }); { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .9), shedWinMat); w.position.set(11.5, 2.2, .27); st.add(w); }
box(.4, 2.5, .4, 0x0c1418, 13.4, 4.8, -3);
for (const [x, z] of [[-14, 2], [-16, 4], [6, 5.5], [-6, -6]]) { const d = new THREE.Mesh(new THREE.SphereGeometry(3, 7, 4), lam(0xbfd0d5)); d.scale.set(1.6, .45, 1); d.position.set(x, 0, z); st.add(d); }
// mast with guy wires and a blinking red light
box(.35, 28, .35, 0x0e181c, -11, 14, -3);
const red = new THREE.Mesh(new THREE.SphereGeometry(.45, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff3b2f })); red.position.set(-11, 28.3, -3); st.add(red);
{ const pts = []; for (const [x, z] of [[-18, -3], [-11, 4], [-5, -8]]) pts.push(-11, 26, -3, x, 0, z);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3)); st.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0x0e181c }))); }
// instrument booth + rope line on three poles
box(2, 1.8, 1.6, 0xb7c8cc, -26, 2.2, 6); for (const dx of [-.8, .8]) box(.15, 1.4, .15, 0x0e181c, -26 + dx, .7, 6);
{ const pts = [new THREE.Vector3(-7, 2.2, 3)]; for (const x of [-12, -17, -22]) { box(.18, 2.4, .18, 0x0e181c, x, 1.2, 4.2); pts.push(new THREE.Vector3(x + 2.5, 1.9, 3.9), new THREE.Vector3(x, 2.3, 4.2)); }
  pts.push(new THREE.Vector3(-25, 2.2, 5.6)); st.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x4a3a28 }))); }
const warm = new THREE.PointLight(0xffa04a, 260, 60, 1.6); warm.position.set(-2, 3.5, 7); scene.add(warm);
const shedLight = new THREE.PointLight(0xffb060, 90, 25, 1.6); shedLight.position.set(11.5, 2.5, 2); scene.add(shedLight);

// ---- smoke + snow particles ----
function dotTex() { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); }
const DOT = dotTex();
// warm halos around the lit windows (they die with the generator)
const haloMat = new THREE.SpriteMaterial({ map: DOT, color: 0xffa040, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false, opacity: .55 });
for (const [x, y, z, s] of [[-4, 3.6, 4.9, 7], [-.8, 3.6, 4.9, 7], [11.5, 2.2, .6, 4.5]]) { const h = new THREE.Sprite(haloMat); h.position.set(x, y, z); h.scale.set(s, s, 1); scene.add(h); }
const SN = 9000, snowBase = new Float32Array(SN * 4), snowPos = new Float32Array(SN * 3);
for (let i = 0; i < SN; i++) { snowBase[i * 4] = (R() - .5) * 260; snowBase[i * 4 + 1] = R() * 90; snowBase[i * 4 + 2] = (R() - .5) * 320 + 60; snowBase[i * 4 + 3] = .6 + R() * .8; }
const snowGeo = new THREE.BufferGeometry(); snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPos, 3));
const snowMat = new THREE.PointsMaterial({ color: 0xe6eef0, size: .5, map: DOT, transparent: true, depthWrite: false, opacity: .9 });
scene.add(new THREE.Points(snowGeo, snowMat));
const SMK = 60, smokeBase = new Float32Array(SMK * 2), smokePos = new Float32Array(SMK * 3);
for (let i = 0; i < SMK; i++) { smokeBase[i * 2] = R(); smokeBase[i * 2 + 1] = R() < .5 ? 0 : 1; }
const smokeGeo = new THREE.BufferGeometry(); smokeGeo.setAttribute('position', new THREE.BufferAttribute(smokePos, 3));
const smokeMat = new THREE.PointsMaterial({ color: 0x8a9aa0, size: 3.2, map: DOT, transparent: true, depthWrite: false, opacity: .35 });
scene.add(new THREE.Points(smokeGeo, smokeMat));

// ---- camera path: from high above the taiga down to the station ----
const path = new THREE.CatmullRomCurve3([new THREE.Vector3(110, 42, 230), new THREE.Vector3(70, 26, 140), new THREE.Vector3(38, 13, 66), new THREE.Vector3(22, 6.5, 36)]);
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);

function render3d(t) {
  const lt = t - T0, off = t >= T_OFF, k = Math.min(1, Math.max(0, (t - T_OFF) / .45));
  // lights die with a flicker
  const flick = !off ? 1 : k < 1 ? (Math.sin(t * 90) > 0 ? .9 : .15) * (1 - k) : 0;
  winMat.color.setRGB(1 * flick + .05, .69 * flick + .06, .29 * flick + .08); shedWinMat.color.copy(winMat.color);
  warm.intensity = 260 * flick; shedLight.intensity = 90 * (off ? 0 : 1); haloMat.opacity = .55 * flick;
  red.visible = (t % 1.4) < .2;
  scene.fog.density = .0032 + (t > PH['06.0'].s ? .004 * ease((t - PH['06.0'].s) / 1.5) : 0);
  for (const m of aurora) m.uniforms.t.value = t;
  const wind = 8 + (t > PH['06.0'].s ? 14 * ease((t - PH['06.0'].s) / 1.5) : 0);
  for (let i = 0; i < SN; i++) { const b = i * 4, sp = snowBase[b + 3];
    snowPos[i * 3] = ((snowBase[b] + t * wind * sp + 130) % 260 + 260) % 260 - 130;
    snowPos[i * 3 + 1] = ((snowBase[b + 1] - t * 3.2 * sp) % 90 + 90) % 90;
    snowPos[i * 3 + 2] = snowBase[b + 2] + Math.sin(t * .7 + i) * .6; }
  snowGeo.attributes.position.needsUpdate = true;
  for (let i = 0; i < SMK; i++) { const p = (smokeBase[i * 2] + t * .18) % 1, shed = smokeBase[i * 2 + 1], alive = shed && off ? 0 : 1;
    const x0 = shed ? 13.4 : 3.5, y0 = shed ? 6 : 10, z0 = shed ? -3 : -1;
    smokePos[i * 3] = x0 + p * 14 + Math.sin(p * 6 + i) * .8; smokePos[i * 3 + 1] = alive ? y0 + p * 16 : -999; smokePos[i * 3 + 2] = z0 + p * 3; }
  smokeGeo.attributes.position.needsUpdate = true;
  const u = ease(lt / 8.6) * .97 + .015; camera.position.copy(path.getPoint(u));
  camera.lookAt(0, THREE.MathUtils.lerp(30, 9, u), 0);   // keep the sky and aurora in the upper part of the frame
  renderer.render(scene, camera);
}

window.renderFrame = function (t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  // hybrid: key 2D inserts of the episode keep their slots, 3D only replaces the wide shots
  const ins = SHOTS.find(s => t >= s.s && t < s.e && s.s >= 85.4);
  if (ins) { ctx.save(); ins.f(ctx, t); ctx.restore(); ctx.setTransform(1, 0, 0, 1, 0, 0); finish(t); stickerS(t, T0 - 1, 'Ночь 49', '−52°'); captions4(t); return; }
  render3d(t); ctx.drawImage(gl, 0, 0);
  if (t >= T_OFF && t < T_OFF + .5) { ctx.fillStyle = `rgba(0,0,0,${.35 * (1 - (t - T_OFF) / .5)})`; ctx.fillRect(0, 0, W, H); }
  finish(t);
  stickerS(t, T0 - 1, 'Ночь 49', '−52°');
  thermoTag(t, T0 - 1, lerp(-38, -52, ease((t - (PH['05.3'].s)) / 2)), Math.round(14 + 10 * ease((t - PH['06.0'].s) / 1.5)));
  captions4(t);
  if (t < T0 + .25) { ctx.fillStyle = `rgba(0,0,0,${1 - (t - T0) / .25})`; ctx.fillRect(0, 0, W, H); }
};
window.ready = window.ready.then(() => true);
window.__is3d = true;   // the renderer waits for this so no frame is drawn by the old 2D renderFrame
