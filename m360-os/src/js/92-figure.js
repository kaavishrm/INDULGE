/* module: figure. The characters in 3D, made only of primitives (sphere, capsule, cylinder, torus, lathe,
   rounded box), coloured per vertex from M.cast.paint and read from three only through T, the namespace
   M.office3d.load() hands over.

     M.figure.build(T, look, {founder, lod, live, acc})  -> rig {root, setPose(name, t, p), blink(on), talk(level), tris, calls, dispose}
     M.figure.crowd(T, items)                            -> ONE Mesh of every still person (cached per figure)
     M.figure.crowd.async(T, items, {budget})            -> Promise of the same, built one figure per idle chunk
     M.figure.coo(T, {lod, dark})                        -> rig {root, setState(s), setYaw(r), setAccent(dark), listen(on), sleep(on), update(dt), dispose}

   A person is one mesh: every part is tagged with its joint (neck, shoulders, elbows, hips, knees, ankles) and
   a pose moves the vertices on the CPU, so a walking person is one draw call and a seated crowd bakes with the
   same code. Kaavish (founder, or live) keeps his eyes and his mouth as their own small meshes, so he blinks and
   talks without touching the rest. Units are metres: feet at y 0, facing +z, about 1.30 m tall, head radius .21.
   A crowd item sits at plan x, y in cm (world x = x / 100, world z = y / 100) and turns by h degrees. */
'use strict';
(function () {
  const R = 0.21, HY = 1.05;
  /* the joints: [parent, x, y, z] at rest, every rest rotation zero */
  const JOINTS = [
    [-1, 0, 0, 0],            /* 0 root */
    [0, 0, 0, 0],             /* 1 body: the torso, the pelvis */
    [1, 0, 0.86, 0],          /* 2 head, at the neck */
    [1, -0.196, 0.765, 0],    /* 3 left shoulder */
    [3, 0, -0.165, 0],        /* 4 left elbow */
    [1, 0.196, 0.765, 0],     /* 5 right shoulder */
    [5, 0, -0.165, 0],        /* 6 right elbow */
    [1, -0.086, 0.42, 0],     /* 7 left hip */
    [7, 0, -0.2, 0],          /* 8 left knee */
    [8, 0, -0.16, 0],         /* 9 left ankle */
    [1, 0.086, 0.42, 0],      /* 10 right hip */
    [10, 0, -0.2, 0],         /* 11 right knee */
    [11, 0, -0.16, 0]         /* 12 right ankle */
  ];
  const J = {root: 0, body: 1, head: 2, shL: 3, elL: 4, shR: 5, elR: 6, hipL: 7, knL: 8, anL: 9, hipR: 10, knR: 11, anR: 12};
  const NJ = JOINTS.length;
  /* rest pivots in figure space */
  const PIVOT = [];
  for (let j = 0; j < NJ; j++) {
    const [p, x, y, z] = JOINTS[j];
    const b = p < 0 ? [0, 0, 0] : PIVOT[p];
    PIVOT.push([b[0] + x, b[1] + y, b[2] + z]);
  }
  const SHIN = 0.16, THIGH = 0.2, ANKLE_Y = 0.06, STRIDE = 0.55;

  const cast = () => M.cast;
  /* one shared matte vinyl per three namespace, so every person is the same material */
  const mats = new WeakMap();
  function material(T) {
    let m = mats.get(T);
    if (!m) { m = new T.MeshStandardMaterial({vertexColors: true, roughness: 0.55, metalness: 0}); mats.set(T, m); }
    return m;
  }
  /* sRGB bytes to the linear floats a vertex colour wants */
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const linear = c => [lin(c[0]), lin(c[1]), lin(c[2])];
  const colourOf = (T, c) => new T.Color().setRGB(c[0] / 255, c[1] / 255, c[2] / 255, T.SRGBColorSpace);

  /* ---------- parts ---------- */
  function placed(T, g, at, rot, scl) {
    const m = new T.Matrix4();
    m.compose(new T.Vector3(...(at || [0, 0, 0])), new T.Quaternion().setFromEuler(new T.Euler(...(rot || [0, 0, 0]))), new T.Vector3(...(scl || [1, 1, 1])));
    g.applyMatrix4(m);
    return g;
  }
  /* a part: geometry in figure space, a colour (or a colour per vertex), the joint it rides on */
  const part = (T, g, c, j, at, rot, scl) => ({g: placed(T, g, at, rot, scl), c, j});

  /* the head: a sphere a touch wider at the cheeks with a soft chin, pushed toward the face the look names */
  const HEAD = {round: [1, 1, 0.95], oval: [0.94, 1.05, 0.95], long: [0.9, 1.1, 0.93], soft: [0.98, 1.02, 0.95], heart: [0.98, 1.04, 0.95]};
  function shapeHead(T, g, face, r) {
    const p = g.attributes.position, v = new T.Vector3();
    const s = HEAD[face] || HEAD.oval;
    for (let i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      const ny = v.y / r;
      if (face === 'soft') {
        const n = v.clone().normalize();
        const k = Math.pow(Math.pow(Math.abs(n.x), 3) + Math.pow(Math.abs(n.y), 3) + Math.pow(Math.abs(n.z), 3), -1 / 3);
        v.multiplyScalar(0.5 + 0.5 * k * 0.92);
      }
      if (face === 'heart') v.x *= 1 + 0.08 * ny - (ny < -0.4 ? 0.12 * (-ny - 0.4) : 0);
      v.x *= 1 + 0.04 * Math.max(0, 1 - Math.abs(ny + 0.15) * 2);
      if (ny < -0.45 && v.z > 0) v.z *= 1 + 0.05 * (-ny - 0.45);
      v.set(v.x * s[0], v.y * s[1] * 1.03, v.z * s[2]);
      p.setXYZ(i, v.x, v.y, v.z);
    }
    g.computeVertexNormals();
    return g;
  }
  /* cut a face window out of a shell (a scarf, a bob, coils), so it frames the face and covers the crown */
  function faceWindow(T, g, w, top, low) {
    const p = g.attributes.position, idx = g.index.array, keep = [];
    const a = new T.Vector3(), b = new T.Vector3(), c = new T.Vector3();
    for (let i = 0; i < idx.length; i += 3) {
      a.fromBufferAttribute(p, idx[i]); b.fromBufferAttribute(p, idx[i + 1]); c.fromBufferAttribute(p, idx[i + 2]);
      const m = a.add(b).add(c).normalize();
      const inside = m.z > 0 && (m.x / w) ** 2 + ((m.y - (top + low) / 2) / ((top - low) / 2)) ** 2 < 1;
      if (!inside) keep.push(idx[i], idx[i + 1], idx[i + 2]);
    }
    g.setIndex(keep);
    return g;
  }

  /* parts(T, look, o) -> {main: [part], eyes: [part], mouth: [part], sticker, look, p}. Every number is a
     table value or a constant; the look holds ids only (M.cast.clean) */
  function parts(T, raw, o) {
    const opts = o || {};
    const C = cast();
    const look = C.clean(raw);
    const p = C.paint(look, !!opts.founder);
    const lod = opts.lod ? 1 : 0;
    /* segment counts: LOD0 for the close views and the people who move, LOD1 (16 by 12 heads, no glints or
       lashes) for phones and the whole floor, and a finer LOD0 for Kaavish (and any live rig) in close views */
    const live = !lod && !!(opts.live || opts.founder);
    const Q = lod ? {head: [16, 12], cap: [10, 4], shell: [12, 7], ball: [5, 4], tiny: [4, 3], eye: [6, 4], fringe: [6, 4], shoe: [8, 4], curl: [4, 3], curls: 8, cr: 5, cc: 1, lathe: 8, tr: 3, tt: 8, limb: 6, fine: 4}
      : live ? {head: [32, 24], cap: [28, 10], shell: [28, 16], ball: [12, 8], tiny: [8, 6], eye: [16, 12], fringe: [16, 10], shoe: [14, 9], curl: [8, 6], curls: 20, cr: 12, cc: 3, lathe: 28, tr: 5, tt: 20, limb: 12, fine: 8}
      : {head: [24, 16], cap: [20, 8], shell: [20, 12], ball: [10, 7], tiny: [6, 4], eye: [12, 8], fringe: [12, 8], shoe: [12, 8], curl: [7, 5], curls: 16, cr: 10, cc: 2, lathe: 20, tr: 4, tt: 16, limb: 10, fine: 6};
    const hs = HEAD[look.face] || HEAD.oval;
    const RX = R * hs[0] * 1.03, RY = R * hs[1] * 1.03, RZ = R * hs[2];
    const front = (x, y) => RZ * Math.sqrt(Math.max(0.02, 1 - (x / RX) ** 2 - (y / RY) ** 2));
    const main = [], eyes = [], mouth = [];
    const add = (g, c, j, at, rot, scl) => { const q = part(T, g, c, j, at, rot, scl); main.push(q); return q; };
    const covered = look.head === 'scarf' || look.head === 'turban';
    const ball = (r, s) => new T.SphereGeometry(r, s ? s[0] : Q.ball[0], s ? s[1] : Q.ball[1]);
    const caps = (r, len) => new T.CapsuleGeometry(r, len, Q.cc, Q.cr);
    /* a capsule from a to b in figure space (glasses temples, sideburns), so it hugs the head */
    const rod = (a, b, r, c, j) => {
      const d = new T.Vector3(b[0] - a[0], b[1] - a[1], b[2] - a[2]);
      const len = d.length();
      const g = new T.CapsuleGeometry(r, Math.max(0.001, len - 2 * r), 1, Q.fine);
      g.applyQuaternion(new T.Quaternion().setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()));
      g.translate((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2);
      const q = {g, c, j};
      main.push(q);
      return q;
    };

    /* head, ears, neck */
    add(shapeHead(T, new T.SphereGeometry(R, Q.head[0], Q.head[1]), look.face, R), p.skin, J.head, [0, HY, 0]);
    if (!covered) for (const sx of [-1, 1]) add(ball(0.047), p.skin, J.head, [sx * RX * 0.97, HY - 0.015, -0.01], 0, [0.42, 1, 0.72]);
    add(new T.CylinderGeometry(0.054, 0.06, 0.12, Q.limb, 1, true), p.skinShade, J.head, [0, 0.85, 0]);

    /* the face: ink beads with a glint, brows, a nose, a mouth, a whisper of cheek */
    const ex = 0.072, ey = 0.004;
    for (const sx of [-1, 1]) {
      const z = front(sx * ex, ey);
      const es = look.eyes === 'almond' ? [1.2, 0.82, 0.5] : look.eyes === 'sleepy' ? [1.05, 0.55, 0.5] : [0.92, 1.12, 0.5];
      eyes.push(part(T, ball(0.029, Q.eye), p.ink, J.head, [sx * ex, HY + ey, z - 0.008], 0, es));
      if (!lod && look.eyes !== 'sleepy') eyes.push(part(T, ball(0.0085, Q.tiny), p.white, J.head, [sx * ex - 0.009, HY + ey + 0.012, z + 0.006]));
      if (!lod && look.eyes === 'lashes') eyes.push(part(T, new T.CapsuleGeometry(0.004, 0.018, 2, 5), p.ink, J.head, [sx * (ex + 0.03), HY + ey + 0.022, z - 0.012], [0, 0, sx * 0.9]));
      if (look.brows !== 'none') {
        const w = look.brows === 'bold' ? 0.012 : look.brows === 'fine' ? 0.0055 : 0.0085;
        const tilt = look.brows === 'arched' ? sx * -0.32 : sx * -0.12;
        add(new T.CapsuleGeometry(w, 0.044, 1, Q.fine), p.brow, J.head, [sx * ex, HY + 0.068, front(sx * ex, 0.068) - 0.003], [0, sx * -0.28, Math.PI / 2 + tilt]);
      }
      if (!lod) add(ball(0.03, Q.tiny), p.cheek, J.head, [sx * 0.11, HY - 0.045, front(sx * 0.11, -0.045) - 0.012], 0, [1, 0.7, 0.4]);
    }
    const nz = front(0, -0.028);
    add(ball(0.022), p.skinShade, J.head, [0, HY - 0.028, nz - 0.007], 0, look.nose === 'long' ? [0.9, 1.35, 0.8] : look.nose === 'soft' ? [1.1, 0.85, 0.7] : [1, 0.8, 0.78]);
    const mz = front(0, -0.088);
    const arc = look.mouth === 'calm' ? 0.36 : 0.62;
    const mouthAt = [0, HY - 0.074 - (look.mouth === 'calm' ? 0.012 : 0), mz - 0.012];
    mouth.push(part(T, new T.TorusGeometry(0.031, look.mouth === 'grin' ? 0.0095 : 0.0068, Q.tr, Q.tt - 4, Math.PI * arc), p.lip, J.head, mouthAt, [0.25, 0, Math.PI + (Math.PI - Math.PI * arc) / 2]));
    if (look.bindi) add(ball(0.0075, Q.tiny), p.bindi, J.head, [0, HY + 0.078, front(0, 0.078) - 0.001], 0, [1, 1, 0.5]);
    if (look.stud && !lod) add(ball(0.005, Q.tiny), p.metal, J.head, [-0.017, HY - 0.036, nz - 0.003]);
    if (!covered && !lod && look.ears !== 'none') for (const sx of [-1, 1]) {
      if (look.ears === 'hoops') add(new T.TorusGeometry(0.018, 0.0035, 3, Q.tt - 4), p.metal, J.head, [sx * RX * 0.99, HY - 0.065, 0.004], [0, Math.PI / 2, 0]);
      else add(ball(0.008, Q.tiny), p.metal, J.head, [sx * RX * 1.0, HY - 0.048, 0.008]);
    }

    /* facial hair: bands of the head's own shape a hair's breadth out, a shade softer than the hair */
    const shell = (scale, t0, t1, ph0, ph1, c) => add(shapeHead(T, new T.SphereGeometry(R * scale, Q.cap[0], Q.cap[1], ph0, ph1, t0, t1), look.face, R * scale), c, J.head, [0, HY, 0]);
    const band = [Math.PI * 0.12, Math.PI * 0.76];
    if (look.facial === 'stubble') shell(1.006, Math.PI * 0.66, Math.PI * 0.3, band[0], band[1], C.mix(p.skin, p.hair, 0.22));
    if (look.facial === 'short' || look.facial === 'full') shell(look.facial === 'full' ? 1.045 : 1.022, Math.PI * 0.645, Math.PI * 0.33, band[0], band[1], p.beard);
    if (look.facial === 'full') add(ball(0.07), p.beard, J.head, [0, HY - 0.17, RZ * 0.58], 0, [1.05, 0.78, 0.8]);
    if (look.facial === 'goatee') add(ball(0.03), p.beard, J.head, [0, HY - 0.15, front(0, -0.15)], 0, [1, 1.1, 0.7]);
    if (look.facial === 'moustache' || look.facial === 'goatee' || look.facial === 'full' || look.facial === 'short') for (const sx of [-1, 1]) {
      add(new T.CapsuleGeometry(0.0095, 0.028, 1, Q.fine), p.beard, J.head, [sx * 0.02, HY - 0.056, mz - 0.003], [0, 0, Math.PI / 2 + sx * 0.28]);
    }

    /* hair: a soft cap tilted back so the hairline rides up the forehead, temples and a nape so it is never a
       bowl, and a fringe that shapes the front hairline */
    const h = covered ? 'none' : look.hair;
    /* under a cap, a beanie or a bucket hat the crown never shows: only the hair below the brim is built */
    const hat = look.head === 'cap' || look.head === 'beanie' || look.head === 'bucket';
    const capG = (scale, t1, tilt) => add(shapeHead(T, new T.SphereGeometry(R * scale, Q.cap[0], Q.cap[1], 0, Math.PI * 2, 0, Math.PI * t1), look.face, R * scale), p.hair, J.head, [0, HY + 0.004, -0.008], [tilt, 0, 0]);
    const nape = scale => add(shapeHead(T, new T.SphereGeometry(R * scale, Q.cap[0], Math.max(3, Q.cap[1] >> 1), Math.PI * 1.08, Math.PI * 0.84, Math.PI * 0.42, Math.PI * 0.26), look.face, R * scale), p.hair, J.head, [0, HY, -0.004]);
    /* sideburns: from the cap's edge down in front of the ear, hugging the head */
    const temples = () => { for (const sx of [-1, 1]) rod([sx * RX * 0.93, HY + 0.07, RZ * 0.3], [sx * RX * 0.97, HY - 0.02, RZ * 0.22], 0.016, p.hair, J.head); };
    const fringe = (x, y, z, rot, scl) => hat && y > 0.13 ? null : add(ball(0.1, Q.fringe), p.hair, J.head, [x, HY + y, z], rot, scl);
    if (h === 'buzz') { if (!hat) capG(1.016, 0.47, -0.3); nape(1.012); }
    if (['crop', 'side', 'quiff', 'curls', 'bun', 'ponytail', 'braid', 'waves', 'bob', 'long', 'coils'].indexOf(h) >= 0) { if (!hat) capG(1.06, 0.5, -0.27); nape(1.05); temples(); }
    if (h === 'crop') { fringe(0.012, 0.148, 0.112, [0.62, 0, -0.08], [1.6, 0.5, 0.78]); fringe(-0.07, 0.12, 0.13, [0.7, 0.3, 0.4], [0.7, 0.42, 0.6]); }
    if (h === 'side') { fringe(-0.04, 0.15, 0.11, [0.6, 0, 0.34], [1.75, 0.6, 0.82]); fringe(0.09, 0.13, 0.1, [0.6, -0.3, -0.5], [0.8, 0.45, 0.7]); }
    if (h === 'quiff') { fringe(-0.015, 0.17, 0.095, [0.5, 0, 0.18], [1.6, 0.66, 1.0]); fringe(0.035, 0.195, 0.035, [0.3, 0, -0.2], [1.1, 0.48, 0.9]); }
    if (h === 'curls') {
      const n = Q.curls;
      for (let i = 0; i < n; i++) {
        const y = 1 - (i + 0.5) / n * 0.68, a = i * 2.39996, s = Math.sqrt(1 - y * y);
        if (hat && y > 0.25) continue;
        add(ball(0.058, Q.curl), p.hair, J.head, [Math.cos(a) * s * RX * 1.05, HY + y * RY * 1.06, Math.sin(a) * s * RZ * 1.05 - 0.012]);
      }
    }
    if (h === 'coils') add(faceWindow(T, new T.SphereGeometry(0.29, Q.shell[0], Q.shell[1], 0, Math.PI * 2, 0, Math.PI * 0.66), 0.5, 0.2, -0.95), p.hair, J.head, [0, HY + 0.05, -0.02], 0, [1, 0.92, 0.95]);
    /* long hair falls round the back and the sides, open at the face on two clean edges */
    const fall = (scale, t1) => add(shapeHead(T, new T.SphereGeometry(R * scale, Q.shell[0], Q.shell[1], Math.PI * 0.71, Math.PI * 1.58, 0, Math.PI * t1), look.face, R * scale), p.hair, J.head, [0, HY, -0.006]);
    if (h === 'bob' || h === 'long') {
      fall(1.09, h === 'long' ? 0.8 : 0.68);
      fringe(0.02, 0.138, 0.118, [0.55, 0, -0.22], [1.8, 0.52, 0.8]);
    }
    if (h === 'long') add(new T.CapsuleGeometry(0.14, 0.2, Q.cc, Q.cr), p.hair, J.body, [0, HY - 0.21, -0.11], [0.1, 0, 0], [1.18, 1, 0.48]);
    if (h === 'waves') {
      fall(1.08, 0.72);
      for (const sx of [-1, 1]) add(ball(0.07), p.hair, J.head, [sx * RX * 0.95, HY - 0.1, -0.03]);
      fringe(-0.02, 0.14, 0.11, [0.6, 0, 0.25], [1.7, 0.5, 0.8]);
    }
    if (h === 'bun') { add(ball(0.078), p.hair, J.head, [0, HY + 0.22, -0.075]); fringe(0, 0.15, 0.1, [0.65, 0, 0], [1.5, 0.42, 0.7]); }
    if (h === 'ponytail') { add(new T.CapsuleGeometry(0.05, 0.17, Q.cc, Q.cr), p.hair, J.head, [0, HY - 0.02, -0.23], [0.45, 0, 0]); fringe(0.01, 0.148, 0.11, [0.62, 0, -0.1], [1.55, 0.45, 0.75]); }
    if (h === 'braid') { for (let i = 0; i < 5; i++) add(ball(0.045 - i * 0.004), p.hair, i < 2 ? J.head : J.body, [0.02, HY - 0.06 - i * 0.07, -0.19 - i * 0.012]); fringe(0.01, 0.148, 0.11, [0.62, 0, -0.1], [1.55, 0.45, 0.75]); }

    /* headwear */
    if (look.head === 'cap' || look.head === 'beanie' || look.head === 'bucket') add(shapeHead(T, new T.SphereGeometry(R * 1.08, Q.cap[0], Q.cap[1], 0, Math.PI * 2, 0, Math.PI * (look.head === 'beanie' ? 0.52 : 0.47)), look.face, R * 1.08), p.headwear, J.head, [0, HY + 0.012, -0.01], [-0.18, 0, 0]);
    if (look.head === 'cap') add(new T.CylinderGeometry(0.12, 0.12, 0.012, Q.tt), p.headwearDark, J.head, [0, HY + 0.078, 0.2], [0.18, 0, 0], [1, 1, 1.25]);
    if (look.head === 'beanie') add(new T.TorusGeometry(0.212, 0.024, Q.tr, Q.tt + 4), p.headwearLight, J.head, [0, HY + 0.035, -0.01], [Math.PI / 2 - 0.18, 0, 0], [RX / R, RZ / R, 1]);
    if (look.head === 'bucket') add(new T.CylinderGeometry(0.215, 0.285, 0.05, Q.tt + 4, 1, true), p.headwearDark, J.head, [0, HY + 0.062, -0.01], [-0.12, 0, 0]);
    if (look.head === 'scarf') {
      add(faceWindow(T, shapeHead(T, new T.SphereGeometry(R * 1.12, Q.shell[0], Q.shell[1], 0, Math.PI * 2, 0, Math.PI * 0.86), look.face, R * 1.12), 0.6, 0.5, -0.78), p.headwear, J.head, [0, HY, -0.004]);
      add(new T.CylinderGeometry(0.11, 0.22, 0.16, Q.tt, 1, true), p.headwear, J.body, [0, 0.86, -0.01]);
      add(new T.TorusGeometry(0.118, 0.02, Q.tr, Q.tt + 8), p.headwearLight, J.head, [0, HY - 0.02, RZ * 0.86], [-0.12, 0, 0], [RX / R * 1.02, 1.28, 0.7]);
    }
    if (look.head === 'turban') {
      add(shapeHead(T, new T.SphereGeometry(R * 1.06, Q.cap[0], Q.cap[1], 0, Math.PI * 2, 0, Math.PI * 0.5), look.face, R * 1.06), p.headwear, J.head, [0, HY + 0.02, -0.01], [-0.2, 0, 0]);
      [[0.19, 0.06, 0.1], [0.182, 0.11, -0.12], [0.16, 0.16, 0.14]].forEach(([rr, y, tz]) => add(new T.TorusGeometry(rr, 0.042, Q.tr, Q.tt + 4), p.headwear, J.head, [0, HY + y, -0.015], [Math.PI / 2 - 0.22, 0, tz], [RX / R, RZ / R * 1.02, 1]));
    }
    /* headphones: a system accessory for focus, never part of the look */
    if (opts.acc && opts.acc.indexOf('headphones') >= 0) {
      add(new T.TorusGeometry(R * 1.13, 0.014, 3, Q.tt, Math.PI), p.ink, J.head, [0, HY + 0.012, -0.01]);
      for (const sx of [-1, 1]) add(new T.CylinderGeometry(0.06, 0.06, 0.05, Q.tt), p.ink, J.head, [sx * R * 1.1, HY - 0.01, -0.01], [0, 0, Math.PI / 2]);
    }

    /* glasses: torus rims, or four capsules for a square or soft lens, a bridge, two temples */
    if (look.glasses !== 'none') {
      const gz = front(ex, ey) + 0.014;
      for (const sx of [-1, 1]) {
        const x = sx * ex;
        if (look.glasses === 'shades') add(new T.CylinderGeometry(0.038, 0.038, 0.004, Q.tt), p.lens, J.head, [x, HY + ey, gz], [Math.PI / 2, 0, 0]);
        if (look.glasses === 'round' || look.glasses === 'shades') add(new T.TorusGeometry(0.041, 0.0058, Q.tr, Q.tt + 2), p.frame, J.head, [x, HY + ey, gz]);
        else {
          const w = 0.047, hh = 0.036, t = look.glasses === 'soft' ? 0.0078 : 0.0062;
          add(new T.CapsuleGeometry(t, w * 2 - 2 * t, 1, Q.fine), p.frame, J.head, [x, HY + ey + hh, gz], [0, 0, Math.PI / 2]);
          add(new T.CapsuleGeometry(t * 0.9, w * 2 - 2 * t, 1, Q.fine), p.frame, J.head, [x, HY + ey - hh, gz], [0, 0, Math.PI / 2]);
          for (const ix of [-1, 1]) add(new T.CapsuleGeometry(t * 0.9, hh * 2 - 2 * t, 1, Q.fine), p.frame, J.head, [x + ix * w, HY + ey, gz]);
        }
        /* the temples follow the head; at LOD1 they are under a pixel, so the far crowd keeps its budget */
        const ty = HY + ey + 0.012, tz = gz - 0.006, tx = ex + (look.glasses === 'round' || look.glasses === 'shades' ? 0.041 : 0.047);
        if (!lod) {
          rod([sx * tx, ty, tz], [sx * RX * 0.96, ty, RZ * 0.42], 0.0042, p.frame, J.head);
          rod([sx * RX * 0.96, ty, RZ * 0.42], [sx * RX * 1.0, ty - 0.01, -0.01], 0.0042, p.frame, J.head);
        }
      }
      add(new T.CapsuleGeometry(0.0045, 0.03, 1, 4), p.frame, J.head, [0, HY + ey + 0.012, gz + 0.004], [0, 0, Math.PI / 2]);
    }

    /* the torso: a lathe flattened front to back; the waist is a doubled ring, so the trousers meet the top
       on a crisp line with no colour bleed. A kurta runs long */
    const kurta = look.top === 'kurta', dress = look.top === 'dress';
    const prof = kurta ? [[0, 0.24], [0.2, 0.25], [0.17, 0.44], [0.166, 0.46], [0.16, 0.6], [0.176, 0.72], [0.15, 0.79], [0.07, 0.83], [0, 0.835]]
      : [[0, 0.37], [0.15, 0.38], [0.165, 0.44], [0.165, 0.445], [0.165, 0.445], [0.166, 0.46], [0.16, 0.6], [0.176, 0.72], [0.15, 0.79], [0.07, 0.83], [0, 0.835]];
    const waist = kurta || dress ? -1 : 3;
    const torso = add(new T.LatheGeometry(prof.map(([x, y]) => new T.Vector2(x, y)), Q.lathe), p.top, J.body, 0, 0, [1, 1, 0.78]);
    if (waist >= 0) torso.c = (i, n) => (i % prof.length) <= waist ? p.bottom : p.top;
    if (look.top === 'crew') add(new T.TorusGeometry(0.062, 0.014, Q.tr, Q.tt), p.topDark, J.body, [0, 0.815, 0], [Math.PI / 2, 0, 0], [1, 0.85, 1]);
    if (look.top === 'hoodie') {
      add(new T.TorusGeometry(0.105, 0.045, Q.tr + 1, Q.tt), p.topDark, J.body, [0, 0.8, -0.03], [Math.PI / 2 - 0.4, 0, 0], [1.1, 1, 1]);
      for (const sx of [-1, 1]) add(new T.CapsuleGeometry(0.004, 0.08, 1, 4), p.chalk, J.body, [sx * 0.03, 0.72, 0.132], [0.15, 0, 0]);
    }
    if (look.top === 'shirt') for (const sx of [-1, 1]) add(new T.BoxGeometry(0.06, 0.012, 0.045), p.topLight, J.body, [sx * 0.035, 0.818, 0.06], [0.5, sx * -0.5, sx * -0.35]);
    if (look.top === 'blazer') {
      add(new T.CylinderGeometry(0.0, 0.072, 0.2, 3, 1), p.chalk, J.body, [0, 0.72, 0.112], [Math.PI, 0, 0], [1, 1, 0.35]);
      for (const sx of [-1, 1]) add(new T.BoxGeometry(0.032, 0.21, 0.012), p.topDark, J.body, [sx * 0.052, 0.71, 0.119], [0.12, 0, sx * 0.32]);
      /* the founder's one flame detail: a pocket square */
      if (p.accent) add(new T.BoxGeometry(0.036, 0.024, 0.012), p.accent, J.body, [-0.1, 0.668, 0.122], [0.12, 0, 0.12]);
    }
    if (kurta) add(new T.CylinderGeometry(0.064, 0.068, 0.035, Q.tt), p.topDark, J.body, [0, 0.832, 0]);
    if (dress || (look.bottom === 'skirt' && !kurta)) {
      const sp = [[0.0, 0.25], [0.26, 0.26], [0.2, 0.36], [0.166, 0.45], [0.0, 0.46]].map(([x, y]) => new T.Vector2(x, y));
      add(new T.LatheGeometry(sp, Q.lathe), dress ? p.top : p.bottom, J.body, 0, 0, [1, 1, 0.8]);
    }

    /* arms: an upper arm from the shoulder and a forearm from the elbow, a hand with a thumb. A short sleeve is
       its own piece over a bare arm, so its edge stays crisp */
    const short = look.top === 'tee' || dress;
    for (const sx of [-1, 1]) {
      const sh = sx < 0 ? J.shL : J.shR, el = sx < 0 ? J.elL : J.elR;
      const [x0, y0] = PIVOT[sh];
      if (short) {
        add(caps(0.047, 0.1), p.skin, sh, [x0, y0 - 0.075, 0]);
        add(caps(0.058, 0.05), p.top, sh, [x0, y0 - 0.045, 0]);
      } else add(caps(0.052, 0.1), p.top, sh, [x0, y0 - 0.075, 0]);
      const ye = y0 - 0.165;
      add(caps(short ? 0.044 : 0.049, 0.08), short ? p.skin : p.top, el, [x0, ye - 0.06, 0]);
      add(caps(0.037, 0.03), p.skin, el, [x0, ye - 0.165, 0.004], 0, [1, 1, 0.8]);
      add(ball(0.017, Q.tiny), p.skin, el, [x0 - sx * 0.026, ye - 0.15, 0.022]);
      if (look.watch && sx < 0) add(new T.TorusGeometry(0.047, 0.011, Q.tr, Q.tt - 4), p.accent && look.top !== 'blazer' ? p.accent : p.strap, el, [x0, ye - 0.115, 0], [Math.PI / 2, 0, 0]);
      if (look.pose === 'mug' && sx > 0 && !opts.noMug) add(new T.CylinderGeometry(0.036, 0.032, 0.085, Q.tt - 4), p.chalk, el, [x0, ye - 0.19, 0.06]);
    }
    /* legs: a thigh from the hip, a shin from the knee, the shoe from the ankle */
    const bare = dress || look.bottom === 'skirt' || look.bottom === 'shorts';
    for (const sx of [-1, 1]) {
      const hip = sx < 0 ? J.hipL : J.hipR, kn = sx < 0 ? J.knL : J.knR, an = sx < 0 ? J.anL : J.anR;
      const [x0, y0] = PIVOT[hip];
      add(caps(bare ? 0.06 : 0.066, 0.1), bare ? p.skin : p.bottom, hip, [x0, y0 - 0.09, 0]);
      if (look.bottom === 'shorts' && !dress) add(caps(0.069, 0.06), p.bottom, hip, [x0, y0 - 0.06, 0]);
      const yk = y0 - THIGH;
      add(caps(bare ? 0.056 : 0.062, 0.08), bare ? p.skin : p.bottom, kn, [x0, yk - 0.075, 0]);
      const ya = yk - SHIN;
      const lo = look.shoes === 'loafers' ? [0.95, 0.5, 1.6] : [1, 0.64, 1.6];
      if (look.shoes === 'boots') add(caps(0.068, 0.04), p.shoe, an, [x0, ya + 0.02, 0]);
      add(ball(0.075, Q.shoe), p.shoe, an, [x0, ya - 0.016, 0.038], 0, look.shoes === 'boots' ? [1, 0.62, 1.55] : lo);
      /* the sole: Kaavish's flame when there is no blazer to carry his detail */
      add(new T.SphereGeometry(0.076, Q.shoe[0], 2, 0, Math.PI * 2, Math.PI * 0.62, Math.PI * 0.22), p.accent && look.top !== 'blazer' ? p.accent : p.sole, an, [x0, ya - 0.022, 0.038], 0, look.shoes === 'boots' ? [1, 0.62, 1.55] : lo);
    }
    /* the starter's chest sticker: a small paper disc; the initials ride on it as a texture */
    const sticker = raw && raw.starter === true ? {initials: C.sticker(raw.initials), at: [0.066, 0.69, 0.142]} : null;
    return {main, eyes, mouth, mouthAt, eyeAt: [0, HY + ey, front(0, ey)], sticker, look, p};
  }

  /* ---------- the skin: rest vertices per joint, posed on the CPU ---------- */
  function pack(list) {
    let nv = 0, ni = 0;
    for (const q of list) { nv += q.g.attributes.position.count; ni += q.g.index ? q.g.index.count : q.g.attributes.position.count; }
    const pos = new Float32Array(nv * 3), nrm = new Float32Array(nv * 3), col = new Float32Array(nv * 3), joint = new Uint8Array(nv);
    const idx = nv > 65535 ? new Uint32Array(ni) : new Uint16Array(ni);
    let v = 0, k = 0;
    for (const q of list) {
      const g = q.g, P = g.attributes.position, N = g.attributes.normal, n = P.count;
      const pv = PIVOT[q.j];
      const flat = typeof q.c === 'function' ? null : linear(q.c);
      for (let i = 0; i < n; i++) {
        const o = (v + i) * 3;
        pos[o] = P.getX(i) - pv[0]; pos[o + 1] = P.getY(i) - pv[1]; pos[o + 2] = P.getZ(i) - pv[2];
        if (N) { nrm[o] = N.getX(i); nrm[o + 1] = N.getY(i); nrm[o + 2] = N.getZ(i); } else nrm[o + 1] = 1;
        const c = flat || linear(q.c(i, n));
        col[o] = c[0]; col[o + 1] = c[1]; col[o + 2] = c[2];
        joint[v + i] = q.j;
      }
      if (g.index) { const a = g.index.array; for (let i = 0; i < g.index.count; i++) idx[k++] = a[i] + v; } else for (let i = 0; i < n; i++) idx[k++] = v + i;
      g.dispose();
      v += n;
    }
    return {pos, nrm, col, joint, idx, count: nv};
  }
  /* joint matrices for a pose: {joint: [rx, ry, rz]}, body offset, shin stretch. Plain 16 arrays, column major */
  function mul(a, b, out) {
    for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) out[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
    return out;
  }
  function local(x, y, z, rx, ry, rz, sy) {
    /* translate, then rotate X then Y then Z (three's XYZ Euler), then scale y */
    const a = Math.cos(rx), b = Math.sin(rx), c = Math.cos(ry), d = Math.sin(ry), e = Math.cos(rz), f = Math.sin(rz);
    const ae = a * e, af = a * f, be = b * e, bf = b * f;
    const s = sy || 1;
    return [c * e, af + be * d, bf - ae * d, 0,
      -c * f * s, (ae - bf * d) * s, (be + af * d) * s, 0,
      d, -b * c, a * c, 0,
      x, y, z, 1];
  }
  function matrices(pose, place) {
    const out = new Array(NJ);
    for (let j = 0; j < NJ; j++) {
      const [p, x, y, z] = JOINTS[j];
      const r = pose.rot[j] || ZERO;
      const off = j === J.body ? pose.body : ZERO;
      const L = local(x + off[0], y + off[1], z + off[2], r[0], r[1], r[2], pose.scale[j]);
      out[j] = p < 0 ? (place ? place.slice() : L) : mul(out[p], L, new Array(16));
    }
    return out;
  }
  const ZERO = [0, 0, 0];
  function skinInto(sk, W, pos, nrm, at) {
    const P = sk.pos, N = sk.nrm, jt = sk.joint, n = sk.count, base = (at || 0) * 3;
    for (let i = 0; i < n; i++) {
      const e = W[jt[i]], o = i * 3, q = base + o;
      const x = P[o], y = P[o + 1], z = P[o + 2];
      pos[q] = e[0] * x + e[4] * y + e[8] * z + e[12];
      pos[q + 1] = e[1] * x + e[5] * y + e[9] * z + e[13];
      pos[q + 2] = e[2] * x + e[6] * y + e[10] * z + e[14];
      const a = N[o], b = N[o + 1], c = N[o + 2];
      let u = e[0] * a + e[4] * b + e[8] * c, v = e[1] * a + e[5] * b + e[9] * c, w = e[2] * a + e[6] * b + e[10] * c;
      const l = Math.hypot(u, v, w) || 1;
      nrm[q] = u / l; nrm[q + 1] = v / l; nrm[q + 2] = w / l;
    }
  }

  /* ---------- poses: procedural, no clips ----------
     pose(look, name, t, p) -> {rot: [joint] -> [x, y, z], body: [x, y, z], scale: [joint] -> sy}
     stand (easy, pockets, folded, mug), walk (p.phase in strides, or p.dist in metres), sit and type (p.seat,
     the chair's seat height, default .46: the shins reach down so the feet rest on the floor), talk, wave */
  function posed(look, name, t, q) {
    const p = q || {};
    const rot = new Array(NJ), scale = new Array(NJ);
    const set = (j, x, y, z) => { rot[j] = [x || 0, y || 0, z || 0]; };
    let body = [0, 0, 0];
    const kind = name === 'stand' ? (look && look.pose) || 'easy' : name;
    set(J.shL, 0, 0, -0.1); set(J.shR, 0, 0, 0.1); set(J.elL, -0.14); set(J.elR, -0.14);
    if (kind === 'pockets') { set(J.shL, 0.22, 0, -0.16); set(J.shR, 0.22, 0, 0.16); set(J.elL, -0.62, 0.2, 0); set(J.elR, -0.62, -0.2, 0); }
    if (kind === 'folded') { set(J.shL, -0.42, 0.1, -0.2); set(J.shR, -0.48, -0.1, 0.2); set(J.elL, -1.75, -0.95, 0); set(J.elR, -1.7, 0.95, 0); }
    if (kind === 'mug') { set(J.shR, -0.28, 0, 0.12); set(J.elR, -1.45, -0.2, 0); }
    if (kind === 'walk') {
      const ph = p.phase != null ? p.phase : (p.dist || 0) / (STRIDE * 2);
      const s = Math.sin(ph * Math.PI * 2);
      set(J.hipL, s * 0.45); set(J.hipR, -s * 0.45);
      set(J.knL, Math.max(0, -s) * 0.55); set(J.knR, Math.max(0, s) * 0.55);
      set(J.shL, -s * 0.32, 0, -0.08); set(J.shR, s * 0.32, 0, 0.08);
      set(J.elL, -0.28); set(J.elR, look && look.pose === 'mug' ? -1.45 : -0.28);
      if (look && look.pose === 'mug') set(J.shR, -0.28, 0, 0.12);
      body = [0, Math.abs(Math.cos(ph * Math.PI * 2)) * 0.018, 0];
      set(J.body, 0, 0, s * 0.02);
    }
    if (kind === 'sit' || kind === 'type') {
      const seat = Number.isFinite(p.seat) ? p.seat : 0.46;
      const hipY = seat + 0.064;
      body = [0, hipY - 0.42, 0];
      const th = Math.PI / 2 - 0.3;
      const kneeY = hipY - THIGH * Math.cos(th);
      const need = Math.max(SHIN, kneeY - ANKLE_Y);
      for (const [hip, kn, an, sx] of [[J.hipL, J.knL, J.anL, -1], [J.hipR, J.knR, J.anR, 1]]) {
        set(hip, -th, 0, sx * -0.05);
        set(kn, th, 0, 0);
        set(an, 0, 0, 0);
        /* the shin reaches down to the floor; the ankle takes the stretch back, so the shoe keeps its shape */
        scale[kn] = need / SHIN;
        scale[an] = SHIN / need;
      }
      if (kind === 'type') {
        set(J.shL, -0.72, 0.12, -0.14); set(J.shR, -0.72, -0.12, 0.14);
        set(J.elL, -0.95 + Math.sin(t * 9) * 0.03, 0.25, 0); set(J.elR, -0.95 + Math.cos(t * 11) * 0.03, -0.25, 0);
        set(J.head, 0.12, 0, 0);
      } else { set(J.shL, -0.32, 0, -0.1); set(J.shR, -0.32, 0, 0.1); set(J.elL, -0.95); set(J.elR, -0.95); set(J.head, 0.05, p.look || 0, 0); }
    }
    if (kind === 'talk') {
      set(J.shR, -0.55 - 0.08 * Math.sin(t * 2.2), -0.3, 0.38); set(J.elR, -1.25 - 0.12 * Math.sin(t * 2.2 + 0.6), 0.45, 0);
      set(J.shL, 0.04, 0, -0.1); set(J.elL, -0.18);
      set(J.head, -0.04 + 0.03 * Math.sin(t * 1.7), 0.1 * Math.sin(t * 0.6) + (p.look || 0), 0.04 * Math.sin(t * 1.3));
      set(J.hipR, -0.05, 0, 0.03); set(J.knR, 0.1);
    }
    if (kind === 'wave') { set(J.shR, 0, 0, 2.55 + Math.sin(t * 8) * 0.18); set(J.elR, -0.35, 0, 0); }
    return {rot, body, scale};
  }

  /* ---------- the sticker: initials on a paper disc, drawn on a canvas (letters only, from M.cast.initials) ---------- */
  function stickerCanvas(list, cell) {
    const C = cast();
    const cols = Math.max(1, Math.min(8, list.length));
    const rows = Math.max(1, Math.ceil(list.length / 8));
    const cv = document.createElement('canvas');
    cv.width = cols * cell; cv.height = rows * cell;
    const g = cv.getContext('2d');
    list.forEach((txt, i) => {
      const x = (i % 8) * cell, y = Math.floor(i / 8) * cell;
      g.fillStyle = C.css(C.HOUSE.white);
      g.beginPath(); g.arc(x + cell / 2, y + cell / 2, cell * 0.46, 0, Math.PI * 2); g.fill();
      g.fillStyle = C.css(C.HOUSE.ink);
      g.font = '600 ' + Math.round(cell * 0.32) + 'px "Space Grotesk", system-ui, sans-serif';
      g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillText(C.sticker(txt), x + cell / 2, y + cell / 2 + cell * 0.02);
    });
    return {canvas: cv, cols, rows};
  }
  function stickerMaterial(T, canvas) {
    const tex = new T.CanvasTexture(canvas);
    tex.colorSpace = T.SRGBColorSpace;
    return new T.MeshStandardMaterial({map: tex, roughness: 0.7, metalness: 0, transparent: true, alphaTest: 0.4});
  }
  /* a quad facing +z at the sticker's place, uv into cell i of the atlas */
  function stickerQuad(at, i, atlas) {
    const s = 0.042, [x, y, z] = at;
    const u0 = (i % 8) / atlas.cols, v1 = 1 - Math.floor(i / 8) / atlas.rows, u1 = u0 + 1 / atlas.cols, v0 = v1 - 1 / atlas.rows;
    return {pos: [x - s, y - s, z, x + s, y - s, z, x + s, y + s, z, x - s, y + s, z], uv: [u0, v0, u1, v0, u1, v1, u0, v1], idx: [0, 1, 2, 0, 2, 3]};
  }

  /* ---------- build: one person you can move ---------- */
  function build(T, raw, o) {
    const opts = o || {};
    const live = !!(opts.live || opts.founder);
    const P = parts(T, raw, opts);
    const list = live ? P.main : P.main.concat(P.eyes, P.mouth);
    const sk = pack(list);
    const geo = new T.BufferGeometry();
    const pos = new Float32Array(sk.count * 3), nrm = new Float32Array(sk.count * 3);
    geo.setAttribute('position', new T.BufferAttribute(pos, 3));
    geo.setAttribute('normal', new T.BufferAttribute(nrm, 3));
    geo.setAttribute('color', new T.BufferAttribute(sk.col, 3));
    geo.setIndex(new T.BufferAttribute(sk.idx, 1));
    const mat = material(T);
    const mesh = new T.Mesh(geo, mat);
    mesh.castShadow = true; mesh.receiveShadow = false;
    const root = new T.Group();
    root.add(mesh);
    /* rigid attachments ride a joint: Kaavish's eyes and mouth, the starter's sticker */
    const attach = [];
    const rigid = (lst, j, centre) => {
      if (!lst.length) return null;
      const s2 = pack(lst);
      const g = new T.BufferGeometry();
      /* the parts sit relative to the joint; centre them on their own pivot so a blink and a word scale in place */
      for (let i = 0; i < s2.count; i++) for (let k = 0; k < 3; k++) s2.pos[i * 3 + k] -= centre[k] - PIVOT[j][k];
      g.setAttribute('position', new T.BufferAttribute(s2.pos, 3));
      g.setAttribute('normal', new T.BufferAttribute(s2.nrm, 3));
      g.setAttribute('color', new T.BufferAttribute(s2.col, 3));
      g.setIndex(new T.BufferAttribute(s2.idx, 1));
      const m = new T.Mesh(g, mat);
      m.castShadow = true; m.matrixAutoUpdate = false;
      root.add(m);
      const a = {mesh: m, j, centre, sy: 1};
      attach.push(a);
      return a;
    };
    const eyesA = live ? rigid(P.eyes, J.head, P.eyeAt) : null;
    const mouthA = live ? rigid(P.mouth, J.head, P.mouthAt) : null;
    let stickerTex = null;
    if (P.sticker && typeof document !== 'undefined') {
      const atlas = stickerCanvas([P.sticker.initials], 64);
      const q = stickerQuad([0, 0, 0], 0, atlas);
      const g = new T.BufferGeometry();
      g.setAttribute('position', new T.Float32BufferAttribute(q.pos, 3));
      g.setAttribute('normal', new T.Float32BufferAttribute([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], 3));
      g.setAttribute('uv', new T.Float32BufferAttribute(q.uv, 2));
      g.setIndex(q.idx);
      const sm = stickerMaterial(T, atlas.canvas);
      stickerTex = sm;
      const m = new T.Mesh(g, sm);
      m.matrixAutoUpdate = false;
      root.add(m);
      attach.push({mesh: m, j: J.body, centre: P.sticker.at, sy: 1});
    }
    geo.boundingSphere = null;
    let W = null;
    const place = () => {
      for (const a of attach) {
        const c = a.centre, pv = PIVOT[a.j];
        const L = local(c[0] - pv[0], c[1] - pv[1], c[2] - pv[2], 0, 0, 0, a.sy);
        a.mesh.matrix.fromArray(mul(W[a.j], L, new Array(16)));
        a.mesh.matrixWorldNeedsUpdate = true;
      }
    };
    const rig = {
      root, look: P.look,
      setPose(name, t, q) {
        W = matrices(posed(P.look, name || 'stand', t || 0, q));
        skinInto(sk, W, pos, nrm, 0);
        geo.attributes.position.needsUpdate = true;
        geo.attributes.normal.needsUpdate = true;
        if (!geo.boundingSphere) { geo.computeBoundingSphere(); geo.boundingSphere.radius += 0.4; }
        place();
        return rig;
      },
      blink(on) { if (eyesA) { eyesA.sy = on ? 0.12 : 1; if (W) place(); } },
      talk(level) { if (mouthA) { mouthA.sy = 1 + Math.max(0, Math.min(1, Number(level) || 0)) * 1.4; if (W) place(); } },
      tris: 0, calls: 0,
      dispose() { geo.dispose(); for (const a of attach) a.mesh.geometry.dispose(); if (stickerTex) { stickerTex.map.dispose(); stickerTex.dispose(); } }
    };
    root.traverse(x => { if (x.isMesh) { rig.calls++; rig.tris += (x.geometry.index ? x.geometry.index.count : x.geometry.attributes.position.count) / 3; } });
    rig.setPose('stand', 0);
    return rig;
  }

  /* ---------- crowd: every still person baked into ONE mesh ----------
     items [{look, founder, x, y, h, pose, acc, lod, seat, t}]: plan cm, heading in degrees. Each posed figure is
     cached by its look's hash, the founder mark, the LOD, the pose and the accessories, so a crowd rebuild only
     poses the people who changed. The starters' stickers ride the same mesh as a second group */
  const posedCache = new Map();
  let crowdStats = {hits: 0, misses: 0};
  function keyOf(it) {
    const C = cast();
    const raw = it.look || {};
    const extra = (it.founder ? 'F' : '') + (raw.starter === true ? 'S' + C.sticker(raw.initials) : '');
    return C.hash(raw, extra) + '|' + (it.lod ? 1 : 0) + '|' + (it.pose || 'stand') + '|' + (Array.isArray(it.acc) ? it.acc.join(',') : '') + '|' + (Number.isFinite(it.seat) ? it.seat : '') + '|' + (it.t ? Math.round(it.t * 10) : 0);
  }
  function bakeOne(T, it) {
    const key = keyOf(it);
    let b = posedCache.get(key);
    if (b) { crowdStats.hits++; posedCache.delete(key); posedCache.set(key, b); return b; }
    crowdStats.misses++;
    const P = parts(T, it.look || {}, {founder: !!it.founder, lod: it.lod, acc: Array.isArray(it.acc) ? it.acc : null, noMug: it.pose && it.pose !== 'stand' && it.pose !== 'walk'});
    const sk = pack(P.main.concat(P.eyes, P.mouth));
    const W = matrices(posed(P.look, it.pose || 'stand', it.t || 0, {seat: it.seat}));
    const pos = new Float32Array(sk.count * 3), nrm = new Float32Array(sk.count * 3);
    skinInto(sk, W, pos, nrm, 0);
    let st = null;
    if (P.sticker) {
      const c = P.sticker.at, pv = PIVOT[J.body], e = W[J.body];
      const x = c[0] - pv[0], y = c[1] - pv[1], z = c[2] - pv[2];
      st = {at: [e[0] * x + e[4] * y + e[8] * z + e[12], e[1] * x + e[5] * y + e[9] * z + e[13], e[2] * x + e[6] * y + e[10] * z + e[14] + 0.002], initials: P.sticker.initials};
    }
    b = {pos, nrm, col: sk.col, idx: sk.idx, count: sk.count, sticker: st};
    posedCache.set(key, b);
    if (posedCache.size > 64) posedCache.delete(posedCache.keys().next().value);
    return b;
  }
  function assemble(T, items, baked) {
    let nv = 0, ni = 0;
    for (const b of baked) { nv += b.count; ni += b.idx.length; }
    const stickers = [];
    baked.forEach((b, i) => { if (b.sticker) stickers.push({b, it: items[i]}); });
    const sv = stickers.length * 4;
    const pos = new Float32Array((nv + sv) * 3), nrm = new Float32Array((nv + sv) * 3), col = new Float32Array((nv + sv) * 3), uv = new Float32Array((nv + sv) * 2);
    const idx = new Uint32Array(ni + stickers.length * 6);
    let v = 0, k = 0;
    /* each figure's place: plan cm to metres, turned by its heading */
    const placeOf = it => {
      const a = (Number(it.h) || 0) * Math.PI / 180;
      return {c: Math.cos(a), s: Math.sin(a), x: (Number(it.x) || 0) / 100, z: (Number(it.y) || 0) / 100};
    };
    baked.forEach((b, i) => {
      const {c, s, x: ox, z: oz} = placeOf(items[i]);
      for (let q = 0; q < b.count; q++) {
        const o = q * 3, d = (v + q) * 3;
        const x = b.pos[o], z = b.pos[o + 2];
        pos[d] = x * c + z * s + ox; pos[d + 1] = b.pos[o + 1]; pos[d + 2] = -x * s + z * c + oz;
        const nx = b.nrm[o], nz = b.nrm[o + 2];
        nrm[d] = nx * c + nz * s; nrm[d + 1] = b.nrm[o + 1]; nrm[d + 2] = -nx * s + nz * c;
        col[d] = b.col[o]; col[d + 1] = b.col[o + 1]; col[d + 2] = b.col[o + 2];
      }
      for (let q = 0; q < b.idx.length; q++) idx[k++] = b.idx[q] + v;
      v += b.count;
    });
    const geo = new T.BufferGeometry();
    geo.setAttribute('position', new T.BufferAttribute(pos, 3));
    geo.setAttribute('normal', new T.BufferAttribute(nrm, 3));
    geo.setAttribute('color', new T.BufferAttribute(col, 3));
    geo.setIndex(new T.BufferAttribute(idx, 1));
    geo.addGroup(0, ni, 0);
    const materials = [material(T)];
    if (stickers.length && typeof document !== 'undefined') {
      geo.setAttribute('uv', new T.BufferAttribute(uv, 2));
      const atlas = stickerCanvas(stickers.map(x => x.b.sticker.initials), 64);
      stickers.forEach(({b, it}, i) => {
        const q = stickerQuad([0, 0, 0], i, atlas);
        const {c, s, x: ox, z: oz} = placeOf(it);
        const base = v;
        for (let n = 0; n < 4; n++) {
          const x = b.sticker.at[0] + q.pos[n * 3], z = b.sticker.at[2];
          pos[v * 3] = x * c + z * s + ox; pos[v * 3 + 1] = b.sticker.at[1] + q.pos[n * 3 + 1]; pos[v * 3 + 2] = -x * s + z * c + oz;
          nrm[v * 3] = s; nrm[v * 3 + 2] = c;
          col[v * 3] = col[v * 3 + 1] = col[v * 3 + 2] = 1;
          uv[v * 2] = q.uv[n * 2]; uv[v * 2 + 1] = q.uv[n * 2 + 1];
          v++;
        }
        for (const n of q.idx) idx[k++] = base + n;
      });
      geo.addGroup(ni, stickers.length * 6, 1);
      materials.push(stickerMaterial(T, atlas.canvas));
    }
    geo.computeBoundingSphere();
    const mesh = new T.Mesh(geo, materials.length > 1 ? materials : materials[0]);
    mesh.castShadow = true; mesh.receiveShadow = false;
    mesh.userData.people = items.length;
    /* the stickers' texture goes with the geometry, so a caller that disposes only the crowd's geometry frees it too */
    if (materials[1]) geo.addEventListener('dispose', () => { materials[1].map.dispose(); materials[1].dispose(); });
    mesh.userData.dispose = () => geo.dispose();
    return mesh;
  }
  function crowd(T, items) {
    const list = (items || []).filter(Boolean);
    return assemble(T, list, list.map(it => bakeOne(T, it)));
  }
  /* the same, one uncached figure per idle chunk of at most budget ms, so a crowd rebuild never drops a frame */
  crowd.async = function crowdAsync(T, items, o) {
    const list = (items || []).filter(Boolean);
    const budget = (o && o.budget) || 8;
    const idle = typeof requestIdleCallback === 'function' ? fn => requestIdleCallback(fn, {timeout: 120}) : fn => setTimeout(fn, 16);
    return new Promise((resolve, reject) => {
      const baked = new Array(list.length);
      let i = 0;
      const step = () => {
        try {
          /* cached figures cost nothing; at most one fresh figure is posed per chunk */
          const t0 = performance.now();
          let fresh = 0;
          while (i < list.length) {
            const miss = !posedCache.has(keyOf(list[i]));
            if (miss && (fresh || performance.now() - t0 > budget)) break;
            baked[i] = bakeOne(T, list[i]);
            if (miss) fresh++;
            i++;
          }
          if (i < list.length) idle(step); else resolve(assemble(T, list, baked));
        } catch (e) { reject(e); }
      };
      idle(step);
    });
  };
  crowd.stats = () => ({...crowdStats, cached: posedCache.size});
  crowd.clear = () => { posedCache.clear(); crowdStats = {hits: 0, misses: 0}; };

  /* ---------- the COO: the dock's droid, a plush flame head with square glasses and a bow tie ----------
     Four draw calls: the plush (head, ears, stem), the antenna ball (a soft glow), the accessories (glasses,
     bow tie, smile, and the headphones at the end of the buffer) and the face (lids, then eyes and glints).
     Listening shows the headphones and sleeping swaps the eyes for lids, by draw range, never a rebuild */
  function coo(T, o) {
    const opts = o || {};
    const C = cast(), H = C.HOUSE;
    const lod = opts.lod ? 1 : 0;
    const seg = lod ? 8 : 16;
    const plush = new T.MeshPhysicalMaterial({color: colourOf(T, H.flame), roughness: 0.85, sheen: 1, sheenRoughness: 0.55, sheenColor: colourOf(T, C.mix(H.flame, H.white, 0.35))});
    const glow = plush.clone();
    glow.emissive = colourOf(T, H.flame); glow.emissiveIntensity = 0.25;
    const accM = new T.MeshStandardMaterial({color: colourOf(T, opts.dark ? H.inkDark : H.ink), roughness: 0.45, metalness: 0});
    const faceM = new T.MeshStandardMaterial({vertexColors: true, roughness: 0.4, metalness: 0});
    const W = 0.44, Hh = 0.39, D = 0.32;
    const geom = (list, cols) => {
      /* merge placed geometries, position and normal only (and a colour per piece when given) */
      let nv = 0, ni = 0;
      for (const g of list) { nv += g.attributes.position.count; ni += g.index ? g.index.count : g.attributes.position.count; }
      const pos = new Float32Array(nv * 3), nrm = new Float32Array(nv * 3), col = cols ? new Float32Array(nv * 3) : null, idx = new Uint32Array(ni);
      let v = 0, k = 0;
      list.forEach((g, n) => {
        const P = g.attributes.position, N = g.attributes.normal, c = cols ? linear(cols[n]) : null;
        for (let i = 0; i < P.count; i++) {
          pos.set([P.getX(i), P.getY(i), P.getZ(i)], (v + i) * 3);
          nrm.set([N.getX(i), N.getY(i), N.getZ(i)], (v + i) * 3);
          if (col) col.set(c, (v + i) * 3);
        }
        if (g.index) for (let i = 0; i < g.index.count; i++) idx[k++] = g.index.array[i] + v; else for (let i = 0; i < P.count; i++) idx[k++] = v + i;
        v += P.count;
        g.dispose();
      });
      const out = new T.BufferGeometry();
      out.setAttribute('position', new T.BufferAttribute(pos, 3));
      out.setAttribute('normal', new T.BufferAttribute(nrm, 3));
      if (col) out.setAttribute('color', new T.BufferAttribute(col, 3));
      out.setIndex(new T.BufferAttribute(idx, 1));
      return out;
    };
    const P = (g, at, rot, scl) => placed(T, g, at, rot, scl);
    /* the plush: a rounded box head, two ears, the antenna stem */
    const plushG = geom([
      P(new T.RoundedBoxGeometry(W, Hh, D, lod ? 2 : 4, Hh * 0.3)),
      P(new T.SphereGeometry(0.045, seg, seg - 4), [-0.25, -0.01, 0], 0, [0.75, 1, 0.85]),
      P(new T.SphereGeometry(0.045, seg, seg - 4), [0.25, -0.01, 0], 0, [0.75, 1, 0.85]),
      P(new T.CylinderGeometry(0.012, 0.014, 0.1, 10), [0, Hh / 2 + 0.05, 0])
    ]);
    const ballG = geom([P(new T.SphereGeometry(0.045, seg, seg - 4), [0, Hh / 2 + 0.135, 0])]);
    /* the accessories: square glasses (four capsules an eye), a bridge, a small smile, the bow tie; then the
       headphones, drawn only while it listens */
    const zf = D / 2;
    const acc = [];
    for (const sx of [-1, 1]) {
      const gx = sx * 0.088, w = 0.064, hh = 0.054, t = 0.0085, gz = zf + 0.012;
      acc.push(P(new T.CapsuleGeometry(t, w * 2 - 2 * t, 2, 6), [gx, 0.012 + hh, gz], [0, 0, Math.PI / 2]));
      acc.push(P(new T.CapsuleGeometry(t, w * 2 - 2 * t, 2, 6), [gx, 0.012 - hh, gz], [0, 0, Math.PI / 2]));
      for (const ix of [-1, 1]) acc.push(P(new T.CapsuleGeometry(t, hh * 2 - 2 * t, 2, 6), [gx + ix * w, 0.012, gz]));
    }
    acc.push(P(new T.CapsuleGeometry(0.0065, 0.022, 2, 6), [0, 0.02, zf + 0.012], [0, 0, Math.PI / 2]));
    acc.push(P(new T.TorusGeometry(0.03, 0.0065, 5, 14, Math.PI * 0.6), [0, -0.082, zf + 0.002], [0, 0, Math.PI + Math.PI * 0.2]));
    for (const sx of [-1, 1]) acc.push(P(new T.CylinderGeometry(0, 0.045, 0.08, 4), [sx * 0.04, -Hh / 2 - 0.05, 0.1], [0, 0, sx * Math.PI / 2], [1, 1, 0.42]));
    acc.push(P(new T.SphereGeometry(0.018, 10, 8), [0, -Hh / 2 - 0.05, 0.108]));
    const accCount = acc.reduce((n, g) => n + (g.index ? g.index.count : g.attributes.position.count), 0);
    acc.push(P(new T.TorusGeometry(W * 0.56, 0.016, 6, 28, Math.PI), [0, 0.02, 0], [0, 0, 0]));
    for (const sx of [-1, 1]) acc.push(P(new T.CylinderGeometry(0.06, 0.06, 0.05, 18), [sx * (W / 2 + 0.04), 0, 0], [0, 0, Math.PI / 2]));
    const accG = geom(acc);
    /* the face: lids first (ink lash arcs over flame lids), then the bead eyes and their glints */
    const flame = H.flame, ink = H.ink, white = H.white;
    const face = [], fc = [];
    for (const sx of [-1, 1]) {
      face.push(P(new T.SphereGeometry(0.036, seg, seg - 4, 0, Math.PI * 2, 0, Math.PI / 2), [sx * 0.088, 0.012, zf - 0.008], [Math.PI / 2 - 0.25, 0, 0], [1, 0.5, 1])); fc.push(flame);
      face.push(P(new T.TorusGeometry(0.03, 0.0055, 5, 12, Math.PI), [sx * 0.088, 0.006, zf + 0.004], [0, 0, Math.PI])); fc.push(ink);
    }
    const lidCount = face.reduce((n, g) => n + g.index.count, 0);
    for (const sx of [-1, 1]) {
      face.push(P(new T.SphereGeometry(0.034, seg, seg - 4), [sx * 0.088, 0.012, zf - 0.004], 0, [1, 1.18, 0.45])); fc.push(ink);
      if (!lod) { face.push(P(new T.SphereGeometry(0.009, 8, 6), [sx * 0.088 - 0.01, 0.026, zf + 0.012])); fc.push(white); }
    }
    const faceG = geom(face, fc);
    const faceAll = faceG.index.count;
    const root = new T.Group(), body = new T.Group();
    root.add(body);
    const mk = (g, m) => { const x = new T.Mesh(g, m); x.castShadow = true; body.add(x); return x; };
    mk(plushG, plush); mk(ballG, glow);
    const accMesh = mk(accG, accM), faceMesh = mk(faceG, faceM);
    const HOVER = 1.15, PAD = Number.isFinite(opts.pad) ? opts.pad : 0.76 + Hh / 2;
    const st = {state: 'desk', listen: false, sleep: false, y: PAD, target: PAD, bobFor: 0, t: 0, tilt: 0};
    const ranges = () => {
      accG.setDrawRange(0, st.listen ? accG.index.count : accCount);
      if (st.sleep) faceG.setDrawRange(0, lidCount); else faceG.setDrawRange(lidCount, faceAll - lidCount);
    };
    ranges();
    body.position.y = st.y;
    const rig = {
      root, body,
      setState(s) {
        st.state = String(s || 'desk');
        st.target = st.state === 'desk' || st.state === 'sleeping' ? PAD : HOVER;
        if (st.state === 'working') st.bobFor = 4;
        rig.sleep(st.state === 'sleeping');
        return rig;
      },
      setYaw(r) { root.rotation.y = Number(r) || 0; return rig; },
      setAccent(dark) { accM.color.copy(colourOf(T, dark ? H.inkDark : H.ink)); return rig; },
      listen(on) { st.listen = !!on; ranges(); return rig; },
      sleep(on) { st.sleep = !!on; ranges(); return rig; },
      /* update(dt seconds) -> true while something still moves: easing to the hover or the pad, a 4 s bob */
      update(dt) {
        const d = Math.min(0.1, Math.max(0, Number(dt) || 0));
        st.t += d;
        let moving = false;
        const gap = st.target - st.y;
        if (Math.abs(gap) > 0.0005) { st.y += gap * Math.min(1, d * 6); moving = true; } else st.y = st.target;
        let bob = 0;
        if (st.bobFor > 0) { st.bobFor = Math.max(0, st.bobFor - d); bob = Math.sin(st.t * Math.PI) * 0.03 * Math.min(1, st.bobFor); moving = true; }
        const tilt = st.listen ? 0.08 : 0;
        if (Math.abs(tilt - st.tilt) > 0.001) { st.tilt += (tilt - st.tilt) * Math.min(1, d * 8); moving = true; } else st.tilt = tilt;
        body.position.y = st.y + bob;
        body.rotation.z = st.tilt;
        return moving;
      },
      tris: 0, calls: 4,
      dispose() { for (const g of [plushG, ballG, accG, faceG]) g.dispose(); for (const m of [plush, glow, accM, faceM]) m.dispose(); }
    };
    rig.tris = [plushG, ballG, accG, faceG].reduce((n, g) => n + g.index.count / 3, 0);
    return rig;
  }

  M.figure = {build, crowd, coo, pose: posed, JOINTS, PIVOT};
})();
