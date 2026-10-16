"""Facts and numbers for the v4 slides.

Westside facts come from Trent's own documents, fetched as text into research_notes/Westside proposal v4/sources/:
store updates for Q2 FY26 (261 stores), Q3 FY26 (278), Q4 FY26 (300) and investor presentations for Q2 FY26, Q4 FY26
and Q1 FY27 (301 stores, 97 cities, online over 6%, like-for-like, Wesness, YNG). The Q2 FY27 update (5 Oct 2026, +10 Westside
stores, revenue +23%) is cited as reported by Upstox and Angel One. Values marked [[ ]] fail STRICT builds. Checked 16 Oct 2026."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent

F = {'stores': '311', 'stores_added': '50', 'cities': '97', 'members': '19 mn+', 'online': '6%+', 'growth': '+23%'}

# (month, event html, result html, quiet?) — research note 03 and the Trent documents above
LAST12 = [
    ('Nov ’25', '<b>Wedding season</b> A men’s wedding style guide on westside.com, featuring Kala by E.T.A.', 'An edit page; we found no campaign', True),
    ('Dec ’25', '<b>Glitz &amp; Glam</b> A party capsule with the I-pop group W.i.S.H.', 'In store and online', False),
    ('Jan ’26', '<b>Quiet month</b> We found no Republic Day or end-of-season sale campaign.', '', True),
    ('Feb ’26', '<b>Wesness Fun Run</b> Mumbai, 8 February, with a W.i.S.H. live set.', '3,600+ participants', False),
    ('Mar ’26', '<b>YNG</b> Trent’s Q4 deck reports Westside’s creator community.', '4,000 members, 6&nbsp;mn views', False),
    ('Apr ’26', '<b>Run2Quiz, Run2Zumba</b> Wesness runs that start at stores in Bengaluru and Mumbai.', '₹499 entry; no results published', False),
    ('May ’26', '<b>Wesness Fun Run</b> Bengaluru, plus Run2Rave, pickleball and heritage runs in four cities.', '3,300+ participants', False),
    ('Jun ’26', '<b>AGM</b> Trent plans about 50 new Westside stores a year.', 'We found no brand activity', True),
    ('Jul ’26', '<b>Run2Stepup</b> Mumbai, 19 July, the last Wesness event we found.', '', True),
    ('Aug ’26', '<b>Quiet month</b> We found no Independence Day or back-to-college work.', '', True),
    ('Sep ’26', '<b>9 Days 9 Colours</b> The Navratri edit on westside.com.', '311 stores at quarter end', False),
    ('Oct ’26', '<b>FRONT ROW</b> A fashion and culture platform: 80 looks, 150 culture-shapers, 30 New Faces.', 'Three national Dance Off challenges to come', False),
]

POSITIONING = {
    'year_title': 'A year measured in turnout and views.',
    'year_line': 'Runs, a creator community, a culture platform and festive edits on westside.com, while 50 new stores opened.',
    'year_stats': [('6&nbsp;mn', 'views from YNG, Westside’s 4,000-member creator community', 'Trent Q4 FY26 investor presentation'),
                   ('3,600+', 'people at the biggest Wesness run, Mumbai, February 2026', 'Trent Q4 FY26 investor presentation'),
                   ('0', 'published results we found that count a store visit', 'our review of Trent filings, decks and press, to 16 Oct 2026')],
    'year_src': ('Sources: Trent investor presentations Q4 FY26 (22 Apr 2026) and Q1 FY27 (6 Aug 2026); Trent store updates; Indian Retailer, '
                 '3 Oct 2026 (FRONT ROW); westside.com; Wesness listings. Anything marked as not found means none in public sources.'),
    'voice_title': 'Westside speaks through YNG, Wesness and FRONT ROW.',
    'voice_lede': 'The everyday voice is warm and inclusive; the events are editorial. Nothing yet links the two, or takes people from a post into a store.',
    'themes': ['<b>New Indian talent.</b> YNG creators, 30 New Faces, FRONT ROW.',
               '<b>Culture beyond clothes.</b> I-pop, dance-offs, fitness runs.',
               '<b>Women together.</b> Wesness runs in four cities, 3,600+ at the biggest.',
               '<b>Own labels first.</b> Bombay Paisley, E.T.A, Utsa, Vark, W Edit.'],
    'opportunities': ['Shoppers rarely hear about the 400–500 new designs a week. Tell them, store by store.',
                      'Turn festive edits into one story from Navratri to the wedding season, in store and on Instagram.',
                      'Give every new store the same local launch, with creators and looks styled from its rails.',
                      'End every post and every event in a store, and count the visit.'],
    'answers': [('Styled by Westside', 'Starts with YNG’s creators and the new designs that land every week.'),
                ('The Westside Coffee Cart', 'Goes where Westside already gathers people, from Wesness finish lines to launch weekends.'),
                ('Window Stories', 'Casts FRONT ROW’s New Faces as the couples and families in the windows.')],
    'voice_src': ('Sources: Trent investor presentations Q2 FY26 to Q1 FY27 (Wesness, YNG), Indian Retailer, 3 Oct 2026 (FRONT ROW), westside.com, '
                  'Bloomberg interview with Shailina Parti, 20 Jul 2026 (designs).'),
}

# research note 04, every row re-checked by search on 16 Oct 2026; source pages are fetched into sources/
COMPETITORS = [
    {'name': 'Shoppers Stop', 'stores': '288 stores, Jun&nbsp;2026',
     'did': '“India Weds with Shoppers Stop”, “The Travel Edit” and “Get Spotlight Ready” with HYBE India (Apr to Jun 2026). Customer entries up 3% like-for-like.',
     'win': 'Every piece is Westside’s own, so each weekly look is stocked in a named store. A multi&#8209;brand floor cannot promise that.'},
    {'name': 'Max Fashion', 'stores': 'Landmark Group',
     'did': '“How New Is Your New?” films with Siddhant Chaturvedi, Kalki Koechlin and Alaya F, selling weekly newness (Aug to Sep 2025).',
     'win': 'Show this week’s new looks on Westside’s pages and in each store’s window.'},
    {'name': 'Pantaloons', 'stores': 'ABFRL',
     'did': 'First-ever ambassador, Samantha Ruth Prabhu, with the festive “Spark Your Imagination” campaign (Oct 2025).',
     'win': 'Westside stylists and local creators instead of one star, each tied to a named store.'},
    {'name': 'Trends', 'stores': 'Reliance Retail',
     'did': '“This Holiday, Trend It” with Aneet Padda: spend ₹1,499 or more, scan a QR code in store, enter a draw for 100+ holidays (20 Apr to 17 May 2026).',
     'win': 'No discounts or lucky draws. People come in for a styled look, a coffee or a window story.'},
    {'name': 'H&amp;M', 'stores': '71 stores in India',
     'did': '“Icons in the Making” with HYBE India: pop-ups in six cities with H&amp;M Beauty stations (May to Jun 2026). A Lollapalooza India 2026 collection.',
     'win': 'The cart and the windows run at Westside’s own stores, on Westside’s calendar, so the visits stay with Westside.'},
    {'name': 'Uniqlo', 'stores': 'Uniqlo India',
     'did': 'Three openings in Bengaluru and Pune (Mar to Jun 2026). A fleece campaign with Kriti Sanon and Jasprit Bumrah (Oct 2026).',
     'win': 'With 311 stores, every new Westside gets a local launch and every window a story.'},
    {'name': 'Myntra', 'stores': 'online only',
     'did': 'A second Creator School with 300+ creators, and triple earnings for creators on festive content ahead of the Big Fashion Festival (2026).',
     'win': 'Tie every creator post to a named store and count its code at the billing counter.'},
]

# The biggest content figure Westside has published in the last twelve months: YNG, Trent Q4 FY26 investor presentation.
BASELINE = {
    'label': 'YNG, views', 'value': '6&nbsp;mn', 'pct_base': 40, 'pct_plan': 100,
    'plan_line': ('Westside’s biggest published content figure in the last year is 6&nbsp;mn YNG views. The test targets 15&nbsp;mn impressions in twelve weeks, '
                  'and at least 20% more reach than Westside’s best comparable campaign of the last year.'),
    'compare_line': ('Views count plays; impressions count every showing. In week one we swap in Westside’s best comparable campaign of the last '
                     'twelve months and commit to beat its reach by at least 20%. If organic reach is behind plan by week six, we move budget into paid Reels.'),
    'src': 'Baseline: Trent Q4 FY26 investor presentation (YNG: 4,000 members, 6 mn views, 50,000+ engagements, 12,000+ shares). Plan: the model on the numbers slide.',
}

# Inputs. Clip and city pages 25,000-50,000 views a post (Qoruz 2025: Rs 1 lakh buys 10-20 meme-page posts and 500,000+ views);
# Reels ads Rs 45-140 per 1,000 impressions in India (Upgrowth 2026 benchmarks), planned at Rs 120. Planning figures, replaced with real
# averages in week two: Westside Reel 20,000 views, creator Reel 25,000, local creator or store Reel 15,000.
PAGE, WS, CR, LOCAL, CPM = 35_000, 20_000, 25_000, 15_000, 120
LINES = [  # idea, channel, units text, units, avg text, avg, paid?
    ('Styled by Westside', 'Westside’s pages', '36 Reels', 36, '20,000', WS, False),
    ('', 'YNG and city creators', '40 Reels', 40, '25,000', CR, False),
    ('', 'Clip and city pages', '55 posts', 55, '35,000', PAGE, False),
    ('', 'Paid Reels boost', '₹1.5 lakh', 150_000, '₹120 per 1,000', None, True),
    ('Coffee Cart', 'Creators at the cart', '30 Reels', 30, '25,000', CR, False),
    ('', 'Clip, city and food pages', '76 posts', 76, '35,000', PAGE, False),
    ('', 'Westside’s pages', '18 Reels', 18, '20,000', WS, False),
    ('', 'Paid Reels boost', '₹2 lakh', 200_000, '₹120 per 1,000', None, True),
    ('Window Stories', 'Store teams and local creators', '60 Reels', 60, '15,000', LOCAL, False),
    ('', 'City pages', '50 posts', 50, '35,000', PAGE, False),
    ('', 'Westside’s pages', '28 Reels', 28, '20,000', WS, False),
    ('', 'Paid Reels boost', '₹1.75 lakh', 175_000, '₹120 per 1,000', None, True),
]


def _imp(units, avg, paid):
    return units / CPM * 1000 if paid else units * avg


def _mn(x):
    return f'{x / 1e6:.2f}'


_rows, _tot, _by_idea, _cur = [], [0, 0, 0], {}, ''


def _subtotal(name):
    lo, base, hi = _by_idea[name]
    return ['', f'<b>{name}, total</b>', '', '', f'<b>{_mn(lo)}</b>', f'<b>{_mn(base)}</b>', f'<b>{_mn(hi)}</b>']


for idea, ch, ut, u, at, a, paid in LINES:
    if idea and _cur:
        _rows.append(_subtotal(_cur))
    _cur = idea or _cur
    base = _imp(u, a, paid)
    lo, hi = (base, base) if paid else (base * .6, base * 1.5)
    _rows.append([idea, ch, ut, at, _mn(lo), _mn(base), _mn(hi)])
    for i, v in enumerate((lo, base, hi)):
        _tot[i] += v
    _by_idea.setdefault(_cur, [0, 0, 0])
    for i, v in enumerate((lo, base, hi)):
        _by_idea[_cur][i] += v
_rows.append(_subtotal(_cur))
PAID = sum(_imp(u, a, p) for _, _, _, u, _, a, p in LINES if p)


def _label(x):
    return f'{x / 1e6:.1f}'.rstrip('0').rstrip('.') + '&nbsp;mn'


def _range(k):
    lo, _, hi = _by_idea[k]
    return f'range {_label(lo)} to {_label(hi)}'


MODEL = {
    'total_label': '15&nbsp;mn',
    'by_idea': _by_idea,
    'table': {'rows': _rows, 'total': ['Total', '', '', '', _mn(_tot[0]), _mn(_tot[1]), _mn(_tot[2])]},
    'src': ('Inputs: clip and city pages at 35,000 views a post, from a Qoruz report via Social Samosa, 2025 (₹1 lakh buys 10–20 meme-page posts and '
            '500,000+ views). Reels ads at ₹45–140 per 1,000 impressions in India (Upgrowth, 2026), planned at ₹120. Westside and creator averages are '
            'planning figures, replaced with real averages in week two. Low = 60% of organic, high = 150%; paid is fixed.'),
    'styling': {
        'label': _label(_by_idea['Styled by Westside'][1]), 'note': _range('Styled by Westside'),
        'ends': 'Each look has a code. Show it at the store and the team brings the outfit in your size.',
        'people': '11', 'people_note': 'a lead, a creative director, three stylists, two camera operators, two editors, a pages manager and an analyst',
        'looks': '120',
        'rows': [['Stylists', 'Mask360 stylists, working from the test city’s Westside stores', '3', 'Every week', '10 complete looks a week between them, all Westside labels'],
                 ['Shoot days', 'Two camera operators and two editors, filming on the shop floor', '24', '2 a week', '3 Reels a week for Westside’s pages, plus cut-downs for clip and city pages'],
                 ['Creators', 'YNG members first, then fashion and lifestyle creators with 50,000 to 500,000 followers', '40', '3 to 4 a week', 'One styled look each, posted on their page'],
                 ['Clip and city pages', 'Paid posts on pages people already follow; Westside approves the list', '55', '4 to 5 a week', 'Reach beyond Westside’s followers'],
                 ['Westside’s pages', 'Instagram and YouTube Shorts', '36', '3 a week', 'Every look in one place'],
                 ['Stores featured', 'Each look tagged to a named store and its rail', '48', '4 a week', 'A code to show at the counter']],
        'src': 'Plan figures are Mask360’s proposal for the twelve-week test. Impressions from the model on the numbers slide.',
    },
    'cart': {
        'label': _label(_by_idea['Coffee Cart'][1]), 'note': _range('Coffee Cart'),
        'ends': 'Each cup sleeve carries a look code from the nearest Westside.',
        'lede': 'Three carts in the test city, Thursday to Sunday for six weeks. A coffee partner runs the bar under its own food licence; we run the rest.',
        'cups': '21,600', 'cups_note': '72 cart days at about 300 cups a day, a planning figure',
        'people': '12', 'people_note': 'six baristas from the coffee partner, three Mask360 hosts in Westside uniform, a producer, a camera operator and a pages manager',
        'rows': [['Carts', 'Built once, in Westside’s look, with the W on the front', '3', 'Each at a different site in the test city'],
                 ['Cart days', 'Thursday to Sunday, on Westside forecourts, in malls, at colleges and in office parks', '72', 'Six weeks, four days a week'],
                 ['Cups', 'Coffee sold at café prices by the partner; no free cup, no discount', '21,600', '21,600 look codes handed out'],
                 ['Creators at the cart', 'Food, fashion and city creators', '30', 'Reels from the queue, the cup and the store'],
                 ['Clip, city and food pages', 'Paid posts, timed to cart days', '76', 'People who never pass the cart still see it'],
                 ['Licences', 'Coffee partner’s food licence; mall and landlord consent for every site', 'Every site', 'No public-street vending']],
        'src': 'Cups per day is a planning figure to confirm with the coffee partner. Impressions from the model on the numbers slide.',
    },
    'windows': {
        'label': _label(_by_idea['Window Stories'][1]), 'note': _range('Window Stories'),
        'ends': 'Each window shows two complete outfits, priced on a card and stocked inside.',
        'people': '6', 'people_note': 'a VM lead, two set stylists, a story writer, a rollout coordinator and a pages manager, working with Westside’s VM team',
        'grid_n': 311,
        'stories': [('Rahul and Anjali', 'Getting ready for a date'), ('The first invite', 'Dressing for a cousin’s mehendi'),
                    ('Monday', 'First day at the new job'), ('Sunday', 'Lunch at Nani’s'),
                    ('New Year’s Eve', 'The party at home'), ('Ten years on', 'The college reunion')],
        'rows': [['Stories written and designed', '12 a quarter', 'A library each store picks from'],
                 ['Window changes', 'Every four weeks', 'A new story to stop for'],
                 ['Stores in the test', 'Every Westside in the test city', 'Then every store, in waves'],
                 ['Reels from the windows, in total', '60', 'Filmed by store teams and local creators']],
        'src': 'Rollout is a planning figure to confirm with Westside’s VM team. Impressions from the model on the numbers slide.',
    },
}

MANIFEST = HERE.parent / 'media' / 'out' / 'manifest.json'
_items = {v['slug']: v for v in json.loads(MANIFEST.read_text())} if MANIFEST.exists() else {}


# Reference clips from the team's Drive folder (WhatsApp exports, 576x1024), captioned by format only.
# 18-42-50-1 repeats 18-20-19 and is left out.
def _v(key, caption):
    return {'item': _items.get('whatsapp-video-2026-10-16-at-' + key), 'caption': caption}


REF_GROUPS = [
    ('Styling formats', [
        _v('18-42-52-1', '<b>One shirt, six ways</b>'),
        _v('18-42-52-2', '<b>Four ways to wear denim</b>'),
        _v('18-19-59', '<b>A mood, then five looks</b>'),
        _v('18-42-51', '<b>One oversized shirt</b>'),
        _v('18-42-51-1', '<b>The try-on, talked through</b>'),
        _v('18-20-04', '<b>Six looks, six moments</b>'),
        _v('18-42-53-1', '<b>Bandhani on the street</b>'),
        _v('18-42-53-2', '<b>Styled from a studio rail</b>'),
        _v('18-42-53', '<b>A saree, layered</b>'),
        _v('18-42-54', '<b>The denim edit, explained</b>'),
        _v('18-42-53-3', '<b>Looks built on one colour</b>'),
        _v('18-42-50', '<b>A creator’s own take</b>'),
    ]),
    ('Finish, store moments and craft', [
        _v('18-20-13', '<b>Fit, captioned on screen</b>'),
        _v('18-20-15', '<b>One studio, quick cuts</b>'),
        _v('18-20-10', '<b>A rail of jackets, outdoors</b>'),
        _v('18-20-19', '<b>One denim jacket</b>'),
        _v('18-20-25', '<b>One bag, told as a story</b>'),
        _v('18-42-50-2', '<b>Straight from the rails</b>'),
        _v('18-42-52', '<b>A creator’s afternoon in store</b>'),
        _v('18-19-48', '<b>A drop launched in store</b>'),
        _v('18-19-55', '<b>A photo booth in store</b>'),
        _v('18-20-03', '<b>A pop-up truck</b>'),
        _v('18-42-51-2', '<b>From dress form to look</b>'),
        _v('18-42-51-3', '<b>A look built on the form</b>'),
    ]),
]
VIDEOS = [v for _, vs in REF_GROUPS for v in vs]
