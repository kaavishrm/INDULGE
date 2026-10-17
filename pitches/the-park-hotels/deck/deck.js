(() => {
  const root = document.documentElement;
  const slides = [...document.querySelectorAll('.slide')];
  const total = slides.length;
  let cur = 0;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // phones and portrait windows read the slides as one scrolling document (deck.css); keep this query in step with its screen query
  const doc = matchMedia('(max-width:760px),(max-aspect-ratio:4/5)');
  const fine = matchMedia('(hover:hover) and (pointer:fine)');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  if (!reduce) root.classList.add('motion');

  const io = new IntersectionObserver(es => {
    es.forEach(e => { if (e.isIntersecting) cur = slides.indexOf(e.target); });
  }, { threshold: 0.55 });
  slides.forEach(s => io.observe(s));

  /* ---------- smooth scroll, the way Hanza's Lenis moves ----------
     Wheel input eases toward its target at the rate measured on Hanza (about 0.08 a frame at 60 Hz, frame-rate independent:
     one wheel tick settles in about a second, 80% of it in the first 400 ms). On the 16:9 slides one flick
     glides to the next slide on Lenis's own curve (1.2 s, exponential ease out) and the rest of that flick is swallowed, so
     a trackpad's inertia cannot run on past it. Touch keeps the browser's own scrolling. */
  const smooth = () => !reduce && fine.matches;
  const syncClass = () => root.classList.toggle('smooth', smooth());
  syncClass();
  fine.addEventListener('change', syncClass);
  let target = scrollY, pos = scrollY, raf = 0, last = 0, tween = null;
  const maxY = () => root.scrollHeight - innerHeight;
  const topOf = s => s.offsetTop;
  const ease = t => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
  function frame(t) {
    const dt = last ? Math.min(64, t - last) : 16.7;
    last = t;
    if (tween) {
      const k = clamp((t - tween.t0) / tween.dur, 0, 1);
      pos = tween.from + (tween.to - tween.from) * ease(k);
      if (k >= 1) { pos = tween.to; tween = null; }
      target = pos;
    } else {
      pos += (target - pos) * (1 - Math.exp(-dt * 0.005));
      if (Math.abs(target - pos) < 0.4) pos = target;
    }
    scrollTo(0, pos);
    if (tween || pos !== target) raf = requestAnimationFrame(frame);
    else { raf = 0; last = 0; }
  }
  const run = () => { if (!raf) raf = requestAnimationFrame(frame); };
  function glideTo(y, dur = 1200) {
    y = clamp(y, 0, maxY());
    if (!smooth()) { scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); return; }
    tween = { from: scrollY, to: y, t0: performance.now(), dur };
    pos = scrollY;
    run();
  }
  // the scroll bar, find in page, touch and the browser's own keys move the page without us: follow them
  addEventListener('scroll', () => { if (!raf) target = pos = scrollY; }, { passive: true });
  addEventListener('resize', () => { if (!raf) target = pos = scrollY; });

  let acc = 0, cool = 0, lastWheel = 0, lastAbs = 0, idle = 0;
  addEventListener('wheel', e => {
    if (!smooth() || open || e.ctrlKey) return;
    e.preventDefault();
    const d = e.deltaMode === 1 ? e.deltaY * 40 : e.deltaMode === 2 ? e.deltaY * innerHeight : e.deltaY;
    const t = performance.now(), abs = Math.abs(d);
    if (doc.matches) { tween = null; target = clamp(target + d, 0, maxY()); run(); return; }
    if (t < cool) {  // the tail of the flick that already moved a slide: let it die away
      if (t - lastWheel < 120 && abs < lastAbs * 0.98) cool = t + 140;
      lastWheel = t; lastAbs = abs;
      return;
    }
    lastWheel = t; lastAbs = abs;
    acc += d;
    if (Math.abs(acc) > 40) { const dir = Math.sign(acc); acc = 0; go(cur + dir); cool = t + 650; return; }
    clearTimeout(idle);
    idle = setTimeout(() => { acc = 0; }, 180);
  }, { passive: false });

  // the next slide is taken from cur, which go() sets at once, so two quick presses move two slides; focus follows, so Tab starts there
  const go = i => { const j = clamp(i, 0, total - 1); cur = j; glideTo(topOf(slides[j])); slides[j].focus({ preventScroll: true }); };

  addEventListener('keydown', e => {
    if (open) { if (e.key === 'Escape') { e.preventDefault(); close(); } else if (e.key === 'PageDown' || e.key === 'PageUp') e.preventDefault(); return; }
    if (doc.matches || e.altKey || e.ctrlKey || e.metaKey) return;
    const t = e.target;
    if (t.closest && (t.closest('video, input, textarea, select, [contenteditable]') || (e.key === ' ' && t.closest('button')))) return;
    const k = e.key;
    if (k === 'ArrowDown' || k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) { e.preventDefault(); go(cur + 1); }
    else if (k === 'ArrowUp' || k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(total - 1); }
  });

  // links inside the deck glide too
  document.addEventListener('click', e => {
    const a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href').length < 2) return;
    const el = document.getElementById(a.getAttribute('href').slice(1));
    if (!el) return;
    e.preventDefault();
    const i = slides.indexOf(el);
    if (i >= 0 && !doc.matches) go(i); else glideTo(el.getBoundingClientRect().top + scrollY);
    history.replaceState(null, '', a.getAttribute('href'));
  });

  /* ---------- reveals, with the settings read from Hanza's own scripts ----------
     Headings rise line by line (opacity 0 to 1, 20 px, 0.8 s, 50 ms a line, from 0.2 s); each page's other blocks fade up in
     order; the column guides draw down; orange rules sweep in; progress squares light one by one; numbers count up; the
     mind maps draw their lines. They replay when a page comes back. On phones each block reveals as it scrolls into view.
     Nothing is hidden unless this script runs, and a failsafe shows everything if it stops part way. */
  const BLOCKS = ['.lab', '.lede-s', '.lede', '.q', '.card', '.post-card', '.vcard', '.acc>div', '.tbl thead', '.tbl tbody tr', '.kv', '.pic',
    '.phone', '.post', '.map', '.cal', '.srcs>div', '.cta', '.mail', '.svc li', '.pages li', '.chap .inset', '.chap>.mono', '.who',
    '.giant', '.nav li', '.spec>div', '.m-logo', '.art.phones', '.rule-plan', '.top>*', '.stack>.mono', '.checks li', '.close .g4>.wm',
    '.cal-key', '.idea-body>p'].join(',');
  const HEADS = '.h1,.h-display,.ct,.idea-name,.cta .h2';
  function splitWords(h) {
    let n = 0;
    const walk = node => {
      [...node.childNodes].forEach(c => {
        if (c.nodeType === 3) {
          const parts = c.textContent.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          parts.forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
            const o = document.createElement('span'); o.className = 'wd';
            const i = document.createElement('span'); i.className = 'wi'; i.textContent = p;
            i.style.setProperty('--w', n++);
            o.appendChild(i); frag.appendChild(o);
          });
          c.replaceWith(frag);
        } else if (c.nodeType === 1) walk(c);
      });
    };
    walk(h);
  }
  const heads = [];
  // each word learns which line it sits on, so a heading rises line by line (and again after a resize reflows it)
  const lineUp = () => heads.forEach(h => {
    let top = null, l = -1;
    h.querySelectorAll('.wi').forEach(w => { const t = Math.round(w.offsetTop); if (top === null || Math.abs(t - top) > 4) { top = t; l++; } w.style.setProperty('--l', l); });
  });
  if (!reduce) {
    slides.forEach(s => {
      const body = s.querySelector('.body');
      if (!body) return;
      body.querySelectorAll(HEADS).forEach(h => { splitWords(h); h.classList.add('rh'); heads.push(h); });
      const els = [...body.querySelectorAll(BLOCKS + ',' + HEADS)].filter((el, _, all) => !all.some(o => o !== el && o.contains(el)));
      els.forEach((el, i) => { el.classList.add(el.matches(HEADS) ? 'rh' : 'rv'); el.style.setProperty('--d', Math.min(i * 70, 980) + 'ms'); });
    });
  }

  lineUp();
  let lt;
  addEventListener('resize', () => { clearTimeout(lt); lt = setTimeout(lineUp, 200); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(lineUp);

  // numbers count up when they come into view (years and labels stay as they are)
  const counters = [...document.querySelectorAll('.big')].filter(el => /^\d{1,4}(%|×|\+)?$/.test(el.textContent.trim()) && !/^(19|20)\d\d$/.test(el.textContent.trim()));
  function count(el) {
    if (el.dataset.done) return;
    el.dataset.done = 1;
    const m = el.textContent.trim().match(/^(\d+)(.*)$/), to = +m[1], suf = m[2];
    if (reduce) return;
    const t0 = performance.now(), dur = 1400;
    const step = t => { const k = clamp((t - t0) / dur, 0, 1); el.textContent = Math.round(to * ease(k)) + suf; if (k < 1) requestAnimationFrame(step); };
    el.textContent = '0' + suf;
    requestAnimationFrame(step);
  }

  // the mind maps draw their lines, then their words
  function drawMap(svg) {
    if (svg.dataset.drawn || reduce || !svg.getBoundingClientRect().width) return;
    svg.dataset.drawn = 1;
    const lines = [...svg.querySelectorAll('path, line')];
    lines.forEach((p, i) => {
      let len = 0;
      try { len = p.getTotalLength ? p.getTotalLength() : 0; } catch (e) {}
      if (!len) return;
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
      p.getBoundingClientRect();
      p.style.transition = `stroke-dashoffset 1.1s cubic-bezier(.65,0,.35,1) ${200 + i * 18}ms`;
      p.style.strokeDashoffset = 0;
    });
    [...svg.querySelectorAll('text, rect, circle')].forEach((t, i) => { t.style.animationDelay = 500 + Math.min(i * 6, 900) + 'ms'; });
    svg.classList.add('drawn');
  }

  function reveal(s) {
    if (s.classList.contains('in')) return;
    s.classList.add('in');
    s.querySelectorAll('.map svg').forEach(drawMap);
  }
  const rio = new IntersectionObserver(es => es.forEach(e => {
    const s = e.target;
    if (doc.matches) { if (e.isIntersecting) s.classList.add('in-doc'); return; }
    if (e.intersectionRatio >= 0.3) reveal(s);
    else if (!e.isIntersecting) s.classList.remove('in');  // off screen: ready to play again
  }), { threshold: [0, 0.3] });
  slides.forEach(s => rio.observe(s));
  // phones: each block reveals on its own as it scrolls in
  let batch = 0, bt = 0;
  const eio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting || !doc.matches) return;
    e.target.style.setProperty('--d', (batch++ % 6) * 70 + 'ms');
    clearTimeout(bt); bt = setTimeout(() => { batch = 0; }, 120);
    e.target.classList.add('in-el');
    eio.unobserve(e.target);
  }), { rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.rv, .rh').forEach(el => eio.observe(el));
  const nio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { count(e.target); nio.unobserve(e.target); } }), { threshold: 0.6 });
  counters.forEach(el => nio.observe(el));
  const mio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) drawMap(e.target); }), { threshold: 0.2 });
  document.querySelectorAll('.map svg').forEach(svg => mio.observe(svg));
  addEventListener('beforeprint', () => { slides.forEach(s => s.classList.add('in')); counters.forEach(el => { el.dataset.done = 1; }); });
  // failsafe: if nothing has revealed after four seconds, show everything
  setTimeout(() => { if (root.classList.contains('motion') && !document.querySelector('.slide.in, .slide.in-doc, .in-el')) root.classList.remove('motion'); }, 4000);

  /* ---------- scroll-linked motion, as Hanza's transform effects ----------
     As a page leaves, its cloth drifts down, grows to 1.2 and fades to half (Hanza's hero); as a page arrives, its columns
     of cards trail behind and meet as it lands (Hanza's stat columns, which start 100 and 250 px low). */
  let sr = 0;
  const link = () => {
    sr = 0;
    if (reduce || doc.matches) return;
    const vh = innerHeight, y = scrollY;
    slides.forEach(s => {
      const p = (s.offsetTop - y) / vh;
      if (p > 1.3 || p < -1.3) return;
      s.style.setProperty('--pa', clamp(p, 0, 1).toFixed(4));
      s.style.setProperty('--pl', clamp(-p, 0, 1).toFixed(4));
    });
  };
  addEventListener('scroll', () => { if (!sr) sr = requestAnimationFrame(link); }, { passive: true });
  link();

  // the cover's clock: Kolkata time, the way Hanza shows its local time
  const clock = document.querySelector('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit' });
    const tickClock = () => { clock.textContent = fmt.format(new Date()); };
    tickClock();
    setInterval(tickClock, 15000);
  }

  // reference videos: nothing loads until someone presses play. Play opens the clip large, over the deck, with the browser's own
  // controls (play, sound, volume, full screen); Esc, the close button or a click outside puts it back on its slide.
  const vids = [...document.querySelectorAll('.vbox video')];
  let lb = null, open = null;
  function close() {
    if (!open) return;
    const { v, box } = open;
    open = null;
    v.pause();
    v.controls = false;
    box.insertBefore(v, box.firstChild);
    lb.classList.remove('on');
    setTimeout(() => { if (!open) lb.hidden = true; }, reduce ? 0 : 320);  // after the fade
    root.classList.remove('lb-open');
    document.querySelector('main').inert = false;
    const b = box.querySelector('.vplay');
    if (b) b.focus({ preventScroll: true });
  }
  function build() {
    lb = document.createElement('div');
    lb.className = 'vlight';
    lb.hidden = true;
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Reference clip');
    lb.innerHTML = '<div class="vl-stage"></div><p class="vl-cap"></p><button class="vl-x" type="button"><span>Close</span><i aria-hidden="true">×</i></button>';
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    lb.querySelector('.vl-x').addEventListener('click', close);
    document.body.appendChild(lb);
  }
  document.querySelectorAll('.vbox .vplay').forEach(b => {
    b.addEventListener('click', () => {
      if (!lb) build();
      if (open) close();
      const box = b.closest('.vbox');
      const v = box.querySelector('video');
      open = { v, box };
      const stage = lb.querySelector('.vl-stage');
      stage.style.setProperty('--ar', box.style.getPropertyValue('--ar') || '9/16');
      stage.appendChild(v);
      lb.querySelector('.vl-cap').textContent = v.getAttribute('aria-label') || '';
      v.controls = true;
      lb.hidden = false;
      requestAnimationFrame(() => lb.classList.add('on'));
      root.classList.add('lb-open');
      document.querySelector('main').inert = true;  // keeps Tab inside the clip while it is open
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
      v.focus({ preventScroll: true });
    });
  });
  vids.forEach(v => v.addEventListener('webkitendfullscreen', close));
  // the browser's seek bar keeps Esc to itself; hand focus back to the clip after a seek or a volume change
  vids.forEach(v => ['seeked', 'volumechange'].forEach(t => v.addEventListener(t, () => { if (open) v.focus({ preventScroll: true }); })));

  // cloth: each canvas is painted (fabric.js) when it comes near the screen, and again when its size changes
  const fabs = [...document.querySelectorAll('canvas[data-fab]')];
  const paint = (cv, force) => { try { Fabric.draw(cv, cv.dataset.fab, +cv.dataset.seed || 1, undefined, force); } catch (e) {} };
  const fio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) paint(e.target); }), { rootMargin: '100% 0px' });
  fabs.forEach(c => fio.observe(c));
  let rt;
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => fabs.forEach(c => { fio.unobserve(c); fio.observe(c); }), 150); });
  addEventListener('beforeprint', () => fabs.forEach(c => paint(c, true)));

  // the statement: its words turn from grey to ink, one after another, when the page arrives (Hanza's scroll reveal)
  document.querySelectorAll('.q').forEach(q => q.querySelectorAll('.w').forEach((w, i) => { w.style.transitionDelay = reduce ? '0ms' : 400 + i * 70 + 'ms'; }));
  const qio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); qio.unobserve(e.target); } }), { threshold: 0.6 });
  document.querySelectorAll('.q').forEach(q => qio.observe(q));
  addEventListener('beforeprint', () => document.querySelectorAll('.q').forEach(q => q.classList.add('on')));

  if (location.hash) {
    const el = document.getElementById(location.hash.slice(1));
    if (el) { el.scrollIntoView({ block: 'start' }); target = pos = scrollY; }
  }
})();
