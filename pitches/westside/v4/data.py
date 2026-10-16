"""Facts and numbers for the v4 slides. Values marked [[ ]] are waiting on the verified research and fail STRICT builds."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# research note 01, verified 16 Oct 2026
F = {
    'stores': '311', 'stores_added': '50', 'cities': '97', 'wsc': '11.85', 'online': '6%',
}

# (month, event html, result html, quiet?) — research note 03, 16 Oct 2026
LAST12 = [
    ('Nov ’25', '<b>Wedding season</b> A men’s wedding style guide on westside.com, built on Kala by E.T.A.', 'An edit page, no campaign', True),
    ('Dec ’25', '<b>Glitz &amp; Glam</b> A party capsule with the I-pop group W.i.S.H.', 'In store and online', False),
    ('Jan ’26', '<b>No sale campaign</b> No Republic Day or end-of-season push, in line with Westside’s no-discount stance.', '', True),
    ('Feb ’26', '<b>Wesness Fun Run</b> Mumbai, 8 February, with a W.i.S.H. live set.', '3,500+ women; 4,000+ registered', False),
    ('Mar ’26', '<b>Wesness, Hyderabad</b> A promo run from Westside Gachibowli.', '23 stores opened in the quarter', False),
    ('Apr ’26', '<b>Run2Quiz, Run2Zumba</b> Wesness runs from stores in Bengaluru and Mumbai.', 'Reported as registrations', False),
    ('May ’26', '<b>Wesness 5K</b> Women’s run, Bengaluru.', '', True),
    ('Jun ’26', '<b>AGM</b> About 50 new Westside stores a year.', 'No brand activity found', True),
    ('Jul ’26', '<b>Run2Stepup</b> Mumbai, 19 July, the last Wesness event we found.', '400–500 designs a week, told to Bloomberg', False),
    ('Aug ’26', '<b>Quiet month</b> No Independence Day or back-to-college work found.', '', True),
    ('Sep ’26', '<b>9 Days 9 Colours</b> The Navratri edit on westside.com.', '311 stores at quarter end', False),
    ('Oct ’26', '<b>FRONT ROW</b> Mumbai, 1 October: 80 looks, 150 culture-shapers, 30 New Faces.', 'Dance Off cities not yet announced', False),
]

POSITIONING = {
    'year_line': 'A year of community and culture platforms, festive edits on westside.com and 50 new stores. Results were reported as turnout, sign-ups and views.',
    'year_stats': [('+50', 'stores in the twelve months to 30 September 2026', 'Trent Q2 FY27 update, 6 Oct 2026'),
                   ('3,500+', 'women at the biggest Wesness run, Mumbai, 8 February', 'Trent filing to the exchanges, 10 Feb 2026'),
                   ('None', 'of the published results counts a store visit', 'our review of Trent filings, decks and press')],
    'year_src': ('Sources: Trent filings, investor decks and business updates (Feb to Oct 2026); FRONT ROW launch coverage, 1 Oct 2026; '
                 'westside.com edits; Wesness event listings; Bloomberg, 20 Jul 2026. “Not found” means not found in public sources.'),
    'voice_title': 'Westside talks through communities, not campaigns.',
    'voice_lede': 'The everyday voice is warm and inclusive. The events are editorial. What is missing is a line that joins them, and the step from the post into the store.',
    'themes': ['<b>New Indian talent.</b> YNG creators, 30 New Faces, FRONT ROW.',
               '<b>Culture beyond clothes.</b> I-pop, dance-offs, fitness runs.',
               '<b>Women together.</b> Wesness, about 25,000 women in four cities.',
               '<b>Own labels as the hero.</b> Bombay Paisley, E.T.A, Utsa, Vark, W Edit.'],
    'opportunities': ['Tell shoppers what is new each week, and in which store. Today the 400–500 designs a week are a story told to investors.',
                      'Turn festive edits into one story from Navratri to the wedding season, carried in store and on social.',
                      'Give every new store the same local launch: creators, styled looks, a reason to visit.',
                      'End every post and every event in a store, and count the visit.'],
    'answers': [('Idea 1 · Styled by Westside', 'Shows what is new every week, styled into complete looks, and names the store that has them.'),
                ('Idea 2 · The Westside Coffee Cart', 'Gives every launch and every busy weekend a reason to visit, and counts the people it brings in.'),
                ('Idea 3 · Window Stories', 'Turns the festive and wedding season into stories people see in the window, then walk in to buy.')],
    'voice_src': ('Sources: Trent filings and investor decks (Wesness, YNG), FRONT ROW launch coverage (1 Oct 2026), westside.com, '
                  'Bloomberg (20 Jul 2026).'),
}

COMPETITORS = [
    {'name': n, 'stores': '[[stores]]', 'did': '[[what they did in the last twelve months, one or two lines]]', 'win': '[[how Westside wins, one line]]'}
    for n in ('Shoppers Stop', 'Lifestyle', 'Max Fashion', 'Pantaloons', 'Reliance Trends', 'H&M', 'Uniqlo', 'Myntra')
]

BASELINE = {
    'label': 'Last 12 months', 'value': '[[x]] mn', 'pct_base': 80, 'pct_plan': 100,
    'plan_line': '[[Against the baseline line]]', 'compare_line': '[[compare line]]', 'src': '[[source]]',
}

MODEL = {
    'total_label': '15 mn',
    'styling': {'label': '5 mn', 'note': '[[note]]', 'people': '[[n]]', 'people_note': '[[note]]', 'looks': '120', 'src': '[[source]]',
                'rows': [['[[line]]', '[[who]]', '[[n]]', '[[often]]', '[[delivers]]']] * 6},
    'cart': {'label': '5.5 mn', 'note': '[[note]]', 'lede': '[[lede]]', 'cups': '[[n]]', 'cups_note': '[[note]]', 'people': '[[n]]', 'people_note': '[[note]]', 'src': '[[source]]',
             'rows': [['[[line]]', '[[detail]]', '[[n]]', '[[delivers]]']] * 6},
    'windows': {'label': '4.5 mn', 'note': '[[note]]', 'people': '[[n]]', 'people_note': '[[note]]', 'src': '[[source]]', 'grid_n': 311,
                'picks': {3: 1, 40: 1, 77: 1, 150: 1, 222: 1, 280: 1},
                'stories': [('Mumbai', 'Rahul and Anjali, dinner at eight'), ('Delhi', 'Sunday lunch at Nani’s'), ('Bengaluru', 'First day at the new job'),
                            ('Kolkata', 'Pujo, the fourth night'), ('Hyderabad', 'A cousin’s mehendi'), ('Pune', 'The college reunion')],
                'rows': [['[[line]]', '[[n]]', '[[delivers]]']] * 4},
    'table': {'rows': [['[[idea]]', '[[channel]]', '[[n]]', '[[avg]]', '[[low]]', '[[plan]]', '[[high]]']] * 9,
              'total': ['Total', '', '', '', '[[low]]', '15 mn', '[[high]]']},
    'src': '[[sources]]',
}

MANIFEST = HERE.parent / 'media' / 'out' / 'manifest.json'
_items = {v['slug']: v for v in json.loads(MANIFEST.read_text())} if MANIFEST.exists() else {}
# captions are written once the clips are seen; until then every clip gets a neutral caption
VIDEOS = [{'item': v, 'caption': f'<b>Reference {i + 1}</b>'} for i, v in enumerate(_items.values())]
