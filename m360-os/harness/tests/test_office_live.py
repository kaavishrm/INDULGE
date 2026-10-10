#!/usr/bin/env python3
"""v35 test: Kaavish live in the office (spec part M, the live channel of part F).

The founder's page and the members' pages share ONE browser context, so they meet in the mock room
(harness/mock.js: a BroadcastChannel that carries merged presence with by, the sender's id). The office is forced
to 3D under SwiftShader, the page clock moved to test_office.py's working Tuesday with travel(). Latencies are
read from each page's own performance clock (timeOrigin plus now), never from Date. Checks:
- a founder walk reaches a member's page: M.officeLive there says 'walk' within 1.5 s of his click, and the
  member's scene then draws him at the desk he went to;
- "Morning, team" said from the composer shows as .office-say on the member's page, and its screen reader line;
- a member drawn flat (the pref) shows .office-founder data-live="1" on the floor, moved off the cabin, and his
  bubble;
- a member's M.officeLive.walkTo and say return false and put nothing in presence;
- peers with by null are ignored, and so is a page that names itself the founder (presence uid); the same message
  sent with his id is believed, so the room really carried it;
- the founder leaving #office: the member sees him seated in the cabin within 2 s, and the flat page puts him back;
- a member's page says it watches (o3w) while the office is open; no console errors.

Run: cd m360-os && python3 harness/tests/test_office_live.py
"""
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from harness.lib import run, FORCE_3D, travel, office_world  # noqa: E402

IST = ZoneInfo('Asia/Kolkata')
F, M1, M2, M4 = 'u_founder', 'u_m1', 'u_m2', 'u_m4'
SHOTS = os.environ.get('COO_SHOTS') or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shots', 'office3d')
READY = '.office[data-render="3d"][data-office3d="ready"]'
SAID = 'Morning, team'
NOW = 'performance.timeOrigin + performance.now()'
PAGE_FLAT = '''(() => { const gi = Storage.prototype.getItem;
  Storage.prototype.getItem = function (k) { return k === 'm360.office.mode' ? 'flat' : gi.call(this, k); }; })();'''
# what the member's page believes, sampled every 50 ms with the page's own clock
WATCH = '''() => { window.__seen = []; clearInterval(window.__watch); window.__watch = setInterval(() => { const s = M.officeLive.state();
  window.__seen.push({t: %s, mode: s.mode, x: s.x, y: s.y, seq: s.seq, live: s.live}); if (window.__seen.length > 4000) window.__seen.shift(); }, 50); }''' % NOW


def test(h):
    checks = []

    def check(cond, msg):
        if not cond:
            raise AssertionError(msg)
        checks.append(msg)

    real = datetime.now(IST)
    tue = (real + timedelta(days=(1 - real.weekday()) % 7 + 7)).date()
    os.makedirs(SHOTS, exist_ok=True)
    c = h.context(init=[FORCE_3D, travel(datetime(tue.year, tue.month, tue.day, 11, 16, tzinfo=IST))])
    f = h.page(c)
    office_world(h, f, tue)

    def until(p, js, msg, arg=None, timeout=10000, polling=200):
        """wait for js to hold in the page; a wait that runs out fails with what it was waiting for"""
        try:
            p.wait_for_function(js, arg=arg, timeout=timeout, polling=polling)
        except Exception:
            raise AssertionError(msg)

    def office(p, ident):
        p.goto(h.url(ident, '#office'))
        h.ready(p)
        until(p, 's => !!document.querySelector(s)', '%s: #office never drew in 3D' % ident, arg=READY, timeout=30000)

    def settle(p):
        """nothing moving on that page's scene, and no frame drawn for 1.5 s"""
        p.wait_for_function('''() => { const s = M.office3d.state(), w = window.__o3w || (window.__o3w = {f: -1, at: 0});
          if (s.frames !== w.f) { w.f = s.frames; w.at = performance.now(); }
          return s.ready && !s.building && !s.moving && performance.now() - w.at > 1500; }''', timeout=60000, polling=250)

    def into_view(p):
        p.evaluate('() => document.querySelector(".office").scrollIntoView({block: "start"})')

    def out_of_view(p):
        """the founder's own scene stops drawing (off screen): one software renderer serves both pages, and the
        member's frames are the ones being measured"""
        p.evaluate('''() => { let s = document.getElementById('o3-spacer'); if (!s) { s = document.createElement('div'); s.id = 'o3-spacer'; s.style.height = '3000px'; document.body.appendChild(s); }
          window.scrollTo(0, document.body.scrollHeight); }''')
        until(p, '() => M.office3d.state().paused', 'the founder\'s scene never paused off screen', timeout=20000, polling=100)

    office(f, 'founder')
    m = h.page(c)
    office(m, 'm1')
    into_view(m)
    until(m, '() => !M.office3d.state().paused', 'the member\'s scene never came into view', timeout=20000)
    check(m.evaluate('() => M.officeLive.state().role') == 'member' and f.evaluate('() => M.officeLive.state().role') == 'owner', 'one owner page and one member page')
    check(m.evaluate('() => (window.__presence || {}).o3w') == 1, 'the member\'s page says it watches the office (o3w 1)')
    until(m, '() => M.officeLive.state().peers >= 1', 'the member\'s page never heard the founder\'s page in the room', timeout=20000)
    k = m.evaluate('() => M.officeLive.state()')
    check(k['mode'] == 'sit' and (k['x'], k['y']) == (1450, 712), 'before he moves, the member sees him seated in the cabin: %r' % [k['mode'], k['x'], k['y']])

    # ---- his walk to a desk reaches the member within 1.5 s; the member's scene draws him there ----
    out_of_view(f)
    settle(m)
    m.evaluate(WATCH)
    # the moment this page knows: its own listener on the room, created after the mock's, runs its check just after
    # the mock has handed the change to M.officeLive (timers run in order), before any frame is drawn
    m.evaluate('''() => { window.__knew = 0; const bc = new BroadcastChannel('m360room');
      bc.onmessage = e => { const d = e.data || {}; if (d.presence && d.presence.o3) setTimeout(() => { if (!window.__knew && M.officeLive.state().mode === 'walk') window.__knew = %s; }, 0); }; }''' % NOW)
    start = m.evaluate('() => { const s = M.officeLive.state(); return [s.x, s.y]; }')
    end = f.evaluate('u => M.office.standPoint(M.office.layout(M.lastCtx), "desk:" + u)', M4)
    at = f.evaluate('u => { const t = %s; document.querySelector(`.office-desk[data-uid="${u}"]`).click(); return t; }' % NOW, M4)
    until(m, '() => window.__knew > 0', 'the member\'s page never had him walking', timeout=15000, polling=100)
    lag = (m.evaluate('() => window.__knew') - at) / 1000
    check(lag < 1.5, 'the member\'s page has him walking %.2f s after his click' % lag)
    until(m, 'e => { const k = M.office3d.state().kaavish; return Math.abs(k.x - e.x) < 25 && Math.abs(k.y - e.y) < 25 && k.mode !== "walk"; }',
          'the member\'s scene never drew him at the desk he went to', arg=end, timeout=30000)
    mid = m.evaluate('([a, b]) => window.__seen.filter(x => x.mode === "walk" && Math.hypot(x.x - a[0], x.y - a[1]) > 20 && Math.hypot(x.x - b[0], x.y - b[1]) > 20).map(x => [x.x, x.y])', [start, [end['x'], end['y']]])
    check(len(mid) >= 1, 'the member sees him walk the aisle (%r) and stop at the desk %r' % (mid[:4], end))
    until(f, 's => !!document.querySelector(s)', 'DeskDrawer never opened on his arrival', arg='.office-drawer[data-uid="%s"]' % M4, timeout=30000)
    check(m.locator('.scrim').count() == 0, 'the drawer opens on his page only')
    f.keyboard.press('Escape')
    until(f, '() => !document.querySelector(".scrim")', 'the drawer never closed on Escape', timeout=20000)
    m.screenshot(path=os.path.join(SHOTS, 'live-member-walk.png'))

    # ---- his words ----
    f.fill('#office-say', SAID)
    f.press('#office-say', 'Enter')
    until(m, 't => { const e = document.querySelector(".office .office-say"); return !!e && e.textContent.trim() === t; }', 'the member never saw his words as .office-say', arg=SAID, timeout=20000)
    info = m.evaluate('() => { const e = document.querySelector(".office .office-say"); return [e.dataset.who, document.querySelector(".office-sr").textContent]; }')
    check(info[0] == 'kaavish', 'the member sees "%s" as .office-say' % SAID)
    until(m, 't => document.querySelector(".office-sr").textContent === "Kaavish says: " + t', 'the screen reader line never came', arg=SAID, timeout=20000)
    check(True, 'and the screen reader hears "Kaavish says: %s"' % SAID)
    check(m.evaluate('() => document.querySelectorAll(".office .office-bubble[data-who=\\"kaavish\\"]").length') == 0, 'his words are never a COO bubble')

    # ---- a member drawn flat sees him live on the floor, and his bubble ----
    fl = h.page(c)
    fl.add_init_script(PAGE_FLAT)
    fl.goto(h.url('m2', '#office'))
    h.ready(fl)
    until(fl, 's => !!document.querySelector(s)', 'the flat member page never drew the office', arg='.office[data-render="flat"] .office-founder', timeout=30000)
    until(fl, '() => { const b = document.querySelector(".office-founder"); return b.dataset.live === "1" && b.dataset.place === "floor"; }', 'the flat page never showed him live on the floor', timeout=20000)
    until(fl, 't => { const e = document.querySelector(".office .office-say"); return !!e && e.textContent.includes(t); }', 'the flat page never showed his words', arg=SAID, timeout=20000)
    pos = fl.evaluate('''() => { const b = document.querySelector('.office-founder'), r = b.getBoundingClientRect(), s = b.parentElement.getBoundingClientRect();
      return {x: (r.left + r.width / 2 - s.left) / s.width, y: (r.top + r.height / 2 - s.top) / s.height}; }''')
    L = fl.evaluate('() => { const L = M.office.layout(M.lastCtx); return {W: L.W, H: L.H}; }')
    near = abs(pos['x'] - end['x'] / L['W']) < 0.06 and abs(pos['y'] - end['y'] / L['H']) < 0.08
    check(near, 'a flat member page shows .office-founder data-live 1 on the floor at his stand point, and his bubble: %r vs %r' % (pos, (end['x'] / L['W'], end['y'] / L['H'])))
    fl.screenshot(path=os.path.join(SHOTS, 'live-member-flat.png'))

    # ---- a member drives nothing ----
    for p in (m, fl):
        calls = p.evaluate('() => (window.__presenceCalls || []).length')
        r = p.evaluate('() => [M.officeLive.walkTo("desk:u_m2"), M.officeLive.walkTo({x: 600, y: 480}), M.officeLive.say("hello everyone"), M.officeLive.clear()]')
        p.wait_for_timeout(300)
        sent = p.evaluate('n => (window.__presenceCalls || []).slice(n).filter(c => c.patch && ("o3" in c.patch || "say" in c.patch))', calls)
        check(r == [False, False, False, False] and not sent and 'o3' not in (p.evaluate('() => window.__presence || {}') or {}),
              'a member\'s walkTo, say and clear return false and put nothing in presence: %r' % [r, sent])
    check(f.evaluate('() => M.officeLive.state().to') == 'desk:' + M4, 'and Kaavish is still where he went')

    # ---- only his own account is believed ----
    seq = m.evaluate('() => M.officeLive.state().seq')
    fake = {'s': seq + 50, 'm': 'idle', 'x': 300, 'y': 900, 'h': 0, 'to': 'floor', 'lv': 0}
    post = '''([peer, by, presence]) => { const bc = new BroadcastChannel('m360room'); bc.postMessage({t: 'p', peer, by, presence, updatedAt: Date.now()}); bc.close(); }'''
    m.evaluate(post, ['xnull', None, {'uid': F, 'page': 'office', 'o3': fake}])
    m.evaluate(post, ['xself', M2, {'uid': F, 'page': 'office', 'o3': fake}])
    m.wait_for_timeout(1500)
    k = m.evaluate('() => M.officeLive.state()')
    check(k['seq'] == seq and (k['x'], k['y']) != (300, 900), 'a peer with by null, or one naming itself the founder, moves nothing: %r' % [k['seq'], k['x'], k['y']])
    m.evaluate(post, ['xreal', F, {'uid': F, 'page': 'office', 'o3': fake}])
    until(m, 's => M.officeLive.state().seq === s', 'the same message from his own account was not believed, so the room never carried it', arg=fake['s'], polling=100)
    check(True, 'the same message from his own account is believed (seq %d)' % fake['s'])
    m.evaluate('''() => { for (const peer of ['xnull', 'xself', 'xreal']) { const bc = new BroadcastChannel('m360room'); bc.postMessage({t: 'bye', peer}); bc.close(); } }''')
    until(m, 's => M.officeLive.state().seq === s', 'the stand-in peers never left the member\'s page', arg=f.evaluate('() => M.officeLive.state().seq'), timeout=20000, polling=100)

    # ---- he leaves #office: seated in the cabin within 2 s ----
    m.evaluate(WATCH)
    m.evaluate('''() => { window.__sat = 0; const bc = new BroadcastChannel('m360room');
      bc.onmessage = e => { const d = e.data || {}; if (d.t === 'p' || d.t === 'bye') setTimeout(() => { const s = M.officeLive.state();
        if (!window.__sat && s.mode === 'sit' && s.x === 1450 && s.y === 712) window.__sat = %s; }, 0); }; }''' % NOW)
    left = f.evaluate('() => { const t = %s; location.hash = "#home"; return t; }' % NOW)
    until(m, '() => window.__sat > 0', 'the member never saw him back in the cabin after he left #office', timeout=15000, polling=100)
    lag = (m.evaluate('() => window.__sat') - left) / 1000
    check(lag < 2, 'the member sees him seated in the cabin %.2f s after he leaves #office' % lag)
    until(m, '() => { const k = M.office3d.state().kaavish; return k.mode === "sit" && k.x === 1450 && k.y === 712; }', 'the member\'s scene never drew him at his cabin desk', timeout=20000)
    # his words may still show for a while: he is live, and seated at his cabin desk
    until(fl, '() => document.querySelector(".office-founder").dataset.place === "cabin"', 'the flat page never put him back in the cabin')
    check(True, 'the member\'s scene draws him at his cabin desk, and the flat page puts him back in the cabin')
    m.screenshot(path=os.path.join(SHOTS, 'live-member-cabin.png'))
    fl.close()
    m.close()
    check(f.evaluate('() => (window.__presence || {}).o3 === undefined'), 'off #office, his presence carries no walk')

    errs = [e for e in h.errors() if 'AudioContext' not in str(e) and 'play()' not in str(e)]
    check(not errs, 'no console errors: %r' % errs[:3])
    return checks


if __name__ == '__main__':
    out = run(test)
    for c in out:
        print('ok', c)
    print('PASS', len(out), 'checks')
