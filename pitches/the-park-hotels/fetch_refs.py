"""Fetches the references for The Park deck: python3 pitches/the-park-hotels/fetch_refs.py site|videos <out-dir>

Runs in GitHub Actions (.github/workflows/park-refs.yml), because the coding sandbox cannot reach framer.website or
Google Drive.
  site    captures the Hanza Framer template (the design reference): full-page screenshots at desktop and phone width,
          each page's text and HTML, the computed type scale, the colours in use and the font files it loads.
  videos  downloads the shared Google Drive folder of video references, re-encodes each one small enough to publish
          with the deck (H.264, faststart, under 12 MB), and writes a poster, a frame strip and manifest.json.
"""
import json, pathlib, re, shutil, subprocess, sys, traceback
from urllib.parse import urlparse, urldefrag

SITE = 'https://hanza-template.framer.website/'
FOLDER = 'https://drive.google.com/drive/folders/1mu2iXzDpEYf1CXChC1UYJkMxSIQBt8D_'
MAX_PAGES = 10
MAX_MB = 12

STYLES_JS = r"""() => {
  const seen = new Map();
  for (const el of document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,a,span,button,li,div')) {
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const s = getComputedStyle(el);
    const key = [s.fontFamily, s.fontSize, s.fontWeight, s.letterSpacing, s.textTransform].join('|');
    const row = seen.get(key) || {fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight,
      lineHeight: s.lineHeight, letterSpacing: s.letterSpacing, textTransform: s.textTransform, color: s.color,
      count: 0, samples: []};
    row.count++;
    if (row.samples.length < 4) row.samples.push(el.textContent.trim().slice(0, 90));
    seen.set(key, row);
  }
  const bg = new Map();
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    const c = getComputedStyle(el).backgroundColor;
    if (r.width * r.height < 20000 || c === 'rgba(0, 0, 0, 0)') continue;
    bg.set(c, (bg.get(c) || 0) + Math.round(r.width * r.height / 1000));
  }
  return {
    body: {background: getComputedStyle(document.body).backgroundColor, color: getComputedStyle(document.body).color},
    type: [...seen.values()].sort((a, b) => parseFloat(b.fontSize) - parseFloat(a.fontSize)),
    backgrounds: [...bg.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20),
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family} ${f.weight} ${f.style}`),
    height: document.documentElement.scrollHeight,
  };
}"""


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60] or 'page'


def scroll_through(page):
    """Framer reveals sections as they scroll into view, so walk the page before the full-page screenshot."""
    y = 0
    while y < page.evaluate('document.documentElement.scrollHeight') and y < 40000:
        page.evaluate(f'window.scrollTo(0, {y})')
        page.wait_for_timeout(260)
        y += 500
    page.wait_for_timeout(800)
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_timeout(1200)


def site(out):
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    (out / 'fonts').mkdir(exist_ok=True)
    host = urlparse(SITE).netloc
    fonts, report = {}, {'pages': []}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        desk = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = desk.new_page()

        def keep_font(resp):
            u = resp.url
            if re.search(r'\.(woff2?|ttf|otf)(\?|$)', u) and u not in fonts:
                try:
                    body = resp.body()
                    name = slug(pathlib.Path(urlparse(u).path).stem) + pathlib.Path(urlparse(u).path).suffix
                    (out / 'fonts' / name).write_bytes(body)
                    fonts[u] = name
                except Exception as e:  # a font that cannot be read should not stop the capture
                    fonts[u] = f'failed: {e}'
        page.on('response', keep_font)

        page.goto(SITE, wait_until='networkidle', timeout=120000)
        links = [SITE]
        for href in page.eval_on_selector_all('a[href]', 'els => els.map(e => e.href)'):
            href = urldefrag(href)[0]
            if urlparse(href).netloc == host and href not in links:
                links.append(href)
        report['links'] = links
        for i, url in enumerate(links[:MAX_PAGES]):
            name = f'{i:02d}-{slug(urlparse(url).path) if urlparse(url).path.strip("/") else "home"}'
            try:
                page.goto(url, wait_until='networkidle', timeout=120000)
                scroll_through(page)
                page.screenshot(path=str(out / f'{name}.jpg'), full_page=True, type='jpeg', quality=72)
                (out / f'{name}.txt').write_text(page.evaluate('document.body.innerText'))
                (out / f'{name}.html').write_text(page.content())
                styles = page.evaluate(STYLES_JS)
                (out / f'{name}.styles.json').write_text(json.dumps(styles, indent=1))
                report['pages'].append({'url': url, 'file': name, 'height': styles['height']})
            except Exception as e:
                report['pages'].append({'url': url, 'file': name, 'error': repr(e)})
        dropped = links[MAX_PAGES:]
        if dropped:
            report['not_captured'] = dropped

        phone = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True,
                                    has_touch=True)
        mp = phone.new_page()
        for i, url in enumerate(links[:3]):
            try:
                mp.goto(url, wait_until='networkidle', timeout=120000)
                scroll_through(mp)
                mp.screenshot(path=str(out / f'phone-{i:02d}.jpg'), full_page=True, type='jpeg', quality=60)
            except Exception as e:
                report.setdefault('phone_errors', []).append(f'{url}: {e!r}')
        browser.close()
    report['fonts'] = fonts
    (out / 'report.json').write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


def probe(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate:format=duration',
                        '-of', 'json', str(f)], capture_output=True, text=True)
    j = json.loads(r.stdout or '{}')
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), {})
    a = any(s.get('codec_type') == 'audio' for s in j.get('streams', []))
    return {'width': v.get('width'), 'height': v.get('height'), 'fps': v.get('r_frame_rate'), 'audio': a,
            'duration': float(j.get('format', {}).get('duration') or 0)}


def videos(out):
    import gdown
    raw = pathlib.Path('raw-videos')
    raw.mkdir(exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'folder': FOLDER, 'files': []}
    try:
        try:
            got = gdown.download_folder(FOLDER, output=str(raw), quiet=False, use_cookies=False)
        except Exception:  # fall back to the command line, which some gdown versions handle differently
            manifest['api_error'] = traceback.format_exc()[-1500:]
            subprocess.run(['gdown', '--folder', FOLDER, '-O', str(raw)], check=False)
            got = [p for p in raw.rglob('*') if p.is_file()]
        manifest['downloaded'] = [str(g) for g in (got or [])]
        if not got:
            manifest['error'] = 'gdown returned nothing: the folder may not be shared as anyone with the link'
    except Exception:
        manifest['error'] = traceback.format_exc()[-2000:]
    for f in sorted(p for p in raw.rglob('*') if p.is_file()):
        row = {'source': str(f.relative_to(raw)), 'bytes': f.stat().st_size}
        name = slug(f.stem)
        info = probe(f)
        row.update(src=info)
        if not info['width'] or info['duration'] < 0.5:
            if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                shutil.copy(f, out / f'{name}{f.suffix.lower()}')
                row['image'] = f'{name}{f.suffix.lower()}'
            manifest['files'].append(row)
            continue
        w, h = info['width'], info['height']
        long_cap = 1280
        short_cap = 720
        if h >= w:
            tw = min(w, short_cap)
            th = round(h * tw / w)
            if th > long_cap:
                th, tw = long_cap, round(w * long_cap / h)
        else:
            tw = min(w, long_cap)
            th = round(h * tw / w)
        tw, th = tw - tw % 2, th - th % 2
        dst = out / f'{name}.mp4'
        for crf in (26, 29, 32, 35):
            cmd = ['ffmpeg', '-y', '-v', 'error', '-i', str(f), '-vf', f'scale={tw}:{th}', '-fpsmax', '30',
                   '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                   '-movflags', '+faststart']
            cmd += ['-c:a', 'aac', '-b:a', '96k', '-ac', '2'] if info['audio'] else ['-an']
            subprocess.run(cmd + [str(dst)], check=True)
            if dst.stat().st_size <= MAX_MB * 1024 * 1024:
                break
        row.update(file=dst.name, out_bytes=dst.stat().st_size, crf=crf, size=[tw, th])
        dur = info['duration']
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{min(dur * 0.25, 3):.2f}', '-i', str(dst), '-frames:v', '1',
                        '-vf', 'scale=540:-2', '-q:v', '4', str(out / f'{name}.jpg')], check=True)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(dst), '-vf', f'fps={8 / dur:.4f},scale=200:-2,tile=8x1',
                        '-frames:v', '1', '-q:v', '5', str(out / f'{name}.strip.jpg')], check=False)
        row.update(poster=f'{name}.jpg', strip=f'{name}.strip.jpg')
        manifest['files'].append(row)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    {'site': site, 'videos': videos}[sys.argv[1]](pathlib.Path(sys.argv[2]))
