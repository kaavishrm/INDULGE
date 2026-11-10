/* v52: with no Resend key, the OS's own emails (reset codes) go out from the founder's connected Gmail.
   Run: node harness/tests/mail_gmail.mjs */
import {createApp} from '../../edgeone/server/core.js';

let fails = 0;
const check = (ok, msg) => { console.log((ok ? 'ok   ' : 'FAIL ') + msg); if (!ok) fails++; };
const UID = 'u_owner', TOK = 'tok_owner_123456789';
const b64d = s => new TextDecoder().decode(Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0)));

function memStore() {
  const data = new Map();
  return {data,
    async get(k, o) { if (!data.has(k)) return null; const v = data.get(k); return o && o.type === 'json' ? JSON.parse(v) : v; },
    async set(k, v, o) { if (o && o.onlyIfNew && data.has(k)) { const e = new Error('exists'); e.code = 'PRECONDITION_FAILED'; throw e; } data.set(k, String(v)); },
    async delete(k) { data.delete(k); },
    async list(o) { const p = (o && o.prefix) || ''; return {blobs: [...data.keys()].filter(k => k.startsWith(p)).sort().map(key => ({key})), directories: []}; }};
}
function seed(store, scope) {
  const put = (k, v) => store.data.set(k, JSON.stringify(v));
  const now = Date.now();
  put('o/owner', {uid: UID});
  put('p/' + UID, {name: 'Owner', email: 'owner@example.test', at: now});
  put('e/' + encodeURIComponent('owner@example.test'), {uid: UID});
  put('x/google', {clientId: 'cid', clientSecret: 'secret'});
  if (scope != null) put('x/g/' + UID, {refresh: 'rt', access: '', exp: 0, email: 'owner@example.test', scope});
}
function fakeGoogle() {
  const sent = [];
  const json = (o, s = 200) => new Response(JSON.stringify(o), {status: s, headers: {'content-type': 'application/json'}});
  const fetch = async (url, init) => {
    const u = new URL(String(url));
    if (u.host === 'oauth2.googleapis.com') return json({access_token: 'at', expires_in: 3600});
    if (u.pathname.endsWith('/messages/send')) { sent.push(b64d(JSON.parse(init.body).raw)); return json({id: 'm1', threadId: 't1'}); }
    return json({error: 'unexpected ' + u}, 500);
  };
  return {sent, fetch};
}
async function call(app, a, body) {
  const r = await app(new Request('https://m360.test/api/m360', {method: 'POST', headers: {'content-type': 'application/json', cookie: 'm360s=' + TOK}, body: JSON.stringify({a, ...(body || {})})}));
  let j = {}; try { j = await r.json(); } catch (e) { /* empty */ }
  return {status: r.status, j};
}

/* 1: Gmail connected with gmail.modify: the reset code is sent from it */
{
  const store = memStore(); seed(store, 'openid email https://www.googleapis.com/auth/gmail.modify');
  const g = fakeGoogle(); globalThis.fetch = g.fetch;
  const app = createApp({store, env: {fetch: g.fetch}});
  const r = await call(app, 'reset', {email: 'owner@example.test'});
  check(r.status === 200 && r.j.sent === true && !r.j.nomail, 'reset answers sent (' + JSON.stringify(r.j) + ')');
  check(g.sent.length === 1, 'one email went through Gmail');
  const m = g.sent[0] || '';
  check(/To: owner@example.test/.test(m) && /From: m360 OS <owner@example.test>/.test(m), 'to the person, from the founder\'s Gmail');
  const parts = [...m.matchAll(/base64\r\n\r\n([A-Za-z0-9+/=]+)/g)].map(x => new TextDecoder().decode(Uint8Array.from(atob(x[1]), c => c.charCodeAt(0))));
  check(parts.some(p => /reset code is \d{6}/.test(p)), 'the 6 digit code is in the email');
  check(/multipart\/alternative/.test(m) && parts.length === 2, 'text and html together');
}
/* 2: no Google at all: still nomail, nothing sent */
{
  const store = memStore(); seed(store, null);
  const g = fakeGoogle(); globalThis.fetch = g.fetch;
  const app = createApp({store, env: {fetch: g.fetch}});
  const r = await call(app, 'reset', {email: 'owner@example.test'});
  check(r.j.nomail === true && g.sent.length === 0, 'no Google, no Resend: nomail as before');
}
/* 3: Google connected for Drive only (no Gmail scope): not used for mail */
{
  const store = memStore(); seed(store, 'openid email https://www.googleapis.com/auth/drive.file');
  const g = fakeGoogle(); globalThis.fetch = g.fetch;
  const app = createApp({store, env: {fetch: g.fetch}});
  const r = await call(app, 'reset', {email: 'owner@example.test'});
  check(r.j.nomail === true && g.sent.length === 0, 'Drive-only Google is not used for mail');
}
console.log(fails ? fails + ' failed' : 'all passed');
process.exit(fails ? 1 : 0);
