# fx: the effects the page ships

The six effects m360 OS uses are the real packages from Libraries.dev and React Bits, bundled once into
`src/js/00-a-fx.vendor.js` and exposed on `window.FX`. The page has no module system (one page, three
script tags, a strict content policy), so the bundle rides inside the page like every other module,
ahead of the m360 code. React, ReactDOM and the JSX runtime resolve to the page's own copies through
`shims/`, so every component shares the React the app runs on.

| Effect | Package | Where |
|---|---|---|
| Orb | `thinking-orbs` | every "thinking" line (size 20), the orb screen on the phone (64, listening), the phone's buddy button (32, breathing) |
| Beam | `border-beam` | any flame card and hot fold (sunset), the thought for the day (colorful, slow) |
| Voice | `voice-glow` | under the Ask input while the mic is live, gathering into a beam while the answer comes; the bottom of the orb screen |
| Bots | `bot-avatars` | beside the AI's words in Ask (clover, flame), in the buddy's bubble (droid) |
| Metal | retired in v36.2 | `metal-fx` is no longer bundled: its chromatic text drew numbers as misaligned coloured ghosts. `M.fx.Metal`, `MetalText` and `MetalBadge` stay as names and draw a plain button, plain text and a flame pill |
| Bell | React Bits `BellToggle` (`BellToggle.jsx`, `src/css/90-bell.vendor.css`) | the notifications card on Home |

The wrappers in `src/js/01-z-fx.js` (`M.fx.Orb`, `Beam`, `Metal`, `Voice`, `Bot`, `Bell`) pick the
house colours and theme and stand down to the plain child when the bundle is missing or the person asked
for reduced motion.

## three.js, for the 3D office (v35)

`three` is pinned at exactly `0.186.1`. `three-entry.js` names the pieces the office uses and nothing else
(the renderer, the lights and materials, the primitive geometries, canvas textures, the raycaster and the maths,
plus `OrbitControls`, `RoomEnvironment`, `RoundedBoxGeometry`, `mergeGeometries` and `mergeVertices`): named
imports only, never `import * as THREE` and never a loader. `build.sh` bundles it a second time with the same
flags minus the React aliases and `--global-name=M3D` into `src/vendor/three.vendor.js` (about 615 KB, 156 KB
gzipped; the budget is 640 KB and 170 KB). It refuses a bundle that holds `fetch(`, `import(`, `eval(`,
`new Function` or a blocking dialog, and replaces em and en dashes as for the effects.

The file lives in `src/vendor`, outside `src/js`, so it is never concatenated as a module. `build.py` inlines it
in the artifact page as one function, `window.M360_3D = function () { ... return M3D; }`, so nothing of it runs
until `M.office3d.load()` asks for it the first time a 3D office is drawn. `build_edgeone.py` ships the same
function as `edgeone/public/vendor/three.<sha8>.js` and names it in the build stamp script
(`M360_3D_SRC`, and its integrity in `M360_3D_SRI`), which the page's CSP already hashes; `edgeone.json` gains one
immutable cache entry for that exact path.

## Rebuilding the bundle

```bash
cd m360-os/fx
npm install
./build.sh          # writes ../src/js/00-a-fx.vendor.js and ../src/vendor/three.vendor.js
cd .. && python3 build.py && python3 harness/conformance.py
```

The bundle is committed, so the page build and the EdgeOne deploy never need npm. `harness/conformance.py`
skips `*.vendor.js` and `*.vendor.css`: they are other people's code, kept as shipped (the bell's default
colours moved to the m360 palette, and em dashes replaced in strings, since the page build refuses them).

One set of edits to the packages, applied by `build.sh`: `patches.py` lets the orbs, the bots and the
voice beam draw sharp at 3x (its metal-fx line still patches the installed package, which is no longer
bundled). On an upgrade, a patch stops the build if its line has moved, so it can be checked.
