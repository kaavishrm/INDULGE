/* office: Kaavish's live stage on the team site (v35). The 3D office shows his walk and his words to the
   whole team within about a second. On claude.ai that rides the room's presence; here it is one blob, never
   a document: no version, no log line, no marker, never in a sync, a backup or the history.

     x/stage    {o3, say, live, by, at, seq}    the owner's walk, pose and bubble, cleaned and bounded

     {a: 'stage', since: <seq>}   anyone on the team: {seq, now, same: 1} when nothing moved, else {seq, now, st}
     {a: 'stage', put: {...}}     the owner alone: {o3, say} or {live: false} when his tab goes away

   o3 is {s, m, p, v, x, y, h, vx, vy, to, lv} in plan centimetres (plan x and y, the floor's own axes). A
   level and the owner are read at most every LEVEL_MS per instance, so a warm poll costs two reads (the
   session and the stage) and a put one read and one write. */
const LEVEL_MS = 15000;
const MAX_PTS = 16, MAX_SAY = 280, SPAN = 100000;   /* centimetres either way from the origin */
const MODES = ['walk', 'pad', 'idle', 'sit'];
const int = (x, lo, hi) => { const n = Math.round(Number(x)); return Number.isFinite(n) ? Math.max(lo, Math.min(hi, n)) : 0; };
/* his words as plain text, as the page's room wants them: a control character or a line break is a space, and a
   format or private use character (a soft hyphen, a direction mark, a zero width space) is dropped. A zero width
   joiner or non joiner stays only between two characters, once, as emoji and Indic scripts need it, and the text
   is cut by characters, never inside one */
const SPACE = /[\s\p{Cc}\p{Zl}\p{Zp}]/u, HIDDEN = /[\p{Cf}\p{Co}]/u;
const FILLER = [4447, 4448, 12644, 65440];      /* the Hangul fillers draw nothing */
const JOINER = [8204, 8205];
const gone = ch => HIDDEN.test(ch) || FILLER.includes(ch.codePointAt(0));
const blank = ch => !ch || SPACE.test(ch) || gone(ch);
function clean(s) {
  const cs = Array.from(String(s || '').slice(0, MAX_SAY * 8)), out = [];
  cs.forEach((ch, i) => {
    if (JOINER.includes(ch.codePointAt(0))) { if (!blank(out[out.length - 1]) && !blank(cs[i + 1])) out.push(ch); return; }
    if (!gone(ch)) out.push(SPACE.test(ch) ? ' ' : ch);
  });
  const cut = Array.from(out.join('').replace(/\s+/g, ' ').trim()).slice(0, MAX_SAY);
  while (cut.length && JOINER.includes(cut[cut.length - 1].codePointAt(0))) cut.pop();
  return cut.join('').trim();
}

export function officeActions({getJ, putJ, levelOf, ownerUid, LEVEL, HttpError}) {
  const levels = new Map();
  async function level(uid) {
    const hit = levels.get(uid), now = Date.now();
    if (hit && now - hit.at < LEVEL_MS) return hit.level;
    const l = await levelOf(uid);
    levels.set(uid, {level: l, at: now});
    return l;
  }
  let owner = null, ownerAt = 0;
  async function isOwner(uid) {
    if (!owner || Date.now() - ownerAt > LEVEL_MS) { owner = await ownerUid(); ownerAt = Date.now(); }
    return !!uid && uid === owner;
  }
  /* what a put may hold: every number bounded, every string a known word or plain text */
  function shape(p) {
    const o3 = p && p.o3 && typeof p.o3 === 'object' ? p.o3 : null;
    const walk = o3 ? {
      s: int(o3.s, 0, 2 ** 31), m: MODES.includes(o3.m) ? o3.m : 'idle',
      p: (Array.isArray(o3.p) ? o3.p : []).slice(0, MAX_PTS).map(q => [int(q && q[0], -SPAN, SPAN), int(q && q[1], -SPAN, SPAN)]),
      x: int(o3.x, -SPAN, SPAN), y: int(o3.y, -SPAN, SPAN), h: int(o3.h, -360, 360), v: int(o3.v, 0, 600),
      vx: int(o3.vx, -600, 600), vy: int(o3.vy, -600, 600), lv: int(o3.lv, 0, 2 ** 31),
      to: /^[a-z]{1,12}(:[\w.-]{1,40})?$/.test(String(o3.to || '')) ? o3.to : ''
    } : null;
    const say = p && p.say && typeof p.say === 'object' ? {id: String(p.say.id || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 24), t: clean(p.say.t)} : null;
    return {o3: walk, say: say && say.t ? say : null, live: !(p && p.live === false)};
  }
  /* two puts in one millisecond still read as two changes to a poller */
  let lastSeq = 0;
  return {
    async stage(v, body) {
      if (!v) throw new HttpError(401, 'noid');
      if (body && body.put) {
        if (!(await isOwner(v.uid))) throw new HttpError(403, 'not_permitted', 'Only Kaavish moves in the office.');
        const now = Date.now();
        lastSeq = Math.max(now, lastSeq + 1);
        const st = {...shape(body.put), by: v.uid, at: now, seq: lastSeq};
        await putJ('x/stage', st);
        return {seq: st.seq, now};
      }
      if ((await level(v.uid)) < LEVEL.interact) throw new HttpError(403, 'not_permitted');
      const st = await getJ('x/stage');
      const now = Date.now();
      if (!st) return {seq: 0, now, same: 1};
      if (Number(body && body.since) === st.seq) return {seq: st.seq, now, same: 1};
      return {seq: st.seq, now, st};
    }
  };
}
