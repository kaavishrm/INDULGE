"""Facts and numbers for the v4 slides. Values marked [[ ]] are waiting on the verified research and fail STRICT builds."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# research note 01, verified 16 Oct 2026
F = {
    'stores': '311', 'stores_added': '50', 'cities': '97', 'wsc': '11.85', 'online': '6%',
}

# (month, event html, result html, quiet?)
LAST12 = [
    ('Nov ’25', '<b>[[event]]</b> [[detail]]', '[[result]]', False),
    ('Dec ’25', '<b>[[event]]</b>', '', True),
    ('Jan ’26', '<b>[[event]]</b>', '', False),
    ('Feb ’26', '<b>Wesness run, Mumbai</b> [[detail]]', '3,500+ women', False),
    ('Mar ’26', '<b>[[event]]</b>', '', True),
    ('Apr ’26', '<b>[[event]]</b>', '', False),
    ('May ’26', '<b>[[event]]</b>', '', True),
    ('Jun ’26', '<b>[[event]]</b>', '', False),
    ('Jul ’26', '<b>[[event]]</b>', '', True),
    ('Aug ’26', '<b>[[event]]</b>', '', False),
    ('Sep ’26', '<b>[[event]]</b>', '', False),
    ('Oct ’26', '<b>FRONT ROW</b> launched in Mumbai, 80 looks, 150 culture-shapers', '[[result]]', False),
]

POSITIONING = {
    'year_line': '[[One plain sentence on what the year added up to.]]',
    'year_stats': [('[[n]]', '[[what]]', '[[source]]'), ('[[n]]', '[[what]]', '[[source]]'), ('[[n]]', '[[what]]', '[[source]]')],
    'year_src': 'Sources: [[sources]]',
    'voice_title': '[[How Westside talks today, one line]]',
    'voice_lede': '[[lede]]',
    'themes': ['[[theme]]', '[[theme]]', '[[theme]]', '[[theme]]'],
    'opportunities': ['[[opportunity]]', '[[opportunity]]', '[[opportunity]]', '[[opportunity]]'],
    'voice_src': 'Sources: [[sources]]',
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
