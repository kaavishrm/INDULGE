"""Line-art illustrations for The Park deck, drawn in SVG in the Westside v4 manner. Colours come from the deck's CSS classes:
ln (ink line), ln2 (fine grey line), fp (bone fill), fi (ink fill), fw (paper fill), fpanel (panel fill); tx-d is the thin
uppercase sans, tx-n the Didone (numbers only)."""
import math
from html import escape as esc


def _t(x, y, s, size=12, cls='', anchor='start', weight=400, ls=0, fill=None):
    st = f'font-size:{size}px;font-weight:{weight}' + (f';letter-spacing:{ls}em' if ls else '') + (f';fill:{fill}' if fill else '')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" style="{st}">{esc(s)}</text>'


def _panel(o):
    o.append('<rect class="fpanel" x="40" y="40" width="720" height="460"/>')
    o.append('<rect class="ln" x="40" y="40" width="720" height="460"/>')


def stage():
    """Someplace Else: a small stage, a mic, an amp and a guitar, string lights, a crowd, a phone filming one take."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a small pub stage with a microphone, an amplifier and a guitar '
         'under string lights, a crowd in front and a phone on a tripod filming the set in one take">']
    _panel(o)
    # string lights
    o.append('<path class="ln2" d="M52 86 Q400 150 748 86"/>')
    for i in range(1, 16):
        t = i / 16
        x = 52 + 696 * t
        y = (1 - t) ** 2 * 86 + 2 * (1 - t) * t * 150 + t ** 2 * 86
        o.append(f'<line class="ln2" x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + 9:.1f}"/>')
        o.append(f'<circle class="{"fp" if i % 3 else "fw"}" cx="{x:.1f}" cy="{y + 14:.1f}" r="5"/><circle class="ln2" cx="{x:.1f}" cy="{y + 14:.1f}" r="5"/>')
    # the sign
    o.append('<rect class="fw" x="276" y="150" width="248" height="46"/><rect class="ln" x="276" y="150" width="248" height="46"/>')
    o.append(_t(400, 180, 'SOMEPLACE ELSE', 19, 'tx-d', anchor='middle', ls=.16))
    # stage
    o.append('<path class="ln" d="M110 392 L690 392 L690 414 L110 414 Z"/>')
    o.append('<line class="ln2" x1="110" y1="400" x2="690" y2="400"/>')
    # amp
    o.append('<rect class="fw" x="168" y="300" width="96" height="92"/><rect class="ln" x="168" y="300" width="96" height="92"/>')
    o.append('<rect class="ln2" x="178" y="324" width="76" height="58"/>')
    for k in range(4):
        o.append(f'<circle class="ln2" cx="{186 + k * 14}" cy="312" r="3.4"/>')
    # mic and stand
    o.append('<path class="ln" d="M400 392 L400 252 M384 392 L416 392"/>')
    o.append('<path class="ln" d="M400 252 L428 232"/>')
    o.append('<ellipse class="fp" cx="434" cy="226" rx="8" ry="12" transform="rotate(-35 434 226)"/>')
    o.append('<ellipse class="ln" cx="434" cy="226" rx="8" ry="12" transform="rotate(-35 434 226)"/>')
    # stool
    o.append('<ellipse class="ln" cx="486" cy="330" rx="24" ry="6"/><path class="ln" d="M468 334 L460 392 M504 334 L512 392 M486 336 L486 392 M466 366 L506 366"/>')
    # guitar on its stand
    o.append('<path class="ln" d="M600 392 L612 352 M636 392 L624 352"/>')
    o.append('<path class="fp" d="M618 368 C596 368 590 346 600 334 C592 322 596 300 618 300 C640 300 644 322 636 334 C646 346 640 368 618 368 Z"/>')
    o.append('<path class="ln" d="M618 368 C596 368 590 346 600 334 C592 322 596 300 618 300 C640 300 644 322 636 334 C646 346 640 368 618 368 Z"/>')
    o.append('<circle class="ln2" cx="618" cy="334" r="8"/>')
    o.append('<path class="ln" d="M615 300 L615 214 L621 214 L621 300 M612 214 L612 196 L624 196 L624 214"/>')
    # crowd
    for k, cx in enumerate(range(96, 720, 52)):
        cy = 444 + (6 if k % 2 else 0)
        o.append(f'<circle class="fw" cx="{cx}" cy="{cy}" r="15"/><circle class="ln2" cx="{cx}" cy="{cy}" r="15"/>')
        o.append(f'<path class="ln2" d="M{cx - 22} {cy + 44} C{cx - 20} {cy + 20} {cx + 20} {cy + 20} {cx + 22} {cy + 44}"/>')
    # phone on a tripod, filming
    o.append('<rect class="fw" x="700" y="296" width="40" height="72" rx="6"/><rect class="ln" x="700" y="296" width="40" height="72" rx="6"/>')
    o.append('<circle class="fi" cx="711" cy="308" r="3"/>')
    o.append(_t(717, 312, 'REC', 10, weight=500, ls=.1))
    o.append('<path class="ln" d="M720 368 L720 430 M720 430 L700 488 M720 430 L740 488"/>')
    o.append(_t(400, 530, 'one take, filmed live', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


def suite():
    """Room 1967: a suite in one-point perspective, a pendant, a bed, a lounge chair, art, a door with its number."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a hotel suite in perspective with a low bed, a pendant lamp, '
         'a lounge chair, two framed artworks and a door marked 1967">']
    _panel(o)
    # the room: back wall and the four edges to the corners
    o.append('<rect class="ln" x="230" y="128" width="340" height="236"/>')
    o.append('<path class="ln2" d="M40 40 L230 128 M760 40 L570 128 M40 500 L230 364 M760 500 L716 468.5 M600 385.5 L570 364"/>')
    # art on the back wall
    o.append('<rect class="fw" x="262" y="160" width="70" height="92"/><rect class="ln" x="262" y="160" width="70" height="92"/>')
    o.append('<circle class="fp" cx="297" cy="206" r="22"/><circle class="ln2" cx="297" cy="206" r="22"/>')
    o.append('<rect class="fw" x="350" y="176" width="54" height="54"/><rect class="ln" x="350" y="176" width="54" height="54"/>')
    o.append('<path class="ln2" d="M356 222 L377 186 L398 222 Z"/>')
    # pendant
    o.append('<path class="ln" d="M470 40 L470 150"/>')
    o.append('<path class="fp" d="M444 176 C444 158 456 150 470 150 C484 150 496 158 496 176 Z"/><path class="ln" d="M444 176 C444 158 456 150 470 150 C484 150 496 158 496 176 Z"/>')
    # bed: headboard on the back wall, mattress coming forward
    o.append('<rect class="fw" x="300" y="262" width="200" height="56"/><rect class="ln" x="300" y="262" width="200" height="56"/>')
    o.append('<path class="fw" d="M292 318 L508 318 L566 430 L234 430 Z"/><path class="ln" d="M292 318 L508 318 L566 430 L234 430 Z"/>')
    o.append('<path class="ln" d="M234 430 L234 444 L566 444 L566 430"/>')
    o.append('<path class="fp" d="M312 324 L392 324 L396 346 L304 346 Z"/><path class="ln2" d="M312 324 L392 324 L396 346 L304 346 Z"/>')
    o.append('<path class="fp" d="M408 324 L488 324 L496 346 L404 346 Z"/><path class="ln2" d="M408 324 L488 324 L496 346 L404 346 Z"/>')
    o.append('<path class="ln2" d="M276 372 L524 372"/>')
    # lounge chair, front right
    o.append('<path class="fp" d="M610 402 C600 352 622 318 664 312 C700 308 716 330 712 360 L700 402 Z"/>')
    o.append('<path class="ln" d="M610 402 C600 352 622 318 664 312 C700 308 716 330 712 360 L700 402 Z"/>')
    o.append('<path class="fw" d="M604 402 L708 402 L700 420 L612 420 Z"/>')
    o.append('<path class="ln" d="M604 402 L708 402 L700 420 L612 420 Z M620 420 L612 470 M692 420 L700 470"/>')
    # door on the left wall, and its number
    o.append('<path class="fw" d="M112 172 L176 186 L176 380 L112 412 Z"/><path class="ln" d="M112 172 L176 186 L176 380 L112 412 Z"/>')
    o.append('<circle class="fi" cx="166" cy="292" r="2.6"/>')
    o.append(_t(136, 160, '1967', 24, 'tx-n', anchor='middle'))
    o.append(_t(400, 530, 'one suite, a new designer every year', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


def cup():
    """Flurys 100: a cup of tea on its saucer, steam, and a ribboned pastry box marked 100."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a cup of tea on a saucer with steam rising, '
         'beside a ribboned pastry box marked Flurys 100">']
    _panel(o)
    o.append('<line class="ln2" x1="60" y1="440" x2="740" y2="440"/>')
    # saucer and cup
    o.append('<ellipse class="fw" cx="290" cy="410" rx="160" ry="30"/><ellipse class="ln" cx="290" cy="410" rx="160" ry="30"/>')
    o.append('<ellipse class="ln2" cx="290" cy="406" rx="96" ry="16"/>')
    o.append('<path class="fw" d="M196 292 C200 372 246 404 290 404 C334 404 380 372 384 292 Z"/>')
    o.append('<path class="ln" d="M196 292 C200 372 246 404 290 404 C334 404 380 372 384 292"/>')
    o.append('<ellipse class="fp" cx="290" cy="292" rx="94" ry="18"/><ellipse class="ln" cx="290" cy="292" rx="94" ry="18"/>')
    o.append('<path class="ln" d="M382 316 C430 308 432 372 370 366"/>')
    for k, x in enumerate((258, 290, 322)):
        o.append(f'<path class="ln2" d="M{x} 262 C{x - 14} 238 {x + 14} 222 {x} 196 C{x - 12} 178 {x + 10} 160 {x} 140"/>')
    # pastry box, resting on the table line
    o.append('<g transform="translate(0 10)">')
    o.append('<path class="fw" d="M486 300 L700 300 L700 430 L486 430 Z"/><path class="ln" d="M486 300 L700 300 L700 430 L486 430 Z"/>')
    o.append('<path class="fw" d="M486 300 L520 262 L734 262 L700 300 Z"/><path class="ln" d="M486 300 L520 262 L734 262 L700 300 Z"/>')
    o.append('<path class="fw" d="M700 300 L734 262 L734 392 L700 430 Z"/><path class="ln" d="M700 300 L734 262 L734 392 L700 430 Z"/>')
    o.append('<path class="ln2" d="M593 300 L593 430 M503 281 L717 281"/>')
    o.append('<path class="ln" d="M593 281 C570 250 548 258 560 276 C566 284 582 284 593 281 C604 278 620 270 626 258 C632 244 612 246 593 281"/>')
    o.append(_t(540, 352, 'FLURYS', 18, 'tx-d', anchor='middle', ls=.16))
    o.append(_t(646, 368, '100', 40, 'tx-n', anchor='middle'))
    o.append(_t(540, 378, 'PARK STREET', 9, anchor='middle', weight=500, ls=.2, fill='var(--ink-3)'))
    o.append('</g>')
    o.append(_t(400, 530, 'a hundred years in 2027', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


def hotels_grid(today=42, target=87, cols=12):
    """One square per hotel: today's filled in ink, the ones still to open drawn as hairlines."""
    cell, gap = 22, 6
    rows = -(-target // cols)
    w = cols * (cell + gap) - gap
    h = rows * (cell + gap) - gap
    o = [f'<svg viewBox="-1 -1 {w + 2} {h + 2}" role="img" aria-label="{target} squares, one per hotel: {today} open today in black, '
         f'{target - today} to open by 2030 in outline">']
    for i in range(target):
        r, c = divmod(i, cols)
        x, y = c * (cell + gap), r * (cell + gap)
        if i < today:
            o.append(f'<rect class="fi" x="{x}" y="{y}" width="{cell}" height="{cell}"/>')
        else:
            o.append(f'<rect x="{x + .5}" y="{y + .5}" width="{cell - 1}" height="{cell - 1}" style="fill:none;stroke:var(--ink-3)"/>')
    o.append('</svg>')
    return ''.join(o)


def phones():
    """Three sample posts for The Sessions, drawn as phones: a Reel cover, a story and a carousel card."""
    o = ['<svg viewBox="0 0 720 420" role="img" aria-label="Line drawing: three phones showing sample posts for The Sessions. '
         'A Reel cover reading Park Street still plays, a story reading 11:40 p.m. Someplace Else, and a carousel card '
         'reading the full set on YouTube">']
    for i, x in enumerate((10, 260, 510)):
        o.append(f'<rect class="fw" x="{x}" y="10" width="200" height="356" rx="22"/><rect class="ln" x="{x}" y="10" width="200" height="356" rx="22"/>')
        screen = ('fi', 'fp', 'fw')[i]
        o.append(f'<rect class="{screen}" x="{x + 9}" y="19" width="182" height="338" rx="15"/>')
        o.append(f'<rect class="{"fw" if i == 0 else "fi"}" x="{x + 78}" y="27" width="44" height="7" rx="3.5"/>')
    # 1: Reel cover, night
    o.append(_t(110, 92, 'SET 01 · ONE TAKE', 11, anchor='middle', weight=500, ls=.18, fill='var(--paper)'))
    o.append('<circle cx="110" cy="188" r="30" style="fill:none;stroke:var(--paper);stroke-width:1.3"/>')
    o.append('<path d="M101 172 L125 188 L101 204 Z" style="fill:var(--paper)"/>')
    o.append(_t(110, 290, 'PARK STREET', 25, 'tx-d', anchor='middle', ls=.02, fill='var(--paper)'))
    o.append(_t(110, 320, 'STILL PLAYS', 25, 'tx-d', anchor='middle', ls=.02, fill='var(--paper)'))
    # 2: story, tonight
    for k in range(3):
        o.append(f'<line class="{"ln" if k == 0 else "ln2"}" x1="{280 + k * 56}" y1="48" x2="{328 + k * 56}" y2="48"/>')
    o.append(_t(360, 178, '11:40', 62, 'tx-n', anchor='middle'))
    o.append(_t(360, 206, 'P.M. TONIGHT', 12, anchor='middle', weight=500, ls=.2))
    o.append('<line class="ln2" x1="300" y1="236" x2="420" y2="236"/>')
    o.append(_t(360, 266, 'SOMEPLACE ELSE', 16, 'tx-d', anchor='middle', ls=.12))
    o.append(_t(360, 288, 'PARK STREET, KOLKATA', 10, anchor='middle', weight=500, ls=.2, fill='var(--ink-3)'))
    # 3: carousel card, the full set
    o.append('<rect class="fp" x="530" y="60" width="160" height="90"/><rect class="ln" x="530" y="60" width="160" height="90"/>')
    o.append('<circle class="fw" cx="610" cy="105" r="17"/><circle class="ln" cx="610" cy="105" r="17"/><path class="fi" d="M604 95 L620 105 L604 115 Z"/>')
    o.append(_t(610, 210, 'THE FULL SET', 21, 'tx-d', anchor='middle', ls=.04))
    o.append(_t(610, 238, 'ON YOUTUBE', 21, 'tx-d', anchor='middle', ls=.04))
    o.append(_t(610, 270, 'START TO FINISH, NO CUTS', 10, anchor='middle', weight=500, ls=.18, fill='var(--ink-3)'))
    for k in range(3):
        o.append(f'<circle class="{"fi" if k == 0 else "ln2"}" cx="{598 + k * 12}" cy="334" r="3"/>')
    for x, lab in ((110, 'Reel'), (360, 'Story'), (610, 'Carousel')):
        o.append(_t(x, 404, lab, 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)
