/* module: the Claude connector (v55). Kaavish's own Claude (claude.ai, his plan) reads and changes the OS through
   this endpoint, POST /api/mcp?k=<key>, which speaks MCP (JSON-RPC over HTTP, JSON answers, no streaming).

   It is the owner's hand and nobody else's. The key is made by the owner alone (the mcpkey action, Admin), shown
   once, and kept here only as its SHA-256 in o/mcp. Every change goes through the same write action the page uses,
   as the owner: the rules, the guards, the backups, the live Drive log and the activity log all apply. A new key
   replaces the old one; mcpoff turns the connector off. */

const PROTOCOL = '2025-06-18';
const OUT_MAX = 60000;
const KINDS = ['update', 'win', 'question', 'announce'];
/* the Base is large and searched on the page; a listing shows this many documents at most */
const LIST_MAX = 200;

const sha256hex = async s => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))),
  b => b.toString(16).padStart(2, '0')).join('');
const isObj = x => x && typeof x === 'object' && !Array.isArray(x);
const clip = s => (s.length > OUT_MAX ? s.slice(0, OUT_MAX) + '\n[cut at ' + OUT_MAX + ' characters: ask for less, or one document at a time]' : s);

const TOOLS = [
  {name: 'os_overview',
    description: 'Start here. Every collection in m360 OS with how many documents it holds, and the team (uid, name, role, title). Paths look like <collection>/<id>, for example tasks/abc or clients/xyz.',
    inputSchema: {type: 'object', properties: {}}},
  {name: 'os_list',
    description: 'The documents in one collection, as {id: document}. Read a few before writing, to see the fields the OS uses.',
    inputSchema: {type: 'object', properties: {collection: {type: 'string', description: 'for example tasks, clients, projects, feed'},
      limit: {type: 'number', description: 'at most ' + LIST_MAX + ', default 50'}}, required: ['collection']}},
  {name: 'os_read',
    description: 'One document by its path, for example tasks/abc.',
    inputSchema: {type: 'object', properties: {path: {type: 'string'}}, required: ['path']}},
  {name: 'os_write',
    description: 'Change one document as Kaavish. op: merge (change the fields given, create if missing), set (replace the whole document), update (change fields of an existing one), delete. Keep the field names and shapes the OS already uses, and set updated to the current time in milliseconds where the document has it. Every change is backed up and logged.',
    inputSchema: {type: 'object', properties: {path: {type: 'string'}, op: {type: 'string', enum: ['merge', 'set', 'update', 'delete']},
      data: {type: 'object', description: 'the fields; leave out for delete'}}, required: ['path', 'op']}},
  {name: 'os_post_update',
    description: 'Post on the team feed as Kaavish. kind: update, win, question or announce (an announcement is pinned to the top of the feed).',
    inputSchema: {type: 'object', properties: {text: {type: 'string'}, kind: {type: 'string', enum: KINDS}}, required: ['text']}},
  {name: 'os_activity',
    description: 'What changed in the OS between two days (YYYY-MM-DD, IST, at most 31 days), person by person.',
    inputSchema: {type: 'object', properties: {from: {type: 'string'}, to: {type: 'string'}}, required: ['from']}}
];

export function mcpDesk({getJ, putJ, store, inventory, readColl, ownerUid, actions, LEVEL, levelOf, HttpError, rand, log}) {
  const KEY = 'o/mcp';

  /* the owner's side, from Admin: make (or replace) the key, see whether one is set, turn it off */
  const deskActions = {
    async mcpkey(v) {
      if (!v || (await levelOf(v.uid)) < LEVEL.owner) throw new HttpError(403, 'invalid_argument', 'Only Kaavish connects Claude.');
      const key = rand(32);
      await putJ(KEY, {h: await sha256hex(key), at: Date.now()});
      await log(v.uid, 'mcpkey', '', 'Claude connector key made');
      return {key};
    },
    async mcpstatus(v) {
      if (!v || (await levelOf(v.uid)) < LEVEL.owner) throw new HttpError(403, 'invalid_argument');
      const c = await getJ(KEY).catch(() => null);
      return {on: !!(c && c.h), at: (c && c.at) || null, used: (c && c.used) || null};
    },
    async mcpoff(v) {
      if (!v || (await levelOf(v.uid)) < LEVEL.owner) throw new HttpError(403, 'invalid_argument');
      await store.delete(KEY).catch(() => {});
      await log(v.uid, 'mcpoff', '', 'Claude connector turned off');
      return {on: false};
    }
  };

  /* the key from ?k= or Authorization: Bearer; the owner when it matches, nobody otherwise */
  async function who(request) {
    let k = '';
    try { k = new URL(request.url).searchParams.get('k') || ''; } catch (e) { k = ''; }
    const auth = String(request.headers.get('authorization') || '');
    if (!k && /^Bearer\s+/i.test(auth)) k = auth.replace(/^Bearer\s+/i, '').trim();
    if (!/^[a-z0-9]{20,80}$/.test(k)) return null;
    const c = await getJ(KEY).catch(() => null);
    if (!c || !c.h || c.h !== await sha256hex(k)) return null;
    const uid = await ownerUid();
    if (!uid) return null;
    /* when it was last used, at most once an hour */
    if (!c.used || Date.now() - c.used > 3600000) putJ(KEY, {...c, used: Date.now()}).catch(() => {});
    return {uid};
  }

  async function names() {
    const team = (await getJ('d/roster~team').catch(() => null)) || {};
    const members = team.members || {};
    const out = [];
    await Promise.all(Object.keys(members).map(async uid => {
      const m = members[uid] || {};
      const p = (await getJ('p/' + uid).catch(() => null)) || {};
      out.push({uid, name: p.name || '', role: m.role || 'member', title: m.title || '', active: m.active !== false});
    }));
    return out.sort((a, b) => a.name.localeCompare(b.name));
  }

  async function call(v, name, args) {
    const a = isObj(args) ? args : {};
    if (name === 'os_overview') {
      const inv = await inventory();
      const collections = {};
      for (const c of Object.keys(inv).sort()) collections[c] = Object.keys(inv[c]).length;
      return {owner: v.uid, team: await names(), collections};
    }
    if (name === 'os_list') {
      const coll = String(a.collection || '').replace(/^\/+|\/+$/g, '');
      if (!coll || coll.split('/').length % 2 !== 1) throw new HttpError(400, 'invalid_argument', 'a collection path has an odd number of parts, like tasks');
      const inv = await inventory();
      const tags = inv[coll] || {};
      const ids = Object.keys(tags).sort();
      const limit = Math.max(1, Math.min(LIST_MAX, Number(a.limit) || 50));
      const pick = {};
      for (const id of ids.slice(0, limit)) pick[id] = tags[id];
      const docs = ids.length ? await readColl(coll, pick) : {};
      return {collection: coll, total: ids.length, shown: Object.keys(docs).length, docs};
    }
    if (name === 'os_read') {
      const path = String(a.path || '').replace(/^\/+|\/+$/g, '');
      if (!path || path.split('/').length % 2) throw new HttpError(400, 'invalid_argument', 'a document path has an even number of parts, like tasks/abc');
      const doc = await getJ('d/' + path.split('/').join('~')).catch(() => null);
      return {path, exists: doc != null, doc};
    }
    if (name === 'os_write') {
      const r = await actions.write(v, {op: String(a.op || ''), path: String(a.path || '').replace(/^\/+|\/+$/g, ''), data: a.data});
      return {ok: true, path: a.path, doc: r && r.doc};
    }
    if (name === 'os_post_update') {
      const text = String(a.text || '').trim().slice(0, 4000);
      if (!text) throw new HttpError(400, 'invalid_argument', 'nothing to post');
      const kind = KINDS.includes(a.kind) ? a.kind : 'update';
      const path = 'feed/' + v.uid;
      const mine = (await getJ('d/feed~' + v.uid).catch(() => null)) || {};
      const id = rand(10);
      const post = {id, kind, text, at: Date.now()};
      const posts = [post, ...(Array.isArray(mine.posts) ? mine.posts : [])].slice(0, 80);
      const patch = {posts};
      if (kind === 'announce') patch.pinned = v.uid + ':' + id;
      await actions.write(v, {op: 'merge', path, data: patch});
      return {ok: true, posted: post};
    }
    if (name === 'os_activity') {
      return actions.logs(v, {from: String(a.from || ''), to: String(a.to || a.from || '')});
    }
    throw new HttpError(400, 'invalid_argument', 'no tool named ' + name);
  }

  async function rpc(v, msg) {
    const {id, method, params} = msg || {};
    const ok = result => ({jsonrpc: '2.0', id, result});
    const err = (code, message) => ({jsonrpc: '2.0', id: id == null ? null : id, error: {code, message}});
    if (!msg || msg.jsonrpc !== '2.0' || typeof method !== 'string') return err(-32600, 'invalid request');
    /* a notification gets no answer */
    if (id === undefined) return null;
    if (method === 'initialize') {
      const asked = params && typeof params.protocolVersion === 'string' ? params.protocolVersion : PROTOCOL;
      return ok({protocolVersion: asked, capabilities: {tools: {}}, serverInfo: {name: 'm360 OS', version: '55'},
        instructions: 'm360 OS, Mask360\'s team workspace. You act as Kaavish, the founder, with full control. Call os_overview first, read a few documents of a collection before changing it, and keep the shapes the OS already uses. Changes show on the team site within seconds.'});
    }
    if (method === 'ping') return ok({});
    if (method === 'tools/list') return ok({tools: TOOLS});
    if (method === 'tools/call') {
      const name = params && params.name;
      try {
        const out = await call(v, name, params && params.arguments);
        return ok({content: [{type: 'text', text: clip(JSON.stringify(out, null, 1))}]});
      } catch (e) {
        /* a refusal is the tool's answer, so Claude reads why and can try again */
        const why = (e && e.message) || 'failed';
        return ok({isError: true, content: [{type: 'text', text: 'Not done: ' + why}]});
      }
    }
    return err(-32601, 'no method ' + method);
  }

  async function handle(request) {
    const json = (obj, status = 200) => new Response(obj == null ? null : JSON.stringify(obj), {status,
      headers: {'content-type': 'application/json', 'cache-control': 'no-store'}});
    /* no stream to open: an MCP client that asks for one with a GET is told so */
    if (request.method !== 'POST') return json({error: 'POST only'}, 405);
    const v = await who(request);
    if (!v) return json({jsonrpc: '2.0', id: null, error: {code: -32001, message: 'This connector link is not valid. Make a new one in Admin on the team site.'}}, 401);
    let body;
    try { body = JSON.parse(await request.text()); } catch (e) { return json({jsonrpc: '2.0', id: null, error: {code: -32700, message: 'bad json'}}, 400); }
    if (Array.isArray(body)) {
      const out = (await Promise.all(body.map(m => rpc(v, m)))).filter(Boolean);
      return out.length ? json(out) : json(null, 202);
    }
    const out = await rpc(v, body);
    return out ? json(out) : json(null, 202);
  }

  return {actions: deskActions, handle};
}
