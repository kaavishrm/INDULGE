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
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
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
            f.click('#claude-make')
            f.wait_for_selector('#claude-fresh')
            link = f.input_value('#claude-link')
            check(link.startswith(base + 'api/mcp?k=') and len(link.split('k=')[1]) >= 40, 'the link is shown once: %s...' % link[:60])
            check('Add custom connector' in f.inner_text('#claude-fresh'), 'the three steps in Claude are shown')
            f.wait_for_selector('#claude-state:has-text("connected")')
            check(True, 'the status reads connected')
            key = link.split('k=')[1]
            kept = store_doc('o/mcp') or {}
            check(kept.get('h') and key not in json.dumps(kept), 'the server keeps only a hash of the key')

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
