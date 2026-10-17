"""Slide copy for Mask360's social media proposal to The Park Hotels, addressed to Anmol Tyagi, who posted the call for
agencies. The Westside v4 deck's way of writing: a headline, a line or two, the numbers, and a one-line source on each
slide; the full sources are on the last page. The content plan is drawn as mind maps (art.content_map, art.handles_map).
Facts come from pitches/the-park-hotels/README.md; Mask360's work comes from its own records. A cold pitch is
conversation one, so there is no pricing and no team grid, and it ends on an open door."""
import datetime as dt
import art
from kit import slide, stat, ul, table, tile, fab, chapter, M_MARK, P_MARK, P_VIEW

TITLE = 'The Park Hotels × Mask360'
DESCRIPTION = ('Mask360’s social media proposal to The Park Hotels, October 2026: Park Street, everywhere. The content map, '
               'the feed, the handles and the numbers.')

# the slides in deck order; page references on the slides are looked up here
ORDER = ['cover', 'promise', 'brief', 'ch-today', 'today', 'channels', 'rule', 'insight', 'ch-idea', 'mindmap', 'mix', 'feed',
         'voice', 'sessions', 'reel', 'room', 'flurys', 'ch-run', 'calendar', 'handles', 'community', 'measure', 'mask360', 'next',
         'close', 'sources']


def pg(sid):
    return f'{ORDER.index(sid) + 1:02d}'


# full sources, shown on the last page; each slide carries a short version
SOURCES = [
    ('The Park today', 'Apeejay Surrendra Park Hotels Q1 FY27 results, Aug 2026: revenue ₹166.8 crore, up 8.1%; occupancy 92%; RevPAR about '
     '₹6,858 (Investywise, ScanX). Food, beverage, nightlife and lifestyle dining about 43% of revenue: IDBI Capital result review, '
     '19 Aug 2026. Flurys 111 stores: Q1 FY27 investor presentation. 42 hotels in 32 cities: Business Traveller, October 2026. '
     '87 hotels by FY30, 45 under development: company investor material, Q1 FY27 and 2 Sep 2026 (Multibagg; filing to NSE).'),
    ('Channels', 'As linked from theparkhotels.com, October 2026: Instagram @theparkhotels, YouTube /theparkhotels, Facebook The Park '
     'Hotels, X @parkhotelsindia, LinkedIn The Park Hotels, Pinterest @theparkhotels. Spotify and WhatsApp are Mask360’s proposal.'),
    ('The brands', 'The Park Hotels corporate overview: five hotel brands, plus Flurys. Zone by The Park at launch: design-conscious and '
     'price-conscious (eHotelier). Ran Baas The Palace, Patiala: 35 suites, opened January 2025, Prix Versailles world’s most '
     'beautiful hotels 2025 (Robb Report India, Time Out).'),
    ('Park Street', 'The Park Kolkata opened in 1967 on Park Street, which gave the group its name (Hotel Designs, Entrepreneur India). '
     'Venues from THE Park Kolkata and THE Park New Delhi dining pages: Someplace Else, Tantra, Roxy, Agni, Aqua, Fire. THE Park '
     'Bangalore was designed by Terence Conran. “Anything but ordinary” has been the line since the 2013 rebrand (Travel Trends Today).'),
    ('The content', 'Flurys turns 100 in 2027 and opened a 24-hour café in Gurugram on 7 Aug 2026 (company announcement via Sahi). The '
     'Kolkata Christmas Festival on Park Street is co-organised by the Apeejay Surrendra Group (News Arena). Instagram’s profile '
     'grid shows posts at 3:4. Pillars, series, formats, cadence, sample posts, captions and the Reel are Mask360’s proposal.'),
    ('Mask360', 'Accounts, managed feeds and the Nexa Platinum Lounge result come from Mask360’s own records.'),
]


def cover():
    body = f'''<div class="stack-l grow" style="justify-content:space-between">
<div class="big-wm pk"><svg viewBox="{P_VIEW}" role="img" aria-label="The Park Hotels"><use href="#logo-p"/></svg></div>
<div class="cover-foot">
  <div class="stack-l">
    <span class="label">A social media proposal from Mask360 · October 2026</span>
    <h1 class="h-display" style="max-width:11em">Park Street, everywhere.</h1>
  </div>
  {M_MARK}
</div></div>'''
    return slide('cover', 'Proposal', body, src='For Anmol Tyagi and the brand team at The Park Hotels · Confidential', bare=True, dark=True,
                 cls='cover scrim', cloth=('kohl', 7))


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">We will make THE Park’s feed the city’s <u>night out</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">01</span><p class="h3">Found</p><p class="mt-s ink2">Reels and search that bring the city in.</p></div>
  <div><span class="no label">02</span><p class="h3">Saved</p><p class="mt-s ink2">Posts people keep for Friday night.</p></div>
  <div><span class="no label">03</span><p class="h3">Booked</p><p class="mt-s ink2">Every post one tap from a table or a room.</p></div>
</div>'''
    return slide('promise', 'Our promise', body)


def brief():
    rows = [['A social media agency', 'A content map, a month on the feed, every handle.', f'{pg("mindmap")} · {pg("calendar")} · {pg("handles")}'],
            ['Hospitality and luxury', 'THE Park in its own numbers, and the feeds we run.', f'{pg("today")} · {pg("mask360")}'],
            ['Think beyond the obvious', 'We post what only THE Park can.', pg('rule')],
            ['Have the work to back it up', 'A Reel, second by second, and a lounge we built.', f'{pg("reel")} · {pg("mask360")}'],
            ['An upcoming pitch', 'This is our point of view. We bring the full plan to the pitch.', pg('next')]]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What you asked for.</h2>
<div class="grow v-center">{table(['You asked', 'Our answer', 'Pages'], rows, cls='tbl roomy brief stackable', right=(2,))}</div>
</div>'''
    return slide('brief', 'Your brief', body, src='From your call for agencies on LinkedIn.')


def ch_today():
    return chapter('ch-today', '01', 'The Park today', 'Full rooms, famous bars, six channels and 45 hotels to come.', ('midnight', 21))


def today():
    body = f'''<div class="stack-l grow">
<h2 class="h1">At 92% full, the feed sells the nights.</h2>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat('92%', 'occupancy', 'Q1 FY27')}
  {stat('43%', 'of revenue from food, drink and nightlife', 'Q1 FY27')}
  {stat('6', 'channels linked from theparkhotels.com', 'October 2026')}
  {stat('42', 'hotels in 32 cities', 'October 2026')}
  {stat('45', 'new hotels by FY2030', 'each one a new handle to launch')}
  {stat('111', 'Flurys stores', '100 years old in 2027')}
</div></div>'''
    return slide('today', 'The Park today · the numbers', body, src='Sources: Q1 FY27 results and investor material, 2026; theparkhotels.com. Full list at the end.')


CHANNELS = [  # channel, handle or status, its job, a week
    ('Instagram', '@theparkhotels', 'The magazine: Reels, carousels, stories', '4 Reels, 4 carousels, stories daily'),
    ('YouTube', '/theparkhotels', 'The Sessions in full, and Shorts', '1 set a month, 3 Shorts'),
    ('Spotify', 'new', 'The Sessions playlist', 'A new set each month'),
    ('WhatsApp', 'new', 'The concierge behind every post', 'Always on'),
    ('Facebook', 'The Park Hotels', 'Events and city listings', '3 posts'),
    ('LinkedIn', 'The Park Hotels', 'Openings, people and design', '2 posts'),
    ('Pinterest', '@theparkhotels', 'Rooms and design boards', '1 board'),
    ('X', '@parkhotelsindia', 'Tonight’s line-up', 'On event nights'),
]


def channels():
    rows = [[f'<b>{c}</b><br><span class="mute f-s">{h}</span>', j, w] for c, h, j, w in CHANNELS]
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Six channels today. Each gets a job.</h2>
  <p class="ink2 lede-s">We add two: a Sessions playlist on Spotify and a WhatsApp line that books tables.</p>
</div>
<div class="grow v-center">{table(['Channel', 'Its job', 'Cadence'], rows, cls='tbl brands tight stackable')}</div>
</div>'''
    return slide('channels', 'The Park on social · channels', body, src='Channels as linked from theparkhotels.com, October 2026. Cadence is Mask360’s proposal.')


def rule():
    park = ['Who played last night', 'What the kitchen cooks at 3 a.m.', 'The people on the night shift', 'A room a designer made',
            'The city after dark']
    series = ['Who Played · every Monday', 'The 3 a.m. Menu · every Thursday', 'Night Shift · every Monday', 'Room 1967 · one suite a year',
              'The Night Map · every Saturday']
    body = f'''<div class="stack-l grow">
<h2 class="h1">We post what only THE Park can.</h2>
<div class="row c2 grow vc">
  <div class="rule stack"><p class="label mute">What only THE Park can post</p>{ul(park, 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label">The series it becomes</p>{ul(series, 'list big-list')}</div>
</div></div>'''
    return slide('rule', 'The house rule', body, src='“Anything but ordinary” has been The Park’s line since 2013. Series are Mask360’s proposal.')


def insight():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">The Park is named after a <u>street</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">1967</span><p class="h3">The first hotel</p><p class="mt-s ink2">The Park opens on Park Street, Calcutta.</p></div>
  <div><span class="no label">The street</span><p class="h3">Jazz, cabaret, late dinners</p><p class="mt-s ink2">Park Street was where Calcutta went out.</p></div>
  <div><span class="no label">Since</span><p class="h3">Kolkata to Delhi</p><p class="mt-s ink2">Someplace Else, Tantra, Agni, Aqua.</p></div>
</div>'''
    return slide('insight', 'The insight', body, src='Sources: The Park Hotels history; THE Park Kolkata and New Delhi dining. Full list at the end.')


def ch_idea():
    return chapter('ch-idea', '02', 'Park Street, everywhere',
                   'Each THE Park hotel becomes the Park Street of its city, told through a magazine of its nights.', ('shaadi', 12))


def _map_tree():
    """The content map as a branching list, shown on phones in place of the drawing."""
    br = ''.join(f'<div class="br"><span class="pill">{p}<small>{w}</small></span><ul>'
                 + ''.join(f'<li{" class=hero" if h else ""}><b>{n}</b><span>{see}</span><em>{fmt}</em></li>' for n, see, fmt, h in series)
                 + '</ul></div>' for p, w, _, series in art.MAP)
    return f'<div class="map-tree"><p class="idea">Park Street, everywhere</p>{br}</div>'


def mindmap():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">The content map.</h2>
  <p class="ink2 lede-s">One idea, four pillars, fifteen series. The three in bold get their own pages. Every post ends one tap from a table or a room.</p>
</div>
<div class="map">{art.content_map()}{_map_tree()}</div>
</div>'''
    return slide('mindmap', 'The idea · the content map', body, src='Venues to confirm with the brand team. Pillars, series and formats are Mask360’s proposal.')


MIX = [  # pillar, posts a week, cloth (kind, seed, dark text), formats, days (from WEEKLY)
    ('After Hours', 3, ('kohl', 31, False), 'Reels · carousels · YouTube', 'Mon · Thu · Fri'),
    ('The Table', 2, ('shaadi', 33, False), 'Reels · carousels', 'Tue · Sun'),
    ('The City', 2, ('midnight', 34, False), 'Carousels · collab Reels', 'Mon · Sat'),
    ('By Design', 1, ('ivory', 32, True), 'Reels · Pinterest', 'Wed'),
]


def mix():
    cols = ''.join(f'''<div class="idea">{tile(c[0], c[1], str(k), n, dark_text=c[2])}
<p class="ink2">{f}</p><div class="rule"><p class="label mute">{"post" if k == 1 else "posts"} a week · {d}</p></div></div>''' for n, k, c, f, d in MIX)
    body = f'''<div class="stack-l grow mix">
<div class="row c-7-5 top">
  <h2 class="h1">Eight posts a week.</h2>
  <p class="ink2 lede-s">Food, drink and nightlife are 43% of revenue, so the night and the table get five of the eight.</p>
</div>
<div class="row grow vc" style="grid-template-columns:3fr 2fr 2fr 1.4fr">{cols}</div>
</div>'''
    return slide('mix', 'The idea · the mix', body, src='Feed posts a week on @theparkhotels: 4 Reels and 4 carousels. Stories run daily on top. Mask360’s proposal.')


FEED = [  # the nine latest posts on Saturday 12 December: date, series, format, cover line, cloth (kind, seed, dark text)
    ('Sat 12 Dec', 'The Sessions · Set 01', 'reel', 'Park Street still plays', ('kohl', 51, False)),
    ('Fri 11 Dec', 'Who’s Playing', 'reel', 'Tonight at Someplace Else', ('slate', 52, False)),
    ('Thu 10 Dec', 'The 3 a.m. Menu', 'reel', 'The kitchen just ate', ('midnight', 53, False)),
    ('Wed 9 Dec', 'Room 1967', 'carousel', 'The search opens', ('bone', 54, True)),
    ('Tue 8 Dec', 'Christmas at Flurys', 'carousel', 'The menu is out', ('shaadi', 55, False)),
    ('Mon 7 Dec', 'Who Played', 'carousel', 'Last night’s set list', ('indigo', 56, False)),
    ('Mon 7 Dec', 'Night Shift', 'carousel', 'The night manager', ('khaki', 57, False)),
    ('Sun 6 Dec', 'The Recipe', 'carousel', 'Save this one', ('rani', 58, False)),
    ('Sat 5 Dec', 'The Night Map', 'carousel', 'Kolkata after dark', ('sand', 59, True)),
]
GLYPH = {'reel': '<svg class="gl" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 2 L10 6 L3 10 Z"/></svg>',
         'carousel': '<svg class="gl" viewBox="0 0 12 12" aria-hidden="true"><path d="M3.5 1.5 H10.5 V8.5 M1.5 3.5 H8.5 V10.5 H1.5 Z"/></svg>'}
ICONS = ('<svg class="acts" viewBox="0 0 120 20" aria-hidden="true"><path d="M10 17 C3 12 1 9 1 6 A4.5 4.5 0 0 1 10 4 A4.5 4.5 0 0 1 19 6 '
         'C19 9 17 12 10 17 Z M34 4 H52 V14 H40 L34 18 Z M64 10 L82 3 L76 18 L73 12 Z M104 2 H116 V18 L110 13 L104 18 Z"/></svg>')


def feed():
    tiles = ''.join(f'''<div class="tile ptile{" d" if c[2] else ""}">{fab(c[0], c[1])}<div class="ov">{GLYPH[f]}<span class="t">{cover}</span></div></div>'''
                    for _, s_, f, cover, c in FEED)
    hl = ''.join(f'<span><i>{fab(k, sd)}</i>{x}</span>' for x, k, sd in (('Sessions', 'kohl', 61), ('Rooms', 'bone', 62), ('Flurys', 'rani', 63), ('Night Map', 'midnight', 64)))
    body = f'''<div class="stack-l grow">
<h2 class="h1">The grid on Saturday 12 December.</h2>
<div class="feed">
  <div class="phone" role="img" aria-label="A phone showing the @theparkhotels profile and its nine latest posts">
    <div class="ph-head"><span class="av">{P_MARK}</span><span class="hd"><b>theparkhotels</b><span>Anything but ordinary. Park Street, everywhere.</span></span></div>
    <div class="btns"><span>Follow</span><span>Message</span><span>Contact</span></div>
    <div class="hl">{hl}</div>
    <div class="pgrid">{tiles}</div>
  </div>
  <div class="post">
    <div class="post-head"><span class="av">{P_MARK}</span><span><b>theparkhotels</b><span>Someplace Else, Kolkata</span></span></div>
    <div class="tile post-img">{fab('kohl', 51)}<div class="ov">{GLYPH['reel']}<span class="t">Park Street still plays</span></div></div>
    {ICONS}
    <p class="cap"><b>theparkhotels</b> Set 01 is up. One take at Someplace Else, Park Street. Message us for a table on Saturday.</p>
    <p class="label mute">Sat 12 Dec · The Sessions · Reel, with the full set on YouTube</p>
  </div>
</div></div>'''
    return slide('feed', 'The idea · the grid', body, src='A mock-up of the grid. Cloth stands in for photography; series, dates and copy are Mask360’s proposal.')


def voice():
    posts = [('Carousel · Who Played', 'Last night at Someplace Else. Swipe for the set list.', ('indigo', 71)),
             ('Reel · The 3 a.m. Menu', 'The kitchen just ate. Tomorrow, it’s on the menu.', ('midnight', 72)),
             ('Reel · Chef’s Counter', 'Thirty seconds at the pass. Tuesday, 9 p.m., Fire.', ('shaadi', 73))]
    c = ''.join(f'''<div class="vpost"><div class="tile vimg">{fab(k, sd)}</div><p class="label mute">theparkhotels · {a}</p><p class="say">{b}</p></div>'''
                for a, b, (k, sd) in posts)
    body = f'''<div class="stack-l grow">
<h2 class="h1">How the feed sounds.</h2>
<div class="row c3 top">{c}</div>
<div class="terms" style="margin-top:auto">
  <div><span class="no label">01</span><p class="h3">Name the place and the time</p><p class="mt-s ink2">Park Street at 11:40 p.m. carries the night.</p></div>
  <div><span class="no label">02</span><p class="h3">Twenty words at most</p><p class="mt-s ink2">The picture does the rest.</p></div>
  <div><span class="no label">03</span><p class="h3">Talk like the night manager</p><p class="mt-s ink2">Warm, sure, and in on the secret.</p></div>
</div></div>'''
    return slide('voice', 'The idea · voice', body, src='Sample captions, written by Mask360. Venues to confirm with the brand team.')


def _idea_page(sid, no, pillar, name, drawing, headline, text, extra, src):
    body = f'''<div class="row c-6-6 grow">
<div class="pic">{drawing}<div class="ov"><span class="no">{no}</span><span class="label">Concept drawing</span></div></div>
<div class="stack-l">
  <span class="label">{pillar} · {name}</span>
  <h2 class="h1">{headline}</h2>
  <p class="f-l ink2">{text}</p>
  {extra}
</div>
</div>'''
    return slide(sid, f'The idea · {name}', body, src=src)


def _posts(drawing, caption):
    return f'''<div class="art phones">{drawing}</div>
  <div class="rule"><p class="label mute">Sample caption</p><p class="mt-s ink2">{caption}</p></div>'''


def sessions():
    return _idea_page('sessions', 'No. 01', 'After Hours', 'The Sessions', art.stage(), 'Someplace Else, one take a month.',
                      'A live set filmed at Someplace Else in a single take, with bands playing their own songs. Reels from the set '
                      'run all month and the full set goes on YouTube. Then Agni in Delhi, and each city’s own venue.',
                      _posts(art.phones(), 'Saturday, 11:40 p.m. Someplace Else, Park Street. One take, start to finish. The full set is on YouTube.'),
                      'Concept drawings. Bands play original songs and sign a release. No drinks brands in frame.')


def reel():
    beats = [('0 to 3', 'The hook', 'The first chord over 11:40 p.m., Park Street, on screen.'),
             ('3 to 10', 'The walk', 'One take through the crowd to the stage.'),
             ('10 to 25', 'The chorus', 'The faces in the room, close.'),
             ('25 to 30', 'The last note', 'Wide: the lights, the stage, the street.'),
             ('End card', 'The full set', 'On YouTube. Message us for a table.')]
    cells = ''.join(f'''<div class="beat"><div class="art">{art.reel_frame(i)}</div><p class="label mute">{t}{" seconds" if i < 4 else ""}</p>
<p class="h3">{a}</p><p class="ink2">{b}</p></div>''' for i, (t, a, b) in enumerate(beats))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Set 01, second by second.</h2>
  <p class="ink2 lede-s">A thirty-second Reel cut from the one take, made for the first three seconds and for the save.</p>
</div>
<div class="row c5 grow vc reel">{cells}</div>
<div class="spec"><div><p class="h4">Sound: the band’s own track, as original audio</p></div><div><p class="h4">Cover: the 11:40 frame, for the grid</p></div></div>
</div>'''
    return slide('reel', 'The idea · the Reel', body, src='A sample cut, written by Mask360. Timings in seconds.')


def room():
    return _idea_page('room', 'No. 02', 'By Design', 'Room 1967', art.suite(), 'One suite a year, revealed on the feed.',
                      'A young Indian designer remakes one suite at THE Park every year. We film it from the empty room to the '
                      'first guest, one Reel a week, and open a waiting list in stories.',
                      _posts(art.room_posts(), 'One designer. One year. One suite. The waiting list is in our bio.'),
                      'Concept drawings. The designer and the hotel to choose with the brand team.')


def flurys():
    return _idea_page('flurys', 'No. 03', 'The Table', 'Flurys 100', art.cup(), 'A hundred stories for a hundred years.',
                      'Flurys turns 100 in 2027. All year we tell one story at a time: a regular, a recipe, a baker at 4 a.m. '
                      'From the tea room on Park Street to the 24-hour café in Gurugram.',
                      _posts(art.flurys_posts(), 'Regular No. 001. Same table, every Sunday. Swipe for the order.'),
                      'Concept drawings. Flurys opened its 24-hour Gurugram café on 7 August 2026.')


def ch_run():
    return chapter('ch-run', '03', 'How it runs', 'A month on the feed, the handles, the people and the numbers.', ('kohl', 23))


# a month on the feed: the series by weekday (pillar class a After Hours, b By Design, c The Table, d The City), then the one-offs
WEEKLY = {0: [('a', 'Who Played'), ('d', 'Night Shift')], 1: [('c', 'Chef’s Counter')], 2: [('b', 'The Object')],
          3: [('a', 'The 3 a.m. Menu')], 4: [('a', 'Who’s Playing')], 5: [('d', 'The Night Map')], 6: [('c', 'The Recipe')]}
SPECIAL = {dt.date(2026, 12, 1): [('a', 'New Year’s Eve: tables open')],
           dt.date(2026, 12, 8): [('c', 'Christmas at Flurys: the menu')],
           dt.date(2026, 12, 9): [('b', 'Room 1967: the search opens')],
           dt.date(2026, 12, 12): [('a', 'The Sessions · Set 01')],
           dt.date(2026, 12, 16): [('b', 'The Architects')],
           dt.date(2026, 12, 17): [('a', 'Two weeks to New Year’s Eve')],
           dt.date(2026, 12, 24): [('a', 'Christmas Eve on Park Street')],
           dt.date(2026, 12, 25): [('a', 'Christmas on Park Street'), ('c', 'Christmas at Flurys')],
           dt.date(2026, 12, 28): [('a', 'Last tables for New Year’s Eve')],
           dt.date(2026, 12, 31): [('a', 'New Year’s Eve at every THE Park')],
           dt.date(2027, 1, 1): [('a', 'Who Played: New Year’s Eve')]}


def calendar():
    start = dt.date(2026, 11, 30)  # the Monday before 1 December
    head = ''.join(f'<span class="wd label">{d}</span>' for d in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
    cells = []
    for i in range(35):
        day = start + dt.timedelta(days=i)
        tags = SPECIAL.get(day, WEEKLY[day.weekday()])
        cls = 'day'
        if day in SPECIAL:
            cls += ' tent'
        elif day.month != 12:
            cls += ' out'
        elif day.day > 7:
            cls += ' rep'  # a weekly repeat, folded away on phones
        t = ''.join(f'<span class="tag {k}">{x}</span>' for k, x in tags)
        cells.append(f'<div class="{cls}"><span class="n" data-wd="{day:%a}">{day.day}</span>{t}</div>')
    key = ''.join(f'<span class="tag label {k}">{n}</span>' for k, n in (('a', 'After Hours'), ('b', 'By Design'), ('c', 'The Table'), ('d', 'The City')))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">December on the feed.</h2>
  <div class="cal-key" style="align-self:end">{key}</div>
</div>
<div class="cal">{head}{''.join(cells)}</div>
<p class="cal-note ink2">The weekly series repeat all month.</p>
</div>'''
    return slide('calendar', 'How it runs · a month', body, src='Assumes a start on 16 November 2026. Shaded days are one-off posts; the big nights go on sale a fortnight ahead.')


def _handles_tree():
    items = ''.join(f'<li><b>{n}</b><span>{v}</span><em>{w}. {h}.</em></li>' for n, v, w, h in art.HANDLES)
    return f'<div class="map-tree"><p class="idea">@theparkhotels · the group feed</p><div class="br"><ul>{items}</ul></div></div>'


def handles():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Every brand speaks in its own voice.</h2>
  <p class="ink2 lede-s">Each hotel films its own version of the series, and the best of each city runs on the group feed. A new hotel opens with nine posts ready.</p>
</div>
<div class="map">{art.handles_map()}{_handles_tree()}</div>
</div>'''
    return slide('handles', 'How it runs · the handles', body, src='Venue accounts to confirm with the brand team. Voices and roles are Mask360’s proposal.')


def community():
    cols = [('Artists', 'A new band each month for The Sessions. One designer a year for Room 1967.'),
            ('Regulars', 'Their photos, reposted with credit. Their nominations for Night Shift.'),
            ('Creators', 'One city creator a month spends The Night Off with us, as a collab Reel.'),
            ('Direct messages', 'Every message gets a person, and a table if they want one.')]
    c = ''.join(f'''<div class="ppl"><div class="art">{art.people(i)}</div><div class="rule-plan"><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div></div>'''
                for i, (a, b) in enumerate(cols))
    body = f'''<div class="stack-l grow">
<h2 class="h1">The people who make the feed.</h2>
<div class="row c4 grow vc">{c}</div>
</div>'''
    return slide('community', 'How it runs · community', body, src='Artists and creators to agree with each hotel.')


def measure():
    rows = [['Skip rate and watch time, per Reel series', 'Instagram Insights, weekly'],
            ['Saves and shares per post', 'Insights, against your last 30 posts'],
            ['WhatsApp chats from social', 'A tagged link per series'],
            ['Tables booked from social', 'A code per venue'],
            ['Room nights booked direct', 'Booking engine, tagged links']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Measured in your numbers.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('2×', 'saves per post, against your last 30', 'draft threshold, set from your data in week 2')}</div>
  {table(['What we count', 'How'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('measure', 'How it runs · measurement', body, src='First readout: week of 22 February 2027. A series that trails at the readout is replaced.')


def mask360():
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-7-5" style="align-items:end">
  <div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div>
  <p class="lede">We run social and content for luxury and hospitality brands in India and the UAE.</p>
</div>
<div class="row c3 pillars mt-m">
  <div><p class="label mute">Hospitality we have worked with</p><p class="mt-s f-l">Anantara Jewel Bagh, Jaipur · Alta Stella, Onrique and DEA, Mumbai · Atlantis The Royal and SANA, Dubai</p></div>
  <div><p class="label mute">Feeds we run</p><p class="mt-s f-l">The Penthouse at St. Regis Mumbai · Moxy Mumbai</p></div>
  <div><p class="label mute">A lounge we built</p><div class="mt-s">{stat('530', 'tickets at ₹75,000 each', 'Nexa Platinum Lounge, Lollapalooza India')}</div></div>
</div>
<div class="rule mt-m"><p class="label mute">Luxury we have worked with</p><p class="mt-s">Dior · Ferrari India · L’Oréal · Dyson</p></div>
</div>'''
    return slide('mask360', 'Mask360', body, dark=True, src='From Mask360’s own records.')


def next_steps():
    body = '''<div class="row c-6-6 grow" style="align-items:end">
<div class="stack-l">
  <h2 class="h-display" style="font-size:calc(var(--u)*5.4)">Put us in the room.</h2>
  <p class="lede">Shortlist Mask360 and we bring the full plan to the pitch.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Shortlist Mask360.</li><li>Thirty minutes with the brand team.</li><li>The pitch: the full plan, handle by handle.</li><li>Set 01 at Someplace Else in December.</li></ol>
  <div class="rule-plan"><p class="h3">Kaavish Ramchandani · Founder, Mask360</p><p class="ink2 mt-s">kaavish@mask360.agency · +91 959 107 5100</p><p class="ink2">mask360.agency · credentials at mask360.work</p></div>
</div></div>'''
    return slide('next', 'Next steps', body)


def close():
    body = f'''<div class="grow" style="display:grid;place-items:center">
<div class="close-mark">
  <svg class="w" viewBox="{P_VIEW}" role="img" aria-label="The Park Hotels"><use href="#logo-p"/></svg>
  <span class="label line">Mask360 · Park Street, everywhere · October 2026</span>
  {M_MARK}
</div></div>'''
    return slide('close', 'The Park Hotels × Mask360', body, bare=True, dark=True, cloth=('ink', 11))


def sources():
    items = ''.join(f'<div><p class="h4">{h}</p><p class="f-s ink2 mt-s">{t}</p></div>' for h, t in SOURCES)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Sources.</h2>
<div class="srcs">{items}</div>
</div>'''
    return slide('sources', 'Appendix · sources', body, src='Every number in the deck, with where it came from.')


def slides():
    out = [cover(), promise(), brief(), ch_today(), today(), channels(), rule(), insight(), ch_idea(), mindmap(), mix(), feed(),
           voice(), sessions(), reel(), room(), flurys(), ch_run(), calendar(), handles(), community(), measure(), mask360(),
           next_steps(), close(), sources()]
    assert [s.split('id="', 1)[1].split('"', 1)[0] for s in out] == ORDER, 'ORDER is out of step with the slides'
    return out
