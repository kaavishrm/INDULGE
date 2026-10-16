"""Builds the website copy of the deck into a folder: python3 pitches/westside/web.py <out> [base-url].

The page is the standalone deck plus an icon, a link-preview image and a no-index rule, so the
pitch opens from a link but stays out of search results."""
import sys, shutil, pathlib
HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1]); base = sys.argv[2].rstrip('/') if len(sys.argv) > 2 else ''
out.mkdir(parents=True, exist_ok=True)
for f in (HERE / 'web').iterdir():
    shutil.copy2(f, out / f.name)
t = (HERE / 'dist' / 'Westside-x-M360-Seen-at-Westside.html').read_text()
desc = "Seen at Westside: Mask360's proposal to Westside. A style account built like @TargetStyle, eight content properties, and a one-opening pilot measured on footfall per store."
img = (base + '/og.jpg') if base else 'og.jpg'
head = f'''<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="Seen at Westside · Mask360">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
'''
assert t.count('<title>Seen at Westside</title>') == 1
(out / 'index.html').write_text(t.replace('<title>Seen at Westside</title>', '<title>Seen at Westside · Mask360</title>\n' + head))
print('site ready in', out)
