"""Facts and numbers for the v4 slides. Values marked [[ ]] are waiting on the verified research and fail STRICT builds."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Primary sources (research_notes/Westside proposal v4/sources): Trent Q2 FY26, Q3 FY26, Q4 FY26 and Q2 FY27 store updates;
# Trent Q2 FY26, Q4 FY26 and Q1 FY27 investor presentations. Checked 16 Oct 2026.
F = {
    'stores': '311', 'stores_added': '50', 'cities': '97', 'members': '19', 'online': '6%',
}

# (month, event html, result html, quiet?) — research note 03, 16 Oct 2026
LAST12 = [
    ('Nov ’25', '<b>Wedding season</b> A men’s wedding style guide on westside.com, built on Kala by E.T.A.', 'An edit page, no campaign', True),
    ('Dec ’25', '<b>Glitz &amp; Glam</b> A party capsule with the I-pop group W.i.S.H.', 'In store and online', False),
    ('Jan ’26', '<b>No sale campaign</b> No Republic Day or end-of-season push, in line with Westside’s no-discount stance.', '', True),
    ('Feb ’26', '<b>Wesness Fun Run</b> Mumbai, 8 February, with a W.i.S.H. live set.', '3,600+ participants', False),
    ('Mar ’26', '<b>YNG</b> Westside’s creator community reports its year to investors.', '4,000 members, 6 mn views', False),
    ('Apr ’26', '<b>Run2Quiz, Run2Zumba</b> Wesness runs from stores in Bengaluru and Mumbai.', 'Reported as registrations', False),
    ('May ’26', '<b>Wesness Fun Run</b> Bengaluru, with Run2Rave, pickleball and heritage runs in four cities.', '3,300+ participants', False),
    ('Jun ’26', '<b>AGM</b> About 50 new Westside stores a year.', 'No brand activity found', True),
    ('Jul ’26', '<b>Run2Stepup</b> Mumbai, 19 July, the last Wesness event we found.', '400–500 designs a week, said in a Bloomberg interview', False),
    ('Aug ’26', '<b>Quiet month</b> No Independence Day or back-to-college work found.', '', True),
    ('Sep ’26', '<b>9 Days 9 Colours</b> The Navratri edit on westside.com.', '311 stores at quarter end', False),
    ('Oct ’26', '<b>FRONT ROW</b> A fashion and culture platform: 80 looks, 150 culture-shapers, 30 New Faces.', 'Dance Off cities not yet announced', False),
]

POSITIONING = {
    'year_line': 'A year of community and culture platforms, festive edits on westside.com and 50 new stores. Results were reported as turnout and views, never as store visits.',
    'year_stats': [('6 mn', 'views from YNG, Westside’s 4,000-member creator community', 'Trent Q4 FY26 investor presentation'),
                   ('3,600+', 'people at the biggest Wesness run, Mumbai, February 2026', 'Trent Q4 FY26 investor presentation'),
                   ('None', 'of the published results counts a store visit', 'our review of Trent filings, decks and press')],
    'year_src': ('Sources: Trent investor presentations Q4 FY26 (22 Apr 2026) and Q1 FY27 (6 Aug 2026); Trent store updates; Indian Retailer, '
                 '3 Oct 2026 (FRONT ROW); westside.com; Wesness listings; Bloomberg, 20 Jul 2026. “Not found” means not found in public sources.'),
    'voice_title': 'Westside talks through communities, not campaigns.',
    'voice_lede': 'The everyday voice is warm and inclusive. The events are editorial. What is missing is a line that joins them, and the step from the post into the store.',
    'themes': ['<b>New Indian talent.</b> YNG creators, 30 New Faces, FRONT ROW.',
               '<b>Culture beyond clothes.</b> I-pop, dance-offs, fitness runs.',
               '<b>Women together.</b> Wesness runs in four cities, 3,600 at the biggest.',
               '<b>Own labels as the hero.</b> Bombay Paisley, E.T.A, Utsa, Vark, W Edit.'],
    'opportunities': ['Tell shoppers what is new each week, and in which store. Today the 400–500 designs a week are a story told to investors.',
                      'Turn festive edits into one story from Navratri to the wedding season, carried in store and on social.',
                      'Give every new store the same local launch: creators, styled looks, a reason to visit.',
                      'End every post and every event in a store, and count the visit.'],
    'answers': [('Idea 1 · Styled by Westside', 'Shows what is new every week, styled into complete looks, and names the store that has them.'),
                ('Idea 2 · The Westside Coffee Cart', 'Gives every launch and every busy weekend a reason to visit, and counts the people it brings in.'),
                ('Idea 3 · Window Stories', 'Turns the festive and wedding season into stories people see in the window, then walk in to buy.')],
    'voice_src': ('Sources: Trent investor presentations Q2 FY26 to Q1 FY27 (Wesness, YNG), Indian Retailer, 3 Oct 2026 (FRONT ROW), westside.com, '
                  'Bloomberg (20 Jul 2026).'),
}

# research note 04, rows re-checked with searches on 16 Oct 2026 (sources listed in the note)
COMPETITORS = [
    {'name': 'Shoppers Stop', 'stores': '288 stores, Jun 2026',
     'did': '“India Weds”, “The Travel Edit” and “Get Spotlight Ready” with HYBE India. Reports customer entries up 3% like-for-like, five quarters running.',
     'win': 'Every Westside look is Westside’s own. Styled weekly and shown store by store, it is a look no multi-brand floor can promise.'},
    {'name': 'Max Fashion', 'stores': 'Landmark Group',
     'did': '“How New Is Your New?” films with Siddhant Chaturvedi, Kalki Koechlin and Alaya F, selling weekly newness (Aug 2025).',
     'win': 'Show what is new instead of saying it: this week’s looks, on Westside’s pages and in each store’s window.'},
    {'name': 'Pantaloons', 'stores': 'ABFRL',
     'did': 'First-ever ambassador, Samantha Ruth Prabhu, with the festive “Spark Your Imagination” campaign on TV, digital and in store (Oct 2025).',
     'win': 'Many real faces instead of one: Westside stylists and local creators, each tied to a named store.'},
    {'name': 'Trends', 'stores': 'Reliance Retail',
     'did': 'Aneet Padda as ambassador (Dec 2025), then “This Holiday, Trend It”: spend ₹1,499, scan a QR code, win a holiday (Apr to May 2026).',
     'win': 'A reason to visit that is not a discount or a draw: a styled look, a coffee, a story in the window.'},
    {'name': 'H&amp;M', 'stores': 'H&amp;M Group',
     'did': '“Icons in the Making” with HYBE India: pop-up parks in six cities with H&amp;M Beauty glam stations (May to Jun 2026). Lollapalooza India 2026 collection.',
     'win': 'Own the moment instead of renting it: the cart and the windows run every month, at Westside’s own stores.'},
    {'name': 'Uniqlo', 'stores': 'about 20 stores',
     'did': 'Linen and fleece campaigns with Kriti Sanon and Jasprit Bumrah (2026). First stores in Bengaluru and Pune (2025).',
     'win': '311 stores against about 20: a local launch for every new Westside and a story in every window.'},
    {'name': 'Myntra', 'stores': 'online only',
     'did': 'Creator School (from Jun 2026, 250+ creators) and triple creator rewards for Big Fashion Festival content.',
     'win': 'Pay creators for store visits, not clicks, with codes counted at the billing counter.'},
]

# The biggest content result Westside has published for the last twelve months: YNG, Trent Q4 FY26 investor presentation.
BASELINE = {
    'label': 'YNG, views reported', 'value': '6 mn', 'pct_base': 40, 'pct_plan': 100,
    'plan_line': ('The biggest content result Westside has published this year is 6 million views from YNG. This plan targets 15 million in twelve '
                  'weeks, and we commit to beat Westside’s own twelve-month total by at least 20%, whichever is higher.'),
    'compare_line': ('Westside’s internal total for the last twelve months replaces the YNG figure in week one. Our commitment: at least 20% above it. '
                     'If organic reach runs behind plan by week six, we move budget into paid Reels to hold the total.'),
    'src': 'Baseline: Trent Q4 FY26 investor presentation (YNG: 4,000 members, 6 mn views, 50,000+ engagements, 12,000+ shares). Plan: the model on the numbers slide.',
}


def _m(units, avg):
    return units * avg


# Inputs. Sourced: clip and meme pages 25,000-50,000 views a post (Qoruz 2025: Rs 1 lakh buys 10-20 meme-page posts and 500,000+ views);
# Reels ads Rs 45-140 per 1,000 impressions in India (2026 benchmarks), planned at Rs 120. Planning assumptions, replaced with real
# averages in week two: Westside Reel 20,000 views, creator Reel 25,000, local creator or store Reel 15,000.
PAGE, WS, CR, LOCAL, CPM = 35_000, 20_000, 25_000, 15_000, 120
LINES = [  # idea, channel, units text, units, avg text, avg, paid?
    ('Styled by Westside', 'Westside’s pages', '36 Reels', 36, '20,000', WS, False),
    ('', 'Creators', '40 Reels', 40, '25,000', CR, False),
    ('', 'Clip, meme and city pages', '55 posts', 55, '35,000', PAGE, False),
    ('', 'Paid Reels boost', '₹1.5 lakh', 150_000, '₹120 CPM', None, True),
    ('Coffee Cart', 'Creators at the cart', '30 Reels', 30, '25,000', CR, False),
    ('', 'Clip, meme, city and food pages', '76 posts', 76, '35,000', PAGE, False),
    ('', 'Westside’s pages', '18 Reels', 18, '20,000', WS, False),
    ('', 'Paid Reels boost', '₹2 lakh', 200_000, '₹120 CPM', None, True),
    ('Window Stories', 'Store teams and local creators', '60 Reels', 60, '15,000', LOCAL, False),
    ('', 'City pages', '50 posts', 50, '35,000', PAGE, False),
    ('', 'Westside’s pages', '28 Reels', 28, '20,000', WS, False),
    ('', 'Paid Reels boost', '₹1.75 lakh', 175_000, '₹120 CPM', None, True),
]


def _imp(units, avg, paid):
    return units / CPM * 1000 if paid else units * avg


def _fmt(x):
    return f'{x / 1e6:.1f} mn' if x >= 1e6 else f'{x / 1e3:.0f}k'


_rows, _tot = [], [0, 0, 0]
_by_idea = {}
_cur = ''
for idea, ch, ut, u, at, a, paid in LINES:
    _cur = idea or _cur
    base = _imp(u, a, paid)
    lo, hi = (base, base) if paid else (base * .6, base * 1.5)
    _rows.append([idea, ch, ut, at, _fmt(lo), _fmt(base), _fmt(hi)])
    for i, v in enumerate((lo, base, hi)):
        _tot[i] += v
    _by_idea.setdefault(_cur, [0, 0, 0])
    for i, v in enumerate((lo, base, hi)):
        _by_idea[_cur][i] += v
PAID = sum(_imp(u, a, p) for _, _, _, u, _, a, p in LINES if p)


def _label(x):
    return f'{x / 1e6:.1f}'.rstrip('0').rstrip('.') + ' mn'


MODEL = {
    'total_label': '15 mn',
    'by_idea': _by_idea,
    'table': {'rows': _rows, 'total': ['Total', '', '', '', _fmt(_tot[0]), _fmt(_tot[1]), _fmt(_tot[2])]},
    'src': ('Inputs: clip and meme pages, Qoruz report via Social Samosa, 2025 (₹1 lakh buys 10–20 meme-page posts and 500,000+ views); Reels ads, '
            '₹45–140 per 1,000 impressions in India, 2026 benchmarks, planned at ₹120. Westside and creator averages are planning figures, replaced '
            'with real averages in week two. Low = 60% of organic, high = 150%; paid is fixed.'),
    'styling': {
        'label': _label(_by_idea['Styled by Westside'][1]), 'note': f"range {_label(_by_idea['Styled by Westside'][0])} to {_label(_by_idea['Styled by Westside'][2])}",
        'people': '11', 'people_note': 'a lead, a creative director, three stylists, two shooters, two editors, a pages manager and an analyst',
        'looks': '120',
        'ends': 'Each look has a code. Show it at the store and get the outfit in your size.',
        'rows': [['Stylists', 'Mask360 stylists in Mumbai, Delhi and Bengaluru', '3', 'Every week', '10 complete looks a week, all Westside labels'],
                 ['Shoot days', 'Two shooters and two editors, filming on the shop floor', '24', 'Two a week', '15 Reels and carousels a week'],
                 ['Creators', 'Fashion and lifestyle creators, mostly 50,000 to 500,000 followers', '40', '3 to 4 a week', 'One styled look each, posted on their page'],
                 ['Clip, meme and city pages', 'Paid posts on pages people already follow', '55', '4 to 5 a week', 'Reach beyond Westside’s followers'],
                 ['Westside’s pages', 'Instagram and YouTube Shorts', '36', '3 a week', 'The home of the series'],
                 ['Stores featured', 'Each look tagged to a named store and its rail', '48', '4 a week', 'A code to show at the counter']],
        'src': 'Plan figures are Mask360’s proposal. Impressions from the model on the numbers slide.',
    },
    'cart': {
        'label': _label(_by_idea['Coffee Cart'][1]), 'note': f"range {_label(_by_idea['Coffee Cart'][0])} to {_label(_by_idea['Coffee Cart'][2])}",
        'lede': 'Three carts, three cities, six weeks of weekends. A coffee partner runs the bar under its own food licence; we run the look, the content and the queue.',
        'ends': 'Each cup sleeve carries a look code from the Westside a few metres away.',
        'cups': '21,600', 'cups_note': '72 cart days at about 300 cups a day, a planning figure',
        'people': '12', 'people_note': 'six baristas from the coffee partner, three Westside hosts, a producer, a shooter and a pages manager',
        'rows': [['Carts', 'Built once, in Westside’s look, with the W on the front', '3', 'One each in Mumbai, Bengaluru and Delhi NCR'],
                 ['Cart days', 'Thursday to Sunday, outside Westside stores, malls, colleges and office parks', '72', 'Six weeks, four days a week'],
                 ['Cups', 'Each sleeve carries a look code from the store nearby', '21,600', 'A look in 21,600 hands'],
                 ['Creators at the cart', 'Food, fashion and city creators', '30', 'Reels from the queue, the cup and the store'],
                 ['Clip, meme, city and food pages', 'Paid posts, timed to cart days', '76', 'The cart reaches people who never see it'],
                 ['Licences', 'Coffee partner’s food licence; mall and landlord consent for every site', 'Every site', 'No public-street vending']],
        'src': 'Cups per day and costs are planning figures to confirm with the coffee partner. Impressions from the model on the numbers slide.',
    },
    'windows': {
        'label': _label(_by_idea['Window Stories'][1]), 'note': f"range {_label(_by_idea['Window Stories'][0])} to {_label(_by_idea['Window Stories'][2])}",
        'people': '6', 'people_note': 'a VM lead, two set stylists, a story writer, a rollout coordinator and a pages manager, working with Westside’s VM team',
        'ends': 'Each window is a complete outfit for two, priced on a card and ready inside.',
        'grid_n': 311, 'picks': {3: 1, 40: 1, 77: 1, 150: 1, 222: 1, 280: 1},
        'stories': [('Mumbai', 'Rahul and Anjali, dinner at eight'), ('Delhi', 'Sunday lunch at Nani’s'), ('Bengaluru', 'First day at the new job'),
                    ('Kolkata', 'Pujo, the fourth night'), ('Hyderabad', 'A cousin’s mehendi'), ('Pune', 'The college reunion')],
        'rows': [['Stories written and designed', '12 a quarter', 'A library each store picks from'],
                 ['Window changes', 'Every 4 weeks', 'A new reason to stop at the glass'],
                 ['Stores in the first twelve weeks', 'The test city’s stores', 'Then every Westside, in waves'],
                 ['Reels from each window', '60', 'Filmed by store teams and local creators']],
        'src': 'Rollout and costs are planning figures to confirm with Westside’s VM team. Impressions from the model on the numbers slide.',
    },
}

MANIFEST = HERE.parent / 'media' / 'out' / 'manifest.json'
_items = {v['slug']: v for v in json.loads(MANIFEST.read_text())} if MANIFEST.exists() else {}
# captions are written once the clips are seen; until then every clip gets a neutral caption
VIDEOS = [{'item': v, 'caption': f'<b>Reference {i + 1}</b>'} for i, v in enumerate(_items.values())]
