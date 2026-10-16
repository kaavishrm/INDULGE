"""Slide copy for the v4 proposal. Plain, direct, corporate English. Every number on a slide carries its source and date
in the folio line. Facts come from research_notes/Westside proposal v4/ and the Trent documents in its sources/ folder."""
import art
from data import F, LAST12, COMPETITORS, POSITIONING, MODEL, BASELINE, REF_GROUPS
from kit import slide, stat, ul, table, months, video_card, W_MARK, M_MARK

TITLE = 'Westside × Mask360'
DESCRIPTION = ('Mask360’s proposal to Westside, October 2026: Styled by Westside, the Westside Coffee Cart and Window Stories, '
               'measured on footfall per store.')

# drinks named after Westside labels with 2025-26 evidence (westside.com, Trent filings, trade press)
MENU = ['Bombay Paisley Filter', 'Nuon Cold Brew', 'Gia Hazelnut Latte', 'E.T.A Flat White', 'Utsa Masala Chai', 'Vark Rose Cardamom']


def cover():
    trio = (f'<div class="trio"><figure>{art.rail(labels=False)}<figcaption class="label">Styled by Westside</figcaption></figure>'
            f'<figure>{art.cart([], labels=False)}<figcaption class="label">The Westside Coffee Cart</figcaption></figure>'
            f'<figure>{art.window(labels=False)}<figcaption class="label">Window Stories</figcaption></figure></div>')
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="lockup">{W_MARK}<span class="x">×</span>{M_MARK}</div>
<h1 class="h-display" style="max-width:13em">From the post to the billing counter.</h1>
<p class="lede">Styled by Westside, the Westside Coffee Cart and Window Stories.<br>Each one is judged on footfall per store.</p>
{trio}
</div>'''
    return slide('cover', 'Proposal', body, src='A proposal from Mask360 to the Westside leadership team, Trent Limited · October 2026 · Confidential', bare=True)


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="h-display" style="max-width:15em">We will take shoppers from the post to the billing counter.</h2>
<p class="lede">Every idea here ends inside a Westside store and is judged on how many more people walk into it.</p>
</div>
<div class="row c3 mt-m">
  <div class="rule"><p class="h3">Test it once</p><p class="mt-s">One city for twelve weeks, built around a store launch or the wedding season.</p></div>
  <div class="rule"><p class="h3">Measure it your way</p><p class="mt-s">Your store entry counts and your bills, read against stores that did not get the programme.</p></div>
  <div class="rule"><p class="h3">No result, nothing to pay</p><p class="mt-s">If the numbers don’t move, you lose nothing.</p></div>
</div>'''
    return slide('promise', 'Our promise', body, dark=True)


def today():
    s = F
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Westside is growing by opening stores.</h2>
  <p class="ink2 lede-s">The next gain is more people walking into each one. This proposal is built for that.</p>
</div>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat(s['stores'], 'stores on 30&nbsp;September&nbsp;2026', f"{s['stores_added']} more than a year earlier")}
  {stat(s['cities'], 'cities on 30 June 2026', 'the latest disclosed count')}
  {stat(s['members'], 'WestStyleClub members, 30&nbsp;September&nbsp;2025', 'the latest count we could confirm')}
  {stat(s['online'], 'of Westside revenue is online, Q1 FY27', 'the other 94% or so is spent in stores')}
  {stat(s['growth'], 'Trent revenue growth, July to September&nbsp;2026', 'fashion like-for-like, April to June: low single digits')}
  {stat('400–500', 'new designs a week', 'with AI design tools, as reported')}
</div></div>'''
    src = ('Sources: Trent store update, Q2 FY26 (261 stores); Trent Q1 FY27 investor presentation, 6&nbsp;Aug&nbsp;2026 (301 stores, cities, online, '
           'like-for-like); Q2 FY27 business update, 5&nbsp;Oct&nbsp;2026, as reported by Upstox (+10 stores, +23%); Trent Q2 FY26 investor presentation '
           '(WestStyleClub); Bloomberg interview with Shailina Parti, 20&nbsp;Jul&nbsp;2026, as reported by Retail Insight Network (designs).')
    return slide('today', 'Westside today', body, src=src)


def last12():
    p = POSITIONING
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">{p['year_title']}</h2>
  <p class="ink2 lede-s">{p['year_line']}</p>
</div>
{months(LAST12)}
<div class="row c3">
  {''.join(f'<div class="rule">{stat(n, k, s)}</div>' for n, k, s in p['year_stats'])}
</div></div>'''
    return slide('last12', 'Westside today · the last twelve months', body, src=p['year_src'])


def voice():
    p = POSITIONING
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">{p['voice_title']}</h2>
  <p class="ink2 lede-s">{p['voice_lede']}</p>
</div>
<div class="stack-l grow" style="justify-content:center">
<div class="row c2">
  <div class="rule stack"><p class="label mute">What Westside says now</p>{ul(p['themes'], 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label plan">Where we take it</p>{ul(p['opportunities'], 'list big-list')}</div>
</div>
<div class="row c3 mt-m">{''.join(f'<div class="panel-bg pad"><p class="label plan">{a}</p><p class="mt-s">{b}</p></div>' for a, b in p['answers'])}</div>
</div></div>'''
    return slide('voice', 'Westside today · how Westside talks', body, src=p['voice_src'])


def competition():
    rows = [[f'<b>{c["name"]}</b><br><span class="mute f-s">{c["stores"]}</span>', c['did'], f'<span class="plan">{c["win"]}</span>'] for c in COMPETITORS]
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">What the others did. How Westside wins.</h2>
  <p class="ink2 lede-s">Their shoppers differ, but often spend from the same budget. Each row is recent marketing we found for that brand, from August 2025 to October 2026, and how Westside beats it.</p>
</div>
<div class="grow v-center">{table(['Brand', 'What they did (recent work we found)', 'How Westside wins'], rows, cls='tbl rivals stackable')}</div>
</div>'''
    src = ('Sources: Shoppers Stop Q1 FY27 results release, 22&nbsp;Jul&nbsp;2026; Passionate in Marketing, 4&nbsp;May&nbsp;2026 (Trends); FashionUnited, '
           '30&nbsp;Apr&nbsp;2026, and Fibre2Fashion (H&amp;M); Retail4Growth, 13&nbsp;Apr&nbsp;2026, and Indian Retailer, 9&nbsp;Oct&nbsp;2026 (Uniqlo); '
           'IndianTelevision, 23&nbsp;Sep&nbsp;2026 (Myntra); Social Samosa, 6&nbsp;Oct&nbsp;2025 (Pantaloons); The Week, 20&nbsp;Aug&nbsp;2025 (Max).')
    return slide('rivals', 'The market', body, src=src)


def plan():
    ideas = [
        ('1', 'Styled by Westside', 'Every week, stylists and creators build complete Westside looks in store, film them and post them on Westside’s, creators’ and paid city pages.', MODEL['styling']),
        ('2', 'The Westside Coffee Cart', 'A Westside-designed cart with a menu named after Westside’s labels. Every cup carries a look from the nearest Westside.', MODEL['cart']),
        ('3', 'Window Stories', 'Two mannequins dressed for a moment everyone knows, every piece sold inside. Each store picks its story.', MODEL['windows']),
    ]
    cols = ''.join(f'''<div class="idea rule-plan"><span class="no">{n}</span><h3 class="h2">{t}</h3><p class="idea-d">{d}</p>
<div class="rule"><p class="label mute">Where it ends</p><p class="mt-s">{m['ends']}</p></div>
<div class="mt-m"><div class="imp">{m['label']}<small>impressions</small></div><p class="f-s mute mt-s">{m['note']}</p></div></div>''' for n, t, d, m in ideas)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">A twelve-week test in one city targets {MODEL['total_label']} impressions.</h2>
  <p class="ink2 lede-s">{BASELINE['plan_line']} It builds on YNG and FRONT ROW, which Westside already runs.</p>
</div>
<div class="row c3 grow vc">{cols}</div>
</div>'''
    return slide('plan', 'The plan', body, src=BASELINE['src'])


def styling():
    formats = [('One piece, three ways', 'A stylist takes one Westside piece from office to dinner to a family function.'),
               ('Style me for…', 'A creator brings a real occasion. Our stylist dresses them from one store in thirty minutes.'),
               ('Head to toe, one budget', 'Clothes, shoes and Studiowest make-up, every piece from the store, with the total on screen.'),
               ('Stylist vs creator', 'Same brief, two looks, the audience picks. The winner gets the front rail for a week, with the store manager’s sign-off.')]
    f = ''.join(f'<div class="rule"><p class="h4">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in formats)
    body = f'''<div class="row c-6-6 grow">
<div class="stack-l" style="justify-content:center">
  <span class="label plan">Styled by Westside</span>
  <h2 class="h1">Make styling the reason people follow Westside.</h2>
  <p>Almost everything Westside sells is its own label, and its designers create 400–500 new designs a week. Most people never see how those pieces go together. Every week our stylists and creators build complete looks from one Westside store, film them on the floor and post them on Instagram and YouTube Shorts.</p>
  <p>Each look has a code. Show it in store and the team brings the whole outfit in your size, or holds it if a size is out. The code is not a discount. It tells the team which look you want, and tells us which post brought you in.</p>
  <div class="row c2 gap-s mt-m">{f}</div>
</div>
<div class="art" style="align-self:center">{art.rail(highlight='saree', code='LOOK 027')}</div>
</div>'''
    return slide('styling', 'Idea 1 of 3', body, src='Designs: Bloomberg interview with Shailina Parti, 20&nbsp;Jul&nbsp;2026, as reported by Retail Insight Network. Own labels: BW Businessworld, 2026. Featured looks use lines with stock depth, signed off by Westside’s buying team.')


def styling_plan():
    m = MODEL['styling']
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">120 coded looks in twelve weeks.</h2>
  <p class="ink2 lede-s">Styled by Westside in the test city. These are the numbers we commit to.</p>
</div>
<div class="grow v-center">{table(['Item', 'Who', 'How many', 'How often', 'What it delivers'], m['rows'], cls='tbl roomy stackable', right=(2,))}</div>
<div class="row c3">
  <div class="rule">{stat(m['label'], 'impressions in twelve weeks', m['note'])}</div>
  <div class="rule">{stat(m['people'], 'people from Mask360 on the programme', m['people_note'])}</div>
  <div class="rule">{stat(m['looks'], 'complete looks, each with a code', 'every look tagged to a named store')}</div>
</div></div>'''
    return slide('styling-plan', 'Idea 1 of 3 · the plan', body, src=m['src'])


def cart():
    menu = ''.join(f'<li>{x}</li>' for x in MENU)
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:center">
  <span class="label plan">The Westside Coffee Cart</span>
  <h2 class="h1">Coffee, and the look that goes with it.</h2>
  <p>A Westside-designed coffee cart that parks outside Westside stores, in malls, at colleges and in office parks. The menu is named after Westside’s own labels, and every cup sleeve carries a look code to show at the nearest store.</p>
  <div class="row c2 gap-s mt-m">
    <div class="rule"><p class="label mute">On the menu</p><ul class="list mt-s">{menu}</ul></div>
    <div class="rule-plan"><p class="label plan">How people see it</p><p class="mt-s">Creators and clip, city and food pages film the cart, the cups and the queue. {MODEL['cart']['reach_line']}</p></div>
  </div>
</div>
<div class="art" style="align-self:center">{art.cart([(x, '') for x in MENU])}</div>
</div>'''
    return slide('cart', 'Idea 2 of 3', body, src='Menu names use Westside’s own labels (westside.com, Trent filings and trade press, 2025–26). Illustration is a concept drawing.')


def cart_plan():
    m = MODEL['cart']
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Three carts serve 21,600 cups in six weeks.</h2>
  <p class="ink2 lede-s">{m['lede']}</p>
</div>
<div class="grow v-center">{table(['Item', 'Detail', 'How many', 'What it delivers'], m['rows'], cls='tbl roomy stackable', right=(2,))}</div>
<div class="row c3">
  <div class="rule">{stat(m['label'], 'impressions in six weeks of cart days', m['note'])}</div>
  <div class="rule">{stat(m['cups'], 'cups, each with a look code on the sleeve', m['cups_note'])}</div>
  <div class="rule">{stat(m['people'], 'people on the cart team', m['people_note'])}</div>
</div></div>'''
    return slide('cart-plan', 'Idea 2 of 3 · the plan', body, src=m['src'])


def windows():
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:center">
  <span class="label plan">Window Stories</span>
  <h2 class="h1">Rahul and Anjali are getting ready for a date.</h2>
  <p>Two mannequins dressed for a moment everyone knows, with every piece on them for sale inside. It is a window people stop to photograph and share.</p>
  <p>Next month the story changes: a first day at a new job, a cousin’s mehendi, Sunday lunch at Nani’s, a college reunion.</p>
  <div class="rule-plan mt-m"><p>Each story is two complete outfits, each look priced on a card in the window, with a code to ask for it in store. Anjali’s dressing table is set with Studiowest, priced on the same card.</p></div>
</div>
<div class="art" style="align-self:center">{art.window()}</div>
</div>'''
    return slide('windows', 'Idea 3 of 3', body, src='Illustration is a concept drawing. Character names are working titles until the story list is approved.')


def windows_scale():
    m = MODEL['windows']
    stories = ''.join(f'<tr><td class="n"><b>{c}</b></td><td>{s}</td></tr>' for c, s in m['stories'])
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:space-between">
  <h2 class="h1">311 windows, each picking its story from one library.</h2>
  <div class="art" style="height:auto">{art.stores_grid(n=m['grid_n'], cols=25)}</div>
  <p class="f-s ink2">One square per Westside store. The test city’s stores go first; every store follows after the go or no&#8209;go.</p>
</div>
<div class="stack-l" style="justify-content:space-between">
  <table class="tbl tight"><thead><tr><th>First six stories</th><th>The story in the window</th></tr></thead><tbody>{stories}</tbody></table>
  {table(['Item', 'How many', 'What it delivers'], m['rows'], cls='tbl tight stackable')}
  <div class="row c2"><div class="rule">{stat(m['label'], 'impressions in twelve weeks', m['note'])}</div><div class="rule">{stat(m['people'], 'people on the windows team', m['people_note'])}</div></div>
</div></div>'''
    return slide('windows-scale', 'Idea 3 of 3 · at scale', body, src=m['src'] + ' FRONT ROW’s New Faces star in the window Reels.')


def look_path():
    steps = [('Made in store', 'A stylist or creator builds the look from one store’s rails; the cart and the windows carry looks from the same rails.'),
             ('Posted the same week', 'Westside’s pages, the creator’s page and paid clip and city pages carry the same look.'),
             ('Tagged with a code', 'Every post, cup sleeve and window card shows a short look code and the store’s name.'),
             ('Shown at the store', 'The shopper shows the code. The team brings the look in their size.'),
             ('Logged at billing', 'The code goes on the bill. Westside’s analytics team matches it to WestStyleClub bills; we see store totals only.')]
    cells = ''.join(f'<div class="rule{"-plan" if i == 4 else ""}"><span class="num step {"plan" if i == 4 else "mute"}">{i + 1}</span><p class="h3 mt-s">{a}</p><p class="ink2 mt-s">{b}</p></div>' for i, (a, b) in enumerate(steps))
    body = f'''<div class="stack-l grow">
<h2 class="h1">How every idea reaches the billing counter.</h2>
<div class="row c5 flow vc grow">{cells}</div>
<div class="row c2 rule">
  <p class="f-l ink2">The look code links each post, cup and window to a store and a bill. That is how we count sales from content. The code is never a discount.</p>
  <p class="f-l ink2">Store teams need one short briefing a week: this week’s looks, where they hang and how to log the code.</p>
</div></div>'''
    return slide('path', 'From post to bill', body)


def numbers():
    rows = MODEL['table']
    b = BASELINE
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">{MODEL['total_label']} impressions, line by line.</h2>
  <p class="ink2 lede-s">Each line is units times an average per unit. Low and high show the range we plan for. Figures in millions.</p>
</div>
<div class="row c-8-4 grow">
  {table(['Idea', 'Channel', 'Units', 'Average per unit', 'Low', 'Plan', 'High'], rows['rows'], cls='tbl small tight model', right=(2, 3, 4, 5, 6), total=rows['total'], col_cls={3: 'm-hide', 4: 'm-hide', 5: 'plan-col', 6: 'm-hide'})}
  <div class="stack-l" style="justify-content:center">
    <p class="label mute">Against YNG, January to March 2026</p>
    <div class="bars">
      <div class="bar"><span class="f-s">{b['label']}</span><span class="t"><i style="width:{b['pct_base']}%"></i></span><span class="v">{b['value']}</span></div>
      <div class="bar us"><span class="f-s">This test, views and impressions</span><span class="t"><i style="width:{b['pct_plan']}%"></i></span><span class="v">{MODEL['total_label']}</span></div>
    </div>
    <p class="ink2">{b['compare_line']}</p>
  </div>
</div></div>'''
    return slide('numbers', 'The numbers', body, src=MODEL['src'])


def measure():
    rows = [['Footfall per store', 'People counters at the entrance', 'Test-city stores against matched stores that did not get the programme'],
            ['Codes used', 'Look codes from posts, cups and windows, logged at billing', 'Per store, per idea, per week'],
            ['Member bills', 'Codes matched to WestStyleClub bills by Westside’s analytics team', 'Members who used a code against members who did not'],
            ['Impressions and views', 'Platform reports from every page and creator', 'Against the plan, line by line, every week']]
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Measured at the billing counter.</h2>
  <p class="ink2 lede-s">Impressions show the work was seen; footfall and bills show it worked. We report both weekly, store by store.</p>
</div>
<div class="row c-4-8 grow vc">
  <div class="rule-plan"><p class="label plan">Draft threshold</p><p class="mt-s f-l">Test-city stores beat matched stores on entries by 5% or more over the twelve live weeks.</p><p class="mt-s ink2">We set the final number from your data before launch.</p></div>
  <div class="stack-l">{table(['What we count', 'How', 'Read against'], rows, cls='tbl roomy stackable')}
  <p class="f-s ink2">A launch store has no history, so it is read against the opening weeks of recent comparable openings. One store on its own needs a lift of about 8–15% to read clearly; pooling a city’s stores lets us read smaller lifts. We see store totals only, never personal data.</p></div>
</div></div>'''
    return slide('measure', 'Measurement', body)


def test():
    body = '''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Start with one city. If the numbers don’t move, you lose nothing.</h2>
  <p class="ink2 lede-s">All three ideas run for twelve weeks, read on footfall per store. You pick what the test is built around.</p>
</div>
<div class="row c2 vc grow">
  <div class="panel-bg pad-l rule-plan stack">
    <p class="label plan">Option A · recommended</p><h3 class="h2">A store launch</h3>
    <p>Westside’s next opening and the stores in its city: looks styled from its rails before it opens, a cart outside from opening weekend, Window Stories across the city.</p>
    <p class="f-s ink2">Read against the opening weeks of recent comparable openings, and against matched stores.</p>
  </div>
  <div class="panel-bg pad-l rule stack">
    <p class="label mute">Option B</p><h3 class="h2">The wedding season</h3>
    <p>One city through the wedding dates: styled looks for every function, three carts across the city, wedding Window Stories in every store.</p>
    <p class="f-s ink2">Read against each store’s previous twelve weeks and matched stores in other cities.</p>
  </div>
</div>
<div class="row c3 mt-m">
  <div class="rule"><p class="h4">If it works</p><p class="mt-s">You pay our fee, agreed now, plus production and media within the cap.</p></div>
  <div class="rule"><p class="h4">If it doesn’t</p><p class="mt-s">No fee, and Mask360 carries production and media for the test, within a cap agreed before launch.</p></div>
  <div class="rule"><p class="h4">What we need from Westside</p><p class="mt-s">A test city and matched stores, people counters working in both, a look-code field at billing, stock depth on featured looks, VM time, help with mall consent, counter and bill data under a data agreement, and sign-off on each week’s posts within 48 hours.</p></div>
</div></div>'''
    return slide('test', 'The test', body)


def timeline():
    weeks = 17
    phases = [('Agree and set up', 1, 3, 'line', 'Test city, matched stores and threshold agreed. Look codes set up at billing. Store teams briefed.'),
              ('Cast and build', 2, 5, 'line', 'Stylists and YNG creators cast. Carts built. First Window Stories designed. Clip and city pages booked.'),
              ('Styled by Westside', 5, 17, 'plan', '120 looks; Westside, creator and page posts every week.'),
              ('Coffee Cart', 7, 13, 'plan', 'Thursday to Sunday, three carts, six weeks.'),
              ('Window Stories', 5, 17, 'plan', 'A new story every four weeks in every store in the city.'),
              ('Readout', 17, 18, 'ink', 'Footfall, codes, bills and impressions against plan. Go or no&#8209;go for the next cities.')]
    head = ''.join(f'<span class="wk label">{i}</span>' for i in range(1, weeks + 1))
    rows = ''.join(f'<p class="h4 ph">{n}</p><i class="bar-{c}" style="grid-column:{s + 1}/{e + 1}"></i><p class="ink2 f-s note">{t}</p>' for n, s, e, c, t in phases)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Sixteen weeks to a readout.</h2>
  <p class="ink2 lede-s">Four weeks to set up, twelve weeks live, then a readout with Westside’s leadership. Dates assume a working session by 27 October and signature by 30 October.</p>
</div>
<div class="gantt vc grow"><span></span>{head}{rows}</div>
<div class="row c4 dates">
  <div class="rule"><p class="label mute">Set up</p><p class="mt-s">2 to 29 November</p></div>
  <div class="rule-plan"><p class="label plan">Live</p><p class="mt-s">30 November to 21 February</p></div>
  <div class="rule"><p class="label mute">Readout</p><p class="mt-s">Week of 22 February 2027</p></div>
  <div class="rule"><p class="label mute">Wedding dates</p><p class="mt-s">Option B runs through the wedding dates either side of the mid&#8209;December to mid&#8209;January pause. We confirm the 2026–27 dates before the city is picked.</p></div>
</div></div>'''
    return slide('timeline', 'Timeline', body)


def mask360():
    pillars = [('Social', 'The Styled by Westside series, creators and paid page posts.'),
               ('Content', 'Stylists, shoots and edits, made in Westside stores.'),
               ('Events and retail', 'The Coffee Cart and Window Stories, built and run.'),
               ('Measurement', 'The per-store scorecard, built with Westside’s analysts.')]
    p = ''.join(f'<div class="rule"><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in pillars)
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-5-7 center">
  <div class="stack"><span class="label mute">Who we are</span><div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div></div>
  <p class="lede">Mask360 is a creative and content agency in India and the UAE. For nine years we have made content, events and campaigns for luxury, lifestyle and real-estate brands, from Mumbai, Delhi, Bengaluru, Dubai and Abu Dhabi.</p>
</div>
<div class="row c4 mt-m">{p}</div>
<div class="rule mt-m"><p class="label mute">Brands we have worked with</p><p class="mt-s f-l">Dior · L’Oréal · FCUK Beauty · Dyson · Anantara · Atlantis The Royal · St. Regis · Ferrari · Rolls-Royce · Swisse · Zorae · Rustomjee · Chandak Group</p></div>
</div>'''
    return slide('mask360', 'Mask360', body)


def next_steps():
    body = '''<div class="row c-6-6 grow center">
<div class="stack-l">
  <h2 class="h-display">Choose the first city.</h2>
  <p class="lede">One working session with your marketing, retail operations and analytics leads. We bring a store shortlist and a draft threshold. Within 72 hours of it, you get a fixed scope and terms.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Pick the test: a store launch or the wedding season.</li><li>Share counter and bill data for the test and matched stores.</li><li>Agree the threshold, our fee and the cap.</li><li>Week one starts the Monday after you sign.</li></ol>
  <div class="rule mt-m"><p class="h3">Kaavish · Mask360</p><p class="ink2">mask360.agency</p></div>
</div></div>'''
    return slide('next', 'Next steps', body, dark=True)


def references():
    out = []
    n = len(REF_GROUPS)
    for i, (title, vids) in enumerate(REF_GROUPS):
        cards = ''.join(video_card(v['item'], v['caption']) for v in vids)
        body = f'''<div class="row c-3-9 grow">
<div class="stack-l">
  <h2 class="h1">{title}.</h2>
  <p class="ink2 lede-s">Clips the team collected for look and pace. They are references, not our work.</p>
  <p class="ink2 f-s">Press play to open a clip large, with sound, volume and a full-screen button. Esc or the close button returns to the slide.</p>
</div>
<div class="vgrid two-rows vc">{cards}</div>
</div>'''
        out.append(slide(f'references-{i + 1}', f'Appendix · references {i + 1} of {n}', body))
    return out


def slides():
    return [cover(), promise(), today(), last12(), voice(), competition(), plan(), styling(), styling_plan(),
            cart(), cart_plan(), windows(), windows_scale(), look_path(), numbers(), measure(), test(), timeline(),
            mask360(), next_steps(), *references()]
