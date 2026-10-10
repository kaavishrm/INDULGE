/* module: cast. The people of the office: what a character is made of, how a look is checked, which look a
   person shows, the colours it is drawn in, and the 2D head drawn from the same parts for every avatar chip,
   the editor's tiles and the 3D office's screens.

     me/<uid>.look   the person's own look {v, skin, face, eyes, brows, nose, mouth, hair, hairColor, facial,
                     glasses, frame, head, headColor, top, topColor, bottom, bottomColor, shoes, shoeColor, ears,
                     bindi, stud, watch, pose, pic, by?, at}. They write it; Kaavish may write it too, with by.
     office/cast     Kaavish's doc {v, at, locks: {uid: {look, at}}}: a locked look shows whatever the person saves.

   A look holds ids only. clean() maps every unknown value to the default and drops unknown keys, so nothing a
   person typed ever reaches a drawing, and a look from a newer page still draws. Flame is never a choice: the
   only flame on a human is Kaavish's one detail, added by paint() for the founder alone. Nothing is ever
   guessed from a photo, a name or pronouns. */
'use strict';
(function () {
  /* ---------- colours ----------
     The house anchors are the allowed hexes; cloth, shades, lips and metal are mixed from them. Skin, hair,
     frames, oak, walnut and the bindi are real colours the house palette cannot mix, so they live once, here,
     in the natural palette: warm hues only (never green, blue or yellow), used for characters and desk tops. */
  const HOUSE_HEX = {flame: '#F53901', deep: '#A82800', ink: '#0E0E0E', col: '#EFEDE7', white: '#FFFFFF', inkDark: '#F2F1EC'};
  /* natural palette: start */
  const NATURAL = {
    skin: {s1: '#F6DDCB', s2: '#EDCAAE', s3: '#E0B28E', s4: '#D09A70', s5: '#BA7F55', s6: '#9C6640', s7: '#7A4D30', s8: '#573523', clay: '#E7E1D6'},
    hair: {black: '#1F1B19', espresso: '#3A2920', brown: '#5C3F2B', chestnut: '#7A4A2C', auburn: '#84391F', sand: '#B29C80', grey: '#8D8A86', silver: '#D5D2CC'},
    frame: {ink: '#161616', tortoise: '#6A4832', clear: '#E4E0D8', metal: '#A7A7A5'},
    oak: '#D9C7AB',
    walnut: '#5C4232',
    bindi: '#7A2230'
  };
  /* natural palette: end */
  const rgbOf = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const HOUSE = {};
  for (const k of Object.keys(HOUSE_HEX)) HOUSE[k] = rgbOf(HOUSE_HEX[k]);
  /* mix(a, b, t): sRGB bytes, as color-mix(in srgb) and the canvas readback give them */
  const mix = (a, b, t) => [0, 1, 2].map(i => Math.round(a[i] + (b[i] - a[i]) * t));
  /* blend([[colour, weight], ...]): a weighted mix of several */
  const blend = parts => {
    let tot = 0;
    const out = [0, 0, 0];
    for (const [c, w] of parts) { tot += w; for (let i = 0; i < 3; i++) out[i] += c[i] * w; }
    return out.map(v => Math.round(v / tot));
  };
  const H = HOUSE;
  const COCOA = blend([[H.deep, 19], [H.ink, 59], [H.col, 22]]);
  /* the neutral cloth: mixes of the house hexes. Camel is col into cocoa, dark enough (L* about 52) and grey
     enough that it never reads as bare skin beside s2 and s3 */
  const CLOTH_RGB = {
    ink: blend([[H.ink, 94], [H.col, 6]]),
    graphite: blend([[H.ink, 80], [H.col, 20]]),
    ash: blend([[H.ink, 57], [H.col, 43]]),
    stone: blend([[H.ink, 26], [H.col, 66], [H.deep, 8]]),
    oat: blend([[H.deep, 6], [H.ink, 6], [H.col, 88]]),
    chalk: blend([[H.col, 70], [H.white, 30]]),
    camel: mix(H.col, COCOA, 0.68),
    cocoa: COCOA
  };
  const list = (o, f) => Object.keys(o).map(id => ({id, c: f ? f(o[id]) : o[id]}));
  const SKIN = list(NATURAL.skin, rgbOf);
  const HAIR = list(NATURAL.hair, rgbOf);
  const FRAMES = list(NATURAL.frame, rgbOf);
  const CLOTH = list(CLOTH_RGB);
  const WOOD = {oak: rgbOf(NATURAL.oak), walnut: rgbOf(NATURAL.walnut)};
  const BINDI = rgbOf(NATURAL.bindi);
  const METAL = mix(H.col, H.ink, 0.25);
  const LENS = mix(H.ink, H.col, 0.05);

  /* ---------- the parts ---------- */
  const SHAPES = {
    face: ['round', 'oval', 'long', 'soft', 'heart'],
    eyes: ['bead', 'almond', 'sleepy', 'lashes'],
    brows: ['natural', 'fine', 'bold', 'arched', 'none'],
    nose: ['button', 'soft', 'long'],
    mouth: ['smile', 'grin', 'calm'],
    hair: ['none', 'buzz', 'crop', 'side', 'quiff', 'curls', 'coils', 'waves', 'bob', 'long', 'bun', 'ponytail', 'braid'],
    facial: ['none', 'stubble', 'moustache', 'short', 'full', 'goatee'],
    glasses: ['none', 'round', 'square', 'soft', 'shades'],
    head: ['none', 'cap', 'beanie', 'bucket', 'scarf', 'turban'],
    top: ['tee', 'crew', 'hoodie', 'shirt', 'blazer', 'kurta', 'dress'],
    bottom: ['trousers', 'shorts', 'skirt'],
    shoes: ['sneakers', 'loafers', 'boots'],
    ears: ['none', 'studs', 'hoops'],
    pose: ['easy', 'pockets', 'folded', 'mug'],
    pic: ['auto', 'photo', 'char']
  };
  const COLOURS = {skin: SKIN, hairColor: HAIR, frame: FRAMES, headColor: CLOTH, topColor: CLOTH, bottomColor: CLOTH, shoeColor: CLOTH};
  const FLAGS = ['bindi', 'stud', 'watch'];
  /* the order a look is read in for its hash: a new part is appended here, so old hashes stay put */
  const ORDER = ['skin', 'face', 'eyes', 'brows', 'nose', 'mouth', 'hair', 'hairColor', 'facial', 'glasses', 'frame', 'head', 'headColor',
    'top', 'topColor', 'bottom', 'bottomColor', 'shoes', 'shoeColor', 'ears', 'bindi', 'stud', 'watch', 'pose'];
  const DEFAULT = Object.freeze({v: 1, skin: 's4', face: 'oval', eyes: 'bead', brows: 'natural', nose: 'button', mouth: 'smile', hair: 'crop', hairColor: 'black',
    facial: 'none', glasses: 'none', frame: 'ink', head: 'none', headColor: 'ink', top: 'tee', topColor: 'chalk', bottom: 'trousers',
    bottomColor: 'graphite', shoes: 'sneakers', shoeColor: 'chalk', ears: 'none', bindi: false, stud: false, watch: false, pose: 'easy', pic: 'auto'});

  const byId = (arr, id) => (typeof id === 'string' && arr.find(x => x.id === id)) || null;
  const colourOf = (arr, id, d) => (byId(arr, id) || byId(arr, d) || arr[0]).c;

  /* clean(raw): a look made only of known parts. Every unknown value becomes the default, every unknown key
     goes; by is kept only as an id, at only as a number. No string from the doc survives except a table id */
  function clean(raw) {
    const src = raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {};
    const r = k => Object.prototype.hasOwnProperty.call(src, k) ? src[k] : undefined;
    const out = {v: 1};
    for (const k of Object.keys(SHAPES)) out[k] = SHAPES[k].indexOf(r(k)) >= 0 ? r(k) : DEFAULT[k];
    for (const k of Object.keys(COLOURS)) out[k] = byId(COLOURS[k], r(k)) ? r(k) : DEFAULT[k];
    for (const k of FLAGS) out[k] = r(k) === true;
    const by = r('by'), at = r('at');
    if (typeof by === 'string' && /^[\w~.-]{1,64}$/.test(by)) out.by = by;
    if (typeof at === 'number' && Number.isFinite(at)) out.at = Math.floor(at);
    return out;
  }
  /* FNV-1a over a string, the multiplier and offset written in decimal */
  const fnv = s => {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h;
  };
  /* hash(look, extra): FNV-1a over the parts in ORDER, base 36. The cache key of a head, a figure and a crowd.
     Key order, at, by and pic never move it */
  function hash(look, extra) {
    const l = clean(look);
    return fnv(ORDER.map(k => String(l[k])).join('|') + (extra ? '|' + extra : '')).toString(36);
  }
  const same = (a, b) => hash(a) === hash(b);

  /* initials for the starter's name sticker: the first letter of the first two words, letters only */
  function initials(n) {
    const words = String(n || '').trim().split(/\s+/).slice(0, 2);
    let out = '';
    for (const w of words) { const m = /\p{L}/u.exec(w); if (m) out += m[0]; }
    return out.toUpperCase().slice(0, 2);
  }
  /* the text a sticker may carry: letters only, at most two, so nothing else ever reaches a drawing */
  const sticker = s => Array.from(String(s || '')).filter(ch => /\p{L}/u.test(ch)).join('').toUpperCase().slice(0, 2);

  /* ---------- the starter: clay until the person styles it ----------
     Only what the roster says is used: the pod picks the tee (pod mates match), the name gives the initials on
     the chest sticker, and Kaavish gets an ink blazer with his flame pocket square. Skin, hair and face are
     never guessed. */
  const POD_TONES = ['oat', 'stone', 'ash', 'camel', 'chalk', 'cocoa', 'graphite'];
  function starter(o) {
    const opts = o || {};
    const pod = String(opts.pod || '').trim().toLowerCase() || 'studio';
    return {...clean({}), skin: 'clay', hair: 'none', brows: 'none', mouth: 'calm', facial: 'none',
      top: opts.founder ? 'blazer' : 'tee', topColor: opts.founder ? 'ink' : POD_TONES[fnv(pod) % POD_TONES.length],
      bottomColor: 'graphite', shoeColor: 'chalk', starter: true, initials: initials(opts.name)};
  }

  /* ---------- which look a person shows ----------
     resolve({uid, me, cast, founderUid, member, name}) -> {look, src, locked, pending, founder, by, pic}
       1. 'lock'     Kaavish's lock (office/cast.locks[uid]); never for Kaavish himself
       2. 'own'      the person's own look
       3. 'starter'  nothing saved yet: clay, with initials
     pic always comes from the person's own look, never from a lock. A look that is not a plain object (a list,
     a string) counts as no look at all, so it never draws the default parts as if someone had chosen them */
  const isLook = x => !!x && typeof x === 'object' && !Array.isArray(x);
  function resolve(o) {
    const opts = o || {};
    const uid = opts.uid, me = opts.me || {}, cast = opts.cast || {};
    const founder = !!uid && !!opts.founderUid && uid === opts.founderUid;
    const own = isLook(me.look) ? clean(me.look) : null;
    const pic = own ? own.pic : 'auto';
    const locks = isLook(cast.locks) ? cast.locks : {};
    const lk = !founder && uid && isLook(locks[uid]) && isLook(locks[uid].look) ? clean(locks[uid].look) : null;
    if (lk) return {look: {...lk, pic}, src: 'lock', locked: true, pending: !!own && !same(own, lk), founder, by: lk.by || null, pic};
    if (own) return {look: own, src: 'own', locked: false, pending: false, founder, by: own.by || null, pic};
    return {look: starter({pod: opts.member && opts.member.pod, name: opts.name, founder}), src: 'starter', locked: false, pending: false, founder, by: null, pic};
  }
  /* the same, read from the app context. name (optional) only gives the starter its initials */
  function resolveFor(ctx, uid, name) {
    if (!ctx || !uid) return resolve({});
    const meMap = (ctx.coll && ctx.coll.me && ctx.coll.me.map) || {};
    const cast = (ctx.office && ctx.office.cast) || null;
    return resolve({uid, me: meMap[uid] || {}, cast, founderUid: ctx.founderUid, member: (ctx.members || {})[uid], name});
  }
  const lookOf = (ctx, uid, name) => resolveFor(ctx, uid, name).look;

  /* paint(look, founder): the colours a look is drawn in, sRGB byte triples. accent is the founder's flame */
  function paint(look, founder) {
    const l = clean(look);
    const skin = colourOf(SKIN, l.skin, 's4');
    const hair = colourOf(HAIR, l.hairColor, 'black');
    const top = colourOf(CLOTH, l.topColor, 'chalk');
    const headwear = colourOf(CLOTH, l.headColor, 'ink');
    return {
      skin, skinShade: mix(skin, mix(H.deep, H.ink, 0.6), 0.16), skinLight: mix(skin, H.white, 0.18),
      hair, hairShade: mix(hair, H.ink, 0.25),
      brow: l.hairColor === 'silver' || l.hairColor === 'grey' ? mix(hair, H.ink, 0.4) : hair,
      beard: mix(hair, skin, 0.12),
      top, topDark: mix(top, H.ink, 0.18), topLight: mix(top, H.white, 0.18),
      bottom: colourOf(CLOTH, l.bottomColor, 'graphite'), shoe: colourOf(CLOTH, l.shoeColor, 'chalk'),
      sole: mix(colourOf(CLOTH, l.shoeColor, 'chalk'), H.ink, 0.12),
      headwear, headwearDark: mix(headwear, H.ink, 0.18), headwearLight: mix(headwear, H.white, 0.08),
      frame: colourOf(FRAMES, l.frame, 'ink'), lens: LENS, ink: H.ink, white: H.white, chalk: CLOTH_RGB.chalk,
      lip: mix(skin, mix(H.deep, H.ink, 0.45), 0.42), cheek: mix(skin, H.flame, 0.08), bindi: BINDI, metal: METAL,
      strap: CLOTH_RGB.ink, accent: founder ? H.flame : null
    };
  }
  const css = c => '#' + c.map(v => Math.max(0, Math.min(255, v | 0)).toString(16).padStart(2, '0')).join('');

  /* ---------- the 2D head: one list of shapes, drawn as SVG (img chips) or with Path2D (canvas textures) ----------
     A 64 by 64 box, the head centred at 32,30, the shoulders at the foot. The ground is left clear: .av sits on
     var(--warm), so one picture works in light and dark. Every number comes from the tables below. */
  const FACE = {round: [13.4, 14.2], oval: [12.4, 15], long: [11.6, 15.8], soft: [13, 14.6], heart: [13, 14.8]};
  const ell = (cx, cy, rx, ry) => 'M' + (cx - rx) + ' ' + cy + 'a' + rx + ' ' + ry + ' 0 1 0 ' + (2 * rx) + ' 0a' + rx + ' ' + ry + ' 0 1 0 ' + (-2 * rx) + ' 0Z';
  const rr = (x, y, w, h, r) => 'M' + (x + r) + ' ' + y + 'h' + (w - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 ' + r + ' ' + r + 'v' + (h - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 ' + (-r) + ' ' + r +
    'h' + (-(w - 2 * r)) + 'a' + r + ' ' + r + ' 0 0 1 ' + (-r) + ' ' + (-r) + 'v' + (-(h - 2 * r)) + 'a' + r + ' ' + r + ' 0 0 1 ' + r + ' ' + (-r) + 'Z';
  function facePath(face) {
    const [rx, ry] = FACE[face] || FACE.oval;
    const cx = 32, cy = 30;
    if (face === 'soft') return rr(cx - rx, cy - ry, rx * 2, ry * 2, 9.5);
    if (face === 'heart') {
      return 'M' + (cx - rx) + ' ' + (cy - 3) + 'C' + (cx - rx) + ' ' + (cy - ry - 2) + ' ' + (cx + rx) + ' ' + (cy - ry - 2) + ' ' + (cx + rx) + ' ' + (cy - 3) +
        'C' + (cx + rx) + ' ' + (cy + 7) + ' ' + (cx + 4) + ' ' + (cy + ry) + ' ' + cx + ' ' + (cy + ry) + 'C' + (cx - 4) + ' ' + (cy + ry) + ' ' + (cx - rx) + ' ' + (cy + 7) + ' ' + (cx - rx) + ' ' + (cy - 3) + 'Z';
    }
    return ell(cx, cy, rx, ry);
  }
  function shapes(look, founder, size) {
    const l = clean(look);
    const p = paint(l, founder);
    const [rx, ry] = FACE[l.face] || FACE.oval;
    const top = 30 - ry, L = 32 - rx, R = 32 + rx;
    const S = [];
    const add = (d, fill, x) => S.push({d, fill, ...(x || {})});
    const covered = l.head === 'scarf' || l.head === 'turban';
    const hairOn = !covered && l.hair !== 'none';
    /* hair that falls behind: drawn first */
    if (hairOn) {
      if (l.hair === 'long') add('M' + (L - 2.5) + ' 30C' + (L - 4) + ' 46 ' + (L - 3) + ' 56 ' + (L + 1) + ' 60H' + (R - 1) + 'C' + (R + 3) + ' 56 ' + (R + 4) + ' 46 ' + (R + 2.5) + ' 30Z', p.hair);
      if (l.hair === 'bob') add('M' + (L - 2.6) + ' 28C' + (L - 3.4) + ' 38 ' + (L - 2) + ' 42 ' + (L + 1) + ' 43.5H' + (R - 1) + 'C' + (R + 2) + ' 42 ' + (R + 3.4) + ' 38 ' + (R + 2.6) + ' 28Z', p.hair);
      if (l.hair === 'waves') add('M' + (L - 2.4) + ' 28C' + (L - 4) + ' 34 ' + (L - 1) + ' 37 ' + (L - 3) + ' 41S' + (L + 1) + ' 47 ' + (L + 2) + ' 46H' + (R - 2) + 'C' + (R - 1) + ' 47 ' + (R + 5) + ' 45 ' + (R + 3) + ' 41S' + (R + 4) + ' 34 ' + (R + 2.4) + ' 28Z', p.hair);
      if (l.hair === 'coils') add(ell(32, top + 9, rx + 7.5, ry * 0.78 + 5), p.hair);
      if (l.hair === 'ponytail') add('M' + (R - 1) + ' ' + (top + 8) + 'C' + (R + 7) + ' ' + (top + 10) + ' ' + (R + 8) + ' ' + (top + 26) + ' ' + (R + 4) + ' ' + (top + 31) + 'C' + (R + 4) + ' ' + (top + 22) + ' ' + (R + 1) + ' ' + (top + 16) + ' ' + (R - 3) + ' ' + (top + 13) + 'Z', p.hair);
      if (l.hair === 'bun') add(ell(32, top - 2.4, 5.2, 4.6), p.hair);
    }
    if (l.head === 'scarf') add('M' + (L - 3.2) + ' 30C' + (L - 3.6) + ' ' + (top - 5) + ' ' + (R + 3.6) + ' ' + (top - 5) + ' ' + (R + 3.2) + ' 30C' + (R + 3.6) + ' 42 ' + (R + 6) + ' 48 ' + (R + 10) + ' 52H' + (L - 10) + 'C' + (L - 6) + ' 48 ' + (L - 3.6) + ' 42 ' + (L - 3.2) + ' 30Z', p.headwear);
    /* shoulders, neck, ears, face */
    add('M4 64C5 55 12 50.5 21 49.5H43C52 50.5 59 55 60 64Z', p.top);
    collar(add, l, p);
    add(rr(27.2, 40, 9.6, 11, 4), p.skinShade);
    if (!covered) { add(ell(L + 0.4, 31.5, 2.4, 3.4), p.skinShade); add(ell(R - 0.4, 31.5, 2.4, 3.4), p.skinShade); }
    add(facePath(l.face), p.skin, {id: 'face'});
    /* the light: a soft shade on the side away from the key, a lift on the forehead */
    add(ell(32 + rx * 0.62, 32, rx * 0.62, ry * 0.92), p.skinShade, {clip: 'face', op: 0.35});
    add(ell(32 - rx * 0.28, top + ry * 0.45, rx * 0.5, ry * 0.32), p.skinLight, {clip: 'face', op: 0.55});
    /* facial hair under the features */
    if (l.facial === 'stubble') add('M' + L + ' 31C' + (L + 1) + ' 44 ' + (R - 1) + ' 44 ' + R + ' 31V48H' + L + 'Z', p.hair, {clip: 'face', op: 0.22});
    if (l.facial === 'short' || l.facial === 'full') {
      const low = l.facial === 'full' ? 4 : 1.5;
      add('M' + (L - 0.2) + ' 30C' + (L + 0.5) + ' ' + (44 + low) + ' ' + (R - 0.5) + ' ' + (44 + low) + ' ' + (R + 0.2) + ' 30C' + (R - 2) + ' 37 ' + (R - 6) + ' 37.5 32 36.6C' + (L + 6) + ' 37.5 ' + (L + 2) + ' 37 ' + (L - 0.2) + ' 30Z', p.beard, {clip: l.facial === 'full' ? null : 'face'});
    }
    if (l.facial === 'goatee') add(ell(32, 41.6, 3.1, 2.6), p.beard);
    /* eyes, brows, nose, mouth */
    const ey = 30.6, ex = 5.3;
    for (const sx of [-1, 1]) {
      const x = 32 + sx * ex;
      if (l.eyes === 'almond') add('M' + (x - 2.5) + ' ' + ey + 'Q' + x + ' ' + (ey - 3.1) + ' ' + (x + 2.5) + ' ' + ey + 'Q' + x + ' ' + (ey + 2.6) + ' ' + (x - 2.5) + ' ' + ey + 'Z', p.ink);
      else if (l.eyes === 'sleepy') add('M' + (x - 2.1) + ' ' + (ey - 0.2) + 'Q' + x + ' ' + (ey + 2.6) + ' ' + (x + 2.1) + ' ' + (ey - 0.2) + 'Z', p.ink);
      else add(ell(x, ey, 1.95, 2.35), p.ink);
      if (l.eyes !== 'sleepy') add(ell(x - 0.6, ey - 0.9, 0.62, 0.62), p.white);
      if (l.eyes === 'lashes') add('M' + (x + sx * 1.6) + ' ' + (ey - 1.8) + 'l' + (sx * 1.4) + ' -1.1', null, {stroke: p.ink, sw: 0.8});
      if (l.brows !== 'none') {
        const w = l.brows === 'bold' ? 1.9 : l.brows === 'fine' ? 0.8 : 1.3;
        const by = ey - (l.eyes === 'sleepy' ? 4.2 : 4.6);
        const d = l.brows === 'arched' ? 'M' + (x - 2.6) + ' ' + (by + 0.9) + 'Q' + (x - 0.3) + ' ' + (by - 1.6) + ' ' + (x + 2.6) + ' ' + (by + 0.5)
          : 'M' + (x - 2.5) + ' ' + (by + 0.4) + 'Q' + x + ' ' + (by - 0.6) + ' ' + (x + 2.5) + ' ' + (by + 0.2);
        add(d, null, {stroke: p.brow, sw: w});
      }
    }
    if (l.nose === 'button') add(ell(32, 34.6, 1.5, 1.05), p.skinShade);
    else if (l.nose === 'soft') add('M31 31.6Q30 34.6 32.6 35.2', null, {stroke: p.skinShade, sw: 1.1});
    else add('M32 30.6Q30.6 34.8 32.8 35.4', null, {stroke: p.skinShade, sw: 1.2});
    if (l.facial === 'moustache' || l.facial === 'goatee' || l.facial === 'full' || l.facial === 'short') add('M28.4 37.2Q32 35.2 35.6 37.2Q32 38.4 28.4 37.2Z', p.beard);
    if (l.mouth === 'grin') { add('M28.6 38.4Q32 43 35.4 38.4Z', p.lip); add('M29.4 38.6H34.6Q32 39.8 29.4 38.6Z', p.white); }
    else if (l.mouth === 'calm') add('M30 39.2Q32 40 34 39.2', null, {stroke: p.lip, sw: 1.1});
    else add('M28.8 38.6Q32 41.4 35.2 38.6', null, {stroke: p.lip, sw: 1.15});
    if (l.bindi) add(ell(32, ey - 6.2, 0.75, 0.75), p.bindi);
    if (l.stud) add(ell(29.6, 35.2, 0.45, 0.45), p.metal);
    if (!covered && l.ears === 'studs') { add(ell(L + 0.2, 35.2, 0.75, 0.75), p.metal); add(ell(R - 0.2, 35.2, 0.75, 0.75), p.metal); }
    if (!covered && l.ears === 'hoops') { add(ell(L + 0.2, 36.4, 1.4, 1.4), null, {stroke: p.metal, sw: 0.7}); add(ell(R - 0.2, 36.4, 1.4, 1.4), null, {stroke: p.metal, sw: 0.7}); }
    /* hair on top */
    if (hairOn) hairFront(add, l, p, {L, R, top, rx});
    /* headwear */
    if (l.head === 'scarf') add('M' + (L - 3.2) + ' 30C' + (L - 3.6) + ' ' + (top - 5) + ' ' + (R + 3.6) + ' ' + (top - 5) + ' ' + (R + 3.2) + ' 30C' + (R + 3) + ' 27 ' + (R - 0.6) + ' ' + (top + 4) + ' 32 ' + (top + 3.4) + 'C' + (L + 0.6) + ' ' + (top + 4) + ' ' + (L - 3) + ' 27 ' + (L - 3.2) + ' 30Z', p.headwear);
    if (l.head === 'turban') {
      add('M' + (L - 1.6) + ' ' + (top + 9) + 'C' + (L - 2.6) + ' ' + (top - 6) + ' ' + (R + 2.6) + ' ' + (top - 6) + ' ' + (R + 1.6) + ' ' + (top + 9) + 'Q32 ' + (top + 5.6) + ' ' + (L - 1.6) + ' ' + (top + 9) + 'Z', p.headwear);
      add('M' + (L + 1) + ' ' + (top + 5.2) + 'Q32 ' + (top - 5) + ' ' + (R - 2) + ' ' + (top + 1.2), null, {stroke: p.headwearDark, sw: 0.9});
      add('M' + (R - 1) + ' ' + (top + 5.6) + 'Q32 ' + (top - 2) + ' ' + (L + 2.4) + ' ' + (top + 0.6), null, {stroke: p.headwearDark, sw: 0.9});
    }
    if (l.head === 'cap' || l.head === 'beanie' || l.head === 'bucket') {
      add('M' + (L - 0.8) + ' ' + (top + 9) + 'C' + (L - 1.6) + ' ' + (top - 4.6) + ' ' + (R + 1.6) + ' ' + (top - 4.6) + ' ' + (R + 0.8) + ' ' + (top + 9) + 'Z', p.headwear);
      if (l.head === 'cap') add(ell(32 + rx * 0.35, top + 8.6, rx * 0.95, 2.2), p.headwearDark);
      if (l.head === 'beanie') add(rr(L - 1.2, top + 5.6, rx * 2 + 2.4, 4.4, 2.2), p.headwearLight);
      if (l.head === 'bucket') add(ell(32, top + 8.6, rx + 4.6, 2.6), p.headwearDark);
    }
    /* glasses over everything on the face */
    if (l.glasses !== 'none') glasses(add, l, p, ey, ex);
    /* the founder's one flame detail, only where there is room to read it as a detail */
    if (p.accent && size >= 40) {
      if (l.top === 'blazer') add('M20.6 55.8l3.4-1.2 0.6 2.6-3.4 0.8Z', p.accent);
      else add('M24 51.4Q32 54.4 40 51.4', null, {stroke: p.accent, sw: 1.2});
    }
    return S;
  }
  function collar(add, l, p) {
    if (l.top === 'tee' || l.top === 'dress') add('M26.2 49.6Q32 55 37.8 49.6Z', p.skinShade);
    if (l.top === 'crew') add('M25.4 49.4Q32 56 38.6 49.4', null, {stroke: p.topDark, sw: 2});
    if (l.top === 'hoodie') { add('M18 52Q32 44 46 52Q32 49.6 18 52Z', p.topDark); add('M29.6 52.6V58M34.4 52.6V58', null, {stroke: p.chalk, sw: 0.8}); }
    if (l.top === 'shirt') { add('M27 49.2L32 54L25 55Z', p.topLight); add('M37 49.2L32 54L39 55Z', p.topLight); add('M32 54V64', null, {stroke: p.topDark, sw: 0.6}); }
    if (l.top === 'blazer') { add('M26.4 49.4L32 64L37.6 49.4Z', p.chalk); add('M26.4 49.4L32 64L23.4 54.6Z', p.topDark); add('M37.6 49.4L32 64L40.6 54.6Z', p.topDark); }
    if (l.top === 'kurta') { add(rr(26.6, 48.4, 10.8, 3.2, 1.6), p.topDark); add('M32 51.6V60', null, {stroke: p.topDark, sw: 0.7}); }
  }
  function hairFront(add, l, p, g) {
    const {L, R, top, rx} = g;
    const cap = (lift, hairline, side) => 'M' + (L - 0.9) + ' ' + (32 - side) + 'C' + (L - 1.6) + ' ' + (top - lift) + ' ' + (R + 1.6) + ' ' + (top - lift) + ' ' + (R + 0.9) + ' ' + (32 - side) +
      'C' + (R - 0.6) + ' 27 ' + (R - 3) + ' ' + hairline + ' 32 ' + hairline + 'C' + (L + 3) + ' ' + hairline + ' ' + (L + 0.6) + ' 27 ' + (L - 0.9) + ' ' + (32 - side) + 'Z';
    const h = l.hair;
    if (h === 'buzz') { add(cap(1.6, top + 5.4, 4), p.hair, {op: 0.92}); return; }
    if (h === 'crop' || h === 'waves' || h === 'bob' || h === 'long' || h === 'bun' || h === 'ponytail' || h === 'braid' || h === 'coils') add(cap(2.8, top + 6.4, 3), p.hair);
    if (h === 'side') { add(cap(3, top + 7, 3), p.hair); add('M' + (L + 1) + ' ' + (top + 6) + 'C' + (L + 6) + ' ' + (top - 1) + ' ' + (R + 1) + ' ' + (top + 1) + ' ' + (R + 0.6) + ' ' + (top + 11) + 'C' + (R - 3) + ' ' + (top + 5) + ' ' + (L + 7) + ' ' + (top + 6) + ' ' + (L + 1) + ' ' + (top + 9) + 'Z', p.hair); }
    if (h === 'quiff') { add(cap(3, top + 6.6, 3), p.hair); add(ell(30.4, top - 0.4, 6.8, 4.2), p.hair); add(ell(29.2, top - 1.4, 3.4, 1.4), p.white, {op: 0.14}); }
    if (h === 'curls') { add(cap(2, top + 6, 3), p.hair); for (let i = 0; i < 7; i++) { const a = Math.PI * (0.08 + i * 0.14); add(ell(32 - Math.cos(a) * (rx + 0.6), top + 5.8 - Math.sin(a) * 5.2, 3.3, 3.3), p.hair); } }
    if (h === 'bob') add('M' + (L + 0.6) + ' ' + (top + 8.6) + 'H' + (R - 0.6) + 'V' + (top + 5) + 'H' + (L + 0.6) + 'Z', p.hair);
    if (h === 'long' || h === 'waves') add('M32 ' + (top + 0.8) + 'L32 ' + (top + 6.6), null, {stroke: p.hairShade, sw: 0.6});
    if (h === 'braid') for (let i = 0; i < 4; i++) add(ell(R - 0.8 + i * 0.6, 41 + i * 4.6, 2.6 - i * 0.2, 2.6), p.hair);
    /* a soft sheen across the top */
    add('M' + (L + 3.4) + ' ' + (top + 3.4) + 'Q32 ' + (top - 0.6) + ' ' + (R - 5) + ' ' + (top + 2.2), null, {stroke: p.white, sw: 1, op: 0.16});
  }
  function glasses(add, l, p, ey, ex) {
    const f = p.frame, sw = l.glasses === 'soft' ? 1.35 : 0.95;
    for (const sx of [-1, 1]) {
      const x = 32 + sx * ex;
      const lens = l.glasses === 'round' ? ell(x, ey, 3.5, 3.5) : rr(x - 3.8, ey - 3.1, 7.6, 6.2, l.glasses === 'square' ? 1.3 : 2.3);
      if (l.glasses === 'shades') add(lens, p.lens, {op: 0.88});
      add(lens, null, {stroke: f, sw});
      if (l.glasses === 'soft') add('M' + (x - 3.6) + ' ' + (ey - 2.7) + 'H' + (x + 3.6), null, {stroke: f, sw: 1.8});
    }
    add('M' + (32 - ex + 3.6) + ' ' + (ey - 0.6) + 'Q32 ' + (ey - 1.8) + ' ' + (32 + ex - 3.6) + ' ' + (ey - 0.6), null, {stroke: f, sw: 0.9});
  }
  /* the SVG document: element names, attribute names and numbers only */
  function toSvg(S) {
    const face = S.find(s => s.id === 'face');
    let out = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="8 9 48 48">';
    if (face) out += '<clipPath id="f"><path d="' + face.d + '"/></clipPath>';
    for (const s of S) {
      out += '<path d="' + s.d + '"' + (s.fill ? ' fill="' + css(s.fill) + '"' : ' fill="none"') +
        (s.stroke ? ' stroke="' + css(s.stroke) + '" stroke-width="' + s.sw + '" stroke-linecap="round"' : '') +
        (s.op != null ? ' opacity="' + s.op + '"' : '') + (s.clip === 'face' ? ' clip-path="url(#f)"' : '') + '/>';
    }
    return out + '</svg>';
  }
  /* the same list on a 2D canvas with Path2D (no image decode, so Safari never taints a texture) */
  function drawList(g, S, px) {
    if (!g || typeof Path2D !== 'function') return;
    const k = (Number(px) || 64) / 48;
    const face = S.find(s => s.id === 'face');
    const fp = face ? new Path2D(face.d) : null;
    g.save(); g.scale(k, k); g.translate(-8, -9); g.lineCap = 'round';
    for (const s of S) {
      const path = new Path2D(s.d);
      g.save();
      if (s.clip === 'face' && fp) g.clip(fp);
      g.globalAlpha = s.op != null ? s.op : 1;
      if (s.fill) { g.fillStyle = css(s.fill); g.fill(path); }
      if (s.stroke) { g.strokeStyle = css(s.stroke); g.lineWidth = s.sw; g.stroke(path); }
      g.restore();
    }
    g.restore();
  }
  /* head2d(look, {founder, size}) -> {url, draw(ctx2d, px)}: one display list, two outputs. Cached by the
     look's hash, the founder mark and the size class (the flame detail shows at 40 px and up) */
  const heads = new Map();
  function head2d(look, o) {
    const opts = o || {};
    const founder = !!opts.founder;
    const size = Number(opts.size) || 64;
    const key = hash(look, (founder ? 'F' : '') + (size >= 40 ? 'L' : 'S'));
    let h = heads.get(key);
    if (!h) {
      const S = shapes(look, founder, size);
      h = {url: 'data:image/svg+xml,' + encodeURIComponent(toSvg(S)), draw: (g, px) => drawList(g, S, px)};
      if (heads.size > 160) heads.delete(heads.keys().next().value);
      heads.set(key, h);
    }
    return h;
  }
  /* headUrl(ctx, uid, {size}): the head a person shows, as a data URL */
  function headUrl(ctx, uid, o) {
    const r = resolveFor(ctx, uid);
    return head2d(r.look, {founder: r.founder, size: (o && o.size) || 64}).url;
  }

  /* shuffle(rand, keep): a fresh look inside the tables for the editor's Shuffle. Skin, facial hair, the
     extras and pic stay the person's own */
  function shuffle(rand, keep) {
    const r = typeof rand === 'function' ? rand : Math.random;
    const pick = arr => arr[Math.floor(r() * arr.length) % arr.length];
    const out = clean(keep);
    for (const k of ['face', 'eyes', 'brows', 'nose', 'mouth', 'hair', 'top', 'bottom', 'shoes', 'pose']) out[k] = pick(SHAPES[k]);
    for (const k of ['hairColor', 'topColor', 'bottomColor', 'shoeColor']) out[k] = pick(COLOURS[k]).id;
    out.glasses = r() < 0.35 ? pick(SHAPES.glasses.slice(1)) : 'none';
    out.frame = pick(FRAMES).id;
    out.head = r() < 0.15 ? pick(SHAPES.head.slice(1, 4)) : 'none';
    out.headColor = pick(CLOTH).id;
    delete out.by; delete out.at;
    return clean(out);
  }

  M.cast = {NATURAL, HOUSE, SKIN, HAIR, CLOTH, FRAMES, WOOD, SHAPES, COLOURS, FLAGS, ORDER, DEFAULT,
    clean, hash, same, starter, initials, sticker, resolve, resolveFor, lookOf, paint, mix, css, head2d, headUrl, shuffle};
})();
