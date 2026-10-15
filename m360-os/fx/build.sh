#!/bin/bash
# Bundles the effects (fx/entry.jsx and the packages in fx/node_modules) into one plain script,
# src/js/00-a-fx.vendor.js, which the page build inlines before the m360 modules. React, ReactDOM and
# the JSX runtime resolve to the page's own copies through fx/shims. Run after `npm install` here.
set -e
cd "$(dirname "$0")"
OUT=../src/js/00-a-fx.vendor.js
python3 patches.py
npx esbuild entry.jsx --bundle --minify --format=iife --target=es2020 --jsx=automatic \
  --alias:react=./shims/react.js --alias:react-dom=./shims/react-dom.js --alias:react/jsx-runtime=./shims/jsx-runtime.js \
  --alias:react/jsx-dev-runtime=./shims/jsx-runtime.js --alias:react-dom/client=./shims/react-dom.js \
  --define:process.env.NODE_ENV=\"production\" --legal-comments=none --log-level=warning --outfile=$OUT.tmp
# the page build refuses em and en dashes anywhere, and a bundle has them in its strings
python3 - "$OUT" <<'EOF'
import sys
p = sys.argv[1]
s = open(p + '.tmp', encoding='utf-8').read()
s = s.replace('—', '-').replace('–', '-')
head = ("/* vendor: the effects from Libraries.dev (thinking-orbs, border-beam, voice-glow, bot-avatars) and\n"
        "   BellToggle from React Bits, bundled by fx/build.sh. Never edited by hand; conformance skips .vendor.js. */\n")
open(p, 'w', encoding='utf-8').write(head + s)
EOF
rm -f "$OUT.tmp"
ls -la "$OUT" | awk '{print $5, $9}'

# three.js for the 3D office: named imports only (three-entry.js), no React aliases, the same flags. It lands in
# src/vendor (outside src/js, so it is never concatenated as a module); build.py wraps it so nothing runs at load.
mkdir -p ../src/vendor
THREE=../src/vendor/three.vendor.js
npx esbuild three-entry.js --bundle --minify --format=iife --global-name=M3D --target=es2020 \
  --legal-comments=none --log-level=warning --outfile=$THREE.tmp
python3 - "$THREE" <<'EOF2'
import json, re, sys
p = sys.argv[1]
s = open(p + '.tmp', encoding='utf-8').read()
s = s.replace('\u2014', '-').replace('\u2013', '-')
# the page holds no network call, no dynamic code and no blocking dialog, so neither may the bundle
for bad in ('fetch(', 'import(', 'eval(', 'new Function'):
    if bad in s:
        sys.exit('three bundle refused: it contains ' + bad)
if re.search(r'(?<![\w.$])(alert|confirm|prompt)\s*\(', s):
    sys.exit('three bundle refused: it calls a blocking dialog')
ver = json.load(open('node_modules/three/package.json'))['version']
head = ('/* vendor: three.js r186 (%s), MIT, Copyright 2010-2026 Three.js Authors. Bundled by fx/build.sh from '
        'fx/three-entry.js. Never edited by hand. */\n' % ver)
open(p, 'w', encoding='utf-8').write(head + s)
EOF2
rm -f "$THREE.tmp"
ls -la "$THREE" | awk '{print $5, $9}'
