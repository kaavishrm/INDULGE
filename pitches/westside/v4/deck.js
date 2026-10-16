(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const total = slides.length;
  let cur = 0;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const io = new IntersectionObserver(es => {
    es.forEach(e => { if (e.isIntersecting) cur = slides.indexOf(e.target); });
  }, { threshold: 0.55 });
  slides.forEach(s => io.observe(s));
  const go = i => slides[Math.max(0, Math.min(total - 1, i))].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });

  addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    const t = e.target;
    if (t.closest && t.closest('video, input, textarea, select, button, [contenteditable]')) return;
    const k = e.key;
    if (k === 'ArrowDown' || k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) { e.preventDefault(); go(cur + 1); }
    else if (k === 'ArrowUp' || k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(total - 1); }
  });

  // reference videos: nothing loads until someone presses play; one plays at a time
  const vids = [...document.querySelectorAll('.vbox video')];
  document.querySelectorAll('.vbox .vplay').forEach(b => {
    b.addEventListener('click', () => {
      const box = b.closest('.vbox');
      const v = box.querySelector('video');
      box.classList.add('on');
      v.controls = true;
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
      v.focus({ preventScroll: true });
    });
  });
  vids.forEach(v => v.addEventListener('play', () => vids.forEach(o => { if (o !== v && !o.paused) o.pause(); })));

  if (location.hash) {
    const el = document.getElementById(location.hash.slice(1));
    if (el) el.scrollIntoView({ block: 'start' });
  }
})();
