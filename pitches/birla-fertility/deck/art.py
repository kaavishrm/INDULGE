"""Line-art illustrations for the Birla Fertility & IVF deck, drawn in SVG in the Westside v4 manner. Colours come from the deck's
CSS classes: ln (ink line), ln2 (fine grey line), fp (bone fill), fi (ink fill), fw (paper fill), fpanel (panel fill); tx-d is the
thin uppercase sans, tx-n the Didone (numbers only)."""
from html import escape as esc


def _t(x, y, s, size=12, cls='', anchor='start', weight=400, ls=0, fill=None):
    st = f'font-size:{size}px;font-weight:{weight}' + (f';letter-spacing:{ls}em' if ls else '') + (f';fill:{fill}' if fill else '')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" style="{st}">{esc(s)}</text>'


def _panel(o):
    o.append('<rect class="fpanel" x="40" y="40" width="720" height="460"/>')
    o.append('<rect class="ln" x="40" y="40" width="720" height="460"/>')


def night():
    """The 1 a.m. Questions: a bedroom at night, the lamp off, a clock at 1:04 and a phone with a question typed into it."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a bedroom at night with the moon in the window, a bedside '
         'table with a lamp switched off and a clock reading 1:04, and a phone with a fertility question typed into its search bar">']
    _panel(o)
    # window and moon
    o.append('<rect class="fw" x="470" y="78" width="210" height="150"/><rect class="ln" x="470" y="78" width="210" height="150"/>')
    o.append('<path class="ln2" d="M575 78 L575 228 M470 153 L680 153"/>')
    o.append('<circle class="fp" cx="630" cy="114" r="20"/><circle class="ln2" cx="630" cy="114" r="20"/>')
    # bed: pillow, mattress, blanket
    o.append('<path class="fw" d="M40 300 L360 300 L360 372 L40 372 Z"/><path class="ln" d="M40 300 L360 300 L360 372 L40 372"/>')
    o.append('<ellipse class="fw" cx="118" cy="290" rx="64" ry="18"/><ellipse class="ln2" cx="118" cy="290" rx="64" ry="18"/>')
    o.append('<path class="fp" d="M190 296 C240 284 300 286 360 298 L360 372 L200 372 Z"/>')
    o.append('<path class="ln2" d="M190 296 C240 284 300 286 360 298 M200 372 L190 296"/>')
    o.append('<path class="ln" d="M60 372 L60 420 M340 372 L340 420"/>')
    # bedside table, drawer and knob
    o.append('<rect class="fw" x="392" y="318" width="150" height="152"/><rect class="ln" x="392" y="318" width="150" height="152"/>')
    o.append('<line class="ln2" x1="392" y1="378" x2="542" y2="378"/><circle class="fi" cx="467" cy="350" r="2.6"/>')
    # lamp, switched off
    o.append('<ellipse class="ln" cx="428" cy="316" rx="18" ry="4"/><path class="ln" d="M428 312 L428 250"/>')
    o.append('<path class="fp" d="M400 250 L456 250 L444 212 L412 212 Z"/><path class="ln" d="M400 250 L456 250 L444 212 L412 212 Z"/>')
    # clock
    o.append('<rect class="fw" x="470" y="282" width="62" height="34"/><rect class="ln" x="470" y="282" width="62" height="34"/>')
    o.append(_t(501, 307, '1:04', 21, 'tx-n', anchor='middle'))
    # the phone and its question
    o.append('<rect class="fw" x="584" y="248" width="140" height="232" rx="16"/><rect class="ln" x="584" y="248" width="140" height="232" rx="16"/>')
    o.append('<rect class="fp" x="596" y="270" width="116" height="190" rx="4"/>')
    o.append('<rect class="fw" x="604" y="282" width="100" height="24" rx="12"/><rect class="ln2" x="604" y="282" width="100" height="24" rx="12"/>')
    o.append('<circle class="ln2" cx="616" cy="294" r="5"/>')
    for i, line in enumerate(('IS IT NORMAL', 'THAT IT’S', 'TAKING US', 'THIS LONG?')):
        o.append(_t(612, 334 + i * 22, line, 12, 'tx-d', ls=.08))
    o.append('<path class="ln" d="M612 422 L612 438"/>')
    o.append('<line class="ln2" x1="604" y1="450" x2="704" y2="450"/>')
    o.append('<line class="ln2" x1="40" y1="470" x2="760" y2="470"/>')
    o.append(_t(400, 530, 'a question typed at 1:04 a.m.', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


def _chair(o, x):
    """A side-view chair facing right, its seat at x to x+86."""
    o.append(f'<path class="ln" d="M{x} 360 L{x - 10} 238"/>')
    o.append(f'<rect class="fp" x="{x - 8}" y="248" width="14" height="96" transform="rotate(-5 {x} 296)"/>')
    o.append(f'<rect class="fp" x="{x}" y="350" width="86" height="14"/><rect class="ln" x="{x}" y="350" width="86" height="14"/>')
    o.append(f'<path class="ln" d="M{x + 6} 364 L{x} 450 M{x + 80} 364 L{x + 86} 450 M{x + 4} 410 L{x + 82} 410"/>')


def chairs():
    """Half the Story: a specialist's desk with two test folders, HERS and HIS, and two chairs facing it."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a fertility specialist’s desk with two test folders on it, '
         'one marked hers and one marked his, and two chairs side by side facing the desk">']
    _panel(o)
    # a framed print on the wall
    o.append('<rect class="fw" x="530" y="96" width="120" height="92"/><rect class="ln" x="530" y="96" width="120" height="92"/>')
    o.append('<circle class="ln2" cx="575" cy="142" r="24"/><circle class="ln2" cx="605" cy="142" r="24"/>')
    # desk
    o.append('<rect class="fw" x="440" y="292" width="300" height="16"/><rect class="ln" x="440" y="292" width="300" height="16"/>')
    o.append('<rect class="fw" x="456" y="308" width="268" height="142"/><rect class="ln" x="456" y="308" width="268" height="142"/>')
    o.append('<line class="ln2" x1="590" y1="308" x2="590" y2="450"/>')
    # the two folders
    for x, label in ((470, 'HERS'), (596, 'HIS')):
        o.append(f'<path class="fp" d="M{x} 292 L{x + 12} 262 L{x + 118} 262 L{x + 106} 292 Z"/>')
        o.append(f'<path class="ln" d="M{x} 292 L{x + 12} 262 L{x + 118} 262 L{x + 106} 292 Z"/>')
        o.append(_t(x + 59, 283, label, 13, 'tx-d', anchor='middle', ls=.2))
    # two chairs, side by side
    _chair(o, 150)
    _chair(o, 300)
    o.append('<line class="ln2" x1="40" y1="450" x2="760" y2="450"/>')
    o.append(_t(400, 530, 'two chairs, one appointment', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


def group():
    """The Good News Question: marigolds, two diyas, and a family chat where the question meets a sticker."""
    o = ['<svg viewBox="0 0 800 560" role="img" aria-label="Line drawing: a phone showing a family chat. An aunt asks good news kab, '
         'the reply is a sticker that says ask me about my trip to Goa, and she answers how was Goa. Marigold strings hang above '
         'and two diyas burn on either side">']
    _panel(o)
    # marigold strings
    for x in range(90, 740, 60):
        o.append(f'<line class="ln2" x1="{x}" y1="40" x2="{x}" y2="{70 + (x // 60 % 3) * 10}"/>')
        for k in range(3):
            o.append(f'<circle class="fp" cx="{x}" cy="{58 + k * 12 + (x // 60 % 3) * 10}" r="6"/>')
    # the phone
    o.append('<rect class="fw" x="292" y="104" width="216" height="372" rx="22"/><rect class="ln" x="292" y="104" width="216" height="372" rx="22"/>')
    o.append('<rect class="fp" x="304" y="124" width="192" height="40"/>')
    o.append(_t(400, 149, 'THE FAMILY GROUP', 12, 'tx-d', anchor='middle', ls=.16))
    # the question
    o.append('<rect class="fw" x="314" y="178" width="140" height="56" rx="10"/><rect class="ln2" x="314" y="178" width="140" height="56" rx="10"/>')
    o.append(_t(326, 198, 'MASI', 10, weight=500, ls=.12))
    o.append(_t(326, 222, 'good news kab?', 14))
    # the sticker
    o.append('<rect class="fp" x="350" y="250" width="140" height="104" rx="18"/><rect class="ln" x="350" y="250" width="140" height="104" rx="18"/>')
    for i, line in enumerate(('ASK ME ABOUT', 'MY TRIP', 'TO GOA')):
        o.append(_t(420, 286 + i * 24, line, 14, 'tx-d', anchor='middle', ls=.08))
    # the reply
    o.append('<rect class="fw" x="314" y="372" width="140" height="56" rx="10"/><rect class="ln2" x="314" y="372" width="140" height="56" rx="10"/>')
    o.append(_t(326, 392, 'MASI', 10, weight=500, ls=.12))
    o.append(_t(326, 416, 'how was Goa?', 14))
    # two diyas
    for cx in (160, 640):
        o.append(f'<path class="fp" d="M{cx - 54} 430 C{cx - 44} 466 {cx + 44} 466 {cx + 54} 430 Z"/>')
        o.append(f'<path class="ln" d="M{cx - 54} 430 C{cx - 44} 466 {cx + 44} 466 {cx + 54} 430 Z"/>')
        o.append(f'<path class="fw" d="M{cx} 384 C{cx + 12} 400 {cx + 12} 418 {cx} 424 C{cx - 12} 418 {cx - 12} 400 {cx} 384 Z"/>')
        o.append(f'<path class="ln" d="M{cx} 384 C{cx + 12} 400 {cx + 12} 418 {cx} 424 C{cx - 12} 418 {cx - 12} 400 {cx} 384 Z"/>')
    o.append('<line class="ln2" x1="40" y1="470" x2="760" y2="470"/>')
    o.append(_t(400, 530, 'a kinder way to change the subject', 15, 'tx-d', anchor='middle'))
    o.append('</svg>')
    return ''.join(o)


# the content, mapped: the platform in the middle, four pillars, three series on each (title, formats)
MAP = [
    ('ANSWER', '40%', 'L', 150, [('THE 1 A.M. QUESTIONS', 'Reels · Shorts'), ('MYTH OR FACT', 'Carousels'),
                                 ('ASK A SPECIALIST', 'Instagram Live, monthly')]),
    ('REASSURE', '20%', 'L', 570, [('YOUR FIRST VISIT', 'Carousels · Reels'), ('THE COUNSELLOR’S HOUR', 'Stories · question box'),
                                   ('A CYCLE, EXPLAINED', 'Carousels · YouTube')]),
    ('THE SCIENCE', '20%', 'R', 150, [('INSIDE THE LAB', 'Reels · YouTube'), ('MEET THE SPECIALIST', 'Reels · LinkedIn'),
                                      ('SCIENCE, SIMPLY', 'YouTube long form')]),
    ('BELONG', '20%', 'R', 570, [('HALF THE STORY', 'Creator series for men'), ('THE GOOD NEWS QUESTION', 'Stickers · a short film'),
                                 ('YOUR QUESTIONS, ANSWERED', 'Reels that reply to comments')]),
]


def mindmap():
    """The content plan as a mind map: the platform in an ellipse, four ink pillars with their share of the feed, and three
    series off each pillar with the formats they run in. Hairline curves join them, in the deck's line-drawing manner."""
    import math
    cx, cy, rx, ry = 800, 360, 168, 74
    pw, ph = 262, 66
    o = ['<svg viewBox="0 0 1600 720" role="img" aria-label="Mind map of the content. In the middle, No question too quiet. Four '
         'pillars branch from it: Answer, 40% of the feed, with The 1 a.m. Questions, Myth or fact and Ask a specialist; Reassure, '
         '20%, with Your first visit, The counsellor’s hour and A cycle, explained; The science, 20%, with Inside the lab, Meet the '
         'specialist and Science, simply; Belong, 20%, with Half the Story, The Good News Question and Your questions, answered.">']
    for name, share, side, py, leaves in MAP:
        px = 520 if side == 'L' else 1080
        inner = px + pw / 2 if side == 'L' else px - pw / 2
        outer = px - pw / 2 if side == 'L' else px + pw / 2
        # the branch from the platform to the pillar
        t = math.atan2((py - cy) / ry, (inner - cx) / rx)
        ex, ey = cx + rx * math.cos(t), cy + ry * math.sin(t)
        o.append(f'<path class="ln" d="M{ex:.1f} {ey:.1f} Q{ex:.1f} {py} {inner} {py}"/>')
        # the three series off the pillar
        for k, (title, fmt) in enumerate(leaves):
            ly = py + (k - 1) * 100
            x0, x1 = (40, 300) if side == 'L' else (1300, 1560)
            near = x1 if side == 'L' else x0
            mid = (outer + near) / 2
            o.append(f'<path class="ln2" d="M{outer} {py} C{mid} {py} {mid} {ly} {near} {ly}"/>')
            o.append(f'<line class="ln" x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}"/>')
            o.append(f'<circle class="fpk" cx="{near}" cy="{ly}" r="4.5"/>')
            o.append(_t(x0, ly - 11, title, 17, 'tx-d', ls=.05))
            o.append(_t(x0, ly + 24, fmt, 14, fill='var(--ink-3)'))
        # the pillar, in ink, with its share of the feed
        o.append(f'<rect class="fi" x="{px - pw / 2}" y="{py - ph / 2}" width="{pw}" height="{ph}"/>')
        o.append(_t(px - pw / 2 + 20, py + 7, name, 19, 'tx-d', ls=.12, fill='#fff'))
        o.append(_t(px + pw / 2 - 18, py + 10, share, 28, 'tx-n', anchor='end', fill='var(--pink)'))
    # the platform in the middle
    o.append(f'<ellipse class="fp" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/><ellipse class="ln" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>')
    o.append(_t(cx, cy - 30, 'THE PLATFORM', 11, anchor='middle', ls=.22, fill='var(--ink-3)'))
    o.append(_t(cx, cy + 2, 'NO QUESTION', 25, 'tx-d', anchor='middle', ls=.06))
    o.append(_t(cx, cy + 32, 'TOO QUIET', 25, 'tx-d', anchor='middle', ls=.06))
    o.append('</svg>')
    return ''.join(o)
