"""Slide copy for Mask360's social media proposal to Birla Fertility & IVF. The Westside v4 deck's way of writing: a headline, a
line or two, the numbers, and a one-line source on each slide; the full sources are on the last page. Facts come from
pitches/birla-fertility/README.md, which lists every source. The look is Westside v4's, kept as it is."""
import art
from kit import slide, stat, ul, table, tile, chapter, wordmark, fab, M_MARK, LOGO, LOGO_REV, MARK, NAME

TITLE = 'Birla Fertility & IVF × Mask360'
DESCRIPTION = ('Mask360’s social media proposal to Birla Fertility &amp; IVF, October 2026: No question too quiet. The content as a '
               'mind map, the grid, a sample week, three campaigns and a sensitivity code for the new NMC rules.')

# the slides in deck order; page references on the slides are looked up here
ORDER = ['cover', 'promise', 'brief', 'ch-today', 'audit', 'rivals', 'law', 'insight', 'ch-idea', 'map', 'platforms', 'grid',
         'week', 'rule', 'ideas', 'asked', 'feed', 'half', 'goodnews', 'voices', 'ch-run', 'code', 'care', 'days', 'measure',
         'mask360', 'next', 'close', 'sources']


def pg(sid):
    return f'{ORDER.index(sid) + 1:02d}'


# full sources, shown on the last page; each slide carries a short version
SOURCES = [
    ('Social today', 'Public profiles, October 2026, approximate: @birlafertility about 35K Instagram followers; '
     '@birlafertility_armcivf about 11K; Facebook about 12K; YouTube @birlafertilityivf 470+ videos and about 10M views; '
     '@indiraivfgroup about 391K. 50+ centres: @birlafertility on Instagram.'),
    ('The numbers', 'Male factors in 40 to 50% of cases in India: Indian Society of Assisted Reproduction, via BioSpectrum India. '
     'Over 90% of people facing fertility problems feel emotionally exhausted and 29% seek timely help: Birla Fertility &amp; IVF '
     'study, released with Fertility Circle, June 2025 (MediaBrief).'),
    ('Birla Fertility &amp; IVF', '50+ centres, 120+ experts and 1,40,000+ IVF cycles: @birlafertility on Instagram. 51 clinics in 38 '
     'cities across 18 states at the Jalandhar launch, 2025 (Medtech Spectrum). ARMC IVF, May 2024, and BabyScience, August 2024 '
     '(Venture Intelligence, BioSpectrum India). “All Heart. All Science.” (Digital Health News). Fertility Circle, 1800 123 1515, '
     'in English and Hindi (MediaBrief, June 2025). YouTube @birlafertilityivf, 470+ videos.'),
    ('The category', 'Indira IVF: 165+ centres (Business Standard, July 2025), about 390K Instagram followers (public profile), '
     'Tumko Meri Kasam (ThePrint, 2025). Nova IVF Fertility creator series (Confluencr). Cloudnine Fertility, “Every Fertility Journey '
     'is Different”, World IVF Day 2026 (Business News This Week). Ferty9 #TogetherInIVF (MediaNews4U). Motherhood “I Am Very '
     'Fortunate” (Motherhood India).'),
    ('The rules', 'NMC public notice of 6 October 2026, as reported by The South First and BestMediaInfo. ASCI Consumer Complaints '
     'Council releases, October 2019 and January 2020; ASCI guidelines for health and finance influencers, 2023. ART (Regulation) '
     'Act 2021, section 32; Surrogacy (Regulation) Act 2021, section 38; PCPNDT Act, section 22; Drugs and Magic Remedies Act 1954, '
     'schedule (India Code). DPDP Rules, November 2025. Meta advertising standards on personal attributes and family planning.'),
    ('Care', 'Tele-MANAS, India’s national mental health helpline: 14416. Fertility Circle, Birla Fertility &amp; IVF’s counselling '
     'line: 1800 123 1515.'),
    ('The ideas', 'Idea names, formats, the content mix, service levels and the plan are Mask360’s proposal. The calendar assumes a '
     'start on Monday 16 November 2026.'),
]


def cover():
    body = f'''<div class="stack-l grow" style="justify-content:space-between">
{wordmark('big-wm')}
<div class="cover-foot">
  <div class="stack-l">
    <span class="label">A social media proposal from Mask360 · October 2026</span>
    <h1 class="h-display" style="max-width:11em">No question too quiet.</h1>
  </div>
  {M_MARK}
</div></div>'''
    return slide('cover', 'Proposal', body, src='For the brand team at Birla Fertility &amp; IVF · Confidential', bare=True, dark=True,
                 cls='cover scrim', cloth=('navy', 7))


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">We will make @birlafertility the account India <u>asks first</u>.</h2>
</div>
<div class="terms">
  <div><span class="no label">01</span><p class="h3">Asked sooner</p><p class="mt-s ink2">People reach a specialist before the worry grows.</p></div>
  <div><span class="no label">02</span><p class="h3">Trusted in private</p><p class="mt-s ink2">Saves, shares and DMs, the signals that come before a consult.</p></div>
  <div><span class="no label">03</span><p class="h3">Safe in every post</p><p class="mt-s ink2">Checked by your doctors and written for the new NMC rules.</p></div>
</div>'''
    return slide('promise', 'Our promise', body)


def brief():
    rows = [['Proven healthcare and fertility experience', 'Live health and wellness work, and our fertility thinking in full.', pg('mask360')],
            ['Understands the category’s sensitivity', 'A sensitivity code, the new rules, and care for every DM.', pg('code')],
            ['Strategic, creative leadership', 'One content platform, mapped from the idea to the post.', pg('map')],
            ['Case studies or sample campaigns', 'Three sample campaigns, drawn and planned.', pg('ideas')]]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What you asked for.</h2>
<div class="grow v-center">{table(['You asked', 'Our answer', 'Page'], rows, cls='tbl roomy brief stackable', right=(2,))}</div>
</div>'''
    return slide('brief', 'Your brief', body, src='From your call for a social media agency on LinkedIn, October 2026.')


def ch_today():
    return chapter('ch-today', '01', 'Your social today', 'Where @birlafertility stands, who else is posting, and the new rules.', ('navy', 21))


def audit():
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Where @birlafertility stands.</h2>
  <p class="ink2 lede-s">470+ YouTube videos are a strong library. On Instagram, the audience is split across two accounts.</p>
</div>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat('35K', 'followers on @birlafertility', 'Instagram')}
  {stat('11K', 'on @birlafertility_armcivf', 'a second Instagram audience')}
  {stat('470+', 'videos on YouTube', 'about 10M views')}
  {stat('12K', 'on Facebook', 'the reach beyond the metros')}
  {stat('50+', 'centres, each with a city to talk to', 'English, Hindi and regional languages')}
  {stat('391K', 'on Instagram for Indira IVF', 'the category’s largest audience')}
</div></div>'''
    return slide('audit', 'Your social today · the audit', body,
                 src='Public profiles, October 2026. Counts are approximate. Full list at the end.')


RIVALS = [  # brand, what we see on social
    ('Indira IVF', '165+ centres, about 390K on Instagram, and a 2025 feature film, Tumko Meri Kasam.'),
    ('Nova IVF Fertility', 'Doctor-led myth-busting, run as a YouTube creator series.'),
    ('Cloudnine Fertility', '“Every Fertility Journey is Different” for World IVF Day 2026, male factor included.'),
    ('Ferty9', '#TogetherInIVF: street plays and creators across Andhra Pradesh and Telangana.'),
    ('Motherhood', 'Patient gratitude stories, a format the October 2026 NMC notice now restricts.'),
    ('Birla Fertility &amp; IVF', '470+ YouTube videos that bust myths, and Fertility Circle, a free counselling line.'),
]


def rivals():
    rows = [[f'<b>{n}</b>', w] for n, w in RIVALS]
    body = f'''<div class="stack-l grow">
<h2 class="h1">The category on social.</h2>
<div class="grow v-center">{table(['Brand', 'What we see on social'], rows, cls='tbl rivals stackable')}</div>
</div>'''
    return slide('rivals', 'Your social today · the category', body,
                 src='Sources: trade press and public profiles, 2025 to 2026. Follower counts are approximate. Full list at the end.')


LAW = [  # rule, what it means on social
    ('NMC public notice, 6 October 2026', 'No testimonials or patient success stories, no “best” or guaranteed outcomes, no AI-made '
     'patients, no pay linked to referrals.'),
    ('ASCI', 'IVF success-rate and “best” claims have been upheld as misleading. Creators giving health advice state their qualifications.'),
    ('ART Act, Surrogacy Act, PCPNDT Act', 'Nothing that suggests sex selection or commercial surrogacy, on any channel.'),
    ('Drugs and Magic Remedies Act, 1954', 'Its schedule lists sterility in women, so no line reads as a cure or remedy claim.'),
    ('DPDP Act and Meta ad policy', 'Explicit consent before patient data touches marketing. Ads never imply a viewer’s health.'),
]


def law():
    rows = [[f'<b>{r}</b>', m] for r, m in LAW]
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">On 6 October, the rules changed.</h2>
  <p class="ink2 lede-s">We plan inside them from day one. Your legal team signs the final checklist.</p>
</div>
<div class="grow v-center">{table(['Rule', 'What it means on social'], rows, cls='tbl roomy stackable')}</div>
</div>'''
    return slide('law', 'Your social today · the rules', body,
                 src='Sources: NMC notice as reported by The South First and BestMediaInfo; ASCI; India Code; Meta. Full list at the end.')


def rule():
    feeds = ['Success-rate banners', 'Stock babies and bumps', 'Patient testimonials', 'Offer and EMI carousels',
             'Festive “good news” greetings']
    ours = ['The question people are scared to ask', 'A named specialist, in daylight', 'Men, spoken to directly',
            'The family, invited in kindly', 'The science, shown with care']
    body = f'''<div class="stack-l grow">
<h2 class="h1">If it adds pressure, we don’t post it.</h2>
<div class="row c2 grow vc">
  <div class="rule stack"><p class="label mute">What fertility feeds post</p>{ul(feeds, 'list big-list')}</div>
  <div class="rule-plan stack"><p class="label">What Birla Fertility &amp; IVF posts</p>{ul(ours, 'list big-list')}</div>
</div></div>'''
    return slide('rule', 'The house rule', body, src='Our read of fertility feeds in India, October 2026.')


def insight():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">The first question gets typed at <u>1 a.m.</u>, alone.</h2>
</div>
<div class="terms">
  <div><span class="no label">90%+</span><p class="h3">Exhausted</p><p class="mt-s ink2">Over 90% feel emotionally exhausted.</p></div>
  <div><span class="no label">29%</span><p class="h3">Unasked</p><p class="mt-s ink2">Only 29% seek timely help.</p></div>
  <div><span class="no label">1 a.m.</span><p class="h3">Alone</p><p class="mt-s ink2">A phone at night is where the first question gets typed.</p></div>
</div>'''
    return slide('insight', 'The insight', body, src='Source: Birla Fertility &amp; IVF study, Fertility Circle launch, June 2025.')


def ch_idea():
    return chapter('ch-idea', '02', 'No question too quiet.',
                   'The content: four pillars, twelve series and three campaigns. All heart, all science.', ('blush', 12))


def mapslide():
    mob = ''.join(f'<div class="rule mt-s"><p class="h4">{n} · {sh}</p>'
                  + ul([f'{t}<br><span class="mute f-s">{f}</span>' for t, f in lv]) + '</div>' for n, sh, _, _, lv in art.MAP)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">The content, mapped.</h2>
  <p class="ink2 lede-s">Four pillars, twelve series, one platform. Each share is that pillar’s part of the feed.</p>
</div>
<div class="art grow m-hide">{art.mindmap()}</div>
<div class="m-only">{mob}</div>
</div>'''
    return slide('map', 'The content · the map', body,
                 src='Series names, formats and the mix are Mask360’s proposal, confirmed after the month-one audit.')


PLATFORMS = [  # platform, its job, rhythm, formats
    ('Instagram', 'Home of the questions', '5 posts a week, stories daily', 'Reels · carousels · Lives · highlights'),
    ('YouTube', 'Answers people search for', '3 Shorts a week, 2 long answers a month', 'Shorts · explainers · the lab'),
    ('Facebook', 'Reach beyond the metros', 'Mirrored, regional language first', 'Reels · Lives in Hindi'),
    ('LinkedIn', 'The science and the people', '2 posts a week', 'Specialists · research · careers'),
    ('WhatsApp channel', 'Cards made to forward', 'Weekly', 'Cards · the Fertility Circle line'),
]


def platforms():
    cells = ''.join(f'<div><span class="dot label">{p}</span><p class="h3">{j}</p><p class="ink2 mt-s">{r}</p>'
                    f'<p class="label mute mt-s">{f}</p></div>' for p, j, r, f in PLATFORMS)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Five platforms, five jobs.</h2>
<div class="row c5 flow vc grow">{cells}</div>
</div>'''
    return slide('platforms', 'The content · the platforms', body, src='Rhythms are Mask360’s proposal, set against your team’s review capacity.')


GRID = [  # format, post, cloth (kind, seed, dark text)
    ('Reel', 'Is it normal it’s taking this long?', ('navy', 61, False)),
    ('Carousel', 'Myth or fact: five things people say about IVF', ('petal', 62, True)),
    ('Reel', 'Inside the embryology lab', ('blush', 63, True)),
    ('Carousel', 'Your first visit, step by step', ('petal', 64, True)),
    ('Reel', 'Can he get tested too?', ('navy', 65, False)),
    ('Sticker drop', 'Ask me about my trip to Goa', ('blush', 66, True)),
    ('Reel', 'What does AMH tell me?', ('navy', 67, False)),
    ('Carousel', 'A cycle, explained in six frames', ('petal', 68, True)),
    ('Live', 'Ask a specialist, Thursday 8 p.m.', ('blush', 69, True)),
]
HIGHLIGHTS = ['1 a.m.', 'For him', 'First visit', 'The lab', 'Circle']


def grid():
    tiles = ''.join(tile(k, sd, f, t, dark_text=d) for f, t, (k, sd, d) in GRID)
    hl = ''.join(f'<span><i></i>{h}</span>' for h in HIGHLIGHTS)
    av = '<i class="cmark" aria-hidden="true"></i>' if MARK else ''
    phone = f'''<div class="ig" role="img" aria-label="Mock-up of the @birlafertility Instagram profile and grid in month one">
  <div class="ig-top"><div class="ig-av">{av}</div><div><p class="ig-h">birlafertility</p>
    <p class="ig-bio">All Heart. All Science. No question too quiet.<br>Fertility Circle · 1800 123 1515</p></div></div>
  <div class="ig-hl">{hl}</div>
  <div class="ig-grid">{tiles}</div>
</div>'''
    body = f'''<div class="row c-6-6 grow">
<div class="stack-l" style="justify-content:space-between">
  <h2 class="h1">The grid, month one.</h2>
  <div class="stack-l">
    <p class="lede">The questions lead the grid. The highlights keep the answers people come back for.</p>
    {ul(['Reels for the questions, carousels for the explainers', 'Highlights: 1 a.m., For him, First visit, The lab, Circle',
         'The bio links to Fertility Circle and WhatsApp', 'Every comment answered within two hours'], 'list big-list')}
  </div>
</div>
{phone}
</div>'''
    return slide('grid', 'The content · the grid', body, src='Mock-up. Post titles are samples; every answer is written with your specialists.')


WEEK = [  # date, day, format, the post, time, cloth (kind, seed)
    ('14', 'Mon', 'Reel', 'The 1 a.m. Questions: “Is it normal that it’s taking this long?”', '10 p.m.', ('navy', 71)),
    ('15', 'Tue', 'Carousel', 'Myth or fact: five things people say about IVF.', '1 p.m.', ('blush', 72)),
    ('16', 'Wed', 'Stories', 'The counsellor’s hour: a question box, answered that night.', '9 p.m.', ('navy', 73)),
    ('17', 'Thu', 'Reel', 'Inside the lab: an embryologist’s first hour.', '7 p.m.', ('blush', 74)),
    ('18', 'Fri', 'Carousel', 'Your first visit, step by step.', '1 p.m.', ('navy', 75)),
    ('19', 'Sat', 'Sticker drop', 'The Good News Question, before the wedding weekend.', '11 a.m.', ('blush', 76)),
    ('20', 'Sun', 'Quiet day', 'No new post. Replies only.', 'All day', ('petal', 77)),
]


def week():
    cols = ''.join(f'''<div class="m{' quiet' if f == 'Quiet day' else ''}{' lt' if k in ('blush', 'petal') else ''}"><div class="sw">{fab(k, sd)}<span class="mn">{d}<small>{day}</small></span></div>
<p class="ev"><b>{f}</b>{w}</p><p class="rs">{t}</p></div>''' for d, day, f, w, t, (k, sd) in WEEK)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">A week on @birlafertility.</h2>
  <p class="ink2 lede-s">The first live week, 14 to 20 December. Comments and DMs are answered every day.</p>
</div>
<div class="months grow" style="grid-template-columns:repeat(7,minmax(0,1fr))">{cols}</div>
<div class="rule-plan"><p class="f-l">A month: 12 Reels · 8 carousels · 4 drops · stories daily · 1 Live · 2 long YouTube answers.</p></div>
</div>'''
    return slide('week', 'The content · a sample week', body, src='Posting times follow when the questions come in, and move with the audit.')


IDEAS = [  # title, line, when, cloth (kind, seed, dark text)
    ('The 1 a.m. Questions', 'Real questions, answered in daylight by your specialists.', 'Always on', ('navy', 41, False)),
    ('Half the Story', 'Men’s fertility, spoken to men directly.', 'Pilot from January', ('blush', 42, True)),
    ('The Good News Question', 'A kind way out of the season’s hardest question.', 'Wedding season', ('petal', 43, True)),
]


def ideas():
    cols = ''.join(f'''<div class="idea">{tile(k, sd, f"No. {i + 1:02d}", t, dark_text=d)}<p class="idea-d">{line}</p>
<div class="rule"><p class="label mute">{w}</p></div></div>''' for i, (t, line, w, (k, sd, d)) in enumerate(IDEAS))
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Three sample campaigns.</h2>
  <p class="ink2 lede-s">Each one answers a question people keep to themselves.</p>
</div>
<div class="row c3 grow vc">{cols}</div>
</div>'''
    return slide('ideas', 'The idea · three campaigns', body, src='Sample campaigns are Mask360’s proposal.')


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


def asked():
    return _idea_page('asked', 'No. 01', 'The 1 a.m. Questions', art.night(), 'Asked at night. Answered in daylight.',
                      'An always-on series. Questions come from comments, DMs, search and your front desks. A named specialist '
                      'answers one per post, in under a minute, filmed in daylight.',
                      ['One question per post', 'A named specialist', 'English, Hindi, regional', 'Cards for WhatsApp'],
                      'Concept drawing. Every answer passes your medical review before it posts.')


QUESTIONS = [  # no, question, format, cloth (kind, seed, dark text)
    ('Q. 01', 'Is it normal that it’s taking us more than a year?', 'Reel, 45 seconds', ('petal', 51, True)),
    ('Q. 02', 'Can he get tested too?', 'Reel with a male fertility specialist', ('navy', 52, False)),
    ('Q. 03', 'What does my AMH number actually tell me?', 'Carousel, six frames', ('blush', 53, True)),
    ('Q. 04', 'Is IVF our only option?', 'Instagram Live, monthly', ('navy', 54, False)),
]


def feed():
    cols = ''.join(f'''<div class="idea">{tile(k, sd, n, q, dark_text=d)}
<div class="rule"><p class="label mute">{fmt}</p></div></div>''' for n, q, fmt, (k, sd, d) in QUESTIONS)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Month one, in the feed.</h2>
  <p class="ink2 lede-s">One question, a named specialist and a review stamp on every post.</p>
</div>
<div class="row c4 grow vc qs">{cols}</div>
</div>'''
    return slide('feed', 'The idea · The 1 a.m. Questions', body,
                 src='Mock covers. Answers are written with your specialists and approved before the shoot.')


def half():
    return _idea_page('half', 'No. 02', 'Half the Story', art.chairs(), 'Up to half the cases involve him. Half the story is his.',
                      'Fertility is still spoken of as her journey. This campaign speaks to men directly, in their language. '
                      'Men’s health creators ask the questions, and a male fertility specialist answers them.',
                      ['Creators ask, doctors answer', 'A men-only Live', 'A short film', 'A pilot in two cities'],
                      'Concept drawing. Male factors in 40 to 50% of cases: Indian Society of Assisted Reproduction.')


def goodnews():
    return _idea_page('goodnews', 'No. 03', 'The Good News Question', art.group(), '“Good news kab?” A kinder answer.',
                      'The question comes up at every wedding and festival, and for a couple who is trying it lands in front of '
                      'everyone. Warm, funny “Ask me about…” stickers and cards let them change the subject. A short film shows a '
                      'favourite aunt learning a new question.',
                      ['Sticker packs', 'Cards for the family group', 'A short film', 'A counsellor-led Live'],
                      'Concept drawing. Runs through the wedding season, December to February.')


VOICES = [  # who, what they do, where
    ('Your specialists', 'Named, filmed in daylight, one question each.', 'Reels · Lives · YouTube'),
    ('Your counsellors', 'The question box at night, and words for hard days.', 'Stories · WhatsApp cards'),
    ('Men’s health creators', 'They ask the questions men keep to themselves.', 'Half the Story'),
    ('Family and wedding creators', 'They carry the sticker drop into the season.', 'The Good News Question'),
]


def voices():
    cells = ''.join(f'<div class="rule-plan"><p class="h3">{w}</p><p class="ink2 mt-s">{d}</p><p class="label mute mt-s">{p}</p></div>'
                    for w, d, p in VOICES)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Who speaks on the feed.</h2>
<div class="row c4 grow vc">{cells}</div>
<p class="lede">Creators are paid a flat fee, disclose every partnership and never give medical advice. Your specialists answer.</p>
</div>'''
    return slide('voices', 'The content · the voices', body, src='In line with ASCI’s influencer guidelines and the October 2026 NMC notice.')


def ch_run():
    return chapter('ch-run', '03', 'How it runs', 'The code, the care, the first 90 days and what we report.', ('navy', 23))


CODE = [  # title, line
    ('Every claim is checked', 'Medical lines come from a named specialist and pass medical review before anything posts.'),
    ('Hope, told honestly', 'No guarantees, no success-rate headlines, no “best”, no miracle words.'),
    ('Both partners, always', 'We name factors and never blame a partner. Men’s fertility gets equal airtime.'),
    ('Every path counts', 'Content speaks to people still trying, freezing eggs, or still deciding.'),
    ('Testimonials stay out', 'No patient success stories or testimonials, in line with the October 2026 NMC notice.'),
    ('Hard days, planned for', 'Mother’s Day, baby showers and festive “good news” moments get a quieter calendar.'),
    ('Real, calm imagery', 'Real rooms, real hands, warm light. No AI-made patients, voices or before-and-after images.'),
    ('Words that comfort', 'We retire “failed”, “barren” and “infertile woman”, and write the way a good counsellor talks.'),
]


def code():
    cells = ''.join(f'<div class="rule"><span class="label mute">{i + 1:02d}</span><p class="h4 mt-s">{t}</p>'
                    f'<p class="f-s ink2 mt-s">{d}</p></div>' for i, (t, d) in enumerate(CODE))
    body = f'''<div class="stack-l grow">
<h2 class="h1">Eight rules we sign in week one.</h2>
<div class="row c4 grow vc">{cells}</div>
</div>'''
    return slide('code', 'How it runs · the sensitivity code', body,
                 src='A draft for your medical, legal and counselling teams to edit and sign.')


def care():
    rows = [['Within 1 hour', 'Every DM gets a human reply, 9 a.m. to 10 p.m., seven days.'],
            ['Within 2 hours', 'Every comment is answered, or hidden and logged when it shames or misleads.'],
            ['Within 15 minutes', 'Any sign of crisis goes to a trained counsellor. The reply shares Tele-MANAS, 14416.'],
            ['Always', 'No diagnosis in a DM. Medical questions move to Fertility Circle, 1800 123 1515, with consent.'],
            ['Every week', 'A listening report: new questions, themes, sentiment and risks.']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Every comment is a person on a hard day.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('1', 'hour, at most, for a human reply to any DM', '9 a.m. to 10 p.m., seven days')}</div>
  {table(['When', 'What happens'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('care', 'How it runs · community care', body,
                 src='Service levels are Mask360’s proposal. Our care team trains with your counsellors before launch.')


def days():
    weeks = 13
    phases = [('Listen', 1, 5, 'line', 'Audit, 300 real questions, one voice book'),
              ('Code signed', 4, 5, 'ink', 'The sensitivity code and the review flow'),
              ('Shoot days', 5, 6, 'ink', 'Two days, 24 answers filmed'),
              ('The 1 a.m. Questions', 5, 14, 'plan', 'Live from 14 December, then always on'),
              ('The Good News Question', 6, 12, 'plan', 'The wedding season, December to February'),
              ('Half the Story', 9, 14, 'plan', 'A pilot in two cities'),
              ('Readout', 13, 14, 'ink', 'What moved, in your numbers')]
    head = ''.join(f'<span class="wk label">{i}</span>' for i in range(1, weeks + 1))
    rows = ''.join(f'<p class="h4 ph">{n}</p><i class="bar-{c}" style="grid-column:{s + 1}/{e + 1}"></i><p class="ink2 f-s note">{t}</p>'
                   for n, s, e, c, t in phases)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Nothing posts before your doctors sign the code.</h2>
<div class="gantt vc grow" style="grid-template-columns:calc(var(--u)*11) repeat({weeks},minmax(0,1fr))"><span></span>{head}{rows}</div>
<div class="row c3 dates">
  <div class="rule"><p class="label mute">Set up</p><p class="mt-s">16 November to 13 December</p></div>
  <div class="rule-plan"><p class="label">Live</p><p class="mt-s">14 December to 7 February</p></div>
  <div class="rule"><p class="label mute">Readout</p><p class="mt-s">Week of 8 February 2027</p></div>
</div></div>'''
    return slide('days', 'How it runs · the first 90 days', body,
                 src='Dates assume a start on Monday 16 November 2026. Weeks run Monday to Sunday.')


def measure():
    rows = [['Saves and shares per post', 'Platform reports, weekly'], ['Questions asked', 'Comments and DMs, monthly'],
            ['Care response', 'DMs inside an hour, crisis flags inside 15 minutes'], ['Search views', 'Instagram and YouTube search, monthly'],
            ['Consult enquiries from social', 'WhatsApp and centre codes, with consent']]
    body = f'''<div class="stack-l grow">
<h2 class="h1">Measured in trust, then consults.</h2>
<div class="row c-4-8 grow vc">
  <div class="board" style="grid-template-columns:1fr">{stat('1', 'page a month', 'in the numbers your brand team reports')}</div>
  {table(['What we count', 'How'], rows, cls='tbl roomy stackable')}
</div></div>'''
    return slide('measure', 'How it runs · measurement', body,
                 src='Targets set with your team in month one. Our fee never depends on patient numbers.')


def mask360():
    pillars_ = [('Social', 'Series, creators, community'), ('Content', 'Shoots, reels, edits'), ('Care', 'Comments and DMs, every day'),
                ('Measurement', 'Trust, then consults')]
    p = ''.join(f'<div><p class="h2">{a}</p><p class="ink2 mt-s">{b}</p></div>' for a, b in pillars_)
    body = f'''<div class="stack-l grow" style="justify-content:center">
<div class="row c-7-5" style="align-items:end">
  <div class="m-logo"><svg viewBox="0 0 1632 473" aria-label="m360"><use href="#logo-m"/></svg></div>
  <p class="lede">A creative and content agency in India and the UAE.</p>
</div>
<div class="row c4 pillars mt-m">{p}</div>
<div class="row c2 mt-m">
  <div class="rule"><p class="label mute">In health and wellness</p><p class="mt-s f-l">Swisse Wellness UAE: a 30-reel shoot with Blah Studio, live now.</p></div>
  <div class="rule"><p class="label mute">Brands we have worked with</p><p class="mt-s">Anantara · Atlantis The Royal · St. Regis · Lollapalooza India · Dior · Ferrari · Rolls-Royce · L’Oréal · Dyson · FCUK Beauty · Swisse · Zorae · Rustomjee · Chandak Group</p></div>
</div>
</div>'''
    return slide('mask360', 'Mask360', body, dark=True)


def next_steps():
    body = '''<div class="row c-6-6 grow" style="align-items:end">
<div class="stack-l">
  <h2 class="h-display" style="font-size:calc(var(--u)*5.4)">Start with the questions.</h2>
  <p class="lede">One working session with your specialists. Six draft posts in the room.</p>
</div>
<div class="stack-l">
  <ol class="list steps"><li>Share the questions your front desks hear most.</li><li>Name one specialist and one medical reviewer.</li><li>Agree the code, the scope and the fee.</li><li>First posts live in December.</li></ol>
  <div class="rule-plan"><p class="h3">Kaavish · Mask360</p><p class="ink2 mt-s">mask360.agency</p></div>
</div></div>'''
    return slide('next', 'Next steps', body)


def close():
    body = f'''<div class="grow" style="display:grid;place-items:center">
<div class="close-mark">
  {f'<img class="clogo w" src="{LOGO_REV or LOGO}" alt="{NAME}">' if LOGO else f'<span class="wt" aria-label="{NAME}">{NAME}</span>'}
  <span class="label line">Birla Fertility &amp; IVF × Mask360 · No question too quiet</span>
  {M_MARK}
</div></div>'''
    return slide('close', 'Birla Fertility &amp; IVF × Mask360', body, bare=True, dark=True, cloth=('navy', 11))


def sources():
    items = ''.join(f'<div><p class="h4">{h}</p><p class="f-s ink2 mt-s">{t}</p></div>' for h, t in SOURCES)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Sources.</h2>
<div class="srcs">{items}</div>
</div>'''
    return slide('sources', 'Appendix · sources', body, src='Every number in the proposal, with where it came from.')


def slides():
    out = [cover(), promise(), brief(), ch_today(), audit(), rivals(), law(), insight(), ch_idea(), mapslide(), platforms(), grid(),
           week(), rule(), ideas(), asked(), feed(), half(), goodnews(), voices(), ch_run(), code(), care(), days(), measure(),
           mask360(), next_steps(), close(), sources()]
    assert [s.split('id="', 1)[1].split('"', 1)[0] for s in out] == ORDER, 'ORDER is out of step with the slides'
    return out
