"""Builds the Zara-app deck: screens from content dicts + wf.json details, assets inlined, two outputs."""
import re, base64, json, html, pathlib, sys
V = pathlib.Path(__file__).resolve().parent
A = V / 'assets' if (V / 'assets').exists() else V.parent / 'assets'
sys.path.insert(0, str(V))
from ips import IPS
E = html.escape
WF = json.loads((V / 'wf.json').read_text())
FINAL = WF['final']
DET = {ip['name']: ip for ip in FINAL['ips']}
SHEETS = {s['name']: s for s in json.loads((V / 'ipsheets.json').read_text())} if (V / 'ipsheets.json').exists() else {}
TGT = json.loads((V / 'target.json').read_text()) if (V / 'target.json').exists() else {}

def path_of(n): return re.search(r' d="([^"]+)"', (A / f'{n}.svg').read_text()).group(1)
def img(n): return 'data:image/webp;base64,' + base64.b64encode((A / f'{n}.webp').read_bytes()).decode()
def font(n): return 'data:font/woff2;base64,' + base64.b64encode((V / 'fonts' / f'{n}.woff2').read_bytes()).decode()

W = '<span class="mk w"><svg viewBox="0 0 1506 1194" aria-hidden="true"><use href="#logo-w"/></svg></span>'
M = '<span class="mk m"><svg viewBox="0 0 1632 473" aria-hidden="true"><use href="#logo-m"/></svg></span>'
PIN = '<svg><use href="#i-pin"/></svg>'
CHAPS = [('brief', 'The brief'), ('today', 'Westside today'), ('idea', 'The idea'), ('ips', 'The IPs'), ('store', 'The store'), ('pilot', 'The pilot'), ('scale', 'Scale'), ('m360', 'Mask360'), ('ask', 'The ask')]
screens, templates = [], []

def scr(id, chap, title, body, cls='', big=False, extra=''):
    screens.append(f'<section class="scr {cls}" id="{id}" data-chap="{chap}" data-title="{E(title)}"{" data-logo=big" if big else ""}{extra}>\n{body}\n</section>')

def tpl(id, inner): templates.append(f'<template id="{id}">{inner}</template>')

def det(id, label='Details +'): return f'<button class="det" type="button" data-sheet="{id}">{label}</button>'

def src_links(urls):
    out = []
    for u in urls:
        u = (u.strip().split() or [''])[0]
        if u.startswith('http'):
            host = re.sub(r'^https?://(www\.)?', '', u).split('/')[0]
            out.append(f'<a href="{E(u)}" target="_blank" rel="noreferrer">{E(host)}</a>')
    return ' · '.join(out)

# ---------------------------------------------------------------- 1 COVER
scr('cover', 'brief', 'Seen at Westside', f'''<canvas class="fill" data-fab="slate" data-seed="7" data-anim></canvas>
<div class="cap-b"><div><span class="kick">A proposal from Mask360 · October 2026</span><h1 class="hl xl">Seen at Westside</h1><p class="sub">Every look has an address.</p></div>
<div style="display:grid;gap:14px;justify-items:end"><span class="mk" style="height:22px"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></span>{det('sh-cover')}</div></div>''', 'tone-d', big=True)
tpl('sh-cover', '''<h3>Seen at Westside</h3><p class="lead">A content-IP system for Westside, from Mask360. Eight properties, one house look and one measure: footfall per store. It starts with one opening (or one store, for a festive drop) for eight weeks.</p><ul><li>Scroll or swipe from screen to screen, or use the arrow keys. DETAILS + opens the detail and sources on any screen.</li><li>The pilot comes pre-filled with what we recommend. ADD TO PILOT adds or removes a property, the PILOT counter at the top keeps the total, and THE ASK shows the result.</li><li>All visuals are mock-ups: rendered fabrics, interface frames and one concept render of a store front. Names, numbers and stores inside them are illustrative.</li></ul>''')

# ---------------------------------------------------------------- 2 BRIEF
scr('brief', 'brief', 'Built like Zara. Counted at the till.', f'''<div class="inner"><div class="stmt"><div class="body">
<span class="kick mute">The brief</span>
<p class="q">Built like Zara.<br>Counted at the <u>till</u>.</p>
<p class="promise">On WhatsApp we promised: "We'd take it one step further, from the post to the billing counter. Content and experiential that pull people into stores, measured on footfall per store. Give us one store launch or one festive drop as a test. If the numbers don't move, you lose nothing." This is how.</p>
</div>
<nav class="toc" aria-label="Contents">
<a href="#today"><span>01</span>Westside today</a><a href="#idea"><span>02</span>The idea: a style account</a><a href="#ips"><span>03</span>The IPs</a><a href="#track"><span>04</span>The store</a>
<a href="#pilot"><span>05</span>The pilot</a><a href="#scale"><span>06</span>Scale</a><a href="#m360"><span>07</span>Mask360</a><a href="#ask"><span>08</span>The ask</a>
</nav></div></div>''')

# ---------------------------------------------------------------- 3 TODAY (six tiles)
tiles = [('311', 'Stores · 30 Sep 2026'), ('~94%', 'Of sales in store'), ('11.85M', 'Active members'), ('25,000', 'Wesness community'), ('3,500+', 'Women at the Mumbai Wesness run'), ('400–500', 'New designs a week')]
def sep(n): return re.sub(r'([,–~+])', r'<span class="sep">\1</span>', n)
cards = ''.join(f'<button class="card" type="button" data-sheet="sh-today"><div class="im paper"><span class="tile-n">{sep(n)}</span></div><div class="tx"><b>{E(l)}</b><span>Details +</span></div></button>' for n, l in tiles)
TN = max(len(n) for n, l in tiles)
scr('today', 'today', '311 stores. About 94% in store.', f'''<div class="inner"><div class="plp">
<div class="head-row"><div><span class="kick mute">Westside today · Oct 2025–Oct 2026</span><h2 class="hl s">311 stores. About 94% in store.</h2></div>{det('sh-today')}</div>
<div class="grid g3 tiles" style="--n:{TN}">{cards}</div></div></div>''')
tpl('sh-today', '''<h3>Westside today</h3><p class="lead">A store business run on a member database, growing by opening doors.</p><ul>
<li><b>311 stores</b> at 30 Sep 2026: 278 at Dec 2025, 300 at Mar 2026. Openings are lumpy: 22 net in Q4 FY26 (23 opened), 1 net in Q1 FY27, 10 net in Q2 FY27. AGM guidance is about 50 a year.</li>
<li><b>About 94% of sales are in store.</b> Online is about 6% of Westside revenue, despite 25–38% growth.</li>
<li><b>11.85M active WestStyleClub members</b> carry over 90% of revenue (FY26 MD&amp;A).</li>
<li><b>Wesness:</b> a women's run community of about 25,000 in four cities; 3,500+ women at the Mumbai run on 8 Feb 2026. Several runs start at a Westside store.</li>
<li><b>YNG:</b> a 4,000-member community, as reported in Trent's Q4 FY26 investor presentation, with 6M views, 50,000+ engagements and 12,000+ shares.</li>
<li><b>400–500 designs a week</b> from an AI design suite, with 30-day lead times targeted (Bloomberg, Jul 2026). The same report quoted up to 100 openings a year; Trent said the next day that these remarks were not guidance.</li>
<li><b>Like-for-like growth</b> in Trent's fashion portfolio has been low single digits or negative for five quarters. Growth comes from new stores.</li></ul>
<p class="src"><a href="https://www.icicidirect.com/research/equity/blog/trent-ltd-reported-its-business-update-for-q2fy27" target="_blank" rel="noreferrer">Q2 FY27 update</a> · <a href="https://www.indiainfoline.com/company/trent-ltd/management-discussions" target="_blank" rel="noreferrer">FY26 MD&amp;A</a> · <a href="https://www.bseindia.com/xml-data/corpfiling/AttachHis/e08ff77d-7f68-46d2-acc6-ed26ee5c4974.pdf" target="_blank" rel="noreferrer">Q4 FY26 deck</a> · <a href="https://www.bseindia.com/xml-data/corpfiling/AttachHis/f98f2ffa-597c-49f2-a9e7-835cfe0dc5a7.pdf" target="_blank" rel="noreferrer">Wesness release</a> · <a href="https://www.business-standard.com/companies/news/tata-s-fashion-brand-westside-plans-biggest-push-yet-with-100-annual-stores-126072000142_1.html" target="_blank" rel="noreferrer">Bloomberg via Business Standard</a></p>''')

# ---------------------------------------------------------------- 4 LOG
scr('log', 'today', 'Thirteen moments', f'''<div class="inner"><div class="plp">
<div class="head-row"><div><span class="kick mute">Westside today · the last twelve months</span><h2 class="hl s">Thirteen moments, mapped</h2></div><div class="railctl" data-rail="logRail"><span class="lbl mute">Tap a moment</span><button type="button" data-dir="-1" aria-label="Previous moments">‹</button><span class="rc" aria-live="polite"></span><button type="button" data-dir="1" aria-label="Next moments">›</button></div></div>
<div class="hrail" id="logRail" aria-label="Westside activity, October 2025 to October 2026"></div></div></div>''')

# ---------------------------------------------------------------- 5 INDIA
it = [('77%', 'Of retail discovery is social'), ('71%', 'Buy within days of creator content'), ('~80%', 'Of Indian fashion is bought offline'), ('46%', 'Of footfall arrives 5–8 PM')]
cards = ''.join(f'<button class="card" type="button" data-sheet="sh-india"><div class="im paper"><span class="tile-n">{sep(n)}</span></div><div class="tx"><b>{E(l)}</b><span>Details +</span></div></button>' for n, l in it)
IN = max(len(n) for n, l in it)
scr('india', 'today', 'Discovery on the phone. The bill in the store.', f'''<div class="inner"><div class="plp">
<div class="head-row"><div><span class="kick mute">The Indian shopper</span><h2 class="hl s">Discovery on the phone. The bill in the store.</h2></div>{det('sh-india')}</div>
<div class="grid g4 tiles one" style="--n:{IN}">{cards}</div></div></div>''')
tpl('sh-india', '''<h3>The Indian shopper</h3><ul><li><b>77%</b> of retail discovery is social; Meta platforms drive 96% of it (Meta + RAI whitepaper, Feb 2026, published by Meta).</li><li><b>71%</b> buy within a couple of days of seeing creator content (same study).</li><li><b>~80%</b> of Indian fashion is still bought offline; e-commerce penetration is about 19% (Redseer FY25).</li><li><b>46%</b> of a fashion store's daily footfall arrives 5–8 PM; mall weekends run about 40% above weekdays (Enalytix FY26).</li><li>Stores where staff engage shoppers within two minutes see longer dwell and lower bounce (Enalytix).</li><li>CAIT estimated about <b>46 lakh weddings</b> between 1 Nov and 14 Dec 2025.</li></ul><p class="src"><a href="https://about.fb.com/news/2026/02/ai-fuels-indias-omnichannel-shopping-surge-meta-retailers-association-of-india/" target="_blank" rel="noreferrer">Meta + RAI</a> · <a href="https://apparelresources.com/business-news/retail/indias-fashion-retail-landscape-shifts-beyond-metros-says-report/" target="_blank" rel="noreferrer">Enalytix</a> · <a href="https://investor.meesho.com/investor-web/_next/docs/ipo/industry-report-e-com.pdf" target="_blank" rel="noreferrer">Redseer</a> · <a href="https://cait.in/wedding-season-2025-to-generate-%E2%82%B96-5-lakh-crore-business-from-46-lakh-weddings-across-india-cait-delhi-alone-to-witness-%E2%82%B91-8-lakh-crore-trade-from-4-8-lakh-weddings-indian/" target="_blank" rel="noreferrer">CAIT</a></p>''')

# ---------------------------------------------------------------- 6 GAP
frames = ['rani', 'bone', 'indigo', 'khaki', 'slate', 'ivory', 'moss', 'sand', 'kohl']
fr = ''.join(f'<div><canvas data-fab="{f}" data-seed="{80+i}"></canvas><span class="loc" style="left:8px;bottom:8px;top:auto">{PIN}—</span></div>' for i, f in enumerate(frames))
scr('gap', 'today', 'Bigger than Zara. Not yet busier.', f'''<div class="pdp">
<div class="pdp-vis"><div class="wingrid">{fr}</div></div>
<div class="pdp-info"><span class="kick mute">The gap</span>
<p class="pline">Bigger than Zara. Not yet busier.</p>
<div style="display:flex;align-items:flex-end;gap:18px"><span class="n" style="font-size:clamp(72px,9vw,150px);line-height:.85">311</span><span style="display:grid;gap:4px;padding-bottom:10px"><span class="n" style="font-size:34px;line-height:1">22</span><span class="lbl mute">Zara India stores</span></span></div>
<p class="pwhy">Westside has 311 stores to Zara India's 22, and on our estimate sells more in total. Each Zara store sells several times more. In the posts we could find, Westside's content seldom ends at a named store, so most frames carry no address.</p>
{det('sh-gap')}</div></div>''')
tpl('sh-gap', '''<h3>The gap</h3><ul><li>Scale: 311 stores against Zara India's 22 (FY26). Zara India FY26 revenue fell about 1% to ₹2,749 crore and profit fell about 32%.</li><li>Westside revenue is not disclosed. Our estimate is about ₹5,000 crore, derived from about ₹300 crore online at about 6% of sales. Per store, Zara sells several times more: a rough calculation, labelled as one.</li></ul><h4>The gap map</h4><ul><li><b>Openings open quietly:</b> about 40 in Oct 2025–Mar 2026, with little launch coverage in trade press. <a href="#ip-firstlook">First Look</a>, read on day-30 footfall against comparable openings.</li><li><b>Views, not visits:</b> the owned platforms report views and turnout, not store visits. <a href="#ip-regulars">The Regulars</a> and the scorecard, read on member-attributed bills.</li><li><b>No weekly reason to come in:</b> 400–500 designs a week, but no day people know to come in. <a href="#ip-window">The Window</a>, read on Friday-to-Sunday footfall and holds collected.</li><li><b>Festive lives on edit pages:</b> we found no Westside film for Diwali 2025 or the wedding season in trade press. <a href="#ip-dehleez">Dehleez</a> and <a href="#ip-fivefunctions">Five Functions</a>, read on festive footfall against controls.</li></ul><ul><li>Trent holds 20% of Zara India (Inditex about 80%). We learn from Zara; we never knock it, and Zara is never named in consumer copy.</li></ul><p class="src"><a href="https://www.outlookbusiness.com/news/zaras-india-fy26-profit-falls-32-to-204-cr-revenue-slips" target="_blank" rel="noreferrer">Zara India FY26</a> · <a href="https://www.outlookbusiness.com/news/zaras-india-fy26-profit-falls-32-to-204-cr-revenue-slips" target="_blank" rel="noreferrer">22 stores and Trent's 20% stake, FY26</a></p>''')

# ---------------------------------------------------------------- 7 IDEA
scr('idea', 'idea', 'Every look has an address.', f'''<img class="fill bw" src="{{{{IMG:store_1600}}}}" alt="Concept render of a Westside store front, in black and white" style="object-position:50% 70%;transform:scale(1.16);transform-origin:50% 0">
<div class="cap-t"><span class="dateline">Seen at Westside, D.N. Nagar, Mumbai</span><h2 class="hl xl" style="margin-top:18px;max-width:15ch;font-size:clamp(40px,6vw,88px)">Every look has an address.</h2></div>
<div class="cap-b"><p class="sub idea-sub" style="margin:0">One magazine with 311 addresses. Every asset is numbered, ends in one store action, and is counted at the till.</p>{det('sh-idea')}</div>''', 'tone-d scrim-t scrim-b2')
tpl('sh-idea', '''<h3>Every look has an address</h3><p class="lead">Seen at Westside is one magazine with 311 addresses: Westside's own Indian calendar, made with Zara's restraint. It is never "Zara at Westside prices".</p><h4>Three rules for every asset</h4><ul><li><b>A number and a dateline:</b> WINDOW No. 047 · SEEN AT WESTSIDE, &lt;STORE&gt;, &lt;CITY&gt;.</li><li><b>One store action:</b> BOOK (a stylist, a room, a portrait), HOLD (your size until Sunday close) or RSVP (a guest list), sent to that store's WhatsApp with a property code.</li><li><b>Counted at the till:</b> the WestStyleClub ID and the code are captured together, linking post, booking, visit and bill for each store.</li></ul><h4>Channels</h4><ul><li>@@@H@@, a dedicated style account built the way @TargetStyle is: the magazine, where the eight properties run as series. @westsidestores keeps offers, launches and store news. Then the app and site, WestStyleClub WhatsApp, 311 windows and thresholds, and each store's Google Business Profile. Creators post on their own handles, tagged to a named store.</li></ul>''')

# ---------------------------------------------------------------- 7b THE ACCOUNT (Westside's @TargetStyle)
ACC = json.loads((V / 'account.json').read_text()) if (V / 'account.json').exists() else {}
H = ACC.get('handle', 'seenatwestside').lstrip('@')
HL_FAB = {'Your store': 'ivory', 'The Window': 'bone', 'Trial Room': 'curtain', 'Seen In': 'sand', 'Mausam': 'slate', 'First Look': 'kohl', 'Functions': 'shaadi', 'Dehleez': 'haldi', 'Regulars': 'moss'}
hls = ACC.get('highlights') or [{'label': k} for k in HL_FAB]
hl = ''.join(f'<span><i><canvas data-fab="{HL_FAB.get(h["label"], "slate")}" data-seed="{200+j}"></canvas></i>{E(h["label"])}</span>' for j, h in enumerate(hls))
posts = ACC.get('grid_posts') or [{'overlay': 'Window No. 047', 'fab': 'slate'}]
LT = {'ivory', 'bone', 'curtain', 'dehleez', 'khaki', 'sand'}
grid = ''.join(f'<div><canvas data-fab="{x.get("fab", "slate")}" data-seed="{220+j}"></canvas><em class="{"d" if x.get("fab") in LT else ""}">{E(x["overlay"])}</em></div>' for j, x in enumerate(posts[:9]))
bio = '<br>'.join(E(b) for b in ACC.get('bio_lines', ['Style, seen in a Westside near you']))
link = E(ACC.get('link_in_bio', 'westside.com/seen'))
prof = f"""<div class="phone acct-phone"><div class="pscr"><div class="prof">
<div class="prof-h"><span>{E(H)}</span><span style="letter-spacing:2px">···</span></div>
<div class="prof-meta"><span class="prof-av"><svg viewBox="0 0 1506 1194"><use href="#logo-w"/></svg></span><div class="prof-nums"><span><b>284</b>posts</span><span><b>8</b>series</span><span><b>311</b>stores</span></div></div>
<div class="prof-bio"><b>{E(ACC.get('display_name', 'Seen at Westside'))}</b><br>{bio}<br><span style="color:#00376b">{link}</span></div>
<div class="prof-hl">{hl}</div>
<div class="prof-grid">{grid}</div></div></div></div>"""
week = ''.join(f'<div><span>{E(d)}</span><b>{E(x)}</b><i>{E(a)}</i></div>' for d, x, a in ACC.get('week', []))
alt = ACC.get('handle_alt', '')
scr('account', 'idea', f'@{H}', f"""<div class="pdp">
<div class="pdp-vis" style="display:grid;place-items:center"><div class="wired-stage acct-stage" data-max="1.45">{prof}</div><span class="lbl mute acct-note">Mock-up · the account in year one</span></div>
<div class="pdp-info"><span class="kick mute">The idea · the style account</span>
<p class="pname">@{E(H)}</p>
<p class="pline">Style is the IP. The account is the magazine.</p>
<p class="pwhy">{E(ACC.get('pitch_line', ''))}</p>
<div class="chips"><div><span>Handle</span><b>@{E(H)}</b></div><div><span>Series</span><b>Eight, one highlight each</b></div><div><span>@westsidestores</span><b>Keeps offers, launches and store news</b></div></div>
<div class="week7" aria-label="The week on the account">{week}</div>
<dl class="hook"><dt>Launch</dt><dd>{E(ACC.get('launch', ''))}</dd></dl>
<p class="from">Borrowed from <b>Target Style</b>: a style handle beside @Target since at least 2014 (2.2M followers to @Target's 4.4M in May 2020), relaunched on 13 Sept 2025 at the Target Style Tailgate during New York Fashion Week, as a hosted live premiere with five set formats. {E(ACC.get('first_in_india', '').split('. ')[0])}.</p>
<div class="acts"><div class="row2"><button class="btn" type="button" data-add="@{E(H)}" data-meta="Pilot 01 · the style account">Add to pilot</button><button class="btn ghost" type="button" data-sheet="sh-account">Details +</button></div></div>
</div></div>""")
def li(xs): return ''.join(f'<li>{E(x)}</li>' for x in xs)
borrow = ''.join(f'<li><b>{E(b["property"])}:</b> {E(b["from_target_style"])}' + (f' <a class="mute" href="{E(b["url"])}" target="_blank" rel="noreferrer">Source</a>' if b.get('url') else '') + '</li>' for b in ACC.get('property_borrowings', []))
comps = ''.join(f'<li><b>{E(a)}:</b> {E(b)}. <a class="mute" href="{E(u)}" target="_blank" rel="noreferrer">Source</a></li>' for a, b, u in ACC.get('comparables', []))
weekli = ''.join(f'<li><b>{E(d)}:</b> {E(x)}, {E(a)}.</li>' for d, x, a in ACC.get('week_detail', []))
tpl('sh-account', f"""<h3>@{E(H)}: the style account</h3><p class="lead">{E(ACC.get('target_style_summary', ''))}</p>
<h4>What lives where</h4><p class="lead">{E(ACC.get('split_with_brand_account', ''))}</p>
<h4>Launch</h4><p class="lead">{E(ACC.get('launch', ''))}</p>
<h4>The week</h4><ul>{weekli}</ul>
<h4>Voice</h4><ul>{li(ACC.get('voice_rules', []))}</ul>
<h4>Borrowed from Target Style</h4><ul>{borrow}</ul>
<h4>Other retailers with a style account</h4><ul>{comps}<li>We found none that reports a store result for its style account. Every @{E(H)} post carries a store code, so its store actions are counted from the first post; footfall is read per store.</li></ul>
<h4>India</h4><p class="lead">{E(ACC.get('first_in_india', ''))}</p>
<h4>Measured on</h4><ul>{li(ACC.get('kpis', []))}</ul>
<p class="src">Handle availability to be checked on Instagram, YouTube and Threads before launch{f'; alternative: @{E(alt)}' if alt else ''}. Store names in the mock-ups are illustrative.</p>""")

# ---------------------------------------------------------------- 8 REFERENCE
ref_z = [
 ('Zara SRPLS', 'Numbered collections, CLLCTN 02 (2019) to CLLCTN 16 (Apr 2026), under one credited creative director.', 'https://us.fashionnetwork.com/news/Zara-expands-its-srpls-range-for-next-summer,1822357.html'),
 ('Zara Studio', 'A stable core crew and a palette declared each season (SS26: powder blue, sage, blush).', 'https://fashionunited.uk/press/fashion/zara-spring-summer-2026-studio-collection/2026032086985'),
 ('The Fold-er', 'Bylined columns inside the app, with a shop link under every image (12 Jun 2026).', 'https://fashionunited.uk/news/retail/zara-creates-its-casita-and-launches-the-fold-er-an-editorial-section-with-influencers-and-trendsetters/2026061288595'),
 ('Zara Nanjing', 'A bookable fit-check and content studio inside the flagship (Mar 2025).', 'https://us.fashionnetwork.com/news/Zara-opens-flagship-store-in-china-s-nanjing-with-cafe-and-content-creation-studio,1714347.html'),
 ('Premieres', 'One room, by appointment, before the wide release: Re{form} by John Galliano, Marais, 1–6 Oct 2026.', 'https://wwd.com/fashion-news/designer-luxury/john-galliano-zara-collab-paris-popup-1239290160/'),
]
ref_t = [(r['name'], r['text'], r['url']) for r in ACC.get('target_style_rows', [])] or [(r['name'], r['text'], r['url']) for r in TGT.get('reference', [])]
def refl(rows): return '<ul class="refl">' + ''.join(f'<li><span>{E(a)}</span><span>{E(b)} <a class="mute" href="{E(u)}" target="_blank" rel="noreferrer">Source</a></span></li>' for a, b, u in rows) + '</ul>'
cols = f'<div><span class="lbl">Zara · few, named, numbered</span>{refl(ref_z)}</div>'
if ref_t: cols += f'<div><span class="lbl">Target Style · style as its own account</span>{refl(ref_t)}</div>'
scr('reference', 'idea', 'Few. Named. Numbered. Dated.', f'''<div class="inner" style="display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;gap:20px">
<div class="head-row"><div><span class="kick mute">Reference · what we borrow</span><h2 class="hl s">Few. Named. Numbered. Dated.</h2><p class="sub">Zara makes IP that feels like a collection. Target Style gives style its own account. We add a store at the end of every post.</p></div>{det('sh-reference')}</div>
<div class="refs" style="margin-top:8px">{cols}</div><div></div>
<p class="lbl mute">Text only by design: no Zara or Target logos, photos or screenshots anywhere in this proposal.</p></div>''')
tpl('sh-reference', '''<h3>What we borrow, and what we leave</h3><h4>From Zara</h4><ul><li><b>Few and numbered:</b> SRPLS counts its collections; Studio keeps one credited crew and declares a palette each season. Westside gets Mausam No. 01–04 and Window No. 001 onward.</li><li><b>Editorial on owned surfaces:</b> The Fold-er puts bylined columns in the app with a shop link under every image. Westside gets Trial Room columns with a store under every look.</li><li><b>The room before the release:</b> Re{form} and the Nanjing studio make the store the venue. Westside gets First Look and the bookable trial room.</li></ul><h4>From Target Style</h4><ul><li><b>Style as its own account:</b> @TargetStyle has run beside @Target since at least 2014, about half its size in 2020 (2.2M to 4.4M). Westside gets @@@H@@ beside @westsidestores.</li><li><b>A dated premiere:</b> Target relaunched @TargetStyle on 13 Sept 2025 at the Target Style Tailgate during New York Fashion Week, a hosted live premiere inside one named season, with five set formats.</li><li><b>Tag to be featured:</b> Target.com invites shoppers to tag @TargetStyle to be featured. Westside gets Seen In and The Regulars, with a store in every tag.</li></ul><h4>From Target, beyond the account</h4><ul><li><b>The store as the feed:</b> SoHo's 'The Drop' rotates a style collection monthly on the first floor. Westside's Window does it weekly, in 311 bays.</li><li><b>Tiered creators:</b> Club Target for fans, Ambassadors for professionals. The Regulars ladder does the same, scored on bills.</li><li><b>An owned object:</b> the red bag carries a season. Dehleez makes the threshold Westside's object.</li></ul><h4>What we leave</h4><ul><li>@TargetStyle has always ended online; we found no store action on it. Zara makes the store its medium, but its social never asks you to book, hold or RSVP at a named store. Target runs a long list of collaborations. Westside's edge is 311 doors and 11.85M members, so every format ends at a door.</li></ul>''')

# ---------------------------------------------------------------- IP visuals
def vis(k, small=False):
    if k == 'mausam':
        board = '' if small else '<div class="lookboard">' + ''.join(f'<figure><img src="{{{{IMG:{im}}}}}" alt="" style="object-position:{op}"><i style="background:{c}"></i><figcaption>{n}</figcaption></figure>' for im, op, c, n in [('mannequin_l', '40% 35%', 'var(--slate)', 'Look 1 · slate'), ('mannequin_r', '50% 30%', 'var(--moss)', 'Look 2 · moss'), ('racks', '35% 45%', 'var(--sand)', 'Look 3 · wet sand')]) + '<span class="c lb-note">Look board, mock-up</span></div>'
        return f'''<canvas class="fill" data-fab="slate" data-seed="71"></canvas>{board}<div class="ov"><div><span class="c">Mausam No. 02 / Baarish</span><div class="deva" style="font-size:22px;margin-top:6px">मौसम</div></div><div class="chips-sw"><i style="background:var(--slate)"></i><i style="background:var(--moss)"></i><i style="background:var(--sand)"></i><span class="c" style="margin-left:6px">Slate · Moss · Wet sand</span></div></div>'''
    if k == 'window':
        cells = [('img', 'mannequin_l'), ('fab', 'slate'), ('fab', 'moss'), ('fab', 'sand'), ('fab', 'linen'), ('fab', 'khaki'), ('fab', 'indigo'), ('fab', 'ivory'), ('fab', 'bone')]
        h = ''
        for i, (t, v) in enumerate(cells):
            m = f'<img src="{{{{IMG:{v}}}}}" alt="">' if t == 'img' else f'<canvas data-fab="{v}" data-seed="{90+i}"></canvas>'
            h += f'<div>{m}<span class="n">No. {i+1:03d}</span></div>'
        return f'<div class="wingrid">{h}</div>'
    if k == 'trialroom':
        return '''<canvas class="fill" data-fab="curtain" data-seed="5"></canvas><figure class="inset"><img src="{{IMG:mannequin_l}}" alt="A look on the trial-room rail, mock-up"><figcaption>Look 2 of 3 · in your size</figcaption></figure><span class="stencil">Trial Room 4 · Westside D.N. Nagar</span>'''
    if k == 'seenin':
        sheet = ''.join(f'<figure><img class="bw" src="{{{{IMG:{im}}}}}" alt="" style="object-position:{op}"><figcaption>{cap}</figcaption></figure>' for im, op, cap in [('mannequin_l', '35% 30%', 'Frame 01 · Salt Lake'), ('mannequin_r', '55% 25%', 'Frame 02 · Salt Lake'), ('racks', '30% 50%', 'Frame 03 · Salt Lake'), ('store_900', '70% 60%', 'Frame 04 · Salt Lake')])
        return f'''<img class="fill bw" src="{{{{IMG:store_900}}}}" alt="" style="object-position:50% 80%"><div class="seam"><div class="contact">{sheet}</div></div><div class="ov d" style="left:18%;right:18%;top:12%"><span class="c">Seen In Salt Lake · 17 Oct · contact sheet, mock-up</span><span class="c">Pavement studio · daylight</span></div>'''
    if k == 'firstlook':
        return '''<img class="fill" src="{{IMG:racks}}" alt="" style="filter:brightness(.34) saturate(.6) blur(4px);transform:scale(1.06)"><div class="ov" style="justify-content:center;align-items:center;text-align:center"><span class="c">First Look</span><span class="n" style="font-size:clamp(56px,7vw,120px);line-height:1;margin:10px 0">No. 330</span><span class="c">Opens Friday</span></div>'''
    if k == 'dehleez':
        return (V / 'dehleez_door.svg.txt').read_text() + '''<div class="ov d"><div><span class="c">Dehleez Edition 01</span><div class="deva" style="font-size:22px;margin-top:6px">दहलीज़</div></div><span class="c">Artist announced Aug 2027</span></div>'''
    if k == 'fivefunctions':
        bands = [('haldi', 'Haldi', ''), ('mehendi', 'Mehendi', ''), ('midnight', 'Sangeet', ''), ('shaadi', 'Wedding', ''), ('ivory', 'Reception', 'lt')]
        return '<div class="five">' + ''.join(f'<div class="{c}"><canvas data-fab="{f}" data-seed="{60+i}"></canvas><span>{n}</span></div>' for i, (f, n, c) in enumerate(bands)) + '</div>'
    if k == 'regulars':
        return '''<canvas class="fill" data-fab="kohl" data-seed="11"></canvas><div class="ladder"><div><b>Front Row</b><span>Culture</span></div><div><b>Window</b><span>Creator</span></div><div><b>Rail</b><span>Runner</span></div><div><b>Floor</b><span>Stylist</span></div></div>'''

# ---------------------------------------------------------------- 9 IPS LISTING
cards = ''
for i, ip in enumerate(IPS):
    cards += f'''<a class="card" href="#ip-{ip['key']}"><div class="im">{vis(ip['key'], True)}</div><div class="tx"><b>{E(ip['name'])}{(' <span class="deva" style="color:inherit;text-transform:none">'+ip['deva']+'</span>') if ip['deva'] else ''}</b><span>{E(ip['price'])}</span></div></a>'''
scr('ips', 'ips', 'Eight properties. One calendar.', f'''<div class="inner"><div class="plp">
<div class="head-row"><div><span class="kick mute">The IPs</span><h2 class="hl s">Eight properties. One calendar.</h2></div>
<div class="density" data-density role="group" aria-label="Grid density"><span class="mute">View</span><button type="button" data-cols="2" aria-pressed="false">2</button><button type="button" data-cols="4" aria-pressed="true">4</button>{det('sh-ips')}</div></div>
<div class="grid g4" id="ipGrid">{cards}</div></div></div>''')
tpl('sh-ips', '''<h3>Eight properties, six roles</h3><ul><li><b>Spine:</b> Mausam, four numbered issues a year.</li><li><b>Weekly:</b> The Window (Friday) and The Trial Room (Wednesday).</li><li><b>Weekly:</b> Seen In, a different priority city each Monday. <b>Rolling:</b> First Look, at every opening.</li><li><b>Dated:</b> Dehleez (Navratri to Bhai Dooj) and Five Functions (Nov to Feb). <b>Engine:</b> The Regulars.</li><li><b>Mechanics, not properties:</b> Style Call (a 15-minute WhatsApp video call that converts to a held room), HOLD, RSVP and the 72-hour Burst (local Regulars, city pages, PR and geo-paid media within 5–8 km of the named store).</li></ul><h4>Weekly rhythm on @@@H@@</h4><ul><li>Mon: Seen In (a different city each week) · Tue: The Regulars · Wed: The Trial Room · Thu: the season slot, plus the members' Window preview at 9 PM · Fri: The Window · Sat: in-store Stories (not live) · Sun: Stories only.</li></ul>''')

# ---------------------------------------------------------------- 10 GLASS CALENDAR
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def mo(w): return months[(w*12)//52] if w == 0 or (w*12)//52 != ((w-1)*12)//52 else ''
BARS = {('m', 15): ('#b8a98a', 'No. 01 Garmi · pilot city', 'dk', 7), ('m', 26): ('var(--slate)', 'No. 02 Baarish', '', 4), ('m', 40): ('#c8611a', 'No. 03 Tyohaar', '', 5), ('m', 46): ('#9e1b26', 'No. 04 Shaadi', '', 4),
        ('d', 1): ('#6a0f16', 'Five Functions Ed. 01 · drop option', '', 9), ('d', 40): ('#23201c', 'Dehleez Ed. 01', 'ol', 5), ('d', 46): ('#6a0f16', 'Five Functions Ed. 02', '', 5)}
FL = (2, 5, 7, 10, 14, 19, 23, 27, 31, 36, 44, 49)
def cell(kind, w):
    if kind in ('m', 'd'):
        b = BARS.get((kind, w))
        return f'<div><span class="b {b[2]}" style="background:{b[0]};right:-{b[3]*100}%">{b[1]}</span></div>' if b else '<div></div>'
    if kind == 'w': return '<div><span class="tick"></span></div>' if w >= 26 else ('<div><span class="tick p"></span></div>' if 4 <= w < 26 else '<div></div>')
    if kind == 's': return '<div><span class="dot"></span></div>' if w % 4 == 2 else '<div></div>'
    if kind == 'f': return '<div><span class="tick" style="background:var(--m360)"></span></div>' if w in FL else '<div></div>'
LANES = [('m', 'Mausam'), ('w', 'The Window'), ('d', 'Dated'), ('s', 'Seen In'), ('f', 'First Look')]
def glass_html(weeks, cls):
    h = '<div class="mo"></div>' + ''.join(f'<div class="mo">{mo(w)}</div>' for w in weeks)
    for k, name in LANES: h += f'<div class="lane">{name}</div>' + ''.join(cell(k, w) for w in weeks)
    return f'<div class="glass {cls}">{h}</div>'
full = glass_html(range(52), 'full')
quarters = ''.join(f'<div class="q"><span class="lbl mute">Q{q+1} 2027</span>' + glass_html(range(q*13, q*13+13), 'quarter') + '</div>' for q in range(4))
scr('glass', 'ips', 'One glass. One message.', f"""<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:22px">
<div class="head-row"><div><span class="kick mute">The IPs · 52-week glass calendar, 2027</span><h2 class="hl s">One glass. One message.</h2><p class="sub">Each store has one window bay, and it carries one programme a week. Short ticks: the pilot store from week 5, then its city cluster with Garmi after the go/no-go. The Window goes national in July.</p></div>{det('sh-glass')}</div>
<div class="glass-wrap" style="align-self:center">{full}<div class="glass-q">{quarters}</div></div></div>""")
tpl('sh-glass', """<h3>The glass calendar</h3><ul><li>Each store has one Window bay, and it changes every Friday.</li><li>Short ticks: until the go/no-go only the pilot store carries The Window, from week 5. After it, the pilot city cluster carries the Garmi cover. The Window goes national in July with Mausam No. 02 Baarish, in two waves a week apart, so each install carries its own control group.</li><li>In a Mausam launch week, that week's Window is the issue cover. Tyohaar's cover is the threshold: in Dehleez weeks the bay carries the Dehleez capsule look and the numbering continues.</li><li>In an opening store, the First Look maker's object holds the bay for weeks 1 to 4; Window No. 001 opens in week 5. Opening ticks are illustrative.</li><li>Five Functions Edition 01 runs only if the festive-drop option is chosen.</li></ul><p class="src">2027 festival dates follow the published calendar and are fixed with Trent before installs are booked.</p>""")

# ---------------------------------------------------------------- 11-18 PDPs
for i, ip in enumerate(IPS):
    d = DET.get(ip['jname'], {})
    chips = ''.join(f'<div><span>{E(a)}</span><b>{E(b)}</b></div>' for a, b in ip['chips'])
    eps = ''.join(f'<li><span>{j+1:02d}</span>{E(e)}</li>' for j, e in enumerate(ip['eps']))
    frm = ip['frm'].replace('<!--TARGET_REGULARS-->', TGT.get('regulars_from', ''))
    name = E(ip['name']) + (f' <span class="deva">{ip["deva"]}</span>' if ip['deva'] else '')
    scr(f'ip-{ip["key"]}', 'ips', ip['name'], f"""<div class="pdp">
<div class="pdp-vis">{vis(ip['key'])}</div>
<div class="pdp-info"><span class="kick mute">Property {i+1:02d} / 08 · {E(ip['role'])}</span>
<p class="pname">{name}</p>
<p class="pline">{E(ip['head'])}</p>
<p class="pwhy">{E(ip['line'])}</p>
<p class="price">{E(ip['kpi'])}</p>
<div class="chips">{chips}</div>
<ol class="eps">{eps}</ol>
<dl class="hook"><dt>Store hook</dt><dd>{E(ip['hook'])}</dd></dl>
<p class="from">{frm}</p>
<div class="acts"><div class="row2"><button class="btn" type="button" data-add="{E(ip['name'])}" data-meta="{E(ip['phase'])}">Add to pilot</button><button class="btn ghost" type="button" data-sheet="sh-ip-{ip['key']}">Details +</button></div></div>
</div></div>""")
    sd = SHEETS.get(ip['jname'])
    def lines(x): return '<ul>' + ''.join(f'<li>{E(str(l).lstrip("- ").strip())}</li>' for l in (x if isinstance(x, list) else str(x).split('\n')) if str(l).strip()) + '</ul>'
    def para(x): return f'<p class="lead">{E(x)}</p>' if x else ''
    if sd:
        srcl = ' · '.join(f'<a href="{E(s["url"].split()[0])}" target="_blank" rel="noreferrer">{E(s["title"])}</a>' for s in sd.get('precedent_sources', []) if s.get('url', '').startswith('http'))
        tpl(f'sh-ip-{ip["key"]}', f"""<h3>{E(ip['name'])}</h3><p class="lead">{E(sd['line'])}</p>
<h4>Role</h4>{para(sd['role'])}<h4>Format</h4>{lines(sd['format'])}<h4>Cadence</h4>{lines(sd['cadence'])}<h4>Channels</h4>{para(sd['channels'])}<h4>Cast</h4>{para(sd['cast'])}
<h4>Store hook</h4>{para(sd['store_hook'])}<h4>KPI</h4>{para(sd['kpi'])}<h4>Art direction</h4>{lines(sd['art_direction'])}
<h4>Precedent</h4>{para(sd['precedent'])}<p class="src">{srcl}</p>""")
    else:
        d = DET.get(ip['jname'], {})
        tpl(f'sh-ip-{ip["key"]}', f"""<h3>{E(ip['name'])}</h3><p class="lead">{E(d.get('line', ip['line']))}</p><h4>Role</h4>{para(d.get('role'))}<h4>Channels</h4>{para(d.get('channels'))}<h4>Precedent</h4>{para(d.get('precedent'))}""")

# ---------------------------------------------------------------- 19 ART DIRECTION
rules = '''<div class="rules4">
<div class="rule-c"><div class="post-mini"><canvas data-fab="ivory" data-seed="301"></canvas><span class="n">No. 047</span><span class="dl">Seen at Westside, Salt Lake, Kolkata</span></div><span class="cap">Number and dateline</span></div>
<div class="rule-c"><span class="n" style="font-size:clamp(48px,5vw,84px)">No. 047</span><span class="cap">Serif numerals only</span></div>
<div class="rule-c"><span class="deva" style="font-size:clamp(40px,4.4vw,72px)">मौसम</span><span class="cap">A second mark Zara can't own</span></div>
<div class="rule-c"><div style="display:grid;gap:6px;width:70%"><span style="height:34px;background:var(--slate)"></span><span style="height:34px;background:var(--moss)"></span><span style="height:34px;background:var(--sand)"></span></div><span class="cap">Three named colours: slate, moss, wet sand</span></div></div>'''
scr('art', 'ips', 'Expensive by restraint.', f'''<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:20px">
<div class="head-row"><div><span class="kick mute">The IPs · art direction</span><h2 class="hl s">Expensive by restraint.</h2><p class="sub">Four of the fourteen rules that make Westside look expensive without spending like it.</p></div>{det('sh-art', 'All 14 rules +')}</div>
<div style="align-self:center">{rules}</div></div>''')
tpl('sh-art', '<h3>The art-direction rules</h3><ul>' + ''.join(f'<li>{E(x.replace("Umashan Naidoo is house creative director.", "We propose Westside\'s chief creative (Umashan Naidoo) as house creative director."))}</li>' for x in FINAL['art_direction_bible']) + '</ul><h4>Naming and voice</h4><ul>' + ''.join(f'<li>{E(x.replace("Zara is named only in the pitch, on its reference screen.", "Zara is named only inside this pitch, never in anything Westside publishes."))}</li>' for x in FINAL['naming_and_voice']) + '</ul>')

# ---------------------------------------------------------------- 20 TRACKER
steps = [('See', 'A Window, a Trial Room episode or a Seen In wall, each naming one store.', 'Specificity: a named place turns "nice" into a plan.'),
         ('Tap', 'BOOK, HOLD or RSVP on that store\'s WhatsApp with a property code.', 'Commitment: a dated slot, not a like.'),
         ('Visit', 'Your size is held, or your stylist is waiting.', 'Endowment: what is already yours is hard to give up.'),
         ('Bill', 'The WestStyleClub ID and the code are captured at the counter.', 'The loop closes per store.'),
         ('Return', 'Collect a portrait or an alteration, or use a 30-day Style Call card.', 'A second visit is built in.')]
tr = ''.join(f'<div class="trk"><span class="s"><i></i>{j+1:02d}</span><span class="big">{a}</span><p>{E(b)}</p><span class="why">{E(c)}</span></div>' for j, (a, b, c) in enumerate(steps))
scr('track', 'store', 'From the post to the billing counter.', f'''<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:20px">
<div class="head-row"><div><span class="kick mute">The store</span><h2 class="hl s">From the post to the billing counter.</h2><p class="sub">Five steps, each one counted per store.</p></div></div>
<div style="align-self:center"><div class="track">{tr}</div></div></div>''')

# ---------------------------------------------------------------- 21 IN THE WILD
wild = (V / 'wild3.html').read_text()
scr('wild', 'store', 'In the wild', f'''<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px">
<div class="head-row"><div><span class="kick mute">The store · in the wild</span><h2 class="hl s">Every frame carries an address.</h2></div><div class="railctl" data-rail="wildRail"><span class="lbl mute">Mock-ups</span><button type="button" data-dir="-1" aria-label="Previous mock-ups">‹</button><span class="rc" aria-live="polite"></span><button type="button" data-dir="1" aria-label="Next mock-ups">›</button></div></div>
<div class="hrail wild" id="wildRail" aria-label="Concept touchpoints">{wild}</div></div>''')

# ---------------------------------------------------------------- 22 WIRED
wired = (V / 'wired3.html').read_text()
scr('wired', 'store', "Wired before it's posted.", f'''<div class="pdp">
<div class="pdp-vis" style="display:grid;place-items:center"><div class="wired-stage">{wired}</div></div>
<div class="pdp-info"><span class="kick mute">The store · operations</span>
<p class="pline">Wired before it's posted.</p>
<p class="pwhy">No post goes out until the store can answer it.</p>
<ol class="eps"><li><span>01</span>One WhatsApp Business route per store, with property codes</li><li><span>02</span>Live per-store stock before anyone is sent</li><li><span>03</span>A reply-time agreement for holds and bookings</li><li><span>04</span>A trained stylist in each pilot store</li><li><span>05</span>Releases, consent and ASCI disclosure built in</li></ol>
{det('sh-wired')}</div></div>''')
tpl('sh-wired', '''<h3>Wired before it's posted</h3><ul><li>One WhatsApp Business provider, with routing to each store and property codes (HOLD 047, BOOK 012, CARD).</li><li>Live per-store stock before anyone is sent, plus an agreed reply time for holds and bookings in each store.</li><li>One trained stylist in each pilot store; alteration capacity checked for Five Functions.</li><li>Signed releases, paid fees and guardian consent; ASCI disclosure; WestStyleClub consent that meets the DPDP Rules (full compliance due 13 May 2027).</li><li>Mall approvals for floor graphics and any early access; the mall fire officer's sign-off for any real flame (Dehleez uses LED diyas by default).</li><li>A cultural review of every festive and wedding asset before release, with Hindi, Urdu and regional reviewers.</li></ul>''')

# ---------------------------------------------------------------- 23 PILOT
scr('pilot', 'pilot', 'One opening. Eight weeks.', f"""<div class="pdp">
<div class="pdp-vis">
<div class="fill bay-frame" data-show="launch"><canvas class="fill" data-fab="kohl" data-seed="166"></canvas><div class="bay"><div class="bay-in"><canvas data-fab="bone" data-seed="167"></canvas><img class="bay-look" src="{{{{IMG:mannequin_r}}}}" alt="One look in the window bay, concept frame"><span class="n bay-no">No. 001</span></div><span class="bay-cap">Window No. 001 · week 5 of the pilot · concept frame</span></div></div>
<div class="five" data-show="drop" hidden>""" + ''.join(f'<div class="{c}"><canvas data-fab="{f}" data-seed="{160+i}"></canvas><span>{n}</span></div>' for i, (f, n, c) in enumerate([('haldi', 'Haldi', ''), ('mehendi', 'Mehendi', ''), ('midnight', 'Sangeet', ''), ('shaadi', 'Wedding', ''), ('ivory', 'Reception', 'lt')])) + f"""</div>
</div>
<div class="pdp-info"><span class="kick mute">The pilot · Pilot 01</span>
<p class="pname" data-show="launch">One opening. Eight weeks.</p><p class="pname" data-show="drop" hidden>One store. Eight weeks.</p>
<p class="pline" data-show="launch">First Look · your first Q4 FY27 opening</p><p class="pline" data-show="drop" hidden>Five Functions, Edition 01</p>
<p class="price">You lose nothing if the numbers don't move</p>
<p class="from" style="margin-top:-6px">No agency fee unless verified footfall beats the comparison by the threshold we agree up front. Production and media at cost, approved upfront.</p>
<div class="sizes" data-toggle role="group" aria-label="Choose the test"><button type="button" data-val="launch" aria-pressed="true"><b>Store launch</b><small>Recommended · Jan–Mar 2027</small></button><button type="button" data-val="drop" aria-pressed="false"><b>Festive drop</b><small>Wedding dates · Jan–Feb 2027</small></button></div>
<dl class="hook" data-show="launch"><dt>Store</dt><dd>Westside's first Q4 FY27 opening, in a city chosen with Trent, plus three cluster stores for The Trial Room. Counters in before it opens.</dd><dt>Runs</dt><dd>@@@H@@ premieres on preview night. First Look holds the bay for weeks 1–4, then Window No. 001. The Trial Room with 4 stylists. Seen In on the opening Saturday and in week 5. About 15–30 catchment Regulars.</dd><dt>Read</dt><dd>Weeks 1–8 entries per sq ft against matched Q4 FY26 openings; the cluster stores like-for-like against matched controls. Readout at opening + 10 weeks.</dd></dl>
<dl class="hook" data-show="drop" hidden><dt>Store</dt><dd>One existing high-footfall store with spare alteration capacity (illustrative: Westside Sky Vista, D.N. Nagar, Mumbai).</dd><dt>Runs</dt><dd>@@@H@@ premieres with Five Functions Episode 01. Bring the Card sessions, five episodes and Trial Room bookings.</dd><dt>Read</dt><dd>Difference-in-differences on a 12-week baseline against 3–5 matched stores, with the January sale matched in the controls.</dd></dl>
<div class="acts"><div class="row2"><button class="btn" type="button" data-add="Pilot 01" data-meta="One opening · eight weeks">Add to pilot</button><button class="btn ghost" type="button" data-sheet="sh-pilot">Details +</button></div>
<div class="row2"><button class="btn ghost" type="button" data-sheet="sh-returns">Returns +</button><button class="btn ghost" type="button" data-sheet="sh-need">What we need +</button></div></div>
</div></div>""")
tpl('sh-pilot', """<h3>Pilot 01: one opening, eight weeks</h3><ul><li><b>Scope:</b> one launch store (the style account, First Look, The Window, The Trial Room, Seen In and The Regulars) plus three cluster stores (The Trial Room only; they are the like-for-like read), each against matched control stores. Four store stylists and about 15 to 30 catchment Regulars. One store can detect a lift of about 10% or more; the cluster stores about 8–15% each, lower pooled.</li><li><b>Recommended:</b> Westside's first Q4 FY27 opening (Jan–Mar 2027). @@@H@@ premieres on preview night, the evening before the store opens. The First Look maker's object holds the bay for weeks 1–4; Window No. 001 opens in week 5.</li><li><b>Festive-drop alternative:</b> Five Functions Edition 01 with Bring the Card in one existing store, on the Jan–Feb 2027 wedding dates, where Westside has bill history to compare against. @@@H@@ premieres with Episode 01. The weeks overlap the end-of-season sale, so the sale weeks are matched in the control stores.</li><li><b>Before January:</b> reserve @@@H@@ (fallback @westsidestyle) on Instagram, YouTube and Threads this week; export Diwali 2026 daily bills per store, and entries where counters exist, as the baseline; optionally run a December soft test of HOLD in one to three stores.</li><li><b>Prep, Nov–Dec 2026:</b> WhatsApp routing, the house trial-room spec, the crew contracted, stylists trained, counters in the pilot store and its controls.</li><li><b>Diwali 2026 (8 Nov):</b> nothing attempted beyond keeping the baseline.</li><li><b>Readout:</b> opening plus 10 weeks, then a go/no-go meeting with Trent. National rollout only if the agreed threshold is met.</li><li><b>Next, after the go/no-go:</b> Mausam No. 01 Garmi in the pilot city cluster on the first Friday after it (April–May 2027), then The Window national from July 2027 with Mausam No. 02 Baarish.</li><li><b>Phase 2, between the go/no-go and July (about April–June 2027):</b> three existing stores outside the pilot city with The Window and The Trial Room, read like-for-like against matched controls (about 5–7% detectable pooled), so the result also speaks to Westside's mature stores.</li></ul>""")
tpl('sh-returns', """<h3>Returns</h3><p class="lead"><b>If the numbers don't move, you lose nothing.</b> In contract terms: no agency fee unless verified footfall beats the comparison by the threshold we agree up front. Production and media are approved upfront and billed at cost, within a cap agreed before launch.</p><h4>The trigger, by option</h4><ul><li><b>Store launch:</b> weeks 1–8 entries per sq ft at the pilot store against the mean of matched Q4 FY26 openings in the same weeks. The threshold is set once Westside shares that cohort's spread. Where those openings had no counters, bills per sq ft per week is the curve.</li><li><b>Festive drop:</b> difference-in-differences against a 12-week baseline and 3–5 matched stores; about 10% is detectable for one store.</li></ul><h4>Who measures</h4><ul><li>Westside's own people counters and POS. We register the method, the control stores and the threshold in writing before launch.</li><li>"Inconclusive" is defined up front (a stock-out, a mall closure): extend the window or call it.</li></ul><h4>What Westside puts in</h4><ul><li>Stock, store-team time, a store manager who owns the pilot, WhatsApp routing and the data.</li></ul><h4>What a lift is worth</h4><ul><li>A worked example with labelled assumptions: a store with 700 entries a day and a 10% lift gains about 70 entries a day. At an assumed 20% conversion that is about 14 extra bills a day, or about 100 a week, at Westside's average bill (to be shared).</li></ul><h4>Alternatives</h4><ul><li>A reduced base fee plus a bonus at agreed lift levels, or a contingent pilot with first rights to the roll-out.</li></ul>""")
tpl('sh-need', """<h3>What we need from Westside</h3><ul><li>The pilot store, chosen with Trent, and confirmed stock.</li><li>Per-store footfall (people counters, installed before opening where needed), POS data and bills linked to WestStyleClub IDs, and agreed control stores.</li><li>The opening curves of comparable Q4 FY26 openings: entries, or bills per sq ft where there were no counters.</li><li>One WhatsApp Business route per store, with property codes.</li><li>A store-team session, a store manager who owns the pilot, and approvals within 48 hours in the live weeks.</li><li>Diwali 2026 daily bills per store, and entries where counters exist, kept as a baseline.</li></ul>""")

# ---------------------------------------------------------------- 24 SCORECARD
rows = [('Footfall per store (entries / trading day)', '—', '—', '—'), ('BOOK · HOLD · RSVP per store', '—', '—', '—'), ('Member-attributed bills', '—', '—', '—'), ('Average bill, booked vs walk-in', '—', '—', '—')]
body = ''.join(f'<tr><td>{E(a)}</td><td>{b}</td><td>{c}</td><td>{d}</td><td><span class="ci"></span></td></tr>' for a, b, c, d in rows)
scr('score', 'pilot', 'Counted at the door.', f"""<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:22px">
<div class="head-row"><div><span class="kick mute">The pilot · scorecard</span><h2 class="hl s">Counted at the door.</h2><p class="sub">Footfall per store first, then bookings, bills and bill size, read against stores that did not get it. Every cell stays empty until the pilot fills it.</p></div>{det('sh-score')}</div>
<div style="align-self:center;overflow-x:auto"><table class="summary"><thead><tr><th>Measure</th><th>Test</th><th>Control</th><th>Difference</th><th>Confidence</th></tr></thead><tbody>{body}</tbody>
<tfoot><tr><td>Threshold</td><td colspan="4" style="text-align:right">Agreed before launch, from the comparison set</td></tr></tfoot></table></div></div>""")
tpl('sh-score', """<h3>How we count</h3><ul><li><b>KPI spine:</b> footfall per store, then BOOK, HOLD and RSVP per store, then member-attributed bills, then average bill against walk-ins.</li><li><b>Counters:</b> aggregate people counters that store no identities, calibrated by a manual count, with the same hardware in test and control stores.</li></ul><h4>Read A · store launch (recommended)</h4><ul><li>A new store has no baseline, so it is read against the opening curves of matched Q4 FY26 openings: pilot weeks 1–8 entries (or bills) per sq ft minus the mean of the matched openings in the same weeks.</li><li>The threshold is set once Westside shares that cohort's spread. The three cluster stores are read like-for-like against matched controls.</li></ul><h4>Read B · festive drop (existing store)</h4><ul><li>(Test live − test baseline) − (control live − control baseline) = extra entries per trading day, on a 12-week baseline with 3–5 matched control stores.</li><li>One store can detect a lift of about 10% or more over 4–6 weeks, so we pool where we can and define "inconclusive" before launch.</li></ul><h4>Illustrative example for Read B, not Westside data</h4><ul><li>Pilot store: 640 → 760 entries a day. Matched stores: 610 → 640.</li><li>Expected without the pilot: about 670. Lift: about +90 a day, roughly +13%.</li></ul><h4>Why we expect it to move</h4><ul><li>In a randomised field experiment with a US apparel retailer, 84% of the sales lift from online ads landed in physical stores (Lewis &amp; Reiley).</li><li>Google reports that 26% of Tanishq's store sales had a Google touchpoint (platform-reported).</li></ul><p class="src"><a href="https://www.informs.org/News-Room/INFORMS-Releases/News-Releases/Over-80-of-online-ad-effect-is-on-offline-sales" target="_blank" rel="noreferrer">Lewis &amp; Reiley via INFORMS</a> · <a href="https://business.google.com/in/think/consumer-insights/omnichannel-retail-strategy-indian-shoppers/" target="_blank" rel="noreferrer">Think with Google (Tanishq)</a></p>""")

# ---------------------------------------------------------------- 25 SCALE
covs = [('bone', 'No. 01', 'Garmi', 'Apr–May 2027', ['#e6dfd1', '#a89a74', '#2c3a68'], 'd'), ('slate', 'No. 02', 'Baarish', 'Jul 2027', ['#5d6872', '#5f6b48', '#c9b79a'], ''), ('door', 'No. 03', 'Tyohaar', 'Oct 2027', ['#e3901c', '#23201c', '#f6efe0'], 'd'), ('midnight', 'No. 04', 'Shaadi', 'Nov 2027', ['#5f6b2e', '#1b2340', '#efe9dc'], '')]
cv = ''.join(f'<div class="cover-c">' + ((V / 'dehleez_door.svg.txt').read_text().replace('xMidYMid slice', 'xMaxYMax meet') if f == 'door' else f'<canvas data-fab="{f}" data-seed="{170+i}"></canvas>') + f'<div class="ov {d}"><div><span class="c">Mausam</span><div class="n">{n}</div><span class="c">{t}</span></div><div style="display:grid;gap:6px"><div class="chips-sw">' + ''.join(f'<i style="background:{c}"></i>' for c in cs) + f'</div><span class="c">{m}</span></div></div></div>' for i, (f, n, t, m, cs, d) in enumerate(covs))
scr('scale', 'scale', 'From one door to 311.', f'''<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr) auto;gap:18px">
<div class="head-row"><div><span class="kick mute">Scale</span><h2 class="hl s">From one door to 311.</h2></div>{det('sh-scale')}</div>
<div style="min-height:0;align-self:center"><div class="covers">{cv}</div></div>
<div class="head-row" style="border-top:1px solid var(--ink);padding-top:10px"><span class="lbl">Stores live</span><span class="n" id="storeCount" style="font-size:clamp(34px,4vw,64px);line-height:1">1</span></div></div>''')
tpl('sh-scale', '''<h3>From one door to 311</h3><ul><li><b>Opening + 10 weeks:</b> the pilot readout and a go/no-go with Trent. Nothing goes national before it.</li><li><b>April–May 2027:</b> Mausam No. 01 Garmi, in the pilot city cluster, on the first Friday after the go/no-go. Phase 2 reads three existing stores.</li><li><b>Jul 2027:</b> after the go/no-go, The Window goes national in two waves a week apart, with Mausam No. 02 Baarish, one of the year's two films.</li><li><b>Aug 2027:</b> the Dehleez artist is announced. <b>Diwali 2027:</b> Dehleez Edition 01: one artist designs every Westside threshold (311 today), and families book portraits in 50 stores.</li><li><b>Nov 2027:</b> Five Functions Edition 02 goes nationwide as Mausam No. 04.</li><li>The Regulars grow from one city cluster to 3–5 per store. First Look runs full tier for new cities and kit tier for infill stores.</li></ul>''')

# ---------------------------------------------------------------- 26 PRODUCTION
prod = [('Weekly', 'One Window still and loop · one Trial Room episode · Seen In, a city a Monday (the pilot city, then six priority cities)'), ('Fortnightly', 'Trial Room columns, growing as stylists join'), ('Monthly', 'One Regulars brief'), ('Four times a year', 'Mausam stills'), ('Per opening', 'A First Look kit'), ('Yearly', 'Two films: the Baarish film and the Five Functions series'), ('Annual, from Diwali 2027', 'Dehleez: one threshold design for every store, portrait sessions in 50'), ('Not in year one', 'Scripted series, label films, routine livestreams, timed races')]
pr = ''.join(f'<tr><td>{a}</td><td style="text-align:left">{E(b)}</td></tr>' for a, b in prod)
scr('made', 'scale', 'Made every week. Kept light.', f'''<div class="inner" style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:22px">
<div class="head-row"><div><span class="kick mute">Scale · composition and care</span><h2 class="hl s">Made every week. Kept light.</h2><p class="sub">Capped at what one agency and Westside's teams can make every week. The money goes on the crew and the edit, never on props.</p></div></div>
<div style="align-self:center"><table class="summary"><thead><tr><th>Cadence</th><th style="text-align:left">Output</th></tr></thead><tbody>{pr}</tbody></table><p class="lbl mute" style="margin-top:12px">Westside VM ships the weekly Window kit from a reference store. The label's merchandiser confirms the look and size depth every Monday.</p></div></div>''')

# ---------------------------------------------------------------- 27 M360
scr('m360', 'm360', 'Mask360', f'''<div class="inner" style="display:grid;grid-template-rows:auto 1fr auto;gap:24px">
<span class="kick">Mask360 · one team, post to counter</span>
<div style="align-self:center;display:grid;gap:26px"><span class="mk" style="height:clamp(80px,13vw,190px)"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></span>
<div class="track" style="border-top-color:currentColor"><div class="trk"><span class="big">Social</span><p style="color:inherit">The @{H} style account, the series and The Regulars.</p></div><div class="trk"><span class="big">Content</span><p style="color:inherit">The house crew, The Window, The Trial Room and Mausam.</p></div><div class="trk"><span class="big">Experiential</span><p style="color:inherit">First Look, Dehleez thresholds and Bring the Card.</p></div><div class="trk"><span class="big">Behaviour</span><p style="color:inherit">Commitment, endowment, social proof and return trips, built into each format.</p></div><div class="trk"><span class="big">Measure</span><p style="color:inherit">The per-store scorecard, built with Westside's data team.</p></div></div></div>
<div style="display:grid;gap:10px"><p class="lbl">India and the UAE · nine years · Mumbai, Delhi, Bengaluru, Dubai, Abu Dhabi</p><p class="lbl">Dior · FCUK Beauty · L'Oréal · Dyson · AJIO Luxe · Anantara · Rustomjee · Chandak Group · Zorae UAE · Ferrari · Rolls-Royce · Swisse UAE · Atlantis The Royal · St. Regis</p><p class="lbl" style="opacity:.75">Westside creative owns the brand and the Mausam look. Westside's social agency runs @westsidestores. Mask360 produces the series on @{H}, the store activation and the measurement.</p><p class="lbl" style="opacity:.75">Pilot team: one lead, a producer and crew, a store-operations lead in the pilot city, and a measurement lead working with Westside's analytics team.</p></div></div>''', 'm360')

# ---------------------------------------------------------------- 28 ASK
scr('ask', 'ask', 'Choose the first door.', f'''<div class="inner"><div class="checkout" style="height:100%;align-content:center">
<div><span class="kick mute">The ask · your pilot</span><h2 class="hl">Choose the first door.</h2><p class="sub">Approve one launch store and three cluster stores for eight weeks, and the data to read them.</p>
<ol class="eps" style="margin-top:22px"><li><span>01</span>Pick the test: one store launch (recommended) or one festive drop</li><li><span>02</span>Share per-store footfall, POS data and member-linked bills; agree control stores</li><li><span>03</span>Set up one WhatsApp route per store, with property codes</li><li><span>04</span>Export Diwali 2026 daily bills per store, and entries where counters exist</li></ol></div>
<div><span class="kick">Pilot [<span class="pc">0</span>]</span><ul class="bag-list" id="bagList"></ul><p class="bag-empty" id="bagEmpty">Nothing in the pilot. Use ADD TO PILOT on any property, or <button type="button" class="linkish" data-reset-bag>restore the recommended pilot</button>.</p>
<div style="display:grid;gap:8px;margin-top:16px"><div class="copy"><span>Kaavish · Mask360</span><span class="mute">mask360.agency</span></div><button class="btn" type="button" data-sheet="sh-contact">Confirm pilot</button></div></div>
</div></div>''')
tpl('sh-contact', '''<h3>Confirm pilot</h3><p class="lead">Checkout is a 45-minute working session with your marketing, retail operations and analytics leads. We bring the store shortlist, the control-store method and a draft threshold, and return a fixed scope, timeline and terms within 72 hours.</p><div style="display:grid;gap:10px;margin-top:8px"><div class="copy"><span>mask360.agency</span><button type="button" data-copy="https://mask360.agency">Copy</button></div><div class="copy"><span>mask360.work · credentials</span><button type="button" data-copy="https://mask360.work">Copy</button></div><a class="btn" href="https://mask360.agency" target="_blank" rel="noreferrer">Contact Mask360</a></div>''')

# ---------------------------------------------------------------- 29 CLOSE
scr('close', 'ask', 'Seen at Westside', f'''<canvas class="fill" data-fab="kohl" data-seed="21"></canvas>
<div style="position:absolute;inset:0;display:grid;place-items:center;text-align:center;color:#fff"><div style="display:grid;gap:18px;justify-items:center"><span class="mk" style="height:clamp(70px,10vw,140px)"><svg viewBox="0 0 1506 1194" aria-label="Westside"><use href="#logo-w"/></svg></span><span class="dateline">Seen at Westside. 311 addresses.</span><span class="mk" style="height:18px;margin-top:10px"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></span></div></div>
<div class="cap-b" style="justify-content:center;text-align:center"><p class="lbl" style="opacity:.7;max-width:70ch">Mask360 · October 2026 · All visuals are mock-ups; store names are illustrative until confirmed. UI grammar inspired by fashion retail apps; not affiliated with Zara/Inditex or Target. {det('sh-sources', 'Sources +')}</p></div>''', 'tone-d')
srcs = [('Westside + Trent', [('Trent Q4 FY26 investor presentation', 'https://www.bseindia.com/xml-data/corpfiling/AttachHis/e08ff77d-7f68-46d2-acc6-ed26ee5c4974.pdf'), ('Wesness Fun Run release, 10 Feb 2026', 'https://www.bseindia.com/xml-data/corpfiling/AttachHis/f98f2ffa-597c-49f2-a9e7-835cfe0dc5a7.pdf'), ('Q2 FY27 update (311 stores)', 'https://www.icicidirect.com/research/equity/blog/trent-ltd-reported-its-business-update-for-q2fy27'), ('FY26 MD&A (WestStyleClub)', 'https://www.indiainfoline.com/company/trent-ltd/management-discussions'), ('Bloomberg via Business Standard, Jul 2026', 'https://www.business-standard.com/companies/news/tata-s-fashion-brand-westside-plans-biggest-push-yet-with-100-annual-stores-126072000142_1.html'), ('FRONT ROW launch', 'https://fashionvaluechain.com/westside-unveils-front-row-fashion-platform/'), ("Trent's 243rd Westside store release", 'https://docs.trent-tata.com/Press_Release_on_launch_of_243rd_Westside_Store.pdf')]),
        ('Zara', [('Zara SRPLS CLLCTN 16', 'https://us.fashionnetwork.com/news/Zara-expands-its-srpls-range-for-next-summer,1822357.html'), ('Zara Studio SS26', 'https://fashionunited.uk/press/fashion/zara-spring-summer-2026-studio-collection/2026032086985'), ('Zara The Fold-er', 'https://fashionunited.uk/news/retail/zara-creates-its-casita-and-launches-the-fold-er-an-editorial-section-with-influencers-and-trendsetters/2026061288595'), ('Re{form} by John Galliano', 'https://wwd.com/fashion-news/designer-luxury/john-galliano-zara-collab-paris-popup-1239290160/'), ('Zara Nanjing fit-check studio', 'https://us.fashionnetwork.com/news/Zara-opens-flagship-store-in-china-s-nanjing-with-cafe-and-content-creation-studio,1714347.html'), ("Zara × Jayesh Sachdev 'Reverie'", 'https://in.fashionnetwork.com/news/Zara-collaborates-with-jayesh-sachdev-for-diwali-capsule-collection,1671932.html'), ("Zara 'Le Dîner'", 'https://highxtar.com/en/zara-turns-a-dinner-into-cinema-with-le-diner-its-new-christmas-film/'), ('Inditex FY2025 results', 'https://www.inditex.com/itxcomweb/gp/en/press/news-detail/b870d5ec-6b7e-491d-b38e-340cd69036df/fy2025-results'), ('Zara India FY26', 'https://www.outlookbusiness.com/news/zaras-india-fy26-profit-falls-32-to-204-cr-revenue-slips'), ('The Impression: Zara Studio Spring 2025 campaign', 'https://theimpression.com/zara-studio-spring-2025-ad-campaign-review/')]),
        ('Shopper + measurement', [('Meta + RAI whitepaper, Feb 2026', 'https://about.fb.com/news/2026/02/ai-fuels-indias-omnichannel-shopping-surge-meta-retailers-association-of-india/'), ('Enalytix fashion footfall, FY26', 'https://apparelresources.com/business-news/retail/indias-fashion-retail-landscape-shifts-beyond-metros-says-report/'), ('Lewis & Reiley via INFORMS', 'https://www.informs.org/News-Room/INFORMS-Releases/News-Releases/Over-80-of-online-ad-effect-is-on-offline-sales'), ('Think with Google: omnichannel strategy and Indian shoppers (Tanishq)', 'https://business.google.com/in/think/consumer-insights/omnichannel-retail-strategy-indian-shoppers/'), ('CAIT: wedding season 2025 estimate', 'https://cait.in/wedding-season-2025-to-generate-%E2%82%B96-5-lakh-crore-business-from-46-lakh-weddings-across-india-cait-delhi-alone-to-witness-%E2%82%B91-8-lakh-crore-trade-from-4-8-lakh-weddings-indian/'), ('Redseer industry report (Meesho prospectus)', 'https://investor.meesho.com/investor-web/_next/docs/ipo/industry-report-e-com.pdf'), ('Kantar BrandZ India 2025', 'https://www.kantar.com/inspiration/brands/indias-top-100-most-valuable-brands-worth-524-billion'), ('Trent clarification on Westside media coverage, Jul 2026', 'https://businessupturn.com/business/trent-clarifies-recent-media-coverage-on-westside-business/')])]
for g, items in TGT.get('sources', []):
    srcs.append((g, items))
USED = ('modash', 'target-soho-spring', '2014/08/upping', 'tubefilter.com/2020/05/26', 'article/2020/05/instagram-shopping', 'retaildive.com/news/target-style-instagram', 'retailtouchpoints.com/?p=154481', 'kitty-ca', 'target.com/finds', 'zanna-roberts', 'woolrich-collab', 'hm-turns', 'ms-man-social', 'macys-steps', 'myt', 'The-Drop', 'indianjeweller', 'entrepreneur.com/article/236914')
ts = [(x['title'], x['url']) for x in ACC.get('sources', []) if any(k in x['url'] for k in USED)]
if ts: srcs.append(('Target Style and other style accounts', ts))
s = ''.join(f'<h4>{E(g)}</h4><ul>' + ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noreferrer">{E(t)}</a></li>' for t, u in items) + '</ul>' for g, items in srcs)
tpl('sh-sources', f'<h3>Sources</h3><p class="lead">Public sources to 15 Oct 2026; Westside activity covers Oct 2025–Oct 2026. Figures are as reported by the cited sources, several of them secondary coverage of primary filings. Where we say we found nothing, that is from public search to 15 Oct 2026. The full eight-gap map is in Mask360’s Westside marketing audit 2026, available on request.</p>{s}')

# ---------------------------------------------------------------- shell + assemble
tabs = ''.join(f'<a href="#{h}" data-chap="{c}">{E(n)}</a>' for c, h, n in [('brief', 'brief', 'The brief'), ('today', 'today', 'Westside today'), ('idea', 'idea', 'The idea'), ('ips', 'ips', 'The IPs'), ('store', 'track', 'The store'), ('pilot', 'pilot', 'The pilot'), ('scale', 'scale', 'Scale'), ('m360', 'm360', 'Mask360'), ('ask', 'ask', 'The ask')])
shell = (V / 'shell3.html').read_text().replace('<!--TABS-->', tabs).replace('<!--SCREENS-->', '\n'.join(screens)).replace('<!--TEMPLATES-->', '\n'.join(templates)).replace('@@H@@', H)
css = (V / 'deck3.css').read_text() + '\n' + (V / 'mock.css').read_text() + '\n' + (V / 'extra3.css').read_text()
IMGS = {}
def sub(t):
    t = re.sub(r'src="\{\{IMG:(\w+)\}\}"', lambda m: (IMGS.setdefault(m.group(1), img(m.group(1))), f'data-img="{m.group(1)}" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="')[1], t)
    t = re.sub(r'\{\{PATH:(\w+)\}\}', lambda m: path_of(m.group(1)), t)
    t = re.sub(r'\{\{IMG:(\w+)\}\}', lambda m: img(m.group(1)), t)
    t = re.sub(r'\{\{FONT:([\w-]+)\}\}', lambda m: font(m.group(1)), t)
    return t
css = sub(css); shell = sub(shell)
left = re.findall(r'\{\{[^}]+\}\}', css + shell); assert not left, left
BAN = re.findall(r'model memory|search-summary|earlier file|this pass|negative search|UNVERIFIED|brief only|folded in|Style Collective|Roshni|Start Line|The Serial|@@H@@|&lt;your store&gt;|No\. 3XX|@westside(?![a-z])', shell, re.I)
import os
if BAN and os.environ.get('STRICT'): raise SystemExit('banned: ' + ', '.join(sorted(set(BAN))))
if BAN: print('WARN banned:', sorted(set(BAN)))
js = 'var IMGS=' + json.dumps(IMGS) + ';document.querySelectorAll("img[data-img]").forEach(function(i){i.src=IMGS[i.dataset.img]});\n' + (V / 'fabric.js').read_text() + '\n' + (V / 'extras3.js').read_text() + '\n' + (V / 'deck3.js').read_text()
head = f'''<title>Seen at Westside</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Mask360's pitch to Westside, built like the Zara app: Seen at Westside, a style account built the way @TargetStyle is, eight content properties modelled on how Zara builds content IP, and a one-opening pilot measured on footfall per store.">
<style>
{css}
</style>
'''
out = (V.parent / 'dist') if (V.parent / 'dist').exists() or V.name == 'src' else (V / 'out'); out.mkdir(exist_ok=True)
(out / ('seen-at-westside.html' if out.name == 'dist' else 'deck3.html')).write_text(head + shell + '\n<script>\n' + js + '\n</script>\n')
(out / 'Westside-x-M360-Seen-at-Westside.html').write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + head + '</head>\n<body>\n' + shell + '\n<script>\n' + js + '\n</script>\n</body>\n</html>\n')
print({f.name: f.stat().st_size for f in out.iterdir() if f.suffix == '.html'}, 'screens', len(screens))
