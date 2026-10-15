/* module: the gate's motion (v36.2). The sign-in and boot screens move the way Apple's do: the m360 mark
   writes itself in from left to right, the title, the line and the form rise into focus one after another
   on a soft spring, a wrong sign-in shakes the box, and the first screen after signing in settles into
   place. Every piece is timed from one start, the moment the static boot screen began to move (its CSS
   animation), so when React swaps that screen for its own, or the boot gate for the sign-in gate, the
   motion carries on where it was and never starts over. A later change (Forgot it?, the code step) rises in fresh. Reduced motion:
   none of it, everything simply shows. The CSS half is src/css/99-gate.css. */
'use strict';
(function () {
  const still = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  const EASE = 'cubic-bezier(.22,1,.36,1)';      /* the curve Apple's sheets settle on */
  const WRITE = {delay: 120, duration: 1600};
  const PEN = 'cubic-bezier(.45,.05,.25,1)';    /* a hand writing: a steady start, an even line, a gentle stop */
  const RISE = [['h1', 520], ['p', 620], ['.g-act', 720]];
  const RISE_MS = 760;
  const FRESH_MS = 460;
  const ENTERED = 'm360.entered';
  const WRITE_KF = [{WebkitMaskPosition: '100% 0', maskPosition: '100% 0'}, {WebkitMaskPosition: '0% 0', maskPosition: '0% 0'}];
  const RISE_KF = [{opacity: 0, transform: 'translateY(12px)', filter: 'blur(8px)'}, {opacity: 1, transform: 'none', filter: 'blur(0px)'}];
  const SHAKE_KF = [{transform: 'translateX(0)'}, {transform: 'translateX(-11px)'}, {transform: 'translateX(9px)'}, {transform: 'translateX(-6px)'},
    {transform: 'translateX(4px)'}, {transform: 'translateX(-2px)'}, {transform: 'translateX(0)'}];
  const ENTER_KF = [{opacity: 0, transform: 'scale(1.012) translateY(6px)', filter: 'blur(6px)'}, {opacity: 1, transform: 'none', filter: 'blur(0px)'}];

  const clock = () => (document.timeline && document.timeline.currentTime) || performance.now();
  const seen = new WeakSet();
  let T0 = null;                       /* when the motion began, on the document timeline */
  const now = () => clock() - (T0 == null ? clock() : T0);

  /* the static boot screen moves by CSS from its first paint: its start is the start of everything */
  function begin(gate) {
    if (T0 != null) return;
    const svg = gate.querySelector('.mark svg');
    const css = svg && svg.getAnimations ? svg.getAnimations()[0] : null;
    T0 = css && css.startTime != null ? css.startTime : clock();
    /* those first elements keep their CSS motion; only what React mounts after them is joined in */
    gate.querySelectorAll('.mark svg, :scope > div > h1, :scope > div > p, :scope > div > .g-act').forEach(el => seen.add(el));
  }

  /* play on that one clock: an element that mounts late joins its motion at the right moment */
  function synced(el, kf, delay, duration, easing) {
    if (!el.animate) return;
    el.style.animation = 'none';
    const a = el.animate(kf, {delay, duration, easing: easing || EASE, fill: 'both'});
    try { a.startTime = T0; } catch (e) { /* an old engine plays it from now */ }
  }
  /* one rise per change: two passes over the same swap (React commits it in steps) never stack two */
  const lastRise = new WeakMap();
  function fresh(el, kf, duration) {
    if (!el.animate) return;
    const t = clock();
    if (t - (lastRise.get(el) || -1e9) < 200) return;
    lastRise.set(el, t);
    el.style.animation = 'none';
    /* what an earlier rise left behind is let go, and this one leaves nothing behind either */
    el.getAnimations().forEach(a => { if (a.playState === 'finished') a.cancel(); });
    el.animate(kf, {duration, easing: EASE});
  }

  function settle(gate) {
    if (still()) return;
    begin(gate);
    const t = now();
    gate.querySelectorAll('.mark svg').forEach(svg => {
      if (seen.has(svg)) return;
      seen.add(svg);
      if (t < WRITE.delay + WRITE.duration) synced(svg, WRITE_KF, WRITE.delay, WRITE.duration, PEN);
      else svg.style.animation = 'none';
    });
    RISE.forEach(([sel, delay]) => gate.querySelectorAll(':scope > div > ' + sel).forEach(el => {
      if (seen.has(el)) return;
      seen.add(el);
      if (t < delay + RISE_MS) synced(el, RISE_KF, delay, RISE_MS);
      else fresh(el, RISE_KF, FRESH_MS);
    }));
  }

  /* what the gate says and asks for: when it changes after the opening, the changed part rises in fresh */
  const sig = gate => {
    const h = gate.querySelector('h1');
    const ids = [...gate.querySelectorAll('.g-act input, .g-act textarea')].map(i => i.id || i.name || i.type).join(',');
    return {h: h ? h.textContent : '', ids};
  };
  let last = null;
  function changed(gate) {
    if (still()) return;
    const s = sig(gate);
    const prev = last;
    last = s;
    if (!prev || now() < 720 + RISE_MS) return;
    if (s.h !== prev.h) { const h = gate.querySelector('h1'); if (h) fresh(h, RISE_KF, FRESH_MS); }
    if (s.ids !== prev.ids) { const b = gate.querySelector('.g-act .join-box') || gate.querySelector('.g-act'); if (b) fresh(b, RISE_KF, FRESH_MS); }
  }

  /* a wrong sign-in, a bad code, a taken email: the box shakes, the way the Mac login does */
  function shake(alert) {
    if (still()) return;
    const box = alert.closest('.join-box') || alert.closest('.g-act');
    if (box && box.animate) box.animate(SHAKE_KF, {duration: 440, easing: 'cubic-bezier(.36,.07,.19,.97)'});
  }

  /* the first screen after signing in settles into place */
  function remember(e) {
    const t = e.target;
    if (!t || !t.closest || !t.closest('.gate')) return;
    const go = e.type === 'click' ? t.closest('.btn') : (e.key === 'Enter' && t.matches('input') ? t : null);
    if (go) try { sessionStorage.setItem(ENTERED, String(Date.now())); } catch (err) { /* private mode: no settle */ }
  }
  document.addEventListener('click', remember, true);
  document.addEventListener('keydown', remember, true);
  let entered = 0;
  try { entered = Number(sessionStorage.getItem(ENTERED)) || 0; } catch (e) { /* keep going */ }
  function arrive(root) {
    if (!entered) return;
    const app = root.querySelector(':scope > .app');
    if (!app) return;
    const fresh15 = Date.now() - entered < 15000;
    entered = 0;
    try { sessionStorage.removeItem(ENTERED); } catch (e) { /* keep going */ }
    if (fresh15 && !still() && app.animate) app.animate(ENTER_KF, {duration: 680, easing: EASE});
  }

  /* once the app itself is up, the gate is done: the watch stops, so a working day costs nothing */
  let obs = null;
  function scan() {
    const root = document.getElementById('root');
    if (!root) return;
    const gate = root.querySelector(':scope > .gate');
    if (gate) { settle(gate); changed(gate); return; }
    if (root.querySelector(':scope > .app')) { arrive(root); if (obs) { obs.disconnect(); obs = null; } }
  }

  function watch() {
    const root = document.getElementById('root');
    if (!root || typeof MutationObserver === 'undefined') return;
    scan();
    if (root.querySelector(':scope > .app')) return;
    obs = new MutationObserver(muts => {
      scan();
      if (!obs) return;
      for (const m of muts) {
        const nodes = m.type === 'characterData' ? [m.target.parentElement] : [...m.addedNodes];
        for (const n of nodes) {
          if (!n || n.nodeType !== 1) continue;
          const a = n.matches('[role="alert"]') ? n : n.querySelector && n.querySelector('[role="alert"]');
          if (a && a.closest('.gate')) shake(a);
        }
      }
    });
    obs.observe(root, {childList: true, subtree: true, characterData: true});
  }
  /* the page carries #root with the static boot screen before its scripts, so the watch starts now, before
     React's first commit replaces that screen */
  if (document.getElementById('root')) watch();
  else document.addEventListener('DOMContentLoaded', watch);

  M.gateMotion = {still, EASE};
})();
