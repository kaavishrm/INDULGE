/* module: sign-in for the Claude connector (v55.1). Claude's custom connectors sign in with OAuth 2.1 (dynamic client
   registration, PKCE), so the connector link carries no secret: Claude sends Kaavish to the team site, he is already
   signed in there, he presses Allow once, and Claude gets a token that works for him alone.

     /.well-known/oauth-protected-resource[/api/mcp]   what protects /api/mcp, and who signs in for it
     /.well-known/oauth-authorization-server            the endpoints below (also as openid-configuration)
     POST /api/oauth/register    a client registers its return address; Claude and a local Claude Code only
     GET  /api/oauth/authorize   the owner, signed in on this site, allows it; anyone else is told no
     POST /api/oauth/token       a code (with its PKCE verifier) or a refresh token becomes a new access token

   Kept in the store: oc/<client> the client, oa/<hash> a code (5 minutes, once), ok/<hash> the Allow button's
   one-time nonce (10 minutes), ot/<hash> an access token (1 hour), or/<hash> a refresh token (90 days, replaced on
   every use). Only SHA-256 hashes of codes and tokens are stored. Disconnect in Admin (mcpoff) ends them all. */

const CODE_MS = 5 * 60000, NONCE_MS = 10 * 60000, ACCESS_S = 3600, REFRESH_MS = 90 * 86400000;
/* where a registered client may send the code back: Claude on the web, and a Claude Code on this machine */
const REDIRECT_OK = /^(https:\/\/(claude\.ai|claude\.com)\/[^\s#]*|http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/[^\s#]*)$/;

const sha = async s => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))),
  b => b.toString(16).padStart(2, '0')).join('');
const b64url = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const s256 = async v => b64url(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(v))));
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

export function oauthDesk({getJ, putJ, store, viewer, ownerUid, rand, log, env}) {
  /* the site's public address: the platform hands a function its own internal address, so the forwarded host wins */
  function siteOf(request) {
    if (env && env.SITE_URL && /^https:\/\//.test(env.SITE_URL)) return String(env.SITE_URL).replace(/\/+$/, '');
    const fwd = String(request.headers.get('x-forwarded-host') || '').split(',')[0].trim();
    if (/^[a-z0-9.-]+(:\d+)?$/i.test(fwd) && !/qcloudteo\.com$/i.test(fwd)) return 'https://' + fwd;
    let u;
    try { u = new URL(request.url); } catch (e) { return ''; }
    const host = String(request.headers.get('host') || '');
    if (/^(localhost|127\.0\.0\.1)(:\d+)?$/.test(host) || /^(localhost|127\.0\.0\.1)$/.test(u.hostname)) return 'http://' + (host || u.host);
    if (/^[a-z0-9.-]+(:\d+)?$/i.test(host) && !/qcloudteo\.com$/i.test(host)) return 'https://' + host;
    return u.origin;
  }
  const meta = site => ({
    issuer: site,
    authorization_endpoint: site + '/api/oauth/authorize',
    token_endpoint: site + '/api/oauth/token',
    registration_endpoint: site + '/api/oauth/register',
    response_types_supported: ['code'],
    grant_types_supported: ['authorization_code', 'refresh_token'],
    code_challenge_methods_supported: ['S256'],
    token_endpoint_auth_methods_supported: ['none'],
    scopes_supported: ['m360']
  });
  const resourceMeta = site => ({resource: site + '/api/mcp', authorization_servers: [site], bearer_methods_supported: ['header'], scopes_supported: ['m360'], resource_name: 'm360 OS'});

  const CORS = {'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET, POST, OPTIONS', 'access-control-allow-headers': 'authorization, content-type, mcp-protocol-version'};
  const json = (obj, status = 200, extra = {}) => new Response(JSON.stringify(obj), {status, headers: {'content-type': 'application/json', 'cache-control': 'no-store', ...CORS, ...extra}});
  const oerr = (error, description, status = 400) => json({error, error_description: description}, status);
  const page = (title, body, status = 200) => new Response('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(title) + '</title>' +
    '<style>body{font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif;background:#f4f1ea;color:#0e0e0e;margin:0;display:grid;place-items:center;min-height:100vh;padding:16px;box-sizing:border-box}' +
    'main{background:#fff;border-radius:14px;padding:28px;max-width:420px;width:100%;box-shadow:0 1px 3px rgba(0,0,0,.08)}h1{font-size:20px;margin:0 0 10px}p{margin:0 0 14px;color:#3a3a3a}' +
    'a.btn{display:inline-block;background:#0e0e0e;color:#fff;text-decoration:none;padding:10px 18px;border-radius:999px;margin-right:8px}a.ghost{color:#0e0e0e;padding:10px 4px}small{color:#7a7a7a}</style></head><body><main>' + body + '</main></body></html>',
  {status, headers: {'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-frame-options': 'DENY',
    'content-security-policy': "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"}});

  async function bodyOf(request) {
    const t = await request.text().catch(() => '');
    const ct = String(request.headers.get('content-type') || '');
    if (/json/i.test(ct)) { try { return JSON.parse(t) || {}; } catch (e) { return {}; } }
    const o = {};
    for (const [k, v] of new URLSearchParams(t)) o[k] = v;
    return o;
  }

  async function register(request) {
    const b = await bodyOf(request);
    const uris = Array.isArray(b.redirect_uris) ? b.redirect_uris.map(String) : [];
    if (!uris.length || uris.length > 5 || uris.some(u => !REDIRECT_OK.test(u))) return oerr('invalid_redirect_uri', 'Only Claude can connect to m360 OS.');
    const id = 'c_' + rand(16);
    const client = {client_id: id, redirect_uris: uris, client_name: String(b.client_name || 'Claude').slice(0, 80), at: Date.now()};
    await putJ('oc/' + id, client);
    return json({...client, client_id_issued_at: Math.floor(client.at / 1000), token_endpoint_auth_method: 'none',
      grant_types: ['authorization_code', 'refresh_token'], response_types: ['code']}, 201);
  }

  async function authorize(request, site) {
    const q = new URL(request.url).searchParams;
    const p = {client_id: q.get('client_id') || '', redirect_uri: q.get('redirect_uri') || '', state: q.get('state') || '',
      code_challenge: q.get('code_challenge') || '', method: q.get('code_challenge_method') || '', response_type: q.get('response_type') || ''};
    const client = /^c_[a-z0-9]{8,40}$/.test(p.client_id) ? await getJ('oc/' + p.client_id).catch(() => null) : null;
    /* a bad client or return address is never sent anywhere: the page says so */
    if (!client || !client.redirect_uris.includes(p.redirect_uri)) return page('Not connected', '<h1>This link is not valid</h1><p>Start again from Claude: Settings, Connectors.</p>', 400);
    const back = (params) => {
      const u = new URL(p.redirect_uri);
      for (const [k, v] of Object.entries(params)) u.searchParams.set(k, v);
      if (p.state) u.searchParams.set('state', p.state);
      return new Response(null, {status: 302, headers: {location: u.toString(), 'cache-control': 'no-store'}});
    };
    if (p.response_type !== 'code' || p.method !== 'S256' || !/^[A-Za-z0-9_-]{43,128}$/.test(p.code_challenge)) return back({error: 'invalid_request', error_description: 'PKCE with S256 is required'});
    const v = await viewer(request);
    const owner = await ownerUid();
    if (!v) return page('Sign in first', '<h1>Sign in to m360 OS first</h1><p>Open the team site in this browser and sign in, then come back to Claude and press Connect again.</p><a class="btn" href="' + esc(site + '/') + '">Open m360 OS</a>', 401);
    if (!owner || v.uid !== owner) return page('Not allowed', '<h1>Only Kaavish connects Claude</h1><p>The Claude connector runs the whole OS, so it is for the founder alone.</p>', 403);
    const nonce = q.get('allow') || '';
    if (nonce) {
      const k = 'ok/' + await sha(nonce);
      const n = await getJ(k).catch(() => null);
      await store.delete(k).catch(() => {});
      const same = n && n.uid === v.uid && n.client_id === p.client_id && n.redirect_uri === p.redirect_uri && n.challenge === p.code_challenge;
      if (!same || Date.now() - n.at > NONCE_MS) return page('Try again', '<h1>That took too long</h1><p>Go back to Claude and press Connect again.</p>', 400);
      const code = rand(32);
      await putJ('oa/' + await sha(code), {uid: v.uid, client_id: p.client_id, redirect_uri: p.redirect_uri, challenge: p.code_challenge, at: Date.now()});
      await log(v.uid, 'mcpkey', '', 'Claude connected');
      return back({code});
    }
    /* the Allow button is a plain link with a one-time nonce tied to this session and this request */
    const fresh = rand(24);
    await putJ('ok/' + await sha(fresh), {uid: v.uid, client_id: p.client_id, redirect_uri: p.redirect_uri, challenge: p.code_challenge, at: Date.now()});
    const allow = new URL(site + '/api/oauth/authorize');
    for (const [k, val] of q) if (k !== 'allow') allow.searchParams.set(k, val);
    allow.searchParams.set('allow', fresh);
    return page('Connect Claude', '<h1>Connect Claude to m360 OS</h1><p>' + esc(client.client_name) + ' will read and change the OS as you: tasks, clients, projects, the feed and the rest. Every change is backed up and logged under your name.</p>' +
      '<p><small>You can disconnect it any time in Admin, Claude.</small></p><a class="btn" id="allow" href="' + esc(allow.toString()) + '">Allow</a><a class="ghost" href="' + esc(site + '/') + '">Cancel</a>');
  }

  async function issue(uid, clientId) {
    const access = rand(40), refresh = rand(40);
    await Promise.all([
      putJ('ot/' + await sha(access), {uid, client_id: clientId, exp: Date.now() + ACCESS_S * 1000}),
      putJ('or/' + await sha(refresh), {uid, client_id: clientId, exp: Date.now() + REFRESH_MS})
    ]);
    return json({access_token: access, token_type: 'Bearer', expires_in: ACCESS_S, refresh_token: refresh, scope: 'm360'});
  }

  async function token(request) {
    const b = await bodyOf(request);
    const owner = await ownerUid();
    if (b.grant_type === 'authorization_code') {
      const k = 'oa/' + await sha(String(b.code || ''));
      const c = await getJ(k).catch(() => null);
      await store.delete(k).catch(() => {});
      if (!c || Date.now() - c.at > CODE_MS) return oerr('invalid_grant', 'code expired or used');
      if (c.client_id !== b.client_id || (b.redirect_uri && b.redirect_uri !== c.redirect_uri)) return oerr('invalid_grant', 'code was issued to another client');
      if (!b.code_verifier || await s256(String(b.code_verifier)) !== c.challenge) return oerr('invalid_grant', 'PKCE check failed');
      if (c.uid !== owner) return oerr('invalid_grant', 'only the owner', 403);
      return issue(c.uid, c.client_id);
    }
    if (b.grant_type === 'refresh_token') {
      const k = 'or/' + await sha(String(b.refresh_token || ''));
      const r = await getJ(k).catch(() => null);
      if (!r || r.exp < Date.now() || (b.client_id && b.client_id !== r.client_id) || r.uid !== owner) return oerr('invalid_grant', 'refresh token not valid');
      /* a refresh token works once: the next one replaces it */
      await store.delete(k).catch(() => {});
      return issue(r.uid, r.client_id);
    }
    return oerr('unsupported_grant_type', 'authorization_code or refresh_token');
  }

  /* an access token's owner, while it is live and he still owns the workspace */
  async function bearer(tok) {
    if (!/^[a-z0-9]{40,80}$/.test(tok)) return null;
    const t = await getJ('ot/' + await sha(tok)).catch(() => null);
    if (!t || t.exp < Date.now()) return null;
    const owner = await ownerUid();
    return owner && t.uid === owner ? {uid: owner} : null;
  }

  /* Disconnect: every token, refresh token, code and registered client goes */
  async function revokeAll() {
    for (const p of ['ot/', 'or/', 'oa/', 'ok/', 'oc/']) {
      const list = ((await store.list({prefix: p}).catch(() => ({blobs: []}))) || {}).blobs || [];
      await Promise.all(list.map(b => store.delete(b.key).catch(() => {})));
    }
  }

  async function handle(request) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '');
    const site = siteOf(request);
    if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: CORS});
    if (path.startsWith('/.well-known/oauth-protected-resource')) return json(resourceMeta(site));
    if (path.startsWith('/.well-known/oauth-authorization-server') || path.startsWith('/.well-known/openid-configuration')) return json(meta(site));
    if (path === '/api/oauth/register' && request.method === 'POST') return register(request);
    if (path === '/api/oauth/authorize' && request.method === 'GET') return authorize(request, site);
    if (path === '/api/oauth/token' && request.method === 'POST') return token(request);
    if (path === '/api/oauth/protected-resource') return json(resourceMeta(site));
    if (path === '/api/oauth/metadata') return json(meta(site));
    return json({error: 'not_found'}, 404);
  }

  return {handle, bearer, revokeAll, siteOf};
}
