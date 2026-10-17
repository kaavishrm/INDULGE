"""Slide copy for Mask360's social media proposal to Birla Fertility & IVF. The Westside v4 deck's way of writing: a headline, a
line or two, the numbers, and a one-line source on each slide; the full sources are on the last page. Facts come from
pitches/birla-fertility/README.md, which lists every source. The look is Westside v4's, kept as it is."""
import art
from kit import slide, stat, ul, table, tile, chapter, M_MARK

TITLE = 'Birla Fertility & IVF × Mask360'
DESCRIPTION = ('Mask360’s social media proposal to Birla Fertility &amp; IVF, October 2026: No question too quiet. One platform, three '
               'sample campaigns and a sensitivity code written for the new NMC rules.')

# the slides in deck order; page references on the slides are looked up here
ORDER = ['cover', 'promise', 'brief', 'ch-today', 'today', 'rivals', 'law', 'rule', 'insight', 'ch-idea', 'pillars', 'ideas',
         'asked', 'feed', 'half', 'goodnews', 'ch-run', 'code', 'care', 'days', 'path', 'measure', 'mask360', 'next', 'close', 'sources']


def pg(sid):
    return f'{ORDER.index(sid) + 1:02d}'


# full sources, shown on the last page; each slide carries a short version
SOURCES = [
    ('The numbers', 'About 17.5% of adults, roughly 1 in 6, experience infertility in their lifetime: World Health Organization, 2023. '
     'Male factors in 40 to 50% of cases in India: Indian Society of Assisted Reproduction, via BioSpectrum India. Over 90% of people '
     'facing fertility problems feel emotionally exhausted and 29% seek timely help: Birla Fertility &amp; IVF study, released with '
     'Fertility Circle, June 2025 (MediaBrief). About 200,000 to 250,000 IVF cycles a year in India, expected to reach 400,000 by 2030: '
     'Business Standard, June 2025.'),
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
<div class="big-wm" aria-label="Birla Fertility &amp; IVF"><span class="t" aria-hidden="true">Birla Fertility &amp; IVF</span></div>
<div class="cover-foot">
  <div class="stack-l">
    <span class="label">A social media proposal from Mask360 · October 2026</span>
    <h1 class="h-display" style="max-width:11em">No question too quiet.</h1>
  </div>
  {M_MARK}
</div></div>'''
    return slide('cover', 'Proposal', body, src='For the brand team at Birla Fertility &amp; IVF · Confidential', bare=True, dark=True,
                 cls='cover scrim', cloth=('midnight', 7))


def promise():
    body = '''<div class="stack-l grow" style="justify-content:center">
<h2 class="q">We will make Birla Fertility &amp; IVF the place India <u>asks first</u>.</h2>
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
            ['Strategic, creative leadership', 'One platform for all of your social, with three campaigns on it.', pg('ch-idea')],
            ['Case studies or sample campaigns', 'Three sample campaigns, drawn and planned.', pg('ideas')]]
    body = f'''<div class="stack-l grow">
<h2 class="h1">What you asked for.</h2>
<div class="grow v-center">{table(['You asked', 'Our answer', 'Page'], rows, cls='tbl roomy brief stackable', right=(2,))}</div>
</div>'''
    return slide('brief', 'Your brief', body, src='From your call for a social media agency on LinkedIn, October 2026.')


def ch_today():
    return chapter('ch-today', '01', 'The category today', 'Exhausted, unasked, and newly regulated.', ('kohl', 21))


def today():
    body = f'''<div class="stack-l grow">
<h2 class="h1">People are exhausted. Most still don’t ask.</h2>
<div class="board grow" style="align-content:center;align-self:stretch">
  {stat('1 in 6', 'adults experience infertility in their lifetime', 'WHO, 2023')}
  {stat('40 to 50%', 'of cases in India involve male factors', 'Indian Society of Assisted Reproduction')}
  {stat('90%+', 'feel emotionally exhausted by fertility problems', 'Birla Fertility &amp; IVF study, 2025')}
  {stat('29%', 'seek timely help', 'the same study')}
  {stat('50+', 'Birla Fertility &amp; IVF centres in India', '120+ experts')}
  {stat('400K', 'IVF cycles a year in India expected by 2030', 'about 200K to 250K today')}
</div></div>'''
    return slide('today', 'The category today', body,
                 src='Sources: WHO; ISAR; Birla Fertility &amp; IVF Fertility Circle study, June 2025; Business Standard, June 2025. Full list at the end.')


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
    return slide('rivals', 'The category today · on social', body,
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
    return slide('law', 'The category today · the rules', body,
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
                   'Birla Fertility &amp; IVF becomes the place India asks first. All heart, all science.', ('rani', 12))


PILLARS = [  # no, name, cloth (kind, seed, dark text), line, where it runs
    ('No. 01', 'Answer', ('ivory', 31, True), 'The 1 a.m. Questions, myth checks and plain explainers.', 'Reels · Shorts · search'),
    ('No. 02', 'Reassure', ('bone', 32, True), 'What a first visit, a counsellor and a cycle look like.', 'Carousels · Lives · WhatsApp'),
    ('No. 03', 'The science', ('slate', 33, False), 'Labs, embryologists and doctors, shown with care.', 'YouTube · LinkedIn · Reels'),
    ('No. 04', 'Belong', ('rani', 34, False), 'Campaigns, counsellor voices and the community’s own questions.', 'Instagram · Facebook · creators'),
]


def pillars():
    cols = ''.join(f'''<div class="idea">{tile(c[0], c[1], n, t, dark_text=c[2])}<p class="idea-d">{d}</p>
<div class="rule"><p class="label mute">{w}</p></div></div>''' for n, t, c, d, w in PILLARS)
    body = f'''<div class="stack-l grow">
<div class="row c-7-5 top">
  <h2 class="h1">Four pillars, one promise.</h2>
  <p class="ink2 lede-s">English and Hindi on every core post, plus the language of each centre’s city.</p>
</div>
<div class="row c4 grow vc">{cols}</div>
</div>'''
    return slide('pillars', 'The idea · four pillars', body, src='The mix and channels are Mask360’s proposal, confirmed after the month-one audit.')


IDEAS = [  # title, line, when, cloth (kind, seed, dark text)
    ('The 1 a.m. Questions', 'Real questions, answered in daylight by your specialists.', 'Always on', ('midnight', 41, False)),
    ('Half the Story', 'Men’s fertility, spoken to men directly.', 'Pilot from January', ('indigo', 42, False)),
    ('The Good News Question', 'A kind way out of the season’s hardest question.', 'Wedding season', ('shaadi', 43, False)),
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
    ('Q. 01', 'Is it normal that it’s taking us more than a year?', 'Reel, 45 seconds', ('bone', 51, True)),
    ('Q. 02', 'Can he get tested too?', 'Reel with a male fertility specialist', ('kohl', 52, False)),
    ('Q. 03', 'What does my AMH number actually tell me?', 'Carousel, six frames', ('sand', 53, True)),
    ('Q. 04', 'Is IVF our only option?', 'Instagram Live, monthly', ('midnight', 54, False)),
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


def ch_run():
    return chapter('ch-run', '03', 'How it runs', 'The code, the care, the first 90 days and what we report.', ('indigo', 23))


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


def path():
    steps = [('Found', 'Reels and search, captioned with the words people type.'),
             ('Saved', 'Saves and shares, the first private signal we read.'),
             ('Asked', 'A DM or the Fertility Circle line, answered by a person.'),
             ('Consulted', 'A first visit at a centre, tracked with consent.'),
             ('Supported', 'Counsellors stay close. New questions shape the next post.')]
    cells = ''.join(f'<div><span class="dot label">{i + 1:02d}</span><p class="h3">{a}</p><p class="ink2 mt-s">{b}</p></div>'
                    for i, (a, b) in enumerate(steps))
    body = f'''<div class="stack-l grow">
<h2 class="h1">How a quiet question reaches a consult.</h2>
<div class="row c5 flow vc grow">{cells}</div>
</div>'''
    return slide('path', 'How it runs · question to consult', body, src='No patient data is ever used for ad targeting.')


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
  <span class="wt" aria-label="Birla Fertility &amp; IVF">Birla Fertility &amp; IVF</span>
  <span class="label line">Birla Fertility &amp; IVF × Mask360 · No question too quiet</span>
  {M_MARK}
</div></div>'''
    return slide('close', 'Birla Fertility &amp; IVF × Mask360', body, bare=True, dark=True, cloth=('ink', 11))


def sources():
    items = ''.join(f'<div><p class="h4">{h}</p><p class="f-s ink2 mt-s">{t}</p></div>' for h, t in SOURCES)
    body = f'''<div class="stack-l grow">
<h2 class="h1">Sources.</h2>
<div class="srcs">{items}</div>
</div>'''
    return slide('sources', 'Appendix · sources', body, src='Every number in the proposal, with where it came from.')


def slides():
    out = [cover(), promise(), brief(), ch_today(), today(), rivals(), law(), rule(), insight(), ch_idea(), pillars(), ideas(),
           asked(), feed(), half(), goodnews(), ch_run(), code(), care(), days(), path(), measure(), mask360(), next_steps(), close(),
           sources()]
    assert [s.split('id="', 1)[1].split('"', 1)[0] for s in out] == ORDER, 'ORDER is out of step with the slides'
    return out
