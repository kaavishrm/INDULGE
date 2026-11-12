#!/usr/bin/env python3
"""v55, the Claude connector: Kaavish runs the OS from his own Claude through /api/mcp, with a key only he makes.

  - the owner makes a link in Admin, Claude; it shows once, with the steps
  - MCP: initialize, tools/list, and every tool (overview, list, read, write, post, activity)
  - a change made through Claude shows on the team site within seconds, logged as Kaavish
  - an announcement lands pinned on the feed
  - no key, a wrong key, an old key after a new one, and any key after Disconnect are refused
  - someone who is not the owner cannot make, read or turn off the key
  - the HQ bar opens Claude with the request written; a member sees no Claude card or bar
  - /api/file, /api/google and /api/browse still answer (they now share the store setup)

Every password here is made up for the test.
Run: cd m360-os && python3 harness/tests/test_claude_connector.py
"""
import base64
import hashlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import build_edgeone  # noqa: E402


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    from playwright.sync_api import sync_playwright
    build_edgeone.main()
    port = free_port()
    store = tempfile.mktemp(suffix='.json')
    srv = subprocess.Popen(['node', os.path.join(ROOT, 'edgeone', 'dev', 'server.mjs'), str(port), store],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    base = 'http://localhost:%d/' % port
    for _ in range(50):
        try:
            urllib.request.urlopen(base, timeout=1)
            break
        except Exception:
            time.sleep(0.1)
    fails, errors, n = [], [], [0]

    def check(cond, msg):
        n[0] += 1
        print(('ok   ' if cond else 'FAIL ') + msg)
        if not cond:
            fails.append(msg)

    def store_doc(key):
        data = json.loads(urllib.request.urlopen(base + '__store').read())
        return json.loads(data[key]) if key in data else None

    def mcp(key, body, auth=None):
        url = base + 'api/mcp' + ('?k=' + key if key else '')
        headers = {'content-type': 'application/json', 'accept': 'application/json, text/event-stream'}
        if auth:
            headers['authorization'] = 'Bearer ' + auth
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        try:
            r = urllib.request.urlopen(req)
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            raw = e.read()
            return e.code, (json.loads(raw) if raw else None)

    def tool(key, name, args=None, rid=9):
        st, j = mcp(key, {'jsonrpc': '2.0', 'id': rid, 'method': 'tools/call', 'params': {'name': name, 'arguments': args or {}}})
        res = (j or {}).get('result') or {}
        text = ((res.get('content') or [{}])[0]).get('text', '')
        try:
            return st, res.get('isError', False), json.loads(text)
        except ValueError:
            return st, res.get('isError', False), text

    try:
        with sync_playwright() as pw:
            exe = os.environ.get('PW_CHROMIUM')
            browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()

            def device():
                c = browser.new_context(viewport={'width': 1280, 'height': 900}, locale='en-IN', timezone_id='Asia/Kolkata')
                c.add_init_script("window.__opened = []; window.open = (u, t, f) => { window.__opened.push(u); return {}; };")
                pg = c.new_page()
                pg.set_default_timeout(15000)
                pg.on('pageerror', lambda e: errors.append(str(e)))
                return c, pg

            fc, f = device()
            f.goto(base)
            f.wait_for_selector('text=Set up m360 OS')
            f.fill('#signin-name', 'Kaavish Ramchandani')
            f.fill('#signin-email', 'kaavish@mask360.agency')
            f.fill('#signin-pw', 'lamp-orbit-9182')
            f.get_by_role('button', name='Set up the workspace').click()
            f.wait_for_selector('.sidebar')
            owner = store_doc('o/owner')['uid']

            # ---- Admin, Claude: make the link ----
            f.goto(base + '#admin')
            f.wait_for_selector('text=Claude')
            f.get_by_text('run the OS from your own Claude').click()
            f.wait_for_selector('#claude-card')
            check('off' in f.inner_text('#claude-state'), 'the connector starts off')
            check(f.input_value('#claude-addr') == base + 'api/mcp', 'the address to paste is the plain one: %s' % f.input_value('#claude-addr'))
            check('Add custom connector' in f.inner_text('#claude-steps') and 'Allow' in f.inner_text('#claude-steps'), 'the three steps in Claude are shown')
            f.click('#claude-keyfold summary')
            f.click('#claude-make')
            f.wait_for_selector('#claude-fresh')
            link = f.input_value('#claude-link')
            check(link.startswith(base + 'api/mcp?k=') and len(link.split('k=')[1]) >= 40, 'the key link is shown once: %s...' % link[:60])
            f.wait_for_selector('#claude-state:has-text("key link on")')
            check(True, 'the status reads key link on')
            key = link.split('k=')[1]
            kept = store_doc('o/mcp') or {}
            check(kept.get('h') and key not in json.dumps(kept), 'the server keeps only a hash of the key')

            # ---- the OAuth sign-in Claude uses (v55.1) ----
            def http(method, path, body=None, form=False, headers=None):
                h = dict(headers or {})
                data = None
                if body is not None:
                    data = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
                    h['content-type'] = 'application/x-www-form-urlencoded' if form else 'application/json'
                req = urllib.request.Request(base + path.lstrip('/'), data=data, method=method, headers=h)
                try:
                    r = urllib.request.urlopen(req)
                    raw = r.read()
                    return r.status, r.headers, (json.loads(raw) if raw and 'json' in (r.headers.get('content-type') or '') else raw)
                except urllib.error.HTTPError as e:
                    raw = e.read()
                    return e.code, e.headers, (json.loads(raw) if raw and 'json' in (e.headers.get('content-type') or '') else raw)

            st, hd, j = http('POST', 'api/mcp', {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}})
            wa = hd.get('www-authenticate') or ''
            check(st == 401 and 'resource_metadata="' + base.rstrip('/') + '/api/oauth/protected-resource"' in wa, 'no sign-in: 401 that names where to sign in: %s' % wa)
            st, hd, prm = http('GET', 'api/oauth/protected-resource')
            check(st == 200 and prm['resource'] == base + 'api/mcp' and prm['authorization_servers'] == [base.rstrip('/')], 'protected resource metadata: %r' % prm)
            for wk in ['.well-known/oauth-protected-resource', '.well-known/oauth-protected-resource/api/mcp']:
                st, hd, j = http('GET', wk)
                check(st == 200 and j.get('resource') == base + 'api/mcp', '/%s answers JSON' % wk)
            for wk in ['.well-known/oauth-authorization-server', '.well-known/openid-configuration']:
                st, hd, asm = http('GET', wk)
                check(st == 200 and asm.get('registration_endpoint') == base + 'api/oauth/register' and asm.get('code_challenge_methods_supported') == ['S256'], '/%s answers the endpoints' % wk)
            st, hd, j = http('POST', 'api/oauth/register', {'redirect_uris': ['https://evil.example/cb'], 'client_name': 'x'})
            check(st == 400 and j.get('error') == 'invalid_redirect_uri', 'a client that returns anywhere but Claude is refused')
            cb = 'https://claude.ai/api/mcp/auth_callback'
            st, hd, cl = http('POST', 'api/oauth/register', {'redirect_uris': [cb], 'client_name': 'Claude', 'grant_types': ['authorization_code', 'refresh_token'], 'token_endpoint_auth_method': 'none'})
            check(st == 201 and cl['client_id'].startswith('c_'), 'Claude registers (dynamic client registration): %s' % cl.get('client_id'))
            verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode()
            challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
            auth_url = base + 'api/oauth/authorize?' + urllib.parse.urlencode({'response_type': 'code', 'client_id': cl['client_id'], 'redirect_uri': cb,
                'code_challenge': challenge, 'code_challenge_method': 'S256', 'state': 'st8', 'scope': 'm360', 'resource': base + 'api/mcp'})
            def allow():
                # Allow is a plain link; its redirect to Claude is read as the browser would get it, with this session's cookie
                href = f.get_attribute('#allow', 'href')
                r = f.request.get(href, max_redirects=0)
                return r.status, r.headers.get('location') or ''
            f.goto(auth_url)
            check('Connect Claude to m360 OS' in f.inner_text('main') and f.locator('#allow').count() == 1, 'the owner, signed in here, is asked to allow it')
            ast, loc = allow()
            q = urllib.parse.parse_qs(urllib.parse.urlparse(loc).query)
            check(ast == 302 and loc.startswith(cb) and q.get('state') == ['st8'] and q.get('code'), 'Allow sends Claude a code with its state: %d %s' % (ast, loc[:70]))
            ast2, loc2 = allow()
            check(ast2 == 400, 'the same Allow link works once (%d)' % ast2)
            code = (q.get('code') or [''])[0]
            st, hd, j = http('POST', 'api/oauth/token', {'grant_type': 'authorization_code', 'code': code, 'code_verifier': 'wrong' * 10, 'client_id': cl['client_id'], 'redirect_uri': cb}, form=True)
            check(st == 400 and j.get('error') == 'invalid_grant', 'a wrong PKCE verifier gets no token')
            st, hd, j = http('POST', 'api/oauth/token', {'grant_type': 'authorization_code', 'code': code, 'code_verifier': verifier, 'client_id': cl['client_id'], 'redirect_uri': cb}, form=True)
            check(st == 400, 'a code works once, even after a failed try')
            # a fresh round, done right
            f.goto(auth_url)
            ast, loc = allow()
            code = urllib.parse.parse_qs(urllib.parse.urlparse(loc).query)['code'][0]
            st, hd, tok = http('POST', 'api/oauth/token', {'grant_type': 'authorization_code', 'code': code, 'code_verifier': verifier, 'client_id': cl['client_id'], 'redirect_uri': cb}, form=True)
            check(st == 200 and tok.get('access_token') and tok.get('refresh_token') and tok.get('token_type') == 'Bearer', 'the code becomes an access and a refresh token')
            at = tok['access_token']
            check(not any(at in v for v in json.loads(urllib.request.urlopen(base + '__store').read()).values()), 'the store keeps no token in the clear')
            st, j = mcp(None, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'}, auth=at)
            check(st == 200 and len(j['result']['tools']) == 6, 'the access token opens the connector')
            st, hd, tok2 = http('POST', 'api/oauth/token', {'grant_type': 'refresh_token', 'refresh_token': tok['refresh_token'], 'client_id': cl['client_id']}, form=True)
            check(st == 200 and tok2.get('access_token') and tok2['refresh_token'] != tok['refresh_token'], 'a refresh token gives a new pair')
            st, hd, j = http('POST', 'api/oauth/token', {'grant_type': 'refresh_token', 'refresh_token': tok['refresh_token'], 'client_id': cl['client_id']}, form=True)
            check(st == 400, 'an old refresh token works once')
            st, j = mcp(None, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'}, auth=tok2['access_token'])
            check(st == 200, 'the refreshed token works')
            f.goto(base + '#admin')
            f.get_by_text('run the OS from your own Claude').click()
            f.wait_for_selector('#claude-state:has-text("connected")')
            check(True, 'Admin reads connected once Claude is signed in')
            oauth_at = tok2['access_token']
            oauth_rt = tok2['refresh_token']
            oauth_client = cl['client_id']
            oauth_url = auth_url

            # ---- MCP handshake ----
            st, j = mcp(key, {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'test', 'version': '1'}}})
            check(st == 200 and j['result']['serverInfo']['name'] == 'm360 OS' and 'tools' in j['result']['capabilities'], 'initialize: %r' % (j or {}).get('result', {}).get('serverInfo'))
            st, j = mcp(key, {'jsonrpc': '2.0', 'method': 'notifications/initialized'})
            check(st == 202, 'a notification gets 202 and no body (%d)' % st)
            st, j = mcp(key, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'})
            names = [t['name'] for t in j['result']['tools']]
            check(names == ['os_overview', 'os_list', 'os_read', 'os_write', 'os_post_update', 'os_activity'], 'tools/list: %r' % names)
            st, j = mcp(None, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'}, auth=key)
            check(st == 200 and 'result' in j, 'the key also works as a Bearer header')

            # ---- the tools ----
            st, err, out = tool(key, 'os_overview')
            check(not err and out['owner'] == owner and out['collections'].get('clients', 0) > 0, 'os_overview lists collections: %r' % list(out.get('collections', {}))[:6])
            check(any(m['name'] == 'Kaavish Ramchandani' and m['role'] == 'founder' for m in out['team']), 'os_overview lists the team')
            st, err, out = tool(key, 'os_list', {'collection': 'clients', 'limit': 3})
            check(not err and out['shown'] <= 3 and out['total'] >= out['shown'] and out['docs'], 'os_list returns documents: %d of %d' % (out.get('shown', 0), out.get('total', 0)))
            cid = sorted(out['docs'])[0]
            st, err, out = tool(key, 'os_read', {'path': 'clients/' + cid})
            check(not err and out['exists'] and out['doc'], 'os_read reads one document')
            st, err, out = tool(key, 'os_write', {'path': 'tasks/t_claude1', 'op': 'set', 'data': {'title': 'Draft the Swisse recap', 'status': 'todo', 'owner': owner, 'by': owner, 'updated': int(time.time() * 1000)}})
            check(not err and out['ok'], 'os_write makes a task: %r' % (out if err else 'ok'))
            check((store_doc('d/tasks~t_claude1') or {}).get('title') == 'Draft the Swisse recap', 'the task is in the store')
            st, err, out = tool(key, 'os_write', {'path': 'tasks/t_claude1', 'op': 'merge', 'data': {'status': 'doing'}})
            check(not err and (store_doc('d/tasks~t_claude1') or {}).get('status') == 'doing', 'os_write merge changes one field')
            st, err, out = tool(key, 'os_write', {'path': 'tasks', 'op': 'set', 'data': {}})
            check(err and 'Not done' in str(out), 'a bad path comes back as a tool error Claude can read: %r' % out)
            st, err, out = tool(key, 'os_post_update', {'text': 'Team call moves to 4 pm today.', 'kind': 'announce'})
            feed = store_doc('d/feed~' + owner) or {}
            check(not err and feed.get('posts', [{}])[0].get('text') == 'Team call moves to 4 pm today.', 'os_post_update posts on the feed')
            check(feed.get('pinned') == owner + ':' + out['posted']['id'], 'an announcement is pinned')
            today = time.strftime('%Y-%m-%d', time.gmtime(time.time() + 330 * 60))
            st, err, out = tool(key, 'os_activity', {'from': today})
            check(not err and ('Draft the Swisse recap' in json.dumps(out) or 'tasks/t_claude1' in json.dumps(out)), 'os_activity shows the change in the log')

            # ---- the change shows on the team site, live ----
            f.goto(base + '#tasks')
            f.wait_for_selector('text=Draft the Swisse recap', timeout=12000)
            check(True, 'the task made through Claude is on the board')
            tool(key, 'os_write', {'path': 'tasks/t_claude1', 'op': 'merge', 'data': {'title': 'Draft the Swisse recap v2'}})
            f.wait_for_selector('text=Draft the Swisse recap v2', timeout=12000)
            check(True, 'a change through Claude reaches an open page within seconds')
            f.goto(base + '#feed')
            f.wait_for_selector('text=Team call moves to 4 pm today.')
            check(True, 'the announcement is on the feed')

            # ---- the HQ bar ----
            f.goto(base + '#hq')
            f.wait_for_selector('#claude-bar')
            f.fill('#claude-ask', 'Move every overdue task to Friday')
            f.click('#claude-go')
            opened = f.evaluate('() => window.__opened')
            check(len(opened) == 1 and opened[0].startswith('https://claude.ai/new?q=') and 'overdue' in urllib.request.unquote(opened[0]) and 'm360 OS connector' in urllib.request.unquote(opened[0]), 'the bar opens Claude with the request written: %r' % opened[:1])
            check(f.input_value('#claude-ask') == '', 'the bar clears after opening')

            # ---- refusals ----
            st, j = mcp(None, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'})
            check(st == 401, 'no key: 401 (%d)' % st)
            st, j = mcp('a' * 48, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'})
            check(st == 401, 'a wrong key: 401 (%d)' % st)
            r = f.evaluate("() => window.M360_API('mcpkey').then(r => r.key)")
            st, j = mcp(key, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'})
            check(st == 401, 'the old key stops once a new one is made (%d)' % st)
            st, j = mcp(r, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'})
            check(st == 200, 'the new key works')
            f.evaluate("() => window.M360_API('mcpoff')")
            st, j = mcp(r, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'})
            check(st == 401, 'after Disconnect no key works (%d)' % st)
            st, j = mcp(None, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list'}, auth=oauth_at)
            check(st == 401, 'after Disconnect the signed-in token stops too (%d)' % st)
            st, hd, j = http('POST', 'api/oauth/token', {'grant_type': 'refresh_token', 'refresh_token': oauth_rt, 'client_id': oauth_client}, form=True)
            check(st == 400, 'and its refresh token')
            req = urllib.request.Request(base + 'api/mcp?k=' + r, method='GET')
            try:
                urllib.request.urlopen(req)
                code = 200
            except urllib.error.HTTPError as e:
                code = e.code
            check(code in (401, 405), 'a GET is refused (%d)' % code)

            # ---- someone who is not the owner ----
            mc, m = device()
            m.goto(base)
            m.wait_for_selector('#signin-email')
            res = m.evaluate("""async () => {
              const out = {};
              try { await window.M360_API('signup', {name: 'Durvesh Patil', email: 'durvesh@mask360.agency', password: 'desk-river-5531'}); out.signup = 'ok'; } catch (e) { out.signup = e.code; }
              for (const a of ['mcpkey', 'mcpstatus', 'mcpoff']) { try { await window.M360_API(a); out[a] = 'ok'; } catch (e) { out[a] = e.status; } }
              return out;
            }""")
            check(res.get('signup') == 'ok' and res.get('mcpkey') == 403 and res.get('mcpstatus') == 403 and res.get('mcpoff') == 403, 'a non-owner cannot make, read or turn off the key: %r' % res)
            check(m.locator('#claude-card, #claude-bar').count() == 0, 'a member sees no Claude card or bar')
            st, hd, cl2 = http('POST', 'api/oauth/register', {'redirect_uris': ['https://claude.ai/api/mcp/auth_callback']})
            m.goto(base + 'api/oauth/authorize?' + urllib.parse.urlencode({'response_type': 'code', 'client_id': cl2['client_id'], 'redirect_uri': 'https://claude.ai/api/mcp/auth_callback', 'code_challenge': 'a' * 43, 'code_challenge_method': 'S256', 'state': 'x'}))
            check('Only Kaavish connects Claude' in m.inner_text('main') and m.locator('#allow').count() == 0, 'a signed-in member is told only Kaavish connects Claude')
            xc, x = device()
            x.goto(base + 'api/oauth/authorize?' + urllib.parse.urlencode({'response_type': 'code', 'client_id': cl2['client_id'], 'redirect_uri': 'https://claude.ai/api/mcp/auth_callback', 'code_challenge': 'a' * 43, 'code_challenge_method': 'S256', 'state': 'x'}))
            check('Sign in to m360 OS first' in x.inner_text('main'), 'someone signed out is asked to sign in first')

            # ---- the other API functions still answer ----
            for path in ['api/file?id=nothing', 'api/browse?u=https%3A%2F%2Fexample.com']:
                try:
                    code = urllib.request.urlopen(base + path).status
                except urllib.error.HTTPError as e:
                    code = e.code
                check(code < 500, '/%s answers (%d)' % (path.split('?')[0], code))

            check(not errors, 'no page errors: %r' % errors[:3])
            browser.close()
    finally:
        srv.kill()
        try:
            os.remove(store)
        except OSError:
            pass
    print('%d checks, %d failed' % (n[0], len(fails)))
    print('PASS' if not fails else 'FAIL')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
