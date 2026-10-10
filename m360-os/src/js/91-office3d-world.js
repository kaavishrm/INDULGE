/* module: office3d (the world). The floor of the 3D office as one object: a rounded plinth floating on the
   studio backdrop, walls cut at 1 m, the benches and stations of the flat office at their plan places, pale oak
   tops, pampas in chalk vases. Primitives only, built from the plan of 90-office.js (1 plan unit = 1 cm; plan x
   is world x / 100 m, plan y is world z / 100 m, the floor top at y 0).

   Every piece belongs to a role (floor, wall, cap, top, leg, seat, board, cell, mark, ink, glass, screen, pot,
   pampas, lamp on, lamp off) and each role's geometry is merged into one mesh with one material, so a theme
   change only sets colours. The builder is a generator: it yields between parts, so the engine can build in
   idle slices of at most 8 ms. Nothing here holds a colour: the engine reads them from the CSS tokens.

     M.office3d.world.build(T, o)        a generator: yields, then returns the world
     M.office3d.world.run(gen)           the same, all at once (for checks)
     M.office3d.world.slab(L)            the plinth's extent, in metres
     M.office3d.world.floorTexture / grainTexture / radial / dropShadowTexture / backdropTexture  (canvas textures) */
'use strict';
(function () {
  const OF = () => M.office;
  const cm = v => v / 100;
  const WALL_H = 1.0, WALL_T = 0.12, TOP_H = 0.74;

  /* the plinth: plan x -40 to 1640, from just behind the back wall to 30 cm past the front, 46 cm thick */
  const slab = L => ({x0: -0.4, z0: 1.1, x1: 16.4, z1: cm(L.H + 30), r: 0.7, h: 0.46});

  /* ---------- the geometry kit ---------- */
  function kit(T, lite) {
    const _m = new T.Matrix4(), _q = new T.Quaternion(), _e = new T.Euler(), _v = new T.Vector3(), _s = new T.Vector3();
    const prep = g => {
      for (const k of Object.keys(g.attributes)) if (k !== 'position' && k !== 'normal') g.deleteAttribute(k);
      return g.index ? g : T.mergeVertices(g, 1e-6);
    };
    const place = (g, at, rot, scl) => {
      _e.set(rot ? rot[0] : 0, rot ? rot[1] : 0, rot ? rot[2] : 0, 'YXZ');
      _m.compose(_v.set(at ? at[0] : 0, at ? at[1] : 0, at ? at[2] : 0), _q.setFromEuler(_e), _s.set(scl ? scl[0] : 1, scl ? scl[1] : 1, scl ? scl[2] : 1));
      g.applyMatrix4(_m);
      return g;
    };
    /* rounded boxes spend triangles on the corners only where a corner shows */
    const rbox = (w, h, d, r, seg) => {
      const rad = Math.min(r == null ? 0.02 : r, Math.min(w, h, d) / 2 - 1e-4);
      return new T.RoundedBoxGeometry(w, h, d, lite ? 1 : (seg || (rad < 0.012 || Math.min(w, h, d) < 0.03 ? 1 : 2)), Math.max(1e-4, rad));
    };
    const seg = (a, b, r, segs) => {
      const A = new T.Vector3(a[0], a[1], a[2]), B = new T.Vector3(b[0], b[1], b[2]), d = B.clone().sub(A), len = Math.max(1e-4, d.length());
      const g = new T.CapsuleGeometry(r, len, segs ? segs[0] : (lite ? 2 : 3), segs ? segs[1] : (lite ? 6 : 10));
      _q.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize());
      _m.compose(A.add(B).multiplyScalar(0.5), _q, _s.set(1, 1, 1));
      g.applyMatrix4(_m);
      return g;
    };
    const ball = (r, w, h) => new T.SphereGeometry(r, lite ? Math.max(8, (w || 16) >> 1) : (w || 16), lite ? Math.max(6, (h || 12) >> 1) : (h || 12));
    const cyl = (rt, rb, h, n) => new T.CylinderGeometry(rt, rb, h, lite ? Math.max(8, (n || 24) >> 1) : (n || 24));
    /* a rounded rectangle in plan, from y0 to y0 + h, with a soft bevel: tops, counters, the plinth */
    function planSlab(x0, z0, x1, z1, r, y0, h, bevel, curve) {
      const s = new T.Shape(), b = bevel == null ? 0.012 : bevel;
      const X0 = x0 + b, X1 = x1 - b, Z0 = z0 + b, Z1 = z1 - b, R = Math.max(0.001, Math.min(r, (X1 - X0) / 2, (Z1 - Z0) / 2));
      s.moveTo(X0 + R, -Z1);
      s.lineTo(X1 - R, -Z1); s.quadraticCurveTo(X1, -Z1, X1, -Z1 + R);
      s.lineTo(X1, -Z0 - R); s.quadraticCurveTo(X1, -Z0, X1 - R, -Z0);
      s.lineTo(X0 + R, -Z0); s.quadraticCurveTo(X0, -Z0, X0, -Z0 - R);
      s.lineTo(X0, -Z1 + R); s.quadraticCurveTo(X0, -Z1, X0 + R, -Z1);
      const g = new T.ExtrudeGeometry(s, {depth: Math.max(0.001, h - 2 * b), bevelEnabled: b > 0, bevelThickness: b, bevelSize: b, bevelSegments: lite ? 1 : 3, curveSegments: lite ? 4 : (curve || 10)});
      g.rotateX(-Math.PI / 2);
      g.translate(0, y0 + b, 0);
      return g;
    }
    /* the pieces of one role, merged at the end */
    class Batch {
      constructor() { this.roles = {}; this.tris = 0; }
      add(role, g, at, rot, scl, m) {
        g = prep(g);
        place(g, at, rot, scl);
        if (m) g.applyMatrix4(m);
        (this.roles[role] = this.roles[role] || []).push(g);
        return g;
      }
      /* pieces built in an object's own space, then turned and placed */
      obj(x, z, ry, y) {
        const m = new T.Matrix4().compose(new T.Vector3(x, y || 0, z), new T.Quaternion().setFromEuler(new T.Euler(0, ry || 0, 0)), new T.Vector3(1, 1, 1));
        return (role, g, at, rot, scl) => this.add(role, g, at, rot, scl, m);
      }
    }
    return {prep, place, rbox, seg, ball, cyl, planSlab, Batch};
  }

  /* ---------- the world ---------- */
  function* build(T, o) {
    const O = OF();
    const L = o.L, D = o.D || [], lite = !!o.lite;
    const K = kit(T, lite);
    const B = new K.Batch();
    const sy = y => (y >= 700 ? y + L.grow : y);
    const Z = y => cm(sy(y));
    const ao = [], anchors = {}, colliders = [], lamps = [], pools = [], homes = [], seatsAt = {};
    const foot = (x0, z0, x1, z1, k, blur, r) => ao.push({x0, z0, x1, z1, k: k == null ? 1 : k, blur: blur || 0.18, r: r == null ? 0.06 : r});
    const disc = (cx, cz, rad, k, blur) => ao.push({cx, cz, rad, k, blur: blur || 0.12});
    const hit = (x0, z0, x1, z1) => colliders.push([Math.round(x0 * 100), Math.round(z0 * 100), Math.round(x1 * 100), Math.round(z1 * 100)]);
    const add = (role, g, at, rot, scl) => B.add(role, g, at, rot, scl);
    const S = slab(L);

    /* ---- walls, cut at 1 m: the cut face a step deeper, as a section is drawn ---- */
    const wall = (x0, z0, x1, z1) => {
      const w = x1 - x0, d = z1 - z0;
      add('wall', K.rbox(w, WALL_H - 0.02, d, 0.025), [(x0 + x1) / 2, (WALL_H - 0.02) / 2, (z0 + z1) / 2]);
      add('cap', K.rbox(w + 0.004, 0.022, d + 0.004, 0.008), [(x0 + x1) / 2, WALL_H - 0.011, (z0 + z1) / 2]);
      foot(x0, z0, x1, z1, 1.1, 0.22, 0.02);
      hit(x0, z0, x1, z1);
    };
    const H = cm(L.H);
    wall(-WALL_T, 1.5 - WALL_T, 16 + WALL_T, 1.5);
    wall(-WALL_T, 1.5, 0, Z(820));
    wall(-WALL_T, Z(900), 0, H);
    wall(16, 1.5, 16 + WALL_T, H);
    /* the cabin: a low wall with its door at plan y 615 to 685 */
    wall(12.0, 5.6, 16, 5.6 + WALL_T); wall(11.94, 5.6 + WALL_T, 12.06, 6.15); wall(11.94, 6.85, 12.06, H);
    /* the meeting room: glass to the same height, a slim frame top and bottom, its door at plan y 176 to 236 */
    const pane = (x0, z0, x1, z1) => {
      const w = Math.max(x1 - x0, 0.02), d = Math.max(z1 - z0, 0.02);
      add('glass', K.rbox(w, WALL_H - 0.03, d, 0.008, 1), [(x0 + x1) / 2, (WALL_H - 0.03) / 2, (z0 + z1) / 2]);
      add('leg', K.rbox(Math.max(w, 0.035), 0.03, Math.max(d, 0.035), 0.012), [(x0 + x1) / 2, WALL_H - 0.015, (z0 + z1) / 2]);
      add('leg', K.rbox(Math.max(w, 0.035), 0.03, Math.max(d, 0.035), 0.01), [(x0 + x1) / 2, 0.015, (z0 + z1) / 2]);
      foot(x0, z0, x1, z1, 0.35, 0.1, 0.01);
      hit(x0, z0, x1, z1);
    };
    pane(11.99, 1.5, 12.01, 1.76); pane(11.99, 2.36, 12.01, 5.2); pane(12.0, 5.19, 16, 5.21);
    for (const [x, z] of [[12, 1.76], [12, 2.36], [12, 5.2], [16, 5.2]]) add('leg', K.cyl(0.02, 0.02, WALL_H, 10), [x, WALL_H / 2, z]);
    yield;

    /* ---- the furniture kit ---- */
    function chair(x, z, ry) {
      const p = B.obj(x, z, ry);
      p('seat', K.rbox(0.46, 0.07, 0.44, 0.03), [0, 0.43, 0]);
      p('seat', K.rbox(0.44, 0.4, 0.06, 0.03), [0, 0.72, -0.21], [-0.12, 0, 0]);
      p('leg', K.cyl(0.022, 0.022, 0.3, 10), [0, 0.25, 0]);
      for (let i = 0; i < 5; i++) { const a = i / 5 * Math.PI * 2; p('leg', K.seg([0, 0.05, 0], [Math.sin(a) * 0.25, 0.04, Math.cos(a) * 0.25], 0.018, [2, 6])); }
      disc(x, z, 0.32, 0.55);
    }
    /* a laptop on a desk top, its screen toward the one who sits at it (they sit at -z of its own space) */
    function laptop(x, z, ry, open) {
      const p = B.obj(x, z, ry, TOP_H);
      p('leg', K.rbox(0.32, 0.014, 0.22, 0.006, 1), [0, 0.007, 0]);
      if (!open) { p('leg', K.rbox(0.32, 0.01, 0.22, 0.005, 1), [0, 0.019, 0]); return; }
      p('leg', K.rbox(0.32, 0.215, 0.009, 0.005, 1), [0, 0.112, 0.13], [0.22, 0, 0]);
      p('screen', K.rbox(0.29, 0.18, 0.002, 0.001, 1), [0, 0.112, 0.124], [0.22, 0, 0]);
    }
    /* a slim monitor on a foot, facing the seat: the call tile for someone working from home */
    function monitor(x, z, ry, uid) {
      const p = B.obj(x, z, ry, TOP_H);
      p('leg', K.rbox(0.5, 0.31, 0.024, 0.014), [0, 0.3, 0.04]);
      p('leg', K.cyl(0.013, 0.013, 0.15, 8), [0, 0.075, 0.06]);
      p('leg', K.rbox(0.18, 0.01, 0.13, 0.005, 1), [0, 0.005, 0.06]);
      const m = new T.Matrix4().compose(new T.Vector3(x, TOP_H, z), new T.Quaternion().setFromEuler(new T.Euler(0, ry || 0, 0)), new T.Vector3(1, 1, 1));
      homes.push({uid, m, at: [0, 0.3, 0.04 - 0.0125], w: 0.46, h: 0.27});
    }
    /* a desk lamp: a base, a stem and a dome that glows at night for whoever is at the desk */
    function lamp(x, z, on, cabin) {
      add('leg', K.cyl(0.06, 0.066, 0.016, 20), [x, TOP_H + 0.008, z]);
      add('leg', K.cyl(0.007, 0.007, 0.3, 8), [x, TOP_H + 0.16, z]);
      lamps.push({x, y: TOP_H + 0.31, z, on: !!on, cabin: !!cabin});
    }
    function legsUnder(x0, z0, x1, z1, top) {
      for (const x of [x0 + 0.06, x1 - 0.06]) {
        add('leg', K.rbox(0.03, top - 0.04, 0.03, 0.01), [x, (top - 0.04) / 2, z0 + 0.1]);
        add('leg', K.rbox(0.03, top - 0.04, 0.03, 0.01), [x, (top - 0.04) / 2, z1 - 0.1]);
        add('leg', K.rbox(0.03, 0.03, z1 - z0 - 0.17, 0.01), [x, top - 0.05, (z0 + z1) / 2]);
        add('leg', K.rbox(0.035, 0.02, z1 - z0 - 0.15, 0.008), [x, 0.01, (z0 + z1) / 2]);
      }
    }
    /* a freestanding board on two legs, its face toward +z of its own space */
    function board(x, z, w, h, y0, ry) {
      const p = B.obj(x, z, ry);
      p('leg', K.rbox(w + 0.05, h + 0.05, 0.035, 0.02), [0, y0 + h / 2, 0]);
      p('board', K.rbox(w, h, 0.04, 0.015), [0, y0 + h / 2, 0.006]);
      for (const s of [-1, 1]) {
        p('leg', K.rbox(0.035, y0 + 0.02, 0.035, 0.012), [s * (w / 2 - 0.12), (y0 + 0.02) / 2, -0.03]);
        p('leg', K.rbox(0.04, 0.025, 0.42, 0.01), [s * (w / 2 - 0.12), 0.012, -0.03]);
      }
      const c = Math.cos(ry || 0), s2 = Math.sin(ry || 0), hw = w / 2, hd = 0.24;
      const xs = [x - hw * Math.abs(c) - hd * Math.abs(s2), x + hw * Math.abs(c) + hd * Math.abs(s2)], zs = [z - hw * Math.abs(s2) - hd * Math.abs(c), z + hw * Math.abs(s2) + hd * Math.abs(c)];
      foot(xs[0], zs[0], xs[1], zs[1], 0.5, 0.16);
      hit(xs[0], zs[0], xs[1], zs[1]);
      return p;
    }
    /* dried pampas plumes in a chalk vase */
    function vase(x, z, s, y, stems) {
      const k = s || 1, y0 = y || 0, n = lite ? 4 : (stems || 7);
      const prof = [[0, 0], [0.09, 0], [0.12, 0.08], [0.11, 0.2], [0.06, 0.3], [0.05, 0.34], [0.058, 0.36], [0, 0.36]].map(([a, b]) => new T.Vector2(a * k, b * k));
      add('pot', new T.LatheGeometry(prof, lite ? 12 : 24), [x, y0, z]);
      for (let i = 0; i < n; i++) {
        const a = i * 2.4 + 0.3, lean = 0.18 + (i % 3) * 0.08, h = (0.75 + (i % 4) * 0.09) * k;
        const tx = Math.cos(a) * lean, tz = Math.sin(a) * lean;
        const top = [x + tx * h, y0 + 0.3 * k + h, z + tz * h];
        add('pampas', K.seg([x, y0 + 0.3 * k, z], top, 0.0045 * k, [1, 4]));
        const q = new T.Quaternion().setFromUnitVectors(new T.Vector3(0, 1, 0), new T.Vector3(tx, 1, tz).normalize());
        const e = new T.Euler().setFromQuaternion(q, 'YXZ');
        add('pampas', K.ball(0.045 * k, 10, 8), top, [e.x, e.y, e.z], [0.7, 2.6, 0.7]);
      }
      if (!y) { disc(x, z, 0.16 * k, 0.8); hit(x - 0.15 * k, z - 0.15 * k, x + 0.15 * k, z + 0.15 * k); }
    }

    /* ---- the benches: every slot of the plan; a seat with someone's name on it gets their desk ---- */
    const P = O.PLAN;
    const bySeat = {};
    for (const u of Object.keys(L.seats)) { const s = L.seats[u]; if (!s.cabin) bySeat[s.slot + ':' + s.j] = u; }
    const byUid = {};
    for (const d of D) byUid[d.uid] = d;
    for (const b of L.benches.concat(L.spare || [])) {
      const x0 = cm(b.x), zb = cm(b.y), x1 = x0 + cm(P.BENCH_W), z0 = zb + 0.2, z1 = zb + 1.4;
      B.add('top', K.planSlab(x0, z0, x1, z1, 0.04, TOP_H - 0.035, 0.035, 0.008, 4));
      legsUnder(x0, z0, x1, z1, TOP_H - 0.035);
      add('cell', K.rbox(cm(P.BENCH_W) - 0.2, 0.3, 0.03, 0.012), [(x0 + x1) / 2, TOP_H + 0.15, (z0 + z1) / 2]);
      foot(x0, z0, x1, z1, 0.75, 0.3, 0.05);
      hit(x0, zb, x1, zb + cm(P.BENCH_H));
      for (let j = 0; j < 6; j++) {
        const [col, top] = P.SEAT_ORDER[j];
        const x = x0 + cm(col * P.DESK_W + P.DESK_W / 2);
        const dir = top ? 1 : -1, edge = top ? z0 : z1, seatZ = top ? zb - 0.08 : zb + cm(P.BENCH_H) + 0.08;
        const ry = top ? 0 : Math.PI;
        const uid = b.slot != null ? bySeat[b.slot + ':' + j] : null;
        const d = uid ? byUid[uid] : null;
        if (!d) { chair(x, edge - dir * 0.1, ry); continue; }
        seatsAt[uid] = {x, z: seatZ, h: ry, dir, edge};
        const st = d.state, here = d.place === 'desk';
        const atDesk = st === 'office' && here;
        if (atDesk) chair(x, seatZ, ry);
        else if (st === 'elsewhere' || (st === 'office' && !here)) chair(x + 0.12, seatZ - dir * 0.04, ry + 0.55);
        else chair(x, edge - dir * 0.1, ry);
        if (atDesk) laptop(x, edge + dir * 0.26, ry, true);
        else if (st === 'wfh') monitor(x, edge + dir * 0.36, ry, uid);
        else if (st === 'out' || st === 'elsewhere' || st === 'office') laptop(x - 0.05, edge + dir * 0.3, ry + 0.06, false);
        lamp(x + 0.42, edge + dir * 0.5, atDesk, false);
        if (d.focus && atDesk) pools.push({kind: 'focus', x, z: seatZ + dir * 0.1, r: 1.05});
        /* a stack of papers, its height the open work (the founder's and a manager's view) */
        if (d.pile) for (let i = 0; i < Math.ceil(d.pile / 3); i++) add('cell', K.rbox(0.21, 0.012, 0.29, 0.003, 1), [x - 0.4, TOP_H + 0.006 + i * 0.014, edge + dir * 0.3], [0, 0.04 * (i % 2 ? 1 : -1), 0]);
      }
      yield;
    }

    /* ---- the back: the calendar wall, the task board, the clock ---- */
    {
      const w = 2.4, h = 1.0, y0 = 0.82, x = 4.6, z = 1.7;
      const p = board(x, z, w, h, y0);
      const cw = (w - 0.24) / 7, ch = (h - 0.26) / 5;
      for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) {
        const today = r === 2 && c === 3, ev = (r * 7 + c) % 5 === 1 && !today;
        p(today ? 'ink' : ev ? 'mark' : 'cell', K.rbox(cw - 0.03, ch - 0.03, 0.012, 0.01, 1), [-w / 2 + 0.12 + cw * (c + 0.5), y0 + 0.1 + ch * (4 - r + 0.5), 0.032]);
      }
      p('mark', K.rbox(0.7, 0.04, 0.01, 0.01, 1), [-w / 2 + 0.47, y0 + h - 0.08, 0.032]);
      anchors.calendar = [x, y0 + h + 0.14, z];
    }
    {
      const w = 2.6, h = 1.1, y0 = 0.78, x = 8.1, z = 1.7;
      const p = board(x, z, w, h, y0);
      const colW = w / 3;
      for (let c = 0; c < 3; c++) {
        const cx = -w / 2 + colW * (c + 0.5);
        p('mark', K.rbox(0.42, 0.035, 0.01, 0.01, 1), [cx - colW / 2 + 0.3, y0 + h - 0.08, 0.032]);
        if (c) p('cell', K.rbox(0.008, h - 0.14, 0.008, 0.003, 1), [cx - colW / 2, y0 + h / 2 - 0.03, 0.03]);
        const n = [4, 2, 3][c];
        for (let k = 0; k < n; k++) {
          const cy = y0 + h - 0.24 - k * 0.2;
          p(c === 1 && k === 0 ? 'ink' : 'cell', K.rbox(colW - 0.16, 0.16, 0.014, 0.012, 1), [cx, cy, 0.034]);
          p('mark', K.rbox((colW - 0.36) * (0.5 + 0.4 * ((k + c) % 2)), 0.022, 0.006, 0.004, 1), [cx - 0.12, cy + 0.03, 0.042]);
        }
      }
      anchors.board = [x, y0 + h + 0.14, z];
    }
    {
      const x = 11.55, z = 1.72;
      add('leg', K.cyl(0.022, 0.022, 1.7, 12), [x, 0.85, z]);
      add('leg', K.cyl(0.16, 0.18, 0.025, 28), [x, 0.0125, z]);
      add('leg', K.cyl(0.28, 0.28, 0.06, 48), [x, 1.92, z + 0.02], [Math.PI / 2, 0, 0]);
      add('board', K.cyl(0.255, 0.255, 0.062, 48), [x, 1.92, z + 0.024], [Math.PI / 2, 0, 0]);
      for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; add('mark', K.rbox(0.012, i % 3 ? 0.03 : 0.05, 0.006, 0.003, 1), [x + Math.sin(a) * 0.22, 1.92 + Math.cos(a) * 0.22, z + 0.058], [0, 0, -a]); }
      add('ink', K.rbox(0.016, 0.13, 0.008, 0.004, 1), [x + 0.04, 1.92 + 0.035, z + 0.062], [0, 0, -1.15]);
      add('ink', K.rbox(0.012, 0.19, 0.008, 0.004, 1), [x - 0.02, 1.92 + 0.085, z + 0.064], [0, 0, 0.22]);
      add('ink', K.ball(0.016, 10, 8), [x, 1.92, z + 0.07]);
      disc(x, z, 0.2, 0.5);
      hit(x - 0.2, z - 0.2, x + 0.2, z + 0.2);
      anchors.clock = [x, 2.3, z];
    }
    /* the review wall: a slim pinboard facing the studio */
    {
      const p = board(11.72, 4.1, 2.0, 0.8, 0.5, -Math.PI / 2);
      for (let k = 0; k < 5; k++) p(k === 2 ? 'mark' : 'cell', K.rbox(0.26, 0.2, 0.012, 0.01, 1), [-0.8 + k * 0.4, 0.5 + 0.4 + 0.12 * ((k % 2) ? 1 : -1), 0.032]);
      anchors.review = [11.72, 1.48, 4.1];
    }
    /* the client wall: a long gallery ledge with six framed pieces */
    {
      const x0 = 0.3, x1 = 1.75, z0 = 2.1, z1 = 4.8;
      B.add('board', K.planSlab(x0, z0, x1, z1, 0.1, 0, 0.62, 0.02, 6));
      add('cell', K.rbox(x1 - x0 - 0.12, 0.04, z1 - z0 - 0.12, 0.01), [(x0 + x1) / 2, 0.64, (z0 + z1) / 2]);
      foot(x0, z0, x1, z1, 1, 0.22, 0.1);
      hit(x0, z0, x1, z1);
      for (let k = 0; k < 6; k++) {
        const z = z0 + 0.3 + k * 0.42, x = 1.02 + (k % 2 ? 0.16 : -0.16);
        const p = B.obj(x, z, Math.PI / 2, 0.66);
        p('leg', K.rbox(0.34, 0.28 + 0.06 * (k % 3), 0.03, 0.012), [0, 0.16, 0], [-0.12, 0, 0]);
        p('board', K.rbox(0.3, 0.24 + 0.06 * (k % 3), 0.032, 0.01), [0, 0.16, 0.004], [-0.12, 0, 0]);
        const mark = [K.ball(0.05, 16, 12), K.rbox(0.09, 0.09, 0.01, 0.02), new T.TorusGeometry(0.045, 0.012, 8, 24)][k % 3];
        p(k === 1 ? 'ink' : 'mark', mark, [0, 0.17, 0.024], [-0.12, 0, 0], k % 3 === 0 ? [1, 1, 0.2] : null);
      }
      anchors.clients = [1.0, 1.15, 3.45];
    }
    yield;
    /* attendance: a slim kiosk by the way in */
    {
      const x = 1.86, z = 6.4;
      add('board', K.rbox(0.3, 1.0, 0.24, 0.08), [x, 0.5, z]);
      const p = B.obj(x, z, 0, 1.0);
      p('screen', K.rbox(0.26, 0.012, 0.19, 0.01, 1), [0, 0.03, 0.01], [-0.5, 0, 0]);
      add('leg', K.rbox(0.3, 0.02, 0.22, 0.01), [x, 1.025, z + 0.005], [-0.5, 0, 0]);
      disc(x, z, 0.22, 0.8);
      hit(x - 0.18, z - 0.15, x + 0.18, z + 0.15);
      anchors.attendance = [x, 1.32, z];
    }
    /* reception: a rounded counter with a plume on it */
    {
      const z0 = Z(722), z1 = Z(792);
      B.add('board', K.planSlab(0.35, z0, 1.85, z1, 0.34, 0, 0.98, 0.03, 12));
      B.add('cell', K.planSlab(0.42, z0 + 0.07, 1.78, z1 - 0.07, 0.3, 0.98, 0.03, 0.01, 12));
      foot(0.35, z0, 1.85, z1, 1, 0.2, 0.3);
      hit(0.35, z0, 1.85, z1);
      vase(0.62, (z0 + z1) / 2, 0.55, 1.01, 5);
      anchors.reception = [1.3, 1.5, (z0 + z1) / 2];
    }
    /* the COO's desk, and beside it the round charging pad it sits on, at desk height */
    {
      const x0 = 3.0, x1 = 5.2, z0 = Z(896), z1 = Z(970);
      B.add('top', K.planSlab(x0, z0, x1, z1, 0.06, TOP_H - 0.035, 0.035, 0.008, 4));
      legsUnder(x0, z0, x1, z1, TOP_H - 0.035);
      foot(x0, z0, x1, z1, 0.75, 0.28, 0.05);
      hit(x0, z0, x1, z1);
      const mx = 3.75, mz = (z0 + z1) / 2 + 0.12;
      const p = B.obj(mx, mz, Math.PI, TOP_H);
      p('leg', K.rbox(0.66, 0.38, 0.03, 0.02), [0, 0.33, 0]);
      p('leg', K.cyl(0.015, 0.015, 0.16, 10), [0, 0.08, 0.03]);
      p('leg', K.rbox(0.22, 0.012, 0.16, 0.006, 1), [0, 0.006, 0.03]);
      p('screen', K.rbox(0.62, 0.34, 0.002, 0.001, 1), [0, 0.33, 0.016]);
      lamp(4.6, (z0 + z1) / 2 + 0.05, false, false);
      vase(4.98, (z0 + z1) / 2 + 0.1, 0.45, TOP_H, 4);
      const pz = Z(862);
      add('board', K.cyl(0.2, 0.24, TOP_H, 40), [4.1, TOP_H / 2, pz]);
      add('cell', K.cyl(0.25, 0.25, 0.025, 40), [4.1, TOP_H + 0.012, pz]);
      add('mark', new T.TorusGeometry(0.21, 0.007, 6, lite ? 24 : 48), [4.1, TOP_H + 0.026, pz], [Math.PI / 2, 0, 0]);
      disc(4.1, pz, 0.26, 0.9);
      hit(3.86, pz - 0.24, 4.34, pz + 0.24);
      anchors.desk = [4.1, 1.42, (z0 + z1) / 2];
    }
    /* the mail room: a low sorter with letters standing in it */
    {
      const x0 = 5.6, x1 = 7.0, z0 = Z(904), z1 = Z(964);
      B.add('board', K.planSlab(x0, z0, x1, z1, 0.06, 0, 0.82, 0.02, 4));
      foot(x0, z0, x1, z1, 1, 0.2, 0.06);
      hit(x0, z0, x1, z1);
      for (let c = 0; c < 4; c++) add('cell', K.rbox(0.012, 0.2, 0.5, 0.004, 1), [x0 + 0.1 + c * 0.4, 0.92, (z0 + z1) / 2]);
      for (let c = 0; c < 3; c++) for (let k = 0; k < 3; k++) {
        const x = x0 + 0.22 + c * 0.4 + k * 0.08;
        add((c + k) % 4 === 1 ? 'cell' : 'board', K.rbox(0.012, 0.15 + 0.03 * ((c + k) % 2), 0.28, 0.004, 1), [x, 0.9, (z0 + z1) / 2], [0, 0, 0.12 * (k - 1)]);
      }
      anchors.mail = [6.3, 1.32, (z0 + z1) / 2];
    }
    /* coffee: a counter, a machine, three cups */
    {
      const x0 = 8.2, x1 = 9.8, z0 = Z(910), z1 = Z(964);
      B.add('board', K.planSlab(x0, z0, x1, z1, 0.08, 0, 0.9, 0.02, 4));
      B.add('cell', K.planSlab(x0 + 0.03, z0 + 0.03, x1 - 0.03, z1 - 0.03, 0.06, 0.9, 0.03, 0.01, 4));
      foot(x0, z0, x1, z1, 1, 0.2, 0.08);
      hit(x0, z0, x1, z1);
      add('leg', K.rbox(0.34, 0.4, 0.3, 0.06), [8.55, 0.93 + 0.2, (z0 + z1) / 2]);
      add('mark', K.rbox(0.2, 0.06, 0.04, 0.02), [8.55, 1.06, z0 + 0.12]);
      for (let k = 0; k < 3; k++) add('board', K.cyl(0.04, 0.034, 0.09, 18), [9.05 + k * 0.16, 0.975, (z0 + z1) / 2 - 0.05 + (k % 2) * 0.06]);
    }
    /* lunch: a round oak table, its stools, and three more at the coffee counter */
    {
      const cx = 10.7, cz = Z(890);
      B.add('top', K.cyl(0.38, 0.38, 0.035, 48), [cx, 0.72, cz]);
      add('leg', K.cyl(0.03, 0.03, 0.7, 12), [cx, 0.36, cz]);
      add('leg', K.cyl(0.22, 0.24, 0.02, 32), [cx, 0.01, cz]);
      disc(cx, cz, 0.42, 0.6, 0.2);
      hit(cx - 0.38, cz - 0.38, cx + 0.38, cz + 0.38);
      for (const [px, py] of O.LUNCH_SEATS) {
        const x = cm(px), z = Z(py);
        add('seat', K.cyl(0.16, 0.15, 0.06, 28), [x, 0.46, z]);
        add('leg', K.cyl(0.02, 0.02, 0.43, 10), [x, 0.215, z]);
        add('leg', K.cyl(0.12, 0.13, 0.015, 24), [x, 0.0075, z]);
        disc(x, z, 0.17, 0.6, 0.1);
      }
      vase(11.42, Z(962), 1.05);
      ao.push({circle: [cx, cz, 1.05], fill: 'rug'});
    }
    yield;

    /* ---- the meeting room: a table at MEET_SEATS' heart, six chairs, a screen ---- */
    ao.push({rect: [12.0, 1.5, 16.0, 5.2], fill: 'rug', r: 0});
    {
      const ms = O.MEET_SEATS;
      B.add('top', K.planSlab(13.12, 3.37, 14.88, 3.97, 0.3, 0.7, 0.04, 0.012, 16));
      for (const x of [13.55, 14.45]) { add('leg', K.cyl(0.035, 0.035, 0.7, 12), [x, 0.35, 3.67]); add('leg', K.cyl(0.2, 0.22, 0.02, 28), [x, 0.01, 3.67]); }
      foot(13.12, 3.37, 14.88, 3.97, 0.7, 0.3, 0.3);
      hit(13.12, 3.37, 14.88, 3.97);
      ms.forEach(([px, py]) => { const x = cm(px), z = cm(py); chair(x, z, Math.atan2(14.0 - x, 3.67 - z)); });
      const p = board(14.0, 1.66, 1.9, 0.95, 0.72);
      p('screen', K.rbox(1.8, 0.85, 0.004, 0.002, 1), [0, 0.72 + 0.475, 0.03]);
      p('mark', K.rbox(0.7, 0.05, 0.006, 0.004, 1), [-0.45, 0.72 + 0.78, 0.034]);
      anchors.meeting = [15.3, 1.3, 2.4];
    }
    /* a planter between the meeting room and the cabin */
    {
      add('pot', K.rbox(3.9, 0.42, 0.3, 0.06), [14.03, 0.21, 5.4]);
      foot(12.08, 5.25, 15.98, 5.55, 0.9, 0.12);
      for (const x of [12.7, 14.0, 15.3]) vase(x, 5.4, 0.8, 0.42, 6);
    }

    /* ---- the cabin: Kaavish's desk at his seat, the lounge, the tray at the door, the books ---- */
    ao.push({rect: [12.06, 5.72, 16.0, H], fill: 'rug', r: 0});
    ao.push({rect: [12.9, 6.55, 15.75, Z(960)], fill: 'rug-edge', r: 0.3});
    const ks = L.founder ? L.seats[L.founder] : null;
    const cab = {x: ks ? cm(ks.x) : 14.5, z: ks ? cm(ks.y) : Z(712)};
    {
      const z0 = cab.z + 0.28, z1 = z0 + 0.66, x0 = cab.x - 0.9, x1 = cab.x + 0.9;
      B.add('top', K.planSlab(x0, z0, x1, z1, 0.06, TOP_H - 0.035, 0.035, 0.008, 6));
      legsUnder(x0, z0, x1, z1, TOP_H - 0.035);
      foot(x0, z0, x1, z1, 0.8, 0.26, 0.08);
      hit(x0, z0, x1, z1);
      const p = B.obj(cab.x, z0 + 0.4, 0, TOP_H);
      p('leg', K.rbox(0.6, 0.36, 0.03, 0.02), [0, 0.32, 0]);
      p('leg', K.cyl(0.015, 0.015, 0.15, 10), [0, 0.075, 0.02]);
      p('leg', K.rbox(0.2, 0.012, 0.15, 0.006, 1), [0, 0.006, 0.02]);
      p('screen', K.rbox(0.56, 0.32, 0.002, 0.001, 1), [0, 0.32, -0.016]);
      lamp(cab.x + 0.6, z0 + 0.3, !!o.kaavishOnline, true);
      chair(cab.x, cab.z, 0);
      seatsAt.cabin = {x: cab.x, z: cab.z, h: 0, dir: 1, edge: z0};
    }
    /* the lounge: a low sofa by the front, where he sits when he is away */
    {
      const x0 = 13.0, x1 = 14.9, z0 = Z(930), z1 = Z(995);
      B.add('seat', K.planSlab(x0, z0, x1, z1, 0.16, 0.0, 0.42, 0.06, 8));
      B.add('seat', K.planSlab(x0, z1 - 0.24, x1, z1 + 0.02, 0.12, 0.38, 0.32, 0.06, 8));
      foot(x0, z0, x1, z1 + 0.02, 1, 0.2, 0.16);
      hit(x0, z0, x1, z1);
      seatsAt.lounge = {x: 13.95, z: z0 + 0.2, h: Math.PI, dir: -1, y: 0.42};
    }
    /* the tray: a small stand at the cabin door, cards waiting */
    {
      const tx = 12.49, tz = 7.05;
      add('board', K.rbox(0.5, 0.66, 0.32, 0.05), [tx, 0.33, tz]);
      add('leg', K.rbox(0.36, 0.05, 0.24, 0.012), [tx, 0.685, tz]);
      for (let k = 0; k < 3; k++) add(k === 2 ? 'mark' : 'board', K.rbox(0.3, 0.008, 0.21, 0.003, 1), [tx + 0.004 * k, 0.69 + k * 0.01, tz - 0.003 * k], [0, 0.05 * k, 0]);
      foot(tx - 0.25, tz - 0.16, tx + 0.25, tz + 0.16, 0.8, 0.14);
      hit(tx - 0.25, tz - 0.16, tx + 0.25, tz + 0.16);
      anchors.tray = [tx, 1.05, tz];
    }
    /* the books cabinet, the owner's alone */
    if (o.owner) {
      const bx = 15.62, bz = Z(942);
      add('board', K.rbox(0.56, 1.2, 0.84, 0.03), [bx, 0.6, bz]);
      for (let r = 0; r < 3; r++) {
        add('cell', K.rbox(0.5, 0.012, 0.76, 0.004, 1), [bx - 0.02, 0.25 + r * 0.36, bz]);
        for (let k = 0; k < 7; k++) {
          const hh = 0.22 + 0.06 * ((k * 7 + r * 3) % 4) / 3;
          const role = ['mark', 'cell', 'leg', 'board', 'seat'][(k + r * 2) % 5];
          add(role, K.rbox(0.22, hh, 0.07, 0.01, 1), [bx - 0.2, 0.26 + r * 0.36 + hh / 2, bz - 0.3 + k * 0.095], [0, 0, k === 6 ? 0.18 : 0]);
        }
      }
      foot(bx - 0.28, bz - 0.42, bx + 0.28, bz + 0.42, 1, 0.2, 0.03);
      hit(bx - 0.28, bz - 0.42, bx + 0.28, bz + 0.42);
      anchors.books = [bx, 1.45, bz];
    }
    vase(15.62, 6.08, 1.15);
    yield;

    /* ---- the way in, and the corners ---- */
    vase(0.48, 1.86, 1.25);
    ao.push({circle: [1.05, Z(862), 0.62], fill: 'rug'});
    B.add('seat', K.planSlab(0.3, Z(935), 1.9, Z(980), 0.2, 0.0, 0.44, 0.05, 8));
    foot(0.3, Z(935), 1.9, Z(980), 1, 0.16, 0.2);
    hit(0.3, Z(935), 1.9, Z(980));
    vase(2.3, Z(962), 0.95);

    /* ---- what Kaavish placed (office/plan props), snapped to the 25 cm grid ---- */
    const props = L.props || {};
    for (const id of Object.keys(props)) {
      const pr = props[id], x = cm(pr.x), z = cm(pr.y), ry = -(pr.r || 0) * Math.PI / 180;
      /* a footprint (half width a, half depth b) on the floor, turned with the prop */
      const turned = (pr.r || 0) % 180 === 90;
      const box = (a, b) => (turned ? [x - b, z - a, x + b, z + a] : [x - a, z - b, x + a, z + b]);
      if (pr.k === 'plant') vase(x, z, 1.0);
      else if (pr.k === 'screen') { const p = board(x, z, 1.2, 0.8, 0.6, ry); p('screen', K.rbox(1.1, 0.7, 0.004, 0.002, 1), [0, 1.0, 0.03]); }
      else if (pr.k === 'sofa') {
        const p = B.obj(x, z, ry);
        p('seat', K.rbox(1.6, 0.4, 0.7, 0.12), [0, 0.2, 0]);
        p('seat', K.rbox(1.6, 0.34, 0.2, 0.08), [0, 0.52, -0.26]);
        foot(...box(0.8, 0.35), 1, 0.18, 0.12);
        hit(...box(0.8, 0.4));
      } else if (pr.k === 'shelf') {
        const p = B.obj(x, z, ry);
        p('board', K.rbox(1.0, 1.1, 0.34, 0.03), [0, 0.55, 0]);
        for (let r = 0; r < 3; r++) p('cell', K.rbox(0.92, 0.012, 0.3, 0.004, 1), [0, 0.22 + r * 0.32, 0.02]);
        foot(...box(0.5, 0.2), 1, 0.18, 0.03);
        hit(...box(0.5, 0.2));
      } else if (pr.k === 'lamp') {
        add('leg', K.cyl(0.14, 0.15, 0.02, 24), [x, 0.01, z]);
        add('leg', K.cyl(0.012, 0.012, 1.5, 8), [x, 0.76, z]);
        lamps.push({x, y: 1.52, z, on: false, floor: true});
        disc(x, z, 0.16, 0.6);
        hit(x - 0.15, z - 0.15, x + 0.15, z + 0.15);
      }
    }
    return {roles: B.roles, ao, anchors, colliders, lamps, pools, homes, seats: seatsAt, slab: S};
  }

  /* run a build generator to its end */
  function run(gen) { for (;;) { const r = gen.next(); if (r.done) return r.value; } }

  /* ---------- canvas textures ---------- */
  const css = (c, a) => (a == null ? 'rgb(' : 'rgba(') + c.slice(0, 3).map(v => Math.round(v)).join(',') + (a == null ? ')' : ',' + a + ')');
  const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  /* the floor: rugs, then a soft contact shade under every footprint (a blurred shadow of a shape kept off the
     canvas). col: the resolved tokens; k: the shade's strength for the theme */
  function floorTexture(T, S, ao, col, k, maxPx) {
    const W = S.x1 - S.x0, D = S.z1 - S.z0;
    const pw = maxPx || 2048, ph = Math.round(pw * D / W), u = pw / W;
    const cv = canvas(pw, ph);
    const g = cv.getContext('2d');
    const X = x => (x - S.x0) * u, Zc = z => (z - S.z0) * u;
    g.fillStyle = css(col.floor); g.fillRect(0, 0, pw, ph);
    const rr = (x0, z0, x1, z1, r) => { g.beginPath(); g.roundRect(X(x0), Zc(z0), (x1 - x0) * u, (z1 - z0) * u, Math.max(0, r * u)); };
    for (const a of ao) {
      if (!a.fill) continue;
      g.fillStyle = css(col[a.fill] || col.floor);
      if (a.rect) { rr(a.rect[0], a.rect[1], a.rect[2], a.rect[3], a.r || 0); g.fill(); }
      if (a.circle) { g.beginPath(); g.arc(X(a.circle[0]), Zc(a.circle[1]), a.circle[2] * u, 0, Math.PI * 2); g.fill(); }
    }
    const off = pw * 4;
    for (const a of ao) {
      if (a.fill) continue;
      g.save();
      g.shadowColor = css(col.shade, Math.min(1, k * (a.k == null ? 1 : a.k)).toFixed(3));
      g.shadowBlur = (a.blur || 0.15) * u;
      g.shadowOffsetX = off;
      g.fillStyle = css(col.shade);
      g.beginPath();
      if (a.cx != null) g.arc(X(a.cx) - off, Zc(a.cz), a.rad * u, 0, Math.PI * 2);
      else g.roundRect(X(a.x0) - off, Zc(a.z0), (a.x1 - a.x0) * u, (a.z1 - a.z0) * u, (a.r || 0) * u);
      g.fill();
      g.restore();
    }
    const t = new T.CanvasTexture(cv);
    t.colorSpace = T.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }
  /* about 1 percent noise, baked in: there is no post pass, so this is what keeps a gradient smooth */
  function dither(g, w, h, amp) {
    const img = g.getImageData(0, 0, w, h), p = img.data;
    let s = 1234567;
    for (let i = 0; i < p.length; i += 4) {
      s = (s * 16807) % 2147483647;
      const n = ((s >> 16) & 7) / 7 * 2 - 1;
      const d = Math.round(n * amp);
      p[i] = Math.max(0, Math.min(255, p[i] + d)); p[i + 1] = Math.max(0, Math.min(255, p[i + 1] + d)); p[i + 2] = Math.max(0, Math.min(255, p[i + 2] + d));
    }
    g.putImageData(img, 0, 0);
  }
  /* a faint grain, multiplied by the wood's own colour */
  function grainTexture(T) {
    const W = 512, c = canvas(W, W), g = c.getContext('2d');
    g.fillStyle = 'rgb(255,255,255)';
    g.fillRect(0, 0, W, W);
    let seed = 7;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 110; i++) {
      const y = rnd() * W, a = 0.012 + rnd() * 0.026, w = 0.8 + rnd() * 2.2, amp = 1 + rnd() * 4, f = 1 + Math.floor(rnd() * 3);
      g.strokeStyle = 'rgba(0,0,0,' + a.toFixed(3) + ')';
      g.lineWidth = w;
      g.beginPath();
      for (let x = -4; x <= W + 4; x += 8) { const yy = y + Math.sin(x / W * Math.PI * 2 * f + i) * amp; if (x < 0) g.moveTo(x, yy); else g.lineTo(x, yy); }
      g.stroke();
    }
    const t = new T.CanvasTexture(c);
    t.colorSpace = T.SRGBColorSpace;
    t.wrapS = t.wrapT = T.RepeatWrapping;
    t.anisotropy = 4;
    return t;
  }
  /* soft round textures: a contact shade, a pool of light (white, tinted by the material) */
  function radial(T, stops, size) {
    const n = size || 128, cv = canvas(n, n);
    const g = cv.getContext('2d'), gr = g.createRadialGradient(n / 2, n / 2, 0, n / 2, n / 2, n / 2);
    for (const [o, a] of stops) gr.addColorStop(o, 'rgba(255,255,255,' + a + ')');
    g.fillStyle = gr; g.fillRect(0, 0, n, n);
    const t = new T.CanvasTexture(cv); t.colorSpace = T.SRGBColorSpace;
    return t;
  }
  /* the slab's own shadow on the backdrop: a long soft rounded rectangle, white, tinted by its material */
  function dropShadowTexture(T) {
    const pw = 512, ph = 320, cv = canvas(pw, ph), g = cv.getContext('2d'), off = pw * 3;
    const layer = (inset, blur, a) => {
      g.save(); g.shadowColor = 'rgba(255,255,255,' + a + ')'; g.shadowBlur = blur; g.shadowOffsetX = off;
      g.fillStyle = 'rgb(255,255,255)'; g.beginPath(); g.roundRect(inset - off, inset * 0.62, pw - inset * 2, ph - inset * 1.24, 30); g.fill(); g.restore();
    };
    layer(80, 60, 0.75);
    layer(100, 26, 0.55);
    const t = new T.CanvasTexture(cv); t.colorSpace = T.SRGBColorSpace;
    return t;
  }
  /* the studio backdrop: a soft radial from the token centre to the token edge, dithered */
  function backdropTexture(T, col, aspect, cv0) {
    const h = 512, w = Math.round(h * Math.max(0.4, Math.min(2.5, aspect || 1.6)));
    const cv = cv0 && cv0.width === w ? cv0 : canvas(w, h);
    const g = cv.getContext('2d', {willReadFrequently: true});
    const gr = g.createRadialGradient(w * 0.5, h * 0.46, 0, w * 0.5, h * 0.5, Math.max(w, h) * 0.72);
    gr.addColorStop(0, css(col['back-c'])); gr.addColorStop(1, css(col['back-e']));
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    dither(g, w, h, 2);
    const t = new T.CanvasTexture(cv); t.colorSpace = T.SRGBColorSpace;
    return t;
  }
  /* the plinth's top face: a rounded rectangle fanned from its centre, mapped onto the floor canvas */
  function floorFace(T, S, inset) {
    const b = inset || 0.05, x0 = S.x0 + b, x1 = S.x1 - b, z0 = S.z0 + b, z1 = S.z1 - b, r = S.r - b, n = 12;
    const pts = [];
    const corner = (cx, cz, a0) => { for (let i = 0; i <= n; i++) { const a = a0 + i / n * Math.PI / 2; pts.push([cx + Math.cos(a) * r, cz + Math.sin(a) * r]); } };
    corner(x1 - r, z1 - r, 0); corner(x0 + r, z1 - r, Math.PI / 2); corner(x0 + r, z0 + r, Math.PI); corner(x1 - r, z0 + r, Math.PI * 1.5);
    const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2, W = S.x1 - S.x0, D = S.z1 - S.z0;
    const pos = [cx, 0.0005, cz], uv = [(cx - S.x0) / W, 1 - (cz - S.z0) / D], nrm = [0, 1, 0], idx = [];
    pts.forEach(([x, z]) => { pos.push(x, 0.0005, z); uv.push((x - S.x0) / W, 1 - (z - S.z0) / D); nrm.push(0, 1, 0); });
    for (let i = 1; i <= pts.length; i++) idx.push(0, i % pts.length + 1, i);
    const g = new T.BufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute(pos, 3));
    g.setAttribute('normal', new T.Float32BufferAttribute(nrm, 3));
    g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2));
    g.setIndex(idx);
    return g;
  }

  M.office3d = Object.assign(M.office3d || {}, {world: {build, run, slab, kit, floorTexture, grainTexture, radial, dropShadowTexture, backdropTexture, floorFace, css}});
})();
