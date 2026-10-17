"""Slide copy for Mask360's proposal to The Park Hotels. The Westside v4 deck's way of writing: a headline, a line or two,
the numbers, and a one-line source on each slide; the full sources are on the last page. Facts come from
pitches/the-park-hotels/README.md, which lists every source. The look is Westside v4's, kept as it is."""
import art
from kit import slide, stat, ul, table, tile, chapter, M_MARK

TITLE = 'The Park Hotels × Mask360'
DESCRIPTION = ('Mask360’s proposal to The Park Hotels, October 2026: Park Street, everywhere. A social platform that sells '
               'THE Park’s nights, tables and new hotels, measured in covers and direct bookings.')

# the slides in deck order; page references on the slides are looked up here
ORDER = ['cover', 'promise', 'brief', 'ch-today', 'today', 'growth', 'brands', 'rule', 'insight', 'ch-idea', 'collections',
         'ideas', 'sessions', 'room', 'flurys', 'ch-run', 'days', 'path', 'measure', 'mask360', 'next', 'close', 'sources']


def pg(sid):
    return f'{ORDER.index(sid) + 1:02d}'


# full sources, shown on the last page; each slide carries a short version
SOURCES = [
    ('The Park today', 'Apeejay Surrendra Park Hotels Q1 FY27 results, Aug 2026: revenue ₹166.8 crore, up 8.1%; occupancy 92%; RevPAR about '
     '₹6,858 (Investywise, ScanX). Food, beverage, nightlife and lifestyle dining about 43% of revenue: IDBI Capital result review, '
     '19 Aug 2026. Flurys 111 stores: Q1 FY27 investor presentation. Management guides to high single-digit growth in room rate.'),
    ('Growth', 'Priya Paul to Business Traveller, 8 Oct 2026: 42 hotels in 32 cities, five THE Park hotels under construction. Priya Paul to '
     'Breaking Travel News, 2026: 85 hotels by FY2030. Zone and Zone Connect openings in Darjeeling, Gangtok and Katra, Mar 2026 (BW Hotelier); '
     'Ayodhya and Ujjain signed, Apr 2026 (Construction World); Bharatpur signed, 1 Oct 2026 (Hospibuz). THE Park Juhu, Mumbai, due mid-2027.'),
    ('The brands', 'The Park Hotels corporate overview: five brands. Zone by The Park at launch, Priya Paul: “fun and zippy” (Hotels Magazine, '
     'eHotelier). Ran Baas The Palace, Patiala: 35 suites, opened January 2025, Prix Versailles world’s most beautiful hotels 2025 '
     '(Robb Report India, Time Out).'),
    ('Park Street', 'The Park Kolkata opened in 1967 on Park Street, which gave the group its name (Hotel Designs, Entrepreneur India). '
     'Venues from THE Park Kolkata and THE Park New Delhi dining pages: Someplace Else, Tantra, Roxy, Agni, Aqua, Fire. '
     '“Anything but ordinary” has been the line since the 2013 rebrand (Travel Trends Today).'),
    ('The ideas', '80% of Indian travellers plan to spend most of their stay at the property, against 51% globally: Booking.com, as reported '
     'by Outlook Traveller. Flurys turns 100 in 2027 and opened a 24-hour café in Gurugram on 7 Aug 2026 (company announcement via Sahi). '
     'Idea names, formats and plans are Mask360’s proposal.'),
    ('The calendar', 'The Kolkata Christmas Festival on Park Street is co-organised by the Apeejay Surrendra Group (News Arena). The Apeejay '
     'Kolkata Literary Festival runs in January; the 17th edition ran 9 to 11 January 2026 (t2online).'),
]


def cover():
    body = f'''<div class="stack-l grow" style="justify-content:space-between">
<div class="big-wm" aria-label="The Park Hotels"><span class="t" aria-hidden="true">The Park Hotels</span></div>
<div class="cover-foot">
  <div class="stack-l">
    <span class="label">A proposal from Mask360 · October 2026</span>
    <h1 class="h-display" style="max-width:11em">Park Street, everywhere.</h1>
  </div>
  {M_MARK}
</div></div>'''
    return slide('cover', 'Proposal', body, src='For the brand team at The Park Hotels · Confidential', bare=True, dark=True, cls='cover scrim', cloth=('kohl', 7))


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">We will make THE Park the address every city <u>goes out to</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">01</span><p class="h3">Worth more a night</p><p class="mt-s ink2">Desire is what carries the room rate.</p></div>
  <div><span class="no label">02</span><p class="h3">Full tables</p><p class="mt-s ink2">The city at your bars and restaurants, every night.</p></div>
  <div><span class="no label">03</span><p class="h3">Every opening, a following</p><p class="mt-s ink2">About 40 new hotels by 2030, each one awaited.</p></div>
</div>'''
    return slide('promise', 'Our promise', body)


def brief():
    rows = [['Know the category', 'Rate, covers and direct bookings, in your numbers.', pg('today')],
            ['Think beyond the obvious', 'If another hotel could post it, we don’t.', pg('rule')],
            ['Have the work to back it up', 'Hospitality and luxury brands, named.', pg('mask360')],
            ['An upcoming pitch', 'A point of view today. The full plan in the room.', pg('next')]]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What you asked for.</h2>
<div class="grow v-center">{table(['You asked', 'Our answer', 'Page'], rows, cls='tbl roomy brief stackable', right=(2,))}</div>
</div>'''
    return slide('brief', 'Your brief', body, src='From your call for agencies on LinkedIn, October 2026.')


def ch_today():
    return chapter('ch-today', '01', 'The Park today', 'Full rooms, famous bars, and twice the hotels by 2030.', ('midnight', 21))


def today():
    body = f'''<div class="stack-l grow">
<h2 class="h1">The Park is full. Growth now comes from desire.</h2>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat('1967', 'opened on Park Street, Kolkata', 'the name comes from the street')}
  {stat('92%', 'occupancy, April to June 2026', 'Q1 FY27')}
  {stat('43%', 'of revenue from food, drink and nightlife', 'Q1 FY27')}
  {stat('42', 'hotels in 32 cities', 'October 2026')}
  {stat('85', 'hotels planned by FY2030', 'about twice today')}
  {stat('111', 'Flurys stores', '100 years old in 2027')}
</div></div>'''
    return slide('today', 'The Park today', body, src='Sources: Q1 FY27 results and investor material; Priya Paul interviews, 2026. Full list at the end.')


def growth():
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:space-between">
  <h2 class="h1">42 hotels today. 85 by 2030.</h2>
  <div class="art" style="height:auto">{art.hotels_grid()}</div>
  <p class="f-s ink2">One square per hotel. Ink is open today.</p>
</div>
<div class="stack-l" style="justify-content:center">
  <div class="rule">{stat('5', 'THE Park hotels under construction')}</div>
  <div class="rule">{stat('3', 'Zone Connect towns signed this year', 'Ayodhya, Ujjain, Bharatpur')}</div>
  <div class="rule">{stat('2027', 'THE Park Juhu, Mumbai, opens mid-year')}</div>
  <p class="lede">Each new hotel should open to a waiting audience.</p>
</div></div>'''
    return slide('growth', 'The Park today · growth', body, src='Sources: Priya Paul to Business Traveller, Oct 2026; company announcements, Mar to Oct 2026.')


BRANDS = [  # brand, what it is, role on social, voice
    ('THE Park', 'design hotels, big cities', 'Culture after dark, by design', 'Seductive'),
    ('THE Park Collection', 'Ran Baas, Patiala', 'Slow, storied, royal', 'Unhurried'),
    ('Zone by The Park', 'hill and culture towns', 'Weekend discovery', 'Fun and zippy'),
    ('Zone Connect', 'pilgrim and business towns', 'Local, in the local language', 'Warm'),
    ('Stop by Zone', 'essential stays', 'Price and place, said plainly', 'Direct'),
    ('Flurys', '111 stores', 'The centenary, all of 2027', 'Nostalgic'),
]


def brands():
    rows = [[f'<b>{n}</b><br><span class="mute f-s">{s}</span>', r, v] for n, s, r, v in BRANDS]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Five brands. One attitude.</h2>
<div class="grow v-center">{table(['Brand', 'Its role on social', 'Its voice'], rows, cls='tbl rivals stackable')}</div>
</div>'''
    return slide('brands', 'The Park today · the brands', body,
                 src='“Fun and zippy” is Priya Paul on Zone. Ran Baas: Prix Versailles, world’s most beautiful hotels, 2025.')


def rule():
    feeds = ['Buffet flat-lays', 'Festive greeting cards', 'Drone shots of an empty pool', 'Room tours', 'Offer carousels']
    park = ['Who played last night', 'What the kitchen cooks at 3 a.m.', 'The people on the night shift', 'A room a designer made',
            'The city after dark']
    body = f'''<div class="stack-l grow">
<h2 class="h1">If another hotel could post it, we don’t.</h2>
<div class="row c2 grow vc">
  <div class="rule stack"><p class="label mute">What hotel feeds post</p>{ul(feeds, 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label">What THE Park posts</p>{ul(park, 'list big-list')}</div>
</div></div>'''
    return slide('rule', 'The house rule', body, src='“Anything but ordinary” has been The Park’s line since 2013.')


def insight():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">The Park is named after a <u>street</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">1967</span><p class="h3">The first hotel</p><p class="mt-s ink2">The Park opens on Park Street, Kolkata.</p></div>
  <div><span class="no label">The street</span><p class="h3">Jazz, cabaret, late dinners</p><p class="mt-s ink2">Park Street was where Calcutta went out.</p></div>
  <div><span class="no label">Since</span><p class="h3">The scene kept going</p><p class="mt-s ink2">Someplace Else, Tantra, Agni, Aqua.</p></div>
</div>'''
    return slide('insight', 'The insight', body, src='Sources: The Park Hotels history; THE Park Kolkata and New Delhi dining. Full list at the end.')


def ch_idea():
    return chapter('ch-idea', '02', 'Park Street, everywhere.',
                   'Every THE Park becomes its city’s Park Street. Social becomes the street’s magazine.', ('shaadi', 12))


COLLECTIONS = [  # no, name, cloth (kind, seed, dark text), line, where it runs
    ('No. 01', 'After Hours', ('kohl', 31, False), 'Live sets, DJ nights, the bartenders as regulars.', 'Reels · YouTube · Spotify'),
    ('No. 02', 'By Design', ('ivory', 32, True), 'Rooms and art shot like a fashion campaign.', 'Instagram · Pinterest · press'),
    ('No. 03', 'The Table', ('shaadi', 33, False), 'Chefs, signature plates and Flurys at 100.', 'Reels · menus · creators'),
    ('No. 04', 'The City', ('midnight', 34, False), 'Each city told by the people who work its nights.', 'Search · Maps · Reels'),
]


def collections():
    cols = ''.join(f'''<div class="idea">{tile(c[0], c[1], n, t, dark_text=c[2])}<p class="idea-d">{d}</p>
<div class="rule"><p class="label mute">{w}</p></div></div>''' for n, t, c, d, w in COLLECTIONS)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Four collections, one street.</h2>
  <p class="ink2 lede-s">Released in seasons, the way a fashion house drops a line.</p>
</div>
<div class="row c4 grow vc">{cols}</div>
</div>'''
    return slide('collections', 'The idea · four collections', body, src='Formats and channels are Mask360’s proposal.')


IDEAS = [  # title, line, cloth (kind, seed, dark text)
    ('The Sessions', 'One-take live sets from Someplace Else.', ('kohl', 41, False)),
    ('The 3 a.m. Menu', 'What the kitchen cooks after the club closes.', ('slate', 42, False)),
    ('Room 1967', 'One suite a year, made by a young Indian designer.', ('bone', 43, True)),
    ('Night Shift', 'Portraits of the people who work the night.', ('midnight', 44, False)),
    ('Don’t Check Out', 'Creators stay 48 hours and never leave the hotel.', ('indigo', 45, False)),
    ('Flurys 100', 'A hundred regulars, recipes and stories.', ('rani', 46, False)),
]


def ideas():
    tiles = ''.join(f'<div>{tile(k, sd, f"No. {i + 1:02d}", t, dark_text=d)}<p class="f-s ink2 mt-s">{line}</p></div>'
                    for i, (t, line, (k, sd, d)) in enumerate(IDEAS))
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:space-between">
  <h2 class="h1">Six ideas from the lookbook.</h2>
  <div class="stack-l">
    <div class="rule">{stat('80%', 'of Indian travellers plan to spend most of their stay at the hotel', 'against 51% worldwide')}</div>
    <p class="lede">Every idea gives them a reason to stay in, and the city a reason to come over.</p>
  </div>
</div>
<div class="stories vc">{tiles}</div>
</div>'''
    return slide('ideas', 'The idea · six ideas', body, src='80%: Booking.com, as reported by Outlook Traveller. Ideas are Mask360’s proposal.')


def _idea_page(sid, no, name, drawing, headline, text, formats, src):
    f = ''.join(f'<div><p class="h4">{a}</p></div>' for a in formats)
    body = f'''<div class="row c-6-6 grow">
<div class="pic">{drawing}<div class="ov"><span class="no">{no}</span><span class="label">Concept drawing</span></div></div>
<div class="stack-l">
  <span class="label">{name}</span>
  <h2 class="h1">{headline}</h2>
  <p class="f-l ink2">{text}</p>
  <div class="spec">{f}</div>
</div>
</div>'''
    return slide(sid, f'The idea · {name}', body, src=src)


def sessions():
    return _idea_page('sessions', 'No. 01', 'The Sessions', art.stage(), 'Kolkata’s live-music pub, one take a month.',
                      'A live set filmed at Someplace Else in a single take. Cut for Reels, posted in full on YouTube, kept on a '
                      'Spotify playlist. Then each city films its own venue.',
                      ['One take, no edits', 'The full set on YouTube', 'A playlist that grows', 'Agni in Delhi next'],
                      'Concept drawing. Venue line-up to agree with each hotel.')


def room():
    return _idea_page('room', 'No. 03', 'Room 1967', art.suite(), 'One suite a year, revealed like a runway show.',
                      'A young Indian designer remakes one suite at THE Park every year. We reveal it the way fashion drops a '
                      'collection: a teaser, a launch night, a waiting list. The design story stays new and earns press.',
                      ['A teaser in the feed', 'A launch night', 'A waiting list', 'Press on the day'],
                      'Concept drawing. The designer and the hotel to choose with the brand team.')


def flurys():
    return _idea_page('flurys', 'No. 06', 'Flurys 100', art.cup(), 'A hundred stories for a hundred years.',
                      'Flurys turns 100 in 2027. All year we tell one story at a time: a regular, a recipe, a baker at 4 a.m. '
                      'From the tea room on Park Street to the 24-hour café in Gurugram.',
                      ['100 regulars', '100 recipes', 'A centenary menu', 'Each new Flurys opens with it'],
                      'Concept drawing. Flurys opened its 24-hour Gurugram café on 7 August 2026.')


def ch_run():
    return chapter('ch-run', '03', 'How it runs', 'The next 100 days, the path to a table, and what we report.', ('kohl', 23))


def days():
    weeks = 14
    phases = [('Listen', 1, 4, 'line', 'Every handle audited, one voice book'),
              ('The Sessions', 4, 15, 'plan', 'First set in December, then monthly'),
              ('Christmas on Park Street', 5, 7, 'plan', 'Shot as one story with New Year’s Eve'),
              ('New Year’s Eve', 7, 8, 'ink', 'The biggest night of the year'),
              ('Literary festival', 8, 10, 'line', 'January, Kolkata'),
              ('Flurys 100', 10, 15, 'plan', 'The countdown begins'),
              ('Readout', 14, 15, 'ink', 'What moved, in your numbers')]
    head = ''.join(f'<span class="wk label">{i}</span>' for i in range(1, weeks + 1))
    rows = ''.join(f'<p class="h4 ph">{n}</p><i class="bar-{c}" style="grid-column:{s + 1}/{e + 1}"></i><p class="ink2 f-s note">{t}</p>'
                   for n, s, e, c, t in phases)
    body = f'''<div class="stack-l grow">
<h2 class="h1">The next 100 days hold the brand’s biggest nights.</h2>
<div class="gantt vc grow" style="grid-template-columns:calc(var(--u)*11) repeat({weeks},minmax(0,1fr))"><span></span>{head}{rows}</div>
<div class="row c3 dates">
  <div class="rule"><p class="label mute">Set up</p><p class="mt-s">16 November to 6 December</p></div>
  <div class="rule-plan"><p class="label">Live</p><p class="mt-s">7 December to 14 February</p></div>
  <div class="rule"><p class="label mute">Readout</p><p class="mt-s">Week of 15 February 2027</p></div>
</div></div>'''
    return slide('days', 'How it runs · the next 100 days', body, src='Dates assume a start on Monday 16 November 2026. Weeks run Monday to Sunday.')


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
    rows = [['Tables booked from social', 'WhatsApp and a code per venue'], ['Room nights booked direct', 'Booking engine, tagged links'],
            ['Share of voice', 'Against upper-upscale peers, monthly'], ['Saves and shares', 'Platform reports, weekly'],
            ['Enquiries per new hotel', 'The first 90 days after opening']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Measured in your numbers.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('1', 'page a month', 'in the numbers the brand team reports')}</div>
  {table(['What we count', 'How'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('measure', 'How it runs · measurement', body, src='Targets set with the brand team against today’s baselines.')


def mask360():
    pillars = [('Social', 'Series, creators, pages'), ('Content', 'Sessions, shoots, edits'), ('Events', 'Launch nights and residencies'),
               ('Measurement', 'Covers and direct bookings')]
    p = ''.join(f'<div><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in pillars)
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-7-5" style="align-items:end">
  <div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div>
  <p class="lede">A creative and content agency in India and the UAE.</p>
</div>
<div class="row c4 pillars mt-m">{p}</div>
<div class="rule mt-m"><p class="label mute">Brands we have worked with</p><p class="mt-s f-l">Anantara · Atlantis The Royal · St. Regis · Lollapalooza India · Dior · Ferrari · Rolls-Royce · L’Oréal · Dyson · FCUK Beauty · Swisse · Zorae · Rustomjee · Chandak Group</p></div>
</div>'''
    return slide('mask360', 'Mask360', body, dark=True)


def next_steps():
    body = '''<div class="row c-6-6 grow" style="align-items:end">
<div class="stack-l">
  <h2 class="h-display" style="font-size:calc(var(--u)*5.4)">Choose the first night.</h2>
  <p class="lede">One working session. Scope and fee within 72 hours.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Pick the city and the venue.</li><li>Share covers and booking data.</li><li>Agree the scope, the fee and the readout.</li><li>The first Session in December.</li></ol>
  <div class="rule-plan"><p class="h3">Kaavish · Mask360</p><p class="ink2 mt-s">mask360.agency</p></div>
</div></div>'''
    return slide('next', 'Next steps', body)


def close():
    body = f'''<div class="grow" style="display:grid;place-items:center">
<div class="close-mark">
  <span class="wt" aria-label="The Park Hotels">The Park Hotels</span>
  <span class="label line">The Park Hotels × Mask360 · Park Street, everywhere</span>
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
    out = [cover(), promise(), brief(), ch_today(), today(), growth(), brands(), rule(), insight(), ch_idea(), collections(),
           ideas(), sessions(), room(), flurys(), ch_run(), days(), path(), measure(), mask360(), next_steps(), close(), sources()]
    assert [s.split('id="', 1)[1].split('"', 1)[0] for s in out] == ORDER, 'ORDER is out of step with the slides'
    return out
