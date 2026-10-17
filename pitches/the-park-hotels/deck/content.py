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
         'voice', 'sessions', 'room', 'flurys', 'ch-run', 'calendar', 'handles', 'community', 'path', 'measure', 'mask360', 'next',
         'close', 'sources']


def pg(sid):
    return f'{ORDER.index(sid) + 1:02d}'


# full sources, shown on the last page; each slide carries a short version
SOURCES = [
    ('The Park today', 'Apeejay Surrendra Park Hotels Q1 FY27 results, Aug 2026: revenue ₹166.8 crore, up 8.1%; occupancy 92%; RevPAR about '
     '₹6,858 (Investywise, ScanX). Food, beverage, nightlife and lifestyle dining about 43% of revenue: IDBI Capital result review, '
     '19 Aug 2026. Flurys 111 stores: Q1 FY27 investor presentation. 42 hotels today and 87 by FY30: company investor material, '
     'Q1 FY27 and 2 Sep 2026 (Multibagg; filing to NSE).'),
    ('Channels', 'As linked from theparkhotels.com, October 2026: Instagram @theparkhotels, YouTube /theparkhotels, Facebook The Park '
     'Hotels, X @parkhotelsindia, LinkedIn The Park Hotels, Pinterest @theparkhotels. Spotify and WhatsApp are Mask360’s proposal.'),
    ('The brands', 'The Park Hotels corporate overview: five hotel brands, plus Flurys. Zone by The Park at launch: design-conscious and '
     'price-conscious (eHotelier). Ran Baas The Palace, Patiala: 35 suites, opened January 2025, Prix Versailles world’s most '
     'beautiful hotels 2025 (Robb Report India, Time Out).'),
    ('Park Street', 'The Park Kolkata opened in 1967 on Park Street, which gave the group its name (Hotel Designs, Entrepreneur India). '
     'Venues from THE Park Kolkata and THE Park New Delhi dining pages: Someplace Else, Tantra, Roxy, Agni, Aqua, Fire. THE Park '
     'Bangalore was designed by Terence Conran. “Anything but ordinary” has been the line since the 2013 rebrand (Travel Trends Today).'),
    ('The content', 'Flurys turns 100 in 2027 and opened a 24-hour café in Gurugram on 7 Aug 2026 (company announcement via Sahi). The '
     'Kolkata Christmas Festival on Park Street is co-organised by the Apeejay Surrendra Group (News Arena). Pillars, series, '
     'formats, cadence, sample posts and captions are Mask360’s proposal.'),
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
    rows = [['Know the category', 'Rate, covers and bookings, read through the feed.', f'{pg("today")} · {pg("measure")}'],
            ['Think beyond the obvious', 'Sixteen series only THE Park can post.', pg('mindmap')],
            ['Have the work to back it up', 'Hospitality accounts, feeds we run, a lounge we built.', pg('mask360')],
            ['An upcoming pitch', 'This is our point of view. We bring the full plan to the pitch.', pg('next')]]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What you asked for.</h2>
<div class="grow v-center">{table(['You asked', 'Our answer', 'Page'], rows, cls='tbl roomy brief stackable', right=(2,))}</div>
</div>'''
    return slide('brief', 'Your brief', body, src='From your call for agencies on LinkedIn.')


def ch_today():
    return chapter('ch-today', '01', 'The Park on social', 'Six channels today, five hotel brands and Flurys, and one feed to lead them.',
                   ('midnight', 21))


def today():
    body = f'''<div class="stack-l grow">
<h2 class="h1">The rooms are full. The feed sells the nights.</h2>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat('92%', 'occupancy', 'Q1 FY27')}
  {stat('43%', 'of revenue from food, drink and nightlife', 'Q1 FY27')}
  {stat('6,858', 'revenue per available room, in rupees', 'Q1 FY27')}
  {stat('42', 'hotels in 32 cities', 'October 2026')}
  {stat('87', 'hotels planned by FY2030', 'each one a new handle to launch')}
  {stat('111', 'Flurys stores', '100 years old in 2027')}
</div></div>'''
    return slide('today', 'The Park on social · the numbers', body, src='Sources: Q1 FY27 results and investor material, 2026. Full list at the end.')


CHANNELS = [  # channel, handle or status, its job, a week
    ('Instagram', '@theparkhotels', 'The magazine: Reels, carousels, stories', '5 Reels, 2 carousels, stories daily'),
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
  <p class="ink2 lede-s">Two new ones carry the content further: Spotify for the music, WhatsApp for the booking.</p>
</div>
<div class="grow v-center">{table(['Channel', 'Its job', 'A week'], rows, cls='tbl brands tight stackable')}</div>
</div>'''
    return slide('channels', 'The Park on social · channels', body, src='Channels as linked from theparkhotels.com, October 2026. Cadence is Mask360’s proposal.')


def rule():
    feeds = ['Buffet flat-lays', 'Festive greeting cards', 'Drone shots of an empty pool', 'Room tours', 'Offer carousels']
    park = ['Who played last night', 'What the kitchen cooks at 3 a.m.', 'The people on the night shift', 'A room a designer made',
            'The city after dark']
    body = f'''<div class="stack-l grow">
<h2 class="h1">We post what only THE Park can.</h2>
<div class="row c2 grow vc">
  <div class="rule stack"><p class="label mute">What most hotel feeds post</p>{ul(feeds, 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label">What THE Park will post</p>{ul(park, 'list big-list')}</div>
</div></div>'''
    return slide('rule', 'The house rule', body, src='“Anything but ordinary” has been The Park’s line since 2013.')


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


def mindmap():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">The content map.</h2>
  <p class="ink2 lede-s">One idea, four pillars, sixteen series. Every series ends one tap from a table or a room.</p>
</div>
<div class="map">{art.content_map()}</div>
</div>'''
    return slide('mindmap', 'The idea · the content map', body, src='Pillars, series and formats are Mask360’s proposal.')


MIX = [  # pillar, share of posts, key class, cloth (kind, seed, dark text), formats, a week
    ('After Hours', 35, 'k1', ('kohl', 31, False), 'Reels · YouTube · Spotify', '3 posts a week'),
    ('The Table', 30, 'k3', ('shaadi', 33, False), 'Reels · carousels · stories', '2 posts a week'),
    ('The City', 20, 'k4', ('midnight', 34, False), 'Carousels · guides · DMs', '1 to 2 posts a week'),
    ('By Design', 15, 'k2', ('ivory', 32, True), 'Reels · carousels · Pinterest', '1 post a week'),
]


def mix():
    bar = ''.join(f'<i class="p{["k1", "k2", "k3", "k4"].index(k) + 1}" style="width:{s}%"></i>' for _, s, k, _, _, _ in MIX)
    cols = ''.join(f'''<div class="idea">{tile(c[0], c[1], f"{s}%", n, dark_text=c[2])}
<p class="key label {k}">{n}</p><p class="ink2">{f}</p><div class="rule"><p class="label mute">{w}</p></div></div>''' for n, s, k, c, f, w in MIX)
    body = f'''<div class="stack-l grow mix">
<div class="row c-7-5 top">
  <h2 class="h1">The mix, week by week.</h2>
  <p class="ink2 lede-s">The night leads, because the bars and tables are 43% of revenue.</p>
</div>
<div class="mixbar" role="img" aria-label="Share of posts: After Hours 35%, The Table 30%, The City 20%, By Design 15%">{bar}</div>
<div class="row c4 grow vc">{cols}</div>
</div>'''
    return slide('mix', 'The idea · the mix', body, src='Share of feed posts on @theparkhotels, Mask360’s proposal. Stories run daily on top.')


FEED = [  # date, series, format, cloth (kind, seed, dark text)
    ('Sat 12 Dec', 'The Sessions · Set 01', 'Reel', ('kohl', 51, False)),
    ('Thu 10 Dec', 'The 3 a.m. Menu', 'Reel', ('slate', 52, False)),
    ('Wed 9 Dec', 'Room 1967: the designer', 'Carousel', ('bone', 53, True)),
    ('Tue 8 Dec', 'Chef’s Counter', 'Reel', ('shaadi', 54, False)),
    ('Mon 7 Dec', 'Who Played', 'Carousel', ('indigo', 55, False)),
    ('Mon 7 Dec', 'Night Shift', 'Portrait carousel', ('midnight', 56, False)),
    ('Sun 6 Dec', 'The Recipe', 'Carousel', ('rani', 57, False)),
    ('Sat 5 Dec', 'The Night Map: Kolkata', 'Guide', ('sand', 58, True)),
    ('Wed 2 Dec', 'The Object', 'Reel', ('ivory', 59, True)),
]


def feed():
    tiles = ''.join(f'''<div class="tile ptile{" d" if c[2] else ""}">{fab(c[0], c[1])}<div class="ov"><span class="f">{f}</span><span class="t">{s}</span></div></div>'''
                    for _, s, f, c in FEED)
    week = ''.join(f'<span class="d label">{d}</span><span class="s">{s}</span><span class="ink2">{f}</span>' for d, s, f, _ in FEED)
    hl = ''.join(f'<span><i></i>{x}</span>' for x in ('Sessions', 'Rooms', 'Flurys', 'Night Map'))
    body = f'''<div class="stack-l grow">
<h2 class="h1">The first fortnight of December on @theparkhotels.</h2>
<div class="feed">
  <div class="phone" role="img" aria-label="A phone showing the @theparkhotels grid with nine posts">
    <div class="ph-head"><span class="av">{P_MARK}</span><span class="hd"><b>theparkhotels</b><span>Anything but ordinary. Park Street, everywhere.</span></span></div>
    <div class="hl">{hl}</div>
    <div class="pgrid">{tiles}</div>
  </div>
  <div class="week">{week}</div>
</div></div>'''
    return slide('feed', 'The idea · the grid', body, src='A mock-up of the grid. Cloth stands in for photography; series and dates are Mask360’s proposal.')


def voice():
    cards = [('Reel · The Sessions', 'Saturday, 11:40 p.m. Someplace Else, Park Street. One take, start to finish. The full set is on YouTube.'),
             ('Story · The 3 a.m. Menu', 'The kitchen just ate. Tomorrow, it’s on the menu.'),
             ('Carousel · Room 1967', 'One designer. One year. One suite. The waiting list is in our bio.')]
    c = ''.join(f'<div class="cap-card"><p class="label mute">{a}</p><p class="say">{b}</p></div>' for a, b in cards)
    body = f'''<div class="stack-l grow">
<h2 class="h1">How the feed sounds.</h2>
<div class="row c3 grow vc">{c}</div>
<div class="terms">
  <div><span class="no label">01</span><p class="h3">Name the place and the time</p><p class="mt-s ink2">Park Street at 11:40 p.m. carries the night.</p></div>
  <div><span class="no label">02</span><p class="h3">Twenty words at most</p><p class="mt-s ink2">The picture does the rest.</p></div>
  <div><span class="no label">03</span><p class="h3">Talk like the night manager</p><p class="mt-s ink2">Warm, sure, and in on the secret.</p></div>
</div></div>'''
    return slide('voice', 'The idea · voice', body, src='Sample captions, written by Mask360.')


def _idea_page(sid, no, name, drawing, headline, text, extra, src):
    body = f'''<div class="row c-6-6 grow">
<div class="pic">{drawing}<div class="ov"><span class="label">{no}</span><span class="label">Concept drawing</span></div></div>
<div class="stack-l">
  <span class="label">{name}</span>
  <h2 class="h1">{headline}</h2>
  <p class="f-l ink2">{text}</p>
  {extra}
</div>
</div>'''
    return slide(sid, f'The idea · {name}', body, src=src)


def _spec(formats):
    return '<div class="spec">' + ''.join(f'<div><p class="h4">{a}</p></div>' for a in formats) + '</div>'


def sessions():
    posts = f'''<div class="art phones">{art.phones()}</div>
  <div class="rule"><p class="label mute">Sample caption</p><p class="mt-s ink2">Saturday, 11:40 p.m. Someplace Else, Park Street. One take, start to finish. The full set is on YouTube.</p></div>'''
    return _idea_page('sessions', 'After Hours', 'The Sessions', art.stage(), 'Someplace Else, one take a month.',
                      'A live set filmed at Someplace Else in a single take, with bands playing their own songs. Cut for Reels, '
                      'posted in full on YouTube. Then Agni in Delhi, and each city’s own venue.',
                      posts, 'Concept drawings. Bands play original songs and sign a release. No drinks brands in frame.')


def room():
    return _idea_page('room', 'By Design', 'Room 1967', art.suite(), 'One suite a year, with its own launch night.',
                      'A young Indian designer remakes one suite at THE Park every year. We reveal it in three steps: a teaser, '
                      'a launch night, a waiting list. Each suite gives the press a new story.',
                      _spec(['A teaser in the feed', 'A launch night', 'A waiting list', 'Press on the day']),
                      'Concept drawing. The designer and the hotel to choose with the brand team.')


def flurys():
    return _idea_page('flurys', 'The Table', 'Flurys 100', art.cup(), 'A hundred stories for a hundred years.',
                      'Flurys turns 100 in 2027. All year we tell one story at a time: a regular, a recipe, a baker at 4 a.m. '
                      'From the tea room on Park Street to the 24-hour café in Gurugram.',
                      _spec(['100 regulars', '100 recipes', 'A centenary menu', 'Each new Flurys opens with it']),
                      'Concept drawing. Flurys opened its 24-hour Gurugram café on 7 August 2026.')


def ch_run():
    return chapter('ch-run', '03', 'How it runs', 'A month on the feed, the handles, the people and the numbers.', ('kohl', 23))


# a month on the feed: the series by weekday (pillar class a After Hours, b By Design, c The Table, d The City), then the big nights
WEEKLY = {0: [('a', 'Who Played'), ('d', 'Night Shift')], 1: [('c', 'Chef’s Counter')], 2: [('b', 'The Object')],
          3: [('a', 'The 3 a.m. Menu')], 4: [('a', 'Who’s playing tonight')], 5: [('d', 'The Night Map')], 6: [('c', 'The Recipe')]}
SPECIAL = {dt.date(2026, 12, 9): [('b', 'Room 1967: the designer')],
           dt.date(2026, 12, 12): [('a', 'The Sessions · Set 01')],
           dt.date(2026, 12, 24): [('a', 'Christmas Eve on Park Street')],
           dt.date(2026, 12, 25): [('a', 'Christmas on Park Street'), ('c', 'Christmas at Flurys')],
           dt.date(2026, 12, 31): [('a', 'New Year’s Eve, live from every THE Park')],
           dt.date(2027, 1, 1): [('a', 'Who Played: New Year’s Eve')]}


def calendar():
    start = dt.date(2026, 11, 30)  # the Monday before 1 December
    head = ''.join(f'<span class="wd label">{d}</span>' for d in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
    cells = []
    for i in range(35):
        day = start + dt.timedelta(days=i)
        tags = SPECIAL.get(day, WEEKLY[day.weekday()])
        cls = 'day' + (' tent' if day in SPECIAL and day.day in (24, 25, 31, 1) else '') + (' out' if day.month != 12 and day not in SPECIAL else '')
        t = ''.join(f'<span class="tag {k}">{x}</span>' for k, x in tags)
        cells.append(f'<div class="{cls}"><span class="n">{day.day}</span>{t}</div>')
    key = ''.join(f'<span class="tag label {k}">{n}</span>' for k, n in (('a', 'After Hours'), ('b', 'By Design'), ('c', 'The Table'), ('d', 'The City')))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">December on the feed.</h2>
  <div class="cal-key" style="align-self:end">{key}</div>
</div>
<div class="cal">{head}{''.join(cells)}</div>
</div>'''
    return slide('calendar', 'How it runs · a month', body, src='Assumes a start on 16 November 2026. Shaded days are the big nights; stories run daily on top.')


def handles():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">One attitude, six accents.</h2>
  <p class="ink2 lede-s">Every brand keeps its own voice, led by the group feed. Each new hotel opens with a launch kit for its handle.</p>
</div>
<div class="map">{art.handles_map()}</div>
</div>'''
    return slide('handles', 'How it runs · the handles', body, src='Ran Baas: Prix Versailles, world’s most beautiful hotels, 2025. Voices are Mask360’s proposal.')


def community():
    cols = [('Residents', 'A band, a designer and a writer in residence each season, behind The Sessions, Room 1967 and Don’t Check Out.'),
            ('Regulars', 'Their photos, reposted with credit. Their nominations for Night Shift.'),
            ('Creators', 'City creators film the night with us. No room tours.'),
            ('The DMs', 'Every message gets a person, and a table if they want one.')]
    c = ''.join(f'<div class="rule-plan"><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in cols)
    body = f'''<div class="stack-l grow">
<h2 class="h1">The people who make the feed.</h2>
<div class="row c4 grow vc">{c}</div>
</div>'''
    return slide('community', 'How it runs · community', body, src='Creators and residents to agree with each hotel.')


def path():
    steps = [('Seen', 'Reels and search, captioned for what people type.'), ('Saved', 'Saves and shares, the first signal we read.'),
             ('Asked', 'One tap from any post to a WhatsApp concierge.'), ('Booked', 'A table or a room, direct and tracked to the post.'),
             ('Back again', 'Regulars become the next post.')]
    cells = ''.join(f'<div><span class="dot label">{i + 1:02d}</span><p class="h3">{a}</p><p class="ink2 mt-s">{b}</p></div>'
                    for i, (a, b) in enumerate(steps))
    body = f'''<div class="stack-l grow">
<h2 class="h1">How every post reaches a table.</h2>
<div class="row c5 flow vc grow">{cells}</div>
</div>'''
    return slide('path', 'How it runs · post to table', body, src='Direct bookings also save the online travel agent’s commission.')


def measure():
    rows = [['Views and reach', 'Platform reports, weekly'], ['Saves and shares per post', 'The first sign someone plans to come'],
            ['Follower growth, by handle', 'Monthly, against upper-upscale peers'], ['DMs to the concierge', 'WhatsApp, logged daily'],
            ['Tables booked from social', 'A code per venue'], ['Room nights booked direct', 'Booking engine, tagged links']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Measured in your numbers.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('14', 'weeks to the first readout', 'week of 15 February 2027')}</div>
  {table(['What we count', 'How'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('measure', 'How it runs · measurement', body, src='Targets set with the brand team against today’s baselines.')


def mask360():
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-7-5" style="align-items:end">
  <div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div>
  <p class="lede">A creative and content agency for luxury and hospitality brands, in India and the UAE.</p>
</div>
<div class="row c3 pillars mt-m">
  <div><p class="label mute">Hospitality we work with</p><p class="mt-s f-l">Anantara Jewel Bagh, Jaipur · The St. Regis Mumbai · Moxy Mumbai · Alta Stella, Onrique and DEA, Mumbai · Atlantis The Royal and SANA, Dubai</p></div>
  <div><p class="label mute">Feeds we run</p><p class="mt-s f-l">The Penthouse at St. Regis Mumbai · Moxy Mumbai</p></div>
  <div><p class="label mute">A lounge we built</p><div class="mt-s">{stat('530', 'tickets at ₹75,000 each', 'Nexa Platinum Lounge, Lollapalooza India')}</div></div>
</div>
<div class="rule mt-m"><p class="label mute">Also</p><p class="mt-s">Dior · Ferrari India · L’Oréal · Dyson · Lollapalooza India</p></div>
</div>'''
    return slide('mask360', 'Mask360', body, dark=True, src='From Mask360’s own records.')


def next_steps():
    body = '''<div class="row c-6-6 grow" style="align-items:end">
<div class="stack-l">
  <h2 class="h-display" style="font-size:calc(var(--u)*5.4)">Put us in the room.</h2>
  <p class="lede">Shortlist Mask360 and we bring the full plan to the pitch.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Shortlist Mask360.</li><li>Thirty minutes with the brand team.</li><li>The pitch: the full plan, handle by handle.</li><li>The first Session in December.</li></ol>
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
           voice(), sessions(), room(), flurys(), ch_run(), calendar(), handles(), community(), path(), measure(), mask360(),
           next_steps(), close(), sources()]
    assert [s.split('id="', 1)[1].split('"', 1)[0] for s in out] == ORDER, 'ORDER is out of step with the slides'
    return out
