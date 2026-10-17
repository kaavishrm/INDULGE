"""Slide copy for the proposal. Short: a headline, a line or two, the numbers. Each slide carries a one-line source;
the full sources and the full impressions model are in the appendix. Facts come from research_notes/Westside proposal v4/
and the Trent documents in its sources/ folder. The look is the v3 deck's, without its app chrome."""
import art
from data import F, LAST12_SHORT, POSITIONING, MODEL, BASELINE, REF_GROUPS, LINES, PAID


def _mn(x):
    return f'{x / 1e6:.1f}'
from kit import slide, stat, ul, table, months, tile, photo, video_card, W_MARK, M_MARK

TITLE = 'Westside × Mask360'
DESCRIPTION = ('Mask360’s proposal to Westside, October 2026: Styled by Westside, the Westside Coffee Cart and Window Stories, '
               'measured on footfall per store.')

# drinks named after Westside labels with 2025-26 evidence (westside.com, Trent filings, trade press)
MENU = ['Bombay Paisley Filter', 'Nuon Cold Brew', 'Gia Hazelnut Latte', 'E.T.A Flat White', 'Utsa Masala Chai', 'Vark Rose Cardamom']

# one cloth per month on the twelve-month strip: (kind, seed, light cloth so the month is set in ink?)
MONTH_CLOTH = [('shaadi', 11, False), ('rani', 12, False), ('bone', 13, True), ('slate', 14, False), ('denim', 15, False), ('linen', 16, True),
               ('moss', 17, False), ('ivory', 18, True), ('indigo', 19, False), ('bone', 20, True), ('mehendi', 21, False), ('kohl', 22, False)]
# the three ideas' cloth: (kind, seed, dark text?)
IDEA_CLOTH = {'styling': ('chikankari', 31, True), 'cart': ('kohl', 32, False), 'windows': ('slate', 33, False)}

# the cart renders the team made (media/out/cart-*.webp): file, name, one line, crop focus
CARTS = [('cart-ape.webp', 'Three-wheeler', 'Sage and cream, open on one side', '58% 50%'),
         ('cart-van.webp', 'Vintage van', 'Two hatches and a pastry counter', '22% 50%'),
         ('cart-awning.webp', 'Cream cart', 'Scalloped awning, brass wheel', '62% 50%'),
         ('cart-kiosk.webp', 'Green kiosk', 'Towable, fits a mall forecourt', '50% 60%')]

# full sources, shown on the last appendix page; each slide carries a short version
SOURCES = [
    ('Westside today', 'Trent store update, Q2 FY26 (261 stores); Trent Q1 FY27 investor presentation, 6 Aug 2026 (301 stores, 97 cities, online over 6%); '
     'Q2 FY27 business update, 5 Oct 2026, as reported by Upstox (+10 stores, Trent revenue +23%); Trent Q2 FY26 investor presentation (WestStyleClub '
     '19 mn+); Bloomberg interview with Shailina Parti, 20 Jul 2026, as reported by Retail Insight Network (400–500 designs a week).'),
    ('The last twelve months', POSITIONING['year_src'].replace('Sources: ', '')),
    ('How Westside talks', POSITIONING['voice_src'].replace('Sources: ', '')),
    ('The market', 'Shoppers Stop Q1 FY27 results release, 22 Jul 2026; Passionate in Marketing, 4 May 2026 (Trends); FashionUnited, 30 Apr 2026, and '
     'Fibre2Fashion (H&amp;M); Retail4Growth, 13 Apr 2026, and Indian Retailer, 9 Oct 2026 (Uniqlo); IndianTelevision, 23 Sep 2026 (Myntra); '
     'Social Samosa, 6 Oct 2025 (Pantaloons); The Week, 20 Aug 2025 (Max).'),
    ('The plan and the numbers', BASELINE['src'] + ' ' + MODEL['src']),
    ('Styled by Westside', 'Designs: Bloomberg interview with Shailina Parti, 20 Jul 2026, as reported by Retail Insight Network. Own labels: BW Businessworld, '
     '2026. Plan figures are Mask360’s proposal; featured looks use lines with stock depth, signed off by Westside’s buying team.'),
    ('The Westside Coffee Cart', 'Menu names use Westside’s own labels (westside.com, Trent filings and trade press, 2025–26). About 300 cups a cart day is a '
     'planning figure to confirm with a coffee partner, who runs the bar under its own food licence; every site needs mall or landlord consent. '
     'Cart images are concept renders.'),
    ('Window Stories', 'Rollout is a planning figure to confirm with Westside’s VM team. FRONT ROW’s New Faces star in the window Reels. '
     'Character names are working titles.'),
    ('Measurement', 'One store on its own needs a lift of about 8–15% to read clearly; pooling a city’s stores lets us read smaller lifts. A launch store is '
     'read against the opening weeks of recent comparable openings. We see store totals only, never personal data.'),
]


def cover():
    body = f'''<div class="stack-l grow" style="justify-content:space-between">
<div class="big-wm" aria-label="Westside">{W_MARK}<span class="t" aria-hidden="true">Westside</span></div>
<div class="cover-foot">
  <div class="stack-l">
    <span class="label">A proposal from Mask360 · October 2026</span>
    <h1 class="h-display" style="max-width:11em">From the post to the billing counter.</h1>
  </div>
  {M_MARK}
</div></div>'''
    return slide('cover', 'Proposal', body, src='For the Westside leadership team · Confidential', bare=True, dark=True, cls='cover scrim', cloth=('slate', 7))


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">We will take shoppers from the post to the <u>billing counter</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">01</span><p class="h3">Test it once</p><p class="mt-s ink2">One city, twelve weeks.</p></div>
  <div><span class="no label">02</span><p class="h3">Measure it your way</p><p class="mt-s ink2">Your footfall and your bills.</p></div>
  <div><span class="no label">03</span><p class="h3">No result, nothing to pay</p><p class="mt-s ink2">If the numbers don’t move, you lose nothing.</p></div>
</div>'''
    return slide('promise', 'Our promise', body)


def today():
    s = F
    body = f'''<div class="stack-l grow">
<h2 class="h1">Westside is growing by opening stores.</h2>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat(s['stores'], 'stores, 30&nbsp;Sep&nbsp;2026', f"+{s['stores_added']} in a year")}
  {stat(s['cities'], 'cities')}
  {stat(s['members'], 'WestStyleClub members', 'Sep 2025')}
  {stat(s['online'], 'of Westside revenue online', 'the rest is in stores')}
  {stat(s['growth'], 'Trent revenue, Jul–Sep 2026')}
  {stat('400–500', 'new designs a week')}
</div></div>'''
    return slide('today', 'Westside today', body, src='Sources: Trent filings and business updates, 2025–26. Full list at the end.')


def last12():
    items = [(m, f'<b>{t}</b>' if t else line, line if t else '', quiet, MONTH_CLOTH[i]) for i, (m, t, line, quiet) in enumerate(LAST12_SHORT)]
    body = f'''<div class="stack-l grow">
<h2 class="h1">A year measured in turnout and views.</h2>
{months(items)}
<div class="row c3">
  <div class="rule">{stat('6&nbsp;mn', 'YNG views, Jan–Mar 2026')}</div>
  <div class="rule">{stat('3,600+', 'at the biggest Wesness run')}</div>
  <div class="rule">{stat('Footfall', 'not yet measured. This test adds it.')}</div>
</div></div>'''
    return slide('last12', 'Westside today · the last twelve months', body, src='Sources: Trent decks and press releases, trade press, westside.com. Full list at the end.')


def voice():
    says = ['New Indian talent', 'Culture beyond clothes', 'Women together', 'Own labels first']
    take = ['Show the 400–500 new designs a week', 'One festive story, Navratri to weddings', 'The same launch for every new store', 'End every post in a store']
    body = f'''<div class="stack-l grow">
<h2 class="h1">{POSITIONING['voice_title']}</h2>
<div class="row c2 grow vc">
  <div class="rule stack"><p class="label mute">What Westside says now</p>{ul(says, 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label">Where we take it</p>{ul(take, 'list big-list')}</div>
</div></div>'''
    return slide('voice', 'Westside today · how Westside talks', body, src='Sources: Trent investor presentations, Indian Retailer, westside.com. Full list at the end.')


RIVALS = [  # condensed from data.COMPETITORS (the long rows are in research note 04)
    ('Shoppers Stop', '115 dept. stores', 'Wedding, travel and HYBE campaigns', 'Own labels, so every look is stocked in a named store'),
    ('Max Fashion', 'Landmark Group', 'Star films selling weekly newness', 'Real looks, styled and stocked in a named store'),
    ('Pantaloons', 'ABFRL', 'A first star ambassador', 'Local stylists and creators, each tied to a store'),
    ('Trends', 'Reliance Retail', 'Spend ₹1,499, enter a holiday contest', 'No discounts or contests. A look, a coffee, a story'),
    ('H&amp;M', '71 stores', 'HYBE pop-ups in six cities', 'Runs on Westside’s calendar and ends in its stores'),
    ('Uniqlo', 'Uniqlo India', 'New stores, a star fleece campaign', '311 stores, a local launch for each'),
    ('Myntra', 'online only', 'Creator School, paid festive posts', 'Every creator post counted at a till'),
]


def competition():
    rows = [[f'<b>{n}</b><br><span class="mute f-s">{s}</span>', d, w] for n, s, d, w in RIVALS]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What the others did. How Westside wins.</h2>
<div class="grow v-center">{table(['Brand', 'What they did', 'How Westside wins'], rows, cls='tbl rivals stackable')}</div>
</div>'''
    return slide('rivals', 'The market', body, src='Sources: company releases and trade press, Aug 2025 to Oct 2026. Full list at the end.')


def plan():
    ideas = [('No. 01', 'Styled by Westside', 'Stylists and creators build looks in store, every week.', MODEL['styling'], IDEA_CLOTH['styling']),
             ('No. 02', 'The Westside Coffee Cart', 'Drinks named after Westside labels, a look code on every cup.', MODEL['cart'], IDEA_CLOTH['cart']),
             ('No. 03', 'Window Stories', 'Two mannequins, one story, every piece sold inside.', MODEL['windows'], IDEA_CLOTH['windows'])]
    cols = ''.join(f'''<div class="idea">{tile(c[0], c[1], n, t, dark_text=c[2])}<p>{d}</p>
<div class="imp">{m['label']}<small>impressions</small></div></div>''' for n, t, d, m, c in ideas)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">{MODEL['total_label']} impressions in twelve weeks, in one city.</h2>
  <p class="ink2 lede-s">At least 20% more than Westside’s best comparable campaign of the last year.</p>
</div>
<div class="row c3 grow vc">{cols}</div>
</div>'''
    return slide('plan', 'The plan', body, src='Baseline: Trent Q4 FY26 investor presentation (YNG). Plan: the impressions model in the appendix.')


def styling():
    formats = ['One piece, three ways', 'Style me for…', 'Head to toe, one budget', 'Stylist vs creator']
    f = ''.join(f'<div><p class="h4">{a}</p></div>' for a in formats)
    body = f'''<div class="row c-6-6 grow">
<div class="pic">{art.rail(highlight='saree', code='LOOK 027')}<div class="ov"><span class="no">No. 01</span><span class="label">Concept drawing</span></div></div>
<div class="stack-l">
  <span class="label">Styled by Westside</span>
  <h2 class="h1">Make styling the reason people follow Westside.</h2>
  <p class="f-l ink2">Every week, stylists and creators build complete looks from one store and post them. Each look has a code. Show it in store and the team brings the outfit in your size.</p>
  <div class="spec">{f}</div>
</div>
</div>'''
    return slide('styling', 'Idea 1 of 3', body, src='Designs: Bloomberg via Retail Insight Network, 20 Jul 2026. Full list at the end.')


def styling_plan():
    m = MODEL['styling']
    rows = [['Stylists', '3', 'every week'], ['Shoot days', '24', '2 a week'], ['Creator Reels', '40', '3 to 4 a week'],
            ['Clip and city page posts', '55', '4 to 5 a week'], ['Westside Reels', '36', '3 a week'], ['Store visits', '48', '4 a week']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">120 coded looks in twelve weeks.</h2>
<div class="row c-7-5 grow vc">
  {table(['Item', 'How many', 'How often'], rows, cls='tbl roomy stackable', right=(1,))}
  <div class="stack-l">
    <div class="rule">{stat(m['label'], 'impressions')}</div>
    <div class="rule">{stat(m['people'], 'people from Mask360')}</div>
  </div>
</div></div>'''
    return slide('styling-plan', 'Idea 1 of 3 · the plan', body, src='Mask360’s plan for the twelve-week test. Impressions: the model in the appendix.')


def cart():
    menu = ''.join(f'<li>{x}</li>' for x in MENU)
    body = f'''<div class="row c-6-6 grow">
<div class="pic ph">{photo('cart-at-store.webp', 'Concept render: a green Westside coffee cart at the entrance of a Westside store', pos='28% 50%')}<div class="ov"><span class="no">No. 02</span><span class="label">Concept render</span></div></div>
<div class="stack-l">
  <span class="label">The Westside Coffee Cart</span>
  <h2 class="h1">Coffee, and the look that goes with it.</h2>
  <p class="f-l ink2">Parked outside Westside stores, in malls and at colleges. Every cup sleeve carries a look code from the nearest store.</p>
  <div class="rule-plan"><p class="label">On the menu</p><ul class="list mt-s">{menu}</ul></div>
</div>
</div>'''
    return slide('cart', 'Idea 2 of 3', body, src='Menu names use Westside’s own labels. Image is a concept render.')


def cart_designs():
    cards = ''.join(f'<figure class="shot">{photo(f, f"Concept render: {t.lower()}, a Westside coffee cart", pos=pos)}'
                    f'<figcaption><span class="label">No. {i + 1:02d} · {t}</span><span class="f-s mute">{d}</span></figcaption></figure>'
                    for i, (f, t, d, pos) in enumerate(CARTS))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Four ways to build the cart.</h2>
  <p class="ink2 lede-s">Concept renders. We choose one with Westside’s brand team.</p>
</div>
<div class="shots grow">{cards}</div>
</div>'''
    return slide('cart-designs', 'Idea 2 of 3 · the cart', body, src='Concept renders by the Mask360 team.')


def cart_plan():
    m = MODEL['cart']
    rows = [['Carts', '3', 'one per site'], ['Cart days', '72', 'Thursday to Sunday, six weeks'], ['Cups', '21,600', 'each with a look code'],
            ['Creator Reels', '30', 'from the queue and the store'], ['Clip, city and food page posts', '76', 'timed to cart days']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Three carts serve 21,600 cups in six weeks.</h2>
<div class="row c-7-5 grow vc">
  {table(['Item', 'How many', 'Detail'], rows, cls='tbl roomy stackable', right=(1,))}
  <div class="stack-l">
    <div class="rule">{stat(m['label'], 'impressions')}</div>
    <div class="rule">{stat(m['people'], 'people on the cart team')}</div>
  </div>
</div></div>'''
    return slide('cart-plan', 'Idea 2 of 3 · the plan', body, src='About 300 cups a cart day is a planning figure. A coffee partner runs the bar under its own food licence.')


def windows():
    body = f'''<div class="row c-6-6 grow">
<div class="pic">{art.window()}<div class="ov"><span class="no">No. 03</span><span class="label">Concept drawing</span></div></div>
<div class="stack-l">
  <span class="label">Window Stories</span>
  <h2 class="h1">Rahul and Anjali are getting ready for a date.</h2>
  <p class="f-l ink2">Two mannequins dressed for a moment everyone knows. Every piece is for sale inside, priced on the window card. Next month, a new story.</p>
</div>
</div>'''
    return slide('windows', 'Idea 3 of 3', body, src='Concept drawing. Character names are working titles.')


def windows_scale():
    m = MODEL['windows']
    cloth = [('rani', 41, False), ('mehendi', 42, False), ('slate', 43, False), ('linen', 44, True), ('kohl', 45, False), ('ivory', 46, True)]
    stories = ''.join(f'<div>{tile(k, sd, f"No. {i + 1:02d}", c, dark_text=d)}<p class="f-s ink2 mt-s">{s}</p></div>' for i, ((c, s), (k, sd, d)) in enumerate(zip(m['stories'], cloth)))
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l" style="justify-content:space-between">
  <h2 class="h1">311 stores, each picking its story.</h2>
  <div class="art" style="height:auto">{art.stores_grid(n=m['grid_n'], cols=25)}</div>
  <p class="f-s ink2">One square per store. The test city goes first.</p>
</div>
<div class="stack-l" style="justify-content:space-between">
  <div class="stories">{stories}</div>
  <div class="row c3">
    <div class="rule">{stat(m['label'], 'impressions')}</div>
    <div class="rule">{stat('12', 'new stories a quarter')}</div>
    <div class="rule">{stat(m['people'], 'people on the team')}</div>
  </div>
</div></div>'''
    return slide('windows-scale', 'Idea 3 of 3 · at scale', body, src='Rollout to confirm with Westside’s VM team. Impressions: the model in the appendix.')


def look_path():
    steps = [('Made in store', 'From one store’s rails.'), ('Posted that week', 'Westside, creators, city pages.'), ('Tagged with a code', 'On every post, cup and window.'),
             ('Shown at the store', 'The team brings it in your size.'), ('Logged at billing', 'Store totals, never personal data.')]
    cells = ''.join(f'<div><span class="dot label">{i + 1:02d}</span><p class="h3">{a}</p><p class="ink2 mt-s">{b}</p></div>' for i, (a, b) in enumerate(steps))
    body = f'''<div class="stack-l grow">
<h2 class="h1">How every idea reaches the billing counter.</h2>
<div class="row c5 flow vc grow">{cells}</div>
</div>'''
    return slide('path', 'From post to bill', body)


SHORT = {'Westside’s pages': 'Westside Reels', 'YNG and city creators': 'creator Reels', 'Creators at the cart': 'creator Reels',
         'Store teams and local creators': 'local Reels', 'Clip and city pages': 'page posts', 'Clip, city and food pages': 'page posts',
         'City pages': 'page posts', 'Paid Reels boost': 'boost'}


def _runs(idea):
    """What runs for one idea, from the model's own lines, e.g. '36 Westside Reels · 40 creator Reels · …'."""
    out, cur = [], ''
    for i, ch, ut, u, at, a, paid in LINES:
        cur = i or cur
        if cur == idea:
            out.append(f'{ut} boost' if paid else f'{u} {SHORT[ch]}')
    return ' · '.join(out)


def numbers():
    lo, base, hi = (sum(v[k] for v in MODEL['by_idea'].values()) for k in range(3))
    rows = [[n, _runs(k), f'<b>{MODEL["by_idea"][k][1] / 1e6:.1f}</b>'] for k, n in
            (('Styled by Westside', 'Styled by Westside'), ('Coffee Cart', 'The Westside Coffee Cart'), ('Window Stories', 'Window Stories'))]
    b = BASELINE
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">How we get to {MODEL['total_label']}.</h2>
  <p class="ink2 lede-s">Range {lo / 1e6:.1f} to {hi / 1e6:.1f}&nbsp;mn. The full model is in the appendix.</p>
</div>
<div class="row c-7-5 grow vc">
  {table(['Idea', 'What runs', 'mn'], rows, cls='tbl roomy stackable', right=(2,), total=['Total', '', f'<b>{base / 1e6:.1f}</b>'])}
  <div class="stack-l">
    <p class="label mute">Against YNG, Jan–Mar 2026</p>
    <div class="bars">
      <div class="bar"><span class="f-s">YNG views</span><span class="t"><i style="width:{b['pct_base']}%"></i></span><span class="v">{b['value']}</span></div>
      <div class="bar us"><span class="f-s">This test</span><span class="t"><i style="width:{b['pct_plan']}%"></i></span><span class="v">{MODEL['total_label']}</span></div>
    </div>
    <p class="ink2">We commit to beat Westside’s best comparable campaign by at least 20%.</p>
  </div>
</div></div>'''
    return slide('numbers', 'The numbers', body, src='Posts count views; boosts count impressions at ₹120 per 1,000. Inputs and sources: appendix.')


def measure():
    rows = [['Footfall per store', 'Entry counts, against matched stores'], ['Codes used', 'Logged at billing, per store and idea'],
            ['Member bills', 'Matched by Westside’s analysts'], ['Views', 'Platform reports, weekly']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Measured at the billing counter.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('5%+', 'more entries than matched stores', 'draft threshold, set from your data')}</div>
  {table(['What we count', 'How'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('measure', 'Measurement', body, src='We see store totals only, never personal data.')


def test():
    body = '''<div class="stack-l grow">
<h2 class="h1">Start with one city. If the numbers don’t move, you lose nothing.</h2>
<div class="row c2 vc grow">
  <div class="opt rec stack"><p class="label">Option A · recommended</p><h3 class="h2">A store launch</h3><p class="ink2">Your next opening and its city.</p></div>
  <div class="opt stack"><p class="label mute">Option B</p><h3 class="h2">The wedding season</h3><p class="ink2">One city through the wedding dates.</p></div>
</div>
<div class="row c3">
  <div class="rule-plan"><p class="h4">If it works</p><p class="mt-s">You pay our fee, plus production and media up to an agreed cap.</p></div>
  <div class="rule-plan"><p class="h4">If it doesn’t</p><p class="mt-s">No fee. We carry production and media up to that cap.</p></div>
  <div class="rule-plan"><p class="h4">What we need</p><p class="mt-s">A test city, matched stores, counter and bill data, a code field at billing.</p></div>
</div></div>'''
    return slide('test', 'The test', body)


def timeline():
    weeks = 17
    phases = [('Set up', 1, 3, 'line', 'Codes at billing, after Diwali'), ('Cast and build', 2, 5, 'line', 'Stylists, creators, carts'),
              ('Styled by Westside', 5, 17, 'plan', '120 looks'), ('Coffee Cart', 7, 13, 'plan', 'Thursday to Sunday, six weeks'),
              ('Window Stories', 5, 17, 'plan', 'A new story every four weeks'), ('Readout', 17, 18, 'ink', 'Go or no&#8209;go')]
    head = ''.join(f'<span class="wk label">{i}</span>' for i in range(1, weeks + 1))
    rows = ''.join(f'<p class="h4 ph">{n}</p><i class="bar-{c}" style="grid-column:{s + 1}/{e + 1}"></i><p class="ink2 f-s note">{t}</p>' for n, s, e, c, t in phases)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Sixteen weeks to a readout.</h2>
<div class="gantt vc grow"><span></span>{head}{rows}</div>
<div class="row c3 dates">
  <div class="rule"><p class="label mute">Set up</p><p class="mt-s">2 to 29 November</p></div>
  <div class="rule-plan"><p class="label">Live</p><p class="mt-s">30 November to 21 February</p></div>
  <div class="rule"><p class="label mute">Readout</p><p class="mt-s">Week of 22 February 2027</p></div>
</div></div>'''
    return slide('timeline', 'Timeline', body, src='Dates assume a working session by 27 October and signature by 30 October.')


def mask360():
    pillars = [('Social', 'Series, creators, pages'), ('Content', 'Stylists, shoots, edits'), ('Events and retail', 'The cart and the windows'), ('Measurement', 'The store scorecard')]
    p = ''.join(f'<div><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in pillars)
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-7-5" style="align-items:end">
  <div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div>
  <p class="lede">A creative and content agency in India and the UAE.</p>
</div>
<div class="row c4 pillars mt-m">{p}</div>
<div class="rule mt-m"><p class="label mute">Brands we have worked with</p><p class="mt-s f-l">Dior · L’Oréal · FCUK Beauty · Dyson · Anantara · Atlantis The Royal · St. Regis · Ferrari · Rolls-Royce · Swisse · Zorae · Rustomjee · Chandak Group</p></div>
</div>'''
    return slide('mask360', 'Mask360', body, dark=True)


def next_steps():
    body = '''<div class="row c-6-6 grow" style="align-items:end">
<div class="stack-l">
  <h2 class="h-display" style="font-size:calc(var(--u)*5.4)">Choose the first city.</h2>
  <p class="lede">One working session. Fixed scope and terms within 72 hours.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Pick the test.</li><li>Share counter and bill data.</li><li>Agree the threshold, fee and cap.</li><li>Start the Monday after signing.</li></ol>
  <div class="rule-plan"><p class="h3">Kaavish · Mask360</p><p class="ink2 mt-s">mask360.agency</p></div>
</div></div>'''
    return slide('next', 'Next steps', body)


def close():
    body = f'''<div class="grow" style="display:grid;place-items:center">
<div class="close-mark">
  <svg class="w" viewBox="0 0 1506 1194" aria-label="Westside"><use href="#logo-w"/></svg>
  <span class="label line">Westside × Mask360 · from the post to the billing counter</span>
  {M_MARK}
</div></div>'''
    return slide('close', 'Westside × Mask360', body, bare=True, dark=True, cloth=('ink', 11))


def references():
    out = []
    n = len(REF_GROUPS)
    for i, (title, vids) in enumerate(REF_GROUPS):
        cards = ''.join(video_card(v['item'], v['caption'], span=v.get('span', '')) for v in vids)
        body = f'''<div class="row c-3-9 grow">
<div class="stack-l">
  <h2 class="h1">{title}.</h2>
  <p class="ink2 lede-s">References the team collected. Press play.</p>
</div>
<div class="vgrid two-rows vc">{cards}</div>
</div>'''
        out.append(slide(f'references-{i + 1}', f'Appendix · references {i + 1} of {n}', body))
    return out


def model():
    rows = MODEL['table']
    base = sum(v[1] for v in MODEL["by_idea"].values())
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">The model, line by line.</h2>
  <p class="ink2 lede-s">Posts count views ({_mn(base - PAID)}&nbsp;mn); boosts count impressions at ₹120 per 1,000 ({_mn(PAID)}&nbsp;mn). Figures in millions.</p>
</div>
{table(['Idea', 'Channel', 'Units', 'Average per unit', 'Low', 'Plan', 'High'], rows['rows'], cls='tbl small tight model', right=(2, 3, 4, 5, 6), total=rows['total'], col_cls={3: 'm-hide', 4: 'm-hide', 5: 'plan-col', 6: 'm-hide'})}
</div>'''
    return slide('model', 'Appendix · the impressions model', body, src=MODEL['src'])


def sources():
    items = ''.join(f'<div><p class="label">{a}</p><p class="f-s ink2 mt-s">{b}</p></div>' for a, b in SOURCES)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Sources.</h2>
<div class="srcs">{items}</div>
</div>'''
    return slide('sources', 'Appendix · sources', body, src='Primary documents are saved as text in the proposal’s research notes.')


def slides():
    return [cover(), promise(), today(), last12(), voice(), competition(), plan(), styling(), styling_plan(),
            cart(), cart_designs(), cart_plan(), windows(), windows_scale(), look_path(), numbers(), measure(), test(), timeline(),
            mask360(), next_steps(), close(), *references(), model(), sources()]
