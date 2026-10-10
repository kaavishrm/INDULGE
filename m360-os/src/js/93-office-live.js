/* module: office live (v35). Kaavish in the office, and the live channel that carries him to everyone.
   He alone walks his avatar (a click or tap on the floor, a desk, a station or the COO; W A S D while the floor
   has focus), talks from the office (the composer under the scene) and arranges it (Arrange, 3D on a desktop).
   Everyone else watches: his walk and his words reach every open office within about a second, through the
   room's presence on claude.ai and through the stage on the team site (src/standalone/shim.js, x/stage).

     M.officeLive.canDrive(ctx)             the owner, on his own view, never a preview
     M.officeLive.useKaavish(ctx)           {live, mode, seq, say, to}: one descriptor for the flat and 3D views
     M.officeLive.sample(now)               {x, y, h, mode, walkPhase, talking}: where he is drawn at that moment
     M.officeLive.useController(api, data)  the owner's pointer and keys on the 3D floor (the scene api of M.office3d)
     M.officeLive.walkTo(target), say(text), clear()    false, and nothing sent, for anyone else
     M.officeLive.Composer({data}), Arrange({api, data})
     M.officeLive.planWrite(ctx, patch)     one write to office/plan: rev + 1, whole top-level maps, ids only
     M.officeLive.state()                   {role, seq, mode, x, y, say, peers}

   Presence carries three fields and nothing else: o3 (his walk: seq s, mode m, points p, speed v, the stop point
   x and y, heading h in degrees, pad speeds vx and vy, the target to, the plan rev lv), say ({id, t}) and o3w (this
   page has the office open). Plan centimetres throughout. A walk plays by intent, from where the change arrived on
   this page, so two devices' clocks are never compared. Only presence sent by the founder's own account (by) is
   believed; a uid a page claims for itself never is. Drawers open on his screen alone and nothing in them is sent. */
'use strict';
(function () {
  const {html, React, U, UI} = M;
  const {useState, useEffect, useRef, useMemo} = React;
  const O = () => M.office || {};

  const WALK_V = 140, PAD_V = 160, EASE_S = .25, MAX_PTS = 16;  /* centimetres a second, seconds */
  const NEAR = 150;                 /* a desk, a station or the COO this close opens at once */
  const PAD_MS = 260;               /* pad presence at most four a second, a final stop included */
  const PAD_FRESH = 800, PAD_DV = .1, PAD_DH = 15;
  const RECKON_MS = 1000, TAU = 120, BLEND_MS = 300;
  const IDLE_MS = 10 * 60000;
  const SAY_MAX = 280, CPS = 30;
  const FOOT = 22;                  /* his footprint against the furniture */
  const GRID = 25, PROPS_MAX = 40, LABEL_MAX = 32;
  const DEG = 180 / Math.PI;
  const clamp = (lo, hi, v) => Math.max(lo, Math.min(hi, v));
  const num = v => (typeof v === 'number' && isFinite(v) ? v : null);
  const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  /* a heading in whole degrees: 0 faces down the plan (the front of the floor), a turn as the figures' own */
  const hdg = (dx, dy) => Math.round(Math.atan2(dx, dy) * DEG);
  /* plain text, as the room wants it and the stage cleans his words: a control character or a line break is a space, a
     format or private use character (a soft hyphen, a direction mark) is dropped, and a zero width joiner or non joiner
     stays only between two characters, once, as emoji and Indic scripts need it. Spaces fold; cut by characters */
  const SPACE = /[\s\p{Cc}\p{Zl}\p{Zp}]/u, HIDDEN = /[\p{Cf}\p{Co}]/u;
  const FILLER = [4447, 4448, 12644, 65440], JOINER = [8204, 8205];
  const gone = ch => HIDDEN.test(ch) || FILLER.indexOf(ch.codePointAt(0)) >= 0;
  const blank = ch => !ch || SPACE.test(ch) || gone(ch);
  function plain(s, max) {
    const cs = Array.from(String(s == null ? '' : s)), out = [];
    cs.forEach((ch, i) => {
      if (JOINER.indexOf(ch.codePointAt(0)) >= 0) { if (!blank(out[out.length - 1]) && !blank(cs[i + 1])) out.push(ch); return; }
      if (!gone(ch)) out.push(SPACE.test(ch) ? ' ' : ch);
    });
    const cut = Array.from(out.join('').replace(/\s+/g, ' ').trim()).slice(0, max);
    while (cut.length && JOINER.indexOf(cut[cut.length - 1].codePointAt(0)) >= 0) cut.pop();
    return cut.join('').trim();
  }

  /* ---------- who may drive ---------- */
  const canDrive = ctx => !!(ctx && ctx.isOwner && !ctx.viewAs && ctx.uid && ctx.uid === ctx.founderUid);

  /* ---------- what the views last handed in; the app's live context when there is one (it moves every minute) ---------- */
  const env = {ctx: null, L: null, api: null, room: null, off: null};
  const layoutOf = ctx => { try { return O().layout ? O().layout(ctx) : null; } catch (e) { return null; } };
  function bind(ctx) { if (ctx) env.ctx = ctx; }
  const live = () => M.lastCtx || env.ctx;
  const floor = () => { const L = layoutOf(live()); if (L) env.L = L; return env.L; };
  const planRev = ctx => { const p = (ctx && ctx.office && ctx.office.plan) || null; return p ? Math.max(0, Math.round(Number(p.rev) || 0)) : 0; };

  /* ---------- the floor: stand points, routes, the furniture (M.office when it has them) ---------- */
  const sy = (L, y) => (y >= 700 ? y + ((L && L.grow) || 0) : y);
  function seatOf(L) {
    const c = live(), fu = c && c.founderUid;
    const s = L && fu && L.seats && L.seats[fu];
    return s ? {x: s.x, y: s.y} : {x: 1450, y: 712 + ((L && L.grow) || 0)};
  }
  /* where the COO is now: the spot the scene shows */
  function cooSpot() {
    try { const el = document.querySelector('.office .office-mascot[data-spot]'); return (el && el.getAttribute('data-spot')) || 'desk'; } catch (e) { return 'desk'; }
  }
  function stationAt(L, k) {
    const s = (O().STATION_POS || {})[k] || (O().SPOTS || {})[k];
    if (!s) return null;
    const via = s.via || [s.x, s.y];
    return {x: s.x, y: sy(L, s.y), via: {x: via[0], y: sy(L, via[1])}};
  }
  /* where he stands to reach it: the office's own rule (M.office.standPoint), the COO resolved where it is now */
  function standAt(L, target) {
    if (target && typeof target === 'object') return {x: Math.round(target.x), y: Math.round(target.y)};
    const t = String(target || '');
    try { return O().standPoint(L, t, t === 'coo' ? cooSpot() : undefined); } catch (e) { return null; }
  }
  /* what he turns to face on arrival */
  function faceOf(L, to, at) {
    let p = null;
    if (to.indexOf('desk:') === 0) p = L.seats && L.seats[to.slice(5)];
    else if (to === 'coo') p = stationAt(L, cooSpot());
    else if (to !== 'floor' && to !== 'cabin') p = stationAt(L, to);
    return p && dist(p, at) > 1 ? hdg(p.x - at.x, p.y - at.y) : 0;
  }
  function routeOf(L, from, to) {
    let pts = null;
    try { pts = O().route ? O().route(L, from, to) : null; } catch (e) { pts = null; }
    if (!pts || pts.length < 2) pts = [from, to];
    pts = pts.map(p => ({x: Math.round(p.x), y: Math.round(p.y)}));
    return pts.length > MAX_PTS ? pts.slice(0, MAX_PTS - 1).concat([pts[pts.length - 1]]) : pts;
  }
  const aislesOf = L => O().aisles(L);
  /* the scene's recorded furniture, [x0, y0, x1, y1] in plan centimetres */
  const collidersOf = api => { try { return ((api && api.colliders && api.colliders()) || []).filter(r => Array.isArray(r) && r.length >= 4); } catch (e) { return []; } };
  const inRect = (r, x, y, pad) => x > Math.min(r[0], r[2]) - pad && x < Math.max(r[0], r[2]) + pad && y > Math.min(r[1], r[3]) - pad && y < Math.max(r[1], r[3]) + pad;

  /* ---------- a walk: the points, the speed, eased in and out over EASE_S ---------- */
  function o3Of(x) {
    if (!x || typeof x !== 'object') return null;
    const s = num(x.s);
    if (s == null) return null;
    const o = {s, m: ['walk', 'pad', 'idle', 'sit'].indexOf(x.m) >= 0 ? x.m : 'idle', v: clamp(20, 600, num(x.v) || WALK_V),
      x: num(x.x) || 0, y: num(x.y) || 0, h: num(x.h) || 0, vx: clamp(-600, 600, num(x.vx) || 0), vy: clamp(-600, 600, num(x.vy) || 0),
      to: typeof x.to === 'string' ? x.to.slice(0, 60) : '', lv: num(x.lv) || 0, p: [], cum: [0], len: 0};
    if (o.m === 'walk') {
      o.p = (Array.isArray(x.p) ? x.p : []).slice(0, MAX_PTS).map(q => (Array.isArray(q) && num(q[0]) != null && num(q[1]) != null ? {x: q[0], y: q[1]} : null)).filter(Boolean);
      for (let i = 1; i < o.p.length; i++) o.cum.push(o.cum[i - 1] + dist(o.p[i - 1], o.p[i]));
      o.len = o.cum[o.cum.length - 1];
      if (o.p.length < 2 || o.len < 1) { o.m = 'idle'; if (o.p.length) { o.x = o.p[o.p.length - 1].x; o.y = o.p[o.p.length - 1].y; } }
    }
    return o;
  }
  const easeOf = o => Math.min(EASE_S, o.len / o.v);
  const walkMs = o => (o.len / o.v + easeOf(o)) * 1000;
  function along(o, t) {
    const ta = easeOf(o), T = o.len / o.v + ta, v = o.v;
    if (t <= 0) return 0;
    if (t >= T) return o.len;
    if (t < ta) return v * t * t / (2 * ta);
    if (t > T - ta) return o.len - v * (T - t) * (T - t) / (2 * ta);
    return v * (t - ta / 2);
  }
  function pointAt(o, d) {
    let i = 1;
    while (i < o.p.length - 1 && o.cum[i] < d) i++;
    const a = o.p[i - 1], b = o.p[i], seg = (o.cum[i] - o.cum[i - 1]) || 1, k = clamp(0, 1, (d - o.cum[i - 1]) / seg);
    return {x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, h: hdg(b.x - a.x, b.y - a.y)};
  }
  function sayOf(x) {
    if (!x || typeof x !== 'object') return null;
    const t = plain(x.t, SAY_MAX), id = String(x.id || '').replace(/[^\w-]/g, '').slice(0, 24);
    return t && id ? {id, t} : null;
  }

  /* ---------- what this page hears: the founder's other tabs and devices ---------- */
  const far = new Map();            /* a trusted peer -> {o3, say, at, snap, sayAt, upd} */
  function trusted(p) {
    const c = live(), fu = c && c.founderUid;
    return !!(p && fu && p.by === fu && p.kind === 'viewer' && !p.guest && !p.sameTab);
  }
  function onPeers(ch) {
    const now = Date.now();
    const joined = new Set(((ch && ch.joined) || []).map(p => p && p.peer));
    const keep = new Set();
    for (const p of (ch && ch.peers) || []) {
      if (!trusted(p)) continue;
      const id = String(p.peer || 'peer');
      keep.add(id);
      const pr = p.presence || {}, was = far.get(id);
      const o3 = o3Of(pr.o3), say = sayOf(pr.say);
      /* the anchor is this page's own time for the change: a peer's updatedAt, never later than now */
      const at = Math.min(now, num(p.updatedAt) || now);
      const rec = {o3, say, upd: num(p.updatedAt) || now, at: was ? was.at : at, snap: !!(was && was.snap), sayAt: was ? was.sayAt : 0};
      if (o3 && (!was || !was.o3 || was.o3.s !== o3.s)) { rec.at = at; rec.snap = joined.has(p.peer); }
      if (say && (!was || !was.say || was.say.id !== say.id)) rec.sayAt = joined.has(p.peer) ? 0 : at;
      far.set(id, rec);
    }
    for (const id of Array.from(far.keys())) if (!keep.has(id)) far.delete(id);
    pick();
  }
  function join(room) {
    if (room === env.room) return;
    if (env.off) { try { env.off(); } catch (e) { /* gone */ } }
    env.room = room || null; env.off = null;
    far.clear();
    if (room && typeof room.onPeers === 'function') { try { env.off = room.onPeers(onPeers, () => {}); } catch (e) { env.off = null; } }
    pick();
    /* a room that came late, or a new one, hears that this page watches */
    o3wSent = null;
    watchSync();
  }

  /* ---------- this page, when it is his: the walk he is on, his words ---------- */
  const me = {s: 0, o3: null, at: 0, upd: 0, say: null, sayAt: 0, arrive: 0, idle: 0, sayT: 0, pad: null};
  const held = new Set();
  let roomless = false, drivers = 0, watchers = 0, o3wSent = null, arranging = false;
  function publish(patch) {
    const c = live(), r = c && c.room;
    if (!r || typeof r.presence !== 'function') { setRoomless(true); return; }
    let p;
    try { p = r.presence(patch); } catch (e) { setRoomless(true); return; }
    Promise.resolve(p).then(() => setRoomless(false), e => {
      /* too big: his words go first */
      if (e && e.code === 'invalid_argument' && patch.say) { me.say = null; pick(); publish({...patch, say: null}); return; }
      setRoomless(true);
    });
  }
  function setRoomless(v) { if (roomless !== v) { roomless = v; ping(); } }
  const maxSeen = () => Array.from(far.values()).reduce((m, r) => Math.max(m, r.o3 ? r.o3.s : 0), me.s);
  /* one presence call: the walk, the stop, the arrival, the seat */
  function setO3(wire) {
    if (!wire) { me.o3 = null; me.at = me.upd = Date.now(); publish({o3: null}); pick(); return; }
    me.s = maxSeen() + 1;
    const out = {...wire, s: me.s};
    me.o3 = o3Of(out); me.at = me.upd = Date.now();
    publish({o3: out});
    pick();
  }
  function touch() {
    clearTimeout(me.idle);
    me.idle = setTimeout(() => { if (me.o3) leave(); }, IDLE_MS);
  }
  /* off the floor: back at his cabin desk for everyone */
  function leave() {
    clearTimeout(me.arrive); me.arrive = 0;
    held.clear();
    if (me.pad) { clearTimeout(me.pad.trail); clearTimeout(me.pad.stop); if (me.pad.off) me.pad.off(); me.pad = null; }
    if (me.o3) setO3(null);
  }
  function drive(n) { drivers = Math.max(0, drivers + n); if (!drivers) leave(); }
  function watchSync() {
    const want = watchers > 0 && document.visibilityState !== 'hidden' ? 1 : null;
    if (want === o3wSent || !(live() && live().room)) return;
    o3wSent = want;
    publish({o3w: want});
  }
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') leave(); watchSync(); });

  /* ---------- the shown source: his newest walk among this page and his other tabs ---------- */
  let cur = {src: null, said: null};
  let desc = {live: false, mode: 'sit', seq: 0, say: null, to: ''};
  const subs = new Set();
  const ping = () => subs.forEach(f => { try { f(); } catch (e) { /* a view */ } });
  function pick() {
    /* a tab of his with nothing on the floor and nothing said leaves him at his desk */
    const all = Array.from(far.values()).filter(r => r.o3 || r.say);
    if (me.o3 || me.say) all.push({o3: me.o3, say: me.say, at: me.at, snap: false, sayAt: me.sayAt, upd: me.upd, local: true});
    const moving = all.filter(r => r.o3);
    const src = moving.length ? moving.reduce((a, r) => (r.o3.s > a.o3.s || (r.o3.s === a.o3.s && r.local) ? r : a))
      : all.length ? all.reduce((a, r) => (r.upd > a.upd ? r : a)) : null;
    const said = src && src.say ? src : all.filter(r => r.say).sort((a, b) => b.upd - a.upd)[0] || null;
    const now = Date.now(), was = drawn(now);
    cur = {src, said};
    reblend(was, now);
    const o = src && src.o3;
    const next = {live: !!src, mode: o ? o.m : 'sit', seq: o ? o.s : 0, say: said ? said.say : null, to: o ? o.to : ''};
    const sid = d => (d.say ? d.say.id : '');
    if (next.live !== desc.live || next.mode !== desc.mode || next.seq !== desc.seq || next.to !== desc.to || sid(next) !== sid(desc)) { desc = next; ping(); }
  }

  /* ---------- sample(now): where he is drawn ---------- */
  function goal(now) {
    const src = cur.src, o = src && src.o3;
    if (!o) { const c = seatOf(floor()); return {x: c.x, y: c.y, h: 0, mode: 'sit', d: 0}; }
    if (src.local && me.pad && o.m === 'pad') return {x: me.pad.x, y: me.pad.y, h: me.pad.h, mode: 'pad', d: me.pad.d};
    const t = Math.max(0, now - src.at);
    if (o.m === 'walk') {
      /* a late joiner, or a walk older than itself, is at its end */
      const d = src.snap ? o.len : along(o, t / 1000);
      const q = pointAt(o, d);
      return {x: q.x, y: q.y, h: q.h, mode: d >= o.len ? 'idle' : 'walk', d};
    }
    if (o.m === 'pad') {
      const k = Math.min(RECKON_MS, src.snap ? RECKON_MS : t) / 1000;
      return {x: o.x + o.vx * k, y: o.y + o.vy * k, h: o.vx || o.vy ? hdg(o.vx, o.vy) : o.h, mode: 'pad', d: Math.hypot(o.vx, o.vy) * k};
    }
    return {x: o.x, y: o.y, h: o.h, mode: o.m, d: 0};
  }
  /* a change is blended in from where he was drawn when it arrived: a critically damped spring (TAU), done within
     BLEND_MS. A seat on either side is a cut, never a glide */
  const K0 = (1 + BLEND_MS / TAU) * Math.exp(-BLEND_MS / TAU);
  const spring = ms => (ms >= BLEND_MS || ms < 0 ? 0 : ((1 + ms / TAU) * Math.exp(-ms / TAU) - K0) / (1 - K0));
  const blend = {s: -1, t0: 0, bx: 0, by: 0};
  function drawn(now) {
    const g = goal(now), k = spring(now - blend.t0);
    return {x: g.x + blend.bx * k, y: g.y + blend.by * k, h: g.h, mode: g.mode, d: g.d};
  }
  function reblend(was, now) {
    const o = cur.src && cur.src.o3, s = o ? o.s : -1;
    if (s === blend.s) return;
    const g = goal(now);
    const glide = was.mode !== 'sit' && g.mode !== 'sit' && dist(was, g) < 400;
    Object.assign(blend, {s, t0: now, bx: glide ? was.x - g.x : 0, by: glide ? was.y - g.y : 0});
  }
  function sample(now) {
    now = num(now) || Date.now();
    const p = drawn(now);
    const sd = cur.said;
    const talking = !!(sd && sd.say && sd.sayAt && now - sd.sayAt < Array.from(sd.say.t).length / CPS * 1000);
    return {x: p.x, y: p.y, h: p.h, mode: p.mode, walkPhase: (p.d / 110) % 1, talking};
  }

  /* ---------- the owner's acts: walk, say, clear ---------- */
  function walkTo(target) {
    const ctx = live();
    /* while he arranges the floor, a click on a desk or a station only opens it */
    if (!canDrive(ctx) || arranging) return false;
    const L = floor();
    if (!L) return false;
    let to, open = '';
    if (target && typeof target === 'object') { if (num(target.x) == null || num(target.y) == null) return false; to = 'floor'; }
    /* his own desk is the cabin seat: he sits, then it opens */
    else { to = open = String(target || ''); if (to === 'desk:' + ctx.founderUid) to = 'cabin'; }
    const end = standAt(L, to === 'floor' ? target : to);
    if (!end || num(end.x) == null || num(end.y) == null) return false;
    const here = sample(Date.now()), from = {x: Math.round(here.x), y: Math.round(here.y)};
    /* already there: the scene opens it at once */
    if (to !== 'floor' && to !== 'cabin' && dist(from, end) <= NEAR) return false;
    touch();
    padOff();
    clearTimeout(me.arrive);
    const pts = routeOf(L, from, end);
    const face = faceOf(L, to, end);
    const wire = {m: 'walk', p: pts.map(q => [q.x, q.y]), v: WALK_V, x: end.x, y: end.y, h: hdg(pts[1].x - pts[0].x, pts[1].y - pts[0].y), to, lv: planRev(ctx)};
    const o = o3Of({...wire, s: 0});
    if (o.m !== 'walk') { arrive(to, end, face, open); return true; }
    setO3(wire);
    me.arrive = setTimeout(() => arrive(to, end, face, open), walkMs(o));
    return true;
  }
  function arrive(to, end, face, open) {
    clearTimeout(me.arrive); me.arrive = 0;
    const ctx = live();
    if (!canDrive(ctx)) { leave(); return; }
    setO3({m: to === 'cabin' ? 'sit' : 'idle', x: end.x, y: end.y, h: face, to, lv: planRev(ctx)});
    /* the drawer is his alone, on this screen */
    const d = env.api && env.api.drawers;
    if (!d) return;
    try {
      if (open.indexOf('desk:') === 0) d.desk(open.slice(5));
      else if (open === 'coo') d.coo();
      else if (open && open !== 'cabin') d.station(open);
    } catch (e) { /* the scene has gone */ }
  }
  /* Escape: he stops where he is */
  function stop() {
    if (me.pad) { held.clear(); padStep(); return; }
    if (!me.o3 || me.o3.m !== 'walk') return;
    clearTimeout(me.arrive); me.arrive = 0;
    const s = sample(Date.now());
    setO3({m: 'idle', x: Math.round(s.x), y: Math.round(s.y), h: s.h, to: 'floor', lv: planRev(live())});
  }
  function say(text) {
    const ctx = live();
    if (!canDrive(ctx)) return false;
    const t = plain(text, SAY_MAX);
    if (!t) return false;
    const id = 's' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    me.say = {id, t}; me.sayAt = me.upd = Date.now();
    publish({say: me.say});
    pick();
    touch();
    /* typed out at 30 a second, held clamp(4 s, 60 ms a character, 12 s), a pill for 30 s, then gone */
    const n = Array.from(t).length;
    clearTimeout(me.sayT);
    me.sayT = setTimeout(() => { if (me.say && me.say.id === id) { me.say = null; me.upd = Date.now(); publish({say: null}); pick(); } }, n / CPS * 1000 + clamp(4000, 12000, 60 * n) + 30000);
    return true;
  }
  /* off the floor and quiet, in one presence call */
  function clear() {
    if (!canDrive(live())) return false;
    const had = !!(me.o3 || me.say);
    clearTimeout(me.sayT);
    me.say = null;
    const o3 = me.o3;
    me.o3 = null;
    leave();
    me.at = me.upd = Date.now();
    if (had) publish({o3: null, say: null});
    if (o3 || had) pick();
    return true;
  }

  /* ---------- pad mode: W A S D relative to the camera, against the furniture ---------- */
  function forward(api) {
    const c = api && api.camera, t = api && api.controls && api.controls.target;
    if (!c || !c.position || !t) return {x: 0, y: -1};
    const fx = t.x - c.position.x, fy = t.z - c.position.z, n = Math.hypot(fx, fy);
    return n > 1e-6 ? {x: fx / n, y: fy / n} : {x: 0, y: -1};
  }
  function blocked(p, x, y) {
    const L = env.L;
    if (!L || x < 20 || x > L.W - 20 || y < 165 || y > L.H - 15) return true;
    return p.rects.some(r => inRect(r, x, y, FOOT));
  }
  function padOn() {
    const api = env.api;
    if (!api || !canDrive(live())) return;
    floor();
    if (me.pad) { clearTimeout(me.pad.stop); me.pad.stop = 0; return; }
    clearTimeout(me.arrive); me.arrive = 0;
    const s = sample(Date.now());
    /* the furniture he already stands in (his chair at the desk) never holds him */
    const rects = collidersOf(api).filter(r => !inRect(r, s.x, s.y, FOOT));
    me.pad = {x: s.x, y: s.y, h: s.h, d: 0, vx: 0, vy: 0, t: Date.now(), rects, sent: null, trail: 0, stop: 0, off: null};
    me.pad.off = api.tick ? api.tick(padStep) : null;
    touch();
    padStep();
  }
  function padStep() {
    const p = me.pad;
    if (!p) return false;
    const now = Date.now(), dt = clamp(0, .1, (now - p.t) / 1000);
    p.t = now;
    let ux = 0, uy = 0;
    if (held.size) {
      const f = forward(env.api);
      const fw = (held.has('f') ? 1 : 0) - (held.has('b') ? 1 : 0), rt = (held.has('r') ? 1 : 0) - (held.has('l') ? 1 : 0);
      ux = f.x * fw - f.y * rt; uy = f.y * fw + f.x * rt;
      const n = Math.hypot(ux, uy);
      if (n) { ux /= n; uy /= n; }
    }
    let vx = ux * PAD_V, vy = uy * PAD_V;
    if (vx) { const nx = p.x + vx * dt; if (blocked(p, nx, p.y)) vx = 0; else p.x = nx; }
    if (vy) { const ny = p.y + vy * dt; if (blocked(p, p.x, ny)) vy = 0; else p.y = ny; }
    p.d += Math.hypot(vx, vy) * dt;
    if (vx || vy) p.h = hdg(vx, vy);
    p.vx = vx; p.vy = vy;
    if (!held.size) { padEnd(); return false; }
    padSend();
    return true;
  }
  function padSend() {
    const p = me.pad, now = Date.now(), was = p.sent;
    const sp = Math.hypot(p.vx, p.vy), wsp = was ? Math.hypot(was.vx, was.vy) : 0;
    const dv = was ? Math.hypot(p.vx - was.vx, p.vy - was.vy) / Math.max(1, wsp) : 1;
    const dh = was && sp && wsp ? Math.abs(((hdg(p.vx, p.vy) - hdg(was.vx, was.vy)) % 360 + 540) % 360 - 180) : 0;
    if (was && dv <= PAD_DV && dh <= PAD_DH && now - was.at < PAD_FRESH) return;
    const wait = was ? was.at + PAD_MS - now : 0;
    if (wait > 0) { if (!p.trail) p.trail = setTimeout(() => { if (me.pad === p) { p.trail = 0; padSend(); } }, wait); return; }
    clearTimeout(p.trail); p.trail = 0;
    p.sent = {vx: p.vx, vy: p.vy, at: now};
    setO3({m: 'pad', x: Math.round(p.x), y: Math.round(p.y), h: p.h, vx: Math.round(p.vx), vy: Math.round(p.vy), to: 'floor', lv: planRev(live())});
  }
  /* the keys are up: one final stop, inside the same four a second */
  function padEnd() {
    const p = me.pad;
    if (!p || p.stop) return;
    clearTimeout(p.trail); p.trail = 0;
    const go = () => {
      if (me.pad !== p) return;
      if (held.size) { p.stop = 0; return; }
      if (p.off) p.off();
      /* he stops on a whole centimetre, where the wire puts him */
      p.x = Math.round(p.x); p.y = Math.round(p.y);
      setO3({m: 'idle', x: p.x, y: p.y, h: p.h, to: 'floor', lv: planRev(live())});
      me.pad = null;
    };
    const wait = p.sent ? p.sent.at + PAD_MS - Date.now() : 0;
    if (wait > 0) p.stop = setTimeout(go, wait); else { p.stop = 1; go(); }
  }
  /* a click walk takes over from the keys at once */
  function padOff() {
    const p = me.pad;
    if (!p) return;
    clearTimeout(p.trail); clearTimeout(p.stop);
    if (p.off) p.off();
    held.clear();
    me.pad = null;
  }
  const KEYS = {w: 'f', arrowup: 'f', s: 'b', arrowdown: 'b', a: 'l', arrowleft: 'l', d: 'r', arrowright: 'r'};
  /* never while typing, and never with Ctrl, Alt or Meta held (the buddy's Ctrl Option, Cmd K) */
  const typing = el => !!(el && (el.isContentEditable || (el.closest && el.closest('input, textarea, select, [contenteditable]:not([contenteditable="false"])'))));

  /* ---------- the views' hooks ---------- */
  const subscribe = f => { subs.add(f); return () => { subs.delete(f); }; };
  const snapshot = () => desc;
  function useKaavish(ctx) {
    bind(ctx);
    const d = React.useSyncExternalStore(subscribe, snapshot, snapshot);
    const room = (ctx && ctx.room) || null;
    useEffect(() => { join(room); }, [room]);
    /* this page watches the office: o3w while it can be seen (the team site polls the stage for it) */
    useEffect(() => { watchers++; watchSync(); return () => { watchers--; watchSync(); }; }, []);
    return d;
  }
  /* the same descriptor for a word that says where he is (the desk list, a drawer): it hears the room and never
     says it watches, so it polls nothing on the team site */
  function useWhere(ctx) {
    bind(ctx);
    const d = React.useSyncExternalStore(subscribe, snapshot, snapshot);
    const room = (ctx && ctx.room) || null;
    useEffect(() => { join(room); }, [room]);
    return d;
  }
  function useController(api, data) {
    const ctx = data && data.ctx;
    if (ctx) bind(ctx);
    const on = !!(api && api.canvas && ctx && canDrive(ctx) && (api.mode === undefined || api.mode === 'page'));
    useEffect(() => {
      if (!on) return undefined;
      env.api = api;
      drive(1);
      const c = api.canvas;
      let down = null;
      const pd = e => { down = e.button === 0 && !arranging ? {x: e.clientX, y: e.clientY, t: Date.now(), id: e.pointerId} : null; };
      const pu = e => {
        const d = down;
        down = null;
        /* a press that moved under 6 px within 250 ms is a click; anything else turned the camera */
        if (!d || d.id !== e.pointerId || arranging || Math.hypot(e.clientX - d.x, e.clientY - d.y) >= 6 || Date.now() - d.t > 250) return;
        const pt = api.floorHit ? api.floorHit(e.clientX, e.clientY) : null;
        if (pt) walkTo({x: pt.x, y: pt.y});
      };
      const kd = e => {
        if (e.key === 'Control' || e.key === 'Alt' || e.key === 'Meta') { if (held.size) { held.clear(); padStep(); } return; }
        if (e.ctrlKey || e.altKey || e.metaKey || typing(e.target) || arranging) return;
        if (e.key === 'Escape') { stop(); return; }
        const k = KEYS[String(e.key || '').toLowerCase()];
        if (!k) return;
        e.preventDefault();
        held.add(k);
        padOn();
      };
      const ku = e => { const k = KEYS[String(e.key || '').toLowerCase()]; if (k && held.delete(k) && !held.size && me.pad) padStep(); };
      const blur = () => { if (held.size) { held.clear(); padStep(); } };
      c.addEventListener('pointerdown', pd);
      c.addEventListener('pointerup', pu);
      c.addEventListener('keydown', kd);
      c.addEventListener('keyup', ku);
      c.addEventListener('blur', blur);
      return () => {
        c.removeEventListener('pointerdown', pd); c.removeEventListener('pointerup', pu);
        c.removeEventListener('keydown', kd); c.removeEventListener('keyup', ku); c.removeEventListener('blur', blur);
        padOff();
        if (env.api === api) env.api = null;
        drive(-1);
      };
    }, [on, api]);
  }

  /* ---------- the composer: his words to the office ---------- */
  function Composer({data}) {
    const ctx = data && data.ctx;
    if (ctx) bind(ctx);
    const on = canDrive(ctx);
    const [text, setText] = useState('');
    React.useSyncExternalStore(subscribe, () => roomless, () => roomless);
    useEffect(() => { if (!on) return undefined; drive(1); return () => drive(-1); }, [on]);
    if (!on) return null;
    const send = () => { if (say(text)) setText(''); };
    const Mic = M.parts.MicButton;
    const heard = t => setText(x => (String(x).trim() ? String(x).trim() + ' ' : '') + t);
    return html`<div class="ol-composer" data-dock-avoid="" data-ai="say something to the office">
      <div class="row nowrap ol-row">
        <input id="office-say" class="input ol-in" maxlength=${SAY_MAX} value=${text} placeholder="Say something to the office" aria-label="Say something to the office"
          onInput=${e => setText(e.target.value)} onKeyDown=${e => { if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); send(); } }}/>
        ${Mic ? html`<${Mic} sm label="Say it" onText=${heard}/>` : null}
        <${UI.Btn} sm disabled=${!plain(text, SAY_MAX)} onClick=${send}>Say<//>
      </div>
      ${roomless || !(ctx && ctx.room) ? html`<p class="small ol-note" role="status">The team sees you at your desk right now. Live view comes back on its own.</p>` : null}
    </div>`;
  }

  /* ---------- office/plan: his layout, one write per change ---------- */
  const MAPS = ['slots', 'seats', 'props', 'labels'];
  const PROP_WORD = {plant: 'Plant', screen: 'Screen', sofa: 'Sofa', shelf: 'Shelf', lamp: 'Lamp'};
  const ADD = [['plant', 'Add a plant'], ['screen', 'Add a screen'], ['sofa', 'Add a sofa'], ['shelf', 'Add a shelf'], ['lamp', 'Add a lamp']];
  const ROOM = () => O().ROOM_LABEL || {};
  const labelKeys = () => Object.keys(O().STATION_LABEL || {}).concat(Object.keys(ROOM()));
  const onGrid = v => { const n = num(v); return n != null && Math.round(n) % GRID === 0 ? Math.round(n) : null; };
  function cleanMap(k, m) {
    const out = {};
    if (!m || typeof m !== 'object') return out;
    if (k === 'slots') {
      for (const s of Object.keys(m)) { const pod = plain(m[s], 60); if (/^\d{1,2}$/.test(s) && Number(s) < 40 && pod) out[String(Number(s))] = pod; }
    } else if (k === 'seats') {
      for (const u of Object.keys(m)) {
        const v = m[u];
        if (/^[\w.-]{1,64}$/.test(u) && Array.isArray(v) && v.length === 2 && Number.isInteger(v[0]) && Number.isInteger(v[1]) && v[0] >= 0 && v[0] < 40 && v[1] >= 0 && v[1] < 6) out[u] = [v[0], v[1]];
      }
    } else if (k === 'props') {
      for (const id of Object.keys(m).slice(0, PROPS_MAX)) {
        const p = m[id] || {}, x = onGrid(p.x), y = onGrid(p.y), r = [0, 90, 180, 270].indexOf(Number(p.r)) >= 0 ? Number(p.r) : 0;
        if (/^[\w-]{1,24}$/.test(id) && PROP_WORD[p.k] && x != null && y != null) out[id] = {k: p.k, x, y, r};
      }
    } else if (k === 'labels') {
      const ok = labelKeys();
      for (const key of Object.keys(m)) { const t = plain(m[key], LABEL_MAX); if (ok.indexOf(key) >= 0 && t) out[key] = t; }
    }
    return out;
  }
  /* null only when there is no plan yet: a read that fails stops the write, so a set() never replaces a plan it could not see */
  async function readPlan(ctx) {
    let s;
    try { s = await ctx.db.doc('office/plan').get(); } catch (e) { M.toast('That did not save. Try again in a moment.', true); throw e; }
    return s && s.exists ? U.dropNulls(s.data()) : null;
  }
  const undo = [];                  /* this session's writes, newest last: the maps as they were */
  /* patch is {slots?, seats?, props?, labels?}, each a whole map, or a function of the plan as it is now */
  async function planWrite(ctx, patch0, back) {
    if (!canDrive(ctx) || !canDrive(live()) || !patch0 || !ctx.W) return null;
    const cur0 = await readPlan(ctx);
    const patch = typeof patch0 === 'function' ? patch0(Object.fromEntries(MAPS.map(k => [k, cleanMap(k, cur0 && cur0[k])]))) : patch0;
    if (!patch || typeof patch !== 'object') return null;
    const rev = Math.max(0, Math.round(Number(cur0 && cur0.rev) || 0)) + 1;
    const out = {rev, at: Date.now(), by: ctx.uid}, before = {};
    for (const k of MAPS) {
      if (!(k in patch)) continue;
      const next = cleanMap(k, patch[k]);
      const was = cur0 && cur0[k] && typeof cur0[k] === 'object' ? cur0[k] : {};
      before[k] = was;
      /* the whole map; a key it no longer has is written as null, which every reader drops */
      if (cur0) for (const key of Object.keys(was)) if (!(key in next)) next[key] = null;
      out[k] = next;
    }
    if (cur0) await ctx.W.update('office/plan', out);
    else await ctx.W.set('office/plan', Object.assign({v: 1, slots: {}, seats: {}, props: {}, labels: {}}, out));
    if (!back) undo.push(before);
    return rev;
  }
  /* the plan as drawn (M.office.planOf); the doc read here only while the app's own copy has not arrived */
  const planOf = (ctx, doc) => {
    const drawn = O().planOf(ctx);
    if (drawn) return drawn;
    const raw = doc || null;
    if (!raw) return {rev: 0, slots: {}, seats: {}, props: {}, labels: {}};
    const p = U.dropNulls(raw);
    return {rev: Math.max(0, Math.round(Number(p.rev) || 0)), slots: cleanMap('slots', p.slots), seats: cleanMap('seats', p.seats), props: cleanMap('props', p.props), labels: cleanMap('labels', p.labels)};
  };

  /* ---------- Arrange: benches, seats, props and labels, by pointer and by keyboard ---------- */
  /* the benches as the office lays them out: their size, a desk's width, the seat order (column, top side) */
  const PLAN = () => O().PLAN;
  function modelOf(L, plan) {
    const benches = (L.benches || []).map((b, i) => ({slot: b.slot != null ? b.slot : i, x: b.x, y: b.y, pod: b.pod, ids: b.ids || []}));
    const spare = (L.spare || []).map((b, i) => ({slot: b.slot != null ? b.slot : benches.length + i, x: b.x, y: b.y, pod: '', ids: []}));
    const slots = benches.concat(spare).sort((a, b) => a.slot - b.slot);
    const seats = {};
    for (const u of Object.keys(L.seats || {})) {
      const s = L.seats[u];
      if (s.cabin || s.j == null) continue;
      seats[u] = {uid: u, x: s.x, y: s.y, slot: s.slot != null ? s.slot : s.bench, j: s.j, pod: s.pod};
    }
    return {slots, seats, props: (plan && plan.props) || {}, plan};
  }
  const benchHome = b => ({x: b.x + PLAN().BENCH_W / 2, y: b.y + PLAN().BENCH_H / 2, h: .8});
  function seatPlaces(model, pod) {
    const out = [], P = PLAN();
    for (const b of model.slots) {
      if (b.pod !== pod) continue;
      P.SEAT_ORDER.forEach(([col, top], j) => out.push({slot: b.slot, j, x: b.x + col * P.DESK_W + P.DESK_W / 2, y: top ? b.y - 8 : b.y + P.BENCH_H + 8}));
    }
    return out;
  }
  /* may a prop stand here: on the floor, off the walkways, clear of seats, stations, the door and the furniture */
  function spotOk(L, api, pt, model, own) {
    if (pt.x < 25 || pt.x > L.W - 25 || pt.y < 175 || pt.y > L.H - 25) return false;
    const A = aislesOf(L);
    if (A.hs.some(y => Math.abs(pt.y - y) < 60 && pt.x > A.left - 60 && pt.x < A.right + 60)) return false;
    if (A.vs.some(x => Math.abs(pt.x - x) < 60 && pt.y > A.top - 60 && pt.y < A.bottom + 60)) return false;
    if (Object.keys(L.seats || {}).some(u => dist(L.seats[u], pt) < 80)) return false;
    for (const k of Object.keys(O().STATION_POS || {})) { const s = standAt(L, k); if (s && dist(s, pt) < 80) return false; }
    const door = (O().SPOTS && O().SPOTS.door) || {x: 44, y: 862};
    if (dist({x: door.x, y: sy(L, door.y)}, pt) < 80) return false;
    const home = own ? model.props[own] : null;
    if (collidersOf(api).some(r => inRect(r, pt.x, pt.y, 0) && !(home && inRect(r, home.x, home.y, 0)))) return false;
    return !Object.keys(model.props).some(id => id !== own && dist(model.props[id], pt) < 50);
  }
  const snapPt = p => ({x: Math.round(p.x / GRID) * GRID, y: Math.round(p.y / GRID) * GRID});
  const WALKWAY = 'That spot is a walkway. Try a little to the side.';
  const SAVED = 'Saved. Everyone sees the new layout.';
  function useWide() {
    const get = () => { try { return window.matchMedia('(min-width: 701px)').matches; } catch (e) { return true; } };
    const [v, set] = useState(get);
    useEffect(() => { const f = () => set(get()); window.addEventListener('resize', f); return () => window.removeEventListener('resize', f); }, []);
    return v;
  }
  /* the camera to a near top-down view and back, through the scene's own orbit controls */
  function camTo(api, polar, done) {
    const c = api.controls, cam = api.camera;
    if (!c || !cam || !c.target || !api.tick) { if (done) done(); return null; }
    const t = c.target, ox = cam.position.x - t.x, oy = cam.position.y - t.y, oz = cam.position.z - t.z;
    const r = Math.hypot(ox, oy, oz) || 1, p0 = Math.acos(clamp(-1, 1, oy / r)), th = Math.atan2(ox, oz), t0 = Date.now();
    c.minPolarAngle = Math.min(c.minPolarAngle, polar); c.maxPolarAngle = Math.max(c.maxPolarAngle, polar);
    let off = null;
    off = api.tick(() => {
      const k = clamp(0, 1, (Date.now() - t0) / 600), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, ph = p0 + (polar - p0) * e;
      cam.position.set(t.x + r * Math.sin(ph) * Math.sin(th), t.y + r * Math.cos(ph), t.z + r * Math.sin(ph) * Math.cos(th));
      if (c.update) c.update();
      if (k >= 1) { if (off) off(); if (done) done(); }
      return k < 1;
    });
    return p0;
  }
  function Arrange({api, data}) {
    const ctx = data && data.ctx;
    const wide = useWide();
    const ok = !!(api && api.overlay && api.floorHit && ctx && canDrive(ctx) && !api.phone && (api.mode === undefined || api.mode === 'page') && wide);
    const [on, setOn] = useState(false);
    const [sel, setSel] = useState('');
    const [naming, setNaming] = useState(false);
    const [adding, setAdding] = useState(false);
    const [, bump] = useState(0);
    const doc = M.useDoc(ctx && ctx.db, ok && on && !(ctx && ctx.office) ? 'office/plan' : null);
    const L = layoutOf(live() || ctx) || env.L;
    const plan = useMemo(() => planOf(ctx, doc.data), [ctx && ctx.office && ctx.office.plan, doc.data]);
    const model = useMemo(() => (L ? modelOf(L, plan) : null), [L, plan]);
    const mv = useRef(null);        /* what is picked up: {kind, key, at, target, bad} */
    const els = useRef(new Map());
    const box = useRef({model, L, api, sel});
    box.current = {model, L, api, sel};
    const saved = useRef(null);
    const queue = useRef(Promise.resolve());

    /* one write at a time, each built from the plan as it stands when its turn comes. A bench or a seat is measured
       on the floor as drawn, so nothing is picked up again until the last write is in and drawn (wrote: its rev) */
    const pending = useRef(0), wrote = useRef(0);
    const write = (patch, back) => {
      pending.current++;
      const run = () => planWrite(M.lastCtx || ctx, patch, back).then(r => { if (r) { wrote.current = r; M.toast(SAVED); } return r; }, () => null);
      queue.current = queue.current.then(run, run).then(r => { pending.current--; bump(n => n + 1); return r; });
      return queue.current;
    };
    const busy = () => pending.current > 0 || (Number(plan.rev) || 0) < wrote.current;
    const slotsMap = m => { const out = {}; for (const b of m.slots) if (b.pod) out[b.slot] = b.pod; return out; };
    /* the plan's own seats, moved with their bench */
    function swapBenches(a, b) {
      const m = box.current.model;
      const slots = slotsMap(m), pa = slots[a], pb = slots[b];
      delete slots[a]; delete slots[b];
      if (pa) slots[b] = pa;
      if (pb) slots[a] = pb;
      return write(cur => {
        const seats = {};
        for (const [u, v] of Object.entries(cur.seats)) seats[u] = [v[0] === a ? b : v[0] === b ? a : v[0], v[1]];
        return {slots, seats};
      });
    }
    function swapSeats(uid, place) {
      const m = box.current.model, me0 = m.seats[uid];
      if (!me0 || (place.slot === me0.slot && place.j === me0.j)) return null;
      const other = Object.values(m.seats).find(s => s.uid !== uid && s.slot === place.slot && s.j === place.j);
      return write(cur => {
        const seats = {...cur.seats, [uid]: [place.slot, place.j]};
        if (other) seats[other.uid] = [me0.slot, me0.j];
        return {seats};
      });
    }
    /* p is the prop, null to remove it, or a function of the prop as it stands when the write's turn comes */
    function putProp(id, p) {
      return write(cur => {
        const props = {...cur.props};
        const next = typeof p === 'function' ? (props[id] ? p(props[id]) : null) : p;
        if (typeof p === 'function' && !next) return null;
        if (next) props[id] = next; else delete props[id];
        return {props};
      });
    }
    /* a new prop at the nearest free grid point to the middle of the view, ring by ring, among the props as they are */
    function addProp(k) {
      const {L: L1, api: a} = box.current;
      const c = a.canvas && a.canvas.getBoundingClientRect();
      const o = snapPt((c && c.width && a.floorHit(c.left + c.width / 2, c.top + c.height / 2)) || {x: L1.W / 2, y: L1.H / 2});
      const id = 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
      let none = false;
      write(cur => {
        if (Object.keys(cur.props).length >= PROPS_MAX) return null;
        for (let ring = 0; ring <= 24; ring++) {
          for (let dx = -ring; dx <= ring; dx++) {
            for (let dy = -ring; dy <= ring; dy++) {
              if (Math.max(Math.abs(dx), Math.abs(dy)) !== ring) continue;
              const pt = {x: o.x + dx * GRID, y: o.y + dy * GRID};
              if (spotOk(L1, a, pt, {props: cur.props}, '')) return {props: {...cur.props, [id]: {k, x: pt.x, y: pt.y, r: 0}}};
            }
          }
        }
        none = true;
        return null;
      }).then(r => { if (r) setSel(id); else if (none) M.toast(WALKWAY, true); });
    }

    /* the handles live in the scene's overlay, placed by it on every frame */
    const homeOf = key => {
      const m = box.current.model;
      if (!m) return null;
      const id = key.slice(2);
      if (key[0] === 'b') { const b = m.slots.find(x => String(x.slot) === id); return b ? benchHome(b) : null; }
      if (key[0] === 'u') { const s = m.seats[id]; return s ? {x: s.x, y: s.y, h: 1.25} : null; }
      const p = m.props[id];
      return p ? {x: p.x, y: p.y, h: .3} : null;
    };
    const anchor = key => () => { const x = mv.current; return x && x.key === key && x.at ? x.at : homeOf(key); };
    const mark = () => {
      const x = mv.current;
      for (const [key, el] of els.current) {
        el.classList.toggle('is-picked', !!x && x.key === key);
        el.classList.toggle('is-bad', !!x && x.key === key && !!x.bad);
        el.classList.toggle('is-target', !!x && !!x.target && x.target.key === key);
        el.classList.toggle('is-sel', key === 'p:' + box.current.sel);
      }
      if (api && api.invalidate) api.invalidate(1);
    };
    const nearestBench = pt => box.current.model.slots.reduce((best, b) => { const d = dist(benchHome(b), pt); return d < 260 && (!best || d < best.d) ? {b, d} : best; }, null);
    const nearestSeat = (uid, pt) => { const s = box.current.model.seats[uid]; return seatPlaces(box.current.model, s.pod).reduce((best, q) => { const d = dist(q, pt); return d < 120 && (!best || d < best.d) ? {q, d} : best; }, null); };
    function aim(x, pt) {
      const {L: L1, api: a, model: m} = box.current;
      if (x.kind === 'b') { const n = nearestBench(pt); x.target = n ? {key: 'b:' + n.b.slot, slot: n.b.slot} : null; x.at = {...pt, h: .8}; }
      else if (x.kind === 'u') {
        const n = nearestSeat(x.id, pt);
        const who = n ? Object.values(m.seats).find(s => s.slot === n.q.slot && s.j === n.q.j) : null;
        x.target = n ? {key: who ? 'u:' + who.uid : '', slot: n.q.slot, j: n.q.j} : null;
        x.at = {...pt, h: 1.25};
      } else { const q = snapPt(pt); x.bad = !spotOk(L1, a, q, m, x.id); x.target = {x: q.x, y: q.y}; x.at = {x: q.x, y: q.y, h: .3}; }
      mark();
    }
    function drop(x) {
      mv.current = null;
      mark();
      if (!x || !x.target) return;
      if (x.kind === 'b') { if (x.target.slot !== Number(x.id)) swapBenches(Number(x.id), x.target.slot); }
      else if (x.kind === 'u') swapSeats(x.id, x.target);
      else if (x.bad) M.toast(WALKWAY, true);
      else { const p = box.current.model.props[x.id], to = x.target; if (p && (p.x !== to.x || p.y !== to.y)) putProp(x.id, q => ({...q, x: to.x, y: to.y})); }
    }
    function pointer(e, key, el) {
      if (e.button !== 0) return;
      e.preventDefault(); e.stopPropagation();
      if (busy()) return;
      const x = {kind: key[0], key, id: key.slice(2), at: null, target: null, moved: false, sx: e.clientX, sy: e.clientY};
      try { el.setPointerCapture(e.pointerId); } catch (err) { /* no capture */ }
      const move = ev => {
        if (x.done) return;
        if (!x.moved && Math.hypot(ev.clientX - x.sx, ev.clientY - x.sy) < 4) return;
        x.moved = true; mv.current = x;
        const pt = box.current.api.floorHit(ev.clientX, ev.clientY);
        if (pt) aim(x, pt);
      };
      /* a drop is the release of a drag still in hand: a cancelled pointer, or Escape mid drag, writes nothing */
      const esc = ev => { if (ev.key === 'Escape' && mv.current === x) { ev.preventDefault(); ev.stopPropagation(); mv.current = null; mark(); } };
      const up = ev => {
        el.removeEventListener('pointermove', move); el.removeEventListener('pointerup', up); el.removeEventListener('pointercancel', up);
        window.removeEventListener('keydown', esc, true);
        const held0 = mv.current === x;
        x.done = true;
        if (ev.type === 'pointercancel') { if (held0) { mv.current = null; mark(); } return; }
        if (x.moved) { if (held0) drop(x); }
        else if (x.kind === 'p') { setSel(x.id); box.current.sel = x.id; mark(); }
      };
      el.addEventListener('pointermove', move); el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
      window.addEventListener('keydown', esc, true);
    }
    /* keyboard: Enter picks, the arrows move between neighbours (props by 25 cm), Enter drops, Escape puts it back */
    function keys(e, key) {
      const x = mv.current, m = box.current.model;
      if (e.key === 'Escape') { if (x) { e.preventDefault(); e.stopPropagation(); mv.current = null; mark(); } return; }
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (x && x.key === key) { drop(x); return; }
        if (busy()) return;
        const h = homeOf(key);
        mv.current = {kind: key[0], key, id: key.slice(2), at: h, target: key[0] === 'p' ? {x: h.x, y: h.y} : key[0] === 'b' ? {key, slot: Number(key.slice(2))} : null, kb: true};
        if (key[0] === 'u') { const s = m.seats[key.slice(2)]; mv.current.target = {key, slot: s.slot, j: s.j}; }
        if (key[0] === 'p') { setSel(key.slice(2)); box.current.sel = key.slice(2); }
        mark();
        return;
      }
      const dir = {ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1]}[e.key];
      if (!dir || !x || x.key !== key) return;
      e.preventDefault();
      if (x.kind === 'b') {
        const now = x.target ? x.target.slot : Number(x.id);
        const want = dir[0] ? (now % 2 === 0 ? now + 1 : now - 1) : now + dir[1] * 2;
        const b = m.slots.find(s => s.slot === want);
        if (b) aim(x, benchHome(b));
      } else if (x.kind === 'u') {
        const s = m.seats[x.id], list = seatPlaces(m, s.pod);
        const i = Math.max(0, list.findIndex(q => x.target && q.slot === x.target.slot && q.j === x.target.j));
        const q = list[(i + (dir[0] || dir[1]) + list.length) % list.length];
        if (q) aim(x, q);
      } else aim(x, {x: x.target.x + dir[0] * GRID, y: x.target.y + dir[1] * GRID});
    }
    const handleKey = useRef({pointer, keys});
    handleKey.current = {pointer, keys};

    const items = !(ok && on && model) ? [] : [].concat(
      model.slots.map(b => ({key: 'b:' + b.slot, cls: 'o3-bench', text: b.pod || '', label: b.pod ? b.pod + ' bench' : 'An empty bench', attr: ['data-slot', String(b.slot)]})),
      Object.values(model.seats).map(s => { const nm = String(((data.profs || {})[s.uid] || {}).name || ''); return {key: 'u:' + s.uid, cls: 'o3-seat', text: nm ? nm.charAt(0).toUpperCase() : '', label: (nm || 'Someone') + ', seat', attr: ['data-uid', s.uid]}; }),
      Object.keys(model.props).map(id => ({key: 'p:' + id, cls: 'o3-prop', text: PROP_WORD[model.props[id].k], label: PROP_WORD[model.props[id].k] + (model.props[id].r ? ', turned ' + model.props[id].r + ' degrees' : ''), attr: ['data-id', id]})));
    const sig = items.map(i => i.key + '|' + i.text + '|' + i.label).join(',');
    useEffect(() => {
      const map = els.current, want = new Set(items.map(i => i.key));
      for (const [key, el] of map) if (!want.has(key)) { try { api.overlay.remove(el); } catch (e) { el.remove(); } map.delete(key); }
      for (const it of items) {
        let el = map.get(it.key);
        if (!el) {
          el = document.createElement('button');
          el.type = 'button';
          el.className = 'o3-handle ' + it.cls;
          el.setAttribute(it.attr[0], it.attr[1]);
          el.addEventListener('pointerdown', e => handleKey.current.pointer(e, it.key, el));
          el.addEventListener('keydown', e => handleKey.current.keys(e, it.key));
          map.set(it.key, el);
          el.textContent = it.text;
          el.setAttribute('aria-label', it.label);
          api.overlay.add(el, anchor(it.key), it.cls === 'o3-bench' ? 40 : 60);
        } else { el.textContent = it.text; el.setAttribute('aria-label', it.label); }
      }
      mark();
    }, [sig, ok, on, api]);
    /* gone with the mode or the scene */
    useEffect(() => () => { for (const el of els.current.values()) { try { api.overlay.remove(el); } catch (e) { el.remove(); } } els.current.clear(); }, [api]);
    useEffect(() => { mark(); }, [sel]);

    const enter = () => {
      setOn(true); arranging = true; setSel(''); setNaming(false);
      const c = api.controls;
      if (c) saved.current = {min: c.minPolarAngle, max: c.maxPolarAngle, rot: c.enableRotate, polar: null};
      /* each drop rebuilds the floor: the top-down view stays while he arranges */
      if (api.hold) api.hold();
      const p0 = camTo(api, 20 / DEG, () => { if (c) { c.enableRotate = false; } });
      if (saved.current) saved.current.polar = p0;
    };
    const done = () => {
      setOn(false); arranging = false; mv.current = null; setNaming(false); setAdding(false);
      const c = api.controls, s = saved.current;
      if (c && s) { c.enableRotate = s.rot !== false; if (s.polar != null) camTo(api, s.polar, () => { c.minPolarAngle = s.min; c.maxPolarAngle = s.max; }); else { c.minPolarAngle = s.min; c.maxPolarAngle = s.max; } }
      saved.current = null;
    };
    useEffect(() => () => { arranging = false; }, []);
    useEffect(() => { if (!ok && on) done(); }, [ok]);
    if (!ok) return null;
    if (!on) return html`<div class="o3-arrange"><button type="button" class="btn sec sm o3-arr-go" data-ai="arrange the office" onClick=${enter}>Arrange</button></div>`;
    const prop = sel && model && model.props[sel];
    const full = model && Object.keys(model.props).length >= PROPS_MAX;
    const back = () => { const b = undo.pop(); if (b) write(b, true); };
    const add = k => { setAdding(false); addProp(k); };
    return html`<div class="o3-arrange on">
      <div class="o3-arr-bar" role="toolbar" aria-label="Arrange the office">
        <span class="o3-add">
          <button type="button" class=${'chip o3-add-go' + (adding ? ' on' : '')} aria-label="Add" aria-haspopup="menu" aria-expanded=${adding} disabled=${full}
            onClick=${() => setAdding(v => !v)}><${M.icons.plus}/></button>
          ${adding ? html`<div class="o3-add-menu" role="menu" onKeyDown=${e => { if (e.key === 'Escape') { e.stopPropagation(); setAdding(false); } }}>
            ${ADD.map(([k, label]) => html`<button key=${k} type="button" role="menuitem" class="o3-add-item" onClick=${() => add(k)}>${label}</button>`)}
          </div>` : null}
        </span>
        ${prop ? html`<button type="button" class="chip" onClick=${() => putProp(sel, q => ({...q, r: (q.r + 90) % 360}))}>Turn</button>
          <button type="button" class="chip" onClick=${() => { const id = sel; setSel(''); putProp(id, null); }}>Remove</button>` : null}
        <button type="button" class=${'chip' + (naming ? ' on' : '')} aria-pressed=${naming} onClick=${() => setNaming(v => !v)}>Rename</button>
        <button type="button" class="chip" disabled=${!undo.length} onClick=${back}>Put back</button>
        <button type="button" class="btn sm o3-arr-done" onClick=${done}>Done</button>
      </div>
      ${naming ? html`<${Names} ctx=${ctx} plan=${plan} onSave=${edit => write(cur => ({labels: edit(cur.labels)}))}/>` : null}
    </div>
    <p class="tiny o3-arr-hint">Drag a bench to another slot to swap it. Drag a person to another seat in their pod. Everyone sees the layout when you drop.</p>`;
  }
  /* the rooms and stations by their names: Enter saves one */
  function Names({ctx, plan, onSave}) {
    const keys = O().shownStations(ctx, 'owner').concat(Object.keys(ROOM()));
    const def = k => O().STATION_LABEL[k] || ROOM()[k] || k;
    const word = k => (plan.labels && plan.labels[k]) || def(k);
    const save = (k, v) => {
      const t = plain(v, LABEL_MAX);
      onSave(was => { const labels = {...was}; if (!t || t === def(k)) delete labels[k]; else labels[k] = t; return labels; });
    };
    return html`<div class="o3-names">${keys.map(k => html`<label key=${k} class="o3-name">
      <span class="tiny ink62">${def(k)}</span>
      <input class="input" maxlength=${LABEL_MAX} defaultValue=${word(k)} data-key=${k} aria-label=${'Rename ' + def(k)}
        onKeyDown=${e => { if (e.key === 'Enter') { e.preventDefault(); save(k, e.target.value); } }}/>
    </label>`)}</div>`;
  }

  /* ---------- for the tests and the buddy's eyes: what this page believes ---------- */
  function state() {
    const s = sample(Date.now());
    const ctx = live();
    return {role: !ctx ? 'none' : canDrive(ctx) ? 'owner' : 'member', seq: desc.seq, mode: s.mode, x: Math.round(s.x), y: Math.round(s.y), h: s.h,
      say: desc.say ? desc.say.t : '', live: desc.live, to: desc.to, talking: s.talking, peers: far.size, watching: watchers, roomless};
  }

  M.officeLive = {canDrive, useKaavish, useWhere, sample, useController, walkTo, say, clear, Composer, Arrange, planWrite, state};
})();
