"""Slide copy for the v4 proposal. Plain, direct, corporate English. Every number on a slide carries its source and date
in the folio line. Facts come from research_notes/Westside proposal v4/ (verified 16 Oct 2026)."""
import json, pathlib
import art
from data import F, LAST12, COMPETITORS, POSITIONING, MODEL, BASELINE, VIDEOS
from kit import slide, stat, ul, table, months, video_card

TITLE = 'Westside × Mask360'
DESCRIPTION = 'Mask360’s proposal to Westside, October 2026: styling as the content engine, the Westside coffee cart and story windows, measured on footfall per store.'
HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = HERE.parent / 'media' / 'out' / 'manifest.json'

# drinks named after Westside labels confirmed live on westside.com (research note 01)
MENU = ['Bombay Paisley Filter Coffee', 'Nuon Cold Brew', 'L.O.V Latte', 'Wardrobe Flat White', 'Utsa Masala Chai', 'Vark Rose Cardamom']


def cover():
    body = f'''<div class="row c-6-6 grow center">
<div class="stack-l">
  <span class="label mute">A proposal to Westside · October 2026</span>
  <h1 class="h-display">From the post to the billing counter.</h1>
  <p class="lede">Content built around styling, a coffee cart people queue for, and windows that tell a story. Measured on one number: footfall per store.</p>
  <p class="f-s mute">Prepared by Mask360 for the Westside leadership team, Trent Limited.</p>
</div>
<div class="art">{art.rail()}</div>
</div>'''
    return slide('cover', 'Proposal', body, src='Scroll, or use the arrow keys, to move between slides.')


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="h-display" style="max-width:15em">We will take Westside from the post to the billing counter.</h2>
<p class="lede">Every idea in this proposal ends inside a Westside store, and every idea is judged on the same number: how many more people walk into that store.</p>
</div>
<div class="row c3">
  <div class="rule"><p class="h3">Test it once</p><p class="mt-s">Give us one store launch or one festive drop.</p></div>
  <div class="rule"><p class="h3">Measure it your way</p><p class="mt-s">Your people counters and your bills, read against stores that did not get the programme.</p></div>
  <div class="rule"><p class="h3">Pay for results</p><p class="mt-s">If the numbers don’t move, you lose nothing.</p></div>
</div>'''
    return slide('promise', 'Our promise', body, dark=True)


def today():
    s = F
    body = f'''<div class="row c-4-8 grow">
<div class="stack-l">
  <h2 class="h1">Westside is growing by opening stores.</h2>
  <p class="lede">The next gain has to come from more people walking into each one. That is what this proposal is built to do.</p>
</div>
<div class="board">
  {stat(s['stores'], 'stores on 30 September 2026', f"{s['stores_added']} more than a year earlier")}
  {stat(s['cities'], 'cities on 30 June 2026', 'latest disclosed count')}
  {stat(s['wsc'], 'active WestStyleClub members, FY26', 'up 53% in a year', small=' mn')}
  {stat(s['online'], 'of Westside revenue is online, Q1 FY27', 'nearly every rupee is spent in a store')}
  {stat('Low', 'single-digit like-for-like growth', 'Trent fashion portfolio, Q4 FY26 to Q1 FY27')}
  {stat('400–500', 'new designs a week', 'Westside’s in-house design team, July 2026')}
</div></div>'''
    src = ('Sources: Trent Q2 FY27 business update, 6 Oct 2026 (stores). Trent Q1 FY27 investor presentation and results, 6 Aug 2026 '
           '(cities, online, like-for-like). Trent FY26 annual report (WestStyleClub). Bloomberg interview with Shailina Parti, 20 Jul 2026 (designs).')
    return slide('today', 'Westside today', body, src=src)


def last12():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">Your last twelve months, on one page.</h2>
  <p class="ink2">{POSITIONING['year_line']}</p>
</div>
{months(LAST12)}
<div class="row c3 mt-auto">
  {''.join(f'<div class="rule">{stat(n, k, s)}</div>' for n, k, s in POSITIONING['year_stats'])}
</div></div>'''
    return slide('last12', 'Westside today · the last twelve months', body, src=POSITIONING['year_src'])


def voice():
    p = POSITIONING
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">{p['voice_title']}</h2>
  <p class="ink2">{p['voice_lede']}</p>
</div>
<div class="row c2 grow mt-m">
  <div class="rule stack"><p class="label mute">What Westside says now</p>{ul(p['themes'], 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label plan">Where we take it</p>{ul(p['opportunities'], 'list big-list')}</div>
</div>
<div class="row c3 mt-auto">{''.join(f'<div class="panel-bg" style="padding:calc(var(--u)*1.2)"><p class="label plan">{a}</p><p class="f-s mt-s">{b}</p></div>' for a, b in p['answers'])}</div>
</div>'''
    return slide('voice', 'Westside today · how Westside talks', body, src=p['voice_src'])


def competition():
    rows = [[f'<b>{c["name"]}</b><br><span class="mute f-s">{c["stores"]}</span>', c['did'], f'<span class="plan">{c["win"]}</span>'] for c in COMPETITORS]
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">What the others did. How Westside wins.</h2>
  <p class="ink2">Their customers are not always Westside’s, but the wallet often is. Each row is what a rival did in the last twelve months, and the move that beats it.</p>
</div>
{table(['Brand', 'What they did, Oct 2025 to Oct 2026', 'How Westside wins'], rows, cls='tbl small tight')}
</div>'''
    return slide('rivals', 'The market', body, src='Sources: company releases and trade press, Oct 2025 to Oct 2026; full list in research_notes/Westside proposal v4/04_competitor_map.md.')


def plan():
    ideas = [
        ('1', 'Styled by Westside', 'Stylists and creators build complete Westside looks every week, film them in store and post them across Westside’s pages, creators and India’s big clip and city pages.', MODEL['styling']),
        ('2', 'The Westside Coffee Cart', 'A Westside-designed cart with a menu named after Westside’s labels. Every cup carries a look from the store next door.', MODEL['cart']),
        ('3', 'Window Stories', 'Two mannequins, one moment everyone recognises, every piece for sale inside. A different story in every store.', MODEL['windows']),
    ]
    cols = ''.join(f'''<div class="idea rule-plan"><span class="no">{n}</span><h3 class="h2">{t}</h3><p>{d}</p>
<div class="mt-auto"><div class="imp">{m['label']}<small>impressions</small></div><p class="f-s mute mt-s">{m['note']}</p></div></div>''' for n, t, d, m in ideas)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">The plan: three ideas, {MODEL['total_label']} impressions, all of it measured in store.</h2>
  <p class="ink2">{BASELINE['plan_line']}</p>
</div>
<div class="row c3 grow">{cols}</div>
</div>'''
    return slide('plan', 'The plan', body, src=BASELINE['src'])


def styling():
    formats = [('One piece, three ways', 'A stylist takes one Westside piece from office to dinner to a family function.'),
               ('Style me for…', 'A creator brings a real occasion. Our stylist dresses them from one store in thirty minutes.'),
               ('Head to toe, one budget', 'A complete look, every piece from the store, with the total on screen.'),
               ('Stylist vs creator', 'Same brief, two looks, the audience picks. The winning look goes on the rail.')]
    f = ''.join(f'<div class="rule"><p class="h4">{a}</p><p class="f-s ink2 mt-s">{b}</p></div>' for a, b in formats)
    body = f'''<div class="row c-6-6 grow">
<div class="stack-l">
  <span class="label plan">Styled by Westside</span>
  <h2 class="h1">Make styling the reason people follow Westside.</h2>
  <p>Westside makes almost everything it sells and launches 400 to 500 new designs a week. Most people never see how those pieces go together. Every week our stylists and creators build complete looks from one Westside store, film them on the floor and post them where people already watch.</p>
  <p>Each look has a code. Show it in store and the team brings you the whole outfit in your size.</p>
  <div class="row c2 gap-s mt-auto">{f}</div>
</div>
<div class="art">{art.rail()}</div>
</div>'''
    return slide('styling', 'Idea 1 of 3', body, src='Design volume: Bloomberg interview with Shailina Parti, 20 Jul 2026. Own-label share: BW Businessworld, 2026.')


def styling_plan():
    m = MODEL['styling']
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">Styled by Westside: who, how many, how often.</h2>
  <p class="ink2">Twelve weeks, three cities. The numbers below are what we commit to deliver.</p>
</div>
{table(['Line', 'Who', 'How many', 'How often', 'What it delivers'], m['rows'], cls='tbl small tight', right=(2,))}
<div class="row c3 mt-auto">
  <div class="rule">{stat(m['label'], 'impressions in twelve weeks', m['note'])}</div>
  <div class="rule">{stat(m['people'], 'people from Mask360 on the programme', m['people_note'])}</div>
  <div class="rule">{stat(m['looks'], 'complete looks, each with a code', 'every look tagged to a named store')}</div>
</div></div>'''
    return slide('styling-plan', 'Idea 1 of 3 · the plan', body, src=m['src'])


def look_path():
    steps = [('Styled in store', 'A stylist or creator builds the look from one store’s rails and films it there.'),
             ('Posted everywhere', 'Westside’s pages, the creator’s page and paid clip and city pages carry the same look in the same week.'),
             ('Saved with a code', 'Every post shows a short look code and the store’s name.'),
             ('Shown at the store', 'The shopper shows the code. The team pulls the look in their size.'),
             ('Billed with the code', 'The code and the WestStyleClub number go on the bill, so we can count it.')]
    cells = ''.join(f'<div class="rule{"-plan" if i == 4 else ""}"><span class="num f-l {"plan" if i == 4 else "mute"}">{i + 1}</span><p class="h4 mt-s">{a}</p><p class="f-s ink2 mt-s">{b}</p></div>' for i, (a, b) in enumerate(steps))
    body = f'''<div class="stack-l grow">
<h2 class="h1">How a look gets from a post to the billing counter.</h2>
<div class="row c5 mt-m">{cells}</div>
<div class="row c2 mt-auto">
  <p class="ink2">The look code is the link between content and sales. Without it, views stay views. With it, every post can be traced to a store and a bill.</p>
  <p class="ink2">Store teams need one short briefing a week: this week’s looks, where they hang and how to log the code.</p>
</div></div>'''
    return slide('path', 'Idea 1 of 3 · from post to bill', body)


def cart():
    menu = ''.join(f'<li>{x}</li>' for x in MENU)
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l">
  <span class="label plan">The Westside Coffee Cart</span>
  <h2 class="h1">Coffee, and the look that goes with it.</h2>
  <p>A Westside-designed coffee cart that parks outside our stores, in malls, at colleges and in office parks. The menu is named after Westside’s own labels. Every cup sleeve carries a look from the store a few metres away: scan it, walk in, try it on.</p>
  <div class="row c2 gap-s">
    <div class="rule"><p class="label mute">On the menu</p><ul class="list mt-s f-s">{menu}</ul></div>
    <div class="rule-plan"><p class="label plan">How we own it</p><p class="f-s mt-s">The cart is the set. Clip pages, city pages, food and fashion creators and marketing pages film the cart, the cups and the queue. That distribution is planned and paid for, so the cart reaches millions, not just the people in the queue.</p></div>
  </div>
</div>
<div class="art">{art.cart([(x, '') for x in MENU])}</div>
</div>'''
    return slide('cart', 'Idea 2 of 3', body, src='Menu names use Westside labels listed on westside.com in October 2026. Illustration is a concept drawing.')


def cart_plan():
    m = MODEL['cart']
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">The Coffee Cart: where it goes and what it earns.</h2>
  <p class="ink2">{m['lede']}</p>
</div>
{table(['Line', 'Detail', 'How many', 'What it delivers'], m['rows'], cls='tbl small tight', right=(2,))}
<div class="row c3 mt-auto">
  <div class="rule">{stat(m['label'], 'impressions over the run', m['note'])}</div>
  <div class="rule">{stat(m['cups'], 'cups, each with a look on the sleeve', m['cups_note'])}</div>
  <div class="rule">{stat(m['people'], 'people on the cart team', m['people_note'])}</div>
</div></div>'''
    return slide('cart-plan', 'Idea 2 of 3 · the plan', body, src=m['src'])


def windows():
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l">
  <span class="label plan">Window Stories</span>
  <h2 class="h1">Rahul and Anjali are getting ready for dinner.</h2>
  <p>Two mannequins, one moment everyone recognises, and every piece on them is for sale inside. That is a Window Story. It turns a display into a scene people stop for, photograph and send to a friend.</p>
  <p>Next month the story changes: a first day at a new job, a cousin’s mehendi, Sunday lunch at Nani’s, a college reunion.</p>
  <div class="rule-plan mt-auto"><p class="f-s">Each story is a complete outfit for two people, with the price of each look on a card in the window and the code to pull it in store.</p></div>
</div>
<div class="art">{art.window()}</div>
</div>'''
    return slide('windows', 'Idea 3 of 3', body, src='Illustration is a concept drawing. Characters are placeholders until the story list is approved.')


def windows_scale():
    m = MODEL['windows']
    stories = ''.join(f'<tr><td class="n"><b>{c}</b></td><td>{s}</td></tr>' for c, s in m['stories'])
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l">
  <h2 class="h1">Now picture it in every Westside store, each with its own story.</h2>
  <div class="art" style="height:auto">{art.stores_grid(n=m['grid_n'], cols=25, picks=m['picks'])}</div>
  <p class="f-s mute">One square for each store. Green: the first city stories.</p>
</div>
<div class="stack-l">
  <table class="tbl small tight"><thead><tr><th>City</th><th>Story in the window</th></tr></thead><tbody>{stories}</tbody></table>
  {table(['Line', 'How many', 'What it delivers'], m['rows'], cls='tbl small tight', right=(1,))}
  <div class="row c2 mt-auto"><div class="rule">{stat(m['label'], 'impressions in twelve weeks', m['note'])}</div><div class="rule">{stat(m['people'], 'people on the windows team', m['people_note'])}</div></div>
</div></div>'''
    return slide('windows-scale', 'Idea 3 of 3 · at scale', body, src=m['src'])


def numbers():
    rows = MODEL['table']
    b = BASELINE
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">{MODEL['total_label']} impressions, line by line.</h2>
  <p class="ink2">Every line is units multiplied by an average we can defend. Low and high show the range we would plan for.</p>
</div>
<div class="row c-8-4 grow">
  {table(['Idea', 'Channel', 'Units', 'Average per unit', 'Low', 'Plan', 'High'], rows['rows'], cls='tbl small tight', right=(2, 3, 4, 5, 6), total=rows['total'], col_cls={5: 'plan-col'})}
  <div class="stack-l">
    <p class="label mute">Against the last twelve months</p>
    <div class="bars">
      <div class="bar"><span class="f-s">{b['label']}</span><span class="t"><i style="width:{b['pct_base']}%"></i></span><span class="v">{b['value']}</span></div>
      <div class="bar us"><span class="f-s">This plan</span><span class="t"><i style="width:{b['pct_plan']}%"></i></span><span class="v">{MODEL['total_label']}</span></div>
    </div>
    <p class="f-s ink2">{b['compare_line']}</p>
  </div>
</div></div>'''
    return slide('numbers', 'The numbers', body, src=MODEL['src'])


def measure():
    rows = [['Footfall per store', 'People counters at the entrance', 'Test stores against matched stores that did not get the programme'],
            ['Codes redeemed', 'Look codes, cup codes and window codes logged at the till', 'Per store, per idea, per week'],
            ['Member bills', 'WestStyleClub number on the bill', 'Bills and bill value from members who saw a code'],
            ['Impressions and views', 'Platform reports from every page and creator', 'Against the plan, line by line, every week']]
    body = f'''<div class="row c-5-7 grow">
<div class="stack-l">
  <h2 class="h1">Measured at the billing counter.</h2>
  <p class="lede">Impressions tell us the work was seen. Footfall and bills tell us it worked. We report both, every week, store by store.</p>
  <p class="ink2">We agree the method, the comparison stores and the success threshold in writing before anything goes live.</p>
</div>
<div class="stack-l">{table(['What we count', 'How', 'Read against'], rows, cls='tbl')}
<p class="f-s mute">A new store has no history, so it is read against the opening weeks of comparable recent Westside openings. An existing store is read against its own last twelve weeks and against matched stores.</p></div>
</div>'''
    return slide('measure', 'Measurement', body)


def test():
    body = '''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">Start with one test. If the numbers don’t move, you lose nothing.</h2>
  <p class="ink2">Pick one of the two. Both run for eight weeks and both are read on footfall per store.</p>
</div>
<div class="row c2 grow">
  <div class="rule-plan stack">
    <p class="label plan">Option A · recommended</p><h3 class="h2">One store launch</h3>
    <p>All three ideas around one new Westside store: styled looks from its rails before it opens, the Coffee Cart outside on opening weekend, and a Window Story in its window.</p>
    <p class="f-s ink2">Read against the opening weeks of comparable recent openings.</p>
  </div>
  <div class="rule stack">
    <p class="label mute">Option B</p><h3 class="h2">One festive drop</h3>
    <p>The wedding season in one city: styled looks for every function, the cart at the city’s busiest Westside, and wedding Window Stories across that city’s stores.</p>
    <p class="f-s ink2">Read against each store’s previous twelve weeks and matched stores elsewhere.</p>
  </div>
</div>
<div class="row c3">
  <div class="rule"><p class="h4">Our fee</p><p class="f-s mt-s">Paid only if footfall beats the comparison by the threshold we agree up front.</p></div>
  <div class="rule"><p class="h4">Production and media</p><p class="f-s mt-s">At cost, approved before we spend, within a cap agreed before launch.</p></div>
  <div class="rule"><p class="h4">What we need from Westside</p><p class="f-s mt-s">The store, its stock, store-team time, people-counter and bill data, and approvals within 48 hours.</p></div>
</div></div>'''
    return slide('test', 'The test', body)


def ninety():
    rows = [['Weeks 1–2', 'Agree the test store, comparison stores and threshold. Set up codes at the till. Brief store teams.'],
            ['Weeks 3–4', 'Cast stylists and creators. Build the cart. Write and design the first Window Stories. Book clip and city pages.'],
            ['Weeks 5–12', 'The test runs: weekly looks, cart days, window changes. A one-page report every Monday.'],
            ['Week 13', 'Readout with Trent: footfall, codes, bills and impressions against plan. Go or no-go for the next cities.']]
    body = f'''<div class="row c-4-8 grow">
<div class="stack-l"><h2 class="h1">The first ninety days.</h2><p class="lede">Four weeks to set up, eight weeks live, one honest readout.</p></div>
<div class="stack-l" style="justify-content:center">{table(['When', 'What happens'], rows, cls='tbl')}</div>
</div>'''
    return slide('ninety', 'Timeline', body)


def references():
    vids = VIDEOS
    n = len(vids) or 3
    cols = 3 if n >= 3 else n
    cards = ''.join(video_card(v.get('item'), v['caption'], v.get('meta', '')) for v in vids) if vids else ''.join(video_card(None, 'Reference video') for _ in range(3))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 center">
  <h2 class="h1">References.</h2>
  <p class="ink2">The tone and finish we are aiming for. Press play; each opens full screen with sound.</p>
</div>
<div class="vgrid grow" style="--vc:{cols}">{cards}</div>
</div>'''
    return slide('references', 'References', body)


def mask360():
    pillars = [('Social', 'The Styled by Westside series, creators and page distribution.'),
               ('Content', 'Stylists, shoots and edits, made in Westside stores.'),
               ('Experiential', 'The Coffee Cart and Window Stories, built and run.'),
               ('Measurement', 'The per-store scorecard, built with Westside’s data team.')]
    p = ''.join(f'<div class="rule"><p class="h2">{a}</p><p class="f-s ink2 mt-s">{b}</p></div>' for a, b in pillars)
    body = f'''<div class="stack-l grow">
<div class="row c-5-7 center">
  <div class="stack"><span class="label mute">Who we are</span><div style="width:46%"><svg viewBox="0 0 1632 473" aria-label="m360" style="fill:currentColor"><use href="#logo-m"/></svg></div></div>
  <p class="lede">Mask360 is a creative and content agency in India and the UAE. For nine years we have made content, events and campaigns for luxury and lifestyle brands, from Mumbai, Delhi, Bengaluru, Dubai and Abu Dhabi.</p>
</div>
<div class="row c4 mt-m">{p}</div>
<div class="rule mt-auto"><p class="label mute">Brands we have worked with</p><p class="mt-s">Dior · FCUK Beauty · L’Oréal · Dyson · Anantara · Rustomjee · Chandak Group · Zorae UAE · Ferrari · Rolls-Royce · Swisse UAE · Atlantis The Royal · St. Regis</p></div>
</div>'''
    return slide('mask360', 'Mask360', body)


def next_steps():
    body = '''<div class="row c-6-6 grow">
<div class="stack-l" style="justify-content:center">
  <h2 class="h-display">Choose the first store.</h2>
  <p class="lede">One working session with your marketing, retail operations and analytics leads. We bring the store shortlist, the comparison method and a draft threshold. You get a fixed scope, timeline and terms within 72 hours.</p>
</div>
<div class="stack-l" style="justify-content:center">
  <ol class="list f-l"><li>Pick the test: a store launch or a festive drop.</li><li>Share people-counter and bill data for the test and comparison stores.</li><li>Agree the threshold and the cap.</li><li>We start building the cart and casting stylists the same week.</li></ol>
  <div class="rule mt-m"><p class="h3">Kaavish · Mask360</p><p class="ink2">mask360.agency</p></div>
</div></div>'''
    return slide('next', 'Next steps', body, dark=True)


def slides():
    return [cover(), promise(), today(), last12(), voice(), competition(), plan(), styling(), styling_plan(), look_path(),
            cart(), cart_plan(), windows(), windows_scale(), numbers(), measure(), test(), ninety(), references(), mask360(), next_steps()]
