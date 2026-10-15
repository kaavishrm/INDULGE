import re, base64, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
B = ROOT/'src'; A = B/'assets'; O = ROOT/'dist'; O.mkdir(exist_ok=True)
css = (B/'styles.css').read_text(); body = (B/'body.html').read_text(); js = (B/'script.js').read_text()
def path_of(name):
    s = (A/f'{name}.svg').read_text(); return re.search(r' d="([^"]+)"', s).group(1)
def img(name):
    data = (A/f'{name}.webp').read_bytes(); return 'data:image/webp;base64,' + base64.b64encode(data).decode()
body = re.sub(r'\{\{PATH:(\w+)\}\}', lambda m: path_of(m.group(1)), body)
body = re.sub(r'\{\{IMG:(\w+)\}\}', lambda m: img(m.group(1)), body)
assert '{{' not in body, re.findall(r'\{\{[^}]+\}\}', body)
head = '''<title>Seen at Westside</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Mask360's proposal to Westside: social, content and in-store experiences that pull people into a named Westside store, measured on footfall per store.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..800&family=Hanken+Grotesk:wght@300..700&display=swap">
<style>
''' + css + '\n</style>\n'
frag = head + body + '\n<script>\n' + js + '\n</script>\n'
(O/'seen-at-westside.html').write_text(frag)
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + '</head>\n<body>\n' + body + '\n<script>\n' + js + '\n</script>\n</body>\n</html>\n')
(O/'Westside-x-M360-Seen-at-Westside.html').write_text(full)
for f in O.iterdir(): print(f, f.stat().st_size)
